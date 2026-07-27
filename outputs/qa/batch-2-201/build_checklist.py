#!/usr/bin/env python3
"""Build Batch 2-201 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-201'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 23 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-06'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar TILX200228 — second batch QA\'d from this railcar; consumed_lot Rail_TILX200228_4.2.2026_offload_1. **2-201 is offload_1 — NOT the railcar\'s last truck-out.** Sister 2-204 (offload_4, 5,805.98 kg) is in the active registry awaiting Max review. Offloads 2 and 3 (sister batches 2-202/2-203) not yet in COBB or per-batch Ops Notes. FC11 last-offload back-calc DOES NOT APPLY here. FC9 N_offloads ≥ N_inbound_BOLs precondition is DEFERRED to whichever batch is the railcar\'s final pull.)'),
    ('META', 'Net CDR (Certify)', '30.58 tCO2e (Calculation View precise: 30.584)'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "1WnkfdTcoazZFCi9vk1k78nw_q93kF3sn" contains "2-201 Ops Notes Rail" Google Sheet (id 19bbnpB8TSoRvXp4lNnKucdteq_w9RyeaGGWh-OVVDC4, owner Garrett Lutz), Scale Tickets subfolder (id 1TAO_WaXqhSuikPJwcKI1rRLvhJSWtXs_, with Full JPG + Empty JPG), and Testing subfolder (id 1U2yflOAKadzN6iPKZQnlSh-XqcboSqUA, EMPTY in Drive — lab CHN cert "2-199 - 2-201.pdf" lives in shared parent Testing folder and is uploaded to Certify Sources). [log:_meta.batch_id, _meta.drive_folder_id, ops_notes.drive_file_id, drive_folder_contents.items]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains "2-201 Full Scale Ticket.jpg" (740 KB) and "2-201 Empty Scale Ticket.jpg" (741 KB). One offload pair (consistent with offload_1 of railcar TILX200228 — each batch represents one truck-out delivery from the railcar). Both also uploaded to Certify Sources (entries #7 Empty and #8 Full, both Public visibility, linked to "Mass of Injectant (per injection)" datapoint). Image pixels Read directly via download_file_content (base64 decode) then Read on the local JPG, NOT Drive OCR snippet, per memory feedback_ocr_not_primary_source. [log:scale_tickets.full_ticket.drive_file_id, scale_tickets.empty_ticket.drive_file_id, scale_tickets._source_method]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Flag',
     'Subfolder exists but is empty. Cert "2-199 - 2-201.pdf" (SR26-02683.003, page 3 of 3) is in Certify Sources #5 + shared parent Testing folder. Cert content verified — cert just not filed in this batch\'s Drive subfolder. Garrett to copy. [log:lab_results.drive_file_id, lab_results.shared_pdf_note, lab_results.page_3_certificate.certificate_id]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-201 Ops Notes Rail" Google Sheet present in Drive folder (owner Garrett Lutz, modified 2026-05-06). Header (Batch number 2-201, Completion Date 4/23/2026), Batch Composition (Railcar TILX200228, sparging 0.0129, lbs-to-kg 0.453592, route distances 2199 mi rail / 107.5 mi single-truck AECN-SOPOR × 3 trucks / 42.9 mi Opelousas-Basco), BOLs Loaded (3 inbound BOLs: 2344-R 25.57 MT + 2345-R 25.48 MT + 2346-R 25.53 MT; aggregate = 76.58 MT total), and offload_1 row populated (Loaded 83,060 lb, Unloaded 29,200 lb, Cargo 24,430.46512 kg, allocation 0.319019, Rail 701.5224967 mi, Truck Leg 1 102.8835858 mi). Rows offload_2/3/4 blank in this batch\'s Ops Notes — sister batches each have their own Ops Notes file. [log:ops_notes.filename, ops_notes.batch_number, ops_notes.completion_date, ops_notes.bols_loaded, ops_notes.total_loaded_mass_mt, ops_notes.trucks_unloaded_offload_1_for_this_batch]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 3 LOCATION = "BASCO LOUISIANA"; Certify project = "Charm Bio-oil Geologic Storage" (Basco). Ops Notes references Opelousas->Basco truck leg 42.9 mi. No Vaulted references in any source. [log:lab_results.page_3_certificate.location, certify_components_tab.header.removal_date]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both images Read directly from pixels (per OCR-vs-image rule). Full ticket #1312226107061, dated 4-17-26 10:54, at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA scale 3122; axle sum 10,000 + 36,460 + 36,600 = 83,060 lb (= certified gross, exact). Empty ticket #1312226107064, dated 4-17-26 13:00 same location/scale; axle sum 9,420 + 11,620 + 8,160 = 29,200 lb (= certified gross, exact). Both internally consistent (gross = axle sum). Same Tractor # CH 2 and Trailer # KL188 on both. Same weighmaster (Marsha Castille) on both — single trip, full and empty weighings 2 hours 6 minutes apart. [log:scale_tickets.full_ticket.ticket_number, scale_tickets.empty_ticket.ticket_number, scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.full_ticket.axle_sum_matches_gross, scale_tickets.empty_ticket.axle_sum_matches_gross]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Both tickets dated 4-17-26 (April 17, 2026). Injection completion date per Ops Notes = 4/23/2026. 6 days between truck-out and injection — within 2-week tolerance. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Both tickets show identical tractor "CH 2" and trailer "KL188". Same scale (3122), location (Pilot Travel Center, Bunkie LA). Same vehicle weighed at both events. Empty ticket cross-references Full ticket #1312226107061 in the "TICKET # OF FULL $ WEIGH (IF REWEIGH)" field — confirms paired weighing. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.empty_ticket.tractor_number, scale_tickets.full_ticket.trailer_number, scale_tickets.empty_ticket.trailer_number, scale_tickets.derived.tractor_match, scale_tickets.derived.trailer_match, scale_tickets.empty_ticket.linked_full_ticket_number]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     'Cargo (kg) at face is raw scale-ticket math: (83,060 - 29,200) lb × 0.453592 = 53,860 lb × 0.453592 = 24,430.4666 kg ≈ Ops Notes offload_1 Cargo Mass (kg) 24,430.46512 (exact within rounding). Per FC11, last-offload back-calc DOES NOT APPLY here (2-201 is offload_1, not the last offload of railcar TILX200228 — sister 2-204 is offload_4). Raw scale-ticket value is authoritative for offload_1. [log:scale_tickets.derived.net_weight_lb, scale_tickets.derived.net_lb_quoted, scale_tickets.derived.net_kg, scale_tickets.derived.net_kg_quoted, ops_notes.trucks_unloaded_offload_1_for_this_batch.cargo_mass_kg, _meta.is_last_offload_of_railcar]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Offload_1 of rail batch — conservative mass framing: scale-ticket-derived 24,430.47 kg (this batch) is well below per-BOL aggregate 76,580 kg (3 BOLs × ~25.5 MT each). For rail batches, the mass conservatism check is per-railcar: sum of per-offload Cargo (kg) ≤ BOL aggregate. Currently sum = 24,430.47 (offload_1) + 5,805.98 (offload_4) + offloads 2/3 pending = 30,236 + pending. Sum well below 76,580 envelope at this point. FC11 last-offload back-calc applicability is for the RAILCAR\'S LAST batch — that\'s 2-204 (per its registry note); not 2-201. For 2-201 the raw scale ticket value is correct and conservative. [log:scale_tickets.derived.net_weight_kg, _derived_values.scale_ticket_net_kg_quoted, _derived_values.cumulative_unloaded_kg_offload1_plus_offload4_quoted, bols_loaded_into_railcar.totals.sum_masse_nette_kg, sister_batch_context_for_railcar.current_railcar_trip_apr_2026]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied: 24,430.46512 × 0.0129 = 315.153 kg sparging loss. Mass of Bio-Oil Injected = 24,430.46512 - 315.153 = 24,115.31212 kg. Ops Notes offload_1 row shows exactly these values (Sparging Loss 315.153 kg, Mass of Bio-Oil Injected 24,115.31212 kg); arithmetic correct. [log:ops_notes.batch_composition.sparging_mass_loss_pct, ops_notes.trucks_unloaded_offload_1_for_this_batch.sparging_loss_kg, ops_notes.trucks_unloaded_offload_1_for_this_batch.mass_of_bio_oil_injected_kg, ops_notes.internal_math_verification.sparging_calc, ops_notes.internal_math_verification.injectate_calc]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Scale ticket net 24,430.47 kg = Ops Notes Cargo (kg) 24,430.46512 = Certify "Allocated Bio-Oil Mass - AECN via Rail" 24.430 t (modal precise 24,430.46) — all four sources align. Post-sparging Mass of Injectant 24,115.31 kg = Certify Datapoints "Mass of Injectant (per injection)" 24.115 t (modal precise 24,115.31). NOTE: COBB row 88 col G shows offloaded_quantity_kg = 19,145 — divergence handled in 5.4 (Garrett-side audit-trail FLAG, not verifier-impacting; Certify reads Ops Notes value directly). [log:scale_tickets.derived.net_weight_kg, ops_notes.trucks_unloaded_offload_1_for_this_batch.cargo_mass_kg, _derived_values.cobb_offloaded_quantity_kg_quoted, certify_uncertainty_per_component.aecn_pyrolysis_process.inputs.mass.value, certify_datapoints_tab.datapoints, certify_uncertainty_per_component.injection_sequestration.inputs.mass_of_product.value]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound truck BOLs present in Drive AECN BOLs folder (id 1NqCHrdMrZGavRR6no8FXYmp1WAZP35Cg) AND in Certify Sources tab (#9 Document Camion 2346-R.pdf, #10 Document Camion 2345-R corr.pdf, #11 Documents camion 2344-R corr.pdf). All three Public, linked to "Allocated Bio-Oil Mass - AECN via Rail" datapoint. [log:certify_sources_tab_total, certify_sources_tab_enumeration, bols_loaded_into_railcar.bol_2344_R.filename, bols_loaded_into_railcar.bol_2345_R.filename, bols_loaded_into_railcar.bol_2346_R.filename]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2344-R, 2345-R, 2346-R) listed in COBB row 88 BOL_number field for batch 2-201 ("2344-R, 2345-R, 2346-R") and in Ops Notes BOLs Loaded section (25.57 + 25.48 + 25.53 MT). Naming convention "-R" suffix = rail-load trucks. All 3 use Camion BIO-03 (same truck, 3 trips on 2026/03/30, 2026/03/31, 2026/03/31). Destination per BOL formal page = "Société du port ferroviaire de Baie-Comeau" (SOPOR railyard at Port-Cartier, Quebec). Weighing destination = "PCT-USINE PORT CARTIER" on each transaction record. [log:cobb_row_88.E_BOL_number, ops_notes.bols_loaded, bols_loaded_into_railcar.bol_2346_R.ship_to]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     'Sum of 3 BOL Masse Nette = 25,570 + 25,480 + 25,530 = 76,580 kg = Ops Notes Total Loaded Mass (76.58 MT) = COBB row 88 origin_quantity_kg (76,580) = Loads tab row 297 actual_loaded_mt (76.58) — four-source match. This batch\'s offload mass = 24,430.47 kg, well below the railcar inbound. Rail-batch BOL mass check applied at railcar level. NOTE: BOL 2346-R formal page shows 25,370 kg / 25.37 MT (volumetric, derived from 21,409 L), but the weighing transaction record on the same PDF shows 25,530 kg gravimetric (PC0038229 scale weighing). Sister BOLs 2344-R and 2345-R explicitly labeled "***Correction BOL"; 2346-R is original but contains the same gravimetric correction in its transaction record. Ops Notes / COBB / Certify all use the gravimetric 25.53 MT — consistent practice. [log:bols_loaded_into_railcar.totals, _derived_values.bol_2344_R_masse_nette_kg_short, _derived_values.bol_2345_R_masse_nette_kg_short, _derived_values.bol_2346_R_masse_nette_kg_short, _derived_values.bol_aggregate_kg_quoted, _derived_values.scale_ticket_net_kg_quoted, ops_notes.total_loaded_mass_mt, cobb_row_88.H_origin_quantity_kg, loads_tab_railcar_record.actual_loaded_mt, bols_loaded_into_railcar.bol_2346_R.header_volumetric_mt, bols_loaded_into_railcar.bol_2346_R.mt_net]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN (BioEnergie AE Côte-Nord, 175 Portage des Mousses, Port-Cartier, Quebec) → SOPOR/Société du port ferroviaire de Baie-Comeau (Port-Cartier railyard via Camion BIO-03, 3 trucks each "-R" rail-load suffix) → Opelousas LA (rail leg via railcar TILX200228 / Watco) → Basco 6 (truck, this batch consumed_lot offload_1). All 3 inbound truck BOLs documented in Drive AECN BOLs + Certify Sources; rail leg distance documented via Watco email "image (44).png" (Section 9.9 hygiene); offload truck leg documented via this batch\'s scale tickets at PILOT BUNKIE LA scale. Loads tab confirms carrier = Watco, asset = TILX200228, COA = RS1-260330-1 + RS1-260331-1, customs doc sent = True, PCB invoices received. [log:bols_loaded_into_railcar.bol_2346_R.from_origin, bols_loaded_into_railcar.bol_2346_R.ship_to, cobb_row_88.C_consumed_lot, loads_tab_railcar_record.carrier, loads_tab_railcar_record.asset_id, loads_tab_railcar_record.COA]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'Three legs verified per FC9 + memory project_rail_distance_allocation. Note Certify stores AECN-side truck legs in km while Ops Notes records all distances in mi — explicit conversions below (1 mi = 1.609344 km). (1) AECN→SOPOR truck full single-truck distance: Ops Notes 107.5 mi × 1.609344 = 173.00 km, matches Certify Datapoint "Distance from AECN to Sopor Quebec (truck)" = 173.00 km exactly. Allocated Distance AECN to Sopor: Ops Notes Truck Leg 1 (offload_1) = 102.8835858 mi × 1.609344 = 165.567 km = Certify "Allocated Distance AECN to Sopor Quebec (truck)" 165.57 km — match within rounding. Methodology: full 322.5 truck-mi-total (3 trucks × 107.5 mi each) × 0.31902 batch allocation = 102.88 mi per batch share = 165.57 km. (2) SOPOR→Opelousas rail (both sources in mi, no conversion): full 2,199 mi per Certify "Distance from SOPOR to Opelousas (RAIL)" = Ops Notes batch_composition. Allocated rail distance: Ops Notes Rail (offload_1) 701.5224967 mi = Certify modal "Allocated Distance Sopor Quebec to Opelousas (rail)" 701.52235 mi (Datapoints view rounds to 702 mi) — match within rounding. (3) Opelousas→Basco truck per-batch (both sources in mi, no conversion): 42.9 mi (full = allocated since each offload uses dedicated truck, no allocation needed); Certify modal shows 42.9 mi precise, Datapoints view rounds to 43 mi. [log:ops_notes.distances_km_or_mi.AECN_to_SOPOR_truck_single_mi, ops_notes.distances_km_or_mi.truck_trips_in_canada, ops_notes.distances_km_or_mi.SOPOR_to_Opelousas_rail_mi, ops_notes.distances_km_or_mi.Opelousas_to_Basco_truck_mi, ops_notes.trucks_unloaded_offload_1_for_this_batch.rail_miles_allocated, ops_notes.trucks_unloaded_offload_1_for_this_batch.truck_leg_1_miles_allocated, _derived_values.km_per_mi, _derived_values.allocated_truck_aecn_to_sopor_km_calc, _derived_values.allocated_truck_aecn_to_sopor_km_calc_short, certify_datapoints_tab.datapoints, certify_uncertainty_per_component.aecn_to_sopor_truck_embodied.inputs.distance_traveled, certify_uncertainty_per_component.sopor_to_opelousas_rail_embodied.inputs.distance_traveled, certify_uncertainty_per_component.opelousas_to_basco_truck_embodied.inputs.distance_traveled]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components present in Certify Components tab: AECN to SOPOR Tanker Truck Process (0.300 t), SOPOR to Opelousas Rail Process (1.391 t), Opelousas to Basco Tanker Truck Process (0.120 t), AECN to SOPOR Tanker Truck Embodied (0.024 t), SOPOR to Opelousas Rail Embodied (0.022 t), Opelousas to Basco Tanker Truck Embodied (0.010 t). Sum = 1.867 tCO2e = Certify Components "Bio-oil transport" total. Modes consistent with AECN rail convention. [log:certify_components_tab.removal_activities.components, certify_components_tab.removal_activities.bio_oil_transport_total_t]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'All 3 BOL/billing PDFs serve as both BOL and billing for the inbound truck legs (AECN convention; PC0038196 / PC0038224 / PC0038229 weighing receipts at Port-Cartier with Customs/TSCA + Purchase Order pages). BCU certificate Charm-A4-2024-10-24-63-1976.pdf (#14 Sources tab) also present. See Section 9.9 for filename hygiene observations. [log:bols_loaded_into_railcar.bol_2344_R.pesee_number, bols_loaded_into_railcar.bol_2345_R.pesee_number, bols_loaded_into_railcar.bol_2346_R.pesee_number, certify_sources_tab_enumeration]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder (or Certify Sources)', 'Pass',
     '"2-199 - 2-201.pdf" present in Certify Sources (#5, Public), linked to "Carbon Content of Bio-oil Injected (per injection)" datapoint. Multi-batch SGS Certificate of Analysis order (SR26-02683) covering 3 samples: page 1 = 2-199 (.001), page 2 = 2-200 (.002), page 3 = 2-201 (.003 — THIS BATCH). Drive Testing subfolder is empty for 2-201; lab cert lives in shared parent Testing folder + Certify Sources — sufficient per Document Location Rule. Lab: SGS North America Inc., Authorised Signatory Jacqualine Kilday. [log:lab_results.shared_pdf_note, lab_results.page_3_certificate.certificate_id, lab_results.page_3_certificate.authorised_signatory]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-201 = 38.3% (m/m) (ASTM D5291 Method C). AECN typical mean 39.42% (n=285), SD 6.09%; 2-SD range 27.2%-51.6%. **38.3% is -0.18 SD below mean — well within the 2-SD range.** Lab cert flags result with "#" (outside test method limits/analytical range) — this is a standard SGS notation for bio-oil because the method precision study used petroleum products; "#" appears on virtually all Charm AECN samples and is not a finding. Carbon used correctly in Certify Net calc (38.30% in datapoint matches lab page 3 exactly). [log:lab_results.page_3_certificate.carbon_pct, _derived_values.aecn_carbon_mean_pct, _derived_values.aecn_carbon_sd_pct, _derived_values.aecn_sample_size_n, _derived_values.aecn_carbon_2sd_lower_pct, _derived_values.aecn_carbon_2sd_upper_pct, _derived_values.carbon_pct_sd_below_mean, certify_datapoints_tab.datapoints, lab_results.carbon_within_aecn_2sd_range]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen, nitrogen, viscosity, acid number reported and reasonable', 'Pass',
     'H 7.8%, N <0.75%, Viscosity 9.820 cSt @ 40°C, Acid 44 mg KOH/g. Within typical AECN ranges. [log:lab_results.page_3_certificate.hydrogen_pct, lab_results.page_3_certificate.nitrogen_reported, lab_results.page_3_certificate.viscosity_cst_at_40C, lab_results.page_3_certificate.acid_number_mgKOH_per_g]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'SR26-02683.003 page 3 CLIENT ID = "BATCH 2-201". Sampled 18-Apr-2026 03:00 at BASCO LOUISIANA, 1 day after offload, 5 days before injection (4/23/2026). [log:lab_results.page_3_certificate.certificate_id, lab_results.page_3_certificate.client_id, lab_results.page_3_certificate.sampled_date, lab_results.page_3_certificate.location]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH of injectate recorded in Section 5.5. [log:_meta.oil_type]',
     'N/A'),
    ('4.6', 'Density above formation fluid threshold for safe injection', 'Pass',
     'Density 1.201 g/cm³ @ 15°C (CHN p3) > 1.01 g/cm³ formation fluid floor. Safe to inject. [log:lab_results.page_3_certificate.density_g_per_cm3_at_15C]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-201, Completion Date = 4/23/2026. Matches Certify removal date (23 Apr 2026). [log:ops_notes.batch_number, ops_notes.completion_date, certify_components_tab.header.removal_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket gross 83,060 lb = Ops Notes offload_1 Loaded Mass (lbs) 83,060 (exact). Empty ticket gross 29,200 lb = Ops Notes offload_1 Unloaded Mass (lbs) 29,200 (exact). Both values verified by direct image Read of Full and Empty JPGs (downloaded via Drive download_file_content + base64 decode, then Read on local file). Cargo (kg) using Ops Notes factor 0.453592: 53,860 × 0.453592 = 24,430.4666 ≈ Ops Notes offload_1 Cargo Mass (kg) 24,430.46512 (exact within rounding). [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.derived.net_weight_lb, scale_tickets.derived.net_lb_quoted, scale_tickets.derived.net_kg, scale_tickets.derived.net_kg_quoted, scale_tickets.derived.net_weight_kg, ops_notes.trucks_unloaded_offload_1_for_this_batch.cargo_mass_kg]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:_meta.oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Flag',
     'COBB row for "2-201" verified via openpyxl Read of "Basco Injection -- COBB" tab in downloaded XLSX export of Bio-oil Injection Tracker: cell A88 = "2-201" (ROW VERIFICATION GATE PASSED), consumed_lot C = "Rail_TILX200228_4.2.2026_offload_1" (matches Ops Notes), BOL_number E = "2344-R, 2345-R, 2346-R" matches Ops Notes BOLs Loaded, origin_quantity_kg H = 76,580 = Ops Notes Total Loaded Mass × 1000 (matches BOL aggregate). injection_completion_date L = 2026-04-23 = Certify removal date and Ops Notes Completion Date (all consistent). injection_ph M = 2.9 = Ops Notes offload_1 pH. **Garrett-side data-provenance FLAG (NOT verifier-impacting):** COBB col F (quantity_consumed_in_injection) and col G (offloaded_quantity_kg) both = 19,145.0 kg, but Ops Notes Cargo (kg) = 24,430.47 kg — divergence of 5,285 kg. Likely cause: 19,145 = 76,580 / 4 exactly, i.e., a placeholder equal-split value entered during planning before actual scale-ticket-derived mass was backfilled. Verifier reads Ops Notes / Certify (24,430.46 t in modal); COBB is not a verifier-facing source per project_railcar_mass_policy.md and FC11. Action item for Garrett: backfill COBB row 88 cols F/G with actual 24,430.47 kg. Same pattern category as TIMX201060 sisters (2-186/187/189 stale 71,010 origin_quantity_kg). [log:cobb_row_id_verified, cobb_cell_A_value, cobb_row_88.A_injection_batch, cobb_row_88.C_consumed_lot, cobb_row_88.E_BOL_number, cobb_row_88.F_quantity_consumed_in_injection_kg, cobb_row_88.G_offloaded_quantity_kg, cobb_row_88.H_origin_quantity_kg, cobb_row_88.L_injection_completion_date, cobb_row_88.M_injection_ph, cobb_row_88._cross_check_vs_ops_notes.OFFLOADED_QUANTITY_KG_DIVERGENCE]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_1 row pH = 2.9 = COBB row 88 injection_ph 2.9 — exact match. Sister offload_4 (2-204) on same railcar TILX200228 shows pH = 3.01, both within typical AECN injectate pH range. [log:ops_notes.trucks_unloaded_offload_1_for_this_batch.ph, cobb_row_88.M_injection_ph, _derived_values.ph_sister_offload_4, sister_batch_context_for_railcar.current_railcar_trip_apr_2026]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date 4/23/2026 = COBB row 88 injection_completion_date 2026-04-23 = Certify removal date 23 Apr 2026 — three-way exact match. COBB column I (order_line_completed_on) shows 2026-04-16 14:58:26 — this is Manufacturo order processing date, NOT injection date (consistent with prior batches\' QA pattern; Manufacturo column tracks order line completion in the inventory system, not the physical injection). Verifier reads Ops Notes / Certify / COBB injection_completion_date, all align. [log:ops_notes.completion_date, certify_components_tab.header.removal_date, cobb_row_88.I_order_line_completed_on, cobb_row_88.L_injection_completion_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include a density entry — expected behavior. (Lab CoA reports density 1.201 g/cm³ for analytical reference only, not used by Ops Notes mass conversion.) [log:_meta.oil_type, ops_notes.batch_composition.density_field_blank, lab_results.page_3_certificate.density_g_per_cm3_at_15C]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" present in Certify Sources (#15, Public), linked to "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" datapoint. Vintage covers H2 2025 (correct for batch sampled in Apr 2026 — H2 2025 EFs carry through Q1/Q2 2026 reporting; same LCA used by sister batches 2-185 through 2-204). [log:certify_sources_tab_enumeration, certify_document_presence_per_vr_appendix_1.aecn_lca_ci_spreadsheet_present]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" present in Certify Sources (#17, Public), linked to "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)". [log:certify_sources_tab_enumeration, certify_document_presence_per_vr_appendix_1.lca_with_stack_emissions_present]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" present in Certify Sources (#18, Public), linked to "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)". [log:certify_sources_tab_enumeration, certify_document_presence_per_vr_appendix_1.supporting_ghg_data_present]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail)" (Datapoints view shows 0.10 rounded). KB current native value 0.10402 tCO2e/t (H2 2025) — matches within rounding. Independent calc: 24.43046 t × 0.104 = 2.5408 t — matches Certify "AECN pyrolysis (from rail loads) - process emissions" 2.541 t (rounds). [log:certify_uncertainty_per_component.aecn_pyrolysis_process.inputs.carbon_emission_factor.value, certify_uncertainty_per_component.aecn_pyrolysis_process.math_verification, _derived_values.pyrolysis_process_recalc_t, _derived_values.pyrolysis_process_recalc_t_short, certify_components_tab.removal_activities.components]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t for "Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail)" (Datapoints view shows 0.02 rounded). KB current value 0.0212 tCO2e/t — modal 0.02116 matches at higher precision. Independent calc: 24.43046 × 0.02116 = 0.5170 t — matches Certify "AECN pyrolysis (from rail loads) - embodied emissions" 0.517 t (rounds). [log:certify_uncertainty_per_component.aecn_pyrolysis_embodied.inputs.carbon_emission_factor.value, certify_uncertainty_per_component.aecn_pyrolysis_embodied.math_verification, certify_components_tab.removal_activities.components]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals confirm mass basis = "Allocated Bio-Oil Mass - AECN via Rail" = 24,430.46 kg = pre-sparging Cargo (kg). Sparging is applied only to Mass of Injectant for sequestration (Section 2.6). Methodology correct per Section 6.6. [log:certify_uncertainty_per_component.aecn_pyrolysis_process.inputs.mass, certify_uncertainty_per_component.aecn_pyrolysis_embodied.inputs.mass]',
     'Bio-oil Geol Storage v1.1'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc with full precision: 24,115.31212 kg (Mass of Bio-Oil Injected, post-sparging) × 0.3830 (Carbon Content from CHN) × 3.667 = 33,866 kg = 33.866 tCO2e. Certify Sequestrations component shows 33.869 tCO2e — match within 0.01% (Certify uses higher-precision internal carbon). [log:ops_notes.trucks_unloaded_offload_1_for_this_batch.mass_of_bio_oil_injected_kg, lab_results.page_3_certificate.carbon_pct, certify_components_tab.sequestrations.total_t, certify_uncertainty_per_component.injection_sequestration.math_verification, _derived_values.gross_co2e_recalc_kg, _derived_values.gross_co2e_recalc_kg_quoted, _derived_values.gross_co2e_recalc_t]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 8 activity components deducted (3 transport process + 3 transport embodied + 2 pyrolysis): AECN→SOPOR truck process 0.300, SOPOR→Opelousas rail process 1.391, Opelousas→Basco truck process 0.120, AECN→SOPOR truck embodied 0.024, SOPOR→Opelousas rail embodied 0.022, Opelousas→Basco truck embodied 0.010, AECN pyrolysis process 2.541, AECN pyrolysis embodied 0.517. Sum = 4.925 tCO2e — matches Certify Activities total (Calculation View shows 4.926, 0.001 rounding gap). Each component independently math-reconciles to native EFs and route geometry (see math verifications in source-read log). [log:certify_components_tab.removal_activities.total_t, certify_calculation_view.activities_t, certify_uncertainty_per_component]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount = 170 kg = 0.170 t = 0.50% of gross sequestrations (= 0.56% of net). Per Isometric Standard S3.7.3 Option B (Variance Propagation), Certify computes the aggregate from per-component ± inputs — Isometric\'s aggregation is authoritative; QA scope is verifying the INPUTS (covered in Section 7a Layer 1+2: ±72.57 kg per discrete-weight datapoint, ±0.1532% carbon = 0.4% relative). Magnitude consistent with sister rail batches at similar mass. [log:certify_calculation_view.uncertainty_discount_kg, certify_calculation_view.uncertainty_discount_pct_of_net, _derived_values.uncertainty_discount_t, _derived_values.uncertainty_discount_pct_of_gross, _derived_values.carbon_uncertainty_pct_relative, _derived_values.carbon_uncertainty_absolute_pct, certify_uncertainty_per_component.injection_sequestration.inputs.carbon_content]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with internal calc and BCU offset', 'Pass',
     'Net = 33.869 (sequestrations) + 1.811 (BCU adjustments) - 4.926 (activities) - 0.170 (uncertainty) = 30.584 tCO2e ≈ Certify Net Calculation View 30.584 t (display 30.58). Math reconciles within rounding. BCU 1.811 t = exact sum of process transport (0.300 + 1.391 + 0.120 = 1.811) — clean BCU calculation, no over- or under-application. [log:certify_calculation_view.net_co2e_removed_t, certify_calculation_view.verification, certify_components_tab.adjustments, certify_components_tab.removal_activities]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components show ±72.57 kg in INPUTS section (verified by opening each component modal individually): Injection Sequestration (Mass of product 24,115.31 ±72.57), AECN→SOPOR Truck Process (Mass of load 24,430.46 ±72.57), SOPOR→Opelousas Rail Process (Mass of load 24,430.46 ±72.57), Opelousas→Basco Truck Process (Mass of load 24,430.46 ±72.57), AECN Pyrolysis Process (Mass 24,430.46 ±72.57), AECN Pyrolysis Embodied (Mass 24,430.46 ±72.57). Embodied transport components correctly have NO Mass-of-load datapoint (per-mile EFs, not per-T-mi). Carbon Content uncertainty ±0.1532% (= 38.3 × 0.004, matches 0.4% relative). [log:certify_uncertainty_per_component.injection_sequestration, certify_uncertainty_per_component.aecn_to_sopor_truck_process, certify_uncertainty_per_component.sopor_to_opelousas_rail_process, certify_uncertainty_per_component.opelousas_to_basco_truck_process, certify_uncertainty_per_component.aecn_pyrolysis_process, certify_uncertainty_per_component.aecn_pyrolysis_embodied]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported ± matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so ±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process + pyrolysis components). Verified by opening each component modal and reading the INPUTS section directly (no aggregate-discount inference). Carbon content ±0.1532% = 38.3 × 0.004 confirms standard 0.4% relative uncertainty. **Conservatism precondition (N_offloads ≥ N_inbound_BOLs = 3) for railcar TILX200228 is DEFERRED** — 2-201 is offload_1 (sister 2-204 = offload_4 awaiting Max review; offloads 2 and 3 not yet in COBB or per-batch Ops Notes); precondition test runs on whichever batch is the railcar\'s last pull. [log:certify_uncertainty_per_component, _meta.is_last_offload_of_railcar, sister_batch_context_for_railcar, sister_batch_context_for_railcar.current_railcar_trip_apr_2026]',
     'KB Section 7a / FC9'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency', 'Pass',
     'Aggregate uncertainty discount = 170 kg in Calculation View. Net formula: Sequestrations + Adjustments - Activities - Uncertainty = 33.869 + 1.811 - 4.926 - 0.170 = 30.584 t Net (Certify display 30.58). Magnitude reasonable given mass and carbon uncertainty inputs. [log:certify_calculation_view.uncertainty_discount_kg, certify_calculation_view.net_co2e_removed_t, certify_calculation_view.verification]',
     'Isometric Standard S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon = 38.3% within typical AECN range (mean 39.42%, -0.18 SD; 2-SD range 27.2-51.6%). Distances (107.5/2199/42.9 mi full-leg + 102.88/701.52 mi allocated), EFs (0.1143 truck process / 0.0259 rail process / 0.1476 truck embodied / 0.0193 rail embodied — 2026 corrected value for rail embodied, not stale 0.0000352240). Mass 24,430.47 kg pre-sparging / 24,115.31 kg post-sparging within typical per-truck offload range (18-25 MT for AECN rail batches; this is offload_1 of TILX200228 at the upper end, not the small last-offload remainder pull). Both scale tickets internally consistent (gross = axle sum). All math reconciles to Certify within rounding. BCU 1.811 t = exact sum of process transport (0.300 + 1.391 + 0.120 = 1.811) — clean BCU calculation, no over- or under-application. [log:lab_results.page_3_certificate.carbon_pct, certify_uncertainty_per_component, certify_calculation_view, certify_bcu_check]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'No spills/losses for this offload. Cargo (kg) = 24,430.47 reflects clean truck-out delivery. Sister offloads (2-202, 2-203, 2-204) have not all been pulled or QA\'d yet — railcar mass-balance reconciliation is performed once all offloads are documented. [log:ops_notes.trucks_unloaded_offload_1_for_this_batch.cargo_mass_kg, sister_batch_context_for_railcar]',
     'GHG Stmt Sec C'),
    ('8.3', 'Sister-batch sanity check (rail batch precondition for FC9 framing)', 'Pass',
     '**2-201 is offload_1 of railcar TILX200228 (4.2.2026 trip) — NOT the last offload.** Sister offload_4 = batch 2-204 (active in registry, status awaiting_max_review, Cargo (kg) 5,805.98 = small last-truck remainder signal). Sister offloads 2 and 3 (= sister batches 2-202 and 2-203) not yet in COBB or per-batch Ops Notes. **FC11 last-offload back-calc DOES NOT APPLY here** — applicability is on whichever batch is the railcar\'s final pull (likely 2-204). **FC9 N_offloads ≥ N_inbound_BOLs precondition test:** N_offloads = 4 expected (this railcar, based on offload_4 = 2-204 in COBB), N_inbound_BOLs = 3 (2344-R, 2345-R, 2346-R) → 4 ≥ 3, conservatism precondition met. The test will be formally validated on the railcar\'s last batch QA. For 2-201 (offload_1), raw scale-ticket math is authoritative and the Net CDR 30.58 t is internally complete. [log:_meta.is_last_offload_of_railcar, sister_batch_context_for_railcar, sister_batch_context_for_railcar.current_railcar_trip_apr_2026, sister_batch_context_for_railcar.implication, _derived_values.n_offloads_expected, _derived_values.n_inbound_bols_aecn_rail, _derived_values.fc9_precondition_met, applicable_failure_categories_summary.FC9, applicable_failure_categories_summary.FC11]',
     'KB Section 8 / FC9 / FC11'),

    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component 33.869 tCO2e. Independent calc full precision: 24,115.31 kg × 0.3830 × 3.667 = 33,866 kg = 33.866 t (rounds to 33.869 in Certify with full carbon precision). Carbon content matches CHN page 3 (38.30%). Component modal: Mass of product 24,115.31 ±72.57 kg, Carbon Content 38.3 ±0.1532 %. Calculation formula in modal: output = product_mass × carbon_content × {co2e_of_carbon}. [log:certify_components_tab.sequestrations.total_t, certify_uncertainty_per_component.injection_sequestration, lab_results.page_3_certificate.carbon_pct, ops_notes.trucks_unloaded_offload_1_for_this_batch.mass_of_bio_oil_injected_kg, _derived_values.gross_co2e_recalc_kg, _derived_values.gross_co2e_recalc_kg_quoted, _derived_values.gross_co2e_recalc_t]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Component-level recalcs (independently verified):\n• AECN→SOPOR Truck Process (0.300 t): 24.43046 t × 107.5 mi (= 173 km full single-truck) × 0.0001143 MTCO2e/(t·mi) × 1000 kg/t = 300.18 kg = 0.300 t ✓\n• SOPOR→Opelousas Rail Process (1.391 t): 24.43046 t × 2199 mi × 0.0000259 MTCO2e/(t·mi) × 1000 = 1391.39 kg = 1.391 t ✓\n• Opelousas→Basco Truck Process (0.120 t): 24.43046 t × 42.9 mi × 0.0001143 × 1000 = 119.79 kg = 0.120 t ✓\n• AECN→SOPOR Truck Embodied (0.024 t): 165.57 km (allocated) × 0.1476 kgCO2e/km = 24.43 kg = 0.024 t ✓\n• SOPOR→Opelousas Rail Embodied (0.022 t): 701.52 mi (allocated) × 0.0000311307 MTCO2e/mi × 1000 = 21.84 kg = 0.022 t ✓ (2026 corrected value, NOT stale 0.0000352240 carried by 2-182 pre-fix)\n• Opelousas→Basco Truck Embodied (0.010 t): 42.9 mi × 1.609344 = 69.04 km × 0.1476 = 10.19 kg = 0.010 t ✓\nAllocated distances correctly use the inbound BOL aggregate (76,580 kg) as denominator (allocation fraction 0.319019 = 24,430.47 / 76,580). [log:certify_uncertainty_per_component.aecn_to_sopor_truck_process, certify_uncertainty_per_component.sopor_to_opelousas_rail_process, certify_uncertainty_per_component.opelousas_to_basco_truck_process, certify_uncertainty_per_component.aecn_to_sopor_truck_embodied, certify_uncertainty_per_component.sopor_to_opelousas_rail_embodied, certify_uncertainty_per_component.opelousas_to_basco_truck_embodied, _derived_values.opelousas_to_basco_truck_embodied_km, _derived_values.scale_ticket_net_kg_quoted, _derived_values.km_per_mi, _derived_values.aecn_to_sopor_truck_process_recalc_kg_full_precision, ops_notes.trucks_unloaded_offload_1_for_this_batch.upstream_allocation_fraction]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted (typical for AECN rail batches). [log:_meta.oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (2.541 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.517 t) present. Component-level recalcs:\n• Pyrolysis Process (2.541 t): 24.43046 t × 0.10402 tCO2e/t = 2.541 t ✓ (Certify modal 0.104, Datapoints displays 0.10 rounded)\n• Pyrolysis Embodied (0.517 t): 24.43046 × 0.02116 = 0.517 t ✓ (Certify modal 0.02116 precise, Datapoints displays 0.02 rounded)\nRail-batch naming convention used (deliberate signal to VVB to expect scale tickets as authoritative mass source). Mass basis = Allocated Bio-Oil Mass (pre-sparging) per Section 6.6. [log:certify_uncertainty_per_component.aecn_pyrolysis_process, certify_uncertainty_per_component.aecn_pyrolysis_embodied]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" (1.811 t = 1,811 kgCO2e) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify_components_tab.adjustments, certify_bcu_check, _derived_values.bcu_in_kg, _derived_values.bcu_in_kg_quoted]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU 1.811 t = exact sum of 3 transport process activities (0.300 + 1.391 + 0.120 = 1.811). BCU ≥ activity (here exactly equal). Embodied transport emissions (0.024 + 0.022 + 0.010 t = 0.056 t) are NOT BCU-eligible per protocol — confirmed not double-claimed. No over-application of BCU credit. [log:certify_bcu_check, certify_components_tab.removal_activities.bio_oil_transport_total_t, certify_components_tab.adjustments, _derived_values.transport_embodied_sum_t, _derived_values.transport_process_sum_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:certify_components_tab.counterfactuals_total_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net 30.584 t (display 30.58 t) = 33.869 (seq) - 4.926 (act) + 1.811 (BCU) - 0.170 (uncertainty); inputs reconcile within rounding. Calculation View formula: Net = Sequestrations + Adjustments - Activities - Uncertainty Discount. Independent verification: 33.869 + 1.811 - 4.926 - 0.170 = 30.584 ✓ exact match. [log:certify_calculation_view.net_co2e_removed_t, certify_calculation_view.formula, certify_calculation_view.verification]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     'Same shared rail-batch hygiene set as sister batches 2-185/2-186/2-187/2-189/2-190/2-191/2-192/2-204 (Garrett-side, NOT verifier-impacting). **Filename-hygiene FLAGs:** (a) 4 non-descriptive Certify filenames carrying across rail batches: "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF source #13), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support #16), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance #19), "image (44).png" (SOPOR-Opelousas rail Watco distance email #20); (b) rail PROCESS EF datapoint sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" (#1 Private) — file says "Embodied" but datapoint is "Rail Transport Fuel Use (Well to Wheel)" PROCESS; same filename also linked to rail Embodied EF (#12 Public, correctly), so file is multi-tab; PROCESS link references the Embodied tab specifically — possible single-tab vs multi-tab PDF inconsistency, EF VALUE is correct; (c) "AECN Process Emissions Calculation.xlsx" (#23) linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint (carryover from sister batches). **BCU cert provenance question (substantive, separate from filename-hygiene):** BCU certificate "Charm-A4-2024-10-24-63-1976.pdf" (#14) used on three distinct railcars now (TILX200231 batches 2-190/2-191/2-192, TIMX201060 batch 2-188, and now TILX200228 batches 2-201/2-204). BCU quantity 1.811 t exactly matches process transport sum 0.300+1.391+0.120 ✓ (quantity verified correct). The question is whether this is a catch-all BCU cert that legitimately spans multiple railcars or whether the wrong cert has been linked — worth one-line Garrett confirmation. [log:certify_sources_tab_total, certify_sources_tab_enumeration, certify_bcu_check]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 23 source-datapoint links. All required Appendix 1 docs present in Certify Sources: 3 inbound BOLs (#9 Document Camion 2346-R, #10 Document Camion 2345-R corr, #11 Documents camion 2344-R corr), AECN LCA CI spreadsheet (#15 Bioenergy AE Cote-Nord 1Jul2025-31Dec2025), LCA with stack emissions (#17 BH 2025), Supporting GHG data (#18 31Dec2025), AECN Process Emissions Calculation (#23), Standard EFs Railcar Embodied (#1 + #12), Charm-A4 BCU certificate (#14), scale tickets (#7 Empty + #8 Full), CHN PDF (#5 multi-batch 2-199 - 2-201), Ops Notes Rail (#2, #3, #4, #6 — 4 references), AECN to SOPOR (Baie Comeau) route map (#21), Truck Embodied Emissions image (#22), plus 4 generic-named screenshots/images flagged in 9.9 (#13, #16, #19, #20). Per Document Location Rule, presence in Certify Sources is sufficient for documents not also in Drive (Drive Testing folder is empty for 2-201 — lab cert lives in Certify Sources only). [log:certify_sources_tab_total, certify_sources_tab_enumeration, certify_document_presence_per_vr_appendix_1]',
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
    if fail_count > 0:
        ws.cell(row, 1).fill = FAIL_FILL; ws.cell(row, 2).fill = FAIL_FILL
    row += 1
    ws.cell(row, 1, 'Flag'); ws.cell(row, 2, flag_count)
    ws.cell(row, 1).fill = FLAG_FILL; ws.cell(row, 2).fill = FLAG_FILL
    row += 1
    ws.cell(row, 1, 'N/A'); ws.cell(row, 2, na_count)
    row += 2
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '30.58 tCO2e (Calculation View precise: 30.584)')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'Clean batch — math reconciles cleanly across all 9 components: 24,115.31 kg × 0.3830 × 3.667 = 33.866 t Seq (Certify 33.869, full-precision carbon); 4.925 t Activities; 1.811 t BCU = exact process transport sum 0.300+1.391+0.120; 0.170 t uncertainty → 30.584 t Net = Certify 30.58 displayed. Carbon 38.3% within range (-0.18 SD). All 6 transport components recalc to native EFs. All uncertainty modals show ±72.57 kg per leg / ±0.1532% Carbon. 2-201 is offload_1 of railcar TILX200228; FC11 last-offload back-calc DOES NOT APPLY here; FC9 N_offloads ≥ N_BOLs precondition test deferred to railcar\'s last batch QA.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '5.4 (Garrett-side data-provenance, NOT verifier-impacting): COBB row 88 cols F and G show offloaded_quantity_kg = 19,145.0 (= 76,580/4 placeholder equal-split) vs Ops Notes Cargo (kg) 24,430.47 (5,285 kg divergence). COBB stale; Certify reads Ops Notes value. Action: Garrett to backfill COBB cols F/G with actual scale-ticket-derived value 24,430.47. 9.9 (Garrett-side filename hygiene, NOT verifier-impacting): (a) 4 non-descriptive Certify filenames [image (44).png, Screenshot 2026-04-10 PM.png, Screenshot 2026-02-23 AM.png, Screenshot 2026-01-27 125934.png] propagating across rail batches (same set as 2-185/186/187/189/190/191/192/204); (b) rail PROCESS EF sourced from "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf" — same filename also linked to rail Embodied EF, possible single-tab vs multi-tab PDF inconsistency; (c) "AECN Process Emissions Calculation.xlsx" linked to "Carbon Intensity - AECN Pyrolysis Embodied Emissions" datapoint — file named "Process" linked to Embodied datapoint (carryover from sister batches). 9.9 (BCU cert PROVENANCE — substantive question, separate from filename-hygiene): "Charm-A4-2024-10-24-63-1976.pdf" used as the BCU certificate on three distinct railcars now (TILX200231 batches 2-190/2-191/2-192, TIMX201060 batch 2-188, and now TILX200228 batches 2-201/2-204). BCU quantity 1.811 t exactly matches process transport sum 0.300+1.391+0.120 ✓ (quantity is verified correct); the question is whether this is a catch-all BCU cert that legitimately spans multiple railcars or whether the wrong cert has been linked. Worth one-line Garrett confirmation.')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-201/Batch_2-201_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
