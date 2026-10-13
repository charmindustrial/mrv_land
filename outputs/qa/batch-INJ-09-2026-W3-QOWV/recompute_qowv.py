#!/usr/bin/env python3
"""Deterministic recompute for the Charm QOWV (Aqueous) weekly batch INJ-09-2026-W3.
Run from the batch output folder BEFORE delivery. Re-sums every tote from the raw Ops Notes
export, rebuilds every Certify component and the net from the live 2026 EF values, and exits
non-zero on any mismatch between a recomputed figure and the Certify values in the source-read
log. Findings against the production record (inventory master) are quantified and printed but
do not change the exit code: they are checklist findings, not arithmetic mismatches."""
import json, glob, sys, math, openpyxl

ops = "source_exports/INJ-09-2026-W3_Ops_Notes.xlsx"
log = json.load(open(glob.glob("batch_*_source_reads.json")[0]))
ws = openpyxl.load_workbook(ops, data_only=True)["QOWV"]
sh = openpyxl.load_workbook(ops, data_only=True)["QOWV Shipments & EE Allocation"]

rows = [dict(tag=ws[f"A{r}"].value, B=ws[f"B{r}"].value, C=ws[f"C{r}"].value, D=ws[f"D{r}"].value,
             E=ws[f"E{r}"].value, F=ws[f"F{r}"].value, G=ws[f"G{r}"].value, H=ws[f"H{r}"].value,
             I=ws[f"I{r}"].value, J=ws[f"J{r}"].value)
        for r in range(11, 49) if ws[f"B{r}"].value not in (None, "")]

n = len(rows)
gross = round(sum(x["B"] for x in rows), 4)
produced = round(sum(x["B"] - x["C"] for x in rows), 4)          # D = B - C, rebuilt
injected = round(sum(x["B"] - x["E"] for x in rows), 4)          # F = B - E, rebuilt (measured post-unload)
pe_kg = sum((x["B"] - x["C"]) * x["H"] for x in rows)            # I = H * D, rebuilt
unc = round(n * 2.5 * 0.453592, 5)
ci = pe_kg / produced
per_row_ok = all(abs((x["B"] - x["C"]) - x["D"]) < 1e-9 and abs((x["B"] - x["E"]) - x["F"]) < 1e-9
                 and abs(x["H"] * x["D"] - x["I"]) < 1e-6 for x in rows)

cb = log["certify"]["component_by_key"]
seq, proc, emb, pyro, bcu = (cb[k] for k in ("injection_sequestration", "transport_process",
                                              "transport_embodied", "pyrolysis", "bcu"))
cpct = seq["inputs"]["carbon_content_pct"] / 100
ef_proc = log["standard_efs_2026"]["flatbed_process"]["value"]        # MT/(t*mi)
ef_emb = log["standard_efs_2026"]["non_tanker_embodied"]["value"]     # MT/mi
dist = proc["inputs"]["distance_mi"]

# allocation rebuilt from the tab's inputs, not its outputs
trucks = [(sh[f"C{r}"].value, sh[f"D{r}"].value) for r in range(12, 16)]
one_way = sh["B8"].value
alloc = sum(b / t * one_way for t, b in trucks)

seq_t = injected * cpct * 3.667 / 1000
proc_t = gross / 1000 * dist * ef_proc                                 # Standard EFs sheet basis (0.0001384 MT/t-mi)
glec_km_t = proc["inputs"]["ef_kgco2e_per_km_t"]                       # Certify datapoint: GLEC V3.2 published 0.086 kgCO2e/(km*t)
proc_certify_t = gross / 1000 * dist * 1.609344 * glec_km_t / 1000     # Certify basis
emb_t = alloc * ef_emb
pyro_t = produced / 1000 * pyro["inputs"]["ci_tco2e_per_t"]

# variance-propagation estimate of the discount (inputs only; aggregation is Isometric's)
rel_c = seq["inputs"]["carbon_content_uncertainty_pct_abs"] / seq["inputs"]["carbon_content_pct"]
rel_m = seq["inputs"]["mass_of_product_uncertainty_kg"] / seq["inputs"]["mass_of_product_kg"]
sd_seq = seq_t * math.hypot(rel_c, rel_m)
sd_proc = proc_t * unc / gross
sd_pyro = pyro_t * unc / produced
disc_est_kg = 1000 * math.sqrt(sd_seq**2 + sd_proc**2 + sd_pyro**2)
# net on Certify's own basis (GLEC process value, unrounded discount estimate); Certify shows the
# discount rounded to whole kg, so the displayed 39 kg alone cannot reproduce the third decimal
net_t = seq_t + bcu["value_t"] - (proc_certify_t + emb_t + pyro_t) - disc_est_kg / 1000
net_t_rounded_disc = seq_t + bcu["value_t"] - (proc_certify_t + emb_t + pyro_t) - log["certify"]["uncertainty_discount_kg"] / 1000

checks = [
    ("n_totes", n, log["n_totes"]),
    ("per_row_formulas_D_F_I_rebuild", per_row_ok, True),
    ("gross_kg", gross, log["ops_notes_totals"]["total_mass_transported_kg"]),
    ("produced_kg", produced, log["ops_notes_totals"]["total_oil_produced_kg"]),
    ("injected_kg", injected, log["ops_notes_totals"]["total_oil_in_batch_kg"]),
    ("production_emissions_kg", round(pe_kg, 4), round(log["ops_notes_totals"]["production_emissions_kg"], 4)),
    ("weighted_ci", round(ci, 10), round(log["ops_notes_totals"]["weighted_avg_ci_kgco2e_per_kg"], 10)),
    ("weighted_ci_vs_certify_6dp", round(ci, 6), pyro["inputs"]["ci_tco2e_per_t"]),
    ("uncertainty_kg", unc, round(log["ops_notes_totals"]["uncertainty_kg"], 5)),
    ("uncertainty_vs_certify_seq", unc, seq["inputs"]["mass_of_product_uncertainty_kg"]),
    ("uncertainty_vs_certify_proc_display", round(unc, 2), proc["inputs"]["mass_of_load_uncertainty_kg_displayed"]),
    ("uncertainty_vs_certify_pyro_display", round(unc, 2), pyro["inputs"]["mass_uncertainty_kg_displayed"]),
    ("carbon_unc_pct_abs", round(cpct * 100 * 0.004, 4), seq["inputs"]["carbon_content_uncertainty_pct_abs"]),
    ("mass_of_product_kg", injected, seq["inputs"]["mass_of_product_kg"]),
    ("mass_of_load_kg", gross, proc["inputs"]["mass_of_load_kg"]),
    ("pyrolysis_mass_kg", produced, pyro["inputs"]["mass_kg"]),
    ("alloc_miles_rebuilt", round(alloc, 2), emb["inputs"]["distance_mi"]),
    ("alloc_miles_vs_tab", round(alloc, 6), round(log["shipment_tracker"]["totals"]["allocated_miles_mi"], 6)),
    ("process_ef_display", round(ef_proc * 1000 / 1.609344, 3), proc["inputs"]["ef_kgco2e_per_km_t"]),
    ("embodied_ef_display", round(ef_emb * 1000, 5), emb["inputs"]["ef_kgco2e_per_mi"]),
    ("seq_t", round(seq_t, 3), seq["value_t"]),
    ("proc_t_certify_basis_glec_0.086", round(proc_certify_t, 3), proc["value_t"]),
    ("proc_t_sheet_basis_within_0.001t", abs(proc_t - proc["value_t"]) <= 0.001, True),
    ("emb_t", round(emb_t, 3), emb["value_t"]),
    ("pyro_t", round(pyro_t, 3), pyro["value_t"]),
    ("bcu_matches_process_at_display_precision_t", round(bcu["inputs"]["constant_co2_reduction_kg"] / 1000, 3), round(proc_certify_t, 3)),
    ("net_t", round(net_t, 3), log["certify"]["net_co2e_removed_t"]),
    ("net_with_rounded_39kg_within_0.001t", abs(net_t_rounded_disc - log["certify"]["net_co2e_removed_t"]) <= 0.001, True),
    ("discount_estimate_rounds_to_certify", round(disc_est_kg), log["certify"]["uncertainty_discount_kg"]),
    ("standard_loss_not_applied", log["ops_notes_totals"]["standard_loss_applied"], False),
    ("lcs_component_needed", log["lcs_use_kg"], None),
]
bad = [(k, a, b) for k, a, b in checks if a != b]
for k, a, b in checks:
    print(f"{'OK ' if a == b else 'BAD'} {k}: recomputed {a} vs certify/log {b}")

b = bcu['inputs']['constant_co2_reduction_kg']
print(f"\nprocess emission: sheet basis {proc_t*1000:.3f} kg, Certify/GLEC basis {proc_certify_t*1000:.3f} kg; BCU constant {b} kg; "
      f"BCU minus process = {b - proc_t*1000:+.3f} kg (sheet) / {b - proc_certify_t*1000:+.3f} kg (Certify)")
print(f"BCU <= process emission (the BCU cap, checklist 8.1; not gating here): {b <= proc_certify_t*1000} on the Certify basis, {b <= proc_t*1000} on the sheet basis")
print(f"net = {net_t:.5f} t with discount estimate {disc_est_kg:.2f} kg; {net_t_rounded_disc:.5f} t with displayed 39 kg")
net_sheet_t = seq_t + bcu["value_t"] - (proc_t + emb_t + produced / 1000 * ci) - disc_est_kg / 1000
print(f"net on the EF sheet's process factor and the Ops Notes H50 CI = {net_sheet_t:.5f} t")

# ---- findings against the production record (printed, not gating) ----
may_ci, jun_ci = log["ops_notes"]["constants"]["L17_May2026"], log["ops_notes"]["constants"]["L18_Jun2026"]
t54 = next(x for x in rows if str(x["tag"]).split(".")[0] == "301154")
over_kg = t54["D"] * (jun_ci - may_ci)
pe_fixed = pe_kg - over_kg
print(f"\nFINDING 301154: {t54['D']} kg x ({jun_ci} - {may_ci}) = {over_kg:.4f} kg CO2e overstated; "
      f"corrected PE {pe_fixed:.4f} kg, weighted CI {pe_fixed/produced:.10f}, net +{over_kg/1000:.5f} t")
t09 = next(x for x in rows if str(x["tag"]).split(".")[0] == "120509")
extra = t09["C"] - 62.93
print(f"FINDING 120509: tote mass 57.6 vs inventory tare 62.93 -> produced mass +{-extra:.2f} kg, "
      f"PE +{-extra*t09['H']:.4f} kg CO2e")
alloc_18 = sum(b / (18 if (t, b) == (17, 3) else t) * one_way for t, b in trucks)
print(f"FINDING COLA_32: 17 vs 18 totes on truck -> allocated {alloc:.4f} vs {alloc_18:.4f} mi "
      f"(+{alloc-alloc_18:.4f} mi), embodied +{(alloc-alloc_18)*ef_emb*1000:.4f} kg CO2e")

# net on the production record: 301154 at the May CI, 120509 at its 62.93 kg tare, COLA_32 over 18 totes,
# BCU entered as the exact process emission (Certify basis)
produced_rec = produced - (62.93 - t09["C"])
pe_rec = pe_fixed - (62.93 - t09["C"]) * t09["H"]
emb_rec_t = alloc_18 * ef_emb
bcu_rec_t = proc_certify_t
disc_rec_kg = 1000 * math.sqrt(sd_seq**2 + sd_proc**2 + (pe_rec / 1000 * unc / produced_rec)**2)
net_rec_t = seq_t + bcu_rec_t - (proc_certify_t + emb_rec_t + pe_rec / 1000) - disc_rec_kg / 1000
print(f"net on the production record = {net_rec_t:.5f} t (+{net_rec_t - net_t:.5f} t vs as submitted); "
      f"pyrolysis {pe_rec:.4f} kg on {produced_rec:.2f} kg, CI {pe_rec/produced_rec:.7f}; embodied {emb_rec_t*1000:.3f} kg; "
      f"BCU {bcu_rec_t*1000:.3f} kg; discount estimate {disc_rec_kg:.2f} kg")
alloc_orders = sum(b / tt * one_way for (t, b), tt in zip(trucks, (20, 18, trucks[2][0], 18)))
print(f"FINDING shipping orders: Truck 1 / Truck 2 totes rode 20- and 18-tote orders (Oil_inventory_data) -> allocated {alloc_orders:.4f} mi "
      f"(+{alloc_orders-alloc:.4f} mi vs tab), embodied {alloc_orders*ef_emb:.5f} t (+{(alloc_orders-alloc)*ef_emb:.5f} t); "
      f"net on the production record incl. orders = {net_rec_t - (alloc_orders-alloc_18)*ef_emb:.5f} t")
print(f"fix values: Certify CI {pe_fixed/produced:.6f} (301154 only) -> pyrolysis {produced*round(pe_fixed/produced,6)/1000:.3f} t; "
      f"embodied distance {alloc_orders:.2f} mi -> {alloc_orders*ef_emb:.3f} t; BCU {proc_certify_t*1000:.3f} kg")

sys.exit(1 if bad else 0)
