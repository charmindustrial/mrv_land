#!/usr/bin/env python3
"""Build INJ-07-2026-W1 AECN weekly batch QA checklist."""
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

SR = json.loads((HERE / "batch_INJ-07-2026-W1_source_reads.json").read_text())
D = SR["_derived_values"]

ROWS = [
 ("INJ-07-2026-W1 — AECN Weekly Batch QA",
  "Reviewer: Claude QA Agent  |  Date: 2026-08-05  |  Injection Site: Basco 6  |  Oil Type: AECN (rail)  |  "
  "Ops week: Sat 2026-06-27 to Sat 2026-07-04  |  Injected: 2026-07-04  |  Certify GHG entry rmv_1KYT7WF6Q1S03R7Q "
  "(period 01–04 Jul 2026)  |  Net CDR 415.176 tCO2e", "SECTION", "", ""),
 ("Scope",
  "Time-block (weekly) batch = all AECN oil injected in the week, aggregated into ONE Certify GHG entry. AECN is all rail: "
  "16 truck-out offloads from 4 railcars (GRPX5188 / GPRX5098 / GPRX5236 / GPRX5107, 4 offloads each) fed by 12 inbound BOLs. "
  "WODO and QOWV were also injected this week but are out of scope for this entry (separate skills). [log:batch_id]", "SECTION", "", ""),
 ("SUMMARY OF FINDINGS",
  "The mass chain verifies end to end. Certify reconciles arithmetically to the Ops Notes; the Ops Notes reconciles to the 12 "
  "inbound BOLs (313,530 kg aggregate) and to the scale tickets on 13 of 16 offloads; and the remaining three offloads use the "
  "documented KL192 trailer standard empty weight of 29,510 lb because each has a rig mismatch between its full and empty ticket. "
  "That substitution was checked four ways at 2.9 — trigger scope, published value (29,321 mean + 189 sigma), trailer selection, "
  "and direction — and is correct on all four. It is deliberately conservative: the week claims 128.2902 kg less mass than raw "
  "ticket math would give, forgoing about 0.1877 tCO2e. Gross sequestration, both pyrolysis components, all six transport "
  "components, the BCU offset, every uncertainty input and all three allocated distances reconstruct to the reported figures. "
  "No Fails. Re-read of Certify on 2026-08-06 found the evidence-linkage gap closed and one methodology improvement: the three "
  "allocated/aggregate distance datapoints now carry the Ops Notes alongside their route image (sources 59 → 62), and a new "
  "datapoint 'Bio-Oil Mass - AECN via Rail (downstream, scale tickets)' 313,028.37512 kg now bases the Opelousas→Basco truck leg "
  "on the mass those trucks actually carried instead of the BOL aggregate. That moved the leg 1.537 → 1.535 t, activities 63.400 "
  "→ 63.398 t and net 415.173 → 415.176 t, and it removed the 0.7 kg rounding shortfall in BCU coverage — the BCU now exceeds the "
  "process sum by 0.0018 t. Five Flags remain: the pyrolysis factor entered at 0.104 against the sheet's 0.1040167408, two "
  "COBB-side items (a missing GPRX5236 offload_1 row and a stale GPRX5107 offload_1 value), BOL print corrections, generic source "
  "filenames, and the RP-level documents outside batch scope. Correction history: an earlier draft raised six Fails across "
  "sections 2, 5 and 8 against the 29,510 lb tare, before the reporting-period VVB guidance and the Ops Notes cell annotations "
  "had been read. Both document the substitution explicitly and name these three offloads. Those six findings were withdrawn.", "SECTION", "", ""),

 ("1. Batch Folder Completeness", "", "SECTION", "", ""),
 ("1.1", "Batch folder named with batch ID", "Pass",
  "Drive folder titled 'W1' (id 1z9nzSrTSuW5BzIJVPGVOlb42LTQFF24y); the Ops Notes workbook and its Summary tab both carry batch "
  "ID 'INJ-07-2026-W1', matching the Certify entry period 01–04 Jul 2026. [log:batch_id] [log:drive._primary_source_opened]", "VR Appendix 1"),
 ("1.2", "Scale Tickets subfolder present and populated", "Pass",
  "Scale Tickets subfolder holds one folder per railcar (GPRX5098 / GPRX5107 / GPRX5236 / GRPX5188), each with offloads 1–4. "
  "All 32 Certify-linked tickets (full + empty × 16 offloads) were downloaded and read this session; the axle weights sum to the "
  "stated gross on every ticket. [log:drive.scale_tickets_subfolders] [log:scale_tickets._primary_source_opened]", "VR Appendix 1"),
 ("1.3", "Testing subfolder present with lab results", "Pass",
  "Testing subfolder holds the AECN weekly composite certificate 'CHARM INDUSTRIAL - AECN 7-2026-W1, QOWV 7-2026-W2.pdf' "
  "(SGS SR26-04220.001), plus the WODO and QOWV certificates for the other oil types. [log:drive.testing_folder_items] "
  "[log:lab_results.certificate_no]", "VR Appendix 1"),
 ("1.4", "Ops Notes present and complete", "Pass",
  "Weekly master workbook 'INJ-07-2026-W1 Ops Notes' exported and read cell-by-cell. AECN Rail tab has all four sections "
  "populated: Section 1 railcars received, Section 2 origins ledger (12 BOLs), Section 3 scale tickets + offload weights "
  "(16 rows), Section 4 rollup. [log:ops_notes._primary_source_opened] [log:ops_notes.constants]", "VR Appendix 1"),
 ("1.5", "Injection site confirmed Basco 6 — no deprecated Vaulted references", "Pass",
  "All 12 BOLs route AECN (Port-Cartier QC) → SOPOR (Baie-Comeau QC); offload tickets weigh at Bunkie / Opelousas LA; the "
  "Certify entry sits in the Charm Bio-oil Geologic Storage project. Every source document opened this session refers only to "
  "AECN, SOPOR, Opelousas or Basco. The SGS certificate's LOCATION field spells it 'BOSCO, LA' — a lab typo for Basco, not a "
  "different site. [log:bol.all_dest_sopor] [log:lab_results.note_location_spelling]", "Basco verification"),

 ("2. Scale Tickets & Mass Determination", "", "SECTION", "", ""),
 ("2.1", "Full and empty ticket images present and legible for each offload", "Pass",
  "Two tickets on file for every one of the 16 offloads — 32 in total, 27 CAT-generated PDFs and 5 phone photos of the CAT "
  "ticket. All 32 opened and read; the three photo-sourced empties were cropped and upscaled 2.6× to read the digits with "
  "certainty, and the axle weights sum to the stated gross on every ticket. Whether each pair belongs to the same vehicle is "
  "assessed separately at 2.3. [log:scale_tickets] [log:scale_tickets.count_read]", "VR Sec 5.1"),
 ("2.2", "Ticket dates within 2 weeks of injection", "Pass",
  "All 32 ticket dates read off the tickets: earliest 6-29-26 (GPRX5098 offload_1 full), latest 7-04-26 (GPRX5107 offload_4 "
  "empty), against an injection date of 2026-07-04 — every weighing inside 14 days. [log:scale_tickets.date_range] "
  "[log:scale_tickets.per_offload]", "VR Sec 3.5"),
 ("2.3", "Tractor and trailer numbers match between full and empty tickets", "Pass",
  "13 of 16 offloads match outright (e.g. GPRX5098 offload_1 CH1/KL192 on both; GPRX5107 offload_4 CH1/KL510 on both). Three "
  "do not: GRPX5188 offload_1 full CH1/KL 192 vs empty CH2/192; GRPX5188 offload_3 full CH1/KL 192 vs empty CH1/KL720; "
  "GPRX5107 offload_3 full CH2/192 vs empty CH1/RL192. Under the reporting-period VVB guidance these are not errors but the "
  "defined trigger for a substitution. The guidance records the cause — 'an operational artifact of a drop-trailer delivery "
  "arrangement' where the loaded weighing carries one tractor and the tare weighing another — and states that 'The make and "
  "model of the trailer ... is the same across both the full and empty weighings, and is the basis on which the two tickets are "
  "matched for that offload.' It then names these exact three offloads in its July 1-31 application list. Handling verified at "
  "2.9. [log:vvb_guidance] [log:vvb_guidance.quote_trigger] [log:vvb_guidance.quote_application_w1] [log:vvb_guidance.quote_drop_trailer] [log:scale_tickets.per_offload]", "VR Sec 5.1"),
 ("2.4", "Net mass correctly calculated in Ops Notes (each offload recomputed)", "Pass",
  "13 of 16 offloads recompute exactly from the ticket images: net (kg) = (Full lb - Empty lb) x 0.453592 equals the Ops Notes "
  "offload-table net to five decimals (e.g. GPRX5098 offload_1 (79,840 - 29,280) x 0.453592 = 22,933.61152 = Ops; GPRX5236 "
  "offload_3 (74,820 - 29,380) x 0.453592 = 20,611.22048 = Ops). The remaining three (GRPX5188 offload_1 and offload_3, "
  "GPRX5107 offload_3) use the documented KL192 standard empty weight of 29,510 lb rather than their filed empty ticket, "
  "because each has a rig mismatch. Those three also recompute exactly on that basis. See 2.9 for the verification of the "
  "substitution itself. [log:vvb_guidance] [log:vvb_guidance.quote_trigger] [log:vvb_guidance.quote_application_w1] [log:scale_tickets.per_offload] "
  "[log:_derived_values.kl192_standard_empty_lb]", "VR Sec 5.1"),
 ("2.5", "Last-offload conservatism (FC11) applied per railcar", "Pass",
  "Fires on exactly the one railcar that overdraws its inbound BOL aggregate and on no other. GPRX5098: offloads sum to "
  "78,353.48208 kg against a BOL aggregate of 78,250, so a back-calc of 103.48208 kg is applied to offload_4 - the only "
  "Uncertainty Adjustment on the week. The other three are all under their aggregate and correctly carry none: GRPX5188 "
  "77,981.53664 vs 78,030, GPRX5236 78,063.1832 vs 78,540, GPRX5107 78,630.1732 vs 78,710, with the shortfalls booked in the "
  "Ops 'Loss (kg)' column. [log:scale_tickets.per_railcar] [log:ops_notes.railcars] [log:ops_notes.rollup]", "GHG Stmt Sec C"),
 ("2.6", "1.29% sparging deduction applied", "Pass",
  "Recomputed from the Ops rollup: 312,924.893 kg mass used × 0.0129 = 4,036.73112 kg, equal to the Ops Notes sparging loss of "
  "4,036.73112 kg. Applied per offload on the post-adjustment mass, so the offload_4 row of GPRX5098 sparges on 13,277.48192 kg "
  "rather than its raw 13,380.964 kg. [log:ops_notes.rollup] [log:_derived_values.sparging_recalc_kg]", "GHG Stmt Sec C"),
 ("2.7", "Mass values consistent across scale tickets, Ops Notes, COBB and Certify", "Pass",
  "The Ops Notes to Certify chain is exact: Ops mass used 312,924.893 - sparging 4,036.73112 - filtration 602.33192 = "
  "308,285.83 kg = the Certify Mass of Injectant datapoint, and the 12-BOL aggregate 313,530 kg = the Certify Bio-Oil Mass "
  "datapoint. Since 2026-08-06 the downstream truck leg also has its own basis in Certify — 'Bio-Oil Mass - AECN via Rail "
  "(downstream, scale tickets)' 313,028.37512 kg, which is the Ops 'Deliveries raw / Downstream Transport (scale tickets)' figure "
  "— so each leg is now costed on the mass that leg actually carried: the BOL aggregate upstream, the scale-ticket total on the "
  "delivery trucks. On 13 offloads Ops equals raw ticket math; on the three rig-mismatch offloads it equals the documented "
  "standard empty basis instead, which is the intended treatment. COBB carries raw ticket math throughout and so differs on those "
  "three by design - the verifier reads Ops Notes and Certify. Two COBB-side items are at 5.4. "
  "[log:vvb_guidance] [log:vvb_guidance.quote_trigger] [log:vvb_guidance.quote_application_w1]" " [log:ops_notes.rollup] [log:certify.datapoints]", "VR Sec 5.1"),
 ("2.8", "Filtration loss (0.195%) deduction applied after sparging", "Pass",
  "Recomputed: (312,924.893 − 4,036.73112) × 0.00195 = 602.33192 kg, equal to the Ops Notes filtration loss of 602.33192 kg. "
  "The constant is labelled 'Filtration Solids Content' 0.00195 in the Ops Notes constants block and is applied after the "
  "sparging deduction — conservative, since it reduces credited mass. [log:ops_notes.rollup] "
  "[log:_derived_values.filtration_recalc_kg] [log:ops_notes.constants]", "GHG Stmt Sec C"),

 ("2.9", "Trailer standard empty weight substitution applied correctly (rig-mismatch offloads)", "Pass",
  "Checked the substitution against the method rather than taking it on trust, on four points. Trigger scope: exactly 3 of the "
  "16 offload pairs have a rig mismatch, and 29,510 lb appears on exactly those 3 rows and on no others — no offload with a "
  "matching pair was given a standard weight, and no mismatched offload was left on its filed ticket. Value: the guidance "
  "publishes KL192 as n = 22, mean 29,321 lb, sigma 189 lb, standard empty = mean + 1 sigma, and 29,321 + 189 = 29,510 lb, the "
  "figure entered. Trailer selection: each of the three loaded on KL192 per its full ticket, so KL192 is the right standard — "
  "including GRPX5188 offload_3, where the filed empty ticket is KL720 and is correctly set aside rather than used. Direction: "
  "the substituted 29,510 lb is heavier than the filed empties it replaces (29,180 / 29,380 / 29,180), which lowers net injected "
  "mass, so the treatment under-credits, as the method intends — 'Because a heavier empty weight yields a lower net injected "
  "mass, mean + 1 sigma ensures the substitution is conservative (under-crediting)'. Measured effect for the week: mass claimed "
  "is 128.2902 kg lower than raw ticket math would give, worth 0.1877 tCO2e of credit foregone. "
  "[log:vvb_guidance] [log:vvb_guidance.quote_method] [log:vvb_guidance.verification] "
  "[log:vvb_guidance.standard_empty_table_lb] [log:_derived_values.kl192_mean_plus_sigma_lb] "
  "[log:_derived_values.n_offloads_triggering_substitution] [log:_derived_values.ops_underclaim_kg] "
  "[log:_derived_values.underclaim_co2e_t]", "GHG Stmt Sec C"),

 ("3. Bills of Lading & Transportation", "", "SECTION", "", ""),
 ("3.1", "All inbound truck BOLs present (3 per railcar into SOPOR)", "Pass",
  "All 12 BOLs opened and read individually — 2377-R/2378-R/2379-R (GPRX5236), 2380-R/2381-R/2382-R (GPRX5098), "
  "2383-R/2384-R/2385-R (GPRX5107), 2386-R/2387-R/2388-R (GRPX5188). Three per railcar, as expected for AECN rail. "
  "[log:bol._primary_source_opened] [log:bol.reads]", "VR Appendix 1"),
 ("3.2", "BOL destination is the SOPOR railyard", "Pass",
  "All 12 BOLs show Ship To 'CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau, 18 Route Maritime, "
  "Baie-Comeau, Québec G4Z 2L6', contact Cédric Bérubé at cedric.berube@sopor.ca — the SOPOR railyard, not Basco. "
  "[log:bol.all_dest_sopor]", "VR Appendix 1"),
 ("3.3", "BOL mass matches the Ops origins ledger; railcar aggregate ≥ claimed mass", "Pass",
  "Each BOL's weighbridge Masse nette (page 3) and page-2 'Qty shipped' agree with the Ops origins ledger to the kilogram, all "
  "12: 26,190 / 26,080 / 26,270 (GPRX5236); 26,160 / 25,910 / 26,180 (GPRX5098); 26,520 / 25,970 / 26,220 (GPRX5107); "
  "25,900 / 25,950 / 26,180 (GRPX5188). Per-railcar sums 78,540 / 78,250 / 78,710 / 78,030 kg each equal that railcar's Ops "
  "'Total Loaded' and each is greater than or equal to its claimed offload mass. The 12 sum to 313,530 kg. [log:bol.reads] "
  "[log:bol.per_railcar_bol_sum_kg] [log:_derived_values.bol_aggregate_kg_recalc]", "VR Sec 3.5"),
 ("3.4", "Origin and destination correct on every BOL", "Pass",
  "All 12: From/De 'BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier, Québec G5B 2V9' — the AECN plant — "
  "to SOPOR Baie-Comeau; product 'Renewable Fuel Oil RFO / Huile pyrolytique' (pyroligneous acids); carrier Transport "
  "Baie-Comeau. [log:bol.all_origin_aecn] [log:bol.all_dest_sopor] [log:bol.carrier]", "PDD Sec A"),
 ("3.5", "Transport distances consistent with the known AECN rail route", "Pass",
  "Full-leg distances all trace to opened evidence. AECN→SOPOR: the route map shows a single Google Maps route via QC-138 O of "
  "173 km, and 173 ÷ 1.609344 = 107.49722 mi, exactly the Certify datapoint. SOPOR→Opelousas: 2,199 mi, evidenced by the Watco "
  "rail-logistics email ('The total milage for this move was 2199') — the carrier-confirmation route used for rail instead of a "
  "map. Opelousas→Basco: the map offers 42.9, 42.9 and 40.9 mi and Certify uses the longest, 42.9 mi. The allocated distances "
  "also reconstruct from the Ops Notes offload table: AECN→SOPOR aggregate 1,287.514724 mi = the Certify 1,287.51; rail "
  "allocated 8,779.053888 mi = Certify 8,779.05; Opelousas→Basco allocated 1,372.8 mi = 42.9 × 2 (round trip) × 16 offloads = "
  "Certify 1,372.8. The two upstream legs are allocated by each offload's share of its railcar's BOL mass; because the Ops table "
  "rounds each per-offload distance, the implied share totals differ trivially between them (3.992397 railcar-equivalents on the "
  "truck leg, 3.992294 on the rail leg — a 0.0001 difference). The round-trip doubling on the Charm-operated delivery leg "
  "follows §5.0: 'full round trip distance of "
  "vehicle traveled when vehicle returns to origination site unloaded, or if next destination is unknown'. "
  "[log:routes._primary_source_opened] [log:_derived_values.km_to_mi_173km] [log:_derived_values.opel_roundtrip_mi_check] "
  "[log:ops_notes.ee_totals_row48] [log:protocol.quote_round_trip]", "Transport Emissions Acctg v1.1"),
 ("3.6", "Transport mode and leg count correct for rail", "Pass",
  "Six transport components on the entry, as expected for a three-leg rail movement: AECN→SOPOR tanker truck process 3.852 t and "
  "embodied 0.306 t; SOPOR→Opelousas rail process 17.864 t and embodied 0.273 t; Opelousas→Basco tanker truck process 1.537 t "
  "and embodied 0.326 t. §5.0 requires that 'Calculations shall be completed separately for each leg of the trip associated "
  "with a removal'. [log:certify.components] [log:protocol.quote_per_leg]", "Certify Datapoints"),
 ("3.7", "Billing / BOL details consistent with the shipments", "Flag",
  "Mass, routing and product are correct on all 12; the flag is documentation hygiene on the BOLs themselves. 2381-R page 1 "
  "carries a '***Correction CofA' note with the certificate-of-analysis number struck through and replaced; 2383-R carries "
  "'***Correction page 2: densité + # de litres' changing litres from 22,038 to 21,928 and density from 1.2034 to 1.2094; "
  "2383-R and 2385-R print the production period as '#0X-2026' rather than a month. None of these touches the weighbridge Masse "
  "nette that Ops uses. Each BOL also prints a volume-derived estimated quantity below the weighed mass (2386-R: 25,474 kg "
  "estimated vs 25,900 kg weighed) — Ops correctly takes the weighed figure. [log:bol.print_quirks_FLAG] "
  "[log:bol.estimated_vs_weighed]", "VR Appendix 1"),

 ("4. Bio-Oil Composition & Testing", "", "SECTION", "", ""),
 ("4.1", "CHN analysis certificate present", "Pass",
  "SGS Certificate of Analysis SR26-04220.001 (SGS order 5470884) opened and read in full: client ID 'AECN 7-2026-W1', sampled "
  "08-Jul-2026 07:20, analysed 13-Jul-2026, signed by Jaszmine Eugene, Chemist, SGS North America. It is in the Drive Testing "
  "subfolder and attached in Certify against the Carbon Content datapoint. [log:lab_results.certificate_no] "
  "[log:lab_results._primary_source_opened] [log:certify.attachment_map]", "VR Appendix 1"),
 ("4.2", "Carbon content within the expected AECN range", "Pass",
  "Certificate carbon 40.5 % (m/m) by ASTM D5291 Method C. Against the historical AECN population read from the Summary "
  "Statistics tab of MRV_AECN_Analysis.xlsx — mean 39.420350877193 %, standard deviation 6.09332409018271 %, n = 285 — the "
  "2-standard-deviation band runs 27.2337 % to 51.607 % and 40.5 % sits at +0.1772 standard deviations. Well inside range. "
  "[log:lab_results.carbon_pct] [log:mrv_historical] [log:_derived_values.carbon_2sd_low_pct] "
  "[log:_derived_values.carbon_2sd_high_pct] [log:_derived_values.carbon_z_score]", "Biomass Feedstock Acctg v1.2"),
 ("4.3", "Hydrogen and nitrogen reported and reasonable", "Pass",
  "Hydrogen 7.2 % (m/m) and nitrogen <0.75 % (m/m), both ASTM D5291 Method C, alongside kinematic viscosity 33.44 cSt at 40 °C "
  "and acid number 73 mg KOH/g by ASTM D664 Method A. Nitrogen below the detection limit is the normal reporting form for this "
  "oil — the historical dataset records numeric nitrogen for only 9 of 285 samples. [log:lab_results.hydrogen_pct] "
  "[log:lab_results.nitrogen_pct] [log:lab_results.viscosity_cSt_40C]", "Biomass Feedstock Acctg v1.2"),
 ("4.4", "Lab report references the correct batch / sample ID", "Pass",
  "The certificate's CLIENT ID reads 'AECN 7-2026-W1', matching the composite sample ID recorded on the Ops Notes Summary tab "
  "('7-2026-W1 AECN') and its lab reference 'COA SR26-04220.001'. Page 2 of the same PDF is a separate certificate "
  "(SR26-04220.002) for the QOWV composite — a different oil type, out of scope here. [log:lab_results.client_id] "
  "[log:ops_notes.summary_tab]", "VR Sec 5.1"),
 ("4.5", "pH / conductivity (aqueous phase)", "N/A",
  "AECN is not an aqueous-phase oil; pH for this batch is checked at 5.5. [log:oil_type]", "UIC Permit / LDENR"),
 ("4.6", "Density above the formation-fluid threshold", "Pass",
  "Certificate density at 15 °C = 1.218 g/cm³ by ASTM D4052, comfortably above the 1.01 g/cm³ formation-fluid floor for safe "
  "injection. Corroborated independently by the sample densities printed on all 12 BOLs, which span 1.2087 to 1.2159 g/ml at "
  "60 °F — every one above the floor. [log:lab_results.density_15C_g_cm3] [log:bol.reads] [log:bol.density_range_g_ml]", "VR Sec 5.1"),

 ("5. Ops Notes Accuracy & Internal Consistency", "", "SECTION", "", ""),
 ("5.1", "Correct batch ID and injection date", "Pass",
  "Ops Notes batch header and Summary tab both read INJ-07-2026-W1 with week Sat 2026-06-27 to Sat 2026-07-04; all 16 offload "
  "rows are dated 2026-07-04, matching the COBB injection_completion_date of 2026-07-04 for all 15 rows it holds. "
  "[log:batch_id] [log:cobb.injection_completion_date] [log:ops_notes.offload_table]", "—"),
 ("5.2", "Scale ticket values correctly transcribed into Ops Notes", "Pass",
  "All 16 full weights and 13 of 16 empty weights transcribe exactly from the ticket images. The other three empty cells hold "
  "29,510 lb, which is not a transcription of a ticket but the documented KL192 standard empty weight, and each of those three "
  "cells carries a note in the workbook saying so: 'Standard empty weight (KL192 = mean+1SD = 29,510 lb) substituted per "
  "Trailer Standard Empty Weight methodology (rig mismatch between full/empty ticket).' The guidance requires exactly this - "
  "'Substituted values are annotated in the ops-notes Empty Scale Ticket cell' - and the annotation is present on all three. "
  "[log:vvb_guidance] [log:vvb_guidance.quote_trigger] [log:vvb_guidance.quote_application_w1]" " [log:vvb_guidance.ops_notes_cell_annotations] [log:scale_tickets.per_offload]", "VR Sec 5.1"),
 ("5.3", "Oil and aqueous phase mass reconciliation", "N/A",
  "AECN-only entry; there is no aqueous phase to reconcile. [log:oil_type]", "—"),
 ("5.4", "COBB values present and matched per offload", "Flag",
  "COBB tab 'Basco Injection -- COBB' holds 15 rows under injection_batch 'INJ-07-2026-W1_bio_oil' (rows 310–325). "
  "origin_quantity_kg per railcar (78,030 / 78,250 / 78,540 / 78,710) equals the BOL aggregates; the BOL number lists are "
  "correct for all four railcars; injection_completion_date 2026-07-04 and injection_ph 3.7 match the Ops Notes. Two COBB-side "
  "issues. GPRX5236 offload_1 has no row at all — 15 rows where 16 offloads were injected, and the Ops Notes plus both tickets "
  "(Full 74,300 lb / Empty 29,040 lb) do carry it. GPRX5107 offload_1 reads 19,658.67728 kg, which back-solves to a 29,200 lb "
  "tare; the tickets for that offload are Full 72,540 / Empty 28,720, both CH2/KL 188, giving 19,876.40144 kg, which is what Ops "
  "and Certify use. On that one offload COBB is the outlier. Neither issue changes the credited figure, which follows the Ops "
  "Notes. [log:cobb._primary_source_opened] [log:cobb.findings] [log:cobb.rows_found]", "—"),
 ("5.5", "pH measurement noted", "Pass",
  "pH 3.7 recorded on every one of the 16 offload rows and in the Section 4 rollup, inside the Ops Notes target band of "
  "2.0–4.0; COBB injection_ph independently reads 3.7. [log:ops_notes.rollup] [log:ops_notes.constants] "
  "[log:cobb.injection_ph]", "—"),
 ("5.6", "Completion date present and matches COBB", "Pass",
  "Ops Notes week end and offload dates give 2026-07-04; COBB injection_completion_date is 2026-07-04 on all 15 rows. The "
  "Certify entry period 01–04 Jul 2026 contains that date. [log:cobb.injection_completion_date] [log:certify.period]", "—"),
 ("5.7", "No erroneous density measurements", "N/A",
  "The weekly Ops Notes format carries no density field for AECN, so there is no value to be wrong. Density is evidenced by the "
  "lab certificate and the BOLs instead (see 4.6). [log:ops_notes.constants] [log:lab_results.density_15C_g_cm3]", "VR Sec 5.1"),

 ("6. AECN Feedstock Emissions & Allocation", "", "SECTION", "", ""),
 ("6.1", "AECN process emissions LCA CI spreadsheet present", "Pass",
  "Certify Sources include 'Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx', linked to the "
  "pyrolysis process carbon-intensity datapoint. [log:certify.attachment_map] [log:certify.sources_enumeration]", "VR Appendix 1"),
 ("6.2", "LCA with stack emissions file present", "Pass",
  "Certify Sources include 'BH 2025 LCA w Stack Emissions.xlsx', also linked to the pyrolysis process carbon-intensity "
  "datapoint. The stack component is visible in the live emission-factor workbook's derivation tab as 0.00412683 MTCO2e per MT "
  "of bio-oil. [log:certify.attachment_map] [log:ef_live_source.aecn_process_derivation]", "VR Appendix 1"),
 ("6.3", "Supporting GHG data file present for the AECN production period", "Pass",
  "Certify Sources include 'Supporting GHG data 31Dec2025 S.xlsx', linked to the same datapoint. Four sources back the "
  "pyrolysis process carbon intensity in total. [log:certify.attachment_map] [log:certify.sources_enumeration]", "VR Appendix 1"),
 ("6.4", "AECN pyrolysis process emission factor matches the current published value", "Flag",
  "Certify carries 0.104 tCO2e/t. The live Standard Emission Factors 2026 tab gives a Final Quantity of 0.1040167408 MTCO2e/MT "
  "for 'Production Emissions for AECN Oil--H1 2026' (baseline 0.1038 plus an uncertainty factor of 0.002088061302). Certify's "
  "value is the baseline rounded to three decimals, so the pyrolysis process emission is understated by 0.00525 tCO2e "
  "(313.530 t × 0.0000167408). Immaterial in size but it is the non-conservative direction, and the entry should carry the "
  "sheet's full-precision factor. H1 2026 is the right vintage to use: the 2026 tab has no H2 2026 AECN row. "
  "[log:ef_live_source] [log:ef_live_source.aecn_process_final] [log:ef_live_source.h2_2026_row_absent] "
  "[log:_derived_values.pyro_process_ef_shortfall_t] [log:_derived_values.pyro_process_at_sheet_ef_t]", "Certify Datapoints"),
 ("6.5", "AECN pyrolysis embodied emission factor applied", "Pass",
  "Certify carries 0.02116 tCO2e/t, exactly the live Standard Emission Factors 2026 tab Final Quantity for 'Embodied Emissions "
  "for AECN Oil' (0.02116 MTCO2e/MT, sourced to AECN information and the NAICS supply-chain factors). Recomputed: 313.530 t × "
  "0.02116 = 6.6343 t against the Certify component of 6.634 t. [log:ef_live_source] "
  "[log:ef_live_source.aecn_embodied_final] "
  "[log:_derived_values.pyro_embodied_recalc_t]", "Certify Datapoints"),
 ("6.6", "Pyrolysis factors applied to pre-sparging origin mass", "Pass",
  "Both pyrolysis component modals take their mass from 'Bio-Oil Mass - AECN via Rail' = 313,530 kg, the 12-BOL aggregate — the "
  "mass AECN actually produced — not the post-deduction injectant of 308,285.83 kg. Correct: the pyrolysis emissions were "
  "incurred to make the whole quantity. [log:certify.uncertainty_modals_read] [log:certify.datapoints]", "Certify Components"),

 ("7. Gross-to-Net Calculation", "", "SECTION", "", ""),
 ("7.1", "Gross CO2e = injectant mass × carbon × 3.667", "Pass",
  "Recomputed: 308,285.83 kg × 0.405 × 3.667 = 457,846.076 kgCO2e = 457.8461 t, against the Certify injection sequestration "
  "component of 457.846 t. The mass and carbon inputs both trace to attached evidence — the Mass of Injectant datapoint is "
  "backed by the 32 tickets, the 12 BOLs and the Ops Notes, and Carbon Content by the SGS certificate. "
  "[log:_derived_values.gross_co2e_recalc_kg] [log:_derived_values.gross_co2e_recalc_t] "
  "[log:certify.calculation_view] [log:certify.attachment_map]", "GHG Stmt Sec E"),
 ("7.2", "Process emissions correctly deducted", "Pass",
  "Activities recomputed component by component: pyrolysis 32.6071 + 6.6343, transport process 3.8523 + 17.864 + 1.5349, "
  "transport embodied 0.3059 + 0.2733 + 0.3261 — total 63.3979 t against the Certify activities figure of 63.398 t. Every leg "
  "reconstructs from mass × distance × factor (process) or allocated distance × per-mile factor (embodied); the full "
  "reconstruction is on the Certify Recon sheet. [log:_derived_values.activities_recalc_t] "
  "[log:_derived_values.transport_process_sum_t] [log:_derived_values.transport_embodied_sum_t]", "GHG Stmt Sec E"),
 ("7.3", "Uncertainty discount correctly applied", "Pass",
  "The Calculation View carries an Uncertainty Discount of 2.526 t, which is 0.5517 % of the 457.846 t gross sequestration, "
  "deducted after sequestrations and adjustments and before the net. [log:certify.calculation_view] "
  "[log:_derived_values.uncertainty_discount_pct_of_gross]", "Isometric Standard v2.0 §3.7"),
 ("7.4", "Net removals consistent with BCU Quant sheet and GHG Statement", "Flag",
  "The arithmetic ties: 457.846 + 23.253 − 63.398 − 2.526 = 415.175 t against the Certify net of 415.176 t, the 0.001 gap being "
  "Certify summing its components at full precision where the displayed subtotals are rounded. The mass beneath it is the "
  "documented basis (see 2.9). The flag is scope: the two documents this item names were not examined. The reporting-period BCU "
  "Quant spreadsheet and the GHG Statement are both RP-level artifacts, and no GHG Statement has been issued for a period "
  "covering 01–04 Jul 2026, so consistency against them cannot be tested at batch level and should be picked up in the "
  "reporting-period review. "
  "[log:_derived_values.net_recalc_t] [log:_derived_values.certify_net_displayed_t] [log:_derived_values.ops_underclaim_kg] [log:_derived_values.underclaim_co2e_t]", "GHG Stmt Sec E"),

 ("7a. Per-Component Uncertainty Verification", "", "SECTION", "", ""),
 ("7a.1", "Completeness — every component carries uncertainty on the correct datapoint", "Pass",
  "All 10 component modals opened individually and their INPUTS read. Injection sequestration carries uncertainty on both "
  "Carbon Content and Mass of Injectant. The two pyrolysis components and all three transport process components carry it on "
  "their mass input. The three embodied components have no mass input at all — they are distance × per-mile factor — so no mass "
  "uncertainty is expected or missing there. The BCU adjustment is a constant and carries none. Every component that "
  "requires an uncertainty input carries one. "
  "[log:certify.uncertainty_modals_read] [log:certify._primary_source_opened]", "Isometric Standard v2.0 §3.7.3"),
 ("7a.2", "Correctness — reported ± values match expected", "Pass",
  "Mass uncertainty reads ±1,161.12 kg on every mass-bearing component, which is 16 offloads × 72.57 kg per discrete weighing = "
  "1,161.12 kg — one outbound weighing per offload, stacked across the week's 16 offloads. Carbon uncertainty reads ±0.162 % "
  "against a measured 40.5 %, which is 0.004 × 40.5 = 0.162. Distance inputs carry no uncertainty, as expected where the "
  "longest mapped route is used. The Ops Notes Summary tab records the same carbon figures independently (0.00162 on a 0.405 "
  "fraction, testing uncertainty 0.004). [log:certify.uncertainty_modals_read] "
  "[log:_derived_values.mass_uncertainty_expected_kg] [log:_derived_values.carbon_uncertainty_expected_pct] "
  "[log:ops_notes.summary_tab]", "Isometric Standard v2.0 §3.7.3"),
 ("7a.3", "Discount present and consistent", "Pass",
  "The 2.526 t discount is present in the Calculation View and flows into the 415.173 t net. It is computed by Certify from the "
  "per-component inputs verified at 7a.1 and 7a.2, and is 0.5517 % of gross. [log:certify.calculation_view] "
  "[log:_derived_values.uncertainty_discount_pct_of_gross]", "Isometric Standard v2.0 §3.7"),

 ("8. Data Integrity & Anomaly Check", "", "SECTION", "", ""),
 ("8.1", "No unexplained outliers in mass, carbon content or calculated values", "Pass",
  "Carbon (40.5 %), density (1.218 g/cm3), the 12 BOL masses (25,900-26,520 kg) and the 16 offload nets all sit in normal "
  "range. The one value that repeats across offloads - 29,510 lb on three of them, across two railcars - is explained rather "
  "than anomalous: it is the KL192 standard empty weight, and it reconciles to the published basis exactly, 29,321 mean + 189 "
  "sigma = 29,510 lb over n = 22 weighings. [log:vvb_guidance.standard_empty_table_lb] "
  "[log:_derived_values.kl192_mean_plus_sigma_lb] [log:vvb_guidance.verification]", "GHG Stmt Sec C"),
 ("8.2", "Spills / losses documented and unrecovered mass deducted", "Pass",
  "No spill or incident is recorded anywhere in the sources opened this session — the Ops Notes has no incident field or note, "
  "and neither the offload table, the origins ledger, COBB nor any BOL records one. Railcar-level losses are accounted for "
  "instead: GRPX5188 48.46336 kg, GPRX5236 476.8168 kg and GPRX5107 79.8268 kg of under-draw are carried in the Ops 'Loss (kg)' "
  "column, and GPRX5098's negative 103.48208 kg is resolved by the back-calc rather than treated as a gain. "
  "[log:ops_notes] [log:cobb] [log:bol] [log:ops_notes.railcars]", "GHG Stmt Sec C"),
 ("8.3", "Cross-week boundary — no offload claimed twice", "Pass",
  "All four railcars show 'Previously Claimed (kg)' of 0.0 in Ops Section 1, so none was drawn down in an earlier week. COBB "
  "confirms it from the other side: the other GPRX5188 rows in the tracker (rows 141–144) carry a different consumed-lot date "
  "(Rail_GPRX5188_5.1.2026), a different origin quantity (77,520 kg) and a different batch (INJ-05-2026-W4, injected "
  "2026-05-31) — an earlier trip of the same railcar, not an overlap with this week's Rail_GRPX5188_6.15.2026 lot. Within this "
  "week each of the 16 offload numbers appears once. [log:ops_notes.railcars] [log:cobb.prior_week_gprx5188_rows] "
  "[log:cobb.offloaded_quantity_kg]", "VR Sec 3.5"),
 ("8.4", "Rail conservatism precondition — offloads ≥ inbound BOLs", "Pass",
  "16 outbound offload weighings against 12 inbound BOL weighings. Because the per-offload framing books 16 × 72.57 kg of mass "
  "uncertainty where the inbound weighings would have produced 12 × 72.57 kg, the aggregate discount absorbs more uncertainty "
  "than the inputs strictly require — the conservative direction. Every railcar is fully drawn down this week, so the check is "
  "settled here rather than deferred. [log:n_offloads] [log:n_inbound_bols] "
  "[log:_derived_values.mass_uncertainty_expected_kg]", "GHG Stmt Sec C"),

 ("9. Isometric Certify — Removal Component Mapping", "", "SECTION", "", ""),
 ("9.1", "SEQUESTRATIONS — gross injection sequestration matches internal gross", "Pass",
  "One sequestration component, 457.846 t. Reconstructed from its own modal inputs: 308,285.83 kg × 0.405 × 3.667 = 457.8461 t. "
  "[log:certify.components] [log:_derived_values.gross_co2e_recalc_t]", "Certify Components"),
 ("9.2", "ACTIVITIES — Transport: process and embodied correct for all three legs", "Pass",
  "All six components recomputed from their modal inputs. Process (mass × full leg distance × per-tonne-mile factor): "
  "AECN→SOPOR 313.530 × 107.49722 × 0.0001143 = 3.8523 t vs 3.852; rail 313.530 × 2,199 × 0.0000259104 = 17.864 t vs 17.864; "
  "Opelousas→Basco 313.02837512 × 42.9 × 0.0001143 = 1.5349 t vs 1.535 — this leg is based on the downstream scale-ticket "
  "mass, not the BOL aggregate. Embodied (allocated distance × per-mile factor): "
  "AECN→SOPOR 1,287.514724 × 0.0002375605888 = 0.3059 t vs 0.306; rail 8,779.053888 × 0.00003113066508 = 0.2733 t vs 0.273; "
  "Opelousas→Basco 1,372.8 × 0.0002375605888 = 0.3261 t vs 0.326. Transport process sum = 3.8523 + 17.864 + 1.5349 = 23.2512 t; "
  "transport embodied sum = 0.3059 + 0.2733 + 0.3261 = 0.9053 t; bio-oil transport total = 24.1565 t against the Certify "
  "subtotal of 24.156 t. [log:_derived_values.sopor_truck_process_recalc_t] "
  "[log:_derived_values.rail_process_recalc_t] [log:_derived_values.opel_truck_process_recalc_t] "
  "[log:_derived_values.sopor_truck_embodied_recalc_t] [log:_derived_values.rail_embodied_recalc_t] "
  "[log:_derived_values.opel_truck_embodied_recalc_t] [log:_derived_values.transport_process_sum_t] "
  "[log:_derived_values.transport_embodied_sum_t] [log:_derived_values.transport_total_t] "
  "[log:certify.uncertainty_modals_read]", "Certify Components"),
 ("9.3", "ACTIVITIES — Injection: LCS and sample transport", "N/A",
  "AECN needs no LCS pre-treatment, and this entry carries no LCS or sample-transport component — the 10 components are the "
  "sequestration, the BCU adjustment, two pyrolysis and six transport. Site-level emissions sit on the separate scapegoat "
  "removal, outside this entry. [log:certify.components] [log:certify.component_count]", "Certify Components"),
 ("9.4", "ACTIVITIES — Pyrolysis: process and embodied entries present", "Pass",
  "Both present under the rail naming convention that signals scale-ticket mass to the verifier: 'AECN pyrolysis (from rail "
  "loads) - process emissions' 32.607 t and '... - embodied emissions' 6.634 t. Recomputed 313.530 × 0.104 = 32.6071 t and "
  "313.530 × 0.02116 = 6.6343 t. The factor-precision point is at 6.4. [log:certify.components] "
  "[log:_derived_values.pyro_process_recalc_t] [log:_derived_values.pyro_embodied_recalc_t]", "Certify Components"),
 ("9.5", "REDUCTIONS — applicable BCU categories populated", "Pass",
  "One category applies to an AECN entry carrying no site-emission burden, and it is populated: 'BCU - Transport Process' "
  "23.253 t under Adjustments. Its source certificate was opened — a TERC Certificate of Retirement, 2,795 TERCs retired by "
  "Amazon.com Services LLC on behalf of Charm Industrial on 18 Dec 2025, commodity Renewable Diesel, verified by Turner, Mason "
  "& Company, certificate TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000, each TERC one tCO2e. The 23.253 t drawn against it "
  "here sits well inside the 2,795 t retired, though that pool is shared across removals and its drawdown ledger (the BCU Quant "
  "sheet) is a reporting-period artifact not examined for this batch. The eligibility criteria EC1–EC5 in Transportation "
  "Emissions Accounting v1.1 §4.1 were read in full and contain no vintage-matching requirement, so the 2024 vintage raises no "
  "criterion under this module. "
  "[log:bcu_certificate] [log:protocol.ec_vintage_absence] [log:_derived_values.bcu_headroom_t]", "Certify Components"),
 ("9.6", "REDUCTIONS — BCU quantity at least the corresponding activity emission", "Pass",
  "BCU 23.253 t against a transport process sum of 3.8523 (AECN→SOPOR truck) + 17.864 (SOPOR→Opelousas rail) + 1.5349 "
  "(Opelousas→Basco truck, on the downstream scale-ticket mass) = 23.2512 t, against a BCU constant of exactly 23,253 kgCO2e. "
  "The BCU exceeds the process sum by 0.0018 t, so the legs are fully covered with a small surplus. The 0.9053 t of "
  "transport embodied emissions is not offset and remains in activities. [log:_derived_values.transport_process_sum_t] "
  "[log:_derived_values.bcu_constant_t] [log:_derived_values.bcu_surplus_over_process_t] "
  "[log:_derived_values.transport_embodied_sum_t] [log:certify.components]", "Certify Components / Calculation View"),
 ("9.7", "COUNTERFACTUALS", "Pass",
  "No counterfactual component exists on the entry — the Calculation View resolves net from sequestrations, adjustments, "
  "activities and the uncertainty discount only, and the component tree holds 10 components none of which is a counterfactual. "
  "[log:certify.counterfactuals] [log:certify.calculation_view]", "Certify Components"),
 ("9.8", "Net removal matches internal calculation", "Pass",
  "457.846 + 23.253 − 63.398 − 2.526 = 415.175 t against the Certify net of 415.176 t; rebuilding activities from the ten "
  "recomputed components rather than the displayed subtotal gives 415.1751 t. Both sit 0.001 t under the displayed net because "
  "Certify sums at full precision. "
  "[log:_derived_values.net_recalc_t] [log:_derived_values.net_from_components_t] [log:_derived_values.certify_net_displayed_t]", "Certify Calculation View"),
 ("9.9", "All datapoints have descriptive source names", "Flag",
  "14 of the 16 datapoints are backed by descriptively named files. Two are not: the rail full-leg distance of 2,199 mi is "
  "evidenced by 'image (44).png' (a screenshot of the Watco email), and the pyrolysis process carbon intensity is partly backed "
  "by 'Screenshot 2026-02-23 at 11.29.10 AM.png'. Content is correct in both cases — the Watco email was opened and reads 'The "
  "total milage for this move was 2199' — so this is naming hygiene, not a reporting error. "
  "[log:routes.generic_filename_FLAG] [log:certify.sources_enumeration]", "Certify Datapoints"),
 ("9.10", "Required evidence attached and linked to the datapoints that depend on it", "Pass",
  "62 source rows on the Sources tab, re-read 2026-08-06. Every datapoint carries the evidence a verifier needs to reproduce it. "
  "The two mass datapoints and the new downstream scale-ticket mass each carry the 32 tickets, the 12 BOLs and the Ops Notes; "
  "Carbon Content carries the SGS certificate and the Ops Notes; the four emission factors carry their source sheets; the three "
  "full-leg distances carry their route evidence. The three derived distances — 'Aggregate Distance AECN to Sopor Quebec (truck)' "
  "1,287.51 mi, 'Allocated Distance Sopor Quebec to Opelousas (rail)' 8,779.05 mi and 'Allocated Distance Opelousas to B6 "
  "(truck)' 1,372.8 mi — now carry both their route image and the Ops Notes offload table that derives them, added as three new "
  "source rows since the first pass (59 → 62). The Ops Notes is linked to seven datapoints in total. The attachment gate passes "
  "with no gaps. [log:certify.recheck_2026-08-06] [log:certify.sources_findings] [log:certify.attachment_map] "
  "[log:certify.certify_sources_tab_total] [log:routes] [log:ef_live_source]", "Certify Sources"),
]

DERIVED = D


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
    for cw, w in [("A", 10), ("B", 46), ("C", 9), ("D", 132), ("E", 26)]:
        ws.column_dimensions[cw].width = w
    ws.freeze_panes = "A2"

    # ---- Sheet 2: mass chain per offload ----
    ws2 = wb.create_sheet("Mass Chain")
    ws2.append(["Railcar", "Offload", "Full tkt (lb)", "Filed empty tkt (lb)", "Empty basis used (lb)",
                "Basis of empty weight", "Net from filed tickets (kg)", "Net as claimed (kg)",
                "Difference (kg)", "Full tkt tractor/trailer", "Empty tkt tractor/trailer", "Rig match"])
    for c in ws2[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    for key, v in SR["scale_tickets"]["per_offload"].items():
        rc, off = key.rsplit("_offload_", 1)
        substituted = v["ops_empty_lb"] == 29510
        basis = "KL192 standard (mean+1σ), rig mismatch" if substituted else "filed empty ticket"
        ws2.append([rc, int(off), v["ticket_full_lb"], v["ticket_empty_lb"], v["ops_empty_lb"], basis,
                    v["ticket_net_kg"], v["ops_net_kg"], round(v["ops_net_kg"] - v["ticket_net_kg"], 5),
                    v["full_tractor_trailer"], v["empty_tractor_trailer"],
                    "match" if v["vehicle_pair_match"] else "MISMATCH → substitution trigger"])
        i = ws2.max_row
        for col in range(1, 13):
            ws2.cell(i, col).border = BORDER; ws2.cell(i, col).alignment = WRAP
        if substituted:
            for col in range(1, 13):
                ws2.cell(i, col).fill = FLAG_FILL; ws2.cell(i, col).font = FLAG_FONT
    ws2.append([])
    ws2.append(["Per-railcar balance (as claimed)"])
    ws2[ws2.max_row][0].font = BOLD
    ws2.append(["Railcar", "BOL aggregate (kg)", "Offload sum as claimed (kg)", "Overdraws BOL?",
                "Back-calc applied (kg)", "Claimed mass (kg)", "Loss booked (kg)"])
    for c in ws2[ws2.max_row]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    for rc, v in SR["scale_tickets"]["per_railcar"].items():
        agg = v["bol_aggregate_kg"]; s = v["ops_net_sum_kg"]
        over = s > agg
        ws2.append([rc, agg, round(s, 5), "yes" if over else "no", v["ops_uncertainty_adj_kg"],
                    round(v["ops_claimed_kg"], 5), round(0 if over else agg - s, 5)])
        i = ws2.max_row
        for col in range(1, 8):
            ws2.cell(i, col).border = BORDER
    ws2.append([])
    ws2.append([f"Claimed total {D['ops_mass_used_kg']} kg. Raw filed-ticket math would give "
                f"{D['corrected_claimed_kg']} kg, so the KL192 standard-empty substitution on the three rig-mismatch offloads "
                f"claims {D['ops_underclaim_kg']} kg less mass = {D['underclaim_co2e_t']} tCO2e of credit forgone. That is the "
                f"intended direction of the method (mean + 1σ tare under-credits), not a defect."])
    for cw, w in [("A", 13), ("B", 18), ("C", 26), ("D", 20), ("E", 30), ("F", 24), ("G", 24),
                  ("H", 18), ("I", 16), ("J", 22), ("K", 24), ("L", 30)]:
        ws2.column_dimensions[cw].width = w

    # ---- Sheet 3: Certify reconciliation ----
    ws3 = wb.create_sheet("Certify Recon")
    ws3.append(["Component / datapoint", "Reconstructed from source (show the work)", "Certify", "Match"])
    for c in ws3[1]:
        c.font = BOLD; c.fill = HEADER_FILL; c.alignment = WRAP; c.border = BORDER
    MATRIX = [
     ("Bio-Oil Mass - AECN via Rail", "12 BOL Masse nette: 78,540 + 78,250 + 78,710 + 78,030 = 313,530 kg", "313,530 kg", "ties"),
     ("Mass of Injectant", f"312,924.893 - 4,036.73112 sparging - 602.33192 filtration = {D['mobi_recalc_kg']} kg", "308,285.83 kg", "ties"),
     ("Carbon Content", "SGS SR26-04220.001 carbon 40.5 % (m/m)", "40.50 %", "ties"),
     ("Injection sequestration", f"308,285.83 x 0.405 x 3.667 / 1000 = {D['gross_co2e_recalc_t']} t", "457.846 t", "ties"),
     ("Pyrolysis process", f"313.530 x 0.104 = {D['pyro_process_recalc_t']} t (sheet factor 0.1040167408 would give {D['pyro_process_at_sheet_ef_t']} t)", "32.607 t", "ties (factor rounded, see 6.4)"),
     ("Pyrolysis embodied", f"313.530 x 0.02116 = {D['pyro_embodied_recalc_t']} t", "6.634 t", "ties"),
     ("AECN->SOPOR truck PROCESS", f"313.530 x 107.49722 mi x 0.0001143 = {D['sopor_truck_process_recalc_t']} t", "3.852 t", "ties"),
     ("SOPOR->Opelousas rail PROCESS", f"313.530 x 2199 mi x 0.0000259104 = {D['rail_process_recalc_t']} t", "17.864 t", "ties"),
     ("Bio-Oil Mass (downstream, scale tickets)", f"Ops 'Deliveries raw / Downstream Transport (scale tickets)' = {D['downstream_mass_kg']} kg", "313.028 t", "new datapoint 2026-08-06"),
     ("Opelousas->Basco truck PROCESS", f"313.02837512 x 42.9 mi x 0.0001143 = {D['opel_truck_process_recalc_t']} t (downstream mass basis)", "1.535 t", "ties"),
     ("AECN->SOPOR truck EMBODIED", f"1,287.514724 mi x 0.0002375605888 = {D['sopor_truck_embodied_recalc_t']} t", "0.306 t", "ties"),
     ("SOPOR->Opelousas rail EMBODIED", f"8,779.053888 mi x 0.00003113066508 = {D['rail_embodied_recalc_t']} t", "0.273 t", "ties"),
     ("Opelousas->Basco truck EMBODIED", f"1,372.8 mi x 0.0002375605888 = {D['opel_truck_embodied_recalc_t']} t", "0.326 t", "ties"),
     ("Transport process sum / BCU", f"3.8523 + 17.864 + 1.5349 = {D['transport_process_sum_t']} t", "BCU 23.253 t", f"BCU exceeds by {D['bcu_surplus_over_process_t']} t"),
     ("Transport embodied sum", f"0.3059 + 0.2733 + 0.3261 = {D['transport_embodied_sum_t']} t", "-", "not BCU-offset"),
     ("Bio-oil transport total", f"{D['transport_process_sum_t']} + {D['transport_embodied_sum_t']} = {D['transport_total_t']} t", "24.156 t", "ties"),
     ("Activities total", f"pyrolysis 39.2414 + transport {D['transport_total_t']} = {D['activities_recalc_t']} t", "63.398 t", "ties"),
     ("Uncertainty discount", f"carbon 0.4% of 40.5 + mass 16 x 72.57 kg propagated by Certify = {D['uncertainty_discount_pct_of_gross']}% of gross", "2.526 t", "present"),
     ("Net CO2e removed", f"457.846 + 23.253 - 63.398 - 2.526 = {D['net_recalc_t']} t", "415.176 t", "ties"),
     ("Allocated distance AECN->SOPOR", f"Ops offload table sum {D['ops_ee_sopor_mi']} mi (173 km = {D['km_to_mi_173km']} mi x 3 trucks x mass share)", "1,287.51 mi", "ties"),
     ("Allocated distance rail", f"Ops offload table sum {D['ops_ee_rail_mi']} mi (2199 mi x mass share per railcar)", "8,779.05 mi", "ties"),
     ("Allocated distance Opelousas->Basco", f"42.9 x 2 round trip x 16 offloads = {D['opel_roundtrip_mi_check']} mi", "1,372.8 mi", "ties"),
     ("Standard-empty substitution", f"KL192 standard 29,321 mean + 189 sigma = {D['kl192_mean_plus_sigma_lb']} lb applied on the {D['n_offloads_triggering_substitution']} rig-mismatch offloads; claims {D['ops_underclaim_kg']} kg less than filed-ticket math", f"{D['underclaim_co2e_t']} t credit forgone", "per VVB guidance, conservative"),
     ("Evidence attachment (re-read 2026-08-06)", "Ops Notes now linked to 7 datapoints incl. all three allocated/aggregate distances; sources 59 -> 62", "attachment gate passes", "9.10 resolved"),
    ]
    for m in MATRIX:
        ws3.append(list(m)); r = ws3.max_row
        for col in range(1, 5):
            ws3.cell(r, col).alignment = WRAP; ws3.cell(r, col).border = BORDER
        if "FAIL" in str(m[-1]):
            for col in range(1, 5):
                ws3.cell(r, col).fill = FAIL_FILL
    for cw, w in [("A", 36), ("B", 74), ("C", 34), ("D", 30)]:
        ws3.column_dimensions[cw].width = w
    return wb


if __name__ == "__main__":
    build_with_validation(
        rows=ROWS,
        source_reads_path=HERE / "batch_INJ-07-2026-W1_source_reads.json",
        out_path=HERE / "Batch_INJ-07-2026-W1_QA_Checklist.xlsx",
        build_workbook_fn=build_workbook,
        derived_values=DERIVED,
    )
    from collections import Counter
    tally = Counter(r[2] for r in ROWS if r[2] != "SECTION")
    print("tally:", dict(tally))
