#!/usr/bin/env python3
"""Build Batch 2-185 QA Checklist xlsx with FAIL/FLAG/N/A formatting and [log:KEY] citations."""

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Status fills/fonts
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

# Checklist rows: (item, check, status, evidence, verifier_ref)
ROWS = [
    # Header rows
    ('HEADER',),
    ('META', 'Batch ID', '2-185'),
    ('META', 'Reporting Period', 'Apr 2026 (Certify removal date 02 Apr 2026)'),
    ('META', 'Reviewer', 'Claude QA Agent'),
    ('META', 'Date', '2026-04-30'),
    ('META', 'Injection Site', 'Basco 6'),
    ('META', 'Oil Type', 'AECN'),
    ('META', 'Delivery Mode', 'Rail (railcar GPRX 5188, offload 4 of 4 — last batch on railcar)'),
    ('SPACER',),
    ('COLUMNS',),
    # Section 1
    ('SECTION', '1. Batch Folder Completeness'),
    ('1.1', 'Batch folder exists with correct naming', 'Pass',
     'Drive folder titled and accessed at id 1LkJifO6CPs5twu7wbZg_PXULew8Wws-G; contains "2-185 Ops Notes Rail" sheet, Testing subfolder, Scale Tickets subfolder. [log:_meta.drive_folder_url]',
     'VR Appendix 1'),
    ('1.2', 'Scale Tickets subfolder present and populated', 'Pass',
     'Drive > Scale Tickets contains 2-185_Full_Scale_Ticket.jpg and 2-185_Empty_Scale_Ticket.jpg (one offload truck-out for this batch — typical AECN rail batch). Both also uploaded to Certify Sources as PUBLIC. [log:scale_tickets.full_ticket.filename_drive, scale_tickets.empty_ticket.filename_drive]',
     'VR Appendix 1, Sec 5.1'),
    ('1.3', 'Testing subfolder present with required lab results', 'Pass',
     'Drive > Testing contains SR26-02231_Batch_2-180-185_COA.pdf (6-page SGS Certificate of Analysis covering batches 2-180 through 2-185). [log:lab_results._source]',
     'VR Appendix 1'),
    ('1.4', 'Ops Notes spreadsheet present and complete', 'Pass',
     '"2-185 Ops Notes Rail" Google Sheet present in Drive folder; owner garrett.lutz@charmindustrial.com; modified 2026-04-27. Batch Composition, BOLs Loaded, and offload table all populated; this batch = offload_4 (last batch on railcar). [log:ops_notes._source, ops_notes._modified_time]',
     'VR Appendix 1'),
    ('1.5', 'Injection site confirmed Basco 6, no Vaulted refs', 'Pass',
     'All sources reference Basco/Evangeline Parish; no Vaulted references in Ops Notes or Certify. Certify project = "Charm Bio-oil Geologic Storage". [log:_meta.injection_site, certify.project_name]',
     'PDD'),
    # Section 2
    ('SECTION', '2. Scale Tickets & Mass Determination'),
    ('2.1', 'Empty and full scale ticket images present', 'Pass',
     'Both PDFs/JPGs readable. Full ticket #1312226090763 dated 2026-03-31 13:30 Pilot Travel Center I-49 Bunkie LA, GROSS 56,650 lb. Empty ticket #1312226090765 dated 2026-03-31 15:11 same location, GROSS 29,280 lb. [log:scale_tickets.full_ticket, scale_tickets.empty_ticket]',
     'VR Sec 5.1'),
    ('2.2', 'Dates within 2 weeks of injection', 'Pass',
     'Scale tickets 2026-03-31; injection completion 2026-04-02. Within 2 days. [log:scale_tickets.full_ticket.date, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('2.3', 'Tractor and trailer numbers match between empty and full', 'Pass',
     'Full ticket: Tractor CH2, Trailer KL-188. Empty ticket: Tractor CH2, Trailer KL-188. Same vehicle weighed at full and empty. [log:scale_tickets.tractor_match, scale_tickets.trailer_match]',
     'VR Sec 5.1'),
    ('2.4', 'Net mass correctly calculated in Ops Notes', 'Pass',
     'POLICY-APPLIED LAST-OFFLOAD CONSERVATISM. 2-185 is offload_4 of 4 on railcar GPRX 5188 (last offload — Oil Left in Railcar = 0). BOL inbound aggregate = 26.01 + 26.00 + 26.01 = 78,020 kg (physical upper bound on what can be drawn from the railcar). Sum of all 4 offloads at raw scale-ticket values would be ~78,408 kg, exceeding the BOL aggregate by ~388 kg (physically impossible). Per Charm policy, the last offload absorbs the discrepancy: Cargo (kg) = BOL_aggregate − sum(prior offloads raw scale tickets) = 78,020 − 65,988.56 = 12,031.44 kg. This is what Ops Notes reports and what flows into Certify. Same conservatism principle as the truck rule (revert to BOL when scale > BOL), realized at last-offload time. See `lessons_learned.md` Failure Category 11 and `project_railcar_mass_policy.md`. [log:_meta, ops_notes, qa_reference_values]',
     'VR Sec 5.1'),
    ('2.5', 'Injectate mass uses conservative MIN(scale net, BOL mass)', 'Pass',
     'Rail-batch interpretation of conservatism: per SKILL.md, when scale-ticket sum across the railcar exceeds BOL inbound aggregate, the last offload is back-calculated to the BOL-cap remainder. Ops Notes Cargo (kg) for offload_4 = 12,031.44 kg implements this rule. Sparging (1.29%) applied to that policy-applied base gives Mass of Bio-Oil Injected = 11,876.23 kg, which is what Certify Mass of Injectant shows. Conservative pathway honored. [log:scale_tickets, ops_notes.offload_table.3.cargo_kg, certify.components.Injection Sequestration.mass_of_injectant_kg, qa_reference_values.policy_applied_last_offload_kg]',
     'VR Sec 5.1, GHG Stmt Sec C'),
    ('2.6', 'Sparging deduction applied correctly', 'Pass',
     'Sparging factor 0.0129 applied to the policy-applied Cargo (kg) base: 12,031.44 × 0.0129 = 155.21 kg sparging loss, leaving 11,876.23 kg injected. Arithmetic correct; base is correct under the rail last-offload conservatism rule (Section 2.4). [log:ops_notes.sparging_mass_loss_factor, ops_notes.offload_table.3]',
     'VR Sec 5.1'),
    ('2.7', 'Mass values consistent across scale tickets, Ops Notes, Certify', 'Pass',
     'Under rail last-offload policy, expected pattern is: Ops Notes Cargo (kg) = Certify Allocated Bio-Oil Mass = 12,031.44 (policy-applied), and Mass of Injectant = 11,876.23 (post-sparging). COBB by design carries raw operator-entered scale-ticket values (12,419.35 here, ≈ axle-sum scale-ticket math), and diverges from Ops Notes on the last-offload row. Operators have a consistent procedure (record raw scale tickets); MRV applies the policy downstream. The verifier looks at Ops Notes and Certify, not COBB. All four sources are internally consistent under the policy. [log:cross_check_summary.mass_chain]',
     'VR Sec 5.1'),
    # Section 3
    ('SECTION', '3. Bills of Lading & Transportation'),
    ('3.1', 'Truck BOLs present for each shipment', 'Pass',
     'All 3 inbound BOLs present in Certify Sources (PUBLIC): Documents Camion 2310-R Charm PO Q42025 (1).pdf, Documents Camion 2312-R Charm PO Q42025.pdf, Truck documents 2313-R.pdf. Per Document Location Rule, presence in Certify Sources is sufficient. [log:bol.bol_filenames_in_certify]',
     'VR Appendix 1'),
    ('3.2', 'Rail batch: 3 truck BOLs from AECN, destination = SOPOR', 'Pass',
     '3 BOLs (2310-R, 2312-R, 2313-R) inbound to SOPOR Quebec railyard. Matches rail-batch convention. [log:bol.n_bols, bol.bol_numbers, bol.destination]',
     'VR Appendix 1'),
    ('3.3', 'BOL mass >= reported injectate mass at railcar level', 'Pass',
     '3 BOL masses sum to 78.02 MT (26.01 + 26.00 + 26.01). Railcar received total = 78,020 kg (per Ops Notes Total Unloaded Mass). Inbound aggregate >= railcar received. Per-batch offload mass authority is scale tickets, not BOL. [log:bol.bol_total_mt_per_ops_notes, ops_notes.total_unloaded_mass_kg]',
     'Transport Emissions Acctg v1.1'),
    ('3.4', 'Origin and destination correct on BOLs', 'Pass',
     'Carrier route: AECN Quebec -> SOPOR (truck, 3 BOLs) -> Opelousas LA (rail) -> Basco 6 (truck, this batch offload_4). Three legs documented. [log:bol.carrier_route]',
     'VR Sec 3.5'),
    ('3.5', 'Transportation distances consistent with known AECN rail route', 'Pass',
     'AECN->SOPOR truck single = 173 km (107.5 mi); SOPOR->Opelousas rail = 2,199 mi; Opelousas->Basco truck = 42.9 mi. All match expected. Rail allocation for offload_4 = 339.11 mi (= 2199 * 0.1542). [log:certify.datapoints, ops_notes.distances, ops_notes.offload_table.3.rail_mi, qa_reference_values]',
     'VR Sec 3.5'),
    ('3.6', 'Transport mode = 6 components (3 process + 3 embodied) for rail', 'Pass',
     '6 transport components in Certify: AECN->SOPOR Truck Process+Embodied, SOPOR->Opelousas Rail Process+Embodied, Opelousas->Basco Truck Process+Embodied. All present. [log:certify.components]',
     'PDD'),
    ('3.7', 'Billing documents present and consistent with BOLs', 'Pass',
     'Documents Camion / Truck documents PDFs serve as both BOLs and billing for the 3 inbound legs (AECN convention). All 3 PUBLIC in Certify Sources. [log:bol.bol_filenames_in_certify]',
     'VR Appendix 1'),
    # Section 4
    ('SECTION', '4. Bio-Oil Composition & Testing'),
    ('4.1', 'CHN PDF present in Testing subfolder', 'Pass',
     'SR26-02231_Batch_2-180-185_COA.pdf (6 pages, SGS) present in Drive Testing subfolder AND Certify Sources. Page 6 covers batch 2-185. [log:lab_results._source, lab_results.page_in_pdf]',
     'VR Appendix 1'),
    ('4.2', 'Carbon content within expected AECN range', 'Pass',
     'Carbon content for batch 2-185 = 43.10%. Within AECN expected range (mean 39.42%, +/-2 SD ~27.2-51.6%). [log:lab_results.carbon_pct, lab_results.carbon_pct_in_AECN_range]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.3', 'Hydrogen and nitrogen values reported and reasonable', 'Pass',
     'Hydrogen 7.2%, Nitrogen <0.75%, Viscosity 14.79 cSt @ 40C, Acid Number 47 mg KOH/g, Density 1.206 g/cm3 @ 15C. All within typical AECN ranges. [log:lab_results]',
     'Biomass Feedstock Acctg v1.2'),
    ('4.4', 'Lab report references correct batch ID', 'Pass',
     'Certificate SR26-02231.006 explicitly labeled "BATCH 2-185" on page 6. Sampled 2026-03-31 11:15 at BASCO LOUISIANA. [log:lab_results.certificate_no, lab_results.batch_id_on_page]',
     'VR Appendix 1'),
    ('4.5', 'pH/conductivity (aqueous phase)', 'N/A',
     'AECN is not aqueous phase. pH/conductivity protocol does not apply at this stage (pH of injectate is recorded in Ops Notes — see Section 5.5). [log:_meta.oil_type]',
     'N/A'),
    # Section 5
    ('SECTION', '5. Ops Notes Accuracy & Internal Consistency'),
    ('5.1', 'Correct batch ID and injection date', 'Pass',
     'Ops Notes Rail header shows Batch number = 2-185, Completion Date = 4/2/2026. Matches Certify removal date and COBB injection_completion_date. [log:ops_notes.batch_id_in_sheet, ops_notes.completion_date]',
     'VR Sec 5.1'),
    ('5.2', 'Scale ticket values correctly transcribed to Ops Notes', 'Pass',
     'Full ticket: certified GROSS WEIGHT = 56,660 lb (= axle sum 9,800+24,040+22,820); empty ticket: GROSS = 29,280 lb (= axle sum). Both tickets internally consistent. Ops Notes Loaded Mass (lbs) = 56,660 matches the full ticket exactly; Unloaded Mass (lbs) = 29,280 matches the empty ticket exactly. Verified by direct image Read of both JPGs (Drive auto-OCR snippet had misread 56,660 as 56,650 — image pixels are primary). [log:scale_tickets.full_ticket, scale_tickets.empty_ticket, ops_notes.offload_table.3.loaded_lb, ops_notes.offload_table.3.unloaded_lb]',
     'VR Sec 5.1'),
    ('5.3', 'Oil and aqueous phase mass reconciliation', 'N/A',
     'AECN-only batch; no aqueous phase. [log:_meta.oil_type]',
     'N/A'),
    ('5.4', 'COBB values present and match Ops Notes', 'Flag',
     'COBB row 62 (cell A verified = "2-185") offloaded_quantity_kg = 12,419.35 kg vs Ops Notes offload_4 Cargo (kg) = 12,031.44 kg. **Divergence is by design.** COBB carries raw operator-entered scale-ticket values (operators have a consistent procedure to follow); MRV applies the rail last-offload conservatism downstream in Ops Notes (Section 2.4). The verifier looks at Ops Notes and Certify, not COBB. COBB BOL_number "2310-R, 2312-R, 2313-R" matches Ops Notes BOLs Loaded — content cross-check OK. **Adjacent issue for Garrett (not 2-185-specific):** COBB row 61 (sister batch 2-184) shows 21,457.08 kg, which doesn\'t match raw scale-ticket math (21,844.99 kg). Per Max, this looks like an Ops/Manufacturo automation glitch on the 2-184 COBB row — Max is handling directly with Garrett. Not verifier-impacting. Surfacing here so the data-provenance issue gets traced. [log:cobb.cobb_row_id_verified, cobb.cobb_cell_A_value, cobb.row_62_data.offloaded_quantity_kg, ops_notes.offload_table.3.cargo_kg, qa_reference_values.cobb_2_184_inconsistency_kg]',
     'VR Sec 5.1'),
    ('5.5', 'pH measurement noted', 'Pass',
     'Ops Notes offload_4 row pH = 3.0. COBB row 62 injection_ph = 3.0. Match. [log:ops_notes.offload_table.3.pH, cobb.row_62_data.injection_ph]',
     'VR Sec 5.1'),
    ('5.6', 'Completion date present and matches COBB', 'Pass',
     'Ops Notes Completion Date = 4/2/2026; COBB row 62 injection_completion_date = 2026-04-02. Match. [log:ops_notes.completion_date, cobb.row_62_data.injection_completion_date]',
     'VR Sec 5.1'),
    ('5.7', 'No erroneous density measurements', 'N/A',
     'Density field expected blank for AECN per protocol. Ops Notes Batch Composition does not include density entry — expected behavior. [log:_meta.oil_type]',
     'N/A'),
    # Section 6
    ('SECTION', '6. AECN Feedstock Emissions & Allocation'),
    ('6.1', 'AECN process emissions LCA CI spreadsheet present', 'Pass',
     '"Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx" PUBLIC in Certify Sources, linked to Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) datapoint. [log:certify.appendix_1_docs_present.AECN_LCA_CI_spreadsheet]',
     'VR Appendix 1'),
    ('6.2', 'LCA with stack emissions file present', 'Pass',
     '"BH 2025 LCA w Stack Emissions.xlsx" PUBLIC in Certify Sources, linked to AECN Pyrolysis Process Emissions datapoint. [log:certify.appendix_1_docs_present.LCA_with_stack_emissions]',
     'VR Appendix 1'),
    ('6.3', 'Supporting GHG data file present', 'Pass',
     '"Supporting GHG data 31Dec2025 S.xlsx" PUBLIC in Certify Sources, linked to AECN Pyrolysis Process Emissions datapoint. [log:certify.appendix_1_docs_present.supporting_GHG_data_file]',
     'VR Appendix 1'),
    ('6.4', 'AECN pyrolysis process EF matches current value', 'Pass',
     'Modal value 0.104 tCO2e/t (precise). KB current value = 0.10402 tCO2e/t (H2 2025). Within rounding. [log:certify.components.AECN pyrolysis (from rail loads) - process emissions.carbon_intensity_tCO2e_per_t, qa_reference_values.kb_aecn_pyrolysis_process_ef_precise]',
     'Standard EFs 2026 tab'),
    ('6.5', 'AECN pyrolysis embodied EF applied', 'Pass',
     'Modal value 0.02116 tCO2e/t. KB current value = 0.0212 tCO2e/t. Within rounding. [log:certify.components.AECN pyrolysis (from rail loads) - embodied emissions.carbon_intensity_tCO2e_per_t, qa_reference_values.kb_aecn_pyrolysis_embodied_ef_precise]',
     'Standard EFs 2026 tab'),
    ('6.6', 'Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging)', 'Pass',
     'Pyrolysis components apply 0.104 / 0.02116 to "Allocated Bio-Oil Mass - AECN via Rail" = 12,031.44 kg = Ops Notes offload_4 Cargo (kg). Cargo (kg) is the pre-sparging mass; sparging is applied at injection (Section 2.6). Methodology correct, even though the underlying mass value is wrong (Section 2.4). [log:certify.components.AECN pyrolysis (from rail loads) - process emissions.mass_kg_pre_sparging]',
     'Bio-oil Geol Storage v1.1'),
    # Section 7
    ('SECTION', '7. Gross-to-Net Calculation'),
    ('7.1', 'Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667', 'Pass',
     'Independent calc on policy-applied mass: 11.87623 t * 0.4310 * 3.667 = 18.770 tCO2e. Matches Certify Sequestrations 18.770 t exactly. Mass basis (11,876.23 kg = policy-applied 12,031.44 kg minus 1.29% sparging) is correct under the rail last-offload conservatism rule (Section 2.4). Carbon content 0.4310 from CHN PDF page 6. [log:certify.totals.sequestrations_t, certify.components.Injection Sequestration.mass_of_injectant_kg, lab_results.carbon_pct]',
     'GHG Stmt Sec E'),
    ('7.2', 'Process emissions correctly deducted', 'Pass',
     'All 9 activity components deducted: 3 transport process (AECN->SOPOR truck 0.148, SOPOR->Opelousas rail 0.685, Opelousas->Basco truck 0.059) + 3 transport embodied (0.012 + 0.011 + 0.010) + AECN pyrolysis process 1.251 + AECN pyrolysis embodied 0.255. Sum = 2.431 t (Certify shows 2.430 — within rounding). Each component math reconciles. [log:certify.components, certify.totals.activities_t, qa_reference_values.transport_process_sum_t]',
     'GHG Stmt Sec E'),
    ('7.3', 'Uncertainty discount correctly applied', 'Pass',
     'Discount = 0.138 t in net calc (Calculation View). Per Isometric Standard S3.7.3 Option B (Variance Propagation) computed from per-component +/- inputs. Magnitude reasonable for batch of this size. [log:certify.totals.uncertainty_discount_t]',
     'Isometric Standard v2.0 S3.7'),
    ('7.4', 'Net removals consistent with BCU Quant and GHG Statement', 'Pass',
     'Net = 17.094 tCO2e = 18.770 + 0.892 - 2.430 - 0.138 (sequestrations + BCUs - activities - uncertainty). All inputs are on the policy-correct mass basis (Section 2.4). Each component reconciles to its modal inputs. [log:certify.totals]',
     'GHG Stmt Sec E'),
    # Section 7a
    ('SECTION', '7a. Per-Component Uncertainty Verification'),
    ('7a.1', 'Layer 1 - Completeness: every required component has uncertainty input', 'Pass',
     'All mass-input components have +/-72.57 kg: Injection Sequestration (Mass of Injectant), AECN->SOPOR Truck Process (Mass of load), SOPOR->Opelousas Rail Process (Mass of load), Opelousas->Basco Truck Process (Mass of load), AECN Pyrolysis Process (Mass), AECN Pyrolysis Embodied (Mass). Embodied transport components correctly have NO mass input (per-mile, not per-T-mi). Carbon Content has uncertainty +/-0.1724% (= 43.1 * 0.004). [log:certify.components, cross_check_summary.uncertainty_per_component]',
     'Isometric Standard S3.7.3'),
    ('7a.2', 'Layer 2 - Correctness: reported +/- matches expected value', 'Pass',
     'Per FC9 per-removal framing: a per-batch offload removal is fixed by ONE outbound discrete weight at Basco offload, so +/-72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process). Verified by opening each component modal and reading the INPUTS section. Carbon content +/-0.1724% = 43.1 * 0.004 confirms standard 0.4% relative uncertainty. [log:certify.components.Injection Sequestration.carbon_content_uncertainty_check]',
     'KB Section 7a'),
    ('7a.3', 'Layer 3 - Discount presence in net calc and consistency with GHG Statement', 'Pass',
     'Aggregate uncertainty discount = 0.138 t in Calculation View. Visible in net formula (18.770 + 0.892 - 2.430 - 0.138 = 17.094). [log:certify.totals]',
     'Isometric Standard S3.7.3'),
    # Section 8
    ('SECTION', '8. Data Integrity & Anomaly Check'),
    ('8.1', 'No unexplained outliers in mass, carbon content, or calculated values', 'Pass',
     'Carbon (43.1%), distances, EFs, and mass values all within expected ranges. Ops Notes Cargo (kg) = 12,031.44 is the policy-applied last-offload value (Section 2.4) — the divergence from raw scale ticket math is expected and explained. Both scale tickets internally consistent (gross = axle sum). No unexplained anomalies. [log:lab_results.carbon_pct, certify.components, cross_check_summary.mass_chain]',
     'GHG Stmt Sec C'),
    ('8.2', 'Spills/losses documented; unrecovered mass deducted', 'N/A',
     'No spills/losses documented for this offload. Ops Notes Oil Left in Railcar = 0 (railcar fully drawn down). [log:ops_notes.oil_left_in_railcar_kg]',
     'N/A'),
    ('8.3', 'Last batch on railcar: N_offloads >= N_BOLs (FC9 conservatism check)', 'Pass',
     'GPRX 5188 fully drawn down with 4 offloads (sister batches 2-182, 2-183, 2-184, 2-185); 3 inbound BOLs (2310-R, 2312-R, 2313-R). 4 >= 3 satisfies the FC9 conservatism precondition: summed per-offload mass uncertainty (4 * 72.57 = 290.28 kg) >= inbound-weighing uncertainty (3 * 72.57 = 217.71 kg). Per-offload uncertainty framing is conservative. [log:_meta, qa_reference_values.fc9_summed_offload_uncertainty_kg, qa_reference_values.fc9_inbound_bol_uncertainty_kg]',
     'KB Section 8 / FC9'),
    # Section 9
    ('SECTION', '9. Isometric Certify - Removal Component Mapping'),
    ('9.1', 'SEQUESTRATIONS: Gross injection sequestration matches internal gross', 'Pass',
     'Certify Sequestration component = 18.770 t. Independent calc: 11.87623 t (Mass of Injectant) × 0.431 × 3.667 = 18.770 t. Mass input is the policy-applied figure post-sparging (Section 2.4). Carbon content matches CHN PDF (43.10%). Reconciles. [log:certify.components.Injection Sequestration]',
     'Certify Components'),
    ('9.2', 'ACTIVITIES - Transport: 6 components correct for AECN rail route', 'Pass',
     '6 transport components present with correct EFs and distances. Notably: rail embodied EF = 0.03113 kgCO2e/mi (= 0.0000311307 MTCO2e/mi 2026 value, NOT stale 0.0000352240). Sister 2-182 had stale value FAILed; 2-185 already updated. [log:certify.components, certify.datapoints]',
     'Certify Components'),
    ('9.3', 'ACTIVITIES - Injection: LCS and sample transport', 'N/A',
     'AECN does not require LCS pre-treatment. Sample transport emissions not separately accounted (typical for AECN rail batches). [log:_meta.oil_type]',
     'N/A'),
    ('9.4', 'ACTIVITIES - Pyrolysis: process + embodied entries present', 'Pass',
     'Both "AECN pyrolysis (from rail loads) - process emissions" (1.251 t) and "AECN pyrolysis (from rail loads) - embodied emissions" (0.255 t) present. Rail-batch naming convention (deliberate signal to VVB). [log:certify.components]',
     'Certify Components'),
    ('9.5', 'REDUCTIONS: applicable BCU categories populated', 'Pass',
     'BCU - Transport (0.892 t) is the only applicable category for typical AECN rail batches without site-emission burdens. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only for site-emission-burdened removals. [log:certify.components.BCU - Transport]',
     'Certify Components'),
    ('9.6', 'REDUCTIONS - BCU quantity >= corresponding activity emission', 'Pass',
     'BCU-Transport = 0.892 t = sum of 3 transport process activities (0.148 + 0.685 + 0.059 = 0.892). Exact match. BCU >= activity satisfied (Section 9.6 rule). Embodied emissions are NOT BCU-eligible per protocol — confirmed not double-claimed. [log:cross_check_summary.bcu_check]',
     'Bio-oil Geol Storage v1.1'),
    ('9.7', 'COUNTERFACTUALS: zero per protocol', 'Pass',
     'Total removal counterfactuals amount = 0 tCO2e (Components tab > Removal counterfactuals section). Correct for bio-oil geological storage. [log:qa_reference_values.counterfactuals_t]',
     'Bio-oil Geol Storage v1.1'),
    ('9.8', 'Net removal matches internal calculation', 'Pass',
     'Certify Net = 17.094 tCO2e = 18.770 + 0.892 - 2.430 - 0.138. Arithmetic reconciles; underlying mass is the policy-applied figure (Section 2.4). [log:certify.totals]',
     'Certify Calculation View'),
    ('9.9', 'All Datapoints have descriptive source names', 'Flag',
     '4 non-descriptive filenames in Certify Sources: "Screenshot 2026-04-10 at 3.19.33 PM.png" (Truck Transport EF), "Screenshot 2026-02-23 at 11.29.10 AM.png" (Pyrolysis Process EF support), "Screenshot 2026-01-27 125934.png" (Opelousas-Basco distance), "image (44).png" (SOPOR-Opelousas rail distance). Hygiene issue — content is correct but names are non-descriptive. Same 4 files appear on sister batches (shared rail-batch datapoints). [log:certify.non_descriptive_filenames]',
     'Certify Sources'),
    ('9.10', 'All Sources match files in batch folder on Drive', 'Pass',
     'Per Document Location Rule, sources in Certify Sources are sufficient. 19 distinct source files enumerated on the Sources tab (21 row instances; 2-185 Ops Notes Rail xlsx linked to 3 datapoints). All required Appendix 1 docs present (3 BOLs, AECN LCA CI, LCA with stack, Supporting GHG, Standard EFs). [log:certify.certify_sources_tab_total, certify.appendix_1_docs_present]',
     'Certify Sources'),
]


def build_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'QA Checklist'

    # Column widths
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
            # Standard row: (item#, check, status, evidence, verifier)
            item, check, status, evidence, verifier = entry
            ws.cell(row, 1, item)
            ws.cell(row, 2, check)
            ws.cell(row, 3, status)
            ws.cell(row, 4, evidence)
            ws.cell(row, 5, verifier)

            # Set borders + wrap
            for c in range(1, 6):
                cell = ws.cell(row, c)
                cell.border = BORDER
                cell.alignment = WRAP

            # Apply status formatting
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

            # Estimate row height from evidence length
            ev_len = len(evidence or '')
            est_lines = max(1, ev_len // 90 + evidence.count('\n'))
            ws.row_dimensions[row].height = max(20, min(est_lines * 14, 200))

            row += 1

    # Summary row at bottom
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
    ws.cell(row, 1, 'Net CDR (reported)').font = Font(bold=True); ws.cell(row, 2, '17.094 tCO2e')
    row += 1
    ws.cell(row, 1, 'Material findings').font = Font(bold=True); ws.cell(row, 2, 'NONE — Net CDR is correct under rail last-offload conservatism policy')
    row += 1
    ws.cell(row, 1, 'Hygiene flags').font = Font(bold=True); ws.cell(row, 2, '5.4 (COBB row 61 sister-batch 2-184 inconsistency for Garrett); 9.9 (4 non-descriptive Certify source filenames)')
    print(f'Pass={pass_count}, Fail={fail_count}, Flag={flag_count}, N/A={na_count}')

    out_path = '/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/qa/batch-2-185/Batch_2-185_QA_Checklist.xlsx'
    wb.save(out_path)
    print(f'Saved {out_path}')

if __name__ == '__main__':
    build_workbook()
