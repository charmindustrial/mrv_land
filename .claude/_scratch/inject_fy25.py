#!/usr/bin/env python3
"""Fill all FY25 column values. FY25 = credits issued in calendar year 2025.
In-window 2025 credit months: Aug-25, Sep-25, Oct-25, Nov-25 (Jul/Dec/Jan = no credits).
For production/operational data FY25 = Aug-Dec 2025 production periods."""

import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

FILE = "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/mrv-operational-documents/MRV_BI_Dashboard_Shell.xlsx"
CERT="E2EFDA"; CALC="EBF1DE"; PP="DEEAF1"
def F(c): return PatternFill("solid", fgColor=c)
def put(ws, row, col, value, fill=None, fmt="#,##0.00"):
    c = ws.cell(row=row, column=col, value=value)
    if fill: c.fill = F(fill)
    if fmt: c.number_format = fmt

CB=2; NM=12; CY=CB+NM; CF=CY+1

wb = openpyxl.load_workbook(FILE)

# ── Pre-computed FY25 sums ────────────────────────────────────────────────────
# Net CDR: credits issued Aug-Nov 2025 (in-window)
NET_AECN_FY25   = 555.95 + 0 + 351.40 + 454.71          # 1,362.06
NET_KERRY_FY25  = 0 + 135.39 + 106.85 + 0               # 242.24
NET_CHARM_FY25  = 0
NET_TOTAL_FY25  = 4461.21   # full-year 2025 (all periods credited in CY2025)
NET_INWINDOW_FY25 = 555.95 + 135.39 + 458.25 + 454.71   # 1,604.30 (in-window only)

# Gross CDR: in-window 2025 periods
GROSS_TOTAL_FY25  = 2177.562
GROSS_AECN_FY25   = 804.551 + 0 + 453.22 + 574.795      # 1,832.566
GROSS_KERRY_FY25  = 0 + 161.907 + 183.08 + 0            # 344.987
GROSS_CHARM_FY25  = 0

# Bio-oil volumes: in-window 2025
BIO_TOTAL_FY25  = 1652.796
BIO_AECN_FY25   = 553.599 + 0 + 379.036 + 432.060       # 1,364.695
BIO_KERRY_FY25  = 0 + 118.562 + 169.539 + 0             # 288.101
BIO_CHARM_FY25  = 0

# Penalties: in-window 2025 (Gross - Net, in-window only)
PEN_TOTAL_FY25   = GROSS_TOTAL_FY25 - NET_INWINDOW_FY25  # 573.262
PEN_AECN_FY25    = 248.601 + 0 + 101.79 + 120.085        # 470.476
PEN_KERRY_FY25   = 0 + 26.517 + 76.27 + 0               # 102.787
PEN_WELLF_FY25   = 176.185 + 2.988 + 162.037 + 24.975   # 366.185
PEN_DOWN_FY25    = 4.860 + 3.633 + 6.845 + 3.472        # 18.810

# Charm PP components FY25 (Aug-Dec 2025 production months: idx 1-5)
CHARM_PROP_FY25  = 8.638 + 0 + 12.905 + 10.574 + 8.205  # 40.322
CHARM_CAPEE_FY25 = 3.091 + 0 + 2.474 + 1.202 + 1.527   # 8.294
CHARM_BM_FY25    = 2.218 + 0 + 1.174 + 1.368 + 1.760   # 6.520
CHARM_SPCE_FY25  = 1.015 + 0 + 1.286 + 0.906 + 0.658   # 3.865
CHARM_ELEC_FY25  = 0.985 + 0 + 1.157 + 1.002 + 0.747   # 3.891
CHARM_OTHER_FY25 = 0.559 + 0 + 1.119 + 1.339 + 0.627   # 3.644
CHARM_PEN_FY25   = 16.508 + 0 + 20.105 + 16.396 + 13.523  # 66.532

# Production FY25 (Aug-Dec 2025 production months)
BIOMASS_FY25    = 84.84 + 64.58 + 47.45 + 25.00 + 28.95   # 250.82
BIOIL_FY25      = 20.928 + 12.630 + 14.227 + 9.984 + 6.481  # 64.250
BIOIL_C_FY25    = 10.353 + 6.573 + 8.247 + 5.684 + 3.157   # 34.014
BIOCHAR_FY25    = 9.186 + 3.868 + 8.085 + 4.580 + 4.074    # 29.793
BIOCHAR_C_FY25  = 7.931 + 3.304 + 7.399 + 3.891 + 3.619    # 26.144

# ── RUN RATE FY25 ─────────────────────────────────────────────────────────────
rr = wb["Run Rate"]
put(rr,  5, CF, NET_TOTAL_FY25,   fill=CERT)   # Net CDR total (full CY2025)
put(rr,  6, CF, NET_AECN_FY25,    fill=CALC)   # AECN (in-window 2025 only)
put(rr,  7, CF, NET_CHARM_FY25,   fill=CALC)   # Charm
put(rr,  8, CF, NET_KERRY_FY25,   fill=CALC)   # Kerry
put(rr, 11, CF, GROSS_TOTAL_FY25, fill=CERT)   # Gross CDR total
put(rr, 12, CF, GROSS_AECN_FY25,  fill=CALC)
put(rr, 13, CF, GROSS_CHARM_FY25, fill=CALC)
put(rr, 14, CF, GROSS_KERRY_FY25, fill=CALC)
# Pipeline FY25 = 0 (pipeline is point-in-time, not annual)
put(rr, 17, CF, 0, fill=CERT)
put(rr, 18, CF, 0, fill=CERT)
put(rr, 19, CF, 0, fill=CERT)
put(rr, 20, CF, 0, fill=CERT)
# Timing rows FY25 = average of monthly values (simple avg, not weighted)
# OKR avg: (27+35+31+14)/4 = 26.75 days (Aug/Sep/Oct/Nov 2025)
put(rr, 23, CF, round((27+35+31+14)/4,1), fill=CALC, fmt="#,##0")
put(rr, 24, CF, round((8+0+0+1)/4,1),     fill=CALC, fmt="#,##0")
put(rr, 25, CF, round((19+35+31+13)/4,1), fill=CALC, fmt="#,##0")

# ── PENALTIES FY25 ───────────────────────────────────────────────────────────
pen = wb["Penalties"]
put(pen,  5, CF, PEN_TOTAL_FY25,   fill=CERT)
put(pen,  6, CF, CHARM_PEN_FY25,   fill=PP)
put(pen,  7, CF, PEN_AECN_FY25,    fill=CALC)
put(pen,  8, CF, PEN_KERRY_FY25,   fill=CALC)
put(pen,  9, CF, PEN_DOWN_FY25,    fill=CALC)
put(pen, 10, CF, PEN_WELLF_FY25,   fill=CERT)
# Charm components FY25
put(pen, 13, CF, CHARM_PROP_FY25,  fill=PP)
put(pen, 14, CF, CHARM_CAPEE_FY25, fill=PP)
put(pen, 15, CF, CHARM_BM_FY25,    fill=PP)
put(pen, 16, CF, CHARM_SPCE_FY25,  fill=PP)
put(pen, 17, CF, CHARM_ELEC_FY25,  fill=PP)
put(pen, 18, CF, CHARM_OTHER_FY25, fill=PP)
# AECN components FY25
put(pen, 23, CF, round(PEN_AECN_FY25*0.005,3), fill=CALC)  # N₂O
put(pen, 24, CF, round(PEN_AECN_FY25*0.995,3), fill=CALC)  # Other
# Kerry components FY25 = 0
for row in [27,28,29,30]: put(pen, row, CF, 0, fill="F2F2F2")
# Downstream components FY25
put(pen, 35, CF, round(GROSS_AECN_FY25*0.00604,3), fill=CALC)   # AECN truck
put(pen, 39, CF, round(GROSS_KERRY_FY25*0.02243,3), fill=CALC)  # Kerry truck
# Well facility % FY25
pass  # well facility % — skip

# ── EFFICIENCY FY25 ──────────────────────────────────────────────────────────
eff = wb["Efficiency"]
put(eff, 17, CF, NET_INWINDOW_FY25,  fill=CERT)   # Net CDR memo
put(eff, 18, CF, GROSS_TOTAL_FY25,   fill=CERT)   # Gross CDR memo
put(eff, 19, CF, BIO_TOTAL_FY25,     fill=CERT)   # Bio-oil total
put(eff, 20, CF, BIO_AECN_FY25,      fill=CALC)   # AECN bio-oil
put(eff, 21, CF, BIO_CHARM_FY25,     fill=CALC)   # Charm bio-oil
put(eff, 22, CF, BIO_KERRY_FY25,     fill=CALC)   # Kerry bio-oil
# Ratio FY25
net_gross_fy25 = round(NET_INWINDOW_FY25/GROSS_TOTAL_FY25, 4)
put(eff, 5, CF, net_gross_fy25, fill=CALC, fmt="0.0%")
put(eff, 6, CF, round(NET_AECN_FY25/GROSS_AECN_FY25,4) if GROSS_AECN_FY25 else None, fill=CALC, fmt="0.0%")
put(eff, 8, CF, round(NET_KERRY_FY25/GROSS_KERRY_FY25,4) if GROSS_KERRY_FY25 else None, fill=CALC, fmt="0.0%")
# Net CDR per tonne FY25
put(eff, 11, CF, round(NET_INWINDOW_FY25/BIO_TOTAL_FY25,4), fill=CALC)
put(eff, 12, CF, round(NET_AECN_FY25/BIO_AECN_FY25,4),      fill=CALC)
put(eff, 14, CF, round(NET_KERRY_FY25/BIO_KERRY_FY25,4),    fill=CALC)

# ── PRODUCTION (CHARM) FY25 ──────────────────────────────────────────────────
prod = wb["Production (Charm)"]
put(prod,  5, CF, BIOMASS_FY25,   fill=PP)
put(prod,  8, CF, BIOIL_FY25,     fill=PP)
put(prod,  9, CF, BIOIL_C_FY25,   fill=PP)
put(prod, 16, CF, BIOCHAR_FY25,   fill=PP)
put(prod, 17, CF, BIOCHAR_C_FY25, fill=PP)

# ── SOURCE MIX FY25 ──────────────────────────────────────────────────────────
sm = wb["Source Mix"]
put(sm,  5, CF, NET_INWINDOW_FY25, fill=CERT)
put(sm,  6, CF, NET_AECN_FY25,     fill=CALC)
put(sm,  7, CF, NET_CHARM_FY25,    fill=CALC)
put(sm,  8, CF, NET_KERRY_FY25,    fill=CALC)
aecn_sh = round(NET_AECN_FY25/NET_INWINDOW_FY25,4)
kerry_sh = round(NET_KERRY_FY25/NET_INWINDOW_FY25,4)
put(sm, 11, CF, aecn_sh,  fill=CALC, fmt="0.0%")
put(sm, 12, CF, 0,        fill=CALC, fmt="0.0%")
put(sm, 13, CF, kerry_sh, fill=CALC, fmt="0.0%")
put(sm, 16, CF, GROSS_TOTAL_FY25,  fill=CERT)
put(sm, 17, CF, GROSS_AECN_FY25,   fill=CALC)
put(sm, 18, CF, GROSS_CHARM_FY25,  fill=CALC)
put(sm, 19, CF, GROSS_KERRY_FY25,  fill=CALC)
put(sm, 22, CF, round(NET_INWINDOW_FY25/GROSS_TOTAL_FY25,4), fill=CALC, fmt="0.0%")
put(sm, 23, CF, round(NET_AECN_FY25/GROSS_AECN_FY25,4),      fill=CALC, fmt="0.0%")
put(sm, 25, CF, round(NET_KERRY_FY25/GROSS_KERRY_FY25,4),    fill=CALC, fmt="0.0%")
put(sm, 28, CF, max(aecn_sh, kerry_sh), fill=CALC, fmt="0.0%")  # largest share
put(sm, 29, CF, 2, fill=CALC, fmt="#,##0")  # 2 sources active in 2025 (AECN + Kerry)

# ── DASHBOARD FY25 ───────────────────────────────────────────────────────────
db = wb["Dashboard"]
put(db, 11, CF, NET_TOTAL_FY25,          fill=CALC)   # Net CDR (full CY2025)
put(db, 12, CF, NET_AECN_FY25,           fill=CALC)
put(db, 13, CF, NET_CHARM_FY25,          fill=CALC)
put(db, 14, CF, NET_KERRY_FY25,          fill=CALC)
put(db, 15, CF, GROSS_TOTAL_FY25,        fill=CALC)
put(db, 16, CF, net_gross_fy25,          fill=CALC, fmt="0.0%")
put(db, 17, CF, 0,                       fill=CALC)   # no pipeline in FY25 (snapshot metric)
put(db, 18, CF, round((27+35+31+14)/4,1),fill=CALC, fmt="#,##0")  # avg OKR
put(db, 19, CF, round(PEN_TOTAL_FY25/GROSS_TOTAL_FY25,4), fill=CALC, fmt="0.0%")
put(db, 20, CF, aecn_sh,                 fill=CALC, fmt="0.0%")
put(db, 21, CF, 0,                       fill=CALC, fmt="0.0%")
put(db, 22, CF, kerry_sh,                fill=CALC, fmt="0.0%")

wb.save(FILE)
print("FY25 column filled.")
print(f"  Net CDR FY25 (full year): {NET_TOTAL_FY25:,.2f} tCO₂e")
print(f"  Net CDR FY25 (in-window): {NET_INWINDOW_FY25:,.2f} tCO₂e")
print(f"  Gross CDR FY25: {GROSS_TOTAL_FY25:,.3f} tCO₂e")
print(f"  Efficiency FY25: {net_gross_fy25:.1%}")
print(f"  Bio-oil FY25: {BIO_TOTAL_FY25:,.3f} t")
print(f"  Net CDR/t FY25: {NET_INWINDOW_FY25/BIO_TOTAL_FY25:.3f} tCO₂e/t")
print(f"  AECN share FY25: {aecn_sh:.1%}")
print(f"  Kerry share FY25: {kerry_sh:.1%}")
print(f"  Total penalties FY25: {PEN_TOTAL_FY25:,.3f} tCO₂e")
print(f"  Penalties % of gross FY25: {PEN_TOTAL_FY25/GROSS_TOTAL_FY25:.1%}")
