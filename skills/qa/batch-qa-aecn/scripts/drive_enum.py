#!/usr/bin/env python3
"""
Drive folder enumeration helper for batch QA workflows.

Reads a Playwright accessibility-snapshot YAML file and extracts every Google
Drive row visible in the snapshot. Returns a list of dicts:

    [
      {"name": "SR26-02231_Batch_2-180-185_COA (1).pdf",
       "type": "PDF",
       "owner": "Garrett Lutz",
       "modified": "Apr 23",
       "size_human": "51 KB",
       "raw_aria_label": "..."},
      ...
    ]

Why this exists: ad-hoc JavaScript selectors against Drive's live DOM (e.g.
`document.querySelectorAll('[data-id][role="row"]')`) silently miss rows when
Drive's rendering pipeline varies between folder types or when lazy-load
timing hasn't completed. The snapshot YAML is captured by Playwright after
the page is fully rendered and reflects exactly what a human user sees — it
is the renderer's output, not a filter over it.

For batch QA, every Drive enumeration MUST use this helper. Never run a
narrow JS query and trust the count. The lesson from batch 2-181 (1.3 false
"folder empty" finding) is the canonical case.

Usage:
    from drive_enum import enumerate_from_snapshot
    rows = enumerate_from_snapshot('outputs/qa/batch-2-181/drive_testing_snap.yml')
    if not rows:
        # GENUINELY empty — verified by absence of any row in the snapshot
        ...
    else:
        for row in rows:
            ...

CLI:
    python drive_enum.py <snapshot.yml>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

# Drive snapshot YAML rows look like this (one line per row, possibly wrapped):
#   - 'row "SR26-02231_Batch_2-180-185_COA (1).pdf PDF Shared Owned by Garrett
#       Lutz Modified Apr 23 Garrett Lutz Size: 51 KB Storage used: 51 KB
#       More actions (Alt+A)" [ref=e587]':
#
# The leading `- 'row "..."'` is the YAML marker. We extract everything inside
# the outer double-quoted string and parse fields out of the aria-label-like
# concatenation Drive renders.
ROW_LINE_RE = re.compile(r"""['"]?row\s+\\?["']([^"']+?)\\?["']\s*\[ref=""")

# Field extractors from the row's aria label. Drive concatenates everything
# into one string in a stable order: <name> <type> <ownership> Owned by <owner>
# Modified <date> <owner-repeat> Size: <size> Storage used: <size> More actions
TYPE_TOKENS = ("PDF", "Document", "Spreadsheet", "Presentation",
               "Image", "Video", "Audio", "Folder", "Shared folder",
               "Google Sheets", "Google Doc", "Google Slides")


def _parse_row(aria: str) -> dict[str, Any]:
    """Parse a single Drive row aria label into structured fields."""
    out: dict[str, Any] = {"raw_aria_label": aria}

    # Owner
    m = re.search(r"Owned by ([^\d]+?)(?:\s+Modified|\s+Size:|$)", aria)
    if m:
        out["owner"] = m.group(1).strip()

    # Modified date
    m = re.search(r"Modified ([A-Z][a-z]+ \d{1,2}(?:, \d{4})?)", aria)
    if m:
        out["modified"] = m.group(1).strip()

    # Size
    m = re.search(r"Size:\s*([\d.]+\s*(?:K|M|G|T)?B)", aria)
    if m:
        out["size_human"] = m.group(1).strip()

    # Type token — find the first known type in the string
    for t in TYPE_TOKENS:
        if f" {t} " in aria or aria.endswith(f" {t}"):
            out["type"] = t
            break

    # Name — everything before the type token (or before " Shared ")
    name_end = len(aria)
    for marker in (" PDF ", " Document ", " Spreadsheet ", " Image ",
                   " Folder ", " Shared folder ", " Google Sheets ",
                   " Google Doc ", " Google Slides ", " Shared "):
        idx = aria.find(marker)
        if idx > 0 and idx < name_end:
            name_end = idx
    out["name"] = aria[:name_end].strip()

    return out


def enumerate_from_snapshot(snapshot_path: str | Path) -> list[dict[str, Any]]:
    """
    Parse a Playwright accessibility snapshot YAML and return every Drive row
    visible in it. Returns [] only if the snapshot genuinely contains no rows.

    The returned list is the authoritative folder enumeration. Callers MUST
    NOT use ad-hoc DOM queries against the live page; the snapshot is the
    rendered-output source of truth.
    """
    path = Path(snapshot_path)
    if not path.exists():
        raise FileNotFoundError(f"Snapshot file not found: {path}")
    content = path.read_text(errors="replace")

    rows: list[dict[str, Any]] = []
    for line in content.splitlines():
        # Strip leading whitespace + YAML list marker for matching
        stripped = line.lstrip()
        if not stripped.startswith("-"):
            continue
        # Skip rows that are clearly navigation/breadcrumb (no Size/Modified/Owned)
        if 'row "' not in stripped and "row '" not in stripped:
            continue
        m = ROW_LINE_RE.search(stripped)
        if not m:
            # Try a looser match without the trailing [ref=...] constraint
            m2 = re.search(r"""row\s+["']([^"']+?)["']""", stripped)
            if not m2:
                continue
            aria = m2.group(1)
        else:
            aria = m.group(1)
        # Filter out rows that are just column-header descriptions
        if aria.lower().startswith(("name ", "type ", "owner ", "last modified")):
            continue
        # Require at least one file-row indicator to count as a real entry
        if not any(marker in aria for marker in
                   (" Size:", " Owned by ", " Modified ",
                    " Shared folder", " Folder ", "PDF", "Document",
                    "Spreadsheet", "Google Sheets")):
            continue
        rows.append(_parse_row(aria))

    return rows


def _cli() -> int:
    if len(sys.argv) != 2:
        print("Usage: drive_enum.py <snapshot.yml>", file=sys.stderr)
        return 1
    rows = enumerate_from_snapshot(sys.argv[1])
    if not rows:
        print("(no Drive rows parsed from snapshot — folder may be genuinely empty, "
              "OR snapshot was taken before render completed; verify manually)")
        return 0
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
