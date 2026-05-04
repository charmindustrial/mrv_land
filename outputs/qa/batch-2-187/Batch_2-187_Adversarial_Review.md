# Batch 2-187 — Adversarial QA Review

**Batch:** 2-187 (AECN rail, railcar TIMX201060, consumed_lot offload_2 of 4 — NOT last offload of railcar)
**Site:** Basco 6
**Certify removal:** rmv_1KQB5JF7Q1S0GN9C
**Net CDR:** 29.48 tCO₂e (29.476 precise)
**Reviewer (adversarial):** Claude QA Adversarial Reviewer
**Date:** 2026-05-01

QA agent counts: Pass=51, Fail=0, Flag=2, N/A=4.

---

## Step 0 — Primary Source Verification Check

**All Section 2 / Section 5 / Section 7a items pass primary-source verification.**

- **Scale ticket items (2.1, 2.3):** Evidence cites specific axle weights (10,200 / 33,920 / 33,780 / sum 77,900 lb on Full; 9,500 / 11,820 / 8,660 / sum 29,980 lb on Empty), weigh numbers (#0762 / #1778), dates (3-31-26 / 4-01-26), location (Pilot Travel Center I-49 Exit 40, Bunkie LA, scale #3122), tractor (CH1) and trailer (KL-192). These details are not present in Ops Notes or COBB and could only be obtained by reading the JPG images directly. Confirmed via `scale_tickets.full_ticket` and `scale_tickets.empty_ticket` log entries — JPGs were downloaded to `.playwright-mcp/2-187-Full-Scale-Ticket.jpg` and `.../2-187-Empty-Scale-Ticket.jpg` and Read directly (NOT Drive OCR snippet, per OCR-vs-image memory rule). ✓

- **COBB items (5.4, 5.6):** Tab named explicitly in log (`tab_name: "Basco Injection -- COBB"`), row 64 cited, `cobb_row_id_verified: true` and `cobb_cell_A_value: "2-187"` present. Specific cell values cited (offloaded_quantity_kg = 21,736.12864, BOL_number = "2314-R, 2316-R, 2317-R", origin_quantity_kg = 71,010 stale, pH = "33" typo, injection_completion_date = 2026-04-03). Sister-batch rows 63/65/66 also enumerated. ✓

- **Uncertainty modal items (7a.1, 7a.2):** Each of the 9 component modals was opened individually (URLs captured in Playwright transcript: cmp_1KQB5JF7Q1S0CTNP, cmp_1KQB5JF7Q1S0KKMH, cmp_1KQB5JF7Q1S078G6, cmp_1KQB5JF7Q1S0TXBV, cmp_1KQB5JF7Q1S0EJ7G, cmp_1KQB5JF7Q1S02735, cmp_1KQB5JF7Q1S0NVYT, cmp_1KQB5JF7Q1S09GTF, cmp_1KQB5JF7Q1S0X5P4, cmp_1KQB5JF7Q1S0DBE5). The INPUTS section of each modal was read and ± values extracted and recorded in `certify_components.components_detail`. ✓

No primary-source verification failures.

---

## Step 1 — Item-by-Item Independent Validation

I independently re-ran the math against the source-read log values:

| Check | Independent Result | Certify Value | Δ |
|---|---|---|---|
| Scale ticket net (lb) | 77,900 − 29,980 = 47,920 lb | Ops Notes 47,920 | 0 ✓ |
| Cargo (kg) | 47,920 × 0.453592 = 21,736.12864 kg | Ops Notes 21,736.12864 | 0 ✓ |
| Sparging loss | 21,736.12864 × 0.0129 = 280.39606 kg | Ops Notes 280.396 | 0 ✓ |
| Mass injected | 21,736.12864 − 280.39606 = 21,455.73258 kg | Certify 21,455.73 | < 0.001 kg ✓ |
| Gross CO₂e | 21,455.73258 × 0.412 × 3.667 = 32.4154 t | Certify 32.415 t | 0.0004 t ✓ rounding |
| AECN→SOPOR truck process | 21.73613 × 107.5 × 0.0001143 = 0.26708 t | Certify 0.267 | 0.0001 t ✓ |
| Rail process | 21.73613 × 2199 × 0.0000259104 = 1.23846 t | Certify 1.238 | 0.0005 t ✓ |
| Opelousas→Basco process | 21.73613 × 42.9 × 0.0001143 = 0.10658 t | Certify 0.107 | 0.0004 t ✓ |
| Opelousas→Basco embodied | 42.9 × 0.00023756059 = 0.01019 t | Certify 0.010 | 0.0002 t ✓ |
| Rail embodied | 592.95062 × 0.0000311307 = 0.01846 t | Certify 0.018 | 0.0005 t ✓ |
| AECN→SOPOR embodied | 86.96 × 0.00023756059 = 0.02066 t | Certify 0.021 | 0.0003 t ✓ |
| Pyrolysis process | 21.73613 × 0.10402 = 2.26099 t | Certify 2.261 | 0.000 t ✓ |
| Pyrolysis embodied | 21.73613 × 0.02116 = 0.45994 t | Certify 0.460 | 0.0001 t ✓ |
| Activities total | sum = 4.38236 t | Certify 4.382 | 0.0004 t ✓ |
| BCU offset | sum of 3 transport process = 1.61212 t | Certify 1.612 | 0.0001 t ✓ |
| Net | 32.4154 − 4.3824 + 1.6121 − 0.170 = 29.4752 | Certify 29.476 | 0.001 t ✓ |
| Sister-batch sum (COBB pre-correction) | 21,854.06 + 21,736.13 + 5,620.18 + 21,799.63 = 71,010.00 kg | COBB origin_quantity_kg 71,010 | 0 ✓ |
| Allocation fraction | 21,736.12864 / 80,610 = 0.26964556 | Ops Notes 0.26964556 | 0 ✓ |
| Rail allocated mi | 2199 × 0.26964556 = 592.95059 | Certify 592.95062 | < 0.0001 mi ✓ |
| Carbon ± | 41.2 × 0.004 = 0.1648% | Certify ±0.1648% | 0 ✓ |
| Mass ± per discrete weight | 72.57 kg (FC9 per-removal framing) | Certify ±72.57 kg on every mass datapoint | 0 ✓ |

**Every reconciliation check confirms the QA agent's findings.**

---

## Challenged Items

**None — no items recommended for status change.**

---

## Confirmed Items (with verification)

### Section 1 — Batch Folder Completeness

- **1.1 Pass — Confirmed:** Drive folder id `1FZKcMtZYmalLB8J3QAcBtR1ecvfHOxkO` resolves to "2-187" per Drive breadcrumb (parent "4/1/26-4/5/26"). Folder inventory matches log (`Testing/`, `Scale Tickets/`, `2-187 Ops Notes Rail`).
- **1.2 Pass — Confirmed:** Two JPGs (`2-187 Full Scale Ticket.jpg` 2.9 MB, `2-187 Empty Scale Ticket.jpg` 2.7 MB) both correspond to offload_2 (the batch's only offload per COBB row 64). Sister batches' tickets live in their own folders by design.
- **1.3 Pass — Confirmed:** SR26-02264.pdf is a single 7-page CoA covering 2-186 → 2-189 + 3-55 → 3-57. Page 2 explicitly labeled "BATCH 2-187". Verified by direct PDF read.
- **1.4 Pass — Confirmed:** Ops Notes Rail file id `1RnVQ7KR1E-u5VBtdlvM2o3B-2sfBHE25yZJLRnRJD7w` accessible; TSV export captured all sections: Batch Composition, BOLs Loaded, offload table.
- **1.5 Pass — Confirmed:** No Vaulted references anywhere; CHN page 2 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco).

### Section 2 — Scale Tickets & Mass Determination

- **2.1 Pass — Confirmed:** Both ticket JPGs Read directly. Full: weigh #0762, axle sum 10,200 + 33,920 + 33,780 = 77,900 lb. Empty: weigh #1778, axle sum 9,500 + 11,820 + 8,660 = 29,980 lb. Both internally consistent.
- **2.2 Pass — Confirmed:** Full 2026-03-31; Empty 2026-04-01; injection completion 2026-04-03 — within 3 days, well inside 14-day window.
- **2.3 Pass — Confirmed:** Tractor CH1 / Trailer KL-192 on both tickets — same vehicle weighed at both events. (Note: differs from sister batch 2-186 which used CH2/KL-188 — different physical truck for different offload, expected.)
- **2.4 Pass — Confirmed:** Independent math: (77,900 − 29,980) × 0.453592 = 47,920 × 0.453592 = **21,736.12864 kg** = Ops Notes Cargo (kg) exactly. Non-last-offload, so no policy back-calc applies. ✓
- **2.5 Pass — Confirmed:** Per-offload rail batch (non-last); scale-ticket math is the authoritative basis for THIS batch (BOL aggregate of 80,610 kg is railcar-level, not per-offload). 21,736.13 kg is the correct injectate basis.
- **2.6 Pass — Confirmed:** 21,736.12864 × 0.0129 = 280.39606 kg sparging loss. Mass injected = 21,455.73258 kg. Ops Notes shows these to 5 decimal places exactly.
- **2.7 Pass — Confirmed:** Mass = 21,736.12864 kg in scale tickets (computed) = Ops Notes Cargo (kg) = COBB row 64 offloaded_quantity_kg = Certify "Allocated Bio-Oil Mass - AECN via Rail" 21.736 t. All four sources align to 5+ decimal places.

### Section 3 — Bills of Lading & Transportation

- **3.1 Pass — Confirmed:** All 3 inbound BOLs in Certify Sources (`Documents camion 2317-R.pdf`, `Billing Truck 2316-R.pdf`, `Billing Truck 2314-T Corrections (1).pdf`). 2314-T filename typo correctly deferred to 9.9 hygiene flag.
- **3.2 Pass — Confirmed:** 3 BOLs (2314-R, 2316-R, 2317-R) listed in COBB row 64 BOL_number field and in Ops Notes BOLs Loaded section.
- **3.3 Pass — Confirmed:** BOL aggregate 26.05 + 29.06 + 25.50 = **80.61 MT** (post-correction); offload mass 21.736 MT < 80.61 MT railcar inbound. Rail-batch railcar-level check.
- **3.4 Pass — Confirmed:** Three legs documented: AECN Quebec → SOPOR (3 truck BOLs), SOPOR → Opelousas (rail), Opelousas → Basco (per-batch truck).
- **3.5 Pass — Confirmed:** Three legs verified with both full + allocated distances. Independent math: 322.5 mi total trucking × 0.26964556 = 86.96069 mi (allocated AECN→SOPOR) — matches Ops Notes/Certify; 2199 × 0.26964556 = 592.95059 mi (rail allocated) — matches Certify modal value 592.95062 mi. Opelousas→Basco truck = 42.9 mi (full per-batch).
- **3.6 Pass — Confirmed:** All 6 transport components present (AECN→SOPOR truck process+embodied, rail process+embodied, Opelousas→Basco truck process+embodied) with correct values listed in `certify_components.components_detail`.
- **3.7 Pass — Confirmed:** Billing/BOL docs for all 3 inbound legs in Certify Sources; Charm-A5 BCU certificate also present.

### Section 4 — Bio-Oil Composition & Testing

- **4.1 Pass — Confirmed:** SR26-02264.pdf in Drive Testing AND CHN-186-189.pdf in Certify Sources (alias). Page 2 = SR26-02264.002 = "BATCH 2-187".
- **4.2 Pass — Confirmed:** Carbon 41.2% within AECN range mean 39.42% ± 2 SD (~27.2%-51.6%). The range itself is documented in KB Section 4.2 with sample size n=285 (March 2026 update).
- **4.3 Pass — Confirmed:** Hydrogen 6.9%, Nitrogen <0.75%, Viscosity 22.04 cSt @ 40°C, Acid # 46 mg KOH/g, Density 1.212 g/cm³ @ 15°C — all reported (specific values cited from CHN page 2). Values within typical AECN ranges per KB Section 3.
- **4.4 Pass — Confirmed:** Certificate SR26-02264.002 explicitly labeled "BATCH 2-187" on page 2; sample 2026-04-02 04:45 at Basco LA — sample taken AFTER offload_2 truck arrived (2026-04-01 per Empty ticket) and BEFORE injection completion (2026-04-03). Timing logical.
- **4.5 N/A — Confirmed:** AECN is not aqueous phase; pH belongs in Section 5.5 per checklist_structure.md.

### Section 5 — Ops Notes Accuracy & Internal Consistency

- **5.1 Pass — Confirmed:** Ops Notes Rail batch number "2-187", completion 4/3/2026 — match Certify removal date and COBB injection_completion_date.
- **5.2 Pass — Confirmed:** Loaded 77,900 lb / Unloaded 29,980 lb match scale ticket axle sums exactly. Cargo 21,736.12864 kg matches scale-ticket math exactly. ✓
- **5.3 N/A — Confirmed:** AECN-only batch; no aqueous phase reconciliation applicable.
- **5.4 Flag — Confirmed both flagged issues:**
  - **(a) origin_quantity_kg = 71,010 stale.** Verified: 71,010 + 9,600 (BOL correction) = 80,610 = Ops Notes Total Loaded Mass. Sister-batch sum across all 4 COBB rows (63-66) = exactly 71,010.00 = pre-correction aggregate. COBB rows pre-date the 9.6 MT correction documented on 2-186's flag (2026-04-30). Garrett-side data-provenance issue.
  - **(b) pH "33" typo.** Verified: log `cobb.pH_in_cobb_raw = "33"` vs `ops_notes.pH_offload_2 = 3.3`. Garrett-side typo; Ops Notes value is correct and is what the verifier reads.
  - Verifier-impact: NONE — verifier reads Ops Notes / Certify (both correct). Both correctly classified as FLAG (process hygiene, not material misstatement) per FAIL/FLAG decision rule.
- **5.5 Pass — Confirmed:** Ops Notes offload_2 pH = 3.3.
- **5.6 Pass — Confirmed:** Three sources align: Ops Notes 4/3/2026, COBB 2026-04-03, Certify 03 Apr 2026.
- **5.7 N/A — Confirmed:** Density blank for AECN per protocol — expected behavior.

### Section 6 — AECN Feedstock Emissions & Allocation

- **6.1 Pass — Confirmed:** "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present at Sources tab item 15 (per log enumeration). Vintage H2 2025 covers Apr 2026 reporting (H2 2025 EFs carry forward through Q1 2026).
- **6.2 Pass — Confirmed:** "BH 2025 LCA w Stack Emissions.xlsx" present at item 17.
- **6.3 Pass — Confirmed:** "Supporting GHG data 31Dec2025 S.xlsx" present at item 18.
- **6.4 Pass — Confirmed:** Modal value 0.104 tCO₂e/t; KB precise value 0.10402 tCO₂e/t. Independent calc: 21,736.13 × 0.10402 / 1000 = 2.26099 t = Certify 2.261 ✓.
- **6.5 Pass — Confirmed:** Modal value 0.02116 tCO₂e/t. Independent calc: 21,736.13 × 0.02116 / 1000 = 0.45994 t = Certify 0.460 ✓.
- **6.6 Pass — Confirmed:** Pyrolysis EFs applied to "Allocated Bio-Oil Mass - AECN via Rail" = 21,736.13 kg = pre-sparging Cargo. Mass-of-Injectant (post-sparging 21,455.73 kg) is used only by the Injection Sequestration component. Methodology correct per KB Section 6.6.

### Section 7 — Gross-to-Net Calculation

- **7.1 Pass — Confirmed:** 21,455.73 × 0.412 × 3.667 = 32,415.41 kg = 32.4154 t. Matches Certify Sequestrations 32.415 t to within rounding (Certify likely uses the precise 21,455.73258 kg without further rounding, yielding 32,415.17 kg). ✓
- **7.2 Pass — Confirmed:** Activities sum 4.382 t verified independently component-by-component (see math table above). All 8 components present.
- **7.3 Pass — Confirmed:** 0.170 t discount present in Calculation View. Per S3.7.3 Option B Variance Propagation, Certify computes the aggregate from per-component ± inputs. QA scope = verify INPUTS (covered in Section 7a); aggregate computation is Certify's responsibility. Magnitude (0.5% of gross) reasonable and consistent with sister batch 2-186 (also ~0.5%).
- **7.4 Pass — Confirmed:** Net = 32.415 + 1.612 − 4.382 − 0.170 = 29.475 ≈ Certify 29.476 (displayed 29.48). Reconciles within rounding.

### Section 7a — Per-Component Uncertainty Verification

- **7a.1 Pass — Confirmed Layer 1 (Completeness):** All 6 mass-input components (Injection Sequestration + 3 transport process + 2 pyrolysis) carry ±72.57 kg per the modals opened. 3 embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, per FC8 methodology). Carbon Content uncertainty ±0.1648% verified.
- **7a.2 Pass — Confirmed Layer 2 (Correctness):** Per FC9 per-removal framing, ±72.57 kg per discrete weight is correct on every leg (1 outbound weighing fixes the per-batch removal mass). Carbon ±0.4% relative = ±0.1648% absolute = 41.2 × 0.004 ✓. Conservatism precondition (N_offloads ≥ N_inbound_BOLs) deferred to railcar's last batch QA — appropriate since 2-187 is mid-drawdown.
- **7a.3 Pass — Confirmed Layer 3 (Discount presence):** 0.170 t aggregate discount visible in net formula and sized appropriately.

### Section 8 — Data Integrity & Anomaly Check

- **8.1 Pass — Confirmed:** All values within expected ranges. Notably: rail embodied EF 0.0000311307 MTCO₂e/mi (= 0.03113 kg/mi = 0.0193 kg/km) — this is the 2026 corrected value from the Standard EFs sheet's `2026 Railcar Embodied Emissions` tab (65.37 MT CTGate ÷ 2.1M mi lifetime). Confirmed NOT the stale 0.0000352240 value that 2-182 originally carried (which was flagged on 2-182 and presumably updated since).
- **8.2 Pass — Confirmed:** No spills/losses; "Oil Left in Railcar" cells correctly blank for non-last offload. Last-offload reconciliation belongs to the railcar's final batch QA.
- **8.3 Pass — Confirmed deferral:** 2-187 is offload_2 (per consumed_lot suffix) of 4 — sister batches 2-188 / 2-189 still pending. Per Max's 2026-04-30 note on 2-186, 2-189 is the actual physical 4th/last pull (consumed_lot suffix doesn't match physical sequence). FC9 conservatism precondition (N_offloads ≥ N_inbound_BOLs) will be formally validated at the railcar's last batch. The deferral framing is correct because there is no last-offload mechanic active on 2-187 — this is independent of the railcar's eventual close-out.

### Section 9 — Isometric Certify Removal Component Mapping

- **9.1 Pass — Confirmed:** Certify Sequestration 32.415 t exactly matches independent calc.
- **9.2 Pass — Confirmed:** All 6 transport components present, EFs correct (0.1143 truck process / 0.0259 rail process / 0.23756 truck embodied / 0.03113 rail embodied — all in native per-mile units, matching KB 2026 values). Allocation fraction 0.26964556 correctly uses corrected BOL aggregate 80,610 kg as denominator.
- **9.3 N/A — Confirmed:** AECN does not require LCS pre-treatment.
- **9.4 Pass — Confirmed:** Both pyrolysis components present using rail-batch naming convention "AECN pyrolysis (from rail loads) - process emissions" / "...embodied emissions".
- **9.5 Pass — Confirmed:** Only "BCUs - Applied to Bio-Oil Transport Process Emissions" applies (no site-emission-burdened categories needed for typical AECN rail batch).
- **9.6 Pass — Confirmed:** BCU 1.612 t = exact sum of 3 transport process activities (0.267 + 1.238 + 0.107 = 1.612). BCU ≥ activity rule satisfied (here exactly equal). Embodied transport (0.049 t) correctly NOT BCU-offset.
- **9.7 Pass — Confirmed:** Counterfactuals = 0.
- **9.8 Pass — Confirmed:** Net 29.476 t reconciles with all inputs.
- **9.9 Flag — Confirmed both issues:**
  - **4 generic Certify filenames** (`image (44).png`, `Screenshot 2026-04-10 at 3.19.33 PM.png`, `Screenshot 2026-02-23 at 11.29.10 AM.png`, `Screenshot 2026-01-27 125934.png`) — same shared rail-batch datapoint sources flagged on 2-185, 2-186. These propagate because they're shared datapoint sources, not per-batch-uploaded files.
  - **`Billing Truck 2314-T Corrections (1).pdf`** filename has "-T" where COBB lists "2314-R" — likely a filename typo. The file is the AECN BOL correction document referenced on 2-186 flag (which renamed it to a corrected BOL aggregate of 80.61 MT). Same 2314-T flag carried on 2-186.
  - Both correctly classified as FLAG (process hygiene; content correct).
- **9.10 Pass — Confirmed:** All 23 source rows enumerated in log; all required Appendix 1 docs present (3 BOLs, AECN LCA CI, LCA w Stack Emissions, Supporting GHG data, Standard EFs Railcar Embodied PDF, Charm-A5 BCU certificate, scale tickets, CHN, Ops Notes, route maps, Truck Embodied EF source, AECN Process Emissions Calculation).

---

## Observations (out-of-scope but noted)

1. **Ops Notes "Trucks Unloaded" table shows TWO populated offload rows (offload_1 + offload_2).** Per checklist_structure.md, rail Ops Notes can show multiple offload rows; "Verify only the populated row(s) for THIS batch's offload number — unpopulated rows are zero by design and not a problem." Here BOTH offload_1 AND offload_2 are populated. The QA agent correctly identified that 2-187 = offload_2 only (per COBB row 64 mapping; Certify Allocated Bio-Oil Mass = 21,736.13 kg matches offload_2 only, NOT the running tally of 43,590.19 kg). The offload_1 row in 2-187's Ops Notes belongs to sister batch 2-186 — it's a running railcar tally artifact. This is *not* a checklist issue but worth flagging as an operational observation: a less-careful verifier could potentially read the "Total Unloaded Mass = 43.59 MT" at the bottom of the Ops Notes and conflate it with this batch's mass. The Allocated Bio-Oil Mass datapoint in Certify (21.736 t) is unambiguous, so verifier-impact is nil — but Garrett may want to clarify Ops Notes layout.

2. **2-189's currently-recorded mass in COBB (21,799.63 kg)** is pre-correction policy-capped per Max's 2026-04-30 note on 2-186. With corrected BOL 80,610 and pulls to date, 2-189's correct Cargo should be ≈ 31.4 MT — not 21.8 MT. This is operational debt for 2-189's QA, not 2-187-impacting (2-187 is independent of last-offload mechanics).

3. **Comparison to 2-186 (the immediately prior batch on this railcar):** Both batches reach the same overall conclusion (0 FAIL, 2 FLAG, no material findings); both flag the same 4 generic Certify filenames + 2314-T typo (shared datapoints); both flag COBB-side data-provenance issues. The 2-187-specific addition is the COBB pH "33" typo (vs Ops Notes 3.3). The QA agent has consistently applied the FAIL/FLAG decision rule, the FC11 last-offload policy framing, and the FC9 per-removal uncertainty framing across both sibling batches. No methodology drift observed.

---

## Verdict

**No challenges. All 51 Pass / 2 Flag / 4 N/A status assignments confirmed with primary-source-grounded evidence and reproducible math.**

The QA agent's findings are accurate. The 2 FLAGs are correctly classified (process hygiene, not material misstatement). The 4 N/As are correctly justified by oil type / batch type. The Net CDR of 29.48 tCO₂e is correctly calculated and supported by the evidence. Section 8.3's deferred last-offload check is appropriate framing for a non-last rail batch.

**Recommendation:** Proceed to Gate 4 (audit script + finalization).
