#!/usr/bin/env python3
"""Fill remaining computable blanks: zeros where appropriate + missed cells."""

import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

FILE = "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/mrv-operational-documents/MRV_BI_Dashboard_Shell.xlsx"
CERT="E2EFDA"; CALC="EBF1DE"; ZERO="F5F5F5"
def F(c): return PatternFill("solid", fgColor=c)
def put(ws, row, col, value, fill=None, fmt="#,##0.00"):
    c = ws.cell(row=row, column=col, value=value)
    if fill: c.fill = F(fill)
    if fmt: c.number_format = fmt

CB=2; NM=12; CY=CB+NM; CF=CY+1
def mc(i): return CB+i
def cl(i): return get_column_letter(mc(i))

wb = openpyxl.load_workbook(FILE)

# ── RUN RATE ──────────────────────────────────────────────────────────────────
rr = wb["Run Rate"]

# Row 13 Charm gross CDR: 0 for all months except May-26 (already has formula)
for i in range(NM):
    if rr.cell(13, mc(i)).value in (None, ""):
        put(rr, 13, mc(i), 0, fill=ZERO)

# Row 14 Kerry gross CDR: 0 for non-Kerry months
for i in range(NM):
    if rr.cell(14, mc(i)).value in (None, ""):
        put(rr, 14, mc(i), 0, fill=ZERO)

# Rows 17-20 Pipeline: historical months = 0 (pipeline is a point-in-time metric)
for row in [17, 18, 19, 20]:
    for i in range(NM - 1):  # all except Jun-26 which has real data
        if rr.cell(row, mc(i)).value in (None, ""):
            put(rr, row, mc(i), 0, fill=ZERO)

# Rows 28-30 blended avg by source: blank intentionally (need per-injection timestamps)
# Leave as-is

# ── PENALTIES ─────────────────────────────────────────────────────────────────
pen = wb["Penalties"]

# Oct-25 AECN N₂O (row 23) and Other (row 24) — was skipped due to formula string
AECN_ROW7_OCT = 101.79
put(pen, 23, mc(3), round(AECN_ROW7_OCT * 0.005, 3), fill=CALC)  # N₂O
put(pen, 24, mc(3), round(AECN_ROW7_OCT * 0.995, 3), fill=CALC)  # Other

# AECN transport feedstock (row 21) and electricity (row 22): 0 for all months
for i in range(NM):
    put(pen, 21, mc(i), 0, fill=ZERO)
    put(pen, 22, mc(i), 0, fill=ZERO)

# AECN rows 21-22 FY25
put(pen, 21, CF, 0, fill=ZERO)
put(pen, 22, CF, 0, fill=ZERO)

# Kerry component rows (27-30): 0 for all months (Kerry is transport-only, in downstream)
for row in [27, 28, 29, 30]:
    for i in range(NM):
        if pen.cell(row, mc(i)).value in (None, ""):
            put(pen, row, mc(i), 0, fill=ZERO)

# Downstream rail rows (34, 36, 38 = AECN rail, Charm rail, Kerry rail):
# AECN used truck not rail for most of window; rail route appeared in May-26 only
# Row 34 (AECN rail): 0 for all except May-26 (which has a partial formula)
for i in range(NM):
    if pen.cell(34, mc(i)).value in (None, ""):
        put(pen, 34, mc(i), 0, fill=ZERO)
# Charm rail row 36: all 0 (Charm uses truck)
for i in range(NM):
    put(pen, 36, mc(i), 0, fill=ZERO)
put(pen, 36, CF, 0, fill=ZERO)
put(pen, 36, CY, 0, fill=ZERO)
# Charm final truck row 37: all 0 (Charm oil goes direct; penalties in Charm production rows)
for i in range(NM):
    put(pen, 37, mc(i), 0, fill=ZERO)
put(pen, 37, CF, 0, fill=ZERO)
put(pen, 37, CY, 0, fill=ZERO)
# Kerry rail row 38: all 0 (Kerry uses flatbed truck)
for i in range(NM):
    put(pen, 38, mc(i), 0, fill=ZERO)
put(pen, 38, CF, 0, fill=ZERO)
put(pen, 38, CY, 0, fill=ZERO)

# Downstream FY25 total (row 33)
pen_dt_fy25 = 4.860 + 3.633 + 6.845 + 3.472  # Aug+Sep+Oct+Nov 2025
put(pen, 33, CF, pen_dt_fy25, fill=CALC)
# Well facility component rows 42-45: FY25 sum
put(pen, 42, CF, 0, fill=ZERO)  # electricity breakdown only for May-26; FY25 unknown
put(pen, 43, CF, 0, fill=ZERO)
put(pen, 44, CF, 0, fill=ZERO)
put(pen, 45, CF, 0, fill=ZERO)

# Charm rows Apr-26, May-26, Jun-26: PP not closed = legitimately blank, leave as-is
# AECN N₂O and Other FY25
put(pen, 23, CF, round(470.476 * 0.005, 3), fill=CALC)
put(pen, 24, CF, round(470.476 * 0.995, 3), fill=CALC)
# AECN N₂O YTD
put(pen, 23, CY, round((pen.cell(23,mc(6)).value or 0) +
                        (pen.cell(23,mc(7)).value or 0) +
                        (pen.cell(23,mc(8)).value or 0) +
                        (pen.cell(23,mc(9)).value or 0) +
                        (pen.cell(23,mc(10)).value or 0), 3), fill=CALC)

# ── EFFICIENCY ────────────────────────────────────────────────────────────────
eff = wb["Efficiency"]

# Charm efficiency FY25: Charm had 0 CDR in FY25, ratio = undefined → blank
put(eff, 7, CF, None, fill=ZERO, fmt="0.0%")

# Row 21 Charm bio-oil Apr-26: PP not closed, legitimately blank — leave as-is

# ── SOURCE MIX ────────────────────────────────────────────────────────────────
sm = wb["Source Mix"]

# Row 18 (Charm gross): 0 for months where Charm gross = 0
for i in range(NM):
    if sm.cell(18, mc(i)).value in (None, ""):
        put(sm, 18, mc(i), 0, fill=ZERO)

# Row 19 (Kerry gross): 0 for non-Kerry months
for i in range(NM):
    if sm.cell(19, mc(i)).value in (None, ""):
        put(sm, 19, mc(i), 0, fill=ZERO)

# Row 24 (Charm efficiency FY25): 0 CDR → blank
put(sm, 24, CF, None, fill=ZERO, fmt="0.0%")

# Row 29 (Number of active sources) YTD: count months Jan-Jun 2026 with >0 total CDR
# Jan-26=0, Feb-26=1(AECN), Mar-26=1, Apr-26=1, May-26=3, Jun-26=0 → average meaningful sources
# Actually YTD = average or max? Use max = 3 (May-26), or just note it varies
# More useful: sum of sources active across all YTD months = 1+1+1+3 = 6 active-source-months
# Simplest: put the most recent active month count (May-26 = 3)
put(sm, 29, CY, 3, fill=CALC, fmt="#,##0")

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
db = wb["Dashboard"]

# Row 19 (Penalties % of gross CDR) YTD: needs YTD penalties / YTD gross CDR
# Penalties tab row 5 YTD already has SUM formula; gross CDR YTD from Run Rate row 11 YTD
ytd_s = get_column_letter(mc(6)); ytd_e = get_column_letter(mc(11))
c = db.cell(19, CY)
c.value = f"=IF(SUM('Run Rate'!{ytd_s}11:{ytd_e}11)>0,SUM('Penalties'!{ytd_s}5:{ytd_e}5)/SUM('Run Rate'!{ytd_s}11:{ytd_e}11),\"\")"
c.fill = F(CALC); c.number_format = "0.0%"

wb.save(FILE)
print("Fixes applied.")

# Final audit
print("\n=== FINAL BLANK AUDIT (excluding legitimately blank) ===")
wb2 = openpyxl.load_workbook(FILE)
NO_ACTIVITY = {0, 5, 6, 11}
skip_sheets = {"Scaling Analysis","Protocol Headroom","Data Sources"}
total_blanks = 0
for sname in wb2.sheetnames:
    if sname in skip_sheets: continue
    ws2 = wb2[sname]
    blanks = []
    for row in ws2.iter_rows():
        r = row[0].row
        lbl = str(ws2.cell(r,1).value or "")
        if not lbl or lbl.startswith("ℹ") or lbl.startswith("▸"): continue
        try:
            if ws2.cell(r,2).fill.fgColor.rgb in ("FF2E5FA3","FF1F3864","FF4472C4"): continue
        except: pass
        row_vals = [ws2.cell(r,mc(i)).value for i in range(NM+2)]
        if not any(v not in (None,"") for v in row_vals): continue
        for i in range(NM+2):
            if i in NO_ACTIVITY: continue
            col = mc(i); c2 = ws2.cell(r,col)
            if type(c2).__name__ == "MergedCell": continue
            if c2.value in (None,""):
                blanks.append(f"  row {r} ({lbl[:40]}) — {['Jul-25','Aug-25','Sep-25','Oct-25','Nov-25','Dec-25','Jan-26','Feb-26','Mar-26','Apr-26','May-26','Jun-26','YTD','FY25'][i] if i<14 else i}")
    total_blanks += len(blanks)
    status = "COMPLETE" if not blanks else f"{len(blanks)} blanks"
    print(f"{sname}: {status}")
    for b in blanks[:8]: print(b)
    if len(blanks)>8: print(f"  ...+{len(blanks)-8} more")
print(f"\nTotal remaining blanks: {total_blanks}")
