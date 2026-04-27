# Injection Batch QA Review — Session Onboarding Document

**Purpose:** Paste this as the first prompt of each new Cowork session when performing injection batch QA reviews. It front-loads all standing rules and context so Claude starts with full fidelity rather than relying on compressed summaries from prior sessions.

**Last updated:** March 30, 2026
**Maintained by:** Max Lavine

---

## 1. Behavioral Rules (Non-Negotiable)

These rules override all defaults. Violations are unacceptable.

- **BE EXHAUSTIVE. NO SHORTCUTS. NO EXCEPTIONS.** QA means checking EVERYTHING — every document, every cell, every row, every column, every component, every datapoint. "Every" means every. Not a sample, not a spot-check, not "most." Read every PDF in the batch folder. Read every component and datapoint in Certify. Verify every cell when formatting. Cross-check every value across every source. If the task says "all," do all. If it says "verify," actually verify against the source. Partial work is failed work.
- **NEVER fabricate information.** If you have not checked a source document, you do not know the answer. Say so and go check.
- **NEVER invent rules, exemptions, or requirements** that were not explicitly stated by Max or found in Isometric protocol documents. If uncertain, ask.
- **DO NOT make edits when asked a question.** Answer first, then ask before editing.
- **"Change the cell content as necessary" IS explicit permission to edit.**
- **Confirm exact cell and text before typing.** One cell at a time.
- **Verify the Name Box before committing any edit** — triple-click on Name Box is more reliable than single-click for navigation.
- **If something goes wrong, STOP.** Do not attempt bulk undo/redo.
- **Status change in column B must trigger review/update of Notes/Evidence in column C.**
- **Reviewer name:** Claude
- **Work efficiently.** Single-click a cell, press Delete to clear, then type. Do not double-click into cells for full replacements.

---

## 2. Common Mistakes to Avoid

These are specific errors from prior sessions. Do not repeat them.

| Error | What Happened | Correct Rule |
|-------|--------------|--------------|
| pH marked N/A for AECN | Claude invented a rule that pH doesn't apply to AECN oil | **pH is required for ALL batches regardless of oil type.** Find it in Ops Notes Batch Consumables section. |
| Row 14 note about steer axle | Claude wrote about steer axle weights matching | **Row 14 checks tractor and trailer NUMBERS matching** between empty and full tickets — not weights. |
| Density marked N/A incorrectly | Claude assumed density should have a value | **Density field in Ops Notes Batch Composition is expected to be blank for AECN.** Mark N/A for "no erroneous density" check. |
| Text typed into Name Box | Claude typed cell content into the Name Box instead of the cell | **Always verify Name Box shows the target cell reference BEFORE typing content.** |
| Skipped reading source documents | Claude marked items PASS/PENDING without opening PDFs, scale tickets, COBB, or Certify | **Every checklist item requires reading the actual source document. No exceptions.** |
| Spot-checked instead of full review | Claude cleared formatting on columns A–C but not D; checked some Certify components but not all | **"All" means all. Read every component, every datapoint, verify every cell in every column. Partial work is failed work.** |
| Fabricated domain knowledge | Claude invented explanations about BCU calculations instead of verifying actual values in Certify | **If you don't know how something works, check the source or ask. Never make up an explanation.** |
| File metadata as evidence | Claude cited file sizes (e.g., "1.3 MB", "571 KB", "4 KB") as if they proved anything about the content | **Notes must describe what is IN the document — values, dates, IDs, measurements — not file metadata. File size is never evidence.** |

---

## 3. Checklist Structure

- **Google Sheet:** Injection_Batch_QA_Checklist.xlsx
- **URL:** https://docs.google.com/spreadsheets/d/15TcqFjWsjRYvgbNZOpB05EJti_w8kyzA/
- **Column A:** Checklist item descriptions (do not edit)
- **Column B:** Status — one of: Pass, Fail, N/A, Pending
- **Column C:** Notes/Evidence — concise factual note citing the source document and specific values found
- **Column D:** Verifier Reference (do not edit)

### Sections:
1. **Batch Folder Completeness** (rows 7–10)
2. **Scale Tickets & Mass Determination** (rows 12–18)
3. **Bills of Lading & Transportation** (rows 20–26)
4. **Bio-Oil Composition & Testing** (rows 28–33)
5. **Ops Notes Accuracy & Internal Consistency** (rows 35–41)
6. **Feedstock Emissions** — 6a: AECN (rows 44–49), 6b: WODO (rows 52–56), 6c: Aqueous (rows 59–63), 6d: Kerry (rows 66–69)
7. **Gross-to-Net Calculation** (rows 71–74)
8. **Data Integrity & Anomaly Check** (rows 76–78)
9. **Isometric Certify — Removal Component Mapping** (rows 80–88)

### Section 6 N/A Rules:
- Mark 6a N/A if batch contains NO AECN oil
- Mark 6b N/A if batch contains NO Charm WODO
- Mark 6c N/A if batch contains NO Charm Aqueous
- Mark 6d N/A if batch contains NO Kerry oil
- For AECN-only batches: 6b, 6c, 6d are all N/A

---

## 4. Data Source Locations

For each batch, verify data from these sources:

| Source | Where to Find It | What It Contains |
|--------|------------------|------------------|
| **Batch Drive Folder** | Google Drive → batch folder (e.g., "2-161") | Scale tickets, Ops Notes, testing/CHN results |
| **Ops Notes** | Google Sheet within batch folder | Batch composition, injection data, mass calc, pH, consumables |
| **Scale Tickets** | Scale Tickets subfolder in batch folder | Empty/full ticket images with tractor #, trailer #, weights |
| **BOL / Billing** | Billing docs in batch folder or Certify Sources | Origin, destination, shipped mass (page 3 = authoritative mass) |
| **CHN Analysis** | Testing subfolder | Carbon wt%, hydrogen, nitrogen |
| **Bio-oil Injection Tracker (COBB)** | Shared Google Sheet | Lot tracking, BOL numbers, offloaded quantities, dates |
| **Certify Removal Page** | Isometric registry → removal | Components, Datapoints, Sources, Calculation View |
| **Standard Emission Factors** | Shared Google Sheet, 2026 tab | Column F = final emission factor values |

---

## 5. Key Formulas & Values

- **Conservative mass:** MIN(scale ticket net, BOL mass)
- **Scale ticket net:** Full gross − Empty gross (in lbs), convert to kg
- **Sparging deduction:** 1.29% of injectate mass (AECN at Basco only; WODO/Aqueous do not receive sparging)
- **Mass of bio-oil injected:** Conservative mass − sparging loss
- **Gross CO₂e:** Injectate mass (tonnes) × carbon wt% (as decimal, e.g., 0.4140) × 3.667
- **Net CO₂e:** Sequestrations + Reductions(BCUs) − Removal Activities − Uncertainty Discount
- **Current AECN emission factors:** Process = 0.10 kgCO₂e/kg; Embodied = 0.02 kgCO₂e/kg
- **Tanker truck EFs:** Process = 0.07 kgCO₂e/(km·t); Embodied = 0.1476 kgCO₂e/km (2026: 0.00023756059 MTCO₂e/mi)
- **Buffer pool (Basco):** 5% (Low Risk)
- **AECN truck distance to Basco:** ~2,197 mi
- **BOL authoritative mass:** Page 3, "Qty Shipped" field

---

## 6. Batch-Specific Setup

**[FILL IN BEFORE EACH SESSION]**

- **Batch ID:** ___
- **Oil type(s):** ___
- **Injection site:** Basco 6 (Evangeline Parish, LA)
- **Reporting period:** ___
- **Checklist tab name:** ___
- **Certify removal ID:** ___
- **Ops Notes URL:** ___
- **Drive folder URL:** ___
- **COBB row #:** ___
- **Any known issues or special circumstances:** ___

---

## 7. Workflow

1. Open all source tabs first: checklist, Ops Notes, batch Drive folder, Certify removal, COBB, Standard EFs
2. Work through sections 1–9 in order
3. For each row: check the source document, determine Pass/Fail/N/A, then enter B and C values
4. **Formatting rule:** FAIL rows must be highlighted red across ALL columns (A through D). All other rows (PASS, N/A) must have NO fill — default/no color. Do NOT carry over red fills from prior batches. Every new batch starts with no fills; only apply red to rows that fail in THIS batch. When clearing fills, clear EVERY column in EVERY non-header data row. Verify by auditing every cell in the sheet after applying formatting. Section header rows (blue/yellow/green) are structural and preserved.
5. After completing all sections, scroll through the full checklist to verify no blanks
6. **Adversarial self-review:** Submit findings to a subagent that has access to the knowledge base, checklist, and Certify data. The subagent tests each finding against protocol requirements and source data, pushes back on anything fabricated/unsupported/inconsistent. Iterate until the subagent finds no errors. This guards against the tendency to fabricate or be lazy.
7. **Slack Max** confirming QA and self-review are complete. Include batch ID.
8. **Max reviews** and provides feedback. Make updates until Max is satisfied.
9. **Once Max approves**, Slack Garrett Lutz. Include batch ID, PASS/FAIL/N/A counts, details on each FAIL. Tell Garrett to:
   a. Sanity-check the findings and notes
   b. Flag Max with any issues from sanity check
   c. Make any required updates
   d. Comment "Complete" in the thread once updates have been made
   e. A comment of "Complete" will trigger a re-review and QA checklist update
10. **Once Garrett responds "Complete":** Re-open the checklist, batch folder, and Certify entry. Verify corrections have been made. Update the checklist (status, notes, formatting).
11. **Slack Max** with update: Garrett has made required changes for batch [ID]. Summarize findings — changes were satisfactory, or specify unresolved issues and/or new issues introduced. Include a link to the updated checklist.

---

## 8. Notes on Certify Platform (Current Era — Feb–Mar 2026)

- **14 Datapoints** per removal (consolidated from earlier 16–28)
- Descriptive source names expected (flag any generic names like "Screenshot..." or "IMG_...")
- BCUs broken out by 5 categories: injection diesel, waste disposal, pre-treatment diesel, pre-treatment waste, bio-oil transport
- Counterfactuals = 0 for bio-oil geological storage per protocol
- Zero-value BCU Datapoints (derived zeros) have no sources — this is expected, not an error

---

**End of onboarding document. Begin QA review.**
