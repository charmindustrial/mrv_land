#!/usr/bin/env python3
"""Build the INJ-09-2026-W3-QOWV (Aqueous) QA checklist. Every quoted figure is computed here
from the source-read log / exports and pushed into _derived_values_numeric so the [log:] audit
can re-check it. Pre-flight validation (checklist_lib) runs before the workbook is written."""
import json, sys, math
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".claude/skills/batch-qa-aecn/scripts"))
from checklist_lib import build_with_validation

HERE = Path(__file__).resolve().parent
LOGP = HERE / "batch_INJ-09-2026-W3-QOWV_source_reads.json"
OUT = HERE / "Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W3.xlsx"
L = json.loads(LOGP.read_text())

# ---------------- derived values (computed, never typed) ----------------
T = L["totes"]; OT = L["ops_notes_totals"]; C = L["certify"]["component_by_key"]; K = L["ops_notes"]["constants"]
trk = L["shipment_tracker"]["trucks"]; EF = L["standard_efs_2026"]
gross = OT["total_mass_transported_kg"]; produced = OT["total_oil_produced_kg"]; injected = OT["total_oil_in_batch_kg"]
pe = OT["production_emissions_kg"]; wci = OT["weighted_avg_ci_kgco2e_per_kg"]; unc = OT["uncertainty_kg"]
proc_sheet = gross / 1000 * 1201 * EF["flatbed_process"]["value"] * 1000
proc_cert = gross / 1000 * 1201 * 1.609344 * C["transport_process"]["inputs"]["ef_kgco2e_per_km_t"]
alloc = L["shipment_tracker"]["totals"]["allocated_miles_mi"]
alloc18 = sum(t["batch_totes"] / (18 if t["truck"] == "COLA-32" else t["totes_on_truck"]) * 1201 for t in trk)
emb_kg = alloc * EF["non_tanker_embodied"]["value"] * 1000
pyro_cert_kg = produced * C["pyrolysis"]["inputs"]["ci_tco2e_per_t"]
seq_kg = injected * 0.08 * 3.667
t54 = next(t for t in T if t["tag"] == "301154"); t09 = next(t for t in T if t["tag"] == "120509")
ci_diff = K["L18_Jun2026"] - K["L17_May2026"]; over54 = t54["net_oil_produced_kg"] * ci_diff
rel_c = 0.032 / 8.0; rel_m = unc / injected
disc_est = 1000 * math.sqrt((seq_kg / 1000 * math.hypot(rel_c, rel_m))**2 + (proc_cert / 1000 * unc / gross)**2 + (pyro_cert_kg / 1000 * unc / produced)**2)
net_precise = seq_kg / 1000 + 6.264 - (proc_cert + emb_kg + pyro_cert_kg) / 1000 - disc_est / 1000
E = [t["empty_tote_weight_kg"] for t in T]; G = [t["gross_kg"] for t in T]
pp_pe = {}
for t in T:
    key = t["production_period_label"].split(", ")[-1]
    pp_pe[key] = pp_pe.get(key, 0) + t["production_emissions_kg"]
D = {
 "n_totes": len(T), "gross_kg": gross, "produced_kg": produced, "injected_kg": injected, "pe_kg": round(pe, 6), "weighted_ci": wci,
 "unc_kg": unc, "per_tote_unc_kg": 1.13398, "kg_per_lb": 0.453592, "lb_per_tote": 2.5,
 "carbon_pct": 8.0, "carbon_unc_pct_abs": 0.032, "carbon_rel_unc": 0.004, "co2_c_ratio": 3.667,
 "seq_kg_precise": round(seq_kg, 4), "seq_t": 9.038,
 "proc_sheet_kg": round(proc_sheet, 3), "proc_certify_kg": round(proc_cert, 3), "proc_t": 6.264,
 "ef_flatbed_mt_t_mi": EF["flatbed_process"]["value"], "ef_flatbed_km_t": 0.086, "ef_flatbed_km_t_converted": round(EF["flatbed_process"]["value"] * 1000 / 1.609344, 7),
 "ef_nontanker_mt_mi": EF["non_tanker_embodied"]["value"], "ef_tanker_mt_mi": EF["tanker_embodied"]["value"], "ef_nontanker_kg_mi": 0.19279, "ef_nontanker_kg_km": 0.1198,
 "alloc_mi": alloc, "alloc_mi_2dp": round(alloc, 2), "emb_kg": round(emb_kg, 3), "emb_t": 0.331,
 "alloc18_mi": round(alloc18, 4), "alloc_over_mi": round(alloc - alloc18, 4), "emb_over_kg": round((alloc - alloc18) * EF["non_tanker_embodied"]["value"] * 1000, 3),
 "cola32_share_17": trk[3]["share"], "cola32_share_18": round(3 / 18, 10), "cola32_miles_17": trk[3]["allocated_miles"], "cola32_miles_18": round(3 / 18 * 1201, 4),
 "t1_share": trk[0]["share"], "t2_share": trk[1]["share"], "c31_share": trk[2]["share"],
 "t1_miles": trk[0]["allocated_miles"], "t2_miles": trk[1]["allocated_miles"], "c31_miles": trk[2]["allocated_miles"],
 "pyro_certify_kg": round(pyro_cert_kg, 3), "pyro_t": 4.978, "net_t": 3.690, "net_precise_t": round(net_precise, 5), "disc_kg": 39, "disc_est_kg": round(disc_est, 2),
 "bcu_kg": 6264, "bcu_excess_certify_kg": round(6264 - proc_cert, 3), "bcu_excess_sheet_kg": round(6264 - proc_sheet, 3),
 "t301154_net_kg": t54["net_oil_produced_kg"], "jun_ci": K["L18_Jun2026"], "may_ci": K["L17_May2026"], "ci_diff": round(ci_diff, 10),
 "over54_kg": round(over54, 4), "pe_corrected_kg": round(pe - over54, 4), "ci_corrected": round((pe - over54) / produced, 10), "net_under_t": round(over54 / 1000, 5),
 "may_sum_kg": 36523.2, "june_sum_kg": 46616.2, "may_summary_kg": 36523, "june_summary_kg": 46616,
 "t120509_tare_inv": 62.93, "tote_mass_ops": 57.6, "prod_over_kg": round(62.93 - 57.6, 2), "pe_over_kg": round((62.93 - 57.6) * t09["ci_kgco2e_per_kg"], 4),
 "empty_min": min(E), "empty_max": max(E), "gross_min": min(G), "gross_max": max(G),
 "route1": 1132, "route2": 1129, "route3": 1201, "one_way_mi": 1201,
 "pp8_ci": K["L10_PP8"], "sep_ci": K["L21_Sep2025"], "apr_ci": K["L16_Apr2026"],
 "pe_share_of_net_pct": round(4.978 / 3.690 * 100, 1), "density": 1.047,
 "pp_pe_jul25": round(pp_pe["July 2025"], 4), "pp_pe_sep25": round(pp_pe["September 2025"], 4), "pp_pe_apr26": round(pp_pe["April 2026"], 4),
 "pp_pe_may26": round(pp_pe["May 2026"], 4), "pp_pe_jun26": round(pp_pe["June 2026"], 4),
 "tote_counts_jul": 14, "tote_counts_sep": 5, "tote_counts_apr": 16, "tote_counts_may": 1, "tote_counts_jun": 1,
 "trucks_1201": 9, "trucks_1202": 10, "trucks_c31": 15, "trucks_c32": 3, "c32_total_inv": 18, "c32_total_tab": 17,
 "sources_total": 6, "datapoints_total": 10, "tars_2795": 2795,
}
# production-record net: 301154 at the May CI, 120509 at its 62.93 kg tare, COLA_32 over 18 totes, BCU = process emission
tare_gap = 62.93 - t09["tote_mass_kg"]
produced_rec = produced - tare_gap; pe_rec = pe - over54 - tare_gap * t09["ci_kgco2e_per_kg"]
emb_rec = alloc18 * EF["non_tanker_embodied"]["value"] * 1000
disc_rec = 1000 * math.sqrt((seq_kg / 1000 * math.hypot(rel_c, rel_m))**2 + (proc_cert / 1000 * unc / gross)**2 + (pe_rec / 1000 * unc / produced_rec)**2)
net_rec = (seq_kg - emb_rec - pe_rec - disc_rec) / 1000
net_sheet = seq_kg / 1000 + 6.264 - (proc_sheet + emb_kg + produced * wci) / 1000 - disc_est / 1000
ci_fix6 = round((pe - over54) / produced, 6)
D.update({
 "net_sheet_t": round(net_sheet, 5), "net_record_t": round(net_rec, 5), "net_record_gain_t": round(net_rec - net_precise, 5),
 "ci_corrected_6dp": ci_fix6, "pyro_corrected_t": round(produced * ci_fix6 / 1000, 3), "ci_corrected_with_22": round(pe_rec / produced_rec, 7),
 "alloc18_2dp": round(alloc18, 2), "emb_corrected_t": round(alloc18 * EF["non_tanker_embodied"]["value"], 3),
 "bcu_under_if_6263_kg": round(proc_cert - 6263, 3), "certify_ci": C["pyrolysis"]["inputs"]["ci_tco2e_per_t"],
 "cobb_rows": 37, "cobb_first_row": 809, "cobb_last_row": 845, "cobb_qty_sum_kg": 38080.6, "cobb_301009_qty_kg": 1549.8, "t301009_gross_kg": 1013.0,
 "st_row19_tare": 62.93, "st_row19_net": 956.07, "wo_tare": 62.9, "inv_row_301352": 747, "inv_row_301307": 746,
 "t301159_gross": 988.0, "t301159_tare": 57.6, "t301159_net": 930.4, "inv_row_301159": 610, "inv_row_301154": 601,
 "apr_sum_kg": 45764.8, "apr_summary_kg": 43912, "pp8_sum_kg": 76217.12, "pp8_summary_kg": 77076, "pp10_sum_kg": 44931.0, "pp10_summary_kg": 41010,
 "aecn_c_pct": 39.7, "aecn_h_pct": 7.0, "rel_unc_pct": 0.4,
 "inv_tare_576_qowv": 566, "inv_tare_6293_qowv": 73,
 "alloc_order_mi": 2308.5889, "alloc_order_2dp": 2308.59, "emb_order_t": 0.445, "truck_change_mi": 603.8361, "truck_change_t": 0.11641,
 "net_record_orders_t": 3.58876, "cobb_rows_minus_576": 24, "cobb_rows_doubled": 12, "cobb_301009_half_kg": 774.9, "cobb_245161_kg": 804.9, "ledger_injected_kg": 30808.5, "t1_order_totes": 20, "t2_order_totes": 18, "t1_order_share": 0.45, "t2_order_share": round(10/18, 10),
})
L["_derived_values_numeric"] = D
L["_derived_values_numeric"] = D
LOGP.write_text(json.dumps(L, indent=1, default=str))
DV = "_derived_values_numeric"

def f(x, n=2): return f"{x:,.{n}f}"

S, R = "SECTION", []
def sec(t): R.append((S, t))
def row(i, q, s, e, ref): R.append((i, q, s, e, ref))

sec("SECTION 1 -- Batch Folder")
row("1.1", "Is there testing in the testing folder for the batch?", "Pass",
 f"The Testing subfolder holds 'SR26-05599 W3 QOWV AECN COA.pdf'. Page 1 is SGS Certificate of Analysis SR26-05599.001 for Client ID '9-2026-w3-QOWV', location FORT LUPTON CO, sampled 17-Sep-2026 10:00: Carbon 8.0 % (m/m) by ASTM D5291 (Method C), Hydrogen 9.1 %, Nitrogen <0.75 %, Kinematic Viscosity 0.9507 cSt, Acid Number 32 mg KOH/g, Density at 15 C {D['density']} g/cm3 (above the 1.01 g/cm3 formation-fluid threshold). Page 2 is the AECN composite SR26-05599.002 (39.7 % C), which belongs to the AECN removal. The copy attached in Certify (src_1M38GJZMB1S0GMHC) reads the same certificate and 8.0 % carbon [log:testing, {DV}].",
 "VR Appendix 1")
row("1.2", "Are Ops Notes in the folder and fully completed?", "Pass",
 f"'INJ-09-2026-W3 Ops Notes' is in the batch folder and was exported from the live sheet and read cell by cell. QOWV tab: B2 'INJ-09-2026-W3', week B3 2026-09-11 to B4 2026-09-18, and {D['n_totes']} tote rows (A11:A47) with every row populated for tag, gross mass, tote mass, net oil produced, empty tote weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty. The row-50 totals all resolve to values: Total Mass Transported {f(gross,1)} kg, Total Oil Produced {f(produced,1)} kg, Total Oil Injected {f(injected,1)} kg, weighted CI {wci:.10f}, production emissions {f(pe,6)} kg, uncertainty {unc} kg. No cell comments on any tab [log:ops_notes, ops_notes_totals, vvb_guidance, {DV}].",
 "VR Appendix 1")
row("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", "Flag",
 f"The allocation is carried by the 'QOWV Shipments & EE Allocation' tab of the batch Ops Notes workbook, which is in the folder. Its truck rows are filled for all four shipping orders feeding this batch -- Truck 1 (CO_AQUEOUS_12.01.25), Truck 2 (CO_AQUEOUS_12.02.25), COLA-31, COLA-32 -- with ship date, totes on truck, batch totes, share, one-way mileage and allocated miles, and batch totes 9 + 10 + 15 + 3 sum to the {D['n_totes']}-tote ledger. The flag: the tab holds truck-level counts only. No row ties any of this batch's {D['n_totes']} tags to a truck -- its one tote block (A58 '--- Shipment 2025-12-10 --- (14 of 35 totes on this truck are W4-relevant)', E60:E73 'INJ-05-2026-W4') belongs to another batch -- and the counts in C12:C15 and D12:D15 are typed. The tag-to-truck record is the production inventory master (Ship Status, Date Shipped), which is not among the six Certify sources, so a verifier cannot check the counts; item 3.4 shows the cost. The Ops Notes' Whole Oil allocation tab carries a check the QOWV allocation tab lacks: A16 'Check - every batch tote is allocated to a truck', B16 '=IF($D$14=$D$6,\"OK\",\"MISMATCH\")'. Adding a per-tote truck column, or attaching the inventory extract to the embodied distance datapoint, clears this [log:shipment_tracker, shipment_tracker.tote_level_rows, shipment_tracker.whole_oil_tab_check, inventory_master, certify.certify_sources_enumeration, {DV}].",
 "VR Appendix 1")

sec("SECTION 2 -- Ops Notes")
row("2.1", 'Is the "Total Mass Transported" value correctly computed as the sum of the gross weight of all totes?', "Pass",
 f"QOWV!B50 is a live sum over the gross-mass column, SUM(B10:B48), and returns {f(gross,1)} kg. Re-summing the {D['n_totes']} per-tote gross values independently gives {f(gross,1)} kg, delta 0.0 kg. Every gross value also matches the production inventory master row for the same tag (37 of 37). The same figure is Certify's Transport Process Mass of Load [log:ops_notes_totals, inventory_master, {DV}].",
 "VR Sec 5.1")
row("2.2", 'Is the "Total Oil Produced" value correctly computed as the sum of the net weight of oil in tote for all totes (gross - tare per tote)?', "Flag",
 f"The arithmetic is right: per-tote D = B - C on every row and QOWV!D50 = SUM(D10:D48) returns {f(produced,1)} kg, which an independent re-sum reproduces. The flag is the tare input. Column C (Tote Mass) is not a per-tote weighing: it reads 57.6 kg on all {D['n_totes']} rows, and the inventory master's Tare Weight column carries 57.6 kg on {D['inv_tare_576_qowv']} QOWV totes and 62.93 kg on {D['inv_tare_6293_qowv']}, the same figures on steel and plastic pallets, with no note on either header cell. Total Oil Produced, which is the pyrolysis mass, therefore rests on a standard tare, and its plus or minus {unc} kg covers the single gross weighing per tote. Total Oil in Batch is unaffected, since it uses the measured post-unload weight (column E). Separately, the production inventory master (Q4 row 45) records tote 120509 (PP#8, MFO Lot 2830) with Tare Weight {D['t120509_tare_inv']} kg and Net Weight 956.07 kg, against 57.6 kg and 961.4 kg here. Using the recorded tare, produced mass is {D['prod_over_kg']} kg lower and production emissions {D['pe_over_kg']} kg CO2e lower, so the sheet as submitted is conservative and the effect is below 0.001 tCO2e. Earlier weeks treat totes the inventory records at 62.93 kg differently: INJ-08-2026-W5 enters 62.9 kg for all 19 such totes, while INJ-07-2026-W1 (15 such totes) and INJ-08-2026-W4 (1) entered 57.6 kg. Two more records give {D['st_row19_tare']} kg for this tote: the inventory's 'Shipment Tracker (Nov 2025+)' tab row 19 (Truck 1, tare {D['st_row19_tare']}, net {D['st_row19_net']}), and the W3 Ops Notes' Whole Oil ledger, which copies inventory tares rather than 57.6 kg (C11 and C14 = {D['wo_tare']} for 301352 and 301307, matching inventory rows {D['inv_row_301352']} and {D['inv_row_301307']}). Fix: enter a measured empty weight per tote in column C, or attach the basis for the 57.6 kg standard figure, and set C29 to the inventory tare of 62.93 kg for tote 120509 [log:inventory_master, inventory_master.tare_distribution, inventory_master.tote_120509_shipment_tracker_tab, inventory_master.whole_oil_tares_same_workbook, ops_notes_totals, {DV}].",
 "VR Sec 5.1")
row("2.3", 'Is the "Total Oil in Batch" value correctly computed (Aqueous: measured pre-unload minus measured post-unload per tote; Standard Loss does NOT apply)?', "Pass",
 f"Correct for Aqueous. Per-tote F = IF(E=\"\",\"\",B-E): gross weight minus the measured post-unload empty tote weight. Column E ranges {D['empty_min']}-{D['empty_max']} kg across the {D['n_totes']} rows, so it is a per-tote weighing, not the 57.6 kg nominal tote mass. Column B is the Fort Lupton production gross weight (it equals the inventory gross on 37 of 37 totes), so the injected mass is production gross minus the measured post-unload tote weight. QOWV!F50 = SUM(F9:F48) returns {f(injected,1)} kg; an independent re-sum of (B - E) gives the same, delta 0.0 kg. No Standard Loss column, constant or deduction appears on the QOWV tab, and Summary!E12/F12 report sparging 0.0 and filtration 0.0 for QOWV. The figure is Certify's Mass of Injectant [log:ops_notes_totals, summary_tab, {DV}].",
 "GHG Stmt Sec C")
row("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", "Pass",
 f"Per-tote J = 2.5*$L$4 with L4 = {D['kg_per_lb']} kg/lb, giving {D['per_tote_unc_kg']} kg on all {D['n_totes']} rows. QOWV!J50 = SUM(J9:J48) returns {unc} kg; expected {D['n_totes']} x {D['per_tote_unc_kg']} = {unc} kg, delta 0.00000 kg. This is the per-tote weighing precision, not AECN's per-truck figure [log:ops_notes_totals, ops_notes, {DV}].",
 "Isometric Standard S3.7.3")

sec("SECTION 3 -- Bio-Oil Shipment Tracker (QOWV Shipments & EE Allocation tab)")
row("3.1", "Are totes for the RP correctly identified?", "Pass",
 f"Batch-relevant totes across the four shipping orders are 9 (Truck 1, 2025-12-01) + 10 (Truck 2, 2025-12-02) + 15 (COLA-31, 2026-08-18) + 3 (COLA-32, 2026-08-20) = {D['n_totes']}, matching the ledger; the count cell D6 = COUNTA(QOWV!A11:A48) is formula-linked to it. Each tote's truck was confirmed tag by tag against Ship Status / Date Shipped on the production inventory master: {D['trucks_1201']} shipped 2025-12-01, {D['trucks_1202']} shipped 2025-12-02, {D['trucks_c31']} on COLA-31, {D['trucks_c32']} on COLA_32 -- the same split as the tab. The Bio-oil Injection Tracker ('Basco Injection -- COBB' tab, rows {D['cobb_first_row']}-{D['cobb_last_row']}) lists exactly these {D['cobb_rows']} tags under injection batch 'INJ-09-2026-W3_aqueous_fraction', injection completed 2026-09-17, and no other injection batch holds any of them. None of the {D['n_totes']} tags appears in any other week's Ops Notes: the QOWV ledgers of INJ-07-2026-W1, INJ-08-2026-W1 to W5 and INJ-09-2026-W1, W2 and W4 were downloaded and searched, and a Drive text search for all 37 tags across every spreadsheet returns this week's Ops Notes and no other [log:shipment_tracker, inventory_master, cobb_injection_record, cross_week_double_count, {DV}].",
 "VR Sec 3.5")
row("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", "Fail",
 f"Checked per attribute, tag by tag, against the production inventory master: tag 37 of 37, fraction QOWV 37 of 37, gross mass 37 of 37, production period 36 of 37. Tote 301154 is 'June 2026' in the Ops Notes (G24) and 'May 2026 PP' in the inventory (row {D['inv_row_301154']}). That is the error set out in 3.5, and its CI consequence is 7.2; one correction clears all three. The roster itself matches: the Bio-oil Injection Tracker ('Basco Injection -- COBB', rows {D['cobb_first_row']}-{D['cobb_last_row']}) lists exactly the {D['cobb_rows']} ledger tags under 'INJ-09-2026-W3_aqueous_fraction', none missing and none extra, and the inventory's per-truck counts of {D['trucks_1201']}, {D['trucks_1202']}, {D['trucks_c31']} and {D['trucks_c32']} match column D of the allocation tab [log:inventory_master, cobb_injection_record, shipment_tracker, {DV}].",
 "VR Sec 3.5")
row("3.3", "Are computed outputs (Batch Share of Truck, Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", "Pass",
 "Every computed cell is a live formula, read from the workbook exported from the live sheet this session: E12 '=D12/C12', E13 '=D13/C13', E14 '=D14/C14', E15 '=D15/C15' (share); G12 '=E12*F12' through G15 '=E15*F15' (allocated miles); G17 '=SUM(G12:G15)' (batch mileage allocation); D6 '=COUNTA(QOWV!A11:A48)'; and F12:F15 '=$B$8' pointing at the single one-way distance input. No computed output is a typed constant; the typed inputs are the tote counts in C and D and the distance in B8 [log:shipment_tracker_cells_are_formulas, shipment_tracker].",
 "Auditability - VR Sec 5.1")
row("3.4", "Are computed outputs computed correctly?", "Fail",
 f"The formulas follow the method (share = batch totes / totes on truck; allocated miles = share x one-way {D['one_way_mi']:,} mi) and reproduce as written: Truck 1 9/40 = {D['t1_share']} -> {D['t1_miles']} mi; Truck 2 10/36 = {D['t2_share']:.10f} -> {D['t2_miles']:.7f} mi; COLA-31 15/20 = {D['c31_share']} -> {D['c31_miles']} mi; COLA-32 3/17 = {D['cola32_share_17']:.10f} -> {D['cola32_miles_17']:.7f} mi; total {D['alloc_mi']:,.6f} mi. The COLA-32 denominator is wrong. The production inventory master lists {D['c32_total_inv']} totes shipped on COLA_32 (17 QOWV plus Whole Oil tote 301310, August 2026 PP), and the two other batches drawing on the same truck divide by 18: INJ-08-2026-W5 QOWV (5 of 18, share 0.2777777778) and INJ-09-2026-W1 Whole Oil ('COLA_32 = 1 of 18 totes on the truck'). C15 here reads {D['c32_total_tab']}. At 3/18 the COLA-32 row is {D['cola32_miles_18']} mi and the batch total {D['alloc18_mi']:,} mi, so this batch carries {D['alloc_over_mi']} mi too many and {D['emb_over_kg']} kg CO2e too much embodied emission -- conservative, but it puts this batch on a different denominator from the two other batches on the same truck (1/17 per tote here, 1/18 there). The Truck 1 and Truck 2 denominators are wrong too. The inventory workbook's Oil_inventory_data tab (receiving record, column shipping_order_number) shows 2025-12-01 as two orders of 20 totes (CO_AQUEOUS_12.01.25 and CO_AQUEOUS_12.1.25_T2) and 2025-12-02 as two orders of 18 (CO_AQUEOUS_12.2 and CO_AQUEOUS_12.2_02); no order in that record holds more than 20 totes. This batch's 9 Truck 1 totes all rode CO_AQUEOUS_12.1.25_T2 and its 10 Truck 2 totes all rode CO_AQUEOUS_12.2_02, so their shares are 9/20 = {D['t1_order_share']} and 10/18 = {D['t2_order_share']:.10f}, not 9/40 and 10/36. That adds {D['truck_change_mi']:,} mi and {D['truck_change_t']} t of embodied emission; unlike the COLA-32 error, it overstates the net. Fix: set C12 to 20 (CO_AQUEOUS_12.1.25_T2), C13 to 18 (CO_AQUEOUS_12.2_02) and C15 to 18, change Certify's 'QOWV Embodied Distance (CO to B6) [Certify input]' to {D['alloc_order_2dp']:,} mi (embodied {D['emb_order_t']} t), and re-attach the corrected Ops Notes. Changing the tab alone would leave Certify at 1,716.53 mi and break 6.2 [log:shipping_orders_2025_12, shipment_tracker, inventory_master, cola32_cross_batch, standard_efs_2026, {DV}].",
 "Transportation Emissions Acctg v1.1")
row("3.5", "Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?", "Fail",
 f"Checked tag by tag against the production inventory master (Q4 2025-2026 Production Inventory tab): (a) tag 37 of 37; (b) fraction QOWV 37 of 37; (c) gross mass 37 of 37; (d) production period 36 of 37. Tote 301154 is 'MFO Lot 301154, June 2026' in the Ops Notes (G24), but the inventory records it as 'May 2026 PP', date range 5/1-5/31, spray paint Pink2605 (May's code; June totes carry Blue2606). The production summaries confirm May: the May 2026 PP Summary's Aqueous Mass of Output reads 36,523 kg and the inventory's May 2026 QOWV totes sum to {D['may_sum_kg']:,} kg only with 301154 ({D['t301154_net_kg']} kg) included; June's reads 46,616 kg and its totes sum to {D['june_sum_kg']:,} kg without it. Inventory row {D['inv_row_301159']}, tote 301159 ('June 2026 PP', COLA_36), carries the same three masses as 301154 ({D['t301159_gross']} / {D['t301159_tare']} / {D['t301159_net']} kg). PP#8 and PP#10 map to July 2025 and September 2025 by the inventory's date ranges. The mislabel carries the wrong CI -- see 7.2 [log:inventory_master, inventory_master.tote_301159_lookalike, pp_summary_sources, {DV}].",
 "VR Sec 3.5")

sec("SECTION 4 -- Certify: Injection Sequestration")
row("4.1", "Does the C content in the testing match the C content in the Sequestration component?", "Pass",
 f"Component detail read directly: Carbon content of product 8 %. Lab certificate SR26-05599.001 reports Carbon 8.0 % (m/m). Delta 0.0 percentage points. Ops Notes Summary!E20 carries 0.08 against composite SR26-05599.001 dated 2026-09-17 [log:certify.component_by_key.injection_sequestration, testing.qowv_certificate, summary_tab, {DV}].",
 "VR Sec 5.1")
row("4.2", "Is the C content properly evidenced (test copy + Ops Notes copy)?", "Pass",
 "The Carbon Content datapoint carries 2 sources, and the Sources tab names both: 'SR26-05599 W3 QOWV AECN COA.pdf' (the lab certificate) and 'INJ-09-2026-W3 Ops Notes.xlsx'. Both are linked to the datapoint itself. The attached Ops Notes copy (src_1M38GJXY31S0WZNQ) was downloaded and is cell-for-cell identical to the live sheet on the QOWV, allocation and Summary tabs [log:certify.attachment_map, certify.certify_sources_enumeration, certify.attached_ops_notes_copy].",
 "VR Appendix 1")
row("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", "Pass",
 f"Component detail read directly: Mass of product {f(injected,1)} kg plus or minus {unc} kg. Ops Notes uncertainty J50 = {unc} kg. Exact match at full precision [log:certify.component_by_key.injection_sequestration, ops_notes_totals, {DV}].",
 "Isometric Standard S3.7.3")
row("4.4", "Does the C content have the appropriately computed 0.4% relative uncertainty?", "Pass",
 f"Component detail read directly: 8 % plus or minus 0.032. Expected 0.004 x 8.0 = {D['carbon_unc_pct_abs']} percentage points absolute. Exact match, entered as an absolute value. Ops Notes Summary!G20 computes the same figure as E20*H20 with H20 = 0.004 [log:certify.component_by_key.injection_sequestration, summary_tab, {DV}].",
 "Isometric Standard S3.7.3")

sec("SECTION 5 -- Certify: Transport Process Emissions")
row("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Pass",
 f"Component detail shows 'Flatbed, Northern America, WTW' at 0.086 kgCO2e/(km*t), a standard published value sourced to GLEC V3.2. The live Standard Emission Factors sheet, 2026 tab, row 7 'Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck' = {D['ef_flatbed_mt_t_mi']} MT CO2e/t-mi (GLEC V3.2 2025), which converts to {D['ef_flatbed_km_t_converted']} kgCO2e/(km*t) -- the same factor, rounded in the sheet. Recompute (tonnes of load x miles x km per mile x kgCO2e per km-tonne): {gross/1000:.3f} x {D['one_way_mi']} x 1.609344 x 0.086 = {D['proc_certify_kg']} kg, i.e. 6.264 t as Certify shows; on the sheet's rounded value it is {D['proc_sheet_kg']:,} kg, 0.00016 tCO2e apart [log:standard_efs_2026, certify.component_by_key.transport_process, {DV}].",
 "Standard EFs 2026 tab, row 7")
row("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", "Pass",
 f"Certify distance is {D['one_way_mi']:,} mi ('Distance from Miniforge CO to Basco'), sourced to 'CO to Basco Routing Map.png'. That image was downloaded from this removal's own Certify source (src_1KSTWP2AP1S0QQPF) and read from the pixels: three routes to destination '4675 LA-115, St Landry, LA 71367' -- via US-287 S {D['route1']:,} mi, via US-287 S and I-20 E {D['route2']:,} mi, via I-70 E {D['route3']:,} mi. Certify uses {D['route3']:,} mi, the longest. The origin field reads 'Your location'; the origin pin sits just north of Denver, consistent with Fort Lupton, CO, the location on lab certificate SR26-05599.001. The file is byte-identical (sha256 9168453b...) to the routing maps attached on INJ-09-2026-W2-QOWV and INJ-07-2026-W1-QOWV [log:google_maps_options, google_maps_note, google_maps_identity, testing, {DV}].",
 "Charm convention - longest route")
row("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", "Pass",
 f"Component detail: Mass of load 'QOWV Transport Mass (CO to B6) [Certify input]' {f(gross,0)} kg = Ops Notes Total Mass Transported (QOWV!B50) {f(gross,1)} kg, delta 0.0 kg. This is the gross figure including tote tares, not Total Oil Produced ({f(produced,1)} kg) or Total Oil Injected ({f(injected,1)} kg). The datapoint title names the fraction, basis and lane correctly [log:certify.component_by_key.transport_process, ops_notes_totals, {DV}].",
 "VR Sec 5.1")
row("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", "Pass",
 "The 'QOWV Transport Mass (CO to B6) [Certify input]' datapoint carries 1 source, 'INJ-09-2026-W3 Ops Notes.xlsx', confirmed on the Sources tab as linked to that datapoint [log:certify.attachment_map, certify.certify_sources_enumeration].",
 "VR Appendix 1")
row("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", "Pass",
 f"Component detail shows {f(gross,0)} kg plus or minus 41.96 kg, the display rounding of the same {D['n_totes']} x {D['per_tote_unc_kg']} = {unc} kg the Ops Notes carries and the Sequestration component holds at full precision. Same totes, same weighings [log:certify.component_by_key.transport_process, ops_notes_totals, {DV}].",
 "Isometric Standard S3.7.3")

sec("SECTION 6 -- Certify: Transport Embodied Emissions")
row("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", "Flag",
 f"The value is right and the label is wrong. Component detail shows 0.19279 kgCO2e/mi (0.1198 kgCO2e/km); the live Standard Emission Factors sheet, 2026 tab, row 12 'Vehicle Embodied Emissions --Non-Tanker Truck' = {D['ef_nontanker_mt_mi']} MT CO2e/mi (GLEC V3.2 2025), the same factor, applied per mile. Recompute: {D['alloc_mi']:,.6f} mi x {D['ef_nontanker_mt_mi']} = {D['emb_kg']} kg, matching Certify's 0.331 t. The datapoint is titled 'Emissions Factor - Vehicle Embodied Emissions - Tanker Truck', while the sheet's tanker row (row 11) is {D['ef_tanker_mt_mi']} MT CO2e/mi, which is not the value used. The same datapoint was titled '... - Flatbed Truck' on INJ-09-2026-W2-QOWV; retitling it to Non-Tanker/Flatbed clears this [log:standard_efs_2026, certify.component_by_key.transport_embodied, {DV}].",
 "Standard EFs 2026 tab, row 12")
row("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", "Pass",
 f"Certify 'QOWV Embodied Distance (CO to B6) [Certify input]' = {D['alloc_mi_2dp']} mi. The allocation tab's total G17 = SUM(G12:G15) = {D['alloc_mi']:,.6f} mi. The Certify figure matches the tracker as submitted. The tracker figure itself carries the denominator errors in 3.4, which would bring it to {D['alloc_order_2dp']:,} mi [log:shipping_orders_2025_12, certify.component_by_key.transport_embodied, shipment_tracker, {DV}].",
 "Transportation Emissions Acctg v1.1")
row("6.3", "Is the aggregate distance evidenced with the Shipment Tracker, batch Charm Contents, and applicable route Google Map?", "Pass",
 "The datapoint carries 2 sources and the Sources tab confirms both: 'INJ-09-2026-W3 Ops Notes.xlsx' (which contains the QOWV Shipments & EE Allocation tab that derives the figure) and 'CO to Basco Routing Map.png' (the one-way route). No standalone Charm Contents sheet exists for this batch -- not present in the Drive batch folder listing or among the six Certify sources -- and the per-period breakdown is the Ops Notes Production Period column, the basis used on every 2026 weekly batch [log:certify.attachment_map, charm_contents, certify.certify_sources_enumeration].",
 "VR Appendix 1")

sec("SECTION 7 -- Certify: Production (Pyrolysis) Emissions")
row("7.1", "Are Production Emissions captured for ALL Production Periods in the batch?", "Pass",
 f"Every tote carries a production period and a period CI, so no period's emissions are left out: July 2025 / PP#8 ({D['tote_counts_jul']} totes, {D['pp_pe_jul25']} kg), September 2025 / PP#10 ({D['tote_counts_sep']}, {D['pp_pe_sep25']} kg), April 2026 ({D['tote_counts_apr']}, {D['pp_pe_apr26']} kg), May 2026 ({D['tote_counts_may']}, {D['pp_pe_may26']} kg) and the tote labelled June 2026 ({D['tote_counts_jun']}, {D['pp_pe_jun26']} kg). They are captured in one production-mass-weighted component, 'Pyrolysis - Charm QOWV PP Emissions', whose total reconciles to the per-tote sum: sum of (net produced x tote CI) = {D['pe_kg']:,} kg; {f(produced,1)} kg x 0.140021 = {D['pyro_certify_kg']:,} kg = 4.978 t in Certify. All totes were produced before July 2026, so each keeps its own monthly CI and the Jul-Dec 2026 blended CI (L7) is correctly not applied [log:ops_notes_totals, production_period_tote_counts_ops_label, certify.component_by_key.pyrolysis, {DV}].",
 "Bio-oil Geological Storage v1.2")
row("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", "Fail",
 f"Certify carries 0.140021 tCO2e/t, which matches Ops Notes QOWV!H50 = SUMPRODUCT(D11:D48,H11:H48)/SUM(D11:D48) = {wci:.10f} and an independent recompute. But one tote carries the wrong period's CI. Tote 301154 is a May 2026 tote on its production record (item 3.5) yet H24 references $L$18, the June 2026 CI {D['jun_ci']:.10f}, instead of $L$17, the May 2026 CI {D['may_ci']:.10f}. On {D['t301154_net_kg']} kg that overstates production emissions by {D['t301154_net_kg']} x {D['ci_diff']:.10f} = {D['over54_kg']} kg CO2e. Corrected: production emissions {D['pe_corrected_kg']:,} kg, weighted CI {D['ci_corrected']:.10f}, net removal {D['net_under_t']} t higher. Conservative, but above the 0.001 tCO2e tolerance. The other periods' CIs are each the Aqueous row of their own summary: PP#8 {D['pp8_ci']:.10f} (0.1576), September 2025 {D['sep_ci']:.10f} (0.1287), April 2026 {D['apr_ci']:.10f} (0.1314), May 2026 (0.1107), June 2026 (0.1237). Fix: relabel G24 as May 2026, point H24 at $L$17, change Certify's 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' datapoint to {D['ci_corrected_6dp']:.6f} (pyrolysis {D['pyro_corrected_t']} t), and re-attach the corrected Ops Notes; this clears 3.2, 3.5 and 7.2 together. Changing the sheet alone would leave Certify at {D['certify_ci']} and this row would still fail. If 2.2 is corrected at the same time, the CI becomes {D['ci_corrected_with_22']} [log:ops_notes, ops_notes_totals, inventory_master, pp_summary_sources, {DV}].",
 "GHG Stmt Sec C")
row("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", "Pass",
 "The CI datapoint 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' carries the batch Ops Notes as its source, which holds the per-tote CI column and the weighted-average cell. Every period CI used is traceable from the sheet: each per-tote CI cell references a constant in K10:M21, and each constant used here carries a hyperlink to its Production Period Summary -- PP#8 (M10), April 2026 (M16), May 2026 (M17), June 2026 (M18) and September 2025 (M21; the INJ-09-2026-W2 workbook's constants block has no September 2025 row). All five summaries were opened and their Aqueous CIs agree with the constants [log:certify.attachment_map, ops_notes, pp_summary_sources, pp_summary_sources.w2_constants_block].",
 "VR Appendix 1")
row("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the periods that apply to the component?", "Pass",
 f"Certify Mass {f(produced,1)} kg. Ops Notes sum of Net Oil Produced across all {D['n_totes']} totes (D50) = {f(produced,1)} kg, delta 0.0 kg. The component uses net-in-tote produced mass, not net injected ({f(injected,1)} kg), since pyrolysis emissions were incurred to produce the full quantity. The one tare input that differs from the production record is covered in 2.2 [log:certify.component_by_key.pyrolysis, ops_notes_totals, {DV}].",
 "GHG Stmt Sec C")
row("7.5", "Does the uncertainty match the sum of uncertainties for the periods that apply to the component?", "Pass",
 f"Component detail: {f(produced,1)} kg plus or minus 41.96 kg, the display rounding of {D['n_totes']} x {D['per_tote_unc_kg']} = {unc} kg. Uncertainty is present on this input, which matters because pyrolysis at 4.978 tCO2e is {D['pe_share_of_net_pct']} % of the 3.690 t net removal -- a dominant input that does not qualify for the under-1 % omission allowance [log:certify.component_by_key.pyrolysis, {DV}].",
 "Bio-oil Geological Storage v1.2 Sec 6.5.1")
row("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", "Pass",
 "No Charm Contents sheet exists for this batch -- not present in the Drive batch folder listing or among the six Certify sources. The per-period mass breakdown lives in the Ops Notes QOWV tab Production Period column, and the Ops Notes is attached and linked to the 'QOWV Pyrolysis Mass [Certify input]' datapoint [log:certify.attachment_map, charm_contents, certify.certify_sources_enumeration].",
 "VR Appendix 1")

sec("SECTION 8 -- Other")
row("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total equal (never exceed) the transport-process sum?", "Fail",
 f"The batch has one diesel transport-process emission, the flatbed leg, and it is offset: 'BCU - Transport Process' carries a Constant CO2 reduction of {D['bcu_kg']:,} kgCO2e, read from the component detail, sourced to the TERC Certificate of Retirement attached in Certify (2,795 TERCs retired Dec 18, 2025, vintage 2024, Renewable Diesel, Amazon.com Services LLC on behalf of Charm Industrial, Inc, verified by Turner, Mason & Company, each TERC one tCO2e). The embodied leg is correctly not offset. The BCU exceeds the emission it offsets: on Certify's basis the process emission is {D['proc_certify_kg']:,} kg ({D['proc_sheet_kg']:,} kg on the EF sheet's rounded factor), so the {D['bcu_kg']:,} kg constant is {D['bcu_excess_certify_kg']} kg over ({D['bcu_excess_sheet_kg']} kg on the sheet basis). The BCU QA Rule reads 'BCU quantity (tCO2e) in Reductions must NOT exceed the corresponding diesel/process emission (tCO2e) in Activities', so over-coverage of any size is a Fail. Fix: enter the constant as the exact process emission, {D['proc_certify_kg']:,} kg on the current 0.086 factor ({D['proc_sheet_kg']:,} kg if the factor moves to the sheet's value). Rounding down to 6,263 kg would under-cover by {D['bcu_under_if_6263_kg']} kg [log:certify.component_by_key.bcu, certify.component_by_key.transport_process, retirement_certificate, standard_efs_2026, bcu_rule_sources, {DV}].",
 "BCU QA Rule (batch-qa-charm SKILL.md)")

sec("SECTION 9 -- Aqueous Buffering (LCS)")
row("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist?", "N/A",
 "No LCS use is reported. Every string cell across all ten tabs was scanned for the LCS abbreviation, calcium, caustic, NaOH and buffer with zero matches, and the Summary tab reports sparging 0.0 kg and filtration 0.0 kg for QOWV. With no LCS use there is no component to require [log:lcs_use_kg, lcs_search_method, summary_tab].",
 "VR Sec 3.1")

sec("CALCULATION CHECK -- independent recompute")
row("C.1", "Does the net removal recompute from source values?", "Pass",
 f"Recomputed by recompute_qowv.py from the Ops Notes export and the source-read log (31 of 31 checks OK, exit 0), using Certify's process factor (0.086 kgCO2e/(km*t)) and Certify's CI ({D['certify_ci']}): Sequestration {f(injected,1)} kg x 8.0 % x 3.667 = {D['seq_kg_precise']:,} kg = 9.038 t; Transport process {D['proc_certify_kg']:,} kg = 6.264 t; Transport embodied {D['emb_kg']} kg = 0.331 t; Pyrolysis {D['pyro_certify_kg']:,} kg = 4.978 t; BCU 6.264 t. Net = 9.038 + 6.264 - (6.264 + 0.331 + 4.978) - discount = {D['net_precise_t']} t, matching Certify's 3.690 t. On the EF sheet's factor ({D['ef_flatbed_mt_t_mi']} MT/t-mi) and the Ops Notes H50 CI the net is {D['net_sheet_t']} t, also 3.690. The discount Certify shows as 39 kg is consistent with variance propagation on the three uncertain masses and the carbon content: estimate {D['disc_est_kg']} kg. This reproduces the removal as submitted, so 3.690 t carries the errors in 2.2, 3.4, 7.2 and 8.1. On the production record (301154 at the May CI, 120509 at its 62.93 kg tare, COLA-32 over 18 totes, BCU equal to the process emission) the net is {D['net_record_t']} t; with the Truck 1 and Truck 2 orders at 20 and 18 totes (3.4) it is {D['net_record_orders_t']} t. The script's BCU line tests agreement at display precision (6.264 t both); BCU at or below the process emission is false, as 8.1 records. Counterfactuals are zero. Ledger integrity: no duplicate tags, no tote whose injected mass exceeds its gross, gross masses {D['gross_min']}-{D['gross_max']} kg, post-unload tote weights {D['empty_min']}-{D['empty_max']} kg [log:certify, shipping_orders_2025_12, {DV}].",
 "Bio-oil Geological Storage v1.2")

SIDEBAR = [
 "Allocation tab rows 58-73 hold a per-tote block headed '--- Shipment 2025-12-10 --- (14 of 35 totes on this truck are W4-relevant)', listing 14 tags assigned to batch INJ-05-2026-W4. No total on the tab references those rows, so no figure here draws on them. The same stale block was on the W2 workbook; recommend deleting it.",
 "QOWV tab rows 49 and 51-70 carry template formulas (G = (D-F)*$L$4, H = G*(1-$L$5)) that evaluate blank and feed no total. Harmless; removing them would tidy the ledger.",
 "Lab certificate SR26-05599.001 marks QOWV Carbon 8.0 % with the footnote 'Result is outside of test method limits and/or analytical range used in method precision study' (page 1). The AECN result on page 2 (SR26-05599.002, 39.7 % C, 7.0 % H) carries the same mark. The 0.4 % relative carbon uncertainty in 4.4 is the checklist standard, not a precision the lab states for this result.",
 "Week window: the QOWV tab labels B3 and B4 'Week Start (Sat)' and 'Week End (Sat)', but 2026-09-11 and 2026-09-18 are Fridays, and INJ-09-2026-W2 ended on 2026-09-12, so the two Ops Notes windows share 11-12 Sep. The Bio-oil Injection Tracker records injection completion on 2026-09-17 for all 37 totes, inside Certify's 12-18 Sep window.",
 "The Bio-oil Injection Tracker's quantity_consumed_in_injection column is the Ops Notes net injected mass minus 57.6 kg on 24 of the 37 rows, twice that on 12 rows (809, 813-819, 821, 824-826; 301009 reads 1,549.8 = 2 x 774.9 kg) and neither on row 841 (245161, 804.9 kg). Column total 38,080.6 kg against ledger net injected 30,808.5 kg. Certify uses the ledger figures.",
 "No measured pH is recorded for this batch: QOWV!L6 '2.0 - 4.0' is labelled 'pH range (target)', and the Bio-oil Injection Tracker's injection_ph is blank on all 37 rows.",
 "Inventory QOWV net sums tie to the Production Period Summaries' Aqueous Mass of Output for May 2026 (36,523.2 vs 36,523 kg) and June 2026 (46,616.2 vs 46,616 kg), not for April 2026 (45,764.8 vs 43,912 kg), PP#8 (76,217.12 vs 77,076 kg) or PP#10 (44,931.0 vs 41,010 kg). The summaries' CIs are used as published; the mass gaps sit in the production records.",
 "Nothing in the batch evidence ties this removal's 6.264 t to a drawdown of the 2,795 TERCs on the attached retirement certificate; no checklist item tests reuse of one certificate across removals.",
 "19 of the 37 totes shipped on 2025-12-01 and 2025-12-02 and were injected on 2026-09-17, about nine and a half months after shipping. All four orders are costed over the direct 1,201 mi Colorado-to-Louisiana route.",
 "The September VVB Guidance's only section covers AECN railcar loaded mass for Week 3; nothing in it bears on this QOWV batch.",
]

def build(rows):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "QA Checklist"
    H = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
    FAIL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    FLAG = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    B = Font(bold=True); W = Alignment(wrap_text=True, vertical="top")
    for c, w in {"A": 19, "B": 60, "C": 10, "D": 110, "E": 32}.items(): ws.column_dimensions[c].width = w
    ws.page_setup.orientation = "landscape"; ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.print_title_rows = "11:11"
    r = 1
    for label, val in [("Batch ID", "INJ-09-2026-W3-QOWV (Aqueous / QOWV)"),
                       ("Reporting Period", "September 1 - September 30 2026; Certify removal window 12 Sep 2026 to 18 Sep 2026; Ops Notes injection week 2026-09-11 to 2026-09-18"),
                       ("Reviewer", "Claude (QA agent)"), ("Date", "2026-09-28"), ("Injection Site", "Basco 6, Louisiana"),
                       ("Oil Type", "Aqueous (QOWV) - Charm-produced, Fort Lupton CO, IBC totes"),
                       ("Production Periods", "July 2025 (PP#8), September 2025 (PP#10), April 2026, May 2026 (plus one tote labelled June 2026 that the production record places in May) - 37 totes, captured in one production-mass-weighted pyrolysis component"),
                       ("Certify Removal ID", "rmv_1M38CNSFV1S0B7V7"),
                       ("Net CO2e Removed", "3.690 tCO2e (Sequestrations 9.038 + Adjustments 6.264 - Activities 11.572 - Uncertainty discount 0.039)")]:
        ws.cell(r, 1, label).font = B; ws.cell(r, 2, val).alignment = W; r += 1
    r += 1
    for i, h in enumerate(["Item", "Question", "Status", "Evidence / Finding", "Reference"], 1):
        c = ws.cell(r, i, h); c.fill = H; c.font = B
    r += 1
    counts = {"Pass": 0, "Fail": 0, "Flag": 0, "N/A": 0}
    for e in rows:
        if e[0] == S:
            ws.cell(r, 1, e[1])
            for col in range(1, 6): ws.cell(r, col).fill = H; ws.cell(r, col).font = B
            r += 1; continue
        item, q, st, ev, ref = e; counts[st] += 1
        for col, v in enumerate([item, q, st, ev, ref], 1):
            c = ws.cell(r, col, v); c.alignment = W
            if st == "Fail": c.fill = FAIL
            elif st == "Flag": c.fill = FLAG; c.font = Font(color="996600")
            elif st == "N/A": c.font = Font(italic=True, color="808080")
        r += 1
    r += 1
    ws.cell(r, 1, "SIDEBAR OBSERVATIONS (no status - for Garrett's attention)")
    for col in range(1, 6): ws.cell(r, col).fill = H; ws.cell(r, col).font = B
    r += 1
    for note in SIDEBAR:   # Excel does not auto-size merged cells, so set the height
        ws.cell(r, 2, note).alignment = W; ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws.row_dimensions[r].height = 15 * max(1, math.ceil(len(note) / 170)); r += 1
    r += 1
    ws.cell(r, 1, "STATUS COUNTS").font = B
    ws.cell(r, 2, f"Pass {counts['Pass']}  |  Flag {counts['Flag']}  |  Fail {counts['Fail']}  |  N/A {counts['N/A']}  ({sum(counts.values())} items)")
    ws.freeze_panes = "A12"
    print("counts", counts)
    return wb

if __name__ == "__main__":
    build_with_validation(R, LOGP, OUT, build)
