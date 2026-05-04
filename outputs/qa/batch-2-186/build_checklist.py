#!/usr/bin/env python3
"""Build Batch 2-186 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-186'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 03 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-04-30'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TIMX201060, offload 1 of 4 — NOT the last batch on the railcar)'),
    ('META', 'Net CDR (Certify)', '30.27 tCO2e'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "2-186" accessed at id 1SpqOOCx_bj3OeixkWvr6J-7dtK-OMDji; contains "2-186 Ops Notes Rail" sheet, Testing subfolder (CHN-186-189.pdf), Scale Tickets subfolder (full + empty JPGs). [log:drive_folder_url, batch_folder_contents]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains 2-186 Full Scale Ticket.jpg and 2-186 Empty Scale Ticket.jpg. One offload pair (consistent with batch being offload_1 of 4 on TIMX201060; subsequent sister batches will each contribute their own pair). Both files also uploaded to Certify Sources as "(2)" copies. [log:scale_tickets.full_ticket.filename_drive, scale_tickets.empty_ticket.filename_drive]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive > Testing contains CHN-186-189.pdf (7-page SGS Certificate of Analysis covering batches 2-186 through 2-189 + 3-55 through 3-57). Page 1 covers batch 2-186 explicitly. [log:lab_results.filename, lab_results.page_for_2_186]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-186 Ops Notes Rail" Google Sheet present in Drive folder; owner garrett.lutz@charmindustrial.com; modified 2026-04-30 12:59. Batch Composition (railcar TIMX201060), BOLs Loaded (3 inbound BOLs), and offload_1 row populated. Offload rows 2-4 correctly blank for this batch. [log:ops_notes.filename_drive]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'CHN PDF location field reads "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). No Vaulted references in any source. [log:lab_results.location_on_page]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both JPG images Read directly (NOT Drive OCR snippet). Full ticket #0770 dated 3-31-26 at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA, GROSS 77,560 lb (= axle sum 10,000 + 33,760 + 33,800). Empty ticket #0770 dated 4-01-26 08:07 same location, GROSS 29,380 lb (= axle sum 9,520 + 11,640 + 8,220). Both internally consistent (gross = axle sum). [log:scale_tickets.full_ticket, scale_tickets.empty_ticket]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Full ticket 2026-03-31; empty ticket 2026-04-01; injection completion 2026-04-03. Within 3 days. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Full ticket: Tractor CH2, Trailer KL-188 (handwritten). Empty ticket: Tractor CH2, Trailer KL-188. Same vehicle weighed at both events. [log:scale_tickets.tractor_match, scale_tickets.trailer_match]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     'NOT the last offload of the railcar (this is offload_1 of 4) — the rail last-offload conservatism policy does NOT apply here. Cargo (kg) is raw scale-ticket math using Ops Notes lbs->kg factor 0.453592: (77,560 - 29,380) lb × 0.453592 = 48,180 lb × 0.453592 = 21,854.06256 kg. Ops Notes offload_1 row shows Cargo Mass (kg) = 21,854.06256 — matches exactly. [log:scale_tickets.net_calc_kg, scale_tickets.net_calc_lb, ops_notes.batch_composition.lbs_to_kg_factor, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Per-offload rail batch (non-last): scale-ticket math is authoritative for this batch; BOL aggregate (80,610 kg) is for the railcar level, not per-offload. The 21,854.06256 kg derived from the scale tickets is THIS batch\'s injectate basis. Sparging deduction (next item) applied to that base. [log:scale_tickets.net_calc_kg, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied: 21,854.06256 × 0.0129 = 281.917407 kg sparging loss. Mass of Bio-Oil Injected = 21,854.06256 - 281.917407 = 21,572.14515 kg. Ops Notes shows exactly these values; arithmetic correct. [log:ops_notes.batch_composition.sparging_mass_loss_fraction, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg, ops_notes.trucks_unloaded_offload_1.sparging_loss_kg, ops_notes.trucks_unloaded_offload_1.mass_of_bio_oil_injected_kg]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Scale ticket net = 21,854.06 kg = Ops Notes Cargo (kg) = COBB offloaded_quantity_kg = Certify "Allocated Bio-Oil Mass - AECN via Rail" = 21,854.06256 kg. Post-sparging Mass of Injectant (Ops Notes) = 21,572.14515 kg shown in Certify as 21.572 t. All four sources align. [log:scale_tickets.net_calc_kg, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg, ops_notes.trucks_unloaded_offload_1.mass_of_bio_oil_injected_kg, cobb_row.offloaded_quantity_kg, certify_datapoints.Allocated Bio-Oil Mass - AECN via Rail]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Certify Sources: Documents camion 2317-R.pdf, Billing Truck 2316-R.pdf, Billing Truck 2314-T Corrections (1).pdf. Per Document Location Rule, presence in Certify Sources is sufficient (not required in Drive folder). Note filename typo "2314-T" in third file — see Section 9.9 / 9.10 hygiene flag. [log:certify_sources_tab_enumeration, BOLs_present_check]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2314-R, 2316-R, 2317-R) listed in COBB BOL_number field for batch 2-186 and in Ops Notes BOLs Loaded section. Destinations = SOPOR Quebec railyard (rail-batch convention). [log:ops_notes.BOLs_loaded, cobb_row.BOL_number]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL masses (26.05 + 29.06 + 25.50) = 80.61 MT = 80,610 kg (Ops Notes Total Loaded Mass). Per Max + Garrett confirmation 2026-04-30: this 80,610 kg is the AECN-CORRECTED inbound total (one of the original BOLs was incorrect; AECN sent a correction documented as "Billing Truck 2314-T Corrections (1).pdf" in Certify Sources, which closed the original 9,600 kg gap). Ops Notes correctly reflects the post-correction figures. This batch\'s offload mass = 21,854.06256 kg, < 80,610 kg railcar inbound. Rail-batch BOL mass check applied at railcar level (per SKILL.md). [log:ops_notes.BOLs_loaded, ops_notes.total_loaded_mass_MT, ops_notes.total_loaded_mass_kg, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN Quebec -> SOPOR (truck, 3 BOLs labeled with "-R" suffix matching rail-load convention) -> Opelousas LA (rail leg via railcar TIMX201060) -> Basco 6 (truck, this batch offload_1). Three legs documented across Drive + Certify Sources. [log:cobb_row.BOL_number, ops_notes.BOLs_loaded]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified: (1) AECN->SOPOR truck single distance = 173 km (= 107.5 mi) per Certify Datapoints "Distance from AECN to Sopor Quebec (truck)"; (2) SOPOR->Opelousas rail = 2,199 mi per "Distance from SOPOR to Opelousas (RAIL)"; (3) Opelousas->Basco truck per-batch = 42.9 mi (used directly, no allocation since each offload uses dedicated truck). Allocated distances applied to per-mile-EF embodied components: AECN->SOPOR Allocated = 140.70534 km (322.5 mi total trucking × 0.2711 batch share = 87.43 mi = 140.71 km within rounding); rail Allocated = 596.1677 mi (2,199 × 0.2711 batch share); Opelousas->Basco Allocated = 42.9 mi (full per-batch, no allocation). All match Ops Notes pre-computed values. [log:certify_datapoints, ops_notes.batch_composition, ops_notes.trucks_unloaded_offload_1.upstream_allocation_fraction, ops_notes.trucks_unloaded_offload_1.rail_allocated_distance_mi, ops_notes.trucks_unloaded_offload_1.truck_leg_1_AECN_to_SOPOR_allocated_distance_mi]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components in Certify: AECN to SOPOR Tanker Truck Transport Process Emissions (0.269 t), SOPOR to Opelousas Rail Transport Process Emissions (1.245 t), Opelousas to Basco - Tanker Truck Transport Process Emissions (0.107 t), AECN to SOPOR Tanker Truck Transport Embodied Emissions - AECN (0.021 t), SOPOR to Opelousas Rail Transport Embodied Emissions (0.019 t), Opelousas to Basco Tanker Truck Transport Embodied Emissions (0.010 t). [log:certify_components]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'Documents camion 2317-R.pdf, Billing Truck 2316-R.pdf, Billing Truck 2314-T Corrections (1).pdf in Certify Sources serve as both BOLs and billing for the 3 inbound truck legs (AECN convention). Charm-A5-2024-10-24-62-1976.pdf (Charm A5 manifest) also present for inbound logistics. [log:certify_sources_tab_enumeration]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder', 'Pass',
     'CHN-186-189.pdf (7 pages, SGS) in Drive Testing subfolder AND Certify Sources. Page 1 covers batch 2-186 (Certificate SR26-02264.001). [log:lab_results.filename, lab_results.page_for_2_186, lab_results.certificate_id]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-186 = 42.0% (ASTM D5291 Method C). Within AECN expected range (mean 39.42%, +/-2 SD ~27.2%-51.6%). [log:lab_results.carbon_pct, lab_results.carbon_within_AECN_range]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 7.0%, Nitrogen <0.75%, Viscosity 20.96 cSt @ 40C, Acid Number 59 mg KOH/g, Density 1.210 g/cm3 @ 15C. All within typical AECN ranges. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct, lab_results.viscosity_cSt_at_40C, lab_results.acid_number_mgKOH_per_g, lab_results.density_g_per_cm3_at_15C]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02264.001 explicitly labeled "BATCH 2-186" on page 1. Sampled 2026-04-01 11:50 at BASCO LOUISIANA. Sample drawn 2 days before injection completion 2026-04-03. [log:lab_results.certificate_id, lab_results.client_id_on_page, lab_results.sample_date]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate is recorded in Ops Notes Section 5.5. [log:_meta.oil_type]',
     'N/A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-186, Completion Date = 4/3/2026. Matches Certify removal date (03 Apr 2026) and COBB injection_completion_date (2026-04-03). [log:ops_notes.batch_number, ops_notes.completion_date, cobb_row.injection_completion_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 77,560 lb = Ops Notes Loaded Mass (lbs) 77,560 (exact). Empty ticket gross 29,380 lb = Ops Notes Unloaded Mass (lbs) 29,380 (exact). Both values verified by direct image Read of JPGs (per Drive-OCR-not-primary-source rule). Cargo (kg) using Ops Notes factor 0.453592: 48,180 × 0.453592 = 21,854.06256 = Ops Notes Cargo Mass (kg) 21854.06256 (exact). [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, ops_notes.batch_composition.lbs_to_kg_factor, ops_notes.trucks_unloaded_offload_1.loaded_mass_lb, ops_notes.trucks_unloaded_offload_1.unloaded_mass_lb, ops_notes.trucks_unloaded_offload_1.cargo_mass_kg]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:_meta.oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Flag',
     'COBB row for "2-186" verified: cell A = "2-186" ✓, BOL_number = "2314-R, 2316-R, 2317-R" matches Ops Notes BOLs Loaded ✓, offloaded_quantity_kg = 21,854.06256 = Ops Notes Cargo (kg) ✓, injection_completion_date = 2026-04-03 = Ops Notes 4/3/2026 ✓, pH = 2.9 = Ops Notes 2.9 ✓. **COBB-side data-provenance flag for Garrett (NOT 2-186-impacting):** Two COBB fields appear to reflect pre-correction BOL data: (a) 2-186\'s row shows origin_quantity_kg = 71,010 (= original short BOL), and (b) sister batch 2-188\'s row shows offloaded_quantity_kg = 5,620.18 (= 71,010 − 65,389.82, derived from pre-correction cap), whereas 2-188\'s own Ops Notes Rail correctly shows 2-188 Cargo (kg) = 15,220.18 (= 80,610 corrected BOL − 21,854.06 − 21,736.13 − 21,799.63, the policy-applied last-offload value with the post-correction cap). Per Max + Garrett confirmation 2026-04-30: original BOL was short by 9.6 MT (mass physically in the railcar but not on the original); AECN sent a corrected BOL ("Billing Truck 2314-T Corrections (1).pdf" in Certify Sources). Ops Notes throughout the railcar correctly reflects the post-correction inbound (80.61 MT) and policy-applies 2-188\'s Cargo using the corrected cap. The "_redo_" suffix in consumed_lot is consistent with the correction reset. COBB hasn\'t been refreshed for the correction. Verifier looks at Ops Notes / Certify (both correct), so this is operational data-provenance for Garrett to clean up rather than a verifier finding. [log:cobb_row_id_verified, cobb_cell_A_value, cobb_row, cobb_origin_vs_BOL_aggregate_discrepancy, ops_notes.BOLs_loaded, ops_notes.total_loaded_mass_MT, ops_notes.total_loaded_mass_kg, ops_notes.note_redo_in_lot_name, sister_batch_confirmation_2026-04-30]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_1 row pH = 2.9. COBB row injection_ph = 2.9. Match. [log:ops_notes.trucks_unloaded_offload_1.ph, cobb_row.injection_ph]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date = 4/3/2026; COBB injection_completion_date = 2026-04-03. Match. [log:ops_notes.completion_date, cobb_row.injection_completion_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include density entry — expected behavior. [log:_meta.oil_type]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity datapoints. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 since EFs are H1/H2 — matches H2 2025). [log:certify_sources_tab_enumeration, AECN_LCA_doc_check.AECN_LCA_CI_spreadsheet]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources, linked to AECN Pyrolysis Process Emissions. [log:certify_sources_tab_enumeration, AECN_LCA_doc_check.LCA_with_stack_emissions]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources, linked to AECN Pyrolysis Process Emissions. [log:certify_sources_tab_enumeration, AECN_LCA_doc_check.supporting_GHG_data]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t (precise) for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)". KB current value 0.10402 tCO2e/t (H2 2025). Within rounding. Verifies via independent calc: 21854.06 × 0.10402 = 2272.99 kg = 2.273 tCO2e ✓ matches Certify "AECN pyrolysis (from rail loads) - process emissions" component. [log:certify_datapoints.Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail), math_verification.AECN_pyrolysis_process]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)". KB current value 0.0212 tCO2e/t (precise per Certify modal is slightly more granular at 0.02116). Verifies: 21854.06 × 0.02116 = 462.42 kg = 0.462 tCO2e ✓ matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" component. [log:certify_datapoints.Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail), math_verification.AECN_pyrolysis_embodied]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Pyrolysis components apply 0.104 / 0.02116 to "Allocated Bio-Oil Mass - AECN via Rail" = 21,854.06 kg = pre-sparging Cargo (kg). Sparging is applied at injection (Section 2.6) and only affects Mass of Injectant for sequestration. Methodology correct. [log:certify_datapoints.Allocated Bio-Oil Mass - AECN via Rail, certify_uncertainty_modals.AECN pyrolysis (from rail loads) - process emissions]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc: 21.572 t (Mass of Injectant, post-sparging) × 0.420 (Carbon Content from CHN) × 3.667 = 33.221 tCO2e. Certify Sequestrations = 33.224 tCO2e. Within rounding (0.003 t delta, immaterial). [log:math_verification.gross_co2e_calc, certify_components.Injection Sequestration]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted: 3 transport process (AECN->SOPOR truck 0.269, SOPOR->Opelousas rail 1.245, Opelousas->Basco truck 0.107) + 3 transport embodied (0.021 + 0.019 + 0.010) + AECN pyrolysis process 2.273 + AECN pyrolysis embodied 0.462. Sum = 4.406 tCO2e. Each component math reconciles independently against per-mile-EF or per-T-mi-EF formulas. [log:certify_components, math_verification]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount = 174 kg = 0.174 tCO2e present in Calculation View. Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate discount from per-component +/- inputs — Isometric\'s aggregation is authoritative, so QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.4% carbon). Layer 3 here is presence + magnitude check: 0.174 t is ~0.5% of gross sequestration (33.224 t), consistent with typical AECN batch discount ratios. NOT independently reproducing the variance-propagation math against the Standard\'s formulation. [log:certify_components.totals.uncertainty_discount_kg, certify_components.totals.uncertainty_discount_t, certify_components.totals.sequestrations_total_t]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Pass',
     'Net = 33.224 (sequestrations) + 1.621 (BCU adjustments) - 4.405 (activities, displayed) - 0.174 (uncertainty) = 30.266 tCO2e. Certify shows Net CO2e Removed = 30.266 t (displayed as 30.27). Reconciles. [log:certify_components.totals, math_verification.net_calculation]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show +/-72.57 kg in INPUTS section (verified by opening each component modal): Injection Sequestration (Mass of product 21,572.15 ±72.57), AECN->SOPOR Truck Process (Mass of load 21,854.06 ±72.57), SOPOR->Opelousas Rail Process (Mass of load 21,854.06 ±72.57), Opelousas->Basco Truck Process (Mass of load 21,854.06 ±72.57), AECN Pyrolysis Process (Mass 21,854.06 ±72.57), AECN Pyrolysis Embodied (Mass 21,854.06 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi). Carbon Content uncertainty +/-0.168% (= 42 × 0.004 = 0.168, matches 0.4% relative). [log:certify_uncertainty_modals]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported +/- matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so +/-72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process). Verified by opening each component modal and reading the INPUTS section directly. Carbon content +/-0.168% = 42 × 0.004 confirms standard 0.4% relative uncertainty. Conservatism precondition (N_offloads ≥ N_inbound_BOLs) for the railcar will be formally validated at last batch (2-188 = offload_4). [log:certify_uncertainty_modals, rail_batch_specific_checks.section_8_N_offloads_vs_N_BOLs_check_deferred_to_2-188]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount = 0.174 t in Calculation View. Visible in net formula (33.224 - 4.405 + 1.621 - 0.174 = 30.266). Magnitude reasonable given mass and carbon uncertainty inputs. [log:certify_components.totals.uncertainty_discount_t, certify_components.totals.net_co2e_removed_t, certify_components.totals.sequestrations_total_t, certify_components.totals.activities_total_t, certify_components.totals.adjustments_total_t]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon (42.0%), distances (107.5/2199/42.9 mi), EFs (0.1143 truck process / 0.0259 rail process / 0.23756 truck embodied / 0.03113 rail embodied 2026 NEW value), and mass values (21,854.06 kg pre-sparging / 21,572.15 kg post-sparging) all within expected ranges. Both scale tickets internally consistent (gross = axle sum). All math reconciles to Certify within rounding. [log:lab_results.carbon_pct, certify_components, math_verification]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. Ops Notes "Oil Left in Railcar (MT/kg)" rows correctly blank for offload_1 (railcar still has remaining oil for sister batches). Last-offload mass reconciliation belongs to 2-188 QA. [log:ops_notes.oil_left_in_railcar_blank_offload_1_not_last]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch precondition for FC9 framing)', 'Pass',
     'Railcar TIMX201060 sister batches verified via 2-188\'s Ops Notes (the last-offload Ops Notes shows the closed mass balance for the full railcar): offload_1 = 2-186 Cargo 21,854.06 kg (raw); offload_2 = 2-187 Cargo 21,736.13 kg (raw); offload_3 = 2-189 Cargo 21,799.63 kg (raw); offload_4 = 2-188 Cargo 15,220.18 kg (policy-applied via FC11 last-offload conservatism using the CORRECTED BOL aggregate 80,610 as cap: 80,610 − 21,854.06 − 21,736.13 − 21,799.63 = 15,220.18). Sum of all 4 offloads = 80.61 MT = post-correction BOL aggregate exactly. Oil Left in Railcar = 0 ✓ (no heel — railcar fully drew down per Max 2026-04-30). N_offloads = 4 (>= N_inbound_BOLs = 3) — per-offload uncertainty framing (+/-72.57 kg) is conservative across the railcar; FC9 precondition satisfied. The 9.6 MT BOL correction is fully absorbed within 2-188\'s policy-applied last-offload Cargo (cap used = corrected 80,610, NOT pre-correction 71,010). For batch 2-186 specifically, this batch is the 1st pull, raw-scale-ticket-driven, and fully independent of the last-offload policy mechanics. [log:ops_notes.sister_batches_railcar_TIMX201060, ops_notes.total_loaded_mass_MT, ops_notes.total_loaded_mass_kg, ops_notes.trucks_unloaded_offload_1.upstream_allocation_fraction, rail_batch_specific_checks, sister_batch_confirmation_2026-04-30]',
     'KB Section 8 / FC9'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component = 33.224 tCO2e. Independent calc: 21.572 t (Mass of Injectant) × 0.42 × 3.667 = 33.221 t. Within rounding. Carbon content matches CHN PDF (42.0%). [log:certify_components.Injection Sequestration, math_verification.gross_co2e_calc]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Notably: rail embodied EF = 0.03113 kgCO2e/mi (NEW 2026 value 0.0000311307 MTCO2e/mi in native units, NOT stale 0.0000352240 carried by sister batch 2-182). Rail embodied finding from 2-182 is RESOLVED on 2-186. Allocated distances correctly use the post-correction BOL inbound (80,610 kg) as denominator (per Max + Garrett confirmation, see Section 5.4); the 9,600 kg heel is correctly excluded from per-batch allocation. All 6 transport components math-reconcile independently. [log:certify_uncertainty_modals.SOPOR to Opelousas Rail Transport Embodied Emissions, certify_datapoints.Emissions Factor - Vehicle Embodied Emissions -- Railcar, math_verification.rail_embodied]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:_meta.oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (2.273 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.462 t) present. Rail-batch naming convention used (deliberate signal to VVB). [log:certify_components]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" (1.621 t) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify_components.BCUs - Applied to Bio-Oil Transport Process Emissions]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU = 1.621 t = exact sum of 3 transport process activities (0.269 + 1.245 + 0.107 = 1.621). BCU >= activity (here exactly equal). Embodied emissions are NOT BCU-eligible per protocol — confirmed not double-claimed. [log:math_verification.BCU_offset_check]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify_components.Counterfactuals]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net = 30.266 t (displayed 30.27 t) = 33.224 - 4.405 + 1.621 - 0.174 ✓. Each input verified independently. [log:certify_components.totals, math_verification.net_calculation]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     '4 non-descriptive filenames in Certify Sources: "Screenshot 2026-04-10 at 3.19.33 PM.png" (likely Truck Transport EF source), "Screenshot 2026-02-23 at 11.29.10 AM.png" (likely Pyrolysis Process EF support), "Screenshot 2026-01-27 125934.png" (likely Opelousas-Basco distance), "image (44).png" (likely SOPOR-Opelousas rail distance). Same 4 files appear on sister batch 2-185 (shared rail-batch datapoints). Hygiene issue — content correct but filenames non-descriptive. **Additionally:** "Billing Truck 2314-T Corrections (1).pdf" has "-T" suffix where COBB lists "2314-R" — likely a filename typo (rail-load BOLs use "-R" suffix; document presumably for 2314-R based on COBB BOL list). [log:non_descriptive_filenames_for_FLAG_section_9_9, BOLs_present_check.filename_typo_2314_T_vs_2314_R]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 row instances enumerating 19 distinct source files (2-186 Ops Notes Rail.xlsx linked to 4 datapoints; Standard EFs PDF linked twice). All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (2314-R, 2316-R, 2317-R), AECN LCA CI spreadsheet, LCA with stack emissions, Supporting GHG data, Standard EFs Railcar Embodied, Charm-A5 manifest, AECN process EF calc, route maps. Per Document Location Rule, presence in Certify Sources is sufficient. [log:certify_sources_tab_total, certify_sources_tab_enumeration, AECN_LCA_doc_check]',
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
            ws.cell(row, 1, 'Charm Industrial — AECN Injection Batch QA Checklist')
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
            ws.row_dimensions[row].height = max(20, min(est_lines * 14, 240))

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
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '30.27 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'NONE — Net CDR 30.27 tCO2e is correctly calculated. Per Max + Garrett 2026-04-30: original BOL was short by 9.6 MT; AECN sent a corrected BOL ("Billing Truck 2314-T Corrections"). Ops Notes throughout the railcar correctly reflects the post-correction inbound (80.61 MT) and policy-applies 2-188 last-offload Cargo using the corrected cap: Cargo = 80,610 - sum(prior 3 offloads) = 15,220.18 kg. Sum of all 4 offloads = 80.61 MT = BOL aggregate; no heel. 2-186 is the 1st pull (raw scale ticket) and reconciles cleanly across scale tickets, Ops Notes, COBB offload row, and Certify.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '5.4 (COBB has stale entries on this railcar reflecting pre-correction BOL math: origin_quantity_kg=71,010 across all 4 sister rows, AND 2-188 row offloaded_quantity_kg=5,620 vs Ops Notes 15,220 — Garrett to refresh COBB; verifier-irrelevant); 9.9 (4 non-descriptive filenames + "2314-T" filename of the corrected BOL where COBB lists "2314-R")')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-186/Batch_2-186_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
