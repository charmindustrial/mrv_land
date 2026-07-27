#!/usr/bin/env python3
"""
PDD change-log tool — on-demand, standalone-tracker workflow.

Detects what changed in the PDD between edits and appends draft rows to a
running change-log spreadsheet. You supply the rationale and the
temporary/permanent call; the tool supplies date, section, and old->new text.

Commands
--------
  init    Snapshot the current PDD as the baseline and create the tracker
          (run once, or after a verified version is locked).
  log     Diff the current PDD against the baseline, print a report, and append
          one Draft row per change to the tracker. Does NOT move the baseline.
  accept  Re-baseline: snapshot the current PDD as the new baseline. Run this
          once you've reviewed the report and the draft rows are in the tracker,
          so the same edits don't show up again next time.

Why three commands: `log` is safe to run as often as you like (read-only on the
baseline). Only `accept` advances the baseline, so you stay in control of when
a set of edits is considered "logged."

Paths are configured below; override the PDD with --pdd if you move it.
"""
import argparse, json, os, re, shutil, sys, datetime, difflib

# ---- configuration ---------------------------------------------------------
# Max versions the PDD by making a NEW .docx with a bumped name (e.g. "Draft V 1.13 …",
# "Final V 1.13 …") and editing that. So we don't hardcode a filename — we auto-pick
# the most recently modified PDD .docx in the folder as "the current working version".
# Override anytime with --pdd "<path>".
PDD_FOLDER = ("/Users/maxlavine/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/"
              "My Drive/MRV/PDDs+Supplemental Docs")
WORKDIR  = os.path.join(PDD_FOLDER, "PDD Change Log")
BASELINE_DIR = os.path.join(WORKDIR, "baseline")
BASELINE     = os.path.join(BASELINE_DIR, "PDD_baseline.docx")
META         = os.path.join(BASELINE_DIR, "baseline_meta.json")
TRACKER      = os.path.join(WORKDIR, "PDD_Change_Log.xlsx")

HEADERS = ["Date", "PDD Version", "Section", "Change",
           "Old → New", "Rationale", "Temporary / Permanent", "Status"]

# ---- helpers ---------------------------------------------------------------
def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()

def _version_from_name(path):
    m = re.search(r"\bV\s*([0-9]+(?:\.[0-9]+)*)", os.path.basename(path))
    return m.group(1) if m else ""

def resolve_current(explicit=None):
    """Return the path to the current working PDD. If --pdd was given, use it;
    otherwise pick the most recently modified PDD .docx in PDD_FOLDER (so the
    tool follows whatever new version file you're editing). The baseline copy
    lives in a subfolder and is never picked up by this top-level scan."""
    if explicit:
        return explicit
    import glob
    cands = [f for f in glob.glob(os.path.join(PDD_FOLDER, "*.docx"))
             if not os.path.basename(f).startswith("~$")
             and re.search(r"PDD", os.path.basename(f), re.I)
             and re.search(r"Charm", os.path.basename(f), re.I)]
    if not cands:
        sys.exit(f"No PDD .docx found in {PDD_FOLDER}. Pass --pdd \"<path>\".")
    return max(cands, key=os.path.getmtime)

_TOC_LEADER = re.compile(r"(…|\.{3,})\s*\d*\s*$")

def classify_heading(style_name, text):
    """Return ('top', text) | ('sub', text) | None.

    The PDD styles every section/appendix heading as 'Heading 3' and only the
    document title as 'Heading 1', so Word's heading levels are not usable.
    We classify by text pattern instead:
      - 'Section X' / 'Appendix N' (and the 'E – ...' shorthand) = top level
      - other heading-styled or numbered lines = sub level
      - Table-of-Contents lines (dotted leaders / trailing page numbers) = skip
      - the document title = skip (not a section)
    """
    t = (text or "").strip()
    if not t or len(t) > 110:
        return None
    if _TOC_LEADER.search(t) or t == "Table of Contents":
        return None  # TOC entry
    if re.match(r"^Appendix\s+\d+\b", t):
        return ("top", t)
    if re.match(r"^Section\s+[A-Z]\b", t) or re.match(r"^[A-Z]\s+[–-]\s", t):
        return ("top", t)
    styled = bool(style_name and style_name.startswith("Heading"))
    if styled or re.match(r"^\d+(?:\.\d+)+\b", t):
        if style_name == "Title":
            return None
        return ("sub", t)
    return None

def linearize(docx_path):
    """Ordered list of content units across paragraphs AND table cells, each
    tagged with the section breadcrumb in force at that point."""
    from docx import Document
    from docx.oxml.ns import qn
    from docx.text.paragraph import Paragraph
    from docx.table import Table
    doc = Document(docx_path)
    section, subsection = "", ""
    units = []

    def emit(text, kind):
        nonlocal section, subsection
        t = _norm(text)
        if not t:
            return
        crumb = section + (" › " + subsection if subsection else "")
        units.append({"section": crumb or "(document start)", "text": t, "kind": kind})

    def handle_paragraph(p):
        nonlocal section, subsection
        raw = p.text
        kind = classify_heading(p.style.name if p.style else "", raw)
        if kind:
            level, t = kind
            if level == "top":
                section, subsection = _norm(t), ""
            else:
                subsection = _norm(t)
            return  # headings anchor the breadcrumb; not diffed as content
        emit(raw, "para")

    def handle_table(tbl):
        for row in tbl.rows:
            seen = []
            for cell in row.cells:
                ct = _norm(cell.text)
                if ct and (not seen or seen[-1] != ct):
                    seen.append(ct)
                    emit(cell.text, "cell")

    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            handle_paragraph(Paragraph(child, doc))
        elif child.tag == qn("w:tbl"):
            handle_table(Table(child, doc))
    return units

def _sentence_subdiff(old, new, limit=240):
    """For a modified unit, surface just the sentences that differ."""
    split = lambda s: [x.strip() for x in re.split(r"(?<=[.;:])\s+", s) if x.strip()]
    o, n = split(old), split(new)
    sm = difflib.SequenceMatcher(None, o, n)
    rem, add = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            rem += o[i1:i2]
        if tag in ("replace", "insert"):
            add += n[j1:j2]
    def clip(parts):
        s = " ".join(parts)
        return (s[:limit] + "…") if len(s) > limit else s
    return clip(rem), clip(add)

def diff_units(base, cur):
    """Return change records comparing baseline units to current units."""
    b_text = [u["text"] for u in base]
    c_text = [u["text"] for u in cur]
    sm = difflib.SequenceMatcher(None, b_text, c_text, autojunk=False)
    changes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            # pair up modified units; surface sentence-level deltas
            old_units, new_units = base[i1:i2], cur[j1:j2]
            for k in range(max(len(old_units), len(new_units))):
                ou = old_units[k] if k < len(old_units) else None
                nu = new_units[k] if k < len(new_units) else None
                if ou and nu:
                    ratio = difflib.SequenceMatcher(None, ou["text"], nu["text"]).ratio()
                    if ratio < 0.3:
                        # unrelated lines that happen to be adjacent: don't call it an edit
                        changes.append({"type": "Removed", "section": ou["section"],
                                        "old": ou["text"], "new": ""})
                        changes.append({"type": "Added", "section": nu["section"],
                                        "old": "", "new": nu["text"]})
                    else:
                        o, n = _sentence_subdiff(ou["text"], nu["text"])
                        changes.append({"type": "Modified", "section": nu["section"],
                                        "old": o or "(wording changed)", "new": n or "(wording changed)"})
                elif nu:
                    changes.append({"type": "Added", "section": nu["section"],
                                    "old": "", "new": nu["text"]})
                else:
                    changes.append({"type": "Removed", "section": ou["section"],
                                    "old": ou["text"], "new": ""})
        elif tag == "insert":
            for u in cur[j1:j2]:
                changes.append({"type": "Added", "section": u["section"], "old": "", "new": u["text"]})
        elif tag == "delete":
            for u in base[i1:i2]:
                changes.append({"type": "Removed", "section": u["section"], "old": u["text"], "new": ""})
    return changes

def _clip(s, n=400):
    s = s or ""
    return (s[:n] + "…") if len(s) > n else s

# ---- tracker ---------------------------------------------------------------
def ensure_tracker():
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    if os.path.exists(TRACKER):
        return
    wb = Workbook(); ws = wb.active; ws.title = "Change Log"
    blue = PatternFill("solid", fgColor="D6E4F0")
    bold = Font(bold=True)
    thin = Side(style="thin", color="BBBBBB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    # legend row
    ws["A1"] = ("PDD Change Log — feeds Section F.1 (narrative) and the appendix Document Revision tables. "
                "Rows marked Draft were auto-detected; fill Rationale + Temporary/Permanent, then set Status to Logged.")
    ws["A1"].font = Font(italic=True, color="555555")
    ws.merge_cells("A1:H1")
    for c, h in enumerate(HEADERS, start=1):
        cell = ws.cell(row=2, column=c, value=h)
        cell.font = bold; cell.fill = blue; cell.border = border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    widths = [12, 12, 28, 40, 60, 34, 20, 12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64+i)].width = w
    ws.freeze_panes = "A3"
    wb.save(TRACKER)

def append_rows(rows, version):
    from openpyxl import load_workbook
    from openpyxl.styles import Alignment, Font
    try:
        wb = load_workbook(TRACKER)
    except PermissionError:
        sys.exit("Tracker is open/locked. Close it in Excel/Sheets and re-run `log`.")
    ws = wb["Change Log"]
    today = datetime.date.today().strftime("%-m/%-d/%y")
    start = ws.max_row + 1
    for r in rows:
        oldnew = (f"OLD: {_clip(r['old'])}\nNEW: {_clip(r['new'])}" if r["type"] == "Modified"
                  else (f"ADDED: {_clip(r['new'])}" if r["type"] == "Added" else f"REMOVED: {_clip(r['old'])}"))
        ws.append([today, version, r["section"], r["type"], oldnew, "", "", "Draft"])
        for c in range(1, 9):
            ws.cell(row=ws.max_row, column=c).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(TRACKER)
    return start

# ---- commands --------------------------------------------------------------
def cmd_init(args):
    pdd = resolve_current(args.pdd)
    os.makedirs(BASELINE_DIR, exist_ok=True)
    shutil.copy2(pdd, BASELINE)
    meta = {"version": _version_from_name(pdd),
            "snapshot_date": datetime.date.today().isoformat(),
            "source": pdd}
    json.dump(meta, open(META, "w"), indent=2)
    ensure_tracker()
    print(f"Baseline set: {os.path.basename(pdd)} (v{meta['version'] or '?'}) @ {meta['snapshot_date']}")
    print(f"Tracker ready: {TRACKER}")

def cmd_log(args):
    if not os.path.exists(BASELINE):
        sys.exit("No baseline yet. Run `init` first.")
    meta = json.load(open(META))
    pdd = resolve_current(args.pdd)
    base, cur = linearize(BASELINE), linearize(pdd)
    changes = diff_units(base, cur)
    print(f"=== PDD CHANGE REPORT — {datetime.date.today().isoformat()} ===")
    print(f"baseline v{meta.get('version','?')} (snapshot {meta.get('snapshot_date','?')})")
    print(f"current : {os.path.basename(pdd)} (v{_version_from_name(pdd) or '?'})")
    if not changes:
        print("No content changes detected."); return
    for r in changes:
        print(f"\n[{r['type']}] {r['section']}")
        if r["old"]: print(f"  - {_clip(r['old'],300)}")
        if r["new"]: print(f"  + {_clip(r['new'],300)}")
    ensure_tracker()
    append_rows(changes, _version_from_name(pdd))
    print(f"\n{len(changes)} draft row(s) appended to: {TRACKER}")
    print("Fill Rationale + Temporary/Permanent, then run `accept` to advance the baseline.")

def cmd_accept(args):
    pdd = resolve_current(args.pdd)
    if not os.path.exists(pdd):
        sys.exit("PDD not found.")
    os.makedirs(BASELINE_DIR, exist_ok=True)
    shutil.copy2(pdd, BASELINE)
    meta = {"version": _version_from_name(pdd),
            "snapshot_date": datetime.date.today().isoformat(),
            "source": pdd}
    json.dump(meta, open(META, "w"), indent=2)
    print(f"Baseline advanced to: {os.path.basename(pdd)} (v{meta['version'] or '?'}) @ {meta['snapshot_date']}")

def main():
    ap = argparse.ArgumentParser(description="PDD change-log tool")
    ap.add_argument("command", choices=["init", "log", "accept"])
    ap.add_argument("--pdd", default=None,
                    help="path to the working PDD (default: newest PDD .docx in the folder)")
    args = ap.parse_args()
    {"init": cmd_init, "log": cmd_log, "accept": cmd_accept}[args.command](args)

if __name__ == "__main__":
    main()
