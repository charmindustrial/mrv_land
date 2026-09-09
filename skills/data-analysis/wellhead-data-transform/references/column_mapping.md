# Column Name Mapping — Basco SCADA Exports

Raw wellhead data exports from Basco use inconsistent column naming across reporting periods and SCADA system versions. The skill must identify and normalize columns to a standard schema before processing.

## Standard Output Schema

| Standard Name | Description | Compliance Role |
|---|---|---|
| `local_time` | Timestamp (local CST/CDT) | Time series |
| `injecting` | Injection status (YES/NaN) | Filter for differential calc |
| `surface_pressure_psi` | Surface injection pressure | Max limit: 455 psig |
| `annular_pressure_psi` | Tubing-casing annular pressure | Min limit: 200 psig |
| `oil_rate_gpm` | Oil flow rate | Quarterly reporting |
| `brine_rate_gpm` | Brine flow rate | Quarterly reporting |
| `total_rate_gpm` | Combined flow rate | Quarterly reporting |
| `oil_total_gal` | Cumulative oil volume | Reference only |
| `brine_total_gal` | Cumulative brine volume | Reference only |

## Known Column Name Variants

### Timestamps
- `local_time` (newer SCADA exports, includes timezone offset)
- `Date` (older exports, may be date-only with separate `time` column as epoch ms)
- `t_stamp` (June 2026 export onward — naive datetime, NO timezone attached. Treat as local site time, Central CST/CDT.)

### Surface / Injection Pressure
- `surface_pressure_psi`
- `Injection Pressure (psi)`
- `Injection Pressure` (June 2026 export onward — same field, no unit suffix)

### Annular / Casing Pressure
- `annular_pressure_psi`
- `Casing Pressure (psi)`
- `Casing Presure (psi)` (known typo in some exports)
- `Annular Pressure` (June 2026 export onward)

### Oil Flow Rate
- `oil_rate_gpm`
- `Oil Flow Rate (gpm)`
- `Flow Rate (gpm)` (in some exports this is oil flow, not total)
- `Injection Rate` (June 2026 export onward — this is the **bio-oil** injection rate, not a combined total. Blank/empty when the well is idle rather than 0.)

### Brine Flow Rate
- `brine_rate_gpm`
- `Brine Rate (gpm)`
- `Brine Flow Rate (gpm)`
- `Brine/QOWV Rate` (June 2026 export onward — combined brine and quench-oil/water-vapor rinse rate. See injection-status caveat below: this flows independently of bio-oil injection and must NOT be used to infer injection status.)

### Cumulative Oil Volume
- `oil_total_gal`
- `Oil Totilizer` (known misspelling in exports)

### Cumulative Brine Volume
- `brine_total_gal`
- `Brine Totalizer`

### Injection Status
- `injecting` — "YES" or NaN
- May not be present in older exports. If absent, infer injection status from flow rate: if `oil_rate_gpm > 0.5`, treat as injecting.
- **Caveat (June 2026 export onward):** the default "oil OR brine > 0.5" rule breaks when a combined `Brine/QOWV Rate` column is present, because that rinse rate runs nearly continuously and independently of bio-oil injection. In the June 2026 export it was above 0.5 in ~42% of rows while true bio-oil injection occurred in only ~19%. When a bio-oil-specific rate column exists (`Injection Rate` / `oil_rate_gpm`), key injection status off the bio-oil rate ALONE. The differential compliance chart depends on this filter, so getting it wrong over-counts "injection" by roughly 3×.

### Columns to Drop (not compliance-relevant)
- Any temperature columns: `injection_temp_f`, `train1_temp_f`, `train2_temp_f`, `Storage Temp (f)`, `Manifold Temp (f)`, `Oil Storage Temp (1)`, `Oil Storage Temp 2`, `Injection Manifold Temperature (f)`, etc.
- `Bottomhole Pressure (psi)` / `Bottom Hole Pressure` / `BHP` — not a surface compliance item
- `Injectivity Index (q/dP)` / `Injectivity Index` — operational metric, not compliance
- Any `qc_*` columns — internal QC flags
- `time` — epoch timestamp (redundant if `Date` is parsed)

## Analytics Workbook Format (July 2026 export onward)

The July 2026 file (`basco6_analytics_2026_07.xlsx`) was not a raw SCADA export. It is a pre-processed analytics workbook pulled from BigQuery, with nine sheets:

`Flow`, `Pressure`, `Daily_Volumes`, `Injectivity`, `Trends`, `Fluid_Properties`, `Events`, `Normalized`, `Params`.

Only three carry minute-level readings; join them on `timestamp`:

| Sheet | Column | Maps to |
|---|---|---|
| Flow | `timestamp` | `local_time` (naive, local CST/CDT) |
| Flow | `corrected_flow_gpm` | `oil_rate_gpm` — bio-oil rate, already cleaned; NaN when idle |
| Flow | `flow_gpm` | raw bio-oil rate, retains noise; use `corrected_` instead |
| Pressure | `tubing_psi` | `surface_pressure_psi` |
| Pressure | `casing_psi` | `annular_pressure_psi` |
| Fluid_Properties | `corrected_brine_rate_gpm` | `brine_rate_gpm` |

Drop from this format: `bottomhole_psi`, `masip_psi` (a constant 455), `viscosity_cp`, `ph`, `bottomhole_temp_f`, `injectivity`/`ii_*`, and all `*_flag` columns. `Daily_Volumes`, `Injectivity`, `Trends`, `Normalized` are derived rollups — do not concatenate them. `Events` spans **all time, not just the reporting period** — filter by `start_time` before using it.

**Read the `Params` sheet first.** It reports the row count the generator retrieved for each tag, e.g. `Rows — Casing Pressure (raw)`. A zero there means the tag returned nothing and the corresponding compliance item cannot be evaluated — catch this before building charts. The first July 2026 file came through with casing pressure at 0 for the whole month while every other tag was full; a corrected file backfilled it from tag PT-1062 and added a `NOTE — Casing backfill` row to `Params`. Check `Params` for such notes on any re-issued file, and diff a re-issue against the original rather than assuming only the named column changed.

**Google Sheets round-trip artifact.** When a corrected file arrives as a native Google Sheet rather than an .xlsx, empty cells come back as empty strings instead of blanks. A naive `DataFrame.equals()` then reports the flag/note text columns as fully changed when no value actually differs. Compare numeric columns with `np.isclose(..., equal_nan=True)` before concluding anything changed.

Cleaning already applied upstream in this format, recorded in the `*_flag` columns: bio-oil readings below 1.0 GPM removed as HMI noise, readings above 100 GPM removed as communication errors, and viscosity pinned at a 1000 cP default removed as communication loss.

`flowmeter_suspect` / `flowmeter_note` mark windows where flow read zero while pressure stayed stable — a metering outage, not a stop in injection. `est_rate_before_gpm` / `est_rate_after_gpm` are the **bracketing rates on either side of the window, not filled-in corrections**; `corrected_flow_gpm` stays NaN there and the volume is unresolved until someone enters a rate.

## Multi-Sheet Handling

Older exports may split data across multiple sheets by date range (e.g., "2.4-2.20", "2.21-3.1"). When this occurs:

1. Read all sheets
2. Normalize column names in each sheet to the standard schema
3. Concatenate into a single DataFrame
4. Sort by timestamp
5. Then apply the user's date range filter

The user's requested date range should span across sheet boundaries seamlessly.

**Not every extra sheet is data to concatenate.** The June 2026 export shipped with a `Sheet1` that was a hand-built pivot summary ("Row Labels" / "Sum of Injection Rate" by day, ending in a "Grand Total"), plus the real minute-level data on a separate sheet named like `Export YYYY-MM-DD HH_MM_SS`. Drop pivot/summary sheets — do not concatenate them. Identify the real data sheet by its column header row (`t_stamp` / `local_time` / `Date` plus pressure columns), not by sheet position.

## Sensor Artifacts to Expect

- **Transmitter saturation rail at exactly 1000.000 psig.** In the June 2026 export, surface and annular pressure both pinned to exactly 1000.000 for a sustained block (~8 days) that coincided with a well workover, and again for ~40 minutes during a mechanical integrity test. A value holding at an exact round number (especially 1000.000) is a transmitter rail / default fault value, not a real pressure. Exclude these from compliance evaluation; they typically fall under the Order Item 6c exemption (workovers, well or reservoir tests, or fluctuations under 4 consecutive hours). Confirm the operational cause in `#injection-ops-la` before writing the Notes tab.
- **Brief annular dropouts to 0 psig** during non-injection periods (e.g., a 6-minute stretch in the June 2026 export) are momentary SCADA communication dropouts, not real pressure events.
