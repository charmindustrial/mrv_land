#!/usr/bin/env python3
"""Build Batch 2-180 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations.

AECN truck batch — direct AECN→Basco delivery. Single scale ticket pair.
"""

import json
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

# Wire the pre-build audit gate (negative-claim + SKILL-proxy + log-key + numeric drift)
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "skills" / "qa" / "batch-qa-aecn" / "scripts"))
from checklist_lib import validate_rows, format_failures, BuildAborted  # noqa: E402

SOURCE_READS_PATH = _REPO_ROOT / "outputs" / "qa" / "batch-2-180" / "batch_2-180_source_reads.json"

FAIL_FILL = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
FAIL_FONT = Font(color='9C0006', bold=True)
FLAG_FILL = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
FLAG_FONT = Font(color='996600')
NA_FONT = Font(color='808080', italic=True)
HEADER_FILL = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
HEADER_FONT = Font(color='FFFFFF', bold=True, size=12)
# Per feedback_checklist_header_one_color: ALL section/sub-section headers = #D6E4F0
SECTION_FILL = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
SECTION_FONT = Font(bold=True, size=11)

THIN = Side(border_style='thin', color='808080')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical='top', horizontal='left')
WRAP_CENTER = Alignment(wrap_text=True, vertical='center', horizontal='center')

ROWS = [
    ('HEADER',),
    ('META', 'Batch ID', '2-180'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 01 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-05-11'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Truck (direct AECN→Basco). Single tanker, BOL 2343-T, scale ticket pair 1312226084637/4638 (Pilot Bunkie LA, 3-25-26).'),
    ('META', 'Net CDR (Certify)', '30.77 tCO2e (Calculation View precise: 30.773)'),
    ('SPACER',),
    ('COLUMNS',),

    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder id 1W3nJQgf82wgk3GLjOrn6nlJ87nqGbh3R titled "2-180" — contains "2-180 Ops Notes" Google Sheet, Scale Tickets subfolder, Testing subfolder. [log:_meta.drive_folder_id, drive_folder_contents.items]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets (id 1X-4Yu1dOSvxOeYV8-BipLq1rk2wFm7n1) contains "2-180 Full Scale Ticket (1).jpg" and "2-180 Empty Ticket (1).jpg". Single truck batch → one ticket pair. Both also in Certify Sources (entries #7 Full Public + #8 Empty Public, linked to "Mass of Injectant (per injection)"). Image pixels Read directly via drive.usercontent.google.com/download + browser_network_request response-body capture per feedback_drive_image_download_pattern.md (not OCR snippet, per feedback_ocr_not_primary_source). [log:scale_tickets.full_ticket.drive_file_id, scale_tickets.empty_ticket.drive_file_id, scale_tickets._source_method]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive Testing subfolder (id 1BQloRHufk0J1Oeo-mF9nCgLHz_AIzs8u) contains "SR26-02231_Batch_2-180-185_COA (1).pdf" (drive_file_id 1qG8JNyROfr3qAXrx8gTQit6pFOR7WSdv) — multi-batch CHN cert covering 2-180 through 2-185, page 1 of 6 dedicated to batch 2-180. Same file present in Certify Sources #5 Public, linked to Carbon Content datapoint. [log:lab_results.certify_source_filename, lab_results.certify_source_ref, lab_results.multi_batch_certificate_range, drive_folder_contents.items]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-180 Ops Notes" Google Sheet (id 1F46loRUaCWHMPZfposf5o4pYEoQO6Ek8hbdR5gCTPb8) present, single sheet "Sheet1" populated: completion date 4/1/2026, batch 2-180, Batch Composition (Origin BOL 2343-T mass 19,910 kg), Constants (sparging 0.0129, lbs/kg 2.20462), Injection Data (Truck 1 full 79,640 / empty 35,800 / net 19,885.47 kg / pH 3.1), Total Injectate 19,885.47, Sparging Loss 256.52, Mass of Bio-Oil Injected 19,628.95, AECN Oil Added 19,910 / Injected 19,628.95 / Loss 281.05 kg = 1.41%. [log:ops_notes.drive_file_id, ops_notes.completion_date, ops_notes.batch_composition.origin_bol, ops_notes.injection_data.truck_1, ops_notes.injection_data.mass_of_bio_oil_injected_kg, ops_notes.mass_loss_summary.loss_pct]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'CHN CoA LOCATION = "BASCO LOUISIANA" (lab cert page 1, batch 2-180). BOL Ship To = "CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367, USA" (Basco). Certify project = "Charm Bio-oil Geologic Storage" with single AECN→LA Tanker Truck Transport route. Exhaustive grep -i "vaulted" across BOL (5 pp), CHN (6 pp), BCU cert (1 p), Ops Notes CSV, COBB CSV returned no matches in any per-batch primary source. [log:lab_results.sample_location, bol.ship_to_address, live_source_verifications_2026_05_11.vaulted_absence_search]',
     'PDD'),

    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both image pixels Read (per OCR-vs-image rule). Full ticket #1312226084637, weigh #4637, dated 3-25-26 at PILOT TRAVEL CENTER I-49 EXIT 40 BUNKIE LA scale 3122; axle sum 13,460 + 33,300 + 32,880 = 79,640 lb (= certified gross, exact). Empty ticket #1312226084638, weigh #4637, dated 3-25-26 09:38 same location/scale; axle sum 12,440 + 14,540 + 8,820 = 35,800 lb (= certified gross, exact). Empty ticket cross-references Full via "TICKET # OF FULL $ WEIGH" = 1312226084637 → confirms paired weighing. Both internally consistent (gross = axle sum). [log:scale_tickets.full_ticket.ticket_number, scale_tickets.empty_ticket.ticket_number, scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, scale_tickets.full_ticket.axle_sum_matches_gross, scale_tickets.empty_ticket.axle_sum_matches_gross, scale_tickets.empty_ticket.reference_to_full_ticket]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Both tickets dated 3-25-26. Injection completion date per Ops Notes = 4/1/2026. 7 days between truck-out weigh and injection — within 2-week tolerance. [log:scale_tickets.full_ticket.date, scale_tickets.empty_ticket.date, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Both tickets show identical tractor "2217" and trailer "36629". Same scale 3122 / location Pilot Bunkie LA / company KIK CARRIER. Same vehicle weighed at both events; trailer 36629 also matches BOL Tanker ID# 36629 (page 1) → same physical tanker AECN→Basco. [log:scale_tickets.full_ticket.tractor_number, scale_tickets.empty_ticket.tractor_number, scale_tickets.full_ticket.trailer_number, scale_tickets.empty_ticket.trailer_number, scale_tickets.consistency_checks.tractor_numbers_match, scale_tickets.consistency_checks.trailer_numbers_match, bol.tanker_id]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     'Scale-ticket math: (79,640 − 35,800) lb × 0.453592 = 43,840 × 0.453592 = 19,885.47 kg. Ops Notes "Truck 1 Injectate Mass (kg)" = 19,885.47328 — exact match. [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, _derived_values.scale_ticket_net_lb, _derived_values.scale_ticket_net_kg_recalc, ops_notes.injection_data.truck_1.injectate_mass_kg]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Scale net 19,885.47 kg vs BOL page-3 authoritative Qty Shipped 19,910 kg (page-3 product delivered + page-4 weighbridge Masse nette both = 19,910 kg). MIN(scale, BOL) = scale ticket net 19,885.47 kg (scale wins by 24.5 kg — well within scale uncertainty). Ops Notes uses 19,885.47 as Total Injectate Mass basis for downstream calc. [log:_derived_values.scale_ticket_net_kg_recalc, bol.authoritative_qty_shipped_kg, _derived_values.conservative_mass_min_scale_bol_kg, _derived_values.conservative_mass_min_basis, ops_notes.injection_data.total_injectate_mass_kg]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 (standard AECN at Basco) applied to scale-net basis: 19,885.47 × 0.0129 = 256.52 kg loss. Mass of Bio-Oil Injected = 19,885.47 − 256.52 = 19,628.95 kg. Ops Notes row shows Sparging Loss 256.5226053 and Mass of Bio-Oil Injected 19,628.95067 — both exact. [log:ops_notes.constants.sparging_mass_loss, ops_notes.injection_data.sparging_loss_kg, ops_notes.injection_data.mass_of_bio_oil_injected_kg, _derived_values.sparging_loss_kg, _derived_values.mass_of_bio_oil_injected_kg, _derived_values.scale_ticket_net_kg_recalc, ops_notes.injection_data.total_injectate_mass_kg]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Scale ticket net 19,885.47 kg = Ops Notes Total Injectate 19,885.47 = post-sparging Mass of Bio-Oil Injected 19,628.95 = Certify Mass of Injectant (per injection) 19.629 t (modal precise: 19,628.95, uncertainty kg per discrete weight from live MRV Uncertainty cheat sheet). BOL Qty Shipped 19,910 kg = Certify Origin Bio-Oil Mass - AECN 19.910 t = Ops Notes Batch Composition Origin Mass 19,910. COBB origin_quantity_kg 19,910 = BOL; COBB offloaded_quantity_kg 19,885.47328 = scale net. All five sources align. [log:_derived_values.scale_ticket_net_kg_recalc, ops_notes.injection_data.total_injectate_mass_kg, ops_notes.injection_data.mass_of_bio_oil_injected_kg, certify_datapoints.datapoints.Mass_of_Injectant_per_injection.value_kg, certify_datapoints.datapoints.Origin_Bio_Oil_Mass_AECN.value_kg, bol.authoritative_qty_shipped_kg, cobb_row_61.G61_offloaded_quantity_kg, cobb_row_61.H61_origin_quantity_kg, live_source_verifications_2026_05_11.standard_efs_sheet_2026_tab]',
     'VR Sec 5.1'),

    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOL present for shipment', 'Pass',
     'BOL "documents 2343-T.pdf" (5-page PDF) downloaded from Certify Sources #10 Public via signed URL and Read locally; linked to "Origin Bio-Oil Mass - AECN" datapoint. BOL number 2343-T appears consistently across page 1 (Straight BOL), page 3 (Shipping Details Run #3-2026), page 4 (Quebec weighbridge transaction PC0038060), page 5 (Commercial Invoice). [log:bol.certify_source_filename, bol.bol_number, bol.certify_source_ref]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'N/A',
     'Truck batch — direct AECN→Basco delivery, single BOL. Rail-leg routing N/A. [log:_meta.delivery_mode]',
     'N/A'),
    ('3.3', 'BOL mass matches or exceeds reported injectate mass', 'Pass',
     'BOL page-3 Product delivered = 19,910 kg = page-4 weighbridge Masse nette 19,910 kg. Mass of Bio-Oil Injected (post-sparging) = 19,628.95 kg. BOL (19,910) ≥ injectate (19,628.95) ✓. BOL also ≥ scale net 19,885.47 (so scale is the binding conservative constraint, BOL is a check). [log:bol.authoritative_qty_shipped_kg, ops_notes.injection_data.mass_of_bio_oil_injected_kg, _derived_values.conservative_mass_min_basis]',
     'VR Sec 3.5'),
    ('3.4', 'Origin and destination correct on BOL', 'Pass',
     'BOL: Origin = BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier, Québec G5B 2V9; Destination = CHARM Industrial Inc., 4687 LA-115, St Landry, LA 71367 USA. Carrier Tandet Logistics, Driver Samir Didrie. Standard AECN truck route. [log:bol.ship_from_name, bol.ship_from_address, bol.ship_to_name, bol.ship_to_address, bol.carrier]',
     'VR Appendix 1, PDD Sec A'),
    ('3.5', 'Transportation distance consistent with known AECN route', 'Pass',
     'Certify Datapoints: "Aggregate Distance Transported AECN to Basco" = 2,197 mi (REPORTED, source AECN to Basco.png) and "Distance from AECN to Basco" = 2,197 mi (DERIVED). Matches expected AECN truck route ~2,197 mi (KB Section 8). Single direct route — no leg allocation needed. Distance source is a Google Maps screenshot (AECN to Basco.png), consistent with truck-batch convention (rail batches use carrier emails). [log:certify_datapoints.datapoints.Aggregate_Distance_Transported_AECN_to_Basco.value, certify_datapoints.datapoints.Distance_from_AECN_to_Basco.value]',
     'VR Sec 3.5, Transport Emissions Acctg v1.1'),
    ('3.6', 'Transport mode = tanker truck', 'Pass',
     'Certify components: "AECN to LA Tanker Truck Transport Process Emissions" + "AECN to LA Tanker Truck Transport Embodied Emissions" — 2 components (correct for truck batch). No rail components. [log:certify_components.activities_bio_oil_transport]',
     'Certify Components'),
    ('3.7', 'Billing/customs documents present and consistent', 'Pass',
     'BOL PDF bundle (single file "documents 2343-T.pdf") contains both BOL and commercial-invoice sides: page 2 Purchase Order Q42025 ($1,740,000 against PO Q32025); page 5 Commercial Invoice 2343-T dated March 18, 2026, 20.00 MT × $305/MT US$ = $6,549.76, customs broker Pacific Custom Broker (Terra Estep), CofA RS3-260318-1, PAPS TNDT511842. PAPS number "511842" matches the DR# 511842 on both scale tickets — cross-checks origin (Quebec border) to destination (Pilot Bunkie LA arrival weigh). [log:bol.page5_commercial_invoice.invoice_number, bol.page5_commercial_invoice.paps_number, bol.page5_commercial_invoice.paps_matches_scale_ticket_DR_number, scale_tickets.full_ticket.dr_number, bol.c_of_a_number]',
     'VR Appendix 1'),

    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder or Certify Sources', 'Pass',
     'SGS Certificate of Analysis "SR26-02231_Batch_2-180-185_COA (1).pdf" present in BOTH locations: Drive > Testing subfolder (drive_file_id 1qG8JNyROfr3qAXrx8gTQit6pFOR7WSdv) AND Certify Sources #5 Public. Multi-batch cert covering 2-180 through 2-185; page 1 of 6 dedicated to batch 2-180. [log:lab_results.certify_source_filename, lab_results.page_in_multi_batch_certificate, drive_folder_contents.items]',
     'VR Appendix 1, Biomass Feedstock Acctg v1.2'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon = 47.2% (ASTM D5291 Method C, lab cert page 1). AECN reference from live MRV_AECN_Analysis.xlsx Summary Statistics tab: filtered to Function=MRV, Offtake=AECN, 439 samples filtered to n=285. Mean 39.420350877%, SD 6.09332409%. 2-SD upper bound 51.6070%. 47.2% within range; z-score 1.2766. SGS # marker = standard "outside method precision study limits" annotation for bio-oil C/H/N, not a quality issue. [log:lab_results.carbon_pct, _derived_values.carbon_pct_within_2sd_range, _derived_values.carbon_pct_z_score, lab_results.carbon_outside_marker_note, live_source_verifications_2026_05_11.mrv_aecn_analysis_carbon_range]',
     'VR Sec 5.1'),
    ('4.3', 'Hydrogen and nitrogen reported and reasonable', 'Pass',
     'H = 8.2% (ASTM D5291 Method C); N = <0.75% (ASTM D5291 Method C). Both within normal bio-oil ranges. # marker on H and N = same SGS method-precision annotation as Carbon. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct]',
     'VR Sec 5.1'),
    ('4.4', 'Lab report references correct batch/sample ID', 'Pass',
     'CHN cert page 1: CLIENT ID = "BATCH 2-180", LOCATION = "BASCO LOUISIANA", SAMPLED 26-Mar-2026 16:15 (= one day after Basco scale-weigh 3-25-26 + injection 4-1-26), ANALYSED 03-Apr-2026 → 04-Apr-2026 by Tiffany Scott (Lab Supervisor), SGS Order # 5437581. Cert # SR26-02231.001 = page-1 cert ID for this batch. [log:lab_results.certificate_number, lab_results.client_id, lab_results.sample_location, lab_results.sampled_date, lab_results.analysed_date, lab_results.lab_supervisor]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH is checked in 5.5. [log:_meta.oil_type]',
     'N/A'),
    ('4.6', 'Density above formation fluid threshold for safe injection', 'Pass',
     'Density at 15°C = 1.206 g/cm³ (ASTM D4052) — above 1.01 g/cm³ formation-fluid floor for safe geological injection. Also consistent with BOL page-3 density at 60°F = 1.1993 g/ml (sister value; small temp-dependent delta). [log:lab_results.density_15C_g_per_cm3, lab_results.density_above_formation_fluid_floor_1_01, bol.page3_shipping_details.density_60F_g_ml]',
     'PDD Sec A'),

    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes header: "Completion Date 4/1/2026", "Batch number 2-180". Matches Certify removal date (01 Apr 2026) and COBB injection_completion_date (2026-04-01). [log:ops_notes.completion_date, ops_notes.batch_number, cobb_row_61.L61_injection_completion_date, _meta.reporting_period]',
     'Ops Notes'),
    ('5.2', 'All scale ticket values correctly transcribed', 'Pass',
     'Ops Notes Truck 1 Full 79,640 lb = scale full gross 79,640 ✓. Truck 1 Empty 35,800 lb = scale empty gross 35,800 ✓. Truck 1 Injectate 43,840 lb = (79,640 − 35,800) ✓. Truck 1 Injectate kg 19,885.47328 = 43,840 × 0.453592 ✓. No transcription errors. [log:scale_tickets.full_ticket.gross_weight_lb, scale_tickets.empty_ticket.gross_weight_lb, ops_notes.injection_data.truck_1.full_mass_lb, ops_notes.injection_data.truck_1.empty_mass_lb, ops_notes.injection_data.truck_1.injectate_mass_lbs, ops_notes.injection_data.truck_1.injectate_mass_kg]',
     'Ops Notes'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch — no aqueous phase. [log:_meta.oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes/BOL', 'Pass',
     'COBB tab "Basco Injection -- COBB", CSV line 62 (row id verified by cell A = "2-180"): consumed_lot 2343-T_offload_1, BOL 2343-T, origin_quantity_kg 19,910 = BOL Qty Shipped, offloaded_quantity_kg 19,885.47328 = scale net = Ops Notes Total Injectate, quantity_consumed_in_injection 19,885 (rounded), injection_completion_date 2026-04-01, pH 3.1. All values reconcile cleanly. [log:cobb_row_61.cobb_row_id_verified, cobb_row_61.cobb_cell_A_value, cobb_row_61.E61_BOL_number, cobb_row_61.G61_offloaded_quantity_kg, cobb_row_61.H61_origin_quantity_kg, cobb_row_61.L61_injection_completion_date, cobb_row_61.M61_injection_ph]',
     'COBB Tracker'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes Injection Data row F = pH 3.1. Matches COBB row 61 col M = 3.1. pH check satisfied. [log:ops_notes.injection_data.truck_1.ph, cobb_row_61.M61_injection_ph]',
     'Ops Notes'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date = 4/1/2026. COBB injection_completion_date = 2026-04-01. Certify removal date = 01 Apr 2026. All three match. order_line_completed_on (2026-03-24 13:41:18 — purchase-order completion) is distinct from injection completion and matches expected: BOL date 2026-03-18 → border arrival 2026-03-20 → PO line completion at receipt → injection 2026-04-01. [log:ops_notes.completion_date, cobb_row_61.L61_injection_completion_date, cobb_row_61.I61_order_line_completed_on, _meta.reporting_period]',
     'Ops Notes / COBB'),
    ('5.7', 'No erroneous density measurements in Ops Notes', 'N/A',
     'Density field blank for AECN in Ops Notes Batch Composition — expected behavior. Density verified at lab (4.6) instead. [log:ops_notes.density_field_present_in_batch_composition, ops_notes.density_field_blank_for_aecn_expected]',
     'N/A'),

    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     'Certify Sources #1 "Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" Private, linked to "AECN Production Process Emissions" datapoint. Covers H2 2025 production period — applicable to batch 2-180 (BOL 2343-T Production Period 3-2026). [log:certify_sources_enumeration.0]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     'Certify Sources #2 "BH 2025 LCA w Stack Emissions.xlsx" Private, linked to "AECN Production Process Emissions" datapoint. [log:certify_sources_enumeration.1]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     'Certify Sources #4 "Supporting GHG data 31Dec2025 S.xlsx" Private, linked to "AECN Production Process Emissions" datapoint. [log:certify_sources_enumeration.3]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Component modal "AECN pyrolysis (from truck loads) - process emissions" INPUTS: AECN Production Process Emissions = 0.104 kgCO₂e/kg (Certify modal precise; Datapoints display rounds to 0.10). KB current value = 0.10402 kgCO₂e/kg (H2 2025). Modal value reconciles to 0.10402 within rounding. [log:certify_uncertainty_per_component.aecn_pyrolysis_process_emissions.ef_kgCO2e_per_kg, certify_datapoints.datapoints.AECN_Production_Process_Emissions.precise_value]',
     'Certify Datapoints'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Component modal "AECN pyrolysis (from truck loads) - embodied emissions" INPUTS: AECN Production Embodied Emissions = 0.0212 kgCO₂e/kg (modal precise; Datapoints display rounds to 0.02). Matches KB current value 0.0212. [log:certify_uncertainty_per_component.aecn_pyrolysis_embodied_emissions.ef_kgCO2e_per_kg, certify_datapoints.datapoints.AECN_Production_Embodied_Emissions.precise_value]',
     'Certify Datapoints'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Both pyrolysis component modals read "Mass = Origin Bio-Oil Mass - AECN = 19,910 kg" (pre-sparging mass = BOL Qty Shipped). NOT injectate mass (19,629 kg post-sparging). Correct per skill spec — pyrolysis emissions were incurred to produce the full quantity. [log:certify_uncertainty_per_component.aecn_pyrolysis_process_emissions.mass_kg, certify_uncertainty_per_component.aecn_pyrolysis_embodied_emissions.mass_kg, certify_datapoints.datapoints.Origin_Bio_Oil_Mass_AECN.value_kg]',
     'Certify Components'),

    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate × carbon% × 3.667', 'Pass',
     'Independent recalc: 19,628.95 kg × 0.472 × 3.667 / 1000 = 19.62895 × 0.472 × 3.667 = 33.974 tCO₂e. Certify "Injection sequestration" = 33.974 tCO₂e — exact match. Carbon used as decimal 0.472 (not 47.2). Units: t × decimal × dimensionless = t. [log:_derived_values.gross_co2e_recalc_basis, _derived_values.gross_co2e_recalc_t, _derived_values.gross_co2e_certify_t, _derived_values.gross_co2e_match]',
     'GHG Stmt Sec E, Bio-oil Geol Storage v1.1'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'Activities deductions in Certify Calculation View total 8.014 t = sum of 4 components: AECN→LA Tanker Process 5.000 + AECN→LA Tanker Embodied 0.522 + AECN Pyrolysis Process 2.071 + AECN Pyrolysis Embodied 0.422 = 8.015 t (Components tab raw sum). Calc View carries one extra decimal (8.014). 0.001 t discrepancy = rounding only. All 4 components present, none missing. [log:certify_components.activities_total_t, certify_calculation_view.activities_t, _derived_values.activities_sum_recalc_t, _derived_values.activities_sum_diff_note]',
     'Certify Calculation View'),
    ('7.3', 'Uncertainty discount applied', 'Pass',
     'Certify Calculation View shows Uncertainty Discount = 187 kg, equal to 0.187 t. Independent variance-propagation recalc (Option B, S3.7.3): σ_total ≈ 0.186 t ≈ 187 kg at one-sigma. Matches within rounding. [log:certify_calculation_view.uncertainty_discount_kg, certify_calculation_view.uncertainty_discount_t, certify_uncertainty_per_component.uncertainty_discount_independent_recalc]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with GHG Statement', 'Pass',
     'Net = 33.974 + 5.000 − 8.014 − 0.187 = 30.773 t = Certify Calculation View Net CO₂e Removed 30.773 t (displayed 30.77). Exact match. [log:certify_calculation_view.math_check, certify_calculation_view.net_co2e_t, _derived_values.net_calc_t, _derived_values.net_certify_t, _derived_values.net_match]',
     'Certify Calculation View / GHG Stmt'),

    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 — Completeness: every AECN component has uncertainty on correct datapoint', 'Pass',
     '5 components checked: (a) Injection Sequestration has Carbon Content + Mass-of-Injectant uncertainty inputs ✓; (b) Tanker Truck Process has Mass-of-Load uncertainty ✓; (c) Tanker Truck Embodied has NO Mass-of-Load (correct — embodied is per-mile EF, not per-T-mi); (d) Pyrolysis Process has Mass uncertainty ✓; (e) Pyrolysis Embodied has Mass uncertainty ✓. Distance has no uncertainty (per spec — use longest Google Maps distance). All required components have uncertainty on the correct datapoints. [log:certify_uncertainty_per_component.injection_sequestration, certify_uncertainty_per_component.aecn_to_la_tanker_truck_transport_process_emissions, certify_uncertainty_per_component.aecn_to_la_tanker_truck_transport_embodied_emissions, certify_uncertainty_per_component.aecn_pyrolysis_process_emissions, certify_uncertainty_per_component.aecn_pyrolysis_embodied_emissions]',
     'Isometric Standard v2.0 S3.7'),
    ('7a.2', 'Layer 2 — Correctness: reported ± matches expected', 'Pass',
     'All 5 component modals opened in Certify; INPUTS section read directly. Expected values from live MRV_Uncertainty_Evidence_Cheat_Sheet.xlsx tab "326 Uncertainty V2": Carbon = .004 × Measured Value; Mass = 72.57 kg per discrete weight. Reported / expected:\n• Injection Seq Carbon Content: ±0.1888% / expected 0.004 × 47.2 = 0.1888 ✓\n• Injection Seq Mass of Injectant: ±72.57 kg / expected 72.57 (1 discrete weight) ✓\n• Truck Process Mass of Load: ±72.57 kg / expected 72.57 ✓\n• Pyrolysis Process Mass: ±72.57 kg / expected 72.57 ✓\n• Pyrolysis Embodied Mass: ±72.57 kg / expected 72.57 ✓\nAll match. [log:certify_uncertainty_per_component.injection_sequestration.carbon_content_uncertainty_pct, certify_uncertainty_per_component.injection_sequestration.carbon_content_match, certify_uncertainty_per_component.injection_sequestration.mass_match, certify_uncertainty_per_component.aecn_to_la_tanker_truck_transport_process_emissions.mass_match, certify_uncertainty_per_component.aecn_pyrolysis_process_emissions.mass_match, certify_uncertainty_per_component.aecn_pyrolysis_embodied_emissions.mass_match, live_source_verifications_2026_05_11.mrv_uncertainty_cheat_sheet]',
     'MRV Uncertainty Cheat Sheet'),
    ('7a.3', 'Layer 3 — Aggregate discount present and consistent', 'Pass',
     'Calc View shows aggregate Uncertainty Discount = 187 kg. Independent variance propagation from per-component inputs above yields σ = 0.186 t ≈ 187 kg at one-sigma. Aggregate discount is present, consistent with GHG Statement (Net = Gross + Adjustments − Activities − Discount). [log:certify_calculation_view.uncertainty_discount_kg, certify_uncertainty_per_component.uncertainty_discount_independent_recalc.sigma_t]',
     'Certify Calculation View'),

    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Mass 19.91 MT (origin) / 19.629 MT (injected) — typical AECN single-truck load (~20 MT contract). Carbon 47.2% within 2-SD range per live MRV_AECN_Analysis.xlsx Summary Statistics (mean 39.420350877, SD 6.09332409, n=285, z-score 1.2766). Loss 1.41% = sparging only (256.5 sparging + 24.5 kg scale-vs-BOL conservatism rounded). No outliers. [log:_derived_values.carbon_pct_within_2sd_range, ops_notes.mass_loss_summary.loss_pct, bol.authoritative_qty_shipped_mt, live_source_verifications_2026_05_11.mrv_aecn_analysis_carbon_range]',
     'GHG Stmt Sec C, VR Sec 3.5'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'Pass',
     'Ops Notes Loss row = 281.05 kg = 256.52 sparging + 24.5 kg scale-vs-BOL conservatism rounding. Exhaustive grep -i "spill" across BOL (5 pp), CHN (6 pp), BCU cert (1 p), Ops Notes CSV, COBB CSV row 61 returned no matches in any per-batch primary source. Sparging is operational (not a loss reportable as a spill); conservatism between BOL and scale is the smaller-of-two rule. [log:ops_notes.mass_loss_summary.loss_kg, ops_notes.mass_loss_summary.loss_pct, _derived_values.sparging_loss_kg, _derived_values.conservative_mass_min_basis, live_source_verifications_2026_05_11.spill_absence_search]',
     'GHG Stmt Sec C'),
    ('8.3', 'Inventory reconciliation: carryover oil documented', 'N/A',
     'Single-truck single-batch AECN — no multi-period or multi-batch inventory allocation. Origin Mass (19,910) − Injectate (19,628.95) − Loss (281.05) balances to zero remaining. [log:ops_notes.mass_loss_summary, bol.authoritative_qty_shipped_kg]',
     'N/A'),

    ('SECTION', '9. Isometric Certify — Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: gross injection sequestration matches internal gross', 'Pass',
     'Certify Injection sequestration = 33.974 tCO₂e. Independent recalc: Mass of Injectant 19.62895 t × Carbon Content 0.472 × 3.667 = 33.974 tCO₂e. Exact match. Component modal confirms inputs: Carbon Content 47.2% with ±0.1888 (= .004 × 47.2 per live MRV Uncertainty cheat sheet rule) and Mass of Injectant 19,628.95 kg with ±72.57 (= 1 discrete weight × 72.57 per cheat sheet). [log:certify_components.sequestrations.Injection_Sequestration.value_t, _derived_values.gross_co2e_recalc_t, certify_uncertainty_per_component.injection_sequestration, live_source_verifications_2026_05_11.mrv_uncertainty_cheat_sheet]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES — Transport: 2 components correct for AECN truck route', 'Pass',
     '2 transport components present (correct for truck batch — rail batches have 6). Component-level recalcs:\n• AECN→LA Tanker Truck Process (5.000 t): 19.910 t Origin Mass × 2,197 mi × 0.0001143 MTCO₂e/(t·mi) = 5.0008 t ✓ (Certify modal precise EF 0.1143 kgCO₂e/(t·mi))\n• AECN→LA Tanker Truck Embodied (0.522 t): 2,197 mi × 0.23756 kgCO₂e/mi (native precise per Standard EFs 2026 tab) = 521.82 kg = 0.522 t ✓\nNo other transport legs. [log:certify_uncertainty_per_component.aecn_to_la_tanker_truck_transport_process_emissions, certify_uncertainty_per_component.aecn_to_la_tanker_truck_transport_embodied_emissions, _derived_values.tanker_process_emissions_recalc_basis, _derived_values.tanker_embodied_emissions_recalc_basis]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES — Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport not separately accounted for this batch (typical). [log:_meta.oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES — Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from truck loads) - process emissions" (2.071 t) and "AECN pyrolysis (from truck loads) - embodied emissions" (0.422 t) present. Component-level recalcs:\n• Pyrolysis Process (2.071 t): 19,910 kg × 0.10402 kgCO₂e/kg = 2,071.1 kg = 2.071 t ✓ (Certify modal precise 0.104)\n• Pyrolysis Embodied (0.422 t): 19,910 kg × 0.0212 kgCO₂e/kg = 422.1 kg = 0.422 t ✓\nMass basis = Origin Bio-Oil Mass (pre-sparging) per Section 6.6. Truck-batch naming convention "(from truck loads)" matches Component naming. [log:certify_uncertainty_per_component.aecn_pyrolysis_process_emissions, certify_uncertainty_per_component.aecn_pyrolysis_embodied_emissions, _derived_values.pyrolysis_process_recalc_basis, _derived_values.pyrolysis_embodied_recalc_basis]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     '"BCUs - Applied to Bio-Oil Transport Process Emissions" of 5.000 t (i.e. 5,000 kgCO₂e) is the only applicable category for typical AECN truck batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify_components.adjustments_bio_oil_transport, certify_datapoints.datapoints.BCUs_Applied_to_Bio_Oil_Transport_Process_Emissions.value]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS — BCU quantity ≥ corresponding activity emission', 'Pass',
     'BCU 5.000 t = AECN→LA Tanker Truck Process emission 5.000 t (exact equality satisfies BCU ≥ Activity rule). Embodied transport emissions (0.522 t) are NOT BCU-eligible per protocol — confirmed not double-claimed. No over-application of BCU credit. [log:_derived_values.bcu_applied_t, _derived_values.bcu_vs_transport_process_pass_check, _derived_values.transport_process_sum_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO₂e. Correct for bio-oil geological storage. [log:certify_components.counterfactuals_total_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net 30.773 t (display 30.77) = 33.974 (seq) + 5.000 (BCU) − 8.014 (act) − 0.187 (uncertainty). Independent: 33.974 + 5.000 − 8.014 − 0.187 = 30.773 ✓ exact. [log:certify_calculation_view.net_co2e_t, certify_calculation_view.math_check, _derived_values.net_match]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     'Filename hygiene (Garrett-side, NOT verifier-impacting). 4 items in Certify Sources opened and content-verified, but filenames are non-descriptive: (a) "Screenshot 2026-02-23 at 11.29.10 AM.png" (#3) — actual content is a Feb-17-2026 email from Viridi Global LCA provider with Q3-Q4 2025 AECN CI reduction explanation, linked to AECN Production Process datapoint; (b) "Screenshot 2026-04-10 at 3.19.33 PM.png" (#9) — actual content is the GLEC framework Road transport reference page (Table 4 NA road values), linked to Truck Transport Fuel Use datapoint; (c) "Carbon emission factor" (#14, no extension) — actual content is "Standard Emission Factors + Calculations (4).xlsx", a 2025-vintage snapshot, linked to AECN Production Embodied datapoint (embodied value 0.02116 unchanged 2025-->2026 so functionally OK); (d) "2-180 Full Empty Ticket (1).jpg" (#8) — redundant "Full" prefix on the Empty ticket filename. Content of each source verified against live primary sources; only the filenames are non-descriptive. Action: Garrett to rename for verifier clarity. [log:certify_sources_enumeration.2.generic_filename_flag, certify_sources_enumeration.8.generic_filename_flag, certify_sources_enumeration.13.generic_filename_flag, certify_sources_enumeration.7.filename_typo_flag, live_source_verifications_2026_05_11.glec_road_transport_screenshot, live_source_verifications_2026_05_11.viridi_global_lca_email_screenshot, live_source_verifications_2026_05_11.source_14_carbon_emission_factor, live_source_verifications_2026_05_11.standard_efs_sheet_2026_tab]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Sources tab shows 14 source-datapoint links. Per Document Location Rule, presence in Certify Sources is sufficient for documents not also in Drive (and vice versa). All VR Appendix 1 docs present: BOL+Invoice (#10 documents 2343-T.pdf), CHN cert (#5 multi-batch 2-180 to 2-185, also in Drive > Testing subfolder), AECN LCA CI (#1), LCA w stack emissions (#2), Supporting GHG data (#4), Scale tickets (#7 Full, #8 Empty, also in Drive > Scale Tickets subfolder), BCU certificate (#11 Charm-A4-2024-10-24-63-1976.pdf), Distance evidence (#12 AECN to Basco.png), Truck Embodied EF source (#13), plus 4 items flagged in 9.9. Drive folder root has Ops Notes Sheet + Scale Tickets subfolder (2 JPGs) + Testing subfolder (1 CHN cert PDF) = 4 Drive files total. Net cross-references: 4 of the 14 Certify sources are also in Drive (Ops Notes #6 + Full scale ticket #7 + Empty scale ticket #8 + CHN cert #5); 10 are Certify-only. [log:certify_sources_tab_total, certify_sources_enumeration, drive_folder_contents.items]',
     'Certify Sources'),
]


def build_workbook():
    # Pre-build audit gate — fail fast before writing the xlsx
    log = json.loads(SOURCE_READS_PATH.read_text())
    failures = validate_rows(ROWS, log)
    if failures:
        raise BuildAborted(
            f"Pre-build audit found {len(failures)} citation gap(s). xlsx NOT written.\n"
            + format_failures(failures)
        )

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
    ws.cell(row, 1, 'Net CDR (Certify, displayed)').font = Font(bold=True); ws.cell(row, 2, '30.77 tCO2e (Calculation View precise: 30.773)')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'Clean batch — math reconciles exactly across all 4 components: 19.62895 t × 0.472 × 3.667 = 33.974 t Seq; 8.014 t Activities (Transport 5.522 + Pyrolysis 2.493); 5.000 t BCU (= exact transport process); 0.187 t uncertainty → 30.773 t Net = Certify 30.77 displayed. Carbon 47.2% within range (+1.28 SD). All component recalcs match Certify modal values. Mass chain: scale net 19,885.47 kg (conservative MIN(scale, BOL 19,910)) → sparging 256.52 → injectate 19,628.95. BOL page-3 + page-4 weighbridge concur at 19,910. All uncertainty modals show ±72.57 kg per leg / ±0.1888% Carbon. Single direct AECN→Basco truck route, no rail leg, no allocation needed.')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '9.9 (Garrett-side filename hygiene, NOT verifier-impacting): (a) 2 non-descriptive screenshot filenames in Certify Sources — "Screenshot 2026-02-23 at 11.29.10 AM.png" and "Screenshot 2026-04-10 at 3.19.33 PM.png"; (b) "Carbon emission factor" (no extension/descriptor) linked to AECN Production Embodied Emissions; (c) "2-180 Full Empty Ticket (1).jpg" — redundant "Full" prefix on the Empty ticket. Content of each source verified correct; only filenames non-descriptive.')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-180/Batch_2-180_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    build_workbook()
