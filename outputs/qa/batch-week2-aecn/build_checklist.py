#!/usr/bin/env python3
"""Build INJ-06-2026-W2 AECN weekly batch QA checklist."""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

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
 ("INJ-06-2026-W2 — AECN Weekly Batch QA", "Reviewer: Claude QA Agent  |  Date: 2026-06-24  |  Injection Site: Basco 6  |  Oil Type: AECN (rail)  |  Week: Sat 2026-06-06 to Sat 2026-06-13  |  Injected: 2026-06-14  |  Certify GHG entry rmv_1KVJW9TAM1S0QVQ2  |  Net CDR 416.33 tCO2e","SECTION","",""),
 ("Scope","Time-block (weekly) batch = all AECN oil for the week, ONE aggregated Certify GHG entry. AECN is ALL RAIL: 16 truck-out offloads from 4 railcars (GPRX5240 / GPRX5139 / TILX200228 / GPRX5106, 4 offloads each). WODO + QOWV were also injected this week but are OUT OF SCOPE (separate skills); this entry is AECN-only. [log:batch_id]","SECTION","",""),
 ("SUMMARY OF FINDINGS","RE-RUN 2026-06-25: GPRX5139 O3 empty-ticket duplicate RESOLVED (Garrett re-uploaded the genuine 29,560 ticket; item 2.1 now Pass). All other findings UNCHANGED on fresh re-pull (Ops Notes, Certify, Drive). 5 root causes: (1) Ops Notes not attached in Certify -> 7.1/9.1/9.2/9.4 (same gap as W1). (2) W2 AECN lab CoA absent everywhere -> 4.1 + Sec-4 dependents. (3) TILX200228 offload_3 Ops mis-transcription (tickets+COBB say 21,309.75; Ops says 22,362.09) -> 2.4/2.5/2.7/5.2; spurious FC11 back-calc; net over-credit only ~6 kg / 0.009 t. (4) Embodied allocated distances wrong: AECN->SOPOR 4x too high, Opel->Basco 32x too low -> 3.5/9.2; net +0.6 t emission (Net CDR conservatively understated). (5) Source set incomplete (Ops Notes + CoA) -> 9.10. All mass/EF/uncertainty math otherwise reconciles to Certify.","SECTION","",""),

 ("1. Batch Folder Completeness","","SECTION","",""),
 ("1.1","Batch folder named with batch ID","Pass","Drive folder '1_OtwOV...QgYhq' holds INJ-06-2026-W2; Ops Notes header batch ID 'INJ-06-2026-W2'. [log:batch_id]","VR Appendix 1"),
 ("1.2","Scale Tickets subfolder present and populated","Pass","Scale Tickets folder holds 4 railcar subfolders (GPRX5240/GPRX5139/TILX200228/GPRX5106), each with O1-O4; 32 ticket images total (full+empty x 16 offloads), all opened and read. One misfiled duplicate noted in 2.1. [log:scale_tickets.reads]","VR Appendix 1"),
 ("1.3","Testing subfolder present with lab results","Fail","The W2 AECN lab Certificate of Analysis is ABSENT. Exhaustive Drive search (5 queries) found only a chain-of-custody TEMPLATE ('June 2026 Week 2 SGS CoC Template') and a solids-content dataset - no SGS CoA reporting the composite '6-2026-W2 AECN' carbon/H/N/density. It is also not among the 92 Certify Sources, and the Ops Summary 'Lab COA Link' cell is blank. (W1 had '6-2026-W1 AECN.pdf' / SR26-03163.) Garrett to file the W2 AECN CoA. [log:lab_results] [log:lab_results.finding_FAIL]","VR Appendix 1"),
 ("1.4","Ops Notes present and complete","Pass","Weekly master workbook 'INJ-06-2026-W2 Ops Notes' (Summary + AECN Rail tabs); all sections populated, downloaded and read in full locally. [log:ops_notes._primary_source_opened]","VR Appendix 1"),
 ("1.5","Injection site confirmed Basco 6","Pass","BOLs route AECN -> SOPOR (Baie-Comeau) -> Basco; Certify is the Charm Bio-oil Geologic Storage (Basco) project; all source docs reference Basco/SOPOR/AECN only. No deprecated Vaulted references. [log:bol.all_dest_sopor]","Basco verification"),

 ("2. Scale Tickets & Mass Determination","","SECTION","",""),
 ("2.1","Full and empty ticket images present per offload","Pass","All 32 tickets present and legible (CAT Scale 3122, Bunkie LA; axle breakdown sums to gross on every ticket). RESOLVED on 2026-06-25 re-run: Garrett re-uploaded the GPRX5139 offload_3 empty ticket (Empty_Ticket_Rail_GPRX5139_5.8.2026_offload_3 (1).pdf, ticket #1312226160902, 6-09-26, axles 10600+10080+8880 = gross 29,560, CH1/KL720) - replacing the earlier misfiled duplicate of offload_4. The 29,560 matches Ops Notes, nets to 19,431.88 = Ops, and the vehicle pair now matches the O3 full (CH1/KL720). [log:scale_tickets] [log:scale_tickets.rerun_2026-06-25]","VR Sec 5.1"),
 ("2.2","Ticket dates within 2 weeks of injection","Pass","All 32 ticket dates read; offload weighings span 2026-06-05 to 2026-06-13 vs injection 2026-06-14 (COBB) - all within 14 days. [log:scale_tickets.reads]","VR Sec 3.5"),
 ("2.2b","Empty ticket date on or after full ticket date","Pass","Per offload (full -> empty) verified empty >= full on all 16 offloads (e.g. GPRX5240 O1 6-05/6-06; TILX200228 O2 6-12/6-13; GPRX5139 O4 6-09/6-10). [log:scale_tickets.reads]","VR Sec 5.1"),
 ("2.3","Tractor & trailer numbers match between full and empty","Pass","Every offload pair (where both tickets present) has matching tractor+trailer: e.g. GPRX5240 O1 CH1/KL188, O2 CH2/KL192, O3 CH1/KL510, O4 CH1/KL720; TILX200228 O1 CH2/KL192, O2 CH2/KL188, O3 CH2/KL510, O4 CH1/KL720; GPRX5106 all pairs match; GPRX5139 all four pairs match (O3 now CH1/KL720 full + empty after the 2026-06-25 re-upload, per 2.1). Charm fleet CH1/CH2 + KL trailers. Cleaner than W1. [log:scale_tickets.reads] [log:scale_tickets.rerun_2026-06-25]","VR Sec 5.1"),
 ("2.4","Net mass correctly calculated in Ops Notes (each offload recomputed)","Fail","15 of 16 offloads: Net (kg) = (Full lb - Empty lb) x 0.453592 from the ticket images = Ops offload-table net exactly (e.g. GPRX5240 O1 (80080-28860)=23,232.98; GPRX5106 O3 (77040-29040)=21,772.42). FAIL on TILX200228 offload_3: the scale tickets read Full 75,560 / Empty 28,580 (verified twice, axle-reconciled: 10140+32520+32900=75,560 and 9400+11200+7980=28,580), net (75560-28580)x0.453592 = 21,309.75 kg. Ops Notes recorded Full 78,560 / Empty 29,260 -> net 22,362.09 kg, i.e. ~+1,052 kg over the tickets. COBB independently shows 21,309.75 for this offload (matches the tickets, not Ops). So the Ops Notes O3 cell is a transcription error. [log:scale_tickets.findings] [log:_derived_values.tilx_o3_ticket_net_kg] [log:_derived_values.offload_net_examples] [log:cobb.findings]","VR Sec 5.1"),
 ("2.5","Conservative / last-offload (FC11) mass policy applied per railcar","Fail","Three of four railcars correct (offloaded < BOL aggregate -> documented loss, no back-calc): GPRX5240 76,947.35 vs BOL 77,730 (loss 782.65); GPRX5139 78,072.26 vs 78,140 (loss 67.74); GPRX5106 78,489.56 vs 78,550 (loss 60.44). FAIL on TILX200228: with the correct ticket O3 net (21,309.75), the 4 offloads sum to 78,153.90 kg vs BOL aggregate 78,160 (normal 6.1 kg loss) - NO back-calc needed. But because Ops inflated O3 to 22,362.09, the Ops sum is 79,206.24 (a physically impossible 1,046 kg OVERDRAW), which spuriously triggered the FC11 back-calc (Uncertainty Adjustment 1,046.24 kg on offload_4). The back-calc is an artifact of the O3 transcription error. [log:scale_tickets.findings] [log:_derived_values.tilx_offload_sum_ticket_kg] [log:ops_notes.railcars]","GHG Stmt Sec C"),
 ("2.6","1.29% sparging deduction applied","Pass","Recomputed (Mass Used post-adj 311,669.16) x 0.0129 = 4,020.53 kg vs Ops Notes sparging loss 4,020.53. Match. [log:ops_notes.rollup]","GHG Stmt Sec C"),
 ("2.7","Mass values consistent across scale tickets, Ops Notes, COBB, Certify","Fail","Two inconsistencies. (a) TILX200228 O3 (material direction): Ops/Certify chain uses 22,362.09 kg; scale tickets + COBB say 21,309.75 kg. Certify Allocated Bio-Oil Mass (311.669 t) was built from Ops Mass Used, so it over-credits by ~6.1 kg / ~0.009 tCO2e (immaterial to the 416.33 t headline, but Certify does not match the authoritative tickets+COBB on this offload). (b) GPRX5240 O4: COBB offloaded 10,523.33 vs scale-ticket/Ops/Certify net 10,750.13 (COBB implies empty 30,020 vs the ticket's 29,520) - here COBB is the outlier and tickets/Ops/Certify agree; Garrett-side COBB hygiene. [log:scale_tickets.findings] [log:cobb.findings] [log:_derived_values.weekly_overcredit_kg]","VR Sec 5.1"),
 ("2.8","Filtration loss (0.195%) deduction","Pass","Recomputed (Mass Used 311,669.16 - sparging 4,020.53) x 0.00195 = 599.91 kg vs Ops Notes filtration loss 599.91. Confirmed by Max as a correct/expected weekly deduction (conservative, reduces credited mass). [log:ops_notes.rollup]","GHG Stmt Sec C"),

 ("3. Bills of Lading & Transportation","","SECTION","",""),
 ("3.1","All truck BOLs present (3 per railcar into SOPOR)","Pass","All 12 BOLs opened and read individually (period folder, id ...uPGsaG): 2356/2357/2358-R (GPRX5240), 2365/2366/2367-R (GPRX5139), 2371/2372/2373-R (TILX200228), 2374/2375/2376-R (GPRX5106). [log:bol.reads]","VR Appendix 1"),
 ("3.2","BOL destination = SOPOR railyard","Pass","All 12 BOLs Ship To 'CHARM/WATCO, Societe du port ferroviaire de Baie-Comeau (SOPOR)', Baie-Comeau QC. [log:bol.all_dest_sopor]","VR Appendix 1"),
 ("3.3","BOL delivered mass matches Ops ledger (each); railcar agg >= claimed","Pass","Per-BOL scale-weighed 'Product delivered' (MT) vs Ops origins ledger - all 12 match exactly: 2356 25.82, 2357 25.82, 2358 26.09, 2365 25.90, 2366 26.10, 2367 26.14, 2371 25.93, 2372 26.00, 2373 26.23, 2374 26.16, 2375 26.20, 2376 26.19. Railcar BOL aggregates 77,730 / 78,140 / 78,160 / 78,550 kg each >= that railcar's claimed offload mass. [log:bol.reads] [log:bol.per_railcar_bol_sum_vs_loaded]","VR Sec 3.5"),
 ("3.4","Origin and destination correct (all 12)","Pass","All 12 BOLs: origin BioEnergie AE Cote-Nord (175 Portage des Mousses, Port-Cartier QC = AECN) -> destination SOPOR (Baie-Comeau); product RFO bio-oil (pyroligneous acids, CAS 8030-97-5). [log:bol.all_origin_aecn]","PDD Sec A"),
 ("3.5","Transport distances verified per source type","Fail","FULL (non-allocated) distances are evidenced and correct: AECN->SOPOR 173 km (Certify) / Google Maps route maps present (May-07/08/11/13-2026); SOPOR->Opelousas 2,199 mi (Watco, image (44).png - carrier confirmation, the rail exception); Opelousas->Basco 43 mi (Google Maps). FAIL on the ALLOCATED (embodied) distances: (a) AECN->SOPOR allocated = 8,279.70 km (=5,144.8 mi) in Certify, EXACTLY 4.00x the Ops EE total 1,286.23 mi (2,070 km); (b) Opelousas->Basco allocated = 43 mi in Certify vs Ops EE total 1,372.8 mi (42.9 x 2 round-trip x 16 offloads). Rail allocated 8,770 mi = Ops 8,770.26 (OK). These drive the embodied-emission errors in 9.2. Also: the allocation working lives in the Ops Notes, which is not attached in Certify (see 9.x). [log:allocated_distance_findings] [log:certify.datapoints]","Transport Emissions Acctg v1.1"),
 ("3.6","Transport mode / 6 rail components present","Pass","6 transport components in Certify: AECN->SOPOR tanker (process+embodied), SOPOR->Opelousas rail (process+embodied), Opelousas->Basco tanker (process+embodied). [log:certify.components]","Certify Datapoints"),
 ("3.7","Billing / BOL details consistent","Flag","Mass/routing all correct; documentation hygiene only: (a) Ops origins-ledger 'Date' = railcar consolidation date (5/7, 5/8, 5/11, 5/13) vs actual BOL loading dates 4/30-5/12 (systematic, by-design). (b) BOL print quirks: prod-period typos '#10-2024' on 2366/2367/2374-R; PO 'Q42025'/prod-period '4-2026' on 2356-R; 2358-R '***Corrections' note. Each BOL also shows an estimated loaded qty (vol x density) distinct from the scale-weighed delivered mass Ops correctly uses. [log:bol.print_quirks_FLAG] [log:bol.reads]","VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing","","SECTION","",""),
 ("4.1","CHN / CoA present","Fail","No W2 AECN SGS Certificate of Analysis exists in Certify Sources, the batch Drive folder, or Drive search (5 queries; only a CoC template + solids dataset). The Carbon Content datapoint (40.80%) in Certify is mis-linked to scale-ticket images instead of a lab certificate. The carbon value driving the 459.4 t sequestration is not verifiable against lab evidence as filed. [log:lab_results.finding_FAIL] [log:certify.sources_findings]","VR Appendix 1"),
 ("4.2","Carbon content within expected AECN range","Flag","The reported carbon 40.80% (Ops Summary + Certify datapoint) is within the historical AECN range: mean 39.42 +/- SD 6.09 (n=285, MRV_AECN_Analysis.xlsx, 2-SD band 27.2-51.6%), at +0.23 SD. The value is plausible, but cannot be verified against a lab certificate (none filed - see 4.1). [log:mrv_historical] [log:lab_results.carbon_pct_ops_and_certify]","Biomass Feedstock Acctg v1.2"),
 ("4.3","Hydrogen / nitrogen / viscosity reported and reasonable","Flag","These parameters live only on the SGS CoA, which is absent (4.1), so H/N/viscosity for the W2 composite cannot be verified. Pending the CoA. [log:lab_results] [log:lab_results.finding_FAIL]","Biomass Feedstock Acctg v1.2"),
 ("4.4","Lab references correct batch/sample ID","Flag","Composite sample ID '6-2026-W2 AECN' is named in the Ops Summary, but the CoA itself is absent (4.1) so the sample ID on the certificate cannot be confirmed. Pending the CoA. [log:lab_results] [log:lab_results.finding_FAIL]","VR Sec 5.1"),
 ("4.5","pH/conductivity (aqueous phase)","N/A","AECN is not aqueous phase; pH is checked in 5.5. [log:oil_type]","UIC Permit"),
 ("4.6","Density above formation-fluid floor","Flag","Density is evidenced via the 12 BOLs (sample density 1.2026-1.2128 g/ml), all above the 1.01 g/cm3 formation-fluid floor and at the historical AECN mean (1.2023, n=188). The lab-cert density for the W2 composite is unavailable (4.1). [log:bol.reads] [log:mrv_historical]","VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency","","SECTION","",""),
 ("5.1","Correct batch ID and injection date","Pass","Ops Notes batch ID INJ-06-2026-W2; COBB injection_completion_date 2026-06-14 (all 16 rows). [log:cobb.injection_completion_date]","-"),
 ("5.2","Scale ticket values correctly transcribed","Fail","15 of 16 offloads transcribed correctly (ticket grosses = Ops Full/Empty lb). FAIL on TILX200228 offload_3: Ops recorded Full 78,560 / Empty 29,260 but the scale tickets read 75,560 / 28,580 (see 2.4). Transcription error in the Ops offload table. [log:scale_tickets.findings]","VR Sec 5.1"),
 ("5.3","Oil/aqueous phase reconciliation","N/A","AECN-only batch; no aqueous phase. [log:oil_type]","-"),
 ("5.4","COBB values present and matched per offload","Flag","COBB tab 'Basco Injection -- COBB', 16 rows batch_id INJ-06-2026-W2_AECN; origin_quantity_kg per railcar (77,730 / 78,140 / 78,160 / 78,550) match BOL aggregates; injection date 2026-06-14, pH 2.7. Two per-offload divergences: (i) TILX200228 O3 COBB 21,309.75 MATCHES the scale tickets (Ops Notes is the outlier at 22,362.09 - see 2.4); (ii) GPRX5240 O4 COBB 10,523.33 vs ticket/Ops/Certify 10,750.13 (COBB-side; Garrett to correct COBB). [log:cobb.findings]","-"),
 ("5.5","pH measurement noted","Pass","pH 2.7 recorded across all offloads (within target 2.0-4.0). [log:ops_notes.rollup]","-"),
 ("5.6","Completion date matches COBB","Pass","Ops injection date and COBB injection_completion_date both 2026-06-14. [log:cobb.injection_completion_date]","-"),
 ("5.7","Density measurement","Pass","Weekly format has no Ops density field; density is evidenced via the 12 BOLs (1.2026-1.2128 g/ml, above the 1.01 floor; see 4.6). No erroneous density value present. [log:bol.reads]","VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation","","SECTION","",""),
 ("6.1","AECN process emissions LCA CI spreadsheet present","Pass","Certify Sources include 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx'. [log:certify.sources_findings]","VR Appendix 1"),
 ("6.2","LCA with stack emissions file present","Pass","Certify Sources include 'BH 2025 LCA w Stack Emissions.xlsx'. [log:certify.sources_findings]","VR Appendix 1"),
 ("6.3","Supporting GHG data file present","Pass","Certify Sources include 'Supporting GHG data 31Dec2025 S.xlsx'. [log:certify.sources_findings]","VR Appendix 1"),
 ("6.4","AECN pyrolysis process EF matches current value","Pass","Certify CI 0.104 tCO2e/t; live Standard EFs 2026 tab AECN Production H1 2026 = 0.1040167 MTCO2e/MT. [log:ef_live_source]","Certify Datapoints"),
 ("6.5","AECN pyrolysis embodied EF applied","Pass","Certify CI 0.02116 tCO2e/t; live Standard EFs 2026 tab AECN Embodied = 0.0211600 MTCO2e/MT (exact). [log:ef_live_source]","Certify Datapoints"),
 ("6.6","Pyrolysis EF mass basis = pre-sparging Allocated Bio-Oil Mass","Pass","Both pyrolysis components use Allocated Bio-Oil Mass 311.669 t (pre-sparging Mass Used), not the post-deduction injectant 307.049 t. Read from both modal INPUTS. [log:certify.datapoints.allocated_bio_oil_mass_t]","Certify Components"),

 ("7. Gross-to-Net Calculation","","SECTION","",""),
 ("7.1","Gross CO2e = injectant mass x carbon x 3.667","Fail","Value reconciles: 307,048.71 kg x 0.408 x 3.667 / 1000 = 459.387 t = Certify injection sequestration 459.387 t. BUT two evidence gaps: (a) the Ops Notes (the mass build-up net->FC11 adj->1.29% sparging->0.195% filtration->MOBI) is NOT attached in Certify - Mass of Injectant is backed only by scale tickets (63 sources), so a verifier cannot reproduce 307,048.71 kg from attached evidence; (b) the carbon 40.80% has no lab CoA attached (4.1). Garrett to attach Ops Notes + lab CoA. [log:certify.sources_findings] [log:_derived_values.gross_co2e_recalc_t] [log:certify.datapoints.mass_of_injectant_t]","GHG Stmt Sec E"),
 ("7.2","Process emissions correctly deducted","Pass","Activities 63.629 t = pyrolysis (32.414 + 6.595) + transport process (3.829 + 17.758 + 1.528) + transport embodied (1.222 + 0.273 + 0.010). Recomputed components match Certify (process legs reconcile exactly; embodied distance issue is flagged in 9.2). [log:certify.calculation_view.activities_t]","GHG Stmt Sec E"),
 ("7.3","Uncertainty discount applied","Pass","Uncertainty Discount 2.539 t present in Calculation View (~0.61% of net). [log:certify.calculation_view.uncertainty_discount_t]","Isometric Standard S3.7"),
 ("7.4","Net removals consistent","Pass","Independent recompute: 459.387 (seq) + 23.115 (BCU) - 63.629 (activities) - 2.539 (uncertainty) = 416.334 t = Certify Net 416.333 (rounding). Note: the embodied-distance errors (9.2) overstate activities by ~0.6 t, so the true Net is ~0.6 t HIGHER (Certify is conservative); and the TILX O3 issue over-credits seq by ~0.009 t. [log:_derived_values.net_recalc_t] [log:certify.calculation_view.net_co2e_removed_t]","GHG Stmt Sec E"),

 ("7a. Per-Component Uncertainty Verification","","SECTION","",""),
 ("7a.1","Completeness: every component carries uncertainty on the correct datapoint","Pass","Opened modals: injection sequestration (carbon + mass), SOPOR->Opelousas rail process (mass of load), AECN->SOPOR truck embodied (no mass term, per-mile - correct), pyrolysis process + embodied (bio-oil mass). All transport-process + pyrolysis components share the 'Allocated Bio-Oil Mass' datapoint carrying the uncertainty; embodied carry none (per-mile EF), as expected. [log:certify.uncertainty_modals_read]","Isometric Standard S3.7.3"),
 ("7a.2","Correctness: reported uncertainty matches expected","Pass","Carbon content +/-0.1632% = 0.004 x 40.80 (0.4%). Mass uncertainty +/-1,161.12 kg on Mass of Injectant and on Allocated Bio-Oil Mass = 16 discrete outbound weighings x 72.57 kg. Read directly from each modal's INPUTS. [log:certify.datapoints.mass_of_injectant_unc_kg] [log:_derived_values.uncertainty_mass_16weights_kg] [log:_derived_values.carbon_unc_pct] [log:_derived_values.carbon_unc_factor] [log:_derived_values.n_weighings] [log:_derived_values.per_weight_kg]","Isometric Standard S3.7.3"),
 ("7a.3","Discount presence and consistency","Pass","Aggregate uncertainty discount 2.539 t present in Calculation View, consistent with the carbon (0.4%) and mass (16x72.57 kg) inputs. [log:certify.calculation_view.uncertainty_discount_t]","Isometric Standard S3.7"),

 ("8. Data Integrity & Anomaly Check","","SECTION","",""),
 ("8.1","Outliers / anomalies investigated","Flag","Anomalies found and traced (not unexplained): (1) TILX200228 O3 Ops vs ticket/COBB mass discrepancy (2.4/2.7); (2) embodied allocated-distance errors AECN->SOPOR and Opel->Basco (3.5/9.2); (3) lab CoA absent (4.1); (4) Ops Notes not attached in Certify (7.1/9.x); (5) GPRX5240 O4 COBB-side discrepancy (5.4). Carbon 40.80% in range (4.2); all mass/EF/uncertainty math reconciles to Certify. [log:scale_tickets.findings] [log:allocated_distance_findings]","GHG Stmt Sec C"),
 ("8.2","Spills/losses documented and deducted","Pass","No spill/loss events in Ops Notes or COBB (both read in full). Mass losses are only routine sparging + filtration + the per-railcar documented offload losses. [log:ops_notes._primary_source_opened] [log:cobb._primary_source_opened]","GHG Stmt Sec C"),
 ("8.3","Cross-week carve-out / no double-count","Pass","All 4 W2 railcars are new this week (GPRX5240/GPRX5139/TILX200228/GPRX5106); none appear in INJ-06-2026-W1 (TIMX201060/GPRX5102/TILX200231) or INJ-05-2026-W4 Ops Notes; Ops 'Prior-RP Claimed' = 0 for all 4; COBB origin_quantity per railcar = BOL aggregate. No double-count. [log:cross_week_carveout_verified]","VR Sec 3.5"),
 ("8.4","Rail uncertainty conservatism (N_offloads >= N_BOLs per railcar)","Pass","Each railcar: 4 offloads >= 3 inbound BOLs. Per-offload 72.57 kg framing is conservative; weekly mass uncertainty stacks to 16 x 72.57 = 1,161.12 kg. [log:ops_notes.offload_table] [log:_derived_values.uncertainty_mass_16weights_kg]","Isometric Standard S3.7.3"),

 ("9. Isometric Certify — Removal Component Mapping","","SECTION","",""),
 ("9.1","Sequestration matches internal gross","Fail","Value reconciles (307,048.71 kg x 0.408 x 3.667 = 459.387 t = Certify), but inherits the evidence gaps from 7.1: Mass of Injectant lacks the Ops Notes (mass build-up not reproducible from attached evidence) and Carbon lacks a lab CoA (4.1). Garrett to attach Ops Notes + CoA. [log:certify.sources_findings] [log:certify.components.injection_sequestration_t]","Certify Components"),
 ("9.2","Transport: process + embodied per leg","Fail","PROCESS legs all reconcile (mass x full-leg distance x EF): AECN->SOPOR 311.669 t x 107.5 mi x 0.0001143 = 3.830 t (Certify 3.829); rail x 2199 mi x 0.0000259104 = 17.758 (Certify 17.758); Opel->Basco x 42.9 mi x 0.0001143 = 1.528 (Certify 1.528). EMBODIED legs - two errors: (a) AECN->SOPOR embodied uses allocated distance 8,279.70 km (=5,144.8 mi), EXACTLY 4x the Ops EE total 1,286.23 mi; emission 1.222 t vs correct ~0.306 t (OVERSTATED +0.917 t). (b) Opelousas->Basco embodied uses 43 mi vs Ops EE total 1,372.8 mi; emission 0.010 t vs correct ~0.326 t (UNDERSTATED -0.316 t). Rail embodied 0.273 t (8,770 mi = Ops) OK. Net embodied error +0.601 t too much emission -> Net CDR conservatively understated ~0.6 t (below 5% materiality, but Certify allocated distances do not match Ops for 2 of 3 embodied legs). Also: Ops Notes (the allocation working) is not attached. Garrett to correct the two allocated-distance datapoints + attach Ops Notes. [log:allocated_distance_findings] [log:_derived_values.sopor_proc_recalc_t] [log:_derived_values.rail_proc_recalc_t] [log:_derived_values.opel_proc_recalc_t] [log:_derived_values.sopor_emb_certify_t] [log:_derived_values.opel_emb_certify_t]","Certify Components"),
 ("9.3","Injection: LCS / sample transport","N/A","AECN requires no LCS pre-treatment; no LCS component on this entry. [log:oil_type]","Certify Components"),
 ("9.4","Pyrolysis: process + embodied present","Fail","Values reconcile: process 311.669 t x 0.1040167 = 32.419 (Certify 32.414); embodied x 0.02116 = 6.595 (Certify 6.595); both use pre-sparging Allocated Bio-Oil Mass; rail-batch naming ('from rail loads') is the deliberate VVB signal. FAIL only on evidence attachment: the mass basis (Allocated Bio-Oil Mass) is backed by scale tickets + BOLs with no Ops Notes among the 92 attached sources, so the mass build-up is not verifier-reproducible. Garrett to attach Ops Notes. [log:certify.sources_findings] [log:_derived_values.pyro_process_recalc_t] [log:_derived_values.pyro_embodied_recalc_t]","Certify Components"),
 ("9.5","Reductions: applicable BCU categories populated","Pass","BCU - Transport Process credit present (only category applicable for AECN rail without site-emission burden). [log:certify.components.bcu_transport_process_t]","Certify Components"),
 ("9.6","BCU quantity >= corresponding activity emission","Pass","Transport process sum recomputed 3.829 + 17.758 + 1.528 = 23.115 t = BCU - Transport Process 23.115 t (exact coverage). Embodied not BCU-eligible per protocol. [log:_derived_values.transport_process_sum_t] [log:certify.components.bcu_transport_process_t]","Certify Components"),
 ("9.7","Counterfactuals zero per protocol","Pass","No counterfactual component; bio-oil geological storage counterfactual is zero per protocol. [log:certify.datapoints]","Certify Components"),
 ("9.8","Net removal matches internal calculation","Pass","Independent gross-to-net 416.334 t (459.387 + 23.115 - 63.629 - 2.539) = Certify Net 416.333 (rounding). [log:_derived_values.net_recalc_t] [log:certify.calculation_view.net_co2e_removed_t]","Certify Calculation View"),
 ("9.9","Descriptive source filenames","Flag","Hygiene (content correct, naming/linkage only): (a) generic EF source filenames 'Screenshot 2026-02-23...png', 'Screenshot 2026-04-10...png', 'image (44).png'; (b) duplicate scale-ticket uploads (92 sources vs ~63 unique - several tickets appear twice); (c) Carbon Content datapoint linked to scale-ticket images rather than a lab CoA; (d) BCU 'Constant CO2 reduction' sourced from 'Charm-RetirementCertificate-RD-EACs-20251218.pdf' (a Dec-2025 RD-EAC retirement cert) - quantity 23.115 = transport process sum exactly, but Garrett to confirm a Dec-2025 EAC cert is the intended coverage for June-2026 transport. [log:certify.sources_findings]","Certify Datapoints"),
 ("9.10","Sources match Drive / complete set","Fail","The 92 Certify Sources are INCOMPLETE for verifier reproducibility: the INJ-06-2026-W2 Ops Notes is not attached (drives 7.1/9.1/9.2/9.4), and the W2 AECN lab CoA is not attached (4.1). The set also contains duplicate ticket uploads (9.9). Garrett to attach the Ops Notes and the lab CoA and de-duplicate. [log:certify.sources_findings] [log:certify.attachment_map_note]","Certify Sources"),
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
ws.column_dimensions["E"].width = 20

# ---- Sheet 2: per-offload mass reconciliation ----
ws2 = wb.create_sheet("Per-Offload Mass")
hdr = ["Offload","Railcar","Full (lb)","Empty (lb)","Net (kg) Ops","Net (kg) TICKET","COBB offloaded","Match notes"]
ws2.append(hdr)
for c in ws2[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
offs = [
 ("GPRX5240 O1","GPRX5240",80080,28860,23232.98,23232.98,23232.98,"all match"),
 ("GPRX5240 O2","GPRX5240",78360,29480,22171.58,22171.58,22171.58,"all match"),
 ("GPRX5240 O3","GPRX5240",75500,29660,20792.66,20792.66,20792.66,"all match"),
 ("GPRX5240 O4","GPRX5240",53220,29520,10750.13,10750.13,10523.33,"COBB outlier (-226.80; implies empty 30020); ticket/Ops/Certify agree 10750.13"),
 ("GPRX5139 O1","GPRX5139",79260,29380,22625.17,22625.17,22625.17,"all match"),
 ("GPRX5139 O2","GPRX5139",76020,29340,21173.67,21173.67,21173.67,"all match"),
 ("GPRX5139 O3","GPRX5139",72400,29560,19431.88,19431.88,19431.88,"empty ticket image misfiled (dup of O4); value 29560 reconciles+balances"),
 ("GPRX5139 O4","GPRX5139",61960,29240,14841.53,14841.53,14841.53,"all match"),
 ("TILX200228 O1","TILX200228",80240,29400,23060.62,23060.62,23060.62,"all match"),
 ("TILX200228 O2","TILX200228",79080,28920,22752.17,22752.17,22752.17,"all match"),
 ("TILX200228 O3","TILX200228","78560 / TICKET 75560","29260 / TICKET 28580",22362.09,21309.75,21309.75,"*** OPS WRONG: Ops 22362.09 vs ticket+COBB 21309.75 (+1052 over) ***"),
 ("TILX200228 O4","TILX200228",54060,29740,11031.36,11031.36,11031.36,"raw match; Ops applies spurious back-calc adj 1046.24 downstream"),
 ("GPRX5106 O1","GPRX5106",78440,29440,22226.01,22226.01,22226.01,"all match"),
 ("GPRX5106 O2","GPRX5106",78220,29160,22253.22,22253.22,22253.22,"all match"),
 ("GPRX5106 O3","GPRX5106",77040,29040,21772.42,21772.42,21772.42,"all match"),
 ("GPRX5106 O4","GPRX5106",56600,29620,12237.91,12237.91,12237.91,"all match"),
]
for o in offs:
    ws2.append(list(o))
    r=ws2.max_row
    for col in range(1,len(hdr)+1): ws2.cell(r,col).border = BORDER; ws2.cell(r,col).alignment=WRAP
    if "OPS WRONG" in o[-1] or "COBB outlier" in o[-1] or "misfiled" in o[-1]:
        for col in range(1,len(hdr)+1): ws2.cell(r,col).fill = FLAG_FILL
ws2.append([])
ws2.append(["Railcar balance:"])
ws2.append(["GPRX5240: offloaded 76,947.35 < BOL 77,730 (loss 782.65) - no back-calc"])
ws2.append(["GPRX5139: offloaded 78,072.26 < BOL 78,140 (loss 67.74) - no back-calc"])
ws2.append(["TILX200228 (TICKET): 23060.62+22752.17+21309.75+11031.36 = 78,153.90 < BOL 78,160 (loss 6.1) - NO back-calc needed"])
ws2.append(["TILX200228 (OPS, wrong O3): sum 79,206.24 > BOL 78,160 -> spurious 1,046.24 back-calc on O4"])
ws2.append(["GPRX5106: offloaded 78,489.56 < BOL 78,550 (loss 60.44) - no back-calc"])
ws2.append(["Weekly Mass Used: Ops 311,669.16 vs corrected 311,663.06 -> Ops over-credits 6.10 kg (~0.009 tCO2e), immaterial"])
for cw,w in [("A",18),("B",13),("C",22),("D",22),("E",14),("F",16),("G",16),("H",60)]: ws2.column_dimensions[cw].width=w

# ---- Sheet 3: Certify reconciliation + distance findings ----
ws3 = wb.create_sheet("Certify Recon")
ws3.append(["Component / datapoint","Source-derived (show the work)","Certify","Match"])
for c in ws3[1]:
    c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
MATRIX = [
 ("Injection sequestration","MOBI 307,048.71 kg x 0.408 x 3.667 /1000 = 459.387 t","459.387 t","="),
 ("Pyrolysis process","311.669 t x 0.1040167 = 32.419 t","32.414 t","= (CI display 0.104)"),
 ("Pyrolysis embodied","311.669 t x 0.02116 = 6.595 t","6.595 t","="),
 ("AECN->SOPOR truck PROCESS","311.669 t x 107.5 mi x 0.0001143 = 3.830 t","3.829 t","="),
 ("SOPOR->Opelousas rail PROCESS","311.669 t x 2199 mi x 0.0000259104 = 17.758 t","17.758 t","="),
 ("Opelousas->Basco truck PROCESS","311.669 t x 42.9 mi x 0.0001143 = 1.528 t","1.528 t","="),
 ("AECN->SOPOR truck EMBODIED","Ops alloc 1,286.23 mi x 0.00023756 = 0.306 t (CORRECT)","1.222 t (uses 8,279.70 km = 5,144.8 mi = 4x Ops)","FAIL +0.917 t"),
 ("SOPOR->Opelousas rail EMBODIED","Ops alloc 8,770.26 mi x 0.0000311307 = 0.273 t","0.273 t (8,770 mi)","="),
 ("Opelousas->Basco truck EMBODIED","Ops alloc 1,372.8 mi x 0.00023756 = 0.326 t (CORRECT)","0.010 t (uses 43 mi)","FAIL -0.316 t"),
 ("Transport process sum / BCU","3.829 + 17.758 + 1.528 = 23.115 t","BCU 23.115 t","ties — exact coverage"),
 ("Activities total","pyro 39.009 + transport 24.620 = 63.629 t","63.629 t","="),
 ("Uncertainty discount","carbon 0.4% + mass 16x72.57 kg propagated","2.539 t","present"),
 ("Net CO2e removed","459.387 + 23.115 - 63.629 - 2.539 = 416.334 t","416.333 t","= (rounding)"),
 ("--- EMBODIED DISTANCE FINDING ---","Net embodied error +0.917 - 0.316 = +0.601 t too much emission","Net CDR understated ~0.6 t (conservative)","FAIL 3.5/9.2"),
 ("--- ATTACHMENT FINDING ---","Ops Notes NOT in 92 Certify Sources; lab CoA NOT attached (carbon mis-linked to tickets)","Mass/pyrolysis/transport lack Ops Notes; carbon lacks CoA","FAIL 4.1/7.1/9.1/9.2/9.4/9.10"),
]
for m in MATRIX:
    ws3.append(list(m)); r=ws3.max_row
    for col in range(1,5): ws3.cell(r,col).alignment=WRAP; ws3.cell(r,col).border=BORDER
    if "FAIL" in m[-1]:
        for col in range(1,5): ws3.cell(r,col).fill=FAIL_FILL
for cw,w in [("A",34),("B",58),("C",40),("D",22)]: ws3.column_dimensions[cw].width=w

out = "outputs/qa/batch-week2-aecn/Batch_INJ-06-2026-W2_QA_Checklist.xlsx"
wb.save(out)
print("saved", out)
from collections import Counter
tally = Counter(r[2] for r in ROWS if r[2] != "SECTION")
print("tally:", dict(tally))
