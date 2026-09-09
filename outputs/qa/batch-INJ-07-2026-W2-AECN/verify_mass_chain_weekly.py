#!/usr/bin/env python3
"""Deterministic arithmetic check for a weekly time-block AECN rail batch.

The pilot compute_mass_chain.py assumes the single-offload (2-1XX era) shape:
one offload, one railcar, one scale-ticket pair at fixed flat keys. A weekly
time-block batch aggregates N offloads across M railcars, so those keys do not
exist. This script performs the equivalent checks against the weekly shape,
recomputing every value in the chain from the logged primary-source readings.

Every number the checklist cites is emitted into _derived_values.
"""
import json
import sys
from pathlib import Path

LOG = Path(sys.argv[1] if len(sys.argv) > 1 else
           "outputs/qa/batch-INJ-07-2026-W2-AECN/batch_INJ-07-2026-W2_source_reads.json")
TOL = 0.01          # kg / mi tolerance on reconstructed sums
TOL_T = 0.0011      # tCO2e tolerance (Certify displays 3 dp)

log = json.loads(LOG.read_text())
KG_PER_LB = log["ops_notes"]["constants"]["kg_per_lb"]
SPARGE = log["ops_notes"]["constants"]["sparging_mass_loss"]
FILTER = log["ops_notes"]["constants"]["filtration_solids_content"]
N_BOL_TRIPS = log["ops_notes"]["constants"]["bol_trips_aecn_to_sopor"]
ROUND_TRIP = log["ops_notes"]["constants"]["round_trip_opel_to_basco"]

results, derived = [], {}


def kid(offload_id):
    """Derived-key-safe offload tag: dots break dot-notation path lookup."""
    return offload_id.replace("Rail_", "").replace(".", "_")


def check(cid, ok, computed, logged, note=""):
    results.append({"check_id": cid, "status": "PASS" if ok else "FAIL",
                    "computed": computed, "logged": logged, "note": note})


tickets = {p["offload"]: p for p in log["scale_tickets"]["pairs"]}
offloads = log["ops_notes"]["offload_table"]
railcars = {r["railcar"]: r for r in log["ops_notes"]["railcars_received"]}
bols = log["bols"]["bols_into_railcar"]

# ---- 1. per-offload scale-ticket subtraction, ticket PDF -> Ops Notes ----
for o in offloads:
    t = tickets[o["id"]]
    net_lb = t["full_ticket"]["gross_weight_lb"] - t["empty_ticket"]["gross_weight_lb"]
    net_kg = net_lb * KG_PER_LB
    check(f"ticket_subtraction::{o['id']}",
          abs(net_lb - t["computed_net_lb"]) < TOL and abs(net_kg - o["net_scaled_kg"]) < TOL,
          {"net_lb": net_lb, "net_kg": round(net_kg, 5)},
          {"ops_notes_net_scaled_kg": o["net_scaled_kg"]},
          f"({t['full_ticket']['gross_weight_lb']} - {t['empty_ticket']['gross_weight_lb']}) x {KG_PER_LB}")
    derived[f"net_lb_{kid(o['id'])}"] = net_lb
    derived[f"net_kg_{kid(o['id'])}"] = round(net_kg, 5)
    # tractor/trailer identity
    check(f"rig_match::{o['id']}",
          t["full_ticket"]["tractor"] == t["empty_ticket"]["tractor"]
          and t["full_ticket"]["trailer"] == t["empty_ticket"]["trailer"],
          {"full": f"{t['full_ticket']['tractor']}/{t['full_ticket']['trailer']}"},
          {"empty": f"{t['empty_ticket']['tractor']}/{t['empty_ticket']['trailer']}"})

# ---- 2. BOL aggregate per railcar ----
for rc, r in railcars.items():
    agg = sum(b["mass_kg"] for b in bols if b["railcar"] == rc)
    check(f"bol_aggregate::{rc}", abs(agg - r["total_loaded_kg"]) < TOL,
          {"sum_bol_kg": agg}, {"ops_notes_total_loaded_kg": r["total_loaded_kg"]},
          " + ".join(f"{b['mass_kg']}" for b in bols if b["railcar"] == rc))
    derived[f"bol_aggregate_{rc}_kg"] = agg
    n_bols = sum(1 for b in bols if b["railcar"] == rc)
    n_off = sum(1 for o in offloads if o["railcar"] == rc)
    derived[f"n_bols_{rc}"] = n_bols
    derived[f"n_offloads_this_week_{rc}"] = n_off

# ---- 3. railcar draw-down balance and FC11 last-offload adjustment ----
for rc, r in railcars.items():
    raw = sum(o["net_scaled_kg"] for o in offloads if o["railcar"] == rc)
    adj = sum(o["uncertainty_adjustment_kg"] for o in offloads if o["railcar"] == rc)
    derived[f"raw_offload_sum_{rc}_kg"] = round(raw, 5)
    derived[f"uncertainty_adjustment_{rc}_kg"] = round(adj, 5)
    check(f"total_offloaded::{rc}", abs(raw - r["total_offloaded_kg"]) < TOL,
          {"sum_raw_nets_kg": round(raw, 5)}, {"ops_notes_total_offloaded_kg": r["total_offloaded_kg"]})
    if r["fully_drawn_this_week"]:
        overdraw = raw - r["total_loaded_kg"]
        derived[f"overdraw_{rc}_kg"] = round(overdraw, 5)
        check(f"fc11_backcalc::{rc}", abs(adj - overdraw) < TOL,
              {"overdraw_kg": round(overdraw, 5)}, {"applied_adjustment_kg": round(adj, 5)},
              f"{round(raw,5)} raw - {r['total_loaded_kg']} BOL aggregate")
        check(f"claimed_equals_bol::{rc}", abs((raw - adj) - r["claimed_this_week_kg"]) < TOL,
              {"raw_minus_adj_kg": round(raw - adj, 5)},
              {"claimed_this_week_kg": r["claimed_this_week_kg"]})
    else:
        check(f"partial_draw_no_adjustment::{rc}", adj == 0,
              {"adjustment_kg": adj}, {"fully_drawn": r["fully_drawn_this_week"]},
              "railcar not fully drawn this week; FC11 back-calc applies at its closing offload")

# ---- 4. per-offload sparging / filtration / MOBI ----
for o in offloads:
    base = o["net_scaled_kg"] - o["uncertainty_adjustment_kg"]
    sp = base * SPARGE
    post_sp = base - sp
    fl = post_sp * FILTER
    mobi = post_sp - fl
    check(f"sparge_filter_mobi::{o['id']}",
          abs(sp - o["sparging_loss_kg"]) < TOL and abs(fl - o["filtration_loss_kg"]) < TOL
          and abs(mobi - o["mobi_kg"]) < TOL,
          {"sparging_kg": round(sp, 5), "filtration_kg": round(fl, 5), "mobi_kg": round(mobi, 5)},
          {"ops_sparging": o["sparging_loss_kg"], "ops_filtration": o["filtration_loss_kg"],
           "ops_mobi": o["mobi_kg"]},
          f"base {round(base,5)} x {SPARGE} sparge, then x {FILTER} filtration")
    derived[f"sparging_kg_{kid(o['id'])}"] = round(sp, 5)
    derived[f"filtration_kg_{kid(o['id'])}"] = round(fl, 5)
    derived[f"post_adj_kg_{kid(o['id'])}"] = round(base, 5)
    derived[f"mobi_kg_{kid(o['id'])}"] = round(mobi, 5)

# ---- 5. weekly rollups ----
roll = log["ops_notes"]["rollup_section4"]
downstream = sum(o["net_scaled_kg"] for o in offloads)
adj_total = sum(o["uncertainty_adjustment_kg"] for o in offloads)
mass_used = downstream - adj_total
sparge_total = sum(o["sparging_loss_kg"] for o in offloads)
filter_total = sum(o["filtration_loss_kg"] for o in offloads)
mobi_total = sum(o["mobi_kg"] for o in offloads)
derived.update({
    "downstream_scale_ticket_sum_kg": round(downstream, 5),
    "uncertainty_adjustment_total_kg": round(adj_total, 5),
    "mass_used_post_adj_kg": round(mass_used, 5),
    "sparging_loss_total_kg": round(sparge_total, 5),
    "filtration_loss_total_kg": round(filter_total, 5),
    "mobi_total_kg": round(mobi_total, 5),
})
check("rollup_downstream", abs(downstream - roll["deliveries_raw_downstream_scale_tickets_kg"]) < TOL,
      {"sum_kg": round(downstream, 5)}, {"ops": roll["deliveries_raw_downstream_scale_tickets_kg"]})
check("rollup_mass_used", abs(mass_used - roll["mass_used_post_adj_kg"]) < TOL,
      {"kg": round(mass_used, 5)}, {"ops": roll["mass_used_post_adj_kg"]},
      f"{round(downstream,5)} - {round(adj_total,5)}")
check("rollup_mobi", abs(mobi_total - roll["mobi_kg"]) < TOL,
      {"kg": round(mobi_total, 5)}, {"ops": roll["mobi_kg"]},
      f"{round(mass_used,5)} - {round(sparge_total,5)} - {round(filter_total,5)}")

# ---- 6. embodied allocated distances ----
ee = log["ops_notes"]["ee_totals_row48"]
full_truck = railcars[offloads[0]["railcar"]]["aecn_sopor_mi"]
full_rail = railcars[offloads[0]["railcar"]]["rail_mi"]
full_opel = railcars[offloads[0]["railcar"]]["opel_basco_mi"]
truck_sum = rail_sum = opel_sum = 0.0
for o in offloads:
    rc = railcars[o["railcar"]]
    post = o["net_scaled_kg"] - o["uncertainty_adjustment_kg"]
    frac = post / rc["total_loaded_kg"]
    t_mi = full_truck * N_BOL_TRIPS * frac
    r_mi = full_rail * frac
    o_mi = full_opel * ROUND_TRIP
    check(f"alloc_distance::{o['id']}",
          abs(t_mi - o["aecn_sopor_ee_mi"]) < TOL and abs(r_mi - o["rail_ee_mi"]) < TOL
          and abs(o_mi - o["opel_basco_ee_mi"]) < TOL,
          {"truck_mi": round(t_mi, 5), "rail_mi": round(r_mi, 5), "opel_mi": o_mi},
          {"ops_truck": o["aecn_sopor_ee_mi"], "ops_rail": o["rail_ee_mi"],
           "ops_opel": o["opel_basco_ee_mi"]},
          f"fraction {round(frac,7)} = {round(post,5)} / {rc['total_loaded_kg']}")
    derived[f"alloc_fraction_{kid(o['id'])}"] = round(frac, 7)
    truck_sum += t_mi; rail_sum += r_mi; opel_sum += o_mi
derived.update({"aecn_sopor_alloc_mi_total": round(truck_sum, 5),
                "rail_alloc_mi_total": round(rail_sum, 5),
                "opel_basco_alloc_mi_total": round(opel_sum, 5)})
check("ee_total_truck", abs(truck_sum - ee["aecn_sopor_mi"]) < TOL,
      {"mi": round(truck_sum, 5)}, {"ops": ee["aecn_sopor_mi"]})
check("ee_total_rail", abs(rail_sum - ee["rail_mi"]) < TOL,
      {"mi": round(rail_sum, 5)}, {"ops": ee["rail_mi"]})
check("ee_total_opel", abs(opel_sum - ee["opel_basco_mi"]) < TOL,
      {"mi": round(opel_sum, 5)}, {"ops": ee["opel_basco_mi"]})

# ---- 7. COBB reconciliation ----
cobb_rows = {r["consumed_lot"]: r for r in log["cobb"]["rows"]}
for o in offloads:
    c = cobb_rows[o["id"]]
    post = o["net_scaled_kg"] - o["uncertainty_adjustment_kg"]
    check(f"cobb_offload::{o['id']}", abs(c["offloaded_quantity_kg"] - post) < TOL,
          {"ops_post_adj_kg": round(post, 5)}, {"cobb_offloaded_kg": c["offloaded_quantity_kg"]})
for rc, r in railcars.items():
    origin = {c["origin_quantity_kg"] for c in log["cobb"]["rows"]
              if c["consumed_lot"].split("_")[1] == rc}
    check(f"cobb_origin::{rc}", origin == {float(r["total_loaded_kg"])},
          {"ops_total_loaded_kg": r["total_loaded_kg"]}, {"cobb_origin_quantity_kg": sorted(origin)})

# ---- 8. Certify components recomputed ----
c = log["certify"]["components"]
ef = log["ef_live_source"]
mass_used_t = mass_used / 1000
downstream_t = downstream / 1000
mobi_t = mobi_total / 1000
carbon = log["lab_results"]["carbon_pct"] / 100

gross = mobi_t * carbon * 3.667
derived["gross_co2e_recalc_t"] = round(gross, 5)
check("certify_sequestration", abs(gross - c["Injection sequestration"]) < TOL_T,
      {"t": round(gross, 5)}, {"certify": c["Injection sequestration"]},
      f"{round(mobi_t,5)} t x {carbon} x 3.667")

pyro_p = mass_used_t * 0.104
derived["pyrolysis_process_recalc_t"] = round(pyro_p, 5)
check("certify_pyrolysis_process", abs(pyro_p - c["AECN pyrolysis (from rail loads) - process emissions"]) < TOL_T,
      {"t": round(pyro_p, 5)}, {"certify": c["AECN pyrolysis (from rail loads) - process emissions"]},
      f"{round(mass_used_t,5)} t x 0.104 tCO2e/t (Certify stored CI)")
pyro_p_sheet = mass_used_t * ef["aecn_process_row3"]["final_quantity"]
derived["pyrolysis_process_at_sheet_final_ef_t"] = round(pyro_p_sheet, 5)
derived["pyrolysis_process_ef_rounding_delta_t"] = round(pyro_p_sheet - pyro_p, 5)

pyro_e = mass_used_t * ef["aecn_embodied_row4"]["final_quantity"]
derived["pyrolysis_embodied_recalc_t"] = round(pyro_e, 5)
check("certify_pyrolysis_embodied", abs(pyro_e - c["AECN pyrolysis (from rail loads) - embodied emissions"]) < TOL_T,
      {"t": round(pyro_e, 5)}, {"certify": c["AECN pyrolysis (from rail loads) - embodied emissions"]},
      f"{round(mass_used_t,5)} t x {ef['aecn_embodied_row4']['final_quantity']} tCO2e/t")

truck_p = mass_used_t * log["routes"]["aecn_to_sopor_mi_converted"] * ef["truck_fuel_row5"]["final_quantity"]
derived["aecn_sopor_truck_process_recalc_t"] = round(truck_p, 5)
check("certify_truck_process", abs(truck_p - c["AECN to SOPOR Tanker Truck Transport Process Emissions"]) < TOL_T,
      {"t": round(truck_p, 5)}, {"certify": c["AECN to SOPOR Tanker Truck Transport Process Emissions"]},
      f"{round(mass_used_t,5)} t x 107.49722 mi x 0.0001143 MTCO2e/(t.mi)")

rail_p = mass_used_t * log["routes"]["rail_sopor_to_opelousas_mi"] * ef["rail_fuel_row9"]["final_quantity"]
derived["rail_process_recalc_t"] = round(rail_p, 5)
check("certify_rail_process", abs(rail_p - c["SOPOR to Opelousas Rail Transport Process Emissions"]) < 0.002,
      {"t": round(rail_p, 5)}, {"certify": c["SOPOR to Opelousas Rail Transport Process Emissions"]},
      f"{round(mass_used_t,5)} t x 2199 mi x 2.5910374e-05 MTCO2e/(t.mi)")

opel_p = downstream_t * log["routes"]["opelousas_to_basco_mi_longest"] * ef["truck_fuel_row5"]["final_quantity"]
derived["opel_basco_truck_process_recalc_t"] = round(opel_p, 5)
check("certify_opel_process", abs(opel_p - c["Opelousas to Basco - Tanker Truck Transport Process Emissions"]) < TOL_T,
      {"t": round(opel_p, 5)}, {"certify": c["Opelousas to Basco - Tanker Truck Transport Process Emissions"]},
      f"{round(downstream_t,5)} t (downstream) x 42.9 mi x 0.0001143 MTCO2e/(t.mi)")

truck_e = truck_sum * ef["tanker_truck_embodied_row10"]["final_quantity"]
derived["aecn_sopor_truck_embodied_recalc_t"] = round(truck_e, 5)
check("certify_truck_embodied", abs(truck_e - c["AECN to SOPOR Tanker Truck Transport Embodied Emissions"]) < TOL_T,
      {"t": round(truck_e, 5)}, {"certify": c["AECN to SOPOR Tanker Truck Transport Embodied Emissions"]},
      f"{round(truck_sum,5)} mi x 0.0002375605888 MTCO2e/mi")

rail_e = rail_sum * ef["railcar_embodied_row12"]["final_quantity"]
derived["rail_embodied_recalc_t"] = round(rail_e, 5)
check("certify_rail_embodied", abs(rail_e - c["SOPOR to Opelousas Rail Transport Embodied Emissions"]) < TOL_T,
      {"t": round(rail_e, 5)}, {"certify": c["SOPOR to Opelousas Rail Transport Embodied Emissions"]},
      f"{round(rail_sum,5)} mi x 3.113066508e-05 MTCO2e/mi")

opel_e = opel_sum * ef["tanker_truck_embodied_row10"]["final_quantity"]
derived["opel_basco_truck_embodied_recalc_t"] = round(opel_e, 5)
check("certify_opel_embodied", abs(opel_e - c["Opelousas to Basco Tanker Truck Transport Embodied Emissions"]) < TOL_T,
      {"t": round(opel_e, 5)}, {"certify": c["Opelousas to Basco Tanker Truck Transport Embodied Emissions"]},
      f"{round(opel_sum,5)} mi x 0.0002375605888 MTCO2e/mi")

# ---- 9. transport sums, BCU adequacy, net ----
tp_sum = (c["AECN to SOPOR Tanker Truck Transport Process Emissions"]
          + c["SOPOR to Opelousas Rail Transport Process Emissions"]
          + c["Opelousas to Basco - Tanker Truck Transport Process Emissions"])
te_sum = (c["AECN to SOPOR Tanker Truck Transport Embodied Emissions"]
          + c["SOPOR to Opelousas Rail Transport Embodied Emissions"]
          + c["Opelousas to Basco Tanker Truck Transport Embodied Emissions"])
derived["transport_process_sum_t"] = round(tp_sum, 5)
derived["transport_embodied_sum_t"] = round(te_sum, 5)
derived["transport_total_t"] = round(tp_sum + te_sum, 5)
bcu = c["BCU - Transport Process"]
derived["bcu_constant_t"] = bcu
derived["bcu_surplus_over_transport_process_t"] = round(bcu - tp_sum, 5)
derived["pyrolysis_process_t_for_comparison"] = c["AECN pyrolysis (from rail loads) - process emissions"]
check("bcu_equals_transport_process", abs(bcu - tp_sum) < TOL_T,
      {"transport_process_sum_t": round(tp_sum, 5)}, {"bcu_constant_t": bcu},
      f"{c['AECN to SOPOR Tanker Truck Transport Process Emissions']} + "
      f"{c['SOPOR to Opelousas Rail Transport Process Emissions']} + "
      f"{c['Opelousas to Basco - Tanker Truck Transport Process Emissions']}")

activities = (c["AECN pyrolysis (from rail loads) - process emissions"]
              + c["AECN pyrolysis (from rail loads) - embodied emissions"] + tp_sum + te_sum)
derived["activities_recalc_t"] = round(activities, 5)
check("certify_activities_total", abs(activities - log["certify"]["calculation_view"]["activities_t"]) < TOL_T,
      {"t": round(activities, 5)}, {"certify": log["certify"]["calculation_view"]["activities_t"]})

unc = log["certify"]["calculation_view"]["uncertainty_discount_kg"] / 1000
net_as_reported = c["Injection sequestration"] + bcu - activities - unc
derived["net_calc_t"] = round(net_as_reported, 5)
check("certify_net", abs(net_as_reported - log["certify"]["calculation_view"]["net_co2e_removed_t"]) < TOL_T,
      {"t": round(net_as_reported, 5)}, {"certify": log["certify"]["calculation_view"]["net_co2e_removed_t"]},
      f"{c['Injection sequestration']} + {bcu} - {round(activities,3)} - {unc}")

net_bcu_capped = c["Injection sequestration"] + tp_sum - activities - unc
derived["net_if_bcu_capped_at_transport_process_t"] = round(net_bcu_capped, 5)
derived["net_overstatement_from_bcu_t"] = round(net_as_reported - net_bcu_capped, 5)
derived["net_overstatement_from_bcu_pct"] = round(
    100 * (net_as_reported - net_bcu_capped) / net_as_reported, 4)

# ---- 10. uncertainty reconstruction (Option B variance propagation) ----
rel_mass = 362.85 / mobi_total
rel_carbon = 0.1664 / 41.6
var = (gross * (rel_mass ** 2 + rel_carbon ** 2) ** 0.5) ** 2
for val, m in ((c["AECN pyrolysis (from rail loads) - process emissions"], mass_used),
               (c["AECN pyrolysis (from rail loads) - embodied emissions"], mass_used),
               (c["AECN to SOPOR Tanker Truck Transport Process Emissions"], mass_used),
               (c["SOPOR to Opelousas Rail Transport Process Emissions"], mass_used),
               (c["Opelousas to Basco - Tanker Truck Transport Process Emissions"], downstream)):
    var += (val * 362.85 / m) ** 2
sigma = var ** 0.5
derived["uncertainty_1sigma_reconstructed_kg"] = round(sigma * 1000, 1)
derived["uncertainty_discount_reported_kg"] = log["certify"]["calculation_view"]["uncertainty_discount_kg"]
derived["mass_uncertainty_kg"] = round(5 * 72.57, 2)
check("uncertainty_reconstruction",
      abs(sigma * 1000 - log["certify"]["calculation_view"]["uncertainty_discount_kg"]) < 3,
      {"reconstructed_1sigma_kg": round(sigma * 1000, 1)},
      {"certify_discount_kg": log["certify"]["calculation_view"]["uncertainty_discount_kg"]},
      "Option B variance propagation on carbon 0.4% + mass +/-362.85 kg (5 weighings x 72.57)")

derived["carbon_uncertainty_abs"] = 0.1664
derived["carbon_uncertainty_rate"] = 0.004
derived["per_weighing_uncertainty_kg"] = 72.57

out = {"batch_id": log["batch_id"], "checks": results, "derived": derived}
Path(str(LOG.parent / "weekly_mass_chain_findings.json")).write_text(json.dumps(out, indent=2))
p = sum(1 for r in results if r["status"] == "PASS")
f = sum(1 for r in results if r["status"] == "FAIL")
print(f"PASS={p}  FAIL={f}")
for r in results:
    if r["status"] == "FAIL":
        print("  FAIL:", r["check_id"], r["computed"], "vs", r["logged"], "|", r["note"])
