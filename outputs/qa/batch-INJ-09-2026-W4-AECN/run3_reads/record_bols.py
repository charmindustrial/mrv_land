"""Merge freshly read BOL values (typed from page images this session) into run3_reads/bol_reads_run3.json
and compare every shared field with run 1's builder values."""
import json, sys, re, datetime, pathlib, ast
H = pathlib.Path(__file__).resolve().parent.parent
OUT = H / "run3_reads" / "bol_reads_run3.json"
new = json.loads(sys.stdin.read())
doc = json.load(open(OUT)) if OUT.exists() else {"_read": "run 3; every page of each BOL opened with the Read tool; values typed from the page images right after each read", "bols": {}}
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for b, d in new.items():
    d["recorded_utc"] = now
    d["local_copy"] = f"bols/BOL_{b}.pdf"
    doc["bols"][b] = d
json.dump(doc, open(OUT, "w"), indent=1, ensure_ascii=False)
src = (H / "run1_2026-10-06_superseded" / "build_source_reads.py").read_text()
blk = src[src.index("B = {"):src.index("SHIP_TO =")]
r1 = {}
for m in re.finditer(r'"(\d{4}-R)": dict\((.*?)\),\n', blk):
    r1[m.group(1)] = eval("dict(" + m.group(2) + ")")
for b, d in new.items():
    o = r1[b]; diffs = []; n = 0
    for k, v in d.items():
        if k in o and k not in ("file", "page_order", "form"):
            n += 1
            if o[k] != v: diffs.append((k, o[k], v))
    print(b, "fields compared with run 1:", n, "differences:", diffs)
