#!/usr/bin/env python3
"""Deterministic recompute for the Charm QOWV (Aqueous) weekly batch INJ-09-2026-W2.
Run from the batch output folder BEFORE delivery. Exits non-zero on any mismatch
between a recomputed figure and the Certify values captured in the source-read log."""
import json, glob, sys, openpyxl

ops = glob.glob("source_exports/*Ops_Notes.xlsx")[0]
log = json.load(open(glob.glob("batch_*_source_reads.json")[0]))
ws = openpyxl.load_workbook(ops, data_only=True)["QOWV"]

rows = [(ws[f"A{r}"].value, ws[f"B{r}"].value, ws[f"C{r}"].value, ws[f"D{r}"].value,
         ws[f"E{r}"].value, ws[f"F{r}"].value, ws[f"G{r}"].value, ws[f"H{r}"].value,
         ws[f"I{r}"].value, ws[f"J{r}"].value)
        for r in range(11, 49) if ws[f"B{r}"].value is not None]

n = len(rows)
gross = round(sum(r[1] for r in rows), 4)
produced = round(sum(r[3] for r in rows), 4)
injected = round(sum(r[5] for r in rows), 4)
pe_kg = sum(r[8] for r in rows)
unc = round(sum(r[9] for r in rows), 5)
ci = pe_kg / produced

c = {x["name"]: x for x in log["certify"]["components"]}
seq = c["Injection sequestration"]
proc = c["CO to LA Flatbed Truck Transport Process Emissions - QOWV"]
emb = c["CO to LA Flatbed Truck Transport Embodied Emissions - QOWV"]
pyro = c["Pyrolysis - Charm QOWV PP Emissions"]
bcu = c["BCU - Transport Process"]

cpct = seq["inputs"]["carbon_content_pct"] / 100
ef_proc = log["standard_efs_2026"]["flatbed_process"]["value"]          # MT/(t*mi)
ef_emb = log["standard_efs_2026"]["non_tanker_embodied"]["value"]        # MT/mi
dist = proc["inputs"]["distance_mi"]
alloc = log["shipment_tracker"]["totals"]["allocated_miles_mi"]

seq_t = injected * cpct * 3.667 / 1000
proc_t = gross / 1000 * dist * ef_proc
emb_t = alloc * ef_emb
pyro_t = produced / 1000 * pyro["inputs"]["ci_tco2e_per_t"]
net_t = seq_t + bcu["value_t"] - (proc_t + emb_t + pyro_t) - log["certify"]["uncertainty_discount_kg"] / 1000

checks = [
    ("n_totes", n, log["n_totes"]),
    ("gross_kg", gross, log["ops_notes_totals"]["total_mass_transported_kg"]),
    ("produced_kg", produced, log["ops_notes_totals"]["total_oil_produced_kg"]),
    ("injected_kg", injected, log["ops_notes_totals"]["total_oil_in_batch_kg"]),
    ("weighted_ci", round(ci, 10), round(log["ops_notes_totals"]["weighted_avg_ci_kgco2e_per_kg"], 10)),
    ("uncertainty_kg", unc, round(n * 2.5 * 0.453592, 5)),
    ("uncertainty_vs_certify", unc, seq["inputs"]["mass_of_product_uncertainty_kg"]),
    ("carbon_unc_pct_abs", round(cpct * 100 * 0.004, 4), seq["inputs"]["carbon_content_uncertainty_pct_abs"]),
    ("mass_of_load_kg", gross, proc["inputs"]["mass_of_load_kg"]),
    ("pyrolysis_mass_kg", produced, pyro["inputs"]["mass_kg"]),
    ("seq_t", round(seq_t, 3), seq["value_t"]),
    ("proc_t", round(proc_t, 3), proc["value_t"]),
    ("emb_t", round(emb_t, 3), emb["value_t"]),
    ("pyro_t", round(pyro_t, 3), pyro["value_t"]),
    ("bcu_matches_proc_at_display_precision_t", round(bcu["inputs"]["constant_co2_reduction_kg"] / 1000, 3), round(proc_t, 3)),
    ("net_t", round(net_t, 3), log["certify"]["net_co2e_removed_t"]),
    ("standard_loss_not_applied", log["ops_notes_totals"]["standard_loss_applied"], False),
    ("lcs_component_needed", log["lcs_use_kg"], None),
]

bad = [(k, a, b) for k, a, b in checks if a != b]
for k, a, b in checks:
    print(f"{'OK ' if a == b else 'BAD'} {k}: recomputed {a} vs certify/log {b}")
b = bcu["inputs"]["constant_co2_reduction_kg"]
proc_certify_kg = gross / 1000 * dist * 1.609344 * proc["inputs"]["ef_kgco2e_per_km_t"]
print(f"\nprocess emission {proc_certify_kg:.3f} kg (Certify 0.086 basis) / {proc_t*1000:.3f} kg (sheet basis); BCU {b} kg; "
      f"BCU minus process {b - proc_certify_kg:+.3f} / {b - proc_t*1000:+.3f} kg; BCU equals process (8.1): {abs(b - proc_certify_kg) < 1e-6}")
x = log["tote_inventory_crosscheck"]; lv_pe = log["live_ops_notes_2026_09_29"]["pe_change_from_submitted_kg"]
print(f"FINDING periods: 5 December-labelled totes overstated production emissions by {lv_pe} kg as submitted (relabelled in the live sheet); "
      f"on the inventory's periods for all 8 totes: {x['total_effect_kg']} kg; "
      f"PE {x['pe_sheet_kg']} -> {x['pe_corrected_kg']} kg; CI {x['ci_sheet']} -> {x['ci_corrected']}; net +{x['net_understated_t']} t")
so = log["shipping_orders_2025_12"]; lv = log["live_ops_notes_2026_09_29"]; lc = log["certify"]["live_change_since_qa"]
print(f"FINDING trucks: Truck 1 (40) is two 20-tote orders -> allocation {so['allocation_by_order_mi']} mi vs {alloc} mi; embodied {so['embodied_by_order_t']} t (+{so['embodied_increase_t']} t)")
print(f"LIVE 2026-09-29: Ops Notes I50 {lv['I50']} kg / D50 {lv['D50']} = CI {lv['I50']/lv['D50']:.10f}; H50 {lv['H50']}; Certify pyrolysis {lc['pyrolysis_t']} t (= {lv['I50']/1000:.3f}), net {lc['net_t']} t")
sys.exit(1 if bad else 0)
