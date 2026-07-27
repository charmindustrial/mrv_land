#!/usr/bin/env python3
"""
Compute Anthropic API cost for a batch QA session by reading Claude Code's
local transcripts.

Usage:
    python compute_batch_token_cost.py 2-187
    python compute_batch_token_cost.py --all
    python compute_batch_token_cost.py 2-188 --window-hours 6

The script finds all Claude Code session transcripts whose aiTitle names the
batch ID (e.g., "QA batch 2-187 certification review") and sums token usage
across every assistant turn in those sessions. If batch_timestamps.json
exists for the batch, turns are clipped to [T0 - 5min, T_last + window-hours].

Pricing assumes claude-opus-4-7 (Opus 4.7). Override via --pricing-json.
"""

import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

WORKSPACE = Path("/Users/maxlavine/Desktop/Claude/Skills/MRV Expert")
PROJECT_TRANSCRIPTS = Path(
    "/Users/maxlavine/.claude/projects/-Users-maxlavine-Desktop-Claude-Skills-MRV-Expert"
)

# Opus 4.7 pricing — $/million tokens
DEFAULT_PRICING = {
    "input": 15.00,
    "output": 75.00,
    "cache_write_5m": 18.75,   # 1.25x input
    "cache_write_1h": 30.00,   # 2.0x input
    "cache_read": 1.50,        # 0.10x input
}


def parse_ts(s):
    if not s:
        return None
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def load_batch_window(batch_id):
    """Return (T0, T_last) from batch_timestamps.json or (None, None)."""
    ts_path = WORKSPACE / f"outputs/qa/batch-{batch_id}/batch_timestamps.json"
    if not ts_path.exists():
        return None, None
    data = json.loads(ts_path.read_text())
    t0 = data.get("T0_initiation") or data.get("T0")
    t_final_keys = [k for k in data if k.startswith("T_final")]
    if t_final_keys:
        t_last = data[t_final_keys[0]]
    else:
        t_keys = sorted(
            k for k in data if k.startswith("T") and "_" in k and k[1:2].isdigit()
        )
        t_last = data.get(t_keys[-1]) if t_keys else None
    return parse_ts(t0), parse_ts(t_last)


def session_matches_batch(session_path, batch_id):
    """A session belongs to a batch if its aiTitle mentions the batch ID."""
    title_re = re.compile(rf"\b{re.escape(batch_id)}\b")
    with open(session_path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            title = d.get("aiTitle")
            if title and title_re.search(title) and "QA" in title.upper():
                return True
    return False


def sum_session_tokens(session_path, t0=None, t_last=None, window_hours=2):
    """Sum token usage across assistant turns in a session, optionally clipped
    to [t0 - 5min, t_last + window_hours]."""
    totals = defaultdict(int)
    turn_count = 0
    first_ts, last_ts = None, None

    if t0:
        clip_start = t0 - dt.timedelta(minutes=5)
    else:
        clip_start = None
    if t_last:
        clip_end = t_last + dt.timedelta(hours=window_hours)
    else:
        clip_end = None

    with open(session_path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            ts = parse_ts(d.get("timestamp"))
            if ts:
                if clip_start and ts < clip_start:
                    continue
                if clip_end and ts > clip_end:
                    continue
                if not first_ts or ts < first_ts:
                    first_ts = ts
                if not last_ts or ts > last_ts:
                    last_ts = ts

            msg = d.get("message", {})
            if not isinstance(msg, dict):
                continue
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                continue

            turn_count += 1
            totals["input_tokens"] += usage.get("input_tokens", 0)
            totals["output_tokens"] += usage.get("output_tokens", 0)
            totals["cache_read_input_tokens"] += usage.get(
                "cache_read_input_tokens", 0
            )

            cw = usage.get("cache_creation", {}) or {}
            totals["cache_write_5m_tokens"] += cw.get(
                "ephemeral_5m_input_tokens", 0
            )
            totals["cache_write_1h_tokens"] += cw.get(
                "ephemeral_1h_input_tokens", 0
            )

    totals["turn_count"] = turn_count
    totals["first_ts"] = first_ts.isoformat() if first_ts else None
    totals["last_ts"] = last_ts.isoformat() if last_ts else None
    return totals


def compute_cost(tokens, pricing):
    """Apply $/M pricing to token totals."""
    return {
        "input": tokens["input_tokens"] / 1e6 * pricing["input"],
        "output": tokens["output_tokens"] / 1e6 * pricing["output"],
        "cache_write_5m": tokens["cache_write_5m_tokens"]
        / 1e6
        * pricing["cache_write_5m"],
        "cache_write_1h": tokens["cache_write_1h_tokens"]
        / 1e6
        * pricing["cache_write_1h"],
        "cache_read": tokens["cache_read_input_tokens"]
        / 1e6
        * pricing["cache_read"],
    }


def discover_all_batches():
    """Scan outputs/qa/ for batch-X-XXX directories with timestamps."""
    out = []
    for p in sorted((WORKSPACE / "outputs/qa").glob("batch-*")):
        m = re.match(r"batch-(\d+-\d+)$", p.name)
        if m:
            out.append(m.group(1))
    return out


def report_batch(batch_id, pricing, window_hours=2, verbose=False):
    t0, t_last = load_batch_window(batch_id)
    sessions = sorted(glob.glob(str(PROJECT_TRANSCRIPTS / "*.jsonl")))
    matched = [s for s in sessions if session_matches_batch(s, batch_id)]

    aggregate = defaultdict(int)
    aggregate["session_ids"] = []
    for s in matched:
        sid = os.path.basename(s).replace(".jsonl", "")
        tokens = sum_session_tokens(s, t0, t_last, window_hours=window_hours)
        if tokens["turn_count"] == 0:
            continue
        aggregate["session_ids"].append(sid)
        for k in (
            "input_tokens",
            "output_tokens",
            "cache_read_input_tokens",
            "cache_write_5m_tokens",
            "cache_write_1h_tokens",
            "turn_count",
        ):
            aggregate[k] += tokens[k]
        if verbose:
            cost = compute_cost(tokens, pricing)
            print(
                f"  session {sid[:8]}: turns={tokens['turn_count']}  "
                f"in={tokens['input_tokens']:,}  out={tokens['output_tokens']:,}  "
                f"cache_r={tokens['cache_read_input_tokens']:,}  "
                f"$={sum(cost.values()):.2f}"
            )

    cost = compute_cost(aggregate, pricing)
    aggregate["cost_usd"] = cost
    aggregate["total_cost_usd"] = sum(cost.values())
    aggregate["batch_id"] = batch_id
    aggregate["t0"] = t0.isoformat() if t0 else None
    aggregate["t_last"] = t_last.isoformat() if t_last else None
    aggregate["pricing_used"] = pricing
    return aggregate


def fmt_row(b):
    return (
        f"{b['batch_id']:>7}  "
        f"{b['turn_count']:>5}  "
        f"{b['input_tokens']:>11,}  "
        f"{b['output_tokens']:>9,}  "
        f"{b['cache_read_input_tokens']:>13,}  "
        f"{b['cache_write_5m_tokens']:>13,}  "
        f"{b['cache_write_1h_tokens']:>13,}  "
        f"${b['total_cost_usd']:>7.2f}"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("batch_id", nargs="?", help="Batch ID, e.g., 2-187")
    p.add_argument("--all", action="store_true", help="Cost every batch in outputs/qa/")
    p.add_argument(
        "--window-hours",
        type=float,
        default=2.0,
        help="Hours after T_last to still count turns (default 2)",
    )
    p.add_argument(
        "--pricing-json",
        help="Path to JSON file overriding default pricing",
    )
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument(
        "--write-summary",
        action="store_true",
        help="Write per-batch JSON to outputs/qa/batch-<id>/token_cost.json",
    )
    args = p.parse_args()

    pricing = DEFAULT_PRICING
    if args.pricing_json:
        pricing = json.loads(Path(args.pricing_json).read_text())

    if not args.batch_id and not args.all:
        p.error("Provide a batch_id or --all")

    batch_ids = discover_all_batches() if args.all else [args.batch_id]

    header = (
        f"{'batch':>7}  {'turns':>5}  {'input_tok':>11}  {'output':>9}  "
        f"{'cache_read':>13}  {'cache_w_5m':>13}  {'cache_w_1h':>13}  {'$total':>8}"
    )
    print(header)
    print("-" * len(header))

    grand = defaultdict(int)
    grand_cost = 0.0
    for bid in batch_ids:
        if args.verbose:
            print(f"\n=== batch {bid} ===")
        result = report_batch(bid, pricing, args.window_hours, args.verbose)
        if result["turn_count"] == 0:
            print(f"{bid:>7}  no matching session transcripts found")
            continue
        print(fmt_row(result))
        grand_cost += result["total_cost_usd"]
        for k in (
            "input_tokens",
            "output_tokens",
            "cache_read_input_tokens",
            "cache_write_5m_tokens",
            "cache_write_1h_tokens",
            "turn_count",
        ):
            grand[k] += result[k]

        if args.write_summary:
            out = WORKSPACE / f"outputs/qa/batch-{bid}/token_cost.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, indent=2, default=str))

    if args.all and len(batch_ids) > 1:
        print("-" * len(header))
        print(
            f"{'TOTAL':>7}  {grand['turn_count']:>5}  "
            f"{grand['input_tokens']:>11,}  {grand['output_tokens']:>9,}  "
            f"{grand['cache_read_input_tokens']:>13,}  "
            f"{grand['cache_write_5m_tokens']:>13,}  "
            f"{grand['cache_write_1h_tokens']:>13,}  ${grand_cost:>7.2f}"
        )
        n = sum(1 for b in batch_ids)
        print(f"\nMean cost / batch: ${grand_cost / n:.2f}")


if __name__ == "__main__":
    main()
