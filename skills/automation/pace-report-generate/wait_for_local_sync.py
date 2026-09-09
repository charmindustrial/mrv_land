#!/usr/bin/env python3
"""
Waits for a local file to appear (Drive Desktop sync is not instant after a
Drive-side copy_file call). Bounded and observable -- prints a progress line
every interval so a caller tailing the log can see it is not stuck silently.

Usage: wait_for_local_sync.py <path> [--timeout SECONDS] [--interval SECONDS]
Exit 0 the moment the path exists. Exit 1 if the timeout elapses first --
that is a real failure to report, not something to keep waiting past.
"""
import argparse
import os
import sys
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--interval", type=float, default=2.5)
    args = ap.parse_args()

    start = time.time()
    while True:
        elapsed = time.time() - start
        if os.path.exists(args.path):
            print(f"OK: found after {elapsed:.1f}s -- {args.path}", flush=True)
            return 0
        if elapsed >= args.timeout:
            print(f"FAILED: not found after {args.timeout:.0f}s -- {args.path}", flush=True)
            return 1
        print(f"...waiting ({elapsed:.1f}s elapsed) -- {args.path}", flush=True)
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
