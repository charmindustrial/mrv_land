---
name: pace-report-generate
description: >
  Weekly MRV Pace Report generator for Charm Industrial. Fired by macOS launchd
  every Wednesday at 15:00 local (also safe to run ad-hoc). Copies the Pace
  Report template in Drive, names it for the following day (Thursday), carries
  each person's "Top 3 I'll Focus On Next Week" items from the current live
  report into "Last Week's Focus - Did It Land" on the matching tab of the new
  one (Max stays with Max, Garrett stays with Garrett), moves every prior
  report into Deprecated/Past, then posts a link to #team-mrv asking the team
  to fill out their section. Hands off to the pace-report-finalize skill,
  which watches for a completion reply and posts to #team-strategery.
  ALWAYS trigger when: a
  scheduled run fires this job, Max says "run the pace report", "generate this
  week's pace report", "Wednesday pace report", or asks about the state of
  this automation.
---

# MRV Pace Report — Weekly Generator

Runs **one full pass** each invocation: create this week's report, carry
forward last week's stated focus items into the new look-back section, move
every prior report into Deprecated/Past, and post to #team-mrv. It does NOT
wait for a reply and does NOT post to #team-strategery — that's
`pace-report-finalize`'s job, triggered once someone replies "Complete" (or
similar) in the thread this skill posts.

**Deprecated move happens here, every week (since 2026-10-12).** Max said on
2026-08-27 and again on 2026-09-10 that prior reports go in the Deprecated
subfolder. The move used to wait for a "Complete" reply in #team-mrv, which
nobody posts, so 9/17, 9/24 and 10/1 piled up in the live folder. The live
folder must hold only the template, the Deprecated/Past subfolder, and the
newest report. `generate_pace_report.py` enforces this right after upload.
`python3 generate_pace_report.py --deprecate-only` does the move alone.

**Config (read first, fail loud if missing):** `config.json` in this folder
holds every changeable fact — channel IDs, Drive folder IDs/paths, the
template file ID, the exact post message. Never hardcode any of these in
prose or in a command; read them from config. Per the workspace rule "skills
hold logic, not facts."

**Autonomous send is authorized for this automation** — see
`_autonomous_send_comment` in config.json. Standing exception scoped only to
this skill's #team-mrv post.

---

## The pass (run top to bottom, every invocation)

### 0. Load config + state
- Read `config.json`.
- Read `state_path`. If it does not exist, treat it as `{"pending_cycles": []}`
  and create it at the end.
- Compute `target_thursday` = tomorrow's date (the day after the Wednesday
  this pass is running). If a pass ever runs on a day other than Wednesday
  (e.g. an ad-hoc test run), still use "tomorrow" — that is the literal rule
  Max gave.
- **Idempotency guard:** if `pending_cycles` already has an entry whose
  `week_date` equals `target_thursday`, a report for this week already
  exists — print `NO-ACTION: already generated for <target_thursday>` and
  stop.

### 1–4. Build the file — one script call, not five tool calls
**Superseded 2026-09-17 after the 09-09 and 09-16 scheduled runs both died at
the 900s watchdog with nothing to show for it.** The 09-16 log
(`~/.pace-report/generate-run.log`) shows the exact death: the model
downloaded the template via `download_file_content`, got it back as an inline
base64 string, and tried to retype that string into a `python3 -c` command to
decode it. At real xlsx size that generation ran past the 32,000-output-token
ceiling, the turn errored out 13 minutes in, and the watchdog killed the run
five minutes later having produced nothing — no file, no Slack post, no
state.json entry, and no visible error until someone went looking at raw
logs. This is the same base64-retyping failure the 2026-09-10 rewrite above
already fixed for the *local-mount* path; it was never fixed for the *Drive
API download* path, and that's the path that's actually run every week.

The fix: file bytes never pass through model output. One program does steps
1–4 end to end using the Drive API directly (list folder → download template
+ source → run `populate_report.py` → upload the result), authenticating
with the OAuth token this workspace already uses for the EAC inventory
monitor (`google_token_path` in config.json, scopes include `drive`).

Run:
```
python3 generate_pace_report.py --target <target_thursday ISO date, e.g. 2026-09-24>
```
- Prints `NO-ACTION: ...` and exits 0 if this week is already recorded in
  `state.json` or a file with the target title already exists in Drive (e.g.
  someone built it by hand) — **do not overwrite an existing file**, human-made
  or automated.
- Prints `FAILED: <reason>` and exits 1 on any real problem (missing token,
  no source candidate, `populate_report.py` failing) — stop and tell Max,
  same as any other FAILED in this workflow.
- On success prints one JSON line to stdout with `new_file_id`,
  `new_file_title`, `new_file_web_link`, `source_file_id`, `source_file_title`,
  `populate_output`, and `deprecated` (names of the reports it moved into
  Deprecated/Past) — everything steps 5–6 below need. Parse it; don't
  re-derive any of those values.

### 5. Post to #team-mrv
- Post one message to `slack_team_mrv_channel_id`:
  ```
  <team_mrv_post_message>
  <new_file_web_link from the script's JSON output>
  ```
- Note the returned message's `ts` — this is the thread anchor
  `pace-report-finalize` will watch.

### 6. Record the pending cycle
Append to `state_path`'s `pending_cycles` array, using the script's JSON
output directly for every field except the Slack ones:
```json
{
  "week_date": "<target_thursday ISO date>",
  "new_file_id": "<new_file_id from script output>",
  "new_file_title": "<new_file_title from script output>",
  "new_file_local_path": "<new_file_local_path from script output>",
  "new_file_web_link": "<new_file_web_link from script output>",
  "thread_channel_id": "<slack_team_mrv_channel_id>",
  "thread_ts": "<the message ts from step 5>",
  "source_file_id": "<source_file_id from script output>",
  "source_file_title": "<source_file_title from script output>",
  "source_file_local_path": "<source_file_local_path from script output>",
  "created_at": "<now, ISO timestamp>"
}
```
Write the whole file back (pretty-printed JSON is fine). This is what makes
`pace-report-finalize` able to find and close this cycle later, and what
makes a missed generate run self-evident (the array just grows if finalize
never sees a completion).

**If Max or Garrett builds the file by hand before this runs** (as happened
2026-09-17, when the automated run's silent failure went unnoticed until the
next morning): skip straight to step 6 using the hand-built file's real id,
title, and web link, and the `ts` of whatever Slack message announced it —
do not build a second, competing file.

---

## Post a completion line for observability
When run headlessly, write a one-line result to the launchd log (stdout):
either `NO-ACTION: already generated for <date>` or
`GENERATED: <new_file_title> — posted to #team-mrv (ts <thread_ts>), carried
forward from <source_file_title>`.

## Scheduling
Fired by `~/Library/LaunchAgents/com.charm.pace-report-generate.plist` via the
runner `~/.pace-report/generate-run.sh`, which invokes Claude Code headless in
the MRV Expert workspace and triggers this skill. Runs Wednesdays at 15:00
local. See `pace-report-finalize/SKILL.md` for the async completion-watching
half of this workflow.
