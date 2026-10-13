#!/usr/bin/env python3
"""Ordered Gate 1 re-pass (2026-10-06 21:30Z onward): compares every source re-read after the
guidance re-read with the first-pass values in the source-read log. Writes repass_comparison.json."""
import hashlib, json, warnings
from pathlib import Path
import openpyxl
warnings.filterwarnings("ignore")
B = Path(__file__).resolve().parent; R = B / "source_exports" / "repass"
log = json.loads((B / "batch_INJ-09-2026-W4-KERRY_source_reads.json").read_text())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
out = {}
def txt(name):
    p = R / name; t = p.read_text()
    if t.startswith('"'):
        t = json.loads(t); p.write_text(t)
    return t
# guidance
for m in ("Sep", "Aug", "Jul"):
    out[f"guidance_{m}_identical"] = txt(f"VVB_Guidance_{m}_2026.txt") == (B / "source_exports" / f"VVB_Guidance_{m}_2026.txt").read_text()
# tickets, CoA, CAR-474
out["full_ticket_identical"] = sha(R / "Sept_W4_Full_Scale_Ticket_Kerry.jpg") == sha(B / "screenshots/Sept_W4_Full_Scale_Ticket_Kerry.jpg")
out["empty_ticket_identical"] = sha(R / "Sept_W4_Empty_Scale_Ticket_Kerry.jpg") == sha(B / "screenshots/Sept_W4_Empty_Scale_Ticket_Kerry.jpg")
out["coa_identical"] = sha(R / "SR26-05719-W4-Kerry-AECN-QOWV-COA.pdf") == log["lab_results"]["drive_copy_sha256"]
car = openpyxl.load_workbook(next(R.glob("CAR-474*.xlsx")), data_only=True).active
out["car474_manitowoc"] = [r for r in car.iter_rows(values_only=True) if r[0] == "MANITOWOC CALCINER PHASE"][0][1]
# Ops Notes: every Kerry/Summary/AECN Rail value and every cell note
def cells(p, tabs):
    wv = openpyxl.load_workbook(p, data_only=True); wf = openpyxl.load_workbook(p)
    v = {f"{t}!{c.coordinate}": c.value for t in tabs for row in wv[t].iter_rows() for c in row if c.value is not None}
    n = {f"{ws.title}!{c.coordinate}": c.comment.text for ws in wf.worksheets for row in ws.iter_rows() for c in row if c.comment}
    return v, n
first_v, first_n = cells(B / "source_exports/INJ-09-2026-W4_Ops_Notes_live_20261006T1828Z.xlsx", ["Kerry", "Summary", "AECN Rail"])
re_v, re_n = cells(R / "INJ-09-2026-W4-Ops-Notes.xlsx", ["Kerry", "Summary", "AECN Rail"])
out["ops_notes_value_diffs"] = [[k, first_v.get(k), re_v.get(k)] for k in sorted(set(first_v) | set(re_v)) if first_v.get(k) != re_v.get(k)]
out["ops_notes_note_diffs"] = [k for k in set(first_n) | set(re_n) if first_n.get(k) != re_n.get(k)]
out["ops_notes_kerry_values_checked"] = len([k for k in re_v if k.startswith("Kerry!")])
for wk, first in (("INJ-09-2026-W3", "INJ-09-2026-W3_Ops_Notes_live_20261006T1830Z.xlsx"), ("INJ-09-2026-W2", "INJ-09-2026-W2_Ops_Notes_live_20261006T1830Z.xlsx"),
                  ("INJ-08-2026-W5", "INJ-08-2026-W5_Ops_Notes_live_20261006T1831Z.xlsx")):
    a, an = cells(B / "source_exports/w3_kerry_cross_check" / first, ["Kerry", "Summary"]); b, bn = cells(R / f"{wk}-Ops-Notes.xlsx", ["Kerry", "Summary"])
    out[f"{wk}_kerry_summary_diffs"] = [[k, a.get(k), b.get(k)] for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    out[f"{wk}_note_diffs"] = [k for k in set(an) | set(bn) if an.get(k) != bn.get(k)]
# Standard EFs 2026 tab rows 6 and 11
ef = openpyxl.load_workbook(R / "Standard-Emission-Factors-Calculations.xlsx", data_only=True)["2026"]
out["ef_row6"], out["ef_row11"] = ef["F6"].value, ef["F11"].value
out["ef_identical_to_log"] = (ef["F6"].value == log["standard_efs_2026"]["row6_tanker_fuel_use_mt_per_t_mi"]
                              and ef["F11"].value == log["standard_efs_2026"]["row11_tanker_embodied_mt_per_mi"])
# COBB and Certify text
import re
_strip = lambda t: re.sub(r"Last updated [^\t]*? ago ", "", t)   # tracker header age stamp ("23 hours ago" vs "1 day ago")
out["cobb_identical"] = _strip(txt("COBB_live_calciner_rows.txt")) == _strip((B / "source_exports/COBB_live_calciner_rows_20261006T1842Z.txt").read_text())
out["cobb_note"] = "compared with the tracker's 'Last updated ... ago' header stamp removed; every data row compared"
for f in ("certify_modal_injection_sequestration.txt", "certify_modal_transport_process.txt", "certify_modal_transport_embodied.txt",
          "certify_modal_bcu.txt", "certify_calculation_view.txt", "certify_datapoints_tab.txt", "certify_sources_tab.txt"):
    out[f + "_identical"] = txt(f) == (B / f).read_text()
comp = txt("certify_components_tab.txt")
out["components_tab_has"] = {k: (k in comp) for k in ("37.73 tCO₂e", "19 Sep 2026 to 25 Sep 2026", "38.206 tCO₂e", "2.244 tCO₂e", "0.259 tCO₂e", "4 components")}
w3 = txt("certify_W3_kerry_datapoints_tab.txt")
out["w3_certify_has"] = {k: (k in w3) for k in ("40.19 tCO₂e", "12 Sep 2026 to 18 Sep 2026", "19.155 t", "19.169 t", "Sept_W3_Full_Scale_Ticket_Kerry.pdf", "57.90 %")}

# second re-pass batch (21:46-21:50Z): Certify-attached copies, route map, retirement certificate, W2/W3 tickets,
# Removal-Batch Cross-Reference, Sep W1 and Oct W1 Ops Notes
X = B / "source_exports"
pairs = [(f, f) for f in ("Certify_attached_COA_src_1M3VZ8S8W1S013HS.pdf", "Certify_attached_src_1M3VZ8VKH1S0MRDE_Sept_W4_Full_Scale_Ticket_Kerry.jpg",
          "Certify_attached_src_1M3VZ8XVN1S0W24R_Sept_W4_Empty_Scale_Ticket_Kerry.jpg", "Certify_attached_src_1KT1W9XED1S08J0H_Kerry_to_Basco_Distance.png",
          "Certify_attached_src_1M1MFJPW11S08KY2_Charm-RetirementCertificate-RD-EACs-20251218.pdf", "Certify_attached_StdEFs_src_1KWZ2NVQM1S08AWN.xlsx",
          "Certify_attached_StdEFs_src_1KVJRSYT91S09G2E.xlsx", "Certify_attached_Ops_Notes_src_1M3W1NWED1S0K0MP.xlsx")]
pairs += [(f"w3_kerry_cross_check/{a}", b) for a, b in (("Sept-W3-Full-Scale-Ticket-Kerry.pdf",) * 2, ("Sept-W3-Empty-Scale-Ticket-Kerry.pdf",) * 2,
          ("Sept-W2-Empty-Scale-Ticket-Kerry.pdf",) * 2, ("Sept_W2_Full_Scale_Ticket_Kerry.jpg",) * 2)]
out["second_batch_files_identical"] = {b: sha(X / a) == sha(R / b) for a, b in pairs}
def allvals(p):
    wb = openpyxl.load_workbook(p, data_only=True)
    return {f"{ws.title}!{c.coordinate}": c.value for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None}
for a, b in (("Removal_Batch_CrossRef_Sep2026_live_20261006T1834Z.xlsx", "Removal_Batch_CrossRef_Sep2026.xlsx"),
             ("w3_kerry_cross_check/INJ-09-2026-W1_Ops_Notes_live_20261006T1831Z.xlsx", "INJ-09-2026-W1-Ops-Notes.xlsx"),
             ("w3_kerry_cross_check/INJ-10-2026-W1_Ops_Notes_live_20261006T1831Z.xlsx", "INJ-10-2026-W1-Ops-Notes.xlsx")):
    va, vb = allvals(X / a), allvals(R / b)
    out[f"second_batch_values_identical_{b}"] = va == vb
out["all_match"] = (all(v for k, v in out.items() if k.endswith("_identical")) and not out["ops_notes_value_diffs"] and not out["ops_notes_note_diffs"]
                    and out["car474_manitowoc"] == 0.071 and all(out["components_tab_has"].values()) and all(out["w3_certify_has"].values())
                    and not any(out[k] for k in out if k.endswith("_kerry_summary_diffs") or k.endswith("_note_diffs"))
                    and all(out["second_batch_files_identical"].values())
                    and all(v for k, v in out.items() if k.startswith("second_batch_values_identical_")))
(B / "repass_comparison.json").write_text(json.dumps(out, indent=1, default=str, ensure_ascii=False))
print(json.dumps(out, indent=1, default=str, ensure_ascii=False))
