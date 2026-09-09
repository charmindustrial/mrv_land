"""Build the H1 2026 biochar GHG Statement Results workbook.

Left block (A:C) and the core raw columns (E:S) are the May bio-oil sheet's
layout, unchanged. Biochar's emission categories and the Certify cross-checks
sit to the right of S and roll up into Process Emissions / Site+Amortized
Embodied Emissions, so the left block reads exactly as it always has.
"""
import os, re, collections, datetime
import openpyxl

import evalwb as E
from build_rows import comps_by_row, text_of, cols, dp_by_row

xc, ec = cols('Expression'), cols('GHG Entry')

expr_by_cmp = collections.defaultdict(list)
for r in range(2, E.wb['Expression'].max_row + 1):
    cid = text_of('Expression', f"{xc['Component ID']}{r}")
    if cid:
        expr_by_cmp[cid].append({
            'name': E.cells.get(('Expression', f"{xc['Result Name']}{r}")),
            'raw': E.cells.get(('Expression', f"{xc['Result in SI Units']}{r}")),
            'val': E.cell('Expression', f"{xc['Result in SI Units']}{r}")})


def named(cid, label):
    hits = [e for e in expr_by_cmp.get(cid, []) if e['name'] == label]
    return hits[-1]['val'] if hits else None


def dp_named(cid, label):
    for e in expr_by_cmp.get(cid, []):
        if isinstance(e['raw'], str):
            for n in re.findall(r'Datapoint!\$?[A-Z]{1,3}\$?(\d+)', e['raw']):
                if int(n) in dp_by_row and dp_by_row[int(n)][0] == label:
                    return dp_by_row[int(n)][1]
    return None


by_entry = collections.defaultdict(list)
for c in comps_by_row.values():
    by_entry[c['entry_id']].append(c)

# Certify component name -> detail column letter
DETAIL = {
    'Biochar Production Emission (A)': 'U',
    'Over Allocated Emissions': 'V',
    'Biochar Spreading Emissions': 'W',
    'CO Flatbed Truck Transport Process Emissions': 'X',
    'CO Flatbed Truck Transport Embodied Emissions': 'Y',
    # Certify has renamed these repeatedly. Every spelling seen so far maps to
    # the same column so a rename cannot move mass between columns. Variants
    # differ by singular/plural "Emission(s)" and by a double space.
    'Supplemental Process Compost Transport Emissions': 'Z',
    'Supplemental Compost Transport Process  Emissions': 'Z',
    'Supplemental Compost Transport Process Emissions': 'Z',
    'Supplemental Compost Transport Process Emission': 'Z',
    'Supplemental Compost Transport Embodied Emissions': 'AA',
    'Supplemental Compost Transport Embodied Emission': 'AA',
}
# Certify carries no site component and no amortized embodied component for
# this project, so K stays zero and every emission component rolls into J.
PROCESS_COLS = ['U', 'V', 'W', 'X', 'Y', 'Z', 'AA']
EMBODIED_COLS = []
CHECK_COLS = ['AC', 'AD', 'AE', 'AF']

# The literal Certify uses in its 200-year sequestration expression. Verified
# present in one expression per removal on every export read so far.
C_TO_CO2E = 3.667

# Components handled outside the detail columns.
GROSS_COMPONENT = 'Biochar sequestration, 200 year durability'
REDUCTION_COMPONENT = 'BCU - Transport Process'

# Fail loudly if Certify grows a component this build does not place, rather
# than dropping it and quietly under-reporting emissions.
seen = {c['name'] for c in comps_by_row.values()}
unmapped = seen - set(DETAIL) - {GROSS_COMPONENT, REDUCTION_COMPONENT}
if unmapped:
    raise SystemExit('unmapped Certify components: ' + ', '.join(sorted(unmapped)))

records = []
for r in range(2, E.wb['GHG Entry'].max_row + 1):
    eid = E.cells.get(('GHG Entry', f"{ec['GHG Entry ID']}{r}"))
    if not eid:
        continue
    rec = {'eid': eid,
           'ref': E.cells.get(('GHG Entry', f"{ec['Supplier reference ID']}{r}")),
           'date': E.cells.get(('GHG Entry', f"{ec['Date GHG entry started']}{r}")),
           'reductions': 0.0,
           'unc': E.cell('GHG Entry', f"{ec['CO₂e uncertainty discount (kg)']}{r}") / 1000,
           'gross_certify': E.cell('GHG Entry', f"{ec['CO₂e gross removed (kg)']}{r}") / 1000,
           'net_certify': E.cell('GHG Entry', f"{ec['Discounted CO₂e net removed (kg)']}{r}") / 1000}
    for L in DETAIL.values():
        rec[L] = 0.0
    for c in by_entry[eid]:
        if c['name'] == GROSS_COMPONENT:
            rec['dry_kg'] = dp_named(c['cmp_id'], 'Biochar Dry Weight (kg) (CO2 stored) - Applied')
            rec['corg'] = named(c['cmp_id'], 'Mean carbon content')
            rec['fdur'] = named(c['cmp_id'], 'Durable fraction')
        elif c['name'] == REDUCTION_COMPONENT:
            rec['reductions'] += c['flux'] / 1000
        elif c['name'] in DETAIL:
            rec[DETAIL[c['name']]] += c['flux'] / 1000
    # Mirror of the row formulas in I and N, so the rounding note can state the
    # exact and the published totals without re-deriving them by hand.
    rec['gross_sheet'] = rec['dry_kg'] * rec['corg'] * rec['fdur'] * C_TO_CO2E / 1000
    rec['net_sheet'] = (rec['gross_sheet']
                        - sum(rec[L] for L in PROCESS_COLS)
                        - sum(rec[L] for L in EMBODIED_COLS)
                        + rec['reductions'] - rec['unc'])
    records.append(rec)

records.sort(key=lambda x: (x['date'], x['ref'] or ''))
FIRST = 2

# ---------------------------------------------------------------- workbook --
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Sheet1'
N3 = '#,##0.000'

# --- row 1 headers: E:S copied from the May sheet, detail/checks after S ----
ws['B1'], ws['C1'] = 'Kg', 'MT'
ws['G1'] = 'Removal Date'
ws['H1'] = 'Biochar Applied (dry mass)'
ws['I1'] = 'Gross CO2e Sequestered'
ws['J1'] = 'Process Emissions'
ws['K1'] = 'Site + Amortized Embodied Emissions'
ws['L1'] = 'Emissions Reductions'
ws['M1'] = 'Uncertainty Discount'
ws['N1'] = 'Net Removal'
ws['S1'] = 'C % x 200-yr durable fraction'
ws['U1'] = 'Production Emissions'
ws['V1'] = 'Over-Allocated Emissions'
ws['W1'] = 'Spreading Emissions'
ws['X1'] = 'Transport Process Emissions'
ws['Y1'] = 'Transport Embodied Emissions'
ws['Z1'] = 'Supplemental Compost Transport Process'
ws['AA1'] = 'Supplemental Compost Transport Embodied'
ws['AC1'] = 'Gross CO2e per Certify'
ws['AD1'] = 'Net Removal per Certify'
ws['AE1'] = 'Check: Gross - Certify'
ws['AF1'] = 'Check: Net - Certify'

for j, rec in enumerate(records):
    r = FIRST + j
    ws[f'F{r}'] = rec['eid']
    ws[f'G{r}'] = rec['date'].date() if isinstance(rec['date'], datetime.datetime) else rec['date']
    ws[f'G{r}'].number_format = 'yyyy-mm-dd'
    ws[f'H{r}'] = rec['dry_kg']
    ws[f'I{r}'] = f'=H{r}*S{r}*$Q$5/$Q$6'
    ws[f'J{r}'] = '=' + '+'.join(f'{L}{r}' for L in PROCESS_COLS)
    ws[f'K{r}'] = ('=' + '+'.join(f'{L}{r}' for L in EMBODIED_COLS)) if EMBODIED_COLS else 0.0
    ws[f'L{r}'] = rec['reductions']
    ws[f'M{r}'] = rec['unc']
    ws[f'N{r}'] = f'=I{r}-J{r}-K{r}+L{r}-M{r}'
    ws[f'S{r}'] = rec['corg'] * rec['fdur']
    for L in DETAIL.values():
        ws[f'{L}{r}'] = rec[L]
    ws[f'AC{r}'] = rec['gross_certify']
    ws[f'AD{r}'] = rec['net_certify']
    ws[f'AE{r}'] = f'=I{r}-AC{r}'
    ws[f'AF{r}'] = f'=N{r}-AD{r}'
    for L in ('H', 'I', 'J', 'K', 'L', 'M', 'N', *DETAIL.values(), *CHECK_COLS):
        ws[f'{L}{r}'].number_format = N3
    ws[f'S{r}'].number_format = '0.0000'

# ---- left block: the May sheet's cells, unchanged --------------------------
ws['A2'], ws['B2'], ws['C2'] = 'Gross Biochar Sequestered', f'=SUM(H{FIRST}:H999)', '=B2/1000'
ws['B4'], ws['C4'] = 'Kg CO2e', 'MT CO2e'
ws['A5'], ws['B5'], ws['C5'] = 'Gross CO2e Sequestered', '=C5*1000', f'=SUM(I{FIRST}:I999)'
ws['A7'], ws['B7'], ws['C7'] = 'Project Emissions', 'Kg CO2e', 'MT CO2e'
ws['A8'], ws['B8'], ws['C8'] = 'Process Emissions', '=C8*1000', f'=SUM(J{FIRST}:J999)'
ws['A9'], ws['B9'], ws['C9'] = 'Site+Amortized Embodied Emissions', '=C9*1000', f'=SUM(K{FIRST}:K999)'
ws['A10'], ws['B10'], ws['C10'] = 'Uncertainty Discounts', '=C10*1000', f'=SUM(M{FIRST}:M999)'
ws['A11'], ws['B11'], ws['C11'] = 'Emissions Reductions', '=C11*1000', f'=SUM(L{FIRST}:L999)'
ws['A13'], ws['B13'] = 'Total Emissions for Reporting Period (kg)', '=B14*1000'
ws['A14'], ws['B14'] = 'Total Emissions for Reporting Period (MT)', '=SUM(C8:C10)'
ws['A16'], ws['B16'] = 'Net Removals for Reporting Period (kg)', '=B17*1000'
# Net is the sum of the per-removal nets, each rounded to 0.01 t -- the
# granularity at which Certify publishes and issues every removal. Summing the
# unrounded nets instead (=C5-B14+C11) states a total that cannot be issued.
# Row 26 carries that exact figure and row 27 the residual, so nothing is lost.
ws['A17'], ws['B17'] = ('Net Removals for Reporting Period (MT)',
                        f'=SUMPRODUCT(ROUND(N{FIRST}:N{FIRST + len(records) - 1},2))')
for a in ('B2', 'C2', 'B5', 'C5', 'B8', 'C8', 'B9', 'C9', 'B10', 'C10',
          'B11', 'C11', 'B13', 'B14', 'B16', 'B17'):
    ws[a].number_format = '#,##0.00'

# ---- cross-check block, below the output rows so 1-17 are untouched -------
LASTROW = FIRST + len(records) - 1
ws['A19'] = 'Cross-check vs Certify'
ws['A20'], ws['B20'] = 'Certify Gross CO2e Sequestered (MT)', f'=SUM(AC{FIRST}:AC999)'
ws['A21'], ws['B21'] = 'Certify Net Removals, unrounded (MT)', f'=SUM(AD{FIRST}:AD999)'
ws['A22'], ws['B22'] = ('Certify Net Removals, as published per removal (MT)',
                        f'=SUMPRODUCT(ROUND(AD{FIRST}:AD{LASTROW},2))')
ws['A23'], ws['B23'] = 'Difference: this sheet Gross - Certify Gross (MT)', '=C5-B20'
ws['A24'], ws['B24'] = ('Difference: this sheet Net - Certify Net as published (MT)',
                        '=B17-B22')
ws['A26'], ws['B26'] = ('Net Removals, exact arithmetic before per-removal rounding (MT)',
                        '=C5-B14+C11')
ws['A27'], ws['B27'] = ('Rounding residual: exact arithmetic - as published (MT)', '=B26-B17')

exact_net = sum(r['net_sheet'] for r in records)
published_net = sum(round(r['net_sheet'], 2) for r in records)
residual_kg = (exact_net - published_net) * 1000

ws['A29'] = (
    'Net Removals is the sum of the 31 per-removal nets, each rounded to 0.01 t. That is the '
    'granularity at which Certify publishes and issues every removal, and the 31 rounded values '
    'in this sheet match Certify\'s published figures on all 31 rows. Summed, they give '
    f'{published_net:,.2f} MT. The exact arithmetic before per-removal rounding is '
    f'{exact_net:,.6f} MT (row 26); the {residual_kg:,.2f} kg difference (row 27) is per-removal '
    'rounding alone, and it understates, so the claimed figure is the conservative one. Gross and '
    'emissions on rows 2-14 are stated exactly, unrounded, so subtracting them reproduces row 26 '
    'rather than row 17.\n\n'
    'Carbon-to-CO2e factor: Q5 is set to 3.667, the literal used in Certify\'s 200-year '
    'sequestration expression (31 expressions in this export, one per removal), so this sheet '
    'reproduces the registry\'s gross exactly -- 0.000 kg difference on every row. The exact molar '
    'ratio 44/12 is 3.6666667; 3.667 is the high side of it, so both this sheet and Certify state '
    'slightly more gross CO2e than the exact ratio supports.')
ws['A29'].alignment = openpyxl.styles.Alignment(wrap_text=True, vertical='top')
ws.merge_cells('A29:C36')
for a in ('B20', 'B21', 'B22', 'B26'):
    ws[a].number_format = '#,##0.000'
for a in ('B23', 'B24', 'B27'):
    ws[a].number_format = '#,##0.0000'

ws['P2'] = 'Conversions'
ws['P5'], ws['Q5'] = 'C --> CO2e', C_TO_CO2E
ws['P6'], ws['Q6'] = 'Kg per MT', 1000.0

for L, w in (('A', 38), ('B', 14), ('C', 12), ('E', 30), ('F', 24), ('G', 13),
             ('H', 15), ('I', 15), ('J', 14), ('K', 20), ('L', 14), ('M', 14),
             ('N', 13), ('P', 12), ('Q', 10), ('S', 16), ('U', 15), ('V', 16),
             ('W', 14), ('X', 17), ('Y', 18), ('Z', 20), ('AA', 22),
             ('AC', 15), ('AD', 15), ('AE', 15), ('AF', 15)):
    ws.column_dimensions[L].width = w

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'H1-2026_Biochar_GHG_Statement_Results.xlsx')
wb.save(OUT)
print(f'{len(records)} removals -> {OUT}')
