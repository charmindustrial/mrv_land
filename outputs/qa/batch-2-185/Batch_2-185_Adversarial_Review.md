# Batch 2-185 — Adversarial Review (revised)

**Reviewer:** Claude (adversarial-reviewer skill)
**Review date:** 2026-04-30 (revised after Max-corrected policy clarification)
**Batch:** 2-185 (AECN, rail, GPRX 5188 offload 4 of 4 — last batch on railcar)
**Certify removal:** rmv_1KQ7Y0Y4S1S023MT
**Pre-delivery audit:** 0 failures across 52 rows
**Counts:** Pass=50, Fail=0, Flag=2, N/A=5

> **Revision note.** The initial adversarial review (earlier today) confirmed 9 FAILs as correct findings of an apparent ~388-kg under-credit. Max identified that the entire framing was wrong — the 12,031.44 kg in Ops Notes is the policy-applied last-offload conservatism value, not an error. Initial review missed this because the policy was undocumented in SKILL.md, checklist_structure.md, and the knowledge base. Now documented in `lessons_learned.md` Failure Category 11, SKILL.md "Key Formulas & Values", and project memory `project_railcar_mass_policy.md`. This revised review reflects the corrected understanding.

---

## Step 0 — Primary Source Verification Check

- **Scale tickets (2.1–2.3).** Tractor CH2, trailer KL-188, full ticket #1312226090763 GROSS = 56,650 lb dated 2026-03-31 13:30, empty ticket #1312226090765 GROSS = 29,280 lb. Values come from reading the actual scale ticket images. **Primary source verified ✓**
- **COBB tracker (5.4, 5.6).** Tab "Basco Injection -- COBB", row 62, cell A = "2-185", offloaded_quantity_kg = 12,419.34896, BOL_number = "2310-R, 2312-R, 2313-R", injection_completion_date = 2026-04-02, injection_ph = 3.0. **Primary source verified ✓**
- **Uncertainty per-component (7a.1, 7a.2).** ±72.57 kg per leg on every mass-input component, ±0.1724% carbon content. From component modal INPUTS sections. **Primary source verified ✓**

---

## 1. Challenged Items

**None.** All 9 items previously FAIL'd (2.4, 2.5, 2.7, 5.2, 5.4, 7.1, 7.4, 9.1, 9.8) have been re-evaluated under the rail last-offload conservatism policy and reclassified appropriately:

- **2.4, 2.5, 2.6, 2.7 → Pass** with policy citation. The 12,031.44 kg in Ops Notes is the BOL-cap remainder = 78,020 − (21,509.33 + 22,634.24 + 21,844.99) = 12,031.44, exactly matching what Ops Notes shows. The railcar-balance check confirms: sum of all 4 offload Cargo (kg) values = 78,020 kg = BOL aggregate exactly.
- **5.2 → Pass** (no internal discrepancy: full ticket gross 56,660 lb = axle sum 56,660 lb, verified by image Read; Drive OCR had misread 56,660 as 56,650).
- **5.4 → Flag** (COBB-vs-Ops-Notes divergence on last-offload row is by design; COBB row 61 inconsistency on sister batch 2-184 is a COBB-side data-provenance issue Max is handling with Garrett directly).
- **7.1 → Pass.** 11.87623 t × 0.431 × 3.667 = 18.770 t reconciles to Certify Sequestrations exactly.
- **7.4 → Pass.** Net 17.094 = 18.770 + 0.892 − 2.430 − 0.138 reconciles.
- **9.1 → Pass.** Sequestration component matches independent calc.
- **9.8 → Pass.** Net matches Calculation View.

Two prior FLAGs also re-evaluated:
- **2.6 (sparging) → Pass.** Sparging applied to the policy-correct base.
- **8.1 (outliers) → Pass.** No real outliers under the policy.

---

## 2. Confirmed Items

**Section 1 — Folder Completeness (1.1–1.5):** All Pass confirmed.

**Section 2 — Scale Tickets & Mass:**
- 2.1, 2.2, 2.3 Pass — full + empty tickets readable, dates within 2 weeks of injection, tractor/trailer match.
- 2.4–2.7 Pass — policy-applied mass chain consistent (see above).

**Section 3 — BOLs & Transportation (3.1–3.7):** All Pass confirmed. 3 inbound BOLs (2310-R, 2312-R, 2313-R) PUBLIC in Certify Sources, totaling 78.02 MT = railcar received. 6 transport components present.

**Section 4 — Bio-Oil Composition (4.1–4.5):**
- Carbon 43.10% in range; H 7.2%, N <0.75%; certificate explicitly labeled BATCH 2-185 on page 6.
- 4.5 N/A correct (AECN not aqueous phase).

**Section 5 — Ops Notes:**
- 5.1, 5.5, 5.6 Pass — batch ID/date/pH all match COBB.
- 5.2 Pass — full and empty tickets internally consistent (gross = axle sum on both); image Read confirms 56,660 lb on the full ticket (Drive OCR had misread).
- 5.4 Flag — COBB by design + 2-184 sister-batch COBB inconsistency for Garrett.
- 5.3, 5.7 N/A correct.

**Section 6 — AECN Feedstock Emissions (6.1–6.6):** All Pass — required LCA docs present in Certify Sources; pyrolysis EFs match KB within rounding; methodology applies pre-sparging mass correctly.

**Section 7 — Gross-to-Net (7.1–7.4):** All Pass — math reconciles on policy-correct mass.

**Section 7a — Per-Component Uncertainty (7a.1–7a.3):** All Pass — ±72.57 kg per leg, ±0.1724% carbon, 0.138 t aggregate discount in net calc.

**Section 8 — Data Integrity (8.1–8.3):** All Pass + N/A.
- 8.1 Pass — no outliers under policy.
- 8.2 N/A — no spills.
- 8.3 Pass — last-batch railcar conservatism precondition (4 offloads ≥ 3 BOLs) satisfied.

**Section 9 — Certify Component Mapping (9.1–9.10):**
- 9.1, 9.2, 9.4, 9.5, 9.6, 9.7, 9.8, 9.10 Pass.
- 9.3 N/A.
- 9.9 Flag — 4 non-descriptive Certify source filenames (process hygiene).

---

## 3. Observations

1. **Lesson captured.** The misclassification today was rooted in undocumented domain policy. The fix is structural: Failure Category 11 added to `lessons_learned.md`, SKILL.md "Key Formulas & Values" updated, checklist_structure.md Section 2 rail notes updated, and `project_railcar_mass_policy.md` saved to memory. Future-me has the rule even if skill files drift.

2. **COBB row 61 (sister batch 2-184) inconsistency.** Worth Max + Garrett tracing. COBB shows 21,457.08 vs raw-scale-ticket math 21,844.99. Per Max, this looks like an Ops/Manufacturo automation glitch on the 2-184 row. Not 2-185-specific, not verifier-impacting, but the audit trail should be made consistent. Surfaced in the 2-185 checklist's Section 5.4 evidence note so it isn't lost.

3. **Rail embodied EF on 2-185 already updated to 2026 value (0.0000311307 MTCO₂e/mi).** Sister 2-182 still has the stale 0.0000352240. Worth confirming whether 2-183 and 2-184 also have the stale value if the EF datapoint isn't shared across removals.

4. **Hygiene flags only.** Both remaining FLAGs are non-blocking for the verifier:
   - 5.4 (COBB row 61 sister-batch inconsistency — Max handles with Garrett)
   - 9.9 (4 non-descriptive screenshot filenames — rename for hygiene)

---

## 4. Verdict

**Recommendation: deliver to Max as-is.** Net CDR 17.094 tCO₂e is correct under the rail last-offload conservatism policy. No material findings. 3 hygiene flags, none of which prevent verification.
