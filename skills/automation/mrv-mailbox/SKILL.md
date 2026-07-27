---
name: mrv-mailbox
description: >
  MRV mailbox automation for Charm Industrial. Runs one full reconcile pass over the
  g_mrv@charmindustrial.com mailbox each time it is invoked: checks whether this month's
  reporting request is owed and sends it, sends 3/5-business-day reminders to anyone
  outstanding, scans for new reporting submissions and routes each to filing or the right
  processing skill, updates the reporting-period ledger, and posts a completion report to
  #team-mrv-alerts. Designed to be fired on a schedule by macOS launchd (and to catch a
  missed run the moment the Mac wakes), but also runs ad-hoc. ALWAYS trigger when: a
  scheduled run fires the MRV mailbox cycle, Max says "run the mailbox cycle", "check the
  MRV inbox", "process MRV reporting", or asks about the state of the current reporting
  period. Connection: the gmail-mrv MCP tools (authorized as g_mrv@). Reads its operating
  spec, ledger template, and email copy from outputs/mrv-operational-documents/mrv-mailbox-automation/.
---

# MRV Mailbox Automation — Reconcile Cycle

This skill is the executable brain of the MRV mailbox automation. Every invocation runs **one full reconcile pass**: it compares what *should* have happened for the current reporting period against the ledger (what *has* happened) and does whatever is still owed. Nothing relies on firing at an exact minute — a missed run is fully recovered by the next run. This is what makes local scheduling safe.

**Operating spec (read first):** `outputs/mrv-operational-documents/mrv-mailbox-automation/Intake_Routing_Spec.md` — reporters, identification, routing, fingerprints, extensibility. This skill executes that spec; it does not restate it.

**Connection:** the `gmail-mrv` MCP tools, authorized as g_mrv@charmindustrial.com (read + send + attachments). Never use the built-in Gmail connector (that's max@).

---

## The reconcile pass (run top to bottom, every invocation)

### 0. Resolve the current reporting period & ledger
- Reporting period = the **just-completed calendar month** (a run on/after the 1st of month M handles month M-1).
- **START-PERIOD GUARD:** `FIRST_LIVE_PERIOD = June 2026` (first request fires July 1, 2026). Never treat any period **before** FIRST_LIVE_PERIOD as owed — if the resolved period is earlier than the start period, do nothing (no request, no ledger, no reminders). This stops a belated request for a month that predates go-live (e.g., a run in late June must NOT fire a May 2026 request).
- Locate this period's ledger at `outputs/automation/mrv-mailbox/ledgers/Reporting_Period_Ledger_<period>.xlsx`. **If it doesn't exist yet** (new month), copy `outputs/mrv-operational-documents/mrv-mailbox-automation/Reporting_Period_Ledger_TEMPLATE.xlsx` to that path, fill the period-info block, and stamp nothing else.
- Read the ledger. It is the single source of truth for every decision below. Read it first, write it last.

### 1. Requester — send this month's request if still owed
- **The authoritative "already sent?" check is the shared mailbox, NOT the local ledger** (so this is safe to run from multiple machines that hold the credential). For each reporter, search g_mrv@'s **Sent** items for a message this period whose subject is `[<Tag>] MRV reporting request — <period>`. If found → that reporter's request already went out; skip it.
- If a reporter's request is **not** found in Sent AND today is on/after the 1st → **send it** (copy from `Monthly_Request_Email_Template.md`, period substituted), then stamp "Requested" in the local ledger (audit copy).
- This gives both guarantees at once: (a) **catch-up** — a request missed on the 1st goes out on the very next run from whatever machine wakes; (b) **no doubles across hosts** — once it's in Sent, every machine sees it and no one re-sends.
- **AUTO-SEND GATE:** `AUTO_SEND_APPROVED = true` — Max approved the email copy on 2026-06-26. Send the requests directly (no longer draft-only). Copy is in `Monthly_Request_Email_Template.md` (synced to Max's approved drafts: sign-off "— MRV Bot"; Community asks for the Updated Events List + Updated Grievance Record). If the copy ever needs re-approval, set this back to false and the skill reverts to staging drafts for review.

### 2. Reminders — nudge anyone outstanding
- "Received" is read from the shared mailbox: a reporter is received if their reply (or a tagged submission) is in g_mrv@. Reminder-already-sent is read from the request thread's Sent messages — both shared across hosts, so reminders never double-fire either.
- For each reporter Requested but not Received: count **business days** since the request went out — skip weekends and the Charm-observed holidays in `outputs/mrv-operational-documents/mrv-mailbox-automation/charm_holidays.json`.
- At **≥3 business days** with no 3-day reminder yet in the thread: send the 3-day reminder as a reply on the request thread.
- At **≥5 business days** with no 5-day reminder yet in the thread: send the 5-day reminder.
- Reminder copy is in `Monthly_Request_Email_Template.md`. Same AUTO-SEND GATE applies.

### 3. Intake scan — find, identify, route new submissions
- Search g_mrv@ for inbox mail **not** carrying the `MRV-Intake/Done` label (create the label once if absent).
- For each new message, **identify** per the spec: sender address → subject tag → structural-fingerprint fallback. **Only route on a confident match.**
- Apply `MRV-Intake/Done` immediately (so the next run skips it), stamp "Received" = its date, then route:
  - **`[Community]`** → file the attachment(s) into the **Community Engagement** Drive folder (`1z_WeA2mp8MT2j0BjbrMsOiL6prcVfIZ_`), month in the filename; stamp "Filed". (Community is received-complete only when BOTH the Events List and Grievance Record rows are received.)
  - **`[Wellhead]`** → hand the attachment to the **wellhead-data-transform** skill → auto-file output into the **Basco MRV** folder (`1oBVyxkx9EQXar2GlZcKInNUcrHrXePrU`) with `— pending review` suffix; stamp "Processed"/"Filed"; set Review flag = PENDING REVIEW; ping Max in Slack.
  - **`[Oxidizer]`** → hand the attachment to the **tox-sparging-analysis** skill → auto-file output into the **CatOx Data** folder (`1AOUY4ux7R7ZF04gFAh_UKd5payKcmU_w`), same `— pending review` / ping pattern.
  - Filenames carry the month (matching existing convention, e.g. `Basco_<Month>_2026_Injection_Report.xlsx`, `<Month> CatOx -- Processed.xlsx`).
- **`[Basco-Insp: PFOT|MIT|Tubing|RTS|Logs|WellheadGas]`** (event-driven annual-inspection stream, spec §8A) → file the attachment(s) into the **Basco 6 Annual Inspection 2026** folder (`18KcW3DPeGhZL2tx982qJrrZsvMU1taKc`), then stamp the matching row of the **tracker Google Sheet** (`1H7bAXCkx4Fpr5DDOwrzqJeyJSqCmWxPohdhGcaFtaC4`): Status → `Received`, Date Received → email date, Filed Document Link → the filed file's link. Leave *In Isometric Package* alone (human flip). This stream's tracker is that Drive Sheet, **not** the monthly xlsx ledger, and it is **not** tied to the monthly period — it only ever files/stamps on arrival. Tag is **required** (Casey also sends `[Wellhead]`); no fingerprint fallback for this stream.
- **Unrecognized** (no confident match): leave untouched, no label, no ledger row — record it for the completion report as "unrecognized — needs a look." Never guess.

### 4. Ledger-keeper — completion report
- Once per day (not every intra-day run), post the completion report to **#team-mrv-alerts**: per reporting item, Requested / Received / Processed / Filed and what's still outstanding; list any unrecognized mail; flag any processed output still PENDING REVIEW.
- Report starts the day after the request goes out; stops once every item is Filed and processed items reviewed.

### 5. Write the ledger back
- Persist every stamp made this pass. Leave the ledger as the accurate current state.

---

## Idempotency & safety (why running this repeatedly — and from more than one machine — is safe)

- **The shared mailbox is the source of truth, not any local file.** "Already requested?" = is it in Sent. "Already reminded?" = is the reminder in the thread. "Received?" = is the reply in the inbox. "Already handled?" = the `MRV-Intake/Done` label. All of these live on the g_mrv@ server, so **every machine that holds the credential sees the same state** — whichever host is awake does the work, the others see it's done. No double-sends, no double-files, no matter how many hosts run it.
- **The local ledger is an audit/convenience copy**, not the gatekeeper. If a machine's ledger is missing or stale, the mailbox checks still keep it correct.
- Re-running the cycle 10× in an hour, or from 3 machines at once, changes nothing after the first.
- **Processed outputs are auto-filed but marked `— pending review`** with a ledger Review flag; the marker clears only when Max approves. An unreviewed verifier-facing file is never mistaken for final.
- **AUTO_SEND_APPROVED gate** keeps all outbound mail in draft until Max signs off on copy.

## Open items
- `AUTO_SEND_APPROVED` is **true** (Max approved copy 2026-06-26) — requests and reminders send directly.
- Holiday list ✓ (`charm_holidays.json`). Destination folders ✓ (Basco MRV / CatOx Data / Community Engagement, IDs in §3). Confirm on the first real filing that outputs land where expected.
- 2-Step Verification enforced on the domain from **Jul 16, 2026** — the stored credential rides through it, but a future forced re-sign-in would need a one-time code (see project memory).
- Scale tickets: future stream — new tag + per-shipment routing, specced when they begin (see spec §8).
