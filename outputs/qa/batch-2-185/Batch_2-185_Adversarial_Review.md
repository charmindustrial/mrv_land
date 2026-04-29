# Batch 2-185 — Adversarial QA Review (Gate 3)

**Reviewer:** Claude (adversarial sub-agent)
**Date:** 2026-04-29
**Batch:** 2-185 (AECN rail, GPRX 5188 offload_4, Basco 6)
**Certify removal:** rmv_1KQ7Y0Y4S1S023MT — Net 17.094 tCO2e
**Inputs reviewed:** `batch_2-185_source_reads.json` (Gate 1 log), `Batch_2-185_QA_Checklist.xlsx` (85 items: 53 PASS / 7 FAIL / 4 FLAG / 21 N/A), KB Sections 6, 7a, 9, lessons_learned.md, checklist_structure.md.

---

## Independent Math Recalculation (Step 0)

I redid every load-bearing calculation against primary sources.

| Quantity | Independent calc | QA agent / Certify | Match |
|---|---|---|---|
| Scale-ticket net cargo | (56,660 − 29,280) lb × 0.453592 = 12,419.34 kg | 12,419.4 kg | ✓ |
| Ops Notes Cargo (kg) | 12,031.43584 kg (read from cell) | 12,031.44 kg | ✓ |
| Cargo discrepancy | 12,419.34 − 12,031.44 = 387.91 kg | 387.96 kg ("388") | ✓ |
| Sparging deduction (on reported base) | 12,031.44 × 0.0129 = 155.21 kg | 155.21 kg | ✓ |
| Mass injected (post-sparging, reported) | 12,031.44 − 155.21 = 11,876.23 kg | 11,876.23 kg | ✓ |
| Gross CO2e (reported inputs) | 11,876.23 × 0.431 × 3.667 / 1000 = 18.7707 t | 18.770 t (Certify) | ✓ |
| Gross CO2e (corrected, scale-ticket mass) | 12,419.35 × 0.9871 × 0.431 × 3.667 / 1000 = 19.3767 t | — | n/a |
| Gross under-claim from 388 kg error | 19.377 − 18.770 = 0.607 tCO2e gross (~3.2% of gross) | 0.61 tCO2e | ✓ |
| Estimated net under-claim (after activities scale up) | ~0.55 tCO2e ≈ 3.2% of net 17.094 | "~3%" | ✓ |
| BCU vs transport-process sum | 0.148 + 0.685 + 0.059 = 0.892 t | 0.892 t (BCU) | ✓ exact |
| Rail process calc check | 12.031 × 2,199 × 0.0000259104 = 0.6855 tCO2e | 0.685 t (Certify) | ✓ |
| Truck process AECN→SOPOR | 12.031 × 107.5 mi × 0.0001143 = 0.1479 t | 0.148 t (Certify) | ✓ |
| Truck process Opelousas→B6 | 12.031 × 42.9 × 0.0001143 = 0.05901 t | 0.059 t | ✓ |
| Net recalculation | 18.770 − 2.428 + 0.892 − 0.140 = 17.094 | 17.094 t | ✓ |
| Allocation fraction | 12,031.44 / 78,020 = 0.154210 | 0.1542096365 (Ops Notes) | ✓ |
| Carbon-content uncertainty | 43.1 × 0.004 = 0.1724% | 0.1724% | ✓ |
| Rail-embodied EF unit conversion | 0.0193 kgCO2e/km × 1.609 = 0.03105 kgCO2e/mi ≈ 0.03113 modal | 0.03113 kgCO2e/mi (= 0.0000311307 MTCO2e/mi) | ✓ 2026 corrected |
| COBB sum across 4 offloads | 21,509.33 + 22,634.24 + 21,457.08 + 12,419.35 = 78,020.00 kg | matches railcar total 78.02 MT | ✓ |
| Ops Notes sum across 4 offloads | 21,509.33 + 22,634.24 + 21,844.99 + 12,031.44 = 78,019.99 kg | matches railcar total 78.02 MT | ✓ |
| Mis-allocation magnitude (offload_3 vs offload_4 in Ops Notes vs COBB) | 387.91 kg shifted from offload_4 → offload_3 in Ops Notes | "same magnitude, opposite direction" | ✓ |

**No fabrication detected.** Every number the QA agent cited is reproducible from primary sources.

---

## 1. Confirmed Items (Status correct, evidence sufficient)

### Section 1 — Folder Completeness
- **R7 / 1.1 PASS** — Drive folder ID + contents enumerated. Evidence specific.
- **R8 / 1.2 PASS** — Both scale ticket file IDs cited. Verified.
- **R9 / 1.3 PASS** — Lab COA file with page-6 mapping for batch 2-185. Verified.
- **R10 / 1.4 PASS** — Ops Notes Drive ID + sheet contents specified.
- **R11 / 1.5 PASS** — Basco LA confirmed across sources, no Vaulted refs.

### Section 2 — Scale Tickets (verified PRIMARY SOURCES)
- **R13 / 2.1 PASS** — Both ticket numbers (763, 765), full+empty, sequential pair, same scale 3122, same date, same location. **Primary source verification confirmed** (KB Lessons Learned §1).
- **R14 / 2.2 PASS** — 3-31-26 vs injection 4/2/26, ~2 days apart.
- **R15 / 2.3 PASS** — Tractor CH2, Trailer KL-188 confirmed via OCR on BOTH ticket images. Primary source check confirmed.

### Section 3 — BOLs / Transportation
- **R21 / 3.1 PASS** — 3 BOLs in Certify Sources cited by name. Document Location Rule correctly applied.
- **R22 / 3.2 PASS** — Destination = SOPOR confirmed; total 78.02 MT correct.
- **R23 / 3.3 PASS** — BOL total 78.02 MT >> per-batch share. Railcar-level conservativeness met.
- **R24 / 3.4 PASS** — Origin/destination chain documented.
- **R25 / 3.5 PASS** — Distances enumerated per leg with sources. Email-from-Watco distance evidence correctly accepted for rail.
- **R26 / 3.6 PASS** — 6 transport components confirmed (rail batch convention).
- **R27 / 3.7 PASS** — Billing combined with BOL PDFs in Certify Sources. Minor naming inconsistency on 2313-R noted (not a blocker).

### Section 4 — Lab/CHN
- **R29 / 4.1 PASS** — SR26-02231 page 6 confirmed.
- **R30 / 4.2 PASS** — 43.1% carbon within AECN range (mean 39.42%, ±2 SD).
- **R31 / 4.3 PASS** — H 7.2%, N <0.75% reasonable.
- **R32 / 4.4 PASS** — CLIENT ID "BATCH 2-185" verified on COA page.
- **R33 / 4.5 N/A** — pH at injection covered in Section 5; no aqueous phase. Correct.
- **R34 / 4.6 PASS** — 43.10% carbon in Certify matches lab COA exactly.

### Section 5 — Ops Notes
- **R36 / 5.1 PASS** — Batch ID + 4/2/2026 in header.
- **R40 / 5.5 PASS** — pH=3 in offload_4 row, normal range, sister-batch consistent.
- **R42 / 5.7 N/A** — Density blank for AECN per KB rule.

### Section 6a — AECN
- **R44 PASS** — Section applies (AECN batch).
- **R45 / 6.1 PASS** — H2 2025 LCA CI xlsx in Certify Sources.
- **R46 / 6.2 PASS** — LCA w Stack Emissions xlsx present.
- **R47 / 6.3 PASS** — Supporting GHG data 31Dec2025 S.xlsx present.
- **R49 / 6.5 PASS** — Pyrolysis embodied EF 0.02116 matches KB 0.0212.

### Sections 6b/6c/6d — All N/A
- **R51, R52, R53, R54, R55, R56, R58, R59, R60, R61, R62, R63, R65, R66, R67, R68, R69 — All N/A** correctly assigned (AECN-only batch).

### Section 7
- **R72 / 7.2 PASS** — Activities total reconciles arithmetically.
- **R73 / 7.3 PASS** — 0.140 tCO2e uncertainty discount present.

### Section 8
- **R76 / 8.1 PASS** — Outliers caught and documented.
- **R77 / 8.2 PASS** — No spills; sparging applied.
- **R78 / 8.3 PASS** — **Last-batch railcar check executed correctly**: Oil Left = 0, mass balance closes (78,019.99 kg ≈ 78.02 MT), N_offloads=4 ≥ N_BOLs=3 ✓ verified. This is the precondition for Section 7a per-offload framing — correctly performed. Note also acknowledges the 388 kg mis-allocation while still confirming closure.

### Section 9
- **R80 / 9.1 PASS** — 18.770 tCO2e gross matches independent calc on reported inputs.
- **R81 / 9.2 PASS** — 6 transport components mapped and reconciled.
- **R82 / 9.3 N/A** — No LCS/sample for pure AECN rail. Correct.
- **R83 / 9.4 PASS** — Pyrolysis components correctly named with rail signal.
- **R84 / 9.5 PASS** — BCU Transport = 0.892 t = exact sum of 3 transport-process activities. Independently verified.
- **R85 / 9.7 PASS** — Counterfactuals zero per protocol.
- **R88 / 9.10 PASS** — 21 Certify Sources enumerated against VR App 1 requirements.

### Section 7a — Per-Component Uncertainty
- **R90 / 7a.1 PASS** — All 9 components inspected via modals. Primary source check satisfied.
- **R91 / 7a.2 PASS** — 43.1 × 0.004 = 0.1724% verified independently.
- **R92 / 7a.3 PASS** — 11,876.23 ±72.57 kg verified.
- **R93 / 7a.4 PASS** — Truck transport mass-of-load uncertainties read from modals: ±72.57 kg each. Per-removal framing correct.
- **R94 / 7a.5 PASS — RAIL UNCERTAINTY (specifically scrutinized).** The KB Section 7a (line 568) literally documents two competing rules: "in-rule" 217.71 kg and "out-rule" 290.28 kg. **However, the locked-in resolution per lessons_learned §9 (batch 2-183 lesson) is the per-removal model: ±72.57 kg per leg, ONLY when N_offloads ≥ N_BOLs is verified at the last batch.** This batch IS the last batch on GPRX 5188 (offload_4 of 4, Oil Left = 0), and N_offloads (4) ≥ N_BOLs (3) is verified at R78. The conservatism precondition is satisfied. The QA agent's PASS classification is correct. (If this were NOT the last batch, the precondition would be deferred and R94 would FLAG.)
- **R95 / 7a.6 PASS** — Pyrolysis modals confirmed. Note about extra ±0.00209 on CI is conservative and not an issue.
- **R96 / 7a.7 PASS** — Distances have no uncertainty input per KB rule.
- **R97 / 7a.8 PASS** — Aggregate discount 140 kg present and propagates correctly.

### Section "Additional Cross-Checks" (rail-specific)
- **R99 PASS** — Allocation 0.15421 verified independently. Correctly notes that allocation would shift slightly with corrected mass (0.15919).
- **R100 PASS** — Pyrolysis EF applied to pre-sparging Origin Bio-Oil Mass per KB Sec 6a.
- **R101 PASS** — Tanker truck embodied EF 0.1476 kgCO2e/km / 0.23756 kgCO2e/mi verified.
- **R102 PASS** — Rail embodied EF 0.0000311307 MTCO2e/mi (2026 corrected) verified. **Sister batch 2-182 had stale 0.0000352240 — this batch has the fix.**
- **R103 PASS** — Rail process EF 0.0000259104 MT/(t·mi) verified, calc check 0.685 t matches.
- **R104 PASS** — Truck process EF 0.0001143 MT/(t·mi) verified, calc checks 0.148 / 0.059 match.

---

## 2. Challenged Items

### CHALLENGE 1 — R17 / Item 2.5 (Conservative MIN selection): FAIL classification is awkward but stand
- **Current Status:** FAIL
- **Issue:** The "MIN(scale ticket net, BOL mass)" rule is **explicitly replaced for rail batches** per `checklist_structure.md` line 73: "scale tickets at the offload truck-out are AUTHORITATIVE for this batch's mass. BOL conservativeness applies to the inbound 3-BOL aggregate vs. railcar received mass, not to the per-batch offload delivery." Strictly read, this item shouldn't be checking conservative MIN at all for a rail batch. The QA agent's FAIL note pivots to "the value used (12,031 kg) does not match the scale ticket math" — which is true but is the same finding as R16/R19. Effectively R17 is a duplicate of R16.
- **Recommendation:** **Keep as FAIL** but rewrite the note to either (a) mark explicitly as "FAIL via R16 — rail batch substitutes scale-ticket authority for MIN rule; scale-ticket value not honored," or (b) demote to N/A with cross-reference to R16. Do NOT remove. Either framing is defensible; currently the language is mildly self-contradictory. Lower-priority change.

### CHALLENGE 2 — R18 / Item 2.6 (Sparging): PASS conflicts with its own evidence note
- **Current Status:** PASS
- **Issue:** The note states: "Sparging FRACTION is correct (1.29%), but applied to wrong base mass — see Item 2.4 FAIL." This is a contradiction. The 1.29% rate is correctly applied, but the resulting absolute values (Sparging Loss 155.21 kg vs expected 160.20 kg; Mass injected 11,876.23 vs expected 12,259.18 kg) are wrong because the base is wrong. Per the FAIL test ("evidence says something different from what's being reported"), the *Mass of Injectant* in Certify (11.876 t) is incorrect. PASS understates the issue.
- **Recommendation:** Keep as PASS but **strip the contradictory hedge** — either say "Sparging rate 1.29% correctly applied; downstream mass values inherit upstream Cargo (kg) error per R16" without internal conflict, OR reclassify to FLAG to surface the propagated error. Borderline; either is acceptable. The cleanest move is rewrite the note so it doesn't read as PASS-but-actually-broken.

### CHALLENGE 3 — R37 / Item 5.2 (Scale ticket transcription): Correctly classified FAIL but evidence framing is partially wrong
- **Current Status:** FAIL
- **Issue:** The item header says "All scale ticket values correctly transcribed into Ops Notes." The QA agent correctly notes that the Loaded/Unloaded LB values WERE transcribed correctly (matching the scale tickets), but the downstream Cargo (kg) cell is wrong. So strictly speaking, "transcription" is correct — the FAIL is about **internal arithmetic** (kg = lb × 0.453592 was not recomputed correctly), not transcription. This is a wording nit, not a classification error.
- **Recommendation:** Keep FAIL. **Tighten the note**: "Loaded/Unloaded LB values transcribed correctly; the kg conversion in Cargo (kg) cell is incorrect (12,031.44 kg recorded vs 12,419.34 kg expected from 27,380 lb × 0.453592)." This makes the failure mode unambiguous.

### CHALLENGE 4 — R74 / Item 7.4 (BCU Quant cross-check): FLAG borderline laziness pattern
- **Current Status:** FLAG
- **Issue:** Per `lessons_learned.md` §2 ("Missing Evidence Marked FLAG"): "If evidence is MISSING, you cannot confirm the reported value. That's a FAIL." The agent flagged because BCU Quant spreadsheet doesn't yet exist for this RP — this is structural deferral, not a real anomaly observed. Per `SKILL.md` adversarial reviewer guidance: "If the agent flagged something because it *couldn't verify* rather than because it *verified and found an anomaly*, that's not a Flag — that's unfinished work."
- **Counter-consideration:** For an AECN rail batch with no site-emission burden, the per-batch BCU is fully verified internally (BCU Transport 0.892 = exact transport-process sum). The BCU Quant rollup is genuinely an RP-level deliverable — not a per-batch artifact — so deferring its check until RP-level QA is structural, not laziness.
- **Recommendation:** **Keep as FLAG**, but rename note to "Per-batch BCU verified internally (0.892 = exact transport-process sum); RP-level BCU Quant rollup is a separate deliverable not yet produced for this RP, deferred to RP-level QA." Make the deferral structural and time-bound rather than open-ended.

### CHALLENGE 5 — Section 8 / R78 (8.3 Last-batch check): Verification was done but should also confirm sister-batch upstream allocation sum
- **Current Status:** PASS
- **Issue:** The note correctly verifies (a) Oil Left = 0, (b) sum of cargo masses ≈ 78.02 MT, (c) N_offloads (4) ≥ N_BOLs (3). However, `checklist_structure.md` line 239 also calls for: "Sum of allocation fractions across all populated sister-batch offload rows for the same railcar should ≈ 1.0." The QA agent did NOT explicitly compute this sum.
- **Independent check:** From the offloads table: 0.27569 + 0.29011 + 0.27999 + 0.15421 = 1.00000 ✓ (within rounding to last decimal). This passes — but the agent should have shown the work.
- **Recommendation:** **Keep PASS**, but add to evidence note: "Sister-batch upstream allocation sum: 0.27569 + 0.29011 + 0.27999 + 0.15421 = 1.00000 ✓." This is a one-line addition that closes a checklist_structure.md requirement.

### CHALLENGE 6 — R86 / Item 9.8 (Net match): Note understates the materiality framing
- **Current Status:** FAIL
- **Issue:** Note says "Material under-claim of ~3% on net — below 5% threshold but a real reporting error." The 5% materiality threshold per Isometric Standard is for VVB-level materiality on aggregated removal portfolio claims — applying it as a per-batch threshold is an inappropriate framing. The KB FAIL/FLAG test is *not* a percentage threshold; it's whether evidence conflicts with reported values. The mass conflict is direct, observable, and cross-source — that's a FAIL regardless of the percentage.
- **Recommendation:** **Keep FAIL**, but **strip the 5% framing** from this note and from R16. Replace with: "Mass values in Certify (12.031 t Allocated, 11.876 t Injectant) directly conflict with COBB (12.419 t) and scale-ticket math (12,419.34 kg). Direct evidence conflict = FAIL per KB FAIL/FLAG decision rule. Garrett to update Certify Allocated Bio-Oil Mass datapoint to 12,419.35 kg, recompute downstream Mass of Injectant to 12,259.18 kg." The materiality argument supports prioritization but should not soften the classification.

### CHALLENGE 7 — R87 / Item 9.9 (Generic filenames): Confirm PASS-equivalent FLAG policy and add concrete rename suggestions
- **Current Status:** FLAG
- **Issue:** Per KB Section 9 line 593: "Generic or non-descriptive filenames are a FLAG, not a FAIL." Classification is correct. **However**, lessons_learned §5 ("Narrow Application of Feedback") warns that if this is a recurring pattern on shared rail-batch datapoints, fixing the filename on one batch's Sources won't fix the same datapoint shared across removals. The QA agent acknowledged this ("These are SHARED datapoints across rail batches — fixing on one batch will not fix them on others") but didn't propose concrete renames.
- **Recommendation:** **Keep FLAG**, but enrich with proposed renames: e.g., "image (44).png" → "Watco_email_SOPOR_to_Opelousas_distance_2026.png"; "Screenshot 2026-04-10 at 3.19.33 PM.png" → "TruckProcess_EF_GLEC_V3.2_2026.png"; etc. Garrett can then rename in Certify Sources once and the fix propagates to all sister rail batches.

---

## 3. Observations (Issues the QA agent didn't surface)

These are not formal challenges — they're items I noticed during independent review.

### Observation A — Scale-ticket axle sum vs printed gross discrepancy
The full ticket shows axle sum = 56,660 lb but printed gross = 56,650 lb (10 lb difference, noted in Gate 1 source-read log as OCR/print artifact). Ops Notes uses 56,660. This is a **trivial** discrepancy (10 lb = ~4.5 kg, ~0.04%) but isn't called out anywhere in the checklist. Recommend a one-line note in R13 or R16 evidence: "Axle sum 56,660 lb used (Ops Notes); printed gross 56,650 lb on ticket — 10 lb diff is an OCR/print artifact, immaterial."

### Observation B — Pyrolysis CI uncertainty (±0.00209) absent from KB cheat sheet
The Pyrolysis Process modal contains a CI uncertainty (0.1038 ±0.00209 tCO2e/t) that the KB Section 7a uncertainty cheat sheet does NOT list as expected (Layer 1 / Layer 2 lists Bio-Oil Mass uncertainty only for pyrolysis components). The QA agent noted "conservative addition, not in KB; not an issue" in R95. **Question for Max/Garrett:** Is this CI uncertainty an intentional Charm input (Charm widening the variance) or an Isometric-required field that wasn't documented in the KB? If the latter, the KB cheat sheet should be updated. Suggest raising in Slack to Garrett.

### Observation C — Sister-batch 2-184 mis-allocation requires correction too
Per the source-read log: COBB shows 2-184 (offload_3) cargo = 21,457.08 kg; Ops Notes shows 21,844.99 kg. Same 387.91 kg discrepancy in OPPOSITE direction. **If 2-185's Certify Allocated Bio-Oil Mass is updated to 12,419.35 kg, sister batch 2-184's Certify must also be updated DOWN to 21,457.08 kg.** Otherwise the sum across the 4 sister batches will exceed the railcar total. The QA agent's R19 note acknowledges this but the recommendation in the summary row (R106) only proposes updating 2-185. **Recommend adding to summary**: "Sister batch 2-184 Certify Allocated Bio-Oil Mass must be updated DOWN to 21,457.08 kg in the same Garrett pass to maintain mass balance across the railcar."

### Observation D — R99 (allocation methodology) PASS uses the wrong-mass allocation
R99 confirms allocation 0.15421 = 12,031.44 / 78,020 ✓. But the correct allocation, after the 388 kg fix, would be 12,419.35 / 78,020 = 0.15919. The Certify allocated rail distance (339.10711 mi) and allocated AECN→SOPOR truck distance (80.03 km) are computed from 0.15421 and would shift to 350.04 mi and 82.61 km respectively after the fix. These derived datapoints will need to be re-derived after Garrett updates the mass. The QA agent flagged this in the R99 note ("True allocation using COBB mass would be 0.15919...") but didn't trace it through to the dependent Certify datapoints. Recommend adding "After Allocated Bio-Oil Mass correction, allocated rail distance recomputes to 2,199 × 0.15919 = 350.04 mi; allocated truck distance to 322.5 × 1.609 × 0.15919 = 82.61 km. These derived Certify datapoints will refresh automatically if Certify recalculates from the source mass datapoint." to R99 evidence.

---

## 4. Critical Issues That Must Be Addressed Before Shipping to Garrett

Ranked by priority:

1. **[CRITICAL]** Confirm 388 kg mis-allocation between offload_3 (sister 2-184) and offload_4 (this batch 2-185) in Ops Notes. The Cargo (kg) cells in the offload table need correction. Both sister batches' Certify Allocated Bio-Oil Mass datapoints need updating in tandem. Summary row R106 currently recommends fixing only 2-185 — **add 2-184**.

2. **[HIGH]** Refine the FAIL/FLAG classification language in R16 / R19 / R86 to remove the "below 5% materiality" framing. Per KB FAIL/FLAG decision rule, this is FAIL because of evidence-vs-reporting conflict, regardless of percentage. The materiality framing is for *prioritization*, not *classification*.

3. **[MEDIUM]** Resolve R18 internal contradiction (PASS evidence note says "applied to wrong base mass"). Either rewrite to show the propagation cleanly without contradicting PASS, or reclassify to FLAG.

4. **[MEDIUM]** R74 BCU Quant FLAG should be tightened to a structural deferral, not open-ended laziness. Add: "Per-batch BCU internally verified; RP-level rollup pending."

5. **[LOW]** R78 (Section 8.3) should explicitly compute the sister-batch upstream allocation sum (= 1.00000) per checklist_structure line 239.

6. **[LOW]** R87 should propose concrete filename renames (and note that Garrett can fix once across shared datapoints).

7. **[LOW]** Observation B — clarify whether pyrolysis CI ±0.00209 is intended Charm input or an unflagged Isometric requirement.

---

## 5. Verdict

**Overall:** This is a strong checklist. The QA agent correctly identified the central failure mode (388 kg Cargo discrepancy), traced its propagation through all 7 affected items, applied the locked-in per-removal uncertainty framing correctly, and confirmed the Section 8 last-batch precondition. Math is reproducible end-to-end. No fabrication. No primary-source-skipping.

**Notable wins:**
- Rail Embodied EF correctly read as **2026-corrected** value 0.0000311307 (sister 2-182 had stale value FAILed in 4/28 QA — this batch has the fix).
- Section 8 last-batch check (Oil Left = 0, N_offloads ≥ N_BOLs) was *actually performed* — gates the per-offload uncertainty PASS legitimately.
- All 9 component uncertainty modals were opened and ±values cited (no Layer 2 avoidance).
- Cross-source mass chain (scale tickets ↔ COBB ↔ Ops Notes ↔ Certify) was independently traced and the discrepancy localized.

**Material gaps:**
- Sister batch 2-184 must be corrected in tandem with 2-185 (Observation C / Critical #1).
- A few classification framings (FAIL with materiality hedge, PASS-but-broken sparging note) need tightening.

**Net classification verdict on the 7 FAILs**: All 7 are correct as FAIL (evidence conflicts with reported values across sources). The per-batch impact is ~3.2% which is non-trivial; combined with sister batch 2-184 correction it represents a real reporting error that must be corrected before VVB review.

**Recommended action:** Address Critical #1 and High #2 before shipping to Garrett. Other items are polish, not blockers.
