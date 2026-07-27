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
    python3 generate_tox_charts.py --input <csv> --output <dir> [--month "June 2026"]

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
def load_data(path):
    """
    Load the temperature export and return (df, raw_df, cols).

    Handles the current export format (May 2026 onward):
      t_stamp, Train1 InletTemp, Train1 OutletTemp, Train2 InletTemp, Train2 OutletTemp
      - 5-minute readings, 0 marks offline/no-reading, columns correctly labeled (NO swap).

    Also tolerates the legacy combined format (7 columns with sparge binaries, -238 sentinel,
    hourly, and the April-era Train 2 header swap) as a fallback.

    Orientation is ALWAYS verified empirically after loading, and the code warns loudly if
    Train 2 looks reversed rather than blindly trusting any historical swap rule.
    """
    raw = pd.read_csv(path)
    cols = list(raw.columns)
    df = raw.copy()

    if len(cols) >= 5 and any('inlet' in c.lower() for c in cols) and any('outlet' in c.lower() for c in cols):
        # Current format — positional map, no swap, 0 = offline
        df = df.rename(columns={cols[0]: 'time', cols[1]: 'T1_in', cols[2]: 'T1_out',
                                cols[3]: 'T2_in', cols[4]: 'T2_out'})
        fmt = '%m/%d/%y %H:%M'
    elif len(cols) == 7:
        # Legacy combined format — apply the April-era T2 header swap
        df = df.rename(columns={cols[0]: 'time', cols[1]: 'sparge1', cols[2]: 'T1_in',
                                cols[3]: 'T1_out', cols[4]: 'sparge2',
                                cols[5]: 'T2_out', cols[6]: 'T2_in'})  # note swap: idx5=out, idx6=in
        fmt = None
    else:
        sys.exit(f"ERROR: unrecognized column layout ({len(cols)} cols): {cols}")

    df['time'] = pd.to_datetime(df['time'], format=fmt, errors='coerce')
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
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--month', help='e.g. "June 2026"; derived from data if omitted')
    a = ap.parse_args()
    out_dir = Path(a.output); out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nSetpoint {THRESH_F}°F  (source: {_CFG['setpoint_source']})")
    print(f"Loading: {a.input}")
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
    print(f"\n  open \"{proc}\"")


if __name__ == '__main__':
    main()
