#!/usr/bin/env python3
"""
Source-read log content validator (site-emissions-qa).

Runs BEFORE audit_checklist.py. Rejects log entries that smuggle
characterizations / findings into the log as if they were extracted
primary-source values.

The audit script downstream validates "every checklist citation resolves
to a log key and quoted numbers match." It cannot validate "the log value
is itself a literal extraction, not an interpretation." That gap is what
let the Apr 2026 site-emissions Phase 1 ship false FAILs on the railcar
sheet (#NAME? — was a Drive renderer artifact, not the actual cells) and
on Waste Disposal classification mismatch (a speculative claim logged as
a Boolean). Both passed audit because the citations resolved fine.

What this validator rejects:

  1. Strings inside *.extracted_values.* containing editorial verbs
     ("errors", "missing", "mismatch", "inconsistent", "unreconciled",
     "broken", "wrong", "violation", "throughout"). Findings belong in
     the checklist, not the log.

  2. Boolean values inside *.extracted_values.* (these are almost always
     a finding dressed as data: "weight_not_on_ticket: True" should be
     a checklist Flag, not a log entry).

  3. Keys in *.extracted_values.* whose name suffixes signal editorial:
     _status, _mismatch, _inconsistent, _broken, _violation, _unreconciled.

  4. Strings inside *.derived.* containing the same editorial verbs UNLESS
     the value is an explicit arithmetic check (contains an "=" sign and a
     digit, indicating a math statement like "9.13535 × 59.4 × 0.0001384
     = 0.07510 MT ✓"). Math is allowed; editorial is not.

What this validator allows:
  - Top-level _meta (session context, narrative framing).
  - kb_sections_read, _source_method, source_method (read-context labels).
  - Numeric leaf values, dates, IDs.
  - Arithmetic expressions in derived blocks (math, not opinion).
  - Notes that document the read mechanism explicitly when they live
    under _meta or _source_method.

Usage:
    python3 validate_log.py <source_reads.json>
        [--strict]   exit 1 on ANY violation (default: exit 1)
        [--quiet]    only print violations, no summary

Exit codes:
    0 = log clean (zero violations)
    1 = log contains characterization / finding fields that must be
        moved to the checklist or removed
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EDITORIAL_TERMS = [
    "errors",
    "missing",
    "mismatch",
    "inconsistent",
    "unreconciled",
    "broken",
    "wrong",
    "violation",
    "throughout",
    "fail",
    "false",
    "predates",
    "discrepancy",
    "drift",
    "stale",
    "fabrication",
]

FORBIDDEN_KEY_SUFFIXES = [
    "_status",
    "_mismatch",
    "_inconsistent",
    "_broken",
    "_violation",
    "_unreconciled",
    "_correct",
    "_match",
    "_artifact_corrected",
    "_understatement",
    "_overstatement",
]

# Path segments that allow editorial framing (session-level meta only)
ALLOWED_EDITORIAL_PARENTS = {
    "_meta",
    "_source_method",
    "source_method",
    "kb_sections_read",
    "kb_authority",
    "_source_method",
    "drive_folder_inventory",  # filename inconsistency observation lives here as fact
}

# Patterns that signal "this is an arithmetic check, not editorial"
ARITHMETIC_HINT_RE = re.compile(r"=\s*\d|\d\s*[×x*]\s*\d|\d\s*[+\-]\s*\d")
EDITORIAL_TERM_RE = re.compile(
    r"\b(" + "|".join(EDITORIAL_TERMS) + r")\b", re.IGNORECASE
)


def is_in_allowed_parent(path_segments: list[str]) -> bool:
    """Return True if any path segment matches an allowed-editorial parent."""
    for seg in path_segments:
        if seg in ALLOWED_EDITORIAL_PARENTS:
            return True
    return False


def is_in_extracted_values(path_segments: list[str]) -> bool:
    return "extracted_values" in path_segments


def is_in_derived(path_segments: list[str]) -> bool:
    return "derived" in path_segments


def violations_for_leaf(path: list[str], key: str, value):
    """Yield violation dicts for a single leaf (key, value) pair."""
    full_path = ".".join(path + [key])
    in_extracted = is_in_extracted_values(path + [key])
    in_derived = is_in_derived(path + [key])
    in_allowed = is_in_allowed_parent(path)

    # Rule 3: forbidden key suffixes anywhere except allowed parents
    if not in_allowed:
        for suf in FORBIDDEN_KEY_SUFFIXES:
            if key.endswith(suf):
                yield {
                    "rule": 3,
                    "path": full_path,
                    "value_repr": repr(value)[:120],
                    "reason": f"key ends with forbidden editorial suffix '{suf}' — looks like a finding dressed as data",
                }
                return  # one violation per leaf is enough

    # Rule 2: Boolean inside extracted_values
    if in_extracted and isinstance(value, bool):
        yield {
            "rule": 2,
            "path": full_path,
            "value_repr": repr(value),
            "reason": "Boolean inside extracted_values — Booleans are findings, not extractions; move to checklist",
        }
        return

    # Rule 1: editorial string inside extracted_values
    if in_extracted and isinstance(value, str) and not in_allowed:
        m = EDITORIAL_TERM_RE.search(value)
        if m:
            yield {
                "rule": 1,
                "path": full_path,
                "value_repr": repr(value)[:160],
                "reason": f"extracted_values string contains editorial term '{m.group(1)}' — log entries must be literal extractions, not characterizations",
            }
            return

    # Rule 4: editorial string inside derived (allow only if it has arithmetic)
    if in_derived and isinstance(value, str) and not in_allowed:
        if EDITORIAL_TERM_RE.search(value) and not ARITHMETIC_HINT_RE.search(value):
            m = EDITORIAL_TERM_RE.search(value)
            yield {
                "rule": 4,
                "path": full_path,
                "value_repr": repr(value)[:160],
                "reason": f"derived string contains editorial term '{m.group(1)}' without arithmetic — derived must be math, not opinion",
            }
            return

    # Rule 4-bis: Boolean in derived
    if in_derived and isinstance(value, bool) and not in_allowed:
        yield {
            "rule": 5,
            "path": full_path,
            "value_repr": repr(value),
            "reason": "Boolean in derived — derived must be math statements with operands, not Boolean conclusions",
        }
        return


def walk(obj, path: list[str], violations: list[dict]):
    """Recursively walk a JSON structure, collecting violations at each leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                walk(v, path + [k], violations)
            else:
                violations.extend(list(violations_for_leaf(path, k, v)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                walk(v, path + [str(i)], violations)
            else:
                # list-of-primitives — uncommon in our log, but handle it
                violations.extend(list(violations_for_leaf(path, str(i), v)))


# Rule A: every xlsx evidence file must be read via openpyxl on the downloaded
# bytes, not via Drive's text renderer. Require both phrases to appear somewhere
# in the read_method / _source_method / read_method_note string — that's a
# substantive proof of method, not an exact-wording check.
REQUIRED_PHRASES_IN_XLSX_READ_METHOD = ["download_file_content", "openpyxl(data_only=True)"]


def check_xlsx_read_method_rule(log):
    """Rule A — Reject any *.evidence_files.* entry pointing to an xlsx/xlsm
    file that doesn't carry an accepted read_method.

    Caught April 2026 Basco RP: railcar sheet read via Drive renderer produced
    false #NAME? finding; Sitework Kerry Tank distance misread as 1,729 vs the
    actual 1,779 because Drive's natural-language render of the xlsx isn't a
    cell-level read. SKILL.md HARD RULE table requires xlsx → openpyxl. This
    enforces it at the log layer.
    """
    out: list[dict] = []
    seen: set[str] = set()

    def visit(obj, path):
        if isinstance(obj, dict):
            fn = obj.get("filename")
            if isinstance(fn, str) and fn.lower().endswith((".xlsx", ".xlsm")):
                key = ".".join(path) + "::" + fn
                if key not in seen:
                    seen.add(key)
                    rm = " ".join(str(obj.get(k, "")) for k in ("read_method", "_source_method", "read_method_note"))
                    if not all(p in rm for p in REQUIRED_PHRASES_IN_XLSX_READ_METHOD):
                        out.append({
                            "rule": "A",
                            "path": ".".join(path),
                            "value_repr": f"filename={fn!r}, read_method={rm!r}",
                            "reason": (
                                "Rule A — xlsx/xlsm evidence file lacks an accepted read_method. "
                                "xlsx/xlsm with formulas MUST be read via "
                                "`download_file_content + openpyxl(data_only=True)`. "
                                "Drive read_file_content text renderer is not a primary-source read for cell-level findings."
                            ),
                        })
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    visit(v, path + [k])
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                if isinstance(v, (dict, list)):
                    visit(v, path + [str(i)])

    visit(log, [])
    return out


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("source_reads", type=Path)
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    if not args.source_reads.exists():
        print(f"ERROR: source-read log not found: {args.source_reads}", file=sys.stderr)
        return 1

    log = json.load(open(args.source_reads))

    violations: list[dict] = []
    walk(log, [], violations)
    violations.extend(check_xlsx_read_method_rule(log))

    if not args.quiet:
        print(f"Validator ran on log: {args.source_reads}")
        print(f"  ({sum(1 for _ in walk_count(log))} leaf values inspected; {len(violations)} violations)")

    for v in violations:
        print(f"\n  [Rule {v['rule']}] {v['path']}")
        print(f"    Value: {v['value_repr']}")
        print(f"    Why:   {v['reason']}")

    if violations:
        print(
            "\nLOG REJECTED. Fix by:\n"
            "  - Moving findings/characterizations OUT of the log and INTO the checklist (cited via [log:KEY] to literal values).\n"
            "  - Replacing Boolean assertions in extracted_values with the literal extracted values that support them.\n"
            "  - Replacing editorial text in derived with explicit arithmetic (e.g., '9.13535 × 59.4 × 0.0001384 = 0.07510 MT ✓').\n",
            file=sys.stderr,
        )
        return 1

    print("\nLog clean. Proceed to audit_checklist.py.")
    return 0


def walk_count(obj):
    """Yield 1 per leaf value, for size reporting only."""
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_count(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_count(v)
    else:
        yield 1


if __name__ == "__main__":
    sys.exit(main())
