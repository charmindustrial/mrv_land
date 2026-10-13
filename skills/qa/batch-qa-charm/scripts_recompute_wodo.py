#!/usr/bin/env python3
"""Deterministic recompute for a Charm WODO weekly batch. Run from the batch output folder
BEFORE delivery. Exits non-zero if any figure fails to tie to the Certify log."""
import json, statistics, sys, glob, openpyxl
ops=glob.glob("source_exports/*Ops_Notes.xlsx") or glob.glob("*Ops_Notes.xlsx")
log=json.load(open(glob.glob("batch_*_source_reads.json")[0]))
ws=openpyxl.load_workbook(ops[0],data_only=True)["WODO"]
rows=[(ws[f"A{r}"].value,ws[f"B{r}"].value,ws[f"C{r}"].value,ws[f"G{r}"].value,ws[f"H{r}"].value) for r in range(11,31) if isinstance(ws[f"A{r}"].value,(int,float))]
n=len(rows); gross=sum(b for _,b,_,_,_ in rows); net=gross-sum(c for _,_,c,_,_ in rows)
sl=ws["L8"].value*n; inj=net-sl; pe=sum((b-c)*h for _,b,c,_,h in rows); ci=pe/net; unc=n*2.5*0.453592
c=log["certify"]["components"]; cv=log["certify"]["calculation_view"]
seq=next(x for x in c if "sequestration" in x["name"].lower()); proc=next(x for x in c if "Process Emissions" in x["name"])
emb=next(x for x in c if "Embodied" in x["name"]); pyro=next(x for x in c if "Pyrolysis" in x["name"]); bcu=next(x for x in c if "BCU" in x["name"])
cpct=seq["inputs"]["carbon_content_pct"]/100; fb=proc["inputs"]["ef_kgco2e_per_t_mi"]; dist=proc["inputs"]["distance_mi"]
nt=emb["inputs"]["ef_kgco2e_per_mi"]; alloc=log["shipment_allocation"]["allocated_miles_mi"]
seq_t=inj*cpct*3.667/1000; proc_t=gross/1000*dist*fb/1000; emb_t=alloc*nt/1000; pyro_t=net*ci/1000
net_t=seq_t+bcu["value_t"]-(proc_t+emb_t+pyro_t)-cv["uncertainty_discount_kg"]/1000
checks=[("n_totes",n,log["n_totes"]),("gross",gross,log["ops_notes_totals"]["total_mass_transported_kg"]),
 ("net_produced",round(net,2),log["ops_notes_totals"]["total_oil_produced_kg"]),("net_injected",round(inj,2),log["ops_notes_totals"]["total_oil_in_batch_kg"]),
 ("weighted_ci",round(ci,6),round(log["ops_notes_totals"]["weighted_avg_ci"],6)),("uncertainty",round(unc,5),seq["inputs"]["mass_uncertainty_kg"]),
 ("c_unc",round(cpct*100*0.004,4),seq["inputs"]["carbon_content_uncertainty_pct_abs"]),("mass_of_load",gross,proc["inputs"]["mass_of_load_kg"]),
 ("seq_t",round(seq_t,3),seq["value_t"]),("proc_t",round(proc_t,3),proc["value_t"]),("emb_t",round(emb_t,3),emb["value_t"]),
 ("pyro_t",round(pyro_t,3),round(pyro["value_t"],3)),("pyro_mass",round(net,1),pyro["inputs"]["mass_kg"]),
 ("bcu_matches_proc_at_display_precision",round(bcu["value_t"],3),round(proc_t,3)),("net_t",round(net_t,3),cv["net_t"])]
bad=[(k,a,b) for k,a,b in checks if a!=b]
for k,a,b in checks: print(f"{'OK ' if a==b else 'BAD'} {k}: recomputed {a} vs certify/log {b}")
bcu_kg=bcu["value_t"]*1000 if "constant_co2_reduction_kg" not in bcu.get("inputs",{}) else bcu["inputs"]["constant_co2_reduction_kg"]
print(f"BCU {bcu_kg} kg vs process emission {proc_t*1000:.4f} kg: BCU minus process = {bcu_kg-proc_t*1000:+.4f} kg; BCU <= process (BCU QA Rule, checklist 8.1): {bcu_kg <= proc_t*1000 + 1e-9}")
sys.exit(1 if bad else 0)
