#!/usr/bin/env python3
"""
One-shot, program-to-program builder for the weekly MRV Pace Report file.

Does every file step of the pace-report-generate pass with the Drive API
directly (no local Drive mount, no base64 passing through the model):

  1. Read config.json (next to this script) and the state file it names.
  2. Idempotency: if state already has a cycle for --target, or Drive already
     holds a file with the target title, print NO-ACTION and exit 0.
  3. Find the source report = newest non-template .xlsx in parent_folder_id.
  4. Download template + source to the scratch dir.
  5. Run populate_report.py (source -> template copy, write "Week of" date).
  6. Upload the populated file to parent_folder_id under the target title.
  7. Print one JSON line with everything the Slack post + state record need.

Usage:
  python3 generate_pace_report.py --target 2026-09-17 [--scratch DIR]

Why this exists (2026-09-17): the 2026-09-09 and 2026-09-16 scheduled runs
both died at the 900s watchdog. The 09-16 log shows the exact cause: the
Drive MCP download returned the template as an inline base64 string and the
model tried to retype it into a python command, hit the 32,000 output-token
ceiling after 13 minutes, and was killed. File bytes must never pass through
model output. This script moves them program-to-program.
"""
import argparse
import io
import json
import os
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))


def fail(msg):
    print(f"FAILED: {msg}")
    sys.exit(1)


def drive_client(token_path):
    if not os.path.exists(token_path):
        fail(f"Google token missing: {token_path}")
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    with open(token_path) as fh:
        raw = json.load(fh)
    scopes = raw.get("scopes") or []
    if "https://www.googleapis.com/auth/drive" not in scopes:
        fail(f"Google token lacks the drive scope. Has: {scopes}")
    creds = Credentials(
        token=raw.get("token") or raw.get("access_token"),
        refresh_token=raw.get("refresh_token"),
        client_id=raw.get("client_id"),
        client_secret=raw.get("client_secret"),
        token_uri=raw.get("token_uri", "https://oauth2.googleapis.com/token"),
        scopes=scopes,
    )
    if not creds.valid:
        creds.refresh(Request())
        raw["token"] = creds.token
        tmp = token_path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(raw, fh)
        os.replace(tmp, token_path)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def download(svc, file_id, dest):
    from googleapiclient.http import MediaIoBaseDownload

    req = svc.files().get_media(fileId=file_id, supportsAllDrives=True)
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = dl.next_chunk()
    with open(dest, "wb") as fh:
        fh.write(buf.getvalue())
    if os.path.getsize(dest) < 1000:
        fail(f"downloaded file suspiciously small: {dest}")


XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def list_live(svc, cfg):
    q = f"'{cfg['parent_folder_id']}' in parents and trashed = false"
    resp = svc.files().list(
        q=q, pageSize=100,
        fields="files(id,name,mimeType,createdTime,webViewLink)",
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    return resp.get("files", [])


def deprecate_old_reports(svc, cfg, keep_id):
    """Move every report except the template and keep_id into Deprecated/Past.

    Max, 2026-08-27 and again 2026-09-10: prior reports go in the Deprecated
    subfolder. This used to wait for a "Complete" reply in the #team-mrv
    thread, which nobody posts, so nothing moved after 9/10 and the live
    folder piled up (9/17, 9/24, 10/1 all still there on 2026-10-12). Now the
    weekly build does it: the live folder holds the template + the newest
    report, nothing else.
    """
    moved = []
    for f in list_live(svc, cfg):
        if f["id"] in (keep_id, cfg["template_file_id"]):
            continue
        if f["mimeType"] != XLSX_MIME or not f["name"].lower().endswith(".xlsx"):
            continue
        svc.files().update(
            fileId=f["id"],
            addParents=cfg["deprecated_folder_id"],
            removeParents=cfg["parent_folder_id"],
            fields="id,parents",
            supportsAllDrives=True,
        ).execute()
        moved.append(f["name"])
    return moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", help="Thursday date, ISO (e.g. 2026-09-17)")
    ap.add_argument("--scratch", default=os.environ.get("TMPDIR", "/tmp"))
    ap.add_argument("--deprecate-only", action="store_true",
                    help="only move every report but the newest into Deprecated/Past")
    args = ap.parse_args()

    with open(os.path.join(HERE, "config.json")) as fh:
        cfg = json.load(fh)
    for k in ("template_file_id", "parent_folder_id", "deprecated_folder_id",
              "new_file_title_format", "state_path", "google_token_path"):
        if k not in cfg:
            fail(f"config.json missing key: {k}")

    if args.deprecate_only:
        svc = drive_client(cfg["google_token_path"])
        reports = [f for f in list_live(svc, cfg)
                   if f["mimeType"] == XLSX_MIME and f["id"] != cfg["template_file_id"]]
        if not reports:
            fail("no reports in parent folder")
        newest = max(reports, key=lambda f: f["createdTime"])
        moved = deprecate_old_reports(svc, cfg, newest["id"])
        print(json.dumps({"status": "DEPRECATED", "kept": newest["name"], "moved": moved}))
        return

    if not args.target:
        fail("--target is required")
    try:
        target = date.fromisoformat(args.target)
    except ValueError:
        fail(f"--target must be ISO date, got {args.target}")

    title = cfg["new_file_title_format"].format(m=target.month, d=target.day)

    # --- idempotency: state ---------------------------------------------
    state = {"pending_cycles": []}
    if os.path.exists(cfg["state_path"]):
        with open(cfg["state_path"]) as fh:
            state = json.load(fh)
    for c in state.get("pending_cycles", []):
        if c.get("week_date") == target.isoformat():
            print(f"NO-ACTION: already generated for {target.isoformat()} "
                  f"({c.get('new_file_title')}, ts {c.get('thread_ts')})")
            sys.exit(0)

    svc = drive_client(cfg["google_token_path"])

    # --- list the folder ---------------------------------------------------
    files = list_live(svc, cfg)

    # --- idempotency: Drive already has this week's file -----------------
    for f in files:
        if f["name"] == title:
            print(f"NO-ACTION: Drive already holds '{title}' (id {f['id']}) "
                  f"but state.json has no cycle for it -- record it by hand or "
                  f"with record_pending_cycle.py")
            sys.exit(0)

    candidates = [
        f for f in files
        if f["mimeType"] == XLSX_MIME
        and f["id"] != cfg["template_file_id"]
        and f["name"].lower().endswith(".xlsx")
    ]
    if not candidates:
        fail("no source report found in parent folder -- a human must seed the first report")
    source = max(candidates, key=lambda f: f["createdTime"])

    # --- download -----------------------------------------------------------
    os.makedirs(args.scratch, exist_ok=True)
    tpl_path = os.path.join(args.scratch, "pace_template.xlsx")
    src_path = os.path.join(args.scratch, "pace_source.xlsx")
    download(svc, cfg["template_file_id"], tpl_path)
    download(svc, source["id"], src_path)

    # --- populate -----------------------------------------------------------
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "populate_report.py"),
         src_path, tpl_path, target.isoformat()],
        capture_output=True, text=True,
    )
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0 or not out.startswith("OK:"):
        fail(f"populate_report.py: {out}")

    # --- upload -------------------------------------------------------------
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(tpl_path, mimetype=XLSX_MIME, resumable=False)
    created = svc.files().create(
        body={"name": title, "parents": [cfg["parent_folder_id"]]},
        media_body=media,
        fields="id,name,webViewLink,createdTime",
        supportsAllDrives=True,
    ).execute()

    # --- move every prior report to Deprecated/Past --------------------------
    try:
        deprecated = deprecate_old_reports(svc, cfg, created["id"])
    except Exception as e:
        fail(f"new report uploaded ({created['webViewLink']}) but moving old "
             f"reports to Deprecated failed: {e}")

    local_folder = cfg.get("drive_local_folder", "")
    result = {
        "status": "BUILT",
        "week_date": target.isoformat(),
        "new_file_id": created["id"],
        "new_file_title": created["name"],
        "new_file_local_path": os.path.join(local_folder, title.replace("/", " ")),
        "new_file_web_link": created["webViewLink"],
        "source_file_id": source["id"],
        "source_file_title": source["name"],
        "source_file_local_path": os.path.join(local_folder, source["name"].replace("/", " ")),
        "populate_output": out,
        "deprecated": deprecated,
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
