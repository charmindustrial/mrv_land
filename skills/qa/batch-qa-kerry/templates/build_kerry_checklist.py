"""
Kerry Injection Batch QA Checklist Template Builder.

Structured around Max's actual QA question framework for Kerry tote-mode batches
(Max Slack 2026-05-06). When Charm moves Kerry to tankers, this will largely
mirror AECN tanker QA save for the system-boundary difference (no biomass-sourcing
or conversion emissions for Kerry — waste boundary).

Template structure:
  Section 1: Injection Sequestration (7 items)
  Section 2A: Transport Emissions — Process (7 items)
  Section 2B: Transport Emissions — Embodied (4 items)
  Section 2C: BCU vs Process Emissions (1 item)

Out-of-frame side observations (system-boundary checks, density anomalies, etc.)
go in a "Sidebar Observations" section at the end with no Pass/Fail status,
just a flagged-for-attention listing.

Usage:
    Caller passes a `findings` dict mapping item-id → {status, evidence, ref}.
    Builder writes the xlsx to OUT path, applies fail/flag/pass formatting,
    and saves.

This is a TEMPLATE — caller fills in findings per-batch, builder applies
canonical formatting and structure. Do NOT hard-code per-batch values into
this template; that defeats the point of having a template.
"""
from __future__ import annotations

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


# Canonical Kerry tote-mode QA structure (Max's framework)
KERRY_TOTE_STRUCTURE = [
    {
        "section": "Section 1: Injection Sequestration",
        "items": [
            ("1.1", "Does the C content match the weighted average of tote C contents?"),
            ("1.2", "Does the C content have sources that validate all C contents reported?"),
            ("1.3", "Is uncertainty quantified and reported correctly for the C content?"),
            ("1.4", "Does the Mass of Injectate match the 'Total Oil Injected' value in Ops Notes?"),
            ("1.5", "Is the 'Total Oil Injected' value in Ops Notes correctly computed?"),
            ("1.6", "Is the uncertainty quantified and reported correctly for the Mass of Injectate?"),
            ("1.7", "Is the 'Total Oil Injected' value evidenced properly (evidence value confirms reported value)?"),
        ],
    },
    {
        "section": "Section 2A: Transport Emissions (Kerry → Basco) — Process",
        "items": [
            ("2A.1", "Is the emission factor correct and up to date?"),
            ("2A.2", "Is the emission factor evidenced appropriately (evidence value confirms reported value)?"),
            ("2A.3", "Is the correct distance being used for the Kerry origin → Basco route?"),
            ("2A.4", "Is the distance evidenced appropriately (evidence value confirms reported value)?"),
            ("2A.5", "Does the Mass of Load match the 'Total Transported' value in Ops Notes?"),
            ("2A.6", "Is the 'Total Transported' value in Ops Notes computed correctly?"),
            ("2A.7", "Is the uncertainty quantified and reported correctly for the 'Total Transported'?"),
        ],
    },
    {
        "section": "Section 2B: Transport Emissions (Kerry → Basco) — Embodied",
        "items": [
            ("2B.1", "Is the emission factor correct and up to date?"),
            ("2B.2", "Is the emission factor evidenced appropriately (evidence value confirms reported value)?"),
            ("2B.3", "Is the correct distance being used for the Kerry origin → Basco route?"),
            ("2B.4", "Is the distance evidenced appropriately (evidence value confirms reported value)?"),
        ],
    },
    {
        "section": "Section 2C: BCUs vs Transport Process Emissions",
        "items": [
            ("2C.1", "Does the total BCUs applied match the total transport process emissions?"),
        ],
    },
    {
        "section": "Section 3: MRV Parameter Checks (per-tote SGS CoA + Ops Notes)",
        "items": [
            ("3.1", "Are per-tote densities reported and above the formation-fluid injection floor (1.01 g/cm³)? Any within-batch outliers flagged?"),
            ("3.2", "Are per-tote hydrogen contents reported and within expected range?"),
            ("3.3", "Are per-tote nitrogen contents reported and within expected range?"),
            ("3.4", "Are per-tote viscosities reported?"),
            ("3.5", "Are per-tote acid numbers reported?"),
            ("3.6", "Is pH recorded (Ops Notes or COBB) and within expected range for bio-oil?"),
        ],
    },
]


# Tanker-mode variant. Same item IDs and same substance as the tote framework —
# only the wording that presumes multiple totes is restated for a single
# shipment. Kerry moved to flatbed-haul tankers with INJ-07-2026-W4 (first
# tanker batch: one weighing pair, one composite sample, no per-tote ledger).
KERRY_TANKER_STRUCTURE = [
    {
        "section": "Section 1: Injection Sequestration",
        "items": [
            ("1.1", "Does the C content match the lab result for this shipment's composite sample?"),
            ("1.2", "Does the C content have sources that validate the C content reported?"),
            ("1.3", "Is uncertainty quantified and reported correctly for the C content?"),
            ("1.4", "Does the Mass of Injectate match the 'Total Oil Injected' value in Ops Notes?"),
            ("1.5", "Is the 'Total Oil Injected' value in Ops Notes correctly computed?"),
            ("1.6", "Is the uncertainty quantified and reported correctly for the Mass of Injectate?"),
            ("1.7", "Is the 'Total Oil Injected' value evidenced properly (evidence value confirms reported value)?"),
        ],
    },
    KERRY_TOTE_STRUCTURE[1],   # Section 2A — mode-independent
    KERRY_TOTE_STRUCTURE[2],   # Section 2B — mode-independent
    KERRY_TOTE_STRUCTURE[3],   # Section 2C — mode-independent
    {
        "section": "Section 3: MRV Parameter Checks (shipment SGS CoA + Ops Notes)",
        "items": [
            ("3.1", "Is density reported and above the formation-fluid injection floor (1.01 g/cm³)?"),
            ("3.2", "Is hydrogen content reported and within expected range?"),
            ("3.3", "Is nitrogen content reported and within expected range?"),
            ("3.4", "Is viscosity reported?"),
            ("3.5", "Is acid number reported?"),
            ("3.6", "Is pH recorded (Ops Notes or COBB) and within expected range for bio-oil?"),
        ],
    },
]

STRUCTURES = {"tote": KERRY_TOTE_STRUCTURE, "tanker": KERRY_TANKER_STRUCTURE}


# Style helpers
FAIL_FILL = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL = PatternFill("solid", fgColor="FFF2CC")
# One neutral colour for EVERY section / sub-section / sidebar header (SKILL.md
# formatting spec). Never yellow (collides with FLAG), never green, never a
# second tone. Status fills are the only semantic colours on the sheet.
SECTION_FILL = PatternFill("solid", fgColor="D6E4F0")
HEADER_FILL = PatternFill("solid", fgColor="D6E4F0")
SIDEBAR_FILL = PatternFill("solid", fgColor="D6E4F0")
FLAG_FONT = Font(color="996600", bold=False)
NA_FONT = Font(italic=True, color="808080")
SECTION_FONT = Font(bold=True, size=12)
HEADER_FONT = Font(bold=True, size=11)
TITLE_FONT = Font(bold=True, size=14)
THIN = Side(border_style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center")


def _write_title_block(ws, batch_meta: dict) -> int:
    ws["A1"] = "Kerry Injection Batch QA Checklist"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:E1")
    rows = [
        ("Batch ID", batch_meta.get("batch_id", "")),
        ("Reporting Period", batch_meta.get("reporting_period", "")),
        ("Reviewer", batch_meta.get("reviewer", "Claude QA Agent")),
        ("Date", batch_meta.get("date", "")),
        ("Injection Site", batch_meta.get("injection_site", "Basco 6")),
        ("Oil Type", "Kerry"),
        ("Delivery Mode", batch_meta.get("delivery_mode", "Tote")),
        ("Certify Removal", batch_meta.get("certify_removal", "")),
    ]
    for i, (k, v) in enumerate(rows, start=2):
        ws[f"A{i}"] = k
        ws[f"B{i}"] = v
        ws[f"A{i}"].font = HEADER_FONT
        ws.merge_cells(f"B{i}:E{i}")
    return len(rows) + 2


def _section_header(ws, row: int, title: str) -> int:
    ws[f"A{row}"] = title
    ws[f"A{row}"].font = SECTION_FONT
    ws[f"A{row}"].fill = SECTION_FILL
    ws.merge_cells(f"A{row}:E{row}")
    return row + 1


def _col_header(ws, row: int) -> int:
    ws[f"A{row}"] = "Item #"
    ws[f"B{row}"] = "Question"
    ws[f"C{row}"] = "Status"
    ws[f"D{row}"] = "Evidence / Finding"
    ws[f"E{row}"] = "Reference"
    for c in "ABCDE":
        ws[f"{c}{row}"].font = HEADER_FONT
        ws[f"{c}{row}"].fill = HEADER_FILL
        ws[f"{c}{row}"].border = BORDER
        ws[f"{c}{row}"].alignment = CENTER
    return row + 1


def _write_item(ws, row: int, item_id: str, question: str, finding: dict) -> int:
    status = finding.get("status", "")
    evidence = finding.get("evidence", "")
    ref = finding.get("ref", "")
    ws[f"A{row}"] = item_id
    ws[f"B{row}"] = question
    ws[f"C{row}"] = status
    ws[f"D{row}"] = evidence
    ws[f"E{row}"] = ref
    for c in "ABCDE":
        ws[f"{c}{row}"].border = BORDER
        ws[f"{c}{row}"].alignment = WRAP
    if status == "Fail":
        for c in "ABCDE":
            ws[f"{c}{row}"].fill = FAIL_FILL
    elif status == "Flag":
        for c in "ABCDE":
            ws[f"{c}{row}"].fill = FLAG_FILL
            ws[f"{c}{row}"].font = FLAG_FONT
    elif status == "N/A":
        for c in "ABCDE":
            ws[f"{c}{row}"].font = NA_FONT
    ws.row_dimensions[row].height = 60
    return row + 1


def _write_sidebar(ws, row: int, observations: list) -> int:
    if not observations:
        return row
    row += 1
    ws[f"A{row}"] = "Sidebar Observations (out-of-frame, no status)"
    ws[f"A{row}"].font = SECTION_FONT
    ws[f"A{row}"].fill = SIDEBAR_FILL
    ws.merge_cells(f"A{row}:E{row}")
    row += 1
    ws[f"A{row}"] = "#"
    ws[f"B{row}"] = "Observation"
    ws[f"C{row}"] = ""
    ws[f"D{row}"] = "Detail"
    ws[f"E{row}"] = "Reference"
    for c in "ABCDE":
        ws[f"{c}{row}"].font = HEADER_FONT
        ws[f"{c}{row}"].fill = HEADER_FILL
        ws[f"{c}{row}"].border = BORDER
        ws[f"{c}{row}"].alignment = CENTER
    row += 1
    for i, obs in enumerate(observations, start=1):
        ws[f"A{row}"] = f"S.{i}"
        ws[f"B{row}"] = obs.get("title", "")
        ws[f"C{row}"] = ""
        ws[f"D{row}"] = obs.get("detail", "")
        ws[f"E{row}"] = obs.get("ref", "")
        for c in "ABCDE":
            ws[f"{c}{row}"].border = BORDER
            ws[f"{c}{row}"].alignment = WRAP
        ws.row_dimensions[row].height = 50
        row += 1
    return row


def build_kerry_checklist(out_path: str, batch_meta: dict, findings: dict, sidebar: list = None,
                          mode: str = None) -> dict:
    """
    Build a Kerry tote-mode QA checklist xlsx.

    Args:
        out_path: absolute path for output xlsx
        batch_meta: dict with batch_id, reporting_period, date, certify_removal,
                    delivery_mode (default 'Tote'), reviewer, injection_site
        findings: dict mapping item_id (e.g. '1.1', '2A.5', '2C.1') ->
                  {'status': 'Pass'|'Fail'|'Flag'|'N/A', 'evidence': str, 'ref': str}
        sidebar: optional list of {'title', 'detail', 'ref'} for out-of-frame observations

    Returns:
        dict with status counts and item id -> status mapping for caller's records.
    """
    sidebar = sidebar or []
    if mode is None:
        mode = str(batch_meta.get("delivery_mode", "tote")).strip().lower()
    structure = STRUCTURES.get(mode)
    if structure is None:
        raise ValueError(f"unknown delivery mode {mode!r}; expected one of {sorted(STRUCTURES)}")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "QA Checklist"

    for col, w in {"A": 8, "B": 56, "C": 9, "D": 100, "E": 28}.items():
        ws.column_dimensions[col].width = w

    r = _write_title_block(ws, batch_meta)
    r += 1

    counts = {"Pass": 0, "Fail": 0, "Flag": 0, "N/A": 0, "Unfilled": 0}
    item_status = {}

    for section in structure:
        r = _section_header(ws, r, section["section"])
        r = _col_header(ws, r)
        for item_id, question in section["items"]:
            finding = findings.get(item_id, {})
            if not finding:
                finding = {"status": "Unfilled", "evidence": "[No finding provided by caller]", "ref": ""}
            r = _write_item(ws, r, item_id, question, finding)
            status = finding.get("status", "Unfilled")
            counts[status] = counts.get(status, 0) + 1
            item_status[item_id] = status
        r += 1

    r = _write_sidebar(ws, r, sidebar)

    ws.freeze_panes = "A2"
    wb.save(out_path)
    return {"counts": counts, "item_status": item_status, "out_path": out_path}


if __name__ == "__main__":
    import sys
    print("Kerry checklist template — call build_kerry_checklist(out_path, batch_meta, findings, sidebar)")
    print("Structure:")
    for s in KERRY_TOTE_STRUCTURE:
        print(f"  {s['section']}")
        for item_id, q in s["items"]:
            print(f"    {item_id}: {q}")
