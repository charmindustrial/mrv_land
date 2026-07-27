#!/usr/bin/env python3
"""
audit_attachments.py — STRUCTURAL evidence-attachment gate (all oil types).

Reconciling a value is NOT the same as confirming its required evidence is
attached/linked to the component in Certify. W1 (AECN) passed mass / pyrolysis /
transport on values that reconciled while the Ops Notes was never uploaded to
Certify. This gate makes that impossible to miss again, for every batch type that
runs audit_checklist.py.

Refuses to pass three ways:
  1. `certify.attachment_map` absent  -> FAIL (you cannot skip by not capturing).
  2. No required-evidence matrix for this batch -> FAIL (define it from the real
     batch's components; do NOT guess). A matrix is resolved from, in order:
        a) log['certify']['required_evidence']  (per-batch, built at QA time)
        b) MATRICES[oil_type]                   (registered after validation on a real batch)
  3. Any component missing a required source CATEGORY among its attached files -> FAIL.

`certify.attachment_map` = { "<datapoint/component name>": ["<attached source filename>", ...] }
captured from the Certify Sources tab (each source row lists its linked datapoint).

A matrix = { "<component-name substring>": ["<required category>", ...] }.

Run standalone:  python3 audit_attachments.py <source_reads.json>
Imported by audit_checklist.py so the standard pre-delivery audit enforces it.
"""
import json, re, sys
from pathlib import Path

# Filename patterns per source category (shared across oil types; extend as needed).
CATEGORY_PATTERNS = {
    "scale_ticket": r"Ticket_Rail|Ticket Rail|Scale Ticket|Weigh",
    "bol":          r"[Cc]amion|documents?[ _]?\d{4}-R|Bill of Lading|BOL",
    "ops_notes":    r"Ops Notes|INJ-\d{2}-\d{4}-W",
    "lab":          r"W1 AECN\.pdf|CoA|Certificate of Analysis|SR\d{2}-\d|SGS|CHARM INDUSTRIAL|WODO\.pdf|Aqueous\.pdf",
    "ef_sheet":     r"Standard Emission Factors|GLEC",
    "lca":          r"LCA|Supporting GHG|Bioenergy AE|Cote-Nord",
    "map_or_watco": r"to SOPOR|Railyard to Basco|AECN to Basco|to B6|image \(44\)|Watco|Google Maps|Maps|Routing Map",
    "production_ci":r"Production Period|CI|Production Emissions|PP\d",   # Charm WODO/Aqueous
}

# Validated, real-batch matrices, keyed by oil type. AECN matrix validated on
# INJ-06-2026-W1. Kerry / WODO / Aqueous are intentionally absent — they must be
# defined from their first real batch (via log['certify']['required_evidence'])
# rather than guessed here.
MATRICES = {
    "AECN": {
        "Mass of Injectant":            ["scale_ticket", "ops_notes"],
        "Allocated Bio-Oil Mass":       ["scale_ticket", "bol", "ops_notes"],
        "Carbon Content":               ["lab"],
        "Carbon Intensity - AECN Pyrolysis": ["lca"],
        "Allocated Distance":           ["ops_notes", "map_or_watco"],
        "Distance from":                ["map_or_watco"],
        "Emissions Factor":             ["ef_sheet"],
        "Emission Factors":             ["ef_sheet"],
    },
    # WODO matrix validated on INJ-06-2026-W1 (weekly time-block, tote-based,
    # Production-Period CI folded into one pyrolysis component, flatbed transport).
    # Tote-based: no scale tickets / BOLs. Mass + distance-allocation basis is the
    # Ops Notes (which embeds the WODO Shipments & EE Allocation tab); CI evidenced
    # by Ops Notes per-PP CIs; lab CoA + Ops Notes copy on Carbon Content.
    "WODO": {
        "Mass of Injectant":                 ["ops_notes"],
        "Carbon Content of Bio-oil Injected": ["lab", "ops_notes"],
        "Transported CO to Basco":           ["ops_notes"],
        "WODO Tote - Carbon Intensity":      ["ops_notes"],
        "WODO Tote - Mass":                  ["ops_notes"],
        "Aggregate Distance":                ["ops_notes", "map_or_watco"],
        "Distance from":                     ["map_or_watco"],
        "Emissions Factor":                  ["ef_sheet"],
    },
}


def _cat_present(files, category):
    pat = CATEGORY_PATTERNS.get(category)
    if pat is None:
        return False
    rx = re.compile(pat, re.IGNORECASE)
    return any(rx.search(f) for f in files)


def _resolve_matrix(log):
    cert = log.get("certify") or {}
    if isinstance(cert.get("required_evidence"), dict) and cert["required_evidence"]:
        return cert["required_evidence"], "log.certify.required_evidence"
    oil = (log.get("oil_type") or "").strip().upper()
    if oil in MATRICES:
        return MATRICES[oil], f"MATRICES[{oil}]"
    return None, None


def audit_attachments(log):
    """Return (ok, failures[list[str]])."""
    failures = []
    cert = log.get("certify") or {}
    amap = cert.get("attachment_map")
    if not amap or not isinstance(amap, dict):
        failures.append(
            "certify.attachment_map NOT CAPTURED — cannot verify required evidence is "
            "attached in Certify. Capture each datapoint's linked sources from the Certify "
            "Sources tab into certify.attachment_map, then re-run."
        )
    matrix, _src = _resolve_matrix(log)
    if matrix is None:
        oil = log.get("oil_type") or "?"
        failures.append(
            f"required-evidence matrix NOT DEFINED for oil_type='{oil}'. Build it from THIS "
            "batch's actual components (do not guess) and put it in log.certify.required_evidence "
            "(or register it in audit_attachments.MATRICES after validating on a real batch)."
        )
    if failures:  # cannot proceed to per-component checks without both inputs
        return False, failures

    for comp, required in matrix.items():
        matched = {k: v for k, v in amap.items() if comp.lower() in k.lower()}
        if not matched:
            continue  # component not present on this entry — not this gate's job
        for dp, files in matched.items():
            for cat in required:
                if not _cat_present(files, cat):
                    failures.append(
                        f"{dp}: required '{cat}' evidence NOT attached in Certify "
                        f"(attached: {len(files)} file(s), none matches {cat}). "
                        f"Per the evidence matrix this component requires {required}."
                    )
    return (len(failures) == 0), failures


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("usage: audit_attachments.py <source_reads.json>", file=sys.stderr)
        return 2
    log = json.load(open(Path(argv[0])))
    ok, failures = audit_attachments(log)
    print(f"Attachment audit: {'PASS' if ok else 'FAIL'} ({len(failures)} gap(s)).")
    for f in failures:
        print(f"  - {f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
