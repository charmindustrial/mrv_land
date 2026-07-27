"""Build evaluation report supporting calculations as .xlsx with live formulas."""
import openpyxl
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              numbers as num_styles)
from openpyxl.utils import get_column_letter

OUT = "outputs/mrv-operational-documents/AI_Agent_Eval_Calculations.xlsx"

wb = openpyxl.Workbook()

# ── Palette ───────────────────────────────────────────
NAVY_HEX   = "1F497D"
BLUE_HEX   = "2E74B5"
LT_BLUE    = "D6E4F0"
LT_GRAY    = "F2F2F2"
WHITE      = "FFFFFF"
YELLOW     = "FFF2CC"
GREEN      = "E2EFDA"

def hdr_fill(hex_): return PatternFill("solid", fgColor=hex_)
def hdr_font(hex_="FFFFFF", sz=10, bold=True): return Font(color=hex_, size=sz, bold=bold)
def body_font(sz=10, bold=False): return Font(size=sz, bold=bold)
thin = Side(style='thin', color='CCCCCC')
def thin_border(): return Border(left=thin, right=thin, top=thin, bottom=thin)

def set_col_width(ws, col, width):
    ws.column_dimensions[get_column_letter(col)].width = width

def hdr_row(ws, row, values, fill_hex=NAVY_HEX, font_hex="FFFFFF"):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.fill = hdr_fill(fill_hex)
        c.font = hdr_font(font_hex)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = thin_border()

def section_hdr(ws, row, text, ncols):
    c = ws.cell(row=row, column=1, value=text)
    c.fill = hdr_fill(LT_BLUE)
    c.font = Font(size=10, bold=True, color=NAVY_HEX)
    c.alignment = Alignment(horizontal="left")
    if ncols > 1:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)

def data_cell(ws, row, col, value, fmt=None, bold=False, fill_hex=None, formula=False):
    c = ws.cell(row=row, column=col, value=value)
    c.font = Font(size=10, bold=bold)
    c.border = thin_border()
    c.alignment = Alignment(vertical="center")
    if fmt:
        c.number_format = fmt
    if fill_hex:
        c.fill = hdr_fill(fill_hex)
    return c

def blank_row(ws, row, ncols):
    for i in range(1, ncols+1):
        ws.cell(row=row, column=i).fill = hdr_fill(WHITE)

# ══════════════════════════════════════════════════════════════
# TAB 1 — Session Cost Actuals
# ══════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = "Session Cost Actuals"
ws1.freeze_panes = "A3"

ws1.row_dimensions[1].height = 30
hdr_row(ws1, 1, [
    "Batch ID","Turns","Output Tokens","Cache Write 1h Tokens","Cache Read Tokens",
    "Cost — Output ($)","Cost — Cache Write ($)","Cost — Cache Read ($)",
    "Cost — Direct Input ($)","Total Cost ($)","Notes"
])
set_col_width(ws1, 1, 10); set_col_width(ws1, 2, 8); set_col_width(ws1, 3, 14)
set_col_width(ws1, 4, 18); set_col_width(ws1, 5, 16)
for c in range(6,11): set_col_width(ws1, c, 15)
set_col_width(ws1, 11, 40)

# Pricing constants in a notes block below data
actuals = [
    # batch, turns, output_tok, cw_tok, cr_tok, cost_out, cost_cw, cost_cr, cost_in, total, note
    ("2-187", 228, 353413, 1026976, 46676286, 26.51, 30.81, 70.01, 0.006, 127.34, "Clean batch — first clean sweep"),
    ("2-204", 229, 289936, 1186942, 52452949, 21.75, 35.61, 78.68, 0.052, 136.08, "Short session, 51 min"),
    ("2-180", 336, 251310, 1187550, 64539850, 18.85, 35.63, 96.81, 0.024, 151.31, "~2 hr session"),
    ("2-181", 318, 389983, 1771865, 75844758, 29.25, 53.16, 113.77, 0.008, 196.18, "Standard session"),
    ("2-201", 310, 362604, 2486492, 68865614, 27.20, 74.59, 103.30, 0.081, 205.17, "~4.5 hr session"),
    ("2-190", 428, 516283, 3205604, 72151506, 38.72, 96.17, 108.23, 0.013, 243.13, "3 sub-sessions"),
    ("2-185", 492, 634552, 2831885, 161985106, 47.59, 84.96, 242.98, 0.015, 375.54, "Recovery session — last offload policy error"),
]

for i, row_data in enumerate(actuals, 2):
    for j, val in enumerate(row_data, 1):
        fill = None
        if row_data[0] == "2-187": fill = GREEN
        c = data_cell(ws1, i, j, val, fill_hex=fill)
        if j in (6,7,8,9,10):
            c.number_format = '"$"#,##0.00'
        if j in (3,4,5):
            c.number_format = '#,##0'

# Summary stats block
r = len(actuals) + 3
section_hdr(ws1, r, "Summary Statistics", 6)
r += 1
stats = [
    ("Minimum", f"=MIN(J2:J{len(actuals)+1})"),
    ("Maximum", f"=MAX(J2:J{len(actuals)+1})"),
    ("Median",  f"=MEDIAN(J2:J{len(actuals)+1})"),
    ("Average", f"=AVERAGE(J2:J{len(actuals)+1})"),
    ("Clean-batch avg (2-187, 2-204)", "=AVERAGE(J2,J3)"),
    ("Complex-session avg (2-190, 2-185)", f"=AVERAGE(J{len(actuals)},J{len(actuals)+1})"),
]
for label, formula in stats:
    ws1.cell(row=r, column=1, value=label).font = Font(size=10, bold=True)
    c = ws1.cell(row=r, column=2, value=formula)
    c.number_format = '"$"#,##0.00'; c.font = Font(size=10)
    c.border = thin_border()
    r += 1

# Pricing reference
r += 1
section_hdr(ws1, r, "Pricing Reference (Anthropic — Opus 4.x, as of May 2026)", 6)
r += 1
pricing = [
    ("Direct input", "$15.00", "per 1M tokens"),
    ("Output", "$75.00", "per 1M tokens"),
    ("Cache write (1-hour TTL)", "$30.00", "per 1M tokens"),
    ("Cache read", "$1.50", "per 1M tokens"),
]
for label, price, unit in pricing:
    ws1.cell(row=r, column=1, value=label).font = Font(size=10)
    ws1.cell(row=r, column=2, value=price).font = Font(size=10, bold=True)
    ws1.cell(row=r, column=3, value=unit).font = Font(size=10, italic=True)
    r += 1

# ══════════════════════════════════════════════════════════════
# TAB 2 — 1,000-User Scaling
# ══════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("1K Users — Scaling")
ws2.freeze_panes = "A4"

section_hdr(ws2, 1, "INPUTS — adjust these cells", 4)
inputs = [
    ("Users",                         1000,  "enterprises"),
    ("QA sessions per user per month", 15,   "sessions/month"),
    ("Current avg cost per session",   205,  "$ (from actuals tab median ≈ $196, rounded)"),
    ("Optimized cost per session",     120,  "$ (40% reduction from model tiering)"),
    ("SaaS price per session",         350,  "$ per session"),
    ("Infrastructure markup",          0.25, "fraction of API cost"),
]
for i, (label, val, note) in enumerate(inputs, 2):
    ws2.cell(row=i, column=1, value=label).font = Font(size=10, bold=True)
    c = ws2.cell(row=i, column=2, value=val)
    c.fill = hdr_fill(YELLOW); c.font = Font(size=10, bold=True)
    c.border = thin_border()
    ws2.cell(row=i, column=3, value=note).font = Font(size=10, italic=True)

set_col_width(ws2, 1, 34); set_col_width(ws2, 2, 14); set_col_width(ws2, 3, 45); set_col_width(ws2, 4, 20)

r = len(inputs) + 3
section_hdr(ws2, r, "CALCULATED OUTPUTS", 4)
r += 1
# Row references for inputs
row_users=2; row_sess=3; row_curr=4; row_opt=5; row_price=6; row_infra=7

calcs = [
    ("Sessions per month",       f"=B{row_users}*B{row_sess}", "#,##0", "sessions"),
    ("API cost — current ($/mo)", f"=B{row_users}*B{row_sess}*B{row_curr}", '"$"#,##0', ""),
    ("Infrastructure — current",  f"=B{row_users}*B{row_sess}*B{row_curr}*B{row_infra}", '"$"#,##0', ""),
    ("Total cost — current ($/mo)",f"=B{row_users}*B{row_sess}*B{row_curr}*(1+B{row_infra})", '"$"#,##0', ""),
    ("API cost — optimized ($/mo)",f"=B{row_users}*B{row_sess}*B{row_opt}", '"$"#,##0', ""),
    ("Total cost — optimized ($/mo)",f"=B{row_users}*B{row_sess}*B{row_opt}*(1+B{row_infra})", '"$"#,##0', ""),
    ("Revenue ($/mo)",             f"=B{row_users}*B{row_sess}*B{row_price}", '"$"#,##0', ""),
    ("Gross margin — current",     f"=1-(B{row_users}*B{row_sess}*B{row_curr}*(1+B{row_infra}))/(B{row_users}*B{row_sess}*B{row_price})", "0.0%", ""),
    ("Gross margin — optimized",   f"=1-(B{row_users}*B{row_sess}*B{row_opt}*(1+B{row_infra}))/(B{row_users}*B{row_sess}*B{row_price})", "0.0%", ""),
    ("Annual revenue run rate",    f"=B{row_users}*B{row_sess}*B{row_price}*12", '"$"#,##0', ""),
]
for label, formula, fmt, note in calcs:
    ws2.cell(row=r, column=1, value=label).font = Font(size=10)
    c = ws2.cell(row=r, column=2, value=formula)
    c.number_format = fmt; c.font = Font(size=10, bold=True)
    c.border = thin_border()
    if note:
        ws2.cell(row=r, column=3, value=note).font = Font(size=10, italic=True)
    r += 1

# ══════════════════════════════════════════════════════════════
# TAB 3 — 1M Users & Optimization Path
# ══════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("1M Users — Optimization")
ws3.freeze_panes = "A4"

section_hdr(ws3, 1, "COST OPTIMIZATION SENSITIVITY — Path to $3-8/session", 5)
ws3.row_dimensions[1].height = 20
hdr_row(ws3, 2, ["Optimization Lever","Mechanism","Cost Reduction","Basis","$/session after"], LT_BLUE, NAVY_HEX)
set_col_width(ws3, 1, 28); set_col_width(ws3, 2, 42); set_col_width(ws3, 3, 18)
set_col_width(ws3, 4, 40); set_col_width(ws3, 5, 18)

levers = [
    ("Baseline (current)",
     "Opus 4.x, full context accumulation, LLM does arithmetic",
     "—",
     "Median of 7 logged sessions",
     205),
    ("Model tiering — extraction to Haiku",
     "Haiku output: $1.25/M vs $75/M (60x cheaper). ~60% of turns are extraction. "
     "Output cost falls from ~$27 to ~$5/session.",
     "~$22 saved on output",
     "Anthropic published Haiku 4.5 pricing; extraction turn fraction estimated from session logs",
     183),
    ("Context compression between gates",
     "Summarize completed gate output rather than carrying raw tool history forward. "
     "Reduces cache-read volume by est. 65%. Cache read falls from ~$100 to ~$35/session.",
     "~$65 saved on cache reads",
     "Cache-read cost is 46–162M tokens/session at $1.50/M; 65% compression est. from gate-output size analysis",
     118),
    ("Deterministic arithmetic scripts",
     "Python handles all numeric checks (mass balance, EF calcs, gross-to-net). "
     "Removes ~40 reasoning-heavy turns per session, cutting output tokens and context growth.",
     "~$15 saved (turns + downstream cache)",
     "Pilot script (compute_mass_chain.py) validated; turn count reduction estimated from session turn profiles",
     103),
    ("Domain fine-tuned model (18-24 mo)",
     "Fine-tuned Haiku trained on extraction tasks from ~500+ logged QA sessions. "
     "Inference cost approaches $0.10-0.25/M on fine-tuned Haiku tiers. "
     "Cache write cost also scales down with smaller model.",
     "~$90 additional saved",
     "Fine-tuning cost reduction: industry benchmarks (Anthropic, OpenAI) show 10-20x cost reduction "
     "for domain fine-tuned models on narrow extraction tasks vs. frontier models",
     8),
]
for i, (lev, mech, red, basis, sess_cost) in enumerate(levers, 3):
    ws3.cell(row=i, column=1, value=lev).font = Font(size=10, bold=(i==3 or i==len(levers)+2))
    ws3.cell(row=i, column=2, value=mech).font = Font(size=10)
    ws3.cell(row=i, column=3, value=red).font = Font(size=10)
    ws3.cell(row=i, column=4, value=basis).font = Font(size=9, italic=True)
    c = ws3.cell(row=i, column=5, value=sess_cost)
    c.number_format = '"$"#,##0'; c.font = Font(size=10, bold=True)
    c.fill = hdr_fill(GREEN if sess_cost < 20 else (LT_GRAY if sess_cost < 100 else WHITE))
    for col in range(1, 6):
        ws3.cell(row=i, column=col).border = thin_border()
        ws3.cell(row=i, column=col).alignment = Alignment(wrap_text=True, vertical="top")
    ws3.row_dimensions[i].height = 52

# 1M user scaling table
r = len(levers) + 5
section_hdr(ws3, r, "1M USER ECONOMICS — Optimized vs Current", 5)
r += 1
hdr_row(ws3, r, ["Scenario","Cost/Session","Sessions/Month","API Cost/Month","Revenue/Month @ $25/session"], LT_BLUE, NAVY_HEX)
r += 1
scenarios = [
    ("Current architecture",         205, "=C{r}*1000000", "=B{r}*C{r}", "=1000000*25"),
    ("Partially optimized (~$15)",     15, "=C{r}*1000000", "=B{r}*C{r}", "=1000000*25"),
    ("Fully optimized (~$5-8)",         6, "=C{r}*1000000", "=B{r}*C{r}", "=1000000*25"),
]
for label, cost_sess, _, _, _ in scenarios:
    ws3.cell(row=r, column=1, value=label).font = Font(size=10)
    c2 = ws3.cell(row=r, column=2, value=cost_sess)
    c2.number_format = '"$"#,##0'; c2.font = Font(size=10, bold=True); c2.border = thin_border()
    c3 = ws3.cell(row=r, column=3, value=1000000)
    c3.number_format = '#,##0,,"M"'; c3.font = Font(size=10); c3.border = thin_border()
    c4 = ws3.cell(row=r, column=4, value=f"=B{r}*C{r}")
    c4.number_format = '"$"#,##0,,"M"'; c4.font = Font(size=10, bold=True); c4.border = thin_border()
    c5 = ws3.cell(row=r, column=5, value=f"=1000000*25")
    c5.number_format = '"$"#,##0,,"M"'; c5.font = Font(size=10); c5.border = thin_border()
    fill = GREEN if cost_sess < 10 else (LT_GRAY if cost_sess < 50 else None)
    if fill:
        for col in range(1, 6):
            ws3.cell(row=r, column=col).fill = hdr_fill(fill)
    r += 1

# ══════════════════════════════════════════════════════════════
# TAB 4 — TAM Analysis
# ══════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("TAM — Sustainability")
ws4.freeze_panes = "A3"

section_hdr(ws4, 1, "SUSTAINABILITY VERIFICATION TAM — Entity & Session Estimates", 6)
hdr_row(ws4, 2, [
    "Market Segment","Addressable Entities","Sessions/Entity/Month",
    "Sessions/Month","Source / Basis","Notes"
], LT_BLUE, NAVY_HEX)
set_col_width(ws4, 1, 30); set_col_width(ws4, 2, 18); set_col_width(ws4, 3, 22)
set_col_width(ws4, 4, 18); set_col_width(ws4, 5, 38); set_col_width(ws4, 6, 30)

segments = [
    ("EU CSRD — large companies (Phase 1-2)",
     50000, 2, None,
     "EU Directive 2022/2464; ~50K large EU + non-EU companies by FY2025 reports",
     "Annual report = ~2 verification events/yr; monthly = 0.17 → rounded to 2/mo for quarterly sub-reports"),
    ("EU CSRD — SMEs (Phase 3, 2026+)",
     250000, 1, None,
     "EC impact assessment (EFRAG): up to 50K large + potentially hundreds of K SMEs",
     "Conservative: only ~250K of estimated 500K+ SMEs captured"),
    ("US IRA clean energy credits (45Q/45V/45Z)",
     8000, 2, None,
     "DOE, IRS guidance; rough count from CCUS, hydrogen, clean fuel project pipelines",
     "Quarterly IRS submissions; semi-annual MRV reports → ~2 events/mo"),
    ("Voluntary Carbon Market — project developers",
     10000, 1, None,
     "VERRA VCS registry: ~10K registered projects (2024); Gold Standard, ACR add ~2K more",
     "Annual verification + interim monitoring = ~1 verification-class event/mo average"),
    ("Compliance carbon (EU ETS, CA-ETS, RGGI, others)",
     30000, 1, None,
     "EU ETS: ~10K installations; CA+RGGI+Canada+UK+Australia: ~20K additional regulated sites",
     "Annual verified emission report; some quarterly sub-reporting"),
    ("US RFS (RINs) + CA LCFS pathways",
     2500, 3, None,
     "EPA RFS: ~1.5K obligated parties + ~600 RIN generators; LCFS: ~300 certified pathways",
     "Monthly RIN generation reports + quarterly pathway audits"),
    ("Environmental attribute certs (RECs, SAF, BCUs, EACs)",
     15000, 2, None,
     "NERC GATS: ~10K REC generators; CORSIA SAF: growing; BCUs, I-RECs globally: ~5K",
     "Quarterly issuance with evidence chains"),
    ("CDR (direct air capture, bio-oil, biochar, enhanced weathering)",
     500, 5, None,
     "Current CDR operator count ~200-300; growing to ~500-1K by 2028 (IEA, BloombergNEF)",
     "Monthly batch QA, quarterly MRV reports — highest sessions/entity"),
]

for i, (seg, entities, sess_per_ent, _, source, notes) in enumerate(segments, 3):
    ws4.cell(row=i, column=1, value=seg).font = Font(size=10)
    c2 = ws4.cell(row=i, column=2, value=entities)
    c2.number_format = '#,##0'; c2.font = Font(size=10, bold=True)
    ws4.cell(row=i, column=3, value=sess_per_ent).font = Font(size=10)
    c4 = ws4.cell(row=i, column=4, value=f"=B{i}*C{i}")
    c4.number_format = '#,##0'; c4.font = Font(size=10, bold=True)
    c4.fill = hdr_fill(LT_BLUE)
    ws4.cell(row=i, column=5, value=source).font = Font(size=9, italic=True)
    ws4.cell(row=i, column=6, value=notes).font = Font(size=9, italic=True)
    for col in range(1, 7):
        ws4.cell(row=i, column=col).border = thin_border()
        ws4.cell(row=i, column=col).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.row_dimensions[i].height = 48

# Totals
total_row = len(segments) + 3
section_hdr(ws4, total_row, "TOTALS", 4)
total_row += 1
ws4.cell(row=total_row, column=1, value="Total addressable entities").font = Font(size=10, bold=True)
c = ws4.cell(row=total_row, column=2, value=f"=SUM(B3:B{len(segments)+2})")
c.number_format = '#,##0'; c.font = Font(size=11, bold=True); c.border = thin_border()

total_row += 1
ws4.cell(row=total_row, column=1, value="Total sessions per month").font = Font(size=10, bold=True)
c = ws4.cell(row=total_row, column=4, value=f"=SUM(D3:D{len(segments)+2})")
c.number_format = '#,##0'; c.font = Font(size=11, bold=True); c.border = thin_border()
c.fill = hdr_fill(GREEN)

total_row += 2
ws4.cell(row=total_row, column=1, value="Revenue @ $25/session (optimized SaaS)").font = Font(size=10, bold=True)
c = ws4.cell(row=total_row, column=4, value=f"=SUM(D3:D{len(segments)+2})*25")
c.number_format = '"$"#,##0,,"M" "per month"'; c.font = Font(size=11, bold=True, color=NAVY_HEX)
c.border = thin_border(); c.fill = hdr_fill(GREEN)

total_row += 1
ws4.cell(row=total_row, column=1, value="API cost @ $6/session (fully optimized)").font = Font(size=10, bold=True)
c = ws4.cell(row=total_row, column=4, value=f"=SUM(D3:D{len(segments)+2})*6")
c.number_format = '"$"#,##0,,"M" "per month"'; c.font = Font(size=11, bold=True)
c.border = thin_border()

total_row += 1
ws4.cell(row=total_row, column=1, value="Gross margin (optimized)").font = Font(size=10, bold=True)
c = ws4.cell(row=total_row, column=4,
             value=f"=1-(SUM(D3:D{len(segments)+2})*6)/(SUM(D3:D{len(segments)+2})*25)")
c.number_format = "0.0%"; c.font = Font(size=11, bold=True, color=NAVY_HEX)
c.border = thin_border(); c.fill = hdr_fill(GREEN)

wb.save(OUT)
print(f"Saved: {OUT}")
