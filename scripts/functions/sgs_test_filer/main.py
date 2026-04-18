"""sgs-test-filer Cloud Function.

Entry point: sgs_test_filer(request) — triggered by Cloud Scheduler via HTTP.

Flow:
  1. Search Gmail for recent SGS Certificate of Analysis emails (last 2 days)
  2. Download PDF attachments
  3. Parse each PDF via Claude API → per-sample data
  4. Classify sample:
       - CLIENT ID 'BATCH X-XX' → Flow A: file into batch Testing/ folder
       - 6-digit tote tag → Flow B: file into PP Miniforge Pyrolysis Output Testing/
  5. Upload PDFs (idempotent — skip if same md5 already there)
  6. Log structured summary
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import date, datetime
from typing import Any

# Add /workspace for local dev; Cloud Functions handles packaging automatically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.auth import get_drive_services, get_gmail_service
from shared.claude_parser import parse_sgs_coa_pdf
from shared.constants import (
    INVOICES_TRACKING_DOCS_ROOT,
    REMOVALS_REPORTING_ROOT,
    SGS_SENDER_QUERIES,
    TEMP_DIR,
)
from shared.drive_helpers import (
    ensure_folder,
    file_exists_in_folder,
    find_child_folder,
    list_folder,
    upload_file_to_folder,
)
from shared.gmail_helpers import list_pdfs_in_recent_threads
from shared.inventory import (
    calendar_month_pp,
    find_tote,
    load_inventory,
    parse_production_date,
    product_to_fraction,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


# ----- Cloud Function entry point -----

def sgs_test_filer(request) -> tuple[str, int]:
    """HTTP-triggered Cloud Function entry point.

    Returns a JSON response body with the run summary.
    """
    summary = run()
    return json.dumps(summary, default=str), 200


def run() -> dict:
    """Main orchestration. Returns a summary dict for logging / response."""
    log.info("sgs_test_filer starting run")
    drive_svc = get_drive_services()
    drive = drive_svc["drive"]
    sheets = drive_svc["sheets"]
    gmail = get_gmail_service()

    # 1. Search Gmail for SGS PDFs
    pdfs = list_pdfs_in_recent_threads(
        gmail, SGS_SENDER_QUERIES, download_dir=f"{TEMP_DIR}/sgs"
    )
    log.info("gmail search returned %d PDFs", len(pdfs))

    if not pdfs:
        return {"pdfs_found": 0, "samples_parsed": 0, "filed": 0, "flags": []}

    # 2. Load inventory once (for Flow B tote → product date lookup)
    inventory = load_inventory(sheets)

    # 3. Find current RP batch folder tree (for Flow A)
    current_rp_folder = _find_current_rp_folder(drive)
    injection_batch_data = None
    if current_rp_folder:
        injection_batch_data = find_child_folder(drive, current_rp_folder["id"], "Injection Batch Data")

    # 4. Process each PDF
    filed_count = 0
    samples_parsed = 0
    flags: list[str] = []
    results: list[dict] = []

    for pdf in pdfs:
        try:
            log.info("parsing %s", pdf["filename"])
            samples = parse_sgs_coa_pdf(pdf["local_path"])
        except Exception as e:
            flags.append(f"parse_failed:{pdf['filename']}:{e}")
            log.exception("failed to parse %s", pdf["filename"])
            continue

        samples_parsed += len(samples)
        destinations_used: set[str] = set()

        for sample in samples:
            dest_folder_id = _resolve_destination(
                sample=sample,
                drive=drive,
                inventory=inventory,
                injection_batch_data=injection_batch_data,
                flags=flags,
            )
            if not dest_folder_id:
                continue

            # Idempotent upload — skip if same PDF already at destination
            if dest_folder_id in destinations_used:
                continue  # avoid double-upload from multi-sample same PDF
            destinations_used.add(dest_folder_id)

            existing = file_exists_in_folder(
                drive, dest_folder_id, os.path.basename(pdf["local_path"]),
                check_md5_of=pdf["local_path"],
            )
            if existing:
                log.info("already filed: %s in %s", existing["name"], dest_folder_id)
                continue

            uploaded = upload_file_to_folder(
                drive, pdf["local_path"], dest_folder_id,
                name=os.path.basename(pdf["local_path"]).split("_", 1)[-1],  # strip msg_id prefix
            )
            filed_count += 1
            results.append({
                "certificate": sample.get("certificate_number"),
                "client_id": sample.get("client_id"),
                "carbon_pct": sample.get("carbon_pct"),
                "destination_folder": dest_folder_id,
                "uploaded_file": uploaded.get("webViewLink"),
            })

    summary = {
        "pdfs_found": len(pdfs),
        "samples_parsed": samples_parsed,
        "filed": filed_count,
        "results": results,
        "flags": flags,
    }
    log.info("sgs_test_filer done: %s", json.dumps({k: v for k, v in summary.items() if k != "results"}))
    return summary


# ----- Helpers -----

def _resolve_destination(
    *,
    sample: dict,
    drive: Any,
    inventory: list[dict],
    injection_batch_data: dict | None,
    flags: list[str],
) -> str | None:
    """Given a parsed sample, return the destination folder ID to file the PDF into.

    Returns None (and appends a flag) when the sample can't be placed.
    """
    client_id = (sample.get("client_id") or "").strip()
    if not client_id:
        flags.append("empty_client_id")
        return None

    # Flow A: BATCH X-XX format
    m = re.match(r"(?:batch\s+)?([235K])-([A-Z0-9-]+)", client_id, re.IGNORECASE)
    if m and injection_batch_data:
        uid = f"{m.group(1)}-{m.group(2)}"
        batch_folder = _find_batch_folder(drive, injection_batch_data["id"], uid)
        if not batch_folder:
            flags.append(f"batch_folder_missing:{uid}")
            return None
        testing_folder = ensure_folder(drive, batch_folder["id"], "Testing")
        return testing_folder["id"]

    # Flow B: 6-digit tote tag
    tag_match = re.match(r"^(\d{6})\s*(qowv|wodo)?", client_id, re.IGNORECASE)
    if tag_match:
        tag = tag_match.group(1)
        tote = find_tote(inventory, tag)
        if not tote:
            flags.append(f"tote_not_in_inventory:{tag}")
            return None
        prod_date = parse_production_date(tote)
        if not prod_date:
            flags.append(f"no_production_date:{tag}")
            return None
        return _find_or_create_pp_testing_folder(drive, prod_date, flags)

    flags.append(f"unknown_client_id_format:{client_id}")
    return None


def _find_current_rp_folder(drive: Any) -> dict | None:
    """Locate the active RP folder under Removals Reporting / [year] / CURRRENT PERIOD /."""
    year_folder = find_child_folder(drive, REMOVALS_REPORTING_ROOT, str(date.today().year))
    if not year_folder:
        return None
    current_period = find_child_folder(drive, year_folder["id"], "CURRRENT PERIOD")
    if not current_period:
        return None
    # Pick the first RP folder inside CURRRENT PERIOD (should be only one active)
    children = list_folder(drive, current_period["id"],
                           query_extra="mimeType='application/vnd.google-apps.folder'")
    return children[0] if children else None


def _find_batch_folder(drive: Any, injection_batch_data_id: str, uid: str) -> dict | None:
    """Search Injection Batch Data tree for a UID folder.

    Handles nested week folders (2-XXX) and Charm Oil / Kerry Oil parent folders.
    """
    # Try direct children first (flat old-style RP)
    direct = find_child_folder(drive, injection_batch_data_id, uid)
    if direct:
        return direct

    # Search all subfolders (week folders, Charm Oil, Kerry Oil) one level deep
    children = list_folder(drive, injection_batch_data_id,
                           query_extra="mimeType='application/vnd.google-apps.folder'")
    for child in children:
        match = find_child_folder(drive, child["id"], uid)
        if match:
            return match
    return None


def _find_or_create_pp_testing_folder(
    drive: Any, prod_date: date, flags: list[str]
) -> str | None:
    """Resolve/create Invoices + Tracking Docs / Miniforge Pyrolysis Output / [Year] / [Month YY] / Testing/"""
    mpo = find_child_folder(drive, INVOICES_TRACKING_DOCS_ROOT, "Miniforge Pyrolysis Output")
    if not mpo:
        flags.append("miniforge_pyrolysis_output_folder_missing")
        return None
    year_folder = find_child_folder(drive, mpo["id"], str(prod_date.year))
    if not year_folder:
        flags.append(f"pp_year_folder_missing:{prod_date.year}")
        return None
    month_label = prod_date.strftime("%B %y")  # e.g. "March 26"
    month_folder = find_child_folder(drive, year_folder["id"], month_label)
    if not month_folder:
        # Try full 4-digit year variant
        alt = prod_date.strftime("%B %Y")
        month_folder = find_child_folder(drive, year_folder["id"], alt)
    if not month_folder:
        flags.append(f"pp_month_folder_missing:{month_label}")
        return None
    testing_folder = ensure_folder(drive, month_folder["id"], "Testing")
    return testing_folder["id"]


# ----- Local test entry point -----
if __name__ == "__main__":
    print(json.dumps(run(), default=str, indent=2))
