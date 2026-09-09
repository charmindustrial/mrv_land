#!/usr/bin/env python3
"""Build INJ-07-2026-W2 AECN weekly batch QA checklist."""
import sys, json
from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "skills" / "qa" / "batch-qa-aecn" / "scripts"))
from checklist_lib import build_with_validation  # noqa: E402

HEADER_FILL = PatternFill("solid", fgColor="D6E4F0")
FAIL_FILL   = PatternFill("solid", fgColor="FFC7CE")
FLAG_FILL   = PatternFill("solid", fgColor="FFF2CC")
FLAG_FONT   = Font(color="996600")
NA_FONT     = Font(color="808080", italic=True)
BOLD        = Font(bold=True)
WRAP        = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

D = json.loads((HERE / "weekly_mass_chain_findings.json").read_text())["derived"]
D["kl192_std_tare_lb"] = 29510
D["carbon_2sd_low_pct"] = 27.2337
D["carbon_2sd_high_pct"] = 51.607
D["carbon_pct"] = 41.6
D["carbon_z_score"] = 0.3577
D["density_g_cm3"] = 1.218
D["density_floor_g_cm3"] = 1.01
D["ph"] = 3.1
D["days_ticket_to_injection_max"] = 3
D["certify_sources_total"] = 33
D["n_offloads"] = 5
D["n_bols_total"] = 6
D["n_railcars"] = 2
D["aecn_sopor_full_mi"] = 107.49722
D["aecn_sopor_km"] = 173
D["rail_full_mi"] = 2199
D["opel_basco_full_mi"] = 42.9
D["sparge_rate"] = 0.0129
D["filter_rate"] = 0.00195
D["ef_aecn_process_sheet_final"] = 0.1040167408
D["ef_aecn_process_certify_stored"] = 0.104
D["ef_aecn_embodied"] = 0.02116
D["ef_truck_fuel"] = 0.0001143
D["ef_rail_fuel"] = 2.5910374e-05
D["ef_truck_embodied"] = 0.0002375605888
D["ef_railcar_embodied"] = 3.113066508e-05
D["ghg_stmt_net_t"] = 136.8623238
D["net_before_correction_t"] = 136.862
D["bcu_before_correction_t"] = 10.193
D["bcu_after_correction_kg"] = 7269
D["ghg_stmt_gross_t"] = 147.3003238
D["ghg_stmt_reductions_t"] = 10.193
D["ghg_stmt_rp_net_mt"] = 877.8863469
D["w1_bcu_surplus_t"] = 0.0018
D["tercs_retired"] = 2795
D["bcu_pct_of_reported_net"] = 2.1365
D["jun_map_distance_mi"] = 2275.569
D["jun_map_distance_km"] = 3662.173
D["charm_three_leg_sum_mi"] = 2349.39722
D["charm_legs_minus_jun_map_mi"] = 73.82822
D["rail_ef_truncation_delta_t"] = 0.000081

DERIVED = D

HDR = ("Reviewer: Claude QA Agent  |  Date: 2026-08-06  |  Injection Site: Basco 6  |  Oil Type: AECN (rail)  |  "
       "Ops week: Sat 2026-07-04 to Sat 2026-07-11  |  Injected: 2026-07-10  |  "
       "Certify GHG entry rmv_1KYWP4BF01S0R568 (period 05-11 Jul 2026)  |  Net CDR 133.938 tCO2e after the BCU correction of 2026-08-06")

SUMMARY = (
 "REVIEWED 2026-08-06, then RE-VERIFIED the same day after Max corrected the BCU in Certify. Net CDR is now 133.938 tCO2e, "
 "down from 136.862 as originally submitted. "
 "The mass chain verifies end to end and every emission component reconstructs to the reported figure. All five offloads have "
 "matching tractor AND trailer on their full/empty ticket pair, so no standard-tare substitution was triggered and none was "
 "applied; the Ops Notes carries no cell annotations, which is consistent. Railcar TIMX201060 was fully drawn down this week and "
 "its four raw ticket nets overdraw the inbound BOL aggregate by 80.27808 kg; the Ops Notes absorbs exactly that on the closing "
 "offload, so the claimed mass equals the 78,500 kg BOL aggregate. Railcar SHPX215079 contributed only its first offload this "
 "week and correctly carries no adjustment. Gross sequestration, both pyrolysis components, all six transport components, all "
 "three allocated distances, every uncertainty input and the net arithmetic reconstruct exactly. COBB matches the Ops Notes on "
 "all five offloads including the post-adjustment closing figure, and the remaining three SHPX215079 offloads are claimed in a "
 "later batch, so there is no double count. "
 "THE ONE MATERIAL FINDING, NOW CORRECTED IN CERTIFY: the BCU offset had been entered as 10,193 kgCO2e, which is exactly the "
 "AECN pyrolysis process emission for this entry rather than a transport figure. The three transport process legs sum to 7.269 "
 "t, so the offset exceeded what it may cover by 2.924 t and overstated net CDR by the same amount. The datapoint now reads "
 "7,269 kgCO2e and Certify's net reads 133.938 t, both confirmed by re-reading Certify. Items 9.6 and 9.8 are resolved. "
 "ONE FAIL REMAINS OPEN: item 7.4. The GHG Statement Results sheet still carries the old 10.193 t reduction and 136.8623238 t "
 "net for this entry, and the reporting-period total is still 877.8863469 MT, so Certify and the statement sheet now disagree. "
 "That clears when the results are regenerated - the row should read 7.269 and 133.938 and the period total should fall to "
 "874.962 MT. "
 "SIX FLAGS, none affecting a quantity: the purchase order bound into all six BOL packages records the order two ways (header "
 "Q42025, line item Q32025, hand-corrected on one copy of six) and carries a Kansas ship-to on a Louisiana injection; COBB "
 "labels the batch INJ-20260709_bio_oil instead of INJ-07-2026-W2, so a verifier tracing by batch ID finds nothing; the "
 "pyrolysis factor is entered at 0.104 against the sheet final quantity 0.1040167408; two source files carry generic names, one "
 "of them the sole evidence for the 2199-mile rail leg; and the three allocated-distance datapoints are missing the Ops Notes "
 "linkage that would let a verifier reproduce them - two of the three files attached to each are AECN-to-Opelousas road-route "
 "cards showing 2275.569 mi, which is not any leg Charm uses and supports none of the allocated values."
 )

ROWS = [
 ("INJ-07-2026-W2 - AECN Weekly Batch QA", HDR, "SECTION", "", ""),
 ("Scope",
  "Time-block (weekly) batch = all AECN oil injected in the week, aggregated into ONE Certify GHG entry. AECN is all rail this "
  "week: 5 truck-out offloads from 2 railcars - SHPX215079 (offload 1 of 4) and TIMX201060 (offloads 1-4, fully drawn) - fed by "
  "6 inbound BOLs. WODO and QOWV were also injected this week under separate GHG entries and are out of scope here. "
  "[log:batch_id] [log:railcars] [log:offload_count]", "SECTION", "", ""),
 ("SUMMARY OF FINDINGS", SUMMARY, "SECTION", "", ""),

 ("1. Batch Folder Completeness", "", "SECTION", "", ""),
 ("1.1", "Batch folder exists with correct naming", "Pass",
  "Drive folder titled 'W2' (id 1tWbQda-dFGW7cA6H7ghj6LY224L8hB8v). The Ops Notes workbook Summary tab cell B2 and the AECN Rail "
  "tab cell B2 both read 'INJ-07-2026-W2', and the Certify source file is named 'INJ-07-2026-W2 Ops Notes.xlsx'. "
  "[log:ops_notes.batch_id] [log:drive_folder_url]", "VR Appendix 1"),
 ("1.2", "Scale Tickets subfolder present and populated", "Pass",
  "Scale Tickets holds one subfolder per railcar (SHPX215079, TIMX201060) containing 10 CAT Scale PDFs plus 10 matching phone "
  "photographs - one full + one empty pair for each of the 5 offloads. All 10 PDFs were opened and read this session; on every "
  "ticket the three axle weights sum to the printed GROSS WEIGHT. [log:scale_tickets] [log:_derived_values.n_offloads]",
  "VR Appendix 1"),
 ("1.3", "Testing subfolder present with required lab results", "Pass",
  "Testing subfolder contains the AECN certificate for this batch, 'CHARM INDUSTRIAL - AECN 7-2026-W2 (SR26-04370.001).pdf', "
  "opened and read this session. It also holds the W2 WODO and QOWV certificates, which belong to the other oil types' entries. "
  "[log:lab_results.certificate_no] [log:lab_results]", "VR Appendix 1"),
 ("1.4", "Ops Notes spreadsheet present and complete", "Pass",
  "'INJ-07-2026-W2 Ops Notes' (Google Sheet, modified 2026-08-04) present in the batch folder and attached to Certify. Eight tabs; "
  "the AECN Rail tab carries the batch header, a 2-row railcar register, a 6-row BOL origins ledger, the 5-row offload table and "
  "the Section 4 rollup, all populated. [log:ops_notes] [log:ops_notes.tabs]", "VR Appendix 1"),
 ("1.5", "Injection site confirmed as Basco 6 - no Vaulted references", "Flag",
  "Injection site is unambiguously Basco 6. The SGS certificate records LOCATION 'BASCO LOUISIANA'; the offload route map runs "
  "to 4687 LA-115, St Landry LA 71367; Certify names three components 'Opelousas to Basco'; every one of the ten scale tickets "
  "was weighed in Louisiana (Bunkie or Opelousas). A location-by-location scan of all batch evidence opened this session - ten "
  "scale tickets, six BOL packages, the lab certificate, the route evidence, the Ops Notes and the Certify component set - is "
  "saved as the artifact for this check. It found no Vaulted reference and no Hutchinson reference anywhere. It did find one "
  "Kansas address: the standing Charm purchase order Q42025, bound as page 5 of each of the six BOL packages - all six read for this review - carries Ship To "
  "'Charm Industrial, 838 SW Purity Springs Road, El Dorado, KS 67042'. That is a procurement address on a blanket order dated "
  "10/2/2025, not an injection or storage site, and it is not Vaulted Deep. It affects no quantity - the delivery path is "
  "evidenced by the BOL Ship To at the SOPOR railyard, the Watco rail record and the Louisiana offload tickets. Flagged only "
  "because a verifier reading that page in isolation sees a Kansas ship-to on a Louisiana injection, and the template is worth "
  "refreshing. [log:site_reference_scan] [log:lab_results.location] [log:certify.components]", "VR Appendix 1"),

("2. Scale Tickets & Mass Determination", "", "SECTION", "", ""),
 ("2.1", "Empty and full scale ticket images present for each truckload", "Pass",
  "5 full + 5 empty CAT Scale certificates, one pair per offload, all opened and read. SHPX215079 offload_1: full 1312226189393 / "
  "empty 1312226190402. TIMX201060 offload_1: full 1124426188220 / empty 1312226188373; offload_2: full 1312226188370 / empty "
  "1312226188375; offload_3: full 1312226189383 / empty 1312226189385; offload_4: full 1312226189384 / empty 1312226189389. "
  "Two operational details worth recording. Four of the ten are CAT Scale $5.25 reweighs carrying a TICKET # OF FULL $ "
  "WEIGH cross-reference, and on three of those four that reference points to a ticket from a different offload of the same "
  "trailer - a CAT fleet-billing artifact that does not alter the certified GROSS WEIGHT printed on each ticket, which is the "
  "value used. And TIMX201060 offload_1 was weighed full at scale 1244 (The Quarters TS, Opelousas) but empty at scale 3122 "
  "(Pilot, Bunkie), whereas the other four pairs used scale 3122 for both; both are CAT-certified weighings and tickets are "
  "paired by trailer per the reporting-period guidance. "
  "[log:scale_tickets.pairs] [log:scale_tickets.reweigh_reference_note] [log:scale_tickets]", "VR Sec 5.1"),
 ("2.2", "Ticket dates within 2 weeks of injection", "Pass",
  "Ticket dates span 7-07-26 to 7-09-26 against an injection date of 2026-07-10, so the widest gap is 3 days - well inside the "
  "14-day window. All ten fall inside the Certify period 05-11 Jul 2026. "
  "[log:scale_tickets.all_ticket_dates] [log:_derived_values.days_ticket_to_injection_max] [log:injection_date_all_offloads]",
  "VR Sec 3.5"),
 ("2.3", "Tractor and trailer numbers match between empty and full tickets", "Pass",
  "All five pairs match on BOTH identifiers: SHPX215079 offload_1 CH1/KL192 on both tickets; TIMX201060 offload_1 CH1/KL192; "
  "offload_2 CH 2/KL188; offload_3 CH1/KL192; offload_4 CH 2/KL188. Because no rig mismatch occurred, the Trailer Standard Empty "
  "Weight substitution in the July VVB guidance was not triggered on any offload, no substituted tare (KL192 29510 lb or any "
  "other) appears in the Ops Notes, and the workbook carries zero cell annotations. The comment-extraction method was verified in "
  "the same session against a workbook that does carry annotations, so the zero is a real absence rather than a read failure. "
  "[log:scale_tickets.all_rig_identifiers_match] [log:scale_tickets.standard_tare_substitutions_applied] "
  "[log:ops_notes.cell_comments_found] [log:vvb_guidance.week2_substitution_needed] [log:_derived_values.kl192_std_tare_lb]",
  "VR Sec 5.1"),
 ("2.4", "Net mass correctly calculated in Ops Notes", "Pass",
  "Each offload recomputed from the ticket images as (Full - Empty) lb x 0.453592: "
  "SHPX215079 o1 (72240 - 29220) = 43020 lb = 19513.52784 kg; TIMX201060 o1 (72920 - 29020) = 43900 lb = 19912.6888 kg; "
  "o2 (72200 - 28940) = 43260 lb = 19622.38992 kg; o3 (73040 - 29320) = 43720 lb = 19831.04224 kg; "
  "o4 (71100 - 28740) = 42360 lb = 19214.15712 kg. Every one matches the Ops Notes Net Scaled Mass cell exactly. "
  "Sum = 98093.80592 kg. [log:_derived_values.net_kg_SHPX215079_6_18_2026_offload_1] "
  "[log:_derived_values.net_kg_TIMX201060_6_22_2026_offload_1] [log:_derived_values.net_kg_TIMX201060_6_22_2026_offload_2] "
  "[log:_derived_values.net_kg_TIMX201060_6_22_2026_offload_3] [log:_derived_values.net_kg_TIMX201060_6_22_2026_offload_4] "
  "[log:_derived_values.net_lb_SHPX215079_6_18_2026_offload_1] [log:_derived_values.net_lb_TIMX201060_6_22_2026_offload_1] [log:_derived_values.net_lb_TIMX201060_6_22_2026_offload_2] [log:_derived_values.net_lb_TIMX201060_6_22_2026_offload_3] [log:_derived_values.net_lb_TIMX201060_6_22_2026_offload_4] [log:_derived_values.downstream_scale_ticket_sum_kg]", "VR Sec 5.1"),
 ("2.5", "Injectate mass uses the conservative value (railcar last-offload policy)", "Pass",
  "Railcar balance run before assessing any divergence. TIMX201060: 6 inbound BOLs give 26150 + 26190 + 26160 = 78500 kg for this "
  "car; its four raw ticket nets sum to 78580.27808 kg, an overdraw of 80.27808 kg, which is physically impossible. The Ops Notes "
  "records exactly 80.27808 kg as the Uncertainty Adjustment on offload_4, the closing offload, so claimed mass = 78580.27808 - "
  "80.27808 = 78500 kg = the BOL aggregate. SHPX215079: BOL aggregate 25940 + 26200 + 26190 = 78330 kg; only offload_1 "
  "(19513.52784 kg) was drawn this week, no overdraw is possible yet and the adjustment is correctly 0. Weekly total mass used "
  "98013.52784 kg. [log:_derived_values.bol_aggregate_TIMX201060_kg] [log:_derived_values.raw_offload_sum_TIMX201060_kg] "
  "[log:_derived_values.overdraw_TIMX201060_kg] [log:_derived_values.uncertainty_adjustment_TIMX201060_kg] "
  "[log:_derived_values.bol_aggregate_SHPX215079_kg] [log:_derived_values.uncertainty_adjustment_SHPX215079_kg] "
  "[log:_derived_values.mass_used_post_adj_kg]", "GHG Stmt Sec C"),
 ("2.6", "Sparging and filtration deductions applied", "Pass",
  "Both deductions applied per offload in sequence on the post-adjustment mass: sparging at 0.0129, then filtration at 0.00195 of "
  "the post-sparging remainder. Worked on the closing offload: base 19214.15712 - 80.27808 = 19133.87904 kg; sparging 19133.87904 "
  "x 0.0129 = 246.82704 kg; post-sparge 18887.052 kg; filtration 18887.052 x 0.00195 = 36.82975 kg; MOBI 18850.22225 kg - all "
  "three match the Ops Notes cells. Weekly: sparging 1264.37451 kg, filtration 188.66085 kg, and 98013.52784 - 1264.37451 - "
  "188.66085 = 96560.49248 kg mass of bio-oil injected. [log:_derived_values.sparge_rate] [log:_derived_values.filter_rate] "
  "[log:_derived_values.sparging_loss_total_kg] [log:_derived_values.filtration_loss_total_kg] "
  "[log:_derived_values.mobi_total_kg] [log:_derived_values.post_adj_kg_TIMX201060_6_22_2026_offload_4] [log:_derived_values.sparging_kg_TIMX201060_6_22_2026_offload_4] [log:_derived_values.filtration_kg_TIMX201060_6_22_2026_offload_4] [log:_derived_values.mobi_kg_TIMX201060_6_22_2026_offload_4]", "GHG Stmt Sec C"),
 ("2.7", "All mass values consistent across tickets, Ops Notes, COBB and Certify", "Pass",
  "Four-way tie. Scale tickets sum 98093.80592 kg = Ops Notes 'Deliveries raw / Downstream Transport' = Certify datapoint "
  "'Bio-Oil Mass - AECN via Rail (downstream, scale tickets)' 98.094 t = sum of the five COBB offloaded_quantity_kg values. "
  "After the 80.27808 kg adjustment, 98013.52784 kg = Ops Notes 'Mass Used' = Certify 'Bio-Oil Mass - AECN via Rail' 98.014 t. "
  "After sparging and filtration, 96560.49248 kg = Certify 'Mass of Injectant' 96.560 t. COBB carries the post-adjustment figure "
  "on the closing offload (19133.87904 kg), so there is no COBB-versus-Ops divergence in this batch. "
  "[log:_derived_values.downstream_scale_ticket_sum_kg] [log:_derived_values.mass_used_post_adj_kg] "
  "[log:_derived_values.mobi_total_kg] [log:cobb.offloaded_quantity_kg_sum] [log:certify.datapoints]", "VR Sec 5.1"),

 ("3. Bills of Lading & Transportation", "", "SECTION", "", ""),
 ("3.1", "Truck BOL(s) present for each shipment", "Pass",
  "All 6 inbound BOLs (2389-R through 2394-R) opened and read this session, pages 1-3 each, and all 6 appear on the Certify "
  "Sources tab. Three feed SHPX215079 and three feed TIMX201060, matching the standard 3-BOLs-per-railcar pattern. "
  "[log:bols.bols_into_railcar] [log:bols] [log:_derived_values.n_bols_total]", "VR Appendix 1"),
 ("3.2", "Rail delivery: truck BOLs from AECN present with destination = railyard", "Pass",
  "Every one of the six BOLs shows Ship To 'CHARM Industrial Inc. /WATCO, Societe du port ferroviaire de Baie-Comeau, 18 Route "
  "Maritime, Baie-Comeau, Quebec' - the SOPOR railyard, not Basco. Attention Cedric Berube, cedric.berube@sopor.ca. "
  "[log:bols.destination_all] [log:bols.destination_is_sopor_not_basco]", "VR Appendix 1"),
 ("3.3", "BOL mass matches or exceeds reported injectate mass", "Pass",
  "Applied at railcar level. TIMX201060: BOL aggregate 78500 kg against 78500 kg claimed - equal, because the closing-offload "
  "policy caps the claim at the aggregate. SHPX215079: BOL aggregate 78330 kg against 19513.52784 kg drawn this week, so ample "
  "headroom. Weekly claimed mass 98013.52784 kg never exceeds the 156830 kg of inbound BOL mass available across the two cars. "
  "[log:_derived_values.bol_aggregate_TIMX201060_kg] [log:_derived_values.bol_aggregate_SHPX215079_kg] "
  "[log:_derived_values.mass_used_post_adj_kg]", "VR Sec 3.5"),
 ("3.4", "Origin and destination correct on BOL", "Pass",
  "All six: From 'BioEnergie AE Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier, Quebec G5B 2V9'; Ship To the SOPOR "
  "railyard at Baie-Comeau. Carrier 'Transport Baie-Comeau' on all six; product 'Renewable Fuel Oil RFO / Huile pyrolytique'; "
  "AECN production period #06-2026; Charm PO Q42025. The onward legs are documented separately - the COBB Loads tab records both "
  "railcars inbound to Opelousas under carrier Watco, and the Opelousas-to-Basco leg by the offload scale tickets. "
  "[log:bols.origin_all] [log:bols.destination_all] [log:bols.carrier_all] [log:cobb.loads_tab_rows]", "PDD Sec A"),
 ("3.5", "Transportation distance consistent with the known AECN rail route", "Pass",
  "All three legs verified against their own evidence, and both shared legs are allocated. AECN->SOPOR truck: route map reads "
  "173 km via QC-138 O between the BOL origin address and SOPOR, = 107.49722 mi, matching Certify's full-leg datapoint; the "
  "allocated aggregate is 402.84103 mi, being 107.49722 x 3 inbound trucks x each offload's mass share, summed over the five "
  "offloads. SOPOR->Opelousas rail: 2199 mi, evidenced by the Watco rail logistics email ('The total milage for this move was "
  "2199'); allocated 2746.81371 mi = 2199 x the same mass shares. Opelousas->Basco truck: 42.9 mi, the longest of the three "
  "Google Maps options offered (42.9 / 42.9 / 40.9); allocated 429 mi = 42.9 x 2 for the round trip x 5 offloads, and this leg is "
  "correctly NOT mass-allocated because each offload uses its own dedicated truck. All three allocated totals match the Certify "
  "datapoints exactly. Provenance: the AECN-to-SOPOR and Opelousas-to-Basco route maps were read from Charm's own Drive "
  "copies (filed under the March and May reporting periods respectively) rather than the Certify-attached copies, which carry "
  "near-identical names; the distances they show reconcile exactly to the Certify datapoints. Two further images attached to "
  "these datapoints, Jun-18 and Jun-22-2026-distance-route_map.png, were downloaded from Certify and read: both show a single "
  "AECN-to-Opelousas road route of 2275.569 mi, which is not any of the three legs and is not used in any component here - see "
  "item 9.10. [log:routes.jun_route_maps] [log:routes.aecn_to_sopor_km] [log:routes.aecn_to_sopor_mi_converted] "
  "[log:routes.rail_sopor_to_opelousas_mi] [log:routes.opelousas_to_basco_mi_longest] "
  "[log:_derived_values.aecn_sopor_alloc_mi_total] [log:_derived_values.rail_alloc_mi_total] "
  "[log:_derived_values.opel_basco_alloc_mi_total] [log:_derived_values.aecn_sopor_full_mi] [log:routes]", "Transport Emissions Acctg v1.1"),
 ("3.6", "Transport mode matches oil type", "Pass",
  "Six transport components present, the full rail set: AECN to SOPOR Tanker Truck (process + embodied), SOPOR to Opelousas Rail "
  "(process + embodied), Opelousas to Basco Tanker Truck (process + embodied). Tanker truck for both road legs and railcar for "
  "the rail leg, which is correct for AECN moved by rail. [log:certify.components]", "Certify Datapoints"),
 ("3.7", "Billing documents present and consistent with BOL", "Flag",
  "Each BOL is a 5-page package and all five pages of all six were read for this review: the Straight Bill of Lading face, the "
  "AECN Shipping Details sheet, the Port-Cartier weighbridge transaction slip, the TSCA import certification signed by "
  "Marie-Michele Corbey, and the Charm purchase order. Product description, production period #06-2026 and carrier Transport "
  "Baie-Comeau agree across all pages of all six, and the weighbridge net on page 3 is the figure the Ops Notes uses on every "
  "BOL - the lower and authoritative of the two quantities each BOL prints. The flag is the purchase order. Its header field "
  "reads PO # Q42025, matching the Customer PO on all six BOL faces, but the line-item column beneath reads Q32025 on all six. "
  "On 2390-R that line item is struck through and hand-amended to Q42025; on 2389-R, 2391-R, 2392-R, 2393-R and 2394-R it is "
  "left as Q32025. So the order this oil was bought under is recorded two different ways inside the same document, and corrected "
  "on only one of six copies. It affects no quantity - the PO is a commercial document and every mass in this batch comes from "
  "the weighbridge and the scale tickets - but a verifier reconciling the paperwork will see it. Worth asking AECN to refresh "
  "the template. [log:bols.purchase_order_page5] [log:bols.tsca_page4] [log:bols.customer_po_all] "
  "[log:bols.production_period_all] [log:bols.page1_estimated_vs_weighbridge_note] [log:bols]", "VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing", "", "SECTION", "", ""),
 ("4.1", "CHN analysis PDF present in Testing subfolder", "Pass",
  "SGS North America Certificate of Analysis SR26-04370.001, SGS order 5470884, present in the Testing subfolder and attached to "
  "Certify against the Carbon Content datapoint. Signed by Rachel Oxley, Laboratory Supervisor. "
  "[log:lab_results.certificate_no] [log:lab_results.sgs_order_no] [log:lab_results.authorised_signatory]", "VR Appendix 1"),
 ("4.2", "Carbon content within the expected AECN range", "Pass",
  "Carbon 41.6 % (m/m) by ASTM D5291 Method C. Against the AECN reference population read this session from the MRV analysis "
  "workbook - mean 39.420350877193 %, standard deviation 6.09332409018271 %, n = 285 - the 2-sigma band is 27.2337 % to 51.607 %, "
  "so 41.6 sits comfortably inside at about 0.3577 standard deviations above the mean. Carbon and hydrogen carry the SGS '#' "
  "annotation, defined on the certificate itself as 'Result is outside of test method limits and/or analytical range used in "
  "method precision study' - a note that the ASTM D5291 precision study was built on petroleum matrices rather than bio-oil, not "
  "a rejection of the result. [log:lab_results.carbon_pct] [log:aecn_carbon_reference.carbon_mean_pct] "
  "[log:aecn_carbon_reference.carbon_sd_pct] [log:aecn_carbon_reference.carbon_n] "
  "[log:_derived_values.carbon_2sd_low_pct] [log:_derived_values.carbon_2sd_high_pct] [log:_derived_values.carbon_z_score] [log:aecn_carbon_reference]",
  "Biomass Feedstock Acctg v1.2"),
 ("4.3", "Hydrogen and nitrogen values reported and reasonable", "Pass",
  "Hydrogen 7.3 % (m/m), nitrogen <0.75 % (m/m), both ASTM D5291 Method C. Hydrogen sits about 0.76 standard deviations above the "
  "AECN reference mean of 6.87438596491228 % (SD 0.562848694875852 %). Nitrogen is reported below the detection limit, which is "
  "the normal result for this stream. Viscosity 39.66 cSt at 40 C and acid number 72 mg KOH/g are also reported. "
  "[log:lab_results.hydrogen_pct] [log:lab_results.nitrogen_pct] [log:aecn_carbon_reference.hydrogen_mean_pct] "
  "[log:aecn_carbon_reference.hydrogen_sd_pct] [log:lab_results.kinematic_viscosity_40C_cSt] "
  "[log:lab_results.acid_number_mgKOH_g]", "Biomass Feedstock Acctg v1.2"),
 ("4.4", "Lab report references the correct batch / sample ID", "Pass",
  "CLIENT ID on the certificate reads 'AECN 7-2026-W2', matching this batch and the Ops Notes Composite Sample ID. SAMPLED "
  "10-Jul-2026 07:00 at BASCO LOUISIANA, which is the injection date recorded for all five offloads. One composite sample per "
  "oil type per week is the validated weekly-batch practice. [log:lab_results.client_id] [log:lab_results.sampled] "
  "[log:lab_results.location] [log:ops_notes.summary_tab_aecn_row]", "VR Sec 5.1"),
 ("4.5", "pH / conductivity (aqueous phase)", "N/A",
  "AECN is not an aqueous-phase stream, so the aqueous-phase pH and conductivity test does not apply. The injectate pH that IS "
  "required for every batch is recorded and checked at item 5.5. [log:oil_type]", "UIC Permit / LDENR"),
 ("4.6", "Density above the formation fluid threshold for safe injection", "Pass",
  "Density at 15 C = 1.218 g/cm3 by ASTM D4052, comfortably above the 1.01 g/cm3 formation-fluid floor required for safe "
  "injection at Basco 6. [log:lab_results.density_15C_g_cm3] [log:lab_results.density_method] "
  "[log:_derived_values.density_floor_g_cm3]", "VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency", "", "SECTION", "", ""),
 ("5.1", "Correct batch ID and injection date", "Pass",
  "Summary tab: Batch ID 'INJ-07-2026-W2', Week Start (Sat) 2026-07-04, Week End (Sat) 2026-07-11. All five offload rows carry "
  "date 2026-07-10, inside the Certify period 05-11 Jul 2026. The week abuts sister batch W1, whose Certify period ends 04 Jul, "
  "so no day is claimed twice. [log:ops_notes.batch_id] [log:week_start_sat] [log:week_end_sat] "
  "[log:injection_date_all_offloads] [log:certify_period]", "VR Sec 5.1"),
 ("5.2", "All scale ticket values correctly transcribed", "Pass",
  "All ten ticket gross weights were read from the PDFs and compared cell by cell against the Ops Notes Full and Empty columns: "
  "72240 / 29220, 72920 / 29020, 72200 / 28940, 73040 / 29320, 71100 / 28740. Ten of ten transcribe exactly, with no substituted "
  "or adjusted value anywhere in the column. [log:scale_tickets.pairs] [log:ops_notes.offload_table]", "VR Sec 5.1"),
 ("5.3", "Oil and aqueous phase mass reconciliation", "N/A",
  "AECN-only entry - there is no aqueous phase to reconcile against. The week's QOWV aqueous volume is reported under its own "
  "GHG entry. [log:oil_type] [log:ops_notes.other_oil_types_in_week_not_in_this_removal]", "VR Sec 5.1"),
 ("5.4", "COBB values present and match", "Flag",
  "All five offloads are present in the 'Basco Injection -- COBB' tab at rows 379-383 and every value agrees with the Ops Notes: "
  "offloaded quantities 19513.52784 / 19912.6888 / 19622.38992 / 19831.04224 / 19133.87904 kg (the closing figure carrying the "
  "post-adjustment mass), origin quantities 78330 and 78500 kg, BOL strings '2389-R, 2390-R, 2391-R' and '2392-R, 2393-R, "
  "2394-R', completion date 2026-07-10 and pH 3.1 on all five. The flag is the row label: COBB records injection_batch as "
  "'INJ-20260709_bio_oil' while the Ops Notes, the Certify source filename and the lab Client ID all use 'INJ-07-2026-W2'. The "
  "date embedded in that label (0709) is also a day earlier than the recorded injection date of 2026-07-10. A verifier tracing "
  "from Certify to COBB by batch ID finds nothing and has to re-search by railcar or BOL, as this review did. Values are correct; "
  "the label is not traceable. [log:cobb.batch_id_col_a] [log:cobb.row_id_at_qa] [log:cobb.rows] "
  "[log:cobb.batch_id_naming_note] [log:ops_notes.batch_id]", "VR Sec 5.1"),
 ("5.5", "pH measurement noted", "Pass",
  "pH 3.1 recorded on every one of the five offload rows and in the Section 4 rollup, inside the Ops Notes target band of 2.0 - "
  "4.0 held in the constants block. COBB independently carries injection_ph 3.1 on all five rows. "
  "[log:_derived_values.ph] [log:ops_notes.constants] [log:cobb.rows]", "VR Sec 5.1"),
 ("5.6", "Completion date present and matches COBB", "Pass",
  "Ops Notes offload date 2026-07-10 on all five rows; COBB injection_completion_date 2026-07-10 on all five rows. COBB "
  "order_line_completed_on is 2026-07-07 16:10:51 for the TIMX201060 offloads and 2026-07-08 19:04:42 for SHPX215079, both "
  "consistent with the scale ticket timestamps of 7-07 and 7-08. [log:injection_date_all_offloads] [log:cobb.rows]",
  "VR Sec 5.1"),
 ("5.7", "No erroneous density measurements", "N/A",
  "The density field in the Ops Notes Batch Composition block is expected to be blank for AECN and is blank. Density for this "
  "batch is carried on the SGS certificate and checked at item 4.6. [log:ops_notes.density_field_present]", "VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation", "", "SECTION", "", ""),
 ("6.1", "AECN process emissions LCA CI spreadsheet present", "Pass",
  "'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx' present on the Certify Sources tab and "
  "linked to the Carbon Intensity - AECN Pyrolysis Process Emissions datapoint. The vendor LCA covering Jul-Dec 2025 is the input "
  "to Charm's H1 2026 factor, which is the current derivation on the emission factor sheet. "
  "[log:certify.attachment_map] [log:certify.certify_sources_enumeration] [log:ef_live_source]", "VR Appendix 1"),
 ("6.2", "LCA with stack emissions file present", "Pass",
  "'BH 2025 LCA w Stack Emissions.xlsx' present on the Certify Sources tab, linked to the same pyrolysis process CI datapoint. "
  "The stack component it supports is quantified on the emission factor sheet as 0.00412683 MTCO2e per MT bio-oil. "
  "[log:certify.attachment_map] [log:ef_live_source.aecn_process_derivation] [log:ef_live_source]", "VR Appendix 1"),
 ("6.3", "Supporting GHG data file present for the AECN production period", "Pass",
  "'Supporting GHG data 31Dec2025 S.xlsx' present on the Certify Sources tab and linked to the pyrolysis process CI datapoint, "
  "alongside a fourth supporting image. The BOLs independently record AECN production period #06-2026 for the oil itself. "
  "[log:certify.attachment_map] [log:bols.production_period_all] [log:ef_live_source]", "VR Appendix 1"),
 ("6.4", "AECN pyrolysis process EF matches the current value", "Flag",
  "Certify's stored carbon intensity is 0.104 tCO2e/t. The emission factor sheet 2026 tab row 3 'Production Emissions for AECN "
  "Oil--H1 2026' gives baseline 0.1038 and Final Quantity 0.1040167408 MTCO2e/MT after the 0.002088061302 conservatism uplift, "
  "and that Final Quantity is the authoritative figure. The stored value is demonstrably the rounded one: 98.01353 t x 0.104 = "
  "10.19341 t, which is what Certify reports, whereas the sheet's final factor gives 10.19505 t. The rounding therefore "
  "understates pyrolysis process emissions by 0.00164 tCO2e - a non-conservative direction, but 0.0012 % of net CDR and far below "
  "materiality. Sister batch W1 stores the same 0.104, so this is a standing entry convention rather than a W2 keying slip; "
  "raised so the full-precision factor can be entered going forward. The rail fuel factor shows the same pattern - "
  "Certify 5.584 t is consistent with a truncated 0.00002591 rather than the sheet 0.000025910374 - but there the effect is "
  "0.000081 tCO2e, which disappears entirely at Certify three-decimal display and needs no action. "
  "[log:_derived_values.rail_ef_truncation_delta_t] [log:_derived_values.ef_aecn_process_certify_stored] "
  "[log:_derived_values.ef_aecn_process_sheet_final] [log:_derived_values.pyrolysis_process_recalc_t] "
  "[log:_derived_values.pyrolysis_process_at_sheet_final_ef_t] [log:_derived_values.pyrolysis_process_ef_rounding_delta_t] "
  "[log:ef_live_source.aecn_process_row3] [log:ef_live_source] [log:sister_batch_w1_context.w1_certify_pyrolysis_ci]", "Certify Datapoints"),
 ("6.5", "AECN pyrolysis embodied EF applied", "Pass",
  "Certify stores 0.02116 tCO2e/t, exactly the emission factor sheet 2026 tab row 4 Final Quantity of 0.02116 MTCO2e/MT (uplift "
  "0.0, so baseline and final coincide). Applied: 98.01353 t x 0.02116 = 2.07397 t against Certify's 2.074 t. Sourced to 'AECN "
  "Embodied Emissions Calc Sheet (1).pdf' on the Sources tab. [log:_derived_values.ef_aecn_embodied] "
  "[log:_derived_values.pyrolysis_embodied_recalc_t] [log:ef_live_source.aecn_embodied_row4] [log:ef_live_source] [log:certify.attachment_map]",
  "Certify Datapoints"),
 ("6.6", "Mass basis for pyrolysis EFs is pre-sparging bio-oil mass", "Pass",
  "Both pyrolysis components take 'Bio-Oil Mass - AECN via Rail' = 98013.52784 kg, which is the post-adjustment but pre-sparging, "
  "pre-filtration mass. That is correct: AECN incurred production emissions on the full quantity produced, not on the smaller "
  "quantity surviving Basco pre-treatment. The post-treatment figure of 96560.49248 kg is used only for sequestration. "
  "[log:_derived_values.mass_used_post_adj_kg] [log:_derived_values.mobi_total_kg] [log:certify.uncertainty_modals_read]",
  "Certify Components"),

 ("7. Gross-to-Net Calculation", "", "SECTION", "", ""),
 ("7.1", "Gross CO2e = injectate mass x carbon wt% x 3.667", "Pass",
  "Recomputed independently: 96.56049248 t x 0.416 x 3.667 = 147.30033 tCO2e against Certify's Injection sequestration of "
  "147.300 t. Carbon entered as a decimal (0.416, i.e. the certificate's 41.6 %), units consistent throughout. The Certify modal "
  "confirms the same blueprint, output = product_mass x carbon_content x co2e_of_carbon. "
  "[log:_derived_values.mobi_total_kg] [log:lab_results.carbon_pct] [log:_derived_values.gross_co2e_recalc_t] "
  "[log:certify.components]", "GHG Stmt Sec E"),
 ("7.2", "Process emissions correctly deducted from gross", "Pass",
  "Activities total 19.820 t, rebuilt from its parts: pyrolysis process 10.193 + pyrolysis embodied 2.074 + transport process "
  "7.269 + transport embodied 0.284 = 19.82 t, matching the Certify calculation view exactly. Nothing is missing and nothing is "
  "double counted. [log:_derived_values.activities_recalc_t] [log:_derived_values.transport_process_sum_t] "
  "[log:_derived_values.transport_embodied_sum_t] [log:certify.calculation_view]", "GHG Stmt Sec E"),
 ("7.3", "Uncertainty discount correctly applied", "Pass",
  "Discount of 811 kg present in the calculation view. Reconstructed by Option B variance propagation from the per-component "
  "inputs actually read in the modals - carbon at 0.4 % of the measured value and mass at 362.85 kg, propagated across the "
  "sequestration and the five mass-bearing emission components - giving 809.6 kg at one standard deviation. That agrees with the "
  "reported figure to within 1.4 kg, the residual being the rounding of the displayed component values used to rebuild it. The "
  "one-sigma treatment is consistent with the conservative percentile the Standard requires. "
  "[log:_derived_values.uncertainty_1sigma_reconstructed_kg] [log:_derived_values.uncertainty_discount_reported_kg] "
  "[log:_derived_values.mass_uncertainty_kg] [log:certify.uncertainty_modals_read]", "Isometric Standard v2.0 S3.7"),
 ("7.4", "Net removals consistent with the BCU Quant sheet and GHG Statement", "Fail",
  "PARTIALLY RESOLVED - Certify is corrected, the GHG Statement Results sheet is not, so the two now disagree. Certify was "
  "re-read this session and shows Net CO2e Removed 133.938 t with Adjustments 7.269 t. The July1-July31 Bio-Oil GHG Statement "
  "Results sheet was re-exported and read in the same session and its row for rmv_1KYWP4BF01S0R568 still shows Emissions "
  "Reductions 10.193 and Net Removal 136.8623238, with Net Removals for Reporting Period (MT) still 877.8863469. So the "
  "reporting-period total continues to carry the full 2.924 t overstatement even though the entry itself no longer does. This "
  "clears when the results are regenerated: the row should read 7.269 and 133.938, and the period total should fall to 874.962 "
  "MT. Separately, no BCU Quant sheet exists for this reporting period - a recursive search of the entire July 1 - July 31 RP "
  "folder for any file named BCU or Quant returned nothing, against a full listing of the folder saved as the artifact. When it "
  "is produced its transport process line for this entry must reconcile to 7.269 t. "
  "[log:ghg_statement_results] [log:certify.correction_applied] [log:_derived_values.ghg_stmt_net_t] "
  "[log:_derived_values.ghg_stmt_reductions_t] [log:_derived_values.ghg_stmt_rp_net_mt] "
  "[log:_derived_values.transport_process_sum_t] [log:_derived_values.net_calc_t] [log:bcu_quant_sheet]", "RP BCU Quant.xlsx"),

 ("7a. Per-Component Uncertainty Verification", "", "SECTION", "", ""),
 ("7a.1", "Layer 1 - completeness: every component has uncertainty on the correct datapoint", "Pass",
  "All ten component modals opened individually and their INPUTS sections read. Mass-of-load uncertainty is present on every "
  "component that carries a mass datapoint: Injection sequestration, both pyrolysis components, and the three transport PROCESS "
  "legs. The three transport EMBODIED components correctly have no mass datapoint at all - embodied emissions are quantified per "
  "mile, not per ton-mile - so no mass uncertainty is expected or missing there. Carbon content carries its own uncertainty on "
  "the sequestration component. Distance datapoints carry no uncertainty, which is correct where the longest published route is "
  "used. The BCU component is a constant and carries none, as expected. [log:certify.uncertainty_modals_read] "
  "[log:certify.component_count]", "MRV Uncertainty Cheat Sheet"),
 ("7a.2", "Layer 2 - correctness: reported +/- matches the expected value", "Pass",
  "Read from the modals, not inferred. Carbon content: 41.6 % +/- 0.1664, and 41.6 x 0.004 = 0.1664, so the 0.4 % rule is applied "
  "exactly. Mass: +/- 362.85 kg on all five mass-bearing components, and 5 x 72.57 = 362.85, one discrete weight per offload "
  "across the five offloads that make up this weekly entry. That is the correct weekly-aggregate form of the per-removal rule - "
  "the entry's mass is fixed by five outbound weighings, so five discrete weights propagate. "
  "[log:certify.uncertainty_modals_read] [log:_derived_values.mass_uncertainty_kg] [log:_derived_values.n_offloads] [log:_derived_values.carbon_uncertainty_abs] [log:_derived_values.carbon_uncertainty_rate] [log:_derived_values.per_weighing_uncertainty_kg]",
  "Isometric Standard v2.0 S3.7.3"),
 ("7a.3", "Layer 3 - discount presence and consistency", "Pass",
  "The aggregate discount of 811 kg is present in the Certify calculation view and carried identically as 0.811 in the GHG "
  "Statement Results sheet row for this entry. It reconstructs to 809.6 kg from the per-component inputs above, so the inputs and "
  "the output are mutually consistent. [log:_derived_values.uncertainty_discount_reported_kg] "
  "[log:_derived_values.uncertainty_1sigma_reconstructed_kg] [log:_derived_values.ghg_stmt_net_t]",
  "Isometric Standard v2.0 S3.7"),

 ("8. Data Integrity & Anomaly Check", "", "SECTION", "", ""),
 ("8.1", "No unexplained outliers in mass, carbon content or calculated values", "Pass",
  "Carbon 41.6 % sits 0.3577 standard deviations above the AECN population mean. The five offload nets span 19214.15712 to "
  "19912.6888 kg, a spread of under 700 kg on roughly 19.5 t loads, normal for tanker offloads. The only apparent anomaly is "
  "TIMX201060's 80.27808 kg overdraw against its BOL aggregate, which is accumulated scale variance across four weighings and is "
  "resolved by the closing-offload policy at item 2.5, not left unexplained. Every emission component reconstructs to its "
  "reported value. [log:_derived_values.carbon_z_score] [log:aecn_carbon_reference] [log:_derived_values.overdraw_TIMX201060_kg] "
  "[log:ops_notes.offload_table]", "GHG Stmt Sec C"),
 ("8.2", "Spills / losses documented and unrecovered mass deducted", "Pass",
  "No spill or loss event is recorded for this batch in the Ops Notes, which carries a Loss column on the railcar register and "
  "leaves it empty for SHPX215079 and negative for TIMX201060 (the overdraw, not a loss). No incident report appears in the batch "
  "folder, whose complete contents were enumerated this session. The one downward mass movement in the batch is the 80.27808 kg "
  "conservatism adjustment, which reduces the claim rather than representing lost product. "
  "[log:ops_notes.spills_or_losses_documented] [log:ops_notes] [log:ops_notes.railcars_received] "
  "[log:_derived_values.uncertainty_adjustment_total_kg]", "GHG Stmt Sec C"),
 ("8.3", "Cross-week carryover and railcar draw-down documented", "Pass",
  "Both cross-period risks checked. Double count: SHPX215079's offloads 2, 3 and 4 appear in COBB rows 388-390 under a different "
  "batch with completion date 2026-07-18, so this week claims only its offload_1 and no offload is claimed twice; TIMX201060's "
  "Previously Claimed field is 0 for both cars, so nothing carried in either. Uncertainty conservatism precondition: TIMX201060 "
  "was fully drawn this week in 4 offloads against 3 inbound BOLs, so offloads >= BOLs holds and the per-offload uncertainty "
  "framing is conservative for that car. SHPX215079 is only 1 of 4 offloads in, so its precondition falls to be confirmed at its "
  "closing batch; COBB already shows the remaining three offloads booked, which will make it 4 against 3. "
  "[log:cobb.cross_week_boundary_rows] [log:ops_notes.railcars_received] [log:_derived_values.n_bols_TIMX201060] "
  "[log:_derived_values.n_offloads_this_week_TIMX201060] [log:_derived_values.n_bols_SHPX215079] "
  "[log:_derived_values.n_offloads_this_week_SHPX215079]", "VR Sec 3.5"),

 ("9. Isometric Certify - Removal Component Mapping", "", "SECTION", "", ""),
 ("9.1", "SEQUESTRATIONS: gross injection sequestration matches internal gross", "Pass",
  "One sequestration component, 147.300 tCO2e, against an independent recomputation of 96.56049248 t x 0.416 x 3.667 = 147.30033 "
  "t. The modal inputs are Mass of Injectant 96560.49 kg and Carbon Content 41.6 %, both traced to the Ops Notes and the SGS "
  "certificate. [log:_derived_values.gross_co2e_recalc_t] [log:certify.components] [log:certify.uncertainty_modals_read]",
  "Certify Components"),
 ("9.2", "ACTIVITIES - Transport: process and embodied correct for each leg", "Pass",
  "All six components rebuilt from full-precision emission factors read off the sheet this session, never from Certify's rounded "
  "display. PROCESS legs, mass x distance x factor: AECN->SOPOR 98.01353 t x 107.49722 mi x 0.0001143 = 1.20429 t (Certify "
  "1.204); rail 98.01353 t x 2199 mi x 0.000025910374 = 5.58451 t (Certify 5.584); Opelousas->Basco 98.09381 t x 42.9 mi x "
  "0.0001143 = 0.481 t (Certify 0.481) - and note this leg correctly uses the downstream scale-ticket mass, being what the trucks "
  "actually carried, not the adjusted figure. EMBODIED legs, allocated distance x per-mile factor: AECN->SOPOR 402.84103 mi x "
  "0.0002375605888 = 0.0957 t (Certify 0.096); rail 2746.81371 mi x 0.00003113066508 = 0.08551 t (Certify 0.086); "
  "Opelousas->Basco 429 mi x 0.0002375605888 = 0.10191 t (Certify 0.102). Transport process sum 1.204 + 5.584 + 0.481 = 7.269 t; "
  "transport embodied sum 0.096 + 0.086 + 0.102 = 0.284 t; bio-oil transport total 7.269 + 0.284 = 7.553 t, matching the Certify "
  "subtotal. [log:_derived_values.aecn_sopor_truck_process_recalc_t] [log:_derived_values.rail_process_recalc_t] "
  "[log:_derived_values.opel_basco_truck_process_recalc_t] [log:_derived_values.aecn_sopor_truck_embodied_recalc_t] "
  "[log:_derived_values.rail_embodied_recalc_t] [log:_derived_values.opel_basco_truck_embodied_recalc_t] "
  "[log:_derived_values.transport_process_sum_t] [log:_derived_values.transport_embodied_sum_t] "
  "[log:_derived_values.transport_total_t] [log:ef_live_source]", "Certify Components"),
 ("9.3", "ACTIVITIES - Injection: LCS and sample transport emissions", "N/A",
  "AECN requires no liquid caustic soda pre-treatment - that belongs to the aqueous stream - and no LCS component appears on this "
  "entry. Sample transport is carried on the emission factor sheet as 'N/A Immaterial' per MT injection batch and is likewise "
  "absent. Neither omission is an error for an AECN rail entry. [log:certify.components] [log:oil_type]", "Certify Components"),
 ("9.4", "ACTIVITIES - Pyrolysis: AECN production process and embodied entries present", "Pass",
  "Both present under the rail naming convention that signals scale tickets as the authoritative mass source: 'AECN pyrolysis "
  "(from rail loads) - process emissions' 10.193 t and '... - embodied emissions' 2.074 t, together 12.267 t. Rebuilt: 98.01353 t "
  "x 0.104 = 10.19341 t and 98.01353 t x 0.02116 = 2.07397 t. [log:_derived_values.pyrolysis_process_recalc_t] "
  "[log:_derived_values.pyrolysis_embodied_recalc_t] [log:certify.component_subtotals]", "Certify Components"),
 ("9.5", "REDUCTIONS: all applicable BCU categories populated", "Pass",
  "One reduction category applies to an AECN rail entry carrying no site-emission burden, and it is present: 'BCU - Transport "
  "Process' under Stored > Bio-oil transport. It is backed by a real retired instrument - the TERC Certificate of Retirement "
  "opened and read this session, 2795 Renewable Diesel TERCs retired on 18 Dec 2025 by Amazon.com Services LLC on behalf of Charm "
  "Industrial, verified by Turner, Mason & Company, each TERC representing one tonne of CO2e reduced - so the certificate has "
  "ample headroom for this entry's draw. The other four BCU categories relate to injection and pre-treatment diesel and waste and "
  "arise only on entries burdened with site emissions, which this one is not. The QUANTITY drawn is assessed at 9.6. "
  "[log:bcu_certificate.tercs_retired] [log:bcu_certificate.certificate_number] [log:bcu_certificate.date_of_retirement] "
  "[log:certify.components]", "Certify Components"),
 ("9.6", "REDUCTIONS: BCU quantity vs the corresponding activity emission", "Pass",
  "RESOLVED 2026-08-06. Originally raised as a Fail: the BCU was entered as a Constant CO2 reduction of 10,193 kgCO2e, which is "
  "exactly the AECN pyrolysis process emission on this same entry, against a transport process total of 1.204 + 5.584 + 0.481 = "
  "7.269 t - an excess of 2.924 t. The protocol caps it two ways: Transportation Emissions Accounting v1.1 section 4.2.1 states "
  "that 'When applying Equation 4, at maximum, an amount of BCUs may be used for each journey, j, such that: (F_j - F_BCU,j x "
  "ED_BCU,j / ED_Fuel,Transportation,j) >= 0', and section 4.1 EC1 requires that 'BCUs must be purchased and retired by the "
  "Project Proponent in a volume equivalent to the volume of fuel substitution claimed'. The datapoint has since been corrected "
  "to 7,269 kgCO2e. Re-read in Certify this session: the Components tab now shows 'BCU - Transport Process | Adjustments | GHG "
  "Entry | 5.43% | 7.269 tCO2e', which equals the transport process sum exactly. Pyrolysis process is unchanged at 10.193 t, "
  "correctly, since that is a real emission. [log:certify.correction_applied] [log:certify.components] "
  "[log:_derived_values.bcu_constant_t] [log:_derived_values.transport_process_sum_t] "
  "[log:_derived_values.bcu_surplus_over_transport_process_t] [log:_derived_values.bcu_after_correction_kg] "
  "[log:protocol.equation5_cap_quote] [log:protocol.ec1_quote] [log:certify]", "Transport Emissions Acctg v1.1 S4"),
 ("9.7", "COUNTERFACTUALS: zero per protocol", "Pass",
  "No counterfactual component appears on the entry and the calculation view shows no counterfactual term - net is built from "
  "sequestrations plus adjustments minus activities minus the uncertainty discount. Zero is correct for bio-oil geological "
  "storage. Losses are likewise absent. [log:certify.counterfactuals] [log:certify.losses] [log:certify.calculation_view]",
  "Certify Components"),
 ("9.8", "Net removal matches the internal calculation", "Pass",
  "RESOLVED 2026-08-06. Certify's calculation view now reads Net CO2e Removed 133.938 t from Sequestrations 147.300 + "
  "Adjustments 7.269 - Activities 19.820 - Uncertainty Discount 0.811, reproduced independently as 147.300 + 7.269 - 19.820 - "
  "0.811 = 133.938 t. That is the evidence-supported figure this review computed before the correction, reached exactly. The "
  "headline moved from 136.862 t to 133.938 t, a reduction of 2.924 t. Every other term was independently reproduced and is "
  "unchanged. [log:_derived_values.net_calc_t] [log:_derived_values.net_before_correction_t] "
  "[log:certify.calculation_view] [log:certify.correction_applied] [log:certify]", "Certify Calculation View"),
 ("9.9", "All datapoints have descriptive source names", "Flag",
  "31 of the 33 sources are descriptively named - scale tickets carry railcar, date, offload number and CAT ticket number; BOLs "
  "carry their number; the lab certificate carries the batch and SGS reference. Two do not. 'image (44).png' is the sole evidence "
  "for the 2199-mile rail leg, the largest single transport emission on the entry at 5.584 t; it is an undated screenshot of a "
  "Gmail thread whose body reads only 'The total milage for this move was 2199', with no subject line, no date and no railcar "
  "identifier, and it is relied on for two different railcars. 'Screenshot 2026-02-23 at 11.29.10 AM.png' supports the pyrolysis "
  "CI. Both are hygiene rather than substance - the underlying values are correct and independently corroborated - but a verifier "
  "cannot tie the rail email to these movements from the file itself. Suggest renaming to something like "
  "'Watco_rail_mileage_confirmation_SOPOR_to_Opelousas.png' and, where possible, re-capturing with the date and subject visible. "
  "[log:certify.generic_filenames_present] [log:routes.rail_evidence_filename_descriptive] "
  "[log:routes.rail_evidence_shows_date_or_railcar] [log:routes.rail_sopor_to_opelousas_mi]", "Certify Datapoints"),
 ("9.10", "All Certify sources match the files in the batch folder", "Flag",
  "33 sources enumerated from the Sources tab and each mapped to its linked datapoints. The mass and composition evidence is "
  "fully attached: Mass of Injectant, Bio-Oil Mass - AECN via Rail and the downstream scale-ticket mass each carry all 17 of the "
  "10 scale tickets, 6 BOLs and the Ops Notes, so the build-up from ticket net through adjustment, sparging and filtration to "
  "injectant is reproducible from attached evidence alone; carbon content carries the SGS certificate plus the Ops Notes; the "
  "pyrolysis carbon intensities carry the LCA set and the embodied calc sheet; each emission factor carries its sheet; the BCU "
  "carries the retirement certificate. The three distance datapoints do not reach that standard. 'Aggregate Distance AECN to "
  "Sopor Quebec (truck)' 402.84103 mi, 'Allocated Distance Sopor Quebec to Opelousas (rail)' 2746.81371 mi and 'Allocated "
  "Distance Opelousas to B6 (truck)' 429 mi each carry three files. Two of those three are Jun-18-2026-distance-route_map.png "
  "and Jun-22-2026-distance-route_map.png, both downloaded from their Certify signed URLs and read for this review. Each is a "
  "Mapbox route card reading Origin (A) 'AECN - Produits Forestiers Arbec S.E.N.C.', Destination (B) 'Opelousas, LA', Distance "
  "'3662.173 km / 2275.569 mi'. The two files differ by checksum but render identical values. Neither shows any of the three leg "
  "distances Charm actually uses, and neither contains offload mass shares - so neither supports the allocated figure it is "
  "attached to, none of which is derivable from 2275.569 mi. The third file on each datapoint is that leg's own route map, which "
  "gives the full leg only. The mass shares that turn a full leg into an allocated distance exist solely in the Ops Notes "
  "offload table, and the Ops Notes is not linked to any of the three. A verifier working from what is attached to these "
  "datapoints cannot reproduce the numbers. The Ops Notes is present in the entry, just not cross-linked here, so this is "
  "incomplete linkage rather than missing evidence; sister batch W1 in this same reporting period does carry the Ops Notes on "
  "its equivalent three datapoints. Two fixes: link INJ-07-2026-W2 Ops Notes.xlsx to the three distance datapoints, and review "
  "whether the two AECN-to-Opelousas road-route cards belong on them at all. Worth noting the road route is 73.82822 mi SHORTER "
  "than Charm's three-leg sum of 2349.39722 mi, so the leg-based treatment in use is the more conservative of the two. "
  "[log:certify.attachment_gate] [log:certify.attachment_map] [log:certify.certify_sources_tab_total] "
  "[log:routes.jun_route_maps] [log:_derived_values.jun_map_distance_mi] [log:_derived_values.jun_map_distance_km] "
  "[log:_derived_values.charm_three_leg_sum_mi] [log:_derived_values.charm_legs_minus_jun_map_mi] "
  "[log:_derived_values.aecn_sopor_alloc_mi_total] [log:_derived_values.rail_alloc_mi_total] "
  "[log:_derived_values.opel_basco_alloc_mi_total] [log:routes]", "Certify Sources"),
]


def build_workbook(rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "QA Checklist"
    ws.append(["Item", "Check", "Status", "Notes / Evidence", "Verifier Reference"])
    for c in ws[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    for r in rows:
        ws.append(list(r))
        i = ws.max_row
        status = r[2]
        for col in range(1, 6):
            cell = ws.cell(i, col)
            cell.alignment = WRAP; cell.border = BORDER
        if status == "SECTION":
            for col in range(1, 6):
                ws.cell(i, col).fill = HEADER_FILL; ws.cell(i, col).font = BOLD
        elif status == "Fail":
            for col in range(1, 6):
                ws.cell(i, col).fill = FAIL_FILL
        elif status == "Flag":
            for col in range(1, 6):
                ws.cell(i, col).fill = FLAG_FILL; ws.cell(i, col).font = FLAG_FONT
        elif status == "N/A":
            for col in range(1, 6):
                ws.cell(i, col).font = NA_FONT
    for cw, w in [("A", 10), ("B", 44), ("C", 9), ("D", 132), ("E", 30)]:
        ws.column_dimensions[cw].width = w
    ws.freeze_panes = "A2"

    # ---- Sheet 2: mass chain ----
    ws2 = wb.create_sheet("Mass Chain")
    ws2.append(["Offload", "Railcar", "Full (lb)", "Empty (lb)", "Tractor/Trailer", "Net (kg)",
                "Unc. Adj (kg)", "Post-adj (kg)", "Sparging (kg)", "Filtration (kg)", "MOBI (kg)", "COBB (kg)"])
    for c in ws2[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    SR = json.loads((HERE / "batch_INJ-07-2026-W2_source_reads.json").read_text())
    cobb = {r["consumed_lot"]: r["offloaded_quantity_kg"] for r in SR["cobb"]["rows"]}
    tix = {p["offload"]: p for p in SR["scale_tickets"]["pairs"]}
    for o in SR["ops_notes"]["offload_table"]:
        t = tix[o["id"]]
        post = o["net_scaled_kg"] - o["uncertainty_adjustment_kg"]
        ws2.append([o["id"].replace("Rail_", ""), o["railcar"], t["full_ticket"]["gross_weight_lb"],
                    t["empty_ticket"]["gross_weight_lb"],
                    f"{t['full_ticket']['tractor']}/{t['full_ticket']['trailer']}",
                    round(o["net_scaled_kg"], 5), o["uncertainty_adjustment_kg"], round(post, 5),
                    round(o["sparging_loss_kg"], 5), round(o["filtration_loss_kg"], 5),
                    round(o["mobi_kg"], 5), cobb[o["id"]]])
        i = ws2.max_row
        for col in range(1, 13):
            ws2.cell(i, col).border = BORDER
    ws2.append(["TOTAL", "", "", "", "", D["downstream_scale_ticket_sum_kg"], D["uncertainty_adjustment_total_kg"],
                D["mass_used_post_adj_kg"], D["sparging_loss_total_kg"], D["filtration_loss_total_kg"],
                D["mobi_total_kg"], D["downstream_scale_ticket_sum_kg"]])
    for c in ws2[ws2.max_row]:
        c.font = BOLD; c.border = BORDER
    ws2.append([])
    ws2.append(["Railcar", "BOL aggregate (kg)", "Raw offload sum (kg)", "Overdraw (kg)",
                "Adjustment applied (kg)", "Claimed (kg)", "Offloads this week", "Inbound BOLs"])
    for c in ws2[ws2.max_row]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    for rc in ("SHPX215079", "TIMX201060"):
        r = [x for x in SR["ops_notes"]["railcars_received"] if x["railcar"] == rc][0]
        ws2.append([rc, D[f"bol_aggregate_{rc}_kg"], D[f"raw_offload_sum_{rc}_kg"],
                    D.get(f"overdraw_{rc}_kg", "n/a - partial draw"),
                    D[f"uncertainty_adjustment_{rc}_kg"], r["claimed_this_week_kg"],
                    D[f"n_offloads_this_week_{rc}"], D[f"n_bols_{rc}"]])
        for c in ws2[ws2.max_row]:
            c.border = BORDER
    for cw, w in [("A", 34), ("B", 14), ("C", 12), ("D", 12), ("E", 18), ("F", 14), ("G", 14),
                  ("H", 14), ("I", 15), ("J", 15), ("K", 15), ("L", 15)]:
        ws2.column_dimensions[cw].width = w

    # ---- Sheet 3: Certify reconciliation ----
    ws3 = wb.create_sheet("Certify Recon")
    ws3.append(["Component / datapoint", "Reconstructed from source (show the work)", "Certify", "Match"])
    for c in ws3[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    MATRIX = [
     ("BOL aggregate SHPX215079", "25,940 + 26,200 + 26,190 (weighbridge Masse nette)", "78,330 kg", "ties"),
     ("BOL aggregate TIMX201060", "26,150 + 26,190 + 26,160 (weighbridge Masse nette)", "78,500 kg", "ties"),
     ("Bio-Oil Mass (downstream, scale tickets)", f"sum of 5 ticket nets = {D['downstream_scale_ticket_sum_kg']} kg", "98.094 t", "ties"),
     ("Closing-offload adjustment", f"{D['raw_offload_sum_TIMX201060_kg']} raw - 78,500 BOL = {D['overdraw_TIMX201060_kg']} kg absorbed on TIMX201060 offload_4", "80.27808 kg", "policy applied correctly"),
     ("Bio-Oil Mass - AECN via Rail", f"{D['downstream_scale_ticket_sum_kg']} - {D['uncertainty_adjustment_total_kg']} = {D['mass_used_post_adj_kg']} kg", "98.014 t", "ties"),
     ("Mass of Injectant", f"{D['mass_used_post_adj_kg']} - {D['sparging_loss_total_kg']} sparging - {D['filtration_loss_total_kg']} filtration = {D['mobi_total_kg']} kg", "96.560 t", "ties"),
     ("Carbon Content", "SGS SR26-04370.001 carbon 41.6 % (m/m)", "41.60 %", "ties"),
     ("Injection sequestration", f"96.56049248 x 0.416 x 3.667 = {D['gross_co2e_recalc_t']} t", "147.300 t", "ties"),
     ("Pyrolysis process", f"98.01353 x 0.104 = {D['pyrolysis_process_recalc_t']} t (sheet final factor 0.1040167408 would give {D['pyrolysis_process_at_sheet_final_ef_t']} t)", "10.193 t", "ties (factor rounded, see 6.4)"),
     ("Pyrolysis embodied", f"98.01353 x 0.02116 = {D['pyrolysis_embodied_recalc_t']} t", "2.074 t", "ties"),
     ("AECN->SOPOR truck PROCESS", f"98.01353 t x 107.49722 mi x 0.0001143 = {D['aecn_sopor_truck_process_recalc_t']} t", "1.204 t", "ties"),
     ("SOPOR->Opelousas rail PROCESS", f"98.01353 t x 2199 mi x 0.000025910374 = {D['rail_process_recalc_t']} t", "5.584 t", "ties"),
     ("Opelousas->Basco truck PROCESS", f"98.09381 t (downstream) x 42.9 mi x 0.0001143 = {D['opel_basco_truck_process_recalc_t']} t", "0.481 t", "ties"),
     ("AECN->SOPOR truck EMBODIED", f"{D['aecn_sopor_alloc_mi_total']} mi x 0.0002375605888 = {D['aecn_sopor_truck_embodied_recalc_t']} t", "0.096 t", "ties"),
     ("SOPOR->Opelousas rail EMBODIED", f"{D['rail_alloc_mi_total']} mi x 0.00003113066508 = {D['rail_embodied_recalc_t']} t", "0.086 t", "ties"),
     ("Opelousas->Basco truck EMBODIED", f"{D['opel_basco_alloc_mi_total']} mi x 0.0002375605888 = {D['opel_basco_truck_embodied_recalc_t']} t", "0.102 t", "ties"),
     ("Allocated distance AECN->SOPOR", f"107.49722 mi x 3 trucks x mass share, summed over 5 offloads = {D['aecn_sopor_alloc_mi_total']} mi", "402.84 mi", "ties"),
     ("Allocated distance rail", f"2199 mi x mass share per railcar, summed = {D['rail_alloc_mi_total']} mi", "2,746.81 mi", "ties"),
     ("Allocated distance Opelousas->Basco", f"42.9 x 2 round trip x 5 offloads = {D['opel_basco_alloc_mi_total']} mi", "429 mi", "ties (not mass-allocated)"),
     ("Transport process sum", f"1.204 + 5.584 + 0.481 = {D['transport_process_sum_t']} t", "-", "basis for BCU"),
     ("Transport embodied sum", f"0.096 + 0.086 + 0.102 = {D['transport_embodied_sum_t']} t", "-", "not BCU-eligible"),
     ("Bio-oil transport total", f"{D['transport_process_sum_t']} + {D['transport_embodied_sum_t']} = {D['transport_total_t']} t", "7.553 t", "ties"),
     ("BCU - Transport Process", f"should equal transport process sum {D['transport_process_sum_t']} t; entered as {D['bcu_constant_t']} t, which is exactly the pyrolysis process figure {D['pyrolysis_process_t_for_comparison']} t", f"exceeds by {D['bcu_surplus_over_transport_process_t']} t", "FAIL - see 9.6"),
     ("Activities total", f"pyrolysis 12.267 + transport {D['transport_total_t']} = {D['activities_recalc_t']} t", "19.820 t", "ties"),
     ("Uncertainty discount", f"carbon 0.4% + mass 5 x 72.57 = {D['mass_uncertainty_kg']} kg propagated = {D['uncertainty_1sigma_reconstructed_kg']} kg at 1 sigma", "811 kg", "ties within rounding"),
     ("Net CO2e removed (as reported)", f"147.300 + {D['bcu_constant_t']} - {D['activities_recalc_t']} - 0.811 = {D['net_calc_t']} t", "136.862 t", "arithmetic ties"),
     ("Net CO2e removed (evidence-supported)", f"147.300 + {D['transport_process_sum_t']} - {D['activities_recalc_t']} - 0.811 = {D['net_if_bcu_capped_at_transport_process_t']} t", f"overstated by {D['net_overstatement_from_bcu_t']} t", "FAIL - see 9.8"),
    ]
    for m in MATRIX:
        ws3.append(list(m)); r = ws3.max_row
        for col in range(1, 5):
            ws3.cell(r, col).alignment = WRAP; ws3.cell(r, col).border = BORDER
        if "FAIL" in str(m[-1]):
            for col in range(1, 5):
                ws3.cell(r, col).fill = FAIL_FILL
    for cw, w in [("A", 38), ("B", 86), ("C", 26), ("D", 30)]:
        ws3.column_dimensions[cw].width = w
    return wb


if __name__ == "__main__":
    build_with_validation(
        rows=ROWS,
        source_reads_path=HERE / "batch_INJ-07-2026-W2_source_reads.json",
        out_path=HERE / "Batch_INJ-07-2026-W2_QA_Checklist.xlsx",
        build_workbook_fn=build_workbook,
        derived_values=DERIVED,
    )
    from collections import Counter
    tally = Counter(r[2] for r in ROWS if r[2] != "SECTION")
    print("tally:", dict(tally))
