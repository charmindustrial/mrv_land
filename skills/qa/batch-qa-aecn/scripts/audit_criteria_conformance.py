#!/usr/bin/env python3
"""Criteria-conformance audit.

Checks a delivered QA checklist against the CANONICAL item list in
references/checklist_structure.md and reports, mechanically:

  MISSING   - a spec criterion that does not appear in the workbook at all
  EXTRA     - an item in the workbook that is not in the spec
  REWORDED  - an item whose check text has drifted from the spec wording
  N/A       - every item marked N/A, with the spec's own note on whether N/A is expected

The point: an agent must not be able to silently widen or narrow the criteria
set between batches. Every item is accounted for against a fixed spec, and any
deviation is printed. Run it on every batch before delivery.

    python3 audit_criteria_conformance.py <checklist.xlsx> [spec.md]

Exit code 1 if there is any MISSING or EXTRA item, or any N/A the spec does not
sanction. REWORDED is reported but does not fail (evidence notes are expected to
be batch-specific; the CHECK column is what must stay stable).
"""
import re
import sys
import difflib
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
DEFAULT_SPEC = HERE.parent / "references" / "checklist_structure.md"

ITEM_ROW = re.compile(r"^\|\s*(\d+[a-z]?\.\d+)\s*\|\s*([^|]+?)\s*\|")
# Spec rows whose own text sanctions an N/A for AECN batches.
NA_SANCTION = re.compile(r"mark n/?a|n/?a for aecn|often n/?a", re.IGNORECASE)


def normalise(text: str) -> str:
    """Strip markdown emphasis, unicode dashes and casing so wording can be compared."""
    t = text.replace("**", "").replace("—", "-").replace("–", "-").replace("×", "x")
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"\s+", " ", t)
    return t.strip().lower().rstrip(".")


def load_spec(spec_path: Path) -> dict[str, dict]:
    spec: dict[str, dict] = {}
    for raw in spec_path.read_text(encoding="utf-8").splitlines():
        m = ITEM_ROW.match(raw)
        if not m:
            continue
        item, check = m.group(1), m.group(2)
        if item in spec:          # first table wins; later tables are rail addenda
            continue
        spec[item] = {"check": check, "row": raw, "na_sanctioned": bool(NA_SANCTION.search(raw))}
    return spec


def load_checklist(xlsx_path: Path) -> dict[str, dict]:
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["QA Checklist"]
    got: dict[str, dict] = {}
    for r in range(1, ws.max_row + 1):
        item = str(ws.cell(r, 1).value or "").strip()
        status = ws.cell(r, 3).value
        if status in ("Pass", "Fail", "Flag", "N/A") and re.fullmatch(r"\d+[a-z]?\.\d+", item):
            got[item] = {"check": str(ws.cell(r, 2).value or ""), "status": status, "row": r}
    return got


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    xlsx = Path(sys.argv[1])
    spec_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_SPEC

    spec = load_spec(spec_path)
    got = load_checklist(xlsx)

    print(f"Checklist : {xlsx.name}")
    print(f"Spec      : {spec_path.name}  ({len(spec)} canonical criteria)")
    print(f"Delivered : {len(got)} items\n")

    missing = sorted(set(spec) - set(got), key=lambda k: [int(x) for x in re.findall(r"\d+", k)])
    extra = sorted(set(got) - set(spec), key=lambda k: [int(x) for x in re.findall(r"\d+", k)])

    hard_fail = False

    if missing:
        hard_fail = True
        print("MISSING - in the spec, absent from the delivered checklist:")
        for i in missing:
            print(f"  {i}  {spec[i]['check']}")
        print()
    else:
        print("MISSING: none - every spec criterion is present.\n")

    if extra:
        hard_fail = True
        print("EXTRA - in the delivered checklist, not in the spec:")
        for i in extra:
            print(f"  {i}  {got[i]['check']}")
        print()
    else:
        print("EXTRA: none - no criterion was added.\n")

    reworded = []
    for i in sorted(set(spec) & set(got), key=lambda k: [int(x) for x in re.findall(r"\d+", k)]):
        a, b = normalise(spec[i]["check"]), normalise(got[i]["check"])
        ratio = difflib.SequenceMatcher(None, a, b).ratio()
        if ratio < 0.75:
            reworded.append((i, ratio, spec[i]["check"], got[i]["check"]))
    if reworded:
        print("REWORDED - check text drifted from the spec (report only, does not fail):")
        for i, ratio, s, g in reworded:
            print(f"  {i}  similarity {ratio:.2f}")
            print(f"      spec: {s}")
            print(f"      got : {g}")
        print()
    else:
        print("REWORDED: none - all check text matches the spec wording.\n")

    nas = [(i, got[i]) for i in got if got[i]["status"] == "N/A"]
    print(f"N/A items ({len(nas)}) - each shown with whether the spec sanctions an N/A:")
    for i, v in sorted(nas, key=lambda kv: [int(x) for x in re.findall(r"\d+", kv[0])]):
        if i not in spec:
            print(f"  {i}  UNSANCTIONED - not in spec")
            hard_fail = True
            continue
        ok = spec[i]["na_sanctioned"]
        if not ok:
            hard_fail = True
        print(f"  {i}  {'sanctioned by spec' if ok else 'NOT SANCTIONED - spec does not mark this N/A'}"
              f"  <- {spec[i]['check']}")
    print()

    tally: dict[str, int] = {}
    for v in got.values():
        tally[v["status"]] = tally.get(v["status"], 0) + 1
    print("Status tally:", tally)
    print()
    print("RESULT:", "CONFORMANCE FAILURE" if hard_fail else "CONFORMS - criteria set matches the spec exactly")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
