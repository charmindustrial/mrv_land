"""Weekly inline pH (PH-1041) -> Mangrove data feed.

Entry point: injectate_ph_feed(request) — triggered by Cloud Scheduler via HTTP,
Saturdays 01:00 America/Denver (02:00 Central).

Flow:
  1. Take the Sat->Sat (America/Chicago) injection week that just closed.
  2. BigQuery (prod-data-warehouse-487604, SCADA historian): PH-1041 readings with
     dataintegrity = 192 while StateRun = 1, reduced to one median per 15 minutes
     (ph_15min_medians.sql).
  3. Upload window_start, window_end, ph_median as CSV to the Mangrove data feed
     ph_measurement_basco. The feed turns each row into one "Inline pH measurement"
     event; Mangrove's weekly batch averages them.

Idempotency: the feed sets no tracking_id, so a second upload would double-count
the week. The function refuses to upload a week that already has any
inline-ph-measurement event in it.

Manual / backfill: POST {"week_start": "YYYY-MM-DD", "dry_run": true}. dry_run
computes and returns the summary without uploading.
"""
from __future__ import annotations

import csv
import io
import json
import logging
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import requests
from google.cloud import bigquery

sys.path.insert(0, str(Path(__file__).parent))
from week import last_closed_week_start, parse_week_start, week_bounds  # noqa: E402

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("injectate_ph_feed")

BQ_PROJECT = "prod-data-warehouse-487604"
BQ_LOCATION = "us-central1"  # not the US multi-region; omitting it fails like a permissions error

MANGROVE_BASE = "https://app.gomangrove.com/api/v1"
MANGROVE_PROJECT_ID = 709
DATA_FEED_ID = "datafd_Mfl1UtLkC3uRvsRx"  # ph_measurement_basco
EVENT_SLUG = "inline-ph-measurement"
FEED_HEADER = ["window_start", "window_end", "ph_median"]

SQL = (Path(__file__).parent / "ph_15min_medians.sql").read_text()


def injectate_ph_feed(request) -> tuple[str, int]:
    """HTTP entry point for Cloud Functions."""
    body = request.get_json(silent=True) or {}
    try:
        summary = run(week_start=body.get("week_start"), dry_run=bool(body.get("dry_run")))
    except Exception as e:  # noqa: BLE001 — surface any failure as a 500 + ERROR log
        log.exception("injectate_ph_feed failed")
        return json.dumps({"ok": False, "error": str(e)}), 500
    log.info(json.dumps(summary, default=str))
    return json.dumps({"ok": True, **summary}, default=str), 200


def run(week_start: str | None = None, dry_run: bool = False, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    ws = parse_week_start(week_start) if week_start else last_closed_week_start(now)
    start, end = week_bounds(ws)
    if end > now:
        raise ValueError(f"week {ws} has not closed yet (ends {end.isoformat()})")

    summary: dict[str, Any] = {
        "week_start": ws.isoformat(),
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "dry_run": dry_run,
    }

    rows = query_week(ws)
    summary.update(summarize(rows))
    if not rows:
        return {**summary, "status": "no-injection"}

    existing = events_in_window(start, end)
    if existing:
        return {**summary, "status": "skipped-existing", "existing_events": len(existing)}

    payload = to_feed_csv(rows)
    if dry_run:
        return {**summary, "status": "dry-run", "csv_bytes": len(payload.encode())}

    run_info = submit_data_feed(payload, f"injectate_ph_{ws.isoformat()}.csv")
    pipeline = run_info.get("pipeline_run", run_info)
    return {**summary, "status": "submitted", "pipeline_run": pipeline.get("id")}


# ---------------------------------------------------------------------------
# BigQuery
# ---------------------------------------------------------------------------

def query_week(week_start: date) -> list[dict]:
    client = bigquery.Client(project=BQ_PROJECT, location=BQ_LOCATION)
    job = client.query(
        SQL,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("week_start", "DATE", week_start)]
        ),
        location=BQ_LOCATION,
    )
    return [dict(r) for r in job.result()]


def summarize(rows: list[dict]) -> dict:
    if not rows:
        return {"intervals": 0, "readings": 0}
    meds = [float(r["ph_median"]) for r in rows]
    return {
        "intervals": len(rows),
        "readings": sum(int(r["n_readings"]) for r in rows),
        "mean_of_medians": round(sum(meds) / len(meds), 3),
        "min": min(meds),
        "max": max(meds),
    }


def to_feed_csv(rows: list[dict]) -> str:
    """CSV matching the feed schema exactly; n_readings is never posted."""
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(FEED_HEADER)
    for r in rows:
        ph = r.get("ph_median")
        # A None/blank median must fail, never post as pH 0.
        if ph is None or ph == "":
            raise ValueError(f"missing ph_median for {r.get('window_start')}")
        w.writerow([r["window_start"], r["window_end"], float(ph)])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Mangrove REST
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    token = os.environ.get("MANGROVE_TOKEN")
    if not token:
        raise RuntimeError("MANGROVE_TOKEN is not set (Secret Manager: mangrove-api-token)")
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def events_in_window(start: datetime, end: datetime) -> list[dict]:
    """inline-ph-measurement events whose start_time falls in [start, end)."""
    out: list[dict] = []
    page = 1
    while True:
        r = requests.get(
            f"{MANGROVE_BASE}/projects/{MANGROVE_PROJECT_ID}/events",
            headers=_headers(),
            params={
                "start_time_after": start.astimezone(timezone.utc).isoformat(),
                "start_time_before": end.astimezone(timezone.utc).isoformat(),
                "page": page,
                "page_size": 200,
            },
            timeout=30,
        )
        r.raise_for_status()
        body = r.json()
        for ev in body.get("data") or []:
            t = datetime.fromisoformat(ev["start_time"].replace("Z", "+00:00"))
            if ev.get("slug") == EVENT_SLUG and start <= t < end:
                out.append(ev)
        nxt = (body.get("info") or {}).get("next_page")
        if not nxt:
            return out
        page = nxt
        if page > 100:
            raise RuntimeError("Mangrove events pagination exceeded 100 pages")


def submit_data_feed(payload: str, filename: str) -> dict:
    """POST the CSV to the feed's endpoint source. 2xx = accepted, processed async."""
    r = requests.post(
        f"{MANGROVE_BASE}/data_feeds/{DATA_FEED_ID}",
        headers=_headers(),
        files={"file": (filename, payload.encode(), "text/csv")},
        timeout=60,
    )
    if not r.ok:
        raise RuntimeError(f"Mangrove upload {r.status_code}: {r.text[:300]}")
    return r.json() if r.text else {}


if __name__ == "__main__":
    # Local: python main.py [YYYY-MM-DD] — always a dry run.
    print(json.dumps(run(week_start=sys.argv[1] if len(sys.argv) > 1 else None, dry_run=True), indent=2, default=str))
