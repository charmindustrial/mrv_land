#!/usr/bin/env python3
"""Deterministic recompute for INJ-09-2026-W4-KERRY (rmv_1M3T2J3V51S0NCHH).

Reads batch_INJ-09-2026-W4-KERRY_source_reads.json only. Recomputes the mass chain, filtration
deduction, gross CO2e, both transport components, the BCU, the uncertainty inputs and net, and
compares each with the Certify value in the log. A difference between Certify and the evidence is
printed as 'FINDING <row>: ...' naming the checklist row that carries it. Exit 1 only if a
difference is not routed to a row, or the script cannot run.
"""
import json, math, sys
from datetime import date
from pathlib import Path

LOG = json.loads((Path(__file__).resolve().parent / "batch_INJ-09-2026-W4-KERRY_source_reads.json").read_text())
TOL_T = 0.001          # tCO2e
TOL_KG = 0.01          # kg
LB_TO_KG = LOG["ops_notes"]["constants"]["M4_kg_per_lb"]
CO2_PER_C = 3.667      # skill formula: MOBI (t) x C (decimal) x 3.667

ok_count, unrouted = 0, []


def check(label, ours, certify, tol, route=None, unit=""):
    global ok_count
    diff = ours - certify
    if abs(diff) <= tol:
        ok_count += 1
        print(f"OK   {label}: recomputed {ours:,.6f}{unit} vs Certify/evidence {certify:,.6f}{unit} (diff {diff:+.6f})")
    elif route:
        print(f"FINDING {route}: {label}: recomputed {ours:,.6f}{unit} vs Certify/evidence {certify:,.6f}{unit} (diff {diff:+.6f})")
    else:
        unrouted.append(label)
        print(f"UNROUTED {label}: recomputed {ours:,.6f}{unit} vs Certify/evidence {certify:,.6f}{unit} (diff {diff:+.6f})")


st, on, cf = LOG["scale_tickets"], LOG["ops_notes"], LOG["certify"]
comp = cf["component_by_key"]
ef = LOG["standard_efs_2026"]
lab = LOG["lab_results"]
cobb = LOG["cobb_tracker"]["w4_row"]

# ---- mass chain (tanker mode)
full_lb, empty_lb = st["full_ticket"]["gross_weight_lb"], st["empty_ticket"]["gross_weight_lb"]
assert st["full_ticket"]["tractor"] == st["empty_ticket"]["tractor"] and st["full_ticket"]["trailer"] == st["empty_ticket"]["trailer"]
net_kg = (full_lb - empty_lb) * LB_TO_KG
print(f"Ticket pair: full {full_lb:,} lb (#{st['full_ticket']['ticket_number']}, {st['full_ticket']['date']}) - empty {empty_lb:,} lb "
      f"(#{st['empty_ticket']['ticket_number']}, {st['empty_ticket']['date']}), tractor {st['full_ticket']['tractor']} / trailer {st['full_ticket']['trailer']} on both")
check("Ticket net vs Ops Notes Kerry F10", net_kg, on["kerry_row"]["F10_net_kg"], TOL_KG, unit=" kg")
check("Ticket net vs Ops Notes Summary B11 (cargo)", net_kg, on["summary"]["B11_deliveries_cargo_kg"], TOL_KG, unit=" kg")
check("Ticket net vs COBB WILA004 quantity (COBB WILA003 carries the same figure, so quantity does not identify the load; see 1.7)", net_kg, cobb["quantity_consumed_in_injection"], TOL_KG, unit=" kg")
check("Ticket net vs Certify Allocated Kerry Oil Gross Mass (4-dp display, t)", net_kg / 1000, comp["transport_process"]["mass_of_load_t"], 0.00005, unit=" t")

solids = on["constants"]["M5_filtration_solids"]
check("Ops Notes M5 vs CAR-474 MANITOWOC CALCINER PHASE", solids, LOG["filtration_constant_source"]["manitowoc_calciner_pct_solids"] / 100, 1e-12)
filt = net_kg * solids
mobi = net_kg - filt
check("Filtration loss vs Ops Notes B18", filt, on["rollup"]["B18_filtration_loss_kg"], TOL_KG, unit=" kg")
check("MOBI vs Ops Notes C18", mobi, on["rollup"]["C18_mobi_kg"], TOL_KG, unit=" kg")
check("MOBI vs Certify Mass of Injectant", mobi, comp["injection_sequestration"]["mass_of_product_kg"], TOL_KG, unit=" kg")
check("Sparging on Kerry (Summary E11) is zero", on["summary"]["E11_sparging_loss_kg"], 0.0, 1e-9, unit=" kg")

# ---- carbon + gross
c_pct = lab["carbon_pct"]
check("CoA SR26-05719.001 carbon vs Certify carbon", c_pct, comp["injection_sequestration"]["carbon_content_pct"], 1e-9, unit=" %")
check("CoA carbon vs Ops Notes Summary E19", c_pct / 100, on["summary"]["E19_c_fraction"], 1e-9)
gross = mobi / 1000 * (c_pct / 100) * CO2_PER_C
check("Gross CO2e (MOBI x C x 3.667) vs Certify Injection sequestration", gross, comp["injection_sequestration"]["value_tCO2e"], TOL_T, unit=" t")

# ---- uncertainty inputs
check("Carbon uncertainty 0.4% of 57.9 vs Certify", c_pct * 0.004, comp["injection_sequestration"]["carbon_content_pm"], 1e-9, unit=" %")
check("Mass of product uncertainty (one CAT weighing) vs Certify", 72.57, comp["injection_sequestration"]["mass_pm_kg"], 1e-9, unit=" kg")
check("Mass of load uncertainty (one CAT weighing) vs Certify", 0.07257, comp["transport_process"]["mass_of_load_pm_t"], 1e-9, unit=" t")

# ---- transport
ef_proc = ef["row6_tanker_fuel_use_mt_per_t_mi"]
ef_emb = ef["row11_tanker_embodied_mt_per_mi"]
dist = LOG["route_map"]["longest_mi"]
check("Process EF live 2026 row 6 (kg/(t.mi)) vs Certify", ef_proc * 1000, comp["transport_process"]["ef_kg_per_t_mi"], 1e-9)
check("Process EF in attached EF workbook vs live", ef["certify_attached_copy"]["row5_tanker_fuel_use"], ef_proc, 1e-15)
check("Embodied EF live 2026 row 11 (kg/mi) vs Certify (5 dp shown)", ef_emb * 1000, comp["transport_embodied"]["ef_kg_per_mi"], 0.000005)
check("Embodied EF in attached EF workbook vs live", ef["certify_attached_copy"]["row10_tanker_embodied"], ef_emb, 1e-15)
check("Distance: longest Google Maps option vs Certify process", dist, comp["transport_process"]["distance_mi"], 0)
check("Distance: longest Google Maps option vs Certify embodied", dist, comp["transport_embodied"]["distance_mi"], 0)
proc = net_kg / 1000 * dist * ef_proc
emb = dist * ef_emb
check("Transport process (mass x distance x EF) vs Certify", proc, comp["transport_process"]["value_tCO2e"], TOL_T, unit=" t")
check("Transport embodied (distance x EF) vs Certify", emb, comp["transport_embodied"]["value_tCO2e"], TOL_T, unit=" t")

# ---- BCU (must equal, never exceed, the process emission)
bcu_t = comp["bcu"]["constant_reduction_kg"] / 1000
check("BCU vs recomputed transport process", bcu_t, proc, TOL_T, unit=" t")
if bcu_t - proc > 1e-6:
    unrouted.append("BCU exceeds process emission")
    print(f"UNROUTED BCU {bcu_t:.6f} t exceeds process {proc:.6f} t")
else:
    ok_count += 1
    print(f"OK   BCU does not exceed process emission ({bcu_t*1000:,.2f} kg vs {proc*1000:,.4f} kg)")

# ---- uncertainty discount (variance propagation, 1 sigma) and net
rel_c = 0.004
rel_m = 72.57 / mobi
sig_seq = gross * math.sqrt(rel_c ** 2 + rel_m ** 2)
sig_proc = proc * (72.57 / net_kg)
sig = math.sqrt(sig_seq ** 2 + sig_proc ** 2)
check("Uncertainty discount (1 sigma, sequestration + process mass) vs Certify", sig * 1000,
      cf["calculation_view"]["uncertainty_discount_kg"], 1.0, unit=" kg")
acts = proc + emb
check("Activities (process + embodied) vs Certify calculation view", acts, cf["calculation_view"]["activities_tCO2e"], TOL_T, unit=" t")
net = gross + bcu_t - acts - cf["calculation_view"]["uncertainty_discount_kg"] / 1000
check("Net (seq + BCU - activities - discount) vs Certify", net, cf["calculation_view"]["net_co2e_removed_t"], 0.0015, unit=" t")

# ---- system boundary
names = [comp[k]["name"] for k in ("transport_process", "transport_embodied", "bcu")] + ["Injection sequestration"]
bad = [n for n in names if any(w in n.lower() for w in ("production", "pyrolysis", "biomass", "feedstock", "counterfactual", "sparg"))]
if cf["components_total"] == 4 and not bad and cf["no_counterfactual_component"]:
    ok_count += 1
    print(f"OK   System boundary: 4 components ({'; '.join(names)}); no upstream Kerry production, biomass or counterfactual component")
else:
    unrouted.append("system boundary")
    print(f"UNROUTED system boundary: {bad}")

# ---- ticket timing and attribution (evidence, routed to 1.7)
def d(mdy):
    m, dd, yy = mdy.split("-")
    return date(2000 + int(yy), int(m), int(dd))
full_d, empty_d = d(st["full_ticket"]["date"]), d(st["empty_ticket"]["date"])
ops_d = date.fromisoformat(on["kerry_row"]["A10_date"])
cobb_done = date.fromisoformat(cobb["injection_completion_date"])
cobb_offload = date.fromisoformat(cobb["order_line_completed_on"][:10])
w3 = LOG["cobb_tracker"]["w3_row"]
w3_offload = date.fromisoformat(w3["order_line_completed_on"][:10])
w3_full = d(LOG["cross_week_kerry"]["w3_tickets"]["full"]["date"])
print(f"INFO Full ticket {full_d} -> Ops Notes row date {ops_d}: {(ops_d-full_d).days} days; -> COBB injection completion {cobb_done}: {(cobb_done-full_d).days} days")
print(f"FINDING 1.7: full ticket dated {full_d} is {(ops_d-full_d).days} days before the Ops Notes Kerry row date {ops_d} (more than 14)")
print(f"FINDING 1.7: COBB WILA004 offload order completed {cobb_offload}, {(cobb_offload-empty_d).days} days after this pair's post-offload empty ticket ({empty_d})")
print(f"FINDING 1.7: COBB WILA003 offload order completed {w3_offload}, one day after this pair's empty ticket and before WILA003's own credited full ticket ({w3_full}); "
      f"COBB quantity cannot separate the loads ({w3['quantity_consumed_in_injection']:,} kg on WILA003 and WILA004 alike)")
sc = LOG["solids_constant_check"]
if sc["kerry_M5_filtration_solids"] < sc["aecn_rail_O7_filtration_solids"]:
    print(f"FINDING 1.5: Kerry solids constant {sc['kerry_M5_filtration_solids']} is below the AECN constant "
          f"{sc['aecn_rail_O7_filtration_solids']} (AECN Rail O7), against the July guidance 'materially higher'; the Aug W5 note "
          f"treats a 0.71% Slack figure as a transcription slip pending confirmation with the lab; at 0.71% sequestration would be {sc['sensitivity_if_0_71_pct']['sequestration_t']} t "
          f"({sc['sensitivity_if_0_71_pct']['difference_t']} t)")
if not on["constants_M5_comment"] and not on["constants_M5_hyperlink"] and not LOG["filtration_constant_source"]["attached_in_certify"]:
    print("FINDING 1.5: filtration constant M5 (0.00071) carries no source citation on the Kerry tab and CAR-474 is not linked to Mass of Injectant in Certify; value matches CAR-474 0.071%")
w3c = LOG["cross_week_kerry"]["w3_certify"]
print(f"FINDING 1.7: the W3 Kerry removal in Certify credits the 9-16/9-18 pair (Mass of Injectant {w3c['mass_of_injectant_t']} t), "
      f"a load delivered after this removal's pair; if the pairs belong the other way round this removal's sequestration would be "
      f"{LOG['cross_week_kerry']['attribution_sensitivity']['sequestration_if_16_18_sep_pair_t']} t")

print(f"\nSummary: {ok_count} checks OK, {len(unrouted)} unrouted differences")
print(f"Recomputed: ticket net {net_kg:,.4f} kg | filtration {filt:,.4f} kg | MOBI {mobi:,.4f} kg | gross {gross:.4f} t | "
      f"process {proc:.4f} t | embodied {emb:.4f} t | BCU {bcu_t:.4f} t | discount {sig*1000:.1f} kg | net {net:.4f} t")
sys.exit(1 if unrouted else 0)
