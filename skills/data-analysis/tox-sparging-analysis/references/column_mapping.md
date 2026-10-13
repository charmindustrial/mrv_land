# ToX Data Column Mapping

## Current export format (September 2026 onward) — ONE COMBINED FILE, pulled by Garrett

For the September 2026 period Garrett pulled the data himself (from Google BigQuery, per his
reply in the #mrv-ops-la Oct 1 ask thread: *"I now have the schema for this where its stored in
Google Big Query, so we can automate this on our end"*) instead of Evan exporting from Ignition.
It arrived as one file, `Oxidizer_Catalyst_Temps_2026-09.csv`, in the period's
`Additional Documentation/Oxidizer Data` folder (Garrett's Drive area — NOT on Max's local Drive
mount; download it through the Drive connector).

| Index | Header (as exported) | Notes |
|---|---|---|
| 0 | `timestamp_central` | Format `M/D/YYYY H:MM`, US Central time |
| 1 | `train1_ox2100_catalyst_inlet_F` | °F |
| 2 | `train1_ox2100_catalyst_outlet_F` | °F |
| 3 | `train2_ox2200_catalyst_inlet_F` | °F |
| 4 | `train2_ox2200_catalyst_outlet_F` | °F |

- Pass the single file to `--input`; the 5-column positional map applies unchanged. Confirm the
  header order still reads Train 1 inlet, Train 1 outlet, Train 2 inlet, Train 2 outlet before
  running — the positional map does not check train identity in a combined file.
- September 2026: 8,640 rows, exactly one per 5 minutes, no gaps or repeated timestamps.
- **Two kinds of "no reading":** `0` for offline stretches (as before) AND, new in this export,
  **empty cells** — scattered single dropped readings (92 rows in September). Both become blank in
  the charts; the script prints the two counts separately so they can be reported apart.

---

## Previous export format (July–August 2026) — ONE FILE PER TRAIN

Since the July 2026 period, Garrett's export arrives as **two CSVs, one per train**, e.g.
`Train 1 OX - JULY.csv` and `Train 2 OX - JULY.csv`. Each is three columns:

| Index | Header (as exported) | Notes |
|---|---|---|
| 0 | t_stamp | Format: `YYYY-MM-DD HH:MM:SS.fff` — **not** the old `M/D/YY H:MM` |
| 1 | `…/2100-Train1/OX-2100/Status/Sts_CatalystInletTemp` (or `2200-Train2`) | Inlet, °F |
| 2 | `…/2100-Train1/OX-2100/Status/Sts_CatalystOutletTemp` (or `2200-Train2`) | Outlet, °F |

Pass **both files** to `--input` in either order. The script merges them on the timestamp into
the same 5-column table the old combined export produced, so everything downstream is unchanged.

- **Train identity comes from the column headers** (`Train1`/`2100` vs `Train2`/`2200`), never
  from the order the files are passed. Passing them backwards produces identical output.
- The merge is an **inner join on the timestamp** — a reading is kept only when both trains
  report the same instant. Any unpaired readings are counted and reported in the run output.
  In July 2026 both files had 8,929 rows with identical timestamps, so nothing was dropped.
- Values are never altered by the merge, only placed side by side, so the Raw workbook is still
  the readings exactly as received.
- Timestamp parsing tries both known shapes and then falls back to auto-detection, so old and
  new exports both load without a code change.

---

## Previous export format (May–June 2026) — single combined file

A plain CSV, temperature-only, 5-minute readings, still loaded without any change:

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
