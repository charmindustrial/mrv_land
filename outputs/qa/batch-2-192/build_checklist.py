#!/usr/bin/env python3
"""Build Batch 2-192 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-192'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 11 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-04'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TILX200231 - sister to 2-190 and 2-191; consumed_lot offload_3. COBB sister window: R67 2-190 offload_1, R68 2-191 offload_2, R69 2-192 offload_3 (THIS). Cumulative offloads 1-3 = 65,335.39 kg of 77,270 kg loaded; ~11,934.61 kg remaining -> at least one more offload to come (offload_4 row in Ops Notes is blank). 2-192 is NOT the last offload of TILX200231; FC11 last-offload mass policy DOES NOT apply.)'),
    ('META', 'Net CDR (Certify)', '40.04 tCO2e'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "2-192" at id 1r215O7QY7Pk_FSw8tEMbuK7ClMc97kGs (parent reporting-period folder 4/6/26-4/12/26); contains "2-192 Ops Notes Rail" Google Sheet (id 1LitV1KLOKHA7pcfQtCpFEyWicNiy9Yn--NDd6Jp5sR8, owner Garrett Lutz), Testing subfolder (CHARM SR26-02553.pdf, batch-specific CHN report; multi-batch CoA covering 2-192/2-193/2-194 KS-RC/2-197/2-198 plus KC-0005..0008), Scale Tickets subfolder (Full + Empty JPGs). [log:batch_id, ops_notes.drive_file_id, lab_results.drive_file_id]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains "2-192 Full Scale Ticket.jpg" (~2.2 MB) and "2-192 Empty Scale Ticket.jpg" (~2.2 MB). One offload pair (consistent with offload_3 of railcar TILX200231 - each batch represents one truck-out delivery from the railcar). Both also uploaded to Certify Sources as "(1)" copies. Image pixels Read directly via image tool (NOT Drive OCR snippet, per memory feedback_ocr_not_primary_source). [log:scale_tickets.drive_full_id, scale_tickets.drive_empty_id]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive > Testing contains "CHARM SR26-02553.pdf" (9-page SGS Certificate). Page 1 covers batch 2-192 (Certificate SR26-02553.001, Client ID = "BATCH 2-192"). Pages 2-9 cover other batches (2-193, 2-194 KS-RC, 2-197, KC-0005, KC-0006, KC-0007, KC-0008, 2-198) sampled in same lab order. Sampled 10-Apr-2026 15:00 at BASCO LOUISIANA. [log:lab_results.filename_drive, lab_results.page_1_2-192.certificate_id, lab_results.page_1_2-192.client_id]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-192 Ops Notes Rail" Google Sheet present in Drive folder; owner Garrett Lutz; modified May 1. Header (Batch number 2-192, Completion Date 4/11/2026), Batch Composition (railcar TILX200231, sparging 0.0129, lbs-to-kg 0.453592, route distances 2199 mi rail / 107.5 mi single-truck AECN-SOPOR x 3 trucks / 42.9 mi Opelousas-Basco), BOLs Loaded (3 inbound BOLs: 2328-R 25.7 MT + 2339-R 25.63 MT + 2340-R 25.94 MT; aggregate = 77.27 MT total), and offload table row 3 populated for offload_3 (Loaded 78660 lb, Unloaded 29200 lb, Cargo 22,434.66032 kg, allocation 0.2903411456, Rail 638.4601792 mi, Truck Leg 1 93.63501945 mi). Rows 1 (offload_1, sister 2-190) and 2 (offload_2, sister 2-191) also visible. Row 4 (offload_4) blank — railcar still has ~11,935 kg remaining as of 2-192 Ops Notes snapshot. [log:ops_notes.filename, ops_notes.batch_id_in_sheet, ops_notes.completion_date, ops_notes.bols_loaded, ops_notes.bol_aggregate_mt, ops_notes.offload_table.2]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 1 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). Ops Notes references Opelousas->Basco truck leg 42.9 mi. No Vaulted references in any source. [log:lab_results.page_1_2-192.location]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both JPG images Read directly from pixels (per OCR-vs-image rule). Full ticket #1312226093828, dated 4-03-26 16:30, at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA scale 3122; axle sum 10,000 + 34,280 + 34,380 = 78,660 lb (= certified gross, exact). Empty ticket #1312226093830, dated 4-03-26 18:09 same location/scale; axle sum 9,440 + 11,560 + 8,200 = 29,200 lb (= certified gross, exact). Both internally consistent (gross = axle sum, no axle-vs-cert discrepancy). Same Weighmaster signature "Maara Castille" on both, same Weigh Number 3828, empty ticket explicitly references full via "TICKET # OF FULL WEIGH (IF REWEIGH): 1312226093828". [log:scale_tickets.full_ticket.ticket_number, scale_tickets.empty_ticket.ticket_number, scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Both tickets dated 4-03-26 (April 3, 2026). Injection completion date per Ops Notes = 4/11/2026. 8 days between truck-out and injection — within 2-week tolerance. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, scale_tickets.ticket_date_vs_injection_date_days, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Both tickets show identical tractor "CH2" and trailer "KL-188". Same scale (3122), location (Pilot Travel Center, Bunkie LA), date (4-03-26), weighmaster signature ("Maara Castille"), and weigh number (3828). Same vehicle weighed at both events. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.empty_ticket.tractor_number, scale_tickets.full_ticket.trailer_number, scale_tickets.empty_ticket.trailer_number, scale_tickets.tractor_match, scale_tickets.trailer_match]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     '2-192 is consumed_lot offload_3 (NOT the last offload of railcar TILX200231 — Ops Notes offload_4 row is blank, sum_allocations = 0.8455 < 1.0; ~11,935 kg remaining implies at least one more offload to come). Rail last-offload conservatism policy (FC11) DOES NOT apply here. Cargo (kg) is raw scale-ticket math: (78,660 - 29,200) lb x 0.453592 = 49,460 lb x 0.453592 = 22,434.66 kg. Ops Notes offload_3 row Cargo Mass (kg) = 22,434.66032 — exact match. [log:scale_tickets.net_lb, scale_tickets.net_kg_calc, ops_notes.offload_table.2, is_last_offload_of_railcar, _derived_values.cumulative_allocation_offloads_1_3, _derived_values.remaining_oil_in_railcar_kg]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Per-offload rail batch (non-last): scale-ticket math is authoritative for THIS batch; BOL aggregate (77.27 MT) is at railcar level, not per-offload. The 22,434.66032 kg from scale tickets is 2-192\'s injectate basis. Sparging deduction (Section 2.6) applied to that base. [log:scale_tickets.net_kg_calc, ops_notes.offload_table.2]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied: 22,434.66032 x 0.0129 = 289.4071 kg sparging loss. Mass of Bio-Oil Injected = 22,434.66032 - 289.4071 = 22,145.2532 kg. Ops Notes offload_3 row shows exactly these values (Sparging Loss 289.4071181 kg, Mass of Bio-Oil Injected 22,145.2532 kg); arithmetic correct. [log:ops_notes.batch_composition, ops_notes.offload_table.2]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Scale ticket net = 22,434.66 kg = Ops Notes Cargo (kg) 22,434.66032 = COBB row 69 offloaded_quantity_kg 22,434.66032 = Certify "Allocated Bio-Oil Mass - AECN via Rail" 22.435 t. Post-sparging Mass of Injectant = 22,145.2532 kg (Ops Notes) shown in Certify Datapoints as 22.145 t. All four sources align. [log:scale_tickets.net_kg_calc, ops_notes.offload_table.2, cobb.G_offloaded_quantity_kg]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Drive AECN BOLs folder (id 1NqCHrdMrZGavRR6no8FXYmp1WAZP35Cg) AND in Certify Sources tab. Drive: "2328-R BOL.pdf", "2339-R BOL.pdf", "2340-R BOL.pdf". Certify Sources: "Correction Costum Documents 2328-R.pdf", "Documents camion 2339-R.pdf", "Documents Camion 2340-R corr (1).pdf". All three linked to the "Allocated Bio-Oil Mass - AECN via Rail" datapoint. [log:certify_sources_tab_total, bols.drive_folder_name, bols.list]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2328-R, 2339-R, 2340-R) listed in COBB row 69 BOL_number field for batch 2-192 and in Ops Notes BOLs Loaded section (25.7 + 25.63 + 25.94 MT). Naming convention "-R" suffix = rail-load trucks. Each BOL page 3 confirms DESTINATION = "PCT-USINE PORT CARTIER" (SOPOR railyard at Port-Cartier, Quebec). All 3 use Camion BIO-03 (same truck, 3 trips on 2026/03/13, 2026/03/17, 2026/03/18). [log:cobb.E_BOL_number, ops_notes.bols_loaded, bols.list, bols.all_three_bols_destination_pct_port_cartier]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL Masse Nette = 25,700 + 25,630 + 25,940 = 77,270 kg = Ops Notes BOL aggregate = COBB row 69 origin_quantity_kg 77,270.0. This batch\'s offload mass = 22,434.66032 kg, well below the railcar inbound. Rail-batch BOL mass check applied at railcar level (per Section 3.3 rail note). [log:bols.aggregate_kg, ops_notes.bol_aggregate_kg, cobb.H_origin_quantity_kg, ops_notes.offload_table.2, bols.matches_ops_notes_bol_aggregate, _derived_values.bol_2328_R_masse_nette_kg, _derived_values.bol_2339_R_masse_nette_kg, _derived_values.bol_2340_R_masse_nette_kg]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN (BioEnergie AE Côte-Nord) -> PCT/SOPOR (Port-Cartier railyard via Camion BIO-03, 3 trucks each "-R" rail-load suffix) -> Opelousas LA (rail leg via railcar TILX200231) -> Basco 6 (truck, this batch consumed_lot offload_3). All 3 inbound truck BOLs documented in Drive AECN BOLs + Certify Sources; rail leg distance documented via Watco email "image (44).png"; offload truck leg documented via this batch\'s scale tickets. [log:bols.list, cobb.C_consumed_lot, bols._destination_note]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified per FC9 + memory project_rail_distance_allocation. Note Certify stores AECN-side truck legs in km while Ops Notes records all distances in mi — explicit conversions below (1 mi = 1.609344 km). (1) AECN->SOPOR truck full single-truck distance: Ops Notes 107.5 mi x 1.609344 = 172.9 km, rounded to 173.00 km in Certify Datapoint "Distance from AECN to Sopor Quebec (truck)" — match. Allocated Distance AECN to Sopor: Ops Notes Truck Leg 1 (offload_3) = 93.63501945 mi x 1.609344 = 150.68705 km = Certify modal value 150.68705 km — exact match. Methodology: full 322.5 truck-mi-total (3 trucks x 107.5 mi each) x 0.2903 batch allocation = 93.635 mi per batch share = 150.687 km. (2) SOPOR->Opelousas rail (both sources in mi, no conversion): full 2,199 mi per Certify "Distance from SOPOR to Opelousas (RAIL)" = Ops Notes batch_composition. Allocated rail distance: Ops Notes Rail (offload_3) 638.4601792 mi = Certify modal precise 638.46017 mi = 2,199 x 0.2903 — exact match. (3) Opelousas->Basco truck per-batch (both sources in mi, no conversion): 42.9 mi (full = allocated since each offload uses dedicated truck, no allocation needed). [log:ops_notes.batch_composition, ops_notes.offload_table.2, certify_datapoints.5, certify_datapoints.7, certify_datapoints.10, certify_datapoints.12, certify_datapoints.14, _derived_values.allocated_truck_distance_mi_rounded, _derived_values.allocated_rail_distance_mi_rounded, _kb_constants.km_per_mi, _unit_conversions_3_5.full_truck_aecn_to_sopor_mi, _unit_conversions_3_5.full_truck_aecn_to_sopor_km_calc, _unit_conversions_3_5.full_truck_aecn_to_sopor_km_certify, _unit_conversions_3_5.allocated_truck_aecn_to_sopor_mi, _unit_conversions_3_5.allocated_truck_aecn_to_sopor_km_calc, _unit_conversions_3_5.allocated_truck_aecn_to_sopor_km_certify]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components present in Certify: AECN to SOPOR Tanker Truck Process (0.276 t), SOPOR to Opelousas Rail Process (1.278 t), Opelousas to Basco Tanker Truck Process (0.110 t), AECN to SOPOR Tanker Truck Embodied (0.022 t), SOPOR to Opelousas Rail Embodied (0.020 t), Opelousas to Basco Tanker Truck Embodied (0.010 t). Modes consistent with AECN rail convention. [log:certify_components.list]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'All 3 BOL/billing PDFs serve as both BOL and billing for the inbound truck legs (AECN convention; PC0037989/PC0038015/PC0038040 weighing receipts at Port-Cartier). Charm-A4-2024-10-24-63-1976.pdf (BCU certificate) also present in Sources tab. See Section 9.9 for filename hygiene observations. [log:bols.list, certify_sources.13]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder', 'Pass',
     '"CHARM SR26-02553.pdf" (9-page SGS Certificate, in Drive Testing). Page 1 = batch 2-192 (Cert SR26-02553.001, "BATCH 2-192", BASCO LOUISIANA, sampled 10-Apr-2026 15:00). Lab: SGS North America Inc., Authorised Signatory Tiffany Scott. [log:lab_results.filename_drive, lab_results.page_1_2-192.certificate_id, lab_results.page_1_2-192.client_id, lab_results.page_1_2-192.location]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Flag',
     'Carbon content for batch 2-192 = 53.1% (m/m) (ASTM D5291 Method C). AECN typical mean 39.42% (n=285), SD 6.09%; 2-SD upper = 51.6%. **53.1% is +2.247 SD above mean — outside the 2-SD threshold (above 51.6%).** Lab cert flags result with "#" (outside test method limits/analytical range). FLAG per Item 4.2 — value plausible (AECN feedstock can vary) but outside historical range; the elevated carbon drives this batch\'s higher Net CDR (40.04 t vs sister batches 2-190/2-191 ~26 t at ~39% C). The high carbon content has been correctly used in Certify Net calc; no FAIL — issue is outlier nature of the input, not a calculation error. Recommend Garrett confirm sample handling/result is correct and consider re-running ASTM if practical. [log:lab_results.page_1_2-192.carbon_pct, lab_results.page_1_2-192.carbon_pct_outside_method_limits, _kb_constants.aecn_carbon_mean_pct, _kb_constants.aecn_carbon_sd_pct, _kb_constants.aecn_sample_size_n, _kb_constants.aecn_carbon_2sd_upper_pct, _derived_values.carbon_pct_sd_above_mean]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 9.3%, Nitrogen <0.75%, Kinematic Viscosity 12.80 cSt @ 40°C, Acid Number 45 mg KOH/g, Density 1.204 g/cm³ @ 15°C. Hydrogen slightly elevated vs typical (~6-7%) but consistent with the elevated carbon — sample chemistry overall trends higher than mean. Nitrogen and viscosity within typical AECN ranges. [log:lab_results.page_1_2-192.hydrogen_pct, lab_results.page_1_2-192.nitrogen_pct, lab_results.page_1_2-192.kinematic_viscosity_40c_cst, lab_results.page_1_2-192.acid_number_mg_koh_per_g, lab_results.page_1_2-192.density_15c_g_per_cm3]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02553.001 explicitly labeled "BATCH 2-192" on page 1. Sampled 10-Apr-2026 15:00 at BASCO LOUISIANA (7 days after offload_3 truck arrived 2026-04-03, 1 day before injection completion 2026-04-11). Sample chain matches injection timing. [log:lab_results.page_1_2-192.certificate_id, lab_results.page_1_2-192.client_id, lab_results.page_1_2-192.sampled_datetime, lab_results.page_1_2-192.location]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate is recorded in Ops Notes Section 5.5. [log:oil_type]',
     'N/A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-192, Completion Date = 4/11/2026. Matches Certify removal date (11 Apr 2026). [log:ops_notes.batch_id_in_sheet, ops_notes.completion_date, certify_components.removal_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 78,660 lb = Ops Notes offload_3 Loaded Mass (lbs) 78,660 (exact). Empty ticket gross 29,200 lb = Ops Notes offload_3 Unloaded Mass (lbs) 29,200 (exact). Both values verified by direct image Read of JPGs. Cargo (kg) using Ops Notes factor 0.453592: 49,460 x 0.453592 = 22,434.66 = Ops Notes offload_3 Cargo Mass (kg) 22,434.66032 (exact). [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.net_lb, scale_tickets.net_kg_calc, ops_notes.offload_table.2]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Pass',
     'COBB row 69 for "2-192" verified: cell A69 = "2-192" (ROW VERIFICATION GATE PASSED), consumed_lot C69 = "Rail_TILX200231_3.23.2026_offload_3" (matches Ops Notes), BOL_number E69 = "2328-R, 2339-R, 2340-R" matches Ops Notes BOLs Loaded, offloaded_quantity_kg G69 = 22,434.66032 = Ops Notes offload_3 Cargo (kg), origin_quantity_kg H69 = 77,270 = Ops Notes Total Loaded Mass x 1000 (NEW railcar TILX200231 — no stale-COBB carryover from prior railcar TIMX201060 which had stale 71,010). All cross-source values match. order_line_completed_on I69 = 2026-04-03 16:20:21 = Manufacturo order processing date (NOT injection date) — same value across rows 67/68/69 for railcar TILX200231; per-batch injection date is in Ops Notes / Certify. [log:cobb.A_injection_batch, cobb.row_number, cobb_row_id_verified, cobb_cell_A_value, cobb.C_consumed_lot, cobb.E_BOL_number, cobb.G_offloaded_quantity_kg, cobb.H_origin_quantity_kg, cobb._no_staleness_flag]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_3 row pH = 3 (whole-number entry). Sister rows 67 (2-190) and 68 (2-191) on same railcar TILX200231 also show pH = 3, consistent within-railcar pattern. [log:ops_notes.offload_table.2]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date 4/11/2026 = Certify removal date 11 Apr 2026. COBB row 69 column I (order_line_completed_on) shows 2026-04-03 — but this is Manufacturo order processing date, NOT injection date (consistent value across rows 67/68/69 for railcar TILX200231; per prior batches\' QA pattern, this is not a discrepancy). Verifier reads Ops Notes / Certify, both align. [log:ops_notes.completion_date, certify_components.removal_date, cobb.I_order_line_completed_on, cobb._date_note]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include a density entry — expected behavior. (Lab CoA reports density 1.204 g/cm³ but this is for analytical reference only, not used by Ops Notes mass conversion.) [log:oil_type, lab_results.page_1_2-192.density_15c_g_per_cm3]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources (#15), linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) datapoint. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 — H2 2025 EFs carry through Q1/Q2 2026 reporting; same LCA used by sister batches 2-190 and 2-191). [log:certify_sources.14]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources (#17), linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources.16]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources (#18), linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail). [log:certify_sources.17]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" (Datapoints view shows 0.10 rounded). KB current native value 0.10402 tCO2e/t (H2 2025) — matches within rounding. Independent calc: 22.43466 t x 0.104 = 2.333 t — matches Certify "AECN pyrolysis (from rail loads) - process emissions" 2.333 t exactly. [log:certify_uncertainty_modals]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)" (Datapoints view shows 0.02 rounded). KB current value 0.0212 tCO2e/t — modal 0.02116 matches at higher precision. Independent calc: 22.43466 x 0.02116 = 0.4747 t = 0.475 t — matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" 0.475 t exactly. [log:certify_uncertainty_modals]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals confirm mass basis = "Allocated Bio-Oil Mass - AECN via Rail" = 22,434.66 kg = pre-sparging Cargo (kg). Sparging is applied only to Mass of Injectant for sequestration (Section 2.6). Methodology correct per Section 6.6. [log:certify_uncertainty_modals]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc with full precision: 22,145.2532 kg (Mass of Bio-Oil Injected, post-sparging) x 0.531 (Carbon Content from CHN) x 3.667 = 43,120.73 kg = 43.121 tCO2e. Certify Sequestrations component shows 43.121 tCO2e — exact match. [log:ops_notes.offload_table.2, lab_results.page_1_2-192.carbon_pct, certify_components.totals, _derived_values.gross_co2e_recalc_kg, _derived_values.gross_co2e_recalc_t]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted (3 transport process + 3 transport embodied + 2 pyrolysis): AECN->SOPOR truck process 0.276, SOPOR->Opelousas rail process 1.278, Opelousas->Basco truck process 0.110, AECN->SOPOR truck embodied 0.022, SOPOR->Opelousas rail embodied 0.020, Opelousas->Basco truck embodied 0.010, AECN pyrolysis process 2.333, AECN pyrolysis embodied 0.475. Sum = 4.524 tCO2e — matches Certify Activities total exactly. Each component independently math-reconciles to native EFs and route geometry. [log:certify_components.list, certify_components.totals]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount = 223 kg (= 0.223 t, 0.517% of gross sequestrations). Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate from per-component ± inputs — Isometric\'s aggregation is authoritative; QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.2124% carbon = 0.4% relative). Magnitude consistent with sister rail batches 2-190/2-191 (~0.5%). [log:certify_components.totals, certify_calc_view.uncertainty_discount_kg, _derived_values.uncertainty_discount_t, _derived_values.uncertainty_discount_pct_of_gross, _derived_values.carbon_uncertainty_relative_pct, _kb_constants.discrete_weight_uncertainty_kg]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Pass',
     'Net = 43.121 (sequestrations) + 1.664 (BCU adjustments) - 4.524 (activities) - 0.223 (uncertainty) = 40.038 tCO2e. Certify shows Net CO2e Removed = 40.038 t (displayed as 40.04). Reconciles exactly. [log:certify_components.net_co2e_t_displayed, certify_components.net_co2e_t_precise, certify_calc_view.net_co2e_removed_t, _derived_values.gross_co2e_recalc_t, _derived_values.transport_process_sum_t, _derived_values.activities_total_t, _derived_values.uncertainty_discount_t, _derived_values.net_calc_t]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show ±72.57 kg in INPUTS section (verified by opening each component modal individually): Injection Sequestration (Mass of product 22,145.25 ±72.57), AECN->SOPOR Truck Process (Mass of load 22,434.66 ±72.57), SOPOR->Opelousas Rail Process (Mass of load 22,434.66 ±72.57), Opelousas->Basco Truck Process (Mass of load 22,434.66 ±72.57), AECN Pyrolysis Process (Mass 22,434.66 ±72.57), AECN Pyrolysis Embodied (Mass 22,434.66 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi) — confirmed by opening AECN->SOPOR Truck Embodied, SOPOR->Opelousas Rail Embodied, and Opelousas->Basco Truck Embodied modals (all show only distance x carbon_intensity, no mass term). Carbon Content uncertainty ±0.2124% (= 53.1 x 0.004, matches 0.4% relative). [log:certify_uncertainty_modals]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported ± matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so ±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process + pyrolysis components). Verified by opening each component modal and reading the INPUTS section directly (no aggregate-discount inference). Carbon content ±0.2124% = 53.1 x 0.004 confirms standard 0.4% relative uncertainty. Conservatism precondition (N_offloads >= N_inbound_BOLs = 3) for railcar TILX200231 will be formally validated at the railcar\'s last batch QA (TBD — sisters 2-190/2-191/2-192 visible at offloads 1/2/3 in COBB; remaining ~11,935 kg implies at least one more offload). [log:certify_uncertainty_modals]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount = 223 kg in Calculation View. Net formula: Sequestrations - Activities + Adjustments - Uncertainty = 40.038 t Net (Certify display 40.04). Magnitude reasonable given mass and carbon uncertainty inputs. [log:certify_components.totals, certify_calc_view.net_co2e_removed_t, certify_calc_view.uncertainty_discount_kg]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon = 53.1% IS an outlier (above 2-SD threshold; surfaced as Section 4.2 FLAG). Distances (107.5/2199/42.9 mi full-leg + 93.63/638.46 mi allocated), EFs (0.1143 truck process / 0.0259 rail process / 0.23756 truck embodied / 0.03113 rail embodied — 2026 corrected value, no stale-EF carryover from 2-182). Mass 22,434.66 kg pre-sparging / 22,145.25 kg post-sparging within expected per-truck offload range. Both scale tickets internally consistent (gross = axle sum). All math reconciles to Certify within rounding. BCU 1.664 t = exact sum of process transport (0.276 + 1.278 + 0.110 = 1.664) — clean BCU calculation, no over- or under-application (unlike sister 2-188). The carbon outlier is the sole input anomaly; the elevated carbon drives this batch\'s 40.04 t Net (vs sister batches 2-190 at 26.28 t and 2-191 at 25.71 t at ~39% C). [log:lab_results.page_1_2-192.carbon_pct, certify_components.list, certify_uncertainty_modals]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. Ops Notes "Oil Left in Railcar (MT/kg)" cells correctly blank for 2-192 — railcar TILX200231 still has ~11,934.61 kg (11.93 MT) remaining as of 2-192\'s Ops Notes snapshot (cumulative through offload_3 = 65.34 MT of 77.27 MT loaded; offload_4 row blank). Last-offload mass reconciliation belongs to whichever batch is the railcar\'s physical last pull (TBD; 2-192 is offload_3, so at minimum offload_4 is to come). [log:ops_notes.total_unloaded_mass_kg_rows_1_3, ops_notes.bol_aggregate_kg, is_last_offload_of_railcar, _derived_values.cumulative_unloaded_mt_offloads_1_3, _derived_values.remaining_oil_in_railcar_kg, _derived_values.remaining_oil_in_railcar_mt]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch precondition for FC9 framing)', 'Pass',
     'Railcar TILX200231 is mid-drawdown at this batch (3 of N+ offloads). Sister-batch state per COBB rows 67-69 (all consumed_lot Rail_TILX200231_3.23.2026_offload_*): R67 2-190 = offload_1 (Cargo 21,491.18896 kg), R68 2-191 = offload_2 (Cargo 21,409.5424 kg), R69 2-192 = offload_3 (THIS BATCH, Cargo 22,434.66032 kg). Cumulative through offload_3 = 65,335.39168 kg of 77,270 kg loaded; ~11,935 kg remaining → at least one more offload to come (offload_4 row blank in Ops Notes). **Section 8.3 last-offload reconciliation DEFERRED to whichever batch is the railcar\'s physical last pull.** For 2-192 (offload_3 mid-drawdown), the FC9 per-offload uncertainty framing (±72.57 kg per leg) is conservative iff N_offloads >= N_inbound_BOLs at last batch — that precondition check (and the railcar mass balance check / FC11) will be formally validated then. 2-192 is independent of last-offload mechanics: this is a non-last raw-scale-ticket pull. [log:_last_offload_status_evidence, ops_notes.total_unloaded_mass_kg_rows_1_3, ops_notes.bol_aggregate_kg]',
     'KB Section 8 / FC9 / FC11'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component 43.121 tCO2e. Independent calc full precision: 22,145.2532 kg x 0.531 x 3.667 = 43,120.73 kg = 43.121 t. Exact match. Carbon content matches CHN page 1 (53.1%). [log:certify_components.totals, lab_results.page_1_2-192.carbon_pct, ops_notes.offload_table.2, _derived_values.gross_co2e_recalc_kg, _derived_values.gross_co2e_recalc_t]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Rail embodied EF = 0.03113 kgCO2e/mi (= 0.0000311307 MTCO2e/mi 2026 current value, NOT stale 0.0000352240 carried by sister batch 2-182 which was previously fixed; refresh propagates cleanly to 2-192). Rail process EF = 0.0259 kgCO2e/(t·mi). Truck process EF = 0.1143 kgCO2e/(t·mi). Truck embodied EF = 0.23756 kgCO2e/mi. Allocated distances correctly use the inbound BOL aggregate (77,270 kg) as denominator (allocation fraction 0.2903 = 22,434.66 / 77,270). All 6 transport components math-reconcile independently to Certify values within rounding. [log:certify_components.list, certify_uncertainty_modals]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (2.333 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.475 t) present. Rail-batch naming convention used (deliberate signal to VVB to expect scale tickets as authoritative mass source). [log:certify_components.list]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" (1.664 t) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify_components.totals]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU 1.664 t = exact sum of 3 transport process activities (0.276 + 1.278 + 0.110 = 1.664). BCU >= activity (here exactly equal). Embodied transport emissions (0.022 + 0.020 + 0.010 t) are NOT BCU-eligible per protocol — confirmed not double-claimed. No over-application of BCU credit (unlike sister-batch 2-188 where BCU value diverged from sister pattern). [log:certify_components.transport_process_sum_t, certify_components._bcu_check]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify_components.totals]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net = 40.038 t (displayed 40.04 t) = 43.121 - 4.524 + 1.664 - 0.223. Each input verified independently. [log:certify_components.net_co2e_t_displayed, certify_components.net_co2e_t_precise, certify_calc_view.net_co2e_removed_t, _derived_values.gross_co2e_recalc_t, _derived_values.activities_total_t, _derived_values.uncertainty_discount_t, _derived_values.net_calc_t]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     'Same shared rail-batch hygiene set as sister batches 2-185/2-186/2-187/2-189/2-190/2-191 (Garrett-side filename hygiene, NOT verifier-impacting): (a) 4 non-descriptive Certify filenames carrying across rail batches: "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF source #13), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support #16), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance #19), "image (44).png" (SOPOR-Opelousas rail Watco distance email #20); (b) rail PROCESS EF datapoint sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" (#4) — same filename also linked to rail Embodied EF #12 (correctly), so file is multi-tab; PROCESS link references the Embodied tab specifically — possible single-tab vs multi-tab PDF inconsistency, EF VALUE is correct; (c) "AECN Process Emissions Calculation.xlsx" (#23) linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint, possible mislink (carryover from 2-190/2-191); (d) "Correction Costum Documents 2328-R.pdf" (#11) — filename has typo "Costum" should be "Custom" (Customs Documents); (e) BCU certificate filename "Charm-A4-2024-10-24-63-1976.pdf" (#14) — same as sister 2-190/2-191 (NEW railcar TILX200231); 2-188 (different railcar TIMX201060) used same A4 filename and Max questioned A4 vs sisters\' A3 pattern. BCU quantity 1.664 t exactly matches process transport sum so the QUANTITY is correct; only filename pattern in question. Same slight improvement vs 2-188/2-189: truck embodied EF datapoint sourced from "Truck Embodied Emissions.png" (descriptive, #22) rather than a Screenshot file. [log:certify_sources, certify_sources_tab_total]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 source-datapoint links. All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (#9 Documents Camion 2340-R corr, #10 Documents camion 2339-R, #11 Correction Costum Documents 2328-R), AECN LCA CI spreadsheet (#15 Bioenergy AE Cote-Nord 1Jul2025-31Dec2025), LCA with stack emissions (#17 BH 2025), Supporting GHG data (#18 31Dec2025), AECN Process Emissions Calculation (#23), Standard EFs Railcar Embodied (#4 + #12), Charm-A4 BCU certificate (#14), scale tickets (#7 Full + #8 Empty as "(1)" copies), CHN PDF (#5 2-192-2-198+Kc0005-Kc-0008.pdf, multi-batch order), Ops Notes Rail (#1, #2, #3, #6 — 4 references), AECN to SOPOR (Baie Comeau) route map (#21), Truck Embodied Emissions image (#22), plus 4 generic-named screenshots/images flagged in 9.9 (#13, #16, #19, #20). Per Document Location Rule, presence in Certify Sources is sufficient. [log:certify_sources_tab_total, certify_sources]',
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
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '40.04 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'NONE — Net CDR 40.04 tCO2e is correctly calculated. 2-192 is the THIRD offload of railcar TILX200231 (consumed_lot offload_3; sister to 2-190 = offload_1 and 2-191 = offload_2); raw-scale-ticket-driven and reconciles cleanly across scale tickets, Ops Notes, COBB row 69 offloaded_quantity_kg, and Certify Allocated Bio-Oil Mass (all = 22,434.66032 kg). Independent gross-to-net calc reproduces Certify within rounding: 22,145.2532 kg x 0.531 x 3.667 = 43,123.97 kg = 43.124 t Sequestrations (Certify 43.121); 4.524 t Activities; 1.664 t BCU offset (= exact process transport sum 0.276 + 1.278 + 0.110); 0.223 t uncertainty discount → Net 40.038 t (displayed 40.04). Carbon content 53.1% is an OUTLIER (above 2-SD upper bound 51.6%; lab cert flags with "#" outside method limits) — surfaced as Section 4.2 FLAG. Outlier carbon is the sole atypical input; it drives this batch\'s elevated Net (40.04 t vs sister batches 2-190 26.28 t and 2-191 25.71 t at ~39% C). The high-carbon value has been correctly used in the Certify calc; no FAIL. Recommend Garrett confirm sample handling/result and consider re-running ASTM D5291 if practical. The railcar last-offload reconciliation belongs to whichever future batch is TILX200231\'s physical last pull (sisters 2-190/2-191/2-192 = offloads 1/2/3 already in COBB; remaining ~11,935 kg implies at least one more offload). Section 7a per-offload uncertainty conservatism precondition check (N_offloads ≥ N_inbound_BOLs = 3) is DEFERRED to that last batch\'s QA per FC9.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '4.2 (Carbon outlier — input data observation, not calc error) and 9.9 (Garrett-side filename hygiene, NOT verifier-impacting): (a) 4 non-descriptive Certify filenames [image (44).png, Screenshot 2026-04-10 PM.png, Screenshot 2026-02-23 AM.png, Screenshot 2026-01-27 125934.png] propagating across rail batches (same set as 2-185/186/187/189/190/191); (b) rail PROCESS EF sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to rail Embodied EF, possible single-tab vs multi-tab PDF inconsistency; (c) "AECN Process Emissions Calculation.xlsx" linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint (carryover from 2-190/2-191); (d) "Correction Costum Documents 2328-R.pdf" — filename has typo "Costum" should be "Custom"; (e) BCU certificate filename "Charm-A4-2024-10-24-63-1976.pdf" — same as sisters 2-190/2-191 (NEW railcar TILX200231); 2-188 (different railcar TIMX201060) used same A4 filename and Max questioned A4 vs sisters\' A3 pattern. BCU quantity 1.664 t exactly matches process transport sum so the QUANTITY is correct; only filename pattern in question.')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-192/Batch_2-192_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
