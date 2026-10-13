#!/usr/bin/env python3
"""
run_gates.py — the ONLY way a batch QA becomes deliverable.

Runs every mandatory pre-delivery gate for a batch and writes a signed receipt
(gate_receipt.json) into the batch folder. The receipt records the sha256 of the
exact checklist file that passed, so it cannot be reused for a later edit of that
file, and it cannot be hand-written without the gates having actually run (each
gate's stdout is captured verbatim into the receipt).

`qa_delivery_gate_guard.sh` refuses any Slack/Gmail delivery about a batch whose
folder has no green receipt whose checklist hash matches the file on disk.

Gates run, in order, all must pass:
  1. recompute_*.py                      -> exit 0
  2. audit_checklist.py (+ attachment gate) -> "0 failures" and "Attachment gate: PASS"
  3. performance tracker row exists for this batch id
  4. checklist status cells are Pass/Fail/Flag/N-A in the casing audit_checklist
     matches, and the audit reports a row count > 0 (the INJ-09-2026-W2 failure:
     upper-case statuses made the audit silently audit zero rows)
  5. Every batch type (Charm WODO / Aqueous, AECN, Kerry; an unrecognised type is
     blocked): every required SKILL.md step has a step_ledger.json entry with evidence
     that resolves, an independent agent's ledger_audit.json verifies every entry of
     that exact ledger, plus file checks that need no ledger (batch_step_ledger.py; the
     INJ-09-2026-W3-QOWV failure: all gates green, eight required steps skipped)

Usage:  python3 run_gates.py <batch_output_folder>
Exit 0 = receipt written, delivery unlocked. Exit 1 = no receipt, delivery blocked.
"""
import json, hashlib, subprocess, sys, re, datetime
from pathlib import Path

WS = Path(__file__).resolve().parents[3]          # MRV Expert workspace root
AUDIT = WS / ".claude/skills/batch-qa-aecn/scripts/audit_checklist.py"
TRACKER = WS / "outputs/qa/performance-monitor/Claude_QA_Performance_Tracker.xlsx"
VALID_STATUSES = {"Pass", "Fail", "Flag", "N/A"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fail(msg: str) -> None:
    print(f"GATE FAIL: {msg}")
    sys.exit(1)


def load_exceptions(folder: Path) -> list:
    """delivery_exceptions.json: required QA steps the MRV lead has authorised leaving undone.
    Findings (Certify gaps, real discrepancies) never go here: they pass as checklist rows."""
    p = folder / "delivery_exceptions.json"
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text()).get("exceptions", [])
    except Exception as e:
        fail(f"delivery_exceptions.json unreadable ({e})")


ROW_ID = re.compile(r"^(?:\d+[a-z]?\.\d+[a-z]?|S\.\d+)$")


def _status_rows(ws):
    for r in range(1, ws.max_row + 1):
        yield str(ws.cell(r, 1).value or "").strip(), ws.cell(r, 3).value, str(ws.cell(r, 4).value or "")


def attachment_gaps_routed(gaps, ws):
    """Findings rule (2026-09-29): a Certify evidence gap blocks delivery only while the checklist
    has not recorded it. It passes once a Fail row cites [log:certify.attachment_gate] and names
    every open datapoint. Returns (row id or None, reason)."""
    for item, status, text in _status_rows(ws):
        if status == "Fail" and "certify.attachment_gate" in text:
            missing = [g for g in gaps if g not in text]
            if not missing:
                return item, ""
            return None, f"row {item} does not name {missing}"
    return None, "no Fail row cites [log:certify.attachment_gate]"


def findings_unrouted(stdout, ws):
    """Every recompute line 'FINDING <row>[/<row>...] ...' must point at checklist rows graded
    Fail or Flag; a finding sitting under a Pass (or no row) is a discrepancy the QA dropped."""
    status = {item: st for item, st, _ in _status_rows(ws)}
    bad = []
    for line in stdout.splitlines():
        if not line.startswith("FINDING "):
            continue
        first_word = line.split()[1].rstrip(":")
        ids = first_word.split("/")
        if not all(ROW_ID.match(i) for i in ids):
            continue      # informational line (scenario, legacy tote id): not a row claim
        for i in ids:
            if status.get(i) not in ("Fail", "Flag"):
                bad.append(f"{line[:140]} -> row {i} is {status.get(i)!r}")
    return bad


def step_exception_ok(ex, sid, ledger, ws):
    """A required QA step left undone passes only with the MRV lead's authorisation quoted, and only
    if the ledger honestly marks it not done. (Findings never need this: they go through as rows.)"""
    if not sid:
        return False, "problem is not tied to a required step"
    if not ex:
        return False, f"no step:{sid} entry in delivery_exceptions.json"
    if (ledger.get(sid) or {}).get("done") is not False:
        return False, f"step_ledger.json must mark {sid} done: false"
    if len(str(ex.get("authorized_by", "")).strip()) >= 3:
        return True, ""
    return False, "needs the MRV lead's authorisation quoted in authorized_by"


def main() -> None:
    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        fail(f"{folder} is not a directory")
    # a failed run must not leave an earlier green receipt unlocking delivery
    (folder / "gate_receipt.json").unlink(missing_ok=True)

    checklists = sorted(folder.glob("*QA_Checklist*.xlsx"))
    checklists = [c for c in checklists if not c.name.startswith("~$")]
    if len(checklists) != 1:
        fail(f"expected exactly 1 checklist xlsx in {folder}, found {len(checklists)}: "
             f"{[c.name for c in checklists]}. Delete superseded versions first — a "
             f"receipt must be unambiguous about which file passed.")
    checklist = checklists[0]

    logs = list(folder.glob("batch_*_source_reads.json"))
    if len(logs) != 1:
        fail(f"expected exactly 1 batch_*_source_reads.json, found {len(logs)}")
    log_path = logs[0]
    log = json.loads(log_path.read_text())
    batch_id = log.get("batch_id") or folder.name

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import batch_step_ledger as bsl
    kind = bsl.batch_kind(log, folder)
    if kind is None:
        fail(f"oil type not recognised (oil_type={log.get('oil_type')!r}, folder {folder.name}): "
             f"no required-step list applies, so delivery stays blocked. Record oil_type in the "
             f"source-read log as AECN, Kerry, WODO or Aqueous.")

    results = {}

    # --- Self-test: the findings rule must still hold before this script is trusted to block ---
    t = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "tests/test_findings_never_block.py")],
                       capture_output=True, text=True)
    if t.returncode != 0:
        fail(f"findings-rule self-test failed; run_gates.py cannot be trusted:\n{t.stdout}\n{t.stderr}")
    results["findings_rule_self_test"] = {"ok": True, "stdout": t.stdout.strip().splitlines()[-1]}

    # --- Gate 0: status casing (structural; the failure this file exists for) ---
    import openpyxl
    ws = openpyxl.load_workbook(checklist).active
    statuses = [ws.cell(r, 3).value for r in range(1, ws.max_row + 1)]
    statuses = [s for s in statuses if isinstance(s, str) and s.strip()]
    bad_case = sorted({s for s in statuses
                       if s.upper() in {"PASS", "FAIL", "FLAG", "N/A"} and s not in VALID_STATUSES})
    if bad_case:
        fail(f"checklist status cells use casing the audit does not match: {bad_case}. "
             f"audit_checklist.py matches exactly {sorted(VALID_STATUSES)}; anything else "
             f"makes it audit ZERO rows while appearing to pass.")
    n_status_rows = sum(1 for s in statuses if s in VALID_STATUSES)
    if n_status_rows == 0:
        fail("no rows carry a Pass/Fail/Flag/N/A status")
    # audit_checklist.py audits Pass/Fail/Flag only, so that is the count the audit
    # must match. N/A rows escape it entirely, so assert their citations here.
    n_auditable = sum(1 for s in statuses if s in {"Pass", "Fail", "Flag"})
    na_rows = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 3).value == "N/A"]
    na_uncited = [ws.cell(r, 1).value for r in na_rows
                  if "[log:" not in str(ws.cell(r, 4).value or "")]
    if na_uncited:
        fail(f"N/A rows with no [log:] citation (the audit script does not check these, "
             f"so they are checked here): {na_uncited}")
    results["status_casing"] = {"ok": True, "status_rows": n_status_rows,
                                "auditable_rows": n_auditable, "na_rows_cited": len(na_rows)}

    # --- Gate 1: deterministic recompute ---
    recomputes = sorted(folder.glob("recompute_*.py"))
    if not recomputes:
        fail("no recompute_*.py in the batch folder — the deterministic recompute is mandatory")
    for rc in recomputes:
        p = subprocess.run([sys.executable, rc.name], cwd=folder, capture_output=True, text=True)
        if p.returncode != 0:
            fail(f"{rc.name} exited {p.returncode}. A non-zero exit means a discrepancy the QA has not "
                 f"routed yet: either fix the QA's own log and rerun, or print it as 'FINDING <row>: ...' "
                 f"so the checklist carries it:\n{p.stdout}\n{p.stderr}")
        unrouted = findings_unrouted(p.stdout, ws)
        if unrouted:
            fail(f"{rc.name} reports findings the checklist does not carry as Fail or Flag:\n  - " + "\n  - ".join(unrouted))
        results[rc.name] = {"ok": True, "exit": 0, "stdout": p.stdout.strip()}

    # --- Gate 2: citation audit + attachment gate ---
    p = subprocess.run([sys.executable, str(AUDIT), checklist.name, log_path.name],
                       cwd=folder, capture_output=True, text=True)
    out = p.stdout + p.stderr
    m = re.search(r"Audit ran on (\d+) rows \((\d+) failures\)", out)
    if not m:
        fail(f"audit_checklist.py produced no row-count line:\n{out}")
    audited, failures = int(m.group(1)), int(m.group(2))
    if audited == 0:
        fail("audit_checklist.py audited 0 rows — the citation gate did not actually run")
    if audited < n_auditable:
        fail(f"audit covered {audited} of {n_auditable} Pass/Fail/Flag rows — rows are being skipped")
    if failures != 0:
        fail(f"audit_checklist.py reported {failures} row failure(s):\n{out}")
    exceptions = load_exceptions(folder)
    applied = []
    if "Attachment gate: PASS" not in out:
        gaps = [m.group(1).strip() for m in re.finditer(r"^\s+- (.+?): required", out, re.M)]
        if not gaps:     # structural failure (no attachment_map / no matrix) is unfinished QA work: blocks
            fail(f"attachment gate did not pass:\n{out}")
        row, why = attachment_gaps_routed(gaps, ws)
        if not row:
            fail(f"attachment gate: Certify evidence gaps the checklist does not carry ({why}):\n{out}")
        applied.append({"id": "attachment_gaps_routed", "covers": gaps, "checklist_row": row,
                        "why": "Certify evidence gaps are findings; the checklist carries them as a Fail"})
    results["audit_checklist"] = {"ok": True, "rows": audited, "failures": 0,
                                  "stdout": out.strip()[-4000:]}

    # --- Gate 3: performance tracker row ---
    if not TRACKER.exists():
        fail(f"performance tracker not found at {TRACKER}")
    tws = openpyxl.load_workbook(TRACKER)["Performance Log"]
    ids = {str(tws.cell(r, 3).value or "") for r in range(1, tws.max_row + 1)}
    if not any(batch_id in i or i in batch_id for i in ids if i):
        fail(f"no performance-tracker row for batch '{batch_id}' — the monitor step has not run")
    results["performance_tracker"] = {"ok": True, "batch_id": batch_id}

    # --- Gate 4: required-step ledger, independent audit of it, file checks (every batch type) ---
    problems =(bsl.check_ledger(folder, log, WS, kind, log_path.name)
                + bsl.check_audit(folder, kind)
                + bsl.check_files(folder, checklist, WS))
    ledger = json.loads((folder / "step_ledger.json").read_text()) if (folder / "step_ledger.json").exists() else {}
    ledger = ledger.get("steps", ledger)
    remaining = []
    for p in problems:
        sid = next((s for s, _, _ in bsl.REQUIRED_STEPS[kind] if p.startswith(f"{s} ") or p.startswith(f"audit {s}:")), None)
        ex = next((e for e in exceptions if sid and e.get("id") == f"step:{sid}"), None)
        ok, why = step_exception_ok(ex, sid, ledger, ws)
        if ok:
            if not any(a["id"] == f"step:{sid}" for a in applied):
                applied.append({"id": f"step:{sid}", "authorized_by": ex.get("authorized_by"),
                                "why": ex.get("why", "")})
        else:
            remaining.append(p + (f"  [no valid exception: {why}]" if sid else ""))
    if remaining:
        fail(f"{kind} required steps not evidenced / file checks failed:\n  - " + "\n  - ".join(remaining))
    results["required_steps"] = {"ok": True, "kind": kind, "steps": len(bsl.REQUIRED_STEPS[kind]),
                                 "ledger_sha256": sha256(folder / "step_ledger.json"),
                                 "ledger_audit_sha256": sha256(folder / "ledger_audit.json")}

    receipt = {
        "batch_id": batch_id,
        "checklist_file": checklist.name,
        "checklist_sha256": sha256(checklist),
        "source_reads_file": log_path.name,
        "source_reads_sha256": sha256(log_path),
        "generated_utc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "all_gates_green": True,
        "recorded_exceptions": applied,
        "gates": results,
    }
    (folder / "gate_receipt.json").write_text(json.dumps(receipt, indent=1))
    print(f"ALL GATES GREEN — receipt written for {checklist.name} "
          f"({audited} rows audited, 0 failures, attachment gate PASS)")
    sys.exit(0)


if __name__ == "__main__":
    main()
