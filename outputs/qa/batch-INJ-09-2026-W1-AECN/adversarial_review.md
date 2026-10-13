# Adversarial Review — Batch INJ-09-2026-W1 (AECN), Basco 6, rmv_1M2GBNMY91S0H2MB

Reviewer: adversarial reviewer (Gate 3). Date: 2026-09-17.
Scope: every row of `Batch_INJ-09-2026-W1-AECN_QA_Checklist.xlsx`, checked against `batch_INJ-09-2026-W1-AECN_source_reads.json`, `build_checklist.py`, `VVB_Guidance_August_1-31_fetched_2026-09-17.txt`, and the skill references `lessons_learned.md` / `checklist_structure.md`. No browser, no live registry. Every arithmetic chain in every Pass/Fail/Flag row was recomputed from logged values; each recomputation is shown in two-operand steps.

---

## 1. Challenged rows

### 2.5 — Injectate mass uses the conservative value
**Current status: Fail. Verdict: ACCEPT the Fail; FIX EVIDENCE — the correction it prescribes is too wide and the effect is understated.**

Recomputed from `ops_notes.aecn_rail_tab.offload_table` and `.rollup_row44`:

- Σ F28:F35 (scale-ticket nets) = 155,681.84624 kg; Σ J = 16.89584 kg. Scale basis: 155,681.84624 − 16.89584 = 155,664.9504 kg (`_derived_values.rail_scale_net_sum_kg`, `.rail_mass_used_scale_basis_kg`). Confirmed.
- A44 = 155,880 kg (the six loading BOLs); C44 = 155,880 − 16.89584 = 155,863.1042 kg. Confirmed.
- Overstatement of Mass Used: 155,863.1042 − 155,664.9504 = **198.1538 kg**. Confirmed.
- Per railcar (`ops_notes.aecn_rail_tab.railcars_received`): GRPX5254 offloaded 77,654.9504 kg against 77,870 kg loaded, a shortfall of 77,870 − 77,654.9504 = 215.0496 kg that is not removed; GPRX5107 offloaded 78,026.89584 kg against 78,010 kg loaded, an overage of 78,026.89584 − 78,010 = 16.89584 kg that is removed in J35.
- D44 2,008.07786 kg and E44 301.1674702 kg are both built off the scale basis, while C44 is on the BOL basis: 2,008.07786 / 155,664.9504 = 0.0129; 155,664.9504 - 2,008.07786 = 153656.87254; 301.1674702 / 153656.87254 = 0.00196.
- The decisive internal check: F44 = 153,553.8588 kg, while the MOBI column sums to Σ K28:K35 = 153,355.70507 kg. The rollup does not equal the sum of its own rows: 153,553.8588 − 153,355.70507 = 198.15373 kg (`_derived_values.mobi_sum_offload_rows_kg`, `.mobi_overstatement_kg`). That alone supports Fail, independent of which mass policy is preferred.

FC11 checked before accepting, per `lessons_learned.md` line 199, which makes the back-calc conditional: *"if the sum of all offloads' raw scale tickets exceeds the BOL inbound aggregate"*. GPRX5107 meets that condition and is correctly trued up in column J; GRPX5254 does not, and the rule never raises a credited mass up to the BOL. The railcar-balance escape hatch (General Principle 14) also fails: 77,654.9504 is not equal to 77,870. The Fail survives FC11.

Two logged supports: `prior_week_ops_notes_comparison.rail_rollup_row65` (W5 took Mass Used from the scale-ticket column, D65 = B65 − C65, and GPRX5236's 145.26 kg loss was excluded), and `VVB_Guidance_August_1-31_fetched_2026-09-17.txt` line 43: *"Only the 74,380.92 kg recorded at offload is credited as injected."*

**Where the row goes wrong.** It prescribes correcting both `Mass of Injectant` and `Bio-Oil Mass - AECN via Rail` to 155,664.95 kg, books a 0.031 tCO2e pyrolysis relief plus a transport-process relief cancelled by the BCU, and lands on a 0.335 tCO2e net effect. The same guidance section it cites states the opposite treatment for the upstream legs — `VVB_Guidance_August_1-31_fetched_2026-09-17.txt` line 44 (logged as `vvb_guidance.gprx5139_direction_quote`):

> "Direction of the conservatism. The full 77,800 kg carries its upstream burden — pyrolysis, truck to SOPOR, rail, and truck to Basco — while only the 74,380.92 kg that reached the wellhead earns a removal. The 3,419.08 kg lost to the spill therefore receives no credit, and its share of the upstream emissions remains allocated across the mass that was credited."

`Bio-Oil Mass - AECN via Rail` 155,863.1042 kg feeds the four pyrolysis and transport components, so under that documented treatment it is correct and must not move. Only the sequestration mass is overstated. Recomputed effect with no upstream relief:

- 198.15373 / 1000 = 0.19815373 t
- 0.19815373 × 0.504 = 0.09986948
- 0.09986948 × 3.667 = 0.36622 → gross overstated by **0.366 tCO2e**
- pyrolysis relief: none; transport-process relief: none, so no matching BCU reduction either — the row's assumption that the transport change cancels against the BCU does not arise
- corrected net: 708.742 − 0.366 = **708.376 tCO2e**
- corrected `Mass of Injectant`: 427,222.923 − 198.15373 = 427,024.77 kg (this part of the row is right)

**Required edits to 2.5:** keep Fail. State the defect as the rollup failing to equal the sum of its own MOBI rows, 153,553.8588 against 153,355.70507 kg, because C44 sits on the BOL basis while D44 and E44 sit on the scale basis. Delete the instruction to move `Bio-Oil Mass - AECN via Rail`, and delete the pyrolysis, transport and BCU relief. Restate the effect as 0.366 tCO2e on both gross and net. Add the FC11 balance-check line so a reader can see the rule was tested, and add the `vvb_guidance.gprx5139_direction_quote` key.

Log keys: `ops_notes.aecn_rail_tab.rollup_row44`, `.offload_table`, `.railcars_received`, `prior_week_ops_notes_comparison.rail_rollup_row65`, `vvb_guidance.gprx5139_offload_credit_quote`, `vvb_guidance.gprx5139_direction_quote`, `_derived_values.rail_scale_net_sum_kg`, `.rail_mass_used_scale_basis_kg`, `.mobi_sum_offload_rows_kg`, `.mobi_overstatement_kg`.

### 9.8 — Net removal matches internal calculation
**Current status: Fail. Verdict: ACCEPT the Fail; FIX EVIDENCE — wrong corrected figure.**
The row states the corrected net would be about 708.407 t, 0.335 t lower. Per the 2.5 analysis, with the upstream burden staying on the loaded mass the corrected net is 708.742 − 0.366 = **708.376 t**. Certify's own terms reproduce the reported figure exactly: 789.580 + 81.318 = 870.898; 870.898 − 157.716 = 713.182; 713.182 − 4.440 = 708.742. Log keys: `certify.calculation_view`, `_derived_values.net_corrected_t` (needs updating in the log too), `vvb_guidance.gprx5139_direction_quote`.

### 2.7 — All mass values consistent across sources
**Current status: Fail. Verdict: ACCEPT; FIX EVIDENCE — narrow the claim.**
Recomputed: 153,553.8588 + 273,669.0642 = 427,222.923 kg, the `Mass of Injectant` value; the 14 truck BOLs sum to 277,790 kg (`_derived_values.truck_bol_sum_kg`, `bols.truck_sum_check`). The break is confined to the sequestration mass: the rail offload rows support 153,355.70507 kg of MOBI while Certify carries 153,553.8588 kg inside 427,222.92. The present wording implies `Bio-Oil Mass - AECN via Rail` 155,863.1042 kg is also unsupported; under the guidance treatment quoted above it is the correct upstream basis. Restate, keep Fail.

### 9.6 — BCU does not exceed transport process emissions
**Current status: Pass. Verdict: CHANGE STATUS TO Flag.**
The row's own numbers show over-coverage while its conclusion says there is none: BCU 81.318 t against the precise transport-process sum 81.31764 t, delta 0.00036 t (`certify_components.bcu_transport.delta_t`). Charm's position is that a BCU must not exceed the emission it offsets, so the honest status is Flag with the number stated, not a Pass asserting the overage does not exist.

Recomputing the four legs from the full-precision factors in `standard_efs.rows` rather than from the rounded per-leg displays makes the overage smaller still, and the row should carry the corrected figure:

- 277.790 × 2,197 = 610304.63; 610304.63 × 0.0001143 = 69.7578
- 155.8631 × 107.49722 = 16754.85; 16754.85 × 0.0001143 = 1.9151
- 155.8631 × 2,199 = 342742.96; 342742.96 × 0.000025910374 = 8.8806
- 155.8631 × 42.9 = 6686.53; 6686.53 × 0.0001143 = 0.7643
- 69.7578 + 1.9151 = 71.6729; 71.6729 + 8.8806 = 80.5535; 80.5535 + 0.7643 = 81.3178
- overage against the BCU input: 81.318 − 81.3178 = 0.0002 t, against the 0.36 kg the row reports

Log keys: `certify_components.bcu_transport`, `certify_components.transport_process`, `standard_efs.rows.B6`, `.B10`.

### 3.3 — BOL mass matches or exceeds reported injectate mass
**Current status: Flag. Verdict: keep Flag; FIX EVIDENCE — one sentence is factually wrong.**
The row says the rail BOL sums exceed the offload sums. That is false for GPRX5107: 78,026.89584 − 78,010 = 16.89584 kg, i.e. it offloaded more than its BOLs recorded, which is why the column-J adjustment exists (`ops_notes.aecn_rail_tab.railcars_received`, `_derived_values.gprx5107_overage_kg`). Rewrite so the two railcars are described separately: GRPX5254 short by 215.0496 kg, GPRX5107 over by 16.89584 kg and trued up in J35.
The 2492-T half of the row is sound: page 1 gives 17,024 L and 20.17 M.Ton, page 3 gives 22,523 L and 27.01 MT with 42,870 − 15,860 = 27,010 kg, and 27,010 − 20,170 = 6,840 kg apart (`bols.truck.2492-T`, `_derived_values.bol_2492T_page3_vs_used_kg`). The lower figure is the one used and the choice is documented in Ops cell comment C19, so Flag rather than Fail is right under FC14; the hygiene issue is that the contradiction reaches the verifier unexplained.

### 8.2 — Spills, losses and irregularities documented
**Current status: Pass. Verdict: keep Pass; FIX EVIDENCE — unsupported range claim.**
The phrase about the normal railcar range cites no range. A documented one exists in a source already in the batch folder, `VVB_Guidance_August_1-31_fetched_2026-09-17.txt` line 33: *"Every other railcar offloaded in the same week falls between −101.75 kg and +480.59 kg."* The six-railcar table on lines 35 to 40 backs it. GRPX5254 at 215.0496 kg and GPRX5107 at 16.89584 kg both sit inside that band. Either cite that line and table or delete the range phrase. Add a cross-reference to 2.5: the 215.0496 kg is documented as a loss in Ops G10 and is nonetheless still credited in the rollup, which is the Fail.

### 4.2 and 4.3 — Carbon, hydrogen and nitrogen
**Current status: Pass (both). Verdict: keep Pass; FIX EVIDENCE — two generalizations with no log key.**
Arithmetic confirmed from `lab_results.aecn_stats`: 50.4 − 39.420351 = 10.979649; 10.979649 / 6.093324 = 1.802 standard deviations; band 27.23 to 51.61 %, n = 285.
Unsupported: 4.2's claim that the hash note appears on AECN certificates generally, and 4.3's claim that nitrogen is below detection as for most AECN samples. One certificate was read this session (`lab_results._primary_source_opened`), and the statistics file carries carbon and hydrogen only — no nitrogen distribution, no cross-certificate survey of footnotes. Drop both phrases or replace them with what is logged: the hash legend text on this certificate, and nitrogen reported as <0.75.

### 5.4 — COBB values present and match Ops Notes/Certify
**Current status: Flag. Verdict: keep Flag; FIX EVIDENCE — one of the three items is by design.**
The GPRX5107 offload-3 line is not a railcar-level divergence: 20,012.47904 − 19,995.5832 = 16.89584 kg, exactly the adjustment the Ops Notes books in column J on offload 4 (`cobb.findings.rail_offload3_GPRX5107`, `ops_notes.aecn_rail_tab.offload_table` row 35). Both sources credit GPRX5107 78,010 kg; they differ only in which row carries the true-up, which is the expected COBB-versus-Ops pattern described in `checklist_structure.md` line 74. Say that instead of listing it as a discrepancy. The 2492-T entry at 27,010 kg and the 2495-T entry at 19,510 kg remain genuine Flag material for Garrett.

### 3.5 — Transportation distances consistent and evidenced
**Current status: Fail. Verdict: ACCEPT; FIX EVIDENCE — explain the 0.01508 mi delta.**
The linkage gap is real and is the Fail: `Allocated Distance AECN to Sopor Quebec (truck)` carries only the two dated route maps and `AECN to SOPOR (Baie Comeau) (2).png`, and is the one datapoint the Ops Notes source is not linked to (`certify.attachment_map`, `certify.ops_notes_source_linked_datapoints.not_linked`). A 644 mi allocated figure is not reproducible from a 107 mi route map, so the attached evidence does not support the reported value — the same finding as INJ-08-2026 W1 and W2.
The row implies the 0.01508 mi delta is itself unexplained. It is explained, and saying so strengthens the row: Certify's 644.09429 mi is the allocation built on the map distance 107.49722 mi (`certify_components.transport_process.AECN_to_SOPOR_truck.distance.value_mi`) rather than the Ops constant 107.5. Recomputed: 77,654.9504 / 77,870 = 0.9972384; 3 × 107.49722 = 322.49166; 322.49166 × 0.9972384 = 321.601; 321.601 + 322.49166 = 644.09266 mi, against Ops L36 644.1093682 mi built on 107.5 (`ops_notes.aecn_rail_tab.distance_rollup_row36`). A basis difference, not an arithmetic error; the evidentiary gap is what fails.

### 9.3 — ACTIVITIES, Injection: LCS / sample transport
**Current status: N/A. Verdict: ACCEPT the N/A; FIX EVIDENCE — no log key.**
Correct per `checklist_structure.md` line 268 (AECN needs no LCS pre-treatment), and the components list holds no injection-side activity component. But the row cites no log key at all, which breaks the every-finding-cites-a-log-key rule (General Principle 12). Add `certify.components_tab`.

### 7.3 and 7a.3 — Uncertainty discount
**Current status: Pass (both). Verdict: ACCEPT; FIX EVIDENCE.**
The criterion in `checklist_structure.md` rows 7.3 and 7a.3 is presence and consistency, which the 4.440 t in the Calculation view satisfies (`certify.calculation_view`). But 7a.3 asserts the discount is derived from the inputs above, a derivation nobody recomputed and no log key supports. State what was actually checked: discount present, ratio to gross 4.440 / 789.580 = 0.005623, subtracted after Sequestrations plus Adjustments less Activities, with the Layer 1 and Layer 2 inputs verified in 7a.1 and 7a.2.

### 5.5 — pH measurement noted
**Current status: Flag. Verdict: ACCEPT, with the tension recorded.**
pH is blank on all 8 rail rows, all 14 truck rows and all 22 COBB rows (`ops_notes.aecn_truck_tab.pH_blank_all_rows`, `cobb.findings.ph`). `checklist_structure.md` line 138 gives the failure condition as pH missing, and states pH is required for all batches including AECN, which reads toward Fail. Against that: pH is not a Certify datapoint and does not enter the Net CDR, so it fails the material-misstatement test, and W4 and W5 carried the same gap as a Flag. Keep Flag; the precedent citation already in the row is what justifies it.

---

## 2. Rows confirmed without change

- **1.1** Drive folder, Ops B2 INJ-09-2026-W1 and the Certify period 30 Aug to 04 Sep all tie (`drive_folder.root_items`, `ops_notes.batch_id_B2`, `certify.header`).
- **1.2** 16 ticket PDFs across two railcar folders, all 16 opened as images (`scale_tickets._summary.tickets_read`).
- **1.3** SR26-05371 present and read; the second Testing file is the sibling WODO removal.
- **1.4** Ops Notes present, the three relevant tabs populated, cell comments read; the single unlinked datapoint is correctly carried to 3.5.
- **1.5** No Vaulted reference in any of the 20 BOLs, the Ops dump or the 14 component names — a negative claim backed by a logged search returning an empty list (`bols.destination_check.vaulted_references_found`).
- **2.1** All 16 Certify ticket uploads md5- and length-identical to the Drive files (`certify_source_file_checks.result`); the spelling variance is carried to 9.9.
- **2.2** Rail tickets 2026-08-31 to 2026-09-03 against a 2026-09-04 booking inside a 30 Aug to 04 Sep period; every empty weigh later than its full weigh (`scale_tickets._summary.empty_after_full_all_pairs`); truck load dates 2026-08-21 to 2026-08-29 against deliveries 2026-08-28 to 2026-09-04, all inside two weeks.
- **2.3** All 8 pairs match on tractor and trailer (`scale_tickets._summary.rig_mismatches` is empty), so the August standard-tare trigger does not fire.
- **2.4** All 8 nets recomputed from the ticket images, e.g. 71,660 − 28,800 = 42,860 lb and 42,860 × 0.453592 = 19,440.95312 kg; every delta against Ops F28:F35 is 0.0.
- **2.6** 2,008.07786 / 155,664.9504 = 0.0129 and 3,583.491 / 277,790 = 0.0129, both equal to constant O5/L5. The rate is right; the basis mismatch belongs to 2.5, not here.
- **2.6a** Flag correct and FC13-compliant: O7 is 0.00196 this week against 0.00195 in W5, same dataset, per-load mean against per-COA mean, conservative direction (`filtration_constant_source.summary_tab_rows`). Arithmetic ties: 155,664.9504 - 2,008.07786 = 153656.87254 and 301.1674702 / 153656.87254 = 0.00196; 277,790 - 3,583.491 = 274206.509 and 537.4447576 / 274206.509 = 0.00196.
- **2.8** Truck BOL sum recomputed as 277,790 kg; the methodology header A26 is quoted in the row.
- **3.1, 3.2, 3.4** 20 BOLs opened, 36 of 36 Certify uploads md5-identical, rail shipping to SOPOR Baie-Comeau and trucks to St Landry LA.
- **3.6** Eight transport components, four legs each with process and embodied (`certify.components_tab`).
- **3.7** Flag correct — carrier overwrite on 2493-T, correction header and commercial invoice on 2494-T, the 2481-T date spread; none affects mass used.
- **4.1, 4.4, 4.6** Certificate SR26-05371.001 under SGS order 5494492, client ID 09-2026-W1 AECN, sampled 05-Sep; density 1.219 g/cm3 against the formation-fluid 1.01 g/mL read from Waypoint 24-200-0020 page 5.
- **4.5, 5.3, 5.7** N/A correct; 5.7 matches the prescribed treatment in `checklist_structure.md` lines 140 and 146, where a blank density field is expected for AECN.
- **5.1, 5.2** Headers tie; Ops D28:E35 equal the 16 ticket gross weights, with the D29 provenance correction and the D34 recovery both read as cell comments.
- **5.6** COBB completion date 2026-09-04 on all 22 rows, equal to the Ops offload dates and the Certify period end.
- **6.1, 6.2, 6.3** LCA and supporting files on the Sources tab; the FH 2026 LCA Certify copy md5 matches the local copy and its I12 reads 0.1371171258.
- **6.4** 0.1371171258 at Standard EF 2026 tab B4, sourced to FH 2026 LCA w Stack Emissions, equal to the LCA I12 and to the Certify display 0.13712; the August guidance states the H2 2026 factor governs every AECN removal in this period.
- **6.5** 0.02116 on both embodied components, equal to Standard EF B5 and to the calc sheet total 0.02115941123.
- **6.6** Pyrolysis mass basis is pre-sparging, 155,863.1042 kg rail and 277,790 kg truck — and under the guidance treatment quoted in 2.5 it stays on the loaded basis even after the fix.
- **7.1** Gross recomputed: 427.222923 × 0.504 = 215.32035; 215.32035 × 3.667 = 789.580 t, equal to the component value. Fail correct as written, with the 0.366 t overstatement.
- **7.2** Activities 157.716 t, made up of pyrolysis 68.639 and transport 89.077; all twelve components recomputed in 9.2 and 9.4.
- **7.4** Flag correct — the September RP is open and no RP-level BCU Quant sheet or GHG Statement exists yet (`rp_status`), the same deferral as the five August weeklies. This is not unfinished work: the artifact does not exist.
- **7a.1** All nine components with a mass or carbon input opened; uncertainty appears on mass and carbon only; the four embodied components are per-mile blueprints with no mass input.
- **7a.2** Flag confirmed, counts recomputed: 580.56 / 72.57 = 8.0 weighings, matching the 8 offloads; 1,088.55 / 72.57 = 15.0 against 14 truck BOL weighings, where 14 × 72.57 = 1,015.98 kg; 1,669.11 / 72.57 = 23.0 against 22 expected, where 22 × 72.57 = 1,596.54 kg. Carbon check: 0.004 × 50.4 = 0.2016, displayed 0.20164. The extra weighing sits on the truck side and propagates into the aggregate; the direction is conservative (a larger discount, a lower net), so Flag rather than Fail is right, and the 72.57 kg per discrete weight is the documented figure (`checklist_structure.md` line 219).
- **8.1** Flag correct: Ops M11 still carries the pre-recovery text about no resolvable ticket pair although row 34 is populated and D34 records the 2026-09-11 recovery; and no September VVB guidance document exists yet (`vvb_guidance.september_2026_guidance_doc_exists` is false, with the search enumerated).
- **8.3** Both railcars new this RP, Previously Claimed and Prior-RP Claimed 0 kg, flag FULL.
- **8.4** 8 offloads against 6 inbound BOLs meets the conservatism precondition: 8 × 72.57 = 580.56 kg against 6 × 72.57 = 435.42 kg.
- **9.2** Four process legs recomputed at full precision in the 9.6 entry above, summing to 81.3178 t against the 81.317 t in the log; embodied legs 7.307, 0.153, 0.137 and 0.163 sum to 7.760 t; both subtotals match. The 2026 railcar embodied factor at `standard_efs.rows.B13`, displayed as 0.03113 kgCO2e/mi, is the one applied.
- **9.4** 155.8631 × 0.13712 = 21.372; 277.790 × 0.13712 = 38.091; 155.8631 × 0.02116 = 3.298; 277.790 × 0.02116 = 5.878 — all four match the components.
- **9.5** BCU component sourced to the retirement certificate, md5-matched and read: 2,795 Renewable Diesel TERCs retired 18 Dec 2025 on behalf of Charm Industrial, verifier Turner, Mason & Company. See the observation below.
- **9.7** No counterfactual term; the Calculation view reproduces exactly (789.580 + 81.318 = 870.898; 870.898 − 157.716 = 713.182; 713.182 − 4.440 = 708.742).
- **9.9** Flag correct and correctly scoped — one generic filename is hygiene, not a reporting error, so Flag not Fail; the GRPX/GPRX filename variance is nomenclature with every other identifier matching.
- **9.10** 53 sources enumerated; 36 of 36 ticket and BOL uploads byte-identical to the Drive originals.

---

## 3. Observations (outside the reviewed rows)

1. **Pooled BCU drawdown is not reconciled.** 9.5 proves the certificate exists and holds 2,795 tCO2e, but nothing in the session confirms this removal's 81,318 kgCO2e sits inside the un-retired balance — the EAC inventory tracker was not read and no log key covers it, while `certify_components.bcu_transport.certificate.note` states the per-removal drawdown is tracked there. No checklist row asks the question. Worth one line of evidence in 9.5 or a new row.
2. **The corrected Mass of Injectant, if Garrett applies it, changes nothing upstream.** Under the guidance treatment quoted in 2.5, only the sequestration input moves, from 427,222.923 kg to 427,024.77 kg. The four pyrolysis components, the four transport-process components and the BCU all stay as they are. Saying so in the Slack ask keeps the fix to a single datapoint.
