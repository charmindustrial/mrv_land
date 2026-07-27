#!/usr/bin/env python3
"""
Final comprehensive data injection — all remaining blank fields.
Source: Certify GHG statement Section E reports + removal records, reviewed 2026-06-05.

Key new data:
- Gross CDR per period (from GHG statement reports)
- Total penalties per period (= gross - net)
- AECN/Kerry penalty allocation by month
- Pipeline: 4 draft removals, 235.70 tCO₂e net
- Aug-25 corrected to 100% AECN (confirmed)
- Sep-25/Oct-25 Kerry source confirmed from removal records
- Efficiency ratio formulas in Efficiency tab
- Source share % formulas in Source Mix
"""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

FILE = "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/mrv-operational-documents/MRV_BI_Dashboard_Shell.xlsx"

CERT = "E2EFDA"   # Certify-verified (green)
CALC = "EBF1DE"   # computed/derived (light green)
PP   = "DEEAF1"   # from PP summary (blue)

def F(c): return PatternFill("solid", fgColor=c)
def put(ws, row, col, value, fill=None, fmt=None):
    c = ws.cell(row=row, column=col, value=value)
    if fill: c.fill = F(fill)
    if fmt:  c.number_format = fmt

CB = 2; NM = 12; CY = CB + NM; CF = CY + 1
def mc(i): return CB + i
MO = ["Jul-25","Aug-25","Sep-25","Oct-25","Nov-25","Dec-25",
      "Jan-26","Feb-26","Mar-26","Apr-26","May-26","Jun-26"]

wb = openpyxl.load_workbook(FILE)

# ══════════════════════════════════════════════════════════════════════════════
#  RUN RATE
# ══════════════════════════════════════════════════════════════════════════════
ws = wb["Run Rate"]

# Row 6 = AECN Net CDR — fix Aug-25 (was pending; now confirmed 100% AECN)
put(ws, 6, mc(1), 555.95, fill=CERT, fmt="#,##0.00")   # Aug-25

# Row 11 = Gross CDR Total (rr_gross_total)
GROSS = {
    1:  804.551,             # Aug-25 (Jun-Jul 2025 period)
    2:  161.907,             # Sep-25 (Aug 1-15 2025)
    3:  "=285.139+351.170",  # Oct-25 (two periods, formula for audit)
    4:  574.795,             # Nov-25 (Oct 1-Nov 6 2025)
    7:  157.052,             # Feb-26 (Nov 7 2025-Jan 31 2026)
    8:  863.601,             # Mar-26 (Feb 1-Mar 2 2026)
    9:  702.779,             # Apr-26 (Mar 3-31 2026)
    10: 578.696,             # May-26 (Apr 1-30 2026)
}
for i, v in GROSS.items():
    put(ws, 11, mc(i), v, fill=CERT, fmt="#,##0.00")

# FY 2025 gross CDR (in-window 2025 credits only: Aug-Nov)
# = 804.551 + 161.907 + (285.139+351.170) + 574.795 = 2,177.562
put(ws, 11, CF, 2177.562, fill=CERT, fmt="#,##0.00")

# Row 12 = AECN Gross CDR
# For 100% AECN months = total; for mixed = proportional by net CDR share
AECN_GROSS = {
    1:  804.551,   # Aug-25: 100% AECN
    2:  0,         # Sep-25: 100% Kerry
    3:  "=351.170+285.139*59.55/166.40",  # Oct-25: full Sep-9-30 + AECN share of Aug-Sep-8
    4:  574.795,   # Nov-25: 100% AECN
    7:  157.052,   # Feb-26: 100% AECN
    8:  863.601,   # Mar-26: 100% AECN
    9:  702.779,   # Apr-26: 100% AECN
    10: "=578.696*475.09/490.82",  # May-26: proportional
}
for i, v in AECN_GROSS.items():
    put(ws, 12, mc(i), v, fill=CALC, fmt="#,##0.00")

# Row 14 = Kerry Gross CDR
KERRY_GROSS = {
    2:  161.907,   # Sep-25: 100% Kerry
    3:  "=285.139*106.85/166.40",   # Oct-25: Kerry share of Aug-Sep-8 period
    10: "=578.696*8.80/490.82",     # May-26: proportional
}
for i, v in KERRY_GROSS.items():
    put(ws, 14, mc(i), v, fill=CALC, fmt="#,##0.00")

# Row 13 = Charm Gross CDR
CHARM_GROSS = {
    10: "=578.696*6.93/490.82",  # May-26: proportional
}
for i, v in CHARM_GROSS.items():
    put(ws, 13, mc(i), v, fill=CALC, fmt="#,##0.00")

# Row 17 = Pipeline Total (Certify draft removals as of 2026-06-05)
# 4 drafts: rmv_1KT27CA911S0PDN0 (AECN 69.12), rmv_1KT4SJ1V71S0BEVX (AECN 138.62),
#           rmv_1KS0CQFV41S06TZK (AECN 18.85), rmv_1KT1WB4TV1S0VFW2 (Kerry 9.11)
put(ws, 17, mc(11), 235.70, fill=CERT, fmt="#,##0.00")  # Jun-26 = current snapshot
put(ws, 18, mc(11), "=69.12+138.62+18.85", fill=CERT, fmt="#,##0.00")   # AECN pipeline
put(ws, 20, mc(11), 9.11, fill=CERT, fmt="#,##0.00")                    # Kerry pipeline

# ══════════════════════════════════════════════════════════════════════════════
#  PENALTIES
# ══════════════════════════════════════════════════════════════════════════════
ws = wb["Penalties"]

# Row 5 = Total penalties (= gross CDR - net CDR per period)
# Formula for auditability where possible; computed values elsewhere
TOTAL_PEN = {
    1:  804.551 - 555.95,                     # Aug-25 = 248.601
    2:  161.907 - 135.39,                     # Sep-25 = 26.517
    3:  "=285.139+351.170-166.40-291.85",     # Oct-25 formula
    4:  574.795 - 454.71,                     # Nov-25 = 120.085
    7:  157.052 - 43.47,                      # Feb-26 = 113.582
    8:  863.601 - 764.14,                     # Mar-26 = 99.461
    9:  702.779 - 612.99,                     # Apr-26 = 89.789
    10: 578.696 - 490.82,                     # May-26 = 87.876
}
for i, v in TOTAL_PEN.items():
    put(ws, 5, mc(i), v, fill=CERT, fmt="#,##0.00")

# Row 7 = AECN production-side penalties (approximate proportional allocation)
# 100% AECN months: total period penalties = AECN penalties
# Mixed months: allocated by net CDR share (approximation — actual varies by CI)
AECN_PEN = {
    1:  248.601,              # Aug-25: 100% AECN
    2:  0,                    # Sep-25: 100% Kerry
    3:  "=59.32+118.739*59.55/166.40",  # Oct-25: Sep-9-30 (100% AECN=59.32) + share of Aug-16-Sep-8
    4:  120.085,              # Nov-25: 100% AECN
    7:  113.582,              # Feb-26: 100% AECN
    8:  99.461,               # Mar-26: 100% AECN
    9:  89.789,               # Apr-26: 100% AECN
    10: "=87.876*475.09/490.82",  # May-26: proportional ≈ 85.07
}
for i, v in AECN_PEN.items():
    put(ws, 7, mc(i), v, fill=CERT if isinstance(v, (int,float)) else CALC, fmt="#,##0.00")

# Row 8 = Kerry production-side penalties
# Kerry penalty structure: essentially transport embodied only (process BCU'd)
# ~2.3% of net CDR for Kerry (from removal record analysis)
KERRY_PEN = {
    2:  26.517,    # Sep-25: 100% Kerry, total = Kerry total
    3:  "=118.739*106.85/166.40",  # Oct-25: Kerry share of Aug-16-Sep-8
    10: "=87.876*8.80/490.82",     # May-26: proportional ≈ 1.58
}
for i, v in KERRY_PEN.items():
    put(ws, 8, mc(i), v, fill=CERT if isinstance(v, (int,float)) else CALC, fmt="#,##0.00")

# Note: Charm penalties in row 6 already populated from PP summaries
# Row 9 (downstream transport) and row 10 (well facility) pending per-removal drill

# ══════════════════════════════════════════════════════════════════════════════
#  EFFICIENCY TAB — memo volumes + ratio formulas
# ══════════════════════════════════════════════════════════════════════════════
ws = wb["Efficiency"]

# Row 17 = Net CDR total (copy from Run Rate row 5)
ws_rr = wb["Run Rate"]
for i in range(NM):
    v = ws_rr.cell(row=5, column=mc(i)).value
    if v is not None:
        put(ws, 17, mc(i), v, fill=CERT, fmt="#,##0.00")
# FY25
put(ws, 17, CF, ws_rr.cell(row=5, column=CF).value, fill=CERT, fmt="#,##0.00")

# Row 18 = Gross CDR total (same data as RR row 11)
for i, v in GROSS.items():
    put(ws, 18, mc(i), v, fill=CERT, fmt="#,##0.00")
put(ws, 18, CF, 2177.562, fill=CERT, fmt="#,##0.00")

# Row 5 = efficiency ratio formula: net/gross for each month
for i in range(NM):
    col = mc(i)
    col_ltr = get_column_letter(col)
    c = ws.cell(row=5, column=col)
    c.value = f"=IF({col_ltr}18>0,{col_ltr}17/{col_ltr}18,\"\")"
    c.fill = F(CALC); c.number_format = "0.0%"
# YTD
ytd_net = f"SUM({get_column_letter(mc(6))}17:{get_column_letter(mc(11))}17)"
ytd_gross = f"SUM({get_column_letter(mc(6))}18:{get_column_letter(mc(11))}18)"
yc = ws.cell(row=5, column=CY)
yc.value = f"=IF({ytd_gross}>0,{ytd_net}/{ytd_gross},\"\")"
yc.fill = F(CALC); yc.number_format = "0.0%"

# ══════════════════════════════════════════════════════════════════════════════
#  SOURCE MIX — gross CDR rows + share % formulas + efficiency formulas
# ══════════════════════════════════════════════════════════════════════════════
ws = wb["Source Mix"]

# Row 16 = Gross CDR total
for i, v in GROSS.items():
    put(ws, 16, mc(i), v, fill=CERT, fmt="#,##0.00")

# Row 17 = AECN Gross CDR
for i, v in AECN_GROSS.items():
    put(ws, 17, mc(i), v, fill=CALC, fmt="#,##0.00")

# Row 19 = Kerry Gross CDR
for i, v in KERRY_GROSS.items():
    put(ws, 19, mc(i), v, fill=CALC, fmt="#,##0.00")

# Row 18 = Charm Gross CDR
for i, v in CHARM_GROSS.items():
    put(ws, 18, mc(i), v, fill=CALC, fmt="#,##0.00")

# Rows 11-13 = Source share % formulas (AECN/Charm/Kerry % of Net CDR total)
# Row 11 = AECN %, row 12 = Charm %, row 13 = Kerry %
for share_row, net_row in [(11,6),(12,7),(13,8)]:
    for i in range(NM):
        col = mc(i)
        cl = get_column_letter(col)
        c = ws.cell(row=share_row, column=col)
        c.value = f"=IF({cl}5>0,{cl}{net_row}/{cl}5,\"\")"
        c.fill = F(CALC); c.number_format = "0.0%"
    # YTD
    ytd_src = f"SUM({get_column_letter(mc(6))}{net_row}:{get_column_letter(mc(11))}{net_row})"
    ytd_tot = f"SUM({get_column_letter(mc(6))}5:{get_column_letter(mc(11))}5)"
    yc = ws.cell(row=share_row, column=CY)
    yc.value = f"=IF({ytd_tot}>0,{ytd_src}/{ytd_tot},\"\")"
    yc.fill = F(CALC); yc.number_format = "0.0%"

# Rows 22-25 = Efficiency by source (net/gross for each source)
# Row 22 = total, 23 = AECN, 24 = Charm, 25 = Kerry
for eff_row, net_row, gross_row in [(22,5,16),(23,6,17),(24,7,18),(25,8,19)]:
    for i in range(NM):
        col = mc(i); cl = get_column_letter(col)
        c = ws.cell(row=eff_row, column=col)
        c.value = f"=IF({cl}{gross_row}>0,{cl}{net_row}/{cl}{gross_row},\"\")"
        c.fill = F(CALC); c.number_format = "0.0%"
    yc = ws.cell(row=eff_row, column=CY)
    ytd_n = f"SUM({get_column_letter(mc(6))}{net_row}:{get_column_letter(mc(11))}{net_row})"
    ytd_g = f"SUM({get_column_letter(mc(6))}{gross_row}:{get_column_letter(mc(11))}{gross_row})"
    yc.value = f"=IF({ytd_g}>0,{ytd_n}/{ytd_g},\"\")"
    yc.fill = F(CALC); yc.number_format = "0.0%"

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD — update key KPI tile references to live formula values
# ══════════════════════════════════════════════════════════════════════════════
# Dashboard summary rows - wire to detail tabs
# Row 11 = Net CDR total, row 15 = Gross CDR total, row 16 = efficiency, row 20 = penalties %
ws = wb["Dashboard"]
# Rows 11-24 are the summary table. Wire Net CDR total and efficiency to RR/Efficiency tabs.
# Row 11 = Net CDR total — copy values from Run Rate row 5
for i in range(NM):
    v = wb["Run Rate"].cell(row=5, column=mc(i)).value
    if v:
        put(ws, 11, mc(i), v, fill=CERT, fmt="#,##0.00")

wb.save(FILE)
print("Saved.")

# Verify key values
wb2 = openpyxl.load_workbook(FILE)
print("\nRun Rate Gross CDR (row 11):")
rr = wb2["Run Rate"]
for i in range(NM):
    v = rr.cell(11, mc(i)).value
    if v: print(f"  {MO[i]}: {v}")

print("\nPenalties Total (row 5):")
pen = wb2["Penalties"]
for i in range(NM):
    v = pen.cell(5, mc(i)).value
    if v: print(f"  {MO[i]}: {v}")

print("\nPipeline (RR row 17, Jun-26):")
print(f"  {rr.cell(17, mc(11)).value}")
