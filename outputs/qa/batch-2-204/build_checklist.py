#!/usr/bin/env python3
"""Build Batch 2-204 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-204'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 29 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-06'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TILX200228 — first batch QA\'d from this railcar; consumed_lot Rail_TILX200228_4.2.2026_offload_4. **Cross-RP scope: 2-204 IS the railcar\'s physical last truck-out, but is NOT the railcar\'s last-reported batch in the April RP.** All 4 offloads occurred physically in April; offload_1 (sister batch) and offload_4 (2-204) were injected in April and report in this RP. The middle two (offload_2 = 2-202, offload_3 = 2-203) needed re-filtering for solids and weren\'t injected until May — they report in the May RP. So within the April RP, 2-204 is the 2nd-and-final RP-reportable offload from this railcar (with the offload_1 sister batch first). FC11 last-offload mass-reconciliation hook lands on whichever of 2-202 / 2-203 is reported LAST in the May RP — NOT on 2-204. The blank rows for offload_2/3 in 2-204\'s Ops Notes view + the "Oil Left in Railcar = 46.34 MT" figure reflect un-injected oil at the time of 2-204\'s QA — those numbers will reconcile in the May RP. For the April RP, 2-204\'s raw-scale-ticket Cargo (kg) of 5,805.98 is the correct mass basis with no FC11 policy adjustment, and Net CDR 6.86 t stands as-is.)'),
    ('META', 'Net CDR (Certify)', '6.86 tCO2e'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "13ddTpFdG1WwG42-P6SB5fjsnGBex3ot9" contains "2-204 Ops Notes Rail" Google Sheet (id 1SZW79dR_qbLUFSRSpXJrCwIKNVxeStSFeSgQO6xaN5c, owner Garrett Lutz), Scale Tickets subfolder (id 11rQdiDiY086CrqGcoDbxAt0rGEwoZ4Xd, with Full JPG + Empty PDF), Testing subfolder (id 113IAEvGGmV2WDiEC4AuOloxOukwx-sru, EMPTY in Drive — lab CHN cert "202-204, 5-10.pdf" is uploaded to Certify Sources only, per Document Location Rule). [log:batch_id, drive_folder_id, ops_notes.drive_id, scale_tickets.full_ticket.drive_id, scale_tickets.empty_ticket.drive_id]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains "2-204 Full Scale Ticket.jpg" (741 KB) and "2-204 Empty Ticket.pdf" (235 KB). One offload pair (consistent with offload_4 of railcar TILX200228 — each batch represents one truck-out delivery from the railcar). Both also uploaded to Certify Sources (entries #5 Full and #6 Empty, both Public visibility, linked to "Mass of Injectant (per injection)" datapoint). Image pixels Read directly: Full ticket via playwright screenshot of Drive image viewer; Empty ticket via curl signed-URL download then PDF Read. NOT Drive OCR snippet, per memory feedback_ocr_not_primary_source. [log:scale_tickets.full_ticket.primary_source_method, scale_tickets.empty_ticket.primary_source_method]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive Testing subfolder is empty; lab cert is in Certify Sources only as "202-204, 5-10.pdf" (#7 Public, linked to Carbon Content datapoint). Per Document Location Rule, presence in Certify Sources is sufficient. Multi-batch SGS Certificate of Analysis order SR26-02828 covering: page 1 = 2-202 (.001), page 2 = 2-203 (.002), page 3 = 2-204 (.003 — THIS BATCH), page 4 = 2-205 (.004), page 5 = 5-10 (.005, separate sample). Lab: SGS North America Inc., Authorised Signatory Rachel Oxley. [log:lab_results.filename_in_certify, lab_results.local_path, lab_results.covers_batches, lab_results.for_2-204.certificate_id, lab_results.for_2-204.client_id, lab_results.for_2-204.lab, lab_results.for_2-204.lab_supervisor]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-204 Ops Notes Rail" Google Sheet present in Drive folder (owner Garrett Lutz, modified 2026-05-06). Header (Batch number 2-204, Completion Date 4/29/2026), Batch Composition (Railcar TILX200228, sparging 0.0129, lbs-to-kg 0.453592, route distances 2199 mi rail / 107.5 mi single-truck AECN-SOPOR x 3 trucks / 42.9 mi Opelousas-Basco), BOLs Loaded (3 inbound BOLs: 2344-R 25.57 MT + 2345-R 25.48 MT + 2346-R 25.53 MT; aggregate = 76.58 MT total), and offload table row populated for offload_4 (Loaded 41,660 lb, Unloaded 28,860 lb, Cargo 5,805.9776 kg, allocation 0.07581584748, Rail 166.7190486 mi, Truck Leg 1 24.45061081 mi). Row offload_1 also populated (sister batch, 24,430.47 kg). Rows offload_2 and offload_3 blank — railcar still has 46,343.56 kg remaining as of 2-204 Ops Notes snapshot. [log:ops_notes.filename, ops_notes.batch_number, ops_notes.completion_date, ops_notes.bols_loaded_listed, ops_notes.total_loaded_mass_mt, ops_notes.offload_table_populated_rows, ops_notes.oil_left_in_railcar_mt]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 3 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). Ops Notes references Opelousas->Basco truck leg 42.9 mi. No Vaulted references in any source. [log:lab_results.for_2-204.location, certify_components.removal_date]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both images Read directly from pixels (per OCR-vs-image rule). Full ticket #1312226110103, dated 4-20-26 14:31, at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA scale 3122; axle sum 9,700 + 16,780 + 15,180 = 41,660 lb (= certified gross, exact). Empty ticket #1312226111129, dated 4-21-26 15:08 same location/scale; axle sum 0 + 20,840 + 8,020 = 28,860 lb (= certified gross, exact). Both internally consistent (gross = axle sum). Same Tractor # CH 2 / CH2 and Trailer # KL188 on both. Different weighmaster signatures (Marsha Castille on full / Paula Mayhall on empty) — same scale, different operator across days; not unusual. [log:scale_tickets.full_ticket.ticket_number, scale_tickets.empty_ticket.ticket_number, scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.full_ticket.axle_sum_check, scale_tickets.empty_ticket.axle_sum_check]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Full ticket dated 4-20-26 (April 20, 2026), empty 4-21-26 (April 21, 2026). Injection completion date per Ops Notes = 4/29/2026. 8-9 days between truck-out and injection — within 2-week tolerance. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Both tickets show identical tractor "CH 2" / "CH2" (full / empty — same vehicle, formatting variant only) and trailer "KL188". Same scale (3122), location (Pilot Travel Center, Bunkie LA). Same vehicle weighed at both events. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.empty_ticket.tractor_number, scale_tickets.full_ticket.trailer_number, scale_tickets.empty_ticket.trailer_number, scale_tickets.tractor_match, scale_tickets.trailer_match, scale_tickets.scale_match]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Flag',
     'Cargo (kg) recalc exact: (41,660 - 28,860) lb x 0.453592 = 12,800 lb x 0.453592 = 5,805.9776 kg = Ops Notes offload_4 row. For the April RP, this raw-scale-ticket value IS the correct mass basis — 2-204 is not the FC11 reconciliation point because the railcar\'s last-reported batch lands in the May RP (offload_2/3 = 2-202/2-203 were physically pulled in April but injected in May after re-filtering for solids). FLAG (not Pass) because the cross-RP split is a corner case that warrants extra Garrett scrutiny on the numbers — any railcar-level loss reconciliation will fall on whichever of 2-202/2-203 is reported last in the May RP, not on 2-204. [log:scale_tickets.net_lb_calc, scale_tickets.net_kg_calc, ops_notes.offload_table_populated_rows, is_last_offload_of_railcar, ops_notes.oil_left_in_railcar_kg, _derived_values.remaining_oil_in_railcar_mt]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Flag',
     'For the April RP: 2-204 uses raw scale-ticket math (5,805.9776 kg) as injectate basis. Sparging deduction (Section 2.6) applied to that. The MIN(scale, BOL) conservatism check at the RAILCAR level (FC11 back-calc) deferred to May RP, where it will land on whichever of 2-202/2-203 is reported last. FLAG (not Pass) to signal the cross-RP railcar split — Garrett, please double-check that the railcar-level reconciliation hand-off is tracked when 2-202/2-203 enter the May QA cycle. [log:scale_tickets.net_kg_calc, ops_notes.offload_table_populated_rows, bols_loaded_into_railcar.bol_aggregate_kg]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied: 5,805.9776 x 0.0129 = 74.89711 kg sparging loss. Mass of Bio-Oil Injected = 5,805.9776 - 74.89711 = 5,731.08049 kg. Ops Notes offload_4 row shows exactly these values (Sparging Loss 74.89711104 kg, Mass of Bio-Oil Injected 5,731.080489 kg); arithmetic correct. [log:ops_notes.sparging_mass_loss_pct, ops_notes.offload_table_populated_rows]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Flag',
     'Scale ticket net 5,805.98 kg = Ops Notes Cargo (kg) 5,805.9776 = COBB row offloaded_quantity_kg 5,805.9776 = Certify "Allocated Bio-Oil Mass - AECN via Rail" 5.806 t. Post-sparging Mass of Injectant 5,731.08 kg = Certify Datapoints 5.731 t. All four sources align — correct for the April RP (no FC11 adjustment applies here since the reconciliation lands on the May-RP last-reported batch). FLAG (not Pass) to signal the cross-RP railcar split — extra care warranted on TILX200228 numbers across both RPs. [log:scale_tickets.net_kg_calc, ops_notes.offload_table_populated_rows, cobb_row.offloaded_quantity_kg, certify_datapoints.Allocated_Bio_Oil_Mass_AECN_via_Rail_t, certify_datapoints.Mass_of_Injectant_t]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Drive AECN BOLs folder (id 1NqCHrdMrZGavRR6no8FXYmp1WAZP35Cg) AND in Certify Sources tab (#9, #10, #11): "Documents camion 2344-R corr.pdf", "Document Camion 2345-R corr.pdf", "Document Camion 2346-R.pdf". All three Public, linked to "Allocated Bio-Oil Mass - AECN via Rail" datapoint. [log:certify_sources_tab_total, bols_loaded_into_railcar.BOL_2344-R.filename, bols_loaded_into_railcar.BOL_2345-R.filename, bols_loaded_into_railcar.BOL_2346-R.filename]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2344-R, 2345-R, 2346-R) listed in COBB row BOL_number field for batch 2-204 ("2344-R, 2345-R, 2346-R") and in Ops Notes BOLs Loaded section (25.57 + 25.48 + 25.53 MT). Naming convention "-R" suffix = rail-load trucks. All 3 use Camion BIO-03 (same truck, 3 trips on 2026/03/30, 2026/03/31, 2026/03/31). Destination per BOL = "Société du port ferroviaire de Baie-Comeau" (SOPOR railyard at Port-Cartier, Quebec) — confirmed on each BOL formal page. Weighing destination = "PCT-USINE PORT CARTIER" on each transaction record. [log:cobb_row.BOL_number, ops_notes.bols_loaded_listed, bols_loaded_into_railcar.to_address]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL Masse Nette = 25,570 + 25,480 + 25,530 = 76,580 kg = Ops Notes Total Loaded Mass (76.58 MT) = COBB row origin_quantity_kg (76,580). This batch\'s offload mass = 5,805.98 kg, well below the railcar inbound. Rail-batch BOL mass check applied at railcar level (per Section 3.3 rail note). NOTE: BOL 2346-R formal page shows 25,370 kg / 25.37 MT (under-weighed), but the weighing transaction record on the same PDF shows 25,530 kg (post-correction). Sister BOLs 2344-R and 2345-R explicitly labeled "*Correction BOL"; 2346-R is the same correction pattern (formal under-weighed, weighing record corrected). Ops Notes / COBB / Certify all use the corrected 25.53 MT — consistent practice. [log:bols_loaded_into_railcar.bol_aggregate_kg, ops_notes.total_loaded_mass_mt, cobb_row.origin_quantity_kg, bols_loaded_into_railcar.BOL_2346-R, _derived_values.bol_2344_R_masse_nette_kg, _derived_values.bol_2345_R_masse_nette_kg, _derived_values.bol_2346_R_masse_nette_kg, _derived_values.scale_ticket_net_kg]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN (BioEnergie AE Côte-Nord, 175 Portage des Mousses, Port-Cartier, Quebec) -> SOPOR/Société du port ferroviaire de Baie-Comeau (Port-Cartier railyard via Camion BIO-03, 3 trucks each "-R" rail-load suffix) -> Opelousas LA (rail leg via railcar TILX200228 / Watco) -> Basco 6 (truck, this batch consumed_lot offload_4). All 3 inbound truck BOLs documented in Drive AECN BOLs + Certify Sources; rail leg distance documented via Watco email "image (44).png" (Section 9.9 hygiene); offload truck leg documented via this batch\'s scale tickets at PILOT BUNKIE LA scale. [log:bols_loaded_into_railcar.from_address, bols_loaded_into_railcar.to_address, cobb_row.consumed_lot]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified per FC9 + memory project_rail_distance_allocation. Note Certify stores AECN-side truck legs in km while Ops Notes records all distances in mi — explicit conversions below (1 mi = 1.609344 km). (1) AECN->SOPOR truck full single-truck distance: Ops Notes 107.5 mi x 1.609344 = 173.00 km, matches Certify Datapoint "Distance from AECN to Sopor Quebec (truck)" = 173.00 km exactly. Allocated Distance AECN to Sopor: Ops Notes Truck Leg 1 (offload_4) = 24.45061081 mi x 1.609344 = 39.349 km = Certify "Allocated Distance AECN to Sopor Quebec (truck)" 39.35 km — match within rounding. Methodology: full 322.5 truck-mi-total (3 trucks x 107.5 mi each) x 0.0758 batch allocation = 24.45 mi per batch share = 39.35 km. (2) SOPOR->Opelousas rail (both sources in mi, no conversion): full 2,199 mi per Certify "Distance from SOPOR to Opelousas (RAIL)" = Ops Notes batch_composition. Allocated rail distance: Ops Notes Rail (offload_4) 166.7190486 mi = Certify "Allocated Distance Sopor Quebec to Opelousas (rail)" 167 mi (= 2,199 x 0.0758, rounds to 167) — match within rounding. (3) Opelousas->Basco truck per-batch (both sources in mi, no conversion): 42.9 mi (full = allocated since each offload uses dedicated truck, no allocation needed); Certify modal shows 42.9 mi precise, Datapoints view rounds to 43 mi. [log:ops_notes.aecn_to_sopor_per_truck_mi, ops_notes.truck_trips_in_canada, ops_notes.sopor_to_opelousas_full_distance_mi, ops_notes.offload_table_populated_rows, certify_datapoints.Distance_from_AECN_to_Sopor_truck_km_full, certify_datapoints.Allocated_Distance_AECN_to_Sopor_truck_km, certify_datapoints.Distance_from_SOPOR_to_Opelousas_RAIL_mi_full, certify_datapoints.Allocated_Distance_Sopor_to_Opelousas_rail_mi, certify_datapoints.Distance_from_Opelousas_to_B6_truck_mi_full, rail_allocation_check.allocation_fraction, rail_allocation_check.allocated_distance_recalc_km, rail_allocation_check.allocated_distance_recalc_mi, _unit_conversions_3_5.allocated_truck_aecn_to_sopor_km_calc, _unit_conversions_3_5.allocated_rail_sopor_to_opelousas_mi_calc, _unit_conversions_3_5.full_truck_aecn_to_sopor_km_calc, _kb_constants.km_per_mi]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components present in Certify: AECN to SOPOR Tanker Truck Process (0.071 t), SOPOR to Opelousas Rail Process (0.331 t), Opelousas to Basco Tanker Truck Process (0.028 t), AECN to SOPOR Tanker Truck Embodied (0.006 t), SOPOR to Opelousas Rail Embodied (0.005 t), Opelousas to Basco Tanker Truck Embodied (0.010 t). Modes consistent with AECN rail convention. [log:certify_components.AECN_to_SOPOR_Truck_Process, certify_components.SOPOR_to_Opelousas_Rail_Process, certify_components.Opelousas_to_Basco_Truck_Process, certify_components.AECN_to_SOPOR_Truck_Embodied, certify_components.SOPOR_to_Opelousas_Rail_Embodied, certify_components.Opelousas_to_Basco_Truck_Embodied]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'All 3 BOL/billing PDFs serve as both BOL and billing for the inbound truck legs (AECN convention; PC0038196 / PC0038224 / PC0038229 weighing receipts at Port-Cartier with Customs/TSCA + Purchase Order pages). Charm-A4-2024-10-24-63-1976.pdf (BCU certificate, #14) also present in Sources tab. See Section 9.9 for filename hygiene observations. [log:bols_loaded_into_railcar.BOL_2344-R.weighing_no, bols_loaded_into_railcar.BOL_2345-R.weighing_no, bols_loaded_into_railcar.BOL_2346-R.weighing_no, certify_sources_full_enumeration]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder (or Certify Sources)', 'Pass',
     '"202-204, 5-10.pdf" present in Certify Sources (#7, Public), linked to "Carbon Content of Bio-oil Injected (per injection)" datapoint. Multi-batch SGS Certificate of Analysis order (SR26-02828) covering 5 samples: page 1 = 2-202 (.001), page 2 = 2-203 (.002), page 3 = 2-204 (.003 — THIS BATCH), page 4 = 2-205 (.004), page 5 = 5-10 (.005). Drive Testing subfolder is empty; lab cert lives in Certify Sources only — sufficient per Document Location Rule. Lab: SGS North America Inc., Authorised Signatory Rachel Oxley. [log:lab_results.filename_in_certify, lab_results.covers_batches, lab_results.for_2-204.certificate_id, lab_results.for_2-204.lab, lab_results.for_2-204.lab_supervisor]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-204 = 36.7% (m/m) (ASTM D5291 Method C). AECN typical mean 39.42% (n=285), SD 6.09%; 2-SD range 27.2%-51.6%. **36.7% is -0.45 SD below mean — well within the 2-SD range.** Lab cert flags result with "#" (outside test method limits/analytical range) — this is a standard SGS notation for bio-oil because the method precision study used petroleum products; "#" appears on virtually all Charm AECN samples and is not a finding. Carbon used correctly in Certify Net calc (36.70% in datapoint matches lab page 3 exactly). [log:lab_results.for_2-204.carbon_pct, certify_datapoints.Carbon_Content_pct, _kb_constants.aecn_carbon_mean_pct, _kb_constants.aecn_carbon_sd_pct, _kb_constants.aecn_sample_size_n, _kb_constants.aecn_carbon_2sd_upper_pct, _kb_constants.aecn_carbon_2sd_lower_pct, _derived_values.carbon_pct_sd_below_mean]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 7.9%, Nitrogen <0.75%, Kinematic Viscosity 7.653 cSt @ 40°C, Acid Number 48 mg KOH/g, Density 1.195 g/cm³ @ 15°C. All values within typical AECN ranges. Density >1.01 g/cm³ confirms safe injection (formation fluid threshold). [log:lab_results.for_2-204.hydrogen_pct, lab_results.for_2-204.nitrogen_pct_lt, lab_results.for_2-204.kinematic_viscosity_cSt_at_40C, lab_results.for_2-204.acid_number_mgKOH_g, lab_results.for_2-204.density_g_cm3_at_15C]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02828.003 explicitly labeled "BATCH 2-204" on page 3 (CLIENT ID field). Sampled 29-Apr-2026 06:36 at BASCO LOUISIANA (same date as injection completion 4/29/2026). Sample chain matches injection timing. [log:lab_results.for_2-204.certificate_id, lab_results.for_2-204.client_id, lab_results.for_2-204.sampled_date, lab_results.for_2-204.location]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate is recorded in Ops Notes Section 5.5. [log:oil_type]',
     'N/A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-204, Completion Date = 4/29/2026. Matches Certify removal date (29 Apr 2026). [log:ops_notes.batch_number, ops_notes.completion_date, certify_components.removal_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 41,660 lb = Ops Notes offload_4 Loaded Mass (lbs) 41,660 (exact). Empty ticket gross 28,860 lb = Ops Notes offload_4 Unloaded Mass (lbs) 28,860 (exact). Both values verified by direct image Read of Full JPG (playwright Drive viewer screenshot) and Empty PDF (curl signed URL + Read PDF page). Cargo (kg) using Ops Notes factor 0.453592: 12,800 x 0.453592 = 5,805.98 = Ops Notes offload_4 Cargo Mass (kg) 5,805.9776 (exact). [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.net_lb_calc, scale_tickets.net_kg_calc, ops_notes.offload_table_populated_rows]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Pass',
     'COBB row for "2-204" verified via gviz CSV query on the live "Basco Injection -- COBB" tab: cell A = "2-204" (ROW VERIFICATION GATE PASSED), consumed_lot C = "Rail_TILX200228_4.2.2026_offload_4" (matches Ops Notes), BOL_number E = "2344-R, 2345-R, 2346-R" matches Ops Notes BOLs Loaded, offloaded_quantity_kg G = 5,805.9776 = Ops Notes offload_4 Cargo (kg), origin_quantity_kg H = 76,580 = Ops Notes Total Loaded Mass x 1000 (NEW railcar TILX200228 — clean origin_quantity_kg, no stale-COBB carryover from prior railcars). All cross-source values match. order_line_completed_on I = 2026-04-16 14:58:26 = Manufacturo order processing date (NOT injection date); injection_completion_date L = 2026-04-29 = Certify removal date and Ops Notes Completion Date (all consistent). injection_ph M = 3.01 = Ops Notes offload_4 pH. [log:cobb_row_id_verified, cobb_cell_A_value, cobb_tab_name, cobb_row.consumed_lot, cobb_row.BOL_number, cobb_row.offloaded_quantity_kg, cobb_row.origin_quantity_kg, cobb_row.injection_completion_date, cobb_row.injection_ph]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_4 row pH = 3.01 = COBB row injection_ph 3.01 — exact match. Sister offload_1 on same railcar TILX200228 shows pH = 2.9, both within typical AECN injectate pH range. [log:ops_notes.offload_table_populated_rows, cobb_row.injection_ph]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date 4/29/2026 = COBB row injection_completion_date 2026-04-29 = Certify removal date 29 Apr 2026 — three-way exact match. COBB column I (order_line_completed_on) shows 2026-04-16 14:58:26 — this is Manufacturo order processing date, NOT injection date (consistent with prior batches\' QA pattern; Manufacturo column tracks order line completion in the inventory system, not the physical injection). Verifier reads Ops Notes / Certify / COBB injection_completion_date, all align. [log:ops_notes.completion_date, certify_components.removal_date, cobb_row.order_line_completed_on, cobb_row.injection_completion_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include a density entry — expected behavior. (Lab CoA reports density 1.195 g/cm³ for analytical reference only, not used by Ops Notes mass conversion.) [log:oil_type, lab_results.for_2-204.density_g_cm3_at_15C]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources (#15, Public), linked to "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" datapoint. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 — H2 2025 EFs carry through Q1/Q2 2026 reporting; same LCA used by sister batches 2-185 through 2-192). [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources (#17, Public), linked to "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)". [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources (#18, Public), linked to "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)". [log:certify_sources_full_enumeration]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" (Datapoints view shows 0.10 rounded). KB current native value 0.10402 tCO2e/t (H2 2025) — matches within rounding. Independent calc: 5.80598 t x 0.104 = 0.6038 t — matches Certify "AECN pyrolysis (from rail loads) - process emissions" 0.604 t (rounds). [log:certify_components.AECN_pyrolysis_process, _derived_values.pyrolysis_process_recalc_t]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)" (Datapoints view shows 0.02 rounded). KB current value 0.0212 tCO2e/t — modal 0.02116 matches at higher precision. Independent calc: 5.80598 x 0.02116 = 0.1228 t — matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" 0.123 t (rounds). [log:certify_components.AECN_pyrolysis_embodied, _derived_values.pyrolysis_embodied_recalc_t]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals confirm mass basis = "Allocated Bio-Oil Mass - AECN via Rail" = 5,805.98 kg = pre-sparging Cargo (kg). Sparging is applied only to Mass of Injectant for sequestration (Section 2.6). Methodology correct per Section 6.6. [log:certify_components.AECN_pyrolysis_process, certify_components.AECN_pyrolysis_embodied]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc with full precision: 5,731.080489 kg (Mass of Bio-Oil Injected, post-sparging) x 0.367 (Carbon Content from CHN) x 3.667 = 7,711.18 kg = 7.711 tCO2e. Certify Sequestrations component shows 7.713 tCO2e — match within 0.03% (rounding of 36.70% carbon to 0.367 in my calc). With full carbon precision 0.3670: 5731.08 x 0.3670 x 3.667 = 7,712.04 kg = 7.712 t (still rounds to 7.713 in Certify). [log:ops_notes.offload_table_populated_rows, lab_results.for_2-204.carbon_pct, certify_components.Sequestrations_t, math_reconciliation.gross_co2e_recalc, _derived_values.gross_co2e_recalc_short_kg, _derived_values.gross_co2e_recalc_short_t, _derived_values.gross_co2e_recalc_full_kg, _derived_values.gross_co2e_recalc_full_t]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted (3 transport process + 3 transport embodied + 2 pyrolysis): AECN->SOPOR truck process 0.071, SOPOR->Opelousas rail process 0.331, Opelousas->Basco truck process 0.028, AECN->SOPOR truck embodied 0.006, SOPOR->Opelousas rail embodied 0.005, Opelousas->Basco truck embodied 0.010, AECN pyrolysis process 0.604, AECN pyrolysis embodied 0.123. Sum = 1.178 tCO2e — matches Certify Activities total exactly. Each component independently math-reconciles to native EFs and route geometry (see math_reconciliation in source-read log). [log:certify_components.Activities_t, math_reconciliation.activities_sum_t]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount = 103 kg (= 0.103 t, 1.34% of gross sequestrations). Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate from per-component ± inputs — Isometric\'s aggregation is authoritative; QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.1468% carbon = 0.4% relative). Magnitude consistent with sister rail batches at smaller mass (uncertainty fraction is larger when the discrete-weight uncertainty is a higher pct of the smaller per-batch mass). [log:certify_components.Uncertainty_Discount_kg, math_reconciliation.uncertainty_discount_t, math_reconciliation.uncertainty_discount_pct_of_gross, _derived_values.uncertainty_discount_t, _derived_values.uncertainty_discount_pct_of_gross, _derived_values.carbon_uncertainty_relative_pct, _kb_constants.carbon_uncertainty_relative_pct, _kb_constants.discrete_weight_uncertainty_kg]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Flag',
     'Net = 7.713 (sequestrations) + 0.430 (BCU adjustments) - 1.178 (activities) - 0.103 (uncertainty) = 6.862 tCO2e ≈ Certify Net 6.861 t (display 6.86). Math reconciles within rounding. April RP scope: 2-204\'s raw-scale-ticket basis is correct as-is — FC11 reconciliation hooks into the May-RP last-reported TILX200228 batch (whichever of 2-202/2-203 is reported last), not 2-204. FLAG (not Pass) to signal the cross-RP corner case — Garrett, please double-check that the railcar-level reconciliation hand-off is tracked when the May QA cycle picks up 2-202/2-203. [log:certify_components.Net_CO2e_Removed_t_displayed, certify_components.Net_CO2e_Removed_t_precise, math_reconciliation.net_recalc_t]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show ±72.57 kg in INPUTS section (verified by opening each component modal individually): Injection Sequestration (Mass of product 5,731.08 ±72.57), AECN->SOPOR Truck Process (Mass of load 5,805.98 ±72.57), SOPOR->Opelousas Rail Process (Mass of load 5,805.98 ±72.57), Opelousas->Basco Truck Process (Mass of load 5,805.98 ±72.57), AECN Pyrolysis Process (Mass 5,805.98 ±72.57), AECN Pyrolysis Embodied (Mass 5,805.98 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi). Carbon Content uncertainty ±0.1468% (= 36.7 x 0.004, matches 0.4% relative). [log:certify_components.Injection_Sequestration, certify_components.AECN_to_SOPOR_Truck_Process, certify_components.SOPOR_to_Opelousas_Rail_Process, certify_components.Opelousas_to_Basco_Truck_Process, certify_components.AECN_pyrolysis_process, certify_components.AECN_pyrolysis_embodied]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported ± matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so ±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process + pyrolysis components). Verified by opening each component modal and reading the INPUTS section directly (no aggregate-discount inference). Carbon content ±0.1468% = 36.7 x 0.004 confirms standard 0.4% relative uncertainty. Conservatism precondition (N_offloads >= N_inbound_BOLs = 3) for railcar TILX200228 will be formally validated at the railcar\'s last batch QA — 2-204 is offload_4, only offloads 1 and 4 populated in 2-204 Ops Notes; 46.34 MT remains in railcar so further offloads to come. [log:certify_components.Injection_Sequestration, certify_components.AECN_to_SOPOR_Truck_Process, certify_components.SOPOR_to_Opelousas_Rail_Process, certify_components.Opelousas_to_Basco_Truck_Process, certify_components.AECN_pyrolysis_process, certify_components.AECN_pyrolysis_embodied, is_last_offload_of_railcar]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount = 103 kg in Calculation View. Net formula: Sequestrations - Activities + Adjustments - Uncertainty = 6.861 t Net (Certify display 6.86). Magnitude reasonable given mass and carbon uncertainty inputs. [log:certify_components.Uncertainty_Discount_kg, certify_components.Net_CO2e_Removed_t_precise, math_reconciliation.uncertainty_discount_t]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon = 36.7% within typical AECN range (mean 39.42%, -0.45 SD; 2-SD range 27.2-51.6%). Distances (107.5/2199/42.9 mi full-leg + 24.45/166.72 mi allocated), EFs (0.1143 truck process / 0.0259 rail process / 0.1476 truck embodied / 0.0193 rail embodied — 2026 corrected value for rail embodied, not stale 0.0000352240). Mass 5,805.98 kg pre-sparging / 5,731.08 kg post-sparging within expected per-truck offload range (smaller end — this is offload_4 of TILX200228 where the last 5.8 MT was pulled, vs sister offload_1 at 24.4 MT). Both scale tickets internally consistent (gross = axle sum). All math reconciles to Certify within rounding. BCU 0.430 t = exact sum of process transport (0.071 + 0.331 + 0.028 = 0.430) — clean BCU calculation, no over- or under-application. [log:lab_results.for_2-204.carbon_pct, certify_components, math_reconciliation]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. The Ops Notes "Oil Left in Railcar = 46.34 MT" cell reflects spreadsheet arithmetic on un-backfilled offload rows (offloads 2 and 3 = sister batches 2-202/2-203 awaiting Ops data), NOT physical oil remaining. Physical state: railcar TILX200228 fully drawn down (2-204 = small 5.8 MT remainder pull = last-truck signal). Railcar mass-balance reconciliation is performed in Section 8.3 once sister offload raw scale ticket data lands. [log:ops_notes.total_unloaded_mass_mt_in_this_ops_notes, ops_notes.oil_left_in_railcar_mt, ops_notes.oil_left_in_railcar_kg, is_last_offload_of_railcar]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch precondition for FC9 framing) + RP-scope last status', 'Flag',
     '**Cross-RP scope:** 2-204 is the railcar\'s physical last truck-out (small Cargo 5.8 MT signal — well below typical 18-25 MT AECN truck-out range), but it is NOT the railcar\'s last-reported batch in this April RP. All 4 offloads physically pulled in April; the middle two (offload_2 = 2-202, offload_3 = 2-203) needed re-filtering for solids and weren\'t injected until May, so they fall in the May RP. April-RP-reportable from this railcar: offload_1 (sister batch, injected April) + offload_4 (2-204, injected April). May-RP-reportable: 2-202 + 2-203. **FC11 last-offload mass-reconciliation hook:** lands on whichever of 2-202 / 2-203 is reported last in the May RP — NOT on 2-204. For 2-204\'s April RP entry, raw-scale-ticket Cargo (5,805.98 kg) is the correct mass basis with no policy adjustment. The blank offload_2/3 rows in 2-204\'s Ops Notes view + the "Oil Left in Railcar = 46,343.56 kg" figure reflect oil pulled-but-not-yet-injected at the time of 2-204\'s QA — those will reconcile in the May RP. **FC9 N_offloads >= N_inbound_BOLs precondition:** 4 (offloads) >= 3 (inbound BOLs 2344-R / 2345-R / 2346-R) — already met, per-leg ±72.57 kg uncertainty framing is conservative. FLAG (not Pass) to signal the cross-RP corner case — Garrett, please be extra careful with TILX200228 numbers and track the railcar-level reconciliation hand-off into the May RP\'s last-reported batch. [log:ops_notes.offload_table_populated_rows, ops_notes.offload_2_and_3_status, ops_notes.total_unloaded_mass_mt_in_this_ops_notes, ops_notes.oil_left_in_railcar_kg, ops_notes.fc11_backcalc_applies, _derived_values.cumulative_unloaded_kg_populated_rows, _derived_values.cumulative_unloaded_mt_populated_rows, _derived_values.remaining_oil_in_railcar_kg, _derived_values.remaining_oil_in_railcar_mt, _derived_values.cargo_mass_mt_2204, _derived_values.typical_truck_out_min_mt, _derived_values.typical_truck_out_max_mt, _kb_constants.n_inbound_bols_aecn_rail, bols_loaded_into_railcar.bol_aggregate_kg]',
     'KB Section 8 / FC9 / FC11'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component 7.713 tCO2e. Independent calc full precision: 5,731.08 kg x 0.3670 x 3.667 = 7,712 kg = 7.712 t (rounds to 7.713 in Certify). Carbon content matches CHN page 3 (36.70%). Component modal: Mass of product 5,731.08 ±72.57 kg, Carbon Content 36.7 ±0.1468 %. [log:certify_components.Sequestrations_t, certify_components.Injection_Sequestration, lab_results.for_2-204.carbon_pct, ops_notes.offload_table_populated_rows, math_reconciliation.gross_co2e_recalc, _derived_values.gross_co2e_recalc_kg_section_9_1, _derived_values.gross_co2e_recalc_t_section_9_1]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Component-level recalcs (independently verified):\\n• AECN→SOPOR Truck Process (0.071 t): 5.80598 t × 107.49 mi (=173 km full single-truck) × 0.0001143 MTCO2e/(t·mi) × 1000 kg/t = 71.32 kg = 0.071 t ✓\\n• SOPOR→Opelousas Rail Process (0.331 t): 5.80598 t × 2199 mi × 0.0000259104 MTCO2e/(t·mi) × 1000 = 330.81 kg = 0.331 t ✓\\n• Opelousas→Basco Truck Process (0.028 t): 5.80598 t × 42.9 mi × 0.0001143 × 1000 = 28.47 kg = 0.028 t ✓\\n• AECN→SOPOR Truck Embodied (0.006 t): 39.35 km (allocated) × 0.1476 kgCO2e/km = 5.81 kg = 0.006 t ✓\\n• SOPOR→Opelousas Rail Embodied (0.005 t): 167 mi (allocated) × 0.0000311307 MTCO2e/mi × 1000 = 5.20 kg = 0.005 t ✓ (2026 corrected value, NOT stale 0.0000352240 carried by 2-182 pre-fix)\\n• Opelousas→Basco Truck Embodied (0.010 t): 42.9 mi × 1.609344 = 69.04 km × 0.1476 = 10.19 kg = 0.010 t ✓\\nAllocated distances correctly use the inbound BOL aggregate (76,580 kg) as denominator (allocation fraction 0.0758 = 5,805.98 / 76,580). [log:certify_components.AECN_to_SOPOR_Truck_Process, certify_components.SOPOR_to_Opelousas_Rail_Process, certify_components.Opelousas_to_Basco_Truck_Process, certify_components.AECN_to_SOPOR_Truck_Embodied, certify_components.SOPOR_to_Opelousas_Rail_Embodied, certify_components.Opelousas_to_Basco_Truck_Embodied, rail_allocation_check, _derived_values.aecn_to_sopor_truck_recalc_kg, _derived_values.aecn_to_sopor_truck_recalc_t, _derived_values.sopor_to_opelousas_rail_recalc_kg, _derived_values.sopor_to_opelousas_rail_recalc_t, _derived_values.opelousas_to_basco_truck_recalc_kg, _derived_values.opelousas_to_basco_truck_recalc_t, _derived_values.aecn_to_sopor_truck_embodied_recalc_kg, _derived_values.sopor_to_opelousas_rail_embodied_recalc_kg, _derived_values.opelousas_to_basco_truck_embodied_km, _derived_values.opelousas_to_basco_truck_embodied_recalc_kg, _derived_values.aecn_to_sopor_truck_distance_mi_from_km, _derived_values.allocation_fraction_recalc]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (0.604 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.123 t) present. Component-level recalcs:\\n• Pyrolysis Process (0.604 t): 5.80598 t × 0.10402 tCO2e/t = 0.6039 t ✓ (Certify modal 0.104, Datapoints displays 0.10 rounded)\\n• Pyrolysis Embodied (0.123 t): 5.80598 × 0.02116 = 0.1228 t ✓ (Certify modal 0.02116 precise, Datapoints displays 0.02 rounded)\\nRail-batch naming convention used (deliberate signal to VVB to expect scale tickets as authoritative mass source). [log:certify_components.AECN_pyrolysis_process, certify_components.AECN_pyrolysis_embodied, _derived_values.pyrolysis_process_recalc_t_alt_precision, _derived_values.pyrolysis_embodied_recalc_t]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" (0.430 t = 430 kgCO2e) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify_components.Adjustments_BCU_t, certify_datapoints.BCU_kgCO2e]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU 0.430 t = exact sum of 3 transport process activities (0.071 + 0.331 + 0.028 = 0.430). BCU ≥ activity (here exactly equal). Embodied transport emissions (0.006 + 0.005 + 0.010 t) are NOT BCU-eligible per protocol — confirmed not double-claimed. No over-application of BCU credit. [log:certify_components.BCU_transport, math_reconciliation.transport_process_sum_t, math_reconciliation.BCU_offsets_transport_process_exactly]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify_components.Counterfactuals_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Flag',
     'Certify Net 6.861 t (display 6.86 t) = 7.713 (seq) - 1.178 (act) + 0.430 (BCU) - 0.103 (uncertainty); inputs reconcile within rounding. April RP Net CDR is correct as-is; FC11 reconciliation lands on May-RP last-reported TILX200228 batch (Section 8.3 FLAG), not 2-204. FLAG (not Pass) to signal the cross-RP corner case warrants extra Garrett scrutiny. [log:certify_components.Net_CO2e_Removed_t_displayed, certify_components.Net_CO2e_Removed_t_precise, math_reconciliation.net_recalc_t]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     'Same shared rail-batch hygiene set as sister batches 2-185/2-186/2-187/2-189/2-190/2-191/2-192 (Garrett-side filename hygiene, NOT verifier-impacting): (a) 4 non-descriptive Certify filenames carrying across rail batches: "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF source #13), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support #16), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance #19), "image (44).png" (SOPOR-Opelousas rail Watco distance email #20); (b) rail PROCESS EF datapoint sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" (#3) — same filename also linked to rail Embodied EF (#12, correctly), so file is multi-tab; PROCESS link references the Embodied tab specifically — possible single-tab vs multi-tab PDF inconsistency, EF VALUE is correct; (c) "AECN Process Emissions Calculation.xlsx" (#23) linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint, possible mislink (carryover from sister batches); (d) BCU certificate filename "Charm-A4-2024-10-24-63-1976.pdf" (#14) — same A4 filename used on TILX200231 batches (2-190/2-191/2-192) and TIMX201060 batches (2-188); 2-204 is railcar TILX200228, the third distinct railcar reusing the same BCU certificate file. BCU quantity 0.430 t exactly matches process transport sum so the QUANTITY is correct; only filename pattern in question — worth one-line confirmation Garrett pulled the right cert for THIS railcar\'s transport offset (it is plausibly a catch-all BCU cert not per-railcar). [log:certify_sources_full_enumeration, certify_sources_tab_total]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 source-datapoint links. All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (#9 Document Camion 2346-R, #10 Document Camion 2345-R corr, #11 Documents camion 2344-R corr), AECN LCA CI spreadsheet (#15 Bioenergy AE Cote-Nord 1Jul2025-31Dec2025), LCA with stack emissions (#17 BH 2025), Supporting GHG data (#18 31Dec2025), AECN Process Emissions Calculation (#23), Standard EFs Railcar Embodied (#3 + #12), Charm-A4 BCU certificate (#14), scale tickets (#5 Full + #6 Empty), CHN PDF (#7 202-204, 5-10 multi-batch), Ops Notes Rail (#1, #2, #4, #8 — 4 references), AECN to SOPOR (Baie Comeau) route map (#21), Truck Embodied Emissions image (#22), plus 4 generic-named screenshots/images flagged in 9.9 (#13, #16, #19, #20). Per Document Location Rule, presence in Certify Sources is sufficient for documents not also in Drive (Drive Testing folder is empty for 2-204 — lab cert lives in Certify Sources only). [log:certify_sources_tab_total, certify_sources_full_enumeration]',
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
            ws.row_dimensions[row].height = max(20, min(est_lines * 14, 280))

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
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '6.86 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'NONE — Net CDR 6.86 tCO2e is correctly calculated and reportable in the April RP as-is. **Cross-RP scope (corner case worth Garrett\'s extra attention):** 2-204 is the physical last truck-out from railcar TILX200228 (small Cargo 5.8 MT signal), but for the April RP it is the 2nd-and-final reportable batch from this railcar (sister offload_1 + 2-204). The middle two physical offloads (offload_2 = 2-202, offload_3 = 2-203) were pulled in April but had to be re-filtered for solids and were not injected until May — they will report in the May RP. FC11 railcar-level mass-reconciliation hook lands on whichever of 2-202 / 2-203 is reported LAST in the May RP, not on 2-204. For 2-204\'s April RP entry, raw-scale-ticket Cargo (5,805.98 kg) is the correct mass basis with no FC11 adjustment. Net CDR 6.86 t stands. Math reconciliation confirmed: 5,731.08 kg x 0.3670 x 3.667 = 7.713 t Seq; 1.178 t Activities (3 transport process + 3 transport embodied + 2 pyrolysis); 0.430 t BCU = exact process transport sum 0.071+0.331+0.028; 0.103 t uncertainty → 6.862 t Net ≈ Certify 6.861 (display 6.86). Carbon 36.7% within range (-0.45 SD from mean 39.42%). All 6 transport components recalc to native EFs. All uncertainty modals show ±72.57 kg per leg / ±0.1468% Carbon. FC9 N_offloads >= N_inbound_BOLs precondition: 4 (offloads) >= 3 (inbound BOLs) ✓ already met. **Action for Garrett:** track the railcar-level reconciliation hand-off when 2-202 / 2-203 enter the May QA cycle — extra care warranted on TILX200228 numbers given the cross-RP split.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '**Cross-RP corner-case FLAGs (8.3, 2.4, 2.5, 2.7):** 2-204 is physically the railcar\'s last truck-out but NOT the railcar\'s last-reported batch in the April RP — middle offloads 2-202 / 2-203 were pulled in April, re-filtered, injected in May, and report in the May RP. FC11 mass-reconciliation moves to whichever of those is last-reported in May. April RP values for 2-204 are correct as raw scale tickets; FLAGs signal Garrett to be extra careful on TILX200228 numbers across both RPs and to track the hand-off. **Hygiene FLAG (9.9, Garrett-side filename hygiene, NOT verifier-impacting):** (a) 4 non-descriptive Certify filenames [image (44).png, Screenshot 2026-04-10 PM.png, Screenshot 2026-02-23 AM.png, Screenshot 2026-01-27 125934.png] propagating across rail batches (same set as 2-185/186/187/189/190/191/192); (b) rail PROCESS EF sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to rail Embodied EF, possible single-tab vs multi-tab PDF inconsistency; (c) "AECN Process Emissions Calculation.xlsx" linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint; (d) BCU certificate filename "Charm-A4-2024-10-24-63-1976.pdf" — same A4 filename used on three different railcars now (TILX200231 batches 2-190/2-191/2-192, TIMX201060 batch 2-188, and now TILX200228 batch 2-204); BCU quantity 0.430 t exactly matches process transport sum — quantity correct, only filename-vs-railcar pattern in question.')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-204/Batch_2-204_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
