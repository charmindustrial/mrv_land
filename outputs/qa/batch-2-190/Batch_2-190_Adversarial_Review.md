# Batch 2-190 — Adversarial Self-Review

**Reviewer:** qa-adversarial-reviewer (independent pass over QA agent output)
**Date:** 2026-05-03
**Inputs reviewed:**
- Checklist: `Batch_2-190_QA_Checklist.xlsx` (52 Pass / 0 Fail / 1 Flag / 4 N/A)
- Source-read log: `batch_2-190_source_reads.json`
- Build script: `build_checklist.py`

**Batch context:**
- Oil: AECN | Mode: Rail | Railcar: TILX200231 (NEW — first appearance in registry)
- consumed_lot: `Rail_TILX200231_3.23.2026_offload_1` — offload_1, NOT the railcar's last pull
- Sisters in COBB: 2-191 (offload_2, row 68), 2-192 (offload_3, row 69); cumulative through offload_3 = 65,335.39 kg of 77,270 kg loaded; ~11,935 kg remains → at least one more offload to come
- Net CDR (Certify): 26.28 tCO2e displayed / 26.277 t precise
- Pre-delivery audit script: PASSED (0 failures across 53 rows)

---

## Step 0 — Primary Source Verification Check

**Scale tickets (Section 2.3):** Evidence note cites tractor **Ch2** and trailer **KL-188** read from BOTH the full and empty JPGs (verified directly from pixels per OCR-vs-image rule). Specific weights cited: Full 76,780 lb (axle sum 10,060 + 33,680 + 33,040), Empty 29,400 lb (axle sum 9,480 + 11,700 + 8,220). Certified gross = axle sum on both tickets — no axle-vs-cert discrepancy. **PASSES the primary source check.** ✓

**COBB (Section 5.4):** Evidence cites the specific tab (`Basco Injection -- COBB`) and row (67), with cell A67 = "2-190" verified per the row-verification gate. Seven cell values extracted: A67, C67, E67, G67, H67, L67, M67. **PASSES the primary source check.** ✓

**Uncertainty modals (Section 7a):** Six component modals individually opened and the ±values read from the INPUTS section: Injection Sequestration (Carbon ±0.15%, Mass ±72.57 kg), AECN→SOPOR Truck Process (Mass ±72.57), SOPOR→Opelousas Rail Process (Mass ±72.57), Opelousas→Basco Truck Process (Mass ±72.57), AECN Pyrolysis Process (Mass ±72.57), AECN Pyrolysis Embodied (Mass ±72.57). Embodied transport modals also opened (AECN→SOPOR Truck Embodied, SOPOR→Opelousas Rail Embodied) and confirmed to have NO Mass-of-load datapoint per FC8 methodology. **PASSES the primary source check.** ✓

**BOL (Section 3.2):** BOL 2339-R Read directly (3-page PDF), ship-to address verified character-by-character: "CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau" = SOPOR Quebec railyard. Page 2 highlighted "Qty shipped" 25.63 MT confirmed against Page 3 scale ticket NET 25,630 KG. **PASSES the primary source check.** ✓

**Lab CHN (Section 4.2):** PDF Read directly, page 1 = "BATCH 2-190", values extracted: C 37.5%, H 7.3%, N 1.28%, Visc 16.08 cSt, Acid 58 mg KOH/g, Density 1.196 g/cm³. **PASSES the primary source check.** ✓

No items fail the primary source check. Proceeding to Step 1.

---

## Step 1 — Independent Calculations

I redid every calculation in the checklist:

**Mass chain:**
- Scale ticket net: (76,780 − 29,400) lb = 47,380 lb. Using Ops Notes factor 0.453592: **47,380 × 0.453592 = 21,491.18896 kg.** ✓ matches Ops Notes Cargo (kg) D17 exactly.
- Sparging: 21,491.18896 × 0.0129 = **277.2363376 kg.** ✓ matches Ops Notes E17.
- Mass of bio-oil: 21,491.18896 − 277.2363376 = **21,213.95262 kg.** ✓ matches Ops Notes F17.
- (Note on log entry `net_kg_via_div_220462: 21490.05` — this appears to be a minor arithmetic error in the log itself; the correct conversion via 1/2.20462 yields ~21,491.20 kg, not 21,490.05. **Not actionable** — the checklist cites `net_kg_via_mult_factor` which is correct, and Ops Notes uses the multiply-factor 0.453592 in cell F5, so this divisor calc never enters the verification chain.)

**Gross-to-net (full precision):**
- Sequestration: 21.21395262 t × 0.375 × 3.667 = **29.171 t.** Certify: 29.172 t. ✓ within 0.001 rounding.
- AECN→SOPOR Truck Process: 21.491 × (173/1.609344) × 0.0001143 = 21.491 × 107.50 × 0.0001143 = **0.264 t.** ✓
- SOPOR→Opelousas Rail Process: 21.491 × 2199 × 0.0000259 = **1.224 t.** ✓
- Opelousas→Basco Truck Process: 21.491 × 42.9 × 0.0001143 = **0.105 t.** ✓
- AECN→SOPOR Truck Embodied: 0.23756 × (144.35/1.609344) = 0.23756 × 89.69 = **21.30 kg = 0.021 t.** ✓
- SOPOR→Opelousas Rail Embodied: 0.03113 × 611.61 = **19.04 kg = 0.019 t.** ✓
- Opelousas→Basco Truck Embodied: 0.23756 × 42.9 = **10.19 kg = 0.010 t.** ✓
- Pyrolysis Process: 21.491 × 0.104 = **2.235 t.** ✓
- Pyrolysis Embodied: 21.491 × 0.02116 = **0.45475 → 0.455 t.** ✓
- Activities sum: 1.593 + 0.050 + 2.690 = **4.333 t** (Calc View shows 4.334, 0.001 rounding accumulation). ✓
- BCU = process transport sum: 0.264 + 1.224 + 0.105 = **1.593 t.** ✓ exact match to BCU value.
- Net: 29.172 + 1.593 − 4.334 − 0.154 = **26.277 t.** Certify: 26.277 t. ✓ exact.

**All math reconciles to Certify within rounding.**

**Emission factors verified against KB Section 6:**
- Truck Process: 0.0001143 MTCO2e/(t·mi) ✓ matches KB
- Rail Process: 0.0000259104 MTCO2e/(t·mi) ✓ matches KB
- Truck Embodied: 0.00023756059 MTCO2e/mi ✓ matches KB 2026 value
- Rail Embodied: 0.0000311307 MTCO2e/mi ✓ matches KB 2026 corrected value (NOT stale 0.0000352240 — propagation of the 2-182 fix is intact)
- AECN Pyrolysis Process: 0.10402 tCO2e/t ✓ matches KB H2 2025 value
- AECN Pyrolysis Embodied: 0.0212 tCO2e/t (precise 0.02116) ✓ matches KB

**Carbon content range verified:** Mean 39.42%, ±2 SD ~27.2%-51.6% (n=285 per MRV_AECN_Analysis.xlsx, KB Section 6). Batch 2-190 = 37.5% — within 1 SD. ✓

**Uncertainty inputs verified against FC9 / KB Section 7a:**
- ±72.57 kg per discrete weight (one outbound weighing at Basco) on every transport process leg + injection seq + both pyrolysis components ✓
- Embodied transport components correctly have NO Mass-of-load datapoint (FC8 methodology) ✓
- Carbon content ±0.4% relative (= 37.5 × 0.004 = 0.15) ✓
- Modal values for all 6 mass-input components confirmed ±72.57 kg ✓

**FC11 railcar last-offload check:** Offload 1 of 4+ — back-calc does NOT apply. Checklist correctly does not flag any policy-driven mass divergence. ✓

**FC9 conservatism precondition (N_offloads ≥ N_inbound_BOLs):** Correctly DEFERRED to the railcar's last batch QA. ✓

---

## Step 2 — Status Classification Review

Applying the FAIL vs FLAG decision rule: *"would a VVB reviewer be unable to confirm the reported value?"*

| Item | Status | My Assessment |
|------|--------|---------------|
| 1.1-1.5 | Pass | All docs present, naming correct, no Vaulted refs ✓ |
| 2.1-2.7 | Pass | Math verified, transcription verified, tractor/trailer match ✓ |
| 3.1-3.7 | Pass | 3 BOLs present, route correct, distances verified, 6 components present ✓ |
| 4.1-4.4 | Pass | CHN docs present, carbon in range, batch ID matches, sampled at Basco LA ✓ |
| 4.5 | N/A | AECN not aqueous ✓ |
| 5.1-5.2 | Pass | Cross-source matches verified ✓ |
| 5.3 | N/A | AECN-only batch, no aqueous phase ✓ |
| 5.4 | Pass | All 7 COBB cells match Ops Notes; row verification gate passed (A67="2-190") ✓ |
| 5.5-5.6 | Pass | pH cross-source match (3=3); date cross-source match ✓ |
| 5.7 | N/A | Density blank for AECN per protocol ✓ |
| 6.1-6.6 | Pass | LCA docs present, EFs match, mass basis correct (pre-sparging) ✓ |
| 7.1-7.4 | Pass | All calculations verified independently ✓ |
| 7a.1-7a.3 | Pass | 6 modals opened, ±72.57 kg verified each, carbon ±0.15% verified ✓ |
| 8.1-8.3 | Pass | No outliers, no spills, sister-batch sanity check appropriately framed ✓ |
| 9.1-9.8 | Pass | All Certify components reconcile ✓ |
| 9.9 | Flag | 4 generic filenames + 2 source-link tab references + BCU cert filename pattern ✓ Correctly classified as Flag (hygiene, not material) |
| 9.10 | Pass | All required Appendix 1 docs present in Certify Sources ✓ |

---

## Step 3 — Specific Items Scrutinized Per Review Brief

**1. Scale ticket lbs-to-kg factor.** Confirmed Ops Notes uses cell F5 = 0.453592 (slightly truncated from exact 0.45359237). 47,380 × 0.453592 = 21,491.18896. ✓ The 21,491.19 in checklist text rounds to 2 decimals consistent with Ops Notes display.

**2. FC11 last-offload policy.** This batch is offload_1 of new railcar TILX200231. The back-calc applies only to the railcar's last pull. Checklist correctly notes "rail last-offload conservatism policy does NOT apply here" in 2.4. No mass divergence flagged. ✓

**3. FC9 per-removal uncertainty framing.** All 3 process transport legs + injection seq + 2 pyrolysis = 6 components show ±72.57 kg in modals. Embodied transport components have no Mass-of-load datapoint. Carbon ±0.15% = 37.5 × 0.004. ✓ Conservatism precondition (N_offloads ≥ N_inbound_BOLs = 3) correctly deferred to last-batch QA per 7a.2 and 8.3. ✓

**4. Gross-to-net independent calc.** Reconciles to Certify within 0.001 t rounding at every step. ✓ See Step 1 above.

**5. BCU sister-pattern check.** 2-190 BCU = 1.593 t = exact sum of process transport (0.264 + 1.224 + 0.105). No over-application (unlike 2-188 where BCU = 5.582 vs sister-pattern 1.6x). Clean. ✓

**6. BCU certificate filename.** "Charm-A4-2024-10-24-63-1976.pdf" — same filename Max flagged on 2-188. For 2-190 this is a NEW railcar (TILX200231 vs prior TIMX201060). The QUANTITY is correct; only the filename pattern (A4 vs sisters' A3) is in question. **9.9 Flag-not-Fail classification is correct** under the decision rule: a VVB reviewer can confirm the reported BCU value (it equals the process transport sum exactly), so this is a hygiene/provenance question for Garrett, not a material misstatement risk.

**7. Sources tab enumeration.** 23 sources. All required AECN docs present (LCA CI, LCA stack emissions, Supporting GHG data, 3 BOLs, scale tickets, CHN, BCU cert, route maps). 4 generic filenames + 2 source-link tab references + 1 new "Process" file linked to "Embodied" datapoint = grouped under 9.9 Flag. ✓

**8. pH = 3 (whole number).** Both Ops Notes G17 and COBB M67 show "3" — pattern-consistent across sister rows 68/69 on same railcar TILX200231. Item 5.5 Pass is correct because both sources match. Could have been a precision Flag, but per the decision rule (would a VVB struggle to confirm?), No → Pass appropriate. The whole-number entry is recorded as a soft observation in the evidence note without escalating to Flag.

**9. Citation discipline.** Every PASS/FAIL/FLAG row has at least one [log:KEY] tag. Audit script ran clean (0 failures across 53 rows). ✓

**10. Confabulation check (FC10).** Every numeric value quoted in evidence notes was located in the source-read log at the cited path. No hypothetical values, no "what if" logic, no parallel-reality challenges. ✓

---

## Final Verdict

**READY FOR MAX.**

### Challenged Items
**NONE.** I cannot identify a single item where the assigned status is wrong, the evidence is unsupported, or a primary source went unread. This is a clean batch and the work was thorough.

### Confirmed Items (one-line per item)

- **1.1** Confirmed: Drive folder ID `1rvCpANvDSh2G64SZQVPCyzrbDHg5NxmP` contains Ops Notes Rail sheet + Testing + Scale Tickets subfolders.
- **1.2** Confirmed: Both scale ticket JPGs present; pixels Read directly from local Drive mount.
- **1.3** Confirmed: 2-190-2-191 Tests.pdf present, page 1 = "BATCH 2-190", Reissue 1.
- **1.4** Confirmed: Ops Notes Rail header B3 = "2-190", B1 = 4/10/2026; row 17 fully populated.
- **1.5** Confirmed: Lab CoA LOCATION = "BASCO LOUISIANA"; no Vaulted refs.
- **2.1** Confirmed: Both tickets show certified gross = axle sum (76,780 = 10,060+33,680+33,040; 29,400 = 9,480+11,700+8,220).
- **2.2** Confirmed: Both tickets dated 4-03-26; injection 4/10/2026; 7-day gap within 2-week tolerance.
- **2.3** Confirmed: Tractor Ch2 / Trailer KL-188 on both tickets (verified pixel-by-pixel).
- **2.4** Confirmed: 47,380 × 0.453592 = 21,491.18896 = Ops Notes D17 exactly.
- **2.5** Confirmed: Per-offload non-last rail batch — scale-ticket math is authoritative; FC11 doesn't apply.
- **2.6** Confirmed: 21,491.18896 × 0.0129 = 277.2363376 kg sparging; F17 = 21,213.95262 kg.
- **2.7** Confirmed: 4-source mass chain alignment (scale tickets / Ops Notes / COBB / Certify all = 21,491.19 kg ± rounding).
- **3.1** Confirmed: 3 BOLs present in Drive (Shared > Logistics > 2026 BOLs > Rail > March > TILX200231) AND in Certify Sources.
- **3.2** Confirmed: BOL 2339-R verified — Ship To = SOPOR Baie-Comeau, From = AECN Port-Cartier.
- **3.3** Confirmed: 25.70 + 25.63 + 25.94 = 77.27 MT BOL aggregate ≥ 21.49 MT this offload.
- **3.4** Confirmed: 4-leg route documented (AECN→SOPOR truck → SOPOR→Opelousas rail → Opelousas→Basco truck).
- **3.5** Confirmed: Allocation fraction 0.27813 yields 144.35 km / 611.61 mi / 89.70 mi consistent with Ops Notes I17/J17.
- **3.6** Confirmed: 6 transport components present (3 process + 3 embodied).
- **3.7** Confirmed: BOL/billing PDFs serve dual purpose per AECN convention.
- **4.1** Confirmed: SGS Order 5437581, 2-page CoA, page 1 = 2-190.
- **4.2** Confirmed: 37.5% within ±2 SD AECN range (27.2%-51.6%).
- **4.3** Confirmed: H 7.3, N 1.28, Visc 16.08, Acid 58, Density 1.196 — all values present and reasonable.
- **4.4** Confirmed: Certificate SR26-02484.001 Reissue 1 explicitly = "BATCH 2-190", sampled 05-Apr at BASCO LA.
- **4.5** Confirmed: N/A — AECN not aqueous.
- **5.1** Confirmed: Batch ID and injection date match across Ops Notes / COBB / Certify.
- **5.2** Confirmed: Ops Notes B17/C17/D17 = scale ticket gross / empty / cargo exactly.
- **5.3** Confirmed: N/A — AECN-only.
- **5.4** Confirmed: 7 COBB cells match Ops Notes; A67 = "2-190" row verification gate passed.
- **5.5** Confirmed: pH = 3 in both sources; sister rows 68/69 also pH = 3.
- **5.6** Confirmed: 4/10/2026 in all three sources.
- **5.7** Confirmed: N/A — density expected blank for AECN.
- **6.1** Confirmed: AECN LCA CI xlsx present in Sources, vintage H2 2025.
- **6.2** Confirmed: BH 2025 LCA w Stack Emissions xlsx present.
- **6.3** Confirmed: Supporting GHG data 31Dec2025 S xlsx present.
- **6.4** Confirmed: 21.491 × 0.104 = 2.235 t matches Certify pyrolysis process.
- **6.5** Confirmed: 21.491 × 0.02116 = 0.455 t matches Certify pyrolysis embodied.
- **6.6** Confirmed: Pyrolysis EFs applied to pre-sparging 21,491 kg, not post-sparging 21,214 kg.
- **7.1** Confirmed: 21.21395262 × 0.375 × 3.667 = 29.171 ≈ Certify 29.172.
- **7.2** Confirmed: Sum of 8 activity components = 4.333 t (Calc View 4.334, 0.001 rounding).
- **7.3** Confirmed: Uncertainty discount = 29.172 + 1.593 − 4.334 − 26.277 = 0.154 t (~0.585% of gross).
- **7.4** Confirmed: Net = 29.172 + 1.593 − 4.334 − 0.154 = 26.277 t.
- **7a.1** Confirmed: All 6 mass-input components show ±72.57 kg; embodied components have no mass datapoint.
- **7a.2** Confirmed: ±72.57 kg matches FC9 per-offload framing; carbon ±0.15% = 37.5 × 0.004.
- **7a.3** Confirmed: Aggregate discount 0.154 t present in Calc View, consistent with input ±values.
- **8.1** Confirmed: All values within expected ranges; BCU = exact process transport sum (no over-app).
- **8.2** Confirmed: No spills; Oil Left in Railcar fields blank (expected for non-last offload).
- **8.3** Confirmed: Sisters in COBB show offload_1/2/3; remaining ~11,935 kg → at least one more offload; last-batch reconciliation deferred.
- **9.1** Confirmed: Sequestrations 29.172 t matches independent gross calc.
- **9.2** Confirmed: 6 transport components correct EFs (rail embodied = 2026 corrected 0.03113, no stale carryover).
- **9.3** Confirmed: N/A — AECN no LCS.
- **9.4** Confirmed: Pyrolysis process + embodied both present with rail-batch naming.
- **9.5** Confirmed: BCU Transport category populated (1.593 t); other BCU categories N/A absent site emissions.
- **9.6** Confirmed: BCU 1.593 = process transport sum exactly; embodied not BCU-eligible per protocol.
- **9.7** Confirmed: Counterfactuals = 0 t per protocol.
- **9.8** Confirmed: Net = 26.277 t reconciles input-by-input.
- **9.9** Confirmed: Flag classification correct — 4 generic filenames + rail PROCESS sourced from "...Embodied Emissions.pdf" + AECN Process xlsx linked to Embodied datapoint + BCU cert filename pattern. All hygiene, none verifier-impacting.
- **9.10** Confirmed: 23 sources cover all VR Appendix 1 requirements.

### Observations (not in scope but worth noting)

1. **Minor log arithmetic error (non-actionable):** Source-read log entry `scale_tickets.net_mass_calc.net_kg_via_div_220462: 21490.05` is wrong (correct value via 1/2.20462 ≈ 21,491.20). Doesn't propagate to checklist because the multiply-factor key is the one cited. Consider a one-line correction to the log for cleanliness, but it has no verification impact.

2. **9.9 sub-flag (NEW for 2-190):** "AECN Process Emissions Calculation.xlsx" linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint. Already captured in 9.9 evidence note, included for Garrett review. Worth a one-line confirmation that the xlsx contains both process AND embodied calcs (in which case naming is incomplete but link is fine).

3. **BCU certificate filename (NEW for new railcar):** Charm-A4-2024-10-24-63-1976.pdf for new railcar TILX200231. Quantity is correct (1.593 t = process transport sum exactly), so verifier-side is clean. Garrett-side question on whether different railcars use different BCU certificates as designed.

---

**Final verdict: READY FOR MAX.** The single Flag (9.9) is correctly classified. All math reconciles. All primary sources opened and Read directly. Citation discipline clean. No challenges, no blocking issues.
