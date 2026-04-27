"""
Generate compliance charts for wellhead injection data.

Usage:
    python generate_compliance_charts.py <input_xlsx> <output_dir> [--max-surface 455] [--min-annular 200] [--min-diff 50]

Produces three PNG charts:
    1. surface_pressure.png  — Surface injection pressure with max compliance line
    2. annular_pressure.png  — Annular pressure with min compliance line
    3. pressure_differential.png — Annular-surface differential during injection with min compliance line

Also prints a JSON summary of compliance results to stdout.
"""

import argparse
import json
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os


def parse_timestamps(df):
    ts = df['local_time'].astype(str)
    ts_clean = ts.str.replace(r'[-+]\d{2}:\d{2}$', '', regex=True)
    df['local_time'] = pd.to_datetime(ts_clean, format='mixed')
    return df


def chart_surface_pressure(df, output_path, max_psi, erroneous_mask=None):
    fig, ax = plt.subplots(figsize=(16, 7))

    if erroneous_mask is not None and erroneous_mask.any():
        normal = ~erroneous_mask
        ax.plot(df.loc[normal, 'local_time'], df.loc[normal, 'surface_pressure_psi'],
                color='#2563EB', linewidth=0.5, alpha=0.8, label='Surface Pressure (PSI)')
        ax.scatter(df.loc[erroneous_mask, 'local_time'], df.loc[erroneous_mask, 'surface_pressure_psi'],
                   color='#F59E0B', s=30, zorder=5, marker='x', linewidths=2,
                   label='Sensor Error (flagged)')
    else:
        ax.plot(df['local_time'], df['surface_pressure_psi'],
                color='#2563EB', linewidth=0.5, alpha=0.8, label='Surface Pressure (PSI)')

    ax.axhline(y=max_psi, color='#DC2626', linewidth=2, linestyle='--',
               label=f'Compliance Limit ({max_psi} PSI)')

    date_range = f"{df['local_time'].min().strftime('%B %-d')}–{df['local_time'].max().strftime('%-d, %Y')}"
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Injection Pressure (PSI)', fontsize=12, fontweight='bold')
    ax.set_title(f'Injection Pressure Over Time — {date_range}', fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.xticks(rotation=45)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(df['surface_pressure_psi'].max() * 1.1, max_psi * 1.15))
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def chart_annular_pressure(df, output_path, min_psi, erroneous_mask=None):
    fig, ax = plt.subplots(figsize=(16, 7))

    if erroneous_mask is not None and erroneous_mask.any():
        normal = ~erroneous_mask
        ax.plot(df.loc[normal, 'local_time'], df.loc[normal, 'annular_pressure_psi'],
                color='#7C3AED', linewidth=0.5, alpha=0.8, label='Annular Pressure (PSI)')
        ax.scatter(df.loc[erroneous_mask, 'local_time'], df.loc[erroneous_mask, 'annular_pressure_psi'],
                   color='#F59E0B', s=30, zorder=5, marker='x', linewidths=2,
                   label='Sensor Error Window')
    else:
        ax.plot(df['local_time'], df['annular_pressure_psi'],
                color='#7C3AED', linewidth=0.5, alpha=0.8, label='Annular Pressure (PSI)')

    ax.axhline(y=min_psi, color='#DC2626', linewidth=2, linestyle='--',
               label=f'Minimum Compliance ({min_psi} PSI)')

    date_range = f"{df['local_time'].min().strftime('%B %-d')}–{df['local_time'].max().strftime('%-d, %Y')}"
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Annular Pressure (PSI)', fontsize=12, fontweight='bold')
    ax.set_title(f'Tubing-Casing Annular Pressure — {date_range}', fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.xticks(rotation=45)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, df['annular_pressure_psi'].max() * 1.1)
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def chart_pressure_differential(df, output_path, min_diff):
    inj = df[df['injecting'] == 'YES'].copy()
    if inj.empty:
        print("WARNING: No injection data points found (injecting=YES). Skipping differential chart.", file=sys.stderr)
        return {'total_injection_points': 0, 'violations': 0, 'min_differential': None}

    inj['pressure_diff'] = inj['annular_pressure_psi'] - inj['surface_pressure_psi']
    compliant = inj['pressure_diff'] >= min_diff
    non_compliant = ~compliant

    fig, ax = plt.subplots(figsize=(16, 7))
    ax.scatter(inj.loc[compliant, 'local_time'], inj.loc[compliant, 'pressure_diff'],
               color='#2563EB', s=3, alpha=0.6, label=f'Compliant (≥{min_diff} PSI gap)')
    if non_compliant.any():
        ax.scatter(inj.loc[non_compliant, 'local_time'], inj.loc[non_compliant, 'pressure_diff'],
                   color='#DC2626', s=12, alpha=0.8, zorder=5,
                   label=f'Below Threshold ({non_compliant.sum()} pts)')

    ax.axhline(y=min_diff, color='#DC2626', linewidth=2, linestyle='--',
               label=f'Minimum Differential ({min_diff} PSI)')

    date_range = f"{df['local_time'].min().strftime('%B %-d')}–{df['local_time'].max().strftime('%-d, %Y')}"
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Annular − Surface Pressure (PSI)', fontsize=12, fontweight='bold')
    ax.set_title(f'Annular-to-Surface Pressure Differential During Injection — {date_range}', fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.xticks(rotation=45)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return {
        'total_injection_points': len(inj),
        'violations': int(non_compliant.sum()),
        'min_differential': round(float(inj['pressure_diff'].min()), 1),
        'max_differential': round(float(inj['pressure_diff'].max()), 1),
    }


def analyze_time_series(df):
    df = df.sort_values('local_time').reset_index(drop=True)
    df['time_diff'] = df['local_time'].diff()
    median_interval = df['time_diff'].median()
    gaps = df[df['time_diff'] > pd.Timedelta(minutes=30)].copy()
    gap_list = []
    for _, row in gaps.iterrows():
        prev_time = row['local_time'] - row['time_diff']
        gap_list.append({
            'from': str(prev_time),
            'to': str(row['local_time']),
            'gap_hours': round(row['time_diff'].total_seconds() / 3600, 1),
            'injecting_after': str(row['injecting']) if pd.notna(row['injecting']) else 'NaN'
        })
    return {
        'median_interval_seconds': round(median_interval.total_seconds(), 1),
        'total_points': len(df),
        'gaps_over_30min': gap_list
    }


def main():
    parser = argparse.ArgumentParser(description='Generate compliance charts for wellhead data')
    parser.add_argument('input_xlsx', help='Input Excel file path')
    parser.add_argument('output_dir', help='Directory to save chart PNGs')
    parser.add_argument('--max-surface', type=float, default=455, help='Max surface pressure (psig)')
    parser.add_argument('--min-annular', type=float, default=200, help='Min annular pressure (psig)')
    parser.add_argument('--min-diff', type=float, default=50, help='Min annular-surface differential (psig)')
    parser.add_argument('--sheet', default='Raw Data', help='Sheet name to read')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_excel(args.input_xlsx, sheet_name=args.sheet)
    df = parse_timestamps(df)
    df = df.sort_values('local_time').reset_index(drop=True)

    # Surface pressure analysis
    above_limit = df['surface_pressure_psi'] > args.max_surface
    surface_result = {
        'max_recorded': round(float(df['surface_pressure_psi'].max()), 1),
        'points_above_limit': int(above_limit.sum()),
        'limit': args.max_surface
    }

    # Annular pressure analysis
    below_min = (df['annular_pressure_psi'] < args.min_annular) & (df['annular_pressure_psi'] > 0)
    annular_result = {
        'min_recorded': round(float(df['annular_pressure_psi'].min()), 1),
        'points_below_min': int(below_min.sum()),
        'limit': args.min_annular
    }

    # Generate charts (no erroneous mask by default — caller should handle annotation)
    chart_surface_pressure(df, os.path.join(args.output_dir, 'surface_pressure.png'), args.max_surface)
    chart_annular_pressure(df, os.path.join(args.output_dir, 'annular_pressure.png'), args.min_annular)
    diff_result = chart_pressure_differential(df, os.path.join(args.output_dir, 'pressure_differential.png'), args.min_diff)

    # Time series analysis
    ts_result = analyze_time_series(df)

    summary = {
        'surface_pressure': surface_result,
        'annular_pressure': annular_result,
        'pressure_differential': diff_result,
        'time_series': ts_result,
    }

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
