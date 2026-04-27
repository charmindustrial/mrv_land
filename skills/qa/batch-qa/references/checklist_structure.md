# AECN Injection Batch QA Checklist — Item-by-Item Reference

This document provides the complete specification for every checklist item in an AECN-only batch QA: what to check, which primary source to open, what values to extract, expected ranges, and common failure modes.

**Scope:** AECN oil batches only. No WODO, Aqueous, or Kerry items.

---

## Section 1: Batch Folder Completeness

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 1.1 | Batch folder exists with correct naming (e.g., 2-XXX) | Google Drive | Folder named with batch ID | Naming inconsistent |
| 1.2 | Scale Tickets subfolder present and populated | Drive > batch folder | Subfolder with full+empty PDFs | Subfolder empty or missing one ticket |
| 1.3 | Testing subfolder present with all required lab results | Drive > batch folder | CHN/CoA PDF(s) from SGS | Wrong batch's lab results |
| 1.4 | Ops Notes spreadsheet present and complete | Drive > batch folder | Google Sheet with all sections filled | Ops Notes partially complete |
| 1.5 | Injection site confirmed as Basco 6 — no references to Vaulted | BOLs, Ops Notes, Certify | All docs say Basco/Evangeline Parish | Legacy Vaulted references not cleaned up |

**Verifier reference:** VR Appendix 1

**Document location rule applies:** Documents may be in Drive OR Certify Sources. Only FAIL if absent from BOTH.

---

## Section 2: Scale Tickets & Mass Determination

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 2.1 | Empty and full scale ticket images present for each truckload | Certify Sources or Drive Scale Tickets subfolder | Both PDFs readable with clear values | Only one ticket present, or image unreadable |
| 2.2 | Dates within 2 weeks of injection | Scale ticket PDFs | Date on tickets within 14 days of Ops Notes injection date | Stale tickets from prior shipment |
| 2.3 | Tractor and trailer numbers match between empty and full tickets | Scale ticket PDFs | Same tractor # and trailer # on both | Mismatch = different vehicle weighed = FAIL |
| 2.4 | Net mass correctly calculated in Ops Notes | Ops Notes vs scale tickets | Full gross - Empty gross (lbs) matches Ops Notes | Transcription error, wrong conversion |
| 2.5 | Injectate mass uses conservative value: MIN(scale ticket net, BOL mass) | Ops Notes, BOL | Smaller of the two used | Wrong mass selected |
| 2.6 | 1.29% sparging deduction applied | Ops Notes | Sparging loss = injectate x 0.0129 | Wrong sparging rate, or sparging not applied |
| 2.7 | All mass values consistent across scale tickets, Ops Notes, Certify | All sources | Values agree within rounding | Mass in Certify doesn't match Ops Notes |

**Verifier references:** VR Sec 5.1, GHG Stmt Sec C

**MANDATORY VERIFICATION SUB-TASK (2.1-2.3):** Open BOTH scale ticket PDFs. Read tractor #, trailer #, gross/tare, date from the image. Do not rely on Ops Notes alone.

**Key formula:** Net mass (kg) = (Full gross lbs - Empty gross lbs) / 2.20462

**AECN-specific notes:**
- Sparging is standard for AECN at Basco (1.29% deduction)
- Density field in Ops Notes Batch Composition is expected to be blank for AECN
- Row 14 in the template checks tractor and trailer NUMBERS matching — not weights. This has been confused before.

---

## Section 3: Bills of Lading & Transportation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 3.1 | Truck BOL(s) present for each shipment | Drive or Certify Sources | At least 1 BOL per truck shipment | BOL missing from both Drive and Certify |
| 3.2 | If rail delivery: truck BOLs from AECN present (destination = SOPOR railyard) | Drive or Certify Sources | 3 BOLs per railcar | Wrong destination, missing BOLs |
| 3.3 | BOL mass matches or exceeds reported injectate mass | BOL page 3 "Qty Shipped" | BOL mass >= injectate mass | BOL mass < reported injectate |
| 3.4 | Origin and destination correct on BOL | BOL | AECN Quebec -> Basco, or AECN -> SOPOR -> Basco (rail) | Wrong origin/destination |
| 3.5 | Transportation distance consistent with known AECN route | Certify Datapoints | AECN truck ~2,197mi; AECN rail ~2,199mi | Distance significantly off |
| 3.6 | Transport mode = tanker truck or railcar (AECN modes) | Certify Datapoints | Tanker truck (direct) or railcar (via SOPOR) | Wrong mode recorded |
| 3.7 | Billing documents present and consistent with BOL | Drive or Certify Sources | Billing matches BOL shipment details | Billing for different shipment |

**Verifier references:** VR Appendix 1, VR Sec 3.5, PDD Sec A, Transport Emissions Acctg v1.1

**BOL authoritative mass:** Page 3, "Qty Shipped" field.

**AECN transport modes:**
- Direct truck: Tanker truck, AECN Quebec -> Basco, ~2,197 mi, 1 BOL
- Rail: Tanker truck to SOPOR railyard (3 BOLs), rail to Opelousas, tanker truck to Basco, ~2,199 mi total

---

## Section 4: Bio-Oil Composition & Testing

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 4.1 | CHN analysis PDF(s) present in Testing subfolder | Drive > Testing | SGS Certificate of Analysis PDF | Wrong batch's lab report |
| 4.2 | Carbon content within expected AECN range | CHN PDF | Mean = 39.42%, SD = 6.09% (n=285). Flag if outside ~27.2%-51.6% | Outlier not flagged |
| 4.3 | Hydrogen and nitrogen values reported and reasonable | CHN PDF | Values present and within normal ranges | Values missing |
| 4.4 | Lab report references correct batch/sample ID | CHN PDF | Batch ID on certificate matches QA batch | Report for different batch |
| 4.5 | pH/conductivity (aqueous phase) | N/A for AECN | **Mark N/A** — AECN is not aqueous phase | Agent incorrectly checking pH here (pH is in Ops Notes, Section 5.5) |

**Verifier references:** VR Appendix 1, Biomass Feedstock Acctg v1.2, VR Sec 5.1

**AECN carbon content stats:** From MRV_AECN_Analysis.xlsx (n=285 MRV samples, updated March 2026). The 2-SD range (~27.2%-51.6%) is the flag threshold, not a hard pass/fail boundary.

**Note:** Carbon content used in the CO2e calculation (checked in Section 7) must match the lab report value here. Cross-reference.

---

## Section 5: Ops Notes Accuracy & Internal Consistency

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 5.1 | Correct batch ID and injection date | Ops Notes | Matches batch being QA'd | Wrong batch ID in header |
| 5.2 | All scale ticket values correctly transcribed | Ops Notes vs scale tickets | Values match ticket images | Transcription error |
| 5.3 | Oil and aqueous phase mass reconciliation | N/A for AECN | **Mark N/A** — AECN-only batches have no aqueous phase | |
| 5.4 | COBB values present and match | COBB tracker vs Ops Notes | origin_qty, BOL_number align | COBB row not found or values differ |
| 5.5 | pH measurement noted | Ops Notes > Batch Consumables | pH value present | pH missing — **pH is required for ALL batches including AECN** |
| 5.6 | Completion date present and matches COBB | Ops Notes vs COBB | Same date in both | Date mismatch |
| 5.7 | No erroneous density measurements | Ops Notes > Batch Composition | **Mark N/A** — density field is expected to be blank for AECN | Agent incorrectly flagging blank density as an issue |

**MANDATORY VERIFICATION SUB-TASK (5.4, 5.6):** Navigate to COBB tracker, verify cell A = batch ID before reading any values.

**CRITICAL — pH:** pH is required for ALL batches regardless of oil type. The agent has previously invented a rule that pH doesn't apply to AECN. It does. Find it in Ops Notes Batch Consumables section.

**CRITICAL — Density:** For AECN, the density field in Ops Notes Batch Composition IS expected to be blank. Mark 5.7 as N/A with note "Density field blank for AECN — expected behavior."

---

## Section 6: AECN Feedstock Emissions & Allocation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 6.1 | AECN process emissions LCA CI spreadsheet present | Certify Sources tab | Document present (check Sources tab, not just Datapoints) | Not checking Sources tab |
| 6.2 | LCA with stack emissions file present | Certify Sources tab | Document present | Same as above |
| 6.3 | Supporting GHG data file present for AECN production period | Certify Sources tab | Document present | Same as above |
| 6.4 | AECN pyrolysis process EF matches current value | Certify Datapoints | 0.10402 kgCO2e/kg (precise) / ~0.10 (display) | Wrong half-year EF, or using display value |
| 6.5 | AECN pyrolysis embodied EF applied | Certify Datapoints | 0.0212 kgCO2e/kg (precise) / ~0.02 (display) | Missing embodied EF entirely |
| 6.6 | Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging) | Certify Components | EF applied to pre-sparging mass | EF applied to post-sparging mass (wrong) |

**Verifier references:** VR Appendix 1, Certify Datapoints, Certify Components

**Document location rule applies to 6.1-6.3.** Check Drive first, then Certify Sources. Only FAIL if absent from BOTH.

**On 6.6:** Pyrolysis EFs should be applied to the Origin Bio-Oil Mass (the mass produced by pyrolysis, before sparging deduction at the injection site). This is correct because the emissions were incurred to produce the full quantity. Verified March 31, 2026 via batch 2-166.

**EF precision:** Certify may show rounded values (0.10, 0.02). The precise values from the Standard EF Sheet are 0.10402 and 0.0212 respectively. Verify against the Standard EF Sheet, not the Certify display.

---

## Section 7: Gross-to-Net Calculation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 7.1 | Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667 | Independent calc vs Certify | Match within rounding | Carbon % not as decimal (42 vs 0.42), unit mismatch |
| 7.2 | Process emissions correctly deducted | Certify Calculation View | AECN pyrolysis + transport deducted | Missing a component |
| 7.3 | Uncertainty discount correctly applied | Certify Calculation View | Present per Isometric Standard | Discount missing |
| 7.4 | Net removals consistent with BCU Quant and GHG Statement | Certify vs BCU Quant | Values align | Discrepancy |

**Verifier references:** GHG Stmt Sec E, Bio-oil Geol Storage v1.1, Isometric Standard v2.0 S3.7

**Formula verification:** Gross = mass_tonnes x carbon_decimal x 3.667. Always verify units are consistent (kg in -> kg CO2e, or tonnes in -> tCO2e). Carbon content must be a decimal (0.4140, not 41.40).

---

## Section 7a: Per-Component Uncertainty Verification

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 7a.1 | Layer 1 — Completeness: every AECN component has uncertainty on correct datapoint | Certify component modals + MRV Uncertainty Cheat Sheet | All required components have +/- values | Missing uncertainty on a component |
| 7a.2 | Layer 2 — Correctness: reported +/- matches expected value | Certify component modals (INPUTS section) | See Uncertainty Reference in SKILL.md | Wrong value, or value not actually checked |
| 7a.3 | Layer 3 — Discount presence and consistency | Certify Calculation View vs GHG Statement | Aggregate discount present in net calc | Discount missing or inconsistent |

**MANDATORY VERIFICATION SUB-TASK:** Open EACH component modal. Read the +/- from INPUTS section. Do not infer from aggregate calculations. +3 laziness penalty for avoidance.

**AECN components requiring uncertainty verification:**
- Injection Sequestration (Carbon Content + Mass of Product)
- Transport Process — AECN->Basco Tanker or AECN->SOPOR + Rail + Opelousas->Basco (Mass of Load per leg)
- AECN Pyrolysis Process Emissions (Bio-Oil Mass)
- AECN Pyrolysis Embodied Emissions (Bio-Oil Mass)

---

## Section 8: Data Integrity & Anomaly Check

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 8.1 | No unexplained outliers in mass, carbon content, or calculated values | All sources | Values within expected AECN ranges | Outlier not investigated |
| 8.2 | Any spills/losses documented, unrecovered mass deducted, incident report filed | Ops Notes, batch folder | If spill occurred: documented and deducted | Spill not deducted from mass |
| 8.3 | If inventory reconciliation: carryover oil documented | Reconciliation spreadsheet | If multi-period allocation: documented | N/A for most single-batch AECN |

**Verifier reference:** GHG Stmt Sec C, VR Sec 3.5

---

## Section 9: Isometric Certify — Removal Component Mapping

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 9.1 | SEQUESTRATIONS: Gross injection sequestration matches internal gross | Certify Components | One sequestration entry for the AECN batch | Sequestration value wrong |
| 9.2 | ACTIVITIES — Transport: Process + embodied correct for AECN route | Certify Components | Tanker truck (direct) or tanker + rail (via SOPOR) | Wrong mode or missing a leg |
| 9.3 | ACTIVITIES — Injection: LCS and sample transport correct | Certify Components | Samples for MRV (<1 kgCO2e typically) | Often N/A for pure AECN (no LCS needed) |
| 9.4 | ACTIVITIES — Pyrolysis: AECN production process + embodied entries present | Certify Components | "AECN Production Process Emissions" + "AECN Production Embodied Emissions" | Missing one of the two |
| 9.5 | REDUCTIONS: All applicable BCU categories populated | Certify Components | 5 categories: injection diesel, injection waste, pre-treat diesel, pre-treat waste, transport | Missing BCU category |
| 9.6 | REDUCTIONS — BCU quantity >= corresponding activity emission | Certify Components + Calculation View | Transport BCU >= transport activity (at minimum) | BCU underfunding a category |
| 9.7 | COUNTERFACTUALS: Zero per protocol | Certify Components | 0 | Non-zero counterfactual |
| 9.8 | Net removal matches internal calculation | Certify Calculation View | Agrees with independent gross-to-net | Discrepancy |
| 9.9 | All Datapoints have descriptive source names | Certify Datapoints | No "Measurement XXXX" or "IMG_001" | Generic names = FLAG (not FAIL) |
| 9.10 | All Sources match files in batch folder on Drive | Certify Sources vs Drive | Same files in both | File in one but not the other |

**Verifier reference:** Certify Components, Certify Datapoints, Certify Sources, Certify Calculation View

**On 9.3 for AECN:** AECN oil does NOT require LCS pre-treatment (that's for Aqueous). Mark LCS items as N/A if no LCS was used. Sample transport emissions are typically present but small (<1 kgCO2e).

**On 9.5:** Zero-value BCU Datapoints (derived zeros) have no sources — this is expected, not an error.

**On 9.6:** BCU QA rule — BCU quantity (tCO2e) in Reductions MUST equal or exceed the corresponding diesel/process emission (tCO2e) in Activities. Check EVERY removal.

**On 9.9:** Generic/non-descriptive filenames are a FLAG with yellow fill, not a FAIL. The content is correct; the naming is a hygiene issue.
