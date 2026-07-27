# ToX Data Column Mapping

## Current export format (May 2026 onward)

A plain CSV, temperature-only, 5-minute readings:

| Index | Header (as exported) | Name in code | Notes |
|---|---|---|---|
| 0 | t_stamp | `time` | Format: `M/D/YY H:MM` (24-hour) |
| 1 | ...Train1...Catalyst-InletTemp | `T1_in` | Inlet, °F |
| 2 | ...Train1...Catalyst-OutletTemp | `T1_out` | Outlet, °F |
| 3 | ...Train2...CatalystInletTemp | `T2_in` | Inlet, °F — **correctly labeled, no swap** |
| 4 | ...Train2...CatalystOutletTemp | `T2_out` | Outlet, °F — **correctly labeled, no swap** |

- **Offline sentinel: `0`** → replace with NaN (blank) before analysis.
- **No sparging binary columns** in this export (temperature only).
- **No Train 2 swap.** See below.

---

## Train 2 column swap — history, NOT a standing rule

In the **April 2026** legacy export, Train 2's columns were reversed from their header labels:
the column labeled "Catalyst Inlet" (TIT-2251) actually carried the outlet signal, and vice
versa. That was a real property of that export.

**It was fixed at the equipment when Train 2 came back from fan service ~May 5–6, 2026.**
Confirmed in the May CatOx Raw data: after service, labeled-inlet TIT-2251 reads ≈600°F and
labeled-outlet TIT-2252 reads ≈850–900°F — i.e. correctly labeled, outlet hotter than inlet.
June 2026 shows the same. **Current and future exports need no swap.**

**Never apply the old swap blindly.** The processing script verifies orientation empirically
every run: on operating rows (both sensors > 100°F), the outlet should read hotter than the
inlet for a working catalytic oxidizer. If a train fails that check, the script warns loudly —
stop and verify before delivering rather than assuming either state.

---

## Legacy combined format (pre-May, fallback only)

Older exports were a single Google Sheet combining temperature + sparging binaries, hourly, with
a `-238` offline sentinel and the April-era Train 2 header swap (index 5 = outlet, index 6 =
inlet). The script still loads this 7-column layout as a fallback and applies the swap for those
files only. New work uses the current format above.

---

## Timestamp Parsing

Current: `pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')`. Legacy: auto-detect. Coerce
errors to NaT and drop resulting rows.
