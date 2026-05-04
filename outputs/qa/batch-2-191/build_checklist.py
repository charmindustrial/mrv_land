#!/usr/bin/env python3
"""Build Batch 2-191 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-191'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 11 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-04'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TILX200231 — sister to 2-190; consumed_lot offload_2. COBB sister window: R67 2-190 offload_1, R68 2-191 offload_2 (THIS), R69 2-192 offload_3. Cumulative offloads 1-3 = 65,335.39 kg of 77,270 kg loaded; ~11,934.61 kg remaining → at least one more offload to come. 2-191 is NOT the last offload of TILX200231; FC11 last-offload mass policy DOES NOT apply.)'),
    ('META', 'Net CDR (Certify)', '25.71 tCO2e'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "2-191" at id 1OaI8UemihJSE-NyYwxqC8g3GLUieaii0; contains "2-191 Ops Notes Rail" Google Sheet (id 11oXg6BYai33FMGmxH7c-w4ybogEZUFcSVAF5afwnphM, owner Garrett Lutz), Testing subfolder (2-190-2-191 Tests.pdf, bundled CHN report shared with sister batch 2-190), Scale Tickets subfolder (Full + Empty JPGs). [log:drive_folder_url, drive_folder_inventory]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains "2-191 Full Scale Ticket.jpg" (~3.0 MB) and "2-191 Empty Scale Ticket.jpg" (~2.3 MB). One offload pair (consistent with offload_2 of railcar TILX200231 — each batch represents one truck-out delivery from the railcar). Both also uploaded to Certify Sources as "(1)" copies. Image pixels Read directly via image tool (NOT Drive OCR snippet, per memory feedback_ocr_not_primary_source). [log:scale_tickets.full_ticket.filename, scale_tickets.empty_ticket.filename]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive > Testing contains "2-190-2-191 Tests.pdf" (single SGS Certificate of Analysis covering both batches 2-190 and 2-191; 2-191 on page 2). Page 2 covers batch 2-191 (Certificate SR26-02484.002 Reissue 1, Client ID = "BATCH 2-191"). Reissue 1 supersedes 17-Apr-2026 issuance with Reissue Comment "Data Updated". [log:lab_results.filename, lab_results.certificate_number_2-191, lab_results.client_id_on_page, lab_results.reissue_comment]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-191 Ops Notes Rail" Google Sheet present in Drive folder; owner Garrett Lutz; modified May 1. Header (Batch number 2-191, Completion Date 4/11/2026), Batch Composition (railcar TILX200231, sparging 0.0129, lbs-to-kg 0.453592, route distances), BOLs Loaded (3 inbound BOLs: 2328-R 25.7 MT + 2339-R 25.63 MT + 2340-R 25.94 MT; aggregate = 77.27 MT total), and offload table row 2 populated for offload_2 (Loaded 76780 lb, Unloaded 29580 lb, Cargo 21,409.5424 kg, allocation 0.27708, Rail 609.29 mi, Truck Leg 1 89.36 mi). Row 1 (offload_1) also visible (sister batch 2-190 carryover values). [log:ops_notes_rail.filename, ops_notes_rail.batch_number, ops_notes_rail.completion_date, ops_notes_rail.bols_loaded, ops_notes_rail.bol_aggregate_MT, ops_notes_rail.offload_table.1]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 2 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). Ops Notes references Opelousas->Basco truck leg 42.9 mi. No Vaulted references in any source. [log:lab_results.location]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both JPG images Read directly from pixels (per OCR-vs-image rule). Full ticket #13122280093825, right-edge id "KL-152", dated 4-03-26 11:38, at PILOT TRAVEL CENTER I-49 EXT 40 BUNKIE LA scale 3122; axle sum 10,260 + 33,220 + 33,300 = 76,780 lb (= certified gross, ✓). Empty ticket #13122280083827, right-edge id "KL-152", dated 4-03-26 14:12 same location/scale; axle sum 9,540 + 11,680 + 8,360 = 29,580 lb (= certified gross, ✓). Both internally consistent (gross = axle sum, no axle-vs-cert discrepancy). Same Weighmaster signature "Mache Castille" on both, same Weigh Number 3822. [log:scale_tickets.full_ticket, scale_tickets.empty_ticket]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Both tickets dated 4-03-26 (April 3, 2026). Injection completion date per Ops Notes = 4/11/2026. 8 days between truck-out and injection — within 2-week tolerance. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes_rail.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Both tickets show identical trailer number "KL-152" (right-edge ticket id matches). Same scale (3122), location (Pilot Travel Center, Bunkie LA), date (4-03-26), weighmaster signature ("Mache Castille"), and weigh number (3822). Tractor handwriting on both tickets matches by inspection. Same vehicle weighed at both events. [log:scale_tickets.full_ticket.trailer_number, scale_tickets.empty_ticket.trailer_number, scale_tickets.tractor_match]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     '2-191 is consumed_lot offload_2 (NOT the last offload of railcar TILX200231 — sister batches 2-190 (offload_1) and 2-192 (offload_3) already in COBB; cumulative through offload_3 implies at least one more offload to come). Rail last-offload conservatism policy DOES NOT apply here. Cargo (kg) is raw scale-ticket math: (76,780 - 29,580) lb × 0.453592 = 47,200 lb × 0.453592 = 21,409.5424 kg. Ops Notes offload_2 row Cargo Mass (kg) = 21,409.5424 — exact match. [log:scale_tickets.net_lb, scale_tickets.net_kg_at_0_453592, ops_notes_rail.constants.lbs_to_kg, ops_notes_rail.offload_table.1.cargo_kg, rail_balance_check, sister_batch_consistency.cobb_sister_window_TILX200231]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Per-offload rail batch (non-last): scale-ticket math is authoritative for THIS batch; BOL aggregate (77.27 MT) is at railcar level, not per-offload. The 21,409.5424 kg from scale tickets is 2-191''s injectate basis. Sparging deduction (Section 2.6) applied to that base. [log:scale_tickets.net_kg_at_0_453592, ops_notes_rail.offload_table.1.cargo_kg]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied: 21,409.5424 × 0.0129 = 276.183 kg sparging loss. Mass of Bio-Oil Injected = 21,409.5424 - 276.183 = 21,133.3593 kg. Ops Notes offload_2 row shows exactly these values (Sparging Loss 276.183097 kg, Mass of Bio-Oil Injected 21,133.3593 kg); arithmetic correct. [log:ops_notes_rail.constants.sparging_mass_loss, ops_notes_rail.offload_table.1.cargo_kg, ops_notes_rail.offload_table.1.sparging_loss_kg, ops_notes_rail.offload_table.1.mobi_kg, independent_calculations_check.sparging_check, independent_calculations_check.mobi_check]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Scale ticket net = 21,409.5424 kg = Ops Notes Cargo (kg) = COBB row 68 offloaded_quantity_kg = Certify "Allocated Bio-Oil Mass - AECN via Rail" 21.410 t. Post-sparging Mass of Injectant = 21,133.3593 kg (Ops Notes) shown in Certify Datapoints as 21.133 t. All four sources align. [log:scale_tickets.net_kg_at_0_453592, ops_notes_rail.offload_table.1.cargo_kg, ops_notes_rail.offload_table.1.mobi_kg, cobb_tracker.values.F_offloaded_quantity_kg, certify_datapoints_tab_total]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Certify Sources tab (per Document Location Rule — not in per-batch Drive folder, but Sources tab is sufficient): "Correction Costum Documents 2328-R.pdf", "Documents camion 2339-R.pdf", "Documents Camion 2340-R corr (1).pdf". All three linked to the "Allocated Bio-Oil Mass - AECN via Rail" datapoint. [log:certify_sources_tab_total, certify_sources, ops_notes_rail.bols_loaded]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2328-R, 2339-R, 2340-R) listed in COBB row 68 BOL_number field for batch 2-191 and in Ops Notes BOLs Loaded section (25.7 + 25.63 + 25.94 MT). Naming convention "-R" suffix = rail-load trucks. Per shared rail-batch convention (verified on sister batches 2-185, 2-186, 2-187, 2-189, 2-190): each BOL represents one truck delivery from AECN (BioEnergie AE Cote-Nord, Port-Cartier QC) to SOPOR (Société du port ferroviaire de Baie-Comeau railyard). [log:cobb_tracker.values.E_BOL_number, ops_notes_rail.bols_loaded]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL masses (25.7 + 25.63 + 25.94 MT) aggregates to Ops Notes Total Loaded Mass = 77,270 kg = COBB row 68 origin_quantity_kg = 77,270.0. This batch''s offload mass = 21,409.5424 kg, well below the railcar inbound. Rail-batch BOL mass check applied at railcar level. [log:ops_notes_rail.bol_aggregate_MT, ops_notes_rail.bol_aggregate_kg, ops_notes_rail.offload_table.1.cargo_kg, cobb_tracker.values.H_origin_quantity_kg]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN (BioEnergie AE Côte-Nord, Port-Cartier QC) -> SOPOR (Société du port ferroviaire de Baie-Comeau railyard, via 3 trucks each "-R" rail-load suffix) -> Opelousas LA (rail leg via railcar TILX200231) -> Basco 6 (truck, this batch consumed_lot offload_2). All 3 inbound truck BOLs documented in Certify Sources; rail leg documented via railcar inbound record + Watco distance email; offload truck leg documented via this batch''s scale tickets. [log:certify_sources, cobb_tracker.values.C_consumed_lot]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified per FC9 + memory project_rail_distance_allocation: (1) AECN->SOPOR truck full single-truck distance 173 km (= 107.5 mi) per Certify Datapoint "Distance from AECN to Sopor Quebec (truck)"; Allocated Distance AECN to Sopor 143.80162 km (= 322.5 mi-total-truck-caravan × 0.27708 batch share, expressed in km) = 89.36 truck-mi per batch; (2) SOPOR->Opelousas rail full 2,199 mi per "Distance from SOPOR to Opelousas (RAIL)"; Allocated 609.29 mi (= 2,199 × 0.27708); (3) Opelousas->Basco truck per-batch 42.9 mi (full = allocated since each offload uses dedicated truck, no allocation). All match Ops Notes pre-computed values for offload_2 (Rail 609.29, Truck Leg 1 89.36 mi). [log:ops_notes_rail.constants, ops_notes_rail.offload_table.1.rail_miles, ops_notes_rail.offload_table.1.truck_leg_1_miles, ops_notes_rail.this_batch_2-191_derived.allocation_check, ops_notes_rail.this_batch_2-191_derived.rail_mi_check, ops_notes_rail.this_batch_2-191_derived.truck_leg_1_mi_check]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components present in Certify: AECN to SOPOR Tanker Truck Process (0.263 t), SOPOR to Opelousas Rail Process (1.219 t), Opelousas to Basco - Tanker Truck Process (0.105 t), AECN to SOPOR Tanker Truck Embodied (0.021 t), SOPOR to Opelousas Rail Embodied (0.019 t), Opelousas to Basco Tanker Truck Embodied (0.010 t). Modes consistent with AECN rail convention. [log:certify_components.components]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'All 3 BOL/billing PDFs serve as both BOL and billing for the inbound truck legs (AECN convention). Charm-A4-2024-10-24-63-1976.pdf (BCU certificate) also present in Sources tab. See Section 9.9 for BCU cert filename observation. [log:certify_sources]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder', 'Pass',
     '"2-190-2-191 Tests.pdf" (2-page SGS Certificate, in Drive Testing) — 2-190 on page 1, 2-191 on page 2. SGS Order No 5437581. Page 2 = batch 2-191 (Cert SR26-02484.002 Reissue 1, "Data Updated"). [log:lab_results.filename, lab_results.certificate_number_2-191, lab_results.client_id_on_page]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-191 = 36.9% (m/m) (ASTM D5291 Method C). Within AECN expected range (mean 39.42%, ±2 SD ~27.2%-51.6%). [log:lab_results.carbon_pct, lab_results.carbon_within_aecn_range]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 6.8%, Nitrogen 2.00%, Kinematic Viscosity 16.59 cSt @ 40°C, Acid Number 53 mg KOH/g, Density 1.201 g/cm³ @ 15°C. All within typical AECN ranges. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct, lab_results.viscosity_cSt_at_40C, lab_results.acid_number_mg_KOH_per_g, lab_results.density_g_per_cm3_at_15C]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02484.002 Reissue 1 explicitly labeled "BATCH 2-191" on page 2. Sampled 2026-04-06 13:10 at BASCO LOUISIANA (3 days after offload_2 truck arrived 2026-04-03, 5 days before injection completion 2026-04-11). COBB row 68 column S = 2026-04-06 confirms sample date. [log:lab_results.certificate_number_2-191, lab_results.client_id_on_page, lab_results.sampled, lab_results.location, cobb_tracker.values.S_sample_date]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate is recorded in Ops Notes Section 5.5. [log:oil_type]',
     'N/A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-191, Completion Date = 4/11/2026. Matches Certify removal date (11 Apr 2026) and COBB row 68 injection_completion_date (2026-04-11). [log:ops_notes_rail.batch_number, ops_notes_rail.completion_date, cobb_tracker.values.L_injection_completion_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 76,780 lb = Ops Notes offload_2 Loaded Mass (lbs) 76,780 (exact). Empty ticket gross 29,580 lb = Ops Notes offload_2 Unloaded Mass (lbs) 29,580 (exact). Both values verified by direct image Read of JPGs. Cargo (kg) using Ops Notes factor 0.453592: 47,200 × 0.453592 = 21,409.5424 = Ops Notes offload_2 Cargo Mass (kg) 21,409.5424 (exact). [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.net_lb, scale_tickets.net_kg_at_0_453592, ops_notes_rail.offload_table.1.loaded_lb, ops_notes_rail.offload_table.1.unloaded_lb, ops_notes_rail.offload_table.1.cargo_kg]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Pass',
     'COBB row 68 for "2-191" verified: cell A68 = "2-191" ✓, consumed_lot C68 = "Rail_TILX200231_3.23.2026_offload_2" ✓ (matches Ops Notes), BOL_number E68 = "2328-R, 2339-R, 2340-R" ✓ matches Ops Notes BOLs Loaded, offloaded_quantity_kg F68 = 21,409.5424 = Ops Notes offload_2 Cargo (kg) ✓, origin_quantity_kg H68 = 77,270 = Ops Notes Total Loaded Mass × 1000 ✓ (NEW railcar TILX200231 — no stale-COBB carryover from prior railcar TIMX201060), injection_completion_date L68 = 2026-04-11 = Ops Notes 4/11/2026 ✓, pH M68 = 3.0 = Ops Notes 3 ✓, sample date S68 = 2026-04-06 = CHN sampled date ✓. All cross-source values match. [log:cobb_tracker.cobb_row_id_verified, cobb_tracker.cobb_cell_A_value, cobb_tracker.values, cobb_tracker.cross_check]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_2 row pH = 3 (whole-number entry). COBB row 68 pH (M68) = 3.0. Both sources match. Lab CoA does not measure pH (in-house Charm injection-time measurement). Sister rows 67 (2-190) and 69 (2-192) on same railcar TILX200231 also show pH = 3.0, consistent within-railcar pattern. [log:ops_notes_rail.offload_table.1.ph, cobb_tracker.values.M_pH]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'All three sources align: Ops Notes Completion Date 4/11/2026, COBB row 68 injection_completion_date 2026-04-11, Certify removal date 11 Apr 2026. [log:ops_notes_rail.completion_date, cobb_tracker.values.L_injection_completion_date, certify_components.removal_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include a density entry — expected behavior. (Lab CoA reports density 1.201 g/cm³ but this is for analytical reference only, not used by Ops Notes mass conversion.) [log:oil_type, lab_results.density_g_per_cm3_at_15C]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) datapoint. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 — H2 2025 EFs carry through Q1/Q2 2026 reporting; same LCA used by sister batch 2-190). [log:certify_sources]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" (Datapoints view shows 0.10 rounded). KB current native value 0.10402 tCO2e/t (H2 2025) — matches within rounding. Independent calc: 21.41 t × 0.10402 = 2.227 t ✓ matches Certify "AECN pyrolysis (from rail loads) - process emissions" 2.227 t exactly. [log:certify_component_modals_uncertainty.AECN pyrolysis (from rail loads) - process emissions]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)" (Datapoints view shows 0.02 rounded). KB current value 0.0212 tCO2e/t — modal 0.02116 matches at higher precision. Independent calc: 21.41 × 0.02116 = 0.453 t ✓ matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" 0.453 t exactly. [log:certify_component_modals_uncertainty.AECN pyrolysis (from rail loads) - embodied emissions]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals confirm mass basis = "Allocated Bio-Oil Mass - AECN via Rail" = 21,409.54 kg = pre-sparging Cargo (kg). Sparging is applied only to Mass of Injectant for sequestration (Section 2.6). Methodology correct per Section 6.6 / FC11 framing. [log:certify_component_modals_uncertainty.AECN pyrolysis (from rail loads) - process emissions, certify_component_modals_uncertainty.AECN pyrolysis (from rail loads) - embodied emissions]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc with full precision: 21,133.35940 kg (Mass of Bio-Oil Injected, post-sparging) × 0.369 (Carbon Content from CHN) × 3.667 = 28,595.78 kg = 28.596 tCO2e. Certify Sequestrations component shows 28.596 tCO2e — exact match. [log:ops_notes_rail.this_batch_2-191_derived.gross_co2e_full_precision_kg, ops_notes_rail.offload_table.1.mobi_kg, lab_results.carbon_pct, certify_components.totals.sequestrations_t]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted (3 transport process + 3 transport embodied + 2 pyrolysis): AECN->SOPOR truck process 0.263, SOPOR->Opelousas rail process 1.219, Opelousas->Basco truck process 0.105, AECN->SOPOR truck embodied 0.021, SOPOR->Opelousas rail embodied 0.019, Opelousas->Basco truck embodied 0.010, AECN pyrolysis process 2.227, AECN pyrolysis embodied 0.453. Sum = 4.317 tCO2e ✓ matches Certify Activities total exactly. Each component independently math-reconciles to native EFs and route geometry. [log:certify_components.components, certify_components.totals.removal_activities_t]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount = 151 kg (= 0.151 t, 0.528% of gross sequestrations). Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate from per-component ± inputs — Isometric''s aggregation is authoritative; QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.1476% carbon). Magnitude consistent with sister rail batches 2-186/2-187/2-189/2-190 (~0.5%). [log:certify_components.uncertainty_discount_kg, certify_components.uncertainty_discount_t, certify_components.uncertainty_discount_pct_of_gross]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Pass',
     'Net = 28.596 (sequestrations) + 1.587 (BCU adjustments) - 4.317 (activities) - 0.151 (uncertainty) = 25.715 tCO2e. Certify shows Net CO2e Removed = 25.714 t (displayed as 25.71). Reconciles within 0.001 t rounding. [log:certify_components.net_calc_check, certify_components.net_co2e_t_full_precision]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show ±72.57 kg in INPUTS section (verified by opening each component modal individually): Injection Sequestration (Mass of product 21,133.36 ±72.57), AECN->SOPOR Truck Process (Mass of load 21,409.54 ±72.57), SOPOR->Opelousas Rail Process (Mass of load 21,409.54 ±72.57), Opelousas->Basco Truck Process (Mass of load 21,409.54 ±72.57), AECN Pyrolysis Process (Mass 21,409.54 ±72.57), AECN Pyrolysis Embodied (Mass 21,409.54 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi) — confirmed by opening AECN->SOPOR Truck Embodied, SOPOR->Opelousas Rail Embodied, and Opelousas->Basco Truck Embodied modals (all show only distance × carbon_intensity, no mass term). Carbon Content uncertainty ±0.1476% (= 36.9 × 0.004, matches 0.4% relative). [log:certify_component_modals_uncertainty]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported ± matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so ±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process + pyrolysis components). Verified by opening each component modal and reading the INPUTS section directly (no aggregate-discount inference). Carbon content ±0.1476% = 36.9 × 0.004 confirms standard 0.4% relative uncertainty. Conservatism precondition (N_offloads ≥ N_inbound_BOLs = 3) for railcar TILX200231 will be formally validated at the railcar''s last batch QA (TBD — sisters 2-191/2-192 visible at offloads 2/3; remaining ~11,935 kg implies at least one more offload). [log:certify_component_modals_uncertainty, uncertainty_three_layer_check.layer_2_correctness, uncertainty_three_layer_check.FC9_per_removal_framing]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount = 151 kg in Calculation View. Net formula: Sequestrations - Activities + Adjustments - Uncertainty = 25.714 t Net (Certify display 25.71). Magnitude reasonable given mass and carbon uncertainty inputs. [log:certify_components.uncertainty_discount_kg, certify_components.uncertainty_discount_t, certify_components.net_co2e_t_full_precision, uncertainty_three_layer_check.layer_3_discount_presence]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon (36.9%, within ±2 SD), distances (107.5/2199/42.9 mi full-leg + 89.36/609.29 mi allocated), EFs (0.1143 truck process / 0.0259 rail process / 0.23756 truck embodied / 0.03113 rail embodied — 2026 corrected value, no stale-EF carryover from 2-182). Mass 21,409.54 kg pre-sparging / 21,133.36 kg post-sparging within expected per-truck offload range. Both scale tickets internally consistent (gross = axle sum). All math reconciles to Certify within rounding. BCU 1.587 t = exact sum of process transport (0.263 + 1.219 + 0.105 = 1.587) — clean BCU calculation, no over- or under-application (unlike sister 2-188). [log:lab_results.carbon_pct, certify_components.components, certify_component_modals_uncertainty.SOPOR to Opelousas Rail Transport Embodied Emissions, certify_component_modals_uncertainty.BCUs - Applied to Bio-Oil Transport Process Emissions]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. Ops Notes "Oil Left in Railcar (MT/kg)" cells correctly blank for 2-191 — railcar TILX200231 still has ~34.37 MT remaining as of 2-191''s Ops Notes snapshot (cumulative through offload_2 = 42.90 MT of 77.27 MT loaded). Last-offload mass reconciliation belongs to whichever batch is the railcar''s physical last pull (TBD; sisters 2-192 already exists at offload_3 in COBB row 69, so at minimum offload_4 is to come). [log:ops_notes_rail.oil_left_in_railcar_MT, ops_notes_rail.total_unloaded_mass_MT, ops_notes_rail.bol_aggregate_MT, rail_balance_check]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch precondition for FC9 framing)', 'Pass',
     'Railcar TILX200231 is mid-drawdown at this batch (2 of N+ offloads). Sister-batch state per COBB rows 67-69 (all consumed_lot Rail_TILX200231_3.23.2026_offload_*): R67 2-190 = offload_1 (Cargo 21,491.18896 kg, completed 2026-04-10), R68 2-191 = offload_2 (THIS BATCH, Cargo 21,409.5424 kg, completed 2026-04-11), R69 2-192 = offload_3 (Cargo 22,434.66032 kg, completed 2026-04-11). Cumulative through offload_3 implies oil left in railcar; at least one more offload to come. **Section 8.3 last-offload reconciliation DEFERRED to whichever batch is the railcar''s physical last pull.** For 2-191 (offload_2 mid-drawdown), the FC9 per-offload uncertainty framing (±72.57 kg per leg) is conservative iff N_offloads ≥ N_inbound_BOLs at last batch — that precondition check (and the railcar mass balance check / FC11) will be formally validated then. 2-191 is independent of last-offload mechanics: this is a non-last raw-scale-ticket pull. [log:rail_balance_check, sister_batch_consistency.cobb_sister_window_TILX200231]',
     'KB Section 8 / FC9 / FC11'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component 28.596 tCO2e. Independent calc full precision: 21,133.35940 kg × 0.369 × 3.667 = 28,595.78 kg = 28.596 t. Exact match. Carbon content matches CHN page 2 (36.9%). [log:certify_components.totals.sequestrations_t, lab_results.carbon_pct, ops_notes_rail.this_batch_2-191_derived.gross_co2e_full_precision_kg]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Rail embodied EF = 0.03113 kgCO2e/mi (= 0.0000311307 MTCO2e/mi 2026 current value, NOT stale 0.0000352240 carried by sister batch 2-182 which was previously fixed). Rail process EF = 0.0259 kgCO2e/(t·mi). Truck process EF = 0.1143 kgCO2e/(t·mi). Truck embodied EF = 0.23756 kgCO2e/mi. Allocated distances correctly use the inbound BOL aggregate (77,270 kg) as denominator (allocation fraction 0.27708 = 21,409.5424 / 77,270). All 6 transport components math-reconcile independently to Certify values within rounding. [log:certify_components.components, certify_component_modals_uncertainty, ops_notes_rail.this_batch_2-191_derived.allocation_check]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (2.227 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.453 t) present. Rail-batch naming convention used (deliberate signal to VVB to expect scale tickets as authoritative mass source). [log:certify_components.components]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" (1.587 t) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify_components.totals.adjustments_BCU_t]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU 1.587 t = exact sum of 3 transport process activities (0.263 + 1.219 + 0.105 = 1.587). BCU >= activity (here exactly equal). Embodied transport emissions (0.021 + 0.019 + 0.010 t) are NOT BCU-eligible per protocol — confirmed not double-claimed. No over-application of BCU credit (unlike sister-batch 2-188 where BCU value diverged from sister pattern). [log:certify_components.totals.transport_process_sum_t, certify_components.bcu_vs_transport_process_check, certify_component_modals_uncertainty.BCUs - Applied to Bio-Oil Transport Process Emissions.vs_transport_process_sum]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify_components.totals.counterfactuals_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net = 25.714 t (displayed 25.71 t) = 28.596 - 4.317 + 1.587 - 0.151. Each input verified independently. [log:certify_components.net_co2e_t_full_precision, certify_components.net_calc_check]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     '4 non-descriptive filenames in Certify Sources (same shared rail-batch hygiene as sister batches 2-185, 2-186, 2-187, 2-189, 2-190): "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF source), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance), "image (44).png" (SOPOR-Opelousas rail Watco distance email). Hygiene issue — content correct but filenames non-descriptive. **Additionally:** the rail PROCESS EF datapoint is sourced from a PDF named "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to the rail Embodied EF datapoint (correctly). The EF value itself is correct per 2026 GLEC V3.2, but the filename references the Embodied tab specifically; if the PDF is an Embodied-tab-only export, the link to the process EF datapoint references the wrong tab/sheet. **Additionally (carryover from 2-190):** "AECN Process Emissions Calculation.xlsx" is linked to the "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint, possible mislink; same hygiene as 2-190 — worth Garrett verifying whether this xlsx contains both process AND embodied calcs (then link is fine but filename is incomplete) OR is process-only (link is wrong). **Additionally (BCU cert filename):** BCU certificate file is "Charm-A4-2024-10-24-63-1976.pdf" — same filename as sister 2-190 (same railcar TILX200231). 2-188 used same A4 filename and Max questioned the A4 vs sisters'' A3 pattern; for 2-190/2-191 this is a NEW railcar (TILX200231) and the BCU quantity 1.587 t exactly equals the process transport sum, so the QUANTITY is correct. Filename pattern (A4 vs A3) is a Garrett-side question of whether different railcars use different BCU certificates by design. Not verifier-impacting since quantity reconciles. **Slight improvement vs 2-190:** the truck embodied EF datapoint is now sourced from "Truck Embodied Emissions.png" (descriptive) rather than a Screenshot file — one fewer generic name in the rail-batch shared set. [log:certify_sources]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 source-datapoint links. All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (2328-R, 2339-R, 2340-R), AECN LCA CI spreadsheet (Bioenergy AE Cote-Nord 1Jul2025-31Dec2025), LCA with stack emissions (BH 2025), Supporting GHG data (31Dec2025), AECN Process Emissions Calculation, Standard EFs Railcar Embodied, Charm-A4 BCU certificate, scale tickets (Full + Empty as "(1)" copies), CHN PDF (2-190-2-191 Tests), Ops Notes Rail (xlsx export, twice — public + private), AECN to SOPOR (Baie Comeau) route map, Truck Embodied Emissions image, plus 4 generic-named screenshots/images flagged in 9.9. Per Document Location Rule, presence in Certify Sources is sufficient. [log:certify_sources_tab_total, certify_sources]',
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
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '25.71 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'NONE — Net CDR 25.71 tCO2e is correctly calculated. 2-191 is the SECOND offload of railcar TILX200231 (consumed_lot offload_2; sister to 2-190 = offload_1, 2-192 = offload_3); raw-scale-ticket-driven and reconciles cleanly across scale tickets, Ops Notes, COBB row 68 offloaded_quantity_kg, and Certify Allocated Bio-Oil Mass (all = 21,409.5424 kg). Independent gross-to-net calc reproduces Certify exactly: 21,133.35940 kg × 0.369 × 3.667 = 28,595.78 kg = 28.596 t Sequestrations; 4.317 t Activities; 1.587 t BCU offset (= exact process transport sum 0.263 + 1.219 + 0.105); 0.151 t uncertainty discount → Net 25.715 t (displayed 25.71). The railcar last-offload reconciliation belongs to whichever future batch is TILX200231\'s physical last pull (sisters 2-192 row 69 = offload_3 already in COBB; remaining ~11,935 kg implies at least one more offload). Section 7a per-offload uncertainty conservatism precondition check (N_offloads ≥ N_inbound_BOLs = 3) is DEFERRED to that last batch\'s QA per FC9.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '9.9 only (Garrett-side hygiene, NOT verifier-impacting): (a) 4 non-descriptive Certify filenames [image (44).png, Screenshot 2026-04-10 PM.png, Screenshot 2026-02-23 AM.png, Screenshot 2026-01-27 125934.png] propagating across rail batches (same set as 2-185/186/187/189/190); (b) rail PROCESS EF sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to rail Embodied EF, possible single-tab vs multi-tab PDF inconsistency; (c) "AECN Process Emissions Calculation.xlsx" linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint (carryover from 2-190); (d) BCU certificate filename "Charm-A4-2024-10-24-63-1976.pdf" — same as sister 2-190 (NEW railcar TILX200231); 2-188 (different railcar TIMX201060) used same A4 filename and Max questioned A4 vs sisters\' A3 pattern. BCU quantity 1.587 t exactly matches process transport sum so the QUANTITY is correct; only filename pattern in question. **Slight improvement vs 2-190:** truck embodied EF datapoint sourced from "Truck Embodied Emissions.png" (descriptive) rather than a Screenshot file — one fewer generic name in shared set.')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-191/Batch_2-191_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
