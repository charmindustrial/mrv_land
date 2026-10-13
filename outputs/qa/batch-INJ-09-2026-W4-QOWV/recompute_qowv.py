#!/usr/bin/env python3
"""Deterministic recompute for the Charm QOWV (Aqueous) weekly batch INJ-09-2026-W4.
Run from the batch output folder BEFORE delivery. Re-sums every tote from the raw Ops Notes
export and rebuilds every Certify component and the net twice:
  (1) on Certify's own inputs, which must reproduce Certify exactly (arithmetic checks, gating);
  (2) on the evidence (live 2026 EF sheet, production-record truck counts, live period summaries),
      where every difference from Certify is printed as 'FINDING <row>: ...' naming the checklist
      row that carries it. Routed findings do not change the exit code.
Exit non-zero only if an arithmetic check fails (a discrepancy not yet routed) or the script cannot run."""
import json, glob, sys, math, openpyxl

ops = "source_exports/INJ-09-2026-W4_Ops_Notes.xlsx"
log = json.load(open(glob.glob("batch_*_source_reads.json")[0]))
wb = openpyxl.load_workbook(ops, data_only=True)
ws, sh = wb["QOWV"], wb["QOWV Shipments & EE Allocation"]

rows = [dict(tag=str(int(ws[f"A{r}"].value)), B=ws[f"B{r}"].value, C=ws[f"C{r}"].value, D=ws[f"D{r}"].value,
             E=ws[f"E{r}"].value, F=ws[f"F{r}"].value, G=ws[f"G{r}"].value, H=ws[f"H{r}"].value,
             I=ws[f"I{r}"].value, J=ws[f"J{r}"].value)
        for r in range(11, 53) if ws[f"B{r}"].value not in (None, "")]
n = len(rows)
gross = round(sum(x["B"] for x in rows), 4)
produced = round(sum(x["B"] - x["C"] for x in rows), 4)          # D = B - C, rebuilt
injected = round(sum(x["B"] - x["E"] for x in rows), 4)          # F = B - E (measured post-unload), rebuilt
pe_kg = sum((x["B"] - x["C"]) * x["H"] for x in rows)            # I = H * D, rebuilt
unc = round(n * 2.5 * 0.453592, 5)
ci = pe_kg / produced
per_row_ok = all(abs((x["B"] - x["C"]) - x["D"]) < 1e-9 and abs((x["B"] - x["E"]) - x["F"]) < 1e-9
                 and abs(x["H"] * x["D"] - x["I"]) < 1e-6 for x in rows)
K = log["ops_notes"]["constants"]
ci_by_label_ok = all(abs(x["H"] - {"June 2026": K["L18_Jun2026"], "July 2026": K["L7_qowv_6mo_ci_jul_dec_2026"],
                                   "February 2026": K["L14_Feb2026"]}[x["G"].split(", ")[-1]]) < 1e-9 for x in rows)

C = log["certify"]; cb = C["component_by_key"]
seq, proc, emb, pyro, bcu = (cb[k] for k in ("injection_sequestration", "transport_process", "transport_embodied", "pyrolysis", "bcu"))
cpct = seq["inputs"]["carbon_content_pct"] / 100
dist = proc["inputs"]["distance_mi"]
EF = log["standard_efs_2026"]

# allocation rebuilt from the tab's inputs, not its outputs
trucks = [(sh[f"A{r}"].value, sh[f"C{r}"].value, sh[f"D{r}"].value) for r in range(12, 16)]
one_way = sh["B8"].value
alloc_tab = sum(b / t * one_way for _, t, b in trucks)

# ---- (1) Certify as submitted, on Certify's own inputs ----
seq_t = injected * cpct * 3.667 / 1000
proc_cert_t = gross / 1000 * dist * proc["inputs"]["ef_kgco2e_per_t_mi"] / 1000        # 0.1143 kg/(t*mi) = tanker row
emb_cert_t = emb["inputs"]["distance_mi"] * emb["inputs"]["ef_kgco2e_per_mi"] / 1000    # 0.23756 kg/mi = tanker row
pyro_cert_t = produced / 1000 * pyro["inputs"]["ci_tco2e_per_t"]
bcu_t = bcu["inputs"]["constant_co2_reduction_kg"] / 1000
rel_c = seq["inputs"]["carbon_content_uncertainty_pct_abs"] / seq["inputs"]["carbon_content_pct"]
rel_m = seq["inputs"]["mass_of_product_uncertainty_kg"] / seq["inputs"]["mass_of_product_kg"]
def discount_kg(seq_t, proc_t, pyro_t, rel_c, produced):
    return 1000 * math.sqrt((seq_t * math.hypot(rel_c, rel_m))**2 + (proc_t * unc / gross)**2 + (pyro_t * unc / produced)**2)
disc_cert = discount_kg(seq_t, proc_cert_t, pyro_cert_t, rel_c, produced)
net_cert_t = seq_t + bcu_t - (proc_cert_t + emb_cert_t + pyro_cert_t) - disc_cert / 1000

checks = [
    ("n_totes", n, log["n_totes"]),
    ("per_row_formulas_D_F_I_rebuild", per_row_ok, True),
    ("per_tote_ci_matches_period_constant", ci_by_label_ok, True),
    ("gross_kg", gross, log["ops_notes_totals"]["total_mass_transported_kg"]),
    ("produced_kg", produced, log["ops_notes_totals"]["total_oil_produced_kg"]),
    ("injected_kg", injected, log["ops_notes_totals"]["total_oil_in_batch_kg"]),
    ("production_emissions_kg", round(pe_kg, 4), round(log["ops_notes_totals"]["production_emissions_kg"], 4)),
    ("weighted_ci_within_1e-9_of_H54", abs(ci - log["ops_notes_totals"]["weighted_avg_ci_kgco2e_per_kg"]) < 1e-9, True),
    ("weighted_ci_vs_certify_6dp", round(ci, 6), pyro["inputs"]["ci_tco2e_per_t"]),
    ("uncertainty_kg", unc, round(log["ops_notes_totals"]["uncertainty_kg"], 5)),
    ("uncertainty_vs_certify_seq", unc, seq["inputs"]["mass_of_product_uncertainty_kg"]),
    ("uncertainty_vs_certify_proc_display", round(unc, 3), proc["inputs"]["mass_of_load_uncertainty_kg_displayed"]),
    ("uncertainty_vs_certify_pyro_display", round(unc, 3), pyro["inputs"]["mass_uncertainty_kg_displayed"]),
    ("carbon_pct_vs_lab", seq["inputs"]["carbon_content_pct"], log["testing"]["qowv_certificate"]["carbon_pct"]),
    ("mass_of_product_kg", injected, seq["inputs"]["mass_of_product_kg"]),
    ("mass_of_load_kg", gross, proc["inputs"]["mass_of_load_kg"]),
    ("pyrolysis_mass_kg", produced, pyro["inputs"]["mass_kg"]),
    ("alloc_miles_rebuilt_from_tab_inputs", round(alloc_tab, 2), emb["inputs"]["distance_mi"]),
    ("alloc_miles_vs_tab_total", round(alloc_tab, 6), round(log["shipment_tracker"]["totals"]["allocated_miles_mi"], 6)),
    ("process_ef_is_sheet_tanker_row", round(EF["tanker_process"]["value"] * 1000, 4), proc["inputs"]["ef_kgco2e_per_t_mi"]),
    ("embodied_ef_is_sheet_tanker_row", round(EF["tanker_embodied"]["value"] * 1000, 5), emb["inputs"]["ef_kgco2e_per_mi"]),
    ("seq_t", round(seq_t, 3), seq["value_t"]),
    ("proc_t_certify_inputs", round(proc_cert_t, 3), proc["value_t"]),
    ("emb_t_certify_inputs", round(emb_cert_t, 3), emb["value_t"]),
    ("pyro_t", round(pyro_cert_t, 3), pyro["value_t"]),
    ("bcu_t_display", round(bcu_t, 3), round(proc_cert_t, 3)),
    ("discount_estimate_rounds_to_certify", round(disc_cert), C["uncertainty_discount_kg"]),
    ("net_t", round(net_cert_t, 3), C["net_co2e_removed_t"]),
    ("standard_loss_not_applied", log["ops_notes_totals"]["standard_loss_applied"], False),
    ("lcs_component_needed", log["lcs_use_kg"], None),
]
bad = [(k, a, b) for k, a, b in checks if a != b]
for k, a, b in checks:
    print(f"{'OK ' if a == b else 'BAD'} {k}: recomputed {a} vs certify/log {b}")
print(f"\nas submitted: seq {seq_t*1000:.4f} kg, process {proc_cert_t*1000:.4f} kg, embodied {emb_cert_t*1000:.4f} kg, "
      f"pyrolysis {pyro_cert_t*1000:.4f} kg, BCU {bcu_t*1000:.0f} kg, discount estimate {disc_cert:.2f} kg -> net {net_cert_t:.5f} t")

# ---- (2) differences between Certify and the evidence: findings ----
proc_ok_t = gross / 1000 * dist * EF["flatbed_process"]["value"]
print(f"\nFINDING 5.1: process EF is the sheet's Tanker row ({EF['tanker_process']['value']} MT/t-mi); the Flatbed row is "
      f"{EF['flatbed_process']['value']} MT/t-mi. {gross/1000} t x {dist} mi x {EF['flatbed_process']['value']} = {proc_ok_t:.6f} t vs "
      f"{proc_cert_t:.6f} t submitted (+{proc_ok_t-proc_cert_t:.6f} t)")
inv = dict(log["shipment_tracker"]["inventory_denominators"])
inv["COLA-40"] = log["shipment_tracker"]["cola40_documented_count"]["tab_C15"]   # documented physical count (A19 annotation)
alloc_inv = sum(b / inv[name] * one_way for name, t, b in trucks)
for name, t, b in trucks:
    if t != inv[name]:
        print(f"FINDING 3.4: {name} totes on truck {t:g} on the tab vs {inv[name]} on the production record -> share "
              f"{b/t:.10f} vs {b/inv[name]:.10f}, {b/t*one_way:.4f} vs {b/inv[name]*one_way:.4f} mi")
print(f"NOTE COLA-40: tab 18 is the physical count documented in A19; inventory master lists "
      f"{log['shipment_tracker']['inventory_denominators']['COLA-40']} (A19 flags it for upstream reconciliation); 18 kept")
print(f"FINDING 3.4: batch mileage allocation {alloc_tab:.4f} mi on the tab vs {alloc_inv:.4f} mi with COLA-38 over its 18 totes "
      f"({alloc_tab-alloc_inv:+.4f} mi)")
emb_ok_t = alloc_inv * EF["non_tanker_embodied"]["value"]
emb_ef_only_t = alloc_tab * EF["non_tanker_embodied"]["value"]
print(f"FINDING 6.1: embodied EF is the sheet's Tanker row ({EF['tanker_embodied']['value']} MT/mi); the Non-Tanker row is "
      f"{EF['non_tanker_embodied']['value']} MT/mi. On the tab's {alloc_tab:.4f} mi: {emb_ef_only_t:.6f} t vs {emb_cert_t:.6f} t "
      f"submitted ({emb_ef_only_t-emb_cert_t:+.6f} t); with 3.4 also corrected: {emb_ok_t:.6f} t ({emb_ok_t-emb_cert_t:+.6f} t)")
c_unc_ok = round(seq["inputs"]["carbon_content_pct"] * 0.004, 5)
print(f"FINDING 4.4: carbon uncertainty {seq['inputs']['carbon_content_uncertainty_pct_abs']} percentage points in Certify vs "
      f"0.004 x {seq['inputs']['carbon_content_pct']} = {c_unc_ok} (Ops Notes Summary!G20 {log['summary_tab']['G20_c_unc']} as a fraction); "
      f"{seq['inputs']['carbon_content_uncertainty_pct_abs']/c_unc_ok-1:+.4%} relative")
used = K["L7_qowv_6mo_ci_jul_dec_2026"]
# 7.2 CIs computed from the summary workbooks themselves (Aqueous row 4 of the allocation table):
# Aqueous emissions = R4 x (I32 - I19 + C11) after BCUs, R4 x I32 as the sheet states; CI = emissions x 1000 / N4
def _summary(path):
    w = openpyxl.load_workbook(path, data_only=True); ws = w[[n for n in w.sheetnames if "PP Summary" in n][0]]
    g = lambda c: ws[c].value or 0
    return dict(N4=g("N4"), R4=g("R4"), I32=g("I32"), I19=g("I19"), C11=g("C11"))
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
LIVE = {m: _summary(f"source_exports/pp_summaries/{m}2026_PP_Summary.xlsx") for m in MONTHS}
PKG = {m: _summary(f"source_exports/pp_summaries/package/{m}2026_PP_Summary_package.xlsx") for m in MONTHS}
after_ci = {m: v["R4"] * (v["I32"] - v["I19"] + v["C11"]) * 1000 / v["N4"] for m, v in LIVE.items()}
pkg_ci = {m: v["R4"] * (v["I32"] - v["I19"] + v["C11"]) * 1000 / v["N4"] for m, v in PKG.items()}
after_blend = sum(v["R4"] * (v["I32"] - v["I19"] + v["C11"]) for v in LIVE.values()) * 1000 / sum(v["N4"] for v in LIVE.values())
live_ci = sum(v["R4"] * v["I32"] for v in LIVE.values()) * 1000 / sum(v["N4"] for v in LIVE.values())
v2_rebuilt = sum(v["R4"] * (v["I32"] - v["I19"] + v["C11"]) for v in PKG.values()) * 1000 / sum(v["N4"] for v in PKG.values())
july = [x for x in rows if x["G"].endswith("July 2026")]
jm = sum(x["D"] for x in july)
pe_ok = sum(x["D"] * (live_ci if x["G"].endswith("July 2026") else x["H"]) for x in rows)        # all totes before BCUs (live basis)
mon = {"June 2026": "Jun", "February 2026": "Feb"}
pe_after = sum(x["D"] * (after_blend if x["G"].endswith("July 2026") else after_ci[mon[x["G"].split(", ")[-1]]]) for x in rows)  # all totes after BCUs
PKV = {"June 2026": pkg_ci["Jun"], "February 2026": pkg_ci["Feb"], "July 2026": used}          # package versions (V2's sources), after BCUs
pe_pkg = sum(x["D"] * PKV[x["G"].split(", ")[-1]] for x in rows)
pe_lv = sum(x["D"] * (after_blend if x["G"].endswith("July 2026") else after_ci[mon[x["G"].split(", ")[-1]]]) for x in rows)   # linked sheets, blend rebuilt
print(f"FINDING 7.2: per the 2026-10-07 ruling (BCUs on diesel transport incl. biomass transport process and handling, not embodied) production "
      f"CIs count biomass transport after its BCUs; the June/February CIs come from linked sheets that count it before. Package versions (V2's sources) "
      f"throughout: June {PKV['June 2026']:.10f}, February {PKV['February 2026']:.10f}, July {used} (blend rebuilt from the package files {v2_rebuilt:.10f}): production emissions {pe_kg:.4f} -> {pe_pkg:.4f} kg "
      f"({pe_pkg-pe_kg:+.4f} kg), weighted CI {pe_pkg/produced:.10f}. Linked sheets throughout: June {after_ci['Jun']:.10f}, February {after_ci['Feb']:.10f}, "
      f"blend rebuilt {after_blend:.10f}: {pe_lv:.4f} kg ({pe_lv-pe_kg:+.4f} kg), weighted CI {pe_lv/produced:.10f}")
print(f"NOTE 7.2: which summary version governs is for the blend owner; for reference, the linked sheets' own basis (before BCUs) would give a July "
      f"blend of {live_ci:.10f} and {pe_ok:.4f} kg")
print(f"FINDING 8.1: BCU {bcu_t*1000:.0f} kg vs process emission as submitted {proc_cert_t*1000:.4f} kg "
      f"({bcu_t*1000-proc_cert_t*1000:+.4f} kg); vs process on the Flatbed factor {proc_ok_t*1000:.4f} kg "
      f"({bcu_t*1000-proc_ok_t*1000:+.4f} kg)")
cf = log["cobb_injection_record"]["post_unload_conflicts"]["301215"]
_oid = list(openpyxl.load_workbook("source_exports/inventory_master_export.xlsx", read_only=True, data_only=True)["Oil_inventory_data"].iter_rows(min_row=39, max_row=40, values_only=True))
_r39, _r40 = _oid
assert str(_r39[2]).replace(".0", "") == "301274" and str(_r40[2]).replace(".0", "") == "301277"
t274 = next(x for x in rows if x["tag"] == "301274")
d_g = _r39[11] - t274["B"]
print(f"FINDING 2.3: 301274 gross {t274['B']} kg in the Ops Notes vs {_r39[11]} kg in the production system's weighing "
      f"(Oil_inventory_data row 39, {_r39[7]}) ({d_g:+.1f} kg); post-unload measured in the Ops Notes (E {t274['E']} kg). If {_r39[11]} kg: sequestration "
      f"{d_g*cpct*3.667:+.4f}, production emissions {d_g*t274['H']:+.4f}, net {d_g*cpct*3.667-d_g*t274['H']:+.4f} kg CO2e. The Ops Notes' {t274['B']} kg "
      f"equals the production weighing of 301277 (Oil_inventory_data row 40: {_r40[7]}, gross {_r40[11]} kg)")
print(f"NOTE 2.3: per the 2026-10-07 ruling the injection tracker's COBB tabs are not a cross-check; the COBB-only conflict on 301215 "
      f"(post-unload {cf['ops_notes_E26_kg']} kg in the Ops Notes vs {cf['tracker_implied_kg']} kg implied by COBB) is not carried")
TW = log["tote_weighing_records"]; CO = TW["june_totes_weighed_in_july"]["corroboration"]
jun_tags = sorted(x["tag"] for x in TW["june_totes_weighed_in_july"]["totes"])
jul_tags = sorted(x["tag"] for x in TW["july_totes_weighed_after_july"]["totes"])
jun_ok = (abs(CO["q4_june_qowv_net_kg"] - CO["june_summary_aqueous_mass_N4_kg"]) < 1e-6 and abs(CO["v2_blend_june_qowv_mass_D12_kg"] - CO["june_summary_aqueous_mass_N4_kg"]) < 1e-6
          and CO["four_totes_inside_june_qowv_rows"] == jun_tags)
print(f"NOTE 3.5: totes {', '.join(jun_tags)} (June 2026 label, June CI) and {', '.join(jul_tags)} (July 2026 label, blended CI) were weighed in the "
      f"following month (2026-07-01, 2026-08-31). The June summary's Aqueous mass {CO['june_summary_aqueous_mass_N4_kg']} kg equals the {CO['q4_june_qowv_rows']} "
      f"June-labelled QOWV rows ({CO['q4_june_qowv_net_kg']} kg, the four June totes included) and the Jan-Jun blend's June mass "
      f"({CO['v2_blend_june_qowv_mass_D12_kg']} kg): {jun_ok}. Each tote's CI matches its labelled period; no change to the removal (documentation flag: no fill date)")

# net with every evidence-side correction (seq unchanged; BCU set equal to the corrected process emission),
# across the CI basis choice in 7.2
glec = gross / 1000 * dist * 1.609344 * 0.086                     # kg, if Certify keeps the GLEC 0.086 kg/(km*t) flatbed datapoint used on W3
print(f"\nBCU must equal the corrected process component's output: {proc_ok_t*1000:.4f} kg on the sheet's {EF['flatbed_process']['value']}; "
      f"{glec:.4f} kg if the component uses GLEC 0.086 kgCO2e/(km*t) as on INJ-09-2026-W3-QOWV")
for label, pe_case in (("after BCUs, package versions", pe_pkg), ("after BCUs, linked sheets with the blend rebuilt", pe_lv)):
    d = discount_kg(seq_t, proc_ok_t, pe_case / 1000, c_unc_ok / seq["inputs"]["carbon_content_pct"], produced)
    net = seq_t + proc_ok_t - (proc_ok_t + emb_ok_t + pe_case / 1000) - d / 1000
    print(f"net on the evidence, CI {label}: {net:.5f} t ({net-net_cert_t:+.5f} t vs {net_cert_t:.5f} t as submitted); "
          f"pyrolysis {pe_case:.4f} kg, embodied {emb_ok_t*1000:.4f} kg, discount estimate {d:.2f} kg")
print(f"fix values: process EF Flatbed {EF['flatbed_process']['value']} MT/t-mi -> {proc_ok_t:.6f} t; BCU = corrected process output; "
      f"embodied EF Non-Tanker {EF['non_tanker_embodied']['value']} MT/mi on {alloc_inv:.4f} mi -> {emb_ok_t:.6f} t; "
      f"carbon uncertainty {c_unc_ok}; pyrolysis CI after BCUs on the governing summary version ({pe_pkg/produced:.10f} package, {pe_lv/produced:.10f} linked)")

sys.exit(1 if bad else 0)
