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

This script is the post-build audit safety net. The same rule set lives in
`checklist_lib.py` and is also invoked at build time by
`checklist_lib.build_with_validation` so most failures get caught before the
xlsx is ever written.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

from checklist_lib import audit_evidence

FILL_FLAG = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
FONT_FLAG = Font(color="996600")


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
    # Set the resolution hint for relative artifact_path lookups — paths in
    # _primary_source_opened entries are resolved relative to the source-read
    # log's directory (the per-batch outputs folder).
    log["_audit_log_path_hint"] = str(args.source_reads.resolve())
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
        ok, gaps = audit_evidence(item, status, notes, log)
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

    # --- STRUCTURAL evidence-attachment gate (required-evidence matrix vs Certify) ---
    try:
        from audit_attachments import audit_attachments
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from audit_attachments import audit_attachments
    att_ok, att_failures = audit_attachments(log)
    print(f"\nAttachment gate: {'PASS' if att_ok else 'FAIL'} ({len(att_failures)} gap(s)).")
    for f in att_failures:
        print(f"    - {f}")
    if not att_ok:
        print("\nAttachment gate failed — required evidence not attached in Certify (or attachment_map not captured). "
              "Record each gap as a Fail row citing [log:certify.attachment_gate] and naming the datapoint; "
              "run_gates.py lets recorded gaps through to Garrett.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
