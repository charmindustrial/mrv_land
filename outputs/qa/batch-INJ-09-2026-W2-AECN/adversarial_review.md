# Gate 3 Adversarial Review — INJ-09-2026-W2 (AECN rail + direct truck), Basco 6, rmv_1M2RKR58N1S0F02M

Reviewer: adversarial-reviewer sub-agent. Date: 2026-09-22.
Inputs: `Batch_INJ-09-2026-W2-AECN_QA_Checklist.xlsx` (57 rows), `batch_INJ-09-2026-W2-AECN_source_reads.json` (the only value source used), `build_checklist.py`, `ops_notes_dump.txt`, `VVB_Guidance_September_1-30_fetched_2026-09-22.txt`, `mass_chain_findings.json`, skill references `lessons_learned.md` and `checklist_structure.md`. No browser, no live registry.

Every number below was recomputed from log values in one script. Each arithmetic line has two operands and one result; running totals are restated in full. Log keys are in `[...]`.

Verdict count: 57 rows. ACCEPT 55. FIX EVIDENCE 1 (row 9.6). CHANGE STATUS 0. Send-back-to-Gate-1 0.

---

## 1. Challenged rows

### Row 2.1 — Fail — verdict ACCEPT

Recomputation of the unevidenced offload (Ops row 33) `[ops_notes.aecn_rail_tab.offload_table]`:
- 74,140 − 28,480 = 45,660 lb
- 45,660 × 0.453592 = 20,711.01072 kg = Ops F33
- 20,711.01072 × 0.0129 = 267.1720383 kg (H33)
- 20,711.01072 − 267.1720383 = 20,443.8386817 kg; 20,443.8386817 × 0.00196 = 40.06992382 kg (I33)
- 20,443.8386817 − 40.06992382 = 20,403.76876 kg MOBI = Ops K33 `[_derived_values.timx_o2_mobi_kg]`
- 20.40376876 × 0.404 = 8.24312258; 8.24312258 × 3.667 = 30.228 tCO2e `[_derived_values.timx_o2_gross_t]`

FC11 railcar-balance test: 25,228.78704 + 20,711.01072 = 45,939.79776; 45,939.79776 + 19,667.74912 = 65,607.54688; 65,607.54688 + 12,192.55296 = 77,800.09984 kg `[_derived_values.timx_offloaded_kg]`; 78,140 − 77,800.09984 = 339.90016 kg `[_derived_values.timx_loss_kg]`. Offloads sum below the BOL total, so no last-offload back-calc applies; the typed D33/E33 are not a policy substitution.
FC14 documented-substitution test: `[vvb_guidance.w2_coverage_check]` reads verbatim: "The document names no INJ-09-2026-W2 offload, railcar TIMX201060 / SHPX215079 / SHPX215046 or truck BOL 2499-T / 2503-T / 2505-T, and contains no standard-tare, missing-ticket or mislabeled-ticket statement." `[ops_notes.cell_comments]` reads "none on Summary, AECN Rail or AECN Truck (openpyxl comment scan)".
Absence is primary-sourced: `[scale_tickets.TIMX201060.offload_2.tickets_found]` = false; Drive API listing `[scale_tickets._primary_source_opened]` items_found = Offload 1, Offload 3, Offload 4; `[certify.scale_tickets_in_sources]` = []; `[certify_sources_enumeration]` = 28 names, none a ticket.
Fail stands: 20,403.76876 kg of Mass of Injectant has no weighing behind it. lessons_learned.md General Principle 7 reads verbatim: "**Missing evidence = FAIL.** No exceptions."

### Row 2.5 — Flag — verdict ACCEPT, one evidence sharpening

Recomputation:
- Ops A44 running sum `[ops_notes.aecn_rail_tab.offload_table]`: 20,810.80096 + 14,841.53024 = 35,652.3312; 35,652.3312 + 21,799.63152 = 57,451.96272; 57,451.96272 + 20,611.22048 = 78,063.1832; 78,063.1832 + 25,228.78704 = 103,291.97024; 103,291.97024 + 20,711.01072 = 124,002.98096; 124,002.98096 + 19,667.74912 = 143,670.73008; 143,670.73008 + 12,192.55296 = 155,863.28304 kg = Ops A44 155,863.283 `[ops_notes.aecn_rail_tab.rollup_row44]` = Certify rail mass 155,863.28 `[certify_components.pyrolysis_process_rail.mass_input.value_kg]`.
- SHPX215046 four-offload sum, Ops basis: 21,055.74064 + 20,992.23776 = 42,047.9784 `[cobb.shpx215046_offloads_1_2]`; 42,047.9784 + 20,810.80096 = 62,858.77936; 62,858.77936 + 14,841.53024 = 77,700.3096 kg; 77,700.3096 − 77,680 = 20.3096 kg `[_derived_values.s46_overage_kg]`.
- Same sum, COBB basis: 62,858.77936 + 14,821.22064 = 77,680.00000 kg; 77,680.00000 − 77,680 = 0.0 `[cobb.shpx215046_four_offload_sum_kg]`.
- 14,821.22064 − 14,841.53024 = −20.3096 kg `[_derived_values.s46_cobb_o4_delta_kg]`; 0.0203096 × 0.404 = 0.00820508; 0.00820508 × 3.667 = 0.0301 tCO2e `[_derived_values.s46_overage_gross_t]`.

FC11 test: the Ops four-offload sum 77,700.3096 does not equal the BOL total 77,680, so the Ops/Certify value is not a policy-applied figure; it is a true-up not yet applied in Ops. This removal's 14,841.53024 kg reconciles to tickets 1124426250546 (61,980 lb) and 1312226251445 (29,260 lb) `[scale_tickets.SHPX215046.offload_4]`: 61,980 − 29,260 = 32,720 lb; 32,720 × 0.453592 = 14,841.53024 kg. The 20.3096 kg over-draw appears when this week's two offloads are added to the two W3 offloads in COBB; it is not visible within this removal's own rows. Value evidenced, cross-week hygiene open, materiality 0.0301 t on 275.193 t: Flag.
Sharpening (no status change): checklist_structure.md row 2.5 rail note reads verbatim: "**For the LAST offload of a railcar**, Charm applies a conservatism rule: if `sum(all offloads' raw scale-ticket Cargo (kg))` exceeds `BOL inbound aggregate` ... the last offload's Cargo (kg) is back-calculated". The log holds this week's ticket dates 2026-09-07 and 2026-09-08 `[scale_tickets.SHPX215046.offload_4.full_ticket.date, .empty_ticket.date]` and COBB completion 2026-09-18 for W3 offloads 1-2 `[cobb.shpx215046_offloads_1_2[].completion_L]`, but no W3 ticket dates. On the dates logged, W3 is the later draw, so COBB placing the true-up on W2 offload 4 is the placement to question. The row may say this; it may not assert W3 ticket dates.

### Row 3.5 — Fail — verdict ACCEPT

Recomputation:
- Direct truck: 2,197 × 3 = 6,591 mi = Ops N25 `[ops_notes.aecn_truck_tab.N25_sum_EE_miles]` = Certify `[certify_components.transport_embodied.AECN_to_LA_direct_truck.distance.value_mi]`.
- AECN–SOPOR map: 173 / 1.609344 = 107.49722 mi `[route_evidence.AECN_to_SOPOR_png.km]`; Certify 107.49722 `[certify_components.transport_process.AECN_to_SOPOR_truck.distance.value_mi]`; Ops 107.5 `[ops_notes.aecn_rail_tab.railcars_received.TIMX201060.aecn_sopor_mi]`.
- Fractions: 77,800.09984 / 78,140 = 0.9956501; 42,410.852 / 77,870 = 0.5446366; 35,652.3312 / 77,680 = 0.4589641 `[_derived_values.timx_offload_fraction, s79_fraction, s46_fraction]`.
- Fraction sum: 0.9956501 + 0.5446366 = 1.5402867; 1.5402867 + 0.4589641 = 1.9992508.
- Truck allocation, Certify basis: 1.9992508 × 107.49722 = 214.91390; 214.91390 × 3 = 644.74171 mi vs Certify 644.74168 `[_derived_values.truck_alloc_recompute_mi]`; 644.74171 − 644.74168 = 0.00003.
- Truck allocation, Ops basis: 1.9992508 × 107.5 = 214.91946; 214.91946 × 3 = 644.75839 = Ops L36 644.7583867 `[ops_notes.aecn_rail_tab.distance_rollup_row36]`; 644.7583867 − 644.74168 = 0.01671 mi `[_derived_values.truck_alloc_delta_mi]`.
- Rail allocation, Certify basis: 2,199 × 0.9956501 = 2,189.4346; 2,199 × 0.5446366 = 1,197.65588; 2,199 × 0.4589641 = 1,009.26205; 2,189.4346 + 1,197.65588 = 3,387.09048; 3,387.09048 + 1,009.26205 = 4,396.35253 mi vs Certify 4,396.35245 `[_derived_values.rail_alloc_massfraction_mi]`; difference 0.00008.
- Rail allocation, Ops basis `[ops_notes.aecn_rail_tab.rail_M_column_note]`: 589.1214123 + 420.1406411 = 1,009.2620534; 1,009.2620534 + 615.6079326 = 1,624.869986; 1,624.869986 + 582.0479496 = 2,206.917936; 2,199 + 2,206.917936 = 4,405.917936 mi = Ops M36; 4,405.917936 − 4,396.35245 = 9.56549 mi `[_derived_values.rail_alloc_delta_mi]`.
- Embodied each basis: 4,405.917936 × 0.03113066508 = 137.16 kg; 4,396.35245 × 0.03113066508 = 136.86 kg `[_derived_values.rail_embodied_basis_calc]`; both display 0.137 t.
- Unallocated share: 2,199 − 2,189.4346 = 9.5654 mi; 9.5654 × 0.03113066508 = 0.298 kg (shown arithmetic). Certify's offloaded-fraction basis leaves TIMX201060's lost 0.435 % of the leg allocated to no removal; Ops' 2,199 for a FULL railcar is the conservative basis. Immaterial; direction noted.
- Opelousas–Basco: 42.9 × 2 = 85.8; 85.8 × 8 = 686.4 mi = Ops N36 = Certify `[_derived_values.opel_basco_allocated_calc]`.

Status test: checklist_structure.md's evidence-attachment gate reads verbatim: "Required-evidence matrix enforced (AECN rail): Mass of Injectant → scale tickets + Ops Notes; Allocated Bio-Oil Mass (pyrolysis + transport basis) → scale tickets + BOLs + Ops Notes; Carbon → lab; Pyrolysis CI → LCA/GHG files; Allocated distances → Ops Notes + Maps; full distances → Maps (rail = Watco); EFs → Standard EF Sheet." `[certify.ops_notes_source_linked_datapoints.not_linked]` lists all three allocated-distance datapoints and both mass datapoints. Required evidence absent from the datapoint is a Fail; and even with the Ops Notes linked, a verifier reproduces 4,405.917936 mi, not Certify's 4,396.35245 mi. FC13: the row names INJ-08-2026 W1/W2 and INJ-09-2026-W1 as the same gap; the Fail status already reflects it.

### Row 6.1 — Fail — verdict ACCEPT

checklist_structure.md Section 6 note reads verbatim: "**Document location rule applies to 6.1-6.3.** Check Drive first, then Certify Sources. Only FAIL if absent from BOTH." Certify Sources enumerated at 28 `[certify_sources_tab_total, certify_sources_enumeration]`; `[certify.lca_supporting_files_in_sources.absent]` = "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jan2026 to 30Jun2026.xlsx" and "Supporting GHG data 30Jun2026 S.xlsx"; Drive root `[drive_folder.root_items]` = Ops Notes, Scale Tickets/, the COA, Kerry Oil/, with every subfolder listed by API `[drive_folder._primary_source_opened]`. Absent from both.
Materiality: I12 = 0.004065098048 + 0.133052027800741 = 0.137117125848741 `[standard_efs.fh_2026_lca_file]`; 0.133052027800741 / 0.137117125848741 = 0.9704 (shown arithmetic) — the vendor input is 97.04 % of the pyrolysis CI and has no derivation document on this removal. Pyrolysis process activities: 21.372 + 8.031 = 29.403 t `[certify.components_tab]`. FC13: `[certify.lca_supporting_files_in_sources.prior_week_had_all_four]` = true. Sister divergence gives Flag at minimum; missing derivation evidence gives Fail.

### Row 6.3 — Fail — verdict ACCEPT

Same rule, same log keys as 6.1 for "Supporting GHG data 30Jun2026 S.xlsx". Embodied side complete: `[certify.attachment_map]` "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)" = "AECN Embodied Emissions Calc Sheet (1).pdf".

### Row 8.1 — Fail — verdict ACCEPT

The contradiction, verbatim from `[ops_notes.aecn_rail_tab.railcars_received.SHPX215046.notes_M]`: "LD3 only candidate CAT ticket (1124426250545, 74,320 lb, 9-07-26) is confirmed mislabeled (printed SHPX215046OFFLOAD3, actually belongs to another car per Garrett); its next-best mass-fit alternative is itself a ticket labeled GPRX5107 (a different, W1 railcar) -- not treated as genuine. LD4 has no resolvable ticket after a wide Gmail harvest. Both LD3 and LD4 Full/Empty left blank pending real tickets." Against it: `[ops_notes.aecn_rail_tab.offload_table]` row 28 full_lb_D = 74320, D_hyperlinked = true; `[scale_tickets.SHPX215046.offload_3.full_ticket.ticket_number]` = "1124426250545".
Mass at stake: 20.50207864 × 0.404 = 8.28283977; 8.28283977 × 3.667 = 30.373 tCO2e `[_derived_values.s46_o3_gross_t]`.
Stale-figure check: M12's "35,632.02" equals COBB offload 3 + offload 4: 20,810.80096 + 14,821.22064 = 35,632.0216 `[cobb.rows]` rows 801-802; Ops F12 = 35,652.3312 `[ops_notes.aecn_rail_tab.railcars_received.SHPX215046.total_offloaded_kg_F]`. M12 was written from COBB values. `[cobb.shpx215046_offloads_1_2]` rows 850-851 show offloads 1-2 do exist in COBB, against M12's "offload_1 and offload_2 do not exist in COBB".
Status: a verifier reading M12 is told the offload-3 evidence is not genuine while row 28 and Certify depend on it; 30.373 t of gross cannot be confirmed. Fail. FC14: guidance quote above covers nothing here.
Log-backed observation for Max: the offload-3 and offload-4 full tickets are consecutive numbers 1124426250545 and 1124426250546 at scale 1244, 10:52 and 10:55 on 2026-09-07, on rigs CH2/KL188 and CH1/KL192 `[scale_tickets.SHPX215046.offload_3.full_ticket, offload_4.full_ticket]`. Two trucks weighed full three minutes apart at Opelousas is consistent with a two-truck draw from one railcar; that favours the tickets being genuine and M12 being wrong. Resolution stays with Garrett.

### Row 9.6 — Flag — verdict FIX EVIDENCE (status stays Flag)

Recomputation from `[standard_efs.rows]` F6 = 0.0001143, F10 = 0.000025910374 and component inputs `[certify_components.transport_process]`:
- P1: 58.570 × 2,197 = 128,678.29; 128,678.29 × 0.0001143 = 14.70793 t
- P2: 155.863283 × 107.49722 = 16,754.86; 16,754.86 × 0.0001143 = 1.91508 t
- P3: 155.863283 × 2,199 = 342,743.36; 342,743.36 × 0.000025910374 = 8.88061 t
- P4: 155.863283 × 42.9 = 6,686.53; 6,686.53 × 0.0001143 = 0.76427 t
- 14.70793 + 1.91508 = 16.62301; 16.62301 + 8.88061 = 25.50362; 25.50362 + 0.76427 = 26.26789 t `[_derived_values.transport_process_sum_precise_t]`; 26.26789 × 1000 = 26,267.89 kg
- 26.187 − 26.26789 = −0.08089 t `[_derived_values.bcu_minus_process_t]`; 0.08089 / 26.26789 = 0.00308 = 0.308 % `[_derived_values.bcu_shortfall_pct]`
Status: under-coverage is the conservative direction. checklist_structure.md 9.6 note reads verbatim: "BCU QA rule — BCU quantity (tCO2e) in Reductions must NOT exceed the corresponding diesel/process emission (tCO2e) in Activities (full coverage = equal; over-coverage launders reductions into removals and is always a FAIL)." Flag is right.
The defect: the row text reads "An input of 26,268 kgCO2e would give full coverage without exceeding it." 26,268 − 26,267.89 = 0.11 kg: it exceeds. 26,267 − 26,267.89 = −0.89 kg: the largest whole-kg input that does not. `[certify_components.bcu_transport.assessment]` already reads "26,267 kg would give full coverage." `[_derived_values.bcu_full_coverage_kg]` = 26268 is wrong. Fix: row text to 26,267 kgCO2e; DERIVED `bcu_full_coverage_kg` to 26267 in `build_checklist.py`.
Log hygiene, same row: `[certify_components.bcu_transport.delta_t]` = −0.08052 (and "80.5 kg") and `[certify_components.transport_process.AECN_to_LA_direct_truck.precise_t]` = 14.7076 disagree with the recomputed −0.08089 and 14.70793. The row uses the correct 80.9 kg; correct the two component-level keys.

### Row 4.4 — Flag — verdict ACCEPT

Identity ties on three fields: `[lab_results.client_id]` = "9-2026-W2-AECN"; `[lab_results.sampled]` = "2026-09-12 07:00" = Ops D18 2026-09-12 `[ops_notes.summary_tab.row18_aecn.D18_date_composited]`; `[lab_results.product_description]` = "Oil - AECN". `[lab_results.location_printed]` = "FORT LUPTON, CO"; `[lab_results.prior_week_certificate.location]` = "BASCO LOUISIANA"; `[lab_results.location_note]` reads "Page 1 (QOWV, Fort Lupton product) prints the same location." Carbon 40.4 `[lab_results.carbon_pct]` = Certify 40.4 `[certify_components.injection_sequestration.carbon_content_input.value_pct]`. Header-field hygiene on a two-product report; value confirmable. Flag.

### Row 7a.2 — Pass — verdict ACCEPT

- 160 × 0.45359237 = 72.5747792 kg; 798.3225712 / 72.5747792 = 11.000 `[certify_components.injection_sequestration.mass_input.uncertainty_kg]`
- 580.56 / 72.57 = 8.000 `[certify_components.pyrolysis_process_rail.mass_input.uncertainty_kg]`; 217.71 / 72.57 = 3.000 `[certify_components.pyrolysis_process_truck.mass_input.uncertainty_kg]`; 8 + 3 = 11
- 11 × 72.57 = 798.27; 798.3225712 − 798.27 = 0.0526 kg `[_derived_values.unc_like_for_like_kg]`
- 0.004 × 40.4 = 0.1616 = displayed 0.16164 `[certify_components.injection_sequestration.carbon_content_input.uncertainty_pct]`
Count matches the per-offload framing: 8 rail offload rows `[ops_notes.aecn_rail_tab.offload_table]` + 3 truck rows `[ops_notes.aecn_truck_tab.deliveries]`. 14 modal artifacts on disk. Pass stands. One of the 8 rail weighings counted (TIMX201060 offload 2) has no ticket; that is the row 2.1 Fail.

---

## 2. Rows confirmed without change

Rows 1.x
- 1.1 Pass — `[drive_folder.folder_id]` = 1Oz-oUtmLMxrMQe7cfyzcLEE5ZUg8qzRh; `[ops_notes.batch_id_B2]` = INJ-09-2026-W2; `[certify.header.period]` = "05 Sep 2026 to 11 Sep 2026".
- 1.2 Flag — `[scale_tickets._summary]` pairs_read 7, tickets_read 14; the missing Offload 2 carries its Fail in 2.1; `[scale_tickets._summary.note_formats]` reads "all fields legible".
- 1.3 Flag — `[drive_folder.testing_subfolder_present]` = false; certificate in root and Certify source 1.
- 1.4 Flag — M12 contradiction (8.1) and linkage gap (3.5), both log-backed `[ops_notes.aecn_rail_tab.railcars_received.SHPX215046.notes_M_contradictions, certify.ops_notes_source_linked_datapoints]`.
- 1.5 Pass — `[bols.destination_check.vaulted_references_found]` = [] with 12 pdf_read entries; 14 component names `[certify.components_tab]` contain no "Vaulted".

Rows 2.x
- 2.2 Pass — ticket dates 2026-09-03 to 2026-09-08 `[scale_tickets.*]`; Ops date 2026-09-11; 11 − 3 = 8 days; `[scale_tickets._summary.empty_after_full_all_pairs]` = true; prior-removal overlap per `[scale_tickets._summary.note_dates]`.
- 2.3 Pass — tractor_match and trailer_match = true on all 7 pairs `[scale_tickets.*.*]`.
- 2.4 Pass — all 8 rows recomputed (D − E) × 0.453592 = F to five decimals, difference 0.000000 on every row; H, I, K tie exactly; sums 155,863.28304 and 153,551.0955 as shown under 2.5.
- 2.6 Pass — 155,863.283 × 0.0129 = 2,010.636351 = D44; 58,570 × 0.0129 = 755.553 = D28 `[ops_notes.aecn_rail_tab.rollup_row44, ops_notes.aecn_truck_tab.rollup_row28]`.
- 2.6a Pass — 155,863.283 − 2,010.636351 = 153,852.646649; 153,852.646649 × 0.00196 = 301.5511875 = E44; 58,570 − 755.553 = 57,814.447; 57,814.447 × 0.00196 = 113.3163161 = E28; `[filtration_constant_source.summary_tab_rows]` reads "Recommended value for filtration loss 0.196%".
- 2.7 Flag — 153,551.0955 + 57,701.13068 = 211,252.22618 = Certify 211,252.2262 `[certify_components.injection_sequestration.mass_input.value_kg]`; the two chain breaks are owned by 2.1 and 2.5.
- 2.8 Pass — 19,710 + 19,190 = 38,900; 38,900 + 19,670 = 58,570 = A28 = Certify `[bols.truck_sum_check]`; `[ops_notes.aecn_truck_tab.methodology_header_A26]` quoted verbatim in the row.

Rows 3.x
- 3.1 Pass — `[bols.truck]` three BOLs pages 1-3; `[certify.attachment_map]` "Bio-Oil Mass - AECN" = BOL_2505-T.pdf, BOL_2503-T.pdf, BOL_2499-T.pdf.
- 3.2 Pass — `[bols.rail]` nine BOLs, all in `[certify_sources_enumeration]`.
- 3.3 Pass — 26,060 + 26,020 = 52,080; 52,080 + 26,060 = 78,140; 25,990 + 25,910 = 51,900; 51,900 + 25,970 = 77,870; 25,940 + 25,900 = 51,840; 51,840 + 25,840 = 77,680 `[bols.rail_sum_check]`; each page-2 qty equals its weigh-slip `[bols.rail.*.aecn_weigh_slip_masse_nette_kg]`.
- 3.4 Pass — `[bols.rail.*.from, .ship_to; bols.truck.*.from, .ship_to]`.
- 3.6 Pass — 8 transport components in `[certify.components_tab]`.
- 3.7 Flag — `[bols.print_oddities]` 2453-R "#0X-2026", 2503-T "#9-2026".

Rows 4.x
- 4.1 Pass — `[lab_results.certificate_number]` = SR26-05494.002; `[lab_results.download_path]` md5 76d0657f0d969e4ec2397cf71ed83434; `[certify.attachment_map]` Carbon Content = the COA and the Ops Notes.
- 4.2 Pass — 40.4 − 39.420350877193 = 0.979649; 0.979649 / 6.09332409018271 = 0.1608 SD; 2 × 6.09332409018271 = 12.18665; 39.420350877193 − 12.18665 = 27.2337; 39.420350877193 + 12.18665 = 51.607 `[lab_results.aecn_stats]`.
- 4.3 Pass — 7.0 − 6.87438596491228 = 0.125614; 0.125614 / 0.562848694875852 = 0.223 SD; N "<0.75"; nitrogen_n_D7 = 9 `[lab_results]`.
- 4.5 N/A — `[oil_type]` = AECN.
- 4.6 Pass — 1.208 > 1.01 `[lab_results.density_g_cm3_at_15C, lab_results.formation_fluid.specific_gravity_g_mL]`.

Rows 5.x
- 5.1 Pass — `[ops_notes.batch_id_B2, week_start_B3, week_end_B4]`.
- 5.2 Flag — ops_full_matches_ticket and ops_empty_matches_ticket = true on 7 rows `[scale_tickets.*.*]`; row 33 has no ticket (2.1).
- 5.3 N/A — no aqueous phase.
- 5.4 Flag — `[cobb.batch_id_col_a]` = INJ-09-2026-W2_bio_oil rows 798-808; 18,956.06327 − 19,190 = −233.93673; 19,593.81362 − 19,710 = −116.18638; 14,821.22064 − 14,841.53024 = −20.3096 `[cobb.rows]`; Certify reconciles to Ops.
- 5.5 Flag — `[cobb.findings.ph]` and `[ops_notes.aecn_truck_tab.pH_blank_all_rows]` = true.
- 5.6 Pass — `[cobb.findings.completion_date]` 2026-09-11 on 11 rows.
- 5.7 N/A — density blank expected for AECN.

Rows 6.x
- 6.2 Pass — 0.004065098048 + 0.133052027800741 = 0.137117125848741 `[standard_efs.fh_2026_lca_file]`.
- 6.4 Pass — `[standard_efs.rows.B4.final_F]` = 0.1371171258; Certify 0.13712; `[standard_efs.h2_2026_aecn_tab.B1_quote]` cited.
- 6.5 Pass — `[standard_efs.rows.B5.final_F]` = 0.02116 = Certify.
- 6.6 Pass — `[certify_components.pyrolysis_process_rail.mass_input.value_kg]` 155,863.28 and `[...pyrolysis_process_truck.mass_input.value_kg]` 58,570, both pre-sparging.

Rows 7.x
- 7.1 Pass — 211.25222618 × 0.404 = 85.3458994; 85.3458994 × 3.667 = 312.963 = Certify `[certify_components.injection_sequestration.value_tCO2e]`.
- 7.2 Pass — 21.372 + 3.298 = 24.670; 24.670 + 8.031 = 32.701; 32.701 + 1.239 = 33.940; 33.940 + 28.286 = 62.226 = Components tab `[certify.components_tab.Emitted_total_t]`; calc view 62.227 `[certify.calculation_view.activities_tCO2e]`.
- 7.3 Pass — discount 1.730 present `[certify.calculation_view.uncertainty_discount_t]`; 1.730 / 312.963 = 0.005528. Sanity check with a formula of my own, not from the log, no status weight: 798.3225712 / 211,252.2262 = 0.0037790; 0.0037790² = 0.00001428; 0.004² = 0.000016; 0.00001428 + 0.000016 = 0.00003028; √0.00003028 = 0.005503; 0.005503 × 312.963 = 1.722 t, against 1.730.
- 7.4 Flag — `[rp_status.september_2026_rp_open]` = true.
- 7a.1 Pass — 14 modal artifacts; `[certify_components.transport_embodied.*.mass_input]` = "none (per-mile blueprint)"; `[certify_components.transport_process.distance_uncertainty]` = "none shown on any of the 4 legs (expected)".
- 7a.3 Pass — 312.963 + 26.187 = 339.150; 339.150 − 62.227 = 276.923; 276.923 − 1.730 = 275.193 `[certify.calculation_view.recalc]`.

Rows 8.x
- 8.2 Pass — 78,140 − 77,800.09984 = 339.90016 kg; 339.90016 / 78,140 = 0.00435; `[vvb_guidance.august_railcar_loss_band_quote]` reads "Every other railcar offloaded in the same week falls between -101.75 kg and +480.59 kg."; `[vvb_guidance.spill_check]` reads "Neither guidance document discloses a spill involving TIMX201060, SHPX215079 or SHPX215046."
- 8.3 Flag — prev_claimed_kg and prior_rp_claimed_kg = 0 on all three `[ops_notes.aecn_rail_tab.railcars_received]`; W3 completion 2026-09-18 `[cobb.shpx215046_offloads_1_2]`; `[vvb_guidance.multi_week_quote]` cited verbatim in the log.
- 8.4 Pass — 4 × 72.57 = 290.28; 3 × 72.57 = 217.71 `[rail_uncertainty_precondition.TIMX201060]`.

Rows 9.x
- 9.1 Pass — same chain as 7.1.
- 9.2 Pass — process 26.26789 as shown under 9.6; embodied: 6,591 × 0.0002375605888 = 1.56576; 644.74168 × 0.0002375605888 = 0.15317; 4,396.35245 × 0.00003113066508 = 0.13686; 686.4 × 0.0002375605888 = 0.16306; 1.56576 + 0.15317 = 1.71893; 1.71893 + 0.13686 = 1.85579; 1.85579 + 0.16306 = 2.01885; 26.267 + 2.019 = 28.286 `[certify.components_tab.Bio-oil_transport_activities_subtotal_t]`; 65.37439668 / 2,100,000 = 0.00003113066508 `[standard_efs.railcar_ee_tab]`.
- 9.3 N/A — `[certify.components_tab.injection_side_activity_components]` = [].
- 9.4 Pass — 155.863283 × 0.1371171258 = 21.3715; 58.570 × 0.1371171258 = 8.0310; 155.863283 × 0.02116 = 3.2981; 58.570 × 0.02116 = 1.2393; Certify 21.372 / 8.031 / 3.298 / 1.239 `[certify.components_tab]`.
- 9.5 Pass — `[certify_components.bcu_transport.input.value_kgCO2e]` = 26187; certificate fields per `[certify_components.bcu_transport.certificate]`.
- 9.7 Pass — `[certify.calculation_view]` has no counterfactual term.
- 9.8 Pass — 275.193 reproduced under 7a.3; `[certify.calculation_view.cross_tab_rounding_gap_t]` = 0.001.
- 9.9 Flag — `[certify.generic_filenames]` = "image (44).png"; lessons_learned.md reads verbatim: "Generic or non-descriptive filenames are a FLAG, not a FAIL."
- 9.10 Flag — `[certify.scale_tickets_in_sources]` = []; `[certify.lca_supporting_files_in_sources.absent]` two files.

---

## 3. Observations outside the rows

1. **Deterministic mass-chain script did not run on this batch shape.** `mass_chain_findings.json` reports every check as INSUFFICIENT_DATA or SKIP, with notes verbatim "Not a railcar batch." and "No offload_table row matching offload=None." The log's `scale_tickets` block is keyed railcar → offload_N, which the script does not read. Every chain above rests on hand math plus this review's recompute; all reconcile, but the tooling gap should be closed before the next weekly.
2. **Log-internal inconsistencies to correct** (no status effect): `certify_components.transport_process.AECN_to_LA_direct_truck.precise_t` 14.7076 → 14.70793; `.sum_precise_t` 26.26752 → 26.26789; `certify_components.bcu_transport.delta_t` −0.08052 → −0.08089 and "80.5 kg" → 80.9 kg; `_derived_values.bcu_full_coverage_kg` 26268 → 26267 (row 9.6).
3. **COBB order-line timestamp precedes the TIMX201060 weighings.** `[cobb.rows]` rows 805-808 order_line_completed_on_I = "2026-08-27 20:02:19"; the four tickets are dated 2026-09-03 and 2026-09-04 `[scale_tickets.TIMX201060.*]`. Row 5.6 tests injection_completion_date_L (2026-09-11), which ties. Provenance oddity for Garrett.
4. **Certify's rail allocation drops the lost mass's share of the leg**: 9.5654 mi, 0.298 kg embodied (arithmetic under 3.5). Ops' M32 = 2,199 for a FULL railcar is the conservative convention; settle which basis Ops and Certify share when 3.5 is fixed.
5. **TIMX201060 offload 1 gross 85,100 lb.** `[scale_tickets._summary.note_timx_o1_gross]` reads "net 55,620 lb = 25,228.79 kg against 42,860-48,540 lb nets on the other six evidenced offloads." Ticket read directly; arithmetic ties; railcar balance closes at 339.90016 kg loss. Not a finding; recorded so it is not re-raised.
6. **Viscosity 14.69 cSt this week vs 269.4 cSt the prior week** `[lab_results.kinematic_viscosity_cSt_40C, lab_results.prior_week_certificate.kinematic_viscosity_cSt_40C]`; density 1.208 vs 1.219. Not a mass or carbon input; carried as an observation in 8.1. If this and the Fort Lupton header (4.4) share a cause at the lab, the carbon value would come into question; the log holds no evidence either way, so nothing is asserted.
7. **Truck BOL 2499-T dated 2026-08-31** `[bols.truck.2499-T.date_page1]`, before the period opens 05 Sep; COBB order line 2026-09-09 `[cobb.rows]` row 800. Transit time. No action.
