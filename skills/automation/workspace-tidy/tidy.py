#!/usr/bin/env python3
"""Weekly tidy of the MRV Expert workspace.

Built 2026-10-13 after the folder needed a full hand clean-up for the third
time (2026-05-05, 2026-07-27, 2026-10-13). Each rule below is a kind of mess
that actually turned up; nothing is guessed.

Nothing is thrown away that could be work. Anything unknown is MOVED to
archive/, never deleted. Only these are deleted:
  - known junk at the root ("<property object at 0x...>" files: a guard-script
    bug on 2026-09-24 left 130 of them)
  - empty folder trees at the root (a path split at the space in "MRV Expert"
    left an empty Expert/ tree on 2026-09-29)
  - leftover Office lock files (~$name, .~lock.name#), only when that Office
    program is not running or the lock is over 7 days old
  - browser captures in .playwright-mcp/ (page snapshots and console logs over
    7 days old, downloads over 30 days old; all can be fetched again)

Then it saves everything to git and pushes to GitHub, so the backup is checked
every week. (The every-turn backup hook had silently stopped on 2026-04-29.)

Usage:  python3 tidy.py            show what would happen, change nothing
        python3 tidy.py --apply    do it
The last line printed is "OK: ..." or "FAILED: ...".
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parents[3]

ROOT_FILES = {"CLAUDE.md", "README.txt", "FOLDER_INDEX.md", ".gitignore",
              ".gitattributes", ".mcp.json", ".DS_Store"}
ROOT_DIRS = {"skills", "outputs", "knowledge-base", "archive", ".claude",
             ".git", ".playwright-mcp"}
ROOT_JUNK = re.compile(r"^<property object at 0x[0-9a-f]+>")
OFFICE_LOCK = re.compile(r"^(~\$|\.~lock\.)")
OFFICE_APPS = ("Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint", "soffice")
LOCK_DAYS = 7
SNAPSHOT_DAYS = 7          # .playwright-mcp page snapshots / console logs
DOWNLOAD_DAYS = 30         # .playwright-mcp downloaded files
SNAPSHOT_EXT = {".yml", ".yaml", ".log"}
MISROUTED_NAMES = {"outputs", "temp", "tmp"}   # folders that never belong inside skills/
GITHUB_MAX_MB = 95         # GitHub refuses files over 100 MB
LOG = WS / "outputs/automation/workspace-tidy/run-log.jsonl"

TODAY = datetime.date.today().isoformat()
NOW = time.time()


def days_old(p):
    return (NOW - p.lstat().st_mtime) / 86400


def has_files(d):
    for _, _, files in os.walk(d, followlinks=False):
        if any(f != ".DS_Store" for f in files):
            return True
    return False


def free_dest(dest):
    """dest, or dest with ' (2)', ' (3)'... if something is already there."""
    if not dest.exists():
        return dest
    n = 2
    while True:
        cand = dest.with_name(f"{dest.stem} ({n}){dest.suffix}")
        if not cand.exists():
            return cand
        n += 1


def office_running():
    try:
        out = subprocess.run(["ps", "-axo", "comm="], capture_output=True, text=True).stdout
    except Exception:
        return True   # can't tell: treat as running, so only old locks go
    return any(app in out for app in OFFICE_APPS)


def plan():
    """Every action as (kind, path, destination-or-None, reason)."""
    acts = []

    # 1. the root
    for p in sorted(WS.iterdir()):
        name = p.name
        if p.is_dir() and not p.is_symlink():
            if name in ROOT_DIRS:
                continue
            if not has_files(p):
                acts.append(("delete", p, None, "empty folder at the root"))
            else:
                acts.append(("move", p, WS / "archive/root-sweep" / TODAY / name,
                             "folder at the root that belongs in one of the four content folders"))
        else:
            if name in ROOT_FILES:
                continue
            if ROOT_JUNK.match(name):
                acts.append(("delete", p, None, "guard-script junk file"))
            elif OFFICE_LOCK.match(name):
                pass   # handled below with the other lock files
            else:
                acts.append(("move", p, WS / "archive/root-sweep" / TODAY / name,
                             "loose file at the root"))

    # 2. leftover Office lock files, anywhere
    running = office_running()
    for dirpath, dirnames, files in os.walk(WS, followlinks=False):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".playwright-mcp")]
        for f in files:
            if OFFICE_LOCK.match(f):
                p = Path(dirpath) / f
                if not running or days_old(p) > LOCK_DAYS:
                    acts.append(("delete", p, None, "leftover Office lock file"))

    # 3. output folders that landed inside skills/
    for dirpath, dirnames, _ in os.walk(WS / "skills", followlinks=False):
        for d in list(dirnames):
            if d in MISROUTED_NAMES:
                p = Path(dirpath) / d
                rel = p.relative_to(WS)
                acts.append(("move", p, WS / "archive/misrouted" / TODAY / rel,
                             "output folder inside skills/; outputs belong under outputs/"))
                dirnames.remove(d)

    # 4. browser captures
    pw = WS / ".playwright-mcp"
    if pw.is_dir():
        for p in pw.rglob("*"):
            if p.is_file() and not p.is_symlink():
                limit = SNAPSHOT_DAYS if p.suffix.lower() in SNAPSHOT_EXT else DOWNLOAD_DAYS
                if days_old(p) > limit:
                    acts.append(("delete", p, None, f"browser capture over {limit} days old"))
    return acts


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(WS), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])}: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def wait_for_git():
    """Another session's backup hook may be mid-commit; wait up to 2 minutes."""
    lock = WS / ".git/index.lock"
    for _ in range(24):
        if not lock.exists():
            return
        time.sleep(5)
    raise RuntimeError("git was busy (.git/index.lock) for 2 minutes")


def save_to_github(summary):
    """Stage everything, hold back files GitHub would refuse, commit, push."""
    wait_for_git()
    git("add", "-A")
    too_big = []
    for rel in git("diff", "--cached", "--name-only", "-z", "--diff-filter=AM").stdout.split("\0"):
        if rel and (WS / rel).is_file() and (WS / rel).stat().st_size > GITHUB_MAX_MB * 1024 * 1024:
            too_big.append(rel)
    if too_big:
        git("reset", "-q", "--", *too_big)
        with open(WS / ".git/info/exclude", "a") as f:
            for rel in too_big:
                f.write("/" + rel + "\n")
    staged = [x for x in git("diff", "--cached", "--name-only", "-z").stdout.split("\0") if x]
    if staged:
        msg = (f"Weekly tidy {TODAY}: {summary}; {len(staged)} file(s) saved\n\n"
               "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
        git("commit", "-q", "-m", msg)
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    # The every-turn backup hook pushes the same branch from this same folder;
    # on 2026-10-13 the two pushes collided ("cannot lock ref"). Wait, retry.
    for attempt in range(4):
        push = git("push", "-q", "origin", branch, check=False)
        if push.returncode == 0:
            break
        time.sleep(30)
        git("fetch", "-q", "origin", branch, check=False)
    if push.returncode != 0:
        raise RuntimeError(f"push to GitHub failed: {(push.stderr or push.stdout).strip()[:300]}")
    git("fetch", "-q", "origin", branch, check=False)
    ahead = git("rev-list", "--count", f"origin/{branch}..HEAD").stdout.strip()
    if ahead != "0":
        raise RuntimeError(f"after pushing, GitHub is still {ahead} commit(s) behind")
    return len(staged), too_big


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="make the changes (default: only show them)")
    ap.add_argument("--no-git", action="store_true", help="tidy only; skip the git save and push")
    a = ap.parse_args()

    acts = plan()
    deleted = moved = 0
    moved_list = []
    for kind, p, dest, why in acts:
        rel = p.relative_to(WS)
        if not a.apply:
            print(f"would {kind}: {rel}" + (f" -> {dest.relative_to(WS)}" if dest else "") + f"  ({why})")
            continue
        if kind == "delete":
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink(missing_ok=True)
            deleted += 1
        else:
            dest = free_dest(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dest))
            moved += 1
            moved_list.append(f"{rel} -> {dest.relative_to(WS)}")
            print(f"moved: {rel} -> {dest.relative_to(WS)}  ({why})")

    if not a.apply:
        print(f"OK: dry run, {len(acts)} change(s) found, nothing changed")
        return 0

    summary = f"deleted {deleted} junk file(s), moved {moved} item(s) to archive/"
    record = {"date": TODAY, "deleted": deleted, "moved": moved_list}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

    if a.no_git:
        print(f"OK: workspace tidy, {summary}; git skipped")
        return 0
    try:
        saved, too_big = save_to_github(summary)
    except Exception as e:
        print(f"FAILED: workspace tidy finished ({summary}) but the GitHub save did not: {e}")
        return 1
    if too_big:
        print(f"FAILED: {len(too_big)} file(s) are over GitHub's size limit and were left out of the backup: "
              + ", ".join(too_big))
        return 1
    print(f"OK: workspace tidy, {summary}; {saved} file(s) saved and pushed to GitHub")
    return 0


if __name__ == "__main__":
    sys.exit(main())
