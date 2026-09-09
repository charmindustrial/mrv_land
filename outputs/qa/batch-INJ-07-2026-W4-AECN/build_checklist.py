#!/usr/bin/env python3
"""Build INJ-07-2026-W4 AECN weekly batch QA checklist (removal components only)."""
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

D = {
 # counts
 "n_offloads": 7, "n_railcars": 2, "n_bols_total": 6, "n_weighings": 14,
 "n_tickets_in_certify": 13, "certify_sources_total": 69, "certify_datapoints_total": 32,
 "certify_component_total": 20,
 # per-offload nets (lb -> kg)
 "o2_gprx_net_lb": 44820, "o2_gprx_net_kg": 20329.99344,
 "o3_gprx_net_lb": 45620, "o3_gprx_net_kg": 20692.86704,
 "o4_gprx_net_lb": 37860, "o4_gprx_net_kg": 17172.99312,
 "o1_tilx_net_lb": 44280, "o1_tilx_net_kg": 20085.05376,
 "o2_tilx_net_lb": 46200, "o2_tilx_net_kg": 20955.95040,
 "o3_tilx_net_lb": 46080, "o3_tilx_net_kg": 20901.51936,
 "o4_tilx_net_lb": 35800, "o4_tilx_net_kg": 16238.59360,
 "raw_offload_sum_kg": 136376.9707,
 "offload_net_lb": [44820, 45620, 37860, 44280, 46200, 46080, 35800],
 "offload_net_kg": [20329.99344, 20692.86704, 17172.99312, 20085.05376, 20955.95040, 20901.51936, 16238.59360],
 "gprx_o4_post_adj_kg": 17099.18064, "tilx_o4_post_adj_kg": 16037.47648,
 "mobi_t": 134.08435, "bio_oil_mass_t": 136.37697,
 # railcar balance
 "gprx_bol_aggregate_kg": 77690, "gprx_prior_claimed_kg": 19567.95888,
 "gprx_this_week_raw_kg": 58195.8536, "gprx_railcar_raw_total_kg": 77763.81248,
 "gprx_overdraw_kg": 73.81248, "gprx_post_adj_total_kg": 77690.0,
 "tilx_bol_aggregate_kg": 77980, "tilx_this_week_raw_kg": 78181.11712,
 "tilx_overdraw_kg": 201.11712, "tilx_post_adj_total_kg": 77980.0,
 "total_uncertainty_adj_kg": 274.9296, "mass_used_post_adj_kg": 136102.0411,
 # losses
 "sparging_rate": 0.0129, "filtration_rate": 0.00195,
 "sparging_total_kg": 1755.71633, "filtration_total_kg": 261.9753333,
 "mobi_kg": 134084.34946,
 # lab
 "carbon_pct": 39.4, "carbon_mean_pct": 39.420350877193, "carbon_sd_pct": 6.09332409018271,
 "carbon_n": 285, "carbon_2sd_low_pct": 27.2337, "carbon_2sd_high_pct": 51.6070,
 "hydrogen_pct": 7.1, "density_g_cm3": 1.211, "density_floor_g_cm3": 1.01,
 "acid_number": 66, "viscosity_cSt": 24.34,
 "ph": 2.9, "ph_target_low": 2.0, "ph_target_high": 4.0,
 # gross / emissions
 "gross_co2e_recalc_t": 193.72480, "gross_certify_t": 193.725,
 "bio_oil_mass_kg": 136376.97,
 "ef_aecn_process_certify": 0.104, "ef_aecn_process_sheet_final": 0.1040167408,
 "ef_aecn_process_baseline": 0.1038, "ef_aecn_process_uncertainty_factor": 0.002088061302,
 "ef_aecn_embodied": 0.02116,
 "pyrolysis_process_recalc_t": 14.18320, "pyrolysis_process_certify_t": 14.183,
 "pyrolysis_process_at_sheet_ef_t": 14.18549, "pyrolysis_ef_gap_kg": 2.283,
 "pyrolysis_embodied_recalc_t": 2.88574, "pyrolysis_embodied_certify_t": 2.886,
 "pyrolysis_subtotal_t": 17.069,
 # distances
 "aecn_sopor_km": 173, "aecn_sopor_full_mi": 107.49722, "rail_full_mi": 2199,
 "opel_basco_full_mi": 42.9, "opel_basco_alt_mi": 40.9,
 "allocated_truck_distance_mi_calc": 563.7711837, "allocated_rail_distance_mi_calc": 3844.1328153,
 "allocated_opel_basco_mi_calc": 600.6,
 "gprx_fraction_this_week": 0.7481277, "gprx_fraction_w3": 0.2518723, "tilx_fraction": 1.0,
 # EFs
 "ef_truck_fuel": 0.0001143, "ef_rail_fuel": 2.5910374e-05,
 "ef_truck_embodied": 0.0002375605888, "ef_railcar_embodied": 3.113066508e-05,
 # transport
 "aecn_sopor_truck_process_recalc_t": 1.67565, "aecn_sopor_truck_process_certify_t": 1.676,
 "rail_process_recalc_t": 7.77034, "rail_process_certify_t": 7.770,
 "opel_basco_truck_process_recalc_t": 0.66872, "opel_basco_truck_process_certify_t": 0.669,
 "aecn_sopor_truck_embodied_recalc_t": 0.13393, "aecn_sopor_truck_embodied_certify_t": 0.134,
 "rail_embodied_recalc_t": 0.11967, "rail_embodied_certify_t": 0.120,
 "opel_basco_truck_embodied_recalc_t": 0.14268, "opel_basco_truck_embodied_certify_t": 0.143,
 "transport_process_sum_t": 10.11471, "transport_process_certify_sum_t": 10.115,
 "transport_embodied_sum_t": 0.39628, "transport_embodied_certify_sum_t": 0.397, "transport_total_t": 10.51099,
 "transport_certify_subtotal_t": 10.512,
 # BCU
 "bcu_transport_t": 10.115, "tercs_retired": 2795,
 # uncertainty
 "unc_per_weighing_kg": 72.57, "unc_mass_total_kg": 507.99,
 "unc_carbon_pct_points": 0.1576, "unc_carbon_rate": 0.004,
 "unc_sequestration_term_t": 1.06731, "unc_rss_aecn_only_t": 1.06908,
 "unc_certify_t": 1.072, "unc_delta_t": 0.00292,
 # net
 "sequestrations_certify_t": 193.725, "adjustments_certify_t": 20.197,
 "activities_certify_t": 52.898, "net_calc_t": 159.952, "net_certify_t": 159.953,
 "aecn_activities_t": 27.581, "site_activities_t": 25.319,
 "ghg_statement_entry_t": 159.95, "ghg_statement_total_t": 874.53,
 "buffer_pct": 5.0, "buffer_credits": 43.728, "supplier_credits": 830.802,
 # ticket age
 "days_ticket_to_injection_max": 16, "days_ticket_to_injection_min": 3,
 "n_tickets_over_14_days": 4,
 # cobb
 "cobb_gprx_o3_kg": 20619.05456, "cobb_gprx_o4_kg": 17172.99312,
 "cobb_gprx_sum_this_week_kg": 58122.04112, "cobb_tilx_sum_kg": 77980.0,
 "cobb_adjustment_delta_kg": 73.81248,
}
DERIVED = D

HDR = ("Reviewer: Claude QA Agent  |  Date: 2026-08-06  |  Injection Site: Basco 6  |  Oil Type: AECN (rail)  |  "
       "Ops week: Sat 2026-07-18 to Sat 2026-07-25  |  Injected: 2026-07-25  |  "
       "Certify GHG entry rmv_1KZBJBN9C1S0M5R5 (period 19-25 Jul 2026)  |  Net CDR 159.953 tCO2e")

SUMMARY = (
 "TWO FAILS, both evidence-attachment gaps rather than quantity errors, and both fixable by uploading and linking a file. "
 "First, the full scale ticket for GPRX5102 offload_3 - the 74,940 lb weighing that produces 20,692.87 kg, 15.2 % of the "
 "week's mass - is not attached to Certify. Thirteen of the fourteen weighings are there; this one exists only as an unnamed "
 "phone photograph of the ticket sitting in the Drive offload folder. Second, the three mass-allocated and aggregated distance "
 "datapoints (563.77 truck-miles, 3,844.13 rail-miles, 600.6 offload-truck-miles) are each backed only by the underlying "
 "single-leg map or carrier email. The Ops Notes, which is the only document carrying the mass fractions, the times-three "
 "inbound-trip multiplier and the times-two round-trip factor, is attached to this entry but is linked to the four mass and "
 "carbon datapoints and to no distance datapoint, so none of the three allocated distances can be reproduced from the evidence "
 "as attached. "
 "EVERYTHING ELSE RECONCILES. The mass chain verifies end to end from the fourteen CAT Scale weighings through the Ops Notes "
 "and COBB into Certify, and every emission component, both allocated distances, the aggregate distance, every uncertainty "
 "input and the net arithmetic reconstruct to the reported figures from full-precision factors read off the 2026 emission "
 "factor sheet this session. All seven offloads carry a matching tractor AND trailer across their full/empty pair, so the "
 "reporting period's Trailer Standard Empty Weight substitution was not triggered and none was applied - consistent with the "
 "July VVB guidance, whose only application list covers Week 1. Both railcars closed out this week and both over-drew their "
 "inbound BOL aggregate, so the closing-offload back-calculation applied to each; after it, both railcars tie to their BOL "
 "aggregate to the kilogram. The cross-week boundary is clean: GPRX5102 offload_1 was claimed in Week 3 at 19,567.95888 kg and "
 "the Week 4 carry-forward figure equals it exactly, and TILX200231 appears in no earlier week. Four offloads out against three "
 "BOLs in on both railcars, so the per-offload uncertainty framing stays conservative. The BCU offset equals the transport "
 "process sum exactly. "
 "SIX FLAGS, none of which changes a quantity. The Ops Notes carries a cell annotation on the TILX200231 carry-forward cell "
 "asserting a prior claim that belongs to a different railcar. COBB books the GPRX5102 over-draw against offload_3 where the "
 "Ops Notes books it against the closing offload, with identical railcar totals either way, and labels the week "
 "INJ-20260719_bio_oil rather than INJ-07-2026-W4. The pyrolysis process factor is stored at 0.104 against the sheet's final "
 "quantity of 0.1040167408. Four of the fourteen weighings are 15 to 16 days before the injection date, a consequence of a "
 "railcar drawn down across two weeks. One BOL misprints its production period and two of the six BOL packages are filed short "
 "of their TSCA and purchase-order pages. And two source files carry generic names, one of them the sole evidence for the "
 "2,199-mile rail leg. "
 "SCOPE: removal components only. The site-emission components carried on this entry - B6 diesel, gasoline, waste disposal, "
 "electricity and RECs, methanol, spare parts, support travel and B6 embodied, together with the BCU - Diesel Site Emissions "
 "and BCU - Waste Disposal Transport adjustments, 25.319 t of activities and 10.082 t of adjustments - were not reviewed here."
 )

ROWS = [
 ("INJ-07-2026-W4 - AECN Weekly Batch QA", HDR, "SECTION", "", ""),
 ("Scope",
  "Time-block (weekly) batch = all AECN oil injected in the week, aggregated into ONE Certify GHG entry. AECN is all rail this "
  "week: 7 truck-out offloads from 2 railcars - GPRX5102 (offloads 2, 3 and 4, closing the railcar that Week 3 opened) and "
  "TILX200231 (all 4 offloads) - fed by 6 inbound BOLs. No WODO, Aqueous/QOWV or AECN-truck oil was injected this week; Kerry "
  "oil was injected in the same week but is a separate GHG entry and a separate QA. This review covers the removal components "
  "only; the site-emission components carried on this scapegoat entry are out of scope. "
  "[log:batch_id] [log:railcars] [log:offload_count] [log:ops_notes.other_oil_types_this_week] [log:qa_scope_note]",
  "SECTION", "", ""),
 ("SUMMARY OF FINDINGS", SUMMARY, "SECTION", "", ""),

 ("1. Batch Folder Completeness", "", "SECTION", "", ""),
 ("1.1", "Batch folder exists with correct naming", "Pass",
  "Drive folder id 1vaYJnDcSyNVILEV6FxEtbBB_4-IBiBrO, holding the Ops Notes plus four subfolders (June W4 Scale Tickets, Kerry "
  "Scale Tickets, Testing, Completed QA Checklists). The Ops Notes Summary tab cell B2 and the AECN Rail tab cell B2 both read "
  "'INJ-07-2026-W4', the Certify source file is named 'INJ-07-2026-W4 Ops Notes.xlsx', and the lab certificate Client ID is "
  "'07-2026-W4 AECN'. [log:ops_notes.batch_id_cell_B2] [log:drive_folder_url] [log:lab_results.client_id]", "VR Appendix 1"),
 ("1.2", "Scale Tickets subfolder present and populated", "Flag",
  "The 'June W4 Scale Tickets' subfolder holds one subfolder per offload, seven in all, matching the seven offloads. Six of the "
  "seven hold both a CAT-numbered Full ticket PDF and a CAT-numbered Empty ticket PDF; each also holds two phone photographs of "
  "the same tickets. The exception is Rail_GPRX5102_6.23.2026_offload_3, which holds the Empty ticket PDF and two photographs "
  "but no Full ticket PDF - the full weighing for that offload survives only as the unnamed photograph "
  "17837195237591692135944532212822.jpg. The photograph is legible and was read this session (CAT ticket 1312226191445, "
  "7-10-26 16:36, gross 74,940 lb, CH1/KL192), so the value is recoverable, but the folder is one named ticket short of the "
  "pattern the other six follow. See item 2.1 for the Certify-side consequence. Rail_TILX200231_6.25.2026_offload_1 holds the "
  "same Full ticket twice under two names (..._CAT1312226202574.pdf and ..._CATticket1312226202574.pdf). "
  "[log:scale_tickets.missing_from_certify] [log:scale_tickets.pairs] [log:offload_count]", "VR Appendix 1"),
 ("1.3", "Testing subfolder present with required lab results", "Pass",
  "Testing subfolder holds one file, 'CHARM INDUSTRIAL - 07-2026-W4 AECN + Kerry (SR26-04592.001-002).pdf', opened and read "
  "this session. It is a two-certificate document: page 1 is SR26-04592.001, Client ID '07-2026-W4 AECN'; page 2 is "
  "SR26-04592.002, Client ID '07-2026-W4 Kerry'. One AECN certificate is the correct count for this entry under the weekly "
  "composite-sample method. [log:lab_results.certificate_no] [log:lab_results.kerry_companion]", "VR Appendix 1"),
 ("1.4", "Ops Notes spreadsheet present and complete", "Pass",
  "'INJ-07-2026-W4 Ops Notes' (Google Sheet, modified 2026-08-04) present in the batch folder AND attached to the Certify entry "
  "as 'INJ-07-2026-W4 Ops Notes.xlsx', linked to four datapoints (Mass of load, Bio-Oil Mass - AECN via Rail, Mass of Injectant "
  "and Carbon Content). Eight tabs. The AECN Rail tab carries the batch header, a 2-row railcar register, a 6-row BOL origins "
  "ledger, the 7-row offload table, the EE totals row and the Section 4 rollup, all populated. Loaded both with and without "
  "value-resolution so cell annotations were read as well as cell values; the workbook carries two comments, on AECN Rail H10 "
  "and H11. [log:ops_notes.tabs] [log:ops_notes.cell_comments] [log:certify.attachment_map]", "VR Appendix 1"),
 ("1.5", "Injection site confirmed as Basco 6 - no Vaulted references", "Pass",
  "Injection site is unambiguously Basco 6. The SGS certificate records LOCATION 'BASCO LOUISIANA'; the offload route map runs "
  "to 4687 LA-115, St Landry LA 71367; Certify names three components 'Opelousas to Basco'; the fourteen weighings were taken "
  "at CAT Scale 3122 (Pilot Travel Center, I-49 Exit 40, Bunkie LA) and CAT Scale 1244 (The Quarters TS, I-49 Exit 23, "
  "Opelousas LA). A term-by-term scan of every machine-readable source opened this session - 605 non-empty Ops Notes cells "
  "across all eight tabs, both cell comments, and the Certify components, calculation view, datapoints, sources and GHG "
  "statement dumps plus the July VVB guidance text, 72,758 characters in all - is saved as the artifact for this check. It "
  "returned zero hits for Vaulted, Hutchinson, Kansas, salt cavern, KDHE, Class III, Advantek and Maize, against 105 hits for "
  "Basco, 27 for SOPOR, 25 for Opelousas and 13 for Louisiana. One Kansas address does appear, in the image-based evidence "
  "rather than the machine-readable set: the standing Charm purchase order bound as page 5 of the four complete BOL packages, "
  "all four read this session, carries Ship To 'Charm Industrial, 838 SW Purity Springs Road, El Dorado, KS 67042'. That is a "
  "procurement address on a blanket order dated 10/2/2025, not an injection or storage site, and it is not Vaulted Deep. "
  "[log:ops_notes.site_reference_scan] [log:lab_results.location] [log:bols.kansas_address_note]", "VR Appendix 1"),

 ("2. Scale Tickets & Mass Determination", "", "SECTION", "", ""),
 ("2.1", "Empty and full scale ticket images present for each offload", "Fail",
  "Fourteen weighings are required for seven offloads and fourteen exist, but only thirteen are attached to Certify. The "
  "Certify Sources tab carries 13 ticket PDFs; Rail_GPRX5102_6.23.2026_offload_3 has its Empty ticket "
  "(CAT 1312226192454, 29,320 lb) but no Full ticket. The missing full weighing is CAT ticket 1312226191445, 7-10-26 16:36, "
  "gross 74,940 lb (steer 10,420 + drive 32,360 + trailer 32,160 = 74,940), CHARM, tractor CH1, trailer KL192, weigh number "
  "1444, reweigh of ticket 1312226191444. It exists in Drive only as the unnamed photograph "
  "17837195237591692135944532212822.jpg, which was opened and read this session. That weighing determines offload_3's net of "
  "45,620 lb = 20,692.87 kg, which is 15.2 % of the week's claimed mass, and it feeds Mass of Injectant, Bio-Oil Mass and Mass "
  "of load. As attached, a verifier cannot reproduce that offload's net from Certify evidence. Remedy: export the ticket to "
  "PDF, name it to the convention used by the other thirteen, upload it and link it to the three mass datapoints. "
  "[log:scale_tickets.missing_from_certify] [log:scale_tickets.pairs] [log:certify.attachment_map] [log:_derived_values.offload_net_lb] [log:_derived_values.offload_net_kg]",
  "VR Sec 5.1"),
 ("2.2", "Ticket dates within 2 weeks of injection", "Flag",
  "All seven offloads are booked to the injection date 2026-07-25, the week-end date the weekly batch uses. The four "
  "TILX200231 offloads were weighed 21-22 July, three to four days before injection. The three GPRX5102 offloads were weighed "
  "9-11 July, because that railcar arrived at Opelousas on 23 June and was drawn down across Weeks 3 and 4. Four of the "
  "fourteen weighings therefore sit outside the two-week window this check applies: offload_2 full (7-09-26, 16 days), "
  "offload_2 empty (7-10-26, 15 days), offload_3 full (7-10-26, 15 days) and offload_4 full (7-10-26, 15 days). Two more sit "
  "exactly on the 14-day boundary. Every ticket is unambiguously tied to a named offload and railcar and the railcar balances "
  "to its BOL aggregate, so no mass is in doubt; the gap is a structural consequence of weekly batching over a railcar that "
  "spans two weeks, and the July VVB guidance publishes no method addressing ticket age (searched, zero hits for 'two week', "
  "'14 day' and 'dwell'). [log:scale_tickets.tickets_beyond_14_days_of_injection] [log:scale_tickets.ticket_age_note] "
  "[log:vvb_guidance.documented_search_for_w4_terms]", "VR Sec 3.5"),
 ("2.3", "Tractor and trailer numbers match between empty and full tickets", "Pass",
  "All seven pairs match on BOTH identifiers, so the reporting period's Trailer Standard Empty Weight substitution was not "
  "triggered on any offload and none was applied - every Empty Scale Ticket cell in the Ops Notes equals the gross printed on "
  "the filed empty ticket. GPRX5102 offload_2 CH2/KL188 = CH2/KL188; offload_3 CH1/KL192 = CH1/KL192 (the empty ticket's "
  "trailer glyph prints as RL192 where the full ticket prints KL192 - the same trailer, and KL192 is the trailer the July "
  "guidance tabulates); offload_4 CH2/KL188 = CH2/KL188. TILX200231 offload_1 CH2/KL188 = CH2/KL188; offload_2 CH1/KL192 = "
  "CH1/KL192; offload_3 CH2/KL188 = CH2/KL188; offload_4 CH1/KL192 = CH1/KL192. The three drop-trailer mismatch offloads named "
  "in the July guidance are all May lots and none of them is in this batch. On all fourteen tickets the three printed axle "
  "weights sum exactly to the printed GROSS WEIGHT. [log:scale_tickets.all_rig_identifiers_match] "
  "[log:scale_tickets.standard_tare_substitutions_applied] [log:scale_tickets.axle_sum_check] "
  "[log:vvb_guidance.drop_trailer_offloads_named]", "VR Sec 5.1"),
 ("2.4", "Net mass correctly calculated in Ops Notes", "Pass",
  "Each offload recomputed from the ticket grosses at 0.453592 kg/lb: GPRX5102 offload_2 73,500 - 28,680 = 44,820 lb -> "
  "20,329.99344 kg; offload_3 74,940 - 29,320 = 45,620 lb -> 20,692.86704 kg; offload_4 66,620 - 28,760 = 37,860 lb -> "
  "17,172.99312 kg; TILX200231 offload_1 72,920 - 28,640 = 44,280 lb -> 20,085.05376 kg; offload_2 75,380 - 29,180 = 46,200 lb "
  "-> 20,955.9504 kg; offload_3 74,720 - 28,640 = 46,080 lb -> 20,901.51936 kg; offload_4 64,700 - 28,900 = 35,800 lb -> "
  "16,238.5936 kg. All seven agree with the Ops Notes Net Scaled Mass cells to the fifth decimal. The seven sum to "
  "= 136376.9707 kg, which is the Section 4 rollup figure and the Certify Bio-Oil Mass. "
  "[log:_derived_values.raw_offload_sum_kg] [log:_derived_values.offload_net_lb] [log:_derived_values.offload_net_kg] [log:ops_notes.offload_table] [log:scale_tickets.pairs]", "VR Sec 5.1"),
 ("2.5", "Injectate mass uses the conservative value (railcar closing-offload rule)", "Pass",
  "Both railcars closed out this week and both over-drew, so the closing-offload back-calculation applied to each - the check "
  "that Failure Category 11 requires before any rail mass divergence is treated as an error. GPRX5102: three inbound BOLs "
  "2395-R + 2396-R + 2397-R = 25,600 + 26,050 + 26,040 = 77,690 kg; four offloads at raw scale-ticket values total "
  "19,567.95888 (claimed in Week 3) + 58,195.8536 (this week) = 77,763.81248 kg, an over-draw of = 73.81248 kg, and the Ops "
  "Notes books exactly that as the Uncertainty Adjustment on offload_4, the closing offload, giving a post-adjustment railcar "
  "total of 77,690.0 kg. TILX200231: 2399-R + 2400-R + 2401-R = 26,100 + 26,050 + 25,830 = 77,980 kg; four offloads total "
  "78,181.11712 kg, an over-draw of = 201.11712 kg, booked on offload_4, giving 77,980.0 kg. Both railcars therefore tie to "
  "their BOL aggregate to the kilogram, and the week's total adjustment = 274.9296 kg reconciles the raw 136,376.9707 kg to the "
  "Mass Used figure of 136,102.0411 kg. [log:_derived_values.gprx_overdraw_kg] [log:_derived_values.tilx_overdraw_kg] "
  "[log:_derived_values.total_uncertainty_adj_kg] [log:ops_notes.railcars_received] [log:bols.bols_into_railcar]",
  "GHG Stmt Sec C"),
 ("2.6", "Sparging and filtration deductions applied", "Pass",
  "Both deductions are applied per offload to the post-adjustment mass, sparging first and filtration on the sparged remainder, "
  "using the Ops Notes constants 0.0129 (Sparging Mass Loss) and 0.00195 (Filtration Solids Content). Worked on the closing "
  "offload of GPRX5102: post-adjustment 17,172.99312 - 73.81248 = 17,099.18064 kg; sparging 17,099.18064 x 0.0129 = 220.57943 "
  "kg; filtration (17,099.18064 - 220.57943) x 0.00195 = 32.91327 kg; MOBI 17,099.18064 - 220.57943 - 32.91327 = 16,845.68794 "
  "kg, matching the Ops Notes cell. All seven offloads recomputed the same way and all seven agree. Week totals: sparging "
  "= 1755.71633 kg, filtration = 261.9753333 kg. [log:_derived_values.sparging_total_kg] "
  "[log:_derived_values.filtration_total_kg] [log:_derived_values.gprx_o4_post_adj_kg] [log:ops_notes.constants] [log:ops_notes.offload_table]", "GHG Stmt Sec C"),
 ("2.7", "Mass values consistent across tickets, Ops Notes, COBB and Certify", "Pass",
  "The chain closes: 14 ticket grosses -> 7 offload nets summing to 136,376.9707 kg -> less 274.9296 kg of closing-offload "
  "adjustment -> 136,102.0411 kg Mass Used -> less 1,755.71633 kg sparging and 261.9753333 kg filtration -> MOBI = 134084.34946 "
  "kg, which is the Certify Mass of Injectant to five decimals. Certify's Bio-Oil Mass - AECN via Rail and Mass of load both "
  "read 136,376.97 kg, the pre-deduction figure, which is the correct basis for pyrolysis and transport. COBB's seven rows sum "
  "to the same railcar totals; the one row-level difference in where the GPRX5102 adjustment is booked is at item 5.4 and "
  "changes no total. [log:_derived_values.mobi_kg] [log:certify.components_in_scope] [log:cobb.cobb_vs_bol_balance]",
  "VR Sec 5.1"),

 ("3. Bills of Lading & Transportation", "", "SECTION", "", ""),
 ("3.1", "Truck BOL(s) present for each shipment", "Pass",
  "Six inbound BOLs, three per railcar, all six present on the Certify Sources tab and all six opened and read this session "
  "from the reporting-period BOL folder: 2395-R, 2396-R and 2397-R into GPRX5102; 2399-R, 2400-R and 2401-R into TILX200231. "
  "Three BOLs per railcar is the expected AECN rail pattern. [log:bols.bols_into_railcar] [log:_derived_values.n_bols_total]",
  "VR Appendix 1"),
 ("3.2", "Rail delivery: BOL destination is the SOPOR railyard", "Pass",
  "All six BOL faces carry the same Ship To: 'CHARM Industrial Inc. /WATCO, Societe du port ferroviaire de Baie-Comeau, 18 "
  "Route Maritime, Baie-Comeau, Quebec, Canada G4Z 2L6' - the SOPOR railyard, not Basco. Origin on all six is BioEnergie AE "
  "Cote-Nord Canada, 175 Portage des Mousses, Port-Cartier. Carrier on all six is Transport Baie-Comeau, driver Santos Bolduc. "
  "[log:bols.destination_all] [log:bols.destination_is_sopor_not_basco] [log:bols.origin_all]", "VR Appendix 1"),
 ("3.3", "BOL mass matches or exceeds reported injectate mass", "Pass",
  "Applied at railcar level, which is the right level for a rail batch. GPRX5102's three BOLs total 77,690 kg against a "
  "post-adjustment railcar draw of 77,690.0 kg; TILX200231's three total 77,980 kg against 77,980.0 kg. Neither railcar is "
  "credited with more than was loaded into it. Each BOL's mass was taken from the page 2 Product Shipment Summary 'Qty shipped' "
  "line and independently confirmed against the page 3 Port-Cartier weighbridge Masse nette, which agree exactly on all six: "
  "2395-R 25,600; 2396-R 26,050; 2397-R 26,040; 2399-R 26,100; 2400-R 26,050; 2401-R 25,830 kg. Page 1's Quantity block prints "
  "a volumetric estimate instead (for example 2399-R shows 25,591 kg against the weighed 26,100 kg); the weighed figure is the "
  "one used. [log:bols.bols_into_railcar] [log:bols.page1_estimated_vs_weighbridge_note] "
  "[log:_derived_values.gprx_post_adj_total_kg] [log:_derived_values.tilx_post_adj_total_kg]", "VR Sec 3.5"),
 ("3.4", "Origin and destination correct across all three legs", "Pass",
  "Leg 1 AECN Port-Cartier to SOPOR Baie-Comeau is documented by the six BOL faces. Leg 2 SOPOR to Opelousas is documented by "
  "the Watco rail logistics email. Leg 3 Opelousas to Basco is documented by the Google Maps card from Acadiana Railway, 1224 "
  "Cortez St, Opelousas to 4687 LA-115, St Landry LA 71367, and by the CAT Scale 1244 weighings taken at Opelousas. All three "
  "legs are evidenced. [log:bols.destination_all] [log:routes] [log:scale_tickets.scales_used]", "PDD Sec A"),
 ("3.5", "Transportation distances consistent with the known AECN rail route", "Fail",
  "The distance VALUES are right and were reconstructed from primary sources this session. The AECN-to-SOPOR map reads 173 km "
  "via QC-138 O, which converts to 107.4972 mi and matches Certify's full-leg datapoint of 107.49722 mi. The Opelousas-to-Basco "
  "map offers three routes at 42.9, 42.9 and 40.9 mi and Certify uses the longest, = 42.9 mi. The rail leg is evidenced by a "
  "Watco email stating 'The total milage for this move was 2199', matching Certify's = 2199 mi. The three derived distances "
  "also reconstruct exactly: allocating each offload's post-adjustment mass against its railcar's BOL aggregate gives "
  "= 563.7711837 aggregate truck-miles (3 x 107.5 mi x the summed fractions), = 3844.1328153 allocated rail-miles (2,199 mi x "
  "the same fractions) and = 600.6 allocated offload-truck-miles (42.9 mi x 2 for the round trip x 7 offloads), against "
  "Certify's 563.77, 3,844.13278 and 600.6. "
  "THE FAILURE IS EVIDENTIARY. None of those three derived datapoints has the Ops Notes attached, and the Ops Notes is linked "
  "to no distance datapoint at all. Aggregate Distance AECN to Sopor Quebec carries one source, the 173 km map. Allocated "
  "Distance Sopor Quebec to Opelousas carries one source, the Watco email. Allocated Distance Opelousas to B6 carries three, of "
  "which only 'Opelousas Railyard to Basco.png' is on point - the other two, 'Jul-18-2026-distance-route_map.png' and "
  "'Jun-23-2026-distance-route_map.png', are Mapbox cards for the whole AECN-to-Opelousas corridor at 3,662.106 km / 2,275.527 "
  "mi and do not evidence a 42.9-mile truck leg. So a verifier holding only what is attached sees 173 km, 2,199 mi and 42.9 mi, "
  "and has no attached document from which to derive 563.77, 3,844.13 or 600.6. Remedy: link the Ops Notes to the three "
  "distance datapoints, and unlink or relabel the two corridor maps. "
  "[log:certify.attachment_gap_allocated_distances] [log:routes] [log:_derived_values.allocated_truck_distance_mi_calc] "
  "[log:_derived_values.allocated_rail_distance_mi_calc] [log:_derived_values.allocated_opel_basco_mi_calc]",
  "Transport Emissions Acctg v1.1"),
 ("3.6", "Transport mode matches oil type and delivery route", "Pass",
  "Six transport components, the full rail set, all present: AECN to SOPOR Tanker Truck process and embodied, SOPOR to "
  "Opelousas Rail process and embodied, Opelousas to Basco Tanker Truck process and embodied. Tanker truck on both road legs "
  "and railcar on the rail leg is correct for AECN via rail. "
  "[log:certify.components_in_scope] [log:_derived_values.transport_certify_subtotal_t]", "Certify Datapoints"),
 ("3.7", "Billing documents present and consistent with the BOLs", "Flag",
  "Two documentation defects on the BOL packages, neither touching a mass figure. First, 2396-R prints its production period as "
  "'#0X-2026' on the page 1 Prod.period field and again on the page 2 Run # field, where its two sister BOLs into the same "
  "railcar, loaded 22 and 23 June 2026, both print '#06-2026' - a single mis-keyed character. Second, the packages are filed to "
  "two different lengths: 2397-R, 2399-R, 2400-R and 2401-R are complete five-page documents carrying the TSCA import "
  "certification signed by Marie-Michele Corbey and the standing Charm purchase order, while 2395-R and 2396-R are filed as "
  "three-page documents with neither. All three mass-bearing pages are present on all six. The purchase order itself identifies "
  "the order two ways on one page, header PO # Q42025 (which is what all six BOL faces record) against line-item PO # Q32025. "
  "The same two BOLs were filed short in Week 3, so this is a property of these documents rather than a Week 4 divergence. "
  "[log:bols.prod_period_typo] [log:bols.package_completeness] [log:bols.purchase_order_page5] [log:bols.tsca_page4]",
  "VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing", "", "SECTION", "", ""),
 ("4.1", "CHN analysis certificate present", "Pass",
  "SGS Certificate of Analysis SR26-04592.001, SGS order 5482329, Client ID '07-2026-W4 AECN', location BASCO LOUISIANA, "
  "sampled 24-Jul-2026 10:00, received 31-Jul-2026 09:45, analysed 31-Jul-2026, signed by Jared Camardelle, Laboratory "
  "Supervisor. Present in the Drive Testing subfolder and on the Certify Sources tab as 'W4 Kerry-AECN SGS COA.pdf'. The sample "
  "date falls inside the 19-25 July week. [log:lab_results.certificate_no] [log:lab_results.sampled] "
  "[log:certify.attachment_map]", "VR Appendix 1"),
 ("4.2", "Carbon content within the expected AECN range", "Pass",
  "Certificate reports Carbon = 39.4 % (m/m) by ASTM D5291 Method C. Against the AECN population statistics read from "
  "MRV_AECN_Analysis.xlsx this session - mean 39.420350877193 %, standard deviation 6.09332409018271, n = 285 - the two-sigma "
  "band runs 27.2337 % to 51.6070 %. The reported value sits essentially on the mean, 0.02 percentage points below it. Certify "
  "carries 39.40 % and the Ops Notes Summary carries 0.394 as a decimal, both matching. "
  "[log:lab_results.carbon_pct] [log:carbon_range] [log:_derived_values.carbon_2sd_low_pct] "
  "[log:_derived_values.carbon_2sd_high_pct]", "Biomass Feedstock Acctg v1.2"),
 ("4.3", "Hydrogen and nitrogen reported and reasonable", "Pass",
  "Hydrogen = 7.1 % (m/m) and Nitrogen reported as <0.75 % (m/m), both by ASTM D5291 Method C, alongside Acid Number = 66 mg "
  "KOH/g by ASTM D664 Method A and Kinematic Viscosity at 40 C = 24.34 cSt by ASTM D445. The certificate's '#' footnote - "
  "result outside test method limits or the analytical range used in the method precision study - is printed against Carbon and "
  "Hydrogen, as it is on every AECN certificate in this series, and is a method-range annotation rather than a data-quality "
  "rejection. [log:lab_results.hydrogen_pct] [log:lab_results.nitrogen_pct] [log:lab_results.hash_footnote] [log:lab_results.acid_number_mgKOH_g] [log:lab_results.kinematic_viscosity_40C_cSt]",
  "Biomass Feedstock Acctg v1.2"),
 ("4.4", "Lab report references the correct batch/sample ID", "Pass",
  "Certificate Client ID reads '07-2026-W4 AECN', matching the Ops Notes Summary Composite Sample ID '07-2026-W4 AECN' and the "
  "Ops Notes lab link 'COA SR26-04592.001'. The companion certificate on page 2, SR26-04592.002, is Client ID '07-2026-W4 "
  "Kerry' and carries 52.8 % carbon; it belongs to the separate Kerry entry and its value is not used here. "
  "[log:lab_results.client_id] [log:ops_notes.summary_tab_aecn_row17] [log:lab_results.kerry_companion]", "VR Sec 5.1"),
 ("4.5", "pH / conductivity (aqueous phase)", "N/A",
  "AECN is not an aqueous-phase oil, so the aqueous-phase pH and conductivity check does not apply. The injectate pH that does "
  "apply to this batch is checked at item 5.5. [log:oil_type]", "UIC Permit / LDENR"),
 ("4.6", "Density above the formation fluid threshold", "Pass",
  "Density at 15 C = 1.211 g/cm3 by ASTM D4052, against the 1.01 g/cm3 formation-fluid floor for safe injection - denser by "
  "0.201 g/cm3. [log:lab_results.density_15C_g_cm3] [log:_derived_values.density_floor_g_cm3]", "VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency", "", "SECTION", "", ""),
 ("5.1", "Correct batch ID and injection date", "Pass",
  "AECN Rail tab B2 = 'INJ-07-2026-W4'; Week Start B3 = 2026-07-18 and Week End B4 = 2026-07-25, matching Certify's stated "
  "period of 19 Jul 2026 to 25 Jul 2026. All seven offload rows carry date 2026-07-25. "
  "[log:ops_notes.batch_id_cell_B2] [log:ops_notes.week_start_B3] [log:certify_period]", "VR Sec 5.1"),
 ("5.2", "Scale ticket values correctly transcribed", "Pass",
  "All fourteen ticket grosses were compared cell by cell against the Full Scale Ticket and Empty Scale Ticket columns of the "
  "seven offload rows. Every one matches, and no cell carries a substituted or annotated value. "
  "[log:ops_notes.offload_table] [log:scale_tickets.pairs] [log:scale_tickets.standard_tare_substitutions_applied]",
  "VR Sec 5.1"),
 ("5.3", "Oil and aqueous phase mass reconciliation", "N/A",
  "AECN-only entry with no aqueous phase, so there is no oil-to-aqueous reconciliation to perform. The week's Kerry oil is a "
  "separate GHG entry. [log:oil_type] [log:ops_notes.other_oil_types_this_week]", "GHG Stmt Sec C"),
 ("5.4", "COBB values present and matching", "Flag",
  "All seven offloads are in the 'Basco Injection -- COBB' tab at rows 391-397, located by reading column A on every row. Two "
  "labelling and placement issues, neither of which changes a total. First, column A reads 'INJ-20260719_bio_oil' rather than "
  "INJ-07-2026-W4, so a verifier tracing by the batch ID that appears everywhere else finds nothing - the same convention "
  "appeared in Week 3. Second, COBB books the GPRX5102 over-draw against a different row than the Ops Notes does: COBB carries "
  "offload_3 at 20,619.05456 kg and offload_4 at 17,172.99312 kg, while the Ops Notes carries offload_3 at its raw 20,692.86704 "
  "kg and applies the adjustment to offload_4. The difference between the two offload_3 figures is = 73.81248 kg, exactly the "
  "railcar over-draw, so the same deduction is made in both records, just on different rows - the Ops Notes places it on the "
  "closing offload, which is where the published policy puts it. Both records give the same railcar totals: COBB's three "
  "GPRX5102 rows sum to 58,122.04112 kg which with Week 3's offload_1 gives 77,690.0 kg, and its four TILX200231 rows sum to "
  "77,980.0 kg, each equal to that railcar's BOL aggregate. Certify follows the Ops Notes. Origin quantities (77,690 and "
  "77,980 kg) and BOL lists match on every row. [log:cobb.batch_id_col_a] [log:cobb.adjustment_row_divergence] "
  "[log:cobb.cobb_vs_bol_balance] [log:cobb.rows]", "VR Sec 5.1"),
 ("5.5", "pH measurement noted", "Pass",
  "pH = 2.9 recorded on all seven offload rows and carried to the Section 4 rollup, inside the Ops Notes target band of 2.0 to "
  "4.0 held in cell O6. [log:ops_notes.offload_table] [log:ops_notes.constants] [log:_derived_values.ph]", "VR Sec 5.1"),
 ("5.6", "Completion date present and matching COBB", "Pass",
  "Ops Notes offload date 2026-07-25 = COBB injection completion date 2026-07-25 on all seven rows = the closing date of "
  "Certify's 19-25 Jul 2026 period and of the GHG statement line for this entry. "
  "[log:ops_notes.offload_table] [log:cobb.rows] [log:certify_period]", "VR Sec 5.1"),
 ("5.7", "No erroneous density measurements", "N/A",
  "The weekly AECN Rail tab has no density column - density is not collected per offload for AECN - so there is no density "
  "figure in the Ops Notes to be wrong. The certificate density is checked at item 4.6. "
  "[log:ops_notes.density_field_aecn]", "VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation", "", "SECTION", "", ""),
 ("6.1", "AECN process emissions LCA CI spreadsheet present", "Pass",
  "'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx' is on the Certify Sources tab and linked "
  "to the Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) datapoint, which carries four sources in total. The "
  "same file backs the sister July entries. [log:certify.attachment_map] [log:certify.certify_sources_tab_enumeration]",
  "VR Appendix 1"),
 ("6.2", "LCA with stack emissions file present", "Pass",
  "'BH 2025 LCA w Stack Emissions.xlsx' is on the Certify Sources tab, linked to the same pyrolysis process CI datapoint. "
  "[log:certify.attachment_map] [log:certify.certify_sources_tab_enumeration]", "VR Appendix 1"),
 ("6.3", "Supporting GHG data file present for the AECN production period", "Pass",
  "'Supporting GHG data 31Dec2025 S.xlsx' is on the Certify Sources tab, linked to the same pyrolysis process CI datapoint. "
  "[log:certify.attachment_map] [log:certify.certify_sources_tab_enumeration]", "VR Appendix 1"),
 ("6.4", "AECN pyrolysis process emission factor matches the current value", "Flag",
  "Certify stores the process carbon intensity as = 0.104 tCO2e/t. The 2026 emission factor sheet, read this session, gives row "
  "3 'Production Emissions for AECN Oil--H1 2026' a Baseline Quantity of 0.1038 MTCO2e/MT, an Uncertainty Factor of "
  "0.002088061302 and a Final Quantity of = 0.1040167408; the sheet's own derivation tab builds the baseline as 0.00412683 "
  "stack plus 0.0997 other process = 0.10382683. The stored value is confirmed to be 0.104 rather than the full-precision "
  "figure by the component result itself: 136.37697 t x 0.104 = 14.18320 t, which is what Certify reports, whereas "
  "136.37697 t x 0.1040167408 = 14.18549 t would report as 14.185. The rounding understates pyrolysis process emissions by "
  "= 2.283 kgCO2e, which is 0.0014 % of the 159.953 t net and immaterial, but it is a stored value that does not equal the "
  "sheet it cites. The same 0.104 was carried on the Week 3 entry. [log:emission_factors] [log:emission_factors.certify_vs_sheet] "
  "[log:emission_factors.rows] [log:_derived_values.pyrolysis_ef_gap_kg] "
  "[log:_derived_values.pyrolysis_process_at_sheet_ef_t]", "Certify Datapoints"),
 ("6.5", "AECN pyrolysis embodied emission factor applied", "Pass",
  "Certify stores = 0.02116 tCO2e/t, exactly the 2026 sheet's row 4 Final Quantity for Embodied Emissions for AECN Oil "
  "(baseline 0.02116, uncertainty factor 0.0). Applied: 136.37697 t x 0.02116 = 2.88574 t against Certify's 2.886 t. "
  "[log:emission_factors.rows] [log:_derived_values.pyrolysis_embodied_recalc_t] [log:certify.components_in_scope]",
  "Certify Datapoints"),
 ("6.6", "Mass basis for the pyrolysis factors is pre-sparging Origin Bio-Oil Mass", "Pass",
  "Both pyrolysis components take Bio-Oil Mass - AECN via Rail = 136376.97 kg, which is the raw sum of the seven offload nets "
  "before the closing-offload adjustment and before sparging and filtration - not the injectate mass of 134,084.34946 kg. That "
  "is the correct and conservative basis: the pyrolysis emissions were incurred producing the whole delivered quantity, and "
  "charging them against the larger mass while crediting the smaller one can only understate net removal. "
  "[log:certify.components_in_scope] [log:_derived_values.bio_oil_mass_kg] [log:_derived_values.mobi_kg]",
  "Certify Components"),

 ("7. Gross-to-Net Calculation", "", "SECTION", "", ""),
 ("7.1", "Gross CO2e = injectate mass x carbon wt% x 3.667", "Pass",
  "134,084.34946 kg / 1000 = 134.08435 t x 0.394 x 3.667 = 193.72480 tCO2e against Certify's = 193.725 t, a difference of 0.2 "
  "kg from display rounding. Carbon is applied as a decimal, and the mass used is the post-sparging, post-filtration injectate. "
  "Certify's own blueprint for the component reads output = product_mass * carbon_content * {co2e_of_carbon}, the same form. "
  "[log:_derived_values.gross_co2e_recalc_t] [log:_derived_values.mobi_kg] [log:_derived_values.mobi_t] [log:lab_results.carbon_pct] "
  "[log:certify.components_in_scope]", "GHG Stmt Sec E"),
 ("7.2", "Process emissions correctly deducted", "Pass",
  "All eight AECN emission components are present and each was recomputed from full-precision factors. Pyrolysis process "
  "14.183 t and embodied 2.886 t give the = 17.069 t Certify shows for the pyrolysis group. The six transport components give "
  "= 10.512 t. The two groups together are the = 27.581 t of AECN-scope activities inside Certify's 52.898 t total; the "
  "remaining 25.319 t is site emissions, out of scope for this review. "
  "[log:_derived_values.pyrolysis_subtotal_t] [log:_derived_values.transport_certify_subtotal_t] "
  "[log:_derived_values.aecn_activities_t] [log:_derived_values.site_activities_t] [log:certify.components_in_scope]",
  "GHG Stmt Sec E"),
 ("7.3", "Uncertainty discount correctly applied", "Pass",
  "A discount of = 1.072 t is present in the calculation view and is deducted in the net line. Charm reports per-datapoint "
  "uncertainties and Certify propagates them, so the inputs are the thing to verify and all of them are correct - see items "
  "7a.1 and 7a.2. Propagating the AECN inputs independently gives = 1.06908 t (sequestration term 1.06731 t from mass and "
  "carbon in quadrature, plus the five mass-bearing emission terms), which is 0.00292 t below what Certify deducts. Certify's "
  "figure is the larger of the two, so the entry is not under-discounted; the residual is attributable to the site-emission "
  "components on this same entry, whose uncertainty inputs were not reviewed here. "
  "[log:_derived_values.unc_rss_aecn_only_t] [log:_derived_values.unc_certify_t] "
  "[log:_derived_values.unc_sequestration_term_t] [log:certify.uncertainty_discount_t]", "Isometric Standard v2.0 S3.7"),
 ("7.4", "Net removals consistent with the GHG Statement", "Pass",
  "193.725 + 20.197 - 52.898 - 1.072 = 159.952 t against Certify's stated Net CO2e Removed of = 159.953 t, the 1 kg gap being "
  "the rounding of the four displayed components. GHG statement ggs_1KZBX6AX41S029JS (DRAFT, 01-31 Jul 2026) lists this entry "
  "as rmv_1KZBJBN9C1S0M5R5, = 159.95 tCO2e, sequestered date 19 Jul 2026 to 25 Jul 2026, credit type REMOVAL. The statement's "
  "nine entries total 874.53 t with a projected buffer allocation of 43.728 credits, = 5.0 % of the total, matching the Basco 6 "
  "low-risk buffer. [log:_derived_values.net_calc_t] [log:certify.net_co2e_removed_t] [log:ghg_statement.this_entry_line] "
  "[log:ghg_statement.buffer_pool_check]", "GHG Stmt Sec E"),

 ("7a. Per-Component Uncertainty Verification", "", "SECTION", "", ""),
 ("7a.1", "Layer 1 - completeness: every component carries uncertainty on the correct datapoint", "Pass",
  "Ten component modals were opened individually this session and their INPUTS sections read. Every mass-bearing component "
  "carries a mass uncertainty and the sequestration additionally carries a carbon uncertainty: Injection sequestration (Carbon "
  "Content and Mass of Injectant), AECN pyrolysis process and embodied (Bio-Oil Mass), AECN to SOPOR truck process (Bio-Oil "
  "Mass), SOPOR to Opelousas rail process (Bio-Oil Mass) and Opelousas to Basco truck process (Mass of load). The three "
  "embodied transport components carry no mass input at all, which is correct - embodied emissions are per-mile, so they have "
  "a distance input and no Mass of Load datapoint to attach an uncertainty to. Distance carries no uncertainty on any leg, per "
  "the convention of using the longest available route. [log:certify.components_in_scope] "
  "[log:_derived_values.n_offloads]", "MRV Uncertainty Cheat Sheet"),
 ("7a.2", "Layer 2 - correctness: reported values match expected", "Pass",
  "Mass uncertainty reads +/- 507.99 kg on every one of the six mass datapoints. Seven discrete outbound weighings at 72.57 kg "
  "each gives 7 x 72.57 = 507.99 kg exactly, and seven is the offload count - one outbound weighing fixes each offload's mass. "
  "Carbon uncertainty reads +/- 0.1576 percentage points, and 0.004 x 39.4 = 0.1576, the 0.4 % rate. The Ops Notes Summary "
  "carries the same two figures as 0.001576 and 0.004 in decimal form. Every value was read from the modal rather than inferred "
  "from the aggregate. [log:certify.components_in_scope] [log:_derived_values.unc_mass_total_kg] "
  "[log:_derived_values.unc_carbon_pct_points] [log:ops_notes.summary_tab_aecn_row17]", "Isometric Standard v2.0 S3.7.3"),
 ("7a.3", "Layer 3 - discount present and consistent", "Pass",
  "The aggregate discount of 1.072 t appears in the calculation view between Activities and Net and is deducted in the net "
  "line, and the resulting net matches the GHG statement entry. The independent propagation at item 7.3 lands 0.3 % below "
  "Certify's figure, on the conservative side. [log:certify.uncertainty_discount_t] [log:_derived_values.unc_rss_aecn_only_t] "
  "[log:ghg_statement.this_entry_line]", "GHG Stmt Sec E"),

 ("8. Data Integrity & Anomaly Check", "", "SECTION", "", ""),
 ("8.1", "No unexplained outliers or unreconciled annotations", "Flag",
  "The quantities carry no outliers: carbon sits on the AECN mean, pH is uniform at 2.9, the seven offload nets span 16,238 to "
  "20,956 kg which is the normal spread for a tanker load, and both railcar balances close to their BOL aggregate. One "
  "annotation does not reconcile. The AECN Rail tab carries two cell comments, on the two Previously Claimed cells. H10, on "
  "GPRX5102, reads 'Prior claimed 19,567.96 kg -- INJ-20260712_bio_oil offload_1, W3' and is correct - Week 3 recorded exactly "
  "19,567.95888 kg for that offload and the cell holds that value. H11, on TILX200231, reads 'Prior-RP claimed 19,513.53 kg - "
  "INJ-20260709_bio_oil offload_1, injected in W2 per COBB', but the cell it annotates holds 0.0. The 19,513.53 kg figure "
  "belongs to a different railcar. COBB row 379 carries the figure and the batch label the comment names - "
  "consumed lot Rail_SHPX215079_6.18.2026_offload_1, batch INJ-20260709_bio_oil, offloaded quantity 19,513.52784 kg, injection "
  "completion 2026-07-10 - so the annotation is verbatim correct for SHPX215079 and has simply been pasted onto the "
  "TILX200231 row. Scanning column C of all 3,000 COBB rows for TILX200231 shows the 6.25.2026 lot in exactly four rows, 394 "
  "to 397, all under this week's batch; the railcar number is reused on three earlier lots (1.22.26, 3.23.2026 and 5.11.2026) "
  "each fully claimed in its own week. So the 0.0 cell value is correct and no oil is double-counted. Left as it stands, a "
  "verifier reading the annotation would conclude the cell beneath it is understated by 19.5 tonnes. Remedy: delete or "
  "correct the comment. [log:ops_notes.cell_comments] [log:ops_notes.cell_comment_H11_contradiction] "
  "[log:ops_notes.cell_comment_H10_verified] [log:cobb.tilx200231_history_check] [log:cross_week_boundary]", "GHG Stmt Sec C"),
 ("8.2", "Spills, losses and irregularities documented and deducted", "Pass",
  "A term-by-term search of the whole Ops Notes workbook and the Certify dumps for spill, incident, leak, release, unrecovered "
  "and overflow returned zero hits on every term; the artifact is saved. The only loss entries anywhere in the workbook are the "
  "Section 1 railcar balance column - which holds the two over-draws, -73.81248 and -201.11712 kg, both absorbed by the "
  "closing-offload Uncertainty Adjustment - and the two process-loss columns for sparging and filtration, both of which reduce "
  "the credited mass. No unrecovered mass is being claimed. [log:ops_notes.spill_incident_scan] "
  "[log:ops_notes.site_reference_scan] [log:ops_notes.railcars_received]", "GHG Stmt Sec C"),
 ("8.3", "Cross-week carryover documented and not double-counted", "Pass",
  "GPRX5102 spans two weeks and the handover is clean. Week 3 claimed offload_1 at 19,567.95888 kg; the Week 4 Ops Notes "
  "carries exactly that figure in the Previously Claimed cell, claims offloads 2, 3 and 4 for = 58195.8536 kg, and the two "
  "together equal the railcar's raw draw of 77,763.81248 kg, which the closing-offload adjustment brings to the 77,690 kg BOL "
  "aggregate. COBB shows the same split, offload_1 under INJ-20260712_bio_oil at row 387 and offloads 2 to 4 under "
  "INJ-20260719_bio_oil at rows 391 to 393. TILX200231 is drawn entirely within this week. No offload number appears in two "
  "weeks. Both railcars discharged in four offloads against three inbound BOLs, so the per-offload mass-uncertainty framing "
  "checked at 7a.2 remains conservative, and because both railcars closed out this week that precondition is settled here "
  "rather than deferred. [log:cross_week_boundary] [log:conservatism_precondition] "
  "[log:_derived_values.gprx_this_week_raw_kg]", "VR Sec 3.5"),

 ("9. Isometric Certify - Removal Component Mapping", "", "SECTION", "", ""),
 ("9.1", "SEQUESTRATIONS: gross injection sequestration matches internal gross", "Pass",
  "One sequestration component, Injection sequestration, at = 193.725 tCO2e, reproduced at item 7.1 from the injectate mass and "
  "the certificate carbon content. It is the only entry in the CO2 stored group. "
  "[log:certify.components_in_scope] [log:_derived_values.gross_co2e_recalc_t]", "Certify Components"),
 ("9.2", "ACTIVITIES - Transport: process and embodied correct for the AECN rail route", "Pass",
  "All six components reconstructed from full-precision factors read off the 2026 sheet this session. Process legs are mass x "
  "full-leg distance x factor: AECN to SOPOR 136.37697 t x 107.49722 mi x 0.0001143 = 1.67565 t against Certify 1.676; SOPOR to "
  "Opelousas 136.37697 t x 2,199 mi x 0.000025910374 = 7.77034 t against 7.770; Opelousas to Basco 136.37697 t x 42.9 mi x "
  "0.0001143 = 0.66872 t against 0.669. Embodied legs are allocated distance x per-mile factor, with no mass term: AECN to "
  "SOPOR 563.7711837 mi x 0.0002375605888 = 0.13393 t against 0.134; rail 3,844.1328153 mi x 0.00003113066508 = 0.11967 t "
  "against 0.120; Opelousas to Basco 600.6 mi x 0.0002375605888 = 0.14268 t against 0.143. Transport process sum "
  "= 1.676 + 7.770 + 0.669 = 10.115 t; transport embodied sum 0.134 + 0.120 + 0.143 = 0.397 t; bio-oil transport total "
  "= 10.51099 t against Certify's group subtotal of 10.512 t. The railcar embodied factor is the current 2026 per-mile value, "
  "not the deprecated one. [log:_derived_values.transport_process_sum_t] [log:_derived_values.transport_embodied_sum_t] "
  "[log:_derived_values.transport_total_t] [log:_derived_values.transport_embodied_certify_sum_t] [log:_derived_values.aecn_sopor_truck_process_recalc_t] [log:_derived_values.rail_process_recalc_t] "
  "[log:_derived_values.opel_basco_truck_process_recalc_t] [log:_derived_values.aecn_sopor_truck_embodied_recalc_t] "
  "[log:_derived_values.rail_embodied_recalc_t] [log:_derived_values.opel_basco_truck_embodied_recalc_t] "
  "[log:_derived_values.bio_oil_mass_t] [log:emission_factors] [log:emission_factors.certify_vs_sheet] [log:certify.components_in_scope]",
  "Certify Components"),
 ("9.3", "ACTIVITIES - Injection: LCS and sample transport", "N/A",
  "AECN oil does not receive LCS pre-treatment - that is an Aqueous-phase step - and no LCS component appears on this entry. "
  "Sample transport is carried on the 2026 emission factor sheet as 'N/A Immaterial' and is not booked as a component. The "
  "injection-side components that do appear on this entry are site emissions, which are outside this review's scope. "
  "[log:certify.components_out_of_scope_site_emissions] [log:qa_scope_note]", "Certify Components"),
 ("9.4", "ACTIVITIES - Pyrolysis: AECN production process and embodied entries present", "Pass",
  "Both present under the rail naming convention that signals scale tickets as the authoritative mass source: 'AECN pyrolysis "
  "(from rail loads) - process emissions' at 14.183 t and '... - embodied emissions' at 2.886 t, summing to the = 17.069 t "
  "shown for the group. Recomputed at items 6.4 and 6.5. [log:certify.components_in_scope] "
  "[log:_derived_values.pyrolysis_subtotal_t]", "Certify Components"),
 ("9.5", "REDUCTIONS: applicable BCU categories populated", "Pass",
  "One transport-side BCU applies to this removal, BCU - Transport Process at 10.115 t, and it is present. Its source is the "
  "TERC Certificate of Retirement read this session: retired by Amazon.com Services LLC on behalf of Charm Industrial, Inc on "
  "Dec 18 2025, vintage 2024, commodity Renewable Diesel TERCS, = 2795 TERCs retired, verification body Turner, Mason & "
  "Company, certificate TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000, each TERC representing one tonne of CO2e reduced. "
  "The certificate is a pooled retirement drawn down across removals rather than an itemised per-batch allocation, and the same "
  "certificate backs the sister July entries. The other two BCU categories on this entry, for site diesel and waste disposal "
  "transport, belong to the site-emissions scope. [log:bcu_certificate] [log:_derived_values.tercs_retired] "
  "[log:certify.components_in_scope]", "Certify Components"),
 ("9.6", "REDUCTIONS: BCU quantity at least equals the corresponding activity emission", "Pass",
  "BCU - Transport Process = 10.115 t against a transport process sum of 1.676 (AECN to SOPOR truck) + 7.770 (SOPOR to "
  "Opelousas rail) + 0.669 (Opelousas to Basco truck) = 10.115 t - equal, so the transport process emissions are fully offset "
  "with nothing over-claimed. Transport embodied of 0.397 t is deliberately not offset, embodied emissions not being "
  "BCU-eligible. [log:_derived_values.bcu_transport_t] [log:_derived_values.transport_process_certify_sum_t] "
  "[log:_derived_values.transport_embodied_sum_t] [log:certify.components_in_scope]", "Certify Components"),
 ("9.7", "COUNTERFACTUALS: zero per protocol", "Pass",
  "The Components tab shows 20 components in two groups, Stored (4) and Emitted (16), and the calculation view runs "
  "Sequestrations plus Adjustments minus Activities minus Uncertainty Discount with no counterfactual and no loss term. Zero "
  "counterfactual is correct for bio-oil geological storage. [log:certify.counterfactuals_t] "
  "[log:certify.counterfactuals_note] [log:certify.component_count]", "Certify Components"),
 ("9.8", "Net removal matches the internal calculation", "Pass",
  "Certify Net CO2e Removed = 159.953 t; the independent line 193.725 + 20.197 - 52.898 - 1.072 gives 159.952 t, agreeing to "
  "the kilogram once display rounding is allowed for. [log:certify.net_co2e_removed_t] [log:_derived_values.net_calc_t]",
  "Certify Calculation View"),
 ("9.9", "Datapoints have descriptive source names", "Flag",
  "Sixty-nine sources, of which two carry names that tell a verifier nothing about their content. 'image (44).png' is the sole "
  "evidence for the 2,199-mile rail leg - it is a screenshot of the Watco email - and 'Screenshot 2026-02-23 at 11.29.10 AM.png' "
  "is one of the four sources on the pyrolysis process carbon intensity - opened this session, it is a Gmail message from "
  "Jean-Christophe Amado of Viridi Global to Max dated 17 Feb 2026 transmitting the Q3-Q4 2025 LCA data and explaining the CI "
  "reduction. Both files were opened this session and both contain what the datapoint needs; the naming is the issue. "
  "Renaming them to describe their content would also make the rail-distance evidence findable. "
  "[log:routes.generic_filenames] [log:routes] [log:certify.certify_sources_tab_enumeration] "
  "[log:_derived_values.certify_sources_total]", "Certify Datapoints"),
 ("9.10", "Certify sources match the files in the Drive batch folder", "Flag",
  "The two sets differ in both directions. In Drive but not Certify: the full weighing for GPRX5102 offload_3, filed only as "
  "the unnamed photograph 17837195237591692135944532212822.jpg - the substantive consequence is the Fail at item 2.1. Also in "
  "Drive only are the second copies of each offload's tickets, kept as phone photographs, and the duplicate Full ticket filed "
  "twice for TILX200231 offload_1. In Certify but not the batch folder: the six BOLs, the route maps, the emission factor "
  "sheets and the retirement certificate, all of which live in reporting-period folders rather than the batch folder, which the "
  "document location rule allows. Two sources carry generic names, covered at 9.9, and two corridor route maps are linked to a "
  "distance datapoint they do not evidence, covered at 3.5. [log:scale_tickets.missing_from_certify] "
  "[log:certify.certify_sources_tab_enumeration] [log:routes.generic_filenames] [log:emission_factors]", "Certify Sources"),
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
    for cw, w in [("A", 10), ("B", 46), ("C", 9), ("D", 132), ("E", 30)]:
        ws.column_dimensions[cw].width = w
    ws.freeze_panes = "A2"

    SR = json.loads((HERE / "batch_INJ-07-2026-W4_source_reads.json").read_text())

    # ---- Sheet 2: mass chain ----
    ws2 = wb.create_sheet("Mass Chain")
    ws2.append(["Offload", "Railcar", "Full (lb)", "Empty (lb)", "Tractor/Trailer", "Net (kg)",
                "Unc. Adj (kg)", "Sparging (kg)", "Filtration (kg)", "MOBI (kg)", "COBB (kg)", "Match"])
    for c in ws2[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    cobb = {r["consumed_lot"]: r["offloaded_quantity_kg"] for r in SR["cobb"]["rows"]}
    keymap = {"Rail_GPRX5102_6.23.2026_offload_2": "GPRX5102_offload_2",
              "Rail_GPRX5102_6.23.2026_offload_3": "GPRX5102_offload_3",
              "Rail_GPRX5102_6.23.2026_offload_4": "GPRX5102_offload_4",
              "Rail_TILX200231_6.25.2026_offload_1": "TILX200231_offload_1",
              "Rail_TILX200231_6.25.2026_offload_2": "TILX200231_offload_2",
              "Rail_TILX200231_6.25.2026_offload_3": "TILX200231_offload_3",
              "Rail_TILX200231_6.25.2026_offload_4": "TILX200231_offload_4"}
    for o in SR["ops_notes"]["offload_table"]:
        t = SR["scale_tickets"]["pairs"][keymap[o["id"]]]
        cv = cobb.get(o["id"])
        padj = o["net_scaled_kg"] - o["uncertainty_adjustment_kg"]
        match = "ties" if (cv is not None and abs(cv - padj) < 0.01) else \
                ("adjustment on a different row - see 5.4" if cv is not None else "-")
        ws2.append([o["id"].replace("Rail_", ""), o["railcar"],
                    o["full_lb"], o["empty_lb"],
                    f"{t['full']['tractor']}/{t['full']['trailer'].split(' ')[0]} = "
                    f"{t['empty']['tractor']}/{t['empty']['trailer'].split(' ')[0]}",
                    round(o["net_scaled_kg"], 5), round(o["uncertainty_adjustment_kg"], 5),
                    round(o["sparging_loss_kg"], 5), round(o["filtration_loss_kg"], 5),
                    round(o["mobi_kg"], 5), cv, match])
    r = SR["ops_notes"]["rollup_section4_row52"]
    ws2.append(["TOTAL", "", "", "", "", round(r["deliveries_raw_downstream_transport_kg"], 4),
                round(r["uncertainty_adj_kg"], 4), round(r["sparging_loss_kg"], 5),
                round(r["filtration_loss_kg"], 5), round(r["mobi_kg"], 5), "", "= Certify Mass of Injectant"])
    for c in ws2[ws2.max_row]:
        c.font = BOLD
    for row in ws2.iter_rows(min_row=1, max_row=ws2.max_row, max_col=12):
        for c in row:
            c.alignment = WRAP; c.border = BORDER
    for cw, w in [("A", 34), ("B", 13), ("C", 11), ("D", 11), ("E", 22), ("F", 14), ("G", 13),
                  ("H", 13), ("I", 13), ("J", 14), ("K", 14), ("L", 34)]:
        ws2.column_dimensions[cw].width = w

    # ---- Sheet 3: verification matrix ----
    ws3 = wb.create_sheet("Verification Matrix")
    ws3.append(["Quantity", "Reconstruction from primary sources", "Certify", "Result"])
    for c in ws3[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    MATRIX = [
     ("Raw offload mass", f"7 ticket pairs, (full - empty) lb x 0.453592, summed = {D['raw_offload_sum_kg']} kg",
      "136,376.97 kg", "ties"),
     ("GPRX5102 railcar balance",
      f"BOLs 25,600 + 26,050 + 26,040 = {D['gprx_bol_aggregate_kg']} kg; raw draw {D['gprx_railcar_raw_total_kg']} kg; "
      f"over-draw {D['gprx_overdraw_kg']} kg booked on the closing offload", "77,690 kg", "ties after adjustment"),
     ("TILX200231 railcar balance",
      f"BOLs 26,100 + 26,050 + 25,830 = {D['tilx_bol_aggregate_kg']} kg; raw draw {D['tilx_this_week_raw_kg']} kg; "
      f"over-draw {D['tilx_overdraw_kg']} kg booked on the closing offload", "77,980 kg", "ties after adjustment"),
     ("Mass of injectant",
      f"{D['mass_used_post_adj_kg']} - {D['sparging_total_kg']} (sparging) - {D['filtration_total_kg']} (filtration) "
      f"= {D['mobi_kg']} kg", "134,084.34946 kg", "ties"),
     ("Gross sequestration",
      f"134.08435 t x 0.394 x 3.667 = {D['gross_co2e_recalc_t']} t", "193.725 t", "ties"),
     ("Pyrolysis PROCESS",
      f"136.37697 t x 0.104 = {D['pyrolysis_process_recalc_t']} t (sheet final quantity would give "
      f"{D['pyrolysis_process_at_sheet_ef_t']} t)", "14.183 t", "ties to the stored factor - see 6.4"),
     ("Pyrolysis EMBODIED", f"136.37697 t x 0.02116 = {D['pyrolysis_embodied_recalc_t']} t", "2.886 t", "ties"),
     ("AECN->SOPOR truck PROCESS",
      f"136.37697 t x 107.49722 mi x 0.0001143 = {D['aecn_sopor_truck_process_recalc_t']} t", "1.676 t", "ties"),
     ("SOPOR->Opelousas rail PROCESS",
      f"136.37697 t x 2199 mi x 0.000025910374 = {D['rail_process_recalc_t']} t", "7.770 t", "ties"),
     ("Opelousas->Basco truck PROCESS",
      f"136.37697 t x 42.9 mi x 0.0001143 = {D['opel_basco_truck_process_recalc_t']} t", "0.669 t", "ties"),
     ("AECN->SOPOR truck EMBODIED",
      f"{D['allocated_truck_distance_mi_calc']} mi x 0.0002375605888 = {D['aecn_sopor_truck_embodied_recalc_t']} t",
      "0.134 t", "ties"),
     ("SOPOR->Opelousas rail EMBODIED",
      f"{D['allocated_rail_distance_mi_calc']} mi x 0.00003113066508 = {D['rail_embodied_recalc_t']} t", "0.120 t", "ties"),
     ("Opelousas->Basco truck EMBODIED",
      f"{D['allocated_opel_basco_mi_calc']} mi x 0.0002375605888 = {D['opel_basco_truck_embodied_recalc_t']} t",
      "0.143 t", "ties"),
     ("Aggregate distance AECN->SOPOR",
      f"107.5 mi x 3 inbound trips x each offload's post-adjustment share of its railcar, summed "
      f"= {D['allocated_truck_distance_mi_calc']} mi", "563.77 mi", "ties - evidence gap at 3.5"),
     ("Allocated distance rail",
      f"2199 mi x the same shares, summed = {D['allocated_rail_distance_mi_calc']} mi", "3,844.13278 mi",
      "ties - evidence gap at 3.5"),
     ("Allocated distance Opelousas->Basco",
      f"42.9 mi x 2 (round trip) x 7 offloads = {D['allocated_opel_basco_mi_calc']} mi", "600.6 mi",
      "ties - evidence gap at 3.5"),
     ("Transport process sum", f"1.676 + 7.770 + 0.669 = {D['transport_process_certify_sum_t']} t", "-",
      "basis for the BCU"),
     ("Transport embodied sum", f"0.134 + 0.120 + 0.143 = 0.397 t", "-", "not BCU-eligible"),
     ("Bio-oil transport total", f"{D['transport_process_sum_t']} + {D['transport_embodied_sum_t']} "
      f"= {D['transport_total_t']} t", "10.512 t", "ties"),
     ("BCU - Transport Process", f"equals the transport process sum, {D['bcu_transport_t']} t", "10.115 t",
      "fully offset, nothing over-claimed"),
     ("AECN activities", f"pyrolysis {D['pyrolysis_subtotal_t']} + transport {D['transport_certify_subtotal_t']} "
      f"= {D['aecn_activities_t']} t", "of 52.898 t total", "remainder is site emissions, out of scope"),
     ("Uncertainty discount",
      f"mass 7 x 72.57 = {D['unc_mass_total_kg']} kg and carbon 0.004 x 39.4 = {D['unc_carbon_pct_points']} propagated "
      f"over the AECN components = {D['unc_rss_aecn_only_t']} t", "1.072 t",
      "Certify deducts more - conservative"),
     ("Net CO2e removed",
      f"193.725 + 20.197 - 52.898 - 1.072 = {D['net_calc_t']} t", "159.953 t", "ties"),
     ("GHG statement row",
      f"9 entries summing to {D['ghg_statement_total_t']} t; buffer {D['buffer_pct']} %",
      "159.95 t / 874.53 t", "ties"),
    ]
    for m in MATRIX:
        ws3.append(list(m)); r2 = ws3.max_row
        for col in range(1, 5):
            ws3.cell(r2, col).alignment = WRAP; ws3.cell(r2, col).border = BORDER
        if "gap" in str(m[-1]) or "6.4" in str(m[-1]):
            for col in range(1, 5):
                ws3.cell(r2, col).fill = FLAG_FILL; ws3.cell(r2, col).font = FLAG_FONT
    for cw, w in [("A", 34), ("B", 96), ("C", 26), ("D", 38)]:
        ws3.column_dimensions[cw].width = w
    return wb


if __name__ == "__main__":
    build_with_validation(
        rows=ROWS,
        source_reads_path=HERE / "batch_INJ-07-2026-W4_source_reads.json",
        out_path=HERE / "Batch_INJ-07-2026-W4_QA_Checklist.xlsx",
        build_workbook_fn=build_workbook,
        derived_values=DERIVED,
    )
    from collections import Counter
    tally = Counter(r[2] for r in ROWS if r[2] != "SECTION")
    print("tally:", dict(tally))
