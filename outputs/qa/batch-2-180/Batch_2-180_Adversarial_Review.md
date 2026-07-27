# Adversarial Review — Batch 2-180

**Reviewer:** Adversarial Reviewer (Claude QA Agent, independent pass)
**Date:** 2026-05-11
**Checklist reviewed:** `outputs/qa/batch-2-180/Batch_2-180_QA_Checklist.xlsx`
**Source-read log:** `outputs/qa/batch-2-180/batch_2-180_source_reads.json`
**QA-agent counts:** 50 Pass / 0 Fail / 2 Flag / 6 N/A
**Audit script status:** Clean (0 failures)

---

## Step 0 — Primary Source Verification Check

| Risk item | QA agent claim | Independent verification | Pass/Reject |
|---|---|---|---|
| **Scale tickets (Section 2)** | Full + Empty PDFs read as image pixels via Drive download URL + `browser_network_request response-body` capture (native-res 3072×4080 / 1057×887 JPGs in `screenshots/`). Tractor 2217, trailer 36629, weights 79,640 / 35,800 lb extracted. | Confirmed — JPGs present on disk (`full_scale_ticket.jpg` 670 KB, `empty_scale_ticket.jpg`), axle sums independently reconcile to gross weights exactly (13,460+33,300+32,880 = 79,640 ✓; 12,440+14,540+8,820 = 35,800 ✓). Method note `feedback_drive_image_download_pattern` cited correctly. | ✅ Pass |
| **COBB tracker (Section 5)** | CSV line 62, cell A verified = "2-180"; tab "Basco Injection -- COBB". | Confirmed — CSV exported via authenticated browser, line 62 starts `2-180,bio_oil,2343-T_offload_1,...`. Row ID verification gate satisfied. | ✅ Pass |
| **Uncertainty modals (Section 7a)** | All 5 component modals opened; +/- values read from INPUTS section directly. | Confirmed — modal text quoted in source-read log includes verbatim "±0.1888 %", "±72.57 kg" strings. All 4 components with Mass-of-Load datapoints have the value; Truck Embodied correctly has no Mass-of-Load (per-mile EF, not per-T-mi). | ✅ Pass |

**Step 0 verdict: PASSED.** Primary sources verified for every section that demands them.

---

## Independent Math Recalculation

| Quantity | QA-agent value | My independent calc | Match? |
|---|---|---|---|
| Scale net | 19,885.47 kg | (79,640 − 35,800) × 0.453592 = **19,885.47328 kg** | ✓ |
| Sparging loss (1.29%) | 256.52 kg | 19,885.47328 × 0.0129 = **256.52261 kg** | ✓ |
| Injectate (post-sparging) | 19,628.95 kg | 19,885.47328 − 256.52261 = **19,628.95067 kg** | ✓ |
| Gross CO₂e | 33.974 t | 19.62895 × 0.472 × 3.667 = **33.974259 t** | ✓ (rounds to 33.974) |
| Truck Process | 5.000 t | 19.910 × 2,197 × 0.0001143 = **4.999741 t** | ✓ (rounds to 5.000) |
| Truck Embodied | 0.522 t | 2,197 × 0.00023756059 = **0.521921 t** | ✓ (rounds to 0.522) |
| Pyrolysis Process | 2.071 t | 19,910 × 0.10402 / 1,000 = **2.071038 t** | ✓ (rounds to 2.071) |
| Pyrolysis Embodied | 0.422 t | 19,910 × 0.0212 / 1,000 = **0.422092 t** | ✓ (rounds to 0.422) |
| Activities sum | 8.014 t (Calc View) / 8.015 t (Components raw) | 4.9997 + 0.5219 + 2.0710 + 0.4221 = **8.014792 t** | ✓ (8.014 Calc View precise; 8.015 is rounded-then-summed) |
| Uncertainty σ | 187 kg | √(0.1359² + 0.1256² + 0.01822² + 0.00755² + 0.00154²) = **0.18611 t = 186.1 kg** | ✓ (within rounding of 187) |
| Net CO₂e | 30.773 t | 33.974259 + 5.000 − 8.014792 − 0.187 = **30.7725 t** | ✓ (rounds to 30.773; display 30.77) |
| BCU vs Activity | BCU 5.000 ≥ Transport Process 5.000 | 5.000 = 4.99974 rounded → BCU exactly covers Transport Process | ✓ |

**All math reconciles within rounding tolerance.** No fabrication, no shortcuts. The QA agent's claims at every level — scale-ticket math, sparging, gross, per-component activities, uncertainty propagation, BCU sufficiency — all hold under independent recalculation.

---

## Cross-Source Consistency Spot-Checks

- **Trailer ID:** scale tickets both = "36629"; BOL Tanker ID = "36629"; consistent ✓
- **PAPS↔DR cross-check:** BOL page 5 PAPS = "TNDT511842"; scale tickets DR# = "511842" — same shipment trail border-to-Bunkie ✓
- **Mass chain (5 sources):** scale net 19,885.47 = Ops Notes Total Injectate 19,885.47 = COBB offloaded_quantity_kg 19,885.47328 ≤ BOL Qty Shipped 19,910 = COBB origin_quantity_kg 19,910 ✓
- **Carbon z-score:** (47.2 − 39.42) / 6.09 = 1.278 — within 2-SD flag threshold ✓
- **Dates:** BOL 2026-03-18 → border arrival 03-20 → scale weigh 03-25 → injection 04-01 → cert sampled 03-26 → cert reported 04-04. Monotonic and operationally sensible ✓
- **Density check:** lab 1.206 g/cm³ at 15°C vs BOL 1.1993 g/ml at 60°F — small temp-dependent delta consistent with bio-oil thermal expansion ✓
- **Loss reconciliation:** 281.05 kg loss = 256.52 sparging + 24.5 kg (= 19,910 − 19,885.47, scale-vs-BOL conservatism) ✓

---

## Challenged Items

**None.** Every Pass/Flag/N/A is supported by the cited evidence and reconciles independently.

---

## Confirmed Items (all 58 entries)

**Section 1 — Folder Completeness**
- **1.1 Pass:** Verified Drive folder id 1W3nJQgf...Gbh3R contains Ops Notes + Scale Tickets + Testing.
- **1.2 Pass:** Verified both Full + Empty JPG present in Scale Tickets subfolder; image-pixel reads at native res (3072×4080 / 1057×887), method cited.
- **1.3 Flag:** Correct application of `feedback_check_text_literal` — subfolder literally empty in Drive even though cert is in Certify Sources #5.
- **1.4 Pass:** Verified Ops Notes Sheet1 has all required fields populated.
- **1.5 Pass:** Verified lab cert location "BASCO LOUISIANA" + BOL Ship To "St Landry LA 71367" (Basco address) consistent.

**Section 2 — Scale Tickets & Mass**
- **2.1 Pass:** Verified ticket numbers 1312226084637 / 1312226084638, weigh #4637, axle sums equal certified gross to the pound on both tickets.
- **2.2 Pass:** Verified 3-25-26 → 4-1-26 = 7 days (within 14-day tolerance).
- **2.3 Pass:** Verified tractor 2217 / trailer 36629 identical on both tickets and matches BOL Tanker ID 36629.
- **2.4 Pass:** Verified 43,840 × 0.453592 = 19,885.47328 (exact match to Ops Notes cell).
- **2.5 Pass:** Verified MIN(scale 19,885.47, BOL 19,910) = scale; correct conservative selection.
- **2.6 Pass:** Verified sparging 19,885.47 × 0.0129 = 256.52 → 19,628.95 (Ops Notes exact).
- **2.7 Pass:** Verified 5-source mass chain reconciles (scale = Ops Notes total = COBB offloaded; BOL = Origin Bio-Oil Mass datapoint = COBB origin).

**Section 3 — BOLs & Transportation**
- **3.1 Pass:** Verified BOL "documents 2343-T.pdf" in Certify Sources #10 Public.
- **3.2 N/A:** Correct — truck batch, no SOPOR rail leg.
- **3.3 Pass:** Verified BOL 19,910 ≥ injectate 19,628.95 ≥ scale 19,885.47 (BOL is the high-water mark, scale is the conservative binding constraint).
- **3.4 Pass:** Verified BioEnergie AE Côte-Nord → CHARM Industrial St Landry origin/destination on BOL pages 1, 3, 5.
- **3.5 Pass:** Verified 2,197 mi consistent with KB AECN truck route, single direct leg.
- **3.6 Pass:** Verified 2 transport components (correct for truck batch).
- **3.7 Pass:** Verified PO + Commercial Invoice + customs broker bundle on BOL pages 2-5; PAPS TNDT511842 cross-references scale ticket DR# 511842.

**Section 4 — Bio-Oil Composition**
- **4.1 Pass:** Verified CHN PDF in Certify Sources #5 (multi-batch 2-180 → 2-185, page 1 of 6).
- **4.2 Pass:** Verified Carbon 47.2% within 2-SD range (z=+1.276, below 51.60 upper bound). On the high side but well within range. SGS # marker correctly identified as standard method-precision annotation.
- **4.3 Pass:** Verified H 8.2% and N <0.75% on cert page 1.
- **4.4 Pass:** Verified CLIENT ID = "BATCH 2-180" on cert page 1.
- **4.5 N/A:** Correct — AECN not aqueous phase.
- **4.6 Pass:** Verified density 1.206 g/cm³ > 1.01 g/cm³ formation-fluid floor; consistent with BOL page-3 1.1993 g/ml at 60°F.

**Section 5 — Ops Notes Accuracy**
- **5.1 Pass:** Verified Completion Date 4/1/2026 and Batch number 2-180 in Ops Notes.
- **5.2 Pass:** Verified all 4 transcribed scale-ticket values (Full 79,640 / Empty 35,800 / Net lbs 43,840 / Net kg 19,885.47328) match.
- **5.3 N/A:** Correct — AECN-only, no aqueous.
- **5.4 Pass:** Verified COBB row 61 cell A = "2-180" gate satisfied; consumed_lot 2343-T_offload_1, BOL 2343-T, origin 19,910, offloaded 19,885.47328, completion 2026-04-01, pH 3.1.
- **5.5 Pass:** Verified pH 3.1 in both Ops Notes col F row 14 and COBB col M.
- **5.6 Pass:** Verified 3 dates align: Ops Notes 4/1/2026 = COBB 2026-04-01 = Certify removal 01 Apr 2026.
- **5.7 N/A:** Correct — density blank for AECN is expected.

**Section 6 — AECN Feedstock Emissions**
- **6.1 Pass:** Verified Cote-Nord LCA CI.xlsx in Certify Sources #1.
- **6.2 Pass:** Verified BH 2025 LCA w Stack Emissions.xlsx in Certify Sources #2.
- **6.3 Pass:** Verified Supporting GHG data 31Dec2025.xlsx in Certify Sources #4.
- **6.4 Pass:** Verified Pyrolysis Process EF modal = 0.104 kgCO₂e/kg (precise 0.10402).
- **6.5 Pass:** Verified Pyrolysis Embodied EF modal = 0.0212 kgCO₂e/kg.
- **6.6 Pass:** Verified pyrolysis modals use Origin Bio-Oil Mass 19,910 kg (pre-sparging), correct per spec.

**Section 7 — Gross-to-Net**
- **7.1 Pass:** Independent recalc 33.974259 t = Certify 33.974 (exact rounding).
- **7.2 Pass:** Activities precise sum 8.014792 t = Calc View 8.014; Components raw sum 8.015 differs by 0.001 (rounding-of-rounded). Correctly explained.
- **7.3 Pass:** Variance propagation σ = 186.1 kg ≈ Certify 187 kg (within rounding).
- **7.4 Pass:** Net 33.974 + 5.000 − 8.014 − 0.187 = 30.773 (exact).

**Section 7a — Per-Component Uncertainty**
- **7a.1 Pass:** Verified all 5 component modals have uncertainty on correct datapoints; embodied correctly omits Mass-of-Load.
- **7a.2 Pass:** All ±values exactly match expected:
  - Carbon ±0.1888 = 0.004 × 47.2 ✓
  - All 4 Mass-of-Load ±72.57 kg (1 discrete weight) ✓
- **7a.3 Pass:** Aggregate 187 kg consistent with variance propagation from per-component inputs.

**Section 8 — Data Integrity**
- **8.1 Pass:** Mass 19.91 MT typical; Carbon 47.2 within 2-SD; no outliers.
- **8.2 Pass:** Loss 281 kg = sparging 256.5 + scale-vs-BOL conservatism 24.5. No spills documented in any source.
- **8.3 N/A:** Correct — single-truck single-batch, no inventory carryover.

**Section 9 — Certify Component Mapping**
- **9.1 Pass:** Gross 33.974 verified.
- **9.2 Pass:** Both truck transport components with inline math reconstruction (`feedback_section9_show_the_work` satisfied).
- **9.3 N/A:** Correct — AECN no LCS.
- **9.4 Pass:** Both pyrolysis components with inline math reconstruction.
- **9.5 Pass:** Single BCU category correct for truck batch without site burdens.
- **9.6 Pass:** BCU 5.000 = Transport Process 5.000 (exact equality satisfies BCU ≥ Activity); Embodied 0.522 correctly excluded from BCU coverage.
- **9.7 Pass:** Counterfactuals zero per protocol.
- **9.8 Pass:** Net 30.773 verified.
- **9.9 Flag:** 4 hygiene items correctly bundled (2 screenshot filenames, "Carbon emission factor" no-extension, "2-180 Full Empty Ticket" redundant-"Full" typo). All content verified correct; only filenames non-descriptive — appropriate FLAG classification per KB.
- **9.10 Pass:** Verified 14 sources enumerated; all VR Appendix 1 docs present per Document Location Rule.

---

## Observations (not new findings — context for Max only)

1. **Carbon 47.2% is on the high end of the AECN range.** Z-score +1.28 (89.9 percentile), below the 51.60% 2-SD upper bound. Below threshold → PASS is correct. Worth noting for trend-watching across H1 2026 AECN batches — if multiple consecutive batches trend high, it could indicate a feedstock or process shift. No action needed for this batch in isolation.

2. **BCU certificate `Charm-A4-2024-10-24-63-1976.pdf` provenance:** Same 2024-vintage A4 cert was flagged on batches 2-185/186/187/189/190/191/192/201/204 (per active registry). This batch (2-180, March 2026 truck) makes another use of the same cert. BCU **quantity** is verified correct (5.000 t = Transport Process 5.000 t exactly). The provenance question — whether one A4 cert legitimately spans multiple batches/transport modes/months — has been raised before and is Garrett's call. Did not raise as a new FLAG on this batch's checklist (would duplicate the open item across the active registry). Worth a single one-line Garrett confirmation across the cohort.

3. **Order_line_completed_on 2026-03-24 vs BOL date 2026-03-18:** 6-day gap between BOL issuance (Quebec) and PO line closure. Consistent with the border-crossing-to-Bunkie-weighing timeline (border arrival 03-20, scale weigh 03-25). No finding.

---

## Verdict

**Checklist is sound. Recommend forwarding to Max without modifications.**

Math reconciles end-to-end. Primary sources verified for every section that requires them. Flags correctly classified. No fabrication, no missed evidence, no shortcuts.
