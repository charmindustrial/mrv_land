# Injection Batch Folder Structure & Ops Notes Template

## Folder Hierarchy

**Root:** `G:/.shortcut-targets-by-id/17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b/Removals Reporting/`

```
Removals Reporting/
  2026/
    [RP Name, e.g. "March 3 - April 1 RP"]/
      Injection Batch Data/
        [Week folder, e.g. "3 16 26-3 22 26"]/    <- format: M DD YY-M DD YY
          [Batch UID]/
            [UID] Ops Notes.gsheet
            Scale Tickets/
              [UID] Full Scale Ticket.pdf
              [UID] Empty Scale Ticket.pdf
            Testing/
              [First UID] - [Last UID].pdf          <- one SGS COA PDF covers all batches in the week
        AECN BOLs/
        Kerry Oil/
```

**Note:** Feb-Mar 2026 RP has batch folders directly under Injection Batch Data (no week sub-folders). Week folders were introduced in the March 3 - April 1 RP.

## Oil Type UIDs

| Oil Type | Source | UID Format | Example |
|----------|--------|-----------|---------|
| 3rd party — AECN | AE Cote-Nord, Port-Cartier QC | 2-XXX | 2-174 |
| 3rd party — Kerry Oil | Kerry | K-XXXXX | K-00001 |
| 1st party — WODO | Charm (Fort Lupton CO) | 3-XXX | 3-46 |
| 1st party — QOWV | Charm (Fort Lupton CO) | 4-XXX | 4-07 |

## Scale Tickets (CAT Scale)

Source: CAT Scale Company (truck stops en route, typically Bunkie LA / I-49 Exit 40)

**Full ticket:** Truck loaded with oil — Gross Weight (LB), Tractor #, Trailer #, Date, Time, Location
**Empty ticket:** Truck after delivery — same fields

**Net injectate mass (lbs) = Full Gross (LB) - Empty Gross (LB)**

## Testing PDF (SGS Certificate of Analysis)

**Lab:** SGS North America Inc., Oil, Gas & Chemicals, St. Rose LA
**Named:** `[First UID] - [Last UID].pdf`

**Fields per batch:**
| Field | Method | Units |
|-------|--------|-------|
| Carbon | ASTM D5291 (Method C) | % (m/m) |
| Hydrogen | ASTM D5291 (Method C) | % (m/m) |
| Nitrogen | ASTM D5291 (Method C) | % (m/m) |
| Kinematic Viscosity at 40C | ASTM D445 | cSt |
| Acid Number (TAN) | ASTM D664 (Method A) | mg KOH/g |
| Density at 15C | ASTM D4052 | g/cm3 |

## Ops Notes Sheet Layout

### Header
- Completion Date
- Batch number (UID)

### Batch Composition Section
Per origin (Origin 1-5): Volume (Gallons), Volume (Liters), Density (kg/L), Mass (kg)
- Origin 1 = AECN tote reference
- Origin 3 = WODO, Origin 4 = QOWV, Origin 5 = Kerry

### Constants
| Constant | Value |
|---------|-------|
| Liters per Gallon | 3.78541 |
| LCS Density (lbs/gal) | 12.76 |
| Kg/Lbs | 0.453592 |
| Sparging Mass Loss | 0.0129 (1.29%) |

### Injection Data Section
Per truck: Full Mass (lb), Empty Mass (lb), Injectate Mass (lbs/kg), pH

**Calculated totals:**
- Total Injectate Mass (kg) = sum of all trucks
- Sparging Loss (kg) = Total Injectate Mass x 0.0129
- Mass of Bio-Oil Injected (kg) = Total Injectate Mass - Sparging Loss

## New Format Starting April 1, 2026
One UID per week instead of one per truck. Same ops notes structure, but multiple trucks all logged within a single batch UID.
