---
phase: "3a"
title: "Protocol Documentation"
type: phase
period: "{{current_rp}}"
status: not_started
depends_on: ["2a", "2b", "2d"]
trigger: "After Phase 2d Certify QA is complete and all batch data is verified"
---

# Phase 3a: Protocol Documentation

**Trigger:** After [[phase2d_certify_qa]] is complete — all batches verified, BCU Quant finalized, Certify mapping confirmed
**Output:** Final Reporting Package assembled and ready for submission to 350 Solutions (VVB)

**Reference:** Feb 1 – Mar 2 Final Reporting Package as template model

---

## Final Reporting Package Structure

Base path: `G:\...\Removals Reporting\2026\[RP Name]\Final Reporting Package [RP]\`

The package mirrors the RP folder structure with everything the VVB needs to verify the period's removals.

---

## Step 1: GHG Statement Report

**File:** `[RP] Removals Isometric GHG Statement Report v[X.X].docx`
**Location:** `[RP]\Additional Documentation\`
**Format:** Isometric-specified template (see PDD Appendix 5)

Update the GHG Statement with current period values:

- [ ] Reporting period dates
- [ ] Total batches and batch UIDs for the period
- [ ] Gross removals (MT CO2e) — must match BCU Quant and Certify
- [ ] Net removals (MT CO2e) — must match BCU Quant and Certify
- [ ] Per-oil-type breakdown (AECN, Charm WODO, Charm QOWV, Kerry if applicable)
- [ ] Process emission factors cited:
  - AECN pyrolysis process: 0.10 tCO2e/t
  - AECN pyrolysis embodied: 0.02 tCO2e/t
  - Charm production: per Production Period CI spreadsheet
- [ ] Uncertainty discount applied per Isometric Standard v2.0
- [ ] Buffer pool contribution (2%, Very Low Risk)
- [ ] Version number incremented from prior period

**Cross-checks:**
- [ ] Gross and net totals match BCU Quant
- [ ] Gross and net totals match Certify removal entries
- [ ] Emission factor values match Standard EF CSV (cell references, not hardcoded)
- [ ] Oil type totals sum correctly to grand total

---

## Step 2: VVB Guidance Document

**File:** `[RP] VVB Guidance.docx`
**Location:** `[RP]\Additional Documentation\` (or top-level RP folder)

Prepare guidance for 350 Solutions covering:

- [ ] Summary of period: dates, batch count, injection site(s), oil types present
- [ ] Any deviations or irregularities from standard process (reference Phase 2d failed sections)
- [ ] New equipment or methodology changes since prior period
- [ ] Open action items carried forward (e.g., missing TOC samples, pending approvals)
- [ ] Kerry oil status: methodology memo approved or still pending
- [ ] Any changes to PDD since last verification (Section F updates)
- [ ] Pointer to key documents the VVB should review first

---

## Step 3: BCU Quant — Final Verification

**File:** `[RP] BCU Quant.xlsx`
**Location:** Top-level RP folder

Final cross-check before packaging (most values populated in Phase 2b):

- [ ] **RP Summary BCUs sheet:** All site emission categories populated (see Phase 2b full list)
- [ ] **Batch Data sheet:** All batch UIDs present with per-batch emissions
- [ ] Grand total site emissions matches sum of individual category trackers
- [ ] Grand total batch emissions matches sum of individual batch entries
- [ ] Gross removals total matches GHG Statement and Certify
- [ ] Net removals total matches GHG Statement and Certify

---

## Step 4: Injection Batch Data Folders — Completeness Audit

For each batch UID in the period, confirm the folder is submission-ready:

- [ ] Folder named correctly per UID convention (`2-XXX`, `3-XXX`, `4-XXX`, `K-XXXXX`)
- [ ] Ops Notes file present and finalized (not draft)
- [ ] Scale Tickets subfolder: full + empty ticket images for each truck
- [ ] Testing subfolder: SGS COA PDF present
- [ ] All files named descriptively (no `IMG_001`, `Measurement XXXX`, `Screenshot...`)

For AECN batches:
- [ ] BOLs present in `AECN BOLs\` folder
- [ ] Rail Batch Summary present if rail batches exist this period

For Kerry batches:
- [ ] Methodology memo present and approved
- [ ] Kerry-specific documentation per approved methodology

---

## Step 5: Site Emissions Trackers — Completeness Audit

Verify every tracker file in `[RP]\Site Emissions\` is finalized:

| Category | Tracker Present | Receipts Complete | Formulas Verified |
|----------|:-:|:-:|:-:|
| Diesel | [ ] | [ ] | [ ] |
| Gasoline | [ ] | [ ] | [ ] |
| Argon | [ ] | [ ] | [ ] |
| Brine | [ ] | [ ] | [ ] |
| Railcar Cleaning | [ ] | [ ] | [ ] |
| Electricity | [ ] | [ ] | [ ] |
| Support Travel | [ ] | [ ] | [ ] |
| Basco Sitework | [ ] | [ ] | [ ] |
| Embodied Emissions | [ ] | [ ] | [ ] |
| KS Equipment Transport | [ ] | [ ] | [ ] |
| Methanol | [ ] | [ ] | [ ] |
| Railcar Loss Emissions | [ ] | [ ] | [ ] |

- [ ] All receipt PDFs present and matched to tracker entries
- [ ] No tracker has placeholder or TBD values remaining
- [ ] **Per-tracker deep audit passed** — see Phase 2b "Per-Tracker Deep Audit Checklist" for full requirements (EF verification, units, naming consistency, formula checks, evidence sources)
- [ ] Naming consistency verified: every folder name matches its calc sheet name and Certify component name

---

## Step 6: Basco MRV Documentation

**Location:** `[RP]\Basco MRV\` (or equivalent)
**Coordination:** Monthly "Basco MRV Round-Up" via Slack — Garrett (or designee) requests inputs from stakeholders at the start of each RP close-out.

### Stakeholder Inputs

| Stakeholder | Deliverable | Slack Request |
|---|---|---|
| **Casey** | Wellhead data for the period | "Can you kick me the wellhead data for [dates]?" |
| **Jen A** | Interpretation memo of Mike's findings (brief ~1 paragraph companion doc to pre-empt VVB concerns) | "Can you write a brief interpretation of Mike's findings?" |
| **Jahvin** | New permitting activity report for the period | "Do we have any new permitting activity to report for [month]?" |

CC: Garrett on all responses.

### Wellhead Data Processing

**Raw wellhead data must NOT be submitted to the VVB.** Casey provides raw injection data that needs to be transformed before inclusion in the reporting package:

1. **Remove** parameters not related to permit compliance verification
2. **Present** permit-relevant parameters as line graphs with a reference line at the permit compliance cutoff level
3. **Identify and annotate** anomalies proactively — the VVB should not discover unexplained deviations on their own

Max has a Claude skill for this transformation. The finished product goes into the Basco MRV folder.

### Checklist

- [ ] Wellhead data received from Casey and filed (raw — not for submission)
- [ ] Wellhead data transformed into reportable format (graphs + compliance lines + anomaly notes)
- [ ] Jen A's interpretation memo received and filed
- [ ] Jahvin confirms permitting status (new permits filed, or "no new activity")
- [ ] LDENR injection reporting for the period (monthly xlsx or PDF)
- [ ] Basco gas testing / leak detection report for the period
- [ ] Well status documentation (if any changes — cleanout, workover, etc.)
- [ ] New permits (if any issued during the period)
- [ ] Displaced brine TOC reports (if Vaulted Deep batches in period)

---

## Step 7: Assemble Final Reporting Package

Copy or verify all finalized documents are in the Final Reporting Package folder:

```
Final Reporting Package [RP]/
  [RP] BCU Quant.xlsx
  Rail Batch Summary [RP].xlsx (if rail batches)
  Additional Documentation/
    [RP] GHG Statement Report v[X.X].docx
    [RP] VVB Guidance.docx
    Community Engagement/
  Injection Batch Data/
    [Each batch UID folder — complete]
    AECN BOLs/
    Kerry Oil/ (if applicable)
  Site Emissions/
    [All category subfolders with trackers + receipts]
  Basco MRV/
    [Regulatory and monitoring docs]
```

- [ ] No extraneous files (drafts, screenshots, temp files)
- [ ] No files with generic names — everything descriptively named
- [ ] Folder structure matches prior period template

---

## Step 8: Pre-Submission Review

Final sign-off before sending to 350 Solutions:

- [ ] Garrett reviews GHG Statement
- [ ] Max reviews GHG Statement
- [ ] Garrett + Max confirm BCU Quant totals
- [ ] All Phase 2d QA checklist items resolved (no open failed sections)
- [ ] Any open action items from prior verification addressed or documented in VVB Guidance
- [ ] Package shared with 350 Solutions via standard process

---

## Output of This Phase

- Final Reporting Package folder — complete and submission-ready
- GHG Statement updated and reviewed
- VVB Guidance document prepared
- All supporting documentation audited for completeness and naming
- Notification sent to 350 Solutions (VVB)

---

## Session Handoff Template

```
Phase: 3a - Protocol Documentation
Period: [RP name]
GHG Statement: [not started / draft / reviewed / final]
VVB Guidance: [not started / draft / final]
BCU Quant final check: [not started / complete]
Batch folders audited: [X of Y]
Site emissions audited: [X of 12 categories]
Package assembled: [yes / no]
Blocked on: [missing docs, pending reviews]
Next: [specific next step]
```

---

## Confirmed Conventions
- **VVB:** 350 Solutions — every period.
- **Sign-off:** Garrett + Max both review GHG Statement before submission.
- **GHG Statement version:** Increment from prior period (e.g., v1.6 → v1.7).
- **File naming:** All source documents must be descriptively named before packaging.
- **Kerry Oil:** Do not include in submission until methodology memo is approved.

## Open Questions
- [ ] Is there a standardized cover letter or transmittal email template for 350 Solutions?
- [ ] Should the community engagement subfolder be populated each period or only when there's new activity?
- [ ] Does the VVB Guidance doc follow a template or is it freeform each period?
