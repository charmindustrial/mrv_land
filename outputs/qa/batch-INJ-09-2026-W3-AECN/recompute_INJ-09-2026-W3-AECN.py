#!/usr/bin/env python3
"""Deterministic recompute for INJ-09-2026-W3-AECN (AECN rail, 10 offloads, 3 railcars).

Reads batch_INJ-09-2026-W3-AECN_source_reads.json, recomputes the mass chain (ticket nets,
Ops rollup, sparging, filtration, R&D removal, MOBI), every Certify component from its own
inputs and from the live 2026 Standard EF sheet values, the allocated distances, the
uncertainty inputs and the net, and exits non-zero on any arithmetic mismatch above
0.001 tCO2e (or 0.01 kg / 0.01 mi for mass and distance). Differences between a Certify
input and its evidence are printed as FINDING lines with their checklist item; they are
checklist findings, not arithmetic mismatches, and do not change the exit code
(same convention as outputs/qa/batch-INJ-09-2026-W3-QOWV/recompute_qowv.py)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
L = json.load(open(HERE / "batch_INJ-09-2026-W3-AECN_source_reads.json"))
W2 = json.load(open(HERE / "../batch-INJ-09-2026-W2-AECN/batch_INJ-09-2026-W2-AECN_source_reads.json"))

KG_PER_LB = L["ops_notes"]["constants"]["kg_per_lb_O4"]          # 0.453592
SPARGE = L["ops_notes"]["constants"]["sparging_O5"]               # 0.0129
FILT = L["ops_notes"]["constants"]["filtration_solids_O7"]        # 0.00196
TRIPS = L["ops_notes"]["constants"]["bol_trips_O8"]               # 3
RT = L["ops_notes"]["constants"]["round_trip_O9"]                 # 2
DENS = L["ops_notes"]["constants"]["aecn_density_R3"]             # 1.192
GAL = L["ops_notes"]["constants"]["gallons_removed_R4"]           # 200
L_GAL = L["ops_notes"]["constants"]["L_per_gal_R5"]               # 3.785411784
MI_KM = 1.609344
CO2 = 3.667
C = L["lab_results"]["carbon_pct"] / 100

EF = L["standard_efs"]
EF_PROC = EF["row4_aecn_process_H2_2026"]["final_F"]
EF_EMB = EF["row5_aecn_embodied"]["final_F"]
EF_TANK = EF["row6_tanker_fuel"]["final_F"]          # MT/(t-mi)
EF_RAIL = EF["row10_rail_fuel"]["final_F"]           # MT/(t-mi)
EF_TANK_EE = EF["row11_tanker_embodied"]["final_F"]  # MT/mi
EF_RAIL_EE = EF["row13_railcar_embodied"]["final_F"]  # MT/mi

comp = L["certify"]["components"]
def cv(name):
    c = comp[name]
    return c["value"] / (1000 if c["unit"].startswith("kg") else 1)
def inp(name, key):
    return comp[name]["inputs"][key]

bad = []
def check(label, got, want, tol, unit):
    d = got - want
    ok = abs(d) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} {label}: recomputed {got:.6f} vs {want:.6f} {unit} (delta {d:+.6f})")
    if not ok:
        bad.append(label)

print("== 1. Scale tickets vs Ops Notes (10 offloads)")
offs = L["scale_tickets"]["offloads"]
rows = {r["id"]: r for r in L["ops_notes"]["offload_table"]}
net_sum = 0.0
for rid, r in rows.items():
    car, n = r["railcar"], rid.rsplit("_", 1)[1]
    t = offs[f"{car}_offload_{n}"]
    net = (t["full_ticket"]["gross_weight_lb"] - t["empty_ticket"]["gross_weight_lb"]) * KG_PER_LB
    net_sum += net
    check(f"{rid} net", net, r["cargo_kg"], 0.01, "kg")
roll = L["ops_notes"]["rollup"]
check("Ops A46 sum of cargo", net_sum, roll["sum_cargo_kg"]["value"], 0.01, "kg")

print("\n== 2. Ops rollup: sparging, filtration, R&D removal, MOBI")
C46 = roll["mass_used_kg"]["value"]
spg = C46 * SPARGE
filt = (C46 - spg) * FILT
rnd = GAL * L_GAL * DENS
mobi = C46 - spg - filt - rnd
check("D46 sparging = C46 x 0.0129", spg, roll["sparging_kg"]["value"], 0.01, "kg")
check("E46 filtration = (C46 - D46) x 0.00196", filt, roll["filtration_kg"]["value"], 0.01, "kg")
check("K46 R&D removal = 200 gal x 3.785411784 L x 1.192 kg/L", rnd, roll["mass_removed_rnd_kg"]["value"], 0.01, "kg")
check("F46 MOBI = C46 - D46 - E46 - K46", mobi, roll["mobi_kg"]["value"], 0.01, "kg")
check("Certify Bio-Oil Mass via Rail = Ops C46", inp("AECN pyrolysis (from rail loads) - process emissions", "mass")["value"] * 1000, C46, 0.01, "kg")

print("\n== 3. Railcar balances (conservative mass, Failure Category 11)")
cars = {r["railcar"]: r for r in L["ops_notes"]["railcars"]}
for car in ("GPRX5102", "TILX200231"):
    out = sum(r["cargo_kg"] for r in rows.values() if r["railcar"] == car)
    loaded = cars[car]["total_loaded_kg"]["value"]
    print(f"{'OK ' if out <= loaded else 'MISMATCH'} {car}: 4 offloads {out:.5f} kg <= loaded {loaded} kg (loss {loaded - out:.5f} kg); back-calc not triggered")
    if out > loaded:
        bad.append(car + " balance")
w2s = W2["scale_tickets"]["SHPX215046"]
shpx_w3 = sum(r["cargo_kg"] for r in rows.values() if r["railcar"] == "SHPX215046")
shpx_w2 = w2s["offload_3"]["computed_net_kg"] + w2s["offload_4"]["computed_net_kg"]
shpx_loaded = cars["SHPX215046"]["total_loaded_kg"]["value"]
over = shpx_w3 + shpx_w2 - shpx_loaded
policy_o4 = shpx_loaded - (shpx_w3 + w2s["offload_3"]["computed_net_kg"])

print("\n== 4. Certify components from their own inputs")
seq_mass = inp("Injection sequestration", "product_mass")["value"]
seq_c = inp("Injection sequestration", "carbon_content")["value"] / 100
check("Injection sequestration = mass x C x 3.667", seq_mass * seq_c * CO2, cv("Injection sequestration"), 0.001, "t")
check("Certify carbon = SGS SR26-05599.002", seq_c, C, 1e-9, "fraction")
M = C46 / 1000
pp = "AECN pyrolysis (from rail loads) - process emissions"
pe = "AECN pyrolysis (from rail loads) - embodied emissions"
check("Pyrolysis process (Certify CI)", M * inp(pp, "carbon_intensity")["value"], cv(pp), 0.001, "t")
check("Pyrolysis process (sheet F4 0.1371171258)", M * EF_PROC, cv(pp), 0.001, "t")
check("Pyrolysis embodied (sheet F5)", M * EF_EMB, cv(pe), 0.001, "t")
legs = [("AECN to SOPOR Tanker Truck Transport Process Emissions", EF_TANK),
        ("SOPOR to Opelousas Rail Transport Process Emissions", EF_RAIL),
        ("Opelousas to Basco - Tanker Truck Transport Process Emissions", EF_TANK)]
proc_cert, proc_sheet = 0.0, 0.0
for name, ef in legs:
    d = inp(name, "distance")["value"]
    m = inp(name, "mass")["value"]
    own = m * d * inp(name, "carbon_intensity")["value"] * MI_KM / 1000
    sheet = m * d * ef
    check(f"{name} (own inputs)", own, cv(name), 0.001, "t")
    check(f"{name} (sheet EF)", sheet, cv(name), 0.001, "t")
    proc_cert += cv(name)
    proc_sheet += sheet

print("\n== 5. Allocated distances and embodied legs")
alloc_sopor_ops = sum(r["aecn_sopor_alloc_mi"] for r in rows.values())
alloc_sopor_recalc = sum(r["cargo_kg"] / cars[r["railcar"]]["total_loaded_kg"]["value"] for r in rows.values()) * cars["GPRX5102"]["aecn_sopor_mi"] * TRIPS
alloc_rail_ops = sum(r["rail_alloc_mi"] for r in rows.values())
alloc_rail_recalc = 2 * 2199 + 2199 * shpx_w3 / shpx_loaded
opel = cars["GPRX5102"]["opel_basco_mi"] * RT * len(rows)
check("Ops L38 = sum(cargo/loaded) x 107.5 x 3", alloc_sopor_recalc, roll["aecn_sopor_alloc_mi_sum"]["value"], 0.01, "mi")
check("Ops M38 = 2199 (GPRX full) + 2199 (TILX full) + 2199 x SHPX W3 fraction", alloc_rail_recalc, roll["rail_alloc_mi_sum"]["value"], 0.01, "mi")
check("Opelousas-Basco allocated = 42.9 x 2 x 10", opel, roll["opel_basco_mi_sum"]["value"], 0.01, "mi")
emb = [("AECN to SOPOR Tanker Truck Transport Embodied Emissions", EF_TANK_EE, roll["aecn_sopor_alloc_mi_sum"]["value"]),
       ("SOPOR to Opelousas Rail Transport Embodied Emissions", EF_RAIL_EE, roll["rail_alloc_mi_sum"]["value"]),
       ("Opelousas to Basco Tanker Truck Transport Embodied Emissions", EF_TANK_EE, roll["opel_basco_mi_sum"]["value"])]
emb_sum = 0.0
for name, ef, ops_mi in emb:
    d = inp(name, "distance")["value"]
    own = d * inp(name, "carbon_intensity")["value"] * MI_KM / 1000
    check(f"{name} (own inputs)", own, cv(name), 0.001, "t")
    check(f"{name} (Ops distance x sheet EF)", ops_mi * ef, cv(name), 0.001, "t")
    emb_sum += cv(name)

print("\n== 6. Uncertainty inputs")
sd_mass = inp("Injection sequestration", "product_mass")["sd"] * 1000
check("Mass +/- = 10 offload weighings x 72.57 kg", 10 * 72.57, sd_mass, 0.01, "kg")
check("Carbon +/- = 0.004 x 39.7 %", 0.004 * 39.7, inp("Injection sequestration", "carbon_content")["sd"], 0.001, "%")

print("\n== 7. Activities, BCU and net")
acts = cv(pp) + cv(pe) + proc_cert + emb_sum
cert = L["certify"]
check("Activities = pyrolysis + transport", acts, cert["activities_t"], 0.001, "t")
bcu = cv("BCU - Transport Process")
disc = cert["uncertainty_discount_t"]
net_terms = cv("Injection sequestration") + bcu - cert["activities_t"] - disc
net_calc_view = float(cert["net_displayed"].split()[0])   # Calculation view, 3 decimals
check("Net = Seq + BCU - Activities - Discount vs Calculation view 249.637", net_terms, net_calc_view, 0.0005, "t")
check("Net vs Certify header (2 decimals)", net_terms, cert["net_co2e_removed_t"], 0.005, "t")

print("\n== 8. Uncertainty discount (combined one-sigma of sequestration and mass-driven activities)")
import math
MASS_ACTS = [cv(pp), cv(pe)] + [cv(n) for n, _ in legs]
def discount(seq_t, moi_kg, rail_kg):
    s_seq = seq_t * math.sqrt((sd_mass / moi_kg) ** 2 + (inp("Injection sequestration", "carbon_content")["sd"] / 39.7) ** 2)
    s_act = sum(MASS_ACTS) * rail_kg / (M * 1000) * (sd_mass / rail_kg)
    return math.sqrt(s_seq ** 2 + s_act ** 2)
disc_calc = discount(cv("Injection sequestration"), seq_mass * 1000, M * 1000)
check("Discount = sqrt(sigma_seq^2 + sigma_act^2)", disc_calc, disc, 1e-6, "t")

print("\n== FINDINGS (Certify input vs evidence; checklist findings, not arithmetic mismatches)")
gross_internal = mobi / 1000 * C * CO2
print(f"FINDING 2.7/7.1/9.1/9.8 Mass of Injectant: Certify {seq_mass * 1000:.5f} kg vs Ops F46 MOBI {mobi:.5f} kg; "
      f"difference {seq_mass * 1000 - mobi:.5f} kg = K46 R&D removal {rnd:.5f} kg not deducted in Certify")
print(f"FINDING 7.1/9.1 gross: Certify {cv('Injection sequestration'):.6f} t vs internal {mobi / 1000:.7f} t x {C} x {CO2} = {gross_internal:.6f} t "
      f"(overstated {cv('Injection sequestration') - gross_internal:.6f} t)")
disc_internal = discount(gross_internal, mobi, M * 1000)
net_internal = gross_internal + min(bcu, proc_cert) - acts - disc_internal
print(f"FINDING 9.8 net: internal {gross_internal:.6f} + min(BCU, process) {min(bcu, proc_cert):.6f} - {acts:.6f} - discount re-derived on corrected mass {disc_internal:.6f} "
      f"= {net_internal:.6f} t vs Certify Calculation view {net_calc_view:.3f} t (delta {net_internal - net_calc_view:+.6f})")
print(f"FINDING 9.6 BCU: {bcu:.6f} t vs transport process sum {proc_cert:.9f} t (Certify values) / {proc_sheet:.9f} t (sheet EFs); "
      f"over-coverage {bcu - proc_cert:.9f} t / {bcu - proc_sheet:.9f} t")
print(f"FINDING 2.5 SHPX215046: W3 offloads 1-2 {shpx_w3:.5f} + W2 offloads 3-4 {shpx_w2:.5f} = {shpx_w3 + shpx_w2:.5f} kg vs loaded {shpx_loaded} kg: "
      f"over-draw {over:.5f} kg; the cut goes on the last load, offload 4 (booked in W2): {policy_o4:.5f} kg vs {w2s['offload_4']['computed_net_kg']:.5f} kg claimed in W2; "
      f"W3 offloads 1-2 stay at their raw ticket nets")
cert_sopor = inp("AECN to SOPOR Tanker Truck Transport Embodied Emissions", "distance")["value"]
print(f"FINDING 3.5 AECN-SOPOR allocated distance: Certify {cert_sopor} mi vs Ops L38 {roll['aecn_sopor_alloc_mi_sum']['value']} mi "
      f"(delta {cert_sopor - roll['aecn_sopor_alloc_mi_sum']['value']:+.5f} mi; with 107.49722 mi the Ops method gives {alloc_sopor_recalc * 107.49722 / 107.5:.5f} mi); "
      f"emission effect {(cert_sopor - roll['aecn_sopor_alloc_mi_sum']['value']) * EF_TANK_EE:+.7f} t")
rail_cert = inp("SOPOR to Opelousas Rail Transport Process Emissions", "carbon_intensity")["value"] * MI_KM / 1000
print(f"FINDING 9.2 rail fuel EF: Certify {rail_cert:.10f} vs sheet F10 {EF_RAIL} MT/(t-mi); effect on rail process {proc_sheet - proc_cert:+.7f} t "
      f"(Certify lower); pyrolysis CI 0.13712 vs sheet 0.1371171258: effect {cv(pp) - M * EF_PROC:+.7f} t (Certify higher)")

print("\n== CORRECTIONS (one pass, each step cumulative; Certify values unchanged)")

def scenario(label, cargo_delta_shpx_o2=0.0, cargo_delta_tilx_o2=0.0, loss_acts=0.0, loss_proc=0.0):
    cargo = C46 + cargo_delta_shpx_o2 + cargo_delta_tilx_o2
    s = cargo * SPARGE
    f = (cargo - s) * FILT
    mobi_s = cargo - s - f - rnd
    gross = mobi_s / 1000 * C * CO2
    k = cargo / C46
    proc_s = proc_cert * k
    pyro_s = (cv(pp) + cv(pe)) * k
    sopor_mi = roll["aecn_sopor_alloc_mi_sum"]["value"] + (cargo_delta_shpx_o2 / shpx_loaded + cargo_delta_tilx_o2 / cars["TILX200231"]["total_loaded_kg"]["value"]) * 107.5 * TRIPS
    rail_mi = roll["rail_alloc_mi_sum"]["value"] + cargo_delta_shpx_o2 / shpx_loaded * 2199
    emb_s = (cv(TE_[0]) * sopor_mi / roll["aecn_sopor_alloc_mi_sum"]["value"] + cv(TE_[1]) * rail_mi / roll["rail_alloc_mi_sum"]["value"] + cv(TE_[2]))
    proc_s += loss_proc
    acts_s = pyro_s + proc_s + emb_s + (loss_acts - loss_proc)
    disc_s = discount(gross, mobi_s, cargo)
    net_s = gross + proc_s - acts_s - disc_s
    print(f"FINDING corrections {label}: cargo {cargo:.5f} kg; MOBI {mobi_s:.5f} kg; gross {gross:.6f} t; activities {acts_s:.6f} t; "
          f"BCU target = transport process {proc_s * 1000:.3f} kgCO2e; discount {disc_s:.6f} t; net {net_s:.6f} t (Certify 249.637; delta {net_s - 249.637:+.6f})")
TE_ = [n for n, _, _ in emb]
loss_kg = sum(cars[c]["total_loaded_kg"]["value"] - sum(r["cargo_kg"] for r in rows.values() if r["railcar"] == c) for c in ("GPRX5102", "TILX200231"))
lt = loss_kg / 1000
loss_pyro = lt * (inp(pp, "carbon_intensity")["value"] + inp(pe, "carbon_intensity")["value"])
loss_truck = lt * inp(legs[0][0], "distance")["value"] * inp(legs[0][0], "carbon_intensity")["value"] * MI_KM / 1000
loss_rail = lt * inp(legs[1][0], "distance")["value"] * inp(legs[1][0], "carbon_intensity")["value"] * MI_KM / 1000
print(f"FINDING 8.2 custody losses: GPRX5102 + TILX200231 lost {loss_kg:.5f} kg between loading and offload; uncharged upstream emissions: "
      f"pyrolysis {loss_pyro:.6f} + AECN-SOPOR truck {loss_truck:.6f} + rail {loss_rail:.6f} = {loss_pyro + loss_truck + loss_rail:.6f} t (Certify factors)")
scenario("A (2.7: deduct K46 R&D removal)")
scenario("B (A + 8.2: charge upstream emissions of the 186.38656 kg railcar losses)", loss_acts=loss_pyro + loss_truck + loss_rail, loss_proc=loss_truck + loss_rail)
std_net = (offs["TILX200231_offload_2"]["full_ticket"]["gross_weight_lb"] - L["vvb_guidance"]["august_standard_tare"]["kl720_standard_lb"]) * KG_PER_LB
scenario("C (B + 2.3: KL720 standard empty 29,645 lb on TILX200231 offload 2)", 0.0, std_net - rows["Rail_TILX200231_8.12.2026_offload_2"]["cargo_kg"], loss_pyro + loss_truck + loss_rail, loss_truck + loss_rail)

print(f"\n{len(bad)} arithmetic mismatch(es){': ' + ', '.join(bad) if bad else ''}")
sys.exit(1 if bad else 0)
