#!/usr/bin/env python3
"""
entrypoint.py — one operator-started QA run inside the Cloud Run job.

  1. Read and validate the operator inputs (QA_* env vars, see qa_inputs.py).
  2. Take the workspace lock in GCS so two runs never edit the registries or
     the performance tracker at the same time.
  3. Pull workspace state from gs://$QA_STATE_BUCKET/state/ : outputs/qa/**
     (batch folders, performance tracker) and the qa_active_*.json registries.
  4. Run the QA skill as ONE CLAUDE SESSION PER GATE (qa_inputs.GATES). Cost is
     roughly turns x context, and a single session carries everything it has
     ever read into every later turn. Each gate session starts clean, re-reads
     the rules (pre-flight docs), checks the previous gate's exit condition
     from the files on disk, does only its own gate, and leaves a handoff note.
     A gate that ends blocked or failed stops the run; the next run resumes at
     that gate (completed gates are recorded in the run folder's gate_status.json).
  5. Push state back, plus every session's transcript and a summary (with
     turns and cost per gate) to gs://$QA_STATE_BUCKET/runs/<execution>/.
     This happens even if the run fails.

Publishing results to Drive is done by the agent itself at the last gate with
tools/drive_read.py put, which refuses a checklist without a green
gate_receipt.json. Nothing here sends Slack or email.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from google.api_core.exceptions import NotFound, PreconditionFailed
from google.cloud import storage

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_inputs  # noqa: E402

WS = Path(os.environ.get("QA_WORKSPACE", "/workspace"))
CONTAINER_DIR = WS / "skills/qa/container"
STATE_PREFIX = "state/"
LOCK_BLOB = "locks/workspace.lock"
LOCK_STALE_HOURS = 8
# Files under these workspace paths are state: pulled before, pushed after.
STATE_GLOBS = ["outputs/qa/**/*", "skills/qa/*/qa_active*.json"]


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[qa-entrypoint {now()}] {msg}", flush=True)


def read_inputs() -> dict:
    return {f: os.environ[qa_inputs.env_name(f)] for f in qa_inputs.FIELDS
            if os.environ.get(qa_inputs.env_name(f))}


# ---------------------------------------------------------------- lock + state

def take_lock(bucket: storage.Bucket, run_id: str, inputs: dict) -> None:
    blob = bucket.blob(LOCK_BLOB)
    body = json.dumps({"run_id": run_id, "taken_at_utc": now(), "inputs": inputs})
    try:
        blob.upload_from_string(body, if_generation_match=0)
        return
    except PreconditionFailed:
        pass
    blob.reload()
    held = json.loads(blob.download_as_text())
    age_h = (datetime.datetime.now(datetime.timezone.utc) - blob.updated).total_seconds() / 3600
    if age_h < LOCK_STALE_HOURS and os.environ.get("QA_BREAK_LOCK") != "1":
        sys.exit(f"Another QA run holds the workspace lock: {held}. "
                 f"Wait for it, or re-run with QA_BREAK_LOCK=1 if that run is dead.")
    log(f"Breaking lock held by {held.get('run_id')} ({age_h:.1f} h old)")
    blob.upload_from_string(body, if_generation_match=blob.generation)


def release_lock(bucket: storage.Bucket, run_id: str) -> None:
    blob = bucket.blob(LOCK_BLOB)
    try:
        if json.loads(blob.download_as_text()).get("run_id") == run_id:
            blob.delete()
    except NotFound:
        pass


def pull_state(bucket: storage.Bucket) -> int:
    n = 0
    for blob in bucket.list_blobs(prefix=STATE_PREFIX):
        rel = blob.name[len(STATE_PREFIX):]
        if not rel or rel.endswith("/"):
            continue
        dest = WS / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(dest))
        n += 1
    return n


def snapshot_state() -> dict[str, float]:
    files = {}
    for pattern in STATE_GLOBS:
        for p in WS.glob(pattern):
            if p.is_file():
                files[p.relative_to(WS).as_posix()] = p.stat().st_mtime
    return files


def push_state(bucket: storage.Bucket, before: dict[str, float]) -> list[str]:
    pushed = []
    for rel, mtime in snapshot_state().items():
        if before.get(rel) != mtime:
            bucket.blob(STATE_PREFIX + rel).upload_from_filename(str(WS / rel))
            pushed.append(rel)
    return pushed


# ---------------------------------------------------------------- gate sessions

def run_folder(inputs: dict) -> Path:
    """Per-QA folder for gate status and handoff notes (state, so it resumes)."""
    key = inputs.get("batch_id") or inputs.get("reporting_period") or "run"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{inputs['mode']}__{key}")
    return WS / "outputs/qa/_container" / slug


def session_prompt(inputs: dict, gate: int | None, gates: list, rf: Path) -> str:
    folder, skill_name, _ = qa_inputs.MODES[inputs["mode"]]
    rel_rf = rf.relative_to(WS).as_posix()
    lines = [
        f"Run the `{skill_name}` skill (skills/qa/{folder}/SKILL.md) in CONTAINER MODE.",
        "Read skills/qa/container/CONTAINER_MODE.md before anything else; it overrides the "
        "skill's MCP-fallback, Drive mount, Slack, Gmail and Excel steps, and says which "
        "Knowledge Base slice to read.",
        "",
        "Operator inputs for this run:",
    ]
    for f in qa_inputs.FIELDS:
        if f != "mode" and inputs.get(f):
            lines.append(f"- {f}: {inputs[f]}")
    if inputs["mode"] == "re-review":
        lines += ["", "The operator has confirmed Garrett finished his corrections for this batch. "
                      "Skip Slack completion detection and go straight to the re-review."]
    if gate is None:
        lines += ["", f"When finished, write {rel_rf}/gate_0_result.json as described in "
                      "CONTAINER_MODE.md (Gate sessions)."]
        return "\n".join(lines)

    last = gates[-1]
    lines += [
        "",
        f"THIS SESSION RUNS GATE {gate} ONLY (gates in this skill: {', '.join(map(str, gates))}).",
        f"Follow CONTAINER_MODE.md 'Gate sessions'. Run folder: {rel_rf}/",
    ]
    if gate == gates[0]:
        lines.append("This is the first gate: do the skill's Pre-Flight Gate first, then Gate "
                     f"{gate}.")
    else:
        prev = gates[gates.index(gate) - 1]
        lines.append(f"Gates up to {prev} are recorded complete. Read {rel_rf}/handoff_gate*.md, "
                     f"then confirm Gate {prev}'s exit condition from the files on disk before "
                     f"starting Gate {gate}.")
    if gate == last:
        lines.append("This is the last gate: it includes finalization, run_gates.py and publishing.")
    else:
        lines.append(f"Do not start Gate {gates[gates.index(gate) + 1]}.")
    lines.append(f"End by writing {rel_rf}/handoff_gate{gate}.md and {rel_rf}/gate_{gate}_result.json.")
    return "\n".join(lines)


def run_session(prompt: str, transcript: Path) -> dict:
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "bypassPermissions",
        "--append-system-prompt", (CONTAINER_DIR / "CONTAINER_MODE.md").read_text(),
        "--max-turns", os.environ.get("QA_MAX_TURNS_PER_GATE", "200"),
    ]
    if os.environ.get("QA_MODEL"):
        cmd += ["--model", os.environ["QA_MODEL"]]
    result: dict = {}
    with transcript.open("w") as out:
        proc = subprocess.Popen(cmd, cwd=WS, stdout=subprocess.PIPE, text=True)
        for line in proc.stdout:
            out.write(line)
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                result = event
            elif event.get("type") == "assistant":
                for block in event.get("message", {}).get("content", []):
                    if block.get("type") == "text":
                        print(block["text"][:2000], flush=True)
        rc = proc.wait()
    return {
        "exit_code": rc,
        "subtype": result.get("subtype"),          # success | error_max_turns | ...
        "num_turns": result.get("num_turns"),
        "total_cost_usd": result.get("total_cost_usd"),
        "usage": result.get("usage"),
        "final_message": result.get("result") or "",
    }


def read_gate_result(rf: Path, gate: int) -> dict:
    p = rf / f"gate_{gate}_result.json"
    if not p.exists():
        return {"status": "failed", "summary": f"session ended without writing {p.name}"}
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return {"status": "failed", "summary": f"{p.name} is not valid JSON"}


# ---------------------------------------------------------------- main

def main() -> int:
    run_id = os.environ.get("CLOUD_RUN_EXECUTION") or f"local-{int(time.time())}"
    inputs = read_inputs()
    problems = qa_inputs.validate(inputs)
    if problems:
        log("Invalid inputs: " + "; ".join(problems))
        return 2

    publish = inputs.get("publish_folder") or inputs.get("drive_folder") or ""
    os.environ["DRIVE_WRITE_FOLDERS"] = publish
    os.environ["QA_CONTAINER"] = "1"
    os.environ["QA_MODE"] = inputs["mode"]

    bucket = storage.Client().bucket(os.environ["QA_STATE_BUCKET"])
    take_lock(bucket, run_id, inputs)
    started = now()
    tmp = Path("/tmp/qa-runs") / run_id      # outside outputs/ so transcripts are not pushed as state
    tmp.mkdir(parents=True, exist_ok=True)
    sessions: list[dict] = []
    outcome, before = "failed", None
    try:
        log(f"Pulled {pull_state(bucket)} state files from gs://{bucket.name}/{STATE_PREFIX}")
        before = snapshot_state()
        rf = run_folder(inputs)
        rf.mkdir(parents=True, exist_ok=True)
        status_path = rf / "gate_status.json"
        status = json.loads(status_path.read_text()) if status_path.exists() else {"completed_gates": []}

        gates = qa_inputs.GATES[inputs["mode"]]
        if os.environ.get("QA_START_GATE"):        # operator override, e.g. a fresh re-run
            start = int(os.environ["QA_START_GATE"])
            status["completed_gates"] = [g for g in status["completed_gates"] if g < start]
        todo = [g for g in gates if g not in status["completed_gates"]] if gates else [None]
        log(f"Gates to run: {todo} (already complete: {status['completed_gates']})")

        outcome = "complete"
        for gate in todo:
            label = f"gate{gate}" if gate is not None else "single"
            log(f"--- session {label}")
            s = run_session(session_prompt(inputs, gate, gates, rf), tmp / f"transcript_{label}.jsonl")
            gr = read_gate_result(rf, gate if gate is not None else 0)
            s.update({"gate": gate, "gate_result": gr})
            sessions.append(s)
            log(f"session {label}: {gr.get('status')} | turns={s['num_turns']} "
                f"cost=${s['total_cost_usd']} subtype={s['subtype']}")
            if gr.get("status") != "complete" or s["subtype"] != "success":
                outcome = gr.get("status") if gr.get("status") == "blocked" else "failed"
                break
            if gate is not None:
                status["completed_gates"].append(gate)
                status_path.write_text(json.dumps(status, indent=1))
    finally:
        pushed = []
        try:
            pushed = push_state(bucket, before) if before is not None else []
        finally:
            final = sessions[-1]["final_message"] if sessions else ""
            summary = {
                "run_id": run_id, "inputs": inputs, "outcome": outcome,
                "model": os.environ.get("QA_MODEL", "(Claude Code default)"),
                "started_at_utc": started, "finished_at_utc": now(),
                "total_cost_usd": round(sum(s.get("total_cost_usd") or 0 for s in sessions), 2),
                "total_turns": sum(s.get("num_turns") or 0 for s in sessions),
                "sessions": [{k: v for k, v in s.items() if k != "final_message"} for s in sessions],
                "state_files_pushed": pushed, "publish_folder": publish, "result": final,
            }
            bucket.blob(f"runs/{run_id}/summary.json").upload_from_string(
                json.dumps(summary, indent=1), content_type="application/json")
            for t in tmp.glob("transcript_*.jsonl"):
                bucket.blob(f"runs/{run_id}/{t.name}").upload_from_filename(str(t))
            release_lock(bucket, run_id)
    log(f"Done: {outcome}. ${summary['total_cost_usd']} over {summary['total_turns']} turns. "
        f"Summary: gs://{bucket.name}/runs/{run_id}/summary.json")
    print(final, flush=True)
    return 0 if outcome == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
