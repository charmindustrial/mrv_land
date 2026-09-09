---
name: pace-report-finalize
description: >
  Watches for completion replies on MRV Pace Report threads in #team-mrv and
  closes the loop for each one. Fired by macOS launchd a few times a day
  (weekday business hours), also safe to run ad-hoc. For every pending cycle
  recorded by pace-report-generate, checks whether anyone has replied
  "Complete" (or similar) in the #team-mrv thread; if so, moves the report
  that cycle's items were carried forward FROM into the Deprecated subfolder,
  posts a link to the NEW (now-filled-out) report in #team-strategery as
  hyperlinked text "MRV Pace", and clears that cycle from the pending list. If
  nobody has replied yet, leaves it pending for the next sweep. ALWAYS trigger
  when: a scheduled run fires this job, Max asks about the state of a pace
  report, whether the pace report is done, or asks about this automation.
---

# MRV Pace Report — Completion Watcher & Finalizer

Runs **one full sweep** each invocation over every pending cycle left by
`pace-report-generate`. A missed sweep self-heals on the next one — state
lives in `pace-report-generate/state.json` (external, durable), not in
timing, and a cycle just sits in `pending_cycles` until someone replies.

**Config:** reads `../pace-report-generate/config.json` — same single source
of truth the generator uses. Never hardcode channel IDs, folder IDs, or the
completion-phrase list here.

**Autonomous send/move is authorized for this automation** — same standing
exception documented in `../pace-report-generate/config.json`'s
`_autonomous_send_comment`. Covers moving the deprecated file and posting to
both #team-mrv (replies, if any) and #team-strategery.

---

## The sweep (run top to bottom, every invocation)

### 0. Load config + state
- Read `../pace-report-generate/config.json`.
- Read `state_path`. If `pending_cycles` is empty, print
  `NO-ACTION: no pending cycles` and stop.

### 1. For each entry in `pending_cycles`
Process every entry — don't stop at the first. Order doesn't matter.

#### a. Check the thread for a completion reply
- Read the thread at `thread_channel_id` / `thread_ts`
  (`slack_read_thread`).
- Look for **any reply from a person (not the bot's own original post)**
  whose message signals they're done filling out the report. Be flexible —
  match intent, not an exact keyword. Any of `completion_phrases` in
  config.json counts, and so does clear equivalent phrasing a human might
  actually use ("all set", "just finished mine", "done on my end"). Use
  judgment the way you would reading a real Slack thread — a question
  ("almost done?") or an unrelated reply does NOT count.
- **If no completion reply yet:** leave this entry as-is, move to the next
  entry in the list.
- **If a completion reply is found:** proceed to (b) for this entry.

#### b. Move the superseded report to Deprecated
- Move `source_file_id` into `deprecated_folder_id` via
  `update_file(fileId=source_file_id, parentId=deprecated_folder_id)`.
- This is the report whose "Top 3 I'll Focus On Next Week" items were
  carried forward into the report that just got completed — it's now
  stale. The NEW report (`new_file_id`) stays in the live folder; it does
  NOT get deprecated — it's what the team just finished filling out.

#### c. Post to #team-strategery
- Post one message to `slack_team_strategery_channel_id` whose entire text
  is the hyperlink, Slack mrkdwn format:
  `<<new_file_web_link>|<strategery_post_link_text>>`
  i.e. literally `<https://drive.google.com/...|MRV Pace>` — no extra
  words, matching Max's literal instruction ("simply says 'MRV Pace' where
  the text is a hyperlink").

#### d. Clear the cycle
- Remove this entry from `pending_cycles` and write `state_path` back
  immediately (don't batch all removals to the end — if the run gets
  interrupted partway through a multi-entry sweep, already-closed cycles
  must not be reprocessed next time).

### 2. Done
If every entry was left pending (no completions found this sweep), that's a
normal, silent outcome — no Slack posts, no file moves.

---

## Post a completion line for observability
When run headlessly, write a one-line result to the launchd log (stdout) per
entry processed: either
`NO-ACTION: no pending cycles`,
`STILL-PENDING: <new_file_title> — no completion reply yet`, or
`CLOSED: <new_file_title> — deprecated <source_file_title>, posted to
#team-strategery`.

## Scheduling
Fired by `~/Library/LaunchAgents/com.charm.pace-report-finalize.plist` via the
runner `~/.pace-report/finalize-run.sh`, which invokes Claude Code headless in
the MRV Expert workspace and triggers this skill. Runs weekdays at
approximately 9:00, 12:00, 15:00, and 18:00 local. See
`pace-report-generate/SKILL.md` for the Wednesday-3pm half of this workflow.
