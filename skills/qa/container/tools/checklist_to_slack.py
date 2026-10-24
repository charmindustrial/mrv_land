#!/usr/bin/env python3
"""
checklist_to_slack.py — turn a finished QA checklist into the Slack post that delivers it.

The Slack post IS the checklist: a top-level message with the batch, the status counts,
every Fail in one line and any notes (e.g. evidence that changed after review), then the
full checklist in the thread, one reply per section, every row with its status, check,
evidence note and verifier reference. Built from the checklist file itself, so the post
cannot drift from what was checked.

  checklist_to_slack.py <Checklist.xlsx> --batch <ID> [--note TEXT ...] [--link URL]
                        --out delivery_messages.json

Checklist layout (the skills' spec): column A item number, B check, C status
(Pass / Fail / Flag / N/A), D evidence, E verifier reference; section header rows between.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ITEM = re.compile(r"^\d{1,2}[a-z]?\.\d{1,2}[a-z]?$")
STATUS = {"pass": "Pass", "fail": "Fail", "flag": "Flag", "n/a": "N/A", "na": "N/A"}
ICON = {"Pass": "✅", "Fail": "🔴", "Flag": "🟡", "N/A": "⚪"}
MAX_REPLY = 3500            # stay well under Slack's per-message limit


def esc(s) -> str:
    """Slack mrkdwn escaping: &, <, > must be entities (this also neutralises any <@...>)."""
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").strip()


def read_checklist(path: Path) -> list[dict]:
    """Sections in order, each {"title", "rows": [{item, check, status, evidence, ref}]}."""
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    sections, current = [], {"title": "Checklist", "rows": []}
    for row in ws.iter_rows(values_only=True):
        cells = list(row[:5]) + [None] * (5 - len(row[:5]))
        a, b, c, d, e = (str(x).strip() if x is not None else "" for x in cells)
        status = STATUS.get(c.lower()) if c else None
        if ITEM.match(a) and status:
            current["rows"].append({"item": a, "check": b, "status": status, "evidence": d, "ref": e})
        elif a and not status and not ITEM.match(a) and (re.match(r"^(section\s+)?\d{1,2}[a-z]?[.:)]?\s+\S", a, re.I)):
            if current["rows"]:
                sections.append(current)
            current = {"title": a if not b else f"{a} {b}", "rows": []}
    if current["rows"]:
        sections.append(current)
    return sections


def build(path: Path, batch: str, notes: list[str], link: str | None) -> dict:
    sections = read_checklist(path)
    rows = [r for s in sections for r in s["rows"]]
    if not rows:
        raise SystemExit(f"No checklist rows found in {path.name}")
    counts = {k: sum(r["status"] == k for r in rows) for k in ("Pass", "Fail", "Flag", "N/A")}
    lede = [f"*QA complete: {esc(batch)}*  {counts['Pass']} Pass · {counts['Fail']} Fail · "
            f"{counts['Flag']} Flag · {counts['N/A']} N/A  (full checklist in thread)"]
    fails = [r for r in rows if r["status"] == "Fail"]
    if fails:
        lede.append("*Fails:*")
        lede += [f"🔴 *{esc(r['item'])}* {esc(r['check'])[:160]}" for r in fails]
    for n in notes:
        lede.append(f"_Note: {esc(n)}_")
    if link:
        lede.append(f"Checklist file: {esc(link)}")
    replies = []
    for s in sections:
        head = f"*{esc(s['title'])}*"
        chunk = head
        for r in s["rows"]:
            line = (f"\n{ICON[r['status']]} *{esc(r['item'])} {r['status']}* {esc(r['check'])}"
                    + (f"\n    {esc(r['evidence'])}" if r["evidence"] else "")
                    + (f"\n    _Ref: {esc(r['ref'])}_" if r["ref"] else ""))
            if len(chunk) + len(line) > MAX_REPLY and chunk != head:
                replies.append(chunk)
                chunk = head + " (cont.)"
            chunk += line[:MAX_REPLY - len(head) - 20]
        replies.append(chunk)
    return {"posts": [{"text": "\n".join(lede), "thread": replies}],
            "source": {"checklist": path.name, "rows": len(rows), "counts": counts}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("checklist")
    ap.add_argument("--batch", required=True)
    ap.add_argument("--note", action="append", default=[])
    ap.add_argument("--link")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = build(Path(a.checklist), a.batch, a.note, a.link)
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    c = out["source"]["counts"]
    print(f"wrote {a.out}: {out['source']['rows']} rows ({c}), {len(out['posts'][0]['thread'])} thread replies")
    return 0


if __name__ == "__main__":
    sys.exit(main())
