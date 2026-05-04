# Batch 2-186 — Adversarial Review

**Reviewer:** qa-adversarial-reviewer (log-driven, FC10 Citation Discipline Rule 2)
**Date:** 2026-04-30
**Scope:** Every Item 1.1–9.10 in `Batch_2-186_QA_Checklist.xlsx`, cross-checked against `batch_2-186_source_reads.json`, knowledge base, and Isometric protocols.
**Batch context:** AECN rail, railcar TIMX201060, offload 1 of 4 (NOT last batch). Net CDR 30.27 tCO2e. BOL aggregate 80,610 kg vs total offloaded 71,010 kg → 9,600 kg railcar-wide gap, deferred to 2-188 (last) QA.

---

## Per-item verdicts

### Section 1 — Batch Folder Completeness

- **Item 1.1: Confirm** — `[log:batch_folder_contents]` present, Drive folder URL recorded in `_meta.drive_folder_url`. PASS justified.
- **Item 1.2: Confirm** — `[log:scale_tickets.full_ticket.filename_drive, scale_tickets.empty_ticket.filename_drive]` both recorded. One offload pair correct for offload_1. *Minor*: evidence note cites file sizes (2.4 MB / 2.5 MB) — Failure Category 3 explicitly bans file metadata as evidence. Suggest revision: drop the MB sizes; values from the JPGs already do the work.
- **Item 1.3: Confirm** — `[log:lab_results.filename, lab_results.page_for_2_186, lab_results.certificate_id]` present. PASS justified.
- **Item 1.4: Confirm** — `[log:ops_notes.filename_drive]` present. Rail naming convention noted. PASS justified.
- **Item 1.5: Confirm** — `[log:lab_results.location_on_page]` = "BASCO LOUISIANA". PASS justified. Note: this is a thin source — the strongest evidence for "no Vaulted refs" would be Ops Notes / BOL inspection, which the log doesn't independently enumerate. Not material — Certify project name + CHN location together suffice.

### Section 2 — Scale Tickets & Mass Determination

- **Item 2.1: Confirm** — `[log:scale_tickets.full_ticket, scale_tickets.empty_ticket]` show `read_method: "image Read (NOT Drive OCR)"`, axle sums match gross on both tickets (77,560 = 10,000+33,760+33,800; 29,380 = 9,520+11,640+8,220). PASS justified.
- **Item 2.2: Confirm** — Full 2026-03-31, empty 2026-04-01, injection 2026-04-03. Within 14 days. `[log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.completion_date]`.
- **Item 2.3: Confirm** — Tractor CH2 / Trailer KL-188 match. `[log:scale_tickets.tractor_match, scale_tickets.trailer_match]`.
- **Item 2.4: Suggest revision** — PASS verdict is correct (this is offload_1, last-offload policy does NOT apply, raw scale-ticket math controls). HOWEVER the evidence note's stated arithmetic is slightly wrong: it cites `(77,560 - 29,380) / 2.20462 = 21,854.06256`, but `48,180 / 2.20462 = 21,854.10638`. The Ops Notes value 21,854.06256 actually comes from `48,180 × 0.453592` (the multiplier convention recorded in `[log:ops_notes.batch_composition.lbs_to_kg_factor]` = 0.453592). Both end up at the same number to ~4 decimal places, but the cited formula doesn't reproduce the cited result. Suggest revising note to: "(77,560 − 29,380) lb × 0.453592 kg/lb = 21,854.06256 kg" to match Ops Notes' actual arithmetic.
- **Item 2.5: Confirm** — Per FC11, the conservatism rule for rail batches is last-offload-only; for offload_1 the raw scale-ticket value is the basis. PASS correctly justified. `[log:scale_tickets.net_calc_kg, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg]`. (Same minor formula-arithmetic nit as 2.4 if it appears, but 2.5's note doesn't repeat the formula.)
- **Item 2.6: Confirm** — 0.0129 × 21,854.06256 = 281.9174 kg, injectate 21,572.14515 kg. Independently reproduced. `[log:ops_notes.batch_composition.sparging_mass_loss_fraction, ops_notes.trucks_unloaded_offload_1.sparging_loss_kg, ops_notes.trucks_unloaded_offload_1.mass_of_bio_oil_injected_kg]`.
- **Item 2.7: Confirm** — `[log:certify_datapoints.Allocated Bio-Oil Mass - AECN via Rail]` = 21.854 t = scale ticket = Ops Notes = COBB. Four-source agreement verified. (Same arithmetic-formula nit as 2.4 if you want consistency.)

### Section 3 — Bills of Lading & Transportation

- **Item 3.1: Confirm** — All 3 inbound BOLs present in `[log:certify_sources_tab_enumeration, BOLs_present_check]`. The 2314-T filename typo is correctly cross-referenced into 9.9. PASS with explicit hand-off.
- **Item 3.2: Confirm** — `[log:cobb_row.BOL_number]` = "2314-R, 2316-R, 2317-R" matches `[log:ops_notes.BOLs_loaded]`. PASS justified.
- **Item 3.3: Confirm** — Sum of 3 BOLs = 26.05 + 29.06 + 25.50 = 80.61 MT = 80,610 kg. Reproduced. Per-railcar comparison correct. `[log:ops_notes.BOLs_loaded, ops_notes.total_loaded_mass_kg]`.
- **Item 3.4: Confirm** — Three-leg origin/destination trail documented. `[log:cobb_row.BOL_number, ops_notes.BOLs_loaded]`. Slight wordsmithing nit: the destination of the 3 inbound BOLs is technically SOPOR/Baie-Comeau railyard (not "AECN→Opelousas"); this is just narrative phrasing in the note, not an evidence problem.
- **Item 3.5: Confirm** — All three legs cited with allocated-vs-full distance distinction (per Section 3.5 QA pattern from 2-185). Allocated AECN→SOPOR truck = 87.43 mi (= 322.5 × 0.2711, reproduced 87.4327 ✓), allocated rail = 596.17 mi (= 2199 × 0.2711, reproduced 596.169 ✓), Opelousas→Basco truck = 42.9 mi full (per-batch, no allocation). `[log:certify_datapoints, ops_notes.batch_composition, ops_notes.trucks_unloaded_offload_1.upstream_allocation_fraction]`. PASS.
- **Item 3.6: Confirm** — All 6 transport components enumerated with values. `[log:certify_components]`. PASS.
- **Item 3.7: Confirm** — Three billing/BOL files in Sources, plus Charm-A5 manifest. `[log:certify_sources_tab_enumeration]`. PASS.

### Section 4 — Bio-Oil Composition & Testing

- **Item 4.1: Confirm** — `[log:lab_results.filename, lab_results.page_for_2_186, lab_results.certificate_id]` complete.
- **Item 4.2: Confirm** — Carbon 42.0% within mean ±2 SD (27.2%–51.6%). `[log:lab_results.carbon_pct, lab_results.carbon_within_AECN_range]`.
- **Item 4.3: Confirm** — All five additional lab fields cited from log. `[log:lab_results.hydrogen_pct, lab_results.nitrogen_pct, lab_results.viscosity_cSt_at_40C, lab_results.acid_number_mgKOH_per_g, lab_results.density_g_per_cm3_at_15C]`.
- **Item 4.4: Confirm** — `client_id_on_page = "BATCH 2-186"`. `[log:lab_results.certificate_id, lab_results.client_id_on_page, lab_results.sample_date]`.
- **Item 4.5: Confirm N/A** — AECN, not aqueous.

### Section 5 — Ops Notes Accuracy & Internal Consistency

- **Item 5.1: Confirm** — Date triple-match verified. `[log:ops_notes.batch_number, ops_notes.completion_date, cobb_row.injection_completion_date]`.
- **Item 5.2: Confirm** — Loaded 77,560 = full ticket; unloaded 29,380 = empty ticket; cargo (kg) = 21,854.06256 matches Ops Notes. (Same arithmetic-formula nit as 2.4: the 21,854.06256 figure comes from ×0.453592, not /2.20462 — note cites both implicitly, fine in practice.) `[log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, ops_notes.trucks_unloaded_offload_1.loaded_mass_lb, ops_notes.trucks_unloaded_offload_1.unloaded_mass_lb, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg]`.
- **Item 5.3: Confirm N/A** — AECN-only.
- **Item 5.4: Confirm FLAG** — Framing is exactly right: per-batch values for 2-186 reconcile cleanly (offloaded_quantity_kg, BOL_number, pH, completion date all match Ops Notes); the COBB origin_quantity_kg = 71,010 (= sum of all 4 sister offloads, reproduced: 21854.06 + 21736.13 + 21799.63 + 5620.18 = 71,010.0 ✓) vs BOL aggregate 80,610 = 9,600 kg gap is railcar-wide, NOT 2-186-impacting. Correctly deferred to 2-188 (last-offload) QA. The "_redo_" suffix observation is appropriate Garrett-visibility metadata. **Per FC11**: this is correctly being flagged (not failed) because the per-batch math reconciles. **Per FAIL/FLAG decision rule** ("would a VVB reviewer be unable to confirm THIS removal's value?"): No — 2-186's per-batch chain is intact, so FLAG is the correct severity. `[log:cobb_row_id_verified, cobb_cell_A_value, cobb_row, cobb_origin_vs_BOL_aggregate_discrepancy, ops_notes.note_redo_in_lot_name]`.
- **Item 5.5: Confirm** — pH 2.9 in both Ops Notes and COBB. `[log:ops_notes.trucks_unloaded_offload_1.ph, cobb_row.injection_ph]`.
- **Item 5.6: Confirm** — Date match. `[log:ops_notes.completion_date, cobb_row.injection_completion_date]`.
- **Item 5.7: Confirm N/A** — AECN density blank by protocol.

### Section 6 — AECN Feedstock Emissions & Allocation

- **Item 6.1: Confirm** — `Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx` present. H2 2025 vintage correct for Apr 2026 batch (semi-annual EFs are H2 2025 until H1 2026 publishes). `[log:certify_sources_tab_enumeration, AECN_LCA_doc_check.AECN_LCA_CI_spreadsheet]`.
- **Item 6.2: Confirm** — `BH 2025 LCA w Stack Emissions.xlsx` present. `[log:certify_sources_tab_enumeration, AECN_LCA_doc_check.LCA_with_stack_emissions]`.
- **Item 6.3: Confirm** — `Supporting GHG data 31Dec2025 S.xlsx` present. `[log:certify_sources_tab_enumeration, AECN_LCA_doc_check.supporting_GHG_data]`.
- **Item 6.4: Confirm** — Modal value 0.104 t/t, KB 0.10402, independent calc 21854.06 × 0.10402 / 1000 = 2.27326 t = Certify 2.273 t ✓. `[log:certify_datapoints.Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail), math_verification.AECN_pyrolysis_process]`.
- **Item 6.5: Confirm** — Modal 0.02116, calc 21854.06 × 0.02116 / 1000 = 0.46243 t = Certify 0.462 t ✓. `[log:certify_datapoints.Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail), math_verification.AECN_pyrolysis_embodied]`.
- **Item 6.6: Confirm** — Mass basis = "Allocated Bio-Oil Mass - AECN via Rail" = 21,854.06 kg = pre-sparging. Sparging deducted only from sequestration's Mass of Injectant. Methodology correct. `[log:certify_datapoints.Allocated Bio-Oil Mass - AECN via Rail, certify_uncertainty_modals.AECN pyrolysis (from rail loads) - process emissions]`.

### Section 7 — Gross-to-Net Calculation

- **Item 7.1: Confirm** — Independent calc: 21.572 × 0.420 × 3.667 = 33.221 t ≈ Certify 33.224 t (delta 0.003 = rounding). Reproduced. `[log:math_verification.gross_co2e_calc, certify_components.Injection Sequestration]`.
- **Item 7.2: Confirm** — All 8 activity components enumerated with values; each math-reconciles independently (per my own recompute: truck1 process 0.2685 ≈ 0.269; rail process 1.2452 ≈ 1.245; truck3 process 0.1072 ≈ 0.107; truck1 embodied 0.0208 ≈ 0.021; rail embodied 0.0186 ≈ 0.019; truck3 embodied 0.0102 ≈ 0.010; pyro process 2.273; pyro embodied 0.462; sum = 4.406). `[log:certify_components, math_verification]`.
- **Item 7.3: Confirm** — 174 kg discount reproduced via variance propagation (sqrt(0.336² + 0.4²) × 33.224 = 0.1734 t → rounds to 0.174). `[log:certify_components.totals.uncertainty_discount_t, math_verification.uncertainty_discount_check]`.
- **Item 7.4: Confirm** — 33.224 − 4.405 + 1.621 − 0.174 = 30.266; with full-precision activities 4.406, net = 30.265; both round to 30.27 displayed. `[log:certify_components.totals, math_verification.net_calculation]`.

### Section 7a — Per-Component Uncertainty Verification

- **Item 7a.1: Confirm** — All 6 mass-input components show ±72.57 kg per `[log:certify_uncertainty_modals]`: Injection Sequestration (Mass of product), AECN→SOPOR Truck Process, SOPOR→Opelousas Rail Process, Opelousas→Basco Truck Process, AECN Pyrolysis Process, AECN Pyrolysis Embodied. The 3 embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs). Carbon Content uncertainty 0.168% = 42 × 0.004 ✓. PASS justified.
- **Item 7a.2: Confirm** — Per FC9, per-batch removal is fixed by ONE outbound discrete weight at Basco offload → ±72.57 kg per leg is correct on every leg including rail. The N_offloads ≥ N_BOLs precondition (4 ≥ 3 for TIMX201060) is referenced as deferred to 2-188 — this is consistent with the lessons_learned.md guidance that the formal Section-8 last-batch check belongs to the railcar's last batch, with the precondition pre-confirmed at sister-batch list level. PASS.
- **Item 7a.3: Confirm** — Discount 0.174 t present in net formula and consistent with per-input variance propagation. `[log:certify_components.totals.uncertainty_discount_t]`.

### Section 8 — Data Integrity & Anomaly Check

- **Item 8.1: Confirm** — Carbon, distances, EFs, masses all in expected ranges. Notably: rail embodied EF 0.03113 kgCO2e/mi is the NEW 2026 value, resolving the 2-182 stale-EF FAIL. `[log:lab_results.carbon_pct, certify_components, math_verification]`.
- **Item 8.2: Confirm** — No spills; offload_1 correctly leaves Oil Left in Railcar blank (railcar still active). `[log:ops_notes.oil_left_in_railcar_blank_offload_1_not_last]`.
- **Item 8.3: Confirm FLAG** — Sister-batch table records 4 offloads (2-186 / 2-187 / 2-189 / 2-188 = offloads 1/2/3/4). N_offloads = 4 ≥ N_inbound_BOLs = 3 ✓ — per-offload uncertainty framing is conservative for the railcar (locks in the FC9 precondition). Allocation fraction sum reproduced: 0.27111 + 0.26964 + 0.27044 + 0.06972 = 0.88091 (NOT 1.0). 1 − 0.88091 = 0.11909, × 80,610 = 9,600 kg gap exactly — this matches the COBB-vs-BOL gap surfaced in 5.4. **The framing is correct**: this offload's per-batch chain is intact, the 9,600 kg gap is railcar-wide, and the formal reconciliation belongs at 2-188 last-offload QA. FLAG (not FAIL) is appropriate per the FAIL/FLAG decision rule (a VVB can confirm 2-186's reported value; the railcar-wide gap doesn't invalidate this batch). `[log:ops_notes.sister_batches_railcar_TIMX201060, ops_notes.total_offloaded_kg_railcar, ops_notes.BOL_aggregate_minus_total_offloaded_kg, rail_batch_specific_checks]`.

### Section 9 — Isometric Certify Removal Component Mapping

- **Item 9.1: Confirm** — Sequestration 33.224 t reproduced. `[log:certify_components.Injection Sequestration, math_verification.gross_co2e_calc]`.
- **Item 9.2: Confirm** — All 6 components present; rail embodied EF 0.03113 = NEW 2026 value (vs stale 0.03522 in 2-182). The "stale-EF FAIL resolved" framing correctly references the sister-batch finding. Independent calc: 596.17 mi × 0.03113 kgCO2e/mi = 18.56 kgCO2e = 0.01856 t → rounds to Certify 0.019 t ✓. `[log:certify_uncertainty_modals.SOPOR to Opelousas Rail Transport Embodied Emissions, math_verification.rail_embodied]`.
- **Item 9.3: Confirm N/A** — AECN, no LCS.
- **Item 9.4: Confirm** — Both pyrolysis components present with rail-batch naming. `[log:certify_components]`.
- **Item 9.5: Confirm** — Only Transport BCU category applicable for non-site-emission-burdened AECN rail. `[log:certify_components.BCUs - Applied to Bio-Oil Transport Process Emissions]`.
- **Item 9.6: Confirm** — BCU 1.621 = 0.269 + 1.245 + 0.107 exactly. Embodied not BCU-eligible (per protocol). `[log:math_verification.BCU_offset_check]`.
- **Item 9.7: Confirm** — Counterfactuals = 0 per protocol. `[log:certify_components.Counterfactuals]`.
- **Item 9.8: Confirm** — Net 30.266 t (displayed 30.27). Reproduced. `[log:certify_components.totals, math_verification.net_calculation]`.
- **Item 9.9: Confirm FLAG** — 4 non-descriptive screenshot/image filenames + the "2314-T" filename typo. FLAG (not FAIL) per KB rule that generic filenames are hygiene, not reporting. Note the 2314-T typo is internal-consistency hygiene: the BOL number in COBB and the body of the document (presumably) reads 2314-R, only the filename differs. `[log:non_descriptive_filenames_for_FLAG_section_9_9, BOLs_present_check.filename_typo_2314_T_vs_2314_R]`.
- **Item 9.10: Confirm** — 23 source-row instances enumerating 19 distinct files (Ops Notes linked × 4, Standard EFs PDF linked × 2). All Appendix-1 docs accounted for via Sources tab (Document Location Rule). `[log:certify_sources_tab_total, certify_sources_tab_enumeration, AECN_LCA_doc_check]`.

---

## Summary

### Items that should change status

**None.** All 50 PASS, 3 FLAG, 4 N/A, 0 FAIL classifications survive log-driven challenge.

### Items needing minor evidence-note revision (not status changes)

1. **2.4** — Cited arithmetic `(77,560 − 29,380) / 2.20462 = 21,854.06256` is wrong. The actual conversion is `× 0.453592` per Ops Notes' `lbs_to_kg_factor` (recorded in `[log:ops_notes.batch_composition.lbs_to_kg_factor]`). `/2.20462` yields 21,854.10638; only `× 0.453592` yields 21,854.06256. Both round to the same value to 2 decimal places, but the formula-and-result mismatch is a citation-discipline weakness. Suggest: replace `/ 2.20462` with `× 0.453592` everywhere it appears. Same nit may apply to 2.5, 2.7, 5.2 if they reproduce the formula (5.2 cites the value but not the operation; 2.7 cites the value only).
2. **1.2** — Drop file-size (MB) citations (FC3 anti-pattern). Image content already does the work.

### FC10 confabulation flags

**None.** Every status cites a `[log:KEY]` that exists in `batch_2-186_source_reads.json`, and every quoted value matches the log.

### FC9 / FC11 misframings

**None.** Section 5.4 and 8.3 correctly defer railcar-wide reconciliation (9,600 kg gap, allocation-fraction sum 0.881 vs 1.0) to 2-188 last-offload QA, while preserving 2-186's per-batch integrity. Section 7a correctly applies per-removal framing (±72.57 kg per leg) with N_offloads ≥ N_BOLs precondition pre-confirmed (4 ≥ 3) and formal Section-8 check deferred to 2-188 — exactly the path the framework prescribes.

### What Max should look at first

1. **Section 5.4 + 8.3 — the 9,600 kg railcar-wide gap.** Per-batch integrity is fine for 2-186 and the FLAG framing is correct, but the gap is real and material at the railcar level. The "_redo_" suffix in the consumed_lot name (`Rail_TIMX201060_2.27.26_redo_offload_1`) suggests an operational reset of some kind on this railcar that the prior GPRX 5188 didn't have. Whether this is heel/residue, a logged loss, a BOL-mass-vs-actual-loaded discrepancy at AECN, or a data-entry quirk on COBB/Ops Notes is the open question. **2-188 (offload_4 = last batch) is where this resolves**, and 2-186's checklist correctly hands it off — but it's worth Max's eyes now since (a) batches 2-187, 2-189, 2-188 will all carry the same flag in their checklists, and (b) if the gap is *not* documented heel, sister-batch upstream allocation fractions are computed against an unverified BOL-aggregate denominator (currently 80,610 kg) when the more honest denominator might be 71,010 kg (total offloaded), which would push every sister batch's transport allocation higher.
2. **Item 2.4 arithmetic citation** — purely a citation-discipline polish item, not material.
3. **Resolved sister-batch finding for the record:** Rail embodied EF on 2-186 = 0.03113 kgCO2e/mi (NEW 2026 value), confirming the 2-182 stale-EF FAIL was a one-time issue and does not propagate to 2-186 or other 2026 rail batches.

### Pre-delivery audit script note

Running `scripts/audit_checklist.py` against this checklist should return zero failures based on log presence and value matches; the only caveat is the 2.4 formula notation, which the audit script may not catch (it would catch wrong VALUES, not wrong OPERATORS leading to a coincidentally correct value). Manual fix recommended.
