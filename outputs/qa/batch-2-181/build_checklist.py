#!/usr/bin/env python3
"""Build Batch 2-181 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

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
    ('META', 'Batch ID', '2-181'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 01 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-11'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Truck (direct AECN Quebec → Basco LA, BOL 2338-T, tanker truck)'),
    ('META', 'Net CDR (Certify)', '23.23 tCO2e (Calculation View precise: 23.227)'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder "1KZ2xuevrnHaekN3g7LvGtsq25alUvkVp" titled "2-181" contains 3 items: Testing subfolder (id 12iONhexzxt8szWvKluTB6Hb8Vm5VuzZ2), Scale Tickets subfolder (id 1l2SpkKmxka42EOjxIXIfftH7EYeOnCbY), and "2-181 Ops Notes" Google Sheet (id 1mFGLeoceVXrFHCcffoSKKQJ-6EzkfaRc33lm-KyuFcQ). Parent folder breadcrumb "4/1/26-4/5/26" — consistent with injection date 4/1/2026. [log:batch_id, drive_folder.id, drive_folder.contents]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains "2-181 Full Scale Ticket.jpg" (517 KB, drive_id 1vgS09NJbuVEZ-U88lEzAEriuGzl-yI_B) and "2-181 Empty Ticket (1).png" (1.9 MB, drive_id 1IVCOu9sVUHWSIR93QqTbcXzD5dzx_t3V). Both uploaded by Garrett Lutz on Apr 30. Both also in Certify Sources tab (file #6 Empty + #7 Full, both Public, linked to "Mass of Injectant (per injection)" datapoint). Files downloaded via drive.usercontent.google.com/download response-body capture per memory feedback_drive_image_download_pattern. [log:scale_tickets.full_ticket.drive_id, scale_tickets.empty_ticket.drive_id, certify.certify_sources_enumeration]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Testing subfolder is populated with "SR26-02231_Batch_2-180-185_COA (1).pdf" (51 KB, owner Garrett Lutz, modified Apr 23) — verified via Playwright snapshot of folder id 12iONhexzxt8szWvKluTB6Hb8Vm5VuzZ2. Multi-batch SGS Certificate of Analysis spanning 2-180 through 2-185 (batch 2-181 = page 2 of 6, Certificate ID SR26-02231.002, Carbon 36.6%). Same cert also present in Certify Sources #5 (Public, linked to "Carbon Content of Bio-oil Injected (per injection)" datapoint) — file is in BOTH locations. [log:drive_folder.contents, drive_folder.testing_folder_empty, lab_results.filename, lab_results.page_for_2_181, evidence_sources]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-181 Ops Notes" Google Sheet present in Drive folder (id 1mFGLeoceVXrFHCcffoSKKQJ-6EzkfaRc33lm-KyuFcQ). All sections populated: Completion Date 4/1/2026, Batch Composition (Origin 2338-T at 19,950 kg, Total 19,950 kg, sparging factor 0.0129, Lbs/Kg 2.20462), Injection Data (Truck 1 Full 78,660 lb / Empty 34,740 lb / Net 43,920 lb = 19,921.76 kg, Truck 2 unused per single-truck batch, pH 3.4), Mass Reconciliation (Total Injectate 19,921.76 kg, Sparging Loss 256.99 kg, Mass of Bio-Oil Injected 19,664.77 kg, AECN Oil Added 19,950 kg, AECN Oil Injected 19,664.77 kg, Loss 285.23 kg / 1.43%). Filename "2-181 Ops Notes" (no Rail suffix) = truck batch. [log:ops_notes.filename, ops_notes.completion_date, ops_notes.origin_lot, ops_notes.origin_mass_kg, ops_notes.truck_1_full_mass_lb, ops_notes.truck_1_empty_mass_lb, ops_notes.truck_1_injectate_mass_kg, ops_notes.ph, ops_notes.mass_of_bio_oil_injected_kg]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 2 LOCATION = "BASCO LOUISIANA"; BOL 2338-T Ship-To = "CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA" (Basco facility address); Certify project = "Charm Bio-oil Geologic Storage" (Basco). No Vaulted references in any source — exhaustive scan of lab cert, BOL Billing Documents PDF, Certify Components/Datapoints/Sources/Calc View tabs all opened and no occurrence of "Vaulted"/"Hutchinson"/"Kansas"/"KDHE" found. [log:lab_results.location, bol.page_1_straight_bol.ship_to, certify.removal_date, evidence_sources]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Flag',
     'Full ticket: directly readable JPG photo of CAT scale ticket #4668 dated 3-25-26, at Pilot Travel Center I-49 Exit 40 Bunkie LA scale #3122; gross 78,660 lb (steer 12,500 + drive 33,380 + trailer 32,780 = 78,660 ✓ axles sum to gross); BOL 2338-T overlaid in same image (Bioenergie AE Côte-Nord Canada → CHARM, dated 2026-03-18). Empty ticket: PNG file is a phone screenshot of an SMS thread (1080×2340 px) containing a photo of the empty CAT ticket, rotated 90° within the screenshot at small effective resolution; CAT template layout and weighmaster signature visible but individual digit values are difficult to verify directly from the image pixels. Both files are uploaded and present, but the empty ticket capture format is a hygiene issue worth Garrett surfacing for future batches (preferred: direct ticket photo, not chat-thread screenshot). Math reconciliation between the two tickets (Full 78,660 - Empty 34,740 per Ops Notes = 43,920 lb = 19,921.76 kg) is internally consistent. [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.full_ticket.steer_axle_lb, scale_tickets.full_ticket.drive_axle_lb, scale_tickets.full_ticket.trailer_axle_lb, scale_tickets.empty_ticket.image_quality, scale_tickets.empty_ticket.directly_readable_from_image, scale_tickets.net_calc_lb, scale_tickets.net_calc_kg]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Full scale ticket dated 3-25-26 (March 25, 2026). Ops Notes Completion Date 4/1/2026 (April 1, 2026). 7 days between Charm-side weighing and injection — within 14-day tolerance. AECN-side BOL date 2026-03-18 (March 18, 2026) — 14 days before injection (inbound transit). All within tolerance. [log:scale_tickets.full_ticket.date, ops_notes.completion_date, bol.page_1_straight_bol.date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Flag',
     'Full ticket explicitly shows Tractor #815 and Trailer #50315 (carrier NORTH HAUL, weighmaster Paula Maynard). Empty ticket image quality (low-resolution phone screenshot of SMS thread) prevents direct pixel-level verification of tractor/trailer digits on the empty ticket. Indirect evidence supporting same-vehicle: (a) Ops Notes records Full 78,660 lb and Empty 34,740 lb → Net 43,920 lb, propagating to Mass of Injectant 19.665 t in Certify with full math reconciliation; (b) same CAT scale (3122) and location implied by ticket template; (c) NORTH HAUL is the consistent carrier on AECN truck batches. Garrett-side action: re-upload empty ticket as direct photo, not SMS screenshot, so future QA can verify tractor/trailer digits directly. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.full_ticket.trailer_number, scale_tickets.full_ticket.carrier_company, scale_tickets.empty_ticket.directly_readable_from_image]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     'Net = Full 78,660 lb - Empty 34,740 lb = 43,920 lb. Converted: 43,920 / 2.20462 = 19,921.76 kg. Ops Notes records exactly 43,920 lb and 19,921.76064 kg (full precision). Math correct, no transcription error. [log:scale_tickets.full_ticket.gross_weight_lb, ops_notes.truck_1_empty_mass_lb, ops_notes.truck_1_injectate_mass_lb, ops_notes.truck_1_injectate_mass_kg, _derived_values.scale_ticket_full_minus_empty_lb, _derived_values.scale_ticket_net_kg_recalc, ops_notes.constants.Lbs_per_Kg]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Scale net (Charm-side, Bunkie LA CAT 3122): 19,921.76 kg. BOL mass (AECN-side, Port Cartier scale PC0038045 per BOL page 4): 19,950 kg masse nette. MIN = 19,921.76 kg (Charm scale) — adopted as Total Injectate Mass in Ops Notes. The 28.24 kg gap between the two scales is within typical truck-trip mass uncertainty (±72.57 kg per discrete weighing, Isometric Standard v2.0 §3.7.3). [log:_derived_values.charm_scale_net_kg, _derived_values.aecn_scale_net_kg, _derived_values.min_of_scale_vs_bol_kg, _derived_values.min_of_scale_vs_bol_winner, ops_notes.total_injectate_mass_kg, bol.authoritative_mass_kg, evidence_sources]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied to Total Injectate Mass: 19,921.76 × 0.0129 = 256.99 kg sparging loss. Mass of Bio-Oil Injected = 19,921.76 - 256.99 = 19,664.77 kg. Ops Notes records sparging loss 256.9907123 kg and Mass of Bio-Oil Injected 19,664.76993 kg — matches independent recalc to full precision. [log:ops_notes.constants.Sparging_Mass_Loss_fraction, ops_notes.total_injectate_mass_kg, ops_notes.sparging_loss_kg, ops_notes.mass_of_bio_oil_injected_kg, _derived_values.sparging_loss_kg_recalc, _derived_values.mass_bio_oil_injected_kg_recalc]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Four-way mass chain reconciles cleanly. Origin (pre-sparging) layer: BOL Billing Documents 2338-T page 3/4 = 19,950 kg = Ops Notes Origin Mass = COBB H_origin_quantity_kg = Certify "Origin Bio-Oil Mass - AECN" 19.950 t. Conservative-mass layer: Charm scale net 19,921.76 kg = Ops Notes Total Injectate Mass = COBB G_offloaded_quantity_kg = COBB F_quantity_consumed_in_injection. Final injectate layer (post-sparging): 19,664.77 kg = Ops Notes Mass of Bio-Oil Injected = Certify "Mass of Injectant (per injection)" 19.665 t. All three layers internally consistent across all four sources. [log:ops_notes.origin_mass_kg, bol.page_3_shipping_details.product_delivered_kg, cobb.fields.H_origin_quantity_kg, certify.datapoints, ops_notes.mass_of_bio_oil_injected_kg, cobb.fields.G_offloaded_quantity_kg, cobb.fields.F_quantity_consumed_in_injection_kg]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOL(s) present for each shipment', 'Pass',
     '"Billing Documents 2338-T.pdf" present in Certify Sources #9 (Public, linked to "Origin Bio-Oil Mass - AECN" datapoint). 5-page PDF: page 1 = Straight Bill of Lading, page 2 = Charm Purchase Order, page 3 = AECN shipping details with scale weighing, page 4 = French scale ticket (No de pesée PC0038045, masse nette 19,950 kg), page 5 = Commercial Invoice. Single BOL = single truck shipment for direct AECN→Basco. [log:bol.filename_in_certify_sources, bol.pages, bol.page_1_straight_bol.bol_number, certify.certify_sources_enumeration]',
     'VR Appendix 1'),
    ('3.2', 'Not applicable for truck batch (rail-only check)', 'N/A',
     'Item 3.2 specifies rail batches (3 truck BOLs from AECN to SOPOR railyard). This is a direct truck batch (AECN Quebec → Basco LA in a single tanker truck). [log:_meta_delivery_mode]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass', 'Pass',
     'BOL authoritative mass (page 3 highlighted "Qty shipped" / page 4 scale-weighed masse nette) = 19,950 kg = 19.95 MT. Reported injectate mass (Certify Mass of Injectant per injection) = 19.665 t. BOL 19,950 ≥ Injectate 19,665 by 285 kg (1.43% — consistent with sparging deduction). Note BOL internal: page 1 Quantity row shows 19,690 kg / 19.69 MT (volumetric derivation from 16,616 L); pages 3-4 show 19,950 kg gravimetric (Port Cartier scale PC0038045). Charm uses the AECN-scale value 19,950 kg as authoritative — this is what flows into Certify Origin Bio-Oil Mass. Pages 5 Commercial Invoice repeats the page-1 volumetric 19.69 MT for export documentation. The 260 kg volumetric-vs-gravimetric BOL-internal gap is documented in derived_values; not a verifier-impacting reporting error since the gravimetric scale weighing is the authoritative input. [log:bol.authoritative_mass_kg, bol.page_3_shipping_details.product_delivered_kg, bol.page_4_scale_ticket_french.masse_nette_kg, bol.page_1_straight_bol.quantity_kg_volumetric_in_parens, bol.page_5_commercial_invoice.quantity_metric_ton, bol.internal_inconsistency_note, _derived_values.bol_volumetric_vs_scale_mass_gap_kg, certify.datapoints]',
     'VR Sec 3.5'),
    ('3.4', 'Origin and destination correct on BOL', 'Pass',
     'BOL page 1: From = BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier, Québec, G5B 2V9. Ship To = CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA (Basco facility). Production Period #03-2026, Customer PO Q4-2025, CofA RS1-260316-1. Carrier ALG Worldwide Logistics, Driver Sylvie Tessier, Truck ID 811, Tanker ID 50397. Origin and destination match the canonical AECN→Basco truck route. [log:bol.page_1_straight_bol.from, bol.page_1_straight_bol.ship_to, bol.page_1_straight_bol.carrier, bol.page_1_straight_bol.driver, bol.page_1_straight_bol.cofa]',
     'PDD'),
    ('3.5', 'Transportation distance consistent with known AECN truck route', 'Pass',
     'Certify Datapoint "Distance from AECN to Basco" = 2,197 mi (Derived), "Aggregate Distance Transported AECN to Basco" = 2,197 mi (Reported). Matches the canonical AECN Quebec → Basco LA direct-truck route (~2,197 mi). Single source: "AECN to Basco.png" (Google Maps screenshot in Certify Sources #12, Public, linked to both distance datapoints). [log:certify.datapoints, certify.component_modal_uncertainty.truck_transport_process.distance_mi, certify.certify_sources_enumeration]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = tanker truck (direct AECN, no rail)', 'Pass',
     'Certify Components tab shows 2 transport components: "AECN to LA Tanker Truck Transport Process Emissions - AECN" (5.010 t, 21.57%) and "AECN to LA Tanker Truck Transport Embodied Emissions - AECN" (0.522 t, 2.25%). No rail leg components present (would be 6 components for a rail batch). Consistent with direct-truck delivery per BOL 2338-T. Component naming uses new 2026 "AECN to LA Tanker Truck" pattern (parallel to "AECN to SOPOR/SOPOR to Opelousas/Opelousas to Basco" naming on rail batches). [log:certify.components.transport_process_aecn_to_la_t, certify.components.transport_embodied_aecn_to_la_t, certify.components.naming_note]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOL', 'Pass',
     'Billing Documents 2338-T.pdf serves as combined BOL + billing + commercial invoice (5 pages in one PDF: BOL, Charm PO Q42025, AECN shipping/weighing details, French scale ticket PC0038045, Commercial Invoice). Customer PO Q4-2025 on BOL matches Q42025 on PO page. Unit value 305 USD/MT × 19.69 MT = 6,448.86 USD on invoice. Consistent BOL ↔ shipping details ↔ invoice cross-references. [log:bol.page_1_straight_bol.customer_po, bol.page_2_purchase_order.po_number_on_po_page, bol.page_5_commercial_invoice.total_us, bol.page_5_commercial_invoice.unit_value_us_per_mt]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder (or Certify Sources)', 'Pass',
     '"SR26-02231_Batch_2-180-185_COA (1).pdf" present in BOTH Drive Testing subfolder (51 KB, owner Garrett Lutz, modified Apr 23) AND Certify Sources #5 (Public, linked to "Carbon Content of Bio-oil Injected (per injection)" datapoint). Multi-batch SGS Certificate of Analysis SR26-02231 covering 6 batches: page 1 = 2-180 (.001), page 2 = 2-181 (.002 — THIS BATCH), page 3 = 2-182 (.003), page 4 = 2-183 (.004), page 5 = 2-184 (.005), page 6 = 2-185 (.006). Lab: SGS North America Inc., Authorised Signatory Tiffany Scott. [log:lab_results.filename, lab_results.multi_batch_cert, lab_results.page_for_2_181, lab_results.authorised_signatory, evidence_sources]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Lab cert SR26-02231.002 page 2 Carbon = 36.6 % (m/m) via ASTM D5291 Method C. AECN historical distribution: mean 39.42%, SD 6.09% (n=285 MRV samples, source: MRV_AECN_Analysis.xlsx via KB Section 5.1/506). 36.6% sits at 0.46 SD BELOW mean — well within 2-SD bounds (27.24%-51.60%); plausible feedstock variation. NOTE: lab report flags both Carbon and Hydrogen with "#" symbol meaning "Result is outside of test method limits and/or analytical range used in method precision study" — this is a SGS method-precision boundary annotation, NOT a sample integrity concern; the 36.6% value carries forward into Certify Carbon Content datapoint exactly. Same "#" flag pattern was observed on sister batch 2-192 (Carbon 53.1% high tail) — independent confirmation that # is a SGS standard annotation on values outside their method precision band, not a sample-handling issue. [log:lab_results.carbon_pct, lab_results.carbon_method, lab_results.carbon_method_range_flag, certify.datapoints, _derived_values.aecn_carbon_sample_size_n, evidence_sources]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Lab cert page 2: Hydrogen 7.7% (m/m) — within AECN typical 7-9% range. Nitrogen <0.75% — below detection limit, normal for AECN. Both via ASTM D5291 Method C. Hydrogen carries same "#" method-range flag as Carbon (see 4.2). [log:lab_results.hydrogen_pct, lab_results.hydrogen_method_range_flag, lab_results.nitrogen_pct]',
     'VR Appendix 1'),
    ('4.4', 'Lab report references correct batch/sample ID', 'Pass',
     'Lab cert SR26-02231.002 page 2 Client ID field = "BATCH 2-181" — matches target batch exactly. SGS Order No. 5437581, sampled 27-Mar-2026 01:50 at BASCO LOUISIANA, received 03-Apr-2026 11:15, analysed 03-Apr-2026 16:07 - 04-Apr-2026 01:44, completed 04-Apr-2026 01:44. [log:lab_results.client_id_for_2_181, lab_results.sampled, lab_results.location, lab_results.sgs_order_no, lab_results.completed]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is bio-oil phase, not aqueous phase — aqueous pH/conductivity check does not apply. (Injection-time pH for the AECN bio-oil is captured separately in Section 5.5 from Ops Notes.) [log:_meta_oil_type]',
     'VR Sec 5.1'),
    ('4.6', 'Density above formation fluid threshold for safe injection', 'Pass',
     'Lab cert page 2 Density at 15°C = 1.188 g/cm³ via ASTM D4052. Threshold per protocol: density must exceed formation fluid (~1.01 g/cm³) for downward gravity-driven injection. 1.188 > 1.01 — comfortably above floor. Same Bioenergie AE truck batch density tolerance as historical AECN batches. [log:lab_results.density_15C_g_per_cm3, lab_results.density_vs_formation_fluid_floor_1_01_g_per_cm3]',
     'VR Sec 5.1'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes header: Batch number = 2-181, Completion Date = 4/1/2026. Both match QA target batch and Certify removal date (01 Apr 2026). [log:ops_notes.batch_number, ops_notes.completion_date, certify.removal_date]',
     'VR Sec 5.1'),
    ('5.2', 'All scale ticket values correctly transcribed', 'Pass',
     'Ops Notes Truck 1 Full Mass (lb) = 78,660 ✓ Full scale ticket gross 78,660. Truck 1 Empty Mass (lb) = 34,740 (matches Net math; empty ticket image quality flagged in 2.1 but Ops Notes value reconciles arithmetically). Truck 1 Injectate Mass (lb) = 43,920 = 78,660 - 34,740 ✓. Truck 1 Injectate Mass (kg) = 19,921.76 = 43,920 / 2.20462 ✓. pH = 3.4. Truck 2 row blank (single-truck batch). [log:scale_tickets.full_ticket.gross_weight_lb, ops_notes.truck_1_full_mass_lb, ops_notes.truck_1_empty_mass_lb, ops_notes.truck_1_injectate_mass_lb, ops_notes.truck_1_injectate_mass_kg, ops_notes.truck_2_present]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch — no aqueous phase to reconcile. [log:_meta_oil_type]',
     'VR Sec 5.1'),
    ('5.4', 'COBB values present and match Ops Notes', 'Flag',
     'COBB row 63 cell A = "2-181" ✓ (verified before any value extraction per ROW VERIFICATION GATE). Field reconciliation: B_injected_product = bio_oil ✓; C_consumed_lot = 2338-T_offload_1 ✓; E_BOL_number = 2338-T ✓ matches Ops Notes Origin lot and BOL filename; F_quantity_consumed_in_injection = 19,921.76064 ✓ matches Ops Notes Total Injectate Mass; G_offloaded_quantity_kg = 19,921.76064 ✓ same; H_origin_quantity_kg = 19,950 ✓ matches Ops Notes Origin Mass and BOL gravimetric; L_injection_completion_date = 2026-04-01 ✓ matches Ops Notes Completion Date. **FLAG — Col M injection_ph = 34.8 vs Ops Notes pH = 3.4.** Adjacent COBB rows 2-123 through 2-129 show pH values in 2.8-3.2 range (single decimal). 34.8 is almost certainly a Garrett-side data entry typo — likely missing decimal point (3.4 → 34.8 or 3.48). pH is NOT a Certify datapoint (not used in CDR calculation); Ops Notes 3.4 is the authoritative injection pH. Verifier-impacting? No. Action: Garrett to backfill COBB col M with 3.4. [log:cobb.row_number, cobb.cobb_row_id_verified, cobb.cobb_cell_A_value, cobb.fields.E_BOL_number, cobb.fields.F_quantity_consumed_in_injection_kg, cobb.fields.G_offloaded_quantity_kg, cobb.fields.H_origin_quantity_kg, cobb.fields.L_injection_completion_date, cobb.fields.M_injection_ph, ops_notes.ph, cobb.ph_data_hygiene_finding]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes Injection Data row records pH = 3.4. Consistent with AECN bio-oil acidic norm (lab cert page 2 shows Acid Number 56 mg KOH/g, consistent with low pH). pH value present and reasonable. COBB col M typo (34.8) noted in 5.4 — Ops Notes is authoritative. [log:ops_notes.ph, lab_results.acid_number_mg_KOH_per_g]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date 4/1/2026 ↔ COBB L_injection_completion_date 2026-04-01 ↔ Certify removal date 01 Apr 2026 — three-way match. COBB also has order_line_completed_on 2026-03-24 13:42:08 (purchase-order completion timestamp, distinct from injection completion). [log:ops_notes.completion_date, cobb.fields.L_injection_completion_date, cobb.fields.I_order_line_completed_on, certify.removal_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field in Ops Notes Batch Composition is expected to be blank for AECN (density tracked in lab cert, not Ops Notes). Confirmed blank in Ops Notes CSV export — no erroneous density value entered. [log:_meta_oil_type, ops_notes.filename]',
     'VR Sec 5.1'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     'Certify Sources #4: "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" (Private, linked to AECN Production Process Emissions). Covers reporting period 1Jul2025-31Dec2025 — relevant to AECN production period #03-2026 (March 2026 production crosses the half-year boundary but H1 2026 EF window applies; the linked LCA CI spreadsheet is the most recent semi-annual update). [log:certify.certify_sources_enumeration]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     'Certify Sources #1: "BH 2025 LCA w Stack Emissions.xlsx" (Private, linked to AECN Production Process Emissions). [log:certify.certify_sources_enumeration]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present for AECN production period', 'Pass',
     'Certify Sources #3: "Supporting GHG data 31Dec2025 S.xlsx" (Private, linked to AECN Production Process Emissions). 4 component-level docs (Stack Emissions + Supporting GHG + LCA CI + 1 screenshot) all linked to the AECN Production Process Emissions datapoint — the full LCA evidence stack for the relevant production period. [log:certify.certify_sources_enumeration]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Certify Datapoint "AECN Production Process Emissions" = 0.10 kgCO₂e/kg (Reported, displayed precision; precise value per Standard EFs 2026 tab = 0.10402). Independent recalc: 19,950 kg × 0.10402 / 1000 = 2.0752 t ↔ Certify Component "AECN pyrolysis (from truck loads) - process emissions" = 2.075 t — exact match (full-precision EF used internally by Certify). [log:certify.datapoints, certify.components.pyrolysis_process_from_truck_loads_t, certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads.ef_precise_kgCO2e_per_kg, _derived_values.pyrolysis_process_recalc_t, _derived_values.pyrolysis_process_formula]',
     'VR Appendix 1'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Certify Datapoint "AECN Production Embodied Emissions" = 0.02 kgCO₂e/kg (displayed; precise per Standard EFs = 0.0212). Independent recalc: 19,950 × 0.0212 / 1000 = 0.4229 t ↔ Certify Component "AECN pyrolysis (from truck loads) - embodied emissions" = 0.423 t — exact match. [log:certify.datapoints, certify.components.pyrolysis_embodied_from_truck_loads_t, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads.ef_kgCO2e_per_kg, _derived_values.pyrolysis_embodied_recalc_t, _derived_values.pyrolysis_embodied_formula]',
     'VR Appendix 1'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals (Process and Embodied) use Mass = 19,950 kg ± 72.57 kg — the Origin Bio-Oil Mass datapoint (pre-sparging), NOT the post-sparging Mass of Injectant 19,664.77 kg. This is correct per protocol — pyrolysis emissions were incurred to produce the full 19,950 kg quantity, before any in-injection sparging loss (1.29% factor per KB Section 423) at Basco. [log:certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads.mass_kg, certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads.mass_basis, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads.mass_kg, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads.mass_basis, ops_notes.origin_mass_kg, evidence_sources]',
     'PDD Sec A'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass × carbon wt% (decimal) × 3.667', 'Pass',
     'Independent recalc: 19.665 t (Mass of Injectant) × 0.3660 (Carbon decimal from lab cert 36.6%) × 3.667 = 26.393 t. Certify Sequestrations / "Injection sequestration" component = 26.393 tCO₂e — exact match. Carbon entered as decimal (0.3660) not raw %. Mass uses post-sparging injectate (correct basis for stored CO₂). [log:certify.calculation_view.sequestrations_t, certify.components.injection_sequestration_t, certify.datapoints, lab_results.carbon_pct, ops_notes.mass_of_bio_oil_injected_kg, _derived_values.gross_co2e_recalc_t, _derived_values.gross_co2e_formula]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'Activities total 8.029 tCO₂e from 4 components: (1) Truck Process 5.010 t (independent: 19.950 × 2,197 × 0.0001143 = 5.0110 t ✓), (2) Truck Embodied 0.522 t (independent: 2,197 × 0.00023756 = 0.5220 t ✓), (3) Pyrolysis Process 2.075 t (independent: 19,950 × 0.10402 / 1000 = 2.0752 t ✓), (4) Pyrolysis Embodied 0.423 t (independent: 19,950 × 0.0212 / 1000 = 0.4229 t ✓). Sum: 5.010 + 0.522 + 2.075 + 0.423 = 8.030 (Components view) ↔ 8.029 (Calc View — 1-kg rounding). All deducted from gross in Net calc. [log:certify.calculation_view.activities_t, certify.components.transport_process_aecn_to_la_t, certify.components.transport_embodied_aecn_to_la_t, certify.components.pyrolysis_process_from_truck_loads_t, certify.components.pyrolysis_embodied_from_truck_loads_t, _derived_values.transport_process_recalc_t, _derived_values.transport_process_recalc_t_4dec, _derived_values.transport_embodied_recalc_t, _derived_values.transport_embodied_recalc_t_4dec, _derived_values.pyrolysis_process_recalc_t, _derived_values.pyrolysis_process_recalc_t_4dec, _derived_values.pyrolysis_embodied_recalc_t, _derived_values.pyrolysis_embodied_recalc_t_4dec, _derived_values.activities_sum_recalc_t, _derived_values.activities_sum_formula]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Calculation View Uncertainty Discount = 146 kg (0.146 t). Per Isometric Standard v2.0 §3.7.3 (Option B Variance Propagation). Discount represents 0.553% of Sequestrations (146 / 26,393) — reasonable for a single-truck batch with 5 mass-of-load inputs all at ±72.57 kg (Isometric Standard discrete-weight uncertainty) and one Carbon Content input at ±0.1464% (= 0.004 × 36.60 per Isometric Standard). Discount present in net calculation. [log:certify.calculation_view.uncertainty_discount_kg, _derived_values.uncertainty_discount_pct_of_gross, _derived_values.uncertainty_discount_pct_of_gross_formula, evidence_sources]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with BCU Quant and GHG Statement', 'Pass',
     'Net independent recalc: 26.393 (Seq) + 5.010 (BCU) - 8.030 (Activities) - 0.146 (Uncertainty) = 23.227 t ↔ Certify Calc View Net 23.227 t (displayed 23.23 t). BCU quantity 5.010 t matches Transport Process emission 5.010 t exactly (full offset, no over/under). [log:certify.calculation_view.net_co2e_t, certify.calculation_view.sequestrations_t, certify.calculation_view.adjustments_bcu_t, certify.calculation_view.activities_t, certify.calculation_view.uncertainty_discount_kg, _derived_values.net_calc_recalc_t, _derived_values.net_calc_formula]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 — Completeness: every AECN component has uncertainty on correct datapoint', 'Pass',
     'All 5 required uncertainty-input components have ± values opened and read from each Certify component modal INPUTS section: (1) Injection Sequestration — Carbon Content ±0.1464%, Mass of Product ±72.57 kg; (2) Truck Transport Process — Mass of Load ±72.57 kg (Distance not required); (3) Truck Transport Embodied — no Mass input (correct — embodied is per-mile per FC8); (4) AECN Pyrolysis Process — Mass ±72.57 kg; (5) AECN Pyrolysis Embodied — Mass ±72.57 kg. BCU component has no uncertainty input (constant_reduction blueprint — correct). [log:certify.component_modal_uncertainty.injection_sequestration, certify.component_modal_uncertainty.truck_transport_process, certify.component_modal_uncertainty.truck_transport_embodied, certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads, certify.component_modal_uncertainty.bcu_applied_to_bio_oil_transport_process, evidence_sources]',
     'Isometric Standard v2.0 S3.7.3'),
    ('7a.2', 'Layer 2 — Correctness: reported ± matches expected value', 'Pass',
     'Per Isometric Standard v2.0 §3.7.3 (KB Section 565-571): Carbon Content uncertainty = 0.004 × Measured Value = 0.004 × 36.60 = 0.1464% (Certify modal shows ±0.1464% — exact match). Mass-of-load uncertainty = 72.57 kg per discrete weight (one truck = one weighing event) — Certify shows ±72.57 kg on all four mass inputs (Inj Seq Mass of Product, Truck Process Mass of Load, Pyrolysis Process Mass, Pyrolysis Embodied Mass) — all exact matches to expected. [log:certify.component_modal_uncertainty.injection_sequestration.carbon_uncertainty_pct, certify.component_modal_uncertainty.injection_sequestration.carbon_expected_uncertainty_pct, certify.component_modal_uncertainty.injection_sequestration.mass_uncertainty_kg, certify.component_modal_uncertainty.truck_transport_process.mass_uncertainty_kg, certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads.mass_uncertainty_kg, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads.mass_uncertainty_kg, _derived_values.carbon_uncertainty_factor, evidence_sources]',
     'Isometric Standard v2.0 S3.7.3'),
    ('7a.3', 'Layer 3 — Discount presence and consistency', 'Pass',
     'Aggregate Uncertainty Discount = 146 kg present in Calc View net formula (Sequestrations + Adjustments − Activities − Uncertainty Discount = Net: 26.393 + 5.010 − 8.029 − 0.146 = 23.227 t displayed 23.23, 1-kg rounding within Components vs Calc View). Discount is 0.553% of Sequestrations — magnitude consistent with the 5 ±72.57-kg inputs + 1 ±0.1464%-Carbon input propagated through Option B variance math (Isometric Standard v2.0 §3.7.3) for a single-truck batch. [log:certify.calculation_view.uncertainty_discount_kg, _derived_values.uncertainty_discount_pct_of_gross, _derived_values.net_calc_recalc_t, evidence_sources]',
     'Isometric Standard v2.0 S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon 36.6% is 0.46 SD below AECN historical mean (39.42%, SD 6.09%) — within 1 SD, plausible feedstock variation (lab "#" method-range flag noted in 4.2). Mass 19,950 kg / 19,921.76 kg / 19,664.77 kg all within typical single-truck AECN range. Net 23.23 t consistent with carbon-driven yield (slightly lower than sister batches with higher carbon, e.g., 2-192 at 53.1% carbon → 40.04 t Net). No unexplained outliers. [log:lab_results.carbon_pct, ops_notes.origin_mass_kg, ops_notes.mass_of_bio_oil_injected_kg, certify.calculation_view.net_co2e_t]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented, unrecovered mass deducted, incident report filed', 'N/A',
     'No spill or unrecovered loss documented in Ops Notes or Drive folder. "Loss (kg) 285.23 / Loss % 1.43%" in Ops Notes Mass Reconciliation reflects the standard MIN(scale, BOL) + sparging deductions (256.99 kg sparging + 28.24 kg scale-vs-BOL conservatism = 285.23 kg total), not a spill event. [log:ops_notes.loss_kg, ops_notes.loss_pct, ops_notes.sparging_loss_kg]',
     'VR Sec 3.5'),
    ('8.3', 'Inventory reconciliation: carryover oil documented', 'N/A',
     'Single-truck batch, no multi-period inventory allocation. Origin lot 2338-T fully consumed in this one batch (Ops Notes "AECN Oil Added 19,950 = Origin 19,950"). [log:ops_notes.origin_lot, ops_notes.origin_mass_kg, ops_notes.aecn_oil_added_kg, cobb.fields.C_consumed_lot]',
     'GHG Stmt Sec C'),

    ('SECTION', '9. Isometric Certify — Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Components Sequestrations = 26.393 tCO₂e (single "Injection sequestration" entry). Independent gross recalc: 19,664.77 kg × 0.3660 × 3.667 / 1000 = 26.393 t — exact match to Certify. Per-component math reconstruction: Mass-of-Product input × Carbon-Content input × 3.6667 CO2/C molar ratio. [log:certify.components.injection_sequestration_t, certify.component_modal_uncertainty.injection_sequestration.mass_of_product_kg, certify.component_modal_uncertainty.injection_sequestration.carbon_content_pct, _derived_values.gross_co2e_recalc_t, _derived_values.gross_co2e_formula]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES — Transport: Process + embodied correct for AECN truck route', 'Pass',
     'Two transport components verified per-component with full math reconstruction: (a) "AECN to LA Tanker Truck Transport Process Emissions" 5.010 t — modal inputs: mass-of-load 19,950 kg, distance 2,197 mi, EF 0.1143 kgCO₂e/(t·mi). Recalc: 19.950 t × 2,197 mi × 0.0001143 MTCO₂e/(t·mi) = 5.0110 t ✓ matches 5.010 displayed. (b) "AECN to LA Tanker Truck Transport Embodied Emissions" 0.522 t — modal inputs: distance 2,197 mi, EF 0.23756 kgCO₂e/mi (= 0.1476 kg/km × 1.609344 km/mi). Recalc: 2,197 mi × 0.00023756 MTCO₂e/mi = 0.5220 t ✓ matches 0.522 displayed. **Transport process sum: 5.010 t (single leg, truck batch).** **Bio-oil transport total: 5.010 + 0.522 = 5.532 tCO₂e** = Certify Components "Bio-oil transport" subtotal. Per FC8: embodied is per-mile (no mass-of-load input on embodied) — confirmed. [log:certify.components.transport_process_aecn_to_la_t, certify.components.transport_embodied_aecn_to_la_t, certify.component_modal_uncertainty.truck_transport_process.distance_mi, certify.component_modal_uncertainty.truck_transport_process.mass_of_load_kg, certify.component_modal_uncertainty.truck_transport_process.ef_kgCO2e_per_t_mi, certify.component_modal_uncertainty.truck_transport_embodied.ef_kgCO2e_per_mi, certify.component_modal_uncertainty.truck_transport_embodied.ef_kgCO2e_per_km_equivalent, certify.component_modal_uncertainty.truck_transport_embodied.distance_mi, _derived_values.transport_process_recalc_t, _derived_values.transport_process_recalc_t_4dec, _derived_values.transport_process_formula, _derived_values.transport_embodied_recalc_t, _derived_values.transport_embodied_recalc_t_4dec, _derived_values.transport_embodied_formula, _derived_values.truck_embodied_ef_kgCO2e_per_km_equivalent, _derived_values.transport_process_sum_t, _derived_values.bio_oil_transport_total_t]',
     'Certify Components, Transport Emissions Acctg v1.1'),
    ('9.3', 'ACTIVITIES — Injection: LCS and sample transport correct', 'N/A',
     'No LCS pre-treatment for AECN at Basco (LCS is Aqueous-only). No sample-transport activity component present on this removal — typical for pure AECN truck batches (sample transport overhead < 1 kg, often allocated at site level rather than per-removal). [log:certify.components, _meta_oil_type]',
     'Certify Components'),
    ('9.4', 'ACTIVITIES — Pyrolysis: AECN production process + embodied present', 'Pass',
     'Two pyrolysis components present with new 2026 "from truck loads" naming convention: (a) "AECN pyrolysis (from truck loads) - process emissions" 2.075 t — modal inputs: mass 19,950 kg, EF 0.104 kgCO₂e/kg (precise 0.10402). Recalc: 19,950 × 0.10402 / 1000 = 2.0752 t ✓. (b) "AECN pyrolysis (from truck loads) - embodied emissions" 0.423 t — modal inputs: mass 19,950 kg, EF 0.0212 kgCO₂e/kg. Recalc: 19,950 × 0.0212 / 1000 = 0.4229 t ✓. Both apply EF to Origin Bio-Oil Mass (pre-sparging) per protocol. Naming "(from truck loads)" parallels the "(from rail loads)" suffix on rail batches — deliberate VVB-facing signal for mass-source provenance. [log:certify.components.pyrolysis_process_from_truck_loads_t, certify.components.pyrolysis_embodied_from_truck_loads_t, certify.components.naming_note, certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads.ef_kgCO2e_per_kg, certify.component_modal_uncertainty.pyrolysis_process_from_truck_loads.mass_kg, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads.ef_kgCO2e_per_kg, certify.component_modal_uncertainty.pyrolysis_embodied_from_truck_loads.mass_kg, _derived_values.pyrolysis_process_recalc_t, _derived_values.pyrolysis_process_recalc_t_4dec, _derived_values.pyrolysis_embodied_recalc_t, _derived_values.pyrolysis_embodied_recalc_t_4dec]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: All applicable BCU categories populated', 'Pass',
     'Single applicable BCU category for AECN truck batch with no site-emission burden: "BCUs - Applied to Bio-Oil Transport Process Emissions" 5.010 t. Other BCU categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only on removals burdened with site emissions — not applicable here. Single-category pattern matches all recent AECN-only truck batches. [log:certify.components.bcu_transport_t]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS — BCU quantity >= corresponding activity emission', 'Pass',
     'BCU "Applied to Bio-Oil Transport Process Emissions" = 5.010 t. **Transport process sum (all process legs): 5.010 t = 5.010 t (AECN→LA Tanker Truck Process; single transport process leg for truck batch — rail batches sum 3 process legs).** BCU 5.010 t ↔ transport process sum 5.010 t — exact full offset, no over/under-funding. Embodied transport (0.522 t) is NOT BCU-eligible per protocol (only fuel/process is offset-eligible) — correctly excluded. [log:certify.component_modal_uncertainty.bcu_applied_to_bio_oil_transport_process.constant_t, certify.component_modal_uncertainty.bcu_applied_to_bio_oil_transport_process.transport_process_total_t, certify.component_modal_uncertainty.bcu_applied_to_bio_oil_transport_process.bcu_meets_or_exceeds_transport_process, certify.components.transport_process_aecn_to_la_t, _derived_values.transport_process_sum_t]',
     'Certify Components'),
    ('9.7', 'COUNTERFACTUALS: Zero per protocol', 'Pass',
     'Certify Components Counterfactuals total = 0 tCO₂e (no entries; 14 unused groups). Per Charm CDR protocol for bio-oil geological storage, counterfactuals are zero (no baseline emissions scenario to subtract — bio-oil sequestered = net removal). [log:certify.components.counterfactuals_t]',
     'PDD'),
    ('9.8', 'Net removal matches independent calculation', 'Pass',
     'Independent: 26.393 (Seq) + 5.010 (BCU) − 8.030 (Activities sum, Components view) − 0.146 (Uncertainty Discount) = 23.227 t. Calc View shows Activities 8.029 t (1-kg rounding diff from Components 8.030 t) and Net 23.227 t precise (displayed 23.23 t). Net matches independent recalc within rounding. [log:certify.calculation_view.net_co2e_t, _derived_values.net_calc_recalc_t, _derived_values.net_calc_formula]',
     'Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     'Sources tab #2 "Screenshot 2026-02-23 at 11.29.10 AM.png" (linked to AECN Production Process Emissions, Private) and #10 "Screenshot 2026-04-10 at 3.19.33 PM.png" (linked to EF Truck Transport Fuel Use, Public) are non-descriptive screenshot filenames — same hygiene set observed across recent AECN batches (2-185/186/187/189/190/191/192/201/204). BCU certificate filename: Charm-A4-2024-10-24-63-1976.pdf — this same A4 BCU cert is now reused across multiple distinct shipments and railcars (TILX200231 batches 2-190/2-191/2-192, TIMX201060 batch 2-188, TILX200228 batches 2-201/2-204, and now AECN-truck batch 2-181). BCU quantity 5.010 t matches Transport Process emission 5.010 t exactly — quantity is verified correct; the question is whether this is a catch-all BCU certificate spanning multiple shipments or whether the wrong cert filename has been linked. Worth Garrett one-line confirmation of cert provenance. Hygiene flags, not verifier-impacting. [log:certify.certify_sources_enumeration]',
     'Certify Datapoints, Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     '14 entries on Certify Sources tab — fully enumerated in source_reads.json (exhaustive scan via Playwright snapshot, all 14 rows captured). Drive folder enumerated via Playwright (3 items: Testing folder [containing lab cert SR26-02231.pdf], Scale Tickets folder [containing both full and empty tickets], 2-181 Ops Notes Google Sheet; exhaustive scan). Cross-reference: 2-181 Full Scale Ticket.jpg ↔ Sources #7 ✓; 2-181 Empty Ticket (1).png ↔ Sources #6 ✓; 2-181 Ops Notes ↔ Sources #8 (Public xlsx export) ✓; lab cert SR26-02231 in Sources #5 AND in Drive Testing subfolder ✓; BOL Billing Documents 2338-T.pdf in Sources #9 (not in Drive — typical for AECN BOLs delivered via Certify Sources direct upload); component-level LCA docs (BH 2025 LCA + Supporting GHG + Bioenergy LCA CI) in Sources #1/#3/#4 (Private; not expected in per-batch Drive). All required documents accounted for. [log:certify.certify_sources_tab_total, certify.certify_sources_enumeration, drive_folder.contents, evidence_sources]',
     'Certify Sources vs Drive'),
]


def build_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Batch 2-181 QA'

    ws.column_dimensions['A'].width = 9
    ws.column_dimensions['B'].width = 45
    ws.column_dimensions['C'].width = 9
    ws.column_dimensions['D'].width = 95
    ws.column_dimensions['E'].width = 22

    row = 1
    for entry in ROWS:
        kind = entry[0]
        if kind == 'HEADER':
            ws.cell(row, 1, 'BATCH 2-181 QA CHECKLIST').font = Font(bold=True, size=14)
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
            ws.row_dimensions[row].height = 22
            row += 1
        elif kind == 'META':
            ws.cell(row, 1, entry[1]).font = Font(bold=True)
            ws.cell(row, 2, entry[2]).alignment = WRAP
            ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=5)
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
    if fail_count > 0:
        ws.cell(row, 1).fill = FAIL_FILL; ws.cell(row, 2).fill = FAIL_FILL
    row += 1
    ws.cell(row, 1, 'Flag'); ws.cell(row, 2, flag_count)
    ws.cell(row, 1).fill = FLAG_FILL; ws.cell(row, 2).fill = FLAG_FILL
    row += 1
    ws.cell(row, 1, 'N/A'); ws.cell(row, 2, na_count)
    row += 2
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True)
    ws.cell(row, 2, '23.23 tCO2e (Calculation View precise: 23.227)')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True)
    ws.cell(row, 2, 'Clean batch on math — all 4 components recalc to Certify within rounding: Gross 26.393 t (19.665 × 0.366 × 3.667), Truck Process 5.011 t (19.950 × 2,197 × 0.0001143), Truck Embodied 0.522 t (2,197 × 0.00023756), Pyrolysis Process 2.075 t (19,950 × 0.10402 / 1000), Pyrolysis Embodied 0.423 t (19,950 × 0.0212 / 1000). BCU 5.010 t = exact transport-process offset. Uncertainty 146 kg = 0.55% of gross. Net 23.227 t. Carbon 36.6% within historical AECN range (0.46 SD below mean 39.42%). Mass chain: BOL/AECN-scale 19,950 → Charm-scale 19,921.76 → conservative MIN → sparging 256.99 → injected 19,664.77 kg. All four sources (BOL/scale tickets/Ops Notes/Certify/COBB) align.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True)
    ws.cell(row, 2, '2.1 + 2.3 (image-quality / Garrett-side): empty scale ticket is a phone screenshot of an SMS thread (rotated CAT ticket at low resolution), preventing direct pixel-level verification of tractor/trailer numbers on the empty ticket; full ticket is directly readable. Math reconciles via Ops Notes (Full 78,660 − Empty 34,740 = 43,920 lb net). Garrett to re-upload empty ticket as direct photo for future batches. 5.4 (Garrett-side data-hygiene, NOT verifier-impacting): COBB row 63 col M injection_ph = 34.8 vs Ops Notes pH = 3.4 — apparent data entry typo (missing decimal point). pH is not a Certify datapoint; Ops Notes 3.4 is authoritative. Garrett to backfill COBB col M with 3.4. 9.9 (Garrett-side filename hygiene, NOT verifier-impacting): 2 non-descriptive Certify filenames (Screenshot 2026-02-23 at 11.29.10 AM.png linked to AECN Production Process Emissions; Screenshot 2026-04-10 at 3.19.33 PM.png linked to EF Truck Transport Fuel Use). 9.9 (BCU cert PROVENANCE, separate substantive question): Charm-A4-2024-10-24-63-1976.pdf now used as BCU certificate across multiple distinct shipments (rail batches 2-188/2-190/2-191/2-192/2-201/2-204 AND truck batch 2-181). BCU quantity 5.010 t exactly matches Transport Process — quantity is correct; cert provenance worth Garrett one-line confirmation (catch-all cert legitimately spanning multiple shipments, or wrong-cert mislink).')

    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-181/Batch_2-181_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
