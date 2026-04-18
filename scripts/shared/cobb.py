"""COBB (Basco Injection -- COBB) helpers.

COBB is the primary tracking sheet for injection batches. This module hides the
specific column conventions behind higher-level lookups.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any, Optional

from .constants import BIO_OIL_INJECTION_TRACKER, COBB_TAB, LOADS_TAB
from .drive_helpers import read_all

UID_PATTERN = re.compile(r"^([235K])-([A-Z0-9-]+)$")


def load_cobb(sheets: Any) -> list[dict]:
    """Load COBB rows as dicts keyed by column header.

    Assumes row 1 is headers. Returns list of dicts.
    """
    rows = read_all(sheets, BIO_OIL_INJECTION_TRACKER, COBB_TAB)
    if not rows:
        return []
    header = rows[0]
    result: list[dict] = []
    for r in rows[1:]:
        padded = r + [""] * (len(header) - len(r))
        result.append({header[i]: padded[i] for i in range(len(header))})
    return result


def filter_batches_by_rp(
    cobb: list[dict],
    *,
    rp_start: date,
    rp_end: date,
    uid_prefixes: tuple[str, ...] = ("2-", "3-", "5-", "K-"),
    completion_date_col: str = "completion_date",
) -> list[dict]:
    """Return COBB rows whose UID starts with any given prefix AND whose completion
    date is within [rp_start, rp_end]. Tolerant to multiple date formats.
    """
    results: list[dict] = []
    for row in cobb:
        uid = (row.get("uid") or row.get("UID") or "").strip()
        if not any(uid.startswith(p) for p in uid_prefixes):
            continue
        raw = row.get(completion_date_col) or ""
        d = _parse_date(raw)
        if d is None:
            continue
        if rp_start <= d <= rp_end:
            results.append(row)
    return results


def _parse_date(raw: str) -> Optional[date]:
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M"):
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    return None


def detect_rail_or_truck(row: dict) -> str:
    """Return 'rail' or 'truck' based on SO number format."""
    so = (row.get("so_number") or row.get("SO Number") or row.get("sales_order") or "").lower()
    if "rail_" in so or "offload_" in so:
        return "rail"
    return "truck"


def extract_railcar_id(so_number: str) -> Optional[str]:
    """Extract the railcar ID from a SO number like 'Rail_GPRX 5188_2.27.26_offload_3'."""
    if not so_number:
        return None
    parts = so_number.split("_")
    if len(parts) >= 2 and parts[0].lower() == "rail":
        return parts[1].strip()
    return None


def extract_offload_number(so_number: str) -> Optional[int]:
    """Extract 1-4 from 'Rail_XXX_date_offload_N'."""
    if not so_number:
        return None
    m = re.search(r"offload_(\d+)", so_number)
    return int(m.group(1)) if m else None


def find_sibling_offloads(cobb: list[dict], railcar_id: str) -> list[dict]:
    """Return all COBB rows for the same railcar, ordered by offload number."""
    sibs = []
    for row in cobb:
        so = row.get("so_number") or row.get("SO Number") or ""
        if extract_railcar_id(so) == railcar_id:
            sibs.append(row)
    sibs.sort(key=lambda r: extract_offload_number(r.get("so_number") or r.get("SO Number") or "") or 99)
    return sibs


def load_loads_tab(sheets: Any) -> list[dict]:
    """Load Loads tab rows as dicts. Used for railcar→BOL lookups."""
    rows = read_all(sheets, BIO_OIL_INJECTION_TRACKER, LOADS_TAB)
    if not rows:
        return []
    header = rows[0]
    return [
        {header[i]: (r + [""] * (len(header) - len(r)))[i] for i in range(len(header))}
        for r in rows[1:]
    ]


def find_railcar_bols(loads: list[dict], railcar_id: str) -> Optional[dict]:
    """Find the railcar row and extract BOLs + total mass (MT)."""
    needle = (railcar_id or "").replace(" ", "").lower()
    for row in loads:
        rc = (row.get("ID") or row.get("id") or "").replace(" ", "").lower()
        if rc == needle:
            return {
                "railcar_id": railcar_id,
                "bols": [
                    row.get("BOL"), row.get("BOL_2"), row.get("BOL_3"),
                ],
                "total_mt": _to_float(row.get("Actual Loaded (metric tons)")),
            }
    return None


def _to_float(v: Any) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", ""))
    except (ValueError, TypeError):
        return None
