#!/usr/bin/env python3
"""
slack_post.py — post a QA run's delivery messages to #team-mrv-alerts as the MRV QA bot.

The only Slack route in the QA. A QA run writes delivery_messages.json (format below);
this script posts it. The model never posts: it only writes the file.

Hard limits, enforced here in code:
  - The only destination is #team-mrv-alerts (C0944NQH1RP). Any other channel, and any
    DM, is refused.
  - No @-mentions of anyone (`<@...>`, `<!here>`, `<!channel>`): refused, not stripped.
  - For a batch QA, the batch folder's gate_receipt.json must be green and match the
    checklist on disk, the same delivery gate as drive_read.py put.

delivery_messages.json:
  {"posts": [
     {"text": "QA complete: INJ-10-2026-W3 ...",          # top-level message
      "thread": ["full detail ...", "..."]},             # replies under it (optional)
     {"thread_ts": "1774978621.877419",                  # or: reply in an existing thread
      "text": "Re-review: 2 of 3 resolved ..."}
  ]}

Usage:
  slack_post.py <delivery_messages.json> [--dry-run]
Token: SLACK_BOT_TOKEN (xoxb-...).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CHANNEL = "C0944NQH1RP"            # #team-mrv-alerts — the only allowed destination
MENTION = re.compile(r"<[@!](?:[^>]*)>")


class Refused(RuntimeError):
    pass


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    posts = data.get("posts")
    if not isinstance(posts, list) or not posts:
        raise Refused(f"{path.name}: needs a non-empty 'posts' list")
    if data.get("channel", CHANNEL) != CHANNEL:
        raise Refused(f"channel {data['channel']!r} refused: only #team-mrv-alerts ({CHANNEL})")
    for i, p in enumerate(posts):
        texts = [p.get("text", "")] + list(p.get("thread") or [])
        if not p.get("text", "").strip():
            raise Refused(f"post {i}: empty text")
        if p.get("thread_ts") and p.get("thread"):
            raise Refused(f"post {i}: use either thread_ts (reply to an existing thread) or thread, not both")
        for t in texts:
            if not isinstance(t, str):
                raise Refused(f"post {i}: every message must be text")
            if MENTION.search(t):
                raise Refused(f"post {i}: @-mentions are not allowed: {MENTION.search(t).group(0)}")
    return data


def check_delivery_gate(path: Path) -> None:
    """A batch QA's messages post only after run_gates.py passed for the checklist on disk."""
    folder = path.resolve().parent
    if not re.search(r"outputs/qa/batch-[^/]+$", folder.as_posix()):
        return
    receipt = folder / "gate_receipt.json"
    if not receipt.exists():
        raise Refused(f"no gate_receipt.json in {folder.name}: run_gates.py has not passed")
    r = json.loads(receipt.read_text(encoding="utf-8"))
    checklist = folder / r.get("checklist_file", "")
    if not r.get("all_gates_green") or not checklist.exists() or \
            hashlib.sha256(checklist.read_bytes()).hexdigest() != r.get("checklist_sha256"):
        raise Refused("gate_receipt.json is not green or does not match the checklist on disk")


def _post(token: str, text: str, thread_ts: str | None = None) -> str:
    body = {"channel": CHANNEL, "text": text, "unfurl_links": False, "unfurl_media": False}
    if thread_ts:
        body["thread_ts"] = thread_ts
    req = urllib.request.Request("https://slack.com/api/chat.postMessage", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {token}",
                                          "Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        out = json.loads(resp.read())
    if not out.get("ok"):
        raise RuntimeError(f"Slack refused the post: {out.get('error')}")
    return out["ts"]


def post_all(data: dict, token: str) -> list[dict]:
    posted = []
    for p in data["posts"]:
        ts = _post(token, p["text"], p.get("thread_ts"))
        replies = [_post(token, t, ts) for t in p.get("thread") or []]
        posted.append({"ts": ts, "replies": replies, "thread_ts": p.get("thread_ts")})
    return posted


def preview(data: dict) -> str:
    lines = [f"Destination: #team-mrv-alerts ({CHANNEL})"]
    for i, p in enumerate(data["posts"], 1):
        where = f"reply in thread {p['thread_ts']}" if p.get("thread_ts") else "new message"
        lines += ["", f"--- message {i} ({where}) ---", p["text"]]
        for j, t in enumerate(p.get("thread") or [], 1):
            lines += [f"    --- thread reply {j} ---", "    " + t.replace("\n", "\n    ")]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("delivery_json")
    ap.add_argument("--dry-run", action="store_true", help="validate and print, post nothing")
    a = ap.parse_args()
    path = Path(a.delivery_json)
    try:
        data = load(path)
        check_delivery_gate(path)
    except Refused as e:
        print(f"NOT POSTED: {e}", file=sys.stderr)
        return 2
    print(preview(data))
    if a.dry_run:
        return 0
    token = os.environ.get("SLACK_BOT_TOKEN", "")
    if not token.startswith("xoxb-"):
        print("NOT POSTED: SLACK_BOT_TOKEN is missing or not a bot token", file=sys.stderr)
        return 2
    print(json.dumps({"posted": post_all(data, token)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
