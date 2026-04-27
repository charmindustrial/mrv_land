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

### Surface / Injection Pressure
- `surface_pressure_psi`
- `Injection Pressure (psi)`

### Annular / Casing Pressure
- `annular_pressure_psi`
- `Casing Pressure (psi)`
- `Casing Presure (psi)` (known typo in some exports)

### Oil Flow Rate
- `oil_rate_gpm`
- `Oil Flow Rate (gpm)`
- `Flow Rate (gpm)` (in some exports this is oil flow, not total)

### Brine Flow Rate
- `brine_rate_gpm`
- `Brine Rate (gpm)`
- `Brine Flow Rate (gpm)`

### Cumulative Oil Volume
- `oil_total_gal`
- `Oil Totilizer` (known misspelling in exports)

### Cumulative Brine Volume
- `brine_total_gal`
- `Brine Totalizer`

### Injection Status
- `injecting` — "YES" or NaN
- May not be present in older exports. If absent, infer injection status from flow rate: if `oil_rate_gpm > 0.5` or `brine_rate_gpm > 0.5`, treat as injecting.

### Columns to Drop (not compliance-relevant)
- Any temperature columns: `injection_temp_f`, `train1_temp_f`, `train2_temp_f`, `Storage Temp (f)`, `Manifold Temp (f)`, `Oil Storage Temp (1)`, `Oil Storage Temp 2`, `Injection Manifold Temperature (f)`, etc.
- `Bottomhole Pressure (psi)` / `Bottom Hole Pressure` — not a surface compliance item
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
