# Batch 2-201 Adversarial Review

**Reviewer:** qa-adversarial-reviewer
**Date:** 2026-05-06
**Checklist counts under review:** 51 Pass / 0 Fail / 2 Flag / 4 N/A
**Net CDR (Certify):** 30.58 t (Calc View precise: 30.584 t)

---

## Step 0: Primary Source Verification Check

| Source class | Required evidence | Status |
|---|---|---|
| Scale tickets (2.1, 2.3, 5.2) | Both JPGs Read directly with tractor/trailer/weights extracted | PASS — log records direct image read of both JPGs; tractor "CH 2", trailer "KL188", axle sums 83060/29200 lb, weighmaster "Marsha Castille" all present. I independently re-read both screenshots and confirm. |
| COBB tracker (5.4, 5.6) | Specific tab + row with cell values | PASS — row 88 of "Basco Injection -- COBB" tab named, all key cell values (A,C,E,F,G,H,I,L,M,Q) extracted from openpyxl read of downloaded XLSX. |
| Component uncertainty (7a.1, 7a.2) | ± values from each modal INPUTS section | PASS — all 9 component modals opened individually, ±72.57 kg per discrete weight and ±0.1532% Carbon recorded with sources_count for each. |

Step 0 satisfied. No reject-on-source-discipline.

---

## Step 1: Per-Item Status & Evidence Review

### Challenged Items

#### Item 9.2 — ACTIVITIES Transport, AECN→SOPOR Truck Process intermediate value
- **Item:** 9.2 (transport components recalc detail)
- **Current Status:** Pass
- **Issue:** The evidence note states `24.43046 t × 107.5 mi × 0.0001143 MTCO2e/(t·mi) × 1000 kg/t = 300.21 kg = 0.300 t`. My independent calc: 24.43046512 × 107.5 × 0.1143 = **300.18 kg**, not 300.21 kg. The 300.21 figure traces to using rounded mass 24.4326 t, not 24.43046 t. Discrepancy is 0.03 kg (0.01%) and rounds to the same 0.300 t Certify display, so the Pass status is still defensible — but the quoted intermediate is internally inconsistent with the precise mass quoted alongside it.
- **Recommendation:** Keep Pass. Tighten the evidence note to read `300.18 kg = 0.300 t` so the inline math is reproducible. This is a cosmetic precision fix, not a status change.

(All other intermediate recalcs in 9.2 reconcile within ≤0.03 kg of my recomputation: rail process 1391.42 kg vs quoted 1391.39, truck embodied AECN→SOPOR 24.44 kg vs quoted 24.43, rail embodied 21.84 = quoted 21.84, Opelousas→Basco truck embodied 10.19 = quoted 10.19, Opelousas→Basco truck process 119.79 = quoted 119.79.)

#### Item 9.9 — BCU certificate filename pattern flagged inside hygiene FLAG
- **Item:** 9.9
- **Current Status:** Flag (covering 4 generic filenames + 2 filename-vs-datapoint mismatches + BCU cert pattern question)
- **Issue:** The FLAG correctly captures the hygiene set, but rolls in a non-hygiene question — whether `Charm-A4-2024-10-24-63-1976.pdf` is the right BCU cert for *this* railcar. That is a substantive accounting question (correct cert pulled?), not a filename-hygiene observation. Evidence already confirms the BCU quantity 1.811 t = exact transport-process sum, so quantity is correct; the open question is provenance. This is fine as a FLAG sub-bullet but should be called out separately so Garrett can resolve it without conflating it with the screenshot-naming work.
- **Recommendation:** Keep FLAG; in the Hygiene flags summary, split bullet (d) out of the filename-hygiene set into its own one-liner: "BCU cert provenance question — `Charm-A4-2024-10-24-63-1976.pdf` reused across TILX200231, TIMX201060, and TILX200228 batches; quantity matches process transport sum exactly, but Garrett should confirm this is the correct cert for THIS railcar's transport offset (not a catch-all)." No status change.

### Items Verified — Confirmed

For each item below I re-derived the load-bearing claim and confirm it.

- **1.1** Drive folder structure correct; Ops Notes Google Sheet, Scale Tickets subfolder (Full + Empty JPG), empty Testing subfolder, lab cert in shared parent + Certify Sources. Confirmed.
- **1.2** Both scale ticket JPGs present in Drive; image pixels read directly (per OCR-not-primary rule); both also in Certify Sources. Confirmed.
- **1.3** Lab cert "2-199 - 2-201.pdf" page 3 = batch 2-201 (.003); Document Location Rule satisfied via Certify Sources presence. Confirmed.
- **1.4** Ops Notes header (batch 2-201, completion 4/23/2026), 3 BOLs (25.57+25.48+25.53=76.58 MT), offload_1 row populated with allocation 0.319019 — internal math reconciles. Confirmed.
- **1.5** Lab cert location BASCO LOUISIANA, no Vaulted refs anywhere. Confirmed.
- **2.1** Re-read both JPG screenshots directly: Full ticket #1312226107061 axle sum 10000+36460+36600=83060 lb = certified gross; Empty ticket #1312226107064 axle sum 9420+11620+8160=29200 lb = certified gross. Both at PILOT TRAVEL CENTER scale 3122, dated 4-17-26, weighmaster Marsha Castille. Confirmed.
- **2.2** Both tickets 4-17-26, injection 4/23/2026 = 6 days later, well within 2-week window. Confirmed.
- **2.3** Tractor CH 2 / Trailer KL188 on both tickets; Empty ticket "TICKET # OF FULL $ WEIGH" field = 1312226107061, paired weighing confirmed. Confirmed.
- **2.4** Net = (83060−29200) × 0.453592 = 53860 × 0.453592 = 24430.4666 kg ≈ Ops Notes 24430.46512 (within rounding). FC11 correctly noted as not applicable (offload_1, not last). Confirmed.
- **2.5** Conservatism per railcar: 24430.47 (this batch) + 5805.98 (sister 2-204 last offload) + offloads 2/3 pending = 30236+pending vs 76580 BOL aggregate envelope. FC11 framing correctly deferred to last batch. Confirmed.
- **2.6** 24430.46512 × 0.0129 = 315.153 kg sparging; 24430.46512 − 315.153 = 24115.31212 kg injectate. Math exact. Confirmed.
- **2.7** Scale 24430.47 kg = Ops Notes 24430.46512 = Certify modal 24430.46 t. Post-sparging 24115.31 = modal 24115.31. COBB divergence pointer to 5.4 correctly handled. Confirmed.
- **3.1** All 3 inbound BOLs in Drive AECN BOLs folder + Certify Sources rows 9/10/11. Confirmed.
- **3.2** 3 -R BOLs match COBB row 88 BOL_number field; destination SOPOR/Société du port ferroviaire de Baie-Comeau confirmed in BOL formal pages. Confirmed.
- **3.3** 25,570 + 25,480 + 25,530 = 76,580 kg = Ops Notes total = COBB H = Loads tab 76.58 MT. Four-source match. The 2346-R header-vs-transaction 160 kg delta correctly handled (Ops Notes uses gravimetric 25.53). Confirmed.
- **3.4** Origin (BioEnergie AE Côte-Nord, Port-Cartier) → SOPOR → rail TILX200228/Watco → Opelousas → Basco. Confirmed.
- **3.5** Distance reconciliation correct: AECN→SOPOR 107.5 mi × 1.609344 = 173.00 km (matches Certify 173.00); allocated 102.88 mi × 1.609344 = 165.57 km (matches Certify modal 165.57); rail 2199 mi full / 701.52 mi allocated; Opelousas→Basco 42.9 mi (no allocation needed for per-batch leg). Conversions explicitly documented per memory unit-conversion-discipline rule. Confirmed.
- **3.6** 6 transport components present, all values correct; sum 1.867 t = bio-oil transport total. Confirmed.
- **3.7** PC0038196/PC0038224/PC0038229 weighing receipts serve as BOL+billing; BCU cert #14 also present. Confirmed.
- **4.1** Multi-batch SGS PDF (SR26-02683.001/.002/.003) page 3 = 2-201 batch ID; Authorised Signatory Jacqualine Kilday. Confirmed.
- **4.2** C 38.3% within AECN range (mean 39.42%, SD 6.09%, n=285, 2-SD = 27.2–51.6%); 38.3% is −0.18 SD. KB Section 7.2 source verified: `AECN mean = 39.42%, SD = 6.09% (n=285 MRV samples, source: MRV_AECN_Analysis.xlsx, updated March 2026)` — line 506 of `Charm_Isometric_Knowledge_Base.md`. Hash flag explained correctly (method-range notation, not finding). Confirmed.
- **4.3** H 7.8%, N <0.75%, viscosity 9.820 cSt, acid number 44 mgKOH/g, density 1.201 g/cm³ — all in normal AECN range. Confirmed.
- **4.4** Cert SR26-02683.003, CLIENT ID = "BATCH 2-201", sampled 18-Apr-2026 (1 day after offload), location BASCO LOUISIANA. Confirmed.
- **4.5** N/A correct — AECN is not aqueous.
- **5.1** Ops Notes batch 2-201, completion 4/23/2026 = Certify removal 23 Apr 2026. Confirmed.
- **5.2** Full 83060 lb = Ops Notes Loaded Mass; Empty 29200 lb = Ops Notes Unloaded Mass; net kg matches. Confirmed.
- **5.3** N/A correct — AECN-only.
- **5.4** FLAG correctly placed. Independently verified the placeholder claim: 76580 / 4 = **19145.0 exactly** — confirms placeholder equal-split origin. Divergence 24430.47 − 19145 = **5285.47 kg** matches log. Direction: COBB *under-states* offloaded mass by 5285 kg vs Ops Notes; Verifier impact correctly noted as none (Certify modal Allocated Bio-Oil Mass = 24430.46 reads from Ops Notes, not COBB). FC11 correctly distinguished from this pattern. Confirmed.
- **5.5** Ops Notes pH 2.9 = COBB row 88 M = 2.9. Sister 2-204 pH 3.01 also normal. Confirmed.
- **5.6** Three-way date match (Ops Notes, COBB col L, Certify); col I (order_line_completed_on) correctly identified as Manufacturo timestamp, not injection. Confirmed.
- **5.7** N/A correct — density blank for AECN per protocol.
- **6.1, 6.2, 6.3** All three LCA documents present in Certify Sources rows 15/17/18 with correct datapoint links. Confirmed.
- **6.4** Modal 0.104 tCO2e/t, KB precise 0.10402 tCO2e/t. Independent recalc: 24.43046 × 0.10402 = 2.5413 t (vs 2.541 displayed; matches to display precision). Confirmed.
- **6.5** Modal 0.02116 tCO2e/t, KB rounded 0.0212. 24.43046 × 0.02116 = 0.5169 t (matches 0.517 displayed). Confirmed.
- **6.6** Mass basis = pre-sparging Allocated Bio-Oil Mass 24430.46 kg per FC; not post-sparging. Confirmed.
- **7.1** Independent gross sequestration: 24115.31 × 0.383 × 3.667 / 1000 = **33.86902 t** → rounds to 33.869 t = Certify Sequestrations. Confirmed.
- **7.2** All 8 activity components sum (display): 0.300+1.391+0.120+0.024+0.022+0.010+2.541+0.517 = **4.925 t** (Calc View shows 4.926 from Certify's full-precision aggregation; 0.001 t rounding gap correctly noted). Confirmed.
- **7.3** Discount 170 kg = 0.170 t = 0.50% of gross / 0.56% of net. Per-component ± inputs (±72.57 kg / ±0.1532%) verified in Section 7a. Confirmed.
- **7.4** Net = 33.869 + 1.811 − 4.926 − 0.170 = **30.584 t** = Certify Calc View 30.584 (displayed 30.58). Independent recalc exact. BCU 1.811 = exact process-transport sum (0.300+1.391+0.120). Confirmed.
- **7a.1** All 6 mass-input components show ±72.57 kg; embodied transport components correctly have NO mass input (per-mile EFs). Carbon ±0.1532% = 38.3 × 0.004. Confirmed.
- **7a.2** Per-removal ±72.57 kg = single outbound discrete weight. Correct per FC9. Confirmed.
- **7a.3** 170 kg aggregate discount in Calc View; net formula and verification arithmetic exact. Confirmed.
- **8.1** No outliers; carbon −0.18 SD; mass 24.43 MT in upper third of typical AECN per-truck range; 2026 corrected rail embodied EF 0.0193 kg/km (not stale 0.0000352240). Confirmed.
- **8.2** No spills. Cargo (kg) reflects clean truck-out. Confirmed.
- **8.3** **FC9 N_offloads ≥ N_inbound_BOLs precondition correctly handled.** N_offloads = 4 (this railcar), N_inbound_BOLs = 3 → 4 ≥ 3 ✓ precondition met. FC11 last-offload back-calc correctly noted as not applicable to 2-201 (offload_1, not last). I confirm: there is no edge case where FC11 should fire on offload_1 — last-offload conservatism is a remainder-pull arithmetic check, by definition runs only on the railcar's last batch (which here is 2-204 per its 5805.98 kg small-remainder signal). Confirmed.
- **9.1** Sequestration 33.869 t with full-precision carbon; modal inputs Mass 24115.31 ±72.57, Carbon 38.3 ±0.1532. Confirmed.
- **9.2** 6 transport components — see Challenged Items above (cosmetic precision fix on truck-process intermediate); status remains Pass.
- **9.3** N/A correct — AECN no LCS.
- **9.4** Pyrolysis process 2.541 + embodied 0.517 = 3.058 t total. Modal EFs 0.104 / 0.02116 verified. Rail-batch naming convention correct. Confirmed.
- **9.5** BCU adjustments only applies to bio-oil transport process. Confirmed.
- **9.6** BCU 1.811 t = sum of 3 transport process components (0.300+1.391+0.120 = 1.811 exact). Embodied transport 0.024+0.022+0.010 = 0.056 t correctly NOT BCU-eligible. Confirmed.
- **9.7** Counterfactuals = 0 per protocol. Confirmed.
- **9.8** Net 30.584 = Calc View display. Independent verification exact. Confirmed.
- **9.9** FLAG (see Challenged Items above for sub-bullet split recommendation). Coverage of 4 generic filenames (Screenshot 2026-04-10, Screenshot 2026-02-23, Screenshot 2026-01-27, image (44).png), 2 filename-vs-datapoint mismatches (Standard EF Railcar Embodied for the PROCESS datapoint, AECN Process Emissions Calc.xlsx for the EMBODIED datapoint), and BCU cert pattern question is complete. Confirmed scope; recommend the cosmetic split.
- **9.10** All 23 Sources tab entries enumerated and Appendix 1 docs (3 BOLs, AECN LCA CI, LCA w Stack, Supporting GHG, AECN Process Emissions Calc, Standard EFs Railcar Embodied, BCU cert, scale tickets, CHN PDF, Ops Notes ×4) all present. Confirmed.

---

## VR Appendix 1 Document-Presence Confirmation

Re-checked from Sources tab enumeration:

- AECN LCA CI spreadsheet: row 15 `Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx` ✓
- LCA with Stack Emissions: row 17 `BH 2025 LCA w Stack Emissions.xlsx` ✓
- Supporting GHG data: row 18 `Supporting GHG data 31Dec2025 S.xlsx` ✓
- 3 BOLs: rows 9, 10, 11 (2346-R, 2345-R corr, 2344-R corr) ✓
- CHN PDF: row 5 `2-199 - 2-201.pdf` ✓
- Scale tickets: rows 7 (Empty), 8 (Full) ✓
- BCU cert: row 14 `Charm-A4-2024-10-24-63-1976.pdf` ✓

All required Appendix 1 documents present.

---

## Final Verdict: **ACCEPT WITH MINOR CHANGES**

The checklist is substantively correct: 51 Pass / 0 Fail / 2 Flag / 4 N/A. All math reconciles within rounding. Both FLAGs are appropriately scoped (Garrett-side, not verifier-impacting). All 4 N/A classifications are protocol-correct for an AECN rail batch.

The two recommended changes are cosmetic / clarity-only and do not affect any status:

1. **Item 9.2 evidence note:** Change `300.21 kg` to `300.18 kg` for the AECN→SOPOR Truck Process intermediate to match the precise mass 24.43046 t quoted alongside it. (Impact: zero on final 0.300 t.)

2. **Hygiene flags summary (item 9.9):** Split the BCU-cert provenance question (bullet d) out of the filename-hygiene set and present it as a separate one-liner so Garrett can confirm the correct BCU cert was pulled for THIS railcar. (Impact: zero on quantity 1.811 t which is verified exact.)

No status downgrades, no missed Fails, no unsupported claims. Ready for Max's review after the two cosmetic edits.
