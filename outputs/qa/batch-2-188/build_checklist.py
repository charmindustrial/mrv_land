#!/usr/bin/env python3
"""Build Batch 2-188 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

FAIL_FILL = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
FAIL_FONT = Font(color='9C0006', bold=True)
FLAG_FILL = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
FLAG_FONT = Font(color='996600')
NA_FONT = Font(color='808080', italic=True)
HEADER_FILL = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
HEADER_FONT = Font(color='FFFFFF', bold=True, size=12)
SECTION_FILL = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
SECTION_FONT = Font(bold=True, size=11)

THIN = Side(border_style='thin', color='808080')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical='top', horizontal='left')
WRAP_CENTER = Alignment(wrap_text=True, vertical='center', horizontal='center')

ROWS = [
    ('HEADER',),
    ('META', 'Batch ID', '2-188'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 03 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-01'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TIMX201060, consumed_lot redo_offload_4 = the railcar PHYSICAL LAST OFFLOAD per Ops Notes structure. Sister batches 2-186=offload_1, 2-187=offload_2, 2-189=offload_3.)'),
    ('META', 'Net CDR (Certify)', '25.50 tCO2e'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "2-188" at id 1Nu4ciH-wDpRB65HIJITsOgUDoYFttqo_; contains "2-188 Ops Notes Rail" sheet, Testing subfolder (SR26-02264.pdf shared CHN report), Scale Tickets subfolder (Full + Empty JPGs). [log:drive_folder_url]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains 2-188 Full Scale Ticket.jpg (3.3 MB) and 2-188 Empty Scale Ticket.jpg (3.0 MB). One offload pair (consistent with 2-188 = consumed_lot offload_4 only; sister batches each contribute their own ticket pairs). Both also linked in Certify Sources. [log:scale_tickets.full_ticket.filename, scale_tickets.empty_ticket.filename]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive > Testing contains SR26-02264.pdf (7-page SGS Certificate of Analysis covering batches 2-186 through 2-189 + 3-55 through 3-57). Page 3 covers batch 2-188 (Certificate SR26-02264.003, Client ID = "BATCH 2-188"). [log:lab_results.certificate_number, lab_results.page, lab_results.batch_id_on_certificate]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-188 Ops Notes Rail" Google Sheet (id 14wgtgZExIQSqi5MnUcRQj5Vu3-4y4LUl7iZecLNeTZE) present in Drive folder; owner Garrett Lutz; modified 2026-05-01 09:04 PDT (same edit pass as 2-189 Ops Notes). Batch Composition (railcar TIMX201060, sparging 0.0129), BOLs Loaded (3 inbound BOLs totaling 80.61 MT post-correction), and offload table fully populated with 4 rows; this batch is offload_4 (Cargo (kg) = 15,220.17728, allocation fraction 0.18881252). [log:ops_notes.filename, ops_notes.modified_at, ops_notes.offload_table.3.associated_batch_id, ops_notes.offload_table.3.cargo_mass_kg, ops_notes.offload_table.3.upstream_allocation]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'CHN PDF page 3 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). Ops Notes references Opelousas->Basco truck leg. No Vaulted references in any source. [log:lab_results.location_on_cert]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both JPG images Read directly from pixels (NOT Drive OCR snippet, per OCR-vs-image rule). Full ticket #1312226091780 dated 4-01-26 13:25 at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA scale #3122, axle sum 10,200 + 27,880 + 27,500 = 65,580 lb. Empty ticket #1312226091790 dated 4-01-26 16:38 same location, axle sum 9,700 + 11,640 + 8,360 = 29,700 lb. Both internally consistent (gross = axle sum, no axle-vs-cert discrepancy). [log:scale_tickets.full_ticket, scale_tickets.empty_ticket]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Both tickets 2026-04-01; injection completion 2026-04-03. 2 days. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Full ticket: Tractor CH1, Trailer KL-192. Empty ticket: Tractor CH1, Trailer KL-192. Same vehicle weighed at both events. (Note: different tractor/trailer than 2-189\'s CH2/KL-188 — expected; each offload uses its own dedicated truck.) [log:scale_tickets.full_ticket.tractor, scale_tickets.empty_ticket.tractor, scale_tickets.tractor_trailer_match]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     '2-188 IS the railcar physical LAST OFFLOAD per Ops Notes structure (offload_4). FC11 last-offload mass conservatism applies: raw scale-ticket math (65,580 - 29,700) lb x 0.453592 = 35,880 lb x 0.453592 = 16,274.88 kg, but sum of all 4 raw scale tickets (21,854.06 + 21,736.13 + 21,799.63 + 16,274.88 = 81,664.70 kg) EXCEEDS the BOL inbound aggregate (80,610 kg) by 1,054.70 kg. Per FC11, last offload\'s Cargo (kg) is back-calculated: Cargo (kg) = 80,610 - sum(prior 3 offloads\' raw scale tickets) = 80,610 - 65,389.82 = 15,220.18 kg. Ops Notes offload_4 row Cargo Mass (kg) = 15,220.17728 — matches policy back-calc exactly. Raw scale ticket reference value (16,274.88 kg) is shown in footer of Ops Notes for transparency. [log:scale_tickets.computed_net_lb, scale_tickets.computed_net_kg, scale_tickets.ops_notes_cargo_kg_policy_applied, scale_tickets.fc11_policy_check_result, ops_notes.batch_composition.lbs_to_kg_factor, ops_notes.offload_table.3.cargo_mass_kg, ops_notes.railcar_balance_check]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Last-offload conservatism applied per FC11: Ops Notes Cargo (kg) = 15,220.18 (policy-applied back-calc) instead of raw scale ticket math 16,274.88 — the policy is more conservative (lower mass = lower CDR claim). Sum of all 4 offloads\' policy-applied Cargo (kg) = 80,610.00 = exactly BOL aggregate. Verifier-correct conservatism. [log:scale_tickets.ops_notes_cargo_kg_policy_applied, scale_tickets.scale_vs_ops_diff_kg, ops_notes.railcar_balance_check, bol_billing_documents.total_bol_aggregate_kg]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied to policy-applied Cargo: 15,220.17728 x 0.0129 = 196.3402869 kg sparging loss. Mass of Bio-Oil Injected = 15,220.17728 - 196.3402869 = 15,023.83699 kg. Ops Notes offload_4 row shows exactly these values; arithmetic correct. [log:ops_notes.batch_composition.sparging_mass_loss_rate, ops_notes.offload_table.3.cargo_mass_kg, ops_notes.offload_table.3.sparging_loss_kg, ops_notes.offload_table.3.mass_of_bio_oil_injected_kg]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Flag',
     'Pre-sparging: Ops Notes Cargo (kg) = 15,220.17728 (policy-applied) = Certify "Allocated Bio-Oil Mass - AECN via Rail" 15,220.18 ✓. Post-sparging: Ops Notes Mass of Bio-Oil Injected = 15,023.83699 = Certify "Mass of Injectant" 15,023.84 ✓. Raw scale ticket math (16,274.88 kg) intentionally NOT used for Certify — by design per FC11 last-offload conservatism. **COBB row 65 carries STALE pre-correction values:** offloaded_quantity_kg = 5,620.18 (vs correct 15,220.18) AND origin_quantity_kg = 71,010 (vs correct 80,610). Both Garrett-side data-provenance issues, NOT verifier-impacting (Ops Notes / Certify both correctly reflect the 9.6 MT post-correction BOL). See item 5.4 for full detail. [log:scale_tickets.computed_net_kg, ops_notes.offload_table.3.cargo_mass_kg, ops_notes.offload_table.3.mass_of_bio_oil_injected_kg, cobb_2-188_row.offloaded_quantity_kg_stale, cobb_2-188_row.stale_value_explanation, certify_components.Injection_sequestration.mass_of_product_kg, _derived_sums._2-188_certify_displayed_mass_kg, bol_billing_documents.total_bol_aggregate_kg]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Certify Sources: Documents camion 2317-R.pdf, Billing Truck 2316-R.pdf, Billing Truck 2314-T Corrections (1).pdf. Per Document Location Rule, presence in Certify Sources is sufficient. Filename "-T" inconsistency on the corrections PDF — see Section 9.9. [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2314-R, 2316-R, 2317-R) listed in COBB row 65 BOL_number field for batch 2-188 and in Ops Notes BOLs Loaded section. Destinations = SOPOR Quebec railyard (rail-batch convention). [log:ops_notes.bols_loaded_section, cobb_2-188_row.bol_number]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL masses (26.05 + 29.06 + 25.50) = 80.61 MT = 80,610 kg (Ops Notes Total Loaded Mass). Post-correction inbound aggregate (the 9.6 MT correction was added by AECN; documented as "Billing Truck 2314-T Corrections (1).pdf"). This batch\'s policy-applied offload mass = 15,220.18 kg, well below 80,610 kg railcar inbound. Sum of all 4 sister offloads\' Cargo (kg) = exactly 80,610 ✓ (railcar fully drained). [log:bol_billing_documents, ops_notes.total_loaded_mass_mt, ops_notes.offload_table.3.cargo_mass_kg, ops_notes.railcar_balance_check]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN Quebec -> SOPOR (truck, 3 BOLs labeled with "-R" rail-load suffix) -> Opelousas LA (rail leg via railcar TIMX201060) -> Basco 6 (truck, this batch consumed_lot offload_4). Three legs documented across Drive + Certify Sources. [log:cobb_2-188_row.bol_number, ops_notes.bols_loaded_section, certify_components]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified. Rail-batch allocation (allocation fraction = 15,220.18/80,610 = 0.18881): (1) AECN->SOPOR truck full single distance 173 km (= 107.5 mi) per Certify Datapoint "Distance from AECN to Sopor Quebec (truck)", and Allocated Distance AECN to Sopor Quebec 97.99 km (60.89 mi) computed as 322.5 mi total trucking x 0.18881 batch share; (2) SOPOR->Opelousas rail full 2,199 mi per "Distance from SOPOR to Opelousas (RAIL)", Allocated 415.20 mi (2,199 x 0.18881); (3) Opelousas->Basco truck per-batch 42.9 mi (full per-batch, no allocation since each offload uses dedicated truck). All match Ops Notes pre-computed values for offload_4 row. [log:certify_datapoints.list, ops_notes.batch_composition, ops_notes.offload_table.3.upstream_allocation, ops_notes.offload_table.3.rail_miles_allocated, ops_notes.offload_table.3.truck_leg_1_miles_allocated]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components in Certify: AECN to SOPOR Tanker Truck Process (0.187 t), SOPOR to Opelousas Rail Process (0.867 t), Opelousas to Basco Tanker Truck Process (0.075 t), AECN to SOPOR Tanker Truck Embodied (0.014 t), SOPOR to Opelousas Rail Embodied (0.013 t), Opelousas to Basco Tanker Truck Embodied (0.010 t). Sum = 1.166 t (transport) per Certify Components page. [log:certify_components, _derived_sums.transport_total_t]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'Documents camion 2317-R.pdf, Billing Truck 2316-R.pdf, Billing Truck 2314-T Corrections (1).pdf in Certify Sources serve as both BOLs and billing for the 3 inbound truck legs. Charm-A4-2024-10-24-63-1976.pdf (BCU certificate) also present — see Section 9.5 for BCU value anomaly. [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder', 'Pass',
     'SR26-02264.pdf (7-page SGS Certificate, in Drive Testing) AND CHN-186-189.pdf (Certify Sources alias). Page 3 covers batch 2-188 (Certificate SR26-02264.003, "BATCH 2-188"). [log:lab_results.filename, lab_results.certify_filename_alias, lab_results.page]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-188 = 42.0% (m/m) (ASTM D5291 Method C). Within AECN expected range (mean 39.42%, +/-2 SD ~27.2%-51.6%). [log:lab_results.carbon_pct, lab_results.carbon_within_aecn_normal_range]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 7.2%, Nitrogen <0.75%, Viscosity 22.92 cSt @ 40C, Acid Number 45 mg KOH/g, Density 1.212 g/cm3 @ 15C. All within typical AECN ranges. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct, lab_results.viscosity_cSt_at_40C, lab_results.acid_number_mg_KOH_per_g, lab_results.density_g_per_cm3_at_15C]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02264.003 explicitly labeled "BATCH 2-188" on page 3. Sampled 2026-04-02 23:05 at BASCO LOUISIANA (after offload_4 truck arrived 2026-04-01). Sample ~1 day before injection completion 2026-04-03. [log:lab_results.batch_id_on_certificate, lab_results.sampled_datetime, lab_results.location_on_cert]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate is recorded in Ops Notes Section 5.5. [log:oil_type]',
     'N/A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-188, Completion Date = 4/3/2026. Matches Certify removal date (03 Apr 2026) and COBB injection_completion_date (2026-04-03). [log:ops_notes.batch_number_on_sheet, ops_notes.completion_date, cobb_2-188_row.injection_completion_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 65,580 lb = Ops Notes offload_4 Loaded Mass (lbs) 65,580 (exact). Empty ticket gross 29,700 lb = Ops Notes offload_4 Unloaded Mass (lbs) 29,700 (exact). Both values verified by direct image Read of JPGs (per Drive-OCR-not-primary-source rule). Raw scale ticket math = 35,880 lb / 16,274.88 kg shown in Ops Notes footer for transparency. Ops Notes offload_4 Cargo Mass (kg) = 15,220.17728 = policy-applied (FC11 back-calc), not raw scale ticket math. Cargo (kg) policy-applied value verified independently via railcar balance check (sum of 4 offloads = 80,610 kg = BOL aggregate). [log:scale_tickets.full_ticket.certified_gross_lb, scale_tickets.empty_ticket.certified_gross_lb, scale_tickets.computed_net_lb, ops_notes.batch_composition.lbs_to_kg_factor, ops_notes.offload_table.3.loaded_mass_lb, ops_notes.offload_table.3.unloaded_mass_lb, ops_notes.offload_table.3.cargo_mass_kg, ops_notes.raw_scale_ticket_reference_kg, bol_billing_documents.total_bol_aggregate_kg]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Flag',
     'COBB row 65 for "2-188" verified: cell A = "2-188" ✓, consumed_lot = "Rail_TIMX201060_2.27.26_redo_offload_4" ✓, BOL_number = "2314-R, 2316-R, 2317-R" matches Ops Notes BOLs Loaded ✓, injection_completion_date = 2026-04-03 = Ops Notes 4/3/2026 ✓, injection_ph = "3" matches Ops Notes offload_4 pH = 3 ✓. **TWO COBB-side data-provenance issues for Garrett (NOT 2-188-impacting since verifier reads Ops Notes / Certify):** (1) COBB row 65 origin_quantity_kg = 71,010 is STALE pre-correction; post-correction = 80,610 kg per Ops Notes Total Loaded Mass (the 9.6 MT AECN BOL correction first surfaced on sister 2-186; same flag carried by sister rows 63/64/66). (2) COBB row 65 offloaded_quantity_kg = 5,620.17728 is STALE — this is the OLD policy back-calc against the pre-correction BOL aggregate (71,010 - 65,389.82 = 5,620.18). Post-correction policy-applied value = 15,220.18 kg (80,610 - 65,389.82) = what Ops Notes / Certify both correctly show. Operational data-provenance for Garrett to refresh — verifier reads Ops Notes / Certify (both correct). [log:cobb_row_id_verified, cobb_cell_A_value, cobb_2-188_row, cobb_sister_rows_pre_correction, ops_notes.total_loaded_mass_mt, bol_billing_documents.total_bol_aggregate_kg, ops_notes.offload_table.3.cargo_mass_kg]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_4 row pH = 3.0. COBB row 65 pH = "3" (matches). [log:ops_notes.offload_table.3.ph, cobb_2-188_row.injection_ph]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'All three sources align: Ops Notes Completion Date 4/3/2026, COBB row 65 injection_completion_date 2026-04-03, Certify removal date 03 Apr 2026. [log:ops_notes.completion_date, cobb_2-188_row.injection_completion_date, certify_components]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include density entry — expected behavior. [log:oil_type]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) datapoint. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 since EFs are H1/H2). [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t (display) for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)". KB current native value 0.10402 tCO2e/t (H2 2025) — within rounding. Independent calc: 15.220179 t x 0.10402 = 1.5832 ≈ 1.583 tCO2e ✓ matches Certify "AECN pyrolysis (from rail loads) - process emissions" 1.583 t. [log:certify_components.AECN_pyrolysis_from_rail_loads_process, ef_verification.aecn_pyrolysis_process]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)". KB current value 0.0212 tCO2e/t (precise per Certify modal at 0.02116). Independent calc: 15.220179 t x 0.02116 = 0.32206 ≈ 0.322 tCO2e ✓ matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" 0.322 t. [log:certify_components.AECN_pyrolysis_from_rail_loads_embodied, ef_verification.aecn_pyrolysis_embodied]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Pyrolysis components apply 0.104 / 0.02116 to "Allocated Bio-Oil Mass - AECN via Rail" = 15,220.18 kg = pre-sparging Cargo (kg) (policy-applied). Sparging is applied at injection (Section 2.6) and only affects Mass of Injectant for sequestration. Methodology correct. [log:certify_datapoints.list, certify_components.AECN_pyrolysis_from_rail_loads_process]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc: 15.02384 t (Mass of Injectant, post-sparging) x 0.420 (Carbon Content from CHN page 3) x 3.667 = 23.139 tCO2e. Certify Sequestrations 23.139 tCO2e — exact match. [log:certify_components.Injection_sequestration, lab_results.carbon_pct, ops_notes.offload_table.3.mass_of_bio_oil_injected_kg]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted: 3 transport process (AECN->SOPOR truck 0.187, SOPOR->Opelousas rail 0.867, Opelousas->Basco truck 0.075) + 3 transport embodied (0.014 + 0.013 + 0.010) + AECN pyrolysis process 1.583 + AECN pyrolysis embodied 0.322. Sum = 3.071 tCO2e ✓ matches Certify Activities total. Each component math reconciles independently. [log:certify_components, certify_calculation_view.activities_t]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount 146 kg present in Calculation View. Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate from per-component +/- inputs — Isometric\'s aggregation is authoritative; QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.4% carbon = 0.168 on 42%). 0.146 t is ~0.6% of gross sequestration (23.139 t), consistent with typical AECN rail batch ratios. [log:certify_calculation_view.uncertainty_discount_kg, certify_calculation_view.sequestrations_t, _derived_sums._carbon_uncertainty_pct_displayed]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Fail',
     'Net = 23.139 (sequestrations) + 5.582 (BCU adjustments) - 3.071 (activities) - 0.146 (uncertainty) = 25.504 tCO2e ≈ 25.50 displayed. Certify math reconciles MECHANICALLY ✓. **HOWEVER, the BCU value 5.582 t is materially anomalous** — see Section 9.5 for the substantive finding. Net CDR is over-claimed by ~4.45 tCO2e (~17%) relative to the sister-batch pattern (where BCU = transport process exactly): expected 2-188 Net per sister pattern = 23.139 + 1.129 - 3.071 - 0.146 ≈ 21.05 tCO2e. The Certify-displayed 25.50 tCO2e relies on an unjustified excess BCU allocation that the verifier cannot independently confirm from available evidence. [log:certify_calculation_view.net_tco2e_displayed, certify_calculation_view.expected_net_if_bcu_matched_transport_process, certify_calculation_view.bcu_anomaly_inflation_kg, sister_batch_bcu_pattern, _derived_sums.net_tco2e_independent_recalc_displayed_form, _derived_sums.activities_total_t]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show ±72.57 kg in INPUTS section (verified by opening each component modal individually): Injection Sequestration (Mass of product 15,023.84 ±72.57), AECN->SOPOR Truck Process (Mass of load 15,220.179 ±72.57), SOPOR->Opelousas Rail Process (Mass of load 15,220.179 ±72.57), Opelousas->Basco Truck Process (Mass of load 15,220.179 ±72.57), AECN Pyrolysis Process (Mass 15,220.179 ±72.57), AECN Pyrolysis Embodied (Mass 15,220.179 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi). Carbon Content uncertainty ±0.168% (= 42 x 0.004 = 0.168, matches 0.4% relative). [log:certify_components.Injection_sequestration, certify_components.AECN_to_SOPOR_Tanker_Truck_Process, certify_components.SOPOR_to_Opelousas_Rail_Process, certify_components.Opelousas_to_Basco_Tanker_Truck_Process, certify_components.AECN_pyrolysis_from_rail_loads_process, certify_components.AECN_pyrolysis_from_rail_loads_embodied]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported ± matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so ±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process). Verified by opening each component modal and reading the INPUTS section directly. Carbon content ±0.168% = 42 x 0.004 confirms standard 0.4% relative uncertainty. **Conservatism precondition (N_offloads >= N_inbound_BOLs) for railcar TIMX201060 is FORMALLY VALIDATED at this batch (the railcar\'s last offload):** 4 offloads (per Ops Notes table) >= 3 inbound BOLs (per BOLs Loaded section). 4 x 72.57 = 290.28 kg total railcar mass uncertainty booked via per-offload framing > 3 x 72.57 = 217.71 kg per-inbound-BOL alternative. Per-offload framing is conservative ✓. See Section 8.3 for the gating check. [log:certify_components, ef_verification, ops_notes.fc9_conservatism_precondition_check]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount 146 kg in Calculation View. Visible in net formula: 23.139 sequestrations + 5.582 BCU - 3.071 activities - 0.146 uncertainty = 25.504 t Net ≈ 25.50 displayed. Magnitude reasonable given mass and carbon uncertainty inputs (smaller batch = smaller absolute uncertainty in tonnes). [log:certify_calculation_view.uncertainty_discount_kg, certify_calculation_view.net_tco2e_displayed, _derived_sums.net_tco2e_independent_recalc_displayed_form, _derived_sums.activities_total_t]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Fail',
     'Carbon (42.0%), distances (107.5/2199/42.9 mi full-leg + 60.89/415.20 mi allocated), most EFs (0.1143 truck process / 0.0259 rail process / 0.23756 truck embodied / 0.03113 rail embodied 2026 corrected) all within expected ranges. Mass 15,220.18 kg pre-sparging / 15,023.84 kg post-sparging within expected range for last-offload remainder (smaller than sisters by design). Both scale tickets internally consistent (gross = axle sum). All component-level math reconciles to Certify within rounding. **One MAJOR outlier:** BCU value 5.582 t is 4.5x the 2-188 transport process emissions (1.129 t) and 4.5x the sister-batch pattern (sisters\' BCUs = ~1.61 t each, all matching their respective transport process). See Section 9.5 for full detail and Section 7.4 for net-CDR-impact sizing. [log:lab_results.carbon_pct, certify_components, ef_verification, sister_batch_bcu_pattern]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. Ops Notes "Oil Left in Railcar (MT)" = 0 and "Oil Left in Railcar (kg)" = 0 — consistent with this being the last offload of railcar TIMX201060 (railcar fully drained). All 4 offloads\' Cargo (kg) sum to exactly 80,610 kg = BOL aggregate ✓ (no unaccounted losses). [log:ops_notes.oil_left_in_railcar_mt, ops_notes.oil_left_in_railcar_kg, ops_notes.railcar_balance_check]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch — last-offload reconciliation + FC9 precondition)', 'Pass',
     'Railcar TIMX201060 fully drained at THIS batch (2-188 = consumed_lot offload_4, the railcar\'s physical last pull per Ops Notes structure). Sister-batch state per Ops Notes 4-row offload table: 2-186 row 1 = offload_1, Cargo 21,854.06 kg (raw scale ticket); 2-187 row 2 = offload_2, Cargo 21,736.13 kg (raw); 2-189 row 3 = offload_3, Cargo 21,799.63 kg (raw); 2-188 row 4 = offload_4 (LAST), Cargo 15,220.18 kg (FC11 policy-applied back-calc = 80,610 - 65,389.82). **FC11 last-offload reconciliation: PASS.** Sum of 4 offloads = 80,610 kg = exact BOL aggregate ✓. Sum of Upstream Allocation fractions ≈ 1.00 ✓ (verified per ops_notes.offload_table). Oil Left in Railcar = 0 ✓ (no unaccounted residual). **FC9 conservatism precondition for Section 7a per-offload uncertainty framing: PASS.** N_offloads (4) >= N_inbound_BOLs (3). Per-offload mass uncertainty (±72.57 kg per leg) summed across 4 sister batches (290.28 kg) > inbound-weighing uncertainty (3 BOLs × 72.57 = 217.71 kg). Verifier sees more uncertainty than inputs strictly required — favorable conservatism. Section 7a Layer 1+2 framing is therefore conservative at the railcar level. [log:cobb_sister_rows_pre_correction, ops_notes.railcar_balance_check, ops_notes.fc9_conservatism_precondition_check, ops_notes.n_offloads, ops_notes.n_inbound_bols, ops_notes.offload_table, ops_notes.oil_left_in_railcar_mt]',
     'KB Section 8 / FC9 / FC11'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component 23.139 tCO2e. Independent calc: 15.02384 t (Mass of Injectant) x 0.420 (Carbon Content) x 3.667 = 23.139 t. Exact match. Carbon content matches CHN PDF page 3 (42.0%). [log:certify_components.Injection_sequestration, lab_results.carbon_pct]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Rail embodied EF = 0.03113 kgCO2e/mi (2026 corrected value 0.0000311307 MTCO2e/mi in native units, NOT stale 0.0000352240). Allocated distances correctly use the post-correction BOL inbound (80,610 kg) as denominator (allocation fraction 0.18881 = 15,220.18 / 80,610). All 6 transport components math-reconcile independently to Certify values within rounding. Sum = 1.166 t. [log:certify_components, ef_verification.rail_embodied, _derived_sums.transport_total_t]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (1.583 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.322 t) present. Rail-batch naming convention used (deliberate signal to VVB to expect scale tickets as authoritative mass source). Sum = 1.905 t. [log:certify_components.AECN_pyrolysis_from_rail_loads_process, certify_components.AECN_pyrolysis_from_rail_loads_embodied, _derived_sums.pyrolysis_total_t]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Fail',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" component populated at 5.582 tCO2e (constant_reduction = 5,581.52 kgCO2e) sourced from Charm-A4-2024-10-24-63-1976.pdf. **MATERIAL ANOMALY:** sister batches in the same railcar (TIMX201060) all have BCU = transport process emissions exactly: 2-186 BCU = 1.621 t (verified by direct Certify read), 2-187 = 1.612 t (verified), 2-189 = 1.617 t (per prior QA source-read = 0.268 + 1.242 + 0.107). For 2-188, transport process = 0.187 + 0.867 + 0.075 = 1.129 t — but BCU is 5.582 t, exceeding transport process by 4.453 tCO2e. The excess BCU (above what cancels transport process) flows directly into Net CDR (since Net = Sequestrations + BCU - Activities - Uncertainty), inflating 2-188\'s reported Net by approximately 4.45 t. Sister 2-188 source filename (Charm-A4-2024-10-24-63-1976.pdf) is also DIFFERENT from sisters 2-186/2-187/2-189 (Charm-A3-2024-10-24-64-1976.pdf), suggesting a different BCU certificate was applied. Without a BCU Quant or allocation document showing 5,581.52 kgCO2e is the correct per-removal allocation for THIS batch, the verifier cannot independently confirm the BCU value. Garrett needs to either (a) replace with the sister-pattern-equivalent ~1.129 t value, or (b) provide explicit documentation showing 5.582 t is the correct allocation for 2-188. [log:certify_components.BCUs_Applied_to_Bio_Oil_Transport_Process, sister_batch_bcu_pattern, certify_sources_full_enumeration, _derived_sums._2-189_transport_process_breakdown_kg, _derived_sums._2-189_transport_process_breakdown_t, _derived_sums.transport_process_components_kg]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'Technically satisfied: BCU 5.582 t >= 2-188 transport process emissions 1.129 t (= 0.187 + 0.867 + 0.075). The KB rule "BCU MUST equal or exceed transport process activity" is met — and exceeded by 4.453 t. Embodied transport emissions (0.014 + 0.013 + 0.010 = 0.037 t) are NOT BCU-eligible per protocol — confirmed not double-claimed at the embodied level. **However, the magnitude of the excess is the substantive issue captured in Section 9.5 (and its Net CDR impact in Section 7.4); this row is just confirming the floor-rule is mechanically met.** [log:certify_components.BCUs_Applied_to_Bio_Oil_Transport_Process, certify_components.AECN_to_SOPOR_Tanker_Truck_Process, certify_components.SOPOR_to_Opelousas_Rail_Process, certify_components.Opelousas_to_Basco_Tanker_Truck_Process, _derived_sums.transport_embodied_total_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify_components]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Fail',
     'Certify Net = 25.503 t (displayed 25.50 t) = 23.139 + 5.582 - 3.071 - 0.146 — math reconciles MECHANICALLY ✓. But the underlying BCU input (5.582 t) is materially over-applied vs sister pattern (expected ~1.129 t per Section 9.5 finding), inflating Net by ~4.45 tCO2e. Sister-pattern-expected Net ≈ 23.139 + 1.129 - 3.071 - 0.146 = 21.051 t. The Certify-displayed 25.50 t cannot be independently verified without justification for the BCU magnitude. [log:certify_calculation_view.net_tco2e_precise, certify_calculation_view.net_tco2e_displayed, certify_calculation_view.independent_check, certify_calculation_view.expected_net_if_bcu_matched_transport_process, sister_batch_bcu_pattern, _derived_sums.net_tco2e_independent_recalc_precise]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     '4 non-descriptive filenames in Certify Sources (same shared rail-batch datapoints as sister batches 2-185, 2-186, 2-187, 2-189): "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF source), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance), "image (44).png" (SOPOR-Opelousas rail Watco distance email). Hygiene issue — content correct but filenames non-descriptive. **Additionally:** "Billing Truck 2314-T Corrections (1).pdf" has "-T" suffix where COBB row 65 BOL list and Ops Notes BOLs Loaded section both list "2314-R" — likely a filename typo (rail-load BOLs use "-R" suffix; this is the AECN BOL correction document referenced on sister batches). **Additionally:** the rail PROCESS EF datapoint is sourced from a PDF named "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to the rail Embodied EF datapoint. The EF value itself is correct per 2026 GLEC V3.2 (0.0259 kg/(t*mi) matches), but the filename references the Embodied tab specifically; if the PDF was an Embodied-tab-only export, this is a wrong source link. Worth Garrett verifying. Same flag set as 2-185/2-186/2-187/2-189 — propagates because these are SHARED rail-batch datapoint sources. [log:certify_sources_full_enumeration, certify_components.SOPOR_to_Opelousas_Rail_Process.ef_kg_per_t_mi, ef_verification.rail_process]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 source-datapoint links from 18 unique files. All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (2314-R, 2316-R, 2317-R), AECN LCA CI spreadsheet, LCA with stack emissions, Supporting GHG data, AECN Process Emissions Calculation, Standard EFs Railcar Embodied, Charm-A4 BCU certificate, scale tickets, CHN PDF, Ops Notes, route maps, Truck Embodied EF source. Per Document Location Rule, presence in Certify Sources is sufficient. (Note: Charm-A4 vs sisters\' Charm-A3 BCU certificate difference is captured in Section 9.5 as a substantive finding, not a sources hygiene issue.) [log:certify_sources_tab_total, certify_sources_tab_unique_files, certify_sources_full_enumeration]',
     'Certify Sources'),
]


def build_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'QA Checklist'

    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 100
    ws.column_dimensions['E'].width = 30

    row = 1

    for entry in ROWS:
        kind = entry[0]
        if kind == 'HEADER':
            ws.cell(row, 1, 'Charm Industrial - AECN Injection Batch QA Checklist')
            ws.cell(row, 1).font = Font(bold=True, size=14)
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
            ws.cell(row, 1).alignment = Alignment(horizontal='center', vertical='center')
            ws.row_dimensions[row].height = 22
            row += 1
        elif kind == 'META':
            ws.cell(row, 1, entry[1]).font = Font(bold=True)
            ws.cell(row, 2, entry[2])
            row += 1
        elif kind == 'SPACER':
            row += 1
        elif kind == 'COLUMNS':
            headers = ['Item #', 'Check Item', 'Status', 'Notes / Evidence', 'Verifier Reference']
            for c, h in enumerate(headers, start=1):
                cell = ws.cell(row, c, h)
                cell.fill = HEADER_FILL
                cell.font = HEADER_FONT
                cell.alignment = WRAP_CENTER
                cell.border = BORDER
            ws.row_dimensions[row].height = 28
            row += 1
        elif kind == 'SECTION':
            ws.cell(row, 1, entry[1]).font = SECTION_FONT
            ws.cell(row, 1).fill = SECTION_FILL
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
            ws.cell(row, 1).alignment = Alignment(horizontal='left', vertical='center', indent=1)
            ws.row_dimensions[row].height = 20
            row += 1
        else:
            item, check, status, evidence, verifier = entry
            ws.cell(row, 1, item)
            ws.cell(row, 2, check)
            ws.cell(row, 3, status)
            ws.cell(row, 4, evidence)
            ws.cell(row, 5, verifier)

            for c in range(1, 6):
                cell = ws.cell(row, c)
                cell.border = BORDER
                cell.alignment = WRAP

            if status == 'Fail':
                for c in range(1, 6):
                    ws.cell(row, c).fill = FAIL_FILL
                    ws.cell(row, c).font = FAIL_FONT
            elif status == 'Flag':
                for c in range(1, 6):
                    ws.cell(row, c).fill = FLAG_FILL
                    ws.cell(row, c).font = FLAG_FONT
            elif status == 'N/A':
                for c in range(1, 6):
                    ws.cell(row, c).font = NA_FONT

            ev_len = len(evidence or '')
            est_lines = max(1, ev_len // 90 + evidence.count('\n'))
            ws.row_dimensions[row].height = max(20, min(est_lines * 14, 320))

            row += 1

    row += 1
    pass_count = sum(1 for e in ROWS if len(e) >= 3 and e[0] not in ('HEADER','META','SPACER','COLUMNS','SECTION') and e[2] == 'Pass')
    fail_count = sum(1 for e in ROWS if len(e) >= 3 and e[0] not in ('HEADER','META','SPACER','COLUMNS','SECTION') and e[2] == 'Fail')
    flag_count = sum(1 for e in ROWS if len(e) >= 3 and e[0] not in ('HEADER','META','SPACER','COLUMNS','SECTION') and e[2] == 'Flag')
    na_count = sum(1 for e in ROWS if len(e) >= 3 and e[0] not in ('HEADER','META','SPACER','COLUMNS','SECTION') and e[2] == 'N/A')
    ws.cell(row, 1, 'SUMMARY').font = Font(bold=True, size=12)
    row += 1
    ws.cell(row, 1, 'Pass'); ws.cell(row, 2, pass_count)
    row += 1
    ws.cell(row, 1, 'Fail'); ws.cell(row, 2, fail_count)
    ws.cell(row, 1).fill = FAIL_FILL; ws.cell(row, 2).fill = FAIL_FILL
    row += 1
    ws.cell(row, 1, 'Flag'); ws.cell(row, 2, flag_count)
    ws.cell(row, 1).fill = FLAG_FILL; ws.cell(row, 2).fill = FLAG_FILL
    row += 1
    ws.cell(row, 1, 'N/A'); ws.cell(row, 2, na_count)
    row += 2
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '25.50 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'BCU OVER-APPLICATION (~4.45 tCO2e Net CDR over-claim, ~17% of stated Net). 2-188\'s "BCUs - Applied to Bio-Oil Transport Process Emissions" component is set at 5.582 tCO2e (constant_reduction = 5,581.52 kgCO2e), sourced from Charm-A4-2024-10-24-63-1976.pdf. Sister batches in the same railcar (TIMX201060) all have BCU = transport process emissions exactly: 2-186 = 1.621 t, 2-187 = 1.612 t, 2-189 = 1.617 t — all sourced from Charm-A3-2024-10-24-64-1976.pdf. For 2-188, transport process = 0.187 + 0.867 + 0.075 = 1.129 t, but BCU is 5.582 t — excess of 4.453 t flows into Net CDR as positive credit (since Net = Sequestrations + BCU − Activities − Uncertainty). Sister-pattern-expected Net for 2-188 ≈ 23.139 + 1.129 − 3.071 − 0.146 = 21.051 t vs Certify-displayed 25.50 t. Garrett needs to either (a) replace BCU with the sister-pattern-equivalent ~1.129 t value, or (b) provide explicit BCU Quant / allocation documentation showing 5.582 t is the correct per-removal allocation for THIS batch.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '5.4 + 2.7 (COBB-side: row 65 has TWO stale values — origin_quantity_kg = 71,010 [pre-correction; corrected = 80,610] AND offloaded_quantity_kg = 5,620.18 [pre-correction policy back-calc against old BOL; post-correction = 15,220.18]. Garrett-side data-provenance, verifier-irrelevant. Same origin_quantity_kg=71,010 stale flag on sister rows 63/64/66.); 9.9 (4 non-descriptive Certify filenames [image (44).png, Screenshot 2026-04-10 PM.png, Screenshot 2026-02-23 AM.png, Screenshot 2026-01-27 125934.png] propagating across rail batches, plus "Billing Truck 2314-T Corrections (1).pdf" with "-T" suffix where COBB lists "2314-R", plus rail PROCESS EF sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to rail Embodied EF, possible single-tab vs multi-tab PDF inconsistency)')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-188/Batch_2-188_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
