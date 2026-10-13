#!/usr/bin/env python3
"""Structural QA for the Tier 2 methodology sheet (GHG Statement Emissions Methodology by lifecycle stage).

Rules checked (all set by Max, 2026-09-22 to 2026-09-25):
  MISSING   every row on '2. Shared Facilities Meth.' has a row on each facility tab (4, 6, 8)
  CIRCULAR  a facility cell that points to the shared tab must not land on a shared cell that points back
  DANGLING  a pointer names a tab or row that does not exist
  EMPTY     a named row has an empty cell in a methodology column
  UNCERT    Modifications to Address Uncertainty is the template, a pointer, N/A/None, or a known exemption

Usage: methodology_sheet_qa.py <xlsx path>   (exit 1 if any blocking finding)
"""
import sys, re, openpyxl

SHARED = "2. Shared Facilities Meth."
FACILITY = {"4. Biomass Conv & Pyro. - Charm": 1, "6. Bio-Oil Pre-Processing & Inj": 2}  # OPERATING facilities only; Vaulted (tab 8) is monitoring-only (Max, 2026-09-25)
NOTE_PREFIXES = ("NOTE", "Shared facility", "General ", "Vaulted (")
UNCERT_EXEMPT = ("Vendor LCA", "roll up into the Production Period CI", "used as is", "used as-is",
                 "emission factor source will depend")

def name_of(ws, r):
    v = ws.cell(r, 2).value if ws.title[0] in "5678" else ws.cell(r, 1).value
    return str(v).strip() if v else None

def is_note(ws, r):
    a = ws.cell(r, 1).value
    if bool(a) and str(a).startswith(NOTE_PREFIXES):
        return True
    # a row whose column A cell is merged across the table is a note or section row, not a parameter
    for m in ws.merged_cells.ranges:
        if m.min_row == r and m.min_col == 1 and m.max_col > 2:
            return True
    return False

def main(path):
    wb = openpyxl.load_workbook(path)
    out = []
    shared = wb[SHARED]
    shared_hdr = [c.value for c in shared[1]]
    shared_rows = {str(shared.cell(r, 1).value).strip(): r for r in range(2, shared.max_row + 1)
                   if shared.cell(r, 1).value and not is_note(shared, r)}
    for t, pc in FACILITY.items():
        ws = wb[t]
        names = {str(ws.cell(r, pc).value).strip() for r in range(2, ws.max_row + 1) if ws.cell(r, pc).value}
        for s, sr in shared_rows.items():
            if s not in names:
                out.append(f"MISSING  '{s}' has no row on {t}"); continue
            # where the shared row defers to the facility ("See facility tab"), the facility cell must hold real text
            fr = next(r for r in range(2, ws.max_row + 1) if ws.cell(r, pc).value and str(ws.cell(r, pc).value).strip() == s)
            fhdr = [c.value for c in ws[1]]
            for k, h in enumerate(shared_hdr):
                sv = shared.cell(sr, k + 1).value
                if isinstance(sv, str) and re.match(r"\s*See facility tab", sv, re.I) and h in fhdr:
                    fv = ws.cell(fr, fhdr.index(h) + 1).value
                    if fv in (None, "") or (isinstance(fv, str) and fv.strip().startswith("See ")):
                        out.append(f"DEFERRED {t} row '{s}' [{h}]: shared tab defers to facility but facility cell is {fv!r}")
    ptr = re.compile(r"See ['‘’\"“](\d+\. [^'’\"”]+)['’\"”] tab(?:, row ['‘’\"“](.+?)['’\"”])?")
    titles = {ws.title: ws for ws in wb}
    SKIP = {"8. Stor. Mon. Vaulted KS Non-Op"}  # monitoring-only, not an operating facility; content is Max's call
    for ws in wb:
        if ws.title in SKIP:
            continue
        hdr = [c.value for c in ws[1]]
        for row in ws.iter_rows(min_row=2):
            for c in row:
                if not isinstance(c.value, str):
                    continue
                for m in ptr.finditer(c.value):
                    tgt, trow = m.group(1), m.group(2)
                    if tgt not in titles:
                        out.append(f"DANGLING {ws.title}!{c.coordinate} -> tab '{tgt}' does not exist"); continue
                    tw = titles[tgt]
                    if trow:
                        rows = {str(tw.cell(r, k).value).strip(): r for r in range(2, tw.max_row + 1) for k in (1, 2) if tw.cell(r, k).value}
                        if trow.strip() not in rows:
                            out.append(f"DANGLING {ws.title}!{c.coordinate} -> '{tgt}' row '{trow}' does not exist"); continue
                        h = hdr[c.column - 1]
                        thdr = [x.value for x in tw[1]]
                        if h in thdr:
                            tv = tw.cell(rows[trow.strip()], thdr.index(h) + 1).value
                            if isinstance(tv, str) and re.match(r"\s*See (facility|stage) tab", tv, re.I):
                                out.append(f"CIRCULAR {ws.title}!{c.coordinate} [{h}] -> '{tgt}' row '{trow}' [{h}] = {tv[:60]!r}")
    for ws in wb:
        hdr = [c.value for c in ws[1]]
        ncols = len([h for h in hdr if h])
        ucol = hdr.index("Modifications to Address Uncertainty") + 1 if "Modifications to Address Uncertainty" in hdr else None
        for r in range(2, ws.max_row + 1):
            nm = name_of(ws, r)
            if not nm or is_note(ws, r):
                continue
            empties = [hdr[k] for k in range(ncols) if hdr[k] not in ("Source", "Notes", "Data Quality Assessment", "Justification of Variables and Emission Factors") and ws.cell(r, k + 1).value in (None, "")]
            if empties:
                out.append(f"EMPTY    {ws.title} r{r} '{nm[:40]}': {empties}")
            if ucol:
                v = ws.cell(r, ucol).value
                if isinstance(v, str) and v.strip():
                    s = v.strip()
                    if "maximum allowable error" in s or s.startswith(("See ", "N/A", "None")) or any(e in s for e in UNCERT_EXEMPT):
                        continue
                    out.append(f"UNCERT   {ws.title} r{r} '{nm[:40]}': {s[:80]}")

    # ASYMMETRIC: a parameter on one operating facility tab but not the other (Max 2026-09-25: vendor delivery,
    # waste rows were on tab 6 only). Facility-unique rows are listed in UNIQUE_OK.
    UNIQUE_OK = {"Biomass Transport", "Biomass loading/unloading", "Mass of Dry Biomass Processed",
                 "Stack Emissions from Pyrolysis -- Charm", "Mass of Pyrolysis Products",
                 "Carbon Mass of Pyrolysis Products", "Carbon Intensity of Pyrolysis Products",
                 "Water Transport -- Process Emissions", "Water Transport -- Embodied Emissions", "Thermal Oxidizer Emissions", "Mass of Bio-Oil Injected (MOBI) -- Method 1 (Truck Scale)", "Mass of Bio-Oil Injected (MOBI) -- Method 2 (Flow Meter and Density)",
                 "Injection Pressure", "Emissions from Sample Transport to Lab"}
    fac_names = {}
    for t, pc in FACILITY.items():
        ws = wb[t]
        fac_names[t] = {str(ws.cell(r, pc).value).strip() for r in range(2, ws.max_row + 1) if ws.cell(r, pc).value}
    ts = list(FACILITY)
    for i, t in enumerate(ts):
        other = ts[1 - i]
        for n in sorted(fac_names[t] - fac_names[other]):
            if n not in UNIQUE_OK and not n.startswith("Bio-Oil Injectate Characterization"):
                out.append(f"ASYMMETRIC '{n}' is on {t} but not on {other}: shared method? then it belongs on tab 2 with pointer rows on both")
    # DUPTEXT: identical long non-pointer text on both facility tabs for the same parameter -> should live once on a shared tab
    for n in fac_names[ts[0]] & fac_names[ts[1]]:
        cells = []
        for t, pc in FACILITY.items():
            ws = wb[t]; hdr = [c.value for c in ws[1]]
            r = next(r for r in range(2, ws.max_row + 1) if ws.cell(r, pc).value and str(ws.cell(r, pc).value).strip() == n)
            cells.append({hdr[k]: ws.cell(r, k + 1).value for k in range(len(hdr)) if hdr[k]})
        for h, v in cells[0].items():
            w = cells[1].get(h)
            if isinstance(v, str) and v == w and len(v) > 80 and not v.lstrip().startswith("See "):
                out.append(f"DUPTEXT  '{n}' [{h}] identical on both facility tabs; move to the shared tab and point")

    # AUDIENCE: the sheet is public and verifier-facing (Max, 2026-09-28). No internal references anywhere.
    AUD = re.compile(r"slack|#[a-z0-9-]+-charm|isometric review|seb green|tom sellers|summary table|\btier [0-3]\b(?!:)|as discussed|see above|internal review|kb\b|knowledge base|todo|placeholder|\(2\)\.xlsx", re.I)
    for ws in wb:
        for row in ws.iter_rows(min_row=1):
            for c in row:
                if isinstance(c.value, str) and AUD.search(c.value):
                    out.append(f"AUDIENCE {ws.title}!{c.coordinate}: {c.value[:90]!r} -- internal reference in a public document")
    for line in out:
        print(line)
    print(f"{len(out)} finding(s)")
    return 1 if out else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
