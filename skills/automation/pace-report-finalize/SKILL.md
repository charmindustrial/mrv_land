---
name: pace-report-finalize
description: >
  Watches for completion replies on MRV Pace Report threads in #team-mrv and
  closes the loop for each one. Fired by macOS launchd a few times a day
  (weekday business hours), also safe to run ad-hoc. For every pending cycle
  recorded by pace-report-generate, checks whether anyone has replied
  "Complete" (or similar) in the #team-mrv thread; if so, posts a link to the
  NEW (now-filled-out) report in #team-strategery as hyperlinked text "MRV
  Pace" and clears that cycle from the pending list. (Moving old reports to
  Deprecated is done by pace-report-generate, not here.) If
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

**Autonomous send is authorized for this automation** — same standing
exception documented in `../pace-report-generate/config.json`'s
`_autonomous_send_comment`. Covers posting to #team-strategery.

**This skill does not move files.** Since 2026-10-12, `pace-report-generate`
moves every prior report into Deprecated/Past as soon as it builds the new
one. Before that, the move waited on a "Complete" reply here; nobody posts
that reply, so 9/17, 9/24 and 10/1 piled up in the live folder despite Max
saying on 2026-08-27 and again on 2026-09-10 that old reports go in
Deprecated.

---

## The sweep (run top to bottom, every invocation)

### 0. Load config + state
- Read `../pace-report-generate/config.json`.
- Read `state_path`. If `pending_cycles` is empty, print
  `NO-ACTION: no pending cycles` and stop.

### 1. For each entry in `pending_cycles`
Process every entry — don't stop at the first. Order doesn't matter.

#### a. Check for a completion reply
- Read the thread at `thread_channel_id` / `thread_ts` (`slack_read_thread`).
  Look for any reply from a person (not the bot's own original post) whose
  message signals they're done filling out the report — any of
  `completion_phrases` in config.json, or clear equivalent phrasing ("all
  set", "just finished mine"). A question or unrelated reply does not count.
- **Do not use the source file's location as a completion signal.** The
  generator now moves it every week, so its location says nothing about
  whether the team finished.
- **No reply:** leave this entry as-is, move to the next entry.
- **Reply found:** do (b) and (c) below for this entry.

#### b. Post to #team-strategery
- Post one message to `slack_team_strategery_channel_id` whose entire text
  is the hyperlink, Slack mrkdwn format:
  `<<new_file_web_link>|<strategery_post_link_text>>`
  i.e. literally `<https://drive.google.com/...|MRV Pace>` — no extra
  words, matching Max's literal instruction ("simply says 'MRV Pace' where
  the text is a hyperlink").

#### c. Clear the cycle
- Remove this entry from `pending_cycles` and write `state_path` back
  immediately (don't batch all removals to the end — if the run gets
  interrupted partway through a multi-entry sweep, already-closed cycles
  must not be reprocessed next time).

### 2. Done
If every entry was left pending (no completions found this sweep), that's a
normal, silent outcome — no Slack posts.

---

## Post a completion line for observability
When run headlessly, write a one-line result to the launchd log (stdout) per
entry processed: either
`NO-ACTION: no pending cycles`,
`STILL-PENDING: <new_file_title> — no completion reply yet`, or
`CLOSED: <new_file_title> — posted to #team-strategery`.

## Scheduling
Fired by `~/Library/LaunchAgents/com.charm.pace-report-finalize.plist` via the
runner `~/.pace-report/finalize-run.sh`, which invokes Claude Code headless in
the MRV Expert workspace and triggers this skill. Runs weekdays at
approximately 9:00, 12:00, 15:00, and 18:00 local. See
`pace-report-generate/SKILL.md` for the Wednesday-3pm half of this workflow.
