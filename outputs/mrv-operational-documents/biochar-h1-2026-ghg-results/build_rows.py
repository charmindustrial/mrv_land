"""Assemble one record per removal from the Certify export.

Read every sheet by explicit row number - the export carries blank spacer
rows, so a filtered list would drift out of step with the row references
the formulas use.
"""
import re, json, collections
import openpyxl
import evalwb as E

SIMPLE = re.compile(r"^=(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_ ]*))!(\$?[A-Z]{1,3}\$?\d+)$")


def text_of(sheet, coord):
    """Follow plain =Sheet!A1 references and return the underlying string."""
    for _ in range(12):
        raw = E.cells.get((sheet, coord.replace('$', '')))
        if not isinstance(raw, str) or not raw.startswith('='):
            return raw
        m = SIMPLE.match(raw)
        if not m:
            return None
        sheet, coord = (m.group(1) or m.group(2)), m.group(3)
    return None


def cols(ws_name):
    return {c.value: c.column_letter for c in E.wb[ws_name][1] if c.value}


# ---- datapoints: row -> (name, value) --------------------------------------
dc = cols('Datapoint')
dp_by_row = {}
for r in range(2, E.wb['Datapoint'].max_row + 1):
    nm = E.cells.get(('Datapoint', f"{dc['Name']}{r}"))
    if nm:
        dp_by_row[r] = (nm, E.cell('Datapoint', f"{dc['Value in SI units']}{r}"))

# ---- expressions: component id -> {datapoint name: value} ------------------
xc = cols('Expression')
cmp_dps = collections.defaultdict(dict)
for r in range(2, E.wb['Expression'].max_row + 1):
    cid = text_of('Expression', f"{xc['Component ID']}{r}")
    if not cid:
        continue
    raw = E.cells.get(('Expression', f"{xc['Result in SI Units']}{r}"))
    if not isinstance(raw, str):
        continue
    for n in re.findall(r'Datapoint!\$?[A-Z]{1,3}\$?(\d+)', raw):
        if int(n) in dp_by_row:
            nm, val = dp_by_row[int(n)]
            cmp_dps[cid][nm] = val

# ---- components, keyed by their real sheet row -----------------------------
gc = cols('GHG Entry Component')
comps_by_row = {}
for r in range(2, E.wb['GHG Entry Component'].max_row + 1):
    rid = E.cells.get(('GHG Entry Component', f"{gc['GHG Entry Component ID']}{r}"))
    if not rid:
        continue
    comps_by_row[r] = {
        'row': r,
        'rvc_id': rid,
        'cmp_id': text_of('GHG Entry Component', f"{gc['Component ID']}{r}"),
        'entry_id': text_of('GHG Entry Component', f"{gc['GHG Entry ID']}{r}"),
        'name': E.cells.get(('GHG Entry Component', f"{gc['Component name']}{r}")),
        'group': E.cells.get(('GHG Entry Component', f"{gc['GHG Entry Component Group Name']}{r}")),
        'type': E.cells.get(('GHG Entry Component', f"{gc['GHG Entry Component Type']}{r}")),
        'flux': E.cell('GHG Entry Component', f"{gc['Attributed Carbon Flux in kg']}{r}"),
        'unc': E.cell('GHG Entry Component', f"{gc['CO₂e uncertainty (kg)']}{r}"),
        'attr': E.cell('GHG Entry Component', f"{gc['Attribution Factor']}{r}"),
    }

by_entry = collections.defaultdict(list)
for c in comps_by_row.values():
    by_entry[c['entry_id']].append(c)

# ---- entries ---------------------------------------------------------------
ec = cols('GHG Entry')
COMPONENT_COLUMNS = [
    'Biochar sequestration, 200 year durability',
    'Biochar Production Emission (A)',
    'Over Allocated Emissions',
    'Biochar Spreading Emissions',
    'CO Flatbed Truck Transport Process Emissions',
    'CO Flatbed Truck Transport Embodied Emissions',
    'BCU - Transport Process',
]
DATAPOINT_COLUMNS = [
    'Biochar Applied (wet mass) (Spreading) - Applied',
    'Biochar Dry Weight (kg) (CO2 stored) - Applied',
    'Biochar Dry Product Weight (kg) (Pyrolysis) - Applied',
    'Biochar Transported (kg) - Applied',
    'Organic Carbon Content % - Applied',
    'Inorganic Carbon Content % - Applied',
    'Biochar - H/C_org - Applied',
    'Biochar Applied - Soil Temperature (Cel)',
    'Biochar Applied - Delivery Distance (km)',
    'Biochar Applied - Allocated Delivery Distance (km)',
    'Biochar Output - Carbon Intensity - Applied',
    'Emissions Factor - Biochar Spreading',
    'Copy - Truck EF',
    'Constant CO₂ reduction',
]

out = []
for r in range(2, E.wb['GHG Entry'].max_row + 1):
    eid = E.cells.get(('GHG Entry', f"{ec['GHG Entry ID']}{r}"))
    if not eid:
        continue
    comps = by_entry.get(eid, [])
    rec = {
        'ghg_entry_id': eid,
        'supplier_ref': E.cells.get(('GHG Entry', f"{ec['Supplier reference ID']}{r}")),
        'date': E.cells.get(('GHG Entry', f"{ec['Date GHG entry started']}{r}")),
        'gross_certify': E.cell('GHG Entry', f"{ec['CO₂e gross removed (kg)']}{r}"),
        'emitted_certify': E.cell('GHG Entry', f"{ec['CO₂e emitted (kg)']}{r}"),
        'reductions_certify': E.cell('GHG Entry', f"{ec['Reductions CO₂e flux (kg)']}{r}"),
        'uncertainty_certify': E.cell('GHG Entry', f"{ec['CO₂e uncertainty discount (kg)']}{r}"),
        'net_certify': E.cell('GHG Entry', f"{ec['Discounted CO₂e net removed (kg)']}{r}"),
        'net_rounded_certify': E.cell('GHG Entry', f"{ec['Discounted CO₂e net removed, rounded (kg)']}{r}"),
        'n_components': len(comps),
    }
    for name in COMPONENT_COLUMNS:
        rec[name] = sum(c['flux'] for c in comps if c['name'] == name)
    rec['_unc_sum'] = sum(c['unc'] for c in comps)
    dpmap = {}
    for c in comps:
        dpmap.update(cmp_dps.get(c['cmp_id'], {}))
    for name in DATAPOINT_COLUMNS:
        rec[name] = dpmap.get(name)
    rec['_groups'] = sorted({(c['name'], c['group']) for c in comps})
    rec['_missing_dp'] = [n for n in DATAPOINT_COLUMNS if dpmap.get(n) is None]
    out.append(rec)

if __name__ == '__main__':
    json.dump(out, open('rows.json', 'w'), indent=1, default=str)
    print(f'{len(out)} removals -> rows.json')
    bad = 0
    for r in out:
        em = (r['Biochar Production Emission (A)'] + r['Over Allocated Emissions']
              + r['Biochar Spreading Emissions'] + r['CO Flatbed Truck Transport Process Emissions']
              + r['CO Flatbed Truck Transport Embodied Emissions'])
        net = r['Biochar sequestration, 200 year durability'] - em + r['BCU - Transport Process']
        for label, mine, theirs in (('emitted', em, r['emitted_certify']),
                                    ('gross', r['Biochar sequestration, 200 year durability'], r['gross_certify']),
                                    ('reduct', r['BCU - Transport Process'], r['reductions_certify']),
                                    ('net', net, r['net_certify'])):
            if abs(mine - theirs) > 0.005:
                bad += 1
                print(f"  MISMATCH {r['ghg_entry_id']} {label}: mine {mine:.3f} vs certify {theirs:.3f}")
    print('components reconcile to Certify entry totals' if not bad else f'{bad} mismatches')
    miss = {n for r in out for n in r['_missing_dp']}
    print('datapoints never resolved:', sorted(miss) or 'none')
