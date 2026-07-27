#!/usr/bin/env python3
"""
score_accuracy.py — runs deterministic checks against all normalized source-reads
files and scores accuracy against the completed QA checklists.

Usage:
    python3 score_accuracy.py <qa_dir> [--csv <output.csv>]

<qa_dir> is the outputs/qa/ folder. For each batch_*_source_reads_normalized.json
file found, runs compute_mass_chain.py and reads the matching QA checklist xlsx to
compare script findings against human QA outcomes.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

SCRIPT_DIR = Path(__file__).parent
COMPUTE_SCRIPT = SCRIPT_DIR / 'compute_mass_chain.py'

# Checklist rows that correspond to each check_id.
# Maps check_id → (section_hint, keyword_hints) for matching checklist items.
CHECK_TO_SECTION = {
    'scale_ticket_subtraction':       ('2', ['scale ticket', 'net weight', 'subtraction', 'gross weight']),
    'scale_ticket_vs_ops_notes_offload': ('2', ['ops notes', 'cargo', 'scale ticket', 'mass chain']),
    'bol_list_sum_vs_stated_total':   ('3', ['BOL', 'bill of lading', 'sum', 'total loaded']),
    'railcar_inbound_outbound_balance': ('5', ['inbound', 'outbound', 'balance', 'railcar mass', 'loss']),
    'last_offload_derivation':        ('5', ['last offload', 'back-calc', 'policy', 'derivation']),
    'cobb_offload_consistency':       ('5', ['COBB', 'offloaded quantity', 'consistency']),
}

STATUS_ISSUE = {'FAIL', 'FLAG'}
STATUS_CLEAR = {'PASS', 'SKIP', 'INSUFFICIENT_DATA'}


def run_checks(normalized_path):
    """Run compute_mass_chain.py against the normalized file. Returns findings dict or None."""
    result = subprocess.run(
        [sys.executable, str(COMPUTE_SCRIPT), str(normalized_path)],
        capture_output=True, text=True
    )
    findings_path = normalized_path.parent / 'mass_chain_findings.json'
    if findings_path.exists():
        with open(findings_path) as f:
            return json.load(f)
    return None


def read_checklist_issues(xlsx_path):
    """
    Read the QA checklist xlsx and return a set of lowercase issue descriptions
    for any FAIL or FLAG items. Returns empty set if openpyxl not available.
    """
    if not HAS_OPENPYXL or not xlsx_path.exists():
        return None
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active
    issues = []
    for row in ws.iter_rows(values_only=True):
        if not row or len(row) < 3:
            continue
        status = str(row[2]).strip().upper() if row[2] else ''
        if status in ('FAIL', 'FLAG'):
            desc = ' '.join(str(c) for c in row[:4] if c).lower()
            issues.append(desc)
    return issues


def match_check_to_checklist(check_id, checklist_issues):
    """
    Heuristically determine if the checklist has an issue that corresponds to check_id.
    Returns True if a matching issue exists, False if none, None if can't determine.
    """
    if checklist_issues is None:
        return None
    _, keywords = CHECK_TO_SECTION.get(check_id, (None, []))
    for issue_text in checklist_issues:
        if any(kw.lower() in issue_text for kw in keywords):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument('qa_dir', type=Path)
    parser.add_argument('--csv', type=Path, help='Write results to CSV')
    args = parser.parse_args()

    normalized_files = sorted(args.qa_dir.rglob('batch_*_source_reads_normalized.json'))
    if not normalized_files:
        print('No normalized files found. Run normalize_source_reads.py --all-batches first.')
        sys.exit(1)

    rows = []
    for norm_path in normalized_files:
        batch_folder = norm_path.parent
        # Derive batch_id from folder name (batch-2-184 → 2-184, batch-K-002 → K-002)
        folder_name = batch_folder.name
        batch_id = folder_name.replace('batch-', '') if folder_name.startswith('batch-') else folder_name

        # Skip Kerry and 2-182 (no useful data)
        if batch_id in ('K-002',) or '2-182' in str(norm_path):
            continue

        # Find matching checklist
        checklist_files = list(batch_folder.glob('*QA_Checklist*.xlsx'))
        checklist_path = checklist_files[0] if checklist_files else None
        checklist_issues = read_checklist_issues(checklist_path) if checklist_path else None

        findings = run_checks(norm_path)
        if findings is None:
            print(f'{batch_id}: script failed or produced no output')
            continue

        for check in findings.get('checks', []):
            cid = check['check_id']
            script_status = check['status']
            mat = check['materiality']

            script_issue = script_status in STATUS_ISSUE
            checklist_has_issue = match_check_to_checklist(cid, checklist_issues)

            # Accuracy classification (only for runnable checks)
            if script_status in ('SKIP', 'INSUFFICIENT_DATA'):
                accuracy = 'SKIP/INSUF'
            elif checklist_has_issue is None:
                accuracy = 'NO_CHECKLIST'
            elif script_issue and checklist_has_issue:
                accuracy = 'TRUE_POS'
            elif not script_issue and not checklist_has_issue:
                accuracy = 'TRUE_NEG'
            elif script_issue and not checklist_has_issue:
                accuracy = 'FALSE_POS'
            else:
                accuracy = 'FALSE_NEG'

            rows.append({
                'batch_id': batch_id,
                'check_id': cid,
                'check_type': check.get('check_type', 'unknown'),
                'materiality': mat,
                'script_status': script_status,
                'checklist_has_issue': checklist_has_issue,
                'accuracy': accuracy,
                'note': check.get('note', '')[:120],
            })

    # Summary
    from collections import Counter

    def _print_stats(label, subset):
        counts = Counter(r['accuracy'] for r in subset)
        runnable = [r for r in subset if r['accuracy'] not in ('SKIP/INSUF', 'NO_CHECKLIST')]
        tp = counts['TRUE_POS']
        tn = counts['TRUE_NEG']
        fp = counts['FALSE_POS']
        fn = counts['FALSE_NEG']
        print(f'\n=== {label} ===')
        print(f'Total check runs:    {len(subset)}')
        print(f'Skipped/insuf data:  {counts["SKIP/INSUF"]}')
        print(f'Scoreable runs:      {len(runnable)}')
        print(f'  True positives:    {tp}  (script found real issue)')
        print(f'  True negatives:    {tn}  (script correctly cleared)')
        print(f'  False positives:   {fp}  (script flagged, checklist clean)')
        print(f'  False negatives:   {fn}  (script missed real issue)')
        if tp + fp > 0:
            print(f'Precision:           {tp/(tp+fp):.0%}  (of script flags, % were real)')
        if tp + fn > 0:
            print(f'Recall:              {tp/(tp+fn):.0%}  (of real issues, % script caught)')

    _print_stats('ACCURACY SUMMARY — ALL CHECKS', rows)
    _print_stats('COMPUTATION CHECKS (arithmetic — direct findings)',
                 [r for r in rows if r['check_type'] == 'computation'])
    _print_stats('POLICY CHECKS (discrepancy detection — routed to LLM)',
                 [r for r in rows if r['check_type'] == 'policy'])

    counts = Counter(r['accuracy'] for r in rows)
    runnable = [r for r in rows if r['accuracy'] not in ('SKIP/INSUF', 'NO_CHECKLIST')]

    print('\n=== PER-BATCH DETAIL ===')
    current_batch = None
    for r in rows:
        if r['batch_id'] != current_batch:
            current_batch = r['batch_id']
            print(f"\n{current_batch}:")
        flag = '✓' if r['accuracy'] in ('TRUE_POS', 'TRUE_NEG') else ('?' if 'NO_CHECKLIST' in r['accuracy'] or 'SKIP' in r['accuracy'] else '✗')
        print(f"  {flag} {r['check_id']:40s} {r['script_status']:20s} [{r['accuracy']}]")

    if args.csv:
        import csv
        with open(args.csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f'\nWrote {args.csv}')


if __name__ == '__main__':
    main()
