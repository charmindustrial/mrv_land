---
name: pace-report-generate
description: >
  Weekly MRV Pace Report generator for Charm Industrial. Fired by macOS launchd
  every Wednesday at 15:00 local (also safe to run ad-hoc). Copies the Pace
  Report template in Drive, names it for the following day (Thursday), carries
  each person's "Top 3 I'll Focus On Next Week" items from the current live
  report into "Last Week's Focus - Did It Land" on the matching tab of the new
  one (Max stays with Max, Garrett stays with Garrett), then posts a link to
  #team-mrv asking the team to fill out their section. Hands off to the
  pace-report-finalize skill, which watches for a completion reply and closes
  the loop (Deprecated move + #team-strategery post). ALWAYS trigger when: a
  scheduled run fires this job, Max says "run the pace report", "generate this
  week's pace report", "Wednesday pace report", or asks about the state of
  this automation.
---

# MRV Pace Report — Weekly Generator

Runs **one full pass** each invocation: create this week's report, carry
forward last week's stated focus items into the new look-back section, and
post to #team-mrv. It does NOT wait for a reply and does NOT touch the
Deprecated folder or #team-strategery — that's `pace-report-finalize`'s job,
triggered separately and asynchronously once someone replies "Complete" (or
similar) in the thread this skill posts.

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

### 1. Find the current live report (the copy source)
- List the contents of `parent_folder_id` via Drive `search_files`
  (`parentId = '<parent_folder_id>'`).
- The **source report** is the most-recently-created `.xlsx` in that listing
  that is NOT the template (`template_file_id`) and is not a folder. Use
  `createdTime` to pick the most recent if more than one candidate exists.
- If no candidate exists (empty folder, first-ever run), stop and tell Max —
  do not guess or fabricate a source; this needs a human to seed the first
  report.

### 2. Copy the template
- `copy_file(fileId=template_file_id, parentId=parent_folder_id, title=<new_file_title_format filled in with target_thursday's month/day, no leading zeros, matching existing convention e.g. "8/27 MRV Weekly Pace Report.xlsx">)`.
- **The title MUST end in `.xlsx`** (config.json's `new_file_title_format` already
  has it — don't strip it). Verified 2026-08-27: `copy_file` does not append an
  extension on its own, and a title without one produces a file `openpyxl`
  refuses to open (`InvalidFileException`), which would silently break every
  weekly run at the populate step.
- Note the returned file's `id`.
- Resolve its local mount path: `drive_local_folder` + "/" + the title with
  "/" replaced by " " (the local Drive mount substitutes a space for the
  slash in the filename) + ".xlsx".
- **Wait for local sync**: Drive Desktop sync is not instant, so run
  ```
  python3 wait_for_local_sync.py "<new_local_path>" --timeout 60
  ```
  instead of polling yourself turn-by-turn. **Why this changed:** the
  2026-09-02 run stalled for the full 900s watchdog window and never
  reached the populate or Slack-post steps — the log
  (`~/.pace-report/generate-run.log`) shows only the start line and the
  watchdog kill, with nothing in between, because this step used to be
  "poll for the file yourself every 2–3 seconds" as a manual, self-paced
  loop of individual tool calls with no hard stop enforced by anything
  other than the model's own follow-through. That is the most likely place
  an unbounded loop turned into a 15-minute stall. The script above enforces
  the 60-second bound in actual code — it will print one progress line every
  ~2.5s and then either `OK: found after <n>s -- <path>` or `FAILED: not
  found after 60s -- <path>` and exit. If it prints `FAILED:`, stop and tell
  Max — do not keep waiting past it, do not invent another way to check.
- Resolve the source report's local path the same way, using its Drive
  title from step 1.

### 3. Populate the new report
Run:
```
python3 populate_report.py "<source_local_path>" "<new_local_path>" "<target_thursday ISO date, e.g. 2026-09-03>"
```
This writes the "Week of" date and carries each person's Top-3-next-week
items into their Last-week's-focus section, tab by tab, without mixing Max's
and Garrett's items. The script now reads the file back after saving and
confirms the date it wrote is actually there before printing `OK:` — added
after a 2026-08-27-vintage report was found still showing the template's
literal `YYYY-MM-DD` placeholder in a fully-populated file, meaning that
write had silently not persisted. Read the script's output line — it should
start with `OK:`. If it starts with `FAILED:`, stop and tell Max what broke;
do not paper over it.

### 4. Post to #team-mrv
- Get the new file's `webViewLink` (via `get_file_metadata` on its ID if not
  already returned by the copy).
- Post one message to `slack_team_mrv_channel_id`:
  ```
  <team_mrv_post_message>
  <the new report's Drive link>
  ```
- Note the returned message's `ts` — this is the thread anchor
  `pace-report-finalize` will watch.

### 5. Record the pending cycle
Append to `state_path`'s `pending_cycles` array:
```json
{
  "week_date": "<target_thursday ISO date>",
  "new_file_id": "<new file's Drive id>",
  "new_file_title": "<new file's title>",
  "new_file_local_path": "<new file's local path>",
  "new_file_web_link": "<new file's webViewLink>",
  "thread_channel_id": "<slack_team_mrv_channel_id>",
  "thread_ts": "<the message ts from step 4>",
  "source_file_id": "<source report's Drive id>",
  "source_file_title": "<source report's title>",
  "source_file_local_path": "<source report's local path>",
  "created_at": "<now, ISO timestamp>"
}
```
Write the whole file back (pretty-printed JSON is fine). This is what makes
`pace-report-finalize` able to find and close this cycle later, and what
makes a missed generate run self-evident (the array just grows if finalize
never sees a completion).

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
