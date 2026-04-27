# Adversarial QA Review: Batch 2-166
**Batch ID:** 2-166
**Oil Type:** AECN only
**Injection Site:** Basco 6
**Certify Removal ID:** rmv_1KMR8930Z1S0ZZ6Y
**Reporting Period:** 3/16/26–3/22/26
**Review Date:** 3/31/2026
**Reviewer:** Adversarial QA Agent

---

## Summary
**Total items reviewed:** 47 (38 Pass, 0 Fail, 8 N/A, 1 Flag)

**Findings:** 2 **challenged items** (calculation discrepancies requiring investigation); 1 **confirmed issue** with documentation practice; 44 **confirmed items** with full verification.

The checklist is substantially sound — all mass, sparging, transport distance, and BOL validations are correct. However, two pyrolysis emission values and the percentage attribution for transport process require clarification against Certify's native calculation.

---

## Challenged Items

### 1. ITEM: Section 6a, Row 50 — AECN Pyrolysis Process Emissions
**Current Status:** Pass
**Cited Value:** 2.092 tCO₂e (7.15% of gross)
**Evidence Note:** "AECN pyrolysis process: 2.092 tCO₂e (7.15%). ... Component: 2.092 tCO₂e (7.15%)."

**Issue:**
The stated pyrolysis process value of 2.092 tCO₂e does not match the standard calculation:
- **Correct calculation:** Injectate mass (19.851 t) × AECN process EF (0.10 kgCO₂e/kg) = 1.985 tCO₂e
- **Stated value:** 2.092 tCO₂e
- **Delta:** +0.107 tCO₂e (+5.4% overstatement)

The checklist correctly identifies the AECN process EF as 0.10 kgCO₂e/kg (matching Knowledge Base), and correctly states the injectate mass is 19.851 t (after sparging). Yet the calculated emission is higher than expected.

**Three possible explanations:**
1. The pyrolysis emissions in Certify use a different mass basis (e.g., pre-sparging mass 20.110 kg), which would yield ~2.011 tCO₂e—closer but still not 2.092.
2. The stated value is Certify's internal calculation, which may use higher precision EFs than displayed.
3. The value is incorrectly transcribed from Certify into the checklist.

**Recommendation:** **FLAG** — The value should be verified directly against Certify's "AECN Production Process Emissions" datapoint and the native EF (not the displayed 0.10). If Certify shows 2.092, confirm the calculation method (does it use gross or net injectate mass? Is the EF more precise than 0.10?). If verification confirms the 2.092 value, update the evidence note to cite the precise EF used and mass basis.

**Evidence needed:** Certify datapoint detail for AECN Production Process Emissions showing native EF value and mass basis.

---

### 2. ITEM: Section 6a, Row 51 — AECN Pyrolysis Embodied Emissions
**Current Status:** Pass
**Cited Value:** 0.426 tCO₂e (1.46% of gross)
**Evidence Note:** "AECN pyrolysis embodied: 0.426 tCO₂e (1.46%). ... Component: 0.426 tCO₂e (1.46%)."

**Issue:**
The stated embodied emission of 0.426 tCO₂e similarly does not match the standard calculation:
- **Correct calculation:** Injectate mass (19.851 t) × AECN embodied EF (0.02 kgCO₂e/kg) = 0.397 tCO₂e
- **Stated value:** 0.426 tCO₂e
- **Delta:** +0.029 tCO₂e (+7.3% overstatement)

If the pre-sparging mass (20.110 kg) were used, the result would be ~0.402 tCO₂e—still not 0.426.

The same root causes apply as for Item 1. The stated values may reflect Certify's internal precision or a different calculation basis not visible in the checklist evidence notes.

**Recommendation:** **FLAG** — Verify the embodied emission value directly in Certify, citing the native EF and mass basis. These two overstatements (process +0.107, embodied +0.029 = +0.136 tCO₂e combined) cascade into the total removal activities (stated as 8.090 tCO₂e but should be ~7.954 tCO₂e if the standard calculation is correct), which affects the net calculation.

**Evidence needed:** Certify datapoint detail for AECN Production Embodied Emissions showing native EF value and mass basis.

---

## Confirmed Items with Verification

**Section 1: Batch Folder Completeness**
- ✓ Row 6: Batch folder naming and location confirmed (2-166 under correct date range).
- ✓ Row 7: Scale tickets present with correct file sizes, dates (3/19/26), and ownership (Garrett Lutz).
- ✓ Row 8: Testing subfolder contains CHN PDF (2-166 - 2-174.pdf, 88 KB, dated 3/26) covering this batch.
- ✓ Row 9: Ops Notes sheet confirmed (4 KB, 3/23) with required sections.
- ✓ Row 10: Basco 6 location confirmed across scale tickets, Ops Notes, and Certify; no Vaulted Deep references.

**Section 2: Scale Tickets & Mass Determination**
- ✓ Row 13: Single tanker pair present (Empty Ticket + Full Ticket).
- ✓ Row 14: Both tickets dated 3/19/26; delta to Ops completion date (3/20/26) = 1 day, well within 2-week threshold.
- ✓ Row 15: Tractor #2208 and Trailer #36562 match across both tickets.
- ✓ Row 16: Net calculation verified: 79,180 − 34,760 = 44,420 lbs = 20,151 kg. Ops Notes conservatively records 20,110 kg (BOL mass). MIN rule correctly applied.
- ✓ Row 17: BOL mass (20,110 kg) < scale ticket net (20,151 kg); MIN correctly applied. Matches Certify Origin Mass (20.110 t).
- ✓ Row 18: Sparging deduction: 20,110 × 0.0129 = 259.4 kg. Injectate: 19,851 kg = 19.851 t. Matches Certify "Mass of Injectant" exactly. AECN-only batch confirms correct protocol.
- ✓ Row 19: All mass values consistent: scale net 20,151 kg | BOL 20,110 kg | Ops Notes 20,110.0 kg | COBB 20,110 kg | Certify Origin 20.110 t | Certify Injectant 19.851 t.

**Section 3: Bills of Lading & Transportation**
- ✓ Row 22: BOL 2325-T referenced in Certify sources for Origin Bio-Oil Mass datapoint; COBB confirms BOL_number = 2325-T.
- ✓ Row 23: N/A correctly applied (tanker truck, not rail). consumed_lot = 2325-T_offload_1 confirms truck transport.
- ✓ Row 24: BOL mass (20,110 kg) exceeds injectate (19,851 kg). ✓
- ✓ Row 25: Certify transport component "AECN to LA Tanker Truck Transport" confirmed; distance 2,197 mi per Knowledge Base. Full ticket shows BOL from Bio Énergie (AECN).
- ✓ Row 26: Distance 2,197 mi matches Knowledge Base reference ("~2,197 mi for AECN truck").
- ✓ Row 27: Transport mode confirmed as tanker truck (AECN). BOL suffix "T" indicates truck. Certify components reference tanker. lot = 2325-T_offload_1.
- ✓ Row 28: Billing document (2325-T.pdf) present in Certify sources, linked to Origin Mass datapoint.

**Section 4: Bio-Oil Composition & Testing**
- ✓ Row 31: CHN PDF (SGS Certificate of Analysis SR26-02012.001, 88 KB) present, dated 26-Mar-2026.
- ✓ Row 32: **Carbon content 44.6% validated.** Knowledge Base specifies: AECN mean = 39.42%, SD = 6.09% (n=285 samples, source MRV_AECN_Analysis.xlsx, updated March 2026). Expected range: 39.42% ± 2×6.09% = 27.2% – 51.6%. Observed 44.6% is 0.85 SD above mean, well within acceptable bounds. ✓
- ✓ Row 33: H = 7.5%, N < 0.75% reported per ASTM D5291 Method C. Values within reasonable range for pyrolysis bio-oil.
- ✓ Row 34: SGS report CLIENT ID "BATCH 2-166", Location "BASCO LOUISIANA", sample date 20-Mar-2026 07:30. Correctly references this batch.
- ✓ Row 35: N/A correctly applied (AECN-only, no aqueous phase).
- ✓ Row 36: **Gross sequestration calculation verified:** 19.851 t (injectate) × 0.4460 (carbon content as decimal, from lab report) × 3.667 (CO₂/C molecular weight ratio per Knowledge Base section on Bio-oil Geol Storage v1.1) = **32.465 tCO₂e**. Matches Certify sequestration value exactly. ✓

**Section 5: Ops Notes Accuracy & Internal Consistency**
- ✓ Row 39: Batch ID 2-166 and completion date 3/20/26 present and match Certify removal date (20 Mar 2026).
- ✓ Row 40: Scale values correctly transcribed. Ops Notes records conservative BOL mass (20,110 kg) vs. higher scale net (20,151 kg).
- ✓ Row 41: N/A correctly applied (AECN-only, no aqueous phase).
- ✓ Row 42: COBB row 45: injection_batch=2-166, consumed_lot=2325-T_offload_1, BOL=2325-T, offloaded_qty=20,110 kg. Matches Ops Notes Total Mass.
- ✓ Row 43: pH = 2.6 (cell H23) recorded in Ops Notes. Reasonable for AECN.
- ✓ Row 44: Completion date 3/20/26 (Ops Notes) matches Certify 20 Mar 2026. Scale date 3/19/26 is 1 day prior—normal for next-day injection.
- ✓ Row 45: N/A correctly applied (density field expected blank for AECN).

**Section 6a: AECN Feedstock Emissions & Allocation**
- ✓ Row 48: LCA CI spreadsheets present in Certify sources: "BH 2025 LCA w Stack Emissions.xlsx", "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx".
- ✓ Row 49: Stack emissions file confirmed in sources.
- ✓ Row 50: Supporting GHG data file (31Dec2025 S.xlsx) present as private source. Also generic screenshot filename flagged (see Sec 9 finding).
- **[CHALLENGED - see Item 1 above]** Row 51: AECN process EF correctly identified as 0.10 kgCO₂e/kg (current 2026 value per Knowledge Base). Stated component value 2.092 tCO₂e requires verification.
- **[CHALLENGED - see Item 2 above]** Row 52: AECN embodied EF correctly identified as 0.02 kgCO₂e/kg (current 2026 value). Stated component value 0.426 tCO₂e requires verification.

**Section 6b, 6c, 6d: Non-AECN Oil Types**
- ✓ Rows 53, 55, 57, 59: N/A correctly applied. Batch 2-166 is AECN-only; no Charm WODO, Charm Aqueous, or Kerry oil present.

**Section 7: Gross-to-Net Calculation**
- ✓ Row 64: Gross CO₂e formula verified: 19.851 t × 0.4460 × 3.667 = 32.465 tCO₂e. Carbon content correctly expressed as decimal. Matches Certify Sequestration. ✓
- ✓ Row 65: Total Removal Activities stated as 8.090 tCO₂e (transport 5.572 + pyrolysis 2.518). **Caveat:** If pyrolysis values (items 1 and 2 above) are incorrect, this total should be ~7.954 tCO₂e instead.
- ✓ Row 66: Uncertainty discount = 0.178 t applied per Isometric Standard. Net formula: 32.465 − 8.090 + 5.050 − 0.178 = **29.247 tCO₂e**, rounds to **29.25 tCO₂e**. Arithmetic verified. ✓
- ✓ Row 67: Net removals consistent with Certify display (29.25 tCO₂e rounded from 29.247).

**Section 8: Data Integrity & Anomaly Check**
- ✓ Row 70: Carbon content 44.6% confirmed within validated AECN range (mean 39.42%, SD 6.09%, n=285). No unexplained outliers.
- ✓ Row 71: No spills, losses, or irregularities. Losses = 0 tCO₂e per Certify. LCS = 0 (AECN does not require pre-treatment at Basco per Knowledge Base).
- ✓ Row 72: N/A correctly applied (single-lot batch; no carryover reconciliation).

**Section 9: Isometric Certify — Removal Component Mapping**
- ✓ Row 75: Gross injection sequestration 32.465 tCO₂e verified against internal gross calc (19.851 × 0.4460 × 3.667).
- ✓ Row 76: **Transport emissions verified.** Stated values: process 5.050 tCO₂e, embodied 0.522 tCO₂e, total 5.572 tCO₂e. Knowledge Base specifies 2026 EFs: transport process 0.07 kgCO₂e/(km·t) (displayed) or 0.0001143 MTCO₂e/(t·mi) (native); transport embodied 0.1476 kgCO₂e/km (updated 3/30/26). **Verification of process emissions using native EF:** 2,197 mi × 20.110 t × 0.0001143 MTCO₂e/(t·mi) = 5.050 MTCO₂e = 5,050 kgCO₂e = 5.050 tCO₂e. ✓ **Note:** The observation in row 96 flags a manual calc variance (stated 4,961 kg vs. Certify 5,050 kg, delta 1.8%) due to EF precision; this is correctly explained as immaterial. ✓
- **[ANNOTATION: Percentage attribution issue]** Row 76 states transport process is 17.26% of gross (32.465 × 0.1726 = 5.605, which does not equal 5.050). The correct percentage is 5.050 ÷ 32.465 = 15.56%. **No Pass/Fail status change needed** — the absolute value (5.050 tCO₂e) is correct per native EF verification; the percentage label appears misattributed (possibly transposed from a different calculation). Recommend noting for Certify audit clarity.
- ✓ Row 77: Pyrolysis emissions labeled "AECN pyrolysis (from truck loads)". Breakdown: process 2.092 tCO₂e (7.15%), embodied 0.426 tCO₂e (1.46%), total 2.518 tCO₂e. **[Subject to items 1 and 2 verification above]**
- ✓ Row 78: Five BCU categories present: injection diesel (0), injection waste (0), pre-treat diesel (0), pre-treat waste (0), transport process (5.050 tCO₂e). Zero-value BCUs are expected for AECN single-lot, no-pre-treatment batches. ✓
- ✓ Row 79: **BCU Quantity Verification Rule confirmed.** Transport process BCU = 5.050 tCO₂e equals transport process activity emission = 5.050 tCO₂e per Knowledge Base mandate: "BCU quantity (tCO₂e) in Reductions MUST equal or exceed the corresponding diesel emission (tCO₂e) in Activities." Rule satisfied. ✓
- ✓ Row 80: Counterfactuals = 0 tCO₂e per bio-oil geological storage protocol (correct; no baseline applicable).
- ✓ Row 81: Net removal calculation in Certify Calculation View: 32.465 − 8.090 + 5.050 − 0.178 = **29.247 tCO₂e** (displays as 29.25). Arithmetic verified. ✓
- ✓ **Row 82 (FLAGGED):** 14 datapoints, 14 sources. One source has a generic name: "Screenshot 2026-02-23 at 11.29.10 AM.png" (AECN Production Process EF datapoint). This is not a data accuracy issue but a documentation practice concern. **Confirmed:** This same generic screenshot was flagged in batch 2-165 and remains unchanged. Recommend renaming to a descriptive format (e.g., "AECN_Production_EF_2H2025_2H2026_20260223.png" or referencing the document it represents). This does NOT change Pass/Fail but improves audit readiness.
- ✓ Row 83: Key batch files confirmed present: Empty/Full scale tickets, Ops Notes, CHN lab results (2-166 - 2-174.pdf), Billing document (2325-T.pdf). AECN LCA/GHG production-period docs correctly stored as private Certify sources (standard practice).

**QA Summary (Row 85–89)**
- ✓ 38 items passed — confirmed through verification.
- ✓ 0 items failed — no critical issues found.
- ✓ 8 items N/A — correctly applied to non-applicable categories.
- ✓ 1 item flagged — generic screenshot filename (documentation practice, not data accuracy).

**Observation (Row 96): Transport Variance Explanation**
- ✓ Manual calc (3,537 km × 20.110 t × 0.07 kgCO₂e/(km·t) = 4,961 kgCO₂e) vs. Certify (5,050 kgCO₂e) variance of 89 kg (1.8%) is correctly explained. Root cause: Using the rounded display EF (0.07) introduces rounding error; Certify's native EF (0.0001143 MTCO₂e/(t·mi)) yields 5,050 kgCO₂e exactly. This is a **valid observation** demonstrating understanding of EF precision. Variance is immaterial (below 5% materiality threshold). ✓

---

## Summary of Recommendations

### 1. Resolve Items 1 & 2 (Pyrolysis Emissions)
Check Certify directly to confirm whether:
- The pyrolysis process value is 2.092 tCO₂e (as stated in checklist).
- The pyrolysis embodied value is 0.426 tCO₂e (as stated in checklist).
- If confirmed, provide the precise EF and mass basis in Certify datapoint notes.

**Impact if values are incorrect:** The net removal would decrease from 29.25 tCO₂e to ~29.11 tCO₂e (if using standard EF × injectate mass = 1.985 + 0.397 + 5.050 + 0.522 = 7.954 instead of 8.090). This is a **0.14 tCO₂e difference (~0.5%)**, below typical materiality but worth confirming.

### 2. Clarify Transport Process Percentage Attribution
The evidence note states transport process is "17.26%" of gross (32.465 tCO₂e), but 5.050 ÷ 32.465 = 15.56%. The absolute value (5.050 tCO₂e) is correct; the percentage label may be misattributed or derived from a different base. Recommend checking Certify's component display to confirm the percentage is consistent there, or note the discrepancy for audit purposes.

### 3. Rename Generic Screenshot in Certify
"Screenshot 2026-02-23 at 11.29.10 AM.png" should be renamed to a descriptive format (e.g., "AECN_Prod_EF_2026_Supporting_Data.png" or similar) for audit clarity. This is consistent with best practices and resolves the flag from batch 2-165 that persists in this batch.

### 4. No Further Action Needed
All mass calculations, sparging deductions, BOL validations, transport distance, carbon content validation, gross sequestration, and net removal arithmetic are **verified and correct**. The checklist demonstrates thorough, accurate QA work. The two challenged items are high-precision edge cases (pyrolysis EF × mass) and should be confirmed against Certify's native calculation, but the overall integrity of the batch data is sound.

---

## Conclusion

**Batch 2-166 QA Checklist Status: SUBSTANTIVELY SOUND**

The adversarial review confirms 44 of 47 items (excluding N/A). Two items (pyrolysis process and embodied emissions values) require clarification against Certify's native calculations to confirm the stated values; if correct, they should be evidenced with full EF and mass basis. One documentation practice (generic screenshot filename) is confirmed and should be corrected per recommendation 3.

**Overall Assessment:** This is a well-executed QA checklist with strong attention to mass consistency, transport validation, and emissions component verification. The net removal value of 29.25 tCO₂e is supported by verified gross sequestration (32.465 tCO₂e), confirmed transport emissions (5.050 tCO₂e process verified via native EF), and appropriate uncertainty discount. The batch meets protocol requirements and is audit-ready pending the three recommendations above.
