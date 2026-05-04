#!/usr/bin/env python3
"""
Pre-delivery audit script for AECN batch QA checklists.

Walks every PASS/FAIL/FLAG row in a batch checklist xlsx, parses [log:KEY]
citation tags from evidence notes, looks up each key in the corresponding
batch_[ID]_source_reads.json, and verifies any quoted values match the log
value to the precision shown.

Mismatches → row is rewritten to:
    Status: Flag
    Notes: Could not verify with cited source: [specific gap]

Also enforces the "blocking" enumeration rule: any status mentioning
"blocking" / "blocked" / "needs Max" must enumerate ≥3 tooling-path attempts.

Usage:
    python audit_checklist.py <checklist.xlsx> <source_reads.json>
        [--write]          apply rewrites and save the file
        [--quiet]          only print failures

Exit codes:
    0 = audit passed (zero failures), or audit ran in dry-run mode and reported
    1 = audit found failures and --write was not specified, or other error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

LOG_KEY_RE = re.compile(r"\[log:([^\]]+)\]")
# Match an explicit "= NUMBER" where the number is a complete numeric token
# (digits with optional commas and at most one decimal point), followed by a
# non-numeric/non-dash/non-slash boundary so we don't capture partial pieces
# like "2" from "2-184" or "4" from "4/2/2026".
QUOTED_VALUE_RE = re.compile(r"=\s*([\d,]+(?:\.\d+)?)(?![\d/.\-])")
BLOCKING_RE = re.compile(r"\b(blocking|blocked|needs[\s_]?max)\b", re.IGNORECASE)
ATTEMPT_RE = re.compile(r"\(\d\)\s*[^;]+;")  # counts "(1) ... ;" "(2) ... ;" patterns

FILL_FLAG = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
FONT_FLAG = Font(color="996600")


def get_path(obj, dotted_path: str):
    """
    Resolve a dotted path into a nested dict/list. Supports list indices via '.0', '.1', etc.
    Returns (found, value). If any segment is missing, returns (False, None).
    """
    cur = obj
    for seg in dotted_path.split("."):
        seg = seg.strip()
        if isinstance(cur, list):
            try:
                idx = int(seg)
            except ValueError:
                return False, None
            if idx < 0 or idx >= len(cur):
                return False, None
            cur = cur[idx]
        elif isinstance(cur, dict):
            if seg not in cur:
                return False, None
            cur = cur[seg]
        else:
            return False, None
    return True, cur


def numeric_match(quoted: str, log_value) -> bool:
    """
    Compare a numeric string from the evidence note (e.g. "21,844.99") against
    a value from the log (which may be int, float, or stringified number).
    Match to the precision shown in `quoted` (number of decimal places after
    stripping commas).
    """
    try:
        q = float(quoted.replace(",", ""))
    except ValueError:
        return False
    if isinstance(log_value, str):
        try:
            lv = float(log_value.replace(",", ""))
        except ValueError:
            return False
    else:
        try:
            lv = float(log_value)
        except (TypeError, ValueError):
            return False
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 10 ** (-decimals) / 2 + 1e-9
    return abs(q - lv) <= tol


def audit_row(item_label, status, notes, log) -> tuple[bool, list[str]]:
    """
    Return (ok, gap_descriptions). ok=True means the row passes the audit.
    """
    gaps = []

    if not isinstance(notes, str) or not notes.strip():
        gaps.append("evidence note is empty")
        return False, gaps

    # Rule 4: blocking enumeration
    if BLOCKING_RE.search(notes):
        attempts = len(ATTEMPT_RE.findall(notes))
        if attempts < 3:
            gaps.append(
                f"label invokes 'blocking'/'needs Max' but enumerates only {attempts} tooling-path attempt(s) "
                "(rule requires ≥3 distinct attempts with specific failure mode each)"
            )

    # Rule 1: log key citation
    keys = LOG_KEY_RE.findall(notes)
    if not keys:
        gaps.append("no [log:KEY] citation in evidence note")
        return False, gaps

    # Resolve each key against the log
    flat_keys: list[str] = []
    for k in keys:
        flat_keys.extend([s.strip() for s in k.split(",")])

    for key in flat_keys:
        ok, val = get_path(log, key)
        if not ok:
            gaps.append(f"cited key not found in source-read log: {key}")

    # Rule 5 inner check: any number after "=" should match a value found via the cited keys.
    # We collect every numeric value reachable from any cited key — including values nested
    # inside dicts and lists — so a key that resolves to a dict (e.g., bcu_check) still
    # contributes the numeric values inside it to the comparison set. This matches FC10's
    # intent: "the quoted value came from somewhere I can verify in the log."
    def collect_numerics(val, acc):
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            acc.append(val)
        elif isinstance(val, str):
            for tok in re.findall(r"[-+]?\d[\d,]*(?:\.\d+)?", val):
                try:
                    acc.append(float(tok.replace(",", "")))
                except ValueError:
                    pass
        elif isinstance(val, dict):
            for v in val.values():
                collect_numerics(v, acc)
        elif isinstance(val, list):
            for v in val:
                collect_numerics(v, acc)
        return acc

    quoted_numbers = QUOTED_VALUE_RE.findall(notes)
    if quoted_numbers:
        log_values = []
        for key in flat_keys:
            ok, val = get_path(log, key)
            if ok:
                collect_numerics(val, log_values)
        for q in quoted_numbers:
            if not any(numeric_match(q, lv) for lv in log_values):
                gaps.append(
                    f"quoted numeric '{q}' in evidence note doesn't match any cited log value "
                    f"(cited keys: {flat_keys})"
                )

    return len(gaps) == 0, gaps


def rewrite_row_to_unverified(ws, row_idx, gaps):
    """
    Rewrite a failed row to Flag status with 'couldn't verify' note.
    Columns per current SKILL.md: A=item, B=check, C=status, D=notes, E=verifier.
    """
    note_cell = ws.cell(row=row_idx, column=4)
    original = note_cell.value or ""
    new_note = (
        "Could not verify with cited source: "
        + "; ".join(gaps)
        + " — original evidence preserved below — ORIGINAL: "
        + str(original)
    )
    ws.cell(row=row_idx, column=3, value="Flag")
    note_cell.value = new_note
    for col in range(1, 6):
        c = ws.cell(row=row_idx, column=col)
        c.fill = FILL_FLAG
        c.font = FONT_FLAG


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("checklist", type=Path)
    p.add_argument("source_reads", type=Path)
    p.add_argument("--write", action="store_true", help="Apply rewrites and save the checklist")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    if not args.checklist.exists():
        print(f"ERROR: checklist not found: {args.checklist}", file=sys.stderr)
        return 1
    if not args.source_reads.exists():
        print(f"ERROR: source-read log not found: {args.source_reads}", file=sys.stderr)
        return 1

    log = json.load(open(args.source_reads))
    wb = load_workbook(args.checklist)
    ws = wb.active

    # Columns per current SKILL.md: A=item, B=check, C=status, D=notes, E=verifier
    failures = []
    audited_count = 0
    for r in range(2, ws.max_row + 1):
        item = ws.cell(row=r, column=1).value
        status = ws.cell(row=r, column=3).value
        notes = ws.cell(row=r, column=4).value
        if status not in ("Pass", "Fail", "Flag"):
            continue
        audited_count += 1
        ok, gaps = audit_row(item, status, notes, log)
        if not ok:
            failures.append((r, item, status, gaps))

    print(f"Audit ran on {audited_count} rows ({len(failures)} failures).")
    for r, item, status, gaps in failures:
        if not args.quiet:
            print(f"\n  Row {r} | Status: {status} | Item: {str(item)[:80]}")
            for g in gaps:
                print(f"    - {g}")

    if failures and args.write:
        for r, item, status, gaps in failures:
            rewrite_row_to_unverified(ws, r, gaps)
        wb.save(args.checklist)
        print(f"\n--write specified: {len(failures)} rows rewritten to 'couldn't verify'.")

    if failures and not args.write:
        print("\nRun with --write to apply rewrites, or fix evidence notes upstream.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
