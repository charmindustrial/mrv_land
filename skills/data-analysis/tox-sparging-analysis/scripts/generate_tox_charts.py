#!/usr/bin/env python3
"""
Basco Thermal Oxidizer (ToX) — CatOx reporting package builder.

Produces the verified reporting package for a reporting period, matching the precedent
established in the May 2026 reporting:

  - "{Month} CatOx -- Raw.xlsx"        raw readings exactly as received (one sheet)
  - "{Month} CatOx -- Processed.xlsx"  verifier-facing: EXACTLY TWO tabs, one clean chart
                                       per train (inlet + outlet lines, 600F setpoint line,
                                       grey offline shading). Nothing else.

The interpretation/controls narrative lives in the static CatOx Engineering Brief
(Google Drive), NOT in these workbooks. Do NOT add Operational Log / Transition Events /
Combustion Signal / Raw Data / Notes tabs to the Processed workbook — those are TMI for a
verifier (confirmed by Max, July 2026).

Usage:
    # combined single-file export (May/June 2026 style)
    python3 generate_tox_charts.py --input <csv> --output <dir> [--month "June 2026"]
    # per-train split export (July 2026 onward): pass both files, either order
    python3 generate_tox_charts.py --input <train1.csv> <train2.csv> --output <dir> --month "July 2026"

Dependencies: pandas, numpy, matplotlib, openpyxl
"""

import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import openpyxl
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

# Drift-prone facts are NOT hardcoded here — they live in the single-source-of-truth config.
# If the config is missing we STOP rather than fall back to a buried default (that fallback is
# exactly how a stale 650F literal survived once). The skill holds logic; the config holds facts.
_CONFIG_PATH = Path(__file__).resolve().parent.parent / 'references' / 'catox_config.json'
try:
    _CFG = json.loads(_CONFIG_PATH.read_text())
    THRESH_F = _CFG['outlet_setpoint_f']
    OFFLINE_SENTINELS = _CFG['offline_sentinels']
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    sys.exit(f"ERROR: cannot load canonical config {_CONFIG_PATH} ({e}). "
             f"Refusing to run with hardcoded defaults — fix the config first.")


# ── Data loading ────────────────────────────────────────────────────────────
def _parse_time(s):
    """
    Parse the timestamp column. Exports have arrived in two shapes:
      'M/D/YY H:MM'            (May/June 2026 combined export)
      'YYYY-MM-DD HH:MM:SS.fff' (July 2026 onward per-train export)
    Try each declared shape, then fall back to pandas' own detection. Unparseable
    values become blank so the caller can drop those rows.
    """
    for fmt in ('%m/%d/%y %H:%M', '%Y-%m-%d %H:%M:%S.%f'):
        out = pd.to_datetime(s, format=fmt, errors='coerce')
        if out.notna().mean() > 0.9:
            return out
    return pd.to_datetime(s, errors='coerce')


def _merge_per_train(paths):
    """
    Combine a per-train split export (July 2026 onward) into the same 5-column table the
    combined export produces. Each file is timestamp + that train's inlet + outlet.

    Files are assigned to trains by what their own column headers say ('Train1'/'2100' vs
    'Train2'/'2200'), NOT by the order they were passed, and the merge is an inner join on
    the timestamp so a reading is only kept when both trains report the same instant.
    Values are never altered — only placed side by side.
    """
    frames = {}
    for p in paths:
        d = pd.read_csv(p)
        if len(d.columns) != 3:
            sys.exit(f"ERROR: {Path(p).name} has {len(d.columns)} columns; a per-train export "
                     f"must be timestamp + inlet + outlet.")
        blob = ' '.join(d.columns).lower()
        t1 = ('train1' in blob.replace(' ', '') or '2100' in blob)
        t2 = ('train2' in blob.replace(' ', '') or '2200' in blob)
        if t1 == t2:
            sys.exit(f"ERROR: cannot tell which train {Path(p).name} is from its headers: "
                     f"{list(d.columns)}")
        n = 1 if t1 else 2
        if n in frames:
            sys.exit(f"ERROR: two files both look like Train {n}. Pass one file per train.")
        ic, oc = d.columns[1], d.columns[2]
        if 'inlet' not in ic.lower() or 'outlet' not in oc.lower():
            sys.exit(f"ERROR: {Path(p).name} columns are not inlet-then-outlet: {list(d.columns)}")
        frames[n] = d.rename(columns={d.columns[0]: 't_stamp'})
        print(f"  Train {n}: {Path(p).name} — {len(d)} rows")

    if set(frames) != {1, 2}:
        sys.exit(f"ERROR: need one Train 1 file and one Train 2 file; got trains {sorted(frames)}.")

    merged = frames[1].merge(frames[2], on='t_stamp', how='inner')
    dropped = max(len(frames[1]), len(frames[2])) - len(merged)
    if dropped:
        print(f"  NOTE: {dropped} reading(s) present for only one train were dropped "
              f"(timestamps must match to pair the trains).")
    return merged


def load_data(paths):
    """
    Load the temperature export(s) and return (df, raw_df, cols).

    Accepts either:
      - ONE combined file (May/June 2026 style):
        t_stamp, Train1 InletTemp, Train1 OutletTemp, Train2 InletTemp, Train2 OutletTemp
      - TWO per-train files (July 2026 onward): each timestamp + inlet + outlet, merged here
        on the timestamp into the same 5-column table. Train identity comes from the headers.

    5-minute readings, 0 marks offline/no-reading, columns correctly labeled (NO swap).

    Also tolerates the legacy combined format (7 columns with sparge binaries, -238 sentinel,
    hourly, and the April-era Train 2 header swap) as a fallback.

    Orientation is ALWAYS verified empirically after loading, and the code warns loudly if
    Train 2 looks reversed rather than blindly trusting any historical swap rule.
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    if len(paths) == 2:
        raw = _merge_per_train(paths)
    elif len(paths) == 1:
        raw = pd.read_csv(paths[0])
    else:
        sys.exit(f"ERROR: --input takes one combined file or two per-train files; got {len(paths)}.")

    cols = list(raw.columns)
    df = raw.copy()

    if len(cols) >= 5 and any('inlet' in c.lower() for c in cols) and any('outlet' in c.lower() for c in cols):
        # Current format — positional map, no swap, 0 = offline
        df = df.rename(columns={cols[0]: 'time', cols[1]: 'T1_in', cols[2]: 'T1_out',
                                cols[3]: 'T2_in', cols[4]: 'T2_out'})
    elif len(cols) == 7:
        # Legacy combined format — apply the April-era T2 header swap
        df = df.rename(columns={cols[0]: 'time', cols[1]: 'sparge1', cols[2]: 'T1_in',
                                cols[3]: 'T1_out', cols[4]: 'sparge2',
                                cols[5]: 'T2_out', cols[6]: 'T2_in'})  # note swap: idx5=out, idx6=in
    else:
        sys.exit(f"ERROR: unrecognized column layout ({len(cols)} cols): {cols}")

    df['time'] = _parse_time(df['time'])
    df = df.dropna(subset=['time']).sort_values('time').reset_index(drop=True)
    for c in ['T1_in', 'T1_out', 'T2_in', 'T2_out']:
        df[c] = pd.to_numeric(df[c], errors='coerce').replace(OFFLINE_SENTINELS, np.nan)

    # ── Orientation self-check (never trust a historical swap blindly) ──
    for n, ic, oc in [(1, 'T1_in', 'T1_out'), (2, 'T2_in', 'T2_out')]:
        m = (df[ic] > 100) & (df[oc] > 100)
        if m.sum() > 50:
            frac = (df.loc[m, oc] > df.loc[m, ic]).mean()
            if frac < 0.5:
                print(f"  *** WARNING: Train {n} outlet reads COLDER than inlet on "
                      f"{(1-frac)*100:.0f}% of operating rows — columns may be reversed. "
                      f"Verify orientation before delivering. ***")
            else:
                print(f"  Train {n} orientation OK (outlet hotter than inlet on {frac*100:.0f}% of operating rows).")

    return df, raw, cols


def report_stuck_readings(df, min_readings=12):
    """
    Flag stretches where a channel repeats one value exactly, reading after reading.

    Short repeats are normal — the historian only logs a change once it exceeds a deadband.
    What matters is a repeat spanning ALL FOUR channels on BOTH trains starting and ending at
    the same instant: two independent oxidizer trains cannot physically hold four temperatures
    constant to the degree, so that pattern is the logger holding last-good values, and those
    rows are not live readings. It matters for the numbers because a value frozen ABOVE the
    setpoint counts as at-temperature and inflates the at-temperature share.

    Printed as a diagnostic for the chat report only. Nothing here goes in the workbook.
    Returns the list of all-channel frozen blocks as (start, end, n_readings).
    """
    chans = ['T1_in', 'T1_out', 'T2_in', 'T2_out']
    print("\n── Stuck-reading check (diagnostic — not in the workbook) ──")

    for c in chans:
        s = df[c]
        run = (s != s.shift()).cumsum()
        g = df.groupby(run).agg(val=(c, 'first'), n=(c, 'size'))
        g = g[(g.n >= min_readings) & g.val.notna()]
        if len(g):
            print(f"  {c}: {len(g)} run(s) of >={min_readings*5/60:.0f}h holding one value "
                  f"({g.n.sum()} readings, {g.n.sum()/len(df)*100:.1f}% of period); "
                  f"longest {g.n.max()*5/60:.1f}h at {g.loc[g.n.idxmax(),'val']:.0f}°F")
        else:
            print(f"  {c}: no held-value run >= {min_readings*5/60:.0f}h")

    # Blocks where every channel is simultaneously repeating its previous value.
    allfrozen = pd.concat([df[c] == df[c].shift() for c in chans], axis=1).all(axis=1)
    blocks = []
    for _, d in df.groupby((allfrozen != allfrozen.shift()).cumsum()):
        if allfrozen.loc[d.index[0]] and len(d) >= min_readings:
            blocks.append((d['time'].iloc[0], d['time'].iloc[-1], len(d)))

    if not blocks:
        print("  No all-channel frozen block found. Readings track independently — good.")
        return blocks

    print(f"\n  *** {len(blocks)} ALL-CHANNEL FROZEN BLOCK(S) — treat as logger hold, not readings ***")
    for st, en, n in blocks:
        held = {c: df.loc[df['time'] == st, c].iloc[0] for c in chans}
        above = [c for c in ('T1_out', 'T2_out') if held[c] >= THRESH_F]
        print(f"    {n} readings ({n*5/60:.1f}h)  {st:%b %d %H:%M} -> {en:%b %d %H:%M}")
        print(f"      held at: " + ", ".join(f"{c} {held[c]:.0f}°F" for c in chans))
        if above:
            print(f"      NOTE: {' and '.join(above)} frozen AT/ABOVE {THRESH_F}°F — these rows "
                  f"inflate the at-temperature share. Report the stat both ways.")

    keep = ~pd.concat([(df['time'] >= s) & (df['time'] <= e) for s, e, _ in blocks],
                      axis=1).any(axis=1)
    print(f"\n  Excluding frozen block(s) — {keep.sum()} of {len(df)} readings remain:")
    for n, oc in [(1, 'T1_out'), (2, 'T2_out')]:
        s = df.loc[keep, oc]
        at = (s >= THRESH_F).sum(); bl = ((s < THRESH_F) & s.notna()).sum(); off = s.isna().sum()
        print(f"    Train {n}: at/above {THRESH_F}°F {at/keep.sum()*100:.1f}% | "
              f"below {bl/keep.sum()*100:.1f}% | offline {off/keep.sum()*100:.1f}%")
    return blocks


# ── Processed chart (matches the May precedent style) ─────────────────────────
def make_chart(df, n, inc, outc, month, path):
    fig, ax = plt.subplots(figsize=(16, 6.5))
    off = df[outc].isna(); ins = False; sx = None
    for t, v in zip(df['time'], off):
        if v and not ins:
            ins, sx = True, t
        elif not v and ins:
            ins = False
            ax.axvspan(sx, t, color='#e6e6e6', zorder=0)
    if ins and sx is not None:
        ax.axvspan(sx, df['time'].iloc[-1], color='#e6e6e6', zorder=0)

    ax.plot(df['time'], df[inc], color='#9ecae1', lw=1.1, label='Catalyst Inlet (°F)', zorder=3)
    ax.plot(df['time'], df[outc], color='#1f4e79', lw=1.3, label='Catalyst Outlet (°F)', zorder=3)
    ax.axhline(THRESH_F, color='darkorange', lw=2.0, ls='--', zorder=2,
               label=f'{THRESH_F}°F minimum setpoint')
    ax.set_title(f'Train {n} — Catalyst Temperatures — {month}', fontsize=15, fontweight='bold')
    ax.set_ylabel('Temperature (°F)', fontsize=12, fontweight='bold')
    ax.set_xlabel(f'Date ({month})', fontsize=11)
    ax.set_ylim(-50, 1250)
    ax.grid(axis='y', alpha=0.3)
    off_patch = mpatches.Patch(color='#e6e6e6', label='Offline')
    h, _ = ax.get_legend_handles_labels()
    ax.legend(handles=h + [off_patch], loc='upper right', fontsize=10, framealpha=0.95)
    span_days = (df['time'].iloc[-1] - df['time'].iloc[0]).days
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, span_days // 10)))
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved chart: {path}")
    return path


def _write_raw_sheet(ws, raw, cols):
    """Populate a worksheet with the raw readings exactly as received."""
    for j, h in enumerate(cols, 1):
        cell = ws.cell(row=1, column=j, value=str(h))
        cell.font = Font(bold=True)
        cell.fill = PatternFill('solid', fgColor='D6E4F0')
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.column_dimensions[get_column_letter(j)].width = 20 if j == 1 else 28
    for i, row in raw.iterrows():
        for j, h in enumerate(cols, 1):
            ws.cell(row=i + 2, column=j, value=row[h])
    ws.freeze_panes = 'A2'


def build_processed(df, raw, cols, month, out_dir):
    # Two chart tabs + a Raw Data tab. Tab set is declared in the config (processed_tabs);
    # we assert the built workbook matches it so code and config cannot drift.
    c1 = make_chart(df, 1, 'T1_in', 'T1_out', month, str(out_dir / 'catox_T1.png'))
    c2 = make_chart(df, 2, 'T2_in', 'T2_out', month, str(out_dir / 'catox_T2.png'))
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    for name, img in [('Train 1 — Temperature', c1), ('Train 2 — Temperature', c2)]:
        ws = wb.create_sheet(name)
        ws.sheet_view.showGridLines = False
        im = XLImage(img); im.anchor = 'A1'; ws.add_image(im)
    _write_raw_sheet(wb.create_sheet('Raw Data'), raw, cols)
    expected = _CFG['processed_tabs']
    if wb.sheetnames != expected:
        sys.exit(f"ERROR: Processed tabs {wb.sheetnames} != config processed_tabs {expected}. "
                 f"Reconcile the script and catox_config.json before delivering.")
    path = out_dir / f'{month.split()[0]} CatOx -- Processed.xlsx'
    wb.save(path)
    return path


def build_raw(raw, cols, month, out_dir):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Raw'
    _write_raw_sheet(ws, raw, cols)
    path = out_dir / f'{month.split()[0]} CatOx -- Raw.xlsx'
    wb.save(path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, nargs='+',
                    help='one combined export CSV, or two per-train export CSVs')
    ap.add_argument('--output', required=True)
    ap.add_argument('--month', help='e.g. "June 2026"; derived from data if omitted')
    a = ap.parse_args()
    out_dir = Path(a.output); out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nSetpoint {THRESH_F}°F  (source: {_CFG['setpoint_source']})")
    print(f"Loading: {', '.join(a.input)}")
    df, raw, cols = load_data(a.input)
    month = a.month or df['time'].dt.strftime('%B %Y').iloc[0]
    print(f"  {len(df)} rows, {df['time'].iloc[0]:%b %d %Y %H:%M} – {df['time'].iloc[-1]:%b %d %Y %H:%M}  ({month})")

    proc = build_processed(df, raw, cols, month, out_dir)
    rawx = build_raw(raw, cols, month, out_dir)
    print(f"\nProcessed (verifier-facing): {proc}")
    print(f"Raw:                          {rawx}")

    # Summary for the chat report to Max (NOT written into any workbook)
    total = len(df)
    print("\n── Summary (for chat report — not in the workbook) ──")
    for n, oc in [(1, 'T1_out'), (2, 'T2_out')]:
        s = df[oc]
        at = (s >= THRESH_F).sum(); below = ((s < THRESH_F) & s.notna()).sum(); off = s.isna().sum()
        peak = s.max()
        print(f"  Train {n}: at/above {THRESH_F}°F {at/total*100:.1f}% | below {below/total*100:.1f}% | "
              f"offline {off/total*100:.1f}% | peak {peak:.0f}°F")

    report_stuck_readings(df)
    print(f"\n  open \"{proc}\"")


if __name__ == '__main__':
    main()
