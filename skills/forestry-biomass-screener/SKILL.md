---
name: forestry-biomass-screener
description: >
  Pre-screen and qualification tool for new forestry biomass sources under BFA v1.3.
  Given a Drive folder of initial evidence, maps each of the 8 Certify feedstock
  requirements to the documents that address them, identifies gaps, and generates
  a go-get-these-docs checklist for the biomass team. In fill mode, drafts ready-to-paste
  Certify submission text for each question. TRIGGER when: Max wants to qualify a new
  forestry biomass source, screen biomass evidence against Isometric requirements,
  find what documentation is missing from a project, or draft Certify feedstock submission
  text. Also trigger when Max says "screen this new prospective biomass source," "screen
  this biomass source," "screen this project," "qualify this feedstock," "what docs do
  we still need," "what's missing from this project," "fill in Certify for [project],"
  or any variation of wanting to evaluate a new forestry biomass source.
---

# Forestry Biomass Source Screener

You are assisting Max Lavine, Carbon Protocol and Verification Lead at Charm Industrial,
qualifying a new forestry biomass source under Isometric's Biomass Feedstock Accounting
module v1.3 (BFA v1.3).

The governing methodology is BFA v1.3 at:
`knowledge-base/isometric-pdfs/Biomass Feedstock Accounting v1.3 — Isometric.pdf`

---

## Universal cross-reference rule (no exceptions)

**Before assessing any requirement, read its source text in BFA v1.3.** Any reference
within that text — to a table, appendix, section, or external document — must be read
before drawing a conclusion about that requirement. This is not a named-section list. It
applies to every requirement, every time. If a criterion says "see Table X" or "subject
to Appendix Y" or "as defined in Section Z," that reference is mandatory reading before
any finding is made. A finding without having read every cross-reference it depends on
is not a finding — it is a guess.

**Operational guidance is subordinate to BFA text — no exceptions.** The operational
guidance and evidence-type lists in each section below describe patterns from Elk Meadow
P2 and general practice. They are NOT a statement of what BFA v1.3 requires. If the BFA
text you read in this session says less than the operational guidance implies, the BFA
text governs — do not flag a gap for something BFA does not require. If the operational
guidance conflicts with what BFA v1.3 actually says after reading it, BFA wins. Elk Meadow
P2 practice ≠ BFA requirement. Treat any "what's needed" or "evidence types" list in the
sections below as belt-and-suspenders context, not as a compliance checklist, unless it
is directly traced to a verbatim BFA v1.3 quote.

---

## Two modes

**Pre-screen** (default): Given a Drive folder of initial evidence, read every document,
map each of the 8 Certify feedstock requirements against what the docs cover, and produce
a gap checklist the biomass team can act on.

**Certify fill**: Given a completed evidence set, draft ready-to-paste submission text
for each Certify question plus a list of documents to attach.

Max will specify the mode, or default to pre-screen when he provides a folder without
saying "fill."

---

## Step 1 — Read all documents in the evidence folder

Max will provide a Google Drive folder ID or URL. If given a URL, extract the folder ID
— it's the string after `/folders/`.

List all files: `mcp__claude_ai_Google_Drive__search_files` with
`query: "parentId = '<folder_id>'"`.

Read every file using `mcp__claude_ai_Google_Drive__read_file_content`. Do not skip any.
For large documents, prioritize sections most likely to contain: project description,
scope of work, grant award details, species and stand information, forester identity and
contact details, merchantability statements, and chain-of-custody language.

---

## Step 1b — Nomenclature Consistency Check

**Run this after reading all documents, before assessing any requirement.**

The grant award documentation is the authoritative name source. Extract the canonical
name for each of the following from the grant award letter or notice (not from any
other document):

- **Program name** — the official grant program name as written in the award
  (e.g., "Colorado State Forest Service Forest Restoration and Wildfire Risk Mitigation
  Program")
- **Grant recipient** — the legal entity named as the grantee in the award
- **Project name / site name** — the project or site name as it appears in the award
  or scope of work attachment
- **Land parcel / geographic identifier** — any parcel number, legal description, or
  named geographic area used to identify the treatment area
- **Forester / vendor name** — legal entity name as it appears in the subcontract,
  forester affidavit, or land manager letter

Then scan every other document in the evidence set (purchase agreement, scope of work,
forester affidavit, land manager letter, species prescription, etc.) and check that
each reference to the above names matches the canonical form exactly — or note the
variation.

**Acceptable variation:** abbreviations used within the same document after a first-
use definition (e.g., "Colorado State Forest Service Forest Restoration and Wildfire
Risk Mitigation Program (FRWRM) ... hereafter 'FRWRM'") are not mismatches. A name
not used at all in a given document is not a mismatch unless that document is expected
to reference it.

**Flag as a nomenclature mismatch:** any document that refers to the program, project,
recipient, parcel, or vendor by a name that differs from the canonical form without a
first-use definition — including partial names, wrong legal entity suffixes (LLC vs.
Inc.), outdated project names, or informal shorthand used in attestations.

**Output:** Produce a Nomenclature Consistency table immediately after completing
Step 1 reads, before the pre-screen assessment. Format:

| Canonical name (grant award) | Document | Name used | Match? | Note |
|---|---|---|---|---|

Include one row per name × document pair where the document is expected to reference
that name. Mark Match = YES / NO / N/A. For every NO row, carry the mismatch forward
as a hard blocker in Section 1 of the pre-screen output (see Step 3a), because an
attestation or agreement that names the wrong project or entity does not form a valid
chain of custody.

---

## Step 2 — The 8 Certify requirements

For each requirement:
1. The **Read** block lists exact BFA v1.3 locations to read before assessing compliance.
2. The **Operational guidance** block describes what evidence to look for.
3. Where an Elk Meadow P2 template exists, it is provided as a validated reference.

Do not assess compliance against a paraphrase of what BFA v1.3 says. Assess compliance
against what BFA v1.3 actually says after reading it.

---

### A.1 — Feedstock Description

**Read (BFA v1.3):** This is a Certify platform requirement, not a numbered BFA v1.3
criterion. No specific section to read — assess based on what the evidence folder contains.

**Operational guidance:** What's needed — species, diameter class or size range, source
project name, general characterization of the material (non-merchantable residues, fuels
treatment material, etc.).

**Elk Meadow template:** "Non-merchantable woody biomass — small-diameter ponderosa pine
(4–18" DBH), and encroaching Douglas-fir lacking sawmill value from the [Project Name]."

**Evidence types:** RFP (stand inventory, species prescription), scope of work,
purchase agreement exhibit specifying biomass type.

---

### A.2 — Organisation Listing

**Read (BFA v1.3):** This is a Certify platform requirement. The Certify field itself
states exactly what's needed for each organisation: company registration number,
organisation name, address, contact person, contact email, contact phone, role description.

**Operational guidance:** In practice — per the validated Elk Meadow P2 submission — A.2 is
satisfied by listing the **forester/vendor** (Charm's direct purchase counterpart) with all
its data points including EIN, plus the hauler when known. Upstream entities (land manager,
grant recipient — conservation district, county open space, fire protection district,
individual grantee) are **named but routed through the forester**; a separate EIN for each
upstream entity is NOT required and its absence is NOT a gap. Do not flag the grant
recipient's or land manager's EIN as a must-have.

The supply chain typically has three layers — (1) land manager / grant recipient,
(2) forester / logging contractor / vendor, (3) hauler — but only the forester/vendor's
full org listing (and eventually the hauler's) is required for submission.

For US entities, the company registration number is the EIN (Employer Identification
Number), found on the W-9 or purchase agreement signature block.

**Elk Meadow template (the validated A.2 submission for COWF-005):**
> Forester/Vendor — SOCO Forest Management (SFM), EIN: 33-3502141, CEO/Founder: Nathan Bean,
> Phone: 205-753-7672, Address: 135 Country Center Dr. F163, Pagosa Springs CO 81147.
> *Note: SFM is our primary contact for biomass purchases. Any communications to JCPOS, ECFPD,
> etc. will be routed through them.* Hauler: [not yet completed].

Isometric raised no issue on this org listing (its open issues ISS-38/39/40 were about
grant / carbon-stock / certification evidence). The forester-only listing is the standard.

**Evidence types:** Purchase/supply agreement signature block (EIN, legal name),
forester affidavit letterhead (contact details), grant SOW signatory block (land manager
details).

---

### A.3 — SC1: Sustainable Sourcing — Forestry Residues

**Read (BFA v1.3):** Table 1 (SC criteria — read the SC1 rows in full, including all
sub-criteria and their documentation requirements). For SC1.1 specifically: Table 1 SC1.1
references Table 6 — read Table 6 in full before assessing SC1.1. Appendix 3 governs how
Table 6 programs satisfy SC1.1 and SC2.1 — read Appendix 3.

**Operational guidance:** SC1 has three sub-criteria (SC1.1, SC1.2, SC1.3). Each has
different documentation paths depending on whether the project is a government wildfire
program. The wildfire program exemption is present in Table 1 for SC1.2 and SC1.3, and
in Table 6/Appendix 3 for SC1.1. Read the actual criterion text for each sub-criterion
before assessing. For SC1.1, Table 6 lists the approved programs — one of them is
government wildfire programs. For SC1.2 and SC1.3, the exemption language appears
directly in Table 1. Do not claim a gap before reading Table 6 and Appendix 3 for SC1.1.

**Note on ISS-38 (Elk Meadow P2):** Isometric raised ISS-38 asking for certification or
risk assessment. This was raised before wildfire grant documentation was provided. Once
grant docs are in hand, ISS-38 is resolved. It is not a standing gap for wildfire
projects — it reflected an incomplete initial submission.

**Evidence types for wildfire programs:** Grant award letter or notice, grant scope of
work (these address SC1.1 via Table 6, and SC1.2/SC1.3 via the wildfire exemption).
For non-wildfire projects: FSC/SFI/PEFC certificate or third-party risk assessment for
SC1.1; independent carbon stock assessment for SC1.2; land type documentation for SC1.3.

---

### A.4 — SC7: Sustainable Sourcing — Invasive Species

**Read (BFA v1.3):** Table 1 SC7 rows (read the SC7 feedstock type definition and both
sub-criteria). Note where SC7 sits in Table 1 relative to SC1 — they are distinct
feedstock categories, not sub-criteria of each other.

**Operational guidance:** SC7 is a separate feedstock category in Table 1. It applies
when the feedstock IS an invasive species. For native species harvested for density
management (lodgepole pine, ponderosa pine, Douglas-fir), SC7 does not apply — assess
as N/A and move on. Do not apply SC7 to every wildfire project by default.

When SC7 does apply: SC7.1 requires a harvest plan showing safeguards against spread.
SC7.2 requires evidence that the sourcing is part of a broader ecosystem management
activity, plus classification of the invasive species by an authority.

**Elk Meadow note:** Elk Meadow P2 involved mountain pine beetle-affected ponderosa pine
where MPB was the invasive pest. SC7 applied there. That template is specific to beetle
projects and must not be applied to projects with no invasive species component.

---

### A.5 — Counterfactual Scenario

**Read (BFA v1.3):** Section 3.0 (Counterfactuals) and Section 3.1 (Counterfactual Fate
Evidencing Requirements), AND Table 2 (Counterfactual Criteria — the CC2 row). Read
Table 2 CC2 before applying §3.1, because CC2 supersedes §3.1 for qualifying wildfire
feedstocks.

**Two paths — do not conflate them:**

**Path A/B (wildfire program feedstocks — CC2 applies):** Table 2 CC2 states: "Feedstock
is sourced through a government managed, funded or otherwise supported wildfire mitigation
program. The CO2e_Counterfactual of these feedstocks is 0." The documentation requirement
for CC2 is program participation + chain-of-custody — not a separate counterfactual fate
statement. §3.1's evidence types do not add a separate requirement on top of CC2. A.5 is
COVERED by the same chain-of-custody evidence used for A.6. No forester affidavit, no
wildfire risk map, and no haul-distance study are required by BFA v1.3 for CC2 feedstocks.
The A.5 submission text states that the counterfactual is wildfire combustion, CO2e = 0
per BFA v1.3 Table 2 CC2, and cites the CC2 chain-of-custody documents.

Note: Elk Meadow P2 submitted a forester affidavit, wildfire risk map, and haul-distance
study under A.5. Those are belt-and-suspenders, not BFA requirements. Do not flag their
absence as gaps for CC2 feedstocks.

**Non-CC2 path (no qualifying government wildfire program):** §3.1 evidence types apply.
At least one of the five types is required. For fuels treatment projects without a
government grant, the three most relevant are: (1) forester/land manager affidavit
confirming counterfactual fate, (3) assessment of most economically viable fate with
all data and assumptions, or (5) affidavit from the feedstock supplier ("in some cases").
Wildfire risk map and haul-distance evidence support option (3).

**Evidence types (CC2 path):** Same as A.6 — program participation and chain-of-custody
documents. No additional documents needed for A.5.

**Evidence types (non-CC2 path):** Forester/land manager affidavit or letter, state
wildfire risk map, USDA/USFS bioenergy economics study, purchase records confirming
counterfactual fate.

---

### A.6 — CC2: Wildfire Mitigation Program Evidence

**Read (BFA v1.3):** Table 2 (Counterfactual Criteria — read the CC2 row in full,
including the criteria text and documentation required column).

**Operational guidance:** CC2 requires evidence of program participation AND chain-of-
custody. Chain-of-custody means every link is documented: government program → land →
forester/contractor → Charm. Gaps in the chain are hard blockers.

Full chain documentation needed:
1. Grant award documentation naming the program and the recipient.
2. Grant scope of work connecting the specific land area to the grant.
3. Forester/vendor connection: subcontract, land manager letter naming the forester,
   or forester affidavit attesting they are contracted for the project.
4. Purchase/supply agreement between Charm and the forester/vendor with an exhibit
   specifying the project name and biomass type.
5. Scale tickets and delivery log as deliveries begin (ongoing; not required at
   submission stage).

**Elk Meadow chain:** COSWAP grant → ECFPD (grant recipient) → affidavit from JCPOS
(land manager) naming SOCO Forest Management → Charm purchase agreement Exhibit A
specifying "non-sawmill quality softwood from the Elk Meadow MPB Phase II Project."

**Evidence types:** Grant award letter/notice, grant scope of work (Attachment A),
land manager letter or forester affidavit naming the contractor, feedstock supply
agreement with project-specific exhibit.

---

### A.7 — PF2: Not Suitable for Long-lived Wood or Pulpwood

**Read (BFA v1.3):** Table 3 PF2 row in full — both the criteria column and the
documentation required column, including the wildfire exemption clause in the
documentation column.

**Operational guidance:** Table 3 PF2 documentation column contains a wildfire program
exemption. Read its exact conditions before assessing. If the wildfire exemption applies,
the CC2 evidence from A.6 covers the formal PF2 requirement — no separate BFA-mandated
documentation is required.

**For a CC2 wildfire feedstock, that is the whole requirement — do NOT flag a
non-merchantability attestation as a gap.** PF2 is exempt via the wildfire program, and
the counterfactual (A.5/CC2) is zeroed by program participation, not by a merchantability
statement. A standalone non-merchantability attestation is neither required by PF2 (exempt)
nor by CC2 (which needs only program participation + chain-of-custody). This matches A.5:
for CC2 feedstocks, a forester affidavit is belt-and-suspenders, not a BFA requirement, and
its absence is not a gap. A non-merchantability statement is only load-bearing on the
NON-CC2 path (§3.1), where you must evidence the counterfactual fate directly.

**Evidence types:** CC2 chain-of-custody docs (same as A.6). Nothing additional for a CC2
feedstock.

> Discipline note (this section previously told the screener to require a non-merchantability
> attestation "regardless of the PF2 exemption" — that was wrong and produced a manufactured
> must-have). A gap belongs on the checklist ONLY when a specific documented criterion is
> both unmet AND not exempted/satisfied. That a validated precedent (COWF-005) happened to
> include a document does NOT make that document required. Evaluate the evidence against the
> criteria; do not invent requirements the criteria do not impose.

---

### A.8 — ML1: Market Leakage

**Read (BFA v1.3):** Section 4.0 (Market Leakage Emissions), Section 4.2 (Evaluating
Market Leakage — Table 4 in full), Section 4.3 (Calculation of Leakage Emissions).

**Isometric confirmed position (Chris Pollard, May 26, 2026):** For feedstocks
qualifying under Path A (government grant — e.g., CSFS FRWRM, CSFS State Fire
Assistance WUI, Boulder County Strategic Fuels Mitigation Grant) or Path B (credentialed
forester citing an authoritative government wildfire mitigation plan):

> "The feedstock would not incur any discounts through the counterfactual storage or
> market leakage mechanisms, as the appropriate counterfactual would be that the
> feedstock would be consumed by wildfire."

**Operational guidance:** For wildfire program feedstocks where CC2 (A.6) is satisfied,
ML1 = 0. No ML sub-pathway (ML4, ML6, etc.) documentation is required. The argument is:
biomass was made available to meet the goals of a wildfire fuels reduction program, not
in response to market demand. The same chain-of-custody evidence used for CC2 covers ML1.

This is confirmed by the Elk Meadow P2 submission approach and by Isometric's written
position. The submission text is the deliverable — no additional documents beyond the
CC2 chain-of-custody already in A.6.

If the project is NOT a qualifying wildfire program (Path A or B), revert to BFA v1.3
Table 4 to identify which ML sub-pathway applies.

**Evidence types:** No new documents. CC2 evidence from A.6 covers ML1.
Reference document: "Charm Wildfire Mitigation Clarification.pdf" (Chris Pollard,
Isometric, 2026-05-26, Drive ID: 1zz6y5A1gORRTYDYSvoR4iv31VGwHH3Yx).

---

## Workflow: folder setup, alerts, and approval gate

When running a pre-screen as part of the full workflow (Max provides a Drive folder):

1. **Create project folder** — create a new folder named after the project inside the
   prospective biomass sources staging folder. Copy all source documents into it.

2. **Run the pre-screen** — read all documents, read all required BFA v1.3 sections,
   produce the pre-screen output per Step 3a below.

3. **Send Slack alert 1** — DM Max directly (user ID: UL2SL4H5H):
   "Finished Initial Review: [Project Name]. Approval required."
   This is the gate. Do not produce final documents until Max explicitly approves.

4. **After approval** — create a subfolder inside the project folder named
   "[Project Name] -- Review Documents". Produce the two work product documents
   (report + checklist) as .docx and .xlsx using python-docx and openpyxl, then copy
   both to that subfolder via the local Drive mount at
   `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/`. Send Slack alert 2
   as a DM to Max: "Review Complete: [Project Name]."

---

## Step 3a — Pre-screen output format

**Do not hand-build the deliverables. There is ONE builder and you MUST use it:**
`build_deliverables.py` (in this skill folder). Assemble a JSON spec (schema documented
at the top of that file) and run:

```
python3 "<skill>/build_deliverables.py" <spec.json> "<project>/… -- Review Documents"
```

It emits the two work products with a structure that is IDENTICAL for every project.
Never improvise a different layout or extra sections ("Overall Assessment", "Summary
Assessment", "Evidence Reviewed") — that is how the projects drifted apart. If the
template must change, change `build_deliverables.py` once so every project moves together.

**Filenames — update in place, never rename or delete an existing deliverable.** If the
project already has a pre-screen report and/or gap checklist, pass its EXACT existing
filename via the spec's `prescreen_filename` / `checklist_filename` so you overwrite that
same file (same Drive identity, same links). Do NOT create a new file under a "tidier"
name and delete the old one — that orphans the user's links and is not what "update" means.
Only when a deliverable does not yet exist do you coin a name:
`"<project> — BFA v1.3 Pre-Screen.docx"` / `"<project> — BFA v1.3 Gap Checklist.xlsx"`.
The source tracker the user provides is an INPUT — never write to it (enforced by
input_file_write_guard.sh).

The builder assembles the spec into the sections below. Your job in the assessment is to
fill the spec correctly (nomenclature rows, must-have/should-have items, A.1–A.8), not to
lay out the document.

Produce two sections **in this order**: outstanding documents first, evidence coverage
second. The biomass team needs the action list at the top.

### Section 1: Outstanding Documents Required for Validation

A numbered list of outstanding items, grouped by urgency.

**Cross-document coverage check (run before writing any gap item):** A blank field in
one document is NOT automatically a gap. Before flagging anything as missing, ask:
"Across ALL documents read this session, does anything satisfy this requirement?" If
another document in the evidence set covers it, the item is not a gap. Only flag an
item if the full evidence set, taken together, leaves the requirement unsatisfied.
This check runs BEFORE generating gap items, not after. Catching a blank field and
then checking coverage is the wrong direction — it produces false gaps.

**Citation gate (no exceptions):** Every gap item MUST include a **Source:** line that
quotes or names the specific BFA v1.3 table row, section, or documentation-required
column text that mandates the item. If you cannot complete the sentence "BFA v1.3
[table/section] requires..." for a given item, the item does not belong in this list.
A gap item with no Source line is the same failure as a coverage finding with no "BFA
requirement" field — do not deliver it.

**Nomenclature mismatches** (hard blockers — carry forward directly from the
Step 1b Nomenclature Consistency table; no BFA source line required because the
blocker is chain-of-custody integrity, not a specific BFA criterion):
- For each NO row in the table: name the document, the canonical name (from grant
  award), the name actually used, and what correction or supplemental attestation
  is needed to resolve it (e.g., "Revised forester affidavit using the legal project
  name as written in the grant SOW," or "Addendum from vendor confirming their legal
  name is X, not Y").

**Must-have before submitting to Isometric** (hard blockers — validation cannot proceed):
- For each: what document is needed, what it must contain or attest to, format guidance
  (letter on company letterhead, signed affidavit, grant award notice, contract exhibit),
  who should provide it, and a **Source:** line tracing the requirement to BFA v1.3

**Should-have** (Isometric will likely flag with an ISS comment during validation, but
submission can proceed):
- Same format as above, including the **Source:** line

Where Elk Meadow P2 had an equivalent gap that was later resolved, note it: "Isometric
raised ISS-XX asking for [X] — this is the equivalent request."

### Section 2: Evidence Coverage

Go through each of the 8 requirements (A.1–A.8) in order. For each, the output MUST
contain all four fields below. A finding with a missing "BFA requirement" field is
incomplete and must not be delivered — go read the source before writing the status.

- **BFA requirement:** Verbatim quote of the governing BFA v1.3 text (the criterion
  and/or documentation required field), read in this session. For A.1 and A.2 (Certify
  platform fields with no BFA criterion), write "Certify platform field — no BFA criterion"
  and proceed. For every other requirement this field must contain actual quoted text.
  This is not optional. If this field is blank, the finding is not done.
- **Status:** COVERED | PARTIAL | MISSING — justified against the verbatim BFA text
  above, not against the operational guidance
- **Evidence:** [document filename] — [verbatim quote or specific content that addresses
  the requirement]
- **Gap (if PARTIAL or MISSING):** what specific element is absent from the full
  evidence set (not from any single document), traced to the BFA requirement above.
  Before writing a gap, confirm the information is absent across ALL documents —
  not merely absent from the document where you would expect to find it.

Be strict. "COVERED" means the document provides the actual information required —
not just that a document exists. A scope of work that describes the project covers
species/stand data for A.1 but does NOT cover the forester's EIN for A.2.

---

## Step 4b — Certify fill output format

For each of the 8 requirements (A.1–A.8), produce:

**Submission text** — Ready to paste into the Certify text field. Match the Elk Meadow P2
style: factual, direct, 2–5 sentences. Name the BFA v1.3 criteria codes (SC1, SC7, CC2,
PF2, ML1) where relevant. Reference specific documents by name (not by Drive URL).

**Documents to attach** — List of specific files from the evidence folder (by filename)
to upload as supporting evidence for this requirement. If a document spans multiple
requirements (grant SOW covers A.3, A.6, and A.7), list it under each.

---

## Reference: Elk Meadow P2 as the validated template

COWF-005 (Elk Meadow P2) is the closest validated precedent. Colorado wildfire program,
beetle-affected ponderosa pine and Douglas-fir, sourced through SOCO Forest Management
under a COSWAP grant. Its Certify submissions are the authoritative template for similar
wildfire-mitigation forestry projects.

Isometric raised three REMI SUGGESTION issues on Elk Meadow P2's initial submission:
- ISS-40: Provide wildfire mitigation grant evidence → fixed by providing COSWAP
  grant documentation
- ISS-39: Provide carbon stock assessment → resolved by establishing wildfire program
  exemption (SC1.2 exemption in Table 1)
- ISS-38: Provide certification or risk assessment → raised before grant docs were
  submitted; resolved once COSWAP grant docs provided (Table 6 lists government wildfire
  programs as satisfying SC1.1 directly via Appendix 3)

For any new project that is also a Colorado wildfire/fuels-reduction program, all three
are pre-empted by submitting complete grant documentation upfront.

The Elk Meadow P2 full submission text is at (Google Doc):
`elk_meadow_p2_feedstock_requirements_certify_2026-06-10`

---

## Citation standard

Every claim about what a document says must be grounded in verbatim text from the
document, read in this session. Do not characterize document content from memory and
present it as a citation. If a document has not been opened this session, say so.
