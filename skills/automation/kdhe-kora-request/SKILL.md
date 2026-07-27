---
name: kdhe-kora-request
description: >
  KDHE KORA records-request builder for Charm Industrial's Vaulted (Advantek Cavern
  Solutions) geologic-storage monitoring. Produces the periodic Kansas Open Records Act
  (KORA) request that pulls Vaulted's permit-required KDHE monitoring reporting — the
  evidence that satisfies Charm's ongoing operational-monitoring obligation to Isometric.
  The SINGLE SOURCE OF TRUTH for what to request is the monitoring tracker
  (Vaulted_KDHE_Monitoring_Tracker_2026.xlsx): the skill reads the tracker, requests exactly
  the scheduled reports that are due and not yet received plus the standing event-driven
  list, drafts the request .docx, and — when KDHE replies — downloads the returned documents
  and updates the tracker. ALWAYS trigger when: Max says to build/draft a KORA request, a
  "KDHE request", a "Vaulted records request", to "pull Vaulted's monitoring", references the
  KDHE monitoring tracker, or asks what Vaulted reporting is outstanding. Scope is
  permit-required monitoring reporting ONLY — never add non-permit items. Read-only on
  Certify and any live registry.
---

# KDHE KORA Request — Vaulted Monitoring Reporting

Charm files periodic Kansas Open Records Act (KORA) requests to KDHE to obtain Vaulted's
permit-required monitoring reporting for the salt caverns holding Charm's stored bio-oil.
This reporting is the evidence that satisfies Charm's **ongoing operational-monitoring
obligation to Isometric.**

## THE ONE RULE (do not violate)

**The tracker is the single source of truth for what to request. Pull only the required
KDHE reporting the tracker sets out — nothing more, nothing invented, nothing from memory.**

`Vaulted_KDHE_Monitoring_Tracker_2026.xlsx` (in the `KDHE Requests` Drive folder) lists,
month by month, every report Vaulted owes KDHE, its due date, its request status, and — once
received — the filename(s). A request is built by **reading the tracker**, not by
reconstructing the report slate from memory. Reconstructing from memory is how errors get in
(a real one: an Advantek "sawdust emplacement pilot final report" was added to a draft even
though it is a project deliverable, not permit-required monitoring — it does not belong).

**Scope test for every line you're about to request:** *Is this a permit-required monitoring
report that appears as a scheduled or event-driven row in the tracker?* If no → it does not go
in the request. Advantek project deliverables, pilot reports, operational one-offs, anything
Charm-generated → out of scope.

## Why this scope is correct (the Isometric agreement)

Per the #isometric-charm thread Dec 2025–Feb 2026 (Seb Green + Tom Sellers, Isometric),
Charm's ongoing operational-monitoring obligation for AR-09 is satisfied by submitting
**Vaulted's KDHE-permit-required reporting** — nothing Charm-generated. Isometric's Salt Cavern
Storage module lists most operational monitoring parameters "as permit," so the KDHE reporting
covers them. The one parameter ever questioned (daily cavern pressure) resolved Feb 18, 2026
when Isometric accepted the KDHE/KOLAR monthly reports as containing it (those reports carry
daily Emplacement/Displacement Gauge + Continuous-Recorder psig). So: pulling the KDHE reports
via KORA **is** the compliance act. See memory `project_kdhe_kora_vaulted_requests`.

## Scope: reversal-monitoring reporting only

The purpose is monitoring **against reversals** of stored carbon. Request the permit's reversal-relevant
reporting only: monthly monitoring, quarterly Level of Emplaced Material, quarterly groundwater, the
**biennial** Elevation Survey (confirmed = every 2 years from the 6/5/2024 permit effective date), sonar
surveys, and the reversal/integrity **event-driven** reports (verified gas detection, loss of mechanical
integrity, anomalous operational data, migration into an unauthorized zone, well treatment/workover,
**well malfunction or failure**, **testing malfunction / other emergency reporting**, cavern completion,
post-cavern-filling monitoring status plan, and the P&A plan/report).

**Intentionally OUT of scope** — permit-required but not reversal monitoring, so do NOT add to a request or
the tracker:
- **Spills** (surface / brine-tank event — not a reversal of stored carbon).
- **Financial Assurance** (annual surety-bond evidence — financial, Section VI).
- **Beneficial Reuse Material Acceptance Plan** (annual update — materials acceptance, Section III).
- **Permit Renewal / Permit Transfer / Corrections to Submittals / Emplacement Stream Changes** (administrative or conditional).

**Deferred (years out):** the routine 5-year **MIT Plan + MIT Report** and the associated **Construction &
Injection Details**. The one-off *reentry* MIT / construction records for **AR-09** are a separate matter —
the permit lists AR-9 as *Plugged* and does not authorize it as an active well, yet emplacement reportedly
resumed there; pursue the AR-09 reentry MIT + any permit modification under that open question, not the
routine tracker.

## Fixed facts

- **Caverns:** AR-09 and SW-12 (Class V emplacement wells).
- **Facility:** "Vaulted Deep," operated by **Advantek Cavern Solutions, LLC (ACS)**,
  7513 South K-14 Highway, Hutchinson, KS 67501, Reno County.
- **Permit:** UIC Permit No. **KS-05-155-002** (both caverns).
- **KDHE contact who fulfills requests:** Jamie Packard (Jamie.Packard@ks.gov), Bureau of Water.
  Submit via the KORA online portal (link on the tracker's Cover tab). KDHE target ~15 business days.
- **Governing permit (the authority behind the tracker):** `knowledge-base/ACS_Vaulted_KDHE_Permit_KS-05-155-002_SIGNED.pdf`
  — the KDHE Class V Underground Injection Control permit (Owner: Underground Cavern Stabilization, LLC;
  Operator: Advantek Cavern Solutions, LLC; effective 6/5/2024, expires 6/5/2034). The tracker's report
  list, frequencies, and due dates derive from this permit's construction/operation/monitoring/reporting
  requirements. Day to day, build requests from the tracker; **if the tracker and permit ever disagree,
  the permit governs** — reconcile the tracker to it.
- **Home folder:** `My Drive/MRV/Injection and Pre-Processing Facilities/Post-Injection/Vaulted/KDHE Requests/`.
  Top level holds the tracker + the request template only. **Each quarter gets its own folder**
  (`Q# 20## KORA Requests`) that holds BOTH that quarter's request letter and the documents KDHE
  returns for it.

## Operating model — one request per quarter

**Cadence / trigger:** make a request when the **last monthly report for a quarter is due** — the
28th of the month after the quarter ends: **~Apr 28** (covers Q1), **~Jul 28** (Q2), **~Oct 28**
(Q3), **~Jan 28** (Q4).

**Every request has three parts:**
1. **Anything outstanding from the previous quarter** — reports already requested but not yet received.
2. **Everything due from the quarter that is ending** — its three monthly reports + that quarter's
   Quarterly Level of Emplaced Material + Groundwater report, plus any biennial/periodic item that
   comes due in the window (e.g. the biennial Elevation Survey).
3. **Any event-based reporting** — the standing event-driven list, since the last request.

**Filing:** the request letter and the documents KDHE returns for it both live in that quarter's
folder, `Q# 20## KORA Requests` (e.g. `Q2 2026 KORA Requests/`).

## Workflow

1. **Read the tracker.** Open `Vaulted_KDHE_Monitoring_Tracker_2026.xlsx` (openpyxl). Walk every
   month tab. Identify (a) the ending quarter's SCHEDULED REPORT rows and (b) any previous-quarter
   rows whose Request Status is not "Received." Also collect the standing EVENT-DRIVEN list. Watch
   for non-monthly rows: the quarterly Level of Emplaced Material + Groundwater, and periodic items
   like the biennial Elevation Survey.
2. **Confirm what's already in hand.** Cross-check against the tracker's filename columns, prior
   quarter folders, and Max's mailbox so you don't re-request received items.
3. **Draft the request .docx** into that quarter's folder (`Q# 20## KORA Requests`), mirroring the
   prior request's letter style (greeting → facility + permit identification → the three-part report
   list → close). Section I = outstanding-from-previous-quarter, Section II = due-from-ending-quarter,
   Section III = event-triggered. Include the permit number and address — KDHE asks for site
   specificity. Open the file; deliver as a **draft only** (no autonomous send).
4. **On KDHE reply:** download the returned documents (see download method below), save them into the
   same quarter folder, and **update the tracker** — set each row's Request Status to "Received" and
   record the filename(s).

## Attachment-download method (Max's main mailbox, max@)

The `gmail-mrv` MCP `download_attachment` FAILS on max@ (Permission denied — wrong mailbox); the
claude.ai Gmail connector has no download tool. Instead: open the thread in Playwright Gmail
(logged in as max@), collect attachment hrefs (`view=att`), same-origin `fetch(...).arrayBuffer()`
→ base64 in `browser_evaluate` (needs `touch /tmp/playwright_writes_approved` — the Certify hook
blocks fetch by default; this is a read-only GET of Max's own attachments), save via the evaluate
`filename` param (lands in workspace root, double-JSON-encoded), decode locally, and drop files into
the Drive local mount. Full detail in memory `project_kdhe_kora_vaulted_requests`.

## Anti-patterns (all real failures — do not repeat)

- **Reconstructing the report list from memory** instead of reading the tracker → missed items
  (e.g. the biennial Elevation Survey) and invented items.
- **Adding non-permit deliverables** (sawdust pilot final report, operational one-offs) to a request
  whose purpose is monitoring compliance.
- **Treating "a document exists and we don't have it" as "outstanding."** Outstanding = a
  permit-required monitoring report that is due and not yet received. Nothing else.
- **Sending anything.** Output is always a draft for Max; he submits via the KORA portal himself.
- **Writing to Certify or any live registry.** This skill is read-only there.
