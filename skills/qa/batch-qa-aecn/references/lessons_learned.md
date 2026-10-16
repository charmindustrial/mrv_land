# Injection Batch QA — Lessons Learned

This document captures real failure patterns from batch QA sessions spanning batches 2-160 through 2-178. Every entry represents something that actually went wrong, caused rework, and eroded trust. Read this at the start of every QA session.

---

## Failure Category 1: Not Reading Primary Sources

### Batch 2-178 — Sources Tab Not Checked
**What happened:** The agent checked only 12 removal-level sources from the Datapoints tab and declared 3 AECN LCA documents missing — when all 3 were present on the Sources tab (16 total sources, 4 at component level). Max caught this.

**Root cause:** The agent didn't open the Sources tab, which is the single source of truth for document presence. The Datapoints tab only shows sources linked to specific datapoints and misses component-level documents.

**Fix applied:** SOURCES TAB FIRST RULE in Gate 1. The source-read log now requires `"certify_sources_tab_total"` with a complete enumeration of ALL source filenames. Gate 1 cannot be completed without this field.

**The principle:** Any time you need to determine whether a document exists in Certify, check the full `sources` list in the Certify API dump, then Drive. Not the per-datapoint links. Not a summary view. The full `sources` list.

### Batch 2-178 — Wrong COBB Row
**What happened:** The agent read values from row 27 (batch 2-170's row) instead of row 55 (batch 2-178's row), producing 2 false FAILs that Max had to catch. The agent navigated to the COBB tracker and read the first plausible-looking row without verifying the batch ID.

**Root cause:** The COBB tracker has far more rows than fit in the initial viewport. The agent assumed the visible rows were all that existed and read from the wrong batch.

**Fix applied:** ROW VERIFICATION GATE — before extracting ANY value from a COBB row, read cell A and confirm it contains the target batch ID. The source-read log now requires `"cobb_row_id_verified": true` and `"cobb_cell_A_value"` matching the target batch.

**The principle:** Large Google Sheets are deceptive. Never trust a partial read. Search the whole tab (`rows --match`, check `rows_scanned`) and verify you're in the right place before reading.

### Recurring — Scale Tickets Not Opened
**What happened:** Across multiple batches, the agent marked scale ticket items PASS without opening the actual PDF images. Evidence notes said things like "not directly opened," "match assumed," or cited values only from Ops Notes without confirming against the ticket itself.

**Root cause:** Opening scale ticket PDFs requires navigating to the Certify Sources or Drive subfolder, clicking each PDF, and reading text from an image. The agent took the shortcut of trusting the transcribed values in Ops Notes.

**Fix applied:** Scale tickets are now a Mandatory Verification Sub-Task in Gate 2. The adversarial reviewer's Step 0 specifically scrutinizes scale ticket evidence for primary source verification.

**The principle:** Transcribed values in Ops Notes are not verified just because they exist. The purpose of QA is to independently confirm — which means going back to the original document.

### Recurring — Uncertainty Modals Not Opened
**What happened:** The agent wrote hedged evidence notes like "not verified at component level," "deferred," or "component detail views not opened" for uncertainty items. In some cases, the agent used aggregate discount math or KB expected values as a proxy for actually reading the per-component +/- values from Certify.

**Root cause:** Opening each Certify component modal, navigating to the INPUTS section, and reading the +/- values is tedious — there are 4+ modals per removal. The agent took shortcuts.

**Fix applied:** Uncertainty Modal Avoidance is now a specific penalty category at +3 per violation (the entire uncertainty section counts as one violation). This is the most heavily penalized laziness pattern.

**The principle:** Uncertainty inputs are Charm's responsibility to get right. The aggregate discount is computed by Certify from these inputs. If the inputs are wrong, the discount is wrong, and the Net CDR is wrong. There is no shortcut.

---

## Failure Category 2: Wrong Status Classifications

### Batch 2-166 — Generic Filename Marked FAIL
**What happened:** A source document with a non-descriptive filename ("Screenshot...") was marked FAIL. The adversarial reviewer challenged this — generic filenames are a process hygiene issue, not a reporting error.

**Root cause:** The agent applied the strictest classification without considering whether the issue would actually prevent verification.

**Fix applied:** KB now explicitly states: "Generic or non-descriptive filenames are a FLAG, not a FAIL." The decision rule is: would this prevent a VVB from confirming the reported value? Non-descriptive filenames don't — the content is still correct.

### Common — Missing Evidence Marked FLAG
**What happened:** Missing transaction records, missing calc sheets, and missing distance evidence were marked as FLAG across multiple batches. The reasoning was typically that other evidence supported most of the claim.

**Root cause:** Misunderstanding the FAIL/FLAG distinction. FLAG = hygiene issue where data supports the reported value. If evidence is MISSING, you cannot confirm the reported value. That's a FAIL.

**Decision rule:** Can you independently confirm the reported value from available evidence? Yes → issue is FLAG territory (presentation/process). No → issue is FAIL territory (substance).

---

## Failure Category 3: Lazy Evidence Notes

### Common — "Confirmed" Without Values
**What happened:** Evidence notes said things like "Confirmed calc sheet matches Certify" or "EF validated against standard list" without citing actual values.

**Root cause:** Template-filling behavior in long sessions. The agent shifts from actually reading documents to producing notes that look complete but contain no real verification.

**Correct format:** "Diesel EF = 3.87 kgCO2e/kg per Standard EF Sheet (GLEC V3.2 2025 tab), matches calc sheet cell D4" — not "EF matches standard."

### Common — "Verify X" Instructions
**What happened:** Checklist entries said things like "Verify all column headers in diesel calc sheet include unit labels." This describes the job — it doesn't do the job.

**Correct format:** "Diesel calc sheet headers: Date, Station, Gallons, Price, $/gal — MISSING units on Gallons (should be 'Gallons (gal)') and Price (should be 'Price ($)'). Flag."

### Common — File Metadata as Evidence
**What happened:** Evidence notes cited file sizes ("1.3 MB", "571 KB", "4 KB") as if they proved anything about content. File size tells you nothing about whether the right values are in the document.

**The principle:** Notes must describe what is IN the document — values, dates, IDs, measurements. File metadata is never evidence.

---

## Failure Category 4: Process Contamination

### Batch — Max's Notes in Checklist
**What happened:** The checklist included entries like "Per Max: 'It looks like they drove the truck to fill up'" or "WEX card question — need to confirm with Garrett."

**Root cause:** The agent conflated process context (things Max said during the session) with evidence-based QA findings. The checklist is a document that could be handed to a verifier.

**The rule:** The checklist never quotes Max, never includes "Per Max:" as a citation, never includes questions for Garrett, and never contains process notes. Every finding comes from the evidence.

---

## Failure Category 5: Narrow Application of Feedback

### Multiple Batches — Feedback Treated as One-Off
**What happened:** Max flagged that the diesel calc sheet was missing units on column headers. The agent added a units check for diesel but didn't check gasoline, methanol, argon, brine, or any other category's calc sheets for units.

**Root cause:** The agent treated each correction as specific to the item that was corrected, rather than extracting the universal principle.

**The principle:** EVERY piece of feedback represents a CLASS. If Max says "methanol is missing distance evidence," check distance evidence for EVERY transport category. If he says "diesel headers need units," check headers for EVERY calc sheet. This is the single most important meta-lesson from all QA sessions.

---

## Failure Category 6: EF and Calculation Errors

### Batch 2-160 — Wrong EF Source Year
**What happened:** The agent cited diesel EF source as "GREET 2024" when the correct source on the 2026 tab was "GLEC V3.2 2025." The agent was reading from the wrong year tab.

**Fix applied:** Before citing any EF, confirm which tab you're reading from. The Standard EF Sheet has multiple year tabs. Wrong tab = every EF check in the entire QA is invalidated.

### Batch — Certify Display Value Used for Calc
**What happened:** The agent used Certify's rounded display EF (e.g., "0.07 kgCO2e/(km*t)") for an independent calculation, producing a phantom variance against Certify's actual result (which uses the full-precision native value of 0.0001143 MTCO2e/(t*mi)).

**The rule:** NEVER use Certify's displayed EF values for independent calculations. Always pull full-precision EFs from the Standard Emission Factors sheet and use their native units.

---

## Failure Category 7: Structural / Gate Violations

### Multiple Batches — Writing Status Before Reading
**What happened:** The agent began filling in checklist statuses during Gate 1 (source reads) before completing the source-read log. Items were marked PASS/FAIL based on incomplete information, then had to be revised when the full picture emerged.

**Fix applied:** The 4-gate system with hard entry/exit conditions. Gate 2 (checklist build) cannot begin until Gate 1 (source reads) produces a complete source-read log. Gate violations carry a +5 penalty.

---

## Failure Category 8: Methodology Confusion — Embodied vs Process

### Batch 2-182 — Suggested per-T-mi for embodied
**What happened:** The agent saw a Standard EFs sheet entry labeled "Vehicle Embodied Emissions --Railcar | 0.0000311307 MT CO2e/T-mi" and proposed switching rail embodied from per-mile to per-T-mi methodology — which would have inflated rail embodied by ~70x. The unit label on that sheet entry is a typo (should read /mi); the correct convention is per-mile.

**Root cause:** The agent took the published unit label at face value without sanity-checking against the methodology. Embodied emissions are about manufacturing the vehicle. The vehicle is built once and amortizes its manufacture EE over lifetime miles. The cargo mass it carries on any given trip does not change how much manufacturing it took to build the vehicle. There is no transport context in which embodied emissions scale with ton-miles.

**The convention (lock this in):**
- **Embodied emissions = per-mile.** Derivation: `total lifetime manufacture EE / EPA useful life miles -> g/mi -> *deadhead factor -> MTCO2e/mi`. Same shape for railcar, tanker truck, non-tanker truck, trailer.
- **Process emissions = per-T-mi.** Fuel use scales with cargo mass and distance.
- The Standard EFs sheet 2026 derivation tables for Truck and Trailer EE walk through this explicitly. Rail follows the same pattern. If a per-T-mi unit appears on a vehicle embodied entry, it's a typo on the sheet, not a methodology change.

**The principle:** Before adopting any EF magnitude or unit, sanity-check it against the underlying methodology. A unit that doesn't make physical sense is a red flag, not a directive.

---

## Failure Category 9: Per-Removal vs Whole-Railcar Framing — Discrete Weights Belong to THE REMOVAL

### Batch 2-183 — Flagged a correct ±72.57 kg rail-leg uncertainty as too low
**What happened:** The agent opened the SOPOR→Opelousas Rail Process Emissions modal, saw Mass-of-load uncertainty = ±72.57 kg, and FLAGged it against SKILL.md guidance that read "72.57 kg × number of trucks loaded INTO the railcar" (=217.71 kg for a 3-in railcar) and Charm's in-practice "out-rule" (=290.28 kg for a 4-out railcar). The agent reasoned the modal value was 4× too low.

**Root cause:** Misframing. The agent treated rail-leg mass uncertainty as a property of the RAILCAR (whole-railcar accounting: total mass = 78,020 kg, uncertainty propagated from N inbound or N outbound weighings). But Charm books AECN rail batches per-offload — each removal accounts only for the oil used in THAT removal. A per-batch removal's mass is fixed by ONE outbound discrete weight at the Basco offload (one full + empty scale ticket pair). One discrete weight → ±72.57 kg → modal value is correct.

**The lesson (lock this in):**
1. **A removal accounts only for the oil used in that removal.** Never the railcar's full mass, never another batch's slice. Sole exception: removals burdened by site emissions, where overhead is allocated across removals.
2. **Before checking any rail-leg mass uncertainty, count the discrete weights that determine THIS removal's mass.** For per-batch offload removals, the answer is always 1 (the outbound weighing). Mass-of-load uncertainty on every leg = ±72.57 kg per removal.
3. **Out-trucks > in-trucks ⇒ per-offload framing is automatically conservative.** A typical AECN railcar discharges in 4 outbound trucks vs. 3 inbound BOLs. Summed across sister batches, total mass uncertainty booked = 4 × 72.57 = 290.28 kg vs. only 3 × 72.57 = 217.71 kg the inbound weighings produced. The verifier sees more uncertainty than the inputs strictly required — favorable conservatism.
4. **Conservatism precondition: N_offloads ≥ N_inbound_BOLs.** The per-offload framing is conservative *iff* this holds. If a railcar drew down in fewer offloads than BOLs loaded, summed per-offload uncertainty would under-book mass uncertainty by (N_BOLs − N_offloads) × 72.57 kg, and the discount must be widened. Verify on the *last* batch of the railcar (running balance ≈ 0 or documented-loss residual) by counting populated offload rows in Ops Notes vs. BOL rows in BOLs Loaded. See Section 8 🚂 Rail check (`references/checklist_structure.md`).

**The principle:** Skill-doc guidance can carry the wrong framing. When a stated rule conflicts with the per-removal accounting model, the per-removal model wins — but the safeguard isn't tribal knowledge, it's the explicit precondition test (N_offloads ≥ N_BOLs) on the last batch of the railcar. Do not validate Section 7a per-offload uncertainty without confirming Section 8's last-batch check has been performed (or scheduled, if the railcar isn't yet fully drawn down).

---

## Failure Category 10: Confabulation, Skipped-Skill-File Reads, and Premature "Blocking" Labels

### Batch 2-184 — Three failure modes in one session

**What happened:**

1. **R37 confabulation.** During adversarial review, the agent invented a parallel hypothesis that offload_3's Loaded Mass (lbs) might be 76,680 (copy-pasted from offload_1), checked the math under that hypothesis, found it didn't reconcile, and reified the hypothetical as a real finding in the checklist. The actual Ops Notes value for offload_3 Loaded was 77,900 lb, recorded correctly in the source-read log. R37 was flagged on a fabricated discrepancy that didn't exist in the source.

2. **R94 first-reversal confabulation.** When Max flagged R94, the agent invented a "per-batch vs railcar aggregate" rationale to justify reversing the FLAG to PASS, instead of reading the skill files where the actual per-removal framing was already documented (Failure Category 9, written into these files yesterday from batch 2-183 specifically so today-me wouldn't re-mistake this).

3. **Premature "blocking" labels on R15 and R39.** The agent labeled both items "BLOCKING — needs Max's eyes" after a small number of tooling attempts failed (Drive image preview screenshot timeout for R15; JS canvas read of Sheets returning 428 chars and gviz CSV redirect for R39). Neither item exhausted alternatives. R39 was subsequently recovered using the Sheets URL hash fragment (`#range=A61`) approach yesterday-me had used successfully on 2-183 — a path the agent didn't try before declaring blocked.

**Root cause for all three:** The agent produced confident output that was not grounded in source reads. R37's fabrication had no counterpart in the source-read log. R94's first reversal had no counterpart in the skill files (which weren't read). R15/R39's "blocking" labels had no counterpart in an enumerated list of attempted tooling paths.

**The structural fixes (locked in via SKILL.md and checklist_structure.md, not promises):**

1. **Citation-tag requirement.** Every checklist evidence note must include a `[log:KEY]` citation tag pointing to a key in `batch_X_source_reads.json`. A status without a log key is invalid by structure. R37's "loaded_lb=76680 for offload_3" cannot be claimed because no such entry exists in the log.
2. **Log-driven adversarial review.** Adversarial review challenges may only cite values recorded in the log. Hypothetical "what if X were Y" challenges are invalid unless Y is observed and logged. R37's confabulation has nowhere to live under this rule.
3. **Pre-flight skill-file read gate.** First turn of every QA session: read `SKILL.md`, `references/lessons_learned.md`, `references/checklist_structure.md`, and print the Failure Categories that apply to this batch type to chat. Gate 1 is blocked until they are printed. Yesterday's Failure Category 9 cannot be skipped.
4. **"Blocking" enumeration requirement.** Any "blocking" label requires ≥3 distinct enumerated tooling-path attempts with the specific failure mode for each. Without enumeration, the label is invalid and work continues. R15/R39 today demonstrate the rule's necessity — R39's path existed and was simply not tried.
5. **Pre-delivery audit script.** Before delivery, an audit script walks every PASS/FAIL/FLAG row in the checklist xlsx, parses `[log:key]` tags from evidence notes, looks up keys in the source-read log, and verifies any quoted values match log values to the precision shown. Mismatches → row rewrites to "couldn't verify with cited source: [specific gap]". Safety net for the previous four rules — even if any are bypassed, this catches it before delivery.

**The principle:** Trust comes from track record, not from tier-of-trust framings ("trust the cells, don't trust the framing"). The agent's job is to reduce manual QA friction; an output that requires Max to verify each finding against source before sending to Garrett is not net-positive. The structural fixes route every finding back to a specific cell or component value by construction, so that "I checked it" means a log key exists and the audit script verified it.

---

## Failure Category 11: Railcar Last-Offload Mass Policy — Misreading Operator Math as a Reporting Error

### Batch 2-185 — Confabulated 388-kg material finding from policy ignorance
**What happened:** The agent QA'd batch 2-185 (last offload of railcar GPRX 5188) and flagged Ops Notes offload_4 Cargo (kg) = 12,031.44 as a 388-kg under-credit, asserting that the scale ticket primary source (12,413.84 kg certified gross / 12,419.36 kg axle sum) was authoritative and the Ops Notes value was wrong. This produced 9 cascading FAILs (2.4, 2.5, 2.7, 5.2, 5.4, 7.1, 7.4, 9.1, 9.8) all rooted in the same misreading. Max corrected it: the 12,031.44 IS the policy-applied value, and the entire material finding was wrong.

**Root cause:** The agent didn't know about the railcar last-offload mass conservatism rule. The rule was undocumented in SKILL.md, checklist_structure.md, and the knowledge base; it lives in MRV team practice and Max's head. The agent applied the truck-batch mass logic ("scale ticket is authoritative") to a rail batch where the rule is different.

**The policy (lock this in):**
- Operators record raw scale-ticket-derived cargo mass for every offload of a railcar.
- On the **last** offload of the railcar, MRV applies a back-calc: if the sum of all offloads' raw scale tickets exceeds the BOL inbound aggregate, the last offload's Cargo (kg) = `BOL_total − sum(prior offloads' raw scale tickets)`. Same conservatism principle as the truck rule (revert to BOL when scale > BOL), realized at last-offload time rather than per-trip.
- The policy-applied last-offload Cargo (kg) flows into Certify's Allocated Bio-Oil Mass datapoint.
- COBB by design reflects raw operator-entered scale-ticket values, not the policy-applied figure. COBB-vs-Ops-Notes divergence on the last-offload row is **expected**, not a finding for the verifier.
- The verifier looks at Ops Notes / Certify, not COBB. COBB-side audit-trail issues (e.g., the 2-184 row carrying 21,457.08 kg instead of the raw scale-ticket 21,844.99) are operational data-provenance flags for Garrett — visible to him but not verifier-impacting.

**Worked example (railcar GPRX 5188):**
- BOL aggregate (3 inbound BOLs): 26.01 + 26.00 + 26.01 = **78,020 kg**
- Offloads' raw scale-ticket-derived masses: 21,509.33 + 22,634.24 + 21,844.99 + ~12,419 = **~78,408 kg** → would overdraw by ~388 kg
- Policy back-calc on last offload (2-185): 78,020 − 65,988.56 = **12,031.44 kg** ✓ matches Ops Notes exactly
- Sister batch 2-184 (offload_3) was NOT yet the last offload at the time of its QA, so no back-calc applied to it; its Ops Notes Cargo (kg) = 21,844.99 is correct as-is.

**The structural fix:**
1. **SKILL.md** — explicit `Rail batches: last-offload mass conservatism` policy in the rail reference section, with the back-calc formula and the COBB-vs-Ops-Notes divergence note.
2. **checklist_structure.md** — Section 2.5 rail notes call out the policy and what to expect (last offload's Cargo (kg) ≠ raw scale ticket math; COBB row may diverge by design).
3. **Memory** — `project_railcar_mass_policy.md` saved so future-me has the rule even if skill files drift.

**The principle:** When a per-batch value diverges from primary-source math by an amount that, summed across the railcar, equals exactly the BOL aggregate, the policy is in play. Always run the railcar-balance check before flagging any rail-batch mass discrepancy as a FAIL: `if sum(all offload Cargo (kg) values in Ops Notes) == BOL_aggregate, the divergence is policy-driven, not an error.` This check would have caught the misreading immediately.

---

## Failure Category 12: Single-fix laziness — deliver the whole chain, not just what was surfaced

### Kerry K-002 — fixed two items, missed a third sharing the same root cause
**What happened:** Max flagged a contradiction in items 1.4 and 1.5 (sheet 4,618 vs Certify 4,619 mass-injectate gap on a Kerry tote batch). Agent fixed those two items and re-delivered. Item 1.7 still said "evidence value confirms reported value end-to-end" — referencing the same 4,619 = sum of per-tote nets claim that had just been refuted. Max caught it: "Fixing one thing because I find it is bush league. Child behavior. If there's an issue, it's on YOU to follow the thread ALL THE WAY DOWN."

**Root cause:** Agent treated the surfaced finding as the entire scope of the fix, instead of treating it as ONE symptom of a root-cause class that may affect multiple checklist items.

**The principle:** When ANY finding changes status or evidence content, the obligation is to map the **full dependency thread** before re-delivering, not just patch the single item that was surfaced.

**Fix applied (locked in via SKILL.md Gate 3 + lessons_learned.md, not promises):**

Every step below is the QA agent's own work. None of it is ever handed to Max or Garrett — they receive the finished, internally consistent product.

1. I identify the root cause of the flagged finding before patching anything.
2. I go back through the checklist row by row and re-read every evidence note that cites the number, filename, datapoint name, or claim behind the original finding, re-opening the underlying documents myself rather than trusting my memory of which rows reference what.
3. I audit every hit. For each match I ask: does this item's status/reasoning still hold given the corrected understanding? If not, I fix it in the same pass.
4. I audit dropped findings too — when restructuring a checklist, real findings can fall through cracks alongside spurious ones. I re-check each prior version's findings list against the new structure before re-delivering.
5. I re-run the audit script after edits.
6. Only then do I re-deliver.

This applies on first delivery, on Max-correction passes, AND on Garrett-correction passes. The standard isn't "fix what was named" — it's "deliver a product that's internally consistent." Half-fixes erode trust per-iteration faster than the original error.

This applies equally to AECN, Kerry, WODO, and Aqueous batch QA — newer skills don't get a discipline pass.

---

## Failure Category 13: Pass-status evidence that narrates a within-RP cross-batch inconsistency

### Batch 2-199 — Item 6.1 (and 9.5) Pass'd despite the evidence describing a divergence from sister batches

**What happened:** First delivery of 2-199 marked Item 6.1 ("AECN process emissions LCA CI spreadsheet present") as **Pass** with an evidence note that explicitly said: *"NOTE: sister batches 2-180/2-181 link to period-specific files ('BH 2025 LCA w Stack Emissions.xlsx' / 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx') instead of the generic Standard EFs sheet — see Item 6.4 for the resulting EF value discrepancy."* Max caught it and asked, *"If one component or datapoint has completely different evidence than comparable ones in the same reporting period how in the world would that not be a flag!?"* Item 9.5 had the same pattern around a BCU cert filename divergence (Charm-A5 vs sister batches' Charm-A4) and was also incorrectly Pass'd until the new audit rule fired.

**Root cause:** The agent treated "the file exists" as the test for Pass, while the evidence note itself documented a verifier-facing provenance inconsistency. The finding was in the narrative; the status didn't reflect it. Streak-bias + literal-reading-of-the-check trap: check item asks "spreadsheet present?" — agent answers yes — Pass — narrative-described divergence ignored. Same shape as Failure Category 1's "Confirmed without values" pattern, but for STATUS classification rather than evidence quality.

**The principle (lock this in):** When the evidence narrative describes a divergence from comparable sister batches in the same RP — different source file, different cert lot, different datapoint linkage — the status MUST be Flag at minimum. If the divergence is genuinely immaterial, remove the comparison phrase from the evidence; don't dilute a Pass with a parenthetical "but sister batches use X instead." That phrase IS the finding.

**The structural fix (audit-enforced, not promised):**

1. `checklist_lib.py` Mode 3 audit (added 2026-05-13): `WITHIN_RP_INCONSISTENCY_RE` matches phrases like `sister batches link/use/source/in the same/reference/cite`, `different from sister batch`, `differs from sister batch`, `inconsistent with sister`, `instead of the period-specific`, `vs sister batches`, `NOTE: sister batches`. Any Pass-status row whose evidence matches → audit failure with explicit guidance to either downgrade to Flag or remove the comparison phrase if the divergence is genuinely immaterial.
2. The audit is enforced at build time (`validate_rows` in `checklist_lib.build_with_validation`) AND at delivery time (`audit_checklist.py`). Two-stage gate, same shape as the negative-claim and SKILL-doc-proxy audits.
3. Pre-flight gate (FC13 added to the print-to-chat list) — every QA session has to print the FC list, so this rule sees the agent's working memory before Gate 1 begins.

**Why this is structural, not promissory:** The agent has repeatedly asserted "I'll watch for this pattern" after similar findings. Words don't prevent recurrence; an audit rule that fails the row at delivery time does. Same principle as Failure Category 10 — the citation-tag requirement, log-driven adversarial review, and pre-delivery audit script are structural because the verbal commitment isn't.

**Cross-skill application:** This audit rule lives in the shared `checklist_lib.py` and applies equally to Kerry, WODO, Aqueous, and AECN batch QA. The class of failure is "narrative-vs-status divergence on within-RP cross-batch comparisons" — oil type doesn't matter.

---

## General Principles (Distilled)

1. **Every piece of feedback represents a class.** Apply every correction universally.
2. **The checklist is a report, not a to-do list.** Every entry describes completed work with specific values.
3. **Context fatigue is real.** After ~100+ items in a long session, quality degrades. Flag it.
4. **Primary source or nothing.** Transcribed values are not verified values.
5. **Google Sheets are larger than they look.** Read the whole tab; check `rows_scanned`.
6. **The full Certify `sources` list is the document truth** (then Drive; a removal-level source not linked to a datapoint is invisible to the API, so an absence from both is still a Fail, noted for confirmation on the Sources tab). Not per-datapoint links, not summary views.
7. **Missing evidence = FAIL.** No exceptions.
8. **Certify display values are rounded.** Use the Standard EF Sheet for calculations.
9. **Track your row.** Verify cell A before reading ANY COBB value.
10. **Own the error.** Every penalty is a lesson. Every clean batch is earned.
11. **A removal accounts only for oil used in that removal.** Per-offload rail uncertainty is ±72.57 kg per leg (one outbound discrete weight). Verify N_offloads ≥ N_BOLs on the last batch of each railcar.
12. **Every finding cites a log key.** No log key, no status. Adversarial review can only challenge logged values, not hypotheticals. Confabulation has no place to live when this rule is enforced.
13. **"Blocking" requires ≥3 enumerated tooling-path attempts.** Without enumeration, the label is invalid. The path you didn't try is the one yesterday-me used.
14. **Rail-batch mass: run the railcar-balance check first.** Before flagging any rail offload's Ops Notes Cargo (kg) as wrong, verify whether `sum(all offloads in Ops Notes) == BOL_aggregate`. If yes, the per-offload divergence from raw scale ticket math is policy-driven (last-offload conservatism), not a reporting error. COBB by design carries raw scale-ticket entries and is expected to diverge from Ops Notes on the last-offload row.
15. **Status reflects the finding, narrative doesn't replace status.** When the evidence note describes a divergence from comparable sister batches in the same RP — different file, different cert lot, different datapoint linkage — the row MUST be Flag at minimum. A Pass with a parenthetical "but sister batches use X instead" is the failure mode; that phrase IS the finding. Audit Mode 3 (`WITHIN_RP_INCONSISTENCY_RE`) enforces this structurally.
16. **Read the period's VVB guidance doc before anything else, and read cell comments as well as cell values.** A number that matches no source document is at least as likely to be a documented substitution as an error, and Charm publishes its substitutions — in the reporting-period VVB guidance doc and in Ops Notes cell annotations. `data_only=True` hides the annotations. Establish what a number IS before writing a finding against it.

---

## Failure Category 14: Raising a finding against a documented method — not reading the period's VVB guidance, and reading cell values without cell comments

### Batch INJ-07-2026-W1 — six Fails raised against a published standard tare

**What happened:** The Ops Notes recorded an empty (tare) weight of 29,510 lb on three offloads (GRPX5188 offload_1, GRPX5188 offload_3, GPRX5107 offload_3). The agent read all 32 scale tickets, confirmed 29,510 lb appears on none of them, found that the filed empty ticket on those three offloads carries a different tractor or trailer than the paired full ticket, and concluded the Ops cells were transcription errors. It raised **six Fails** (2.3, 2.4, 2.5, 2.7, 5.2, 8.1), computed that two railcars' FC11 back-calc had therefore been "missed", and reported a 128.29 kg / 0.1877 tCO2e under-claim as a defect. It delivered all of this to Max.

Every one of the six was wrong. Two documents said so:

1. **"VVB Guidance July 1 - July 31"** (Drive, owner garrett.lutz@) has a section titled *Trailer Standard Empty Weight (AECN Rail Offloads)*: *"When an offload's empty scale ticket is missing, or its trailer/tractor does not match the Full ticket (a rig mismatch), the recorded empty weight cannot be used directly. In these cases a conservative per-trailer standard empty weight is substituted."* It publishes the table (KL192: n = 22, mean 29,321 lb, σ 189 lb, standard empty = 29,510 lb), states the conservatism (*"Because a heavier empty weight yields a lower net injected mass, mean + 1 sigma ensures the substitution is conservative (under-crediting)"*), and **names the exact three offloads** in a July 1–31 application list. It also explains the rig mismatch itself as *"an operational artifact of a drop-trailer delivery arrangement"* with the trailer, not the tractor, as the matching basis.
2. **The Ops Notes workbook itself.** All three substituted cells carry a cell comment: *"Standard empty weight (KL192 = mean+1SD = 29,510 lb) substituted per Trailer Standard Empty Weight methodology (rig mismatch between full/empty ticket)."*

**Root cause — two independent misses, either of which alone would have prevented this:**

- The agent never looked for a reporting-period guidance doc. Gate 1 listed six source categories and none of them was "the doc where Charm writes down its methods."
- The agent loaded the Ops Notes with `openpyxl.load_workbook(..., data_only=True)` and read cell *values*. Cell comments are not values. The explanation was in the workbook it had already downloaded.

The 128.29 kg figure was arithmetically correct and its sign was correct; what was wrong was calling intended conservatism a defect. Being right about the arithmetic while wrong about the meaning still produces a false accusation.

**The structural fixes (locked into SKILL.md, not promises):**

1. **Gate 1 step 0** — read the reporting-period VVB guidance doc in full BEFORE any other source, record it under `vvb_guidance` with `live_source_url` and verbatim quotes. If none exists, record the search.
2. **Gate 1 step 4** — Ops Notes reads must dump `cell.comment.text` for the offload table, which requires loading the workbook **without** `data_only=True`.
3. **Gate 1 step 1** — a tractor/trailer mismatch is documented as the *trigger* for a standard-tare substitution, not automatically a finding. Check guidance + cell annotation before classifying it.

**The principle:** before writing a finding against a number that doesn't tie, establish what the number *is*. A value that matches no source document is at least as likely to be a documented substitution as an error — and Charm publishes its substitutions. FC11 taught this for the railcar last-offload back-calc; this is the same lesson with a different method. When a value diverges from primary-source math, first ask "is there a published method that produces exactly this?" and go read it.
