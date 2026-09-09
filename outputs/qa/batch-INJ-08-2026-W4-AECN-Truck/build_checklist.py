#!/usr/bin/env python3
"""Build INJ-08-2026-W4-AECN-Truck (direct AECN->Basco truck) QA checklist."""
import sys
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

sys.path.insert(0, "skills/qa/batch-qa-aecn/scripts")
from checklist_lib import build_with_validation

HEADER_FILL = PatternFill("solid", fgColor="D6E4F0")
FAIL_FILL   = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL   = PatternFill("solid", fgColor="FFF2CC")
FLAG_FONT   = Font(color="996600")
NA_FONT     = Font(color="808080", italic=True)
BOLD        = Font(bold=True)
WRAP        = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

ROWS = [
 ("INJ-08-2026-W4-AECN-Truck — AECN Direct Truck Batch QA","Reviewer: Claude QA Agent  |  Date: 2026-08-31  |  Injection Site: Basco 6  |  Oil Type: AECN (direct truck)  |  Period: 16 Aug 2026 to 22 Aug 2026  |  Certify GHG entry rmv_1M103GTGP1S0BB07","SECTION","",""),
 ("Scope","Direct AECN->Basco truck removal for the week (4 truck BOLs: 2471-T, 2472-T, 2474-T, 2477-T). This is a SEPARATE Certify GHG entry from the AECN-rail weekly removal already QA'd for the same week (INJ-08-2026-W4, rmv_1M10397551S0CB5R) -- the two share the same Drive folder and Ops Notes workbook but different tabs ('AECN Truck' vs 'AECN Rail') and different Certify removals. Net CDR 101.640 tCO2e. [log:vvb_guidance.week4_direct_truck_table_row] [log:batch_id]","SECTION","",""),

 ("1. Batch Folder Completeness","","SECTION","",""),
 ("1.1","Batch folder / evidence set named with batch ID","Pass","Drive folder path 'Injection Batch Data/W4'; Ops Notes 'AECN Truck' tab B2 = 'INJ-08-2026-W4'; COBB batch_id_col_a = 'INJ-08-2026-W4_bio_oil' on all 4 rows (605-608). Certify removal period 16-22 Aug 2026 = Ops Notes Week End (2026-08-22). [log:ops_notes.batch_id_cell_B2] [log:cobb.rows] [log:ops_notes.week_end]","VR Appendix 1"),
 ("1.2","Scale Tickets subfolder present and populated","N/A","Drive 'Scale Tickets > AECN Truck' subfolder contains the 4 BOL PDFs (legacy subfolder naming), not scale tickets -- wellhead scale tickets are not required for direct AECN truck deliveries per the documented 2026-05-26 methodology change (Ops Notes row-10 cell comment, read in full: 'Mass Used = Sum BOL kg per the 2026-05-26 BOL-as-MOBI methodology; wellhead scale tickets are not required for direct trucks. The former Scale Full / Scale Empty / Cargo columns were deleted from the AECN Truck sheet on 2026-08-26.'). All 4 BOLs present and individually opened (see Section 3). [log:ops_notes.row10_C_cell_comment] [log:bols._primary_source_opened]","VR Appendix 1"),
 ("1.3","Testing subfolder present with lab results","Pass","Drive 'Testing' subfolder contains 'CHARM INDUSTRIAL - 08-2026-W4 AECN + QOWV (SR26-05110.001-002).pdf', opened and read in full (page 1 = SR26-05110.001, this batch's AECN sample; page 2 = QOWV, out of scope). [log:lab_results._primary_source_opened] [log:lab_results.certificate_number]","VR Appendix 1"),
 ("1.4","Ops Notes present and complete","Pass","Weekly master workbook 'INJ-08-2026-W4 Ops Notes' (8 tabs); 'AECN Truck' and 'Summary' tabs read in full including every cell comment, via openpyxl without data_only=True. [log:ops_notes._primary_source_opened] [log:ops_notes.sheet_names]","VR Appendix 1"),
 ("1.5","Injection site confirmed Basco 6, no Vaulted references","Pass","All 4 BOLs (opened) route BioEnergie AE Cote-Nord Canada (Port-Cartier, QC) -> CHARM Industrial Inc, 4687 LA-115, St Landry, LA 71367 (Basco). Searched for 'Vaulted' across every document opened this session (4 BOLs, lab CoA, Ops Notes AECN Truck + Summary tabs incl. comments, VVB Guidance full text) -- no reference found in any. [log:bols.2471-T] [log:bols.2477-T]","Basco verification"),

 ("2. Mass Determination (BOL-basis, no scale tickets)","","SECTION","",""),
 ("2.1","Full and empty scale ticket images present per truckload","N/A","No scale tickets exist for direct AECN truck deliveries under the documented 2026-05-26 methodology (see 1.2) -- BOL page-3 'Product Shipment Summary' is the authoritative mass source instead. [log:ops_notes.row10_C_cell_comment]","VR Sec 5.1"),
 ("2.2","Ticket dates within 2 weeks of injection","N/A","No scale tickets exist for this delivery mode (see 2.1). BOL loading dates (2026-08-15 for 2471-T, 2026-08-17 for 2477-T) and Ops Notes AECN-delivery dates (8/19, 8/19, 8/22, 8/21) both fall within days of the Certify injection_completion_date (2026-08-22) and COBB dates, well inside any reasonable window. [log:bols.2471-T] [log:bols.2477-T] [log:ops_notes.deliveries_ledger]","VR Sec 3.5"),
 ("2.3","Tractor & trailer numbers match between full and empty tickets","N/A","No scale tickets / tractor-trailer pairs exist for this delivery mode (see 2.1).","VR Sec 5.1"),
 ("2.4","BOL mass correctly transcribed into Ops Notes","Pass","All 4 BOL page-3 'Quantity sent in M.Tons at 60F' values individually opened and read this session -- not sampled: 2471-T=19.56 MT, 2472-T=19.87 MT, 2474-T=19.40 MT, 2477-T=20.05 MT. Every value matches Ops Notes column C exactly for its row. Page-1 header 'Quantity' figures observed on 2471-T (19.64 MT) and 2477-T (19.77 MT) are pre-load volumetric estimates, correctly NOT used -- exactly the documented pattern the Ops Notes cell comment describes. [log:ops_notes.deliveries_ledger] [log:bols.2471-T] [log:bols.2472-T] [log:bols.2474-T] [log:bols.2477-T]","VR Sec 5.1"),
 ("2.5","Injectate mass basis correctly derived from BOL sum","Pass","Σ4 BOL page-3 masses = 19,560+19,870+19,400+20,050 = 78,880 kg = Certify Bio-Oil Mass - AECN datapoint (78.880 t) exactly, and matches the VVB Guidance's own per-removal table ('Week 4 (direct truck): Pyrolysis mass (kg) = 78,880') to the kilogram. No scale-ticket MIN() comparison applies under the documented BOL-only methodology (see 2.1). [log:_derived_values.bol_sum_kg] [log:_derived_values.bol_sum_note] [log:vvb_guidance.week4_direct_truck_table_row]","GHG Stmt Sec C"),
 ("2.6","1.29% sparging deduction applied","Pass","Recomputed 78,880 kg x 0.0129 = 1,017.552 kg = Ops Notes rollup Sparging Loss exactly. [log:_derived_values.sparging_loss_recalc_kg] [log:_derived_values.sparging_loss_recalc_note]","GHG Stmt Sec C"),
 ("2.7","Mass values consistent across BOLs, Ops Notes, COBB, Certify","Flag","BOL sum (78,880 kg) = Certify Bio-Oil Mass - AECN (78.880 t); MOBI recomputed with 0.195% filtration also applied (151.8317736 kg) gives 77,710.61623 kg = Certify Mass of Injectant (77.711 t) exactly. COBB origin_quantity_kg matches the BOL on all 4 rows exactly. However, COBB's separate quantity_consumed_in_injection/offloaded_quantity_kg field diverges from origin_quantity_kg on 2 of 4 rows (2472-T: -265.75 kg; 2477-T: -382.25 kg) by amounts that do not cleanly reconcile to sparging-only or sparging+filtration math computed from the Ops Notes per-delivery figures -- see 5.4. The Certify-authoritative datapoints reconcile directly to the BOLs/Ops Notes independent of this COBB field. [log:_derived_values.filtration_loss_recalc_kg] [log:_derived_values.mobi_recalc_kg] [log:_derived_values.mobi_recalc_note] [log:cobb.origin_quantity_kg_vs_bol_check]","VR Sec 5.1"),

 ("3. Bills of Lading & Transportation","","SECTION","",""),
 ("3.1","All truck BOLs present","Pass","All 4 BOLs (2471-T, 2472-T, 2474-T, 2477-T) individually uploaded to Certify Sources (not merely Ops-Notes-hyperlinked); all 4 individually opened and read this session -- not sampled. [log:certify_sources_tab_total] [log:bols._primary_source_opened]","VR Appendix 1"),
 ("3.2","Rail-leg BOL destination = SOPOR railyard","N/A","Direct truck route, no rail leg -- destination is Basco directly (see 3.4).","VR Appendix 1"),
 ("3.3","BOL mass matches or exceeds reported injectate mass","Pass","BOL sum 78,880 kg exceeds reported injectate mass (Mass of Injectant, post sparging+filtration losses) 77,710.61623 kg by exactly the documented loss total. [log:_derived_values.mobi_recalc_kg] [log:_derived_values.mobi_total_loss_kg] [log:_derived_values.mobi_total_loss_pct] [log:_derived_values.mobi_total_loss_note]","VR Sec 3.5"),
 ("3.4","Origin and destination correct on BOLs","Pass","All 4 BOLs (page 1, opened): origin BioEnergie AE Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier, Quebec G5B 2V9; destination CHARM Industrial Inc, 4687 LA-115, St Landry, LA 71367 (Basco). Consistent across all 4. [log:bols.2471-T] [log:bols.2477-T]","PDD Sec A"),
 ("3.5","Transport distance verified per route-map source, EFs at full precision","Pass","Route map 'AECN to Basco.png' (opened, Google Maps) shows origin/destination matching the BOLs exactly with a ~35-36hr long-haul truck route consistent with the applied ~2,197mi. Distance independently corroborated by two reconciling calcs at full-precision live-sheet EFs: Process 78.880t x 2,197mi x 0.0001143 MTCO2e/(t.mi) = 19.8083t = Certify Transport Process 19.808t exactly; Embodied 2,197mi x 0.23756 kgCO2e/mi = 0.521919t = Certify Transport Embodied 0.522t. [log:route_map_check._primary_source_opened] [log:_derived_values.transport_process_recalc_t] [log:_derived_values.transport_process_recalc_note] [log:_derived_values.transport_embodied_recalc_t] [log:_derived_values.transport_embodied_recalc_note] [log:standard_ef_sheet] [log:standard_ef_sheet.row6_truck_process_tanker] [log:standard_ef_sheet.row11_truck_embodied_tanker]","Transport Emissions Acctg v1.1"),
 ("3.6","Transport mode = tanker truck, 2 components present","Pass","2 transport components present in Certify (direct-truck expectation, not 6 like a rail batch): 'AECN to LA Tanker Truck Transport Process Emissions - AECN' (19.808t) and '...Embodied Emissions - AECN' (0.522t), both modals opened directly. [log:certify_components._primary_source_opened] [log:certify_components.transport_process_t] [log:certify_components.transport_embodied_t]","Certify Datapoints"),
 ("3.7","Billing / BOL details consistent","Pass","Page 1 individually opened and read on all 4 BOLs -- not sampled. All 4 carry Production Period '#08-2026', matching ship-to/from blocks, and a signed Ctrl Room Operator field (Dieu Tazi on 2471-T/2472-T, Sylvia Marcoux on 2474-T/2477-T). 2474-T additionally shows Customer PO 'Q4-2025' and Tariff code '2707.99.9090'. No print-typo or cross-shipment mismatch found on any of the 4. [log:bols.2471-T] [log:bols.2472-T] [log:bols.2474-T] [log:bols.2477-T]","VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing","","SECTION","",""),
 ("4.1","CHN/CoA present","Pass","SGS Certificate of Analysis SR26-05110.001, weekly composite AECN sample, sampled 2026-08-24 17:00, received 2026-08-26 10:20, completed 2026-08-26 15:15, signed Rachel Oxley (Laboratory Supervisor). [log:lab_results._primary_source_opened] [log:lab_results.certificate_number]","VR Appendix 1"),
 ("4.2","Carbon content checked against historical AECN range","Pass","Carbon 40.4% (ASTM D5291 Method C), read directly. MRV_AECN_Analysis.xlsx Summary Statistics tab opened directly this session (Data filtered to Function=MRV, Offtake=AECN, 439 samples): mean 39.420350877193%, SD 6.09332409018271%, n=285. 40.40% is ~0.16 SD above the mean -- comfortably inside range, not an outlier. The '#' flag on the cert ('outside test method limits and/or analytical range used in method precision study') is a generic SGS lab-method caveat appearing on Carbon/Hydrogen for both samples on this cert -- not a Charm-side outlier signal. [log:lab_results.carbon_pct] [log:lab_results.carbon_sgs_method_flag] [log:mrv_aecn_analysis_carbon_range]","Biomass Feedstock Acctg v1.2"),
 ("4.3","Hydrogen / nitrogen / viscosity / acid number reported and reasonable","Pass","Hydrogen 7.9%, Nitrogen <0.75%, Kinematic Viscosity @40C 15.45 cSt, Acid Number 84 mg KOH/g -- all read directly, all present and within plausible AECN ranges. [log:lab_results._primary_source_opened]","Biomass Feedstock Acctg v1.2"),
 ("4.4","Lab report references correct batch/sample ID","Pass","Cert Client ID '08-2026-W4 AECN' matches this batch/week exactly, and matches the Ops Notes Summary tab 'Composite Sample ID' field verbatim ('08-2026-W4 AECN'). [log:lab_results.client_id] [log:ops_notes.summary_tab]","VR Sec 5.1"),
 ("4.5","pH/conductivity (aqueous phase)","N/A","AECN is not aqueous phase; pH is checked in Section 5.5. [log:oil_type]","UIC Permit / LDENR"),
 ("4.6","Density above formation-fluid floor for safe injection","Pass","Density 1.204 g/cm3 at 15C -- above the 1.01 g/cm3 formation-fluid floor. [log:lab_results.density_g_cm3_15C]","VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency","","SECTION","",""),
 ("5.1","Correct batch ID and injection date","Pass","Ops Notes 'AECN Truck' tab batch ID 'INJ-08-2026-W4'; Week End 2026-08-22 = Certify removal period end 22 Aug 2026. [log:ops_notes.batch_id_cell_B2] [log:ops_notes.week_end]","-"),
 ("5.2","BOL values correctly transcribed","Pass","Every BOL's page-3 mass value transcribed correctly into the Ops Notes deliveries ledger -- verified value-by-value against the opened BOL images for all 4 deliveries (2.4). [log:ops_notes.deliveries_ledger]","VR Sec 5.1"),
 ("5.3","Oil/aqueous phase mass reconciliation","N/A","This Certify removal is AECN-only (direct truck); the week's QOWV/Aqueous totes are a separate removal. [log:oil_type]","-"),
 ("5.4","COBB values present and matched per delivery","Flag","All 4 relevant COBB rows found on the 'Basco Injection -- COBB' tab (rows 605-608), cell A confirmed = 'INJ-08-2026-W4_bio_oil' before extracting any value. origin_quantity_kg matches the BOL exactly on all 4 rows. But quantity_consumed_in_injection/offloaded_quantity_kg diverges from origin_quantity_kg on 2 of the 4 rows (2472-T: 19,604.24624 vs 19,870 kg, -265.75 kg; 2477-T: 19,667.74912 vs 20,050 kg, -382.25 kg) by amounts not cleanly explained by sparging-only (1.29%) or sparging+filtration combined math -- worth Garrett's review of the COBB/Manufacturo-side inventory-draw logic, though it does not affect any Certify-facing value (which reconciles directly to the BOLs and Ops Notes independent of this COBB field). [log:cobb._primary_source_opened] [log:cobb.rows] [log:cobb.origin_quantity_kg_vs_bol_check]","-"),
 ("5.5","pH measurement noted, within target range","Flag","pH column (E10:E13) is blank on all 4 deliveries in the Ops Notes AECN Truck tab, with no cell comment explaining the gap; COBB's injection_ph field is likewise blank on all 4 rows. This matches the exact same week-wide template gap already found and flagged on the sibling AECN Rail removal for this week (both Rail and Truck tabs blank, no VVB Guidance coverage). pH is not among the 10 Certify datapoints, so this does not affect the reported Net CDR value. [log:ops_notes.section2_rollup_row28] [log:cobb.rows]","-"),
 ("5.6","Completion date present and matches COBB","Pass","All 4 COBB rows carry injection_completion_date = 2026-08-22, matching the Ops Notes Week End exactly. [log:cobb.rows] [log:ops_notes.week_end]","-"),
 ("5.7","No erroneous density measurement","N/A","Density field in Ops Notes Batch Composition is expected to be blank for AECN (density is measured on the lab CoA instead -- see 4.6). [log:oil_type]","VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation","","SECTION","",""),
 ("6.1","AECN process emissions LCA CI spreadsheet present","Pass","Certify Sources includes 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jan2026 to 30Jun2026.xlsx', linked to the Pyrolysis Process CI datapoint -- one of the 3 documents the VVB Guidance doc states supports the H2 2026 factor, and correctly period-specific (Jan-Jun 2026). [log:certify_sources_tab_total] [log:vvb_guidance.evidence_docs_note]","VR Appendix 1"),
 ("6.2","LCA with stack emissions file present","Pass","Certify Sources includes 'FH 2026 LCA w Stack Emissions.xlsx' -- the stack-emissions calculation document referenced by the VVB Guidance and matching the live Standard EF sheet's H2 2026 tab source citation exactly ('FH 2026 LCA w Stack Emissions'). Minor filename oddity: 'FH' rather than the more natural 'H1' abbreviation, but the linkage and content are confirmed correct against the live sheet. [log:certify_sources_tab_total] [log:standard_ef_sheet.row4_h2_2026_process]","VR Appendix 1"),
 ("6.3","Supporting GHG data file present","Pass","Certify Sources includes 'Supporting GHG data 30Jun2026 S.xlsx' -- matches the VVB Guidance's cited 'vendor's supporting greenhouse gas data as at 30 June 2026'. [log:certify_sources_tab_total] [log:vvb_guidance.evidence_docs_note]","VR Appendix 1"),
 ("6.4","AECN pyrolysis process EF matches current value, at full precision","Pass","Live Standard EF sheet 'H2 2026 AECN Process Emissions' tab cell I12 = 0.1371171258 t CO2e/t bio-oil, exactly matching the value shown in the Certify component modal. 78.880t x 0.1371171258 = 10.8159t = Certify Pyrolysis Process 10.816t exactly. The VVB Guidance's own worked table lists 'Week 4 (direct truck): Pyrolysis mass 78,880 kg, additional process emissions 795 kg CO2e' -- matching this removal's mass to the kilogram. [log:standard_ef_sheet.h2_2026_tab_i12] [log:_derived_values.pyrolysis_process_recalc_t] [log:_derived_values.pyrolysis_process_recalc_note] [log:vvb_guidance.week4_direct_truck_table_row]","Certify Datapoints"),
 ("6.5","AECN pyrolysis embodied EF applied, at full precision, matches its own cited source","Flag","Certify's Pyrolysis Embodied component modal shows the applied carbon emission factor as 0.0212 kgCO2e/kg (full precision, read directly). But the live Standard EF sheet's current '2026' tab (F5) AND the actual attached Certify source file itself ('Standard Emission Factors + Calculations (4).xlsx', downloaded and read directly) both show 0.02116 (0.02115941123) for 'Embodied Emissions for AECN Oil' -- the datapoint value does not match its own cited source. 78.880t x 0.0212 = 1.672256t = Certify's displayed 1.672t exactly (confirming 0.0212 is what's in use); 78.880t x 0.02116 = 1.6691t (a 0.0029t / ~0.17% discrepancy). Immaterial to Net CDR and conservative in direction (higher EF entered = more emissions = lower reported net, not an over-credit), but a genuine value mismatch against the cited primary source worth Garrett's correction. [log:certify_components.pyrolysis_embodied_uncertainty] [log:standard_ef_sheet] [log:standard_ef_sheet.row5_embodied_aecn] [log:certify_attached_ef_source_stale_check] [log:certify_attached_ef_source_stale_check.attached_file_2025_tab_row4_embodied_aecn] [log:certify_attached_ef_source_stale_check.finding] [log:_derived_values.pyrolysis_embodied_recalc_using_live_sheet_ef_t] [log:_derived_values.pyrolysis_embodied_recalc_using_applied_ef_t]","Certify Datapoints"),
 ("6.6","Pyrolysis EF mass basis = pre-sparging Origin Bio-Oil Mass","Pass","Both pyrolysis component modals (opened) use 'Bio-Oil Mass - AECN' = 78,880 kg (pre-sparging, pre-filtration), not the post-deduction Mass of Injectant (77,710.616 kg). Correct per methodology. [log:certify_components.pyrolysis_process_uncertainty] [log:certify_components.pyrolysis_embodied_uncertainty]","Certify Components"),

 ("7. Gross-to-Net Calculation","","SECTION","",""),
 ("7.1","Gross CO2e = injectant mass x carbon x 3.667","Pass","77,710.61623 kg (Mass of Injectant) x 0.404 (carbon decimal) x 3.667 / 1000 = 115.1258 t = Certify Injection Sequestration 115.126 t (matches within rounding). [log:_derived_values.gross_co2e_recalc_t] [log:_derived_values.gross_co2e_recalc_note]","GHG Stmt Sec E"),
 ("7.2","Process + transport emissions correctly deducted","Pass","Activities recomputed = pyrolysis subtotal (10.816+1.672=12.488, matching Certify's own 'Pyrolysis or other process' subtotal) + transport subtotal (19.808+0.522=20.330, matching Certify's own 'Bio-oil transport' subtotal) = 32.818 t = Certify Components/Calculation-View Activities (32.818t) exactly. [log:certify_components.pyrolysis_process_t] [log:certify_components.pyrolysis_embodied_t] [log:certify_components.pyrolysis_subtotal_t] [log:certify_components.transport_process_t] [log:certify_components.transport_embodied_t] [log:certify_components.transport_subtotal_t] [log:certify_calculation_view.activities_t]","GHG Stmt Sec E"),
 ("7.3","Uncertainty discount applied","Pass","Uncertainty Discount 476 kg (0.476 t) present in Calculation View (~0.41% of gross). Note: this discount's correctness depends in part on the Mass-of-Product uncertainty input flagged in 7a.2 as understated -- see cross-reference there. [log:certify_calculation_view.uncertainty_discount_kg]","Isometric Standard S3.7"),
 ("7.4","Net removals internally consistent","Pass","Internal recompute: 115.126 + 19.808 - 32.818 - 0.476 = 101.640 t = Certify displayed Net CO2e Removed 101.640 t exactly, no cross-tab rounding gap. Cross-check against the RP-level BCU Quant spreadsheet and GHG Statement is deferred, as the reporting period (16-22 Aug 2026) is still open. [log:certify_calculation_view.recompute_check] [log:_derived_values.net_recalc_t] [log:_derived_values.net_recalc_note]","GHG Stmt Sec E"),

 ("7a. Per-Component Uncertainty Verification","","SECTION","",""),
 ("7a.1","Completeness: every component carries uncertainty on the correct datapoint","Pass","Opened all 5 component modals directly: Injection Sequestration (Carbon Content + Mass of product), Transport Process (Mass of load + EF + Distance), Transport Embodied (Distance EF + Distance, correctly NO mass-of-load input -- embodied is per-mile not per-tonne-mile), Pyrolysis Process (Mass), Pyrolysis Embodied (Carbon EF + Mass). [log:certify_components._primary_source_opened]","Isometric Standard S3.7.3"),
 ("7a.2","Correctness: reported uncertainty matches expected calculation","Fail","Carbon content uncertainty is correct: 0.1616% = exactly 0.004 x 40.40%. Mass-of-load uncertainty is correct on Transport Process, Pyrolysis Process, and Pyrolysis Embodied: 290.28 kg = exactly 72.57 kg x 4 discrete BOL weighings, applied identically across all three components (Bio-Oil Mass - AECN, 78,880 kg). BUT Injection Sequestration's 'Mass of product' input uses a DIFFERENT datapoint (Mass of Injectant, 77,710.61623 kg -- the same 4-BOL basis after documented losses) with an uncertainty of only ±4.53592 kg -- a ~64x understatement relative to the ±290.28 kg (or a proportionally loss-scaled ~286 kg) that the same 4-discrete-weighing basis produces everywhere else on this removal. This is the single largest component in the removal (115.126 t of 101.64 t net) and no documented methodology change (VVB Guidance or Ops Notes comments, both read in full) was found to justify a smaller uncertainty specifically for Injection Sequestration's mass input on BOL-sourced direct-truck batches. [log:certify_components.injection_sequestration_uncertainty] [log:certify_components.transport_process_uncertainty] [log:certify_components.pyrolysis_process_uncertainty] [log:certify_components.pyrolysis_embodied_uncertainty] [log:_derived_values.mass_of_product_uncertainty_expected_kg] [log:_derived_values.mass_of_product_uncertainty_expected_note]","Isometric Standard S3.7.3"),
 ("7a.3","Discount presence and consistency","Pass","Aggregate Uncertainty Discount 0.476 t is present in the Calculation View and reconciles exactly with the Net CDR formula (7.3/7.4). Flagged only via 7a.2: if the Mass-of-Product uncertainty on Injection Sequestration is corrected upward per that finding, this discount would need to be recomputed larger (more conservative), which would not create a FAIL-direction concern but should be tracked to closure alongside 7a.2. [log:certify_calculation_view.uncertainty_discount_kg] [log:certify_calculation_view.recompute_check]","Isometric Standard S3.7"),

 ("8. Data Integrity & Anomaly Check","","SECTION","",""),
 ("8.1","No unexplained outliers in mass, carbon content, or calculated values","Pass","Carbon 40.40% within historical range (4.2); every BOL's mass reconciles BOL->Ops Notes (2.4); BOL-sum and per-delivery mass independently tie to Certify (2.5, 2.7). Every divergence found this session (COBB per-BOL gap 2.7/5.4, pH gap 5.5, embodied-EF source mismatch 6.5, mass-uncertainty understatement 7a.2) is explained/quantified/flagged, not unexplained. [log:lab_results.carbon_pct]","GHG Stmt Sec C"),
 ("8.2","Spills/losses documented and deducted","Pass","No spill or loss events documented anywhere in the Ops Notes AECN Truck tab (read in full, including all cell comments) or the RP VVB Guidance doc (read in full). The documented sparging (1.29%) and filtration (0.195%) deductions are routine, explained losses, not spills; no incident report is expected or required. [log:ops_notes] [log:vvb_guidance]","GHG Stmt Sec C"),
 ("8.3","Cross-week / carry-forward inventory documented","N/A","All 4 BOLs are delivered and fully consumed within this single week per COBB (no partial/residual truck loads); direct-truck batches carry no railcar-style cross-week carryover to reconcile. [log:cobb.rows]","VR Sec 3.5"),

 ("9. Isometric Certify — Removal Component Mapping","","SECTION","",""),
 ("9.1","Sequestration matches internal gross","Pass","Mass of Injectant 77,710.61623 kg x Carbon Content 40.40% x 3.667 = 115.1258 t = Certify Injection Sequestration 115.126 t (see 7.1). [log:certify_components.sequestration_t] [log:_derived_values.gross_co2e_recalc_note]","Certify Components"),
 ("9.2","Transport: process + embodied (2 components), full math shown","Pass","AECN to LA Tanker Truck Transport Process: 78.880t x 2,197mi x 0.0001143 MTCO2e/(t.mi) = 19.8083t = Certify 19.808t exactly. AECN to LA Tanker Truck Transport Embodied: 2,197mi x 0.23756 kgCO2e/mi = 521.919 kg = 0.521919t = Certify 0.522t. Bio-oil transport total = 19.808 (process) + 0.522 (embodied) = 20.330t = Certify Components 'Bio-oil transport' subtotal exactly. [log:_derived_values.transport_process_recalc_t] [log:_derived_values.transport_process_recalc_note] [log:_derived_values.transport_embodied_recalc_t] [log:_derived_values.transport_embodied_recalc_note] [log:certify_components.transport_process_t] [log:certify_components.transport_embodied_t] [log:certify_components.transport_subtotal_t] [log:standard_ef_sheet]","Certify Components"),
 ("9.3","Injection: LCS / sample transport","N/A","AECN requires no LCS pre-treatment at Basco; no LCS component on this entry. [log:oil_type]","Certify Components"),
 ("9.4","Pyrolysis: process + embodied present, full math shown","Flag","AECN pyrolysis (from truck loads) - process emissions: 78.880t x 0.1371171258 = 10.8159t = Certify 10.816t exactly. AECN pyrolysis (from truck loads) - embodied emissions: 78.880t x 0.0212 (value actually applied) = 1.672256t = Certify 1.672t exactly -- but the cited source document itself (and the live Standard EF sheet) shows 0.02116, which would give 1.6691t instead. Same finding as 6.5; cross-referenced here since this is the Certify component-mapping section. Mass basis correctly = pre-sparging Bio-Oil Mass - AECN (78,880 kg). [log:_derived_values.pyrolysis_process_recalc_t] [log:_derived_values.pyrolysis_embodied_recalc_using_applied_ef_t] [log:_derived_values.pyrolysis_embodied_recalc_using_live_sheet_ef_t] [log:certify_attached_ef_source_stale_check.finding]","Certify Components"),
 ("9.5","Reductions: applicable BCU categories populated","Pass","Certify's Components tree carries a 'BCU - Transport Process' reduction of 19.808t under 'Bio-oil transport', linked in Sources to a Certificate of Retirement (Charm-RetirementCertificate-RD-EACs-20251218.pdf, downloaded and read in full: Amazon.com Services LLC retiring 2,795 Renewable Diesel TERCs on behalf of Charm Industrial, Dec 18 2025, cert# TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000). This is the same pooled-certificate pattern used across multiple prior AECN batches; other BCU categories (injection diesel, injection waste, pre-treat diesel/waste) correctly do not apply absent a site-emission burden on this removal. [log:bcu_certificate._primary_source_opened] [log:bcu_certificate.note]","Certify Components"),
 ("9.6","BCU quantity must at least cover the corresponding transport process activity emission, no over-coverage","Pass","Transport process activity = 19.808 t. BCU (Constant CO2 reduction) = 19.808 t -- EXACT full coverage, no shortfall and no over-crediting. [log:certify_components.bcu_transport_process_t] [log:_derived_values.bcu_vs_transport_process_check]","Certify Components"),
 ("9.7","Counterfactuals zero per protocol","Pass","No counterfactual emission component present on this removal; bio-oil geological storage counterfactual is zero per protocol. [log:certify_components._primary_source_opened]","Certify Components"),
 ("9.8","Net removal matches internal calculation","Pass","Independent recompute 115.126 + 19.808 - 32.818 - 0.476 = 101.640 t = Certify displayed Net CO2e Removed 101.640 t exactly -- no cross-tab rounding gap. [log:certify_calculation_view.recompute_check] [log:_derived_values.net_recalc_note]","Certify Calculation View"),
 ("9.9","Descriptive source filenames","Pass","All 17 Certify Sources carry descriptive filenames -- no generic 'Screenshot...'/'image (NN).png' pattern found on this removal, unlike several sister weekly batches. Minor cosmetic note: 'FH 2026 LCA w Stack Emissions.xlsx' uses an unusual 'FH' prefix (see 6.2), content/linkage confirmed correct. [log:certify_sources_tab_total]","Certify Datapoints"),
 ("9.10","Sources match Drive / complete set","Pass","17 sources enumerated in full from the Certify Sources tab (single source of truth). Every datapoint's required source category present: mass -> 4 BOLs + Ops Notes; carbon -> lab CoA; pyrolysis CI -> 3 period-specific LCA/GHG documents; distance -> 3 route-map images + BOLs + Ops Notes; EFs -> Standard Emission Factors sheet (x3 uploads); BCU -> retirement certificate. [log:certify_sources_tab_total] [log:standard_ef_sheet]","Certify Sources"),
]

def build_workbook(rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "QA Checklist"
    ws.append(["Item","Check","Status","Notes / Evidence","Verifier Ref"])
    for c in ws[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    for (a,b,status,*rest) in rows:
        ev = rest[0] if rest else ""
        vr = rest[1] if len(rest)>1 else ""
        if status == "SECTION":
            ws.append([a,b,"","",""])
            r = ws.max_row
            for col in range(1,6):
                cell = ws.cell(r,col); cell.fill = HEADER_FILL; cell.font = BOLD; cell.alignment = WRAP; cell.border=BORDER
            continue
        ws.append([a,b,status,ev,vr])
        r = ws.max_row
        for col in range(1,6):
            ws.cell(r,col).alignment = WRAP; ws.cell(r,col).border = BORDER
        if status == "Fail":
            for col in range(1,6): ws.cell(r,col).fill = FAIL_FILL
        elif status == "Flag":
            for col in range(1,6): ws.cell(r,col).fill = FLAG_FILL; ws.cell(r,col).font = FLAG_FONT
        elif status == "N/A":
            for col in range(1,6): ws.cell(r,col).font = NA_FONT
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 40
    ws.column_dimensions["C"].width = 8
    ws.column_dimensions["D"].width = 100
    ws.column_dimensions["E"].width = 22

    # ---- Sheet 2: BOL mass reconciliation ----
    ws2 = wb.create_sheet("BOL Mass Reconciliation")
    hdr = ["BOL","Page-1 header est. (MT)","Page-3 Qty Shipped (MT)","Ops Notes col C (MT)","COBB origin_quantity_kg","COBB quantity_consumed_kg","Divergence (kg)"]
    ws2.append(hdr)
    for c in ws2[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    rows2 = [
        ("2471-T", 19.64, 19.56, 19.56, 19560, 19560, 0),
        ("2472-T", "-", 19.87, 19.87, 19870, 19604.24624, -265.75376),
        ("2474-T", "-", 19.40, 19.40, 19400, 19400, 0),
        ("2477-T", 19.77, 20.05, 20.05, 20050, 19667.74912, -382.25088),
    ]
    for r in rows2:
        ws2.append(list(r))
        for col in range(1,len(hdr)+1): ws2.cell(ws2.max_row,col).border=BORDER; ws2.cell(ws2.max_row,col).alignment=WRAP
    ws2.append(["TOTAL","","78.88","78.88","78880","78641.99536","-647.99536"])
    for col in range(1,len(hdr)+1):
        ws2.cell(ws2.max_row,col).font=BOLD; ws2.cell(ws2.max_row,col).fill=HEADER_FILL; ws2.cell(ws2.max_row,col).border=BORDER
    ws2.append([])
    ws2.append(["Note: COBB's quantity_consumed_in_injection field diverges from origin_quantity_kg (=BOL) on 2472-T and 2477-T by amounts not cleanly matching sparging (1.29%) or sparging+filtration (1.29%+0.195%) math computed from the Ops Notes per-delivery rows. Certify's authoritative datapoints (Bio-Oil Mass - AECN = BOL sum; Mass of Injectant = documented Ops Notes rollup formula) reconcile directly to the BOLs and Ops Notes independent of this COBB field -- see checklist items 2.7 / 5.4."])
    for cw,w in [("A",10),("B",22),("C",22),("D",22),("E",22),("F",26),("G",18)]: ws2.column_dimensions[cw].width=w

    # ---- Sheet 3: Certify-vs-Source evidence matrix ----
    ws3 = wb.create_sheet("Source Matrix")
    ws3.append(["Certify value","Required sources","Source-derived","Certify","Match"])
    for c in ws3[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    MATRIX = [
     ("Bio-Oil Mass - AECN","4 BOLs","19,560+19,870+19,400+20,050 = 78,880 kg","78.880 t","="),
     ("Mass of Injectant","BOLs + Ops Notes formula","78,880 - 1,017.552 (sparging) - 151.832 (filtration) = 77,710.616 kg","77.711 t","="),
     ("Carbon Content","Lab CoA SR26-05110.001","40.40%","40.40%","="),
     ("Injection Sequestration","Mass x Carbon x 3.667","77.71062 t x 0.404 x 3.667 = 115.1258 t","115.126 t","="),
     ("Pyrolysis Process","Live EF sheet H2-2026 I12 x mass","78.880 t x 0.1371171258 = 10.8159 t","10.816 t","="),
     ("Pyrolysis Embodied","Cited-source EF (0.02116) x mass","78.880 t x 0.02116 = 1.6691 t","1.672 t","≠ (0.0029t gap -- see 6.5; Certify actually uses 0.0212)"),
     ("Transport Process","Live EF sheet x mass x distance","78.880 t x 2,197 mi x 0.0001143 = 19.8083 t","19.808 t","="),
     ("Transport Embodied","Live EF sheet x distance","2,197 mi x 0.23756 = 0.521919 t","0.522 t","="),
     ("BCU / Reductions","Transport process sum >= BCU, no over-coverage","19.808 t transport process","19.808 t BCU","= (full coverage, no over-credit)"),
     ("Uncertainty Discount","Variance propagation","See 7a.2 -- Mass-of-Product input on Injection Sequestration understated","0.476 t","Flagged input, see 7a.2/7a.3"),
     ("Net CO2e Removed","Sequestrations + BCU - Activities - Uncertainty","115.126+19.808-32.818-0.476 = 101.640","101.640 t","="),
    ]
    for m in MATRIX:
        ws3.append(list(m))
        for col in range(1,6): ws3.cell(ws3.max_row,col).alignment=WRAP; ws3.cell(ws3.max_row,col).border=BORDER
    for cw,w in [("A",26),("B",30),("C",56),("D",14),("E",50)]: ws3.column_dimensions[cw].width=w

    return wb

DERIVED = {}

if __name__ == "__main__":
    out_path = "outputs/qa/batch-INJ-08-2026-W4-AECN-Truck/Batch_INJ-08-2026-W4-AECN-Truck_QA_Checklist.xlsx"
    source_reads_path = "outputs/qa/batch-INJ-08-2026-W4-AECN-Truck/batch_INJ-08-2026-W4-AECN-Truck_source_reads.json"
    build_with_validation(
        rows=ROWS,
        source_reads_path=source_reads_path,
        out_path=out_path,
        build_workbook_fn=build_workbook,
        derived_values=DERIVED,
    )
    print("saved", out_path)
    from collections import Counter
    tally = Counter(r[2] for r in ROWS if r[2] != "SECTION")
    print("tally:", dict(tally))
