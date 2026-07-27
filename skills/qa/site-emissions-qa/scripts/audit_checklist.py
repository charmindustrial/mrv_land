#!/usr/bin/env python3
"""
Pre-delivery audit script for site-emissions QA checklists.

Walks every Pass/Fail/Flag/Pending row in a site-emissions checklist xlsx,
parses [log:KEY] citation tags from evidence notes, looks up each key in the
corresponding site_emissions_[Site]_[RP]_source_reads.json, and verifies any
quoted numeric values match the log value to the precision shown.

Mismatches → row is rewritten to:
    Status: Flag
    Notes: Could not verify with cited source: [specific gap]

Also enforces:
- Rule 1 (log key citation required on every status)
- Rule 4 ("Pending — blocking" / "needs Max" requires ≥3 enumerated tooling-path attempts)
- Rule 5 (numeric values quoted in evidence notes must match cited log values)

Differences from the batch-qa-aecn audit_checklist.py:
- Six-column layout (A=Item, B=Status, C=Notes, D=Certify Component, E=Verifier
  Reference, F=Phase Resolved) instead of batch-qa-aecn's five-column layout.
- Header rows / metadata block are at the top of the file before the data
  rows; the script auto-detects the header row by scanning for the first row
  whose column B value is a valid status string.
- Phase 1 `Pending` is a valid status and is audited the same way (must carry
  a [log:KEY] pointing to the calc-sheet authoritative value preserved for
  Phase 2).
- Section header rows (merged cells in column A with no status) are skipped
  automatically.

Usage:
    python3 audit_checklist.py <checklist.xlsx> <source_reads.json>
        [--write]   apply rewrites and save the file
        [--quiet]   only print failures

Exit codes:
    0 = audit passed (zero failures), or rewrites were applied with --write
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
RULE_KEY_RE = re.compile(r"\[rule:([^\]]+)\]")
# Rule C: words that indicate a rule-assertion (something "must" be a certain
# way, or "should be," or "is required to," etc.). When a Fail or Flag note uses
# this kind of language, the row must cite the rule it's invoking via [rule:KEY]
# so the rule itself can be verified and exceptions checked.
RULE_ASSERTION_RE = re.compile(
    r"\b("
    r"must (be|have|include|match|exceed|equal|use|carry|appear|fail|pass|reflect|"
    r"contain|come|go|flow|amortize|map|reside|stay|stop|adopt)"
    r"|is required (to|by)|is mandatory|are mandatory|are required (to|by)"
    r"|should (be|have|match|include|use)|shall (be|have|match)"
    r"|protocol requires|skill requires|standard requires"
    r"|never\s+(BCU|eligible|allowed|acceptable|valid|applied)"
    r"|always\s+(BCU|eligible|required|use|apply)"
    r")\b",
    re.IGNORECASE,
)
# Match an explicit "= NUMBER" where the number is a complete numeric token
# (digits with optional commas and at most one decimal point), followed by a
# non-numeric/non-dash/non-slash boundary so we don't capture partial pieces
# like "2" from "2-184" or "4" from "4/2/2026".
QUOTED_VALUE_RE = re.compile(r"=\s*([\d,]+(?:\.\d+)?)(?![\d/.\-])")
BLOCKING_RE = re.compile(r"\b(blocking|blocked|needs[\s_]?max)\b", re.IGNORECASE)
ATTEMPT_RE = re.compile(r"\(\d\)\s*[^;]+;")  # counts "(1) ... ;" "(2) ... ;" patterns

# Rule D: speculation/hedge phrases in evidence notes must be backed by a
# [verified-via:METHOD] citation pointing to the primary-source step that
# confirmed the claim. Without this, the audit can't distinguish a verified
# read from a confident-sounding guess. This rule was added 2026-05-13 after
# repeated in-session failures where the agent re-wrote one bullshit claim
# into a different bullshit claim ("is a display format, not a stored-value
# difference") while pretending to fix the original ("0.51 kWh shortfall").
# The full vocabulary is built from those specific failures.
SPECULATION_RE = re.compile(
    r"\b("
    r"may be|might be|could be|probably|presumably|possibly"
    r"|appears to(?: be)?|seems to(?: be)?"
    r"|i\s+think|i\s+believe"
    r"|is\s+(?:a\s+)?display(?:\s+(?:format|artifact|value|rounding))?"
    r"|is\s+a\s+storage\s+(?:format|value)"
    r"|is\s+likely\b|likely\s+a\s+(?:rounding|display|storage)"
    r"|if\s+(?:it|this|the\s+value|metric[-\s]tonne|short[-\s]ton|x|y|z)\s+(?:is|are|were)\s+(?:correct|right|true)"
    r"|convention\s+(?:generally\s+)?treats"
    r"|implicit\s+(?:interpretation|conversion|assumption)"
    r"|recommend\s+confirming\s+(?:GREET|the|whether|that)"
    r")\b",
    re.IGNORECASE,
)
VERIFIED_VIA_RE = re.compile(r"\[verified-via:([^\]]+)\]")

# Rule E: applied-offset / coverage claim audit. Added 2026-07-10 after the
# INJ-06-2026-W2 site electricity was Pass'd as "REC-covered" on the strength of
# the BCU Quant column NAME ("Basco Site Electricity (RECs)") — a label — while
# Certify actually carried it at the full grid EF (0.4671667218) with no EAC
# retirement in evidence. The failure: asserting a reduction MECHANISM is APPLIED
# from a summary/label/folder/component-name instead of opening the source that
# proves it is applied (the Certify component showing the reduced value/EF, plus
# the backing retirement/EAC/REC certificate). This is the positive-claim sibling
# of the negative-claim audit and Rule D: a coverage/offset Pass is only as good
# as the applied-mechanism primary source behind it.
COVERAGE_CLAIM_RE = re.compile(
    r"\b("
    r"REC[-\s]?covered|covered\s+by\s+(?:a\s+)?RECs?|RECs?\s+applied|RECs?\s+cover"
    r"|EAC[-\s]?covered|covered\s+by\s+(?:an\s+)?EAC|EACs?\s+applied"
    r"|offset\s+by\s+(?:a\s+)?BCU|BCU[-\s]?offset|fully\s+offset|net\s+of\s+RECs?|net\s+of\s+BCUs?"
    r"|derated|renewable[-\s]?covered|reduction\s+applied|is\s+REC'?d"
    r")\b",
    re.IGNORECASE,
)
# The [verified-via:METHOD] method string must name a source that actually shows
# the mechanism APPLIED — a Certify component/reduction/datapoint that was opened,
# or a retirement/EAC/REC certificate that was read. A tracker label, BCU-Quant
# column name, folder name, or component name is NOT sufficient and does not match.
APPLIED_MECHANISM_RE = re.compile(
    r"(modal|component|reduction|datapoint|certificate|retirement|Certify|EF[-\s]?applied|derated[-\s]?EF|grid_?electricity)",
    re.IGNORECASE,
)
# Second required leg for an APPLIED REC/EAC/BCU coverage Pass: the qty must be
# shown drawn down from the inventory/tracker sheet. Per Max's 2026-07-10 rule,
# an applied REC shows in BOTH Certify (derated EF) AND the inventory sheet;
# Certify-only or inventory-only is a FAIL, not a Pass.
INVENTORY_VERIFY_RE = re.compile(
    r"(inventory|tracker|drawn[-\s]?down|deduct|retired|quant[-\s]?sheet)",
    re.IGNORECASE,
)

VALID_STATUSES = {"Pass", "Fail", "Flag", "Pending", "N/A"}

FILL_FLAG = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
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
    Compare a numeric string from the evidence note (e.g., "847.917") against
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


def collect_numerics(val, acc):
    """Recursively collect every numeric value from a possibly-nested log payload."""
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


def audit_row(item_label, status, notes, log) -> tuple[bool, list[str]]:
    """
    Return (ok, gap_descriptions). ok=True means the row passes the audit.
    """
    gaps = []

    if not isinstance(notes, str) or not notes.strip():
        gaps.append("evidence note is empty")
        return False, gaps

    # Rule 4: blocking enumeration. Note: this applies to "Pending — blocking"
    # or "needs Max" framing, not to plain Phase 1 Pending (which is the
    # standard deferral and needs only a [log:KEY] to the preserved value).
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

    # Rule C: any Fail/Flag note that asserts a rule violation (uses "must",
    # "required", "should be", etc.) must also carry a [rule:KEY] tag. This
    # forces the rule to be cited so exceptions can be checked. Without it,
    # findings can rest on guideline-as-hard-rule misinterpretations (caught
    # April 2026 on Sitework non-diesel → CapEx amortization Flag).
    if status in ("Fail", "Flag"):
        if RULE_ASSERTION_RE.search(notes):
            rule_tags = RULE_KEY_RE.findall(notes)
            if not rule_tags:
                gaps.append(
                    "Rule C — finding uses rule-assertion language (e.g., 'must', 'required', "
                    "'should be', 'never', 'always') but carries no [rule:KEY] citation. "
                    "Cite the rule text (KB section, category_evidence_guide section, protocol clause) "
                    "OR reframe the finding as a question pending confirmation."
                )

    # Rule D: speculation/hedge language in an evidence note must be backed by
    # a [verified-via:METHOD] citation indicating how the speculative claim was
    # confirmed against a primary source. Without it, the speculation is
    # unverified and the row must either be reworded to remove the speculation,
    # rewritten as a pure observed fact, or carry an explicit verification tag.
    # Applies to every status (Pass too — Pass with unverified speculation is
    # the failure mode this rule was built to catch).
    if SPECULATION_RE.search(notes):
        verified_tags = VERIFIED_VIA_RE.findall(notes)
        if not verified_tags:
            match = SPECULATION_RE.search(notes)
            phrase = match.group(0) if match else "(speculative phrase)"
            gaps.append(
                f"Rule D — evidence note contains speculation phrase '{phrase}' "
                "but carries no [verified-via:METHOD] citation. Either remove "
                "the speculation, replace with a verified literal value, or add "
                "[verified-via:WHAT-YOU-ACTUALLY-DID] (e.g., "
                "[verified-via:opened-detail-modal], [verified-via:Max-confirmed-direct-read], "
                "[verified-via:GREET-database-lookup]) documenting how the claim "
                "was confirmed against primary source."
            )

    # Rule E: applied-offset / coverage claim. Any note asserting a reduction is
    # APPLIED (REC-covered, offset by BCU, net of RECs, derated, EAC-covered…)
    # must carry a [verified-via:METHOD] whose method names an applied-mechanism
    # primary source (Certify component/reduction opened, retirement/EAC cert
    # read) — never a tracker label / column name / folder name. Fires on every
    # status, but the failure mode it was built for is a Pass resting on a label.
    if COVERAGE_CLAIM_RE.search(notes):
        phrase = COVERAGE_CLAIM_RE.search(notes).group(0)
        vias = VERIFIED_VIA_RE.findall(notes)
        certify_leg = any(APPLIED_MECHANISM_RE.search(v) for v in vias)
        inventory_leg = any(INVENTORY_VERIFY_RE.search(v) for v in vias)
        # A Pass asserting applied coverage needs BOTH legs (Certify derated-EF
        # applied AND inventory qty drawn down). Fail/Pending/N-A that merely
        # mention a coverage term (e.g. describing the FAIL) aren't held to Pass
        # standards, but a coverage-claim Pass is.
        if status == "Pass":
            missing = []
            if not certify_leg:
                missing.append("Certify-side ([verified-via:opened-Certify-reduction] — derated REC/BCU EF actually applied)")
            if not inventory_leg:
                missing.append("inventory-side ([verified-via:REC-inventory-deduction] — qty drawn from the REC/EAC/BCU inventory sheet)")
            if missing:
                gaps.append(
                    f"Rule E — Pass claims an APPLIED offset ('{phrase}') but is missing the "
                    + " AND ".join(missing) + ". An applied REC/EAC/BCU must show in BOTH Certify and the "
                    "inventory sheet (a label/column/folder name proves neither). If only one side is "
                    "present that's a FAIL (mismatch); if neither is applied, downgrade to Flag "
                    "(non-applied, intent unclear) — do not Pass."
                )
        elif not certify_leg and not inventory_leg:
            # Non-Pass coverage mention with no verification at all: nudge (not a hard fail on Fail/Flag).
            gaps.append(
                f"Rule E — note uses applied-offset language ('{phrase}') without any [verified-via:] leg. "
                "If asserting the offset IS applied, cite Certify + inventory; if pending, reword to "
                "'intended/pending, carried gross' so it doesn't read as applied."
            )

    # Resolve each key against the log
    flat_keys: list[str] = []
    for k in keys:
        flat_keys.extend([s.strip() for s in k.split(",")])

    for key in flat_keys:
        ok, _val = get_path(log, key)
        if not ok:
            gaps.append(f"cited key not found in source-read log: {key}")

    # Rule 5 inner check: any number after "=" should match a value found
    # via the cited keys. We collect every numeric value reachable from any
    # cited key — including values nested inside dicts and lists — so a key
    # that resolves to a dict still contributes its inner numerics. This
    # matches the intent: "the quoted value came from somewhere I can verify
    # in the log."
    quoted_numbers = QUOTED_VALUE_RE.findall(notes)
    if quoted_numbers:
        log_values: list[float] = []
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
    Site-emissions column layout: A=item, B=status, C=notes, D=Certify, E=verifier, F=phase.
    """
    note_cell = ws.cell(row=row_idx, column=3)
    original = note_cell.value or ""
    new_note = (
        "Could not verify with cited source: "
        + "; ".join(gaps)
        + " — original evidence preserved below — ORIGINAL: "
        + str(original)
    )
    ws.cell(row=row_idx, column=2, value="Flag")
    note_cell.value = new_note
    for col in range(1, 7):
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

    # Site-emissions checklist has a metadata block at the top before data
    # rows. We auto-detect data rows by scanning for any row whose column B
    # value is one of the valid statuses. Section header rows (merged cells
    # in column A with no status in column B) are naturally skipped.
    failures = []
    audited_count = 0
    # Rule B: track rows that have an Item (col A) but no Status (col B). These
    # are rows where content was dropped silently (merge-cell collision or other
    # write failure). They look "empty" in the spreadsheet but the Item label
    # is still there, so they're not legitimate section headers either.
    empty_status_rows = []
    section_header_re = re.compile(r"^(GATE \d|Categories N/A|Phase \d Summary|Cross-Agent|Universal Cross-Cutting|Substantive FAILs|FLAGs|Phase 2 deferrals)", re.IGNORECASE)
    for r in range(1, ws.max_row + 1):
        item = ws.cell(row=r, column=1).value
        status = ws.cell(row=r, column=2).value
        notes = ws.cell(row=r, column=3).value
        if status not in VALID_STATUSES:
            # Rule B check: is this a data row that lost its status?
            # Heuristic: column A has a substantive item label, but it's NOT a
            # section header pattern, AND the row is below the column header row.
            if (isinstance(item, str)
                    and item.strip()
                    and not section_header_re.match(item.strip())
                    and item not in ("Checklist Item",)  # the column header row
                    and r > 12):  # past the metadata block
                empty_status_rows.append((r, item))
            continue
        audited_count += 1
        ok, gaps = audit_row(item, status, notes, log)
        if not ok:
            failures.append((r, item, status, gaps))

    # Rule B: empty-status rows are an audit failure regardless of citation
    for r, item in empty_status_rows:
        failures.append((r, item, "(empty)", [
            "Rule B — row has an item label but empty Status / Notes. Content was likely "
            "dropped silently during a cell-patch operation (merge-cell write collision). "
            "Either repopulate with a real Status + Notes + citation, or remove the row."
        ]))

    print(f"Audit ran on {audited_count} status rows ({len(failures)} failures).")
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
