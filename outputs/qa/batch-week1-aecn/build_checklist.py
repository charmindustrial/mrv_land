#!/usr/bin/env python3
"""Build INJ-06-2026-W1 AECN weekly batch QA checklist."""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

HEADER_FILL = PatternFill("solid", fgColor="D6E4F0")   # section/sub-header
FAIL_FILL   = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL   = PatternFill("solid", fgColor="FFF2CC")
FLAG_FONT   = Font(color="996600")
NA_FONT     = Font(color="808080", italic=True)
BOLD        = Font(bold=True)
WRAP        = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

# (item, check, status, evidence, verifier)  status in {Pass,Fail,Flag,N/A,SECTION}
ROWS = [
 ("INJ-06-2026-W1 — AECN Weekly Batch QA", "Reviewer: Claude QA Agent  |  Date: 2026-06-23 (re-review 2026-06-25, post-Garrett)  |  Injection Site: Basco 6  |  Oil Type: AECN (rail)  |  Week: Sat 2026-05-30 to Sat 2026-06-06  |  Injected: 2026-06-05  |  Certify GHG entry rmv_1KTYCT2551S0V1ZT","SECTION","",""),
 ("Scope","Time-block (weekly) batch = all AECN oil for the week, aggregated into ONE Certify GHG entry. This week AECN is ALL RAIL: 9 truck-out offloads from 3 railcars (TIMX201060 offload_4 only; GPRX5102 offloads 1-4; TILX200231 offloads 1-4). Net CDR 230.096 tCO2e. [log:batch_id]","SECTION","",""),

 ("1. Batch Folder Completeness","","SECTION","",""),
 ("1.1","Batch folder named with batch ID","Pass","Drive folder 'W1' contains the INJ-06-2026-W1 batch; Ops Notes header batch ID 'INJ-06-2026-W1'. [log:batch_id]","VR Appendix 1"),
 ("1.2","Scale Tickets subfolder present and populated","Pass","Scale Tickets folder holds one subfolder per railcar; 18 ticket images total (full+empty for each of 9 offloads), all read. [log:scale_tickets.ticket_file_ids]","VR Appendix 1"),
 ("1.3","Testing subfolder present with lab results","Pass","Testing folder holds SGS CoA 'SR26-03624.001' (Client ID '6-2026-W1 AECN'). [log:lab_results.cert_no]","VR Appendix 1"),
 ("1.4","Ops Notes present and complete","Pass","Weekly master workbook 'INJ-06-2026-W1 Ops Notes' (Summary + AECN Rail tabs); all sections populated, read in full locally. [log:ops_notes._primary_source_opened]","VR Appendix 1"),
 ("1.5","Injection site confirmed Basco 6","Pass","Lab cert location 'Basco Louisiana'; BOLs route AECN to SOPOR to Basco; Certify entry is the Basco project. All source docs reference Basco / SOPOR / AECN only. [log:lab_results.location]","Basco verification"),

 ("2. Scale Tickets & Mass Determination","","SECTION","",""),
 ("2.1","Full and empty ticket images present per offload","Pass","All 18 tickets opened and read (CAT Scale 3122, Bunkie LA). Every offload has a legible full and empty ticket; each ticket's axle breakdown sums to its stated gross. [log:scale_tickets.reads]","VR Sec 5.1"),
 ("2.2","Ticket dates within 2 weeks of injection","Pass","All 18 ticket dates read: TIMX O4 5-28; GPRX O1 5-29/5-30, O2 5-29, O3 6-01, O4 6-01/6-03; TILX O1 6-03, O2 6-03/6-04, O3 6-04/6-05, O4 6-05. Span 2026-05-28 to 2026-06-05 vs injection 2026-06-05; all within 14 days. [log:scale_tickets.reads]","VR Sec 3.5"),
 ("2.2b","Empty ticket date on or after full ticket date (same trip ordering)","Pass","Per offload (full -> empty): TIMX O4 5-28/5-28; GPRX O1 5-29/5-30, O2 5-29/5-29, O3 6-01/6-01, O4 6-01/6-03; TILX O1 6-03/6-03, O2 6-03/6-04, O3 6-04/6-05, O4 6-05/6-05. Empty >= full on all 9 offloads. [log:ticket_date_rule]","VR Sec 5.1"),
 ("2.3","Tractor & trailer numbers match between full and empty (same vehicle weighed)","Flag","Masses reconcile on every ticket, but vehicle-ID fields are recorded inconsistently across tickets (Charm fleet 'CH1'/'CH2' + trailer 'KL188'/'KL192'; carrier 'Honorable Transport' tractor '0622' trailer 'CHARM'; DOT-style '4365824' trailer '0'). Within-pair vehicle-ID mismatch on GPRX5102 offload_1, TILX200231 offload_1, TILX200231 offload_2 (plus minor CH1-vs-CH2 on TILX200231 offload_3). The credited mass is anchored to the BOL aggregate per railcar (each railcar's offloads sum exactly to its BOL total), not to individual offload nets, so the reported CDR is unaffected; this is a documentation/audit-trail gap. Garrett to confirm same physical truck recorded under different identifier conventions vs genuinely different trucks. [log:scale_tickets.vehicle_id_finding]","VR Sec 5.1"),
 ("2.4","Net mass correctly calculated in Ops Notes (each offload recomputed)","Pass","Net Scaled (kg) = (Full lb - Empty lb) x 0.453592, recomputed from the ticket images and shown against the Ops-reported net for each offload (computed = Ops):\nGPRX O1 (81420-29080)x.453592 = 23741.01 = Ops 23741.01;\nGPRX O2 (81560-29400) = 23659.36 = Ops 23659.36;\nGPRX O3 (79260-29500) = 22570.74 = Ops 22570.74;\nGPRX O4 (51240-29300) = 9951.81 = Ops 9951.81;\nTILX O1 (78660-29140) = 22461.88 = Ops 22461.88;\nTILX O2 (74820-29640) = 20493.29 = Ops 20493.29;\nTILX O3 (82020-29220) = 23949.66 = Ops 23949.66;\nTILX O4 (58780-32780) = 11793.39 = Ops 11793.39;\nTIMX O4 (53920-33320) = 9344.00 = Ops 9344.00.\nFull/Empty lb read from the scale-ticket images; net checked against the Ops offload table value. [log:scale_tickets.reads] [log:ops_notes.offloads]","VR Sec 5.1"),
 ("2.5","Conservative / last-offload mass policy (FC11) applied per railcar","Pass","FC11 last-offload back-calc in the 'Uncertainty Adjustment' column (offload_4 of each railcar: 39.47 / 1672.91 / 448.21 kg) forces each railcar's post-adjustment offload sum to its BOL aggregate: GPRX5102 offloads sum = 78250.00 vs BOL agg 78250; TILX200231 offloads sum = 78250.00 vs BOL agg 78250; TIMX201060 this-week offload_4 9304.52 + prior-week 68755.53 = 78060.05 vs BOL agg 78060. [log:_derived_values.gprx5102_railcar_offload_sum_kg] [log:_derived_values.tilx200231_railcar_offload_sum_kg] [log:_derived_values.timx201060_thisweek_plus_prior_kg] [log:ops_notes.bol_aggregate_per_railcar_kg] [log:cross_week_carveout_verified]","GHG Stmt Sec C"),
 ("2.6","1.29% sparging deduction applied","Pass","Recomputed (Sum deliveries 167965.12 - uncertainty adj 2160.59) x 0.0129 = 2138.88 kg vs Ops Notes sparging loss 2138.88 (rollup 2138.878367). Match. [log:_derived_values.sparging_recalc_kg] [log:ops_notes.rollup_section4]","GHG Stmt Sec C"),
 ("2.7","Mass values consistent across scale tickets, Ops Notes, COBB, Certify","Pass","Per-railcar COBB offloaded sums vs BOL aggregate: GPRX5102 78250.00 vs 78250; TILX200231 78250.00 vs 78250; TIMX201060 this-week 9304.52. All offloads total 165804.52 kg vs Ops 'Mass Used post-adj' 165804.52 vs Certify Allocated Bio-Oil Mass 165804.47 (165.804 t) - match across all four sources. [log:_derived_values.gprx5102_railcar_offload_sum_kg] [log:_derived_values.tilx200231_railcar_offload_sum_kg] [log:cobb.sum_all_cobb_offloaded_kg] [log:ops_notes.rollup_section4] [log:certify.datapoints.allocated_bio_oil_mass_t]","VR Sec 5.1"),
 ("2.8","Filtration loss deduction","Pass","Ops Notes applies a Filtration Loss deduction at 0.195% (constant 0.00195, 'Filtration Solids Content') after sparging; recomputed (mass used 165804.52 - sparging 2138.88) x 0.00195 = 319.15 kg vs Ops Notes filtration loss 319.15 (rollup 319.1480102). Match. Confirmed by Max as a correct, expected weekly-batch deduction; conservative (reduces credited mass). [log:_derived_values.filtration_recalc_kg] [log:ops_notes.rollup_section4]","GHG Stmt Sec C"),

 ("3. Bills of Lading & Transportation","","SECTION","",""),
 ("3.1","All truck BOLs present and cross-checked to BOL folder (3 per railcar into SOPOR)","Pass","All 9 BOLs opened and read individually (not sampled): 2359/2360/2361-R (GPRX5102), 2362/2363/2364-R (TIMX201060), 2368/2369/2370-R (TILX200231). Cross-checked Ops origins-ledger list against the period BOL folder (id ...uPGsaG, holds 2356-2376-R): all 9 present in the folder; folder also holds adjacent-week BOLs (expected). [log:bol.bol_folder_crosscheck]","VR Appendix 1"),
 ("3.2","BOL destination = SOPOR railyard","Pass","All 9 BOLs Ship To 'CHARM/WATCO, Societe du port ferroviaire de Baie-Comeau (SOPOR)', 18 Route Maritime, Baie-Comeau. [log:bol.all_dest_sopor]","VR Appendix 1"),
 ("3.3","BOL delivered mass matches Ops ledger (each) and railcar agg >= claimed","Pass","Per-BOL scale-weighed 'Product delivered' vs Ops ledger MT: 2359 26.05, 2360 26.09, 2361 26.11, 2362 26.10, 2363 25.86, 2364 26.10, 2368 26.16, 2369 26.20, 2370 25.89 - all 9 match exactly. Railcar aggregates 78060/78250/78250 kg >= each railcar's claimed offload mass. [log:bol.reads]","VR Sec 3.5"),
 ("3.4","Origin and destination correct (all 9)","Pass","All 9 BOLs: origin BioEnergie AE Cote-Nord (175 Portage des Mousses, Port-Cartier QC = AECN) -> destination SOPOR (Baie-Comeau); product RFO bio-oil (pyroligneous acids, CAS 8030-97-5). [log:bol.all_origin_aecn]","PDD Sec A"),
 ("3.5","Transport distances verified per source type","Pass","RESOLVED on re-review 2026-06-25: the Ops Notes (allocation working) is now attached in Certify and linked to all 3 allocated-distance datapoints (AECN->Sopor truck, Sopor->Opelousas rail, Opelousas->B6 truck), confirmed on a live Sources-tab read (47 sources; Ops Notes added, none removed). [log:rereview_2026_06_25._primary_source_opened] NON-ALLOCATED full distances (Google Maps, rail exception = Watco): AECN->SOPOR 107.5 mi single-truck (Google Maps 'AECN to SOPOR (Baie Comeau).png' 172 km, ~107.5 mi; Certify full datapoint 173.00 km); Opelousas->Basco 42.9 mi (Google Maps 'Opelousas Railyard to Basco.png' I-49 S route 42.9 mi; matches Certify/Ops 42.9); SOPOR->Opelousas rail 2199 mi (Watco email, M. Bergeland 'total mileage for this move was 2199' - carrier confirmation is the rail evidence). ALLOCATED distances (Ops Notes x Google Maps full): per-offload allocated = full leg x (post-adj offload mass / railcar BOL aggregate); reconstructed for all 9 offloads and matches Ops Notes columns exactly; sums AECN->SOPOR 683.44, rail 4660.11, Opel->Basco 772.2 mi vs Certify allocated datapoints 683 / 4660 / 772. [log:route_verification] [log:ops_notes.allocated_distance_sums] [log:certify.datapoints]","Transport Emissions Acctg v1.1"),
 ("3.6","Transport mode / 6 rail components present","Pass","6 transport components in Certify: AECN-SOPOR tanker (process+embodied), SOPOR-Opelousas rail (process+embodied), Opelousas-Basco tanker (process+embodied). [log:certify.components.transport]","Certify Datapoints"),
 ("3.7","Billing / BOL details consistent","Flag","Two documentation items (mass/routing all correct): (1) Ops origins-ledger 'Date' = railcar consolidation date (2359-2364 all 5/7; 2368-2370 all 5/11) but actual BOL loading dates span 5/01-5/08 - systematic by-design but undocumented. (2) Minor BOL print typos: 2361-R PO 'Q42026'; 2364-R ship-date '2025'; 2368-R prod-period '#05-2024'; 2369-R prod-period '#10-2024'; 2370-R tanker id 22095. Also each BOL carries an estimated loaded qty (volume x density) distinct from the scale-weighed delivered mass Ops uses (the correct one). [log:bol.date_convention_finding]","VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing","","SECTION","",""),
 ("4.1","CHN/CoA present","Pass","SGS CoA SR26-03624.001 (Reissue 1, corrected D5291), one weekly composite AECN sample (sampled 2026-06-10, Basco LA). Weekly batching uses one composite sample for the week (vs per-injection historically) - confirmed correct by Max. [log:lab_results.cert_no]","VR Appendix 1"),
 ("4.2","Carbon content checked against historical AECN mean","Pass","Carbon 42.2% (ASTM D5291 Method C) vs MRV_AECN_Analysis historical mean 39.42 +/- 6.08 (n=285): +0.46 SD, well in range. Matches Certify 42.20% and Ops 0.422. The '#' is the method analytical-range flag (same as prior AECN certs), not an outlier. [log:mrv_historical] [log:lab_results.carbon_pct]","Biomass Feedstock Acctg v1.2"),
 ("4.3","Hydrogen / nitrogen / viscosity checked against historical means","Pass","All read from lab cert and compared to MRV_AECN_Analysis historical means: Hydrogen 7.6% vs 6.87 +/- 0.56 (n=285) = +1.29 SD (most elevated parameter, still in range); Nitrogen <0.75% (below detection, consistent with historical where most are <0.75); Kinematic viscosity 41.53 cSt vs historical 41.03 +/- 17.8 (n=20) = +0.03 SD, essentially at mean; Acid number 63 mg KOH/g reported (no historical column in this source). No outliers. [log:mrv_historical]","Biomass Feedstock Acctg v1.2"),
 ("4.4","Lab references correct batch/sample ID","Pass","Cert Client ID ' 6-2026-W1 AECN' matches the week. [log:lab_results.client_id]","VR Sec 5.1"),
 ("4.5","pH/conductivity (aqueous phase)","N/A","AECN is not aqueous phase; pH is checked in Section 5.5. [log:oil_type]","UIC Permit"),
 ("4.6","Density above formation-fluid floor + vs historical","Pass","Density 1.216 g/cm3 at 15C: above the 1.01 g/cm3 formation-fluid floor for safe injection, and at the historical AECN mean 1.202 (n=188). [log:mrv_historical] [log:lab_results.density_g_cm3_15C]","VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency","","SECTION","",""),
 ("5.1","Correct batch ID and injection date","Pass","Ops Notes batch ID INJ-06-2026-W1; Ops injection date 2026-06-05 (all offloads) vs COBB injection_completion_date 2026-06-05 - match. [log:cobb.injection_completion_date]","-"),
 ("5.2","Scale ticket values correctly transcribed","Pass","Each ticket gross transcribed into Ops Notes Full/Empty (lb) columns - shown value-by-value in item 2.4 (all 18 ticket grosses = Ops Full/Empty per offload, computed net = Ops net). No transcription discrepancy. [log:scale_tickets.reads] [log:ops_notes.offloads]","VR Sec 5.1"),
 ("5.3","Oil/aqueous phase reconciliation","N/A","AECN-only batch; no aqueous phase. [log:oil_type]","-"),
 ("5.4","COBB values present and matched per offload","Pass","COBB tab 'Basco Injection -- COBB', 9 rows batch_id INJ-06-2026-W1_AECN. Per-offload COBB offloaded_quantity vs Ops net_scaled: COBB = Ops net minus the uncertainty adjustment (BOL-cap). Equal where adj=0 (GPRX O1 23741.01, O2 23659.36, O3 22570.74; TILX O1 22461.88, O2 20493.29, O3 23949.66). On the three last-offloads COBB = net - adj: TIMX O4 9344.00 - 39.47 = 9304.52 (COBB 9304.52); GPRX O4 9951.81 - 1672.91 = 8278.90 (COBB 8278.90); TILX O4 11793.39 - 448.21 = 11345.18 (COBB 11345.18). All 9 reconcile. See Per-Offload Mass tab. [log:cobb_vs_ops_per_offload]","-"),
 ("5.5","pH measurement noted","Pass","pH 2.1 recorded (within target range 2.0-4.0). [log:ops_notes.rollup_section4]","-"),
 ("5.6","Completion date matches COBB","Pass","Ops injection date and COBB injection_completion_date both 2026-06-05. [log:cobb.injection_completion_date]","-"),
 ("5.7","No erroneous density measurement","Pass","Density is measured and valid this batch: lab cert 1.216 g/cm3 (verified in 4.6 - at historical AECN mean 1.202, above the 1.01 formation floor) and per-BOL shipment densities 1.2026 / 1.2079 / 1.2091 / 1.2063 / 1.2063 / 1.2082 / 1.2106 / 1.2106 / 1.2086 g/ml - all consistent, within normal AECN range. (Legacy N/A rationale was a blank Ops density field in the per-injection format; weekly format has no Ops density field and density is on the lab cert.) [log:lab_results.density_g_cm3_15C] [log:bol.reads]","VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation","","SECTION","",""),
 ("6.1","AECN process emissions LCA CI spreadsheet present","Pass","Certify Sources include 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx' and '6-2026-W1 AECN.pdf'. [log:certify.certify_sources_filenames]","VR Appendix 1"),
 ("6.2","LCA with stack emissions file present","Pass","Certify Sources include 'BH 2025 LCA w Stack Emissions.xlsx'. [log:certify.certify_sources_filenames]","VR Appendix 1"),
 ("6.3","Supporting GHG data file present","Pass","Certify Sources include 'Supporting GHG data 31Dec2025 S.xlsx'. [log:certify.certify_sources_filenames]","VR Appendix 1"),
 ("6.4","AECN pyrolysis process EF matches current value","Pass","Certify CI 0.104 tCO2e/t; live Standard EFs 2026 tab AECN Production H1 2026 0.1040167 MTCO2e/MT. [log:ef_live_source]","Certify Datapoints"),
 ("6.5","AECN pyrolysis embodied EF applied","Pass","Certify CI 0.02116 tCO2e/t; live Standard EFs 2026 tab AECN Embodied 0.0211600 MTCO2e/MT (exact). [log:ef_live_source]","Certify Datapoints"),
 ("6.6","Pyrolysis EF mass basis = pre-sparging Allocated Bio-Oil Mass","Pass","Both pyrolysis components use Allocated Bio-Oil Mass 165.804 t (pre-sparging Mass Used), not the post-deduction injectant 163.346 t. [log:certify.datapoints.allocated_bio_oil_mass_t]","Certify Components"),

 ("7. Gross-to-Net Calculation","","SECTION","",""),
 ("7.1","Gross CO2e = injectant mass x carbon x 3.667","Pass","RESOLVED on re-review 2026-06-25: the Ops Notes is now attached in Certify and linked to the Mass of Injectant datapoint, confirmed on a live Sources-tab read (47 sources; Ops Notes + RD-EAC cert added, none removed). The mass build-up (raw nets -> FC11 adj -> 1.29% sparging -> 0.195% filtration -> MOBI) is now reproducible from attached component evidence. [log:rereview_2026_06_25._primary_source_opened] Value reconciles: injectant = sum of 9 per-offload MOBI; each MOBI = (Full-Empty) scale-ticket net (18 tickets, item 2.4) less FC11 adj, 1.29% sparging, 0.195% filtration. Ops Notes MOBI rollup 163346.50 kg vs Certify Mass of Injectant 163346.5 kg - match. Independent gross 163346.50 x 0.422 (carbon, lab cert) x 3.667 = 252.774 t vs Certify injection sequestration 252.774 t - match. [log:_derived_values.gross_co2e_recalc_t] [log:_derived_values.ops_mobi_injected_kg] [log:certify.datapoints.mass_of_injectant_kg] [log:scale_tickets.reads] [log:ops_notes.offloads]","GHG Stmt Sec E"),
 ("7.2","Process emissions correctly deducted","Pass","Activities recomputed = pyrolysis 17.244 + 3.508 + transport 2.037 + 0.162 + 9.447 + 0.145 + 0.813 + 0.183 = 33.539 t = Certify Activities 33.540 (rounding). [log:_derived_values.activities_sum_recalc_t] [log:certify.calculation_view.activities_t]","GHG Stmt Sec E"),
 ("7.3","Uncertainty discount applied","Pass","Uncertainty Discount 1.436 t present in net calc (~0.62% of net). [log:certify.calculation_view.uncertainty_discount_t]","Isometric Standard S3.7"),
 ("7.4","Net removals consistent","Pass","Recomputed: 252.774 (seq) + 12.297 (BCU) - 33.540 (activities) - 1.436 (uncertainty) = 230.095 t; Certify displays Net 230.096 (rounding). [log:_derived_values.net_recalc_t] [log:certify.calculation_view.net_co2e_removed_t]","GHG Stmt Sec E"),

 ("7a. Per-Component Uncertainty Verification","","SECTION","",""),
 ("7a.1","Completeness: every component carries uncertainty on the correct datapoint","Pass","Opened all six relevant modals: injection sequestration (carbon + mass), 3 transport process legs (mass of load), 2 pyrolysis (bio-oil mass). Embodied transport legs carry no mass-of-load datapoint (per-mile EF), as expected. [log:certify.uncertainty_modals_read]","Isometric Standard S3.7.3"),
 ("7a.2","Correctness: reported uncertainty matches expected","Pass","Carbon content 0.1688% (0.4% of measured 42.2 carbon). Mass uncertainty 653.13 kg on injectant and every mass-of-load and bio-oil-mass datapoint, across nine discrete outbound weighings at 72.57 kg per weight. Read directly from each modal's INPUTS. [log:certify.datapoints.mass_of_injectant_uncertainty_kg]","Isometric Standard S3.7.3"),
 ("7a.3","Discount presence and consistency","Pass","Aggregate uncertainty discount 1.436 t present in Calculation View, consistent with carbon and mass inputs (~0.57-0.62% of gross). [log:certify.calculation_view.uncertainty_discount_t]","Isometric Standard S3.7"),

 ("8. Data Integrity & Anomaly Check","","SECTION","",""),
 ("8.1","No unexplained outliers","Pass","No unexplained outliers: carbon 42.2% within historical range (item 4.2, +0.46 SD); per-offload nets reconcile ticket->Ops (item 2.4) and railcar sums = BOL aggregate (item 2.5); net 230.096 t reconstructed from mass x carbon x 3.667 less activities/uncertainty (item 7.4). [log:lab_results.carbon_pct] [log:_derived_values.net_recalc_t]","GHG Stmt Sec C"),
 ("8.2","Spills/losses documented and deducted","Pass","No spill or loss events documented in Ops Notes or COBB (both reviewed in full). Mass losses are only the routine sparging + filtration deductions. [log:ops_notes._primary_source_opened] [log:cobb._primary_source_opened]","GHG Stmt Sec C"),
 ("8.3","Cross-week carve-out / no double-count (prior-week boundary)","Pass","Railcar TIMX201060 (loaded 2026-05-07) drawn down across two weeks. Verified directly against INJ-05-2026-W4 Ops Notes (AECN Rail tab): W4 claims TIMX201060 offloads 1, 2, 3 only (68755.53 kg), with no offload_4 row; W1 claims offload_4 only (9304.52 kg). Sum reconciles to BOL aggregate 78060 kg. No double-count across the week boundary. [log:cross_week_carveout_verified._primary_source_opened]","VR Sec 3.5"),
 ("8.4","Rail uncertainty conservatism (N_offloads >= N_BOLs per railcar)","Pass","GPRX5102 4 offloads >= 3 inbound BOLs; TILX200231 4 >= 3; TIMX201060 fully drawn across weeks (4 offloads total >= 3 BOLs). Per-offload 72.57 kg framing is conservative. [log:ops_notes.offloads]","Isometric Standard S3.7.3"),

 ("9. Isometric Certify — Removal Component Mapping","","SECTION","",""),
 ("9.1","Sequestration matches internal gross","Pass","RESOLVED on re-review 2026-06-25: the Mass of Injectant datapoint now carries the Ops Notes (live Sources-tab read; Ops Notes attached + linked) alongside the 18 scale tickets and the lab cert (carbon), so the mass build-up behind the sequestration is verifier-reproducible. [log:rereview_2026_06_25._primary_source_opened] Value: Ops MOBI 163346.50 x 0.422 x 3.667 = 252.774 t = Certify injection sequestration 252.774 t. [log:_derived_values.gross_co2e_recalc_t] [log:certify.components.injection_sequestration_t]","Certify Components"),
 ("9.2","Transport: process + embodied per leg","Pass","RESOLVED on re-review 2026-06-25: the Ops Notes is now attached in Certify and linked to the Allocated Bio-Oil Mass datapoint (the transport mass basis) and the allocated-distance datapoints, confirmed on a live Sources-tab read (47 sources). [log:rereview_2026_06_25._primary_source_opened] Process = allocated bio-oil mass 165.804 t x full leg distance x EF; Embodied = allocated distance sum x per-mile EF (EFs from live 2026 sheet):\n- AECN->SOPOR Truck Process: 165.804 t x 107.5 mi x 0.0001143 MTCO2e/(t-mi) = 2.037 t = Certify 2.037 [log:_derived_values.aecn_sopor_proc_recalc_t]\n- SOPOR->Opelousas Rail Process: 165.804 t x 2199 mi x 0.0000259104 = 9.447 t = Certify 9.447 [log:_derived_values.rail_proc_recalc_t]\n- Opelousas->Basco Truck Process: 165.804 t x 42.9 mi x 0.0001143 = 0.813 t = Certify 0.813 [log:_derived_values.opel_proc_recalc_t]\n- AECN->SOPOR Truck Embodied: 683.44 mi (alloc) x 0.00023756059 MTCO2e/mi = 0.162 t = Certify 0.162 [log:_derived_values.aecn_sopor_emb_recalc_t]\n- SOPOR->Opelousas Rail Embodied: 4660.11 mi (alloc) x 0.0000311307 = 0.145 t = Certify 0.145 [log:_derived_values.rail_emb_recalc_t]\n- Opelousas->Basco Truck Embodied: 772.2 mi (alloc) x 0.00023756059 = 0.183 t = Certify 0.183 [log:_derived_values.opel_emb_recalc_t]\nSource lineage: process mass basis 165.804 t traces to scale tickets + 9 BOLs + Ops (per item 9.4); full leg distances from Google Maps / Watco (item 3.5); allocated distances = Ops x Maps (item 3.5); EFs from Standard EF sheet. [log:ef_live_source] [log:scale_tickets.reads] [log:bol.reads] [log:ops_notes.allocated_distance_sums]","Certify Components"),
 ("9.3","Injection: LCS / sample transport","N/A","AECN requires no LCS pre-treatment; no LCS component on this entry. [log:oil_type]","Certify Components"),
 ("9.4","Pyrolysis: process + embodied present","Pass","RESOLVED on re-review 2026-06-25: the Ops Notes is now attached in Certify and linked to the Allocated Bio-Oil Mass datapoint (the pyrolysis mass basis), confirmed on a live Sources-tab read (47 sources). [log:rereview_2026_06_25._primary_source_opened] Mass basis = pre-sparging allocated bio-oil 165804.52 kg (165.804 t) = GPRX5102 full 78250.00 + TILX200231 full 78250.00 + TIMX201060 offload_4 only 9304.52 (its offloads 1-3 were claimed prior week, item 8.3); each railcar contribution traces to its offload scale-ticket nets (item 2.4) reconciled to that railcar's BOL aggregate (item 3.3) via Ops Notes rollup. CIs from live Standard EF 2026 sheet:\n- Process: 165.804 t x 0.104 tCO2e/t = 17.244 t = Certify 17.244 [log:_derived_values.pyro_proc_recalc_t]\n- Embodied: 165.804 t x 0.02116 tCO2e/t = 3.508 t = Certify 3.508 [log:_derived_values.pyro_emb_recalc_t]\nRail-batch naming ('from rail loads') is the deliberate VVB signal. [log:ef_live_source] [log:scale_tickets.reads] [log:bol.reads] [log:ops_notes.rollup_section4] [log:_derived_values.gprx5102_railcar_offload_sum_kg] [log:cross_week_carveout_verified]","Certify Components"),
 ("9.5","Reductions: applicable BCU categories populated","Pass","BCU - Transport Process credit present; for AECN rail without site-emission burden only the transport-process BCU applies. On re-review 2026-06-25 the supporting RD-EAC retirement certificate ('Charm-RetirementCertificate-RD-EACs-20251218 (1).pdf') is now attached in Certify and linked to the Constant CO2 reduction datapoint (newly added, was not among the prior 39 sources). [log:certify.components.bcu_transport_process_t] [log:rereview_2026_06_25.bcu_rdeac_cert_attached]","Certify Components"),
 ("9.6","BCU quantity >= corresponding activity emission","Pass","Transport process sum recomputed: 9.447 + 2.037 + 0.813 = 12.297 t = BCU - Transport Process 12.297 t (exact coverage). Embodied not BCU-eligible per protocol. [log:_derived_values.transport_process_sum_t] [log:certify.components.bcu_transport_process_t]","Certify Components"),
 ("9.7","Counterfactuals zero per protocol","Pass","No counterfactual emission component; bio-oil geological storage counterfactual is zero per protocol. [log:certify.datapoints]","Certify Components"),
 ("9.8","Net removal matches internal calculation","Pass","Independent gross-to-net recompute 230.095 t (252.774 + 12.297 - 33.540 - 1.436) = Certify Net 230.096 (rounding). [log:_derived_values.net_recalc_t] [log:certify.calculation_view.net_co2e_removed_t]","Certify Calculation View"),
 ("9.9","Descriptive source filenames","Flag","Non-descriptive / inconsistent source filenames (content correct, naming only): generic 'image (44).png', 'Screenshot 2026-02-23 at 11.29.10 AM.png', 'Screenshot 2026-04-10 at 3.19.33 PM.png'; inconsistent BOL camion naming ('Documents Camion' / 'documents' / 'Document_Camion'); 'Full_Ticket_Rail_GPRX5102_5.7.2026_offload_4.png' is a low-resolution distant photo (legible only via crop/enlarge). Garrett to rename/re-shoot for verifier clarity. [log:certify.certify_sources_filenames]","Certify Datapoints"),
 ("9.10","Sources match Drive / complete set","Pass","47 sources on the Certify Sources tab (live re-review 2026-06-25; was 39): 18 scale tickets, 9 BOL camion docs, 4 AECN LCA/GHG files, EF + route + framework sources, the INJ-06-2026-W1 Ops Notes (now linked to Mass of Injectant, Allocated Bio-Oil Mass + 3 allocated-distance datapoints), and the BCU RD-EAC retirement cert. Document set complete. [log:certify.certify_sources_filenames] [log:rereview_2026_06_25.sources_tab_total]","Certify Sources"),
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
ws.column_dimensions["D"].width = 95
ws.column_dimensions["E"].width = 20

# ---- Sheet 2: per-offload mass reconciliation ----
ws2 = wb.create_sheet("Per-Offload Mass")
hdr = ["Offload (consumed_lot)","Railcar","Full (lb)","Empty (lb)","Net Scaled (kg)","Unc. Adj (kg)","Sparging (kg)","Filtration (kg)","MOBI (kg)","COBB offloaded (kg)","Ticket gross match"]
ws2.append(hdr)
for c in ws2[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
offs = [
 ("Rail_TIMX201060_5.7.2026_offload_4","TIMX201060",53920,33320,9343.9952,39.4706,120.0283673,17.90976765,9166.586465,9304.52464,"Y"),
 ("Rail_GPRX5102_5.7.2026_offload_1","GPRX5102",81420,29080,23741.00528,0,306.2589681,45.69775531,23389.04856,23741.00528,"Y"),
 ("Rail_GPRX5102_5.7.2026_offload_2","GPRX5102",81560,29400,23659.35872,0,305.2057275,45.54059834,23308.61239,23659.35872,"Y"),
 ("Rail_GPRX5102_5.7.2026_offload_3","GPRX5102",79260,29500,22570.73792,0,291.1625192,43.44517203,22236.13023,22570.73792,"Y"),
 ("Rail_GPRX5102_5.7.2026_offload_4","GPRX5102",51240,29300,9951.80848,1672.9104,106.7977852,15.93559557,8156.164699,8278.89808,"Y"),
 ("Rail_TILX200231_5.11.2026_offload_1","TILX200231",78660,29140,22461.87584,0,289.7581983,43.2356294,22128.88201,22461.87584,"Y"),
 ("Rail_TILX200231_5.11.2026_offload_2","TILX200231",74820,29640,20493.28656,0,264.3633966,39.44640017,20189.47676,20493.28656,"Y"),
 ("Rail_TILX200231_5.11.2026_offload_3","TILX200231",82020,29220,23949.6576,0,308.950583,46.09937868,23594.60764,23949.6576,"Y"),
 ("Rail_TILX200231_5.11.2026_offload_4","TILX200231",58780,32780,11793.392,448.212,146.352822,21.837713,11176.98947,11345.18,"Y"),
]
for o in offs:
    ws2.append(list(o))
    for col in range(1,len(hdr)+1): ws2.cell(ws2.max_row,col).border = BORDER; ws2.cell(ws2.max_row,col).alignment=WRAP
ws2.append(["WEEK TOTAL","3 railcars","","","167965.12","2160.59","2138.88","319.15","163346.50 (injected)","165804.52 (=Mass Used post-adj)",""])
for col in range(1,len(hdr)+1):
    ws2.cell(ws2.max_row,col).font=BOLD; ws2.cell(ws2.max_row,col).fill=HEADER_FILL; ws2.cell(ws2.max_row,col).border=BORDER
ws2.append([])
ws2.append(["Railcar BOL-aggregate reconciliation:"])
ws2.append(["GPRX5102: 23741.01+23659.36+22570.74+8278.90 = 78250.0 = BOL aggregate (26.05+26.09+26.11)"])
ws2.append(["TILX200231: 22461.88+20493.29+23949.66+11345.18 = 78250.0 = BOL aggregate (26.16+26.20+25.89)"])
ws2.append(["TIMX201060: this week offload_4 9304.52; offloads 1-3 (68755.48) claimed prior week INJ-05-2026-W4; total = 78060.0 BOL aggregate"])
for col_w,w in [("A",42),("B",13),("C",10),("D",10),("E",14),("F",12),("G",12),("H",12),("I",20),("J",22),("K",10)]:
    ws2.column_dimensions[col_w].width = w

# ---- Sheet 3: Certify-vs-Source evidence matrix ----
ws3 = wb.create_sheet("Source Matrix")
ws3.append(["Certify value","Required sources (Max matrix)","Source-derived","Certify","Match"])
for c in ws3[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
MATRIX = [
 ("** EVIDENCE-ATTACHMENT FINDING — RESOLVED 2026-06-25 **","Ops Notes is now ATTACHED in Certify (47 sources; live re-review). Linked to Mass of Injectant, Allocated Bio-Oil Mass + 3 allocated-distance datapoints.","Every component whose required sources include 'Ops Notes' now has that evidence attached - prior FAILs 3.5 / 7.1 / 9.1 / 9.2 / 9.4 all flipped to Pass. Values reconcile AND the required evidence is attached.","","RESOLVED"),
 ("Mass of Injectant","All scale tickets + Ops Notes","163,346.50 kg (Sigma 9 offload MOBI; nets from 18 tickets) - VALUE OK, OPS NOTES NOW ATTACHED","163,346.5 kg","="),
 ("Carbon Content","Lab test","42.2% (SGS SR26-03624.001)","42.20%","="),
 ("Allocated Bio-Oil Mass (pre-sparge)","All scale tickets + all BOLs + Ops","165,804.52 kg (railcar sums = BOL aggregates)","165,804 kg","="),
 ("Pyrolysis Process","tickets + BOLs + Ops x EF sheet","165.804 t x 0.1040167 = 17.244 t","17.244 t","="),
 ("Pyrolysis Embodied","tickets + BOLs + Ops x EF sheet","165.804 t x 0.02116 = 3.508 t","3.508 t","="),
 ("Transport AECN->SOPOR Process","tickets + BOLs + Ops x dist x EF sheet","165.804 x 107.5 mi x 0.0001143 = 2.037 t","2.037 t","="),
 ("Transport Rail Process","tickets + BOLs + Ops x dist x EF sheet","165.804 x 2199 mi x 0.000025910374 = 9.447 t","9.447 t","="),
 ("Transport Opel->Basco Process","tickets + BOLs + Ops x dist x EF sheet","165.804 x 42.9 mi x 0.0001143 = 0.813 t","0.813 t","="),
 ("Transport AECN->SOPOR Embodied","alloc dist (Ops) x EF sheet","683.44 mi x 0.00023756059 = 0.162 t","0.162 t","="),
 ("Transport Rail Embodied","alloc dist (Ops) x EF sheet","4660.11 mi x 0.0000311307 = 0.145 t","0.145 t","="),
 ("Transport Opel->Basco Embodied","alloc dist (Ops) x EF sheet","772.2 mi x 0.00023756059 = 0.183 t","0.183 t","="),
 ("Allocated dist AECN->SOPOR","Ops Notes + Google Maps","Ops sum 683.44 mi (full 322.5 x mass/railcar)","683 mi","="),
 ("Allocated dist Rail","Ops Notes + Google Maps","Ops sum 4660.11 mi","4660 mi","="),
 ("Allocated dist Opel->Basco","Ops Notes + Google Maps","Ops sum 772.2 mi (85.8/offload x 9)","772 mi","="),
 ("Full dist AECN->SOPOR","Google Maps","Maps 172 km (~107.5 mi)","173.00 km","ties (1km)"),
 ("Full dist Rail","Watco email (rail exception)","Watco 'total mileage 2199'","2199 mi","="),
 ("Full dist Opel->Basco","Google Maps","Maps I-49 S 42.9 mi","43 mi","="),
 ("Emission Factors (all)","Standard EF Sheet 2026","truck proc 0.0001143; rail proc 0.000025910374; truck emb 0.00023756059; railcar emb 0.0000311307; pyro proc 0.1040167; pyro emb 0.02116","Certify display matches","="),
]
for m in MATRIX:
    ws3.append(list(m))
    for col in range(1,6): ws3.cell(ws3.max_row,col).alignment=WRAP; ws3.cell(ws3.max_row,col).border=BORDER
for cw,w in [("A",30),("B",34),("C",58),("D",16),("E",10)]: ws3.column_dimensions[cw].width=w

out = "outputs/qa/batch-week1-aecn/Batch_INJ-06-2026-W1_QA_Checklist.xlsx"
wb.save(out)
print("saved", out)
# quick status tally
from collections import Counter
tally = Counter(r[2] for r in ROWS if r[2] not in ("SECTION",))
print("tally:", dict(tally))
