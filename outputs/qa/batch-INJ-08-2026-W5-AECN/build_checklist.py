#!/usr/bin/env python3
"""Build script for INJ-08-2026-W5-AECN QA checklist."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "skills/qa/batch-qa-aecn/scripts"))
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from checklist_lib import build_with_validation

HERE = Path(__file__).parent
SOURCE_READS = HERE / "batch_INJ-08-2026-W5-AECN_source_reads.json"
OUT = HERE / "Batch_INJ-08-2026-W5-AECN_QA_Checklist.xlsx"

DERIVED = {
    "gross_co2e_recalc_t": 437.169,
    "gross_co2e_recalc_calc": "309.6550734 t x 0.385 x 3.667 = 437.169",
    "mass_used_total_kg": 309655.0734,
    "mass_used_calc": "153160 (rail MOBI) + 156495.0734 (truck MOBI) = 309655.0734 kg",
    "truck_bol_sum_MT": 158.85,
    "truck_bol_sum_calc": "19.99+19.46+20.10+19.47+19.95+19.91+19.96+20.01 = 158.85 MT",
    "rail_gprx5188_bol_sum_kg": 77710,
    "rail_gprx5188_bol_calc": "25820+25840+26050 = 77710 kg",
    "rail_gprx5236_bol_sum_kg": 77900,
    "rail_gprx5236_bol_calc": "26040+26030+25830 = 77900 kg",
    "transport_process_sum_t": 51.431,
    "transport_process_sum_calc": "39.890 + 1.912 + 8.866 + 0.763 = 51.431",
    "aggregate_distance_calc": "2197 mi x 8 truck deliveries = 17576 mi",
    "embodied_recompute_truck_direct": "17576 mi x 1.609344 km/mi x 0.1476 kgCO2e/km = 4173.5 kg = 4.174 t vs Certify 4.175 t",
    "embodied_recompute_aecn_sopor": "644 mi x 1.609344 x 0.1476 = 153.0 kg = 0.153 t vs Certify 0.153 t",
    "embodied_recompute_rail": "4398 mi x 1.609344 x 0.0193 kgCO2e/km = 136.6 kg = 0.137 t vs Certify 0.137 t",
    "embodied_recompute_opel_basco": "686 mi x 1.609344 x 0.1476 = 163.0 kg = 0.163 t vs Certify 0.163 t",
    "carbon_uncertainty_calc": "0.004 x 38.5 = 0.154",
    "mass_uncertainty_calc": "72.57 kg x 16 discrete weighings (8 rail offloads + 8 truck deliveries) = 1161.12 kg",
    "rail_mass_uncertainty_calc": "72.57 kg x 6 BOL weighings = 435.42 kg",
    "truck_mass_uncertainty_calc": "72.57 kg x 8 BOL weighings = 580.56 kg",
    "sparging_rate_check": "1.29",
    "filtration_rate_check": "0.195",
    "mass_used_total_t": 309.6551,
    "mass_used_total_t_display": 309.655,
    "bol_page1_nominal_2473T": 20.41,
}

HDR_FILL = PatternFill("solid", fgColor="D6E4F0")
FAIL_FILL = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL = PatternFill("solid", fgColor="FFF2CC")
FLAG_FONT = Font(color="996600")
NA_FONT = Font(italic=True, color="808080")

# ROWS: (kind_or_item, check, status, evidence, verifier_ref)
ROWS = [
    ("HEADER", "Batch ID: INJ-08-2026-W5-AECN | Reporting Period: 2026-08-22 to 2026-08-29 | Reviewer: Claude QA Agent | Injection Site: Basco 6 | Oil Type: AECN (rail + direct truck) | Scope: Removal components only (site emissions out of scope per Max, 2026-08-06 precedent)", "", "", ""),
    ("SECTION", "1. Batch Folder Completeness", "", "", ""),
    ("1.1", "Batch folder exists with correct naming", "Pass", "Drive folder titled 'W5' under 'Injection Batch Data' parent, confirmed via folder path breadcrumb. [log:drive_folder_url]", "VR App. 1"),
    ("1.2", "Scale Tickets subfolder present and populated", "Pass", "Certify Sources tab shows 16 scale ticket PDFs (GPRX5188 LD1-4 + GPRX5236 LD1-4, full+empty each). All 16 individually opened and read this session. [log:scale_tickets._primary_source_opened]", "VR App. 1"),
    ("1.3", "Testing subfolder / lab results present", "Pass", "AECN, QOWV, SR26-05208.pdf opened in Certify Sources; Certificate SR26-05208.001, client order 08-2026-W5_AECN. [log:lab_results.certificate_number]", "VR App. 1"),
    ("1.4", "Ops Notes spreadsheet present and complete", "Pass", "INJ-08-2026-W5 Ops Notes.xlsx opened directly (Drive + Certify Sources); AECN Rail and AECN Truck tabs both fully populated. [log:ops_notes.file]", "VR App. 1"),
    ("1.5", "Injection site confirmed as Basco 6, no Vaulted references", "Pass", "Rail BOLs show destination WATCO/SOPOR->Opelousas->Basco route; truck BOLs ship to CHARM Industrial Inc, St Landry LA (Basco). No Vaulted references found in any of the 14 BOLs or Ops Notes, all individually opened and read this session. [log:bols.destination_check, bols]", "verify BOLs/Ops Notes/Certify"),

    ("SECTION", "2. Scale Tickets & Mass Determination", "", "", ""),
    ("2.1", "Empty and full scale ticket images present for each rail offload", "Pass", "All 16 rail scale ticket PDFs (8 offloads x full+empty) individually opened and read. [log:scale_tickets._primary_source_opened]", "VR Sec 5.1"),
    ("2.2", "Dates within 2 weeks of injection", "Pass", "Rail ticket dates 2026-08-24 to 2026-08-28; truck BOL dates 2026-08-16 to 2026-08-22; injection week 2026-08-22 to 2026-08-29. All within range. [log:scale_tickets.GPRX5188, scale_tickets.GPRX5236, bols.truck]", "VR Sec 3.5"),
    ("2.3", "Tractor and trailer match between empty and full tickets, each offload", "Fail", "7 of 8 rail offload pairs match (GPRX5188 offloads 1-4 all match: CH1/KL192, CH1/KL720, CH2/KL510, CH1/KL720 respectively; GPRX5236 offloads 1-3 match: CH1/KL188 all three). GPRX5236 offload_4 does NOT match: Full ticket tractor=CH2, Empty ticket tractor=CH1 (trailer KL188 identical on both). Checked VVB Guidance August 1-31 doc in full for coverage -- zero mentions of GPRX5236 or 'offload 4' anywhere in the document (only W1's GPRX5240/TILX200228 and W3's GPRX5139 substitutions are documented). Checked Ops Notes cell comments on AECN Rail rows 43-46 (GPRX5236) -- zero comments present (full-sheet comment scan found only 13 comments, all on rows 39-42/GPRX5188). No substitution was applied; the raw net from this mismatched pair (17,263.712 kg) flows unchanged into Ops Notes MOBI and Certify. [log:scale_tickets.GPRX5236.offload_4]", "VR Sec 5.1"),
    ("2.4", "Net mass correctly calculated in Ops Notes (rail)", "Pass", "All 8 offload nets independently recomputed from ticket images: e.g. GPRX5188 O1 = (74,140-28,900) lb x 0.453592 = 20,520.502 kg, matches Ops Notes F39 = 20520.50208 kg. All 8 offloads reconcile exactly. [log:scale_tickets.GPRX5188.offload_1, ops_notes.aecn_rail_tab.offload_table]", "GHG Stmt Sec C"),
    ("2.5", "Injectate mass uses conservative/policy value (rail last-offload back-calc)", "Pass", "GPRX5188: raw offload sum (77,791.028 kg) exceeds BOL aggregate (77,710 kg) by exactly 81.028 kg; back-calc correctly absorbed on offload_4 (the last offload) per documented FC11 policy: offload_4 MOBI = raw net - sparging - filtration - 81.028 kg uncertainty adj = 17,884.2495 kg. GPRX5236: raw offload sum (77,754.74064 kg) is UNDER the BOL aggregate (77,900 kg) by 145.25936 kg (genuine loss, not over-draw), so no back-calc applies -- confirmed correct per policy (back-calc only triggers when raw sum EXCEEDS BOL aggregate). [log:ops_notes.aecn_rail_tab.railcars_received, ops_notes.aecn_rail_tab.offload_table]", "GHG Stmt Sec C"),
    ("2.6", "Sparging deduction (1.29%) applied correctly", "Pass", "Rail: total sparging loss 2,005.495154 kg divided by mass used 155,464.7406 kg reduces to the standard rate of 1.29 percent exactly. Truck: 2,049.165 kg divided by 158,850 kg likewise reduces to 1.29 percent exactly. Both match the standard AECN sparging rate. [log:ops_notes.aecn_rail_tab.rollup_row65, ops_notes.aecn_truck_tab.rollup_row28, _derived_values.sparging_rate_check]", "GHG Stmt Sec C"),
    ("2.6a", "Filtration loss (0.195%) applied correctly (weekly-batching methodology)", "Pass", "Rail: 299.2455287 kg divided by (155,464.7406-2,005.495154) kg reduces to the standard rate of 0.195 percent exactly. Truck: 305.7616283 kg divided by (158,850-2,049.165) kg likewise reduces to 0.195 percent exactly. Matches current weekly filtration-loss methodology. [log:ops_notes.aecn_rail_tab.rollup_row65, ops_notes.aecn_truck_tab.rollup_row28, _derived_values.filtration_rate_check]", "Weekly methodology (project_weekly_timeblock_batching)"),
    ("2.7", "All mass values consistent across scale tickets/BOLs, Ops Notes, and Certify", "Pass", "Rail MOBI 153,160 kg plus Truck MOBI 156,495.0734 kg totals 309,655.0734 kg = 309.6551 t, matching Certify 'Mass of Injectant (per injection)' = 309.655 t (rounding) exactly. [log:_derived_values.mass_used_calc, _derived_values.mass_used_total_t, _derived_values.mass_used_total_t_display, certify_components.injection_sequestration.mass_input]", "VR Sec 5.1"),
    ("2.8", "Truck deliveries: BOL-as-MOBI methodology (no scale tickets required, per 2026-05-26 policy)", "Pass", "Ops Notes AECN Truck tab header states explicitly: 'Mass Used = Sigma BOL kg; scale tickets no longer required for direct trucks per 2026-05-26'. Independently confirmed against Garrett Lutz's actual Slack message (#mrv-ops-la, 2026-05-26 13:02:28 PDT): 'We can officially use the AECN BOL as the mass statement for all direct trucks and no longer need scale tickets! (For trucks only)... ONLY APPLIES TO TRUCKS, WE STILL NEED SCALE TICKETS FOR RAIL.' Date and scope match the Ops Notes header exactly -- not just the operator's internal restatement, the underlying policy announcement itself. [log:ops_notes.aecn_truck_tab.methodology_header, ops_notes.aecn_truck_tab.scale_ticket_policy_slack_corroboration]", "Ops methodology, confirmed 2026-05-26"),

    ("SECTION", "3. Bills of Lading & Transportation", "", "", ""),
    ("3.1", "Truck BOL(s) present for each shipment", "Pass", "All 8 truck BOLs (2473,2475,2476,2478,2479,2480,2482,2483-T) individually opened. [log:bols._primary_source_opened]", "VR App. 1"),
    ("3.2", "Rail: 3 BOLs per railcar, destination = SOPOR railyard", "Pass", "GPRX5188: BOLs 2447/2448/2449-R (3). GPRX5236: BOLs 2441/2442/2443-R (3). Page 1 of all six rail BOLs individually opened -- every one confirms Ship To = WATCO / Societe du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau Quebec (SOPOR). Not a sample; all 6 checked. [log:bols.destination_check]", "VR App. 1"),
    ("3.3", "BOL mass matches or exceeds reported injectate mass", "Pass", "Truck: sum of all 8 BOLs' page-3 'Qty shipped' = 158.85 MT, exactly matches Certify 'Bio-Oil Mass - AECN' = 158.850 t. Rail: GPRX5188 BOL sum 77,710 kg = Ops Notes Total Loaded exactly; GPRX5236 BOL sum 77,900 kg = Ops Notes Total Loaded exactly. Note: BOL page 1 shows a nominal/estimated 'Estimated Quantity Loaded' figure that does not match (e.g. 2473-T page 1 = 20.41 MT vs page 3 = 19.99 MT) -- page 3's weighed 'Qty shipped' is the authoritative figure and is what Ops Notes/Certify use throughout. [log:_derived_values.truck_bol_sum_calc, _derived_values.rail_gprx5188_bol_calc, _derived_values.rail_gprx5236_bol_calc, _derived_values.bol_page1_nominal_2473T]", "VR Sec 3.5"),
    ("3.4", "Origin and destination correct on all BOLs", "Pass", "Truck BOLs: BioEnergie AE Cote-Nord, Port-Cartier QC -> CHARM Industrial Inc, St Landry LA (confirmed on all 8, page 1 each). Rail BOLs: BioEnergie AE Cote-Nord -> WATCO/SOPOR, Baie-Comeau QC (confirmed on all 6, page 1 each). Both consistent with AECN routing. [log:bols.destination_check]", "PDD Sec A"),
    ("3.5", "Transportation distances consistent with known AECN routes", "Pass", "Aggregate truck distance = 2,197 mi x 8 deliveries = 17,576 mi, matches Certify 'Aggregate Distance Transported AECN to Basco' exactly. Allocated distances (AECN->SOPOR 644 mi, rail 4,398 mi, Opelousas->Basco 686 mi) all reproduce exactly from Ops Notes row 61 rollup and match Certify's three allocated-distance datapoints. [log:_derived_values.aggregate_distance_calc, certify_components.distances]", "Transport Emissions Acctg v1.1"),
    ("3.6", "Transport mode matches oil type/route (tanker=truck direct+SOPOR legs, railcar=SOPOR-Opelousas leg)", "Pass", "Certify shows 6 rail-path transport components (AECN-SOPOR truck process+embodied, SOPOR-Opelousas rail process+embodied, Opelousas-Basco truck process+embodied) plus 2 direct-truck components (AECN-LA tanker process+embodied) = 8 total, correct for a combined rail+direct-truck weekly batch. [log:certify_components.distances]", "Certify Datapoints"),
    ("3.7", "Billing documents present and consistent with BOL", "Pass", "Each truck/rail BOL doubles as its own billing document (Straight Bill of Lading + Analytical Details / weigh-ticket pages within the same PDF); all 14 individually opened end-to-end. [log:bols._primary_source_opened]", "VR App. 1"),

    ("SECTION", "4. Bio-Oil Composition & Testing", "", "", ""),
    ("4.1", "CHN analysis PDF present", "Pass", "SGS Certificate of Analysis SR26-05208.001 opened directly. [log:lab_results.file]", "VR App. 1"),
    ("4.2", "Carbon content within expected AECN range", "Pass", "Opened MRV_AECN_Analysis.xlsx Summary Statistics tab directly this session (not carried over from the knowledge base): filtered to Function=MRV, Offtake=AECN (439 samples), Carbon mean is 39.4204 percent, standard deviation 6.0933 percent, count 285 -- matching the KB-stated figures exactly to 2 decimals. Two-SD range is approximately 27.2 to 51.6 percent. Lab value 38.5 percent for this batch falls well within that range. [log:lab_results.carbon_pct, lab_results._primary_source_opened]", "Biomass Feedstock Acctg v1.2"),
    ("4.3", "Hydrogen and nitrogen values reported and reasonable", "Pass", "Hydrogen 7.5%, Nitrogen <0.75%, both within normal ranges for AECN pyrolysis oil. [log:lab_results.hydrogen_pct, lab_results.nitrogen_pct]", "Biomass Feedstock Acctg v1.2"),
    ("4.4", "Lab report references correct batch/sample ID", "Pass", "Certificate's Client Order Number field reads '08-2026-W5_AECN', matching this batch exactly. Sample date 2026-08-29 falls within the batch week (2026-08-22 to 08-29). [log:lab_results.client_order_number, lab_results.sample_date]", "VR Sec 5.1"),
    ("4.5", "pH/conductivity (aqueous phase)", "N/A", "AECN is not aqueous phase.", ""),
    ("4.6", "Density above formation fluid safe-injection threshold", "Pass", "Lab density = 1.204 g/cm3 at 15C, exceeds the formation-fluid density baseline. That baseline is independently sourced this session (not the internal knowledge-base restatement): Waypoint Analytical Lab Report 24-200-0020, 'Basco 6 SWD MRV' formation fluid sample (Lab No. 98021), downloaded and opened directly -- Report of Analysis, page 5: 'Specific Gravity 1.01 g/mL, ASTM D-1298-85'. Batch's 1.204 g/cm3 exceeds this measured formation-fluid baseline. [log:lab_results.density_g_cm3_at_15C, geology_density_threshold]", "UIC Permit / safe injection"),

    ("SECTION", "5. Ops Notes Accuracy & Internal Consistency", "", "", ""),
    ("5.1", "Correct batch ID and injection week in Ops Notes", "Pass", "AECN Rail and AECN Truck tab headers both read Batch ID 'INJ-08-2026-W5', Week Start 2026-08-22, Week End 2026-08-29. [log:ops_notes.file]", "verify header"),
    ("5.2", "Scale ticket values correctly transcribed into Ops Notes", "Pass", "All 8 rail offload Full/Empty lb values in Ops Notes columns D/E independently cross-checked against the actual ticket images -- exact match in all 16 cases (8 offloads x 2 tickets). [log:scale_tickets.GPRX5188, scale_tickets.GPRX5236]", "VR Sec 5.1"),
    ("5.3", "Oil and aqueous phase mass reconciliation", "N/A", "AECN-only batch, no aqueous phase.", ""),
    ("5.4", "COBB values present and match Ops Notes/Certify", "Flag", "Rail: 7 of 8 offload rows match exactly; GPRX5188 offload_1 diverges from Ops Notes by exactly -81.028 kg (the FC11 back-calc adjustment appears to be applied to offload_1 in COBB instead of offload_4, where Ops Notes/Certify correctly apply it) -- known COBB-vs-Ops-Notes divergence pattern, not verifier-impacting since Certify's Allocated Bio-Oil Mass derives from Ops Notes, not COBB. Truck: re-opened COBB columns H-S directly this session. Column H (origin_quantity_kg) -- the field that actually ties to the BOL/Ops Notes/Certify mass chain -- matches the Ops Notes BOL mass EXACTLY on all 8 truck rows (2475-T=19460, 2478-T=19470, 2480-T=19910, 2479-T=19950, 2482-T=19960, 2473-T=19990, 2483-T=20010, 2476-T=20100), zero deltas. The 76-247 kg divergence originally flagged here is in a different column, F (quantity_consumed_in_injection), which tracks partial/rolled-over consumption rather than delivered mass -- consistent with the Ops Notes A10 comment describing frac-tank carryover accounting for 2473-T/2475-T/2476-T (see 8.3, where the specific cited Slack source could not be independently located). Certify's own 'Bio-Oil Mass - AECN' (158.850 t) reconciles exactly and independently to the Ops Notes BOL sum via column H regardless, so this remains a COBB-side column-labeling item worth Garrett's attention (F is not the source-of-truth field, and reading it as one overstates the divergence), not a verifier-facing problem. [log:cobb.truck_divergence_finding, cobb.column_h_reconciliation, cobb.rail_rows]", "COBB tracker, Basco Injection -- COBB tab"),
    ("5.5", "pH measurement noted (all batches, all oil types)", "Pass", "pH = 2.93 recorded consistently across all 8 rail offloads and all 8 truck deliveries (same weekly composite sample). [log:ops_notes.aecn_rail_tab.rollup_row65, ops_notes.aecn_truck_tab.rollup_row28]", "GHG Stmt Sec C"),
    ("5.6", "Completion date present and matches COBB", "Pass", "COBB batch_id_col_a = 'INJ-08-2026-W5_bio_oil', located at rows 691-706, matching this batch. Column L (injection_completion_date) = 2026-08-29 for every one of these rows, exactly matching the Ops Notes Week End date (2026-08-22 to 2026-08-29). [log:cobb.batch_id_col_a, cobb.completion_date_check]", "VR Sec 3.5"),
    ("5.7", "No erroneous density measurements", "N/A", "Density field expected blank for AECN in Ops Notes Batch Composition -- expected behavior.", ""),

    ("SECTION", "6. AECN Feedstock Emissions & Allocation", "", "", ""),
    ("6.1", "AECN process emissions LCA CI spreadsheet present", "Pass", "FH 2026 LCA w Stack Emissions.xlsx present on Certify Sources tab, linked to Carbon Intensity - AECN Pyrolysis Process Emissions datapoint. [log:certify_sources_tab_total]", "VR App. 1"),
    ("6.2", "LCA with stack emissions file present", "Pass", "Same file as 6.1 (FH 2026 LCA w Stack Emissions.xlsx) -- title itself confirms stack-emissions content, present in Sources tab. [log:certify_sources_tab_total]", "VR App. 1"),
    ("6.3", "Supporting GHG data file / embodied calc sheet present", "Pass", "AECN Embodied Emissions Calc Sheet (1).pdf present in Certify Sources and independently opened -- content read directly (facility+transport embodied buildup). [log:certify_components.pyrolysis_embodied_ef._primary_source_opened]", "VR App. 1"),
    ("6.4", "AECN pyrolysis process EF matches current H2 2026 value", "Pass", "Certify's own component input shows precise EF 0.13712 tCO2e/t identically on both the rail and truck pyrolysis-process components (shared datapoint, internally consistent). Primary source independently opened and read this session on the 4th navigation attempt: the first 3 attempts failed (Certify preview download crashed 3 separate times; standalone source page rendered only a placeholder with no extractable cell content; no matching xlsx request was initially visible in network traffic), then browser_network_requests surfaced the direct signed download URL for this exact source. Downloaded FH 2026 LCA w Stack Emissions.xlsx and read it directly with openpyxl. Sheet1 cell I12 = 0.1371171258 MT CO2e/MT Bio Oil (= Stack Emissions 0.004065098 + Other Process Emissions from Vendor LCA 0.133052028), an exact match to Certify's displayed 0.13712. Primary source now genuinely opened and read, not inferred from Certify's display. [log:certify_components.pyrolysis_process_ef.blocked_primary_source]", "Certify Datapoints / Component Inputs"),
    ("6.5", "AECN pyrolysis embodied EF applied", "Pass", "0.0211594123 tCO2e/t confirmed directly from AECN Embodied Emissions Calc Sheet (1).pdf, primary source opened and read this session. Rail and truck embodied components both recompute consistently (3.293/155.610=0.02116; 3.368/158.850=0.02121). [log:certify_components.pyrolysis_embodied_ef]", "Certify Datapoints"),
    ("6.6", "Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)", "Pass", "Rail pyrolysis mass basis = 155,610 kg = BOL-loaded mass (pre-sparging); truck = 158,850 kg = Sigma BOL mass (pre-sparging). Both correctly pre-sparging, consistent with KB rule. [log:certify_components.pyrolysis_process_ef.rail_component, certify_components.pyrolysis_process_ef.truck_component]", "Certify Components"),

    ("SECTION", "7. Gross-to-Net Calculation", "", "", ""),
    ("7.1", "Gross CO2e = injectate mass x carbon wt% x 3.667", "Pass", "309.6550734 t x 0.385 x 3.667 = 437.169 tCO2e, exact match to Certify Injection Sequestration component. [log:_derived_values.gross_co2e_recalc_calc, certify_components.injection_sequestration.recalc]", "GHG Stmt Sec E"),
    ("7.2", "Process emissions correctly deducted", "Pass", "Pyrolysis process (21.337 rail + 21.782 truck), pyrolysis embodied (3.293 + 3.368), and all 8 transport process/embodied legs appear as Activities in the Calculation View, correctly subtracted from Sequestrations to reach Net. [log:certify_components.distances]", "GHG Stmt Sec E"),
    ("7.3", "Uncertainty discount correctly applied", "Pass", "Calculation view shows Uncertainty Discount present at 2.465 t, reducing Net CDR (Sequestrations 437.169 plus Adjustments 76.487 minus Activities 172.693 minus the Uncertainty Discount). [log:certify_components.calculation_view]", "Isometric Standard v2.0 S3.7"),
    ("7.4", "Net removals consistent with BCU Quant / GHG Statement", "Flag", "RP-level BCU Quant sheet / GHG Statement cross-check not performed at batch level (RP still open, week 5 of an in-progress August 2026 RP) -- standard deferral for an in-progress reporting period, consistent with prior weekly-batch precedent (W1-W4). [log:rp_status]", "RP BCU Quant.xlsx"),

    ("SECTION", "7a. Per-Component Uncertainty Verification", "", "", ""),
    ("7a.1", "Layer 1 - Completeness: every AECN component has uncertainty on the correct datapoint", "Pass", "Opened all 7 components requiring uncertainty verification directly this session: Injection Sequestration, AECN pyrolysis (rail) process, AECN pyrolysis (truck) process, and all 4 transport-process legs (AECN-LA direct truck, AECN-SOPOR truck, SOPOR-Opelousas rail, Opelousas-Basco truck). All 7 show uncertainty on the correct Mass/Carbon Content inputs; the 4 transport legs each reuse one of the two already-verified shared mass datapoints rather than carrying separate figures. [log:certify_components.injection_sequestration, certify_components.pyrolysis_process_ef, certify_components.transport_process_uncertainty]", "MRV Uncertainty+ Evidence Cheat Sheet"),
    ("7a.2", "Layer 2 - Correctness: reported +/- matches expected formula", "Pass", "Carbon Content: 38.5 +/-0.154% = 0.004 x 38.5 exactly. Mass of Injectant (aggregate): 309,655.07 +/-1,161.12 kg = 72.57 kg x 16 discrete weighings (8 rail offloads + 8 truck deliveries) exactly. Bio-Oil Mass - AECN via Rail: 155,610 +/-435.42 kg = 72.57 x 6 BOL weighings exactly, reused unchanged on all 3 rail-path transport legs (AECN-SOPOR truck, SOPOR-Opelousas rail, Opelousas-Basco truck). Bio-Oil Mass - AECN (truck): 158,850 +/-580.56 kg = 72.57 x 8 BOL weighings exactly, reused unchanged on the AECN-LA direct truck leg. Distance-traveled carries no uncertainty on any of the 4 transport legs, consistent with KB rule. All values opened directly in Certify component modals (7 of 7) and recomputed. [log:_derived_values.carbon_uncertainty_calc, _derived_values.mass_uncertainty_calc, _derived_values.rail_mass_uncertainty_calc, _derived_values.truck_mass_uncertainty_calc, certify_components.transport_process_uncertainty]", "Isometric Standard S3.7.3"),
    ("7a.3", "Layer 3 - Discount presence and consistency", "Pass", "Aggregate Uncertainty Discount is present in Calculation View at 2.465 t, consistent with the per-component inputs verified in 7a.1/7a.2. [log:certify_components.calculation_view]", "Isometric Standard S3.7.3"),

    ("SECTION", "8. Data Integrity & Anomaly Check", "", "", ""),
    ("8.1", "No unexplained outliers in mass, carbon content, or calculated values", "Flag", "GPRX5236 offload_4 tractor mismatch (see 2.3) is the one unexplained anomaly this session surfaced -- flagged there, cross-referenced here. All other mass/carbon/EF values reconcile cleanly with no unexplained variance. [log:scale_tickets.GPRX5236.offload_4]", "GHG Stmt Sec C"),
    ("8.2", "Any spills/losses documented, unrecovered mass deducted", "Pass", "GPRX5236 shows a 145.25936 kg (0.19%) railcar loss (raw offload sum under BOL aggregate) -- a normal, small in-transit loss, not a documented spill event. VVB Guidance's only disclosed spill event this RP (GPRX5139, Week 3, ~3,419 kg) does not involve either of this batch's railcars (GPRX5188, GPRX5236) -- confirmed by checking the full spill-disclosure table against this batch's railcar names. [log:ops_notes.aecn_rail_tab.railcars_received, vvb_guidance.spill_check]", "GHG Stmt Sec C"),
    ("8.3", "Inventory reconciliation / carryover documented (if applicable)", "Flag", "Ops Notes cell comment (A10) documents that 3 truck BOLs (2473-T, 2475-T, 2476-T) carried over from Week 4's frac tank, attributed to 'Brad (Slack, 2026-08-24)'. That documentation itself is present and legitimate -- an operator's own contemporaneous annotation. However, 11 distinct Slack searches this session (by sender name, by sender's user ID, by channel, by the exact phrase quoted in the comment, by each truck number, by the date, and a direct read of the one Slack thread from that exact date mentioning a named truck -- which turned out to be two photos with no text) could not locate the specific message described. Either it sits outside searchable Slack text (a DM, a huddle, an in-person conversation) or the comment's citation is imprecise. This does not affect Certify's reported value -- the underlying mass ties out independently via COBB column H regardless of the carryover explanation (see 5.4). Flagged as a citation-precision item for Garrett, not a mass or verifier-facing problem. [log:ops_notes.aecn_truck_tab.carryover_note, ops_notes.aecn_truck_tab.carryover_slack_source_search]", "VR Sec 3.5"),

    ("SECTION", "9. Isometric Certify - Removal Component Mapping", "", "", ""),
    ("9.1", "SEQUESTRATIONS: Gross injection sequestration matches internal gross", "Pass", "Certify Injection Sequestration = 437.169 tCO2e, matches independent recalculation exactly. [log:_derived_values.gross_co2e_recalc_calc]", "Certify Components"),
    ("9.2", "ACTIVITIES - Transport: process + embodied correct for all 8 legs (4 truck-mode, 4 rail-mode)", "Pass", "8 transport components present: AECN-LA direct truck (process 39.890 + embodied 4.175), AECN-SOPOR truck (1.912 + 0.153), SOPOR-Opelousas rail (8.866 + 0.137), Opelousas-Basco truck (0.763 + 0.163). Transport process total = 51.431 tCO2e. All 4 embodied legs independently recomputed from allocated distance x precise EF (not Certify's rounded display): 17,576 mi x 1.609344 x 0.1476 kgCO2e/km = 4.174 t; 644 mi x 1.609344 x 0.1476 = 0.153 t; 4,398 mi x 1.609344 x 0.0193 kgCO2e/km = 0.137 t; 686 mi x 1.609344 x 0.1476 = 0.163 t -- all four match Certify within rounding. All distances independently reconciled in item 3.5. [log:_derived_values.transport_process_sum_calc, _derived_values.embodied_recompute_truck_direct, _derived_values.embodied_recompute_aecn_sopor, _derived_values.embodied_recompute_rail, _derived_values.embodied_recompute_opel_basco]", "Certify Components"),
    ("9.3", "ACTIVITIES - Injection: LCS / sample transport correct", "N/A", "AECN does not require LCS pre-treatment (that applies to Aqueous only); no LCS component present for this batch, as expected.", "Certify Components"),
    ("9.4", "ACTIVITIES - Pyrolysis: both process and embodied entries present, correctly labeled for rail+truck", "Pass", "4 pyrolysis components present: 'AECN pyrolysis (from rail loads) - process/embodied emissions' (21.337 + 3.293) and 'AECN pyrolysis (from truck loads) - process/embodied emissions' (21.782 + 3.368), correctly split by delivery mode per rail-batch naming convention. [log:certify_components.pyrolysis_process_ef]", "Certify Components"),
    ("9.5", "REDUCTIONS: applicable BCU categories populated", "Pass", "Two BCU categories present and applicable to this batch's scope: 'BCUs - Applied to Bio-Oil Transport Process Emissions' (51.414 t) and 'BCU - Additional Transport' (0.556 t, site-emissions-adjacent, out of batch scope but present). Site-emission BCU categories (injection diesel, waste, well work) are out of scope for this QA per the established scope boundary. [log:certify_components.bcu_transport_coverage]", "Certify Components"),
    ("9.6", "REDUCTIONS - BCU quantity vs transport process activity (no over-coverage)", "Pass", "BCU = 51.414 t vs transport process sum = 51.431 t (39.890+1.912+8.866+0.763). Delta = -0.017 t (~0.03%), i.e. BCU is very slightly UNDER the process-activity sum -- not an over-coverage FAIL, effectively full coverage, immaterial. [log:_derived_values.transport_process_sum_calc, certify_components.bcu_transport_coverage]", "Certify Components / Calculation View"),
    ("9.7", "COUNTERFACTUALS: zero per protocol", "Pass", "Bio-oil geological storage counterfactual is zero, per protocol. [log:certify_removal_url]", "Certify Components"),
    ("9.8", "Net removal matches internal calculation", "Pass", "Net CDR for the removal-component scope ties to the independently-recomputed gross (437.169 t) minus verified Activities and Uncertainty Discount. [log:_derived_values.gross_co2e_recalc_calc]", "Certify Calculation View"),
    ("9.9", "All Datapoints have descriptive source names", "Pass", "All 14 BOL and 16 scale-ticket filenames are fully descriptive (BOL_XXXX-T/R.pdf, GPRXNNNN_LDN_FULL/EMPTY_ticketnumber.pdf). No generic 'Measurement XXXX' or 'IMG_001' style names found among the removal-component sources. [log:bols._primary_source_opened, scale_tickets._primary_source_opened]", "Certify Datapoints"),
    ("9.10", "All Sources match files in Drive/Certify", "Pass", "All 14 BOLs and 16 scale tickets independently opened via Certify Sources tab and confirmed to be genuine, correctly-named, batch-relevant documents. Certify Sources total = 81 (up from 79 mid-session due to an unrelated site-emissions addition). [log:certify_sources_tab_total]", "Certify Sources"),
]


def build_workbook(rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "QA Checklist"
    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 60
    ws.column_dimensions["C"].width = 10
    ws.column_dimensions["D"].width = 90
    ws.column_dimensions["E"].width = 30

    r = 1
    for row in rows:
        kind = row[0]
        if kind == "HEADER":
            ws.cell(row=r, column=1, value=row[1])
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
            ws.cell(row=r, column=1).font = Font(bold=True)
            ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
            r += 1
            continue
        if kind == "SECTION":
            ws.cell(row=r, column=1, value=row[1])
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
            cell = ws.cell(row=r, column=1)
            cell.font = Font(bold=True)
            cell.fill = HDR_FILL
            r += 1
            continue
        item, check, status, evidence, verifier = row
        ws.cell(row=r, column=1, value=item)
        ws.cell(row=r, column=2, value=check)
        ws.cell(row=r, column=3, value=status)
        ws.cell(row=r, column=4, value=evidence)
        ws.cell(row=r, column=5, value=verifier)
        for col in range(1, 6):
            ws.cell(row=r, column=col).alignment = Alignment(wrap_text=True, vertical="top")
        if status == "Fail":
            for col in range(1, 6):
                ws.cell(row=r, column=col).fill = FAIL_FILL
        elif status == "Flag":
            for col in range(1, 6):
                ws.cell(row=r, column=col).fill = FLAG_FILL
                ws.cell(row=r, column=col).font = Font(color="996600")
        elif status == "N/A":
            for col in range(1, 6):
                ws.cell(row=r, column=col).font = NA_FONT
        r += 1
    return wb


if __name__ == "__main__":
    build_with_validation(
        rows=ROWS,
        source_reads_path=SOURCE_READS,
        out_path=OUT,
        build_workbook_fn=build_workbook,
        derived_values=DERIVED,
    )
