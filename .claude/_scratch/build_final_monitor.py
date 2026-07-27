#!/usr/bin/env python3
"""
EE Amortization Monitor
  Tab 1 — Asset Dashboard: remaining balance, forward rate, window status per asset
  Tab 2 — Monthly Monitor: CDR vs schedule, GWP drawn vs expected, running balance
  Tab 3 — Projection: Liam's monthly numbers

Load order: (1) RPs → derive SNAPSHOT/NEW_START → (2) Projection → (3) Assets
No dates, rates, or volumes are hard-coded. Everything traces to a source CSV.
"""

import pandas as pd
import numpy as np
import re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE   = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/.playwright-mcp'
OUTPUT = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/EE_Monitor_v1.xlsx'

# ── 1. RP ACTUALS — drives SNAPSHOT and NEW_START ─────────────────────────────
# Source: Historical Actuals CSV, INJ section
# INJ RPs all contain "RP" in their name. CO rows use "PP1…" or "Aug 2025…" — filtered out.
hist_raw = pd.read_csv(
    f'{BASE}/Master-EE-UoP-Amortization-CO-Injection---Historical-Actuals.csv',
    header=None, skiprows=4, usecols=[0,1,2,3], names=['rp','start','end','mt'])
hist_raw = hist_raw[hist_raw['start'].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}$', na=False)].copy()
rps = hist_raw[hist_raw['rp'].astype(str).str.contains('RP', na=False)].copy()
rps = rps[rps['mt'].notna() & (rps['mt'].astype(str).str.strip() != '')].copy()
rps['start'] = pd.to_datetime(rps['start'])
rps['end']   = pd.to_datetime(rps['end'])
rps['mt']    = pd.to_numeric(rps['mt'], errors='coerce')
rps = rps.dropna(subset=['mt']).reset_index(drop=True)
rps['days']  = (rps['end'] - rps['start']).dt.days + 1

assert len(rps) > 0,        "No closed INJ RPs in Historical Actuals CSV"
assert rps['mt'].min() > 0, "Zero or negative MT in a closed RP — check source"

# SNAPSHOT = last day of the last closed RP. NEW_START = first day of the next month.
SNAPSHOT  = rps['end'].max().normalize()
NEW_START = (SNAPSHOT + pd.offsets.MonthBegin(1)).normalize()

print(f"Source: Historical-Actuals.csv — {len(rps)} closed INJ RPs")
print(rps[['rp','start','end','mt']].to_string(index=False))
print(f"Snapshot (last closed RP end): {SNAPSHOT.date()}")
print(f"New schedule start:            {NEW_START.date()}")

# ── 2. PROJECTION — Liam's monthly INJ gross removals ────────────────────────
# Source: Projection CSV, INJ section (first occurrence of each month — CSV has two sections)
proj = pd.read_csv(
    f'{BASE}/Master-EE-UoP-Amortization-CO-Injection---Projection.csv',
    header=None, skiprows=5, usecols=[0,1], names=['month','mt'])
proj = proj[proj['month'].astype(str).str.match(r'^\d{4}-\d{2}', na=False)].copy()
proj['month'] = pd.to_datetime(proj['month'])
proj['mt']    = pd.to_numeric(proj['mt'].astype(str).str.replace(',',''), errors='coerce').fillna(0)
proj = proj.drop_duplicates(subset=['month'], keep='first').reset_index(drop=True)
proj_dict = dict(zip(proj['month'], proj['mt']))

assert len(proj) > 0,       "No projection rows loaded"
assert proj['mt'].sum() > 0,"All projected MT are zero — check Projection CSV"

print(f"\nSource: Projection.csv — {len(proj)} months, "
      f"{proj['month'].min().date()} → {proj['month'].max().date()}, "
      f"total {proj['mt'].sum():,.0f} MT")

def sum_proj(start, end):
    """Sum projected MT for months start ≤ month ≤ end."""
    if pd.isna(start) or pd.isna(end): return 0.0
    m1 = pd.Timestamp(start.year, start.month, 1)
    m2 = pd.Timestamp(end.year,   end.month,   1)
    return float(proj.loc[(proj['month'] >= m1) & (proj['month'] <= m2), 'mt'].sum()) if m2 >= m1 else 0.0

# ── 3. ASSETS — inventory + Drawn to Date ────────────────────────────────────
# Source: Combined Amortization History CSV
raw = pd.read_csv(
    f'{BASE}/Master-EE-UoP-Amortization-CO-Injection---Combined-Amortization-History.csv',
    header=None, skiprows=3, low_memory=False)
raw.columns = raw.iloc[0]
df = raw.iloc[1:].reset_index(drop=True)
df = df[df['Asset ID'].astype(str).str.match(r'^EE-', na=False)].copy()
for c in ['Total GWP', 'Drawn to Date']:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(r'[,\s$]', '', regex=True), errors='coerce').fillna(0)
df['Commission']  = pd.to_datetime(df['Commission'], errors='coerce')
df['Disposal']    = pd.to_datetime(df['Disposal'],   errors='coerce')
df['is_disposed'] = df['Disposal'].notna()
df['cutoff']      = df['Commission'].apply(
    lambda d: d + pd.DateOffset(months=59) if pd.notna(d) else pd.NaT)

# Forward calculations — all relative to NEW_START and 5yr cutoff
df['remaining_gwp'] = df['Total GWP'] - df['Drawn to Date']
df['proj_fwd']      = df.apply(lambda r: sum_proj(NEW_START, r['cutoff']), axis=1)
df['rate_fwd']      = np.where(df['proj_fwd'] > 0, df['remaining_gwp'] / df['proj_fwd'], 0.0)
df['pct_done']      = np.where(df['Total GWP'] > 0, df['Drawn to Date'] / df['Total GWP'] * 100, 0.0)
df['window_expired']= df['cutoff'].apply(lambda c: pd.notna(c) and c < NEW_START)
df['closes_in_time']= np.where(
    df['is_disposed'],       'Disposed',
    np.where(df['window_expired'], 'Window expired',
    np.where(df['proj_fwd'] > 0,  'Yes — on projection', 'No CDR in window')))

active = df[~df['is_disposed']].copy()
portfolio_rate = active['rate_fwd'].sum()

assert len(active) > 0,           "No active assets — check Amortization History CSV"
assert active['Total GWP'].sum() > 0, "Total GWP is zero — check source"
assert active['proj_fwd'].sum() > 0,  "No projected CDR in any window — check Projection CSV"

print(f"\nSource: Combined-Amortization-History.csv — {len(active)} active, {df['is_disposed'].sum()} disposed")
print(f"  Total GWP:    {active['Total GWP'].sum():>12,.0f} kg")
print(f"  Drawn to date:{active['Drawn to Date'].sum():>12,.0f} kg")
print(f"  Remaining:    {active['remaining_gwp'].sum():>12,.0f} kg")
print(f"  Portfolio rate: {portfolio_rate:.5f} kg/MT CDR")

# ── 4. MONTHLY CDR — day-weighted allocation of closed RPs to calendar months ─
def month_cdr(m):
    m_end = m + pd.offsets.MonthEnd(0)
    t = 0.0
    for _, rp in rps.iterrows():
        ov_s = max(rp['start'], m)
        ov_e = min(rp['end'],   m_end)
        if ov_e >= ov_s:
            t += rp['mt'] * ((ov_e - ov_s).days + 1) / rp['days']
    return round(t, 3) if t > 0 else None

last_closed_month = pd.Timestamp(rps['end'].max().year, rps['end'].max().month, 1)

# Monitor runs from new schedule start through the last 5yr window across all assets
MONITOR_END = df['cutoff'].dropna().max()

# ── 5. BUILD MONTHLY MONITOR ROWS ────────────────────────────────────────────
mon_months = pd.date_range(NEW_START, MONITOR_END, freq='MS')
mon_rows = []
for m in mon_months:
    sched       = proj_dict.get(m, 0.0)
    actual      = month_cdr(m) if m <= last_closed_month else None
    delta_cdr   = round(actual - sched, 3) if actual is not None else None
    gwp_sched   = round(sched  * portfolio_rate, 1)
    gwp_actual  = round(actual * portfolio_rate, 1) if actual is not None else None
    gwp_delta   = round(gwp_actual - gwp_sched, 1)  if gwp_actual is not None else None
    mon_rows.append({'month': m, 'year': m.year,
                     'sched_cdr': sched,   'actual_cdr': actual,   'delta_cdr': delta_cdr,
                     'gwp_sched': gwp_sched,'gwp_actual': gwp_actual,'gwp_delta': gwp_delta})

mon = pd.DataFrame(mon_rows)

cs, ca, rr = 0., 0., active['remaining_gwp'].sum()
cumul_cs, cumul_ca, cumul_dc, rem_col = [], [], [], []
for _, r in mon.iterrows():
    cs += r['sched_cdr']
    cumul_cs.append(round(cs, 1))
    if pd.notna(r['actual_cdr']):
        # Closed month — use actual draw
        ca  += r['actual_cdr']
        rr  -= r['gwp_actual']
        cumul_ca.append(round(ca, 1))
        cumul_dc.append(round(ca - cs, 1))
    else:
        # Future month — project remaining using scheduled draw
        rr  -= r['gwp_sched']
        cumul_ca.append(None)
        cumul_dc.append(None)
    rem_col.append(round(rr, 1))

mon['cumul_sched']   = cumul_cs
mon['cumul_actual']  = cumul_ca
mon['cumul_delta']   = cumul_dc
mon['gwp_remaining'] = rem_col

# ── 6. BUILD EXCEL ────────────────────────────────────────────────────────────
wb = Workbook()

DARK  = PatternFill('solid', fgColor='1F3864')
MID   = PatternFill('solid', fgColor='2E75B6')
CO_F  = PatternFill('solid', fgColor='EBF5EB')
INJ_F = PatternFill('solid', fgColor='EBF3FB')
DSP_F = PatternFill('solid', fgColor='F2F2F2')
YR_F  = PatternFill('solid', fgColor='E8E8E8')
TOT_F = PatternFill('solid', fgColor='D6DCE4')
WHT   = PatternFill('solid', fgColor='FFFFFF')
FUT_F = PatternFill('solid', fgColor='F7F7F7')

WF = Font(name='Calibri', bold=True, color='FFFFFF', size=10)
BF = Font(name='Calibri', bold=True, size=10)
NF = Font(name='Calibri', size=10)
GF = Font(name='Calibri', size=10, color='AAAAAA')
L  = Alignment(horizontal='left',   vertical='center')
R  = Alignment(horizontal='right',  vertical='center')
C  = Alignment(horizontal='center', vertical='center', wrap_text=True)
N1 = '#,##0.0'
N2 = '#,##0.00'
PCT= '0.0"%"'
DT = 'YYYY-MM-DD'

# ── TAB 1: Asset Dashboard ────────────────────────────────────────────────────
ws1 = wb.active
ws1.title = 'Asset Dashboard'

note1 = (f'Snapshot: {SNAPSHOT.date()}  |  New schedule start: {NEW_START.date()}  |  '
         f'Sources: Combined-Amortization-History.csv, Projection.csv, Historical-Actuals.csv  |  '
         f'Rate = Remaining GWP ÷ projected CDR ({NEW_START.date()} → 5yr cutoff)')
ws1.merge_cells('A1:L1')
ws1.cell(1,1, note1).font = Font(name='Calibri', italic=True, size=9, color='444444')
ws1.cell(1,1).alignment = L

for i, h in enumerate(['Asset ID','Stream','Site','Item Name',
                        'Total GWP\n(kg)','Drawn to Date\n(kg)','% Done',
                        'Remaining\n(kg)','5yr Window\nCloses',
                        'CDR in Window\n(MT projected)','Rate\n(kg/MT CDR)','Status'], 1):
    c = ws1.cell(2,i,h); c.font=WF; c.fill=DARK; c.alignment=C
ws1.row_dimensions[2].height = 36
ws1.freeze_panes = 'A3'

row = 3
for _, r in df.iterrows():
    is_d = r['is_disposed']
    fill = DSP_F if is_d else (CO_F if r['Stream']=='CO' else INJ_F)
    font = GF   if is_d else NF
    vals = [r['Asset ID'], r['Stream']+(' ✕' if is_d else ''), r['Site'], r['Item Name'],
            r['Total GWP'], r['Drawn to Date'], r['pct_done'], r['remaining_gwp'],
            r['cutoff'].date() if pd.notna(r['cutoff']) else None,
            r['proj_fwd'], r['rate_fwd'], r['closes_in_time']]
    fmts = ['@','@','@','@', N2,N2,PCT, N2,DT, N1,'0.00000','@']
    for ci,(val,fmt) in enumerate(zip(vals,fmts),1):
        c = ws1.cell(row,ci,val); c.font=font; c.fill=fill
        c.alignment = L if ci in (1,4,12) else R
        if fmt!='@' and val is not None and not isinstance(val,str): c.number_format=fmt
    row += 1

def subtotal(ws, ri, label, sub):
    act = sub[~sub['is_disposed']]
    tots = ['','','','', act['Total GWP'].sum(), act['Drawn to Date'].sum(),
            act['Drawn to Date'].sum()/act['Total GWP'].sum()*100 if act['Total GWP'].sum()>0 else 0,
            act['remaining_gwp'].sum(), None, act['proj_fwd'].sum(), None, '']
    fmts = ['@','@','@','@', N2,N2,PCT, N2,None, N1,None,'@']
    for ci,(val,fmt) in enumerate(zip(tots,fmts),1):
        c = ws.cell(ri,ci); c.font=BF; c.fill=TOT_F; c.alignment=L if ci==1 else R
        c.value = f'TOTAL — {label}' if ci==1 else val
        if fmt and val is not None and not isinstance(val,str): c.number_format=fmt

row += 1
subtotal(ws1, row,   'CO',         df[df['Stream']=='CO'])
subtotal(ws1, row+1, 'INJ',        df[df['Stream']=='INJ'])
subtotal(ws1, row+2, 'ALL ACTIVE', df)

for i,w in enumerate([14,8,13,34, 14,15,9, 14,14, 20,13,20],1):
    ws1.column_dimensions[get_column_letter(i)].width = w

# ── TAB 2: Monthly Monitor ────────────────────────────────────────────────────
ws2 = wb.create_sheet('Monthly Monitor')

note2 = (f'Opening balance: {active["remaining_gwp"].sum():,.0f} kg remaining as of {SNAPSHOT.date()}  |  '
         f'Portfolio rate: {portfolio_rate:.4f} kg/MT CDR  |  '
         f'CDR actuals from {len(rps)} closed RPs (Historical-Actuals.csv, last: {rps["end"].max().date()})  |  '
         f'Schedule from Projection.csv')
ws2.merge_cells('A1:K1')
ws2.cell(1,1, note2).font = Font(name='Calibri', italic=True, size=9, color='444444')
ws2.cell(1,1).alignment = L

ws2.merge_cells('C2:G2')
ws2.cell(2,3,'GROSS CDR  (MT bio-oil)').font=WF; ws2.cell(2,3).fill=MID; ws2.cell(2,3).alignment=C
ws2.merge_cells('H2:K2')
ws2.cell(2,8,'GWP AMORTIZATION  (kg)').font=WF; ws2.cell(2,8).fill=DARK; ws2.cell(2,8).alignment=C
for ci in [1,2]: ws2.cell(2,ci).fill=DARK
ws2.row_dimensions[2].height=16

for i,h in enumerate(['Month','Year','Scheduled','Actual','Delta',
                       'Cumul. Scheduled','Cumul. Delta',
                       'Expected Draw','Actual Draw','GWP Delta','GWP Remaining'],1):
    c = ws2.cell(3,i,h); c.font=WF; c.fill=DARK
    c.alignment=Alignment(wrap_text=True,horizontal='center',vertical='center')
ws2.row_dimensions[3].height=30
ws2.freeze_panes='A4'

prev_yr, row = None, 4
for _, r in mon.iterrows():
    is_fut = r['actual_cdr'] is None
    fill = FUT_F if is_fut else WHT
    font = GF   if is_fut else NF
    if r['month'].year != prev_yr:
        for ci in range(1,12): ws2.cell(row,ci).fill=YR_F
        ws2.cell(row,1,str(r['month'].year)).font=BF; ws2.cell(row,1).fill=YR_F; ws2.cell(row,1).alignment=L
        ws2.row_dimensions[row].height=13; row+=1; prev_yr=r['month'].year
    vals=[r['month'].strftime('%b %Y'),None,
          r['sched_cdr'],r['actual_cdr'],r['delta_cdr'],r['cumul_sched'],r['cumul_delta'],
          r['gwp_sched'],r['gwp_actual'],r['gwp_delta'],r['gwp_remaining']]
    fmts=['@','@',N1,N1,N1,N1,N1,N1,N1,N1,N1]
    for ci,(val,fmt) in enumerate(zip(vals,fmts),1):
        c=ws2.cell(row,ci,val); c.font=font; c.fill=fill
        c.alignment=L if ci==1 else R
        if fmt!='@' and val is not None and not isinstance(val,str): c.number_format=fmt
    row+=1

for i,w in enumerate([13,6,12,10,10,17,14,16,13,12,16],1):
    ws2.column_dimensions[get_column_letter(i)].width=w

# ── TAB 3: Projection ─────────────────────────────────────────────────────────
ws3 = wb.create_sheet('Projection (Liam)')
ws3.cell(1,1,'Month').font=WF; ws3.cell(1,1).fill=DARK; ws3.cell(1,1).alignment=C
ws3.cell(1,2,'Projected Gross CDR (MT bio-oil)').font=WF; ws3.cell(1,2).fill=DARK; ws3.cell(1,2).alignment=C
for ri,(_, p) in enumerate(proj.iterrows(),2):
    ws3.cell(ri,1,p['month'].date()).number_format=DT
    ws3.cell(ri,2,p['mt']).number_format=N1
ws3.column_dimensions['A'].width=14; ws3.column_dimensions['B'].width=32
ws3.freeze_panes='A2'

wb.save(OUTPUT)
print(f'\nSaved → {OUTPUT}')
