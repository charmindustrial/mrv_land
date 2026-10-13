#!/usr/bin/env python3
"""Writes one compute_mass_chain.py input per W4 offload (14) from the W4 source-read log,
runs the script on each, and writes mass_chain/summary.json.

SHPX215079 offloads 1-2 were injected in W2; their nets come from the W2 log
(prior_weeks.w2_SHPX215079) so the last-offload rule can be tested on offload 4."""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
SCRIPT = ROOT / "skills/qa/_lab/batch-qa-aecn-deterministic/scripts/compute_mass_chain.py"
L = json.load(open(HERE / "batch_INJ-09-2026-W4-AECN_source_reads.json"))
ops, tix, cobb = L["ops_notes"], L["scale_tickets"]["offloads"], L["cobb"]
w2 = L["prior_weeks"]["w2_SHPX215079"]
DATE = {"SHPX215053": "9.1.2026", "SHPX215039": "8.6.2026", "SHPX215091": "8.11.2026", "SHPX215079": "8.4.2026"}
cobb_row = {d["consumed_lot"]: d["row"] for d in cobb["rows_latest"]}

summary, worst = [], 0
for key, t in tix.items():
    car, n = t["railcar"], t["offload"]
    oid = f"Rail_{car}_{DATE[car]}_offload_{n}"
    table = [{"id": r["id"], "cargo_kg": r["cargo_kg"]} for r in ops["offload_table"] if r["railcar"] == car]
    if car == "SHPX215079":
        table = [{"id": f"Rail_SHPX215079_8.4.2026_offload_1", "cargo_kg": w2["offload_1_net_kg"], "_from": "W2 log"},
                 {"id": f"Rail_SHPX215079_8.4.2026_offload_2", "cargo_kg": w2["offload_2_net_kg"], "_from": "W2 log"}] + table
    bols = L["bols"]["per_railcar"][car]
    log = {"batch_id": f"INJ-09-2026-W4::{oid}", "_schema_version": "1.0", "offload": f"offload_{n}", "railcar": car,
           "scale_tickets": {"full_ticket": {"gross_weight_lb": t["full_ticket"]["gross_weight_lb"]},
                             "empty_ticket": {"gross_weight_lb": t["empty_ticket"]["gross_weight_lb"]},
                             "computed_net_lb": t["computed_net_lb"], "computed_net_kg": t["computed_net_kg"]},
           "ops_notes": {"bols_into_railcar": [{"bol": b, "mass_MT": L["bols"]["per_bol"][b]["qty_shipped_mt"]} for b in bols["bols"]],
                         "total_railcar_loaded_MT": bols["sum_qty_shipped_mt"], "offload_table": table},
           "cobb": {"row_id_at_qa": cobb_row[oid], "batch_id_col_a": cobb["batch_id_col_a"],
                    "offloaded_quantity_kg": cobb["offloaded_quantity_kg"][oid]},
           "_note": "Per-offload input built from the W4 source-read log; cargo_kg = Ops 'AECN Rail' F (net) less J (Uncertainty Adjustment); total_railcar_loaded_MT = sum of BOL 'Qty shipped' read from the BOL images"}
    d = HERE / "mass_chain" / oid
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"batch_{oid}_source_reads.json"
    p.write_text(json.dumps(log, indent=1))
    r = subprocess.run([sys.executable, str(SCRIPT), str(p)], capture_output=True, text=True)
    worst = max(worst, r.returncode)
    for c in json.load(open(d / "mass_chain_findings.json"))["checks"]:
        summary.append({"offload": oid, "check_id": c["check_id"], "check_type": c["check_type"], "status": c["status"], "note": c["note"]})
    print(oid, r.stdout.strip().splitlines()[-1])
(HERE / "mass_chain" / "summary.json").write_text(json.dumps(summary, indent=1))
from collections import Counter
print(Counter(s["status"] for s in summary))
for s in summary:
    if s["status"] not in ("PASS", "SKIP"):
        print(s["offload"], s["check_id"], s["status"], "|", s["note"])
print("exit codes max:", worst)
