---
phase: "2a"
title: "Injection Batch Data"
type: phase
period: "{{current_rp}}"
status: not_started
depends_on: []
trigger: "End of injection reporting period"
---

# Phase 2a: Injection Batch Data

**Trigger:** End of injection reporting period (e.g., March 3 – April 1)
**Output:** Complete, verified ops notes for every batch UID in the period — ready to feed into Mangrove and Certify

---

## Data Sources

| Source | Location | Access |
|--------|----------|--------|
| Bio-Oil Injection Tracker (COBB tab) | Google Sheet ID: `116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q` | Open real-time via Playwright browser — no export needed |
| Injection Batch folders | `G:\...Removals Reporting\2026\[RP Name]\Injection Batch Data\` | Readable |
| Ops Notes | `[Batch folder]\[UID] Ops Notes.gsheet` | Not directly readable — export needed |
| Scale Tickets | `[Batch folder]\Scale Tickets\` | PDF/JPG — readable |
| SGS COA (CHN analysis) | `[Batch folder]\Testing\[UID range].pdf` | PDF — readable |
| AECN BOLs | `[RP folder]\Injection Batch Data\AECN BOLs\` | PDF — readable |

---

## Folder Structure (April 1+ format with week sub-folders)

```
Injection Batch Data/
  [M DD YY - M DD YY]/          ← week folder
    [UID]/                       ← one UID per week (new format)
      [UID] Ops Notes.gsheet
      Scale Tickets/
        [UID] Full Scale Ticket.pdf
        [UID] Empty Scale Ticket.pdf
      Testing/
        [UID range].pdf
  AECN BOLs/
  Kerry Oil/
```

Pre-April 1: one UID per truck (multiple UIDs per week), no week sub-folders.

---

## UID Types

| Oil Type | UID Format | Example |
|----------|-----------|---------|
| AECN (3rd party) | 2-XXX | 2-174 |
| Kerry Oil (3rd party) | K-XXXXX | K-00001 |
| Charm WODO (1st party) | 3-XXX | 3-46 |
| Charm QOWV (1st party) | 4-XXX | 4-07 |

---

## Step-by-Step (per batch UID)

### Step 1: Pull COBB Data
Source: Bio-Oil Injection Tracker → COBB tab
Fields needed per row:
- `injection_batch` (UID)
- `consumed_lot` (SO number)
- `BOL_number`
- `offloaded_quantity_kg`
- `origin_quantity_kg`
- `injection_completion_date`
- `injection_ph`

**I do:** Open COBB tab real-time via Playwright browser at session start — no export needed.

### Step 2: Scale Tickets → Injectate Mass
For each truck:
- Read Full Scale Ticket PDF → Gross Weight (LB), Tractor #, Trailer #
- Read Empty Scale Ticket PDF → same fields
- Net injectate mass (lbs) = Full − Empty
- Net injectate mass (kg) = lbs × 0.453592
- Verify tractor + trailer # match between full and empty ticket
- Verify ticket dates within 2 weeks of injection date

### Step 3: SGS COA → Carbon Content
Read Testing PDF for each UID:
- Carbon % (ASTM D5291 Method C)
- Hydrogen %
- Nitrogen %
- Density at 15°C (g/cm³)
- Acid Number (TAN)
- Kinematic Viscosity at 40°C
- Sample date, received date, completed date

Verify carbon content reasonable (AECN: ~41–42%)

### Step 4: BOL Verification
For each batch:
- Confirm BOL is present in AECN BOLs folder
- BOL mass ≥ reported injectate mass
- Origin/destination correct (AECN→Basco, Charm→Basco, or AECN→SOPOR→Basco for rail)
- For rail: typically 3 BOLs per railcar (2278R, 2279R, 2281R format)

### Step 5: Ops Notes Verification / Population
Key fields in Ops Notes:
- Completion date ✓ matches COBB
- Batch UID ✓
- Batch composition: origin volumes (gal), density (kg/L), mass (kg) per origin
- Truck injection data: Full Mass (lb), Empty Mass (lb), Injectate Mass (lb), Injectate Mass (kg)
- pH ✓ matches COBB
- Total Injectate Mass (kg)
- Sparging Loss (kg) = Total × 0.0129 (AECN only — NOT Charm WODO/QOWV)
- Mass of Bio-Oil Injected (kg) = Total − Sparging Loss

**Key rule:** Sparging deduction applies to AECN input mass only. Charm QOWV gets LCS pre-treatment instead.

### Step 6: Summary Check
- AECN Oil Added (kg) vs AECN Oil Injected (kg)
- Loss (kg) = Added − Injected
- Loss % — flag if unusual
- Cross-check against COBB offloaded_quantity_kg

---

## Key Constants (embedded in Ops Notes)

| Constant | Value |
|---------|-------|
| Sparging Mass Loss | 1.29% (0.0129) |
| lbs → kg | × 0.453592 |
| Liters per Gallon | 3.78541 |
| LCS Density (lbs/gal) | 12.76 |

---

## Output of This Phase
- Verified injectate mass (kg) per UID
- Carbon content (%) per UID
- pH per UID
- Completion date per UID
- Batch composition (oil types, sources) per UID
- Sparging loss per UID (where applicable)
- BOL references confirmed

All of the above feed directly into [[phase2b_injection_emissions]] and [[phase2c_mangrove]].

---

## Session Handoff Template

```
Phase: 2a - Injection Batch Data
Period: [RP name]
Batches total: [N]
Batches completed: [list UIDs]
Batches remaining: [list UIDs]
Blocked on: [missing docs, exports needed]
Next: [continue with UID X, or proceed to Phase 2b]
```

---

## Confirmed Conventions
- **Kerry Oil:** Batches appear in COBB. Use same format as the most recent prior period unless told otherwise.
- **Weekly batch format (April 1+):** To be discussed separately.
- **COBB access:** Real-time Playwright — no export.

## Open Questions
- [ ] For the new weekly batch format (April 1+), is the ops notes structure the same or different? *(deferred)*
- [ ] Rail batches: is there a separate Rail Batch Summary xlsx like in Feb-Mar RP?
