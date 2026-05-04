#!/usr/bin/env python3
"""Build Batch 2-190 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-190'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 10 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-03'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TILX200231 — NEW railcar; consumed_lot offload_1, FIRST pull. Sisters in COBB: 2-191=offload_2 row 68, 2-192=offload_3 row 69; running balance ~11,935 kg implies at least one more offload to come — last offload TBD.)'),
    ('META', 'Net CDR (Certify)', '26.28 tCO2e'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "2-190" at id 1rvCpANvDSh2G64SZQVPCyzrbDHg5NxmP under reporting period folder "4/6/26-4/12/26"; contains "2-190 Ops Notes Rail" Google Sheet, Testing subfolder (2-190-2-191 Tests.pdf), Scale Tickets subfolder (Full + Empty JPGs). [log:drive_folder_url, drive_folder_contents]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains 2-190 Full Scale Ticket.jpg (1.9 MB) and 2-190 Empty Scale Ticket.jpg (2.9 MB). One offload pair (consistent with offload_1 of railcar TILX200231 — each batch represents one truck-out delivery from the railcar). Both also uploaded to Certify Sources as "(1)" copies. Image pixels Read directly (NOT Drive OCR snippet, per OCR-vs-image rule). [log:scale_tickets.full_ticket.filename, scale_tickets.empty_ticket.filename]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive > Testing contains 2-190-2-191 Tests.pdf (2-page SGS Certificate of Analysis covering batches 2-190 + 2-191). Page 1 covers batch 2-190 (Certificate SR26-02484.001 Reissue 1, Client ID = "BATCH 2-190"). Reissue 1 supersedes 17-Apr-2026 issuance with Reissue Comment "Data Updated". [log:lab_results.certificate_2-190, lab_results.page_for_2-190, lab_results.client_id]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-190 Ops Notes Rail" Google Sheet (id 1I2sLZxEPOxZYj2hnCVeZo_eN8l3t6p6DlF-plG1GP1g) present in Drive folder; owner Garrett Lutz; modified May 1. Header (Batch number 2-190, Completion Date 4/10/2026), Batch Composition (railcar TILX200231, sparging 0.0129, lbs-to-kg 0.453592, route distances), BOLs Loaded (3 inbound BOLs: 2328-R 25.70 MT + 2339-R 25.63 MT + 2340-R 25.94 MT = 77.27 MT total), and offload table row 17 populated for offload_1 (Cargo 21,491.18896 kg, allocation 0.27813). [log:ops_notes.filename, ops_notes.header, ops_notes.bols_loaded, ops_notes.trucks_unloaded_row_17]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 1 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). Ops Notes references Opelousas->Basco truck leg (42.9 mi). No Vaulted references in any source. [log:lab_results.location]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both JPG images Read directly from pixels. Full ticket #13122260903B23 dated 4-03-26 11:21 at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA scale #3122, axle sum 10,060 + 33,680 + 33,040 = 76,780 lb (= certified gross). Empty ticket #13122260903823 dated 4-03-26 13:10 same location, axle sum 9,480 + 11,700 + 8,220 = 29,400 lb (= certified gross). Both internally consistent (gross = axle sum, no axle-vs-cert discrepancy). Same Weighmaster Mara Castill on both, Weigh Number 3823 both. [log:scale_tickets.full_ticket, scale_tickets.empty_ticket]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Both tickets dated 4-03-26 (April 3, 2026). Injection completion date per Ops Notes = 4/10/2026. 7 days between truck-out and injection — within 2-week tolerance. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.header.completion_date_B1]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Full ticket: Tractor Ch2, Trailer KL-188. Empty ticket: Tractor Ch2, Trailer KL-188. Same vehicle weighed at both events. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.empty_ticket.tractor_number, scale_tickets.match_check]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     '2-190 is consumed_lot offload_1 (1st pull), NOT the last offload of railcar TILX200231 — rail last-offload conservatism policy does NOT apply here. Cargo (kg) is raw scale-ticket math: (76,780 - 29,400) lb × 0.453592 = 47,380 lb × 0.453592 = 21,491.18896 kg. Ops Notes offload_1 row Cargo Mass (kg) = 21,491.18896 — exact match. [log:scale_tickets.net_mass_calc, ops_notes.batch_composition.constants.Lbs_to_kg_F5, ops_notes.trucks_unloaded_row_17.cargo_mass_kg_D17]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Per-offload rail batch (non-last): scale-ticket math is authoritative for THIS batch; BOL aggregate (77.27 MT) is at railcar level, not per-offload. The 21491.18896 kg from scale tickets is 2-190\'s injectate basis. Sparging deduction (Section 2.6) applied to that base. [log:scale_tickets.net_mass_calc.net_kg_via_mult_factor, ops_notes.trucks_unloaded_row_17.cargo_mass_kg_D17]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied: 21,491.18896 × 0.0129 = 277.2363376 kg sparging loss. Mass of Bio-Oil Injected = 21,491.18896 - 277.2363376 = 21,213.95262 kg. Ops Notes shows exactly these values (E17, F17); arithmetic correct. [log:ops_notes.batch_composition.constants.Sparging_Mass_Loss_F6, ops_notes.trucks_unloaded_row_17.cargo_mass_kg_D17, ops_notes.trucks_unloaded_row_17.sparging_loss_kg_E17, ops_notes.trucks_unloaded_row_17.mass_of_bio_oil_kg_F17, ops_notes.sparging_check]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Scale ticket net = 21491.18896 kg = Ops Notes Cargo (kg) = COBB row 67 offloaded_quantity_kg = Certify "Allocated Bio-Oil Mass - AECN via Rail" 21.491 t. Post-sparging Mass of Injectant (Ops Notes F17) = 21213.95262 kg shown in Certify Datapoints as 21.214 t. All four sources align. [log:scale_tickets.net_mass_calc.net_kg_via_mult_factor, ops_notes.trucks_unloaded_row_17.cargo_mass_kg_D17, ops_notes.trucks_unloaded_row_17.mass_of_bio_oil_kg_F17, cobb.row_67_data.G67_offloaded_quantity_kg]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Certify Sources AND in Drive shared folder (Charm Industrial > Logistics > BOLs & Freight Documentation > 2026 BOLs > Rail > March > TILX200231): "Correction Costum Documents 2328-R.pdf", "Documents camion 2339-R.pdf", "Documents Camion 2340-R corr (1).pdf". [log:bol.bols, bol.drive_location, certify_sources_tab_enumeration]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2328-R, 2339-R, 2340-R) listed in COBB row 67 BOL_number field for batch 2-190 and in Ops Notes BOLs Loaded section. BOL 2339-R Read directly: Ship To = "CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau Québec G4Z 2L6" (= SOPOR Quebec railyard) ✓; From = "BioEnergie AE Côte-Nord Canada, Port-Cartier Québec" (= AECN) ✓. [log:bol.bols.1.verification_notes.origin_short, bol.bols.1.verification_notes.destination_short, ops_notes.bols_loaded, cobb.row_67_data.E67_BOL_number]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL masses (25.70 + 25.63 + 25.94) = 77.27 MT = 77270 kg (Ops Notes Total Loaded Mass = COBB origin_quantity_kg). This batch\'s offload mass = 21491.18896 kg, well below 77270 kg railcar inbound. Rail-batch BOL mass check applied at railcar level. BOL 2339-R "Qty shipped" highlighted on Page 2 = 25.63 MT = scale ticket NET 25630 kg on Page 3 (authoritative per skill). [log:bol.bol_aggregate_mt, bol.bol_aggregate_kg, bol.bols.1.verification_notes.page2_qty_shipped_highlighted_mton, bol.bols.1.verification_notes.page3_scale_ticket.masse_nette_kg, ops_notes.bols_loaded.total_loaded_mass_B13_mt, ops_notes.trucks_unloaded_row_17.cargo_mass_kg_D17, cobb.row_67_data.H67_origin_quantity_kg]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN (BioEnergie AE Côte-Nord, Port-Cartier QC) -> SOPOR (Société du port ferroviaire de Baie-Comeau, via 3 trucks each labeled "-R" rail-load suffix) -> Opelousas LA (rail leg via railcar TILX200231) -> Basco 6 (truck, this batch consumed_lot offload_1). Three legs documented across Drive + Certify Sources. BOL 2339-R verified as AECN->SOPOR truck ship date 2026-03-17. [log:bol.bols.1.verification_notes, cobb.row_67_data.E67_BOL_number, ops_notes.bols_loaded, certify.components]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified: (1) AECN->SOPOR truck full single-truck distance 173 km (= 107.5 mi) per Certify Datapoint "Distance from AECN to Sopor Quebec (truck)", and Allocated Distance AECN to Sopor Quebec 144.34997 km = 322.5 mi caravan total × 1.609344 km/mi × 0.27813 batch share; (2) SOPOR->Opelousas rail full 2,199 mi per "Distance from SOPOR to Opelousas (RAIL)", Allocated 611.61 mi (2,199 × 0.27813); (3) Opelousas->Basco truck per-batch 42.9 mi (full = allocated since each offload uses dedicated truck). All match Ops Notes pre-computed values for offload_1 (I17 = 611.6102565, J17 = 89.697275 mi). [log:section_3_route_distances]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components in Certify: AECN to SOPOR Tanker Truck Process (0.264 t), SOPOR to Opelousas Rail Process (1.224 t), Opelousas to Basco Tanker Truck Process (0.105 t), AECN to SOPOR Tanker Truck Embodied (0.021 t), SOPOR to Opelousas Rail Embodied (0.019 t), Opelousas to Basco Tanker Truck Embodied (0.010 t). [log:certify.components.removal_activities.bio_oil_transport]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'All 3 BOL/billing PDFs serve as both BOL and billing for the inbound truck legs (AECN convention). Charm-A4-2024-10-24-63-1976.pdf (BCU certificate) also present in Sources tab. See Section 9.9 for BCU cert filename pattern observation. [log:certify_sources_tab_enumeration]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder', 'Pass',
     '"2-190-2-191 Tests.pdf" (2-page SGS Certificate, in Drive Testing) — 2-190 on page 1, 2-191 on page 2. SGS Order No 5437581. [log:lab_results.filename, lab_results.sgs_order_no, lab_results.page_for_2-190]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-190 = 37.5% (m/m) (ASTM D5291 Method C). Within AECN expected range (mean 39.42%, ±2 SD ~27.2%-51.6%). [log:lab_results.carbon_pct, lab_results.carbon_within_range]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 7.3%, Nitrogen 1.28%, Kinematic Viscosity 16.08 cSt @ 40°C, Acid Number 58 mg KOH/g, Density 1.196 g/cm³ @ 15°C. All within typical AECN ranges. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct, lab_results.kinematic_viscosity_40C_cSt, lab_results.acid_number_mg_KOH_g, lab_results.density_15C_g_per_cm3]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02484.001 Reissue 1 explicitly labeled "BATCH 2-190" on page 1. Sampled 2026-04-05 02:20 at BASCO LOUISIANA (after offload_1 truck arrived 2026-04-03). Sample ~2 days after offload, ~5 days before injection completion 2026-04-10. Reissue 1 supersedes 17-Apr-2026 issuance ("Data Updated" comment). [log:lab_results.certificate_2-190, lab_results.client_id, lab_results.sampled_at, lab_results.location, lab_results.reissue_status]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate is recorded in Ops Notes Section 5.5. [log:oil_type]',
     'N/A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-190 (B3), Completion Date = 4/10/2026 (B1). Matches Certify removal date (10 Apr 2026) and COBB row 67 injection_completion_date (2026-04-10). [log:ops_notes.header, cobb.row_67_data.L67_injection_completion_date, certify.removal_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 76,780 lb = Ops Notes offload_1 Loaded Mass (lbs) B17 76,780 (exact). Empty ticket gross 29,400 lb = Ops Notes offload_1 Unloaded Mass (lbs) C17 29,400 (exact). Both values verified by direct image Read of JPGs. Cargo (kg) using Ops Notes factor 0.453592: 47,380 × 0.453592 = 21,491.18896 = Ops Notes offload_1 Cargo Mass (kg) D17 21,491.18896 (exact). [log:scale_tickets.full_ticket.gross_lb, scale_tickets.empty_ticket.gross_lb, ops_notes.batch_composition.constants.Lbs_to_kg_F5, ops_notes.trucks_unloaded_row_17.loaded_mass_lb_B17, ops_notes.trucks_unloaded_row_17.unloaded_mass_lb_C17, ops_notes.trucks_unloaded_row_17.cargo_mass_kg_D17]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Pass',
     'COBB row 67 for "2-190" verified: cell A67 = "2-190" ✓, consumed_lot C67 = "Rail_TILX200231_3.23.2026_offload_1" ✓ (matches Ops Notes A17), BOL_number E67 = "2328-R, 2339-R, 2340-R" matches Ops Notes BOLs Loaded ✓, offloaded_quantity_kg G67 = 21,491.18896 = Ops Notes offload_1 Cargo (kg) ✓, origin_quantity_kg H67 = 77,270 = Ops Notes Total Loaded Mass × 1000 ✓ (NEW railcar TILX200231 — no stale-COBB issue carried forward from prior railcar TIMX201060), injection_completion_date L67 = 2026-04-10 = Ops Notes 4/10/2026 ✓, injection_ph M67 = 3 = Ops Notes G17 ✓. All 7 cross-source values match. [log:cobb_row_id_verified, cobb_cell_A_value, cobb.row_67_data, cobb.cross_check_vs_ops_notes]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_1 row pH (G17) = 3 (whole-number entry). COBB row 67 pH (M67) = 3. Both sources match. Lab CoA does not measure pH (in-house Charm injection-time measurement). Sister rows 68 (2-191) and 69 (2-192) on same railcar TILX200231 also show pH = 3, consistent within-railcar pattern. [log:ops_notes.trucks_unloaded_row_17.ph_G17, cobb.row_67_data.M67_injection_ph, ph_observation]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'All three sources align: Ops Notes Completion Date 4/10/2026, COBB row 67 injection_completion_date 2026-04-10, Certify removal date 10 Apr 2026. [log:ops_notes.header.completion_date_B1, cobb.row_67_data.L67_injection_completion_date, certify.removal_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include a density entry — expected behavior. (Lab CoA reports density 1.196 g/cm³ but this is for analytical reference only, not used by Ops Notes mass conversion.) [log:oil_type, lab_results.density_15C_g_per_cm3]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) datapoint. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 — H2 2025 EFs carry through Q1/Q2 2026 reporting). [log:certify_sources_tab_enumeration, certify_required_aecn_docs_present.AECN_LCA_CI_spreadsheet]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources_tab_enumeration, certify_required_aecn_docs_present.LCA_with_stack_emissions]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources_tab_enumeration, certify_required_aecn_docs_present.Supporting_GHG_data]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" (Datapoints view shows 0.10 rounded). KB current native value 0.10402 tCO2e/t (H2 2025) — matches within rounding. Independent calc: 21.491 t × 0.104 = 2.235 tCO2e ✓ matches Certify "AECN pyrolysis (from rail loads) - process emissions" 2.235 t exactly. [log:certify.components.removal_activities.pyrolysis.AECN_pyrolysis_from_rail_loads_process_t, certify_uncertainty_modals_opened.AECN_Pyrolysis_Process]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)" (Datapoints view shows 0.02 rounded). KB current value 0.0212 tCO2e/t (precise per Certify modal at 0.02116). Independent calc: 21.491 × 0.02116 → matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" 0.455 t. [log:certify.components.removal_activities.pyrolysis.AECN_pyrolysis_from_rail_loads_embodied_t, certify_uncertainty_modals_opened.AECN_Pyrolysis_Embodied]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Pyrolysis components apply 0.104 / 0.02116 to "Allocated Bio-Oil Mass - AECN via Rail" = 21491.18 kg = pre-sparging Cargo (kg). Sparging is applied at injection (Section 2.6) and only affects Mass of Injectant for sequestration. Methodology correct per FC6.6. [log:certify_uncertainty_modals_opened.AECN_Pyrolysis_Process.mass_kg, certify_uncertainty_modals_opened.AECN_Pyrolysis_Process.mass_basis, certify_uncertainty_modals_opened.AECN_Pyrolysis_Embodied.mass_basis]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc with full precision: 21.21395262 t (Mass of Injectant, post-sparging, F17/1000) × 0.375 (Carbon Content from CHN) × 3.667 = 29.171 tCO2e. Certify Sequestrations 29.172 tCO2e — match within rounding (0.001 t / 0.003%). Display calc: 21.214 × 0.375 × 3.667 = 29.166. [log:gross_to_net_independent_calc, certify.components.sequestrations]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted (3 transport process + 3 transport embodied + 2 pyrolysis): AECN->SOPOR truck process 0.264, SOPOR->Opelousas rail process 1.224, Opelousas->Basco truck process 0.105, AECN->SOPOR truck embodied 0.021, SOPOR->Opelousas rail embodied 0.019, Opelousas->Basco truck embodied 0.010, AECN pyrolysis process 2.235, AECN pyrolysis embodied 0.455. Sum = 4.333 tCO2e (Calc View shows 4.334 — 0.001 rounding) ✓ matches Certify Activities total. Each component independently math-reconciles. [log:certify.components.removal_activities, certify.calc_view.activities_t]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount ~0.154 t (calculated as 29.172 + 1.593 - 4.334 - 26.277 net = 0.154 t) present in Calculation View. Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate from per-component ± inputs — Isometric\'s aggregation is authoritative; QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.4% carbon = ±0.15%). 0.154 t is ~0.585% of gross sequestration (29.172 t), consistent with typical AECN rail batch ratios (sister rail batches 2-186/2-187/2-189 were ~0.5%). [log:certify.calc_view.uncertainty_discount_t_implied, certify.calc_view.uncertainty_discount_pct_of_gross]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Pass',
     'Net = 29.172 (sequestrations) + 1.593 (BCU adjustments) - 4.334 (activities) - 0.154 (uncertainty) = 26.277 tCO2e. Certify shows Net CO2e Removed = 26.277 t (displayed as 26.28). Reconciles exactly. [log:gross_to_net_independent_calc, certify.calc_view.net_t]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show ±72.57 kg in INPUTS section (verified by opening each component modal individually): Injection Sequestration (Mass of product 21,213.95 ±72.57), AECN->SOPOR Truck Process (Mass of load 21,491.18 ±72.57), SOPOR->Opelousas Rail Process (Mass of load 21,491.18 ±72.57), Opelousas->Basco Truck Process (Mass of load 21,491.18 ±72.57), AECN Pyrolysis Process (Mass 21,491.18 ±72.57), AECN Pyrolysis Embodied (Mass 21,491.18 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi) — confirmed by opening AECN->SOPOR Truck Embodied and SOPOR->Opelousas Rail Embodied modals. Carbon Content uncertainty ±0.15% (= 37.5 × 0.004 = 0.15, matches 0.4% relative). [log:certify_uncertainty_modals_opened]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported ± matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so ±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process). Verified by opening each component modal and reading the INPUTS section directly. Carbon content ±0.15% = 37.5 × 0.004 confirms standard 0.4% relative uncertainty. Conservatism precondition (N_offloads ≥ N_inbound_BOLs) for railcar TILX200231 will be formally validated at the railcar\'s last batch QA (TBD — sisters 2-191/2-192 visible in COBB are offloads 2 and 3; remaining ~11,935 kg implies at least one more offload). [log:certify_uncertainty_modals_opened, fc9_per_removal_uncertainty_framing_check]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount ~0.154 t in Calculation View. Visible in net formula: 29.172 sequestrations + 1.593 BCU - 4.334 activities - 0.154 uncertainty = 26.277 t Net. Magnitude reasonable given mass and carbon uncertainty inputs. [log:certify.calc_view.uncertainty_discount_t_implied, certify.calc_view.net_t]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon (37.5%, within ±2 SD), distances (107.5/2199/42.9 mi full-leg + 89.7/611.61 mi allocated), EFs (0.1143 truck process / 0.0259 rail process / 0.23756 truck embodied / 0.03113 rail embodied — 2026 corrected value, no stale-EF carryover). Mass 21,491.19 kg pre-sparging / 21,213.95 kg post-sparging within expected per-truck offload range. Both scale tickets internally consistent (gross = axle sum). All math reconciles to Certify within rounding. BCU 1.593 t = exact sum of process transport (0.264 + 1.224 + 0.105 = 1.593) — clean BCU calculation, no over- or under-application. [log:lab_results.carbon_pct, certify.components, certify.datapoints, certify_uncertainty_modals_opened.BCU_modal]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. Ops Notes "Oil Left in Railcar (MT/kg)" cells (B23/B24) correctly blank for 2-190 — railcar TILX200231 still has ~55.78 MT remaining (sisters 2-191/2-192/etc to be drawn). Last-offload mass reconciliation belongs to whichever batch is the railcar\'s physical last pull (TBD, after offloads 2 and 3 already in COBB). [log:ops_notes.totals_and_balance, fc11_railcar_balance_check]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch precondition for FC9 framing)', 'Pass',
     '2-190 is the 1st pull of new railcar TILX200231. Sisters in COBB: 2-191 row 68 = offload_2 (21409.5424 kg), 2-192 row 69 = offload_3 (22434.66032 kg); 2-193 not in COBB. Cumulative through offload_3 = 65335.39168 kg of 77270 kg loaded; ~11934.61 kg remains so at least one more offload is coming. Last-offload checks (FC11 back-calc, FC9 N_offloads ≥ N_inbound_BOLs) belong to the railcar\'s physical last pull, not 2-190. [log:cobb.sister_batches_same_railcar, cobb.sister_offload_kg_sum_through_offload_3, cobb.remaining_kg_after_offload_3, cobb.row_67_data.G67_offloaded_quantity_kg, cobb.row_67_data.H67_origin_quantity_kg, fc11_railcar_balance_check, fc9_per_removal_uncertainty_framing_check]',
     'KB Section 8 / FC9 / FC11'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component 29.172 tCO2e. Independent calc: 21.21395262 t (Mass of Injectant) × 0.375 × 3.667 = 29.171 t. Match within rounding (0.001 t / 0.003%). Carbon content matches CHN page 1 (37.5%). [log:certify.components.sequestrations, lab_results.carbon_pct, gross_to_net_independent_calc]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components, each math-reconstructed independently from the modal inputs:\n• AECN→SOPOR truck process: 21.491 t × 107.5 mi × 0.0001143 MTCO2e/(t·mi) = 0.264 t (matches Certify 0.264)\n• SOPOR→Opelousas rail process: 21.491 × 2199 × 0.0000259 = 1.224 t (matches 1.224)\n• Opelousas→B6 truck process: 21.491 × 42.9 × 0.0001143 = 0.105 t (matches 0.105)\n• AECN→SOPOR truck embodied: 0.23756 kgCO2e/mi × 89.69 mi (= 144.34997 km allocated / 1.609344) = 21.30 kg = 0.021 t (matches 0.021)\n• SOPOR→Opelousas rail embodied: 0.03113 × 611.61 mi = 19.04 kg = 0.019 t (matches 0.019)\n• Opelousas→B6 truck embodied: 0.23756 × 42.9 → 0.010 t (matches 0.010)\nRail embodied EF 0.03113 kgCO2e/mi = 0.0000311307 MTCO2e/mi (2026 corrected — NOT stale 0.0000352240 carried by 2-182, fix is propagated). Allocation fraction 0.27813 = 21491.18896 / 77270. [log:certify.components.removal_activities.bio_oil_transport, certify_uncertainty_modals_opened.AECN_to_SOPOR_Truck_Process, certify_uncertainty_modals_opened.SOPOR_to_Opelousas_Rail_Process, certify_uncertainty_modals_opened.Opelousas_to_Basco_Truck_Process, certify_uncertainty_modals_opened.AECN_to_SOPOR_Truck_Embodied, certify_uncertainty_modals_opened.SOPOR_to_Opelousas_Rail_Embodied, certify_uncertainty_modals_opened.Opelousas_to_Basco_Truck_Embodied, cobb.row_67_data.H67_origin_quantity_kg, cobb.row_67_data.G67_offloaded_quantity_kg, ops_notes.trucks_unloaded_row_17.upstream_allocation_H17, section_3_route_distances]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both pyrolysis components present, math-reconstructed independently:\n• AECN pyrolysis (from rail loads) — process emissions: 21.491 t × 0.104 tCO2e/t = 2.235 t (matches Certify 2.235)\n• AECN pyrolysis (from rail loads) — embodied emissions: 21.491 × 0.02116 = 0.455 t (matches 0.455)\nMass basis = "Allocated Bio-Oil Mass - AECN via Rail" 21491.18 kg (pre-sparging, per FC6.6 — the Mass datapoint is shared with the transport-process components, not the post-sparging Mass of Injectant). Rail-batch naming convention "(from rail loads)" is the deliberate VVB signal to expect scale tickets as authoritative mass source. [log:certify.components.removal_activities.pyrolysis, certify_uncertainty_modals_opened.AECN_Pyrolysis_Process, certify_uncertainty_modals_opened.AECN_Pyrolysis_Embodied]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" (1.593 t) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify.components.adjustments_reductions]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU 1.593 t = exact sum of 3 transport process activities (0.264 + 1.224 + 0.105 = 1.593). BCU >= activity (here exactly equal). Embodied transport emissions (0.021 + 0.019 + 0.010 t) are NOT BCU-eligible per protocol — confirmed not double-claimed. No over-application of BCU credit (unlike sister-batch 2-188 where BCU value diverged from sister pattern). [log:certify.components.adjustments_reductions.BCUs_applied_to_bio_oil_transport_process_t, certify.components.adjustments_reductions.matches_process_transport_sum, certify_uncertainty_modals_opened.BCU_modal.matches_process_transport_sum_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify.components.counterfactuals_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net = 26.277 t (displayed 26.28 t) = 29.172 - 4.334 + 1.593 - 0.154 ✓. Each input verified independently. [log:certify.calc_view.net_t, gross_to_net_independent_calc]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     '4 non-descriptive filenames in Certify Sources (same shared rail-batch datapoints as sister batches 2-185, 2-186, 2-187, 2-189): "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF source), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance), "image (44).png" (SOPOR-Opelousas rail Watco distance email). Hygiene issue — content correct but filenames non-descriptive. **Additionally:** the rail PROCESS EF datapoint is sourced from a PDF named "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to the rail Embodied EF datapoint (correctly). The EF value itself is correct per 2026 GLEC V3.2, but the filename references the Embodied tab specifically; if the PDF was an Embodied-tab-only export, the link to the process EF datapoint references the wrong tab/sheet. **Additionally (NEW for 2-190):** "AECN Process Emissions Calculation.xlsx" is linked to the "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint. File named "Process Emissions" linked to Embodied datapoint — possible mislink; worth Garrett verifying whether this xlsx contains both process AND embodied calcs (in which case the link is fine but the filename is incomplete) OR is process-only (in which case the link is wrong). **Additionally (BCU cert filename observation):** BCU certificate file is "Charm-A4-2024-10-24-63-1976.pdf" — same filename as 2-188 (where Max flagged it as DIFFERENT from sisters\' "Charm-A3-2024-10-24-64-1976.pdf"). For 2-190 this is a NEW railcar (TILX200231) and the BCU quantity 1.593 t exactly equals the process transport sum, so the QUANTITY is correct. Filename pattern (A4 vs A3) is a Garrett-side question of whether different railcars use different BCU certificates as designed. Not verifier-impacting since quantity reconciles. [log:certify_sources_tab_enumeration]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 source-datapoint links. All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (2328-R, 2339-R, 2340-R), AECN LCA CI spreadsheet (Bioenergy AE Cote-Nord 1Jul2025-31Dec2025), LCA with stack emissions (BH 2025), Supporting GHG data (31Dec2025), AECN Process Emissions Calculation, Standard EFs Railcar Embodied, Charm-A4 BCU certificate, scale tickets (Full + Empty as "(1)" copies), CHN PDF (2-190-2-191 Tests), Ops Notes Rail (xlsx export, twice), AECN to SOPOR (Baie Comeau) route map, Truck Embodied Emissions image, plus 4 generic-named screenshots/images flagged in 9.9. Per Document Location Rule, presence in Certify Sources is sufficient. [log:certify_sources_tab_total, certify_sources_tab_enumeration, certify_required_aecn_docs_present]',
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
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '26.28 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'NONE — Net CDR 26.28 tCO2e is correctly calculated. 2-190 is the FIRST offload of NEW railcar TILX200231 (consumed_lot offload_1); raw-scale-ticket-driven and reconciles cleanly across scale tickets, Ops Notes, COBB row 67 offloaded_quantity_kg, and Certify Allocated Bio-Oil Mass (all = 21,491.19 kg). Independent gross-to-net calc reproduces Certify exactly: 21.21395 t × 0.375 × 3.667 = 29.171 t Sequestrations; 4.334 t Activities; 1.593 t BCU offset (= exact process transport sum 0.264 + 1.224 + 0.105); 0.154 t uncertainty discount → Net 26.277 t (displayed 26.28). The railcar last-offload reconciliation belongs to whichever future batch is TILX200231\'s physical last pull (sisters 2-191 row 68 = offload_2 and 2-192 row 69 = offload_3 already in COBB; remaining ~11,935 kg implies at least one more offload). Section 7a per-offload uncertainty conservatism precondition check (N_offloads ≥ N_inbound_BOLs = 3) is DEFERRED to that last batch\'s QA per FC9.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '9.9 only (Garrett-side hygiene, NOT verifier-impacting): (a) 4 non-descriptive Certify filenames [image (44).png, Screenshot 2026-04-10 PM.png, Screenshot 2026-02-23 AM.png, Screenshot 2026-01-27 125934.png] propagating across rail batches; (b) rail PROCESS EF sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to rail Embodied EF, possible single-tab vs multi-tab PDF inconsistency; (c) NEW for 2-190: "AECN Process Emissions Calculation.xlsx" linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint, worth Garrett verifying whether xlsx is multi-tab or mislinked; (d) BCU certificate filename "Charm-A4-2024-10-24-63-1976.pdf" — same filename as sister 2-188 where Max questioned A4 vs sisters\' A3 pattern; for 2-190 this is a NEW railcar (TILX200231) so the cert may legitimately differ. BCU quantity 1.593 t exactly matches process transport sum so the QUANTITY is correct; only the filename pattern is in question.')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-190/Batch_2-190_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
