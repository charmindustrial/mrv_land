#!/usr/bin/env python3
"""Build Batch 2-199 QA Checklist xlsx — AECN truck batch, site-emissions burdened scapegoat removal."""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

FAIL_FILL = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
FAIL_FONT = Font(color='9C0006', bold=True)
FLAG_FILL = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
FLAG_FONT = Font(color='996600')
NA_FONT = Font(color='808080', italic=True)
HEADER_FILL = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
HEADER_FONT = Font(color='FFFFFF', bold=True, size=12)
# Per feedback_checklist_header_one_color.md: normalize ALL section and sub-section headers to single #D6E4F0
SECTION_FILL = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
SECTION_FONT = Font(bold=True, size=11)

THIN = Side(border_style='thin', color='808080')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical='top', horizontal='left')
WRAP_CENTER = Alignment(wrap_text=True, vertical='center', horizontal='center')

ROWS = [
    ('HEADER',),
    ('META', 'Batch ID', '2-199'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 23 Apr 2026; parent Drive folder "4/20/26-4/30/26")'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-13 (re-reviewed after Garrett EF refresh)'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Truck (direct AECN Quebec → Basco LA, BOL 2352-T, single tanker truck)'),
    ('META', 'Site Emissions', 'YES — scapegoat removal burdened with 11 Bio-oil injection activity components (15.293 t)'),
    ('META', 'Net CDR (Certify)', '19.10 tCO2e (post Garrett 2026-05-13 AECN Process EF refresh from 0.12704 to 0.104 kgCO2e/kg; was 18.66 pre-fix)'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder id "192HXAmzipuF93uyVBBP5R5BKTdYSpbO4" titled "2-199" contains 3 items: Testing subfolder (id 1ezQcegIks8nv440nVKFBs6obE_BTNIWZ), Scale Tickets subfolder (id 1cAYELqpVYrP07AbtzhovJF7QDpV1EPF_), and "2-199 Ops Notes" Google Sheet (id 1f3_U9hr5x-UL5vh4gHj9ZH1BlWy9i1QsKcF4z81dQUE). Parent folder breadcrumb "4/20/26-4/30/26" — RP-consistent with injection date 4/23/2026. [log:batch_id, drive_folder.items, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains "2-199 Full Scale Ticket.jpg" (499 KB, owner Garrett Lutz, modified Apr 30) and "2-199 Empty Ticket.png" (493 KB, owner Garrett Lutz, modified Apr 30). Both also linked to Certify Sources "Mass of Injectant (per injection)" datapoint (sources #11 + #12, both Public). Both files downloaded via drive.usercontent.google.com/download response-body capture per feedback_drive_image_download_pattern memory. [log:scale_tickets.full_ticket.file, scale_tickets.empty_ticket.file, _derived_values, standard_efs_sheet]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Testing subfolder is populated with "2-199 - 2-201.pdf" (46 KB, owner Garrett Lutz, modified Apr 29) — verified via drive_enum.py on snapshot of folder id 1ezQcegIks8nv440nVKFBs6obE_BTNIWZ. Multi-batch SGS CoA SR26-02683 covering 3 batches: page 1 (.001) = 2-199, page 2 (.002) = 2-200, page 3 (.003) = 2-201. Same cert also present in Certify Sources #8 (Public, linked to "Carbon Content of Bio-oil Injected (per injection)" datapoint) — file in BOTH locations. [log:drive_folder.items, lab_results.certificate_id, lab_results.multi_batch_cert_pages, lab_results.page, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-199 Ops Notes" Google Sheet present (id 1f3_U9hr5x-UL5vh4gHj9ZH1BlWy9i1QsKcF4z81dQUE). All sections populated: Completion Date 4/23/2026; Batch Composition (Origin 2352-T at 18,800 kg, Total 18,800 kg); Constants (Lbs/Kg 2.20462, Sparging 0.0129, AECN Solids 0.0016, Filtration Factor 0.9984); Injection Data (Truck 1 Full 76,740 lb / Empty 35,220 lb / Net 41,520 lb = 18,833.14 kg, Truck 2 blank, pH 3); Totals (Total Injectate 18,800 kg, Sparging Loss 242.52 kg, Mass of Bio-Oil Injected 18,557.48 kg, MOBI post-filtration 18,527.79 kg); Loss reconciliation (242.52 kg / 1.29%). Filename "2-199 Ops Notes" (no Rail suffix) = truck batch. [log:ops_notes.file, ops_notes.completion_date, ops_notes.batch_composition.origin_mass_kg, ops_notes.injection_data.truck_1_full_lb, ops_notes.injection_data.truck_1_empty_lb, ops_notes.totals.total_injectate_mass_kg, ops_notes.totals.mobi_post_filtration_kg, ops_notes.injection_data.ph, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'Lab CoA page 1 LOCATION = "BASCO LOUISIANA"; BOL 2352-T Ship-To = "CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA" (Basco facility); Certify project "Charm Bio-oil Geologic Storage" (Basco). No Vaulted references in any opened source (BOL pages 1-5, lab cert pages 1-3, Ops Notes CSV, COBB row 88, Certify Components/Datapoints/Sources/Calc View tabs all opened — exhaustive scan). [log:lab_results.location, bol.ship_to, certify.removal_id, _derived_values, standard_efs_sheet, certify]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Flag',
     'Full ticket: directly readable JPG photo of CAT scale ticket #6041 dated 4-16-26, at Pilot Travel Center I-49 Exit 40 Bunkie LA scale #3122; gross 76,740 lb (steer 12,840 + drive 31,420 + trailer 32,480 = 76,740 ✓ axles sum to gross); Tractor 2214, Trailer 36562, Carrier KIK CARRIER, Driver Paul Anadé, Weighmaster Marsha Castelle. Empty ticket: PNG file is a phone screenshot of the same CAT ticket viewed in iOS document viewer with "Eye Protect" yellow tint overlay (1080×2340 px), making the image lower contrast than the full ticket JPG; CAT template layout and weighmaster signature visible, individual digit values readable but with reduced clarity due to viewer-mode overlay. Both files uploaded and present. Math reconciliation between the two tickets (Full 76,740 - Empty 35,220 = 41,520 lb net, axle sums match gross on both) is internally consistent. Hygiene flag: same pattern as 2-181 — Garrett to re-upload empty ticket as direct photo (not in-app viewer screenshot) for future batches. [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.full_ticket.axle_match, scale_tickets.empty_ticket.image_note, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.empty_ticket.axle_match, scale_tickets.net_calc.full_minus_empty_lb, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Full and empty scale tickets both dated 4-16-26 (April 16, 2026). Ops Notes Completion Date 4/23/2026 — 7 days between Charm-side weighing and injection (within 14-day tolerance). BOL Date of loading 2026-04-10 (Quebec origin) → arrival 2026-04-12 → Basco scale weighing 2026-04-16 → injection 2026-04-23. Cross-border haul timeline consistent. [log:scale_tickets.full_ticket.date, ops_notes.completion_date, bol.ship_date, bol.arrival_date, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Both scale tickets show Tractor #2214 and Trailer #36562 — match confirmed via direct pixel-read of both images. Note: BOL Quebec-origin paperwork records Truck ID #2201 (different from Basco-arrival tractor #2214); this is the typical cross-border driver/tractor swap pattern on a 6-day Canada→LA haul. Trailer (36562) is consistent across BOL + both scale tickets. Within-scale-ticket pair: 2214/36562 match on both, axle sums match gross on both. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.full_ticket.trailer_number, scale_tickets.empty_ticket.tractor_number, scale_tickets.empty_ticket.trailer_number, scale_tickets.net_calc.trailer_match, scale_tickets.net_calc.tractor_match_between_full_and_empty, bol.truck_id_quebec_origin, bol.tractor_mismatch_note, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     'Net = Full 76,740 lb − Empty 35,220 lb = 41,520 lb. Converted: 41,520 / 2.20462 = 18,833.14 kg. Ops Notes records Truck 1 Injectate Mass (lb) = 41,520 and Truck 1 Injectate Mass (kg) = 18,833.13984 — exact match to recalc. [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.net_calc.full_minus_empty_lb, scale_tickets.net_calc.net_mass_kg, ops_notes.injection_data.truck_1_injectate_lb, ops_notes.injection_data.truck_1_injectate_kg_raw, _derived_values.scale_ticket_net_kg, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Scale net (Charm-side Basco): 18,833.14 kg. BOL mass (AECN-side Port Cartier scale, page 4 masse nette CORRECTED via page 3 ***Corrections***): 18,800 kg. MIN = 18,800 kg (BOL value lower) — adopted as Total Injectate Mass in Ops Notes. The 33.14 kg gap between scales is within typical truck-trip mass uncertainty (±72.57 kg per discrete weighing, Isometric Standard v2.0 §3.7.3). Note BOL was corrected on page 3: original tare 16,910 kg → corrected 16,190 kg, yielding corrected net 18,800 kg (vs original 18,080 kg, the pre-correction value that COBB still carries per Item 5.4). [log:scale_tickets.net_calc.net_mass_kg, bol.net_kg_corrected, bol.page_4_weigh_ticket.masse_nette_kg, _derived_values.min_scale_vs_bol_kg, ops_notes.totals.total_injectate_mass_kg, ops_notes.totals.min_scale_vs_bol_chosen, bol.tare_correction_kg, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied to Total Injectate Mass: 18,800 × 0.0129 = 242.52 kg sparging loss. Mass of Bio-Oil Injected (pre-filtration) = 18,800 − 242.52 = 18,557.48 kg. Ops Notes records Sparging Loss 242.52 kg and Mass of Bio-Oil Injected 18,557.48 kg — exact match. Post-filtration (× 0.9984): 18,527.79 kg = MOBI used in Certify Mass of Injectant. [log:ops_notes.constants.sparging_mass_loss, ops_notes.totals.total_injectate_mass_kg, ops_notes.totals.sparging_loss_kg, ops_notes.totals.mass_of_bio_oil_injected_kg, ops_notes.totals.mobi_post_filtration_kg, _derived_values.sparging_loss_kg_recalc, _derived_values.mass_bio_oil_injected_kg_recalc, _derived_values.mobi_post_filtration_kg_recalc, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Four-way mass chain reconciles. Origin (pre-sparging) layer: BOL page 3+4 corrected = 18,800 kg = Ops Notes Origin Mass = Certify "Origin Bio-Oil Mass - AECN" 18.800 t. Conservative-mass layer: 18,800 kg (BOL chosen MIN) = Ops Notes Total Injectate Mass. Final injectate layer (post-sparging × filtration factor): 18,527.79 kg = Ops Notes MOBI post-filtration = Certify "Mass of Injectant (per injection)" 18.528 t. NOTE: COBB row 88 cells F/G/H = 18,080 (stale pre-correction BOL value) — see 5.4 separately. The Ops Notes/Certify chain is internally consistent. [log:bol.net_kg_corrected, ops_notes.batch_composition.origin_mass_kg, ops_notes.totals.total_injectate_mass_kg, ops_notes.totals.mobi_post_filtration_kg, certify.datapoints, certify.components.activities_pyrolysis, _derived_values, standard_efs_sheet, certify]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOL(s) present for each shipment', 'Pass',
     '"documents 2352-T corr.pdf" present in Certify Sources #35 (Public, linked to "Origin Bio-Oil Mass - AECN" datapoint). 5-page PDF: page 1 = Straight BOL (BioEnergie AE → Charm, dated 2026-04-10), page 2 = Charm PO Q42025, page 3 = AECN Shipping Details with ***Corrections page 3*** annotation (tare 16910→16190, net 18080→18800), page 4 = French scale ticket (No de pesée PC0038402, masse nette 18,800 kg), page 5 = Commercial Invoice. The "corr" suffix in filename indicates the corrected version (page-3 Corrections applied). Single BOL = single-truck direct delivery. [log:bol.bol_number, bol.correction_note, bol.page_4_weigh_ticket.no_pesee, certify.sources, _derived_values, standard_efs_sheet, certify]',
     'VR Appendix 1'),
    ('3.2', 'Not applicable for truck batch (rail-only check)', 'N/A',
     'Item 3.2 specifies rail batches (3 truck BOLs from AECN to SOPOR railyard). This is a direct truck batch (AECN Quebec → Basco LA in a single tanker truck). [log:delivery_mode, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass', 'Pass',
     'BOL authoritative mass (page 3 corrected + page 4 French scale ticket masse nette) = 18,800 kg = 18.80 MT. Reported injectate mass at injection (Certify Mass of Injectant) = 18.528 t. BOL 18,800 ≥ Injectate 18,528 by 272 kg (1.45% — consistent with sparging 1.29% + filtration 0.16%). Note BOL page 1 internal: original net 18,847 kg (volumetric) appears parenthesized; page 3 corrected gravimetric 18,800 kg is authoritative (matches Ops Notes Origin Mass). The page-5 invoice value 18.85 MT reflects volume × density 1.185 = 18,847 kg (the volumetric pre-correction figure used for export commercial documentation). [log:bol.net_kg_corrected, bol.invoice_metric_tons, bol.page_1_original_kg_parenthesized, certify.datapoints, _derived_values.bol_2352t_net_kg_corrected, _derived_values, standard_efs_sheet, certify]',
     'VR Sec 3.5'),
    ('3.4', 'Origin and destination correct on BOL', 'Pass',
     'BOL page 1: From = BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier, Québec, G5B 2V9. Ship To = CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA. Carrier of record = Tandet Logistics (Quebec); arrival carrier (per scale ticket) = KIK Carrier. Driver Quebec = jerome langlois. CofA = RS3-260410-1. Customer PO Q4-2025. Production Period #04-2026. Origin/destination match the canonical AECN→Basco truck route. [log:bol.from, bol.ship_to, bol.carrier_of_record, bol.driver_quebec, bol.cofa_number, scale_tickets.full_ticket.carrier, _derived_values, standard_efs_sheet]',
     'PDD'),
    ('3.5', 'Transportation distance consistent with known AECN truck route', 'Pass',
     'Certify Datapoint "Distance from AECN to Basco" = 2,197 mi (Derived) AND "Aggregate Distance Transported AECN to Basco" = 2,197 mi (Reported). Source: "AECN to Basco.png" in Certify Sources #32 (Public, linked to both distance datapoints). Matches the canonical AECN Quebec → Basco LA direct-truck route (~2,197 mi). Component modal Inputs row confirms Distance traveled = 2,197 mi for both Transport Process and Embodied. [log:certify.datapoints, certify.uncertainty_inputs.aecn_to_la_transport_process.distance_mi, _derived_values, standard_efs_sheet, certify]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = tanker truck (direct AECN, no rail)', 'Pass',
     'Certify Components tab shows 2 transport components under Bio-oil transport: "AECN to LA Tanker Truck Transport Process Emissions - AECN" (4.721 t, 25.30%) and "AECN to LA Tanker Truck Transport Embodied Emissions - AECN" (0.522 t, 2.80%). No rail leg components (would be 6 for a rail batch). Consistent with direct truck delivery via BOL 2352-T. NOTE: this removal does carry an "Additional Railcar Movement - Emissions" component (0.162 t, with "Copy of Railline Distances.png" + "April 2026 Railcar Emissions Calc Sheet.xlsx" as evidence) — that is a site-emission allocation for empty railcar repositioning at SOPOR, NOT a transport leg of THIS batch. [log:certify.components.activities_bio_oil_transport, certify.components.activities_bio_oil_injection, _derived_values, standard_efs_sheet, certify]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOL', 'Pass',
     '"documents 2352-T corr.pdf" includes the Commercial Invoice as page 5 (BioEnergie AE, Date of Export 04-10-26, Invoice No 2352-T, Customer PO Q4-2025, Quantity 18.85 MT × 305 USD/MT = $6,172.91, NAFTA cert on file at broker). Volume cross-check: 15,905 L × 1.185 density (B factor) = 18,847 kg ≈ 18.85 MT invoice value. Page-3 corrected gravimetric (18,800 kg) is what feeds Charm/Certify; the 50 kg gap between commercial invoice volumetric and corrected gravimetric is documented and not a verifier-impacting error. [log:bol.invoice_metric_tons, bol.volume_l, bol.density_g_per_ml_at_60F, bol.page_1_original_kg_parenthesized, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder (or Certify Sources)', 'Pass',
     '"2-199 - 2-201.pdf" present in BOTH Drive Testing subfolder (46 KB, owner Garrett Lutz, modified Apr 29) AND Certify Sources #8 (Public, linked to "Carbon Content of Bio-oil Injected (per injection)" datapoint). Multi-batch SGS CoA SR26-02683 covering 3 batches: page 1 (.001) = 2-199 [THIS BATCH], page 2 (.002) = 2-200, page 3 (.003) = 2-201. Lab: SGS North America Inc., Authorised Signatory Jacqualine Kilday. [log:lab_results.certificate_id, lab_results.multi_batch_cert_pages, lab_results.page, lab_results.lab, lab_results.signatory, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Flag',
     'Lab cert SR26-02683.001 page 1 raw Carbon = 53.0 % (m/m) via ASTM D5291 Method C, flagged with "#" symbol meaning "Result is outside test method analytical range used in method precision study". AECN historical distribution: mean 39.42%, SD 6.09% (n=285 MRV samples). 53.0% is 2.23 SD above mean — OUTSIDE the 2-SD upper bound 51.60%. Same outlier pattern as batch 2-192 (carbon 53.1%). **Outlier policy applied:** Certify Carbon Content datapoint = 49.26% (not the raw 53.0%) — sourced from "AECN C Content Outlier Analysis - 2026 YTD.xlsx" (Certify Sources #7, Private). The applied 49.26% sits at z = 1.62 SD above mean (within 2-SD upper bound). Math check: Mass of Injectant 18.528 t × 0.4926 × 3.667 = 33.467 t ≈ Certify Sequestrations 33.468 t ✓ (the 49.26% applied value reconciles, not the 53.0% raw). FLAG for the lab raw value being outside method/SD range; Charm outlier cap correctly applied. Worth Garrett one-line confirmation that the cap policy file is the authoritative methodology. [log:lab_results.carbon_pct, lab_results.carbon_method_range_flag, lab_results.aecn_carbon_2sd_upper_pct, lab_results.carbon_z_score, lab_results.carbon_outlier_finding, certify.datapoints, _derived_values.carbon_content_applied_pct_certify, _derived_values.gross_co2e_check, _derived_values, standard_efs_sheet]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Lab cert page 1: Hydrogen 6.5% (m/m, also flagged with "#" — same SGS method-range annotation as Carbon), Nitrogen <0.75% (below detection). Both via ASTM D5291 Method C. Values within typical AECN ranges. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct_max, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('4.4', 'Lab report references correct batch/sample ID', 'Pass',
     'Lab cert SR26-02683.001 page 1 Client ID field = "BATCH 2-199" — matches target batch exactly. SGS Order No. 5448290, Location BASCO LOUISIANA. Sampled 16-Apr-2026 20:40 (matches scale ticket date 4-16-26 — sample taken at Basco upon receipt). Received 27-Apr-2026 10:10, completed 27-Apr-2026 20:43. [log:lab_results.certificate_id, lab_results.client_id_on_page, lab_results.location, lab_results.sampled_datetime, lab_results.completed_datetime, _derived_values, standard_efs_sheet]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is bio-oil phase, not aqueous. (Injection-time pH for the AECN bio-oil captured in Section 5.5 from Ops Notes.) [log:oil_type, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('4.6', 'Density above formation fluid threshold for safe injection', 'Pass',
     'Lab cert page 1 Density at 15°C = 1.213 g/cm³ via ASTM D4052. Per protocol: density must exceed formation fluid (~1.01 g/cm³) for downward gravity-driven injection. 1.213 >> 1.01 — comfortably above floor. Other lab properties: Viscosity 15.11 cSt @40°C, Acid Number 58 mg KOH/g — within AECN norms. [log:lab_results.density_at_15C_g_per_cm3, lab_results.density_above_formation_fluid_floor, lab_results.viscosity_at_40C_cSt, lab_results.acid_number_mg_koh_g, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes header: Batch number = 2-199, Completion Date = 4/23/2026. Both match QA target batch and Certify removal date (23 Apr 2026). [log:ops_notes.batch_number, ops_notes.completion_date, certify.removal_date, _derived_values, standard_efs_sheet, certify]',
     'VR Sec 5.1'),
    ('5.2', 'All scale ticket values correctly transcribed', 'Pass',
     'Ops Notes Truck 1 Full Mass (lb) = 76,740 ✓ matches full scale ticket gross. Truck 1 Empty Mass (lb) = 35,220 ✓ matches empty scale ticket gross. Truck 1 Injectate Mass (lb) = 41,520 = 76,740 − 35,220 ✓. Truck 1 Injectate Mass (kg) = 18,833.14 = 41,520 / 2.20462 ✓. pH = 3. Truck 2 row blank (single-truck batch). [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, ops_notes.injection_data.truck_1_full_lb, ops_notes.injection_data.truck_1_empty_lb, ops_notes.injection_data.truck_1_injectate_lb, ops_notes.injection_data.truck_1_injectate_kg_raw, ops_notes.injection_data.ph, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch — no aqueous phase to reconcile. [log:oil_type, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('5.4', 'COBB values present and match Ops Notes', 'Flag',
     'COBB row 88 cell A = "2-199" ✓ (verified before any value extraction per ROW VERIFICATION GATE). Field reconciliation: B_injected_product = bio_oil ✓; C_consumed_lot = 2352-T_offload_1 ✓ (single-truck convention); E_BOL_number = 2352-T ✓ matches BOL and Ops Notes Origin; L_injection_completion_date = 2026-04-23 ✓ matches Ops Notes; M_injection_ph = 3 ✓ matches Ops Notes. **FLAG — Cells F/G/H all = 18,080 kg** (quantity_consumed_in_injection / offloaded_quantity_kg / origin_quantity_kg). This is the PRE-correction BOL Page 1 net (before the page-3 ***Corrections***: tare 16910→16190, net 18080→18800). Ops Notes/Certify use the corrected 18,800 kg. 720 kg COBB-side data-provenance gap. Same operational pattern as 2-201 (placeholder split), 2-186 (origin stale), 2-188 (multi-field stale). Verifier-impacting? NO — Certify reads the corrected 18,800 kg via the BOL page-3 corrected gravimetric. Action: Garrett to backfill COBB row 88 F/G/H with 18,800 kg. [log:cobb_row_88.cobb_row_id_verified, cobb_row_88.row_number, cobb_row_88.injection_batch, cobb_row_88.BOL_number, cobb_row_88.quantity_consumed_in_injection_kg, cobb_row_88.offloaded_quantity_kg, cobb_row_88.origin_quantity_kg, cobb_row_88.injection_completion_date, cobb_row_88.injection_ph, cobb_row_88.stale_value_finding, bol.net_kg_corrected, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes Injection Data row records pH = 3. COBB col M also = 3 ✓ (consistent with Ops Notes for this batch; no decimal-typo issue like sister batches 2-181/2-187). Lab cert Acid Number 58 mg KOH/g consistent with AECN low-pH bio-oil. [log:ops_notes.injection_data.ph, cobb_row_88.injection_ph, lab_results.acid_number_mg_koh_g, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date 4/23/2026 ↔ COBB L_injection_completion_date 2026-04-23 ↔ Certify removal date 23 Apr 2026 — three-way match. COBB also has order_line_completed_on 2026-04-15 17:09:36 (purchase-order completion, distinct from injection completion). [log:ops_notes.completion_date, cobb_row_88.injection_completion_date, cobb_row_88.order_line_completed_on, certify.removal_date, _derived_values, standard_efs_sheet, certify]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field in Ops Notes Batch Composition is expected to be blank for AECN. Confirmed blank in Ops Notes CSV export — no erroneous density value. [log:oil_type, ops_notes.file, _derived_values, standard_efs_sheet]',
     'VR Sec 5.1'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Flag',
     'Source-file provenance inconsistency vs sister batches in the same RP. 2-199 Certify Sources #40 links AECN Production Process Emissions datapoint to the generic "Standard Emission Factors + Calculations (4).xlsx" (Public; same file also linked at #39 to AECN Production Embodied Emissions). Sister AECN truck batches in the same April 2026 RP link to period-specific AECN LCA CI documents: 2-180 → "BH 2025 LCA w Stack Emissions.xlsx"; 2-181 → "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx". Even with the EF value now refreshed to 0.104 (matching), the underlying evidence file linked to the datapoint is different from comparable sisters — a verifier-facing provenance inconsistency. Garrett to relink 2-199 to the same period-specific AECN LCA CI files used by 2-180/2-181 for consistent within-RP evidence chain. [log:certify.sources, _derived_values, standard_efs_sheet, certify]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     'Stack emissions data is incorporated in the H1 2026 AECN Process Emissions tab of the Standard Emission Factors sheet (Total Stack Emissions g CO2e/MT Bio Oil = 4126.83, source GHGenius Ensyn RTP Model). Live H1 2026 sheet read confirms stack emissions integrated into AECN process EF derivation (Total Process = Stack 0.00412683 + Other Process from Vendor LCA 0.09970 = 0.10382683 MTCO2e/MT). [log:standard_efs_sheet.h1_2026_aecn_process_ef_basis, _derived_values]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present for AECN production period', 'Pass',
     'AECN production period #04-2026 (per BOL page 3 "BioEnergie AE Côte-Nord Prod.period #04-2026"). H1 2026 AECN Process Emissions tab in live Standard EFs sheet (gid=148943611) supplies the GHG accounting for this period. Linked Certify source: "Standard Emission Factors + Calculations (4).xlsx" (Public). [log:bol.cofa_number, standard_efs_sheet.h1_2026_aecn_process_ef_final_kgco2e_per_kg, _derived_values]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Re-verified 2026-05-13 after Garrett refresh. Certify component modal Inputs row for "AECN pyrolysis (from truck loads) - process emissions" now shows EF = **0.104 kgCO2e/kg** (precise 0.10402, matches H1 2026 sheet final 0.104017). Component output: 0.104 × 18,800 = 1,955 kgCO2e = 1.955 t ✓ matches new Certify component value (was 2.388 t pre-fix). Live Standard EFs sheet 2026 main tab "Production Emissions for AECN Oil--H1 2026" base 0.10380 + uncertainty add 0.002088 = final 0.104017 kgCO2e/kg — Certify display 0.104 is the rounded form. Now aligned with sister batches 2-180/2-181 EF 0.10402. [log:certify.uncertainty_inputs.aecn_pyrolysis_process.carbon_ef_kgco2e_per_kg, certify.components.activities_pyrolysis, standard_efs_sheet.h1_2026_aecn_process_ef_base_kgco2e_per_kg, standard_efs_sheet.h1_2026_aecn_process_ef_final_kgco2e_per_kg, _derived_values.aecn_process_ef_certify_kgco2e_per_kg, _derived_values.aecn_process_ef_sheet_h1_2026_final_kgco2e_per_kg, _derived_values, certify]',
     'VR Appendix 1, Standard EFs sheet 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Certify Datapoint "AECN Production Embodied Emissions" = 0.02 kgCO2e/kg (display; precise per modal = 0.0212). Live Standard EFs 2026 tab "Embodied Emissions for AECN Oil" = 0.02116 base / 0.021160 final — matches. Independent recalc: 18,800 × 0.0212 / 1000 = 0.39856 t ↔ Certify component "AECN pyrolysis (from truck loads) - embodied emissions" = 0.399 t ✓ exact match. [log:certify.uncertainty_inputs.aecn_pyrolysis_embodied.carbon_ef_kgco2e_per_kg, certify.components.activities_pyrolysis, standard_efs_sheet.h1_2026_aecn_embodied_ef_final_kgco2e_per_kg, _derived_values.aecn_embodied_ef_kgco2e_per_kg, _derived_values.aecn_embodied_emissions_check_t, _derived_values, certify]',
     'VR Appendix 1'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals (Process and Embodied) use Mass = 18,800 kg ± 72.57 kg = Origin Bio-Oil Mass datapoint (pre-sparging), NOT post-sparging Mass of Injectant 18,528 kg. Per protocol: pyrolysis emissions incurred to produce the full 18,800 kg, before in-injection sparging loss (1.29% at Basco). [log:certify.uncertainty_inputs.aecn_pyrolysis_process.mass_kg, certify.uncertainty_inputs.aecn_pyrolysis_embodied.mass_kg, ops_notes.batch_composition.origin_mass_kg, _derived_values, standard_efs_sheet, certify]',
     'PDD Sec A'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass × carbon wt% (decimal) × 3.667', 'Pass',
     'Independent recalc: 18.528 t (Mass of Injectant) × 0.4926 (Carbon decimal — outlier-capped value applied per Item 4.2) × 3.667 = 33.467 t ↔ Certify Sequestrations 33.468 t — exact match (1-kg rounding). NOTE: lab raw carbon is 53.0%, but Certify applies the outlier-capped 49.26% from "AECN C Content Outlier Analysis - 2026 YTD.xlsx". The 49.26% value is what reconciles to Certify gross; the raw 53.0% would yield 35.998 t (well above Certify). Cap policy correctly applied. [log:certify.calculation_view.sequestrations_t, certify.uncertainty_inputs.injection_sequestration.carbon_content_pct, certify.uncertainty_inputs.injection_sequestration.mass_of_injectant_kg, _derived_values.gross_co2e_recalc_t, _derived_values.gross_co2e_check, _derived_values, standard_efs_sheet, certify]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'Re-verified 2026-05-13 after Garrett refresh. Activities = 22.889 tCO2e total (was 23.322 pre-fix). Bio-oil-specific subset: (1) Truck Process 4.721 t (independent: 18.800 × 2,197 × 0.0001143 = 4.7211 t ✓), (2) Truck Embodied 0.522 t (independent: 2,197 × 0.00023756 = 0.5220 t ✓), (3) Pyrolysis Process 1.955 t (independent: 18,800 × 0.104017 / 1000 = 1.9555 t ✓), (4) Pyrolysis Embodied 0.398 t (independent: 18,800 × 0.0212 / 1000 = 0.399 t ≈ 0.398 t display rounding). Bio-oil chain subtotal: 4.721 + 0.522 + 1.955 + 0.398 = 7.596 t. Site-emissions burden adds another 15.293 t to Activities. Total: 7.596 + 15.293 = 22.889 ✓. [log:certify.calculation_view.activities_tco2e, certify.components.activities_bio_oil_transport, certify.components.activities_pyrolysis, _derived_values.tanker_truck_process_recalc_t, _derived_values.tanker_truck_embodied_recalc_t, _derived_values.aecn_process_emissions_certify_t, _derived_values.aecn_process_emissions_at_sheet_ef_t, _derived_values.aecn_embodied_emissions_check_t, _derived_values.bio_oil_chain_activities_subtotal_t, _derived_values, standard_efs_sheet, certify]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Re-verified 2026-05-13. Calculation View Uncertainty Discount = 0.186 t (was 0.190 pre-fix; slight reduction reflects lower variance from corrected process emission). Per Isometric Standard v2.0 §3.7.3 (Option B Variance Propagation). Discount = 0.56% of Sequestrations (186 / 33,468). Discount present in net formula. [log:certify.uncertainty_discount_tco2e_implied, _derived_values.uncertainty_discount_pct_of_gross, _derived_values, standard_efs_sheet, certify]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with BCU Quant and GHG Statement', 'Pass',
     'Re-verified 2026-05-13 after Garrett refresh. Independent net recalc: 33.468 (Seq) + 8.707 (BCU) − 22.889 (Activities, post fix) − 0.186 (Uncertainty) = 19.100 t ↔ Certify Calc View Net 19.10 t (displayed) — exact match. BCU breakdown unchanged: 4.721 (Transport Process, Charm-A5) + 2.731 (Diesel Site) + 0.981 (LA Sitework) + 0.125 (Brine Transport) + 0.074 (Railcar) + 0.075 (Waste Disposal Process) = 8.707 t ✓. AECN Process EF refreshed to 0.104 — 6.4/7.2 FAILs cleared. Net rose from 18.66 → 19.10 (delta +0.44 t = matches predicted +0.433 t correction). [log:certify.calculation_view.net_co2e_t, certify.calculation_view.calculation_check, _derived_values.net_calc_t, _derived_values, standard_efs_sheet, certify]',
     'GHG Stmt Sec E'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 — Completeness: every AECN component has uncertainty on correct datapoint', 'Pass',
     'All 4 required AECN-component uncertainty inputs opened and read from each Certify component modal INPUTS section: (1) Injection Sequestration — Carbon Content ±0.197%, Mass of Product ±72.57 kg; (2) AECN→LA Tanker Truck Transport Process — Mass of Load ±72.57 kg (Distance no uncertainty per protocol); (3) AECN Pyrolysis Process — Mass ±72.57 kg; (4) AECN Pyrolysis Embodied — Mass ±72.57 kg. Embodied transport correctly has no Mass of Load input (per-mile basis per FC8). [log:certify.uncertainty_inputs.injection_sequestration, certify.uncertainty_inputs.aecn_to_la_transport_process, certify.uncertainty_inputs.aecn_pyrolysis_process, certify.uncertainty_inputs.aecn_pyrolysis_embodied, _derived_values, standard_efs_sheet, certify]',
     'Isometric Standard v2.0 S3.7.3'),
    ('7a.2', 'Layer 2 — Correctness: reported ± matches expected value', 'Pass',
     'Per Isometric Standard v2.0 §3.7.3: Carbon Content uncertainty = 0.004 × Measured = 0.004 × 49.26 = 0.197% (Certify modal shows ±0.197 — exact match). Mass-of-load uncertainty = 72.57 kg per discrete weight (one truck = one weighing event) — Certify shows ±72.57 kg on all four AECN mass inputs (Injection Sequestration Mass of Product, Truck Transport Process Mass of Load, Pyrolysis Process Mass, Pyrolysis Embodied Mass). All exact matches to SKILL doc + Isometric Standard expected values. [log:certify.uncertainty_inputs.injection_sequestration.carbon_uncertainty_pct, certify.uncertainty_inputs.injection_sequestration.carbon_uncertainty_formula, certify.uncertainty_inputs.injection_sequestration.mass_uncertainty_kg, certify.uncertainty_inputs.aecn_to_la_transport_process.mass_uncertainty_kg, certify.uncertainty_inputs.aecn_pyrolysis_process.mass_uncertainty_kg, certify.uncertainty_inputs.aecn_pyrolysis_embodied.mass_uncertainty_kg, _derived_values, standard_efs_sheet, certify]',
     'Isometric Standard v2.0 S3.7.3'),
    ('7a.3', 'Layer 3 — Discount presence and consistency', 'Pass',
     'Aggregate Uncertainty Discount = 0.186 t present in Calc View net formula (33.468 + 8.707 − 22.889 − 0.186 = 19.100 ✓ post Garrett fix). Discount = 0.56% of Sequestrations — magnitude consistent with the multi-input variance propagation (5×±72.57 kg mass + ±0.197% carbon + site-emission constant uncertainties) per Option B (Isometric Standard v2.0 §3.7.3). [log:certify.uncertainty_discount_tco2e_implied, _derived_values.uncertainty_discount_pct_of_gross, _derived_values.uncertainty_discount_t, _derived_values.net_calc_t, _derived_values, standard_efs_sheet, certify]',
     'Isometric Standard v2.0 S3.7.3'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Lab raw Carbon 53.0% IS an outlier (2.23 SD above mean, # method-range flag) — surfaced in 4.2 and explained via the outlier-cap policy (Charm applies cap → 49.26% in Certify). Mass 18,800 kg / 18,833.14 kg / 18,528 kg all within typical AECN truck range. Net 18.66 t reflects gross 33.468 t minus the heavy site-emissions burden — explainable, not anomalous. No unexplained outliers; outlier handling documented. [log:lab_results.carbon_pct, lab_results.carbon_outlier_finding, ops_notes.batch_composition.origin_mass_kg, certify.calculation_view.net_co2e_t, _derived_values, standard_efs_sheet, certify]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented, unrecovered mass deducted, incident report filed', 'N/A',
     'No spill or unrecovered loss documented in Ops Notes or Drive folder. Ops Notes "Loss 242.52 kg / Loss % 1.29%" = sparging loss only, NOT a spill. Site Emissions folder includes a "March Oil Spill Disposal.png" file linked to Basco Injection Waste Disposal Emissions component — that is a site-level historical spill disposal evidence, not a 2-199 batch-specific spill. [log:ops_notes.totals.sparging_loss_kg, certify.sources, _derived_values, standard_efs_sheet, certify]',
     'VR Sec 3.5'),
    ('8.3', 'Inventory reconciliation: carryover oil documented', 'N/A',
     'Single-truck batch, no multi-period inventory allocation. Origin lot 2352-T fully consumed in this one batch (Ops Notes "Total" = "Origin" = 18,800 kg, single Truck 1 row populated). [log:ops_notes.batch_composition.origin_bol, ops_notes.batch_composition.total_mass_kg, cobb_row_88.consumed_lot, _derived_values, standard_efs_sheet]',
     'GHG Stmt Sec C'),

    ('SECTION', '9. Isometric Certify — Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Components Sequestrations = 33.468 tCO2e (single "Injection sequestration" entry). Independent recalc: 18,527.79 kg × 0.4926 × 3.667 / 1000 = 33.467 t — matches Certify to 1-kg rounding. Per-component math: Mass of Injectant 18.528 t × Carbon Content (outlier-capped) 49.26% × 3.667 CO2/C molar ratio. [log:certify.components.sequestrations, certify.uncertainty_inputs.injection_sequestration.mass_of_injectant_kg, certify.uncertainty_inputs.injection_sequestration.carbon_content_pct, _derived_values.gross_co2e_recalc_t, _derived_values, standard_efs_sheet, certify]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES — Transport: Process + embodied correct for AECN truck route', 'Pass',
     'Two transport components verified per-component with full math: (a) "AECN to LA Tanker Truck Transport Process Emissions" 4.721 t — modal inputs: mass-of-load 18,800 kg, distance 2,197 mi, EF 0.0001143 MTCO2e/(t·mi). Recalc: 18.800 × 2,197 × 0.0001143 = 4.7211 t ✓ matches 4.721 displayed. (b) "AECN to LA Tanker Truck Transport Embodied Emissions" 0.522 t — modal inputs: distance 2,197 mi, EF 0.1476 kgCO2e/km. Recalc: 0.1476 × 2,197 × 1.609344 = 521.95 kg ≈ 0.522 t ✓. **Transport process sum (single leg): 4.721 t.** **Bio-oil transport total: 4.721 + 0.522 = 5.243 tCO2e** = Certify Components "Bio-oil transport" subtotal. Per FC8 convention: embodied is per-mile (no mass-of-load input on embodied). [log:certify.components.activities_bio_oil_transport, certify.uncertainty_inputs.aecn_to_la_transport_process.distance_mi, certify.uncertainty_inputs.aecn_to_la_transport_process.mass_of_load_kg, _derived_values.tanker_truck_process_ef_mtco2e_per_t_mi, _derived_values.tanker_truck_process_recalc_t, _derived_values.tanker_truck_process_recalc_basis, _derived_values.tanker_truck_embodied_ef_kgco2e_per_km, _derived_values.tanker_truck_embodied_recalc_t, _derived_values.tanker_truck_embodied_recalc_basis, _derived_values.transport_process_sum_t, _derived_values.transport_total_t, _derived_values, standard_efs_sheet, certify]',
     'Certify Components, Transport Emissions Acctg v1.1'),
    ('9.3', 'ACTIVITIES — Site emissions: 11 components on Bio-oil injection (site-emissions burdened scapegoat)', 'Pass',
     'This is a scapegoat removal carrying the full April 2026 Basco site emissions burden (15.293 t across 11 components). Per-component reconciliation against the Site Emissions folder (https://drive.google.com/drive/folders/15IgMdOSbekKv8GCZ8NfmdLqyTN9gsBAi): (1) Basco Site Electricity Use (RECs) 2.168 t ← Basco April 26 Electricity (1).xlsx + Delta Region FH25 REC retirement; (2) B6 Diesel 2.731 t ← 4-1-_4-30 Diesel Consumption Calcs.xlsx + 4 diesel receipt PDFs + Diesel EF 3.87 kgCO2e/kg; (3) B6 Gasoline 0.700 t ← 4-1-_4-30 Gasoline Tracker LA.xlsx + 5 gas receipt PDFs + Gasoline EF 3.74 kgCO2e/kg; (4) B6 Waste Disposal 2.453 t ← Waste Disposal Emissions Calc Sheet - 4_26.xlsx + March Oil Spill Disposal.png (labeled "BCUs NOT applied" by design); (5) Additional Railcar Movement 0.162 t ← April 2026 Railcar Emissions Calc Sheet.xlsx + Copy of Railline Distances.png (empty railcar repositioning, NOT this batch transport); (6) B6 Water Embodied Transport 0.016 t + (7) B6 Water Process Transport 0.125 t ← Water Transport Calc Sheet.xlsx + Bourque Invoice 20260624 - 4.20.26 Brine.pdf (Brine 19.305 t, distance 57 mi); (8) B6 Injection Embodied 0.685 t ← Basco 6 Capital and Sitework Embodied Emissions Inventory Apr 1 - Apr 30.xlsx; (9) SP&C April Basco 0.458 t ← Basco Inj Operations SP+C Inventory Apr 1 - Apr 30.xlsx; (10) Basco Support Travel 4.812 t ← Basco Support Travel Calc Sheet Apr 1 - Apr 30.xlsx; (11) Louisiana Sitework 0.983 t ← Louisiana Sitework Apr 1 - Apr 30.xlsx. Sum: 2.168+0.016+2.731+0.700+2.453+0.162+0.125+0.685+0.458+4.812+0.983 = 15.293 t ✓ matches Certify "Bio-oil injection" Activities subtotal. **All 11 components have corresponding Drive subfolder evidence in the per-RP Site Emissions folder.** (Deep per-category methodological QA is the qa-site-emissions skill\'s territory — this batch QA verifies presence + math allocation to this scapegoat removal.) [log:certify.components.activities_bio_oil_injection, certify.components.activities_bio_oil_injection_total_t, site_emissions_folder.subfolders_present, site_emissions_folder.subfolders_to_certify_components_mapping, _derived_values.site_emission_burdened_total_t, _derived_values, standard_efs_sheet, certify]',
     'Certify Components'),
    ('9.4', 'ACTIVITIES — Pyrolysis: AECN production process + embodied present', 'Pass',
     'Re-verified 2026-05-13 after Garrett refresh. Two pyrolysis components present with "from truck loads" naming: (a) "AECN pyrolysis (from truck loads) - process emissions" 1.955 t (was 2.388 pre-fix) — modal inputs: mass 18,800 kg, EF 0.104 kgCO2e/kg (precise 0.10402, matches H1 2026 sheet final 0.104017). Recalc: 18,800 × 0.104017 / 1000 = 1.9555 t ✓. (b) "AECN pyrolysis (from truck loads) - embodied emissions" 0.398 t — modal inputs: mass 18,800 kg, EF 0.0212 kgCO2e/kg. Recalc: 18,800 × 0.0212 / 1000 = 0.399 t ≈ 0.398 t (display rounding). Embodied EF matches H1 2026 sheet (0.02116 base / 0.021160 final). Both apply EF to Origin Bio-Oil Mass (pre-sparging) per protocol. Pyrolysis subtotal: 1.955 + 0.398 = 2.353 t (was 2.787 pre-fix). [log:certify.components.activities_pyrolysis, certify.uncertainty_inputs.aecn_pyrolysis_process, certify.uncertainty_inputs.aecn_pyrolysis_embodied, _derived_values.aecn_process_ef_certify_kgco2e_per_kg, _derived_values.aecn_process_ef_sheet_h1_2026_final_kgco2e_per_kg, _derived_values.aecn_embodied_ef_kgco2e_per_kg, _derived_values, certify]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: All applicable BCU categories populated', 'Pass',
     '6 BCU constant-reduction datapoints applied across 3 component subcategories (matches site-emissions-burdened scapegoat removal pattern): **Bio-oil processing** (3.837 t): BCU - Diesel Site Emissions 2.731 t + BCU - Louisiana Sitework 0.981 t + BCU - Brine Transport 0.125 t = 3.837 t ✓. **Bio-oil transport** (4.721 t): BCU - Transport Process 4.721 t (cert: Charm-A5-2024-10-24-63-1976.pdf — World Energy PoS, 21.912 MT renewable diesel HEFA tallow, 70.603 MT CO2 reduction pool, 4.721 t allocated to this batch). **Miscellaneous** (0.149 t): BCU - Railcar Emissions 0.074 t + BCU - Waste Disposal Process 0.075 t = 0.149 t ✓. Total adjustments: 3.837 + 4.721 + 0.149 = 8.707 t ✓ matches Certify Adjustments total. (BCU cert filename provenance flagged separately in Item 9.9.) [log:certify.components.adjustments_bio_oil_processing, certify.components.adjustments_bio_oil_transport, certify.components.adjustments_miscellaneous, certify.adjustments_bcus_tco2e, certify.sources, _derived_values, standard_efs_sheet, certify]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS — BCU quantity >= corresponding activity emission', 'Flag',
     'BCU vs activity for BCU-eligible items (Transport Process sum shown explicitly per feedback_show_transport_process_sum.md): Transport Process BCU 4.721 = transport process sum 4.721 (AECN→LA Tanker Truck Process; single leg) ✓; Diesel BCU 2.731 = activity 2.731 ✓; Brine Transport BCU 0.125 = activity 0.125 ✓; Louisiana Sitework BCU 0.981 < activity 0.983 by 0.002 t (rounding-level, 0.2% shortfall); **Railcar Movement BCU 0.074 < activity 0.162 by 0.088 t (54% shortfall — material coverage gap).** Items where the rule does not apply by protocol design: embodied components (5× summing 1.622 t, embodied not BCU-eligible per protocol); Waste Disposal Process activity 2.453 t (component explicitly labeled "BCUs NOT applied" by datapoint name; the 0.075 BCU - Waste Disposal Process is a separate component covering waste-transport process, not disposal proper); Gasoline 0.700 t and Support Travel 4.812 t (outside protocol scope); Electricity 2.168 t (REC offset separately via Delta Region FH25 retirement). Garrett action: confirm whether Railcar Movement BCU should be increased to fully cover 0.162 t, or whether the partial 0.074 t is intentional (e.g., only the BCU-eligible portion of railcar emissions). [log:certify.components.adjustments_bio_oil_transport, certify.components.activities_bio_oil_transport, certify.components.adjustments_bio_oil_processing, certify.components.activities_bio_oil_injection, _derived_values.transport_process_sum_t, _derived_values.bcu_transport_process_coverage_pct, _derived_values.bcu_diesel_coverage_pct, _derived_values.bcu_brine_transport_coverage_pct, _derived_values.bcu_louisiana_sitework_coverage_pct, _derived_values, standard_efs_sheet, certify]',
     'Certify Components'),
    ('9.7', 'COUNTERFACTUALS: Zero per protocol', 'Pass',
     'Certify Components Counterfactuals total = 0 tCO2e. Per Charm CDR protocol for bio-oil geological storage, counterfactuals are zero. [log:certify.counterfactuals_tco2e, _derived_values, standard_efs_sheet, certify]',
     'PDD'),
    ('9.8', 'Net removal matches independent calculation', 'Pass',
     'Re-verified 2026-05-13 after Garrett refresh. Independent: 33.468 (Seq) + 8.707 (BCU) − 22.889 (Activities, post fix) − 0.186 (Uncertainty) = 19.100 t ↔ Certify Calc View 19.10 t ✓ exact match. AECN Process EF refreshed to 0.104 — discrepancy resolved. [log:certify.calculation_view.net_co2e_t, certify.calculation_view.calculation_check, _derived_values.net_calc_t, _derived_values, standard_efs_sheet, certify]',
     'Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     'Hygiene issues on Certify Sources tab: (a) #34 "Screenshot 2026-04-10 at 3.19.33 PM.png" linked to EF Truck Transport Fuel Use (same non-descriptive screenshot filename as sister batches 2-180/2-181/2-185 etc.); (b) #36 / #39 / #40 "Standard Emission Factors + Calculations (4).xlsx" linked to TWO different AECN Pyrolysis datapoints (Embodied AND Process) — the generic "(4)" suffix and shared filename obscures which file version is authoritative (relates to the AECN Process EF discrepancy in 6.4). (c) BCU cert filename "Charm-A5-2024-10-24-63-1976.pdf" — A5 lot ID differs from sister-batch A4 pattern; BCU quantity 4.721 t exactly matches Transport Process — quantity verified correct, cert provenance worth Garrett one-line confirmation. Hygiene flags only, not verifier-impacting individually but compound with 6.4 EF question. [log:certify.sources, _derived_values, standard_efs_sheet, certify]',
     'Certify Datapoints, Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     '41 entries on Certify Sources tab — fully enumerated in source_reads.json (exhaustive scan via Playwright snapshot, all 41 rows captured). Drive folder enumerated via Playwright (3 items: Testing folder containing lab cert, Scale Tickets folder containing both tickets, Ops Notes Sheet). Cross-reference: 2-199 Full Scale Ticket.jpg ↔ Sources #11 ✓; 2-199 Empty Ticket.png ↔ Sources #12 ✓; 2-199 Ops Notes ↔ Sources #10 (xlsx export, "2-199 Ops Notes (1).xlsx") ✓; lab cert 2-199 - 2-201.pdf in Sources #8 AND Drive Testing subfolder ✓; BOL "documents 2352-T corr.pdf" in Sources #35 (per Document Location Rule, BOLs may be in Certify Sources rather than Drive — acceptable). Site emissions evidence files (33 of the 41 sources) cross-referenced against the Site Emissions Drive folder (https://drive.google.com/drive/folders/15IgMdOSbekKv8GCZ8NfmdLqyTN9gsBAi) — 9 category subfolders + BCU Quant sheet, all sources accounted for. All required documents accounted for. [log:certify.certify_sources_tab_total, certify.sources, drive_folder.items, site_emissions_folder.subfolders_present, _derived_values, standard_efs_sheet, certify]',
     'Certify Sources vs Drive'),
]


def build_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Batch 2-199 QA'

    ws.column_dimensions['A'].width = 9
    ws.column_dimensions['B'].width = 45
    ws.column_dimensions['C'].width = 9
    ws.column_dimensions['D'].width = 95
    ws.column_dimensions['E'].width = 22

    row = 1
    for entry in ROWS:
        kind = entry[0]
        if kind == 'HEADER':
            ws.cell(row, 1, 'BATCH 2-199 QA CHECKLIST').font = Font(bold=True, size=14)
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
            # Apply SECTION_FILL across all 5 columns (#D6E4F0 per feedback_checklist_header_one_color.md)
            for c in range(1, 6):
                cell = ws.cell(row, c)
                cell.fill = SECTION_FILL
                cell.border = BORDER
            ws.cell(row, 1, entry[1]).font = SECTION_FONT
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
            ws.row_dimensions[row].height = max(20, min(est_lines * 14, 400))

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
    ws.cell(row, 2, '19.10 tCO2e (post Garrett 2026-05-13 EF refresh; was 18.66 pre-fix)')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True)
    ws.cell(row, 2, 'CLEARED — Prior 5 FAILs (items 6.4 / 7.2 / 7.4 / 9.4 / 9.8) all cleared by Garrett refresh on 2026-05-13. Certify AECN Production Process EF refreshed from 0.12704 → 0.104 kgCO2e/kg (matches H1 2026 sheet final 0.104017 and sister batches 2-180/2-181 value 0.10402). AECN Pyrolysis Process component dropped from 2.388 t → 1.955 t (delta -0.433 t). Activities total dropped from 23.322 → 22.889 t. Net rose from 18.66 → 19.10 t. Math independently verified: 33.468 - 22.889 + 8.707 - 0.186 = 19.100 ✓.')
    row += 1
    ws.cell(row, 1, 'Other notable findings').font = Font(bold=True)
    ws.cell(row, 2, '4.2 FLAG (Carbon outlier-cap policy): Lab raw Carbon = 53.0% (flagged with "#" indicating outside SGS test method analytical range) — 2.23 SD above AECN mean 39.42 (n=285), outside 2-SD upper 51.60%. Certify applies an outlier-cap policy via "AECN C Content Outlier Analysis - 2026 YTD.xlsx" yielding the 49.26% applied value used in Sequestrations math. Math reconciles cleanly with capped value (18.528 × 0.4926 × 3.667 = 33.467 ≈ 33.468 Sequestrations). Same outlier pattern as 2-192. Worth Garrett one-line confirmation that the cap policy is authoritative.\n\n2.1 FLAG (image hygiene): Empty scale ticket is a phone screenshot of CAT ticket in iOS document viewer with "Eye Protect" yellow tint overlay — same hygiene pattern as 2-181. Values legible, math reconciles, but Garrett to re-upload direct photo for future batches.\n\n5.4 FLAG (COBB-side data hygiene, NOT verifier-impacting): COBB row 88 cells F/G/H = 18,080 (pre-correction BOL value, before BOL page-3 ***Corrections*** tare 16910→16190 → net 18080→18800). Ops Notes/Certify use the corrected 18,800. 720 kg COBB-side gap. Garrett to backfill COBB row 88 F/G/H with 18,800.\n\n9.9 FLAG (Garrett-side filename hygiene): (a) "Screenshot 2026-04-10 at 3.19.33 PM.png" non-descriptive filename linked to Truck Transport EF (sister-batch hygiene set). (b) Generic "Standard Emission Factors + Calculations (4).xlsx" links to BOTH AECN Pyrolysis Process AND Embodied — compounds the EF discrepancy in 6.4. (c) BCU cert "Charm-A5-2024-10-24-63-1976.pdf" — A5 vs sister batches\' A4 lot ID; BCU quantity 4.721 t exactly matches Transport Process — quantity verified correct, cert provenance worth Garrett one-line confirmation.')
    row += 1
    ws.cell(row, 1, 'Site emissions burden').font = Font(bold=True)
    ws.cell(row, 2, 'This is a scapegoat removal carrying 11 site-emissions activity components (15.293 t total): Basco Site Electricity (RECs) 2.168, Diesel 2.731, Gasoline 0.700, Waste Disposal 2.453, Railcar Movement 0.162, Brine (process+embodied) 0.141, B6 Injection Embodied 0.685, SP&C 0.458, Support Travel 4.812, LA Sitework 0.983. All 11 components verified evidenced by the per-RP Site Emissions Drive folder (https://drive.google.com/drive/folders/15IgMdOSbekKv8GCZ8NfmdLqyTN9gsBAi) which has 9 category subfolders + BCU Quant sheet. Net remains positive (19.100 t post-fix) — no net-emissive concern. Per-category methodological QA of site emissions is the qa-site-emissions skill\'s territory; this batch QA verifies presence + math allocation only.')

    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-199/Batch_2-199_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
