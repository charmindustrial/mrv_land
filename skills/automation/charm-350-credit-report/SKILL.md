---
name: charm-350-credit-report
description: >
  Daily Charm bio-oil credit-submission report for Charm Industrial. Once a day (fired by
  launchd at 3pm local, and safe to run ad-hoc), checks the #ext-proj-charm-350-isometric
  Slack channel for a NEW announcement that a bio-oil GHG statement has been submitted for
  verification. If there is none, it does nothing. If there is one, it opens the Charm
  Bio-oil project in Isometric Certify (READ-ONLY), finds the GHG statement under verification
  for the prior calendar month, classifies every removal by oil source (Charm-produced QOWV /
  WODO / Aqueous, AECN, Kerry), builds a spreadsheet (removal ID linked, removal date, oil
  type, tCDR; one section per source with subtotal, plus a grand total) saved to Drive, and
  sends the report to the fixed recipient list. Idempotent: it will not re-report a statement it has already reported.
  ALWAYS trigger when: a scheduled run fires this job, Max says "run the 350 credit report",
  "check for a credit submission", "check #ext-proj-charm-350 for a submission", or asks
  about the state of this automation. This skill is READ-ONLY on Certify and any live
  registry — it never writes to the registry.
---

# Charm 350 Bio-oil Credit-Submission Report

This skill runs **one full pass** each invocation. A missed run self-heals on the next run
because the trigger (a submission announcement in Slack) and the dedup key (the GHG statement
ID) both live in durable external state, not in timing. Read the ledger first, write it last.

**This is NOT a QA process.** No Pass/Fail, no checklist, no adversarial review. QA knowledge
is used only to *recognize* which removals are Charm-produced oil, AECN, or Kerry.

**Config (read first, fail loud if missing):** `config.json` in this folder holds every
changeable fact — channel ID, project ID, recipient user IDs, Drive folder, oil-type keywords,
delivery mode. Never hardcode any of these in prose or in a command; read them from config.
Per the workspace rule "skills hold logic, not facts."

**Live-registry rule:** Certify is READ-ONLY. Only `browser_navigate`, `browser_snapshot`,
`browser_evaluate` (pure read expressions — `innerText`/`querySelector`/etc.), and
view-changing `browser_click`. Never type, submit, or click any write-class control. If a
write ever seems required, stop and surface to Max.

---

## The pass (run top to bottom, every invocation)

### 0. Load config + ledger
- Read `config.json`. If `delivery_mode` is still `UNSET__…`, STOP and tell Max the automation
  is not yet configured for delivery — do not guess a mode.
- Read the ledger at `ledger_path` (a JSON list of already-reported `statement_id`s). If it
  does not exist, treat it as empty `[]`; create it at the end.

### 1. Check Slack for a NEW submission announcement
- Read the announcement channel (`slack_announcement_channel_id`), newest ~30 messages.
- A **submission announcement** is a message (historically from Garrett Lutz, but do not
  require a specific author) that announces a bio-oil GHG statement / reporting period has
  been **submitted for verification**. Recognize it by the trigger phrases in config AND/OR a
  link to a Certify GHG statement (`.../ghg-statement/ggs_…`). Examples seen in practice:
  - "GHG Statement is in for June!" with a `ggs_…` link.
  - "The 5/1–5/31 Reporting Period has been submitted."
- Ignore posts that are clearly NOT submission announcements (dataset refreshes, engineering
  updates, verifier findings, "Certificates issued", general discussion).
- **Dedup:** if the statement the announcement points to (or, if no direct link, the statement
  you resolve in step 2) is already in the ledger, this pass has nothing to do → **stop, take
  no action.**
- If there is no new submission announcement → **stop, take no action.** (This is the common
  case — announcements are roughly monthly.)

### 2. Find the GHG statement under verification (Certify, read-only)
- Open `certify_ghg_statements_url`. If you hit an SSO login wall, surface it to Max with a
  clear handoff (the persistent Playwright profile usually carries the session) and stop.
- Identify the target statement:
  - **Date range** = typically the calendar month **prior** to the announcement.
  - **Status** = "under verification" (or similar), NOT "Certificates issued".
  - Prefer the exact `ggs_…` from the announcement link if present.
- If the only matching statement already shows "Certificates issued", note it — a real live
  run should find "under verification". (A backfill/test run against an issued statement is
  fine but must be labeled as such and NOT auto-sent to colleagues without Max's OK.)
  **Enforced since 2026-10-01:** the report header must state the Certify status verbatim, and
  the posting hook (`~/.claude/hooks/scoped_automation_slack_send.sh`) refuses any send to a
  colleague whose message lacks "under verification" or Certify's own wording "Awaiting
  verification" (accepted since 2026-10-27; copy whichever Certify shows, never add words it
  doesn't show). Any other status goes to Max only, first
  line "BACKFILL — needs your OK before forwarding", ledger untouched. (A 2026-10-01 run sent
  the already-issued August statement to all four recipients after quoting this rule to itself.)

### 3. Read the removals and classify by oil source (Charm / AECN / Kerry)
**Every removal on the statement goes in the report** (since 2026-10-09, at JZ's request — the
earlier Charm-only version made him ask for the AECN and Kerry numbers separately). The
classification only decides which section a removal lands in.
- Preferred read: the Isometric MCP server. Call `how_to` with the goal "list all removals in
  GHG statement <ggs_…> with co2eRemoved, dates and component names", then run the returned
  query. One call returns every removal with its components. Fall back to the browser (GHG
  Entries tab, then each removal via `certify_removal_url_prefix` + removal_id,
  `browser_evaluate` → `main` innerText) only if the MCP server is unavailable.
- Note each removal's ID, tonnes removed (tCO₂e = the tCDR for that removal), and sequestered
  date range. Classify by the **production/pyrolysis and transport component names**:
  - **CHARM** — component names contain a Charm oil keyword (`charm_oil_keywords`:
    QOWV / WODO / Aqueous) and/or Charm production emissions, e.g. "Pyrolysis - Charm QOWV PP
    Emissions", "Pyrolysis - Charm WODO Emissions", "CO to LA … Transport … - QOWV/WODO".
    Set `oil_type` to the specific keyword (QOWV / WODO / Aqueous).
  - **AECN** — component names contain an `aecn_keywords` term, e.g. "AECN pyrolysis (from
    rail loads)", "AECN to SOPOR Tanker Truck", "SOPOR to Opelousas Rail". Set `oil_type`
    to "AECN".
  - **KERRY** — component names contain a `kerry_keywords` term, e.g. "Kerry to Basco Tanker
    Truck Transport Process Emissions". Kerry removals have no pyrolysis components (waste
    scope). Set `oil_type` to "Kerry".
  - Site-emission components (RECs, diesel, embodied, BCU adjustments) sit on one removal per
    period and say nothing about oil source — ignore them for classification.
- If a removal matches none of the keyword sets, or more than one, **FLAG it to Max and do
  not guess**. No fabricated classification. The report is not sent until every removal has
  a section.
- Check: the sum of all removals' tCDR must equal the statement total shown in Certify.

### 4. Build the spreadsheet
- Assemble the payload (statement_id, period_label, period_slug like `2026-06`, the Certify
  status string, and ALL removals with removal_id / date / oil_type / tcdr) and run:
  `python3 build_report.py '<json payload>'`
- It writes `Charm_Bio-oil_Credits_<period_slug>.xlsx` to the Drive folder — three sections
  (Charm-produced, AECN, Kerry) each with a subtotal, plus a grand total — and prints the path
  and the per-source totals. If the file already exists it is overwritten in place (never
  removed and recreated) so the Drive file ID and any shared link survive. Then find the file
  via the Drive connector to get its shareable `viewUrl`.
- `open` the saved file locally so Max can see it (per the "open generated docs" rule).

### 5. Send the report
- Deliver per `delivery_mode` in config:
  - `dedicated_channel`: post one message to `dedicated_channel_id`.
  - `individual_dms`: send the same message to each recipient `user_id`.
- Message = a short header (statement ID, Certify status verbatim, period) + a per-source
  summary table (Charm-produced / AECN / Kerry: number of removals and tCDR, with a total row)
  + a Markdown table of every removal (ID linked to Certify, removal date, oil type, tCDR)
  + the Drive spreadsheet link. Keep it lossless and scannable.
- **Autonomous send is authorized for this automation** (Max set it up to send directly to the
  fixed recipient list). This is a narrow, standing exception to the general no-autonomous-send
  rule — it applies ONLY to this report, ONLY to the configured recipients. Any change to
  recipients or scope reverts to draft-for-approval.

### 6. Update the ledger
- Append the reported `statement_id` to the ledger and write it. This is what makes re-runs
  idempotent.

---

## Post a completion line for observability
When run headlessly, write a one-line result to the launchd log (stdout): either
`NO-ACTION: no new submission announcement` or
`SENT: <statement_id> — N removals (Charm <x> / AECN <y> / Kerry <z>), <total> tCDR`.

## Scheduling
Fired by `~/Library/LaunchAgents/com.charm.charm-350-credit-report.plist` via the runner
`~/.charm-350-credit-report/run.sh`, which invokes Claude Code headless in the workspace and
triggers this skill. See that runner for the exact invocation. The job runs daily at 15:00
local time (launchd uses local time, so it tracks PST/PDT automatically).
