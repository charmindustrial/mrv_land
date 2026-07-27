# Site Emissions QA — Lessons Learned

This document captures specific failure patterns from real QA sessions. The QA agent should read this alongside `category_evidence_guide.md` at the start of each session. These aren't theoretical risks — they are things that actually went wrong and caused rework.

## Session: Basco 6 LA, March 2026

### Failure 1: Describing Work Instead of Doing It

**What happened:** The checklist contained entries like "Verify all column headers, EF cells, and totals in diesel calc sheet include unit labels." This was flagged as a laziness violation — the agent was writing instructions for a future reviewer rather than reporting its own findings.

**Root cause:** Context fatigue in a long session. The agent shifted from actually reading documents to producing template-like entries that looked complete but contained no real verification.

**Fix applied:** SKILL.md now includes Anti-Pattern 1 ("Verify X" Cop-Outs) and Universal Requirement U1 (Units on All Labels) which specifies the expected output format: "Column headers: Date (no units needed), Volume (gallons), Mass (kg), EF (kgCO₂e/kg), Total (kgCO₂e) — all present."

### Failure 2: Quoting Max's Notes Verbatim

**What happened:** The agent included entries like "Per Max: 'It looks like they drove the truck to fill up'" in the QA checklist. Max had shared this as a question for Garrett (a process conversation), not as a QA finding. The agent treated it as a confirmed fact.

**Root cause:** The agent conflated process context (things Max said to help the agent understand the workflow) with evidence-based findings. The checklist should only contain what the agent verified from the evidence.

**Fix applied:** Universal Requirement U8 (QA Output Standards) now explicitly prohibits quoting Max or including process conversations. Anti-Pattern 4 documents this in detail.

### Failure 3: Treating Feedback as One-Off Corrections

**What happened:** Max flagged that the diesel calc sheet was missing units on column headers. The agent added a units check for diesel but didn't check any other category's calc sheets for units. Similarly, when Max flagged missing distance evidence for methanol, the agent didn't check distance evidence for other transport categories.

**Root cause:** The agent treated each piece of feedback as a specific correction rather than extracting the universal principle. This is the single most important lesson from the session — every gap Max identifies represents a class of checks, not a single instance.

**Fix applied:** Anti-Pattern 2 (Treating Feedback as Case-Specific) and the Universal Cross-Cutting Requirements section in SKILL.md. The key principle is now in Key Principles: "When a requirement exists (units on labels, distance evidence, BCU cross-check), it applies to every category."

### Failure 4: Wrong FAIL/FLAG Classification

**What happened:** A missing diesel transaction record (receipt #013317) was marked as FLAG instead of FAIL. The reasoning was that other receipts supported most of the total, so the missing one was a minor gap.

**Root cause:** Misunderstanding of the FAIL/FLAG distinction. FLAG = hygiene issue where the data still supports the reported value. FAIL = you cannot independently confirm the reported value. A missing receipt means you can't confirm that receipt's contribution to the total — that's a FAIL.

**Fix applied:** Universal Requirement U4 (Missing Evidence = FAIL) with the decision rule: "Can you independently confirm the reported value from the available evidence? Yes → FLAG. No → FAIL."

### Failure 5: Missing BCU Cross-Check for Methanol Transport

**What happened:** Methanol transport process emissions (36.17 kgCO₂e) are BCU-eligible, but the agent didn't check whether a BCU offset was applied or whether the BCU Quant sheet had a corresponding line item.

**Root cause:** The agent checked BCU eligibility for diesel and brine (the most obvious categories) but missed methanol transport, argon transport, and other eligible components. BCU cross-checking was applied inconsistently across categories.

**Fix applied:** Universal Requirement U3 (BCU Quant Sheet Cross-Check) now includes the complete list of BCU-eligible site emission components and requires that every one be cross-checked against the BCU Quant sheet.

### Failure 6: Wrong EF Source Year

**What happened:** The agent initially cited diesel EF source as "GREET 2024." The actual source on the correct tab of the Standard EF Sheet is "GLEC V3.2 2025." The agent was reading from the wrong tab.

**Root cause:** The Standard EF Sheet has multiple tabs (one per year). The agent didn't confirm which tab it was reading from, or read from a prior-year tab.

**Fix applied:** Universal Requirement U7 (Correct Year Tab) with the specific Google Sheet ID and the rule: always confirm which tab you're reading from before citing any EF values.

### Failure 7: Including Process Questions as Findings

**What happened:** The agent included a WEX card question (whether WEX fuel card transactions are captured in the diesel calc sheet) as a checklist item. This was a question Max had raised with Garrett — a process discussion, not a QA finding.

**Root cause:** Same as Failure 2 — the agent didn't distinguish between process context and QA findings.

**Fix applied:** Covered by U8 and Anti-Pattern 4.

### Failure 8: SP&C Finding Incorrectly Diagnosed

**What happened:** The agent reported SP&C as FAIL due to "missing calc." The actual issue was that the calc sheet existed but had a formula error — an extra space in the Total Weekly Penalty function causing the totals to error out.

**Root cause:** The agent either didn't open the calc sheet or didn't read it carefully enough to identify the actual problem. It reported a blanket "missing" when the issue was more nuanced.

**Fix applied:** This reinforces the core principle: actually open and read every document. Don't infer from the absence of a result that the document is missing — it might be present but broken. Report what you actually see.

## Session: Basco 6 LA, April 2026 (added 2026-05-07)

This session triggered the structural overhaul of the site-emissions-qa skill: introduction of the source-read log artifact (Gate 1), `[log:KEY]` citation discipline (Rule 1), pre-delivery audit script (Rule 5), and Filename Matching Avoidance / Calc Sheet Surface Read as distinct +3 penalty categories. The agent shipped a Phase 1 checklist with multiple Pass rows that did not survive primary-source verification once Max pushed back. Memory had four prior entries on the underlying pattern; pattern recurred. Fix had to live in the skill itself.

### Failure Category 9: Filename Matching Avoidance

**What happened:** Agent inventoried Drive subfolders and called distance evidence Pass on filename match alone. Specifically: "Sitework Distances subfolder contains Douglas Tank to Basco Distance Map.png — Pass on distance evidence." The PNG was never opened. When opened (after Max pushed back), it showed three route options (1,759 / 1,756 / 1,779 mi); calc sheet used 1,729 mi. None of the route options matched the calc-sheet number — 30-mile understatement on Kerry Tank transport process emissions (~9.4 kg) and embodied (~5.8 kg).

**Root cause:** The agent treated Drive file presence as evidence. Filename matching is inventory, not verification.

**Fix applied:** (1) Anti-Pattern 6 in SKILL.md. (2) Mandatory verification sub-task #2 in Gate 2: every distance PNG must be opened and the value extracted. (3) Source-read log requirement: `evidence_files` entries without `extracted_values` are invalid, and the audit script catches Pass rows whose `[log:KEY]` resolves to a stub. (4) Filename Matching Avoidance penalty: +3 per affected category.

### Failure Category 10: Sample of One

**What happened:** Agent opened one of four diesel receipts and one of five gasoline receipts, called both categories Pass on receipt-vs-calc-sheet, missed that the 4/27 gasoline receipt was Unleaded Plus (not Regular). Max caught it and asked: "did you do the math by referencing what's in each receipt?" Honest answer: no — sampled one, inferred the rest from filenames.

**Root cause:** Sampling is not auditing. A sample of one validates one row, not a category.

**Fix applied:** Mandatory verification sub-task #1 in Gate 2: every receipt PDF / invoice / scale ticket opened, every value extracted into the source-read log. Sample-of-one is treated as Filename Matching Avoidance (+3). Per Charm KB §0: "BE EXHAUSTIVE. NO SHORTCUTS. NO EXCEPTIONS."

### Failure Category 11: Calc-Sheet Surface Read

**What happened:** Agent reported "Diesel calc sheet Total CO2e (kg): 847.917 → matches BCU Quant 847.917 → Pass on math." But never opened the formula cell. Actual formula was `Total Delivered (gal) × 3.87` — gallons multiplied by the per-kg-fuel emission factor with no density conversion. Correct math: `gal × 3.21725 kg/gal × 3.87 kgCO2e/kg = ~2,727.8 kg`. ~3.2× understatement (~1,880 kg). The parallel gasoline calc sheet correctly applied density × EF; the diesel sheet's bug was visible only by reading the formula.

**Root cause:** Surface-reading the output cell missed a dimensionally-incorrect formula. The output looked fine; the math was broken.

**Fix applied:** (1) Anti-Pattern 8 in SKILL.md. (2) Source-read log `derived` block requirement: every calc-sheet output cited in the log must have its constituent inputs and the formula trace recorded, not just the output value. (3) Calc Sheet Surface Read penalty: +3 per affected calc sheet.

### Failure Category 12: KB Skipped Under "Scope Gap" Rationale

**What happened:** Agent never read `Charm_Isometric_Knowledge_Base.md` during the April 2026 Basco RP. Noted it as a "scope gap to revisit if any KB-specific issue arises." Then the agent flagged the railcar email PNG as "lower-rigor evidence than Google Maps" — a finding that the KB explicitly invalidates. KB §3 (AECN Rail Batch Reference) authorizes email/written confirmation from the rail logistics provider as the AUTHORITATIVE source for rail distances; no Google Maps required for rail. The agent's flag was wrong by KB convention.

**Root cause:** Skipping the KB makes the agent unable to recognize KB-sanctioned exceptions, so the agent invents wrong flags.

**Fix applied:** Pre-Flight Gate in SKILL.md mandates KB read before Gate 1. The print-Failure-Categories step makes skipping visible to Max in the chat. Gate 1 source-read log requires `kb_sections_read` to be non-empty.

### Failure Category 13: LCA Document Filename-Only "Pass"

**What happened:** CapEx LCA documentation links: agent observed Documentation subfolder filenames (Kerry Tank LCA.docx, Triton Shaker LCA.docx, etc.) and gave the row a Flag with note "Documentation subfolder content suggests recent additions are documented." The LCA docx files were never opened. When opened (after Max pushed back), three substantive findings emerged: (a) Kerry Tank LCA used a stainless-steel EF unit interpretation different from the Catch Tank LCA in the same folder (one treats `MTCO2e/T Steel` as per-short-ton, the other as per-metric-tonne — Kerry overstated by ~167 kg); (b) Triton Shaker and 60kW Generator LCAs used an off-list ecoinvent EF (1.937 production + 0.07 + 0.06 = 2.067 kgCO2e/kg) not in Charm's Standard EF Sheet; (c) Catch Tank weight is an engineering estimate, not vendor nameplate.

**Root cause:** Same as FC9 — Drive file presence treated as evidence.

**Fix applied:** Mandatory verification sub-task #3 in Gate 2: every new LCA docx opened, weight + EF + GWP extracted. Filename-only Pass = Filename Matching Avoidance violation.

### Failure Category 15: Renderer-as-Source for xlsx with Formulas

**What happened (Apr 2026 Basco re-run, after the new source-read-log + citation system was already in place):** The Railcar calc sheet was read via Drive's `read_file_content` tool. That tool returns a natural-language text representation of the file. For xlsx with named-range formulas (e.g., `=F2*ProcessEF`, `=F2*EmbodiedEF`), the renderer cannot resolve the named ranges and emits `#NAME?` as the cell text. The agent logged `"formula_cells_status": "#NAME? errors throughout"` as an extracted value and shipped a FAIL on "Railcar calc sheet — formula errors throughout." Max opened the actual xlsx, saw normal computed cells, and called it out. Verification via `openpyxl.load_workbook(path, data_only=True)` showed the sheet computes correctly: Total Process = 0.07361 MT, Total Embodied = 0.08844 MT, Total = 0.16205 MT — matching BCU Quant exactly.

**Root cause:** Treating Drive's `read_file_content` text dump as a primary-source read of an xlsx with formulas. The renderer is a stand-in, not the cells. The audit script validates citations against the log but cannot validate that values IN the log are correct — garbage in, garbage out.

**Fix applied:** SKILL.md Gate 1 now contains a HARD RULE table that maps each source type to the correct read method. xlsx with formulas MUST go through `download_file_content` → openpyxl with `data_only=True` → cached-value read. The earlier soft-rule mention of "open the calc sheet" is insufficient when the implicit "open" was Drive's text renderer.

**What this means structurally:** the source-read log + audit script catches "did you cite a logged value." It does NOT catch "is the logged value itself a fabrication or a renderer artifact." Type-aware read methods are the missing layer.

### Failure Category 14: Manifest Surface Read (Waste Disposal)

**What happened:** Calc sheet treated Manifest 620157 disposal as "Bio-Oil Contaminated Gravel" with disposal EF 0.000259 MTCO2e/kg. The actual ticket (March Oil Spill Disposal.png) was never opened in the first pass. When opened, it showed: material classified as "C&D YARD ACADIANA" (Construction & Demolition); ticket dated 3/12/2026 (March, not April RP); Gross/Tare/Net all 00 lb (load was NOT weighed — mass derived from 20 cubic yards × 999 lb/cy density assumption); customer code L105142/REDBOX, not Charm directly. None of these substantive findings would have been caught without opening the ticket itself.

**Root cause:** Same as FC9 + FC11 (filename matching + surface read of the calc sheet rather than primary source).

**Fix applied:** Mandatory verification sub-task #4 in Gate 2: the actual disposal ticket / manifest opened, with material classification, weight fields, date, customer code extracted into the source-read log.

## Phase Contract (added 2026-05-07)

The skill supports Phase 1 (pre-Certify) / Phase 2 (post-Certify) / Full modes. Strategic intent: push QA earlier so errors get caught and fixed in the calc-sheet layer before they ever reach Certify. Phase 2 should be a thin reconciliation pass over a much smaller set of survivors. If Phase 2 keeps surfacing substantive errors (math, missing evidence, wrong EF), that's a signal Phase 1 isn't catching enough and the skill needs to be tightened.

Hard rules:
- `Pending` is ONLY for checks requiring Certify state that does not yet exist. Missing Drive evidence in Phase 1 is still FAIL (U4 still applies inside the folder).
- Every `Pending` evidence note MUST contain the calc-sheet authoritative value. Phase 2 compares Certify against THAT value, not against the source receipts again.
- A Phase 1 checklist with `Pending` items is not "done." It's halfway. Deliver it as a Phase 1 deliverable awaiting Phase 2, not as a finished QA.
- In Phase 2, do not re-QA non-Pending items. Phase 1 findings are findings-of-record. Re-running them is wasted effort and risks inconsistency.
- Same file is reused across phases. Do not create a Phase 2 file — open the Phase 1 file and update it.

## General Takeaways

1. **Every piece of feedback represents a class.** If Max says "methanol is missing distance evidence," check distance evidence for EVERY transport category. If he says "diesel headers need units," check headers for EVERY calc sheet.

2. **The checklist is a report, not a to-do list.** Every entry should describe a completed check with specific values, not an instruction to perform a check.

3. **Context fatigue is real and predictable.** After ~100+ checklist items in a long session, quality degrades. The agent should self-monitor and recommend a fresh session rather than producing template-filled output.

4. **The three-layer chain is the backbone.** Certify value → Certify evidence → Drive folder. Every break is a FAIL. This is the single most important structural concept in site emissions QA.

5. **BCU eligibility requires exhaustive checking.** No automated guardrail prevents erroneous BCU applications. The agent must check every eligible component and every applied BCU, every time. The BCU Quant sheet is the reconciliation tool — use it.
