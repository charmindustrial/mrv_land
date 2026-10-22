#!/usr/bin/env python3
"""
parity_check.py — is a container QA run at least as strict as the Mac run it replaces?

Compares two checklists for the SAME batch item by item: the baseline (a QA
already done the old way, on the Mac) and the container run.

  python3 parity_check.py <baseline.xlsx> <container.xlsx> [--out report.json]

Severity order: Fail > Flag > Pass; N/A is compared separately. For every item:
  REGRESSION  the container grades it LESS severe than the baseline (Fail -> Flag/Pass,
              Flag -> Pass), grades an applicable item N/A, or drops the item.
              Any regression fails the check (exit 1).
  STRICTER    the container grades it MORE severe. Not a failure, but every one
              must be looked at: either the container found something real, or it
              is wrong.
  same        identical status.

Read the evidence column for STRICTER items before signing off. Identical
statuses with different evidence are listed as `evidence_changed` for a spot check.

Caveat: a baseline Fail that was CORRECTED in Certify between the two runs will
show as a regression. Compare against a batch whose Certify data has not changed
since the baseline run, or confirm each such item against the correction record.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import openpyxl

SEVERITY = {"Fail": 2, "Flag": 1, "Pass": 0}
ITEM_ID = re.compile(r"^\d{1,2}[a-z]?\.\d{1,2}[a-z]?$")


def read_checklist(path: Path, id_col: int, status_col: int, evidence_col: int) -> dict[str, dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    items: dict[str, dict] = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            cells = {c.column: c.value for c in row}
            item = str(cells.get(id_col) or "").strip()
            status = str(cells.get(status_col) or "").strip()
            if ITEM_ID.match(item) and status:
                norm = {"pass": "Pass", "fail": "Fail", "flag": "Flag", "n/a": "N/A", "na": "N/A"}.get(status.lower(), status)
                items[item] = {"status": norm, "evidence": str(cells.get(evidence_col) or ""),
                               "where": f"{ws.title}!{row[0].row}"}
    return items


def compare(base: dict, cont: dict) -> dict:
    report = {"regressions": [], "stricter": [], "evidence_changed": [], "same": 0,
              "baseline_items": len(base), "container_items": len(cont), "new_in_container": []}
    for item, b in base.items():
        c = cont.get(item)
        if c is None:
            report["regressions"].append({"item": item, "baseline": b["status"], "container": "MISSING"})
            continue
        bs, cs = b["status"], c["status"]
        if bs == cs:
            report["same"] += 1
            if b["evidence"].strip() != c["evidence"].strip():
                report["evidence_changed"].append({"item": item, "status": bs})
            continue
        entry = {"item": item, "baseline": bs, "container": cs,
                 "baseline_evidence": b["evidence"][:400], "container_evidence": c["evidence"][:400]}
        if cs == "N/A" and bs != "N/A":
            report["regressions"].append(entry)           # applicable item skipped
        elif bs == "N/A":
            report["stricter"].append(entry)              # container checked something baseline skipped
        elif SEVERITY.get(cs, -1) < SEVERITY.get(bs, -1):
            report["regressions"].append(entry)
        else:
            report["stricter"].append(entry)
    report["new_in_container"] = sorted(set(cont) - set(base))
    report["verdict"] = "PASS" if not report["regressions"] else "FAIL"
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("baseline"); ap.add_argument("container")
    ap.add_argument("--id-col", type=int, default=1, help="item number column (default A)")
    ap.add_argument("--status-col", type=int, default=3, help="status column (default C)")
    ap.add_argument("--evidence-col", type=int, default=4, help="evidence column (default D)")
    ap.add_argument("--out")
    a = ap.parse_args()
    base = read_checklist(Path(a.baseline), a.id_col, a.status_col, a.evidence_col)
    cont = read_checklist(Path(a.container), a.id_col, a.status_col, a.evidence_col)
    if not base:
        sys.exit(f"No checklist items found in {a.baseline}; check the column options.")
    report = compare(base, cont)
    text = json.dumps(report, indent=1)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    print(f"{report['verdict']}: {report['same']} same, {len(report['stricter'])} stricter, "
          f"{len(report['regressions'])} regressions, {len(report['evidence_changed'])} evidence changed "
          f"(baseline {report['baseline_items']} items, container {report['container_items']})")
    for r in report["regressions"]:
        print(f"  REGRESSION {r['item']}: {r['baseline']} -> {r['container']}")
    for r in report["stricter"]:
        print(f"  STRICTER   {r['item']}: {r['baseline']} -> {r['container']}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
