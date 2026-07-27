#!/usr/bin/env python3
"""EE CDR Delivery Monitor — actual vs. Liam projection schedule"""

import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE   = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/.playwright-mcp'
OUTPUT = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/EE_CDR_Monitor_v1.xlsx'

LAST_ACTUAL_MONTH = pd.Timestamp('2026-04-01')  # last closed RP

# ── Projection ────────────────────────────────────────────────────────────────
proj_raw = pd.read_csv(f'{BASE}/Master-EE-UoP-Amortization-CO-Injection---Projection.csv',
    header=None, skiprows=5, usecols=[0,1], names=['month','mt'])
proj_raw = proj_raw[proj_raw['month'].astype(str).str.match(r'^\d{4}-\d{2}', na=False)].copy()
proj_raw['month'] = pd.to_datetime(proj_raw['month'])
proj_raw['mt'] = pd.to_numeric(proj_raw['mt'].astype(str).str.replace(',',''), errors='coerce').fillna(0)
# CSV has two sections (INJ then CO tDBM) with same date column — keep INJ (first occurrence)
proj_raw = proj_raw.drop_duplicates(subset=['month'], keep='first')
proj_dict = dict(zip(proj_raw['month'], proj_raw['mt']))

# ── RP actuals — hard-coded from Historical Actuals tab ───────────────────────
rp_data = [
    ('Mini RP',    '2025-08-11', '2025-08-15',  162.188),
    ('Aug-Sep RP', '2025-08-16', '2025-09-08',  280.091),
    ('Sep RP',     '2025-09-09', '2025-09-30',  351.137),
    ('Oct-Nov RP', '2025-10-01', '2025-11-06',  574.730),
    ('Nov-Jan RP', '2025-11-07', '2026-01-31',  157.040),
    ('Feb-Mar RP', '2026-02-01', '2026-03-02',  864.000),
    ('Mar RP',     '2026-03-03', '2026-03-31',  711.760),
    ('Apr RP',     '2026-04-01', '2026-04-30',  578.837),
]
rps = pd.DataFrame(rp_data, columns=['rp','start','end','mt'])
rps['start'] = pd.to_datetime(rps['start'])
rps['end']   = pd.to_datetime(rps['end'])
rps['days']  = (rps['end'] - rps['start']).dt.days + 1

def month_actual(month_ts):
    """Day-weighted allocation of closed RP totals to a calendar month."""
    m_end = month_ts + pd.offsets.MonthEnd(0)
    total = 0.0
    for _, rp in rps.iterrows():
        ov_s = max(rp['start'], month_ts)
        ov_e = min(rp['end'],   m_end)
        if ov_e >= ov_s:
            total += rp['mt'] * ((ov_e - ov_s).days + 1) / rp['days']
    return round(total, 3) if total > 0 else None

# ── Build row data ────────────────────────────────────────────────────────────
months = pd.date_range('2025-08-01', '2030-12-01', freq='MS')
rows = []
for m in months:
    sched  = proj_dict.get(m, 0.0)
    actual = month_actual(m) if m <= LAST_ACTUAL_MONTH else None
    delta  = round(actual - sched, 3) if actual is not None else None
    rows.append({'month': m, 'year': m.year, 'scheduled': sched, 'actual': actual, 'delta': delta})

df = pd.DataFrame(rows)

# Cumulative columns (running from Jan 2025 through last actual)
cs, ca = 0.0, 0.0
cumul_s, cumul_a, cumul_d = [], [], []
for _, r in df.iterrows():
    cs += r['scheduled']
    cumul_s.append(round(cs, 1))
    if pd.notna(r['actual']):
        ca += r['actual']
        cumul_a.append(round(ca, 1))
        cumul_d.append(round(ca - cs, 1))
    else:
        cumul_a.append(None)
        cumul_d.append(None)

df['cumul_scheduled'] = cumul_s
df['cumul_actual']    = cumul_a
df['cumul_delta']     = cumul_d

# ── Annual rollup ─────────────────────────────────────────────────────────────
annual = []
for yr, grp in df.groupby('year'):
    sched     = grp['scheduled'].sum()
    act_rows  = grp[grp['actual'].notna()]
    n_months  = len(grp)
    actual    = act_rows['actual'].sum() if len(act_rows) > 0 else None
    delta     = round(actual - sched, 1) if actual is not None else None
    pct       = round(actual / sched * 100, 1) if (actual is not None and sched > 0) else None
    partial   = len(act_rows) < n_months
    annual.append({'year': yr, 'scheduled': round(sched,1), 'actual': actual,
                   'delta': delta, 'pct': pct, 'partial': partial})
annual = pd.DataFrame(annual)

# ── Styles ────────────────────────────────────────────────────────────────────
wb = Workbook()

HDR_FILL   = PatternFill('solid', fgColor='1F3864')
YR_FILL    = PatternFill('solid', fgColor='D6DCE4')
FUT_FILL   = PatternFill('solid', fgColor='F7F7F7')
ANN_FILL   = PatternFill('solid', fgColor='2E75B6')
WHITE_FILL = PatternFill('solid', fgColor='FFFFFF')
HDR_FONT   = Font(name='Calibri', bold=True, color='FFFFFF', size=10)
YR_FONT    = Font(name='Calibri', bold=True, size=10)
ANN_FONT   = Font(name='Calibri', bold=True, color='FFFFFF', size=10)
NORM       = Font(name='Calibri', size=10)
FUTURE     = Font(name='Calibri', size=10, color='AAAAAA')
CENTER     = Alignment(horizontal='center', vertical='center')
RIGHT      = Alignment(horizontal='right',  vertical='center')
LEFT       = Alignment(horizontal='left',   vertical='center')
N1 = '#,##0.0'
N0 = '#,##0'

thin = Side(style='thin', color='CCCCCC')
BORDER = Border(bottom=thin)

def cell(ws, row, col, val=None, font=None, fill=None, fmt=None, align=None):
    c = ws.cell(row, col, val)
    if font:  c.font  = font
    if fill:  c.fill  = fill
    if fmt:   c.number_format = fmt
    if align: c.alignment = align
    return c

# ── Tab 1: Monthly CDR Monitor ────────────────────────────────────────────────
ws = wb.active
ws.title = 'CDR Monitor'
ws.freeze_panes = 'A3'

# Note
note = (f'Schedule: Liam TMRV-674 annual projections ÷ 12 (flat monthly)  |  '
        f'Actuals: day-weighted from closed RPs  |  '
        f'Last closed: Apr 2026  |  '
        f'Cumulative runs from Jan 2025')
ws.merge_cells('A1:H1')
c = ws.cell(1, 1, note)
c.font = Font(name='Calibri', italic=True, size=9, color='555555')
c.alignment = LEFT
ws.row_dimensions[1].height = 15

# Header
COLS = ['Month', 'Year', 'Scheduled (MT)', 'Actual (MT)', 'Monthly Delta (MT)',
        'Cumul. Scheduled (MT)', 'Cumul. Actual (MT)', 'Cumul. Delta (MT)']
for i, h in enumerate(COLS, 1):
    c = ws.cell(2, i, h)
    c.font = HDR_FONT; c.fill = HDR_FILL
    c.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
ws.row_dimensions[2].height = 32

# Data rows — group by year
row = 3
prev_year = None

for _, r in df.iterrows():
    yr = r['year']
    is_future = r['actual'] is None and r['month'] > LAST_ACTUAL_MONTH
    font = FUTURE if is_future else NORM
    fill = FUT_FILL if is_future else WHITE_FILL

    # Year separator label
    if yr != prev_year:
        for c_idx in range(1, 9):
            c = ws.cell(row, c_idx)
            c.fill = YR_FILL
            c.font = YR_FONT
        ws.cell(row, 1, str(yr)).font = YR_FONT
        ws.cell(row, 1).fill = YR_FILL
        ws.cell(row, 1).alignment = LEFT
        ws.row_dimensions[row].height = 14
        row += 1
        prev_year = yr

    vals = [
        r['month'].strftime('%b %Y'),
        None,
        r['scheduled'],
        r['actual'],
        r['delta'],
        r['cumul_scheduled'],
        r['cumul_actual'],
        r['cumul_delta'],
    ]
    for c_idx, val in enumerate(vals, 1):
        c = ws.cell(row, c_idx, val)
        c.font = font; c.fill = fill
        c.alignment = RIGHT if c_idx > 1 else LEFT
        if c_idx >= 3 and val is not None:
            c.number_format = N1
    row += 1

# Widths
for i, w in enumerate([14, 7, 17, 14, 20, 22, 20, 20], 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# ── Tab 2: Annual Rollup ──────────────────────────────────────────────────────
ws2 = wb.create_sheet('Annual Rollup')

ANN_HDRS = ['Year', 'Scheduled (MT)', 'Actual (MT)', 'Delta (MT)', '% of Schedule', 'Note']
for i, h in enumerate(ANN_HDRS, 1):
    c = ws2.cell(1, i, h)
    c.font = HDR_FONT; c.fill = HDR_FILL
    c.alignment = CENTER
ws2.row_dimensions[1].height = 24
ws2.freeze_panes = 'A2'

for row_i, r in enumerate(annual.itertuples(), 2):
    is_fut = r.actual is None
    font   = FUTURE if is_fut else NORM
    note_  = 'partial year' if r.partial and not is_fut else ('' if not is_fut else 'projected only')
    vals   = [r.year, r.scheduled, r.actual, r.delta, r.pct, note_]
    for c_idx, val in enumerate(vals, 1):
        c = ws2.cell(row_i, c_idx, val)
        c.font = font
        c.alignment = CENTER if c_idx != 1 else LEFT
        if c_idx in (2,3,4) and val is not None: c.number_format = N1
        if c_idx == 5 and val is not None: c.number_format = '0.0"%"'

for i, w in enumerate([8, 18, 16, 14, 16, 16], 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

wb.save(OUTPUT)
print(f"Saved → {OUTPUT}")
print("\n=== ANNUAL ROLLUP ===")
print(annual[['year','scheduled','actual','delta','pct']].to_string(index=False))
print("\n=== MONTHLY SAMPLE (Aug 2025 – Apr 2026) ===")
print(df[df['month'] >= '2025-08-01'][['month','scheduled','actual','delta','cumul_delta']].head(12).to_string(index=False))
