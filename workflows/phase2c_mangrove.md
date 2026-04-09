---
phase: "2c"
title: "Mangrove Data Entry"
type: phase
period: "{{current_rp}}"
status: complete
depends_on: ["2a", "2b"]
trigger: "After Phase 2a and 2b are complete"
---

# Phase 2c: Mangrove Data Entry

**Trigger:** After [[phase2a_injection_batch_data]] and [[phase2b_injection_emissions]] are complete
**Output:** All events for the reporting period entered and evidenced in Mangrove

**Project:** Charm Basco Bio-oil/Biochar (`/nexus/709/data-inputs/events`)
**URL:** https://app.gomangrove.com/nexus/709/data-inputs/events

**Session type:** Playwright browser automation — keep sessions focused, one category at a time

---

## Event Categories

### Category A: Site Emission Events (from Phase 2b)

#### A1. Gasoline Usage Events
**Event type:** Basco Injection Gasoline Usage
**One event per receipt/invoice**
**Fields:**
- Date range: [purchase date] 00:00 – 23:59 [timezone]
- Tracking ID: invoice number
- Origin: Basco 6 Injection
- Destination: Basco 6 Injection
- Basco Injection Gasoline Usage (gal): gallons from receipt
- **Do NOT check** "Update distance and attach route map as evidence"

**Evidence to attach:** Receipt image/PDF from `Gasoline\Receipts\`

#### A2. Diesel Delivery Events
**Event type:** Basco Injection Diesel Delivery
**One event per invoice**
**Fields:**
- Date range: [delivery date] 00:00 – 23:59 [timezone]
- Tracking ID: invoice number
- Origin: Basco 6 Injection
- Destination: Basco 6 Injection
- Basco Injection Diesel Usage (gal): gallons from receipt
- **Do NOT check** "Update distance and attach route map as evidence"

**Evidence to attach:** Receipt PDF from `Diesel\Receipts\`
**Note:** Multiple invoices can share one receipt file (e.g., two Mar 30 diesel invoices both use `3.30.26 LA Fuel.pdf`)

#### A3–AN. Other Emission Events

**Full event type list (confirmed):**
- `Additional Emissions - Basco Injection` — catch-all for argon, railcar, sitework, embodied emissions, etc.
- `Additional Emissions - KS Pre-Treatment` — KS-side only (no longer active)
- `Basco Injection Brine Water Used`
- `Basco Injection Diesel Delivery` ← A2 above
- `Basco Injection Electricity Usage (Grid)`
- `Basco Injection Gasoline Usage` ← A1 above
- `Basco Injection Injected Oil` ← Category B below
- `Basco Injection LCS Delivery`
- `Basco Injection - Number of Trucks (Opel to B6)`
- `Basco Injection Waste Disposal`

**TODO:** Document field structure for each unmapped category (brine, electricity, LCS, additional emissions) when we work through them for the first time.

---

### Category B: Injection Batch Events (from Phase 2a)

**Event type:** `Basco Injection Injected Oil`
**One event per injection batch**
**Mangrove note:** *"Enter the Order Number of the injection in the Tracking ID field."*

#### Fields

| Field | Value | Source |
|---|---|---|
| Date Range | Injection completion date, 00:00 – 23:59 | COBB |
| Tracking ID | Order Number | COBB |
| Injected Oil - Mass | Offloaded kg − sparging loss | COBB (gross) → ops notes (sparging loss % per batch) → net injected mass |
| Injected Oil - % Carbon Content (from sample) | % C value | SGS lab report |
| Injected Oil - pH (from sample) | pH value | SGS/email testing data |
| Injected Oil - Salt (lb) | **Always 0** | — |
| Injection - LCS consumed | **Always 0** | — |
| Injection - Brine Flush Vol | **Always 0** | — |
| Injected Oil - Density (from sample) | Leave null | — |
| Injected Oil - Water Content (from sample) | Leave null | — |

**Mass source:**
Use **"Mass of Bio-Oil Injected (kg)"** from the Ops Notes sheet — this is already net of sparging loss (1.29% constant).
Location: `Removals Reporting/2026/[RP]/Injection Batch Data/[Week folder]/[UID]/[UID] Ops Notes.gsheet`
Do NOT use COBB offloaded kg directly — that is gross mass before sparging loss.

**Evidence to attach:** Scale ticket (from MFO/Manufacturo) + SGS lab report PDF

---

## Playwright Session Workflow

### Before starting
1. Copy all receipt files to `C:\Users\Garett Lutz\Desktop\Claude\.playwright-mcp\` (Playwright can only upload from this path)
2. Have tracker data ready (event dates, invoice numbers, gallons)
3. Open a fresh Playwright session — navigate to Mangrove events page

### For each event
1. Click "Add Event" → select event type
2. Fill date range (calendar nav: use `.ant-picker-header-prev-btn` if calendar opens on current month)
3. Fill tracking ID, value, locations
4. Uncheck "Update distance and attach route map as evidence" (under Locations section)
5. Save event
6. Re-open event → click "Upload" in Evidence section
7. Click "Choose File" → `browser_file_upload` with path in `.playwright-mcp\`
8. Click Save in upload dialog
9. Verify receipt appears in Evidence list

### Timezone note
- Events before ~Mar 8: MST (Mountain Standard Time)
- Events from ~Mar 8 onward: MDT (Mountain Daylight Time)
- Mangrove handles this automatically based on date

### Auto route map
- Mangrove auto-generates a route map when locations have different origin/destination
- For gasoline/diesel events: origin = destination = Basco 6 Injection → no map should generate
- If a map appears anyway: delete it from Evidence, then edit event and uncheck "Update distance and attach route map as evidence"

---

## File Upload Setup (per session)

Receipt files to pre-copy to `.playwright-mcp\`:

**Current period (Mar 3 – Apr 1) gasoline:**
- `WorkTruck_3-3-2026.jpg` → Mar 3, inv 660985
- `3 6 26.jpg` → Mar 6, inv 1119
- `F-150_3-12-2026.jpg` → Mar 12, inv E/4191914
- `F-150_3-17-2026.jpg` → Mar 17, inv E/4193506
- `3 30 26.JPEG` → Mar 30, inv 813314

**Current period (Mar 3 – Apr 1) diesel:**
- `3.13.26 Fuel.pdf` → Mar 13, inv 36747114800
- `3.29.26 LA Fuel.pdf` → Mar 29, inv 36938149060
- `3.30.26 LA Fuel.pdf` → Mar 30, inv 36949105180 AND inv 013317

---

## Status Tracking (current period Mar 3 – Apr 1)

### Gasoline Events — Mar 3–Apr 1 RP (complete)
| Date | Invoice | Gallons | Entered | Receipt | Map Removed |
|------|---------|---------|---------|---------|-------------|
| Mar 3 | 660985 | 22.316 | ✓ | ✓ | ✓ |
| Mar 6 | 1119 | 22.007 | ✓ | ✓ | ✓ |
| Mar 12 | E/4191914 | 17.615 | ✓ | ✓ | ✓ |
| Mar 17 | E/4193506 | 12.5006 | ✓ | ✓ | ✓ |
| Mar 30 | 813314 | 18.295 | ✓ | ✓ | ✓ |

### Diesel Events — Mar 3–Apr 1 RP (complete)
| Date | Invoice | Gallons | Entered | Receipt | Map Removed |
|------|---------|---------|---------|---------|-------------|
| Mar 13 | 36747114800 | 62.869 | ✓ | ✓ | ✓ |
| Mar 29 | 36938149060 | 57.842 | ✓ | ✓ | ✓ |
| Mar 30 | 36949105180 | 52.403 | ✓ | ✓ | ✓ |
| Mar 30 | 013317 | 10.484 | ✓ | ✓ | ✓ |

---

## Session Handoff Template

```
Phase: 2c - Mangrove
Period: [RP name]
Session focus: [gasoline events / diesel events / batch events / etc.]
Completed: [list]
Remaining: [list]
Browser crashed: [yes/no — if yes, need MCP restart]
Next: [specific event or category to start with]
```

---

## Confirmed Conventions
- **All site emission categories** get Mangrove events every period.
- **Unsanctioned/unmapped categories** use a general "Additional Site Emission" event type — confirm exact name on first entry.
- **Order:** No required order across categories.

## Open Questions
- [ ] Injection batch event type names and field structure for AECN, WODO, QOWV, Kerry — map in a live session.
- [ ] Exact event type name for unsanctioned site emission categories.
