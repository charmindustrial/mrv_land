---
name: workspace-tidy
description: Weekly clean-up of the MRV Expert workspace folder, plus its GitHub backup. Fired by the shared scheduled-job launcher every Monday 07:00 Pacific; also safe to run ad-hoc. Runs one fixed script (tidy.py) that deletes known junk, moves anything unknown at the root (or output folders inside skills/) into archive/, prunes old browser captures, then saves everything to git and pushes to GitHub. ALWAYS trigger when Max says "tidy the workspace", "clean up the folder", "the folder is a mess", "run the workspace tidy", or asks about the state of this automation or the GitHub backup of this folder.
---

# Workspace tidy

Built 2026-10-13 after the third full hand clean-up (2026-05-05, 2026-07-27, 2026-10-13).

## What to do

Run, from the workspace root:

```
python3 skills/automation/workspace-tidy/tidy.py --apply
```

Print the script's last line as your final status line, unchanged. Do not move, rename, or delete anything by hand, and do not add rules on the fly: an unattended run must do exactly what the script does. If the script prints `FAILED:`, stop there.

To preview without changing anything, run it without `--apply`.

## What the script does

| Mess | Action |
|---|---|
| `<property object at 0x…>` files at the root | delete (guard-script bug, 2026-09-24) |
| Empty folder trees at the root | delete (unquoted path split at "MRV Expert", 2026-09-29) |
| Any other file or folder at the root not on the allowed list | move to `archive/root-sweep/<date>/` |
| Office lock files (`~$name`, `.~lock.name#`) | delete when that Office program isn't running, or the lock is over 7 days old |
| `outputs/`, `temp/`, `tmp/` folders inside `skills/` | move to `archive/misrouted/<date>/` |
| `.playwright-mcp/` page snapshots and console logs over 7 days old; downloads over 30 days old | delete (can be fetched again) |
| Everything else | `git add -A`, commit, push to `origin`; fail if GitHub is still behind afterwards |

Allowed at the root: `CLAUDE.md`, `README.txt`, `FOLDER_INDEX.md`, `.gitignore`, `.gitattributes`, `.mcp.json`, and the folders `skills/`, `outputs/`, `knowledge-base/`, `archive/`, `.claude/`, `.playwright-mcp/`.

Files over 95 MB are held back from git (GitHub refuses files over 100 MB), listed in `.git/info/exclude`, and reported as `FAILED:` so Max hears about it once.

Each run appends what it deleted and moved to `outputs/automation/workspace-tidy/run-log.jsonl`.

## Scheduling

Scheduled job `workspace-tidy` in `~/.claude/scheduled/` (instructions in `jobs/workspace-tidy/prompt.txt`). It is a Claude job, not a plain-script job, because macOS blocks launchd-started scripts from touching anything under ~/Desktop; only the `claude` program has that access.

## Prevention

`.claude/hooks/workspace_hygiene_guard.sh` blocks Claude from writing any new file at the root. The weekly sweep catches what scripts and other programs leave behind.
