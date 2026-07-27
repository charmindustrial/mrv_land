#!/usr/bin/env python3
"""
Deterministic report builder for the Charm 350 bio-oil credit report.

Given the statement period + the list of CHARM-OIL removals already classified by the
skill (the classification itself needs judgment and is done by the agent from the
Certify component names), this writes the .xlsx to the Drive folder and prints the
saved path + total. It does NOT decide inclusion/exclusion and does NOT send anything.

Usage:
    build_report.py '<json payload>'

Payload shape:
{
  "statement_id": "ggs_...",
  "period_label": "01 Jun 2026 to 30 Jun 2026",
  "period_slug": "2026-06",
  "removals": [
     {"removal_id": "rmv_...", "date": "20-27 Jun 2026", "oil_type": "QOWV", "tcdr": 5.19},
     ...
  ]
}
Every value must trace to what the agent read in Certify this run. No defaults, no guesses.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(f"FAIL: config.json not found at {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    for k in ("certify_removal_url_prefix", "drive_output_folder"):
        if not cfg.get(k):
            sys.exit(f"FAIL: config.json missing required key '{k}'")
    return cfg


def main():
    if len(sys.argv) != 2:
        sys.exit("FAIL: expected one JSON payload argument")
    cfg = load_config()
    p = json.loads(sys.argv[1])

    for k in ("statement_id", "period_label", "period_slug", "removals"):
        if k not in p:
            sys.exit(f"FAIL: payload missing '{k}'")
    if not p["removals"]:
        sys.exit("FAIL: no Charm-oil removals passed — nothing to build (this is a guard, not an error you should force past)")

    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    base = cfg["certify_removal_url_prefix"]
    outdir = cfg["drive_output_folder"]
    os.makedirs(outdir, exist_ok=True)

    rows = p["removals"]
    total = round(sum(float(r["tcdr"]) for r in rows), 2)

    wb = Workbook(); ws = wb.active; ws.title = "Charm Bio-oil Credits"
    HDR = PatternFill("solid", fgColor="D6E4F0"); TOT = PatternFill("solid", fgColor="EAF1FB")
    bold = Font(bold=True); link = Font(color="0563C1", underline="single")
    thin = Side(style="thin", color="BBBBBB"); border = Border(thin, thin, thin, thin)
    center = Alignment(horizontal="center", vertical="center"); left = Alignment(horizontal="left", vertical="center")

    ws["A1"] = f"Charm Bio-oil Credits Submitted — {p['period_label']}"; ws["A1"].font = Font(bold=True, size=13)
    ws.merge_cells("A1:C1")
    ws["A2"] = (f"GHG Statement {p['statement_id']} • Charm-produced oil only "
                f"(QOWV/WODO/Aqueous); AECN removals excluded")
    ws["A2"].font = Font(italic=True, size=9, color="666666"); ws.merge_cells("A2:C2")

    hr = 4
    for c, h in enumerate(["Certify Removal ID", "Removal Date", "Removal Quantity (tCDR)"], 1):
        cell = ws.cell(hr, c, h); cell.font = bold; cell.fill = HDR; cell.border = border; cell.alignment = center

    r = hr + 1
    for row in rows:
        a = ws.cell(r, 1, row["removal_id"]); a.hyperlink = base + row["removal_id"]; a.font = link; a.alignment = left; a.border = border
        b = ws.cell(r, 2, row["date"]); b.alignment = center; b.border = border
        c = ws.cell(r, 3, float(row["tcdr"])); c.number_format = "0.00"; c.alignment = center; c.border = border
        r += 1

    t = ws.cell(r, 1, "TOTAL"); t.font = bold; t.fill = TOT; t.border = border; t.alignment = left
    ws.cell(r, 2, "").fill = TOT; ws.cell(r, 2).border = border
    tv = ws.cell(r, 3, f"=SUM(C{hr+1}:C{r-1})"); tv.font = bold; tv.fill = TOT; tv.number_format = "0.00"; tv.alignment = center; tv.border = border

    ws.column_dimensions["A"].width = 30; ws.column_dimensions["B"].width = 18; ws.column_dimensions["C"].width = 22
    ws.freeze_panes = "A5"

    path = os.path.join(outdir, f"Charm_Bio-oil_Credits_{p['period_slug']}.xlsx")
    wb.save(path)
    print(json.dumps({"saved_path": path, "total_tcdr": total, "n_rows": len(rows)}))


if __name__ == "__main__":
    main()
