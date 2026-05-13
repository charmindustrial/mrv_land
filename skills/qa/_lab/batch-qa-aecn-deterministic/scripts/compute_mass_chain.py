#!/usr/bin/env python3
"""
compute_mass_chain.py — deterministic mass-chain reconciliation for AECN batches.

Reads batch_<ID>_source_reads.json and emits mass_chain_findings.json
to the same directory. One entry per check_id with status, materiality,
computed block (script's own arithmetic), log_values block, one-line note.

Spec: skills/qa/_lab/batch-qa-aecn-deterministic/ (mass-chain pilot).
"""
import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

LB_TO_KG = 0.453592
TOLERANCE_PCT = 0.5
LOSS_FLAG_PCT = 5.0


def _is_railcar_batch(log):
    return bool(log.get("railcar"))


def _offload_num(row_id):
    if not isinstance(row_id, str):
        return -1
    try:
        return int(row_id.rsplit("offload_", 1)[-1])
    except ValueError:
        return -1


def _find_offload_row(log):
    offload_id = log.get("offload")
    if not offload_id:
        return None
    target = _offload_num(offload_id)
    for row in log.get("ops_notes", {}).get("offload_table", []) or []:
        if _offload_num(row.get("id", "")) == target:
            return row
    return None


def _pct_delta(a, b):
    ref = max(abs(a), abs(b))
    if ref == 0:
        return 0.0
    return round(abs(a - b) / ref * 100, 4)


def _skip(check_id, materiality, note, computed=None, log_values=None):
    return {
        "check_id": check_id,
        "materiality": materiality,
        "status": "SKIP",
        "computed": computed or {},
        "log_values": log_values or {},
        "note": note,
    }


def _insufficient(check_id, materiality, note):
    return {
        "check_id": check_id,
        "materiality": materiality,
        "status": "INSUFFICIENT_DATA",
        "computed": {},
        "log_values": {},
        "note": note,
    }


def check_scale_ticket_subtraction(log):
    cid, mat = "scale_ticket_subtraction", "material"
    try:
        full = log["scale_tickets"]["full_ticket"]["gross_weight_lb"]
        empty = log["scale_tickets"]["empty_ticket"]["gross_weight_lb"]
        log_net_lb = log["scale_tickets"]["computed_net_lb"]
        log_net_kg = log["scale_tickets"]["computed_net_kg"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat,
            "Missing scale_tickets.full_ticket.gross_weight_lb, .empty_ticket.gross_weight_lb, .computed_net_lb, or .computed_net_kg.")

    computed_net_lb = full - empty
    computed_net_kg = round(computed_net_lb * LB_TO_KG, 2)
    log_net_kg_rounded = round(log_net_kg, 2)

    lb_match = computed_net_lb == log_net_lb
    kg_match = computed_net_kg == log_net_kg_rounded
    status = "PASS" if lb_match and kg_match else "FAIL"
    note = (
        f"Computed: {full} − {empty} = {computed_net_lb} lb ({computed_net_kg} kg). "
        f"Log: {log_net_lb} lb ({log_net_kg} kg). "
        f"{'Match.' if status == 'PASS' else 'MISMATCH.'}"
    )
    return {
        "check_id": cid, "materiality": mat, "status": status,
        "computed": {"full_lb": full, "empty_lb": empty,
                     "net_lb": computed_net_lb, "net_kg": computed_net_kg},
        "log_values": {"computed_net_lb": log_net_lb, "computed_net_kg": log_net_kg},
        "note": note,
    }


def check_scale_ticket_vs_ops_notes_offload(log):
    cid, mat = "scale_ticket_vs_ops_notes_offload", "material"
    try:
        scale_kg = log["scale_tickets"]["computed_net_kg"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat, "Missing scale_tickets.computed_net_kg.")

    row = _find_offload_row(log)
    if row is None:
        return _insufficient(cid, mat,
            f"No offload_table row matching offload={log.get('offload')!r}.")
    ops_kg = row.get("cargo_kg")
    if ops_kg is None:
        return _insufficient(cid, mat,
            f"offload_table row {row.get('id')!r} has no cargo_kg.")

    delta_kg = round(scale_kg - ops_kg, 2)
    delta_pct = _pct_delta(scale_kg, ops_kg)
    status = "PASS" if delta_pct <= TOLERANCE_PCT else "FAIL"
    return {
        "check_id": cid, "materiality": mat, "status": status,
        "computed": {"scale_ticket_kg": scale_kg, "ops_notes_cargo_kg": ops_kg,
                     "delta_kg": delta_kg, "delta_pct": delta_pct},
        "log_values": {"matched_offload_row_id": row.get("id")},
        "note": (f"Scale ticket = {scale_kg} kg; Ops Notes cargo = {ops_kg} kg; "
                 f"delta = {delta_kg} kg ({delta_pct}%). Tolerance ≤{TOLERANCE_PCT}%."),
    }


def check_bol_list_sum_vs_stated_total(log):
    cid, mat = "bol_list_sum_vs_stated_total", "hygiene"
    if not _is_railcar_batch(log):
        return _skip(cid, mat, "Not a railcar batch.")
    try:
        bols = log["ops_notes"]["bols_into_railcar"]
        stated_total = log["ops_notes"]["total_railcar_loaded_MT"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat,
            "Missing ops_notes.bols_into_railcar or .total_railcar_loaded_MT.")
    if not bols:
        return _insufficient(cid, mat, "ops_notes.bols_into_railcar is empty.")

    bol_values = [b.get("mass_MT") for b in bols]
    if any(v is None for v in bol_values):
        return _insufficient(cid, mat, "One or more BOLs missing mass_MT.")

    summed = round(sum(bol_values), 2)
    stated_rounded = round(stated_total, 2)
    status = "PASS" if summed == stated_rounded else "FLAG"
    note = (f"Σ(BOLs) = {summed} MT; stated total = {stated_total} MT. "
            f"{'Match.' if status == 'PASS' else 'MISMATCH — Ops Notes data-entry issue.'}")
    return {
        "check_id": cid, "materiality": mat, "status": status,
        "computed": {"bol_sum_MT": summed, "bol_count": len(bols)},
        "log_values": {"total_railcar_loaded_MT": stated_total,
                       "individual_BOL_mass_MT": bol_values},
        "note": note,
    }


def check_railcar_inbound_outbound_balance(log):
    cid, mat = "railcar_inbound_outbound_balance", "mixed"
    if not _is_railcar_batch(log):
        return _skip(cid, mat, "Not a railcar batch.")
    try:
        bols = log["ops_notes"]["bols_into_railcar"]
        offload_table = log["ops_notes"]["offload_table"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat,
            "Missing ops_notes.bols_into_railcar or .offload_table.")

    bol_values = [b.get("mass_MT") for b in bols] if bols else []
    if not bol_values or any(v is None for v in bol_values):
        return _insufficient(cid, mat, "BOL mass_MT values missing or empty.")

    cargo_values = [row.get("cargo_kg") for row in offload_table] if offload_table else []
    if not cargo_values or any(v in (None, 0) for v in cargo_values):
        return _skip(cid, mat,
            "Railcar not fully offloaded — one or more offload_table rows have cargo_kg of 0 or null (sister-batch backfill pending).",
            log_values={"offload_count": len(offload_table or [])})

    inbound_kg = round(sum(bol_values) * 1000, 2)
    outbound_kg = round(sum(cargo_values), 2)
    loss_kg = round(inbound_kg - outbound_kg, 2)
    loss_pct = round(loss_kg / inbound_kg * 100, 4) if inbound_kg else 0.0

    if loss_kg < 0:
        status = "FAIL"
        note = (f"IMPOSSIBLE: outbound ({outbound_kg} kg) > inbound ({inbound_kg} kg) "
                f"by {-loss_kg} kg.")
    elif loss_pct <= LOSS_FLAG_PCT:
        status = "PASS"
        note = (f"Inbound = {inbound_kg} kg; outbound = {outbound_kg} kg; "
                f"loss = {loss_kg} kg ({loss_pct}%). Within ≤{LOSS_FLAG_PCT}%.")
    else:
        status = "FLAG"
        note = (f"Inbound = {inbound_kg} kg; outbound = {outbound_kg} kg; "
                f"loss = {loss_kg} kg ({loss_pct}%). Loss exceeds {LOSS_FLAG_PCT}% — "
                f"operator should explain in Ops Notes.")

    return {
        "check_id": cid, "materiality": mat, "status": status,
        "computed": {"inbound_kg": inbound_kg, "outbound_kg": outbound_kg,
                     "loss_kg": loss_kg, "loss_pct": loss_pct},
        "log_values": {"bol_count": len(bols), "offload_count": len(offload_table)},
        "note": note,
    }


def check_last_offload_derivation(log):
    cid, mat = "last_offload_derivation", "material"
    if not _is_railcar_batch(log):
        return _skip(cid, mat, "Not a railcar batch.")

    this_offload = log.get("offload")
    if not this_offload:
        return _insufficient(cid, mat, "log.offload missing.")

    try:
        offload_table = log["ops_notes"]["offload_table"]
        bols = log["ops_notes"]["bols_into_railcar"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat,
            "Missing ops_notes.offload_table or .bols_into_railcar.")
    if not offload_table:
        return _insufficient(cid, mat, "offload_table empty.")

    sorted_rows = sorted(offload_table, key=lambda r: _offload_num(r.get("id", "")))
    last_row = sorted_rows[-1]
    this_num = _offload_num(this_offload)
    last_num = _offload_num(last_row.get("id", ""))

    if this_num != last_num:
        return _skip(cid, mat,
            f"This batch is offload_{this_num}, not the last offload (last = offload_{last_num}). "
            f"Derivation rule does not apply.",
            computed={"this_offload": this_offload, "last_offload": f"offload_{last_num}"})

    prior_rows = sorted_rows[:-1]
    prior_cargo = [r.get("cargo_kg") for r in prior_rows]
    if any(v is None for v in prior_cargo):
        return _insufficient(cid, mat, "One or more prior offloads lack cargo_kg.")
    actual_kg = last_row.get("cargo_kg")
    if actual_kg is None:
        return _insufficient(cid, mat, "Last offload cargo_kg missing.")

    bol_values = [b.get("mass_MT") for b in bols] if bols else []
    if not bol_values or any(v is None for v in bol_values):
        return _insufficient(cid, mat, "BOL mass_MT values missing.")

    inbound_kg = round(sum(bol_values) * 1000, 2)
    prior_sum_kg = round(sum(prior_cargo), 2)
    expected_kg = round(inbound_kg - prior_sum_kg, 2)
    delta_kg = round(actual_kg - expected_kg, 2)
    delta_pct = _pct_delta(actual_kg, expected_kg)
    status = "PASS" if delta_pct <= TOLERANCE_PCT else "FAIL"

    return {
        "check_id": cid, "materiality": mat, "status": status,
        "computed": {
            "inbound_kg": inbound_kg,
            "prior_offload_sum_kg": prior_sum_kg,
            "expected_last_offload_kg": expected_kg,
            "actual_last_offload_kg": actual_kg,
            "delta_kg": delta_kg,
            "delta_pct": delta_pct,
        },
        "log_values": {"this_offload": this_offload, "last_row_id": last_row.get("id")},
        "note": (f"Expected = {expected_kg} kg (= {inbound_kg} − {prior_sum_kg}); "
                 f"actual = {actual_kg} kg; delta = {delta_kg} kg ({delta_pct}%). "
                 f"Tolerance ≤{TOLERANCE_PCT}%."),
    }


def check_cobb_offload_consistency(log):
    cid, mat = "cobb_offload_consistency", "hygiene"

    cobb_keys = [k for k in log.keys()
                 if k.startswith("cobb_row_") and isinstance(log[k], dict)]
    if not cobb_keys:
        return _insufficient(cid, mat, "No cobb_row_* node found in log.")
    cobb_key = cobb_keys[0]
    cobb_row = log[cobb_key]

    cobb_kg = None
    for k, v in cobb_row.items():
        if "offloaded_quantity_kg" in k:
            cobb_kg = v
            break
    if cobb_kg is None:
        return _insufficient(cid, mat,
            f"No *_offloaded_quantity_kg field in {cobb_key}.")

    row = _find_offload_row(log)
    if row is None:
        return _insufficient(cid, mat,
            f"No offload_table row matching offload={log.get('offload')!r}.")
    ops_kg = row.get("cargo_kg")
    if ops_kg is None:
        return _insufficient(cid, mat,
            f"offload_table row {row.get('id')!r} has no cargo_kg.")

    delta_kg = round(cobb_kg - ops_kg, 2)
    delta_pct = _pct_delta(cobb_kg, ops_kg)
    status = "PASS" if delta_pct <= TOLERANCE_PCT else "FLAG"
    suffix = "Match." if status == "PASS" else "Back-end mismatch — not verifier-facing, warrants review."
    return {
        "check_id": cid, "materiality": mat, "status": status,
        "computed": {"cobb_offloaded_kg": cobb_kg, "ops_notes_cargo_kg": ops_kg,
                     "delta_kg": delta_kg, "delta_pct": delta_pct},
        "log_values": {"cobb_row_key": cobb_key,
                       "matched_offload_row_id": row.get("id")},
        "note": (f"COBB offloaded = {cobb_kg} kg; Ops Notes cargo = {ops_kg} kg; "
                 f"delta = {delta_kg} kg ({delta_pct}%). Tolerance ≤{TOLERANCE_PCT}%. {suffix}"),
    }


CHECKS = [
    check_scale_ticket_subtraction,
    check_scale_ticket_vs_ops_notes_offload,
    check_bol_list_sum_vs_stated_total,
    check_railcar_inbound_outbound_balance,
    check_last_offload_derivation,
    check_cobb_offload_consistency,
]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("source_reads_path", type=Path,
                        help="Path to batch_<ID>_source_reads.json")
    args = parser.parse_args()

    if not args.source_reads_path.exists():
        print(f"ERROR: {args.source_reads_path} does not exist.", file=sys.stderr)
        sys.exit(2)

    with open(args.source_reads_path) as f:
        log = json.load(f)

    checks = [fn(log) for fn in CHECKS]

    findings = {
        "batch_id": log.get("batch_id", "UNKNOWN"),
        "computed_at": datetime.now().isoformat(timespec="seconds"),
        "source_reads_path": str(args.source_reads_path),
        "checks": checks,
    }

    out_path = args.source_reads_path.parent / "mass_chain_findings.json"
    with open(out_path, "w") as f:
        json.dump(findings, f, indent=2)
        f.write("\n")

    counts = {"PASS": 0, "FAIL": 0, "FLAG": 0, "SKIP": 0, "INSUFFICIENT_DATA": 0}
    for c in checks:
        counts[c["status"]] = counts.get(c["status"], 0) + 1

    print(f"Wrote {out_path}")
    print(f"PASS={counts['PASS']}  FAIL={counts['FAIL']}  FLAG={counts['FLAG']}  "
          f"SKIP={counts['SKIP']}  INSUFFICIENT_DATA={counts['INSUFFICIENT_DATA']}")

    if counts["FAIL"] or counts["INSUFFICIENT_DATA"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
