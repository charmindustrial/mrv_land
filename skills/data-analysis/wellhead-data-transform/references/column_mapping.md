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
