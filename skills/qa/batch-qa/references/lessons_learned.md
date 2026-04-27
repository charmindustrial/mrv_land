# Injection Batch QA — Lessons Learned

This document captures real failure patterns from batch QA sessions spanning batches 2-160 through 2-178. Every entry represents something that actually went wrong, caused rework, and eroded trust. Read this at the start of every QA session.

---

## Failure Category 1: Not Reading Primary Sources

### Batch 2-178 — Sources Tab Not Checked
**What happened:** The agent checked only 12 removal-level sources from the Datapoints tab and declared 3 AECN LCA documents missing — when all 3 were present on the Sources tab (16 total sources, 4 at component level). Max caught this.

**Root cause:** The agent didn't open the Sources tab, which is the single source of truth for document presence. The Datapoints tab only shows sources linked to specific datapoints and misses component-level documents.

**Fix applied:** SOURCES TAB FIRST RULE in Gate 1. The source-read log now requires `"certify_sources_tab_total"` with a complete enumeration of ALL source filenames. Gate 1 cannot be completed without this field.

**The principle:** Any time you need to determine whether a document exists in Certify, check the Sources tab. Not the Datapoints tab. Not a summary view. The Sources tab.

### Batch 2-178 — Wrong COBB Row
**What happened:** The agent read values from row 27 (batch 2-170's row) instead of row 55 (batch 2-178's row), producing 2 false FAILs that Max had to catch. The agent navigated to the COBB tracker and read the first plausible-looking row without verifying the batch ID.

**Root cause:** The COBB tracker has far more rows than fit in the initial viewport. The agent assumed the visible rows were all that existed and read from the wrong batch.

**Fix applied:** ROW VERIFICATION GATE — before extracting ANY value from a COBB row, read cell A and confirm it contains the target batch ID. The source-read log now requires `"cobb_row_id_verified": true` and `"cobb_cell_A_value"` matching the target batch.

**The principle:** Large Google Sheets are deceptive. Never trust what's visible on screen. Navigate deliberately and verify you're in the right place before reading.

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

## General Principles (Distilled)

1. **Every piece of feedback represents a class.** Apply every correction universally.
2. **The checklist is a report, not a to-do list.** Every entry describes completed work with specific values.
3. **Context fatigue is real.** After ~100+ items in a long session, quality degrades. Flag it.
4. **Primary source or nothing.** Transcribed values are not verified values.
5. **Google Sheets are larger than they look.** Navigate beyond the viewport.
6. **The Sources tab is the document truth.** Not Datapoints, not summary views.
7. **Missing evidence = FAIL.** No exceptions.
8. **Certify display values are rounded.** Use the Standard EF Sheet for calculations.
9. **Track your row.** Verify cell A before reading ANY COBB value.
10. **Own the error.** Every penalty is a lesson. Every clean batch is earned.
