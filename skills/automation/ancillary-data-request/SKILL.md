---
name: ancillary-data-request
description: >
  Slack-based reporting-period-close automation for Charm Industrial's three cross-functional
  ancillary data streams: Community Event + Grievance log (Alison), Wellhead data (Casey), and
  Oxidizer sensor data (Evan Weisenberger). On the 1st of the month it posts three separate asks
  in #mrv-ops-la, each tagging the reporter and asking them to reply in a thread on that post with
  a link to the prior month's data. Every run after that (fired every 3 hours) scans each thread
  for a qualifying reply, routes Wellhead to wellhead-data-transform and Oxidizer to
  tox-sparging-analysis for processing (Community is filed as submitted, no processing), uploads
  the finished product to the Processed Ancillary Data Drafts Drive folder, and posts an alert
  (no @-mentions) to #team-mrv-alerts — noting when the last item for the period lands. Human review and the
  final drop into the reporting package folder happen after this skill's job is done; it does not
  do that step. ALWAYS trigger when: a scheduled run fires this job, Max says "run the ancillary
  data request", "check RP close", "check the mrv-ops-la threads", or asks about the state of this
  automation or the current reporting period's ancillary data. This supersedes the retired
  mrv-mailbox automation (email-based; see archive/mrv-mailbox-superseded/).
---

# Ancillary Data Request — Slack Reconcile Cycle

This skill is the executable brain of the RP-close ancillary-data automation. Every invocation
runs **one full reconcile pass**: resolve the current reporting period, post the month's asks if
still owed, scan every open thread for a qualifying reply, route and file whatever has arrived,
alert on each finished product, and write the ledger back. A missed run is fully recovered by the
next one — nothing depends on firing at an exact minute.

**Config (read first):** `references/config.json` — channel IDs, reporter Slack user IDs, the
Drive destination folder, and the `AUTO_POST_APPROVED` gate. **Message copy (read first):**
`references/message_templates.md` — the exact text for the three RP-close asks and the two alert
templates. Do not paraphrase either file; use them verbatim.

**Connections:** `claude_ai_Slack` MCP tools (posting and reading as Max — the ask channel and
alert channel are both public channels Max is in) and `claude_ai_Google_Drive` MCP tools.

---

## Ledger

One JSON file per reporting period at `~/.ancillary-data-request/ledgers/<period>.json` (e.g.
`2026-08.json` for the August 2026 period). This is the single source of truth this skill reads
first and writes last. Shape:

```json
{
  "period": "August 2026",
  "items": {
    "community": {"posted_ts": null, "permalink": null, "requested_date": null,
                   "received": false, "received_link": null, "received_date": null,
                   "filed": false, "filed_drive_id": null, "filed_drive_link": null,
                   "alerted": false},
    "wellhead":  { "...same shape..." },
    "oxidizer":  { "...same shape..." }
  },
  "period_complete_alert_sent": false
}
```

If the period's ledger file doesn't exist yet, create it with all fields null/false.

---

## The reconcile pass (run top to bottom, every invocation)

### 0. Resolve the current reporting period
- Reporting period = the **just-completed calendar month** (a run on/after the 1st of month M
  asks for month M-1's data — matches "prior month's" in the ask copy).
- Locate/create this period's ledger at `~/.ancillary-data-request/ledgers/<period>.json`.

### 1. Post the month's asks, if still owed
- **Owed** if today is on/after `post_day_of_month` (config: 1) AND the ledger shows no
  `posted_ts` for one or more items yet this period.
- For each item not yet posted: send it as its own **top-level** message in
  `ask_channel_id` (#mrv-ops-la) using the exact copy from `message_templates.md` for that
  reporter — do not combine the three into one message, do not thread them together. Capture the
  returned message timestamp and permalink; stamp `posted_ts`, `permalink`, `requested_date` in
  the ledger immediately after each send (so a crash mid-post doesn't re-send the ones already
  out — check per-item `posted_ts` before sending, not just once at the top).
- **AUTO_POST_APPROVED gate:** if `false` in config, do not send — instead report to Max in chat
  exactly what would have been posted (channel + all three message bodies) and stop this section.
  Live sends only happen once this is flipped to `true`.

### 2. Scan open threads for a qualifying reply
For each item where `posted_ts` is set but `received` is not yet `true`:
- Read the thread with `slack_read_thread` (channel = ask channel, `message_ts` = the item's
  `posted_ts`).
- A reply **qualifies** when it is authored by that item's tagged reporter (`user_id` in config)
  AND delivers the data — either a Drive/http(s) link in the message text, or one or more files
  attached directly to the Slack reply. Either form is a completed delivery; don't hold out for a
  link when the reporter has already handed over the file. If a reply (link or attachment) comes
  from someone other than the tagged reporter, do **not** auto-complete the item — note it in this
  run's chat report as "reply from someone else, needs a look" so a team member can confirm it's
  authorized, and leave `received` false. Never guess.
- On a qualifying reply: stamp `received = true`, `received_date` = today, and:
  - **Link delivery**: `received_link` = the URL.
  - **Attachment delivery**: pull each attached file down from Slack (see "Downloading a Slack
    attachment" below) and `received_link` = the Slack message permalink (there's no Drive link to
    record yet — the routing step in section 3 works from the downloaded file directly).

### 3. Route and produce the finished product
For each item just marked `received` this pass (or received in an earlier pass but not yet
`filed` — recover a missed step):

- **Community** (`route: file_as_submitted`): the finished product is the linked document
  as-is. Use Drive tools to resolve the link to a file, `copy_file` it into the
  `finished_product_folder_id`, naming the copy with the period, e.g.
  `<Period>_Community_Events_Grievance.<ext>`. This does **not** touch or move Alison's original.
- **Wellhead** (`route: process`, skill `wellhead-data-transform`): get the source file — from
  Drive if it was a link delivery, downloaded from Slack (see below) if it was an attachment
  delivery — hand it to the `wellhead-data-transform` skill for this reporting period, then upload
  the skill's output workbook to `finished_product_folder_id` (`create_file` with the local
  output's content).
- **Oxidizer** (`route: process`, skill `tox-sparging-analysis`): same pattern, handing the source
  file (Drive or downloaded-from-Slack) to `tox-sparging-analysis` and uploading its output
  workbook(s) to `finished_product_folder_id`.
- Stamp `filed = true`, `filed_drive_id`, `filed_drive_link` in the ledger.

This skill's job ends at the upload. **Do not** move anything into a "reporting package" folder
and do not attempt final QA — that is human review, explicitly out of scope here (see Max's
spec — "that's the end of the line for you").

**Downloading a Slack attachment:** there is no dedicated file-download tool on the Slack
connection, but the logged-in `playwright-mrv` browser session downloads a Slack attachment like
any other file — the download lands directly in this project's own `.playwright-mcp/` folder
(same folder the browser tool saves every screenshot/snapshot to), which Bash and Read already
have full access to. No fetch, no extra permission, no workaround needed. Steps:

1. `slack_search_public_and_private` (`content_types: files`, scoped to the ask channel /
   reporter) to get the file's permalink and file ID, or read it straight off the thread reply.
2. `browser_navigate` to the permalink (`.../files/<user>/<file_id>/<name>`) — the persistent
   Slack session in that profile is already authenticated as Max, no login step needed.
3. Two cases, depending on whether Slack can preview the file inline:
   - **Previewable text type (csv, txt, log, etc.):** the page loads directly and its HTML embeds
     `url_private_download` as a JSON string. Read it with a plain, read-only DOM string search
     (e.g. `document.documentElement.innerHTML.indexOf('url_private_download')` and slice out the
     surrounding substring) — then `browser_navigate` straight to that URL. The browser treats the
     response as a download rather than a page and saves the file into `.playwright-mcp/`.
   - **Non-previewable binary type (xlsx, docx, pdf, etc.):** the same permalink instead redirects
     to an "Opening in Slack…" interstitial. That page offers a link reading "open this link in
     your browser" pointing to `.../messages/<channel_id>/files/<file_id>` — navigate there
     instead. It loads the full Slack web app with a "File details" panel already open for that
     file, containing a real `<a>` link labeled "Download `<filename>`"; read its `href` (that's
     the `url_private_download` URL) and `browser_navigate` to it directly.
4. **Confirm the file landed** by listing `.playwright-mcp/` for the expected filename (Bash
   `find`/`ls`, not a Read of a specific guessed path — Slack sanitizes the filename slightly, e.g.
   spaces become dashes) — do this **regardless of whether the navigate call itself returned an
   error**. A large binary download has, in practice, crashed the browser process a few seconds
   *after* the file finished writing to disk, which surfaces to this skill as a `Connection closed`
   error on the *next* tool call — that error describes the browser, not the download. Check the
   folder before concluding the download failed. If the file genuinely isn't there, retry the
   `browser_navigate` (the MCP server relaunches automatically, and the persistent profile keeps
   the login) or fall back to the other playwright-mrv-N session.
5. Once confirmed, read the file directly from `.playwright-mcp/<name>` with Bash/Read/pandas as
   needed for the routing step below — no upload or Drive round-trip required to reach it.

(Corrected 2026-09-08: an earlier pass of this skill wrongly concluded a browser-downloaded
Slack attachment was unreachable — stuck in some other process's private sandbox, fixable only by
asking Max to approve a `fetch()` call that then failed on Slack's own cross-origin policy anyway.
Neither claim held up: the file was sitting in this project's own `.playwright-mcp/` folder the
entire time. The fix was checking the working directory the tool actually told me it saved to,
not concluding absence from three unrelated directories. Do not reintroduce the
Drive-link-only / ask-the-reporter workaround this mistake produced — attachments download fine.)

### 4. Alert on each finished product
For each item just marked `filed` this pass where `alerted` is not yet `true`:
- Check whether this is the **last** of the three items to reach `filed = true` for this period
  (all three `filed == true` after this one, and `period_complete_alert_sent` is false).
- Post to `alert_channel_id` (#team-mrv-alerts) using the finished-product template from
  `message_templates.md`. Prefix one `<@id>` mention per entry in `tag_on_alert_user_ids`; that
  list is empty, so the post carries no mentions — the channel post is the alert. If this is the last item,
  append the second line from the template and set `period_complete_alert_sent = true`.
- Stamp `alerted = true`.

### 5. Write the ledger back
Persist every stamp made this pass.

### 6. Report the pass in chat
One short summary: what was posted (or would have been posted, if gate is off), what was
received, what was filed, what was alerted, anything flagged "needs a look."

---

## Idempotency & safety

- The ledger is authoritative for "already posted / already filed / already alerted" — re-running
  the cycle repeatedly in an hour changes nothing after the first pass, because every send/upload
  is gated on a ledger field being unset.
- **AUTO_POST_APPROVED** gates the RP-close asks (step 1) exactly like `AUTO_SEND_APPROVED` gated
  the retired mrv-mailbox automation — Max flips it once the copy and timing are confirmed live.
  It does **not** gate the finished-product alerts (step 4): once an item is genuinely received and
  filed, alerting the team in #team-mrv-alerts is the whole point of the automation and should never be held
  back by a copy-review gate meant for the outbound ask.
- Never invent a reply. A thread with no reply, or a reply with no link, or a reply from the wrong
  person, all leave the item `received: false` — surfaced in the chat report, never marked done.

## Open items / assumptions made 2026-09-02 (flag to Max if wrong)

- **Completion rule is "any one qualifying delivery" (link or attachment)** — the retired
  mrv-mailbox automation required Community to submit *two* documents (Events List AND Grievance
  Record) before treating it as received. Max's new spec asks for one combined "Community Event
  and Grievance log" reply, so this version treats a single qualifying delivery as complete. If
  Community still needs two separate documents, this needs a second per-item sub-check like the
  old design had. (Corrected 2026-09-03: the original build of this skill required the qualifying
  reply to contain an `http(s)://` link — that was never something Max asked for, just an
  assumption baked in without being flagged as one. A reporter dropping files straight into the
  thread, as Evan did for the September pass, now qualifies too.)
- **Reply authorship check** — only a reply from the exact tagged reporter counts automatically;
  a link posted by anyone else is flagged, not auto-accepted. Not specified by Max; built this way
  so the automation never closes out a report on an unverified say-so.
- **Cadence is literally every 3 hours, all day** (00/03/06/09/12/15/18/21 local) — matches "scan
  for responses every three hours" literally rather than restricting to business hours.
