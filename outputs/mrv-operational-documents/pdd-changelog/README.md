# PDD change-log workflow

On-demand tool that detects what changed in the PDD between edits and appends
**Draft** rows to a standalone tracker spreadsheet. You supply the rationale and
the temporary/permanent call; the tool supplies the date, the section, and the
old→new text.

## Files

- `pdd_changelog.py` — the tool (this folder, version-controlled).
- Baseline snapshot + tracker live next to the PDD on the Drive mount:
  `My Drive/MRV/PDDs+Supplemental Docs/PDD Change Log/`
  - `baseline/PDD_baseline.docx` + `baseline_meta.json` — the last-logged version.
  - `PDD_Change_Log.xlsx` — the running log (Date · PDD Version · Section · Change ·
    Old→New · Rationale · Temporary/Permanent · Status).

The 2 MB baseline is kept on Drive, not in the git workspace, so the repo stays light.

## How it works

The PDD is mostly tables, so the tool linearizes **paragraphs and table cells**
in document order, tracks the section/appendix heading in force at each point
(by text pattern — "Section X" / "Appendix N" are top level; Table-of-Contents
lines are ignored), and diffs the current file against the baseline. Genuine
edits show as `Modified` (with just the changed sentences surfaced); unrelated
lines show as clean `Added` / `Removed`.

## Commands

Run from this folder:

```
python3 pdd_changelog.py init      # snapshot current PDD as baseline + create tracker (run once)
python3 pdd_changelog.py log       # diff vs baseline → report + append Draft rows to the tracker
python3 pdd_changelog.py accept    # re-baseline to the current PDD once the rows are logged
```

- `log` is read-only on the baseline — run it as often as you like.
- Only `accept` advances the baseline, so the same edits don't reappear next time.
- Close the tracker in Excel/Sheets before running `log` (an open handle blocks the write).
- Override the PDD path with `--pdd "<path>"` if it moves.

## Typical loop

1. Edit the PDD.
2. `log` → review the report, then open the tracker and fill **Rationale** +
   **Temporary/Permanent** on the new Draft rows; set **Status** to `Logged`.
3. Use the logged rows to write the Section F.1 narrative entry and bump the
   appendix Document Revision table.
4. `accept` to set the new baseline.

The tracker feeds the PDD's own change records — it does not replace them:
**Section F.1** (date-stamped narrative, temporary vs permanent) and the
per-appendix **Document Revision** tables remain the verifier-facing log.
