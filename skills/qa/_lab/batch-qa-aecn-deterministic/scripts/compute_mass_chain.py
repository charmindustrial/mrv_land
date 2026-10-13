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
EXPECTED_OFFLOADS = 4  # Standard for AECN rail as of 2026-05-15. Update when ops changes.


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


def _skip(check_id, materiality, check_type, note, computed=None, log_values=None):
    return {
        "check_id": check_id,
        "materiality": materiality,
        "check_type": check_type,
        "status": "SKIP",
        "computed": computed or {},
        "log_values": log_values or {},
        "note": note,
    }


def _insufficient(check_id, materiality, check_type, note):
    return {
        "check_id": check_id,
        "materiality": materiality,
        "check_type": check_type,
        "status": "INSUFFICIENT_DATA",
        "computed": {},
        "log_values": {},
        "note": note,
    }


def check_scale_ticket_subtraction(log):
    cid, mat, ct = "scale_ticket_subtraction", "material", "computation"
    try:
        full = log["scale_tickets"]["full_ticket"]["gross_weight_lb"]
        empty = log["scale_tickets"]["empty_ticket"]["gross_weight_lb"]
        log_net_lb = log["scale_tickets"]["computed_net_lb"]
        log_net_kg = log["scale_tickets"]["computed_net_kg"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat, ct,
            "Missing scale_tickets.full_ticket.gross_weight_lb, .empty_ticket.gross_weight_lb, .computed_net_lb, or .computed_net_kg.")

    computed_net_lb = full - empty
    computed_net_kg = round(computed_net_lb * LB_TO_KG, 2)
    log_net_kg_rounded = round(log_net_kg, 2)

    lb_match = computed_net_lb == log_net_lb
    kg_match = abs(computed_net_kg - log_net_kg_rounded) <= 0.02  # ±0.02 kg covers floating-point lb→kg rounding
    status = "PASS" if lb_match and kg_match else "FAIL"
    note = (
        f"Computed: {full} − {empty} = {computed_net_lb} lb ({computed_net_kg} kg). "
        f"Log: {log_net_lb} lb ({log_net_kg} kg). "
        f"{'Match.' if status == 'PASS' else 'MISMATCH.'}"
    )
    return {
        "check_id": cid, "materiality": mat, "check_type": ct, "status": status,
        "computed": {"full_lb": full, "empty_lb": empty,
                     "net_lb": computed_net_lb, "net_kg": computed_net_kg},
        "log_values": {"computed_net_lb": log_net_lb, "computed_net_kg": log_net_kg},
        "note": note,
    }


def check_scale_ticket_vs_ops_notes_offload(log):
    # Policy check: the comparison involves policy rules (MIN( selection, FC11 back-calc).
    # Scale ticket arithmetic itself is verified by check_scale_ticket_subtraction.
    # A mismatch here means "route to LLM — was the right policy applied, or is this an error?"
    cid, mat, ct = "scale_ticket_vs_ops_notes_offload", "material", "policy"
    try:
        scale_kg = log["scale_tickets"]["computed_net_kg"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat, ct, "Missing scale_tickets.computed_net_kg.")

    row = _find_offload_row(log)
    if row is None:
        return _insufficient(cid, mat, ct,
            f"No offload_table row matching offload={log.get('offload')!r}.")
    ops_kg = row.get("cargo_kg")
    if ops_kg is None:
        return _insufficient(cid, mat, ct,
            f"offload_table row {row.get('id')!r} has no cargo_kg.")

    delta_kg = round(scale_kg - ops_kg, 2)
    delta_pct = _pct_delta(scale_kg, ops_kg)
    status = "PASS" if delta_pct <= TOLERANCE_PCT else "FLAG"
    suffix = ("Match." if status == "PASS" else
              "Difference detected — route to LLM: is this the MIN( rule selecting "
              "BOL mass over scale, FC11 back-calc on a last offload, or a transcription error?")
    return {
        "check_id": cid, "materiality": mat, "check_type": ct, "status": status,
        "computed": {"scale_ticket_kg": scale_kg, "ops_notes_cargo_kg": ops_kg,
                     "delta_kg": delta_kg, "delta_pct": delta_pct},
        "log_values": {"matched_offload_row_id": row.get("id")},
        "note": (f"Scale ticket = {scale_kg} kg; Ops Notes cargo = {ops_kg} kg; "
                 f"delta = {delta_kg} kg ({delta_pct}%). {suffix}"),
    }


def check_bol_list_sum_vs_stated_total(log):
    cid, mat, ct = "bol_list_sum_vs_stated_total", "hygiene", "computation"
    if not _is_railcar_batch(log):
        return _skip(cid, mat, ct, "Not a railcar batch.")
    try:
        bols = log["ops_notes"]["bols_into_railcar"]
        stated_total = log["ops_notes"]["total_railcar_loaded_MT"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat, ct,
            "Missing ops_notes.bols_into_railcar or .total_railcar_loaded_MT.")
    if not bols:
        return _insufficient(cid, mat, ct, "ops_notes.bols_into_railcar is empty.")

    bol_values = [b.get("mass_MT") for b in bols]
    if any(v is None for v in bol_values):
        return _insufficient(cid, mat, ct, "One or more BOLs missing mass_MT.")

    summed = round(sum(bol_values), 2)
    stated_rounded = round(stated_total, 2)
    status = "PASS" if summed == stated_rounded else "FLAG"
    note = (f"Σ(BOLs) = {summed} MT; stated total = {stated_total} MT. "
            f"{'Match.' if status == 'PASS' else 'MISMATCH — Ops Notes data-entry issue.'}")
    return {
        "check_id": cid, "materiality": mat, "check_type": ct, "status": status,
        "computed": {"bol_sum_MT": summed, "bol_count": len(bols)},
        "log_values": {"total_railcar_loaded_MT": stated_total,
                       "individual_BOL_mass_MT": bol_values},
        "note": note,
    }


def check_railcar_inbound_outbound_balance(log):
    cid, mat, ct = "railcar_inbound_outbound_balance", "mixed", "computation"
    if not _is_railcar_batch(log):
        return _skip(cid, mat, ct, "Not a railcar batch.")
    try:
        bols = log["ops_notes"]["bols_into_railcar"]
        offload_table = log["ops_notes"]["offload_table"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat, ct,
            "Missing ops_notes.bols_into_railcar or .offload_table.")

    bol_values = [b.get("mass_MT") for b in bols] if bols else []
    if not bol_values or any(v is None for v in bol_values):
        return _insufficient(cid, mat, ct, "BOL mass_MT values missing or empty.")

    cargo_values = [row.get("cargo_kg") for row in offload_table] if offload_table else []
    if not cargo_values:
        return _insufficient(cid, mat, ct, "offload_table has no rows.")
    if any(v in (None, 0) for v in cargo_values):
        # Incomplete table — cannot verify the physical invariant (sum offloads ≤ sum BOLs).
        # Scale ticket arithmetic is confirmed by scale_ticket_subtraction.
        # Reason for incompleteness requires LLM judgment: cross-RP deferral, out-of-order
        # injection, or sister-batch backfill lag are all legitimate; an unexplained gap is not.
        filled = sum(1 for v in cargo_values if v not in (None, 0))
        total = len(cargo_values)
        return {
            "check_id": cid, "materiality": mat, "check_type": "policy", "status": "FLAG",
            "computed": {},
            "log_values": {"offload_rows_filled": filled, "offload_rows_total": total,
                           "expected_offloads": EXPECTED_OFFLOADS},
            "note": (f"Offload table partially filled ({filled}/{total} rows have cargo_kg). "
                     f"Cannot verify mass conservation (sum offloads ≤ sum BOLs). "
                     f"Scale ticket arithmetic confirmed separately. Route to LLM: is the "
                     f"incomplete table explained by cross-RP deferral, out-of-order injection, "
                     f"or sister-batch backfill lag? If so, document. If not, investigate."),
        }

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
        "check_id": cid, "materiality": mat, "check_type": ct, "status": status,
        "computed": {"inbound_kg": inbound_kg, "outbound_kg": outbound_kg,
                     "loss_kg": loss_kg, "loss_pct": loss_pct},
        "log_values": {"bol_count": len(bols), "offload_count": len(offload_table)},
        "note": note,
    }


def check_last_offload_derivation(log):
    cid, mat, ct = "last_offload_derivation", "material", "computation"
    if not _is_railcar_batch(log):
        return _skip(cid, mat, ct, "Not a railcar batch.")

    this_offload = log.get("offload")
    if not this_offload:
        return _insufficient(cid, mat, ct, "log.offload missing.")

    try:
        offload_table = log["ops_notes"]["offload_table"]
        bols = log["ops_notes"]["bols_into_railcar"]
    except (KeyError, TypeError):
        return _insufficient(cid, mat, ct,
            "Missing ops_notes.offload_table or .bols_into_railcar.")
    if not offload_table:
        return _insufficient(cid, mat, ct, "offload_table empty.")

    sorted_rows = sorted(offload_table, key=lambda r: _offload_num(r.get("id", "")))
    last_row = sorted_rows[-1]
    this_num = _offload_num(this_offload)
    last_num = _offload_num(last_row.get("id", ""))

    if this_num != last_num:
        return _skip(cid, mat, ct,
            f"This batch is offload_{this_num}, not the last offload (last = offload_{last_num}). "
            f"Derivation rule does not apply.",
            computed={"this_offload": this_offload, "last_offload": f"offload_{last_num}"})

    prior_rows = sorted_rows[:-1]
    prior_cargo = [r.get("cargo_kg") for r in prior_rows]
    if any(v is None for v in prior_cargo):
        # Cannot compute expected last-offload mass without complete prior offload data.
        # May be cross-RP (prior offloads injected in a different period) or out-of-order
        # injection — legitimate but requires LLM to confirm and document the explanation.
        missing = sum(1 for v in prior_cargo if v is None)
        return {
            "check_id": cid, "materiality": mat, "check_type": "policy", "status": "FLAG",
            "computed": {},
            "log_values": {"this_offload": this_offload,
                           "prior_offloads_missing_cargo": missing,
                           "prior_offloads_total": len(prior_cargo)},
            "note": (f"Last offload identified (offload_{this_num}) but {missing} of "
                     f"{len(prior_cargo)} prior offload row(s) lack cargo_kg — cannot compute "
                     f"expected mass. Scale ticket arithmetic confirmed separately. Route to LLM: "
                     f"are the missing prior offloads explained by cross-RP deferral or "
                     f"out-of-order injection? If so, document. Also verify: when all offloads "
                     f"are reported, sum(offloads) must not exceed sum(BOLs)."),
        }
    actual_kg = last_row.get("cargo_kg")
    if actual_kg is None:
        return _insufficient(cid, mat, ct, "Last offload cargo_kg missing.")

    bol_values = [b.get("mass_MT") for b in bols] if bols else []
    if not bol_values or any(v is None for v in bol_values):
        return _insufficient(cid, mat, ct, "BOL mass_MT values missing.")

    inbound_kg = round(sum(bol_values) * 1000, 2)
    prior_sum_kg = round(sum(prior_cargo), 2)
    # Failure Category 11: the back-calc applies only when the raw scale-ticket total
    # would exceed the BOL total. Otherwise the last offload keeps its raw ticket value.
    raw_this_kg = (log.get("scale_tickets") or {}).get("computed_net_kg")
    triggered = raw_this_kg is None or prior_sum_kg + raw_this_kg > inbound_kg
    if triggered:
        expected_kg = round(inbound_kg - prior_sum_kg, 2)
        basis = f"back-calc {inbound_kg} − {prior_sum_kg}"
    else:
        expected_kg = round(raw_this_kg, 2)
        basis = (f"raw scale ticket; back-calc not triggered because "
                 f"{prior_sum_kg} + {round(raw_this_kg, 2)} ≤ {inbound_kg}")
    delta_kg = round(actual_kg - expected_kg, 2)
    delta_pct = _pct_delta(actual_kg, expected_kg)
    status = "PASS" if delta_pct <= TOLERANCE_PCT else "FAIL"

    return {
        "check_id": cid, "materiality": mat, "check_type": ct, "status": status,
        "computed": {
            "inbound_kg": inbound_kg,
            "prior_offload_sum_kg": prior_sum_kg,
            "raw_this_offload_kg": raw_this_kg,
            "back_calc_triggered": triggered,
            "expected_last_offload_kg": expected_kg,
            "actual_last_offload_kg": actual_kg,
            "delta_kg": delta_kg,
            "delta_pct": delta_pct,
        },
        "log_values": {"this_offload": this_offload, "last_row_id": last_row.get("id")},
        "note": (f"Expected = {expected_kg} kg ({basis}); "
                 f"actual = {actual_kg} kg; delta = {delta_kg} kg ({delta_pct}%). "
                 f"Tolerance ≤{TOLERANCE_PCT}%."),
    }


def check_cobb_offload_consistency(log):
    cid, mat, ct = "cobb_offload_consistency", "hygiene", "policy"

    cobb = log.get("cobb")
    if not cobb or not isinstance(cobb, dict):
        return _insufficient(cid, mat, ct, "No 'cobb' node found in log.")

    cobb_kg = cobb.get("offloaded_quantity_kg")
    if cobb_kg is None:
        return _insufficient(cid, mat, ct, "cobb.offloaded_quantity_kg missing.")

    row_id_at_qa = cobb.get("row_id_at_qa", "unknown")
    batch_id_col_a = cobb.get("batch_id_col_a", "unknown")

    row = _find_offload_row(log)
    if row is None:
        return _insufficient(cid, mat, ct,
            f"No offload_table row matching offload={log.get('offload')!r}.")
    ops_kg = row.get("cargo_kg")
    if ops_kg is None:
        return _insufficient(cid, mat, ct,
            f"offload_table row {row.get('id')!r} has no cargo_kg.")

    delta_kg = round(cobb_kg - ops_kg, 2)
    delta_pct = _pct_delta(cobb_kg, ops_kg)
    status = "PASS" if delta_pct <= TOLERANCE_PCT else "FLAG"
    suffix = "Match." if status == "PASS" else "Discrepancy detected — route to LLM for operational context (known correction lag vs. real error)."
    return {
        "check_id": cid, "materiality": mat, "check_type": ct, "status": status,
        "computed": {"cobb_offloaded_kg": cobb_kg, "ops_notes_cargo_kg": ops_kg,
                     "delta_kg": delta_kg, "delta_pct": delta_pct},
        "log_values": {"cobb_row_id_at_qa": row_id_at_qa,
                       "cobb_batch_id_col_a": batch_id_col_a,
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
