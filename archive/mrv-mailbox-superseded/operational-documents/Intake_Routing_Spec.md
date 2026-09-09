# MRV Mailbox Automation — Intake & Routing Spec

**Mailbox:** g_mrv@charmindustrial.com
**Reporting cadence:** monthly (one reporting period per calendar month)
**Status:** design complete; connection built and wired, awaiting one-time g_mrv@ sign-in (IT password reset in progress)

This is the operating spec for the automated handling of ancillary MRV reporting that arrives in the MRV mailbox. It covers what comes in, how each submission is recognized and routed, how completion is tracked, and how to add new reporting streams later (scale tickets are coming — see *Extensibility*).

---

## 1. The four moving parts

The system is four jobs sharing one ledger. None of them keeps private state — each reads the ledger first and writes it last.

| Part | What it does | When it runs |
|------|--------------|--------------|
| **Requester** | Sends the monthly request to all reporters on the 1st; sends reminders at 3 and 5 business days to anyone not yet received | 1st of month + daily reminder check |
| **Intake & router** | Scans for new mail, recognizes the reporter, files or hands off to the right processing skill, stamps the ledger | several times a day |
| **Processing** | The existing `wellhead-data-transform` and `tox-sparging-analysis` skills — invoked by the router, not rebuilt | on demand, when a submission arrives |
| **Ledger keeper** | Owns the period ledger; posts the completion report to Slack | daily |

---

## 2. Reporters

| Reporter | Address | Data type | Subject tag |
|----------|---------|-----------|-------------|
| Alison Kelman | alison@charmindustrial.com | Community Engagement Log | `[Community]` |
| Casey Korejwo | casey.korejwo@charmindustrial.com | Wellhead Data Log | `[Wellhead]` |
| Evan Weisenberger | evan.Weisenberger@charmindustrial.com | Oxidizer Temp Log | `[Oxidizer]` |

The **Community** submission is two documents — an **Events List** and a **Grievance Record**. They may arrive as one file or two. The reporting item is not "received-complete" until **both** are present (tracked as two ledger rows).

---

## 3. Identification — structured first, content fallback

When a new message lands, the router identifies which reporting it is, in this order:

1. **Sender address.** Each reporter sends only one data type, so the from-address alone routes correctly.
2. **Subject tag.** The bracketed tag (`[Community]` / `[Wellhead]` / `[Oxidizer]`) confirms the type and catches the case of a shared or forwarded address.
3. **Content fallback (structural fingerprint).** If sender and tag are both missing or ambiguous, the router opens the attachment and matches its structure against the fingerprints below. **It only routes on a confident match.** Anything ambiguous — empty file, unknown format, two fingerprints at once — is left untouched and surfaced in the daily completion report as "unrecognized — needs a look." It never guesses.

### Structural fingerprints (verified against real files, 2026-06)

| Type | Fingerprint (header row / structure) |
|------|--------------------------------------|
| **Wellhead** | Time-stamped table with `surface_pressure_psi` and `annular_pressure_psi` columns (also `local_time, injecting, oil_rate_gpm, brine_rate_gpm, total_rate_gpm, oil_total_gal, brine_total_gal`). The pressure-column pair is unique to this stream. |
| **Oxidizer** | Time-stamped table with the Basco sensor names in the headers: `TIT-2151`, `TIT-2152`, `TIT-2251`, `TIT-2252`, under `Sparging Train 1 / Sparging Train 2`. These sensor tags appear in no other reporting. |
| **Community** | Text-heavy table, no sensor/pressure grid. Events List columns: `Date, Location, Event, Organizer, External/Charm Event, Website, # Attendees, Description, Press/Notes`. Grievance Record columns: `Date, Name of Submitter, …, Grievance/Question, Response, Response Date, Response Owner`. |

---

## 4. Routing

| Tag | Reporter | Route |
|-----|----------|-------|
| `[Community]` | Alison | File the attachment(s) into the **Community Engagement** folder; stamp Filed. No processing. |
| `[Wellhead]` | Casey | Hand the attachment to the **`wellhead-data-transform`** skill → output (raw-data tab + processed tabs + compliance charts) → auto-file into the **Basco MRV** folder marked **pending review** → ping Slack. |
| `[Oxidizer]` | Evan | Hand the attachment to the **`tox-sparging-analysis`** skill → output (raw-data tab + processed tabs + Notes) → auto-file into the **CatOx Data** folder marked **pending review** → ping Slack. |

### Destinations (confirmed Drive folders)

Each stream files into its own data-type folder, with the **month in the filename** (matching the existing convention, e.g. `Basco_April_2026_Injection_Report.xlsx`, `May CatOx -- Processed.xlsx`). There is **no per-period subfolder** — the month lives in the filename.

| Stream | Folder | Folder ID |
|--------|--------|-----------|
| Wellhead | Basco MRV | `1oBVyxkx9EQXar2GlZcKInNUcrHrXePrU` |
| Oxidizer | CatOx Data | `1AOUY4ux7R7ZF04gFAh_UKd5payKcmU_w` |
| Community | Community Engagement | `1z_WeA2mp8MT2j0BjbrMsOiL6prcVfIZ_` |

**Ledger location:** the per-period ledger is the automation's own tracking artifact — it lives in the workspace at `outputs/automation/mrv-mailbox/ledgers/Reporting_Period_Ledger_<period>.xlsx` (git-tracked, auditable). The human-facing view of status is the daily Slack completion report; the ledger itself does not need a Drive home.

**Pending-review marker.** Processed (wellhead/oxidizer) outputs are verifier-facing, so each auto-filed file carries a `— pending review` filename suffix and a Review-flag on its ledger row. The marker clears only when Max approves. This files automatically (as decided) without an unreviewed file ever being mistaken for verified-final.

---

## 5. Not double-handling the same mail

The intake scan runs several times a day and would otherwise see the same message repeatedly. On pickup, the router applies the Gmail label **`MRV-Intake/Done`** to the message and filters it out on the next scan. Labels are visible in the mailbox, so the trail is auditable by eye.

---

## 6. Completion tracking & Slack report

The **ledger keeper** posts a completion report to **#team-mrv-alerts** (Slack):

- **Starts** the day after the monthly request goes out.
- Each day lists, per reporting item: Requested / Received / Processed / Filed, and what's still outstanding.
- **Reminders** fire at **3 and 5 business days** to any reporter not yet received. Business-day count skips weekends and Charm-observed holidays listed in `charm_holidays.json` (sourced from the Charm Holiday calendar in g_mrv@; refresh per year).
- **Ends** once every item is Filed (and processed items reviewed).

---

## 7. Schedule (defaults — adjust as needed)

| Job | Time (Max's timezone) |
|-----|------|
| Monthly request | 1st of month, 8:00 am |
| Inbox scans | 9:00 am, 1:00 pm, 4:00 pm |
| Reminder + completion check | daily, 8:30 am |

These run as scheduled cloud agents (unattended). Build-time check still open: confirm the g_mrv@ connection carries into the scheduled environment before relying on it.

---

## 8. Extensibility — adding a new stream (e.g., scale tickets)

The system is built so a new reporting stream is a **configuration change, not a rebuild**. To add one:

1. **Add a row** to the Reporters table (§2): reporter name, sending address, data type, subject tag.
2. **Define its fingerprint** (§3) for the content fallback.
3. **Add a routing rule** (§4): file-only, or hand to a processing skill.
4. **Add its rows** to the ledger template.

**Scale tickets (coming).** Scale tickets are mass/weight evidence for bio-oil shipments and feed batch QA (railcar/truck mass chains). When they start routing to the mailbox they'll get their own tag (e.g. `[ScaleTicket]`) and a route that files them where the batch-QA work can reach them — most likely a per-batch or per-shipment destination rather than the monthly period folder, since they're tied to shipments, not the monthly cadence. They are images/PDFs, so intake must **download the image and read the pixels directly** (the auto-OCR text can misread digits — established practice for scale tickets). We'll spec the exact destination and the batch-matching logic when the routing actually begins; this section reserves the slot.

---

## 8A. Active added stream — Basco 6 Annual Inspection (event-driven, 2026)

**Nature:** a one-time annual event, **not** part of the monthly request/reminder cycle. There is no monthly request for this stream — the router only files and stamps when a tagged report arrives. The stream is complete when every tracker row is marked *In Isometric Package*.

**Reporters & tags.** The subject tag is **required** here (not just confirmatory): Casey sends more than one data type — she already owns `[Wellhead]` — so sender-address alone no longer disambiguates. Route on the tag.

| Item | Reporter | Subject tag |
|------|----------|-------------|
| Pressure Fall-off Test | Casey | `[Basco-Insp: PFOT]` |
| Mechanical Integrity Test | Casey | `[Basco-Insp: MIT]` |
| Corrosion — tubing & packer | Casey | `[Basco-Insp: Tubing]` |
| Radioactive Tracer Survey | Casey | `[Basco-Insp: RTS]` |
| Cased Hole Logs | Jen Anderson | `[Basco-Insp: Logs]` |
| 6-month Wellhead Gas | Casey | `[Basco-Insp: WellheadGas]` |

**Identification: subject tag only.** These reports are heterogeneous PDFs (lab results, scan reports, wireline logs) with no stable structural fingerprint, so this stream has **no content fallback**. An untagged or mistagged inspection email is surfaced in the Slack report as "unrecognized — needs a look" and left untouched — never guessed into a row.

**Routing.** File the attachment(s) into the **Basco 6 Annual Inspection 2026** Drive folder (ID `18KcW3DPeGhZL2tx982qJrrZsvMU1taKc`), item/date in the filename, then stamp the tracker Sheet row matching the tag:
- Status → `Received`
- Date Received → the email's date
- Filed Document Link → the Drive link of the filed file
- *In Isometric Package* is left for a human — that flip is Max's call once the package is assembled.

Then ping **#team-mrv-alerts**.

**Tracker (this stream's ledger).** The shared Google Sheet **Basco 6 Annual Inspection — Reporting Tracker (2026)** (ID `1H7bAXCkx4Fpr5DDOwrzqJeyJSqCmWxPohdhGcaFtaC4`), living in the folder above. Unlike the monthly streams (git-tracked xlsx ledger), this tracker is a Drive Sheet so Jen and Casey can edit it directly as work progresses. The router reads it first (find the row for a tag) and writes it last (stamp) — humans and the router share the one Sheet.

**Dedup.** Same as §5 — label picked-up mail `MRV-Intake/Done` so the next scan skips it.

---

## 9. Status & open items

**Live as of 2026-06-26.** Connection authorized as g_mrv@; reconcile skill built; macOS launchd schedule installed and verified (clean no-op test); auto-send enabled with Max-approved copy. **First live send: July 1, 2026** (June 2026 reporting).

Resolved: g_mrv@ sign-in ✓ · destination folders ✓ (above) · holiday list ✓ (`charm_holidays.json`) · scheduled-environment run ✓ (headless launchd run exited 0).

Still open:
- **Drive folder confirmation in practice** — destinations are wired (Basco MRV / CatOx Data / Community Engagement); confirm on the first real filing that they land where expected.
- **2-Step Verification** enforced on the domain from **Jul 16, 2026** — the stored credential rides through it; a future forced re-sign-in would need a one-time code (see project memory).
- **Scale-ticket routing** — future stream: new tag + per-shipment routing, specced when tickets begin arriving (see §8).
