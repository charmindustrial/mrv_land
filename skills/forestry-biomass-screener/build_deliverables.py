#!/usr/bin/env python3
"""
build_deliverables.py — THE canonical builder for forestry-biomass pre-screen
deliverables. One code path, so every project gets the identical structure.

DO NOT hand-build a pre-screen report or gap checklist. Assemble the JSON spec
(schema below) and run:

    python3 build_deliverables.py <spec.json> <output_dir>

It writes two files, named identically for every project:
    "<project> — BFA v1.3 Pre-Screen.docx"
    "<project> — BFA v1.3 Gap Checklist.xlsx"

Structure is locked to the skill's defined format (Step 1b + Step 3a):
  Pre-Screen .docx:
    - Title + meta line
    - Nomenclature Consistency table            (Step 1b — mandatory)
    - 1 — Outstanding Documents Required for Validation   (Step 3a §1)
        Must-have  /  Should-have  (each: What it must contain / Format /
                                    Who provides / Source (BFA v1.3))
    - 2 — Evidence Coverage (A.1–A.8)            (Step 3a §2)
        each: BFA requirement / Status / Evidence / Gap
  Gap Checklist .xlsx:
    - "Gap Checklist"     sheet (mirrors §1)
    - "Evidence Coverage" sheet (mirrors §2)
    - "Nomenclature"      sheet (mirrors Step 1b)

NOTHING ELSE. No "Overall Assessment", no "Summary Assessment", no "Evidence
Reviewed" — those were ad-hoc additions that broke templating. If the template
needs to change, change it HERE, once, and every project moves together.

JSON spec schema:
{
  "project": "Quartz Valley Forest Restoration Project",
  "date": "2026-07-08",
  "docs_reviewed": 6,
  "folder_id": "1aSOBRox...",
  "nomenclature": [[canonical, document, name_used, "YES|NO|RECONCILED|N/A", note], ...],
  "must_have":   [{"item","contains","format","who","source"}, ...],
  "should_have": [{"item","contains","format","who","source"}, ...],
  "coverage":    [{"req":"A.1","name":"Feedstock Description","status":"COVERED|PARTIAL|MISSING|N/A",
                   "requirement":"<verbatim BFA>","evidence":"...","gap":""}, ... x8]
}
"""
import json, os, sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HDR = "D6E4F0"
STC = {"COVERED": "1E7B34", "PARTIAL": "B26A00", "MISSING": "B00020", "N/A": "555555"}

def _shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)

def _hdr_table(doc, headers, widths=None):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""
        r = c.paragraphs[0].add_run(h); r.bold = True; _shade(c, HDR)
    return t

def _field(doc, lead, text):
    p = doc.add_paragraph(); r = p.add_run(lead); r.bold = True; p.add_run(text); return p

def build_prescreen(spec, out_dir):
    doc = Document()
    p = doc.add_paragraph(); r = p.add_run(f"{spec['project']} — BFA v1.3 Pre-Screen")
    r.bold = True; r.font.size = Pt(19)
    _field(doc, "", f"Date: {spec['date']}     Documents reviewed: {spec['docs_reviewed']}"
                    f"     Methodology: Biomass Feedstock Accounting v1.3 (Isometric)")

    # Nomenclature Consistency (Step 1b)
    h = doc.add_paragraph(); r = h.add_run("Nomenclature Consistency"); r.bold = True
    r.font.size = Pt(14); r.font.color.rgb = RGBColor.from_string("1F3864")
    t = _hdr_table(doc, ["Canonical name (grant award)", "Document", "Name used", "Match?", "Note"])
    for row in spec.get("nomenclature", []):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = str(v)

    # Section 1
    h = doc.add_paragraph(); r = h.add_run("1 — Outstanding Documents Required for Validation")
    r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RGBColor.from_string("1F3864")
    for label, key in (("Must-have  —  required before validation can proceed", "must_have"),
                       ("Should-have  —  Isometric may flag; submission can proceed", "should_have")):
        sp = doc.add_paragraph(); rr = sp.add_run(label); rr.bold = True
        items = spec.get(key, [])
        if not items:
            doc.add_paragraph("None.", style="List Bullet")
            continue
        for n, it in enumerate(items, 1):
            pp = doc.add_paragraph(style="List Number"); rr = pp.add_run(it["item"]); rr.bold = True
            _field(doc, "What it must contain: ", it.get("contains", ""))
            _field(doc, "Format: ", it.get("format", ""))
            _field(doc, "Who provides it: ", it.get("who", ""))
            _field(doc, "Source (BFA v1.3): ", it.get("source", ""))

    # Section 2
    h = doc.add_paragraph(); r = h.add_run("2 — Evidence Coverage (A.1–A.8)")
    r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RGBColor.from_string("1F3864")
    for c in spec.get("coverage", []):
        pp = doc.add_paragraph(); rr = pp.add_run(f"{c['req']} — {c['name']}"); rr.bold = True
        st = c.get("status", "")
        pp.add_run("    "); s = pp.add_run(st); s.bold = True
        s.font.color.rgb = RGBColor.from_string(STC.get(st, "000000"))
        _field(doc, "BFA requirement: ", c.get("requirement", ""))
        _field(doc, "Evidence: ", c.get("evidence", ""))
        if c.get("gap"):
            _field(doc, "Gap: ", c["gap"])

    name = spec.get("prescreen_filename") or f"{spec['project']} — BFA v1.3 Pre-Screen.docx"
    path = os.path.join(out_dir, name)
    doc.save(path); return path

def build_checklist(spec, out_dir):
    hdrfill = PatternFill("solid", fgColor=HDR); bold = Font(bold=True)
    wrap = Alignment(wrap_text=True, vertical="top")
    thin = Side(style="thin", color="BFBFBF"); bord = Border(thin, thin, thin, thin)
    wb = openpyxl.Workbook()

    # Sheet 1 — Gap Checklist (mirrors §1)
    ws = wb.active; ws.title = "Gap Checklist"
    ws["A1"] = f"Gap Checklist — {spec['project']} — {spec['date']}"; ws["A1"].font = Font(bold=True, size=13)
    ws.append(["Priority", "#", "Item", "What It Must Contain", "Format", "Who Provides", "Source (BFA v1.3)"])
    for c in ws[2]:
        c.font = bold; c.fill = hdrfill; c.alignment = wrap; c.border = bord
    n = 0
    for pri, key in (("MUST-HAVE", "must_have"), ("SHOULD-HAVE", "should_have")):
        for it in spec.get(key, []):
            n += 1
            ws.append([pri, n, it["item"], it.get("contains", ""), it.get("format", ""),
                       it.get("who", ""), it.get("source", "")])
            for c in ws[ws.max_row]:
                c.alignment = wrap; c.border = bord
    for col, w in zip("ABCDEFG", [13, 4, 30, 50, 26, 28, 40]):
        ws.column_dimensions[col].width = w

    # Sheet 2 — Evidence Coverage (mirrors §2)
    s = wb.create_sheet("Evidence Coverage")
    s["A1"] = f"Evidence Coverage — {spec['project']}"; s["A1"].font = Font(bold=True, size=13)
    for k, v in (("Date", spec["date"]),
                 ("Methodology", "Biomass Feedstock Accounting v1.3 (Isometric)"),
                 ("Source folder", spec.get("folder_id", ""))):
        s.append([k, v]); s[s.max_row][0].font = bold
    s.append([])
    s.append(["Requirement", "Name", "Status", "Evidence", "Gap"])
    for c in s[s.max_row]:
        c.font = bold; c.fill = hdrfill; c.border = bord
    for c in spec.get("coverage", []):
        s.append([c["req"], c["name"], c.get("status", ""), c.get("evidence", ""), c.get("gap", "") or "—"])
        for cc in s[s.max_row]:
            cc.alignment = wrap; cc.border = bord
    for col, w in zip("ABCDE", [12, 28, 10, 50, 40]):
        s.column_dimensions[col].width = w

    # Sheet 3 — Nomenclature (mirrors Step 1b)
    nm = wb.create_sheet("Nomenclature")
    nm.append(["Canonical name (grant award)", "Document", "Name used", "Match?", "Note"])
    for c in nm[1]:
        c.font = bold; c.fill = hdrfill; c.border = bord
    for row in spec.get("nomenclature", []):
        nm.append([str(x) for x in row])
        for cc in nm[nm.max_row]:
            cc.alignment = wrap; cc.border = bord
    for col, w in zip("ABCDE", [34, 34, 26, 12, 40]):
        nm.column_dimensions[col].width = w

    name = spec.get("checklist_filename") or f"{spec['project']} — BFA v1.3 Gap Checklist.xlsx"
    path = os.path.join(out_dir, name)
    wb.save(path); return path

def main():
    spec = json.load(open(sys.argv[1]))
    out_dir = sys.argv[2]
    d = build_prescreen(spec, out_dir)
    c = build_checklist(spec, out_dir)
    print("wrote:", os.path.basename(d))
    print("wrote:", os.path.basename(c))

if __name__ == "__main__":
    main()
