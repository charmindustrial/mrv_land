#!/usr/bin/env python3
"""
normalize_source_reads.py — maps legacy source-reads.json files to the
canonical format required by compute_mass_chain.py.

Each batch was written in a different ad-hoc format. This script extracts
the values needed for the 6 deterministic checks using known fallback paths
for each field variation observed across the batch corpus.

Usage:
    python3 normalize_source_reads.py <source_reads.json>
    python3 normalize_source_reads.py --all-batches <outputs/qa/> [--report]
"""
import argparse
import json
import re
import sys
from pathlib import Path

LB_TO_KG = 0.453592


def _dig(d, *paths):
    """Try multiple dot-notation paths, return first non-None value found."""
    for path in paths:
        cur = d
        ok = True
        for key in path.split('.'):
            if isinstance(cur, dict) and key in cur and cur[key] is not None:
                cur = cur[key]
            else:
                ok = False
                break
        if ok:
            return cur
    return None


def _offload_num_from_str(s):
    """Extract trailing offload number from strings like 'offload_3' or '...offload_3'."""
    if not isinstance(s, str):
        return None
    m = re.search(r'offload_(\d+)', s)
    return int(m.group(1)) if m else None


def _extract_full_gross(st):
    full = st.get('full_ticket') or st.get('full') or {}
    if not isinstance(full, dict):
        return None
    return (full.get('gross_weight_lb') or
            full.get('certified_gross_weight_lb') or
            full.get('gross_weight_lb_per_image'))


def _extract_empty_gross(st):
    empty = st.get('empty_ticket') or st.get('empty') or {}
    if not isinstance(empty, dict):
        return None
    return (empty.get('gross_weight_lb') or
            empty.get('certified_gross_weight_lb') or
            empty.get('gross_weight_lb_per_image'))


def _extract_net_lb(st, full_lb, empty_lb):
    """Try stored net, then compute from full - empty."""
    net = (st.get('computed_net_lb') or
           st.get('net_lb') or
           st.get('net_load_lb') or
           st.get('net_calc_lb'))
    if net is None:
        nc = st.get('net_calc')
        if isinstance(nc, dict):
            net = nc.get('net_lb') or nc.get('net_weight_lb')
    if net is None and full_lb is not None and empty_lb is not None:
        net = full_lb - empty_lb
    return net


def _extract_net_kg(st, net_lb):
    """Try stored net kg, then compute from net_lb."""
    net = (st.get('computed_net_kg') or
           st.get('net_kg') or
           st.get('net_load_kg') or
           st.get('net_calc_kg') or
           st.get('net_kg_at_0_453592'))
    if net is None:
        nc = st.get('net_calc')
        if isinstance(nc, dict):
            net = nc.get('net_kg') or nc.get('net_weight_kg')
    if net is None and net_lb is not None:
        net = round(net_lb * LB_TO_KG, 2)
    return net


def _extract_offload(raw):
    """Determine which offload this batch represents."""
    offload = raw.get('offload')
    if offload:
        return offload
    n = raw.get('offload_number')
    if n is not None:
        return f'offload_{n}'
    n = raw.get('consumed_lot_offload_number')
    if n is not None:
        return f'offload_{n}'
    for cl_key in ('consumed_lot', 'consumed_lot_per_cobb', 'consumed_lot_suffix_per_cobb'):
        cl = raw.get(cl_key)
        if cl:
            n = _offload_num_from_str(cl)
            if n:
                return f'offload_{n}'
    # _meta: is_last_batch_on_railcar + n_offloads_on_railcar
    meta = raw.get('_meta', {})
    if isinstance(meta, dict):
        n = meta.get('offload_number')
        if n is not None:
            return f'offload_{n}'
        if meta.get('is_last_batch_on_railcar') and meta.get('n_offloads_on_railcar'):
            return f'offload_{meta["n_offloads_on_railcar"]}'
    return None


def _extract_bols(raw, on):
    """Extract BOLs-into-railcar list with mass_MT per BOL."""
    bols_raw = (on.get('bols_into_railcar') or
                on.get('bols_loaded') or
                on.get('BOLs_loaded') or
                on.get('bols_loaded_section') or
                on.get('bols_loaded_listed') or
                raw.get('bols_loaded_into_railcar') or
                raw.get('bols_into_railcar'))

    _MASS_KEYS = ('mass_MT', 'mass_mt', 'bol_mass_mt', 'BOL_mass_MT', 'BOL_mass_mt',
                  'loaded_mass_MT', 'loaded_mass_mt', 'masse_nette_mt', 'masse_nette_MT',
                  'masse_nette_kg')

    def _get_mass(b):
        for k in _MASS_KEYS:
            v = b.get(k)
            if v is not None:
                return v / 1000 if 'kg' in k.lower() else v
        if b.get('mass_kg'):
            return round(b['mass_kg'] / 1000, 5)
        return None

    if not bols_raw:
        # Last resort: bol_billing_documents top-level dict
        bbd = raw.get('bol_billing_documents')
        if isinstance(bbd, dict):
            result = []
            for k, v in bbd.items():
                if isinstance(v, dict) and k.startswith('bol_'):
                    mass = _get_mass(v)
                    if mass is not None:
                        result.append({'mass_MT': mass})
            if result:
                return result
        return []

    if isinstance(bols_raw, list):
        result = []
        for b in bols_raw:
            if not isinstance(b, dict):
                continue
            mass = _get_mass(b)
            if mass is not None:
                result.append({'mass_MT': mass})
        return result

    if isinstance(bols_raw, dict):
        result = []
        for k, v in bols_raw.items():
            if isinstance(v, dict) and (k.startswith('BOL') or k.startswith('bol')):
                mass = _get_mass(v)
                if mass is not None:
                    result.append({'mass_MT': mass})
        return result
    return []


def _extract_total_mt(on, bols=None):
    v = (on.get('total_railcar_loaded_MT') or
         on.get('total_loaded_mass_MT') or
         on.get('total_loaded_mass_mt') or
         on.get('bol_aggregate_mt'))
    if v is None and bols:
        masses = [b.get('mass_MT') for b in bols if b.get('mass_MT') is not None]
        if len(masses) == len(bols) and masses:
            v = round(sum(masses), 5)
    return v


def _normalize_offload_table(on):
    """Normalize offload table rows to canonical field names."""
    raw_ot = (on.get('offload_table') or
              on.get('offload_table_populated_rows') or
              on.get('trucks_unloaded') or [])

    # Handle single-dict cases (one offload stored as a dict, not a list)
    for single_key in ('trucks_unloaded_offload_1',
                       'trucks_unloaded_offload_1_for_this_batch'):
        single = on.get(single_key)
        if isinstance(single, dict):
            raw_ot = [single]
            break

    if isinstance(raw_ot, dict):
        raw_ot = [raw_ot]

    result = []
    for row in raw_ot:
        if not isinstance(row, dict):
            continue
        row_id = (row.get('id') or
                  row.get('so_number') or
                  row.get('SO_number') or
                  row.get('consumed_lot'))
        cargo = (row.get('cargo_kg') or row.get('cargo_mass_kg'))
        result.append({'id': row_id, 'cargo_kg': cargo})
    return result


def _extract_cobb(raw):
    """Extract COBB offloaded quantity, row ID, and batch ID from any format."""
    cobb_kg = None
    row_id = None
    batch_id = None

    # New canonical: cobb.offloaded_quantity_kg
    cobb_node = raw.get('cobb')
    if isinstance(cobb_node, dict):
        cobb_kg = cobb_node.get('offloaded_quantity_kg')
        row_id = cobb_node.get('row_id_at_qa') or cobb_node.get('cobb_row_number') or cobb_node.get('row_number')
        batch_id = (cobb_node.get('batch_id_col_a') or
                    cobb_node.get('cobb_cell_A_value') or
                    cobb_node.get('A_injection_batch'))
        # 2-185 style: cobb.row_62_data.F_quantity_consumed_in_injection_kg
        if cobb_kg is None:
            for key in ['row_62_data', 'row_data', 'row_values']:
                rd = cobb_node.get(key)
                if isinstance(rd, dict):
                    cobb_kg = (rd.get('F_quantity_consumed_in_injection_kg') or
                               rd.get('offloaded_quantity_kg') or
                               rd.get('F_offloaded_quantity_kg'))
                    if cobb_kg is not None:
                        break
        # 2-192 style: direct field on cobb node
        if cobb_kg is None:
            cobb_kg = cobb_node.get('F_quantity_consumed_in_injection_kg')

    # cobb_tracker format (2-191)
    if cobb_kg is None:
        ct = raw.get('cobb_tracker')
        if isinstance(ct, dict):
            vals = ct.get('values', {})
            if isinstance(vals, dict):
                cobb_kg = (vals.get('F_offloaded_quantity_kg') or
                           vals.get('offloaded_quantity_kg') or
                           vals.get('F_quantity_consumed_in_injection_kg'))
            row_id = ct.get('row_index') or row_id
            batch_id = ct.get('cobb_cell_A_value') or batch_id

    # cobb_row top-level dict (without numeric suffix — 2-186, 2-204 style)
    if cobb_kg is None:
        cr = raw.get('cobb_row')
        if isinstance(cr, dict):
            cobb_kg = (cr.get('offloaded_quantity_kg') or
                       cr.get('quantity_consumed_in_injection_kg') or
                       cr.get('F_quantity_consumed_in_injection_kg'))
            row_id = row_id or cr.get('row_number')
            batch_id = batch_id or cr.get('injection_batch') or cr.get('cobb_cell_A_value')

    # Old cobb_row_* format (2-184, 2-180 style)
    if cobb_kg is None:
        for k, v in raw.items():
            if k.startswith('cobb_row_') and isinstance(v, dict):
                for fk, fv in v.items():
                    if 'offloaded_quantity_kg' in fk or 'F_quantity_consumed' in fk:
                        cobb_kg = fv
                        row_id = row_id or k
                        break
                if cobb_kg is not None:
                    break

    # cobb_row_88 / cobb_row_NN top-level dict
    if cobb_kg is None:
        for k in raw:
            if re.match(r'cobb_row_\d+', k) and isinstance(raw[k], dict):
                v = raw[k]
                cobb_kg = (v.get('F_quantity_consumed_in_injection_kg') or
                           v.get('offloaded_quantity_kg'))
                row_id = row_id or v.get('row_number') or k
                batch_id = batch_id or v.get('cobb_cell_A_value') or v.get('injection_batch')
                if cobb_kg is not None:
                    break

    # cobb_data format (2-182 style)
    if cobb_kg is None:
        cd = raw.get('cobb_data')
        if isinstance(cd, dict):
            cobb_kg = (cd.get('offloaded_quantity_kg') or
                       cd.get('F_quantity_consumed_in_injection_kg'))

    batch_id = batch_id or raw.get('cobb_cell_A_value')

    return cobb_kg, row_id, batch_id


def normalize(raw):
    """Convert any source-reads dict to canonical format."""
    out = {}

    # Batch metadata
    out['_schema_version'] = '1.0-normalized'
    out['batch_id'] = _dig(raw, 'batch_id', '_meta.batch_id') or 'UNKNOWN'
    out['oil_type'] = _dig(raw, 'oil_type', '_meta.oil_type') or 'AECN'
    out['delivery_mode'] = (_dig(raw, 'delivery_mode', '_meta.delivery_mode') or '').lower()
    out['railcar'] = (_dig(raw, 'railcar', '_meta.railcar',
                           'ops_notes.railcar_number', 'ops_notes.railcar') or '')
    out['injection_site'] = _dig(raw, 'injection_site', '_meta.injection_site') or ''

    out['offload'] = _extract_offload(raw)

    # Scale tickets
    st = raw.get('scale_tickets') or {}
    full_lb = _extract_full_gross(st)
    empty_lb = _extract_empty_gross(st)
    net_lb = _extract_net_lb(st, full_lb, empty_lb)
    net_kg = _extract_net_kg(st, net_lb)

    out['scale_tickets'] = {
        'full_ticket': {'gross_weight_lb': full_lb},
        'empty_ticket': {'gross_weight_lb': empty_lb},
        'computed_net_lb': net_lb,
        'computed_net_kg': net_kg,
    }

    # Ops Notes
    on = raw.get('ops_notes') if isinstance(raw.get('ops_notes'), dict) else {}
    bols = _extract_bols(raw, on)
    total_mt = _extract_total_mt(on, bols)
    offload_table = _normalize_offload_table(on)

    out['ops_notes'] = {
        'bols_into_railcar': bols,
        'total_railcar_loaded_MT': total_mt,
        'offload_table': offload_table,
    }

    # COBB
    cobb_kg, cobb_row_id, cobb_batch_id = _extract_cobb(raw)
    out['cobb'] = {
        'row_id_at_qa': str(cobb_row_id) if cobb_row_id is not None else None,
        'batch_id_col_a': cobb_batch_id,
        'offloaded_quantity_kg': cobb_kg,
    }

    return out


def coverage_report(normalized, batch_id):
    """Report which fields were found vs. missing."""
    checks = {
        'full_lb': normalized['scale_tickets']['full_ticket']['gross_weight_lb'],
        'empty_lb': normalized['scale_tickets']['empty_ticket']['gross_weight_lb'],
        'net_lb': normalized['scale_tickets']['computed_net_lb'],
        'net_kg': normalized['scale_tickets']['computed_net_kg'],
        'offload': normalized['offload'],
        'railcar': normalized['railcar'],
        'bols': len(normalized['ops_notes']['bols_into_railcar']),
        'total_mt': normalized['ops_notes']['total_railcar_loaded_MT'],
        'offload_table_rows': len(normalized['ops_notes']['offload_table']),
        'cobb_kg': normalized['cobb']['offloaded_quantity_kg'],
    }
    missing = [k for k, v in checks.items() if v is None or v == '' or v == 0]
    found = {k: v for k, v in checks.items() if k not in missing}
    return found, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument('source_reads_path', nargs='?', type=Path)
    parser.add_argument('--all-batches', type=Path, metavar='QA_DIR',
                        help='Normalize all batch_*_source_reads.json files under QA_DIR')
    parser.add_argument('--report', action='store_true',
                        help='Print coverage report for each batch')
    parser.add_argument('--output', type=Path,
                        help='Output path for normalized JSON (single-file mode)')
    args = parser.parse_args()

    if args.all_batches:
        files = sorted(args.all_batches.rglob('batch_*_source_reads.json'))
        results = []
        for f in files:
            with open(f) as fh:
                raw = json.load(fh)
            norm = normalize(raw)
            out_path = f.parent / f.name.replace('_source_reads.json', '_source_reads_normalized.json')
            with open(out_path, 'w') as fh:
                json.dump(norm, fh, indent=2)
                fh.write('\n')
            found, missing = coverage_report(norm, norm['batch_id'])
            result = {'batch_id': norm['batch_id'], 'file': str(f),
                      'normalized_path': str(out_path),
                      'found': found, 'missing': missing}
            results.append(result)
            if args.report:
                miss_str = ', '.join(missing) if missing else 'none'
                print(f"{norm['batch_id']:8s}  missing: {miss_str}")
        print(f'\nNormalized {len(files)} files.')
        return

    if not args.source_reads_path:
        parser.print_help()
        sys.exit(1)

    with open(args.source_reads_path) as f:
        raw = json.load(f)
    norm = normalize(raw)

    out_path = args.output or args.source_reads_path.parent / \
        args.source_reads_path.name.replace('_source_reads.json', '_source_reads_normalized.json')
    with open(out_path, 'w') as f:
        json.dump(norm, f, indent=2)
        f.write('\n')

    found, missing = coverage_report(norm, norm['batch_id'])
    print(f'Wrote {out_path}')
    print(f"Found:   {', '.join(f'{k}={v}' for k,v in found.items())}")
    if missing:
        print(f"Missing: {', '.join(missing)}")


if __name__ == '__main__':
    main()
