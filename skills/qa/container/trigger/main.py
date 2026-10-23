"""
qa-trigger — HTTP start path for the qa-runner Cloud Run job.

Deployed with --no-allow-unauthenticated: Cloud Run checks the caller's
Google identity token and only principals with run.invoker on this service
get through. The caller's email (from that already-verified token) is
recorded as the run's operator.

  POST /run      JSON body with the qa_inputs.FIELDS (mode required).
                 Starts one job execution; returns its name.
  GET  /status/<execution>
                 Execution state from Cloud Run plus the run's summary.json
                 (final agent message, exit code) once it exists.
  GET  /candidates
                 The latest discovery list (discovery/latest.json): recent Certify
                 removals resolved to batch ID, mode, Drive folder and reporting period,
                 each marked ready / needs a person, with its QA status.
  POST /discover Refresh that list (starts the job in discover mode; no model).
  GET  /health     (not /healthz: Cloud Run reserves paths ending in "z")

Example:
  curl -X POST "$URL/run" -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: application/json" \
    -d '{"mode":"batch-qa-aecn","batch_id":"INJ-09-2026-W4-AECN","certify_url":"...","drive_folder":"..."}'
"""
from __future__ import annotations

import base64
import json
import os

import google.auth
from flask import Flask, jsonify, request
from google.auth.transport.requests import AuthorizedSession
from google.cloud import storage

import qa_inputs

PROJECT = os.environ["QA_PROJECT"]
REGION = os.environ["QA_REGION"]
JOB = os.environ["QA_JOB"]
BUCKET = os.environ["QA_STATE_BUCKET"]
RUN_API = "https://run.googleapis.com/v2"

app = Flask(__name__)
_creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
_session = AuthorizedSession(_creds)


def caller_email() -> str:
    """Email claim of the identity token Cloud Run already verified."""
    auth = request.headers.get("Authorization", "")
    try:
        payload = auth.split(" ", 1)[1].split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("email", "unknown")
    except (IndexError, ValueError):
        return "unknown"


@app.get("/health")
def health():
    return "ok"


@app.post("/run")
def run():
    inputs = {k: str(v) for k, v in (request.get_json(silent=True) or {}).items() if v not in (None, "")}
    inputs["operator"] = caller_email()
    problems = qa_inputs.validate(inputs)
    if problems:
        return jsonify({"error": "invalid inputs", "problems": problems}), 400

    env = [{"name": qa_inputs.env_name(k), "value": v} for k, v in inputs.items()]
    resp = _session.post(
        f"{RUN_API}/projects/{PROJECT}/locations/{REGION}/jobs/{JOB}:run",
        json={"overrides": {"containerOverrides": [{"env": env}]}},
    )
    if resp.status_code >= 300:
        return jsonify({"error": "job start failed", "detail": resp.text[:1000]}), 502
    execution = (resp.json().get("metadata") or {}).get("name", "")
    return jsonify({"started": True, "execution": execution.rsplit("/", 1)[-1],
                    "inputs": inputs}), 202


@app.get("/candidates")
def candidates():
    blob = storage.Client().bucket(BUCKET).blob("discovery/latest.json")
    if not blob.exists():
        return jsonify({"error": "no discovery run yet: POST /discover first"}), 404
    return app.response_class(blob.download_as_text(), mimetype="application/json")


@app.post("/discover")
def discover():
    env = [{"name": "QA_MODE", "value": "discover"}, {"name": "QA_OPERATOR", "value": caller_email()}]
    resp = _session.post(
        f"{RUN_API}/projects/{PROJECT}/locations/{REGION}/jobs/{JOB}:run",
        json={"overrides": {"containerOverrides": [{"env": env}]}},
    )
    if resp.status_code >= 300:
        return jsonify({"error": "discovery start failed", "detail": resp.text[:1000]}), 502
    execution = (resp.json().get("metadata") or {}).get("name", "")
    return jsonify({"started": True, "execution": execution.rsplit("/", 1)[-1]}), 202


@app.get("/status/<execution>")
def status(execution: str):
    resp = _session.get(
        f"{RUN_API}/projects/{PROJECT}/locations/{REGION}/jobs/{JOB}/executions/{execution}")
    if resp.status_code >= 300:
        return jsonify({"error": "execution not found", "detail": resp.text[:500]}), 404
    ex = resp.json()
    out = {"execution": execution,
           "running": ex.get("runningCount", 0), "succeeded": ex.get("succeededCount", 0),
           "failed": ex.get("failedCount", 0), "completion_time": ex.get("completionTime")}
    blob = storage.Client().bucket(BUCKET).blob(f"runs/{execution}/summary.json")
    if blob.exists():
        out["summary"] = json.loads(blob.download_as_text())
    return jsonify(out)
