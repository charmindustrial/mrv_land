#!/usr/bin/env python3
"""Build INJ-08-2026-W1 AECN weekly batch QA checklist."""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

HEADER_FILL = PatternFill("solid", fgColor="D6E4F0")   # section/sub-header — ONE color, never yellow/green
FAIL_FILL   = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL   = PatternFill("solid", fgColor="FFF2CC")
FLAG_FONT   = Font(color="996600")
NA_FONT     = Font(color="808080", italic=True)
BOLD        = Font(bold=True)
WRAP        = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

ROWS = [
 ("INJ-08-2026-W1 — AECN Weekly Batch QA", "Reviewer: Claude QA Agent  |  Date: 2026-08-25  |  Injection Site: Basco 6  |  Oil Type: AECN (rail)  |  Week: Sat 2026-07-25 to Sat 2026-08-01  |  Injected: 2026-08-01  |  Certify GHG entry rmv_1M0DVG8ZB1S05TY0","SECTION","",""),
 ("Scope","Time-block (weekly) batch = all AECN oil for the week, aggregated into ONE Certify GHG entry. This week AECN is ALL RAIL: 11 truck-out offloads from 3 railcars (GPRX5106 offloads 1-4, FULL; TILX200228 offloads 1-3, PARTIAL — offload_4 not yet occurred; GPRX5240 offloads 1-4, FULL). Net CDR 276.262 tCO2e. [log:railcars]","SECTION","",""),

 ("1. Batch Folder Completeness","","SECTION","",""),
 ("1.1","Batch folder / evidence set named with batch ID","Pass","Ops Notes header B2 = 'INJ-08-2026-W1'; Certify removal date 01 Aug 2026 = Ops Notes Week End. No separate per-batch Drive folder was provided or needed — all evidence (scale tickets, BOLs, lab CoA) is linked directly from Ops Notes cell hyperlinks and/or Certify Sources; Document Location Rule is satisfied via Certify Sources presence for every item checked below. [log:ops_notes.week_end] [log:removal_date]","VR Appendix 1"),
 ("1.2","Scale Tickets present and populated","Pass","All 21 available scale ticket PDFs opened and read directly (11 offloads across 3 railcars; GPRX5240 offload_1's empty ticket does not exist by design — see 2.5). [log:scale_tickets._primary_source_opened] [log:scale_tickets.tickets_opened_count]","VR Appendix 1"),
 ("1.3","Lab results present","Pass","SGS Certificate of Analysis SR26-04724.001 (AECN sample '08-2026-W1 AECN') opened in full, both pages read including method-limit footnote. [log:lab_results._primary_source_opened]","VR Appendix 1"),
 ("1.4","Ops Notes present and complete","Pass","Weekly master workbook 'INJ-08-2026-W1 Ops Notes' (8 tabs; Summary + AECN Rail read in full, including cell comments, via openpyxl without data_only). [log:ops_notes._primary_source_opened]","VR Appendix 1"),
 ("1.5","Injection site confirmed Basco 6","Pass","Lab cert location 'BASCO LOUISIANA'; all 9 BOLs route AECN (Port-Cartier, QC) -> SOPOR (Baie-Comeau) -> Opelousas -> Basco. [log:lab_results.certificate_number]","Basco verification"),

 ("2. Scale Tickets & Mass Determination","","SECTION","",""),
 ("2.1","Full and empty ticket images present per offload","Pass","21 of 22 possible tickets present and opened (CAT Scale, text-based PDFs, read directly — not OCR). GPRX5240 offload_1's empty ticket is documented as unrecoverable and substituted (2.5). [log:scale_tickets._primary_source_opened]","VR Sec 5.1"),
 ("2.2","Ticket dates within 2 weeks of injection","Pass","All ticket dates read: 2026-07-23 through 2026-07-31 vs injection 2026-08-01 — all within 14 days. [log:scale_tickets._primary_source_opened]","VR Sec 3.5"),
 ("2.3","Tractor & trailer numbers match between full and empty tickets","Flag","9 of 11 offloads match cleanly. TWO genuine, undocumented rig mismatches found on primary-source read: (1) TILX200228 offload_2 — full ticket 1312226209697 (tractor CH1 / trailer RL192, commodity field generic 'FREIGHT ALL KINDS', no railcar/offload identifier) vs empty ticket 1312226211738 (tractor CH2 / trailer KL188) — full tractor+trailer mismatch, no VVB Guidance coverage, no standard-tare substitution applied. (2) GPRX5240 offload_2 — full ticket 1312226210732 (CH1/RL192) vs empty ticket 1312226211739 (CH1/KL192) — trailer mismatch. GPRX5240 is a FULL railcar this week and its 4-offload total (78,041.86 kg) reconciles to within 88 kg of the 78,130 kg BOL aggregate, which corroborates offload_2's value despite the ticket ambiguity. TILX200228 is only PARTIALLY drawn down this week (offload_4 pending) so no equivalent railcar-level closure check is available yet for its offload_2. The trailer code 'RL192' recurs on 3 independent full tickets across 2 different weighmasters/dates, arguing against a simple typo. Neither the Trailer Standard Empty Weight substitution methodology (which exists for exactly this trigger) nor any other documented resolution was applied to either offload. Garrett to confirm whether 'RL192' is a real, untracked trailer unit and whether these two offloads' masses should be revisited when TILX200228's railcar closes. [log:scale_tickets.rig_mismatches_found] [log:scale_tickets.rl192_pattern_note]","VR Sec 5.1"),
 ("2.4","Net mass correctly calculated in Ops Notes (each offload recomputed)","Pass","Net Scaled (kg) = (Full lb - Empty lb) x 0.453592, recomputed from ticket images/VVB Guidance and checked against Ops Notes for all 11 offloads — all match exactly (see 'Per-Offload Mass' tab for the full table). [log:ops_notes.offload_table] [log:scale_tickets._primary_source_opened]","VR Sec 5.1"),
 ("2.5","Standard-tare substitution / conservative mass policy applied where documented","Pass","GPRX5240 offload_1: empty ticket unrecoverable (paired tare ticket 1312226211738 carries commodity label '200228' and was reassigned to TILX200228 offload_2). Trailer Standard Empty Weight for KL188 (29,307 lb = mean 28,997 + 1SD 309, n=14, Apr-Jul 2026) substituted per the RP VVB Guidance doc, read in full. Recomputed net = (70,760-29,307)x0.453592 = 18,802.74918 kg = Ops Notes F39 exactly. VVB Guidance's own stated effect (266.26 kg lower than the raw 19,069.01 kg operational record, i.e. conservative) verified against the COBB raw entry (19,069.00768 kg, row 470) — matches. [log:vvb_guidance.content_verbatim_relevant] [log:ops_notes.offload_table] [log:cobb.rows_confirmed]","GHG Stmt Sec C"),
 ("2.6","1.29% sparging deduction applied","Pass","Recomputed 213,774.7345 kg (Mass Used, post-adj) x 0.0129 = 2,757.694074 kg = Ops Notes rollup Sparging Loss exactly. [log:ops_notes.rollup_section4]","GHG Stmt Sec C"),
 ("2.7","Mass values consistent across scale tickets, Ops Notes, COBB, Certify","Pass","All 11 offloads' raw scale-net values tie exactly between scale tickets and Ops Notes (2.4). COBB matches Ops Notes exactly on 10 of 11 rows; the 1 divergence (GPRX5240 offload_1, COBB 19,069.00768 vs Ops/Certify 18,802.74918) is the documented, expected raw-vs-policy-applied substitution difference (2.5) — not an error. Certify's Bio-Oil Mass - AECN via Rail datapoint (213.775 t) and Mass of Injectant (210.606 t) both trace exactly to the Ops Notes rollup. [log:cobb.rows_confirmed] [log:ops_notes.rollup_section4] [log:certify_datapoints.certify_datapoints_crosscheck]","VR Sec 5.1"),
 ("2.8","Filtration solids loss deduction applied","Pass","Recomputed (213,774.7345 - 2,757.694074) x 0.00195 = 411.4832287 kg = Ops Notes rollup Filtration Loss exactly. [log:ops_notes.rollup_section4]","GHG Stmt Sec C"),

 ("3. Bills of Lading & Transportation","","SECTION","",""),
 ("3.1","All 9 loading BOLs present and individually opened","Pass","All 9 BOLs (2409-R through 2417-R) opened and read individually, not sampled. [log:bols._primary_source_opened]","VR Appendix 1"),
 ("3.2","BOL destination = SOPOR railyard","Pass","All 9 BOLs: Ship To 'CHARM Industrial Inc. /WATCO, Societe du port ferroviaire de Baie-Comeau, 18 Route Maritime, Baie-Comeau, Quebec'. [log:bols._primary_source_opened]","VR Appendix 1"),
 ("3.3","BOL delivered mass matches Ops ledger and railcar aggregate","Pass","All 9 BOL 'Masse Nette' values read directly and match the Ops Notes origins ledger exactly: GPRX5106 25.98+25.90+26.02=77.90 MT; TILX200228 26.06+25.81+26.11=77.98 MT; GPRX5240 26.07+26.06+26.00=78.13 MT — all match the railcar 'Total Loaded' figures exactly. [log:bols.aggregate_check]","VR Sec 3.5"),
 ("3.4","Origin and destination correct (all 9)","Pass","All 9 BOLs: origin BioEnergie AE Cote-Nord (175 Portage des Mousses, Port-Cartier QC = AECN) -> SOPOR; product 'Renewable Fuel Oil RFO / Huile pyrolytique' (pyroligneous acids, CAS 8030-97-5). [log:bols._primary_source_opened]","PDD Sec A"),
 ("3.5","Transport distances verified per source type, EFs at full precision","Fail","VALUES reconcile: single-leg distances (used with EF x aggregate mass, since every offload's mass independently travels the same fixed route length) are AECN->SOPOR truck 107.49722 mi (source 'AECN to SOPOR (Baie Comeau) (2).png'); SOPOR->Opelousas rail 2,199 mi; Opelousas->Basco truck 42.9 mi (source 'Opelousas Railyard to Basco.png') — all confirmed in each transport-process component's Inputs (9.2), and precise EFs opened live on the Standard EFs 2026 tab match exactly (row 5 Truck 0.0001143 MTCO2e/t-mi = 0.1143 kgCO2e/(t.mi); row 9 Rail 0.000025910374 MTCO2e/T-mi = 0.02591 kgCO2e/(t.mi)). HOWEVER: expanded every grouped source on the Datapoints tab directly and confirmed neither 'Allocated Distance Sopor Quebec to Opelousas (rail)' (6,030 mi) nor 'Allocated Distance Opelousas to B6 (truck)' (944 mi) is linked to the Ops Notes — both are linked ONLY to route-map PNG images (image (44).png, 2x Jul-29-2026 and 1x Jul-26-2026 route maps for the rail one; Jul-29/Jul-26 route maps + Opelousas Railyard to Basco.png for the truck one). The route maps evidence the single-leg distance; the ALLOCATION math (per-offload mass fraction x full leg, summed across 11 offloads) that produces the reported 'Allocated' figures exists only in the Ops Notes AECN Rail tab, which is not attached to either datapoint. A verifier cannot independently reconstruct the allocated distance from the attached evidence alone. Same structural gap as documented on prior batch INJ-07-2026-W4 (Fail 3.5). [log:standard_ef_sheet_live_check.truck_transport_process_ef_live_2026_sheet_row5] [log:standard_ef_sheet_live_check.rail_transport_process_ef_live_2026_sheet_row9] [log:certify.attachment_map] [log:certify.attachment_map_note]","Transport Emissions Acctg v1.1"),
 ("3.6","Transport mode / 6 rail components present","Pass","6 transport components present in Certify: AECN-SOPOR tanker (process 2.627t + embodied 0.210t), SOPOR-Opelousas rail (process 12.180t + embodied 0.188t), Opelousas-Basco tanker (process 1.048t + embodied 0.224t). [log:certify_components._primary_source_opened]","Certify Datapoints"),
 ("3.7","Billing / BOL details consistent","Flag","BOL 2414-R's printed Invoice/BOL field reads '2314-R' — a digit-transposition typo on the source document itself (not a hand-corrected/highlighted field like 2415-R/2416-R/2417-R, which show deliberate corrections). Mass value (26,110 kg) and row linkage to the 2414-R entry in Ops Notes/COBB are both correct and unaffected — hygiene finding only, no material impact. [log:bols.print_typo_finding]","VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing","","SECTION","",""),
 ("4.1","CHN/CoA present","Pass","SGS Certificate of Analysis SR26-04724.001, composite weekly AECN sample, sampled 2026-08-01 07:00, received 2026-08-06 10:20, completed 2026-08-07 12:46, signed Tiffany Scott (Lab Supervisor). [log:lab_results.certificate_number]","VR Appendix 1"),
 ("4.2","Carbon content checked against historical AECN range","Pass","Carbon 41.6% (ASTM D5291 Method C). Opened the live MRV_AECN_Analysis.xlsx directly: the most recent 15 historical AECN samples (batches 2-107 through 2-122, Sep-Dec 2025) show individual Carbon values of 40.8-45.2%, so 41.6% sits comfortably inside the directly-observed recent range. The '#' flag on the cert (footnote: 'Result is outside of test method limits and/or analytical range used in method precision study') is a generic SGS lab-method caveat applying to Carbon/Hydrogen/Nitrogen uniformly — not a Charm-side outlier signal (matches the pattern seen on prior AECN batches 2-192/2-199). [log:mrv_aecn_analysis_carbon_range._primary_source_opened] [log:lab_results.sgs_method_flag]","Biomass Feedstock Acctg v1.2"),
 ("4.3","Hydrogen / nitrogen / viscosity / acid number reported and reasonable","Pass","Hydrogen 7.8%, Nitrogen <0.75%, Kinematic Viscosity @40C 14.46 cSt, Acid Number 76 mg KOH/g — all read directly from the CoA, all present and within plausible AECN ranges seen in prior batches. [log:lab_results._primary_source_opened]","Biomass Feedstock Acctg v1.2"),
 ("4.4","Lab report references correct batch/sample ID","Pass","Cert Client ID '08-2026-W1 AECN' matches this batch/week exactly. [log:lab_results.certificate_number]","VR Sec 5.1"),
 ("4.5","pH/conductivity (aqueous phase)","N/A","AECN is not aqueous phase; pH is checked in Section 5.5. [log:oil_type]","UIC Permit / LDENR"),
 ("4.6","Density above formation-fluid floor for safe injection","Pass","Density 1.206 g/cm3 at 15C — above the 1.01 g/cm3 formation-fluid floor. [log:lab_results.density_g_cm3_15C]","VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency","","SECTION","",""),
 ("5.1","Correct batch ID and injection date","Pass","Ops Notes batch ID 'INJ-08-2026-W1'; Week End 2026-08-01 = Certify removal date 01 Aug 2026. [log:ops_notes.week_end] [log:removal_date]","-"),
 ("5.2","Scale ticket values correctly transcribed","Pass","Every ticket's Full/Empty lb value transcribed correctly into the Ops Notes offload table — verified value-by-value in item 2.4's full recompute. [log:scale_tickets._primary_source_opened] [log:ops_notes.offload_table]","VR Sec 5.1"),
 ("5.3","Oil/aqueous phase mass reconciliation","N/A","This removal is AECN-only (rail); no aqueous phase component. [log:oil_type]","-"),
 ("5.4","COBB values present and matched per offload","Flag","All 8 relevant COBB rows found (row 463-473 on the 'Basco Injection -- COBB' tab, under COBB's own date-based label 'INJ-20260726_bio_oil' rather than the week-numbered ID — a known, harmless naming-convention divergence between COBB and Ops Notes/Certify). 10 of 11 offload quantities match Ops Notes exactly; the 1 divergence (GPRX5240 offload_1) is the documented raw-vs-substituted difference (2.5/2.7), not an error. ONE genuine COBB-side labeling defect found: row 467 (TILX200228 offload_1)'s consumed_lot cell shows GPRX5240's BOL numbers as a text string ('2415-R, 2416-R, 2417-R_offload_1') instead of the expected 'Rail_TILX200228_7.6.2026_offload_1' pattern used by the adjacent rows. The BOL_number column and quantity value on that same row are both correct. Cosmetic, Garrett-side data-provenance issue — not verifier-impacting. [log:cobb.rows_confirmed] [log:cobb.cobb_naming_note]","-"),
 ("5.5","pH measurement noted, within target range","Pass","pH 2.88 recorded uniformly across all 11 offloads (target range 2.0-4.0). [log:ops_notes.ph_check]","-"),
 ("5.6","Completion date present and matches COBB","Flag","The 'Basco Injection -- COBB' tab's date-type field for these rows is 'order_line_completed_on' (e.g. 2026-07-09 19:28:01 for GPRX5106 offload_1) — this predates GPRX5106's own 2026-07-25 arrival at Opelousas, so it is an upstream ERP/order-fulfillment timestamp, not an injection-completion date. No field on the COBB tracker's 'Basco Injection -- COBB' tab can be directly cross-checked against the batch's 2026-08-01 injection date. Schema-mapping gap — cannot confirm match or mismatch; not a value discrepancy. [log:cobb._primary_source_opened]","-"),
 ("5.7","No erroneous density measurement","N/A","Density field in Ops Notes Batch Composition is expected to be blank for AECN (density is measured on the lab CoA instead — see 4.6). [log:oil_type]","VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation","","SECTION","",""),
 ("6.1","AECN process emissions LCA CI spreadsheet present","Pass","Certify Sources includes 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx', linked to the Pyrolysis Process CI datapoint. [log:certify_sources_enumeration]","VR Appendix 1"),
 ("6.2","LCA with stack emissions file present","Pass","Certify Sources includes 'BH 2025 LCA w Stack Emissions.xlsx'. [log:certify_sources_enumeration]","VR Appendix 1"),
 ("6.3","Supporting GHG data file present","Pass","Certify Sources includes 'Supporting GHG data 31Dec2025 S.xlsx'. [log:certify_sources_enumeration]","VR Appendix 1"),
 ("6.4","AECN pyrolysis process EF matches current value, at full precision","Flag","Certify's process-emissions component computes to an implied EF of 0.10399 tCO2e/t (22.233t / 213.77472t), sourced from the 4 period-specific H2-2025 LCA/CI files linked to this datapoint (NOT the generic 'Standard Emission Factors + Calculations' sheet). The live 'Standard Emission Factors + Calculations' 2026 tab, opened directly, shows row 3 'Production Emissions for AECN Oil--H1 2026' = 0.10380 MTCO2e/MT (confirmed still current — searched the sheet for 'H2 2026', 0 of 0 matches, so no semi-annual update has superseded it as of this session). The ~0.0002 gap between the period-specific LCA file's implied rate and the generic sheet's tracked value is small (~0.043t on this removal) but exceeds the checklist's 0.001t tolerance, and mirrors the same within-RP source-file divergence pattern flagged on batch 2-199 (Failure Category 13). Recommend Garrett confirm which document is authoritative for the current EF and reconcile the generic sheet if it has drifted. [log:standard_ef_sheet_live_check]","Certify Datapoints"),
 ("6.5","AECN pyrolysis embodied EF applied, at full precision","Pass","Certify's embodied component shows 0.02116 tCO2e/t — EXACT match to the live '2026' tab row 4 (0.02116 MTCO2e/MT), opened and read directly. [log:standard_ef_sheet_live_check]","Certify Datapoints"),
 ("6.6","Pyrolysis EF mass basis = pre-sparging Origin Bio-Oil Mass","Pass","Both pyrolysis components (modals opened) use 'Bio-Oil Mass - AECN via Rail' = 213,774.72 kg (pre-sparging), not the post-deduction Mass of Injectant (210,605.56 kg). Correct per methodology. [log:certify_components.component_detail]","Certify Components"),

 ("7. Gross-to-Net Calculation","","SECTION","",""),
 ("7.1","Gross CO2e = injectant mass x carbon x 3.667","Pass","210.6056 t (Mass of Injectant) x 0.416 (carbon decimal) x 3.667 = 321.273 tCO2e = Certify Injection Sequestration exactly. [log:ops_notes.rollup_section4] [log:certify_components.sequestrations_t]","GHG Stmt Sec E"),
 ("7.2","Process + transport emissions correctly deducted","Pass","Activities recomputed = pyrolysis (22.233+4.523=26.756) + transport (2.627+0.210+12.180+0.188+1.048+0.224=16.477) = 43.233 t = Certify Activities exactly. [log:_derived_values.pyrolysis_sum_t] [log:_derived_values.transport_total_t] [log:_derived_values.activities_sum_t]","GHG Stmt Sec E"),
 ("7.3","Uncertainty discount applied","Pass","Uncertainty Discount 1.778 t present in Calculation View (~0.55% of gross). [log:certify_calculation_view._primary_source_opened]","Isometric Standard S3.7"),
 ("7.4","Net removals consistent with BCU Quant / GHG Statement","Flag","Internal recompute is exact: 321.273 - 43.233 - 1.778 = 276.262 t = Certify displayed Net. Cross-check against the RP-level BCU Quant spreadsheet and GHG Statement is deferred (RP still open) — same treatment as prior batches. Separately and more materially, see items 9.5/9.6: this removal carries ZERO BCU reductions, which the internal recompute does not depend on but which represents a real, unexplained departure from every comparable prior AECN batch. [log:certify_calculation_view._primary_source_opened]","GHG Stmt Sec E"),

 ("7a. Per-Component Uncertainty Verification","","SECTION","",""),
 ("7a.1","Completeness: every component carries uncertainty on the correct datapoint","Pass","Opened all 9 component modals. Carbon Content + Mass of Product on Injection Sequestration; Mass of Load on all 3 transport-process legs and both pyrolysis components (5 mass-basis components total, all sharing the same physical mass datapoint); the 3 embodied legs correctly carry NO mass-of-load datapoint (per-mile EF, not mass-scaled). [log:certify_components.uncertainty_layer1_completeness]","Isometric Standard S3.7.3"),
 ("7a.2","Correctness: reported uncertainty matches expected calculation","Pass","Carbon content uncertainty 0.1664% = exactly 0.004 x 41.6%. Mass uncertainty 798.27 kg = exactly 11 x 72.57 kg — the 11 discrete truck-out weighings across all 3 railcars this week (4 GPRX5106 + 3 TILX200228 + 4 GPRX5240), applied consistently and identically across every mass-basis component. [log:certify_components.component_detail]","Isometric Standard S3.7.3"),
 ("7a.3","Discount presence and consistency","Pass","Aggregate Uncertainty Discount 1.778 t present in Calculation View and reconciles exactly with the Net CDR formula (7.3/7.4). [log:certify_calculation_view._primary_source_opened]","Isometric Standard S3.7"),

 ("8. Data Integrity & Anomaly Check","","SECTION","",""),
 ("8.1","No unexplained outliers in mass, carbon content, or calculated values","Pass","Carbon 41.6% within historical range (4.2); every offload's net mass reconciles ticket->Ops Notes (2.4) and railcar totals reconcile to BOL aggregates within expected tolerance (3.3); Net 276.262t independently reconstructed from mass x carbon x 3.667 less activities/uncertainty (7.4). The two rig-mismatch findings (2.3) and the zero-BCU finding (9.5/9.6) ARE explained/flagged, not unexplained. [log:lab_results.carbon_pct]","GHG Stmt Sec C"),
 ("8.2","Spills/losses documented and deducted","Pass","No spill or loss events documented in the Ops Notes AECN Rail tab (read in full, including all cell comments) or the RP VVB Guidance doc (read in full). Mass losses this week are only the routine sparging (1.29%) and filtration (0.195%) deductions plus the documented GPRX5240 offload_1 substitution. [log:ops_notes._primary_source_opened] [log:vvb_guidance._primary_source_opened]","GHG Stmt Sec C"),
 ("8.3","Cross-week / carry-forward inventory documented","Pass","TILX200228 is only partially drawn down this week (3 of 4 offloads; offload_4 not yet occurred) — its remaining ~20 MT stays in the railcar for a future week's batch, consistent with the 'Full Railcar This Week?' = PARTIAL flag in the Ops Notes railcar table. No double-counting risk: this week only claims the 3 offloads that actually occurred. [log:ops_notes.railcars_received_this_week]","VR Sec 3.5"),
 ("8.4","Rail uncertainty conservatism (N_offloads >= N_inbound_BOLs per railcar)","Pass","GPRX5106 (FULL, closed this week): 4 offloads >= 3 inbound BOLs — conservative. GPRX5240 (FULL, closed this week): 4 offloads >= 3 inbound BOLs — conservative. TILX200228: not yet the railcar's last batch (only 3 of 4 offloads claimed) — this check is deferred to whichever future week closes out that railcar, per methodology. [log:ops_notes.railcars_received_this_week]","Isometric Standard S3.7.3"),

 ("9. Isometric Certify — Removal Component Mapping","","SECTION","",""),
 ("9.1","Sequestration matches internal gross","Pass","Mass of Injectant 210,605.55715 kg x Carbon Content 41.6% x 3.667 = 321.273 t = Certify Injection Sequestration component exactly. [log:certify_components.component_detail]","Certify Components"),
 ("9.2","Transport: process + embodied per leg (6 components), full math shown","Flag","Arithmetic reconciles exactly for all 6 components (shown below) — see item 3.5 for a real, separate finding: the two Allocated Distance datapoints feeding these calculations are not attached to the Ops Notes (only to route-map images), so the allocation math itself is not independently reconstructable from Certify's attached evidence.\nAECN->SOPOR Truck Process: 213.77472t x 0.1143 kgCO2e/(t.mi) x 107.49722mi = 2,627.3 kg = 2.627t = Certify exactly.\nSOPOR->Opelousas Rail Process: 213.77472t x 0.02591 x 2,199mi = 12,180.6 kg = 12.180t = Certify exactly.\nOpelousas->Basco Truck Process: 213.77472t x 0.1143 x 42.9mi = 1,048.2 kg = 1.048t = Certify exactly.\nAECN->SOPOR Truck Embodied 0.210t, SOPOR->Opelousas Rail Embodied 0.188t, Opelousas->Basco Truck Embodied 0.224t all confirmed present with the correct EF sourcing (0.1476 kgCO2e/km tanker EF, live sheet row 10; 0.0193 kgCO2e/km railcar EF, live sheet row 12) and no mass-of-load datapoint (correct — embodied is per-mile). [log:embodied_ef_live_check.tanker_truck_embodied_live_2026_sheet_row10] [log:embodied_ef_live_check.railcar_embodied_live_2026_sheet_row12]\nBio-oil transport total = 2.627+12.180+1.048 (process) + 0.210+0.188+0.224 (embodied) = 15.855 + 0.622 = 16.477t = Certify 'Bio-oil transport' subtotal exactly. [log:certify_components.component_detail] [log:_derived_values.transport_process_sum_t] [log:_derived_values.transport_embodied_sum_t] [log:_derived_values.transport_total_t]","Certify Components"),
 ("9.3","Injection: LCS / sample transport","N/A","AECN requires no LCS pre-treatment at Basco; no LCS component on this entry. [log:oil_type]","Certify Components"),
 ("9.4","Pyrolysis: process + embodied present, full math shown","Pass","AECN pyrolysis (from rail loads) - process emissions: 213.77472t x 0.10399 (implied, see 6.4) = 22.233t = Certify exactly.\nAECN pyrolysis (from rail loads) - embodied emissions: 213.77472t x 0.02116 = 4.523t = Certify exactly.\nMass basis = pre-sparging Bio-Oil Mass - AECN via Rail (213,774.72 kg), correct per methodology (6.6). Rail-batch naming ('from rail loads') is the deliberate VVB signal per convention. [log:certify_components.component_detail]","Certify Components"),
 ("9.5","Reductions: applicable BCU categories populated","Fail","Certify's Components tree for this removal contains ONLY 'Stored' (321.273t) and 'Emitted' (43.233t) — there is NO 'Reductions' category at all, and none of the 17 Certify Sources is a BCU/RD-EAC certificate. Every comparable AECN batch reviewed in the active QA registry (2-181, 2-190, 2-191, 2-192, 2-199, 2-201, 2-204, INJ-06-2026-W1, etc.) carries a 'BCU's Transport' reduction that exactly matches the transport process sum. No VVB Guidance entry, Ops Notes comment, or other documentation addresses or explains this absence. Checked the 'Charm EAC Verification Inventory tracker' (BCU Inventory tab) directly to rule out inventory exhaustion as an innocent explanation: the RD-EACs retirement certificate (issued 2025-12-18) carries 2,561.71 units of remaining, undrawn BCU inventory — well above the 200-unit alert floor and more than sufficient to cover this removal's 15.855t shortfall. Available inventory existed and was simply not drawn against this removal. Per the checklist's own BCU QA Rule ('BCU quantity... MUST equal or exceed the corresponding... emission... EVERY removal'), this is a clear, unexplained departure from required and historically consistent practice. [log:certify_components.reductions_category_present] [log:certify_sources_bcu_certificate_present] [log:eac_inventory_check.conclusion]","Certify Components"),
 ("9.6","BCU quantity >= corresponding transport process activity emission","Fail","Transport process sum = 2.627 + 12.180 + 1.048 = 15.855 t. BCU coverage = 0 t (see 9.5). Shortfall = 15.855 t (100% of transport process emissions unoffset). [log:_derived_values.aecn_sopor_process_t] [log:_derived_values.rail_process_t] [log:_derived_values.opel_basco_process_t] [log:_derived_values.transport_process_sum_t] [log:_derived_values.bcu_coverage_t] [log:_derived_values.bcu_shortfall_t]","Certify Components"),
 ("9.7","Counterfactuals zero per protocol","Pass","No counterfactual emission component present on this removal; bio-oil geological storage counterfactual is zero per protocol. [log:certify_components._primary_source_opened]","Certify Components"),
 ("9.8","Net removal matches internal calculation","Pass","Independent recompute 321.273 - 43.233 - 1.778 = 276.262 t = Certify Net CO2e Removed exactly. This arithmetic does not depend on the missing-BCU finding (9.5/9.6) — Net CDR is correctly stated for what Certify currently reports; whether it SHOULD be higher if a BCU reduction is later added is the open question captured at 9.5/9.6, not an error in this calculation. [log:certify_calculation_view._primary_source_opened]","Certify Calculation View"),
 ("9.9","Descriptive source filenames","Flag","2 of 17 Certify Sources have non-descriptive filenames (content correct, naming only): 'Screenshot 2026-02-23 at 11.29.10 AM.png' (linked to AECN Pyrolysis Process CI) and 'image (44).png' (linked to the Sopor-Opelousas rail allocated distance). Also 2 near-duplicate 'Jul-29-2026-distance-route_map.png' uploads exist under different source IDs (same filename, both linked to the AECN->SOPOR distance datapoints) — worth Garrett's confirmation these aren't an accidental double-upload. [log:certify_sources_enumeration]","Certify Datapoints"),
 ("9.10","Sources match Drive / complete set","Pass","17 sources enumerated in full from the Certify Sources tab (single source of truth). Every source needed for this removal's datapoints is present: Ops Notes, lab CoA, 3 EF/route reference files, 4 AECN LCA/GHG period files, and the 3 distance/route map images. No per-batch Drive folder exists separately to cross-check against (1.1) — all evidence is Certify-Sources-resident or Ops-Notes-hyperlinked, both of which were opened directly. [log:certify_sources_enumeration] [log:certify_sources_tab_total]","Certify Sources"),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "QA Checklist"
ws.append(["Item","Check","Status","Notes / Evidence","Verifier Ref"])
for c in ws[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
for (a,b,status,*rest) in ROWS:
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

# ---- Sheet 2: per-offload mass reconciliation ----
ws2 = wb.create_sheet("Per-Offload Mass")
hdr = ["Offload (consumed_lot)","Railcar","Full (lb)","Empty (lb)","Net Scaled (kg)","MOBI (kg)","COBB offloaded (kg)","Scale-ticket rig match"]
ws2.append(hdr)
for c in ws2[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
offs = [
 ("Rail_GPRX5106_7.03.2026_offload_1","GPRX5106",72400,29220,19586.10256,19295.74163,19586.10256,"Y (CH1/KL192)"),
 ("Rail_GPRX5106_7.03.2026_offload_2","GPRX5106",71860,29020,19431.88128,19143.80665,19431.88128,"Y (CH2/KL188)"),
 ("Rail_GPRX5106_7.03.2026_offload_3","GPRX5106",74260,29060,20502.3584,20198.41411,20502.3584,"Y (CH1/KL192)"),
 ("Rail_GPRX5106_7.03.2026_offload_4","GPRX5106",69180,28740,18343.26048,18071.32449,18343.26048,"Y (CH2/KL188)"),
 ("Rail_TILX200228_7.6.2026_offload_1","TILX200228",70580,28600,19041.79216,18759.50054,19041.79216,"Y (CH2/KL188)"),
 ("Rail_TILX200228_7.6.2026_offload_2","TILX200228",72640,28720,19921.76064,19626.42363,19921.76064,"N -- see item 2.3 (CH1/RL192 vs CH2/KL188)"),
 ("Rail_TILX200228_7.6.2026_offload_3","TILX200228",70560,28880,18905.71456,18625.44027,18905.71456,"Y (CH2/KL188)"),
 ("Rail_GPRX5240_7.6.2026_offload_1","GPRX5240",70760,"29,307 (substituted)",18802.74918,18524.00133,19069.00768,"N/A -- substituted per VVB Guidance (2.5)"),
 ("Rail_GPRX5240_7.6.2026_offload_2","GPRX5240",73560,29200,20121.34112,19823.04536,20121.34112,"N -- see item 2.3 (CH1/RL192 vs CH1/KL192)"),
 ("Rail_GPRX5240_7.6.2026_offload_3","GPRX5240",63840,28800,15893.86368,15658.23961,15893.86368,"Y"),
 ("Rail_GPRX5240_7.6.2026_offload_4","GPRX5240",80080,28880,23223.9104,22879.61953,23223.9104,"Y (CH1/KL192)"),
]
for o in offs:
    ws2.append(list(o))
    for col in range(1,len(hdr)+1): ws2.cell(ws2.max_row,col).border = BORDER; ws2.cell(ws2.max_row,col).alignment=WRAP
ws2.append(["WEEK TOTAL","3 railcars","","","213774.7345","210605.5572 (post-loss)","",""])
for col in range(1,len(hdr)+1):
    ws2.cell(ws2.max_row,col).font=BOLD; ws2.cell(ws2.max_row,col).fill=HEADER_FILL; ws2.cell(ws2.max_row,col).border=BORDER
ws2.append([])
ws2.append(["Railcar BOL-aggregate reconciliation:"])
ws2.append(["GPRX5106 (FULL): 19586.10256+19431.88128+20502.3584+18343.26048 = 77863.60 kg vs BOL aggregate 77,900 kg (loss 36.40 kg, within 5% tolerance)"])
ws2.append(["TILX200228 (PARTIAL, 3 of 4 offloads): 19041.79216+19921.76064+18905.71456 = 57869.27 kg claimed this week; BOL aggregate 77,980 kg; remainder carried to a future week (8.3)"])
ws2.append(["GPRX5240 (FULL): 18802.74918+20121.34112+15893.86368+23223.9104 = 78041.86 kg vs BOL aggregate 78,130 kg (loss 88.14 kg, within 5% tolerance)"])
for col_w,w in [("A",40),("B",13),("C",22),("D",14),("E",14),("F",16),("G",18),("H",34)]:
    ws2.column_dimensions[col_w].width = w

# ---- Sheet 3: Certify-vs-Source evidence matrix ----
ws3 = wb.create_sheet("Source Matrix")
ws3.append(["Certify value","Required sources","Source-derived","Certify","Match"])
for c in ws3[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
MATRIX = [
 ("Mass of Injectant","Scale tickets + Ops Notes","210,605.5572 kg (rollup: raw nets - sparging 1.29% - filtration 0.195%)","210,605.55715 kg","="),
 ("Carbon Content","Lab CoA","41.6% (SGS SR26-04724.001)","41.60%","="),
 ("Bio-Oil Mass - AECN via Rail (pre-sparge)","Scale tickets + BOLs + Ops Notes","213,774.7345 kg (11 offload raw nets, GPRX5240 O1 substituted)","213,774.72 kg","="),
 ("Injection Sequestration","Mass x Carbon x 3.667","210.6056 t x 0.416 x 3.667 = 321.273 t","321.273 t","="),
 ("Pyrolysis Process","period-specific LCA files x mass","213.77472 t x 0.10399 (implied) = 22.233 t","22.233 t","= (see Flag 6.4 on EF source)"),
 ("Pyrolysis Embodied","AECN Embodied Calc Sheet x mass","213.77472 t x 0.02116 = 4.523 t","4.523 t","="),
 ("Transport AECN->SOPOR Process","tickets+BOLs+Ops x dist x EF sheet","213.77472 x 107.49722mi x 0.1143 kgCO2e/(t.mi) = 2.627 t","2.627 t","="),
 ("Transport Rail Process","tickets+BOLs+Ops x dist x GLEC EF","213.77472 x 2199mi x 0.02591 kgCO2e/(t.mi) = 12.180 t","12.180 t","="),
 ("Transport Opel->Basco Process","tickets+Ops x dist x EF sheet","213.77472 x 42.9mi x 0.1143 kgCO2e/(t.mi) = 1.048 t","1.048 t","="),
 ("Transport embodied (3 legs)","Standard EF sheet, per-mile EFs","0.1476 kgCO2e/km tanker; 0.0193 kgCO2e/km railcar, applied to allocated distances","0.210 / 0.188 / 0.224 t","="),
 ("Uncertainty Discount","Variance propagation (carbon 0.4%, mass 11x72.57kg)","Reconciles: 321.273-43.233-1.778=276.262","1.778 t","="),
 ("Net CO2e Removed","Sequestrations - Activities - Uncertainty","321.273-43.233-1.778 = 276.262","276.262 t","="),
 ("BCU / Reductions","Expected: BCU-Transport-Process >= 15.855t transport process sum","NONE FOUND -- no Reductions category, no BCU cert in Sources","0 t","FAIL -- 15.855t shortfall, see 9.5/9.6"),
]
for m in MATRIX:
    ws3.append(list(m))
    for col in range(1,6): ws3.cell(ws3.max_row,col).alignment=WRAP; ws3.cell(ws3.max_row,col).border=BORDER
    if "FAIL" in str(m[-1]):
        for col in range(1,6): ws3.cell(ws3.max_row,col).fill = FAIL_FILL
for cw,w in [("A",30),("B",34),("C",58),("D",16),("E",30)]: ws3.column_dimensions[cw].width=w

out = "outputs/qa/batch-INJ-08-2026-W1-AECN/Batch_INJ-08-2026-W1_QA_Checklist.xlsx"
wb.save(out)
print("saved", out)
from collections import Counter
tally = Counter(r[2] for r in ROWS if r[2] != "SECTION")
print("tally:", dict(tally))
