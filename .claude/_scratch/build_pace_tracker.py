#!/usr/bin/env python3
"""EE Pace Tracker v1 — clean experimental build"""

import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE   = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/.playwright-mcp'
OUTPUT = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/EE_Pace_Tracker_v1.xlsx'
CUTOFF = pd.Timestamp('2026-04-30')   # latest closed RP

# ── Projection ────────────────────────────────────────────────────────────────
proj = pd.read_csv(
    f'{BASE}/Master-EE-UoP-Amortization-CO-Injection---Projection.csv',
    header=None, skiprows=5, usecols=[0, 1], names=['month', 'mt'])
proj = proj[proj['month'].astype(str).str.match(r'^\d{4}-\d{2}', na=False)].copy()
proj['month'] = pd.to_datetime(proj['month'])
proj['mt'] = pd.to_numeric(
    proj['mt'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
proj = proj[proj['month'] <= '2035-12-01'].reset_index(drop=True)

def sum_cdr(start, end):
    """Sum projected MT for all months start <= month <= end (month boundaries)."""
    if pd.isna(start) or pd.isna(end):
        return 0.0
    m1 = pd.Timestamp(start.year, start.month, 1)
    m2 = pd.Timestamp(end.year,   end.month,   1)
    if m2 < m1:
        return 0.0
    return float(proj.loc[(proj['month'] >= m1) & (proj['month'] <= m2), 'mt'].sum())

# ── Assets ────────────────────────────────────────────────────────────────────
raw = pd.read_csv(
    f'{BASE}/Master-EE-UoP-Amortization-CO-Injection---Combined-Amortization-History.csv',
    header=None, skiprows=3, low_memory=False)
raw.columns = raw.iloc[0]
df = raw.iloc[1:].reset_index(drop=True).copy()
df = df[df['Asset ID'].astype(str).str.match(r'^EE-', na=False)][
    ['Asset ID','Stream','Site','Item Name','Total GWP','Commission','Disposal','Drawn to Date']
].copy()

for c in ['Total GWP', 'Drawn to Date']:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(r'[,\s$]', '', regex=True),
        errors='coerce').fillna(0)

df['Commission'] = pd.to_datetime(df['Commission'], errors='coerce')
df['Disposal']   = pd.to_datetime(df['Disposal'],   errors='coerce')
df['is_disposed'] = df['Disposal'].notna()

# 5-year window = 60 months starting from commission month
df['window_close'] = df['Commission'].apply(
    lambda d: d + pd.DateOffset(months=59) if pd.notna(d) else pd.NaT)

# ── Calculations ──────────────────────────────────────────────────────────────
df['proj_full']      = df.apply(lambda r: sum_cdr(r['Commission'],  r['window_close']),              axis=1)
df['proj_to_cutoff'] = df.apply(lambda r: sum_cdr(r['Commission'],  CUTOFF),                          axis=1)
df['proj_remaining'] = df.apply(lambda r: sum_cdr(CUTOFF + pd.DateOffset(months=1), r['window_close']), axis=1)

# Expected amortized by CUTOFF = Total GWP × (proj so far / proj full window)
df['expected'] = np.where(
    df['proj_full'] > 0,
    df['Total GWP'] * df['proj_to_cutoff'] / df['proj_full'],
    0.0)

df['remaining_gwp'] = df['Total GWP'] - df['Drawn to Date']

# Behind (kg): positive = behind, negative = ahead
df['behind_kg'] = df['expected'] - df['Drawn to Date']

# % of expected schedule completed
df['pct_done'] = np.where(
    df['expected'] > 0,
    df['Drawn to Date'] / df['expected'] * 100,
    np.where(df['Drawn to Date'] > 0, 999.0, 0.0))   # 999 = "ahead with 0 expected"

# Required rate going forward — only for active (non-disposed) assets
df['rate_fwd'] = np.where(
    (df['proj_remaining'] > 0) & (~df['is_disposed']),
    df['remaining_gwp'] / df['proj_remaining'],
    0.0)

# ── Build Excel ───────────────────────────────────────────────────────────────
wb = Workbook()
ws = wb.active
ws.title = 'Pace Tracker'

HDR_FILL  = PatternFill('solid', fgColor='1F3864')
CO_FILL   = PatternFill('solid', fgColor='E2EFDA')
INJ_FILL  = PatternFill('solid', fgColor='DAEEF3')
TOT_FILL  = PatternFill('solid', fgColor='D6DCE4')
DISP_FILL = PatternFill('solid', fgColor='F2F2F2')
HDR_FONT  = Font(name='Calibri', bold=True,  color='FFFFFF', size=10)
BOLD      = Font(name='Calibri', bold=True,  size=10)
NORM      = Font(name='Calibri',             size=10)
GRAY      = Font(name='Calibri',             size=10, color='999999')

# Note row
note = (f'Amortized to date through: {CUTOFF.strftime("%b %d, %Y")}  |  '
        f'Projection: Liam (TMRV-674)  |  '
        f'Drawn to Date: Combined Amortization History (any method — tDBM or injection MT)  |  '
        f'Required Rate Fwd = Remaining GWP ÷ projected CDR from {CUTOFF.strftime("%b %Y")} to 5yr window close')
ws.cell(1, 1, note).font = Font(name='Calibri', italic=True, size=9, color='555555')
ws.merge_cells('A1:L1')
ws.row_dimensions[1].height = 18

HEADERS = [
    'Asset ID', 'Stream', 'Site', 'Item Name',
    'Total GWP\n(kg)', 'Commission', '5yr Window\nCloses',
    'Amortized\nto Date (kg)', '% Complete',
    'Remaining\n(kg)', 'CDR Remaining\nin Window (MT)', 'Required Rate\nFwd (kg/MT CDR)'
]
NFMT = ['@','@','@','@',
        '#,##0.00','YYYY-MM-DD','YYYY-MM-DD',
        '#,##0.00','0.0"%"',
        '#,##0.00','#,##0.0','0.00000']

for col, h in enumerate(HEADERS, 1):
    c = ws.cell(2, col, h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
ws.row_dimensions[2].height = 36
ws.freeze_panes = 'A3'

row = 3
for _, r in df.iterrows():
    is_d = r['is_disposed']
    fill = DISP_FILL if is_d else (CO_FILL if r['Stream'] == 'CO' else INJ_FILL)
    font = GRAY if is_d else NORM

    pct_complete = r['Drawn to Date'] / r['Total GWP'] * 100 if r['Total GWP'] > 0 else 0
    vals = [
        r['Asset ID'],
        r['Stream'] + (' (disposed)' if is_d else ''),
        r['Site'],
        r['Item Name'],
        r['Total GWP'],
        r['Commission'].date() if pd.notna(r['Commission']) else None,
        r['window_close'].date() if pd.notna(r['window_close']) else None,
        r['Drawn to Date'],
        pct_complete,
        r['remaining_gwp'],
        r['proj_remaining'],
        r['rate_fwd'],
    ]
    for col, (val, fmt) in enumerate(zip(vals, NFMT), 1):
        c = ws.cell(row, col, val)
        c.font = font
        c.fill = fill
        c.alignment = Alignment(horizontal='left', vertical='center')
        if fmt != '@' and val is not None and not isinstance(val, str):
            c.number_format = fmt
    row += 1

# Subtotals
def add_subtotal(ws, row_idx, label, sub):
    active = sub[~sub['is_disposed']]
    tot_gwp   = active['Total GWP'].sum()
    tot_drawn = active['Drawn to Date'].sum()
    vals = [f'TOTAL — {label}  (active only)', '', '', '',
            tot_gwp, None, None,
            tot_drawn,
            tot_drawn / tot_gwp * 100 if tot_gwp > 0 else 0,
            active['remaining_gwp'].sum(),
            None, None]
    for col, (val, fmt) in enumerate(zip(vals, NFMT), 1):
        c = ws.cell(row_idx, col, val)
        c.font = BOLD
        c.fill = TOT_FILL
        c.alignment = Alignment(horizontal='left', vertical='center')
        if fmt != '@' and val is not None and not isinstance(val, str):
            c.number_format = fmt

row += 1
add_subtotal(ws, row,   'CO',       df[df['Stream']=='CO'])
add_subtotal(ws, row+1, 'INJ',      df[df['Stream']=='INJ'])
add_subtotal(ws, row+2, 'COMBINED', df)

# Column widths
for i, w in enumerate([14,10,14,34,14,13,15,18,11,15,22,20], 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# ── Projection tab ────────────────────────────────────────────────────────────
ws2 = wb.create_sheet('Projection (Liam TMRV-674)')
for col, h in enumerate(['Month', 'Projected Gross CDR (MT bio-oil)'], 1):
    c = ws2.cell(1, col, h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal='center')
for r, (_, p) in enumerate(proj.iterrows(), 2):
    ws2.cell(r, 1, p['month'].date()).number_format = 'YYYY-MM-DD'
    ws2.cell(r, 2, p['mt']).number_format          = '#,##0.0'
ws2.column_dimensions['A'].width = 14
ws2.column_dimensions['B'].width = 32
ws2.freeze_panes = 'A2'

wb.save(OUTPUT)
print(f"Saved → {OUTPUT}")
print(f"Assets: {len(df)} total  ({(~df['is_disposed']).sum()} active, {df['is_disposed'].sum()} disposed)")
print(f"CO active: {((df['Stream']=='CO') & ~df['is_disposed']).sum()}")
print(f"INJ active: {((df['Stream']=='INJ') & ~df['is_disposed']).sum()}")

# Quick sanity check on a known asset
chk = df[df['Asset ID']=='EE-CO-001'].iloc[0]
print(f"\nSanity check EE-CO-001 (Peanut Wagon):")
print(f"  Total GWP:        {chk['Total GWP']:.2f} kg")
print(f"  Drawn to Date:    {chk['Drawn to Date']:.2f} kg  (tDBM method)")
print(f"  Expected by Now:  {chk['expected']:.2f} kg  (injection-pace)")
print(f"  Behind (kg):      {chk['behind_kg']:.2f}  (negative = ahead)")
print(f"  % of schedule:    {chk['pct_done']:.1f}%")
