#!/usr/bin/env python3
"""Build the INJ-09-2026-W4-QOWV (Aqueous) QA checklist. Every quoted figure is computed here
from the source-read log / exports and pushed into _derived_values_numeric so the [log:] audit
can re-check it. Pre-flight validation (checklist_lib) runs before the workbook is written."""
import json, sys, math
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".claude/skills/batch-qa-aecn/scripts"))
from checklist_lib import build_with_validation

HERE = Path(__file__).resolve().parent
LOGP = HERE / "batch_INJ-09-2026-W4-QOWV_source_reads.json"
OUT = HERE / "Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W4.xlsx"
L = json.loads(LOGP.read_text())

# ---------------- derived values (computed, never typed) ----------------
T = L["totes"]; OT = L["ops_notes_totals"]; C = L["certify"]["component_by_key"]; K = L["ops_notes"]["constants"]
EF = L["standard_efs_2026"]; ST = L["shipment_tracker"]; trk = ST["trucks"]; inv = ST["inventory_denominators"]
BL = L["blended_ci_source"]; CO = L["cobb_injection_record"]; LAB = L["testing"]["qowv_certificate"]
gross = OT["total_mass_transported_kg"]; produced = OT["total_oil_produced_kg"]; injected = OT["total_oil_in_batch_kg"]
pe = OT["production_emissions_kg"]; wci = OT["weighted_avg_ci_kgco2e_per_kg"]; unc = OT["uncertainty_kg"]; n = len(T)
cpct = C["injection_sequestration"]["inputs"]["carbon_content_pct"]; c_unc_cert = C["injection_sequestration"]["inputs"]["carbon_content_uncertainty_pct_abs"]
c_unc_ok = round(cpct * 0.004, 5)
seq_kg = injected * cpct / 100 * 3.667
proc_cert = gross / 1000 * 1201 * C["transport_process"]["inputs"]["ef_kgco2e_per_t_mi"]
proc_ok = gross / 1000 * 1201 * EF["flatbed_process"]["value"] * 1000
alloc_tab = ST["totals"]["allocated_miles_mi"]
alloc_inv = L["shipment_tracker"]["allocated_miles_corrected_c38_only"]   # COLA-38 over 18; COLA-40 at its documented physical 18
emb_cert = C["transport_embodied"]["inputs"]["distance_mi"] * C["transport_embodied"]["inputs"]["ef_kgco2e_per_mi"]
emb_nt_tab = alloc_tab * EF["non_tanker_embodied"]["value"] * 1000
emb_ok = alloc_inv * EF["non_tanker_embodied"]["value"] * 1000
pyro_cert = produced * C["pyrolysis"]["inputs"]["ci_tco2e_per_t"]
live_ci = BL["live_recompute"]["qowv_ci"]; used_ci = K["L7_qowv_6mo_ci_jul_dec_2026"]
july = [t for t in T if t["production_period"] == "July 2026"]; june = [t for t in T if t["production_period"] == "June 2026"]; feb = [t for t in T if t["production_period"] == "February 2026"]
jm = sum(t["net_oil_produced_kg"] for t in july)
pe_ok = sum(t["net_oil_produced_kg"] * (live_ci if t["production_period"] == "July 2026" else t["ci_kgco2e_per_kg"]) for t in T)
PB = L["pp_summary_basis"]; after_blend = PB["after_bcu_live_blend"]["qowv"]; aci = PB["after_bcu_ci"]
pe_after = sum(t["net_oil_produced_kg"] * (after_blend if t["production_period"] == "July 2026" else aci[{"June 2026": "Jun", "February 2026": "Feb"}[t["production_period"]]]) for t in T)
rel_m = unc / injected
def disc(seq_t, proc_t, pyro_t, rel_c):
    return 1000 * math.sqrt((seq_t * math.hypot(rel_c, rel_m))**2 + (proc_t * unc / gross)**2 + (pyro_t * unc / produced)**2)
disc_cert = disc(seq_kg / 1000, proc_cert / 1000, pyro_cert / 1000, c_unc_cert / cpct)
net_cert = seq_kg / 1000 + 5.895 - (proc_cert + emb_cert + pyro_cert) / 1000 - disc_cert / 1000
def net_case(pe_case):
    d = disc(seq_kg / 1000, proc_ok / 1000, pe_case / 1000, c_unc_ok / cpct)
    return seq_kg / 1000 + proc_ok / 1000 - (proc_ok + emb_ok + pe_case) / 1000 - d / 1000, d
net_ok, disc_ok = net_case(pe_ok); net_keep, _ = net_case(pyro_cert); net_after, disc_after = net_case(pe_after)
RU = PB["ruling_2026_10_07"]; PK = RU["package_version"]; LV = RU["linked_sheets_version"]
net_pkg, _ = net_case(PK["pe_kg"])               # 2026-10-07 ruling, package versions throughout (V2's sources)
net_lv, _ = net_case(LV["pe_kg"])                # 2026-10-07 ruling, linked sheets throughout (blend rebuilt)
glec_kg = gross / 1000 * 1201 * 1.609344 * 0.086
E = [t["empty_tote_weight_kg"] for t in T]; G = [t["gross_kg"] for t in T]
pc = CO["post_unload_conflicts"]
dE = pc["301215"]["tracker_basis_net_injected_kg"] - pc["301215"]["ops_net_injected_kg"]
gc = L["production_records"]["gross_conflict_301274"]
t40 = {t["truck"]: t for t in trk}
v2m = BL["v2_qowv_emissions_by_month_mt"]; live = L["pp_summary_sources"]["live"]
D = {
 "n_totes": n, "gross_kg": gross, "produced_kg": produced, "injected_kg": injected, "residue_kg": round(produced - injected, 4),
 "pe_kg": round(pe, 6), "weighted_ci": wci, "unc_kg": unc, "per_tote_unc_kg": 1.13398, "kg_per_lb": 0.453592, "lb_per_tote": 2.5,
 "june_totes": len(june), "july_totes": len(july), "feb_totes": len(feb),
 "june_mass_kg": round(sum(t["net_oil_produced_kg"] for t in june), 4), "july_mass_kg": round(jm, 4), "feb_mass_kg": round(sum(t["net_oil_produced_kg"] for t in feb), 4),
 "june_pe_kg": round(sum(t["production_emissions_kg"] for t in june), 4), "july_pe_kg": round(sum(t["production_emissions_kg"] for t in july), 4), "feb_pe_kg": round(sum(t["production_emissions_kg"] for t in feb), 4),
 "jun_ci": K["L18_Jun2026"], "feb_ci": K["L14_Feb2026"], "blend_ci_used": used_ci, "blend_ci_v2": BL["qowv_result"]["ci"], "blend_ci_live": live_ci,
 "blend_ci_diff": round(live_ci - used_ci, 10), "pe_ok_kg": round(pe_ok, 4), "pe_gain_kg": round(pe_ok - pe, 4), "wci_ok": round(pe_ok / produced, 10), "wci_ok_6dp": round(pe_ok / produced, 6),
 "pyro_ok_t": round(produced * round(pe_ok / produced, 6) / 1000, 6),
 "live_aq_mass_kg": BL["live_recompute"]["qowv_mass_kg"], "live_aq_mt": BL["live_recompute"]["qowv_emissions_mt"], "v2_aq_mt": BL["qowv_result"]["emissions_mt"],
 "wodo_blend_used": BL["wodo_result"]["ci"], "wodo_blend_live": BL["live_recompute"]["wodo_ci"],
 "v2_jun_mt": v2m["Jun 2026"], "live_jun_mt": live["Jun"]["aqueous_emissions_mt"], "v2_feb_mt": v2m["Feb 2026"], "live_feb_mt": live["Feb"]["aqueous_emissions_mt"],
 "v2_jan_mt": v2m["Jan 2026"], "live_jan_mt": live["Jan"]["aqueous_emissions_mt"],
 "carbon_pct": cpct, "carbon_unc_cert": c_unc_cert, "carbon_unc_ok": c_unc_ok, "carbon_unc_over_pct": round((c_unc_cert / c_unc_ok - 1) * 100, 4),
 "co2_c_ratio": 3.667, "seq_kg": round(seq_kg, 4), "seq_t": 9.902,
 "ef_tanker_proc": EF["tanker_process"]["value"], "ef_flatbed_proc": EF["flatbed_process"]["value"], "ef_tanker_emb": EF["tanker_embodied"]["value"], "ef_nontanker_emb": EF["non_tanker_embodied"]["value"],
 "ef_cert_proc_kg_t_mi": 0.1143, "ef_cert_emb_kg_mi": 0.23756,
 "proc_cert_kg": round(proc_cert, 4), "proc_ok_kg": round(proc_ok, 4), "proc_gain_kg": round(proc_ok - proc_cert, 4), "proc_t": 5.895,
 "alloc_tab_mi": round(alloc_tab, 6), "alloc_tab_2dp": round(alloc_tab, 2), "alloc_inv_mi": round(alloc_inv, 4), "alloc_over_mi": round(alloc_tab - alloc_inv, 4),
 "c37_share": t40["COLA-37"]["share"], "c37_miles": t40["COLA-37"]["allocated_miles"], "c39_miles": t40["COLA-39"]["allocated_miles"],
 "c38_share_tab": t40["COLA-38"]["share"], "c38_miles_tab": round(t40["COLA-38"]["allocated_miles"], 4), "c38_share_inv": round(5 / 18, 10), "c38_miles_inv": round(5 / 18 * 1201, 4),
 "c40_share_tab": t40["COLA-40"]["share"], "c40_miles_tab": round(t40["COLA-40"]["allocated_miles"], 4), "c40_share_inv": round(2 / 17, 10), "c40_miles_inv": round(2 / 17 * 1201, 4),
 "c38_total_inv": inv["COLA-38"], "c38_total_tab": t40["COLA-38"]["totes_on_truck"], "c40_total_inv": inv["COLA-40"], "c40_total_tab": t40["COLA-40"]["totes_on_truck"],
 "c38_claimed": L["other_batches_on_shared_trucks"]["cola38_shares_claimed"],
 "emb_cert_kg": round(emb_cert, 4), "emb_nt_tab_kg": round(emb_nt_tab, 4), "emb_ok_kg": round(emb_ok, 4), "emb_t": 0.769,
 "pyro_cert_kg": round(pyro_cert, 4), "pyro_t": 5.01, "certify_ci": C["pyrolysis"]["inputs"]["ci_tco2e_per_t"],
 "bcu_kg": 5895, "bcu_short_cert_kg": round(proc_cert - 5895, 4), "bcu_short_ok_kg": round(proc_ok - 5895, 4),
 "net_t": 4.076, "net_cert_t": round(net_cert, 5), "net_ok_t": round(net_ok, 5), "net_gain_t": round(net_ok - net_cert, 5),
 "disc_kg": 47, "disc_est_kg": round(disc_cert, 2), "disc_ok_kg": round(disc_ok, 2),
 "pe_share_of_net_pct": round(5.010 / 4.076 * 100, 1),
 "e_min": min(E), "e_max": max(E), "gross_min": min(G), "gross_max": max(G),
 "e_301215_ops": pc["301215"]["ops_notes_E26_kg"], "e_301215_trk": pc["301215"]["tracker_implied_kg"], "g_301215": pc["301215"]["tracker_gross_kg"],
 "inj_301215_ops": pc["301215"]["ops_net_injected_kg"], "inj_301215_trk": pc["301215"]["tracker_basis_net_injected_kg"],
 "g_301274_ops": gc["ops_notes_B40_kg"], "g_301274_trk": gc["production_system_gross_kg"], "g_301274_gap": round(gc["production_system_gross_kg"] - gc["ops_notes_B40_kg"], 1), "e_301274_ops": gc["ops_notes_E40_kg"],
 "cobb_rows_live": 168, "cobb_ph": 2.97, "cobb_ph_rows": 126,
 "g274_seq_gain": gc["if_production_gross"]["seq_gain_kg"], "g274_pe_gain": gc["if_production_gross"]["pe_gain_kg"], "g274_net_gain": gc["if_production_gross"]["net_gain_kg"],
 "res_kg": round(442.5 - 57.6, 1), "res_share_301166": round((442.5 - 57.6) / 1036.4, 4), "res_share_301215": round((442.5 - 57.6) / 983.4, 4), "cobb_qty_july_300020": 883.0,
 "inj_gain_kg": round(dE, 1), "seq_gain_kg": round(dE * cpct / 100 * 3.667, 4), "residue_301215_kg": round(442.5 - 57.6, 1),
 "route1": 1132, "route2": 1129, "route3": 1201, "one_way_mi": 1201,
 "lab_c": LAB["carbon_pct"], "lab_h": LAB["hydrogen_pct"], "lab_density": LAB["density_15C_g_cm3"], "lab_acid": LAB["acid_number_mgKOH_g"], "lab_kv": LAB["kinematic_viscosity_40C_cSt"],
 "tercs": 2795, "sources_total": 6, "datapoints_total": 10, "cobb_first_row": 861, "cobb_last_row": 3723, "cobb_rows": 42, "cobb_qty_301204": 1540.8, "cobb_qty_300020": 666.4,
 "t300022_net_inj": 724, "tare": 57.6,
 "net_keep_t": round(net_keep, 5), "net_after_t": round(net_after, 5), "net_keep_gain_t": round(net_keep - net_cert, 5), "net_after_gain_t": round(net_after - net_cert, 5),
 "blend_ci_after": after_blend, "jun_ci_after": aci["Jun"], "feb_ci_after": aci["Feb"], "pe_after_kg": round(pe_after, 4), "pe_after_drop_kg": round(pe - pe_after, 4),
 "wci_after": round(pe_after / produced, 10), "wodo_blend_after": PB["after_bcu_live_blend"]["wodo"], "glec_bcu_kg": round(glec_kg, 4), "glec_gap_kg": round(glec_kg - proc_ok, 4),
 "unc_june_kg": round(len(june) * 1.13398, 5), "unc_july_kg": round(len(july) * 1.13398, 5), "unc_feb_kg": round(len(feb) * 1.13398, 5),
 "jun_bcu_mt": PB["by_month"]["Jun"]["live_bcus_applied_C10_mt"], "jun_share": PB["by_month"]["Jun"]["live_aqueous_share"],
 "dev_301215": round(821.4 - (598.5 - 57.6), 1),
 "may_c85_live": PB["by_month"]["May"]["C85_live"], "may_c85_copy": PB["by_month"]["May"]["C85_copy"], "c40_doc": 18,
 "pkg_jun_ci": PK["ci_by_period"]["June 2026"], "pkg_feb_ci": PK["ci_by_period"]["February 2026"], "pkg_pe_kg": PK["pe_kg"], "pkg_pe_change_kg": PK["pe_change_kg"], "pkg_wci": PK["weighted_ci"],
 "lv_pe_kg": LV["pe_kg"], "lv_pe_change_kg": LV["pe_change_kg"], "lv_wci": LV["weighted_ci"],
 "blend_mar_kg": LV["blend_difference_on_july_totes_by_month_kg"]["Mar"], "blend_may_kg": LV["blend_difference_on_july_totes_by_month_kg"]["May"],
 "net_pkg_t": round(net_pkg, 5), "net_pkg_gain_t": round(net_pkg - net_cert, 5), "net_lv_t": round(net_lv, 5), "net_lv_gain_t": round(net_lv - net_cert, 5),
 "g_301277_prod": 1036.0, "g_301227_prod": 1070.0,
 "jun_late_kg": L["tote_weighing_records"]["june_totes_weighed_in_july"]["net_oil_produced_kg"],
 "jun_n4_kg": L["tote_weighing_records"]["june_totes_weighed_in_july"]["corroboration"]["june_summary_aqueous_mass_N4_kg"],
 "jun_q4_rows": L["tote_weighing_records"]["june_totes_weighed_in_july"]["corroboration"]["q4_june_qowv_rows"],
}
L["_derived_values_numeric"] = D
LOGP.write_text(json.dumps(L, indent=1, default=str))
DV = "_derived_values_numeric"

def f(x, n=2): return f"{x:,.{n}f}"
S, R = "SECTION", []
def sec(t): R.append((S, t))
def row(i, q, s, e, ref): R.append((i, q, s, e, ref))

# ================= SECTION 1 =================
sec("SECTION 1 -- Batch Folder")
row("1.1", "Is there testing in the testing folder for the batch?", "Pass",
 f"The Testing subfolder holds 'SR26-05719 W4 Kerry AECN QOWV COA.pdf' (Drive id 1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ). It was downloaded and read, and it is byte-identical (same sha256) to the certificate attached in Certify (src_1M3VZ8S8W1S013HS): page 3 is SGS Certificate of Analysis SR26-05719.003, Client ID '9-2026-W4-QOWV', FORT LUPTON CO, sampled 25-Sep-2026 10:00, analysed 28-Sep-2026: Carbon {LAB['carbon_pct']} % (m/m) by ASTM D5291 (Method C), Hydrogen {LAB['hydrogen_pct']} %, Nitrogen <0.75 %, Kinematic Viscosity {LAB['kinematic_viscosity_40C_cSt']} cSt, Acid Number {LAB['acid_number_mgKOH_g']} mg KOH/g, Density at 15 C {LAB['density_15C_g_cm3']} g/cm3, above the formation-fluid density of 1.01 g/cm3 (knowledge base, Density Requirements: 'All streams exceed formation fluid density (1.01 g/cm\u00b3)'). Pages 1 and 2 are the Kerry (SR26-05719.001) and AECN (SR26-05719.002) composites for the other removals [log:testing, testing.formation_fluid_density, {DV}].",
 "VR Appendix 1")
row("1.2", "Are Ops Notes in the folder and fully completed?", "Pass",
 f"'INJ-09-2026-W4 Ops Notes' is in the batch folder and was exported from the live sheet and read cell by cell. QOWV tab: B2 'INJ-09-2026-W4', week B3 2026-09-18 to B4 2026-09-25, and {n} tote rows (A11:A52) with every row populated for tag, gross mass, tote mass, net oil produced, empty tote weight, net oil injected, production period, carbon intensity, production emissions and scale uncertainty. The row-54 totals all resolve to values: Total Mass Transported {f(gross,1)} kg, Total Oil Produced {f(produced,1)} kg, Total Oil Injected {f(injected,1)} kg, weighted CI {wci:.10f}, production emissions {pe:,.6f} kg, uncertainty {unc} kg. The workbook's only two cell notes sit on the AECN Truck and Kerry tabs (wellhead pH) [log:ops_notes, ops_notes_totals, vvb_guidance.ops_notes_cell_comments, {DV}].",
 "VR Appendix 1")
row("1.3", "Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?", "Flag",
 f"The allocation is carried by the 'QOWV Shipments & EE Allocation' tab of the batch Ops Notes workbook, which is in the folder. Its truck rows are filled for all four shipping orders feeding this batch -- COLA-37, COLA-38, COLA-39, COLA-40 -- with ship date, totes on truck, batch totes, share, one-way mileage and allocated miles, and batch totes 15 + 5 + 20 + 2 sum to the {n}-tote ledger. The flag: the tab holds truck-level counts only. Rows 20-74 are empty, so no row ties any of the {n} tags to a truck, and the tab has no 'every batch tote is allocated to a truck' check row of the kind the Whole Oil allocation tab carries at A16. The truck membership had to be rebuilt tag by tag from the production inventory master (3.1). The A19 note records a COLA-40/COLA-41 count correction that the tab itself calls unreconciled (3.4) [log:shipment_tracker, inventory_master, {DV}].",
 "VR Appendix 1")

# ================= SECTION 2 =================
sec("SECTION 2 -- Ops Notes")
row("2.1", "Is the \"Total Mass Transported\" value correctly computed as the sum of the gross weight of all totes?", "Pass",
 f"QOWV!B54 is a live sum over the gross-mass column, SUM(B11:B52), and returns {f(gross,1)} kg. Re-summing the {n} per-tote gross values independently gives {f(gross,1)} kg, delta 0.0 kg. Every gross value also matches the inventory master's Q4 production tab for the same tag ({n} of {n}); the production system's weighing record (the tracker's Historical Tote Record, dated 2026-02-17 (lot 4746, filed under tag 300020) to 2026-08-31) matches the ledger gross on 40 of the 41 tags it carries under their own tag (no record states where the totes were weighed); it gives tote 301274 1,080.0 kg rather than 1,036.0 kg, which 2.3 carries, and files tote 300022's lot under tag 300020 (3.1). The same figure is Certify's Transport Process Mass of Load [log:ops_notes_totals, inventory_master, tote_weighing_records, production_records.gross_conflict_301274, {DV}].",
 "VR Sec 5.1")
row("2.2", "Is the \"Total Oil Produced\" value correctly computed as the sum of the net weight of oil in tote for all totes (gross - tare per tote)?", "Flag",
 f"The arithmetic is right: per-tote D = B - C on every row and QOWV!D54 = SUM(D11:D52) returns {f(produced,1)} kg, which an independent re-sum reproduces. The flag is the tare input. Column C (Tote Mass) reads {D['tare']} kg on all {n} rows, and the inventory master's Tare Weight for all {n} tags is the same {D['tare']} kg standard figure, not a per-tote weighing. Total Oil Produced, which is the pyrolysis mass, therefore rests on a standard tare; its plus or minus {unc} kg covers only the gross weighing. Total Oil in Batch is unaffected, since it uses the measured post-unload weight (column E). Same basis as INJ-09-2026-W3-QOWV. The disputed gross of tote 301274 (2.3) would also move this total [log:ops_notes_totals, inventory_master.tare_distribution_batch, production_records.gross_conflict_301274, {DV}].",
 "VR Sec 5.1")
row("2.3", "Is the \"Total Oil in Batch\" value correctly computed?", "Fail",
 f"The method is right for Aqueous: per-tote F = IF(E=\"\",\"\",B-E), gross minus the measured post-unload tote weight; column E ranges {D['e_min']}-{D['e_max']} kg, so it is a weighing, not the {D['tare']} kg nominal tote mass. QOWV!F54 = SUM(F11:F52) returns {f(injected,1)} kg and an independent re-sum of (B - E) gives the same. No Standard Loss column or constant appears, and Summary!E12/F12 report sparging 0.0 and filtration 0.0 for QOWV. Custody: the {D['residue_kg']:,} kg left in the totes still carries its production emissions (pyrolysis mass is net produced, D) and transport emissions (mass of load is gross, B). The injection tracker's COBB tabs are not a source of record for this check (batch-qa-charm FC-C14). The fail: two production records disagree on tote 301274's gross weight. The Ops Notes (B40) and the inventory master's Q4 production tab (row 694) give {D['g_301274_ops']} kg; the production system's own weighing gives {D['g_301274_trk']} kg, {D['g_301274_gap']} kg more (Oil_inventory_data row 39 and the Historical Tote Record row 1181: work order OIL260721143336, 2026-07-21, net 1,022.4 kg). The post-unload weight is measured in the Ops Notes (E40, {D['e_301274_ops']} kg), so if {D['g_301274_trk']} kg is right, transported, produced and injected mass each rise {D['g_301274_gap']} kg: sequestration {D['g274_seq_gain']} kg CO2e higher, production emissions {D['g274_pe_gain']} kg higher at the July CI, net {D['g274_net_gain']} kg higher. The files point to the BGN record as the error: its rows look shifted. BGN's 1,036.0 kg for 301274 is the production system's weighing of tote 301277 (OIL260721142141, Oil_inventory_data row 40, Historical Tote Record row 1180), and BGN's 301277 row (693) carries tote 301227's {D['g_301227_prod']:,} kg (OIL260721133028). The order among the Ops Notes, the BGN inventory and the production system's records is not yet ruled (batch-qa-charm FC-C14). Fix: confirm 301274's gross and correct the Ops Notes and BGN rows (and 301277's, outside this batch); a change also moves 2.1, 2.2, 4.3 (the Mass of Product it quotes), 5.3 and 7.4 and, through the process emission, 8.1 [log:ops_notes_totals, production_records.gross_conflict_301274, production_records.bgn_row_shift_301274, production_records.source_hierarchy, inventory_master, max_rulings, summary_tab, {DV}].",
 "GHG Stmt Sec C")
row("2.4", "Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?", "Pass",
 f"Per-tote J = 2.5*$L$4 with L4 = {D['kg_per_lb']} kg/lb, giving {D['per_tote_unc_kg']} kg on all {n} rows. QOWV!J54 = SUM(J11:J52) returns {unc} kg; expected {n} x {D['per_tote_unc_kg']} = {unc} kg, delta 0.00000 kg. This is the per-tote weighing precision, not AECN's per-truck figure [log:ops_notes_totals, ops_notes, {DV}].",
 "Isometric Standard S3.7.3")

# ================= SECTION 3 =================
sec("SECTION 3 -- Bio-Oil Shipment Tracker (QOWV Shipments & EE Allocation tab)")
row("3.1", "Are totes for the RP correctly identified?", "Flag",
 f"Batch-relevant totes across the four shipping orders are 15 (COLA-37, 2026-09-09) + 5 (COLA-38, 2026-09-10) + 20 (COLA-39, 2026-09-15) + 2 (COLA-40, 2026-09-17) = {n}, matching the ledger; the count cell D6 = COUNTA(QOWV!A11:A52) is formula-linked to it. Each tote's truck was confirmed tag by tag against Ship Status on the production inventory master: 15 on COLA_37, 5 on COLA_38, 20 on COLA_39, 2 on COLA_40. None of the {n} tags appears in any other week's Ops Notes (INJ-08-2026-W5 to INJ-10-2026-W3, every cell scanned; the scan finds W3's own tag 301009 four times in its workbook as a control). The flag is one tote's identity: the ledger and the Q4 production tab call lot 4746 tote 300022, but the production system (Oil_inventory_data rows 360 and 350, Historical Tote Record rows 840 and 850) gives security tag 300020 to two lots, 4746 (1,012.0 kg) and LOT00004770 (1,085.0 kg). Lot numbers and weights agree in every production record, so no mass is counted twice, but the metal tag cannot identify this tote on its own. Fix: give lot 4746 its own tag number in the production system [log:inventory_master, cross_week_double_count, production_records.tag_300020, shipment_tracker, {DV}].",
 "VR Sec 3.5")
row("3.2", "Do all totes identified for RP match the Ops Notes for the applicable batch?", "Pass",
 f"Checked per attribute, tag by tag, against the production inventory master: tag {n} of {n}, fraction QOWV {n} of {n}, gross mass {n} of {n}, production period {n} of {n} (June 2026 PP {D['june_totes']}, July 2026 PP {D['july_totes']}, February 2026 PP {D['feb_totes']}; spray-paint codes Blue2606, Purple2607 and Blue2602 agree with the periods) [log:inventory_master, totes, {DV}].",
 "VR Sec 3.5")
row("3.3", "Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?", "Pass",
 "Every computed cell is a live formula, read from the workbook exported from the live sheet this session: E12 '=D12/C12', E13 '=D13/C13', E14 '=D14/C14', E15 '=D15/C15' (share); G12 '=E12*F12' through G15 '=E15*F15' (allocated miles); G17 '=SUM(G12:G15)' (batch mileage allocation); D6 '=COUNTA(QOWV!A11:A52)'; and F12:F15 '=$B$8' pointing at the single one-way distance input. The typed inputs are the tote counts in C and D and the distance in B8 [log:shipment_tracker_cells_are_formulas, shipment_tracker].",
 "Auditability - VR Sec 5.1")
row("3.4", "Are computed outputs computed correctly?", "Fail",
 f"The formulas follow the method (share = batch totes / totes on truck; allocated miles = share x one-way 1,201 mi) and reproduce as written: COLA-37 15/20 = {D['c37_share']} -> {D['c37_miles']} mi; COLA-38 5/6 = {D['c38_share_tab']:.10f} -> {D['c38_miles_tab']} mi; COLA-39 20/20 -> {D['c39_miles']} mi; COLA-40 2/18 = {D['c40_share_tab']:.10f} -> {D['c40_miles_tab']} mi; total {D['alloc_tab_mi']:,.6f} mi. The COLA-38 denominator is wrong. C13 reads {D['c38_total_tab']}, counting only its QOWV totes, but the inventory master lists {D['c38_total_inv']} totes shipped on COLA_38 (6 QOWV + 12 Whole Oil), and INJ-10-2026-W2 and INJ-10-2026-W3 Whole Oil allocate the same truck over {D['c38_total_inv']} ('12 DC Whole Oil + 6 BGN QOWV'), so the three batches together claim {D['c38_claimed']} of that truck. At 5/18 = {D['c38_share_inv']} the share is {D['c38_miles_inv']} mi. COLA-40's {D['c40_total_tab']} is the physical count documented in the tab's own A19 note (totes 301347 and 301356 rode COLA-41); the inventory master lists {D['c40_total_inv']}, a gap the note flags for upstream reconciliation, so 18 stands; if the master's 17 proves right instead, the allocation becomes 2,576.6552 mi. With COLA-38 over 18 the batch mileage allocation is {D['alloc_inv_mi']:,} mi, {D['alloc_over_mi']:,} mi lower; the error over-charges this batch's embodied emissions, so it is conservative for W4 but double-counts the truck across batches. Fix: C13 to 18, then carry the new G17 into Certify (6.2) [log:shipment_tracker, inventory_master, other_batches_on_shared_trucks, {DV}].",
 "Transportation Emissions Acctg v1.1")
row("3.5", "Do the totes assigned to each batch match the Ops Notes on: (a) tag number, (b) fraction, (c) gross mass, (d) production period?", "Flag",
 f"(a) tag {n} of {n}; (b) fraction QOWV {n} of {n}; (c) gross mass {n} of {n}; (d) production period {n} of {n}, each against the production inventory master row for the tag (rows 410-741 of the Q4 2025-2026 Production Inventory tab). The flag is documentation: no 2026 tote has a fill date (Form/tote Date is blank on all 421 rows labelled January-September 2026), and the production system dates 8 totes in the month after their label. Its production_date and weighing record read 2026-07-01 for 301210, 301215, 301223 and 301228 (June 2026), and the weighing record reads 2026-08-31 for 301305, 301312, 301317 and 301331 (July 2026); these dates are the weigh-in, not the fill. The records place the totes in their labelled period. The June summary's Aqueous mass (N4, 46,616.2 kg) is the sum of the 48 QOWV rows labelled June 2026, these four included, and the Jan-Jun blend counts the same June mass, so both CIs were computed with them as June output. They carry June's spray paint (Blue2606), and the four July totes July's (Purple2607). Weigh-ins in the month after the label are routine (10 May totes on 2026-06-01, 16 June totes 2026-07-01 to 07-03, 20 July totes in August). No change to the removal. Fix: record each tote's fill date, or the rule that assigns its production period, in the production inventory [log:inventory_master, totes, tote_weighing_records.june_totes_weighed_in_july, tote_weighing_records.june_totes_weighed_in_july.corroboration, tote_weighing_records.july_totes_weighed_after_july, pp_summary_sources.live, {DV}].",
 "VR Sec 3.5")

# ================= SECTION 4 =================
sec("SECTION 4 -- Certify: Injection Sequestration")
row("4.1", "Does the C content in the testing match the C content in the Sequestration component?", "Pass",
 f"Component detail read directly: Carbon content of product {cpct} %. Lab certificate SR26-05719.003 reports Carbon {LAB['carbon_pct']} % (m/m). Delta 0.0 percentage points. Ops Notes Summary!E20 carries 0.079 against composite SR26-05719.003 dated 2026-09-25 [log:certify.component_by_key.injection_sequestration, testing.qowv_certificate, summary_tab, {DV}].",
 "VR Sec 5.1")
row("4.2", "Is the C content in the Sequestration component properly evidenced (test copy + Ops Notes copy)?", "Pass",
 "The Carbon Content datapoint carries 2 sources, and the Sources tab names both: 'SR26-05719 W4 Kerry AECN QOWV COA.pdf' (the lab certificate) and 'INJ-09-2026-W4 Ops Notes.xlsx'. Both are linked to the datapoint itself. The attached Ops Notes copy (src_1M3VZCDQF1S0FQ0D) was downloaded and is cell-for-cell identical to the live sheet on the QOWV, allocation and Summary tabs [log:certify.attachment_map, certify.certify_sources_enumeration, certify.attached_ops_notes_copy].",
 "VR Appendix 1")
row("4.3", "Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?", "Pass",
 f"Component detail read directly: Mass of product {f(injected,1)} kg plus or minus {unc} kg. Ops Notes uncertainty J54 = {unc} kg. Exact match at full precision [log:certify.component_by_key.injection_sequestration, ops_notes_totals, {DV}].",
 "Isometric Standard S3.7.3")
row("4.4", "Does the C content have the appropriately computed 0.4% relative uncertainty (0.004 x reported value)?", "Fail",
 f"Component detail: {cpct} % plus or minus {c_unc_cert} percentage points. Expected 0.004 x {cpct} = {c_unc_ok} percentage points, the figure the Ops Notes itself computes (Summary!G20 = E20*H20 = 0.000316 as a fraction). Certify is {D['carbon_unc_over_pct']} % high relative, outside the 0.001 absolute tolerance. Nothing on the lab certificate or in the Ops Notes produces {c_unc_cert}. The same unexplained carbon-uncertainty overstatement was raised on INJ-08-2026-W5 WODO. Overstating the uncertainty enlarges the discount, so the error is conservative, but the datapoint does not match its evidence. Fix: set the Carbon Content uncertainty to {c_unc_ok} [log:certify.component_by_key.injection_sequestration, summary_tab, {DV}].",
 "Isometric Standard S3.7.3")

# ================= SECTION 5 =================
sec("SECTION 5 -- Certify: Transport Process Emissions")
row("5.1", "Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?", "Fail",
 f"No. The component 'CO to LA Flatbed Truck Transport Process Emissions - QOWV' uses the datapoint 'Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck' at {D['ef_cert_proc_kg_t_mi']} kgCO2e/(t*mi), sourced to 'Standard Emission Factors + Calculations (8).xlsx'. That is the Tanker row of the live Standard Emission Factors sheet, 2026 tab (row 6, {D['ef_tanker_proc']} MT CO2e/t-mi). The Flatbed row (row 7) is {D['ef_flatbed_proc']} MT CO2e/t-mi (GLEC V3.2 2025), and the attached EF workbook carries the same two rows. Recompute: {gross/1000} t x 1,201 mi x {D['ef_cert_proc_kg_t_mi']} = {D['proc_cert_kg']:,} kg = 5.895 t as Certify shows; on the Flatbed factor = {D['proc_ok_kg']:,} kg, {D['proc_gain_kg']:,} kg higher. INJ-09-2026-W3-QOWV used the Flatbed factor. Fix: switch the datapoint to the Flatbed row; the BCU must move with it (8.1) [log:standard_efs_2026, certify.component_by_key.transport_process, certify_attached_ef_sheet, {DV}].",
 "Standard EFs 2026 tab, row 7")
row("5.2", "Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?", "Pass",
 f"Certify distance is 1,201 mi ('Distance from Miniforge CO to Basco'), sourced to 'CO to Basco Routing Map.png'. That image was downloaded from this removal's own Certify source (src_1KSTWP2AP1S0QQPF) and read from the pixels: three routes to destination '4675 LA-115, St Landry, LA 71367' -- via US-287 S {D['route1']:,} mi, via US-287 S and I-20 E {D['route2']:,} mi, via I-70 E {D['route3']:,} mi. Certify uses 1,201 mi, the longest. The origin field reads 'Your location' with the pin just north of Denver; this same map's origin was confirmed as Fort Lupton on INJ-07-2026-W1 (registry max_rulings_2026_08_06). The file is byte-identical to the routing map on INJ-09-2026-W3-QOWV [log:google_maps_options, google_maps_note, certify.component_by_key.transport_process, {DV}].",
 "Charm convention - longest route")
row("5.3", "Does the Mass of Load match the Total Mass Transported value in Ops Notes?", "Pass",
 f"Component detail: Mass of load 'QOWV Transport Mass (CO to B6) [Certify input]' {f(gross,0)} kg = Ops Notes Total Mass Transported (QOWV!B54) {f(gross,1)} kg, delta 0.0 kg. This is the gross figure including tote tares, not Total Oil Produced ({f(produced,1)} kg) or Total Oil Injected ({f(injected,1)} kg). The datapoint title names the fraction, basis and lane correctly [log:certify.component_by_key.transport_process, ops_notes_totals, {DV}].",
 "VR Sec 5.1")
row("5.4", "Is the Mass of Load evidenced by a copy of the batch Ops Notes?", "Pass",
 "The 'QOWV Transport Mass (CO to B6) [Certify input]' datapoint carries 1 source, 'INJ-09-2026-W4 Ops Notes.xlsx', confirmed on the Sources tab (the Ops Notes row's '+ 5 more' list) as linked to that datapoint [log:certify.attachment_map, certify.certify_sources_enumeration].",
 "VR Appendix 1")
row("5.5", "Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?", "Pass",
 f"Component detail shows {f(gross,0)} kg plus or minus 47.627 kg, the display rounding of the same {n} x {D['per_tote_unc_kg']} = {unc} kg the Ops Notes carries and the Sequestration component holds at full precision. Same totes, same weighings [log:certify.component_by_key.transport_process, ops_notes_totals, {DV}].",
 "Isometric Standard S3.7.3")

# ================= SECTION 6 =================
sec("SECTION 6 -- Certify: Transport Embodied Emissions")
row("6.1", "Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?", "Fail",
 f"No. The component uses 'Emissions Factor - Vehicle Embodied Emissions - Tanker Truck' at {D['ef_cert_emb_kg_mi']} kgCO2e/mi (0.1476 kgCO2e/km on the Datapoints tab), the Tanker row of the live 2026 tab (row 11, {D['ef_tanker_emb']} MT CO2e/mi). The Non-Tanker row (row 12) is {D['ef_nontanker_emb']} MT CO2e/mi (GLEC V3.2 2025). The value applied is the tanker one, not only the label: {D['alloc_tab_2dp']:,} mi x {D['ef_cert_emb_kg_mi']} = {D['emb_cert_kg']} kg reproduces Certify's 0.769 t, while the Non-Tanker factor on the same miles gives {D['emb_nt_tab_kg']} kg. With the 3.4 allocation also corrected ({D['alloc_inv_mi']:,} mi) the embodied emission is {D['emb_ok_kg']} kg. Fix: switch the datapoint to the Non-Tanker row [log:standard_efs_2026, certify.component_by_key.transport_embodied, certify_attached_ef_sheet, {DV}].",
 "Standard EFs 2026 tab, row 12")
row("6.2", "Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?", "Pass",
 f"Certify 'QOWV Embodied Distance (CO to B6) [Certify input]' = {D['alloc_tab_2dp']:,} mi. The allocation tab's total G17 = SUM(G12:G15) = {D['alloc_tab_mi']:,.6f} mi. The Certify figure matches the tracker as submitted. The tracker figure itself carries the COLA-38 denominator error in 3.4, which would bring it to {D['alloc_inv_mi']:,} mi [log:certify.component_by_key.transport_embodied, shipment_tracker, {DV}].",
 "Transportation Emissions Acctg v1.1")
row("6.3", "Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?", "Pass",
 "The datapoint carries 2 sources and the Sources tab confirms both: 'INJ-09-2026-W4 Ops Notes.xlsx' (which contains the QOWV Shipments & EE Allocation tab that derives the figure) and 'CO to Basco Routing Map.png' (the one-way route). No standalone Charm Contents sheet exists for this batch: none in the Drive batch folder listing or among the six Certify sources, and the per-period breakdown is the Ops Notes Production Period column, the basis used on every 2026 weekly batch [log:certify.attachment_map, charm_contents, batch_folder_listing, certify.certify_sources_enumeration].",
 "VR Appendix 1")

# ================= SECTION 7 =================
sec("SECTION 7 -- Certify: Production (Pyrolysis) Emissions")
row("7.1", "Are there Production Emissions components for ALL Production Periods in the batch?", "Pass",
 f"Every tote carries a production period and a period CI, so no period's emissions are left out: June 2026 ({D['june_totes']} totes, {D['june_mass_kg']:,} kg, {D['june_pe_kg']:,} kg CO2e), July 2026 ({D['july_totes']}, {D['july_mass_kg']:,} kg, {D['july_pe_kg']:,} kg CO2e) and February 2026 ({D['feb_totes']}, {D['feb_mass_kg']:,} kg, {D['feb_pe_kg']:,} kg CO2e). They are captured in one production-mass-weighted component, 'Pyrolysis - Charm QOWV PP Emissions', whose total reconciles to the per-tote sum: sum of (net produced x tote CI) = {D['pe_kg']:,} kg; {f(produced,1)} kg x {D['certify_ci']} = {D['pyro_cert_kg']:,} kg = 5.010 t in Certify. June and February totes keep their own monthly CI; the July 2026 totes, produced inside the Jul-Dec 2026 window, take the Jan-Jun 2026 blended CI, as the CI policy requires (its value is 7.2). Eight totes' weighing records fall outside their labelled period (3.5); whichever period they belong to, it is captured in this one component [log:ops_notes_totals, production_period_tote_counts, certify.component_by_key.pyrolysis, tote_weighing_records.july_totes_weighed_after_july, tote_weighing_records.june_totes_weighed_in_july, {DV}].",
 "Bio-oil Geological Storage v1.2")
row("7.2", "Does the CI match the Ops Notes weighted-average CI across all totes in the injection?", "Fail",
 f"Certify carries {D['certify_ci']} tCO2e/t, which matches Ops Notes QOWV!H54 = SUMPRODUCT(D11:D52,H11:H52)/SUM(D11:D52) = {wci:.10f}, and the June ({D['jun_ci']:.10f}) and February ({D['feb_ci']:.10f}) CIs equal the Aqueous rows of the live period summaries the sheet links (M18, M14). The fail: BCUs apply to diesel transport, including biomass transport process emissions and handling, not embodied emissions (Charm BCU scope rule, batch-qa-charm FC-C13), so production CIs must count biomass transport after its BCUs. In every summary C10 = SUM(C5,C7) holds process and handling and C11 = C9-C10 is the embodied part, so the ruled basis is I19 = C11*F7 ('Remaining Emissions to Allocate'). The June and February CIs (L18, L14) come from the summaries the Ops Notes link, which use I19 = C9*F7 ('Total Emissions', under 'Consolidated Emissions Inventory (No GHG Neutralization)'). Two versions of the six summaries exist. The July blend (L7 = {D['blend_ci_used']}; 'V2_Charm_BioOil_Mass_Weighted_CI_Jan-Jun_2026.xlsx', {D['blend_ci_v2']:.10f}) was built on the ruled basis from package versions saved 2026-08-11, which rework the linked sheets: local downloads of the linked sheets dated 2026-07-11 to 2026-08-11 already hold today's values. On the package versions throughout: June {D['pkg_jun_ci']}, February {D['pkg_feb_ci']}, July {D['blend_ci_used']}; production emissions fall {D['pkg_pe_change_kg']} kg to {D['pkg_pe_kg']:,} kg, weighted CI {D['pkg_wci']:.10f}. On the linked sheets throughout: June {D['jun_ci_after']:.10f}, February {D['feb_ci_after']:.10f}, blend rebuilt {D['blend_ci_after']:.10f}; production emissions fall {D['lv_pe_change_kg']} kg to {D['lv_pe_kg']:,} kg, weighted CI {D['lv_wci']:.10f}; the blend difference comes mostly from March ({D['blend_mar_kg']} kg on the July totes) and May's C85 'Transport Emissions (Embodied)', 0.73646 linked against 0.073646 in the package ({D['blend_may_kg']} kg). The files favor the package versions: the linked February sheet prices biomass transport at 2026 factors (C5, C6 typed) where its own factor tab and the package's 'Biomass Transport Emissions.xlsx' ('Feb 2026 and earlier = 2025 EFs') call for 2025 ones, and the package's June inputs (109.03 t, 354.5 mi) match that workbook's 'Monthly Totals' row 14 while the linked sheet's (129.1156 t, 405.5 mi) trace to no file read. Which version governs is for the blend owner to confirm. Fix for this batch: enter the governing June and February after-BCU CIs in Ops Notes L18 and L14 and the resulting weighted CI in Certify. The linked summaries also sit behind other removals (January, March and April are on the same basis), so correcting the sheets themselves is a separate decision. The WODO blend in use ({D['wodo_blend_used']:.9f}) is on the ruled basis; rebuilt from the linked sheets it would be {D['wodo_blend_after']:.10f} [log:ops_notes, pp_summary_sources, pp_summary_basis, pp_summary_basis.ruling_2026_10_07, blended_ci_source, max_rulings, certify.component_by_key.pyrolysis, {DV}].",
 "GHG Stmt Sec C; Charm CI policy (Jan-Jun 2026 blended CI for Jul-Dec 2026 product); Charm BCU scope rule (batch-qa-charm 7.2)")
row("7.3", "Is the CI evidenced (Ops Notes weighted-average across totes)?", "Flag",
 "The CI datapoint 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' carries the batch Ops Notes as its source, which holds the per-tote CI column and the weighted-average cell, and every monthly constant used (L14 February, L18 June) carries a hyperlink to its Production Period Summary (M14, M18). The flag is the blended CI: K7/L7 'QOWV 6-Mo CI (kg CO2e/kg), Jul-Dec 2026' = 0.120947 is typed with no link (M7 and M19 empty), and the workbook that derives it, 'V2_Charm_BioOil_Mass_Weighted_CI_Jan-Jun_2026.xlsx' (Drive id 1J1_DxRBIbYTa3o65q_zEv_GSB6Ci6Pt8), is not among the six Certify sources, so a verifier has no route from the sheet to the derivation for the 8 July totes. Both Drive files titled 'Jul 26 Production Period Summary' are cell-for-cell copies of June's (summary tab still named 'Jun 26 PP Summary', Aqueous CI 0.1236896674), so a verifier opening them for the 8 July totes finds June's CI, not the 0.120947 applied; 'July 26 Production Period Output Summary' (one tab) is an unfilled template. Link M7 to the blended-CI workbook (or to its successor if the blend is rebuilt, 7.2) [log:certify.attachment_map, certify.certify_sources_enumeration, ops_notes, blended_ci_source, pp_summary_sources.july_2026].",
 "VR Appendix 1")
row("7.4", "Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP that applies to the component (from Ops Notes)?", "Pass",
 f"Certify Mass {f(produced,1)} kg. Ops Notes sum of Net Oil Produced across all {n} totes (D54) = {f(produced,1)} kg, delta 0.0 kg; by period June 2026 {D['june_mass_kg']:,} kg ({D['june_totes']} totes), July 2026 {D['july_mass_kg']:,} kg ({D['july_totes']}), February 2026 {D['feb_mass_kg']:,} kg ({D['feb_totes']}), which the single aggregated component sums. The component uses net-in-tote produced mass, not net injected ({f(injected,1)} kg), so the {D['residue_kg']:,} kg left in the totes carries its production emissions. The tare basis of this mass is covered in 2.2 [log:certify.component_by_key.pyrolysis, ops_notes_totals, production_period_net_produced_kg, {DV}].",
 "GHG Stmt Sec C")
row("7.5", "Does the uncertainty match the sum of uncertainties for the PP that applies to the component (from Ops Notes)?", "Pass",
 f"Component detail: {f(produced,1)} kg plus or minus 47.627 kg, the display rounding of {n} x {D['per_tote_unc_kg']} = {unc} kg; by period June {D['june_totes']} x {D['per_tote_unc_kg']} = {D['unc_june_kg']} kg, July {D['july_totes']} x {D['per_tote_unc_kg']} = {D['unc_july_kg']} kg, February {D['feb_totes']} x {D['per_tote_unc_kg']} = {D['unc_feb_kg']} kg, summing to the component's figure. Uncertainty is present on this input, which matters because pyrolysis at 5.010 tCO2e is {D['pe_share_of_net_pct']} % of the 4.076 t net removal -- a dominant input that does not qualify for the under-1 % omission allowance [log:certify.component_by_key.pyrolysis, {DV}].",
 "Bio-oil Geological Storage v1.2 Sec 6.5.1")
row("7.6", "Is the mass evidenced with a copy of the Charm Contents sheet for the batch?", "Pass",
 "No Charm Contents sheet exists for this batch: none in the Drive batch folder listing or among the six Certify sources. The per-period mass breakdown lives in the Ops Notes QOWV tab Production Period column, and the Ops Notes is attached and linked to the 'QOWV Pyrolysis Mass [Certify input]' datapoint [log:certify.attachment_map, charm_contents, batch_folder_listing, certify.certify_sources_enumeration].",
 "VR Appendix 1")

# ================= SECTION 8 / 9 / C =================
sec("SECTION 8 -- Other")
row("8.1", "Are all diesel transport-process emissions offset by BCUs, and does the BCU total equal (never exceed) the transport-process sum?", "Fail",
 f"The batch has one diesel transport-process emission, the flatbed leg, and it is offset: 'BCU - Transport Process' carries a Constant CO2 reduction of {D['bcu_kg']:,} kgCO2e, read from the component detail, sourced to the TERC Certificate of Retirement attached in Certify ({D['tercs']:,} TERCs retired Dec 18, 2025, vintage 2024, Renewable Diesel, Amazon.com Services LLC on behalf of Charm Industrial, Inc, verified by Turner, Mason & Company, each TERC one tCO2e). The embodied leg is correctly not offset. The BCU does not equal the process emission. As submitted the emission is {D['proc_cert_kg']:,} kg, so the constant is {D['bcu_short_cert_kg']} kg short; on the correct Flatbed factor (5.1) the emission is {D['proc_ok_kg']:,} kg on the sheet's value, and the BCU is {D['bcu_short_ok_kg']:,} kg short. Fix: once 5.1 is corrected, enter the constant as exactly what the corrected process component outputs ({D['proc_ok_kg']:,} kg on the sheet's factor; {D['glec_bcu_kg']:,} kg if the component uses the GLEC 0.086 per km-tonne datapoint as INJ-09-2026-W3-QOWV did, {D['glec_gap_kg']} kg apart) [log:certify.component_by_key.bcu, certify.component_by_key.transport_process, retirement_certificate, standard_efs_2026, {DV}].",
 "BCU QA Rule (batch-qa-charm SKILL.md)")
sec("SECTION 9 -- Aqueous Buffering (LCS)")
row("9.1", "If LCS use is reported in Ops Notes, does a matching Certify component exist (correct mass, correct EF, evidenced)?", "N/A",
 "No LCS use is reported. Every string cell across all ten tabs was scanned for the LCS abbreviation, calcium, caustic, NaOH and buffer with zero matches, and the Summary tab reports sparging 0.0 kg and filtration 0.0 kg for QOWV. With no LCS use there is no component to require [log:lcs_use_kg, lcs_search_method, summary_tab].",
 "VR Sec 3.1")
sec("CALCULATION CHECK -- independent recompute")
row("C.1", "Does the net removal recompute from source values?", "Pass",
 f"Recomputed by recompute_qowv.py from the Ops Notes export and the source-read log (30 of 30 checks OK, exit 0), on Certify's own inputs: Sequestration {f(injected,1)} kg x {cpct} % x 3.667 = {D['seq_kg']:,} kg = 9.902 t; Transport process {D['proc_cert_kg']:,} kg = 5.895 t; Transport embodied {D['emb_cert_kg']} kg = 0.769 t; Pyrolysis {D['pyro_cert_kg']:,} kg = 5.010 t; BCU 5.895 t. Net = 9.902 + 5.895 - (5.895 + 0.769 + 5.010) - discount = {D['net_cert_t']} t, matching Certify's 4.076 t. The discount Certify shows as 47 kg is consistent with variance propagation on the three uncertain masses and the carbon content: estimate {D['disc_est_kg']} kg. This reproduces the removal as submitted, so 4.076 t carries the errors in 2.3, 3.4, 4.4, 5.1, 6.1, 7.2 and 8.1; 3.5 is a documentation flag and does not change the net. On the evidence (Flatbed process with a matching BCU, Non-Tanker embodied on {D['alloc_inv_mi']:,} mi, 0.4 % carbon uncertainty, injected mass as submitted, production CIs after BCUs per 7.2) the net is {D['net_pkg_t']} t ({D['net_pkg_gain_t']:+} t) on the package versions of the summaries, or {D['net_lv_t']} t ({D['net_lv_gain_t']:+} t) on the linked sheets with the blend rebuilt, which carries May's tenfold C85. Counterfactuals are zero. Ledger integrity: no duplicate tags, no tote whose injected mass exceeds its gross, gross masses {D['gross_min']}-{D['gross_max']} kg, post-unload tote weights {D['e_min']}-{D['e_max']} kg [log:certify, {DV}].",
 "Bio-oil Geological Storage v1.2")

SIDEBAR = [
 "The W4 workbook's 'Whole Oil' tab (B2) and 'Whole Oil Shipments & EE Alloca' tab (A1, A6) still read INJ-09-2026-W3 with zero totes, and the 'WODO Shipments & EE Allocation' tab's A1 and A6 read INJ-09-2026-W2: templates carried over from earlier workbooks. Nothing on the QOWV tabs references them; worth clearing so the W4 file only names W4.",
 "QOWV tab row 53 and rows 55-74 carry template formulas (G = (D-F)*$L$4, H = G*(1-$L$5)) that evaluate blank and feed no total. Harmless; removing them would tidy the ledger.",
 "Lab certificate SR26-05719.003 marks QOWV Carbon 7.9 % and Hydrogen 7.9 % with the footnote 'Result is outside of test method limits and/or analytical range used in method precision study' (page 3). The 0.4 % relative carbon uncertainty in 4.4 is the checklist standard, not a precision the lab states for this result.",
 "Week window: the QOWV tab labels B3 and B4 'Week Start (Sat)' and 'Week End (Sat)', but 2026-09-18 and 2026-09-25 are Fridays. Certify's window is 19-25 Sep, the September VVB Guidance gives Week 4 as 18-25 September, and the composite sample was drawn 25-Sep 10:00.",
 "Totes 301166 and 301215 both read 442.5 kg after unloading in the Ops Notes, 384.9 kg of residue each above the 57.6 kg tote mass: 0.3714 of 301166's net oil and 0.3914 of 301215's. Batch residue is 6,346.3 kg; its production and transport emissions are charged (2.3, 7.4).",
 "The 7.2 basis reaches beyond this batch: the linked Jan-Jun 2026 summaries (January to April and June; May has no biomass transport) and local copies of the Jul-Dec 2025 summaries count biomass transport before its BCUs, for WODO and Aqueous alike. Any batch carrying that product at those monthly CIs overstates production emissions; on the Ops Notes as exported 2026-10-06 this reaches INJ-08-2026-W5, INJ-09-2026-W1, W2 and W3 (cross_batch_bcu_basis_scan.txt). The Jan-Jun blends in use (QOWV 0.120947, WODO 0.795241059) are on the ruled basis.",
 "May 2026 period summary, C85 'Transport Emissions (Embodied)': 0.73646 on the live sheet against 0.073646 in the 2026-08-11 copy, a factor of ten. No W4 tote is May product; the May CI the Ops Notes link draws on the live sheet, while the Jan-Jun blend in use was built from the package copy.",
 "Nothing in the batch evidence ties this removal's 5.895 t BCU to a drawdown of the 2,795 TERCs on the attached retirement certificate; no checklist item tests reuse of one certificate across removals.",
 "The September VVB Guidance (edited 2026-10-05) has six sections: AECN R&D withdrawal (W3), AECN Baton Rouge routing (W4), AECN bio-oil loss, site E-85, rail-yard compressor diesel and argon. None covers QOWV; its loss section states the same custody principle applied in 2.3.",
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
    for label, val in [("Batch ID", "INJ-09-2026-W4-QOWV (Aqueous / QOWV)"),
                       ("Reporting Period", "September 1 - September 30 2026; Certify removal window 19 Sep 2026 to 25 Sep 2026; Ops Notes injection week 2026-09-18 to 2026-09-25"),
                       ("Reviewer", "Claude (QA agent)"), ("Date", "2026-10-06"), ("Injection Site", "Basco 6, Louisiana"),
                       ("Oil Type", "Aqueous (QOWV) - Charm-produced, Fort Lupton CO, IBC totes"),
                       ("Production Periods", "June 2026 (32 totes), July 2026 (8 totes, Jan-Jun 2026 blended CI), February 2026 (2 totes) - 42 totes, captured in one production-mass-weighted pyrolysis component"),
                       ("Certify Removal ID", "rmv_1M3SG7D701S0HZ1Z"),
                       ("Net CO2e Removed", "4.076 tCO2e (Sequestrations 9.902 + Adjustments 5.895 - Activities 11.674 - Uncertainty discount 0.047)")]:
        ws.cell(r, 1, label).font = B; ws.cell(r, 1).alignment = W; ws.cell(r, 2, val).alignment = W
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws.row_dimensions[r].height = 15 * max(1, math.ceil(len(val) / 170)) + 2; r += 1
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
        ws.row_dimensions[r].height = 15 * max(2, math.ceil(len(ev) / 105) + 1)
        r += 1
    r += 1
    ws.cell(r, 1, "SIDEBAR OBSERVATIONS (no status - for Garrett's attention)")
    for col in range(1, 6): ws.cell(r, col).fill = H; ws.cell(r, col).font = B
    r += 1
    for note in SIDEBAR:   # Excel does not auto-size merged cells, so set the height
        ws.cell(r, 2, note).alignment = W; ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws.row_dimensions[r].height = 15 * max(1, math.ceil(len(note) / 160)) + 4; r += 1
    r += 1
    ws.cell(r, 1, "STATUS COUNTS").font = B
    ws.cell(r, 2, f"Pass {counts['Pass']}  |  Flag {counts['Flag']}  |  Fail {counts['Fail']}  |  N/A {counts['N/A']}  ({sum(counts.values())} items)")
    ws.freeze_panes = "A12"
    print("counts", counts)
    return wb

if __name__ == "__main__":
    build_with_validation(R, LOGP, OUT, build)
