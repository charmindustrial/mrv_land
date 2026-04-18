"""BGN Production Bio-Oil Inventory lookups.

Used for SGS tote-tag resolution (Flow B) and Charm Contents sheet population.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from .constants import BGN_PRODUCTION_INVENTORY, INVENTORY_TAB
from .drive_helpers import read_all


def load_inventory(sheets: Any) -> list[dict]:
    """Load the Oil_inventory_data tab. Skips the A1 freshness stamp row."""
    rows = read_all(sheets, BGN_PRODUCTION_INVENTORY, INVENTORY_TAB)
    if len(rows) < 2:
        return []
    # Row 0 is the "Last updated X ago" stamp; row 1 is headers; data starts row 2
    header = rows[1]
    data: list[dict] = []
    for r in rows[2:]:
        padded = r + [""] * (len(header) - len(r))
        data.append({header[i]: padded[i] for i in range(len(header))})
    return data


def find_tote(inventory: list[dict], security_tag: str) -> Optional[dict]:
    """Return the first inventory row matching the given security_tag."""
    tag = str(security_tag).strip()
    for row in inventory:
        if str(row.get("security_tag") or "").strip() == tag:
            return row
    return None


def parse_production_date(row: dict) -> Optional[date]:
    """Parse production_date from an inventory row. Tolerates multiple formats."""
    raw = (row.get("production_date") or "").strip()
    if not raw:
        return None
    for fmt in ("%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def product_to_fraction(product: str) -> Optional[str]:
    """Map inventory product field to SGS fraction suffix (QOWV or WODO)."""
    p = (product or "").strip().lower()
    if p == "aqueous_fraction":
        return "QOWV"
    if p == "wodo":
        return "WODO"
    return None


def calendar_month_pp(d: date) -> str:
    """Return PP label for a post-258 production date, e.g. 'April 2026'."""
    return d.strftime("%B %Y")
