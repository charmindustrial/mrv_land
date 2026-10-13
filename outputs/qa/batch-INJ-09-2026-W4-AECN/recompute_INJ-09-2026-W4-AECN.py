#!/usr/bin/env python3
"""Deterministic recompute for INJ-09-2026-W4-AECN (AECN rail, 14 offloads, 4 railcars; SHPX215053 via
Baton Rouge, the rest via Opelousas).

Reads batch_INJ-09-2026-W4-AECN_source_reads.json, recomputes the ticket nets, the SHPX215079 over-draw
cut, the Ops rollup (sparging, filtration, MOBI), the railyard mass split, every AECN Certify component
from its own inputs and from the 2026 Standard EF sheet, the allocated distances, the uncertainty
inputs, the discount, the loss component and the net. Exits non-zero on any arithmetic mismatch
(0.001 tCO2e, 0.01 kg, 0.01 mi). Differences between a Certify input and its evidence are printed as
FINDING lines naming the checklist rows that carry them; they do not change the exit code."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
L = json.load(open(HERE / "batch_INJ-09-2026-W4-AECN_source_reads.json"))

K = L["ops_notes"]["constants"]
KG_PER_LB = K["kg_per_lb_O4"]                      # 0.453592
SPARGE = K["sparging_O5"]                          # 0.0129
FILT = K["filtration_solids_O7"]["value"]          # 0.00196
TRIPS = K["bol_trips_O8"]                          # 3
RT = K["round_trip_O9"]                            # 2
MI_KM = 1.609344
CO2 = 3.667
C = L["lab_results"]["carbon_pct"] / 100
UNC_W = 72.57                                      # kg per offload weighing

EF = L["standard_efs"]
EF_PROC = EF["row4_aecn_process_H2_2026"]["final_F"]
EF_EMB = EF["row5_aecn_embodied"]["final_F"]
EF_TANK = EF["row6_tanker_fuel"]["final_F"]           # MT/(t-mi)
EF_RAIL = EF["row10_rail_fuel"]["final_F"]            # MT/(t-mi)
EF_TANK_EE = EF["row11_tanker_embodied"]["final_F"]   # MT/mi
EF_RAIL_EE = EF["row13_railcar_embodied"]["final_F"]  # MT/mi

comp = L["certify"]["components"]
def cv(n):
    return comp[n]["value_t"]
def inp(n, k):
    return comp[n]["inputs"][k]
def km(i):
    return i["value"] * (MI_KM if i["unit"] == "mi" else 1.0)

SEQ = "Injection sequestration"
PP, PE = "AECN pyrolysis (from rail loads) - process emissions", "AECN pyrolysis (from rail loads) - embodied emissions"
T_AS = "AECN to SOPOR Tanker Truck Transport Process Emissions"
R_OP = "SOPOR to Opelousas Rail Transport Process Emissions"
T_OB = "Opelousas to Basco - Tanker Truck Transport Process Emissions"
R_BR = "SOPOR to Baton Rouge Rail Process Emissions"
T_BB = "Baton Rouge to Basco Tanker Truck Process Emissions"
E_AS = "AECN to SOPOR Tanker Truck Transport Embodied Emissions"
E_R = "SOPOR to Opelousas/Baton Rouge Rail Transport Embodied Emissions"
E_TB = "Opelousas/Baton Rouge to Basco Tanker Truck Transport Embodied Emissions"
LOSS = "AECN Bio-oil Loss"
BCU = "BCU - Transport Process"
PROC_LEGS = [T_AS, R_OP, T_OB, R_BR, T_BB]
EMB_LEGS = [E_AS, E_R, E_TB]

bad = []
def check(label, got, want, tol, unit):
    d = got - want
    ok = abs(d) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} {label}: recomputed {got:.6f} vs {want:.6f} {unit} (delta {d:+.6f})")
    if not ok:
        bad.append(label)

print("== 1. Scale tickets vs Ops Notes (14 offloads)")
offs = L["scale_tickets"]["offloads"]
rows = L["ops_notes"]["offload_table"]
raw_sum = 0.0
for r in rows:
    t = offs[f"{r['railcar']}_offload_{r['id'].rsplit('_', 1)[1]}"]
    net = (t["full_ticket"]["gross_weight_lb"] - t["empty_ticket"]["gross_weight_lb"]) * KG_PER_LB
    raw_sum += net
    check(f"{r['id']} net", net, r["net_scaled_kg_F"], 0.01, "kg")
roll = L["ops_notes"]["rollup"]
check("Ops A46 = sum of ticket nets", raw_sum, roll["sum_deliveries_raw_kg"]["value"], 0.01, "kg")

print("\n== 2. SHPX215079 last-offload cut (Failure Category 11)")
cars = {r["railcar"]: r for r in L["ops_notes"]["railcars"]}
w2 = L["prior_weeks"]["w2_SHPX215079"]
w4_079 = [r for r in rows if r["railcar"] == "SHPX215079"]
loaded_079 = L["bols"]["per_railcar"]["SHPX215079"]["sum_delivered_kg"]
over = w2["sum_kg"] + sum(r["net_scaled_kg_F"] for r in w4_079) - loaded_079
check("H13 previously claimed = W2 offloads 1-2", w2["offload_1_net_kg"] + w2["offload_2_net_kg"], cars["SHPX215079"]["previously_claimed_kg"]["value"], 0.01, "kg")
check("Over-draw = W2 + W4 nets - BOL 77,870 = J41", over, w4_079[-1]["uncertainty_adj_kg_J"], 0.01, "kg")
check("B46 = sum of J", over, roll["sum_uncertainty_adj_kg"]["value"], 0.01, "kg")
check("Offload 4 after cut = 77,870 - W2 - offload 3", loaded_079 - w2["sum_kg"] - w4_079[0]["net_scaled_kg_F"], w4_079[-1]["cargo_kg"], 0.01, "kg")
check("COBB offload 4 offloaded_quantity_kg", L["cobb"]["offloaded_quantity_kg"]["Rail_SHPX215079_8.4.2026_offload_4"], w4_079[-1]["cargo_kg"], 0.01, "kg")

print("\n== 3. Ops rollup: sparging, filtration, MOBI")
C46 = roll["mass_used_kg"]["value"]
spg = sum(r["cargo_kg"] * SPARGE for r in rows)
filt = sum((r["cargo_kg"] * (1 - SPARGE)) * FILT for r in rows)
mobi = C46 - spg - filt
check("C46 = A46 - B46", raw_sum - over, C46, 0.01, "kg")
check("D46 sparging = sum(cargo x 0.0129)", spg, roll["sparging_kg"]["value"], 0.01, "kg")
check("E46 filtration = sum((cargo - sparging) x 0.00196)", filt, roll["filtration_kg"]["value"], 0.01, "kg")
check("F46 MOBI = C46 - D46 - E46 (K46 blank)", mobi, roll["mobi_kg"]["value"], 0.01, "kg")
for r in rows:
    k = r["cargo_kg"] * (1 - SPARGE) * (1 - FILT)
    if abs(k - r["mobi_kg_K"]) > 0.01:
        check(f"{r['id']} MOBI K", k, r["mobi_kg_K"], 0.01, "kg")
check("Summary B17 = F46", L["ops_notes"]["summary_aecn"]["B17_mobi"], roll["mobi_kg"]["value"], 0.01, "kg")
check("Certify Mass of Injectant = F46", inp(SEQ, "product_mass")["value"] * 1000, roll["mobi_kg"]["value"], 0.01, "kg")
check("Certify Bio-Oil Mass via Rail = C46", inp(PP, "mass")["value"] * 1000, C46, 0.01, "kg")

print("\n== 4. Railcar balances, losses and railyard split")
loss_by_car = {}
for car, r in cars.items():
    out = sum(x["cargo_kg"] for x in rows if x["railcar"] == car) + r["previously_claimed_kg"]["value"]
    loaded = L["bols"]["per_railcar"][car]["sum_delivered_kg"]
    check(f"{car} loaded E = BOL Qty shipped sum", r["total_loaded_kg"]["value"], loaded, 0.01, "kg")
    lk = max(0.0, loaded - out)
    loss_by_car[car] = lk
    check(f"{car} loss G = loaded - delivered", lk, r["loss_kg"]["value"], 0.01, "kg")
br = sum(x["cargo_kg"] for x in rows if x["railcar"] == "SHPX215053")
opl = C46 - br
check("C49 Baton Rouge mass = SHPX215053 delivered", br, L["ops_notes"]["railyard_split"]["raillogix_baton_rouge"]["value"], 0.01, "kg")
check("C50 Opelousas mass = C46 - C49", opl, L["ops_notes"]["railyard_split"]["opelousas"]["value"], 0.01, "kg")
check("Certify Baton Rouge rail Mass of load = C49", inp(R_BR, "mass")["value"] * 1000, br, 0.01, "kg")
check("Certify Baton Rouge truck Mass of load = C49", inp(T_BB, "mass")["value"] * 1000, br, 0.01, "kg")
check("Certify Opelousas rail Mass of load = C50", inp(R_OP, "mass")["value"] * 1000, opl, 0.01, "kg")

print("\n== 5. Certify components from their own inputs")
check("Injection sequestration = mass x C x 3.667", inp(SEQ, "product_mass")["value"] * inp(SEQ, "carbon_content")["value"] / 100 * CO2, cv(SEQ), 0.001, "t")
check("Certify carbon = SGS SR26-05719.002", inp(SEQ, "carbon_content")["value"] / 100, C, 1e-9, "fraction")
M = C46 / 1000
check("Pyrolysis process (Certify CI)", M * inp(PP, "carbon_intensity")["value"], cv(PP), 0.001, "t")
check("Pyrolysis process (sheet F4)", M * EF_PROC, cv(PP), 0.001, "t")
check("Pyrolysis embodied (Certify CI)", M * inp(PE, "carbon_intensity")["value"], cv(PE), 0.001, "t")
check("Pyrolysis embodied (sheet F5)", M * EF_EMB, cv(PE), 0.001, "t")
def own_transport(n, mass_t=None, dist=None):
    i = comp[n]["inputs"]
    m = i["mass"]["value"] if mass_t is None else mass_t
    d = km(i["distance"]) if dist is None else dist
    return m * d * i["carbon_intensity"]["value"] / 1000
sheet_ef = {T_AS: EF_TANK, R_OP: EF_RAIL, T_OB: EF_TANK, R_BR: EF_RAIL, T_BB: EF_TANK}
proc_cert = 0.0
for n in PROC_LEGS:
    check(f"{n} (own inputs)", own_transport(n), cv(n), 0.001, "t")
    proc_cert += cv(n)
sheet = {T_AS: M * 107.49722 * EF_TANK, R_OP: opl / 1000 * 2199 * EF_RAIL, T_OB: opl / 1000 * 42.9 * EF_TANK,
         R_BR: br / 1000 * cars["SHPX215053"]["rail_mi"] * EF_RAIL, T_BB: br / 1000 * cars["SHPX215053"]["opel_basco_mi"]["value"] * EF_TANK}
for n in (T_AS, R_OP, T_BB):
    check(f"{n} (evidence mass x distance x sheet EF)", sheet[n], cv(n), 0.001, "t")
print(f"INFO {T_OB}: evidence basis (Opelousas mass C50 x 42.9 mi x sheet EF) {sheet[T_OB]:.6f} t vs Certify {cv(T_OB):.6f} t (see FINDING)")
print(f"INFO {R_BR}: evidence basis (C49 x 2,152 mi x sheet EF) {sheet[R_BR]:.6f} t vs Certify {cv(R_BR):.6f} t (see FINDING)")

print("\n== 6. Allocated distances and embodied legs")
alloc_sopor_ops = sum(r["cargo_kg"] / cars[r["railcar"]]["total_loaded_kg"]["value"] for r in rows) * cars["SHPX215039"]["aecn_sopor_mi"] * TRIPS
alloc_sopor_cert_basis = alloc_sopor_ops * inp(T_AS, "distance")["value"] / cars["SHPX215039"]["aecn_sopor_mi"]
w4_079_cargo = sum(r["cargo_kg"] for r in w4_079)
rail_rt = RT * (cars["SHPX215053"]["rail_mi"] + cars["SHPX215039"]["rail_mi"] + cars["SHPX215091"]["rail_mi"]) + RT * cars["SHPX215079"]["rail_mi"] * w4_079_cargo / loaded_079
rail_ow = rail_rt / RT
truck_rt = RT * (42.9 * sum(1 for r in rows if r["railcar"] != "SHPX215053") + cars["SHPX215053"]["opel_basco_mi"]["value"] * sum(1 for r in rows if r["railcar"] == "SHPX215053"))
check("Ops L42 = sum(cargo/loaded) x 107.5 x 3", alloc_sopor_ops, roll["aecn_sopor_alloc_mi_sum"]["value"], 0.01, "mi")
check("Certify AECN-SOPOR allocated = Ops method on 107.49722 mi", alloc_sopor_cert_basis, inp(E_AS, "distance")["value"], 0.01, "mi")
check("Ops M42 = 2 x (2152 + 2199 + 2199) + 2 x 2199 x SHPX215079 W4 share", rail_rt, roll["rail_alloc_mi_sum"]["value"], 0.01, "mi")
check("Certify rail allocated = Ops M42", inp(E_R, "distance")["value"], roll["rail_alloc_mi_sum"]["value"], 0.01, "mi")
check("Ops N42 = 2 x (42.9 x 10 + 136 x 4)", truck_rt, roll["truck_ee_mi_sum"]["value"], 0.01, "mi")
check("Certify truck allocated = Ops N42", inp(E_TB, "distance")["value"], roll["truck_ee_mi_sum"]["value"], 0.01, "mi")
emb_sheet = {E_AS: roll["aecn_sopor_alloc_mi_sum"]["value"] * EF_TANK_EE, E_R: roll["rail_alloc_mi_sum"]["value"] * EF_RAIL_EE, E_TB: roll["truck_ee_mi_sum"]["value"] * EF_TANK_EE}
emb_cert = 0.0
for n in EMB_LEGS:
    i = comp[n]["inputs"]
    check(f"{n} (own inputs)", km(i["distance"]) * i["carbon_intensity"]["value"] / 1000, cv(n), 0.001, "t")
    check(f"{n} (Ops distance x sheet EF)", emb_sheet[n], cv(n), 0.001, "t")
    emb_cert += cv(n)

print("\n== 7. Uncertainty inputs")
n_all, n_opl, n_br = len(rows), sum(1 for r in rows if r["railcar"] != "SHPX215053"), sum(1 for r in rows if r["railcar"] == "SHPX215053")
check(f"Mass of Injectant +/- = {n_all} x 72.57", n_all * UNC_W, inp(SEQ, "product_mass")["sd"] * 1000, 0.01, "kg")
check(f"Bio-Oil Mass via Rail +/- = {n_all} x 72.57", n_all * UNC_W, inp(PP, "mass")["sd"] * 1000, 0.01, "kg")
check(f"Opelousas rail Mass of load +/- = {n_opl} x 72.57", n_opl * UNC_W, inp(R_OP, "mass")["sd"] * 1000, 0.01, "kg")
check(f"Baton Rouge truck Mass of load +/- = {n_br} x 72.57", n_br * UNC_W, inp(T_BB, "mass")["sd"] * 1000, 0.01, "kg")
check("Carbon +/- = 0.004 x 44.0", 0.004 * 44.0, inp(SEQ, "carbon_content")["sd"], 0.0001, "%")
print(f"INFO Baton Rouge rail Mass of load +/-: Certify {inp(R_BR, 'mass')['sd']} (none); expected {n_br} x 72.57 = {n_br * UNC_W:.2f} kg (see FINDING)")

print("\n== 8. Activities, adjustments and net")
cert = L["certify"]
acts_aecn = cv(PP) + cv(PE) + proc_cert + emb_cert + cv(LOSS)
check("AECN activities = pyrolysis + transport + loss", acts_aecn, cert["activities_batch_scope_t"], 0.001, "t")
site_acts = cert["activities_t"] - acts_aecn
check("Site activities (out of batch scope) = 20.550448", site_acts, 20.55044756997949, 0.001, "t")
check("Activities total vs Calculation view 83.620", cert["activities_t"], 83.620, 0.0005, "t")
check("Adjustments total vs Calculation view 22.439", cert["adjustments_t"], 22.439, 0.0005, "t")
check("Sequestrations vs Calculation view 425.691", cv(SEQ), 425.691, 0.0005, "t")
disc = cert["uncertainty_discount_t"]
net_terms = cv(SEQ) + cert["adjustments_t"] - cert["activities_t"] - disc
check("Net = Seq + Adj - Activities - Discount vs Calculation view 362.068", net_terms, 362.068, 0.0005, "t")
check("Net vs Certify header", net_terms, cert["net_co2e_removed_t"], 0.005, "t")

print("\n== 9. Uncertainty discount (combined one-sigma, one term per datapoint; correlated uses summed)")
def discount(vals=None, extra_sd=None, relink=None):
    """vals: component value overrides (t). extra_sd: {component: (input key, sd[, input value])} sets an input's +/-
    (and, when given, the input value it is measured against).
    relink: {component: datapoint_id} moves a component's mass input onto another datapoint."""
    vals = vals or {}
    extra_sd = extra_sd or {}
    relink = relink or {}
    contrib = {}
    for n, c in comp.items():
        sign = {"SEQUESTRATION": 1, "ACTIVITY": -1}.get(c["type"])
        if sign is None:
            continue
        v = vals.get(n, c["value_t"])
        for k, i in c["inputs"].items():
            sd, base = i["sd"], i["value"]
            if n in extra_sd and extra_sd[n][0] == k:
                sd = extra_sd[n][1]
                base = extra_sd[n][2] if len(extra_sd[n]) > 2 else base
            if not sd:
                continue
            if c["blueprint"] == "grid_electricity_use_with_recs" and k == "grid_electricity_use":
                d = sd * c["inputs"]["grid_carbon_intensity"]["value"] / 1000    # kWh x kg/kWh -> t
            else:
                d = v * sd / base
            dp = relink.get(n, i["datapoint_id"]) if k == "mass" else i["datapoint_id"]
            contrib.setdefault(dp, 0.0)
            contrib[dp] += sign * d
    return math.sqrt(sum(x * x for x in contrib.values())), contrib
disc_calc, contrib = discount()
check("Discount from component inputs (electricity +/- at grid factor 0.4630140342)", disc_calc, disc, 1e-6, "t")
for dp, x in sorted(contrib.items(), key=lambda kv: -abs(kv[1])):
    print(f"   term {dp}: {x:+.6f} t")

print("\n== 10. AECN Bio-oil Loss (guidance: pyrolysis CIs + loading-origin-to-rail-yard transport, pro-rated)")
def loss_t(car, rail_mi):
    lt = loss_by_car[car] / 1000
    loaded = L["bols"]["per_railcar"][car]["sum_delivered_kg"] / 1000
    pyro = lt * (inp(PP, "carbon_intensity")["value"] + inp(PE, "carbon_intensity")["value"])
    proc = lt * (107.49722 * EF_TANK + rail_mi * EF_RAIL)
    emb = lt / loaded * (cars[car]["aecn_sopor_mi"] * TRIPS * EF_TANK_EE + rail_mi * EF_RAIL_EE)
    return pyro + proc + emb, pyro, proc, emb
ex = loss_t("SHPX215053", 2199)
check("Example image: SHPX215053 341.43 kg on Opelousas distances = 0.07833", ex[0], 0.07833, 0.00001, "t")
check("Example transport process 0.02365", ex[2], 0.02365, 0.00001, "t")
check("Example transport embodied 0.00064", ex[3], 0.00064, 0.00001, "t")
loss_opel = sum(loss_t(c, 2199)[0] for c in ("SHPX215053", "SHPX215039", "SHPX215091"))
loss_guid = loss_t("SHPX215053", cars["SHPX215053"]["rail_mi"])[0] + sum(loss_t(c, 2199)[0] for c in ("SHPX215039", "SHPX215091"))
check("Loss, all three railcars on Opelousas distances vs Certify 145 kg", loss_opel, cv(LOSS), 0.001, "t")
print(f"INFO loss with SHPX215053 on its own 2,152 mi rail leg: {loss_guid:.6f} t; per tonne lost {loss_guid / (sum(loss_by_car.values()) / 1000):.4f} t (guidance 'approximately 0.229')")

print("\n== FINDINGS (Certify input vs evidence; checklist findings, not arithmetic mismatches)")
br_mi = cars["SHPX215053"]["rail_mi"]
br_rail_ev = own_transport(R_BR, dist=br_mi * MI_KM)
print(f"FINDING 3.5/9.2/7.2 Baton Rouge rail distance: Certify 'Distance traveled' {inp(R_BR, 'distance')['value']} {inp(R_BR, 'distance')['unit']} (no source) vs Ops K10 {br_mi} mi "
      f"and guidance '2,152'; on 2,152 mi the leg is {br_rail_ev:.6f} t vs Certify {cv(R_BR):.6f} t: understated {br_rail_ev - cv(R_BR):.6f} t")
opl_truck_ev = own_transport(T_OB, mass_t=opl / 1000)
print(f"FINDING 2.7/9.2 Opelousas-Basco truck mass: Certify uses 'Bio-Oil Mass - AECN via Rail' {inp(T_OB, 'mass')['value']:.5f} t (all four railcars) vs Ops C50 Opelousas mass {opl / 1000:.5f} t; "
      f"SHPX215053's {br / 1000:.5f} t is charged on both the Opelousas and the Baton Rouge truck legs: leg {opl_truck_ev:.6f} t vs Certify {cv(T_OB):.6f} t, overcharged {cv(T_OB) - opl_truck_ev:.6f} t")
d_br_sd = discount(extra_sd={R_BR: ("mass", n_br * UNC_W / 1000)})[0]
print(f"FINDING 7a.1 Baton Rouge rail Mass of load {inp(R_BR, 'mass')['value']} t carries no +/- (expected {n_br * UNC_W:.2f} kg, as the Baton Rouge truck leg has); discount {disc:.10f} -> {d_br_sd:.10f} t with it")
print(f"FINDING 9.2 Baton Rouge legs use GLEC library factors, not the Standard EF sheet: rail 0.0161 vs sheet {EF_RAIL * 1000 / MI_KM:.10f} kg/(km t); "
      f"truck 0.071 vs sheet {EF_TANK * 1000 / MI_KM:.10f} kg/(km t): truck leg {cv(T_BB):.6f} t vs sheet {sheet[T_BB]:.6f} t ({cv(T_BB) - sheet[T_BB]:+.6f} t)")
print(f"FINDING 9.2 factor rounding: pyrolysis CI 0.13712 vs sheet {EF_PROC} ({cv(PP) - M * EF_PROC:+.6f} t); rail embodied 0.03113 kg/mi vs sheet {EF_RAIL_EE * 1000:.8f} ({cv(E_R) - emb_sheet[E_R]:+.6f} t); "
      f"tanker embodied 0.23756 kg/mi vs sheet {EF_TANK_EE * 1000:.10f} ({cv(E_AS) + cv(E_TB) - emb_sheet[E_TB] - inp(E_AS, 'distance')['value'] * EF_TANK_EE:+.6f} t)")
print(f"FINDING 3.5 AECN-SOPOR allocated distance: Certify {inp(E_AS, 'distance')['value']} mi vs attached-sheet Ops L42 {roll['aecn_sopor_alloc_mi_sum']['value']} mi "
      f"(Certify follows the Ops method on 107.49722 mi, {alloc_sopor_cert_basis:.5f}); effect {(inp(E_AS, 'distance')['value'] - roll['aecn_sopor_alloc_mi_sum']['value']) * EF_TANK_EE:+.7f} t")
print(f"FINDING 3.5/9.2 rail embodied basis: W4 doubles the rail leg (round trip) {rail_rt:.5f} mi; W1-W3 and the 2026-10-01 Ops copy used one way ({rail_ow:.5f} mi); "
      f"W4 charges {(rail_rt - rail_ow) * EF_RAIL_EE:.6f} t more than the September weeks before it; the guidance names the round trip for the tanker leg only")
bcu = cv(BCU)
proc_ev = proc_cert - cv(R_BR) + br_rail_ev - cv(T_OB) + opl_truck_ev
proc_only_truck = proc_cert - cv(T_OB) + opl_truck_ev
print(f"FINDING 9.6 BCU {bcu} t vs Certify process sum {proc_cert:.7f} t (BCU {bcu - proc_cert:+.7f}); vs evidence-corrected sum {proc_ev:.7f} t ({bcu - proc_ev:+.7f}); "
      f"if only the Opelousas truck mass is corrected the sum is {proc_only_truck:.7f} t and the BCU exceeds it by {bcu - proc_only_truck:.7f} t")
print(f"FINDING 8.2 loss: Certify 0.145 t follows the example's Opelousas distances for SHPX215053 ({loss_opel:.6f}); on its own 2,152 mi rail leg the loss is {loss_guid:.6f} t "
      f"(Certify higher by {cv(LOSS) - loss_guid:.6f} t); the loss datapoint carries no +/-")
c1 = L["certify"]["ops_notes_copies"]["copy1_src_1M3VZCDQF1S0FQ0D"]
c2 = L["certify"]["ops_notes_copies"]["copy2_src_1M3W1NWED1S0K0MP_2026-10-01"]
print(f"FINDING 9.10 attached Ops Notes copies: src_1M3VZCDQF1 (Bio-Oil Mass, rail allocated distance) shows K10 {c1['K10_rail_mi']}, L10 {c1['L10_truck_mi']}, M42 {c1['M42_rail_alloc_sum']}, N42 {c1['N42_truck_ee_sum']}, no railyard split; "
      f"src_1M3W1NWED1 (loss) shows M42 {c2['M42_rail_alloc_sum']}, N42 {c2['N42_truck_ee_sum']}; Certify uses {inp(E_R, 'distance')['value']} mi, {inp(E_TB, 'distance')['value']} mi, {br:.5f} and {opl:.5f} kg from the live sheet only")
print("FINDING 2.2/8.3 SHPX215079 offloads 3-4 weighed 2026-09-05 09:29 to 2026-09-06 07:50 (W2's Ops window 2026-09-05 to 2026-09-12) and booked here with injection completion 2026-09-25, 19-20 days after weighing; no cell note or guidance text covers the hold")

print("\n== CORRECTIONS (cumulative; Certify values unchanged)")
NET_CV = 362.068
v = {R_BR: br_rail_ev}
def step(label, vals, extra=None, relink=None, loss=None):
    vv = dict(vals)
    if loss is not None:
        vv[LOSS] = loss
    acts = cert["activities_t"] + sum(vv[n] - cv(n) for n in vv)
    d = discount(vv, extra, relink)[0]
    net = cv(SEQ) + cert["adjustments_t"] - acts - d
    print(f"FINDING 9.8 corrections {label}: activities {acts:.6f} t; discount {d:.6f} t; net {net:.6f} t (Certify {NET_CV}; delta {net - NET_CV:+.6f})")
    return net
step("A (3.5: Baton Rouge rail on 2,152 mi)", v)
v[T_OB] = opl_truck_ev
relink = {T_OB: inp(R_OP, "mass")["datapoint_id"]}
extra = {T_OB: ("mass", n_opl * UNC_W / 1000, opl / 1000)}
step("B (A + 2.7: Opelousas truck on the Opelousas mass +/- 725.7 kg, linked to its Mass of load)", v, extra, relink)
extra = dict(extra, **{R_BR: ("mass", n_br * UNC_W / 1000)})
step("C (B + 7a.1: Baton Rouge rail +/- 290.28 kg)", v, extra, relink)
net_d = step("D (C + 8.2: loss on SHPX215053's own rail leg; BCU left at 19.339)", v, extra, relink, loss=loss_guid)
vE = dict(v); vE[LOSS] = loss_guid
actsE = cert["activities_t"] + sum(vE[n] - cv(n) for n in vE)
dE = discount(vE, extra, relink)[0]
adjE = cert["adjustments_t"] - bcu + proc_ev
netE = cv(SEQ) + adjE - actsE - dE
print(f"FINDING 9.8 corrections E (D + 9.6: BCU set to the corrected transport process sum {proc_ev:.7f} t, Charm's exact-figure rule): adjustments {adjE:.6f} t; "
      f"net {netE:.6f} t (Certify {NET_CV}; delta {netE - NET_CV:+.6f}); the BCU draw on certificate 13-47206-50000 rises by {proc_ev - bcu:.7f} t")

print("\n== 11. Further checks added after run 1's Gate 3 review")
w2a = L["prior_weeks"]["w2_SHPX215079"]["w2_rail_alloc_mi"]
w4a = [r["rail_alloc_mi_M"] for r in w4_079]
print(f"FINDING 3.5 SHPX215079 rail miles across weeks: W2 {w2a[0]} + {w2a[1]} (one way) + W4 {w4a[0]} + {w4a[1]} (round trip) gives {sum(w2a) + sum(w4a):.5f} mi, "
      f"neither one way (2,199) nor round trip (4,398) for the railcar")
dbl = 0.0
for c in ("SHPX215053", "SHPX215039", "SHPX215091"):
    share = loss_by_car[c] / L["bols"]["per_railcar"][c]["sum_delivered_kg"]
    dbl += share * 2199 * EF_RAIL_EE
print(f"FINDING 8.2 rail embodied on lost oil counted twice: the rail allocation gives each FULL railcar its whole trip in M, and the loss figure charges the lost share again: "
      f"{dbl:.6f} t (conservative); the loss uses one-way rail embodied while the W4 rail embodied component uses round trip")
rw = L["rp_status"]["results_workbook"]
w4r = rw["w4_aecn_row"]
check("RP results workbook W4 AECN net vs Certify", w4r["net_t"], cert["net_co2e_removed_t"], 0.005, "t")
check("RP results workbook W4 AECN process vs Certify AECN activities", w4r["process_t"], acts_aecn, 0.0005, "t")
check("RP results workbook W4 AECN reductions vs Certify adjustments", w4r["reductions_t"], cert["adjustments_t"], 0.0005, "t")
check("RP results workbook W4 AECN discount vs Certify", w4r["discount_t"], disc, 0.00005, "t")
check("RP results workbook reductions total = sum of 11 removals", sum(rw["reductions_by_removal_t"]), rw["rp_totals"]["reductions_t"], 0.005, "t")
sr = L["rp_status"]["statement_report_v1_7"]["section_e"]
print(f"FINDING 7.4 RP drafts disagree: statement report v1.7 Section E process {sr['process_t']} / site {sr['site_t']} / reductions {sr['reductions_t']} / net {sr['net_t']} t "
      f"against the results workbook {rw['rp_totals']['process_t']} / {rw['rp_totals']['site_t']} / {rw['rp_totals']['reductions_t']} / {rw['rp_totals']['net_t']} t; "
      f"the report's W4 site figure {L['rp_status']['statement_report_v1_7']['w4_site_t']} t against Certify {site_acts:.6f} t; both drafts carry Certify's W4 AECN process figure ({w4r['process_t']} t), not the evidence figure {acts_aecn + (actsE - cert['activities_t']):.6f} t")
eac = L["bcu_sources"]["usage_september"]["co2e_abated_mt"]
print(f"FINDING S.1 EAC tracker September usage {eac} t against the results workbook's reductions {sum(rw['reductions_by_removal_t']):.4f} t (sum of 11 removals): under-logged by {sum(rw['reductions_by_removal_t']) - eac:.4f} t; "
      f"the corrected W4 BCU adds {proc_ev - bcu:.7f} t more")

print("\n== 12. Checks added after the run-3 Gate 3 review")
oc = L["certify"]["ops_notes_copies"]
cp2 = oc["copy2_src_1M3W1NWED1S0K0MP_2026-10-01"]
pos_kg = oc["loss_positive_sum_kg"]
check("Loss rows G10:G12 = loaded - delivered (SHPX215053, SHPX215039, SHPX215091)", pos_kg, sum(loss_by_car[c] for c in ("SHPX215053", "SHPX215039", "SHPX215091")), 0.01, "kg")
rate = loss_opel / (pos_kg / 1000)
print(f"FINDING 8.2/9.10 loss evidence attached in Certify: the linked Ops copy (2026-10-01) has G10:G13 {cp2['G10_G13_loss_kg']} kg (G13 '{cp2['G13_formula']}'), "
      f"summing to {cp2['G_loss_sum_kg']} kg; at Certify's own {rate:.6f} t per t lost that is {cp2['G_loss_sum_kg'] / 1000 * rate:.6f} t against Certify {cv(LOSS)} t; "
      f"Certify's figure needs {pos_kg} kg, which drops G13, as only the live sheet's MAX(0, E13-F13) does")
tb = L["standard_efs"]["tanker_embodied_build"]
check("Tanker embodied factor = B12 x (1 + B14 deadhead)", tb["A12_B12"][1] * (1 + tb["A14_B14"][1]), EF_TANK_EE, 1e-12, "MT/mi")
emb_tb_rt_nodh = roll["truck_ee_mi_sum"]["value"] * tb["A12_B12"][1]
print(f"FINDING 9.2 empty return counted twice on the Opelousas/Baton Rouge to Basco tanker embodied leg: {roll['truck_ee_mi_sum']['value']} mi is already a round trip "
      f"(guidance: 'The tanker leg is counted as a round trip') and the factor {EF_TANK_EE} MT/mi already adds the {tb['A14_B14'][1]} deadhead share ('{tb['A15_B15'][0]}'); "
      f"without the uplift the leg is {emb_tb_rt_nodh:.6f} t against Certify {cv(E_TB):.6f} t, {cv(E_TB) - emb_tb_rt_nodh:.6f} t over (conservative; a standing method across weeks)")
rcb = L["standard_efs"]["railcar_embodied_build"]
print(f"FINDING 3.5 railcar embodied basis: the factor is '{rcb['A5_B5'][0]}' {rcb['A5_B5'][1]} with no empty-return uplift, so W4's round trip ({rail_rt:.5f} mi) fits it "
      f"and the one-way basis used in W1-W3 would charge W4's railcars {(rail_rt - rail_ow) * EF_RAIL_EE:.6f} t less than the miles they travelled; the basis needs settling for the period, not W4 reverting to one way")
ag = "Argon Electricity Usage (RECs)"
gi = inp(ag, "grid_electricity_use")
d_ag = discount(extra_sd={ag: ("grid_electricity_use", 0.02 * gi["value"])})[0]
pp_none = [n for n, c in comp.items() if "procured_power_electricity_use" in c["inputs"] and not c["inputs"]["procured_power_electricity_use"]["sd"]]
print(f"FINDING 7a.1 site inputs (site-emissions QA scope): '{ag}' grid use {gi['value']} kWh carries no +/- while the knowledge base lists 'Grid Electricity Usage: 0.02 x Measured Value'; "
      f"with 2 % ({0.02 * gi['value']:.6f} kWh) the discount is {d_ag:.10f} t ({d_ag - disc:+.7f} t); the procured-power input carries no +/- on {len(pp_none)} components ({'; '.join(pp_none)})")
w3wk = L["prior_weeks"]["w3_ops_week"]
pre = sorted({(r["railcar"], r["offload"], r["full_ticket"]["date"]) for r in offs.values() if r["full_ticket"]["date"] < "2026-09-19"})
pre_w4 = [p for p in pre if p[0] != "SHPX215079"]
print(f"FINDING 2.2 weighed before the Certify period (2026-09-19): {', '.join(f'{c} offload {o} full {d}' for c, o, d in pre_w4)}; "
      f"W3's Ops week is {w3wk['A3_B3'][1][:10]} to {w3wk['A4_B4'][1][:10]} and W4's {L['ops_notes']['week_start']['value'][:10]} to {L['ops_notes']['week_end']['value'][:10]}, both containing 2026-09-18; W3 did not book them; COBB books every W4 offload on injection completion 2026-09-25")
ls_ = L["cobb"]["late_september_railcars"]
print(f"INFO 8.3 booking basis: COBB rows {ls_['rows']} ({', '.join(ls_['railcars'])}; order lines completed {ls_['order_lines_completed'][0][:10]} to {ls_['order_lines_completed'][-1][:10]}) "
      f"sit in {ls_['all_rows_batch'][0]} with injection completion {ls_['all_rows_completion'][0][:10]}: oil is booked in the week it is injected, none of it in W4")
rws = L["rp_status"]["results_workbook"]
check("RP results workbook discount column M2:M12 vs report v1.7 Section E 'Uncertainty Discounts' 11.00", rws["discount_column_sum_t"], 11.00, 0.005, "t")
vF = dict(vE)
dF = discount(vF, extra, {T_OB: "opelousas_truck_mass_own_datapoint"})[0]
netF = cv(SEQ) + adjE - actsE - dF
print(f"INFO 9.8 corrections E with the corrected Opelousas truck mass entered as its own datapoint (not linked to the rail Mass of load): discount {dF:.6f} t; net {netF:.6f} t (Certify {NET_CV}; delta {netF - NET_CV:+.6f})")

print(f"\n{len(bad)} arithmetic mismatch(es){': ' + ', '.join(bad) if bad else ''}")
sys.exit(1 if bad else 0)
