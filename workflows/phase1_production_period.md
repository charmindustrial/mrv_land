---
phase: "1"
title: "Production Period"
type: phase
cycle: monthly
status: ongoing
depends_on: []
trigger: "Garrett notifies data is available for a given month"
---

# Phase 1: Production Period

**Trigger:** Garrett notifies me that data is available for a given month — I execute at that point
**Output:** PP Close Summary Google Sheet — finalized production period emissions data ready to feed into injection batch CI calculations

**Key distinction:** Production period = CO calendar month. NOT the same as injection reporting period.
See memory: `project_production_vs_reporting_period.md`

**Sequence:** No fixed order — work through components as data is available
**All components are present every month** — even if a category has no activity, it still gets reported (zero or N/A)

---

## End Product: PP Close Summary

**Location:** `G:\...Invoices + Tracking Docs\PP Close Summaries\2026\[Month 26 Production Period Summary].gsheet`

Examples: `Jan 26 Production Period Summary.gsheet`, `Feb 26 Production Period Summary.gsheet`, `Mar 26 Production Period Summary.gsheet`

These are Google Sheets — not directly readable via File Stream. To work with them, export to xlsx first or describe the structure to me.

**Note:** There is also a PP QA Checklist: `G:\...Invoices + Tracking Docs\PP QA Checklist.gsheet`

---

## Component Folders & Structure

**Base path:** `G:\.shortcut-targets-by-id\1k1Hk_7pQumdwZ7dnw-gSVdDlx-rmnzzi\Invoices + Tracking Docs\`

### 1. Pyrolysis Up-Time
**Path:** `Pyrolysis Up-Time\`
**Master tracker:** `Miniforge Pyrolysis Up-Time Reporting.gsheet` (Google Sheet — not readable)
**Per-period evidence:** `2024 2025\Up-Time Data [Period Name]\` — contains PNG screenshots + `.gsheet`
**2026:** No period subfolders visible yet — likely uses master gsheet only
**What it tracks:** System run hours, uptime %, pyrolysis active time for the month
**I can do:** Read PNG screenshots if present; cannot read gsheet directly
**Gaps to fill:** [ ] What fields from uptime feed into the PP Summary? (hours, %, other?)

### 2. Miniforge Pyrolysis Output
**Path:** `Miniforge Pyrolysis Output\2026\[Month 26]\`
**File:** `[Month 26] Production Period Output Summary.gsheet`
**Template:** `[Template] Production Period Output Summary.gsheet`
**What it tracks:** Bio-oil produced (WODO, QOWV volumes/masses), pyrolysis output per month
**Data sources:**
- BGN inventory sheet (Google Sheet — open via Playwright)
- Char sheet (Google Sheet — open via Playwright)
- Manufacturo query via Coefficient (pull by UID — open via Playwright)
**I fill in via:** Playwright browser automation

### 3. Consumables — Diesel
**Path:** `Consumables\Diesel\Diesel Receipts and Invoices\2026\[Month 26]\`
**File:** `[Month 26] Diesel Consumption Calc.gsheet` + `Receipts\` subfolder
**Template:** `[Template] Diesel Consumption Calculator.gsheet`
**What it tracks:** Diesel used at Fort Lupton production facility
**Data source:** Agfinity invoices sent automatically to Garrett's Gmail — I search Gmail when triggered
**I fill in via:** Playwright browser automation (edit gsheet directly)

### 4. Consumables — Gasoline
**Path:** `Consumables\(Dame mas) Gasolina\Gasoline Invoices and Receipts\2026\[Month 26]\`
**Template:** `[Template] Gasoline Consumption Calculator.gsheet`
**What it tracks:** Gasoline used at Fort Lupton production facility
**Data source:** WEX fleet card — Garrett downloads the report and I grab it from `C:\Users\Garett Lutz\Downloads\`
**I fill in via:** Playwright browser automation

### 5. Consumables — Electricity
**Path:** `Consumables\Miniforge Electricity Consumption Records\2026\[Month 26]\`
**Template:** `[Template] Miniforge Electricity Consumption Calculator.gsheet`
**What it tracks:** kWh consumed at Fort Lupton, used to calculate grid electricity emissions
**Data source:** Garrett pulls from utility directly and enters — out of scope for me

### 6. Consumables — Propane
**Path:** `Consumables\Propane and Propane Accessories\Propane Receipts and Invoices\2026\[Month 26]\`
**Template:** `[Template] Propane Consumption Calculator.gsheet`
**What it tracks:** Propane used at Fort Lupton — present every period
**Data sources:**
- Bulk propane: Agfinity invoices (auto-emailed to Garrett) — I search Gmail when triggered
- Cylinder propane: Buckeye invoices (auto-emailed to Garrett) — I search Gmail when triggered
**I fill in via:** Playwright browser automation

### 7. Consumables — Biomass
**Path:** `Consumables\Biomass\`
**Files:**
- `Dry Accepts\2026\` — dry biomass accepted at facility
- `Green Logs Transport Allocation\` — transport emissions for green log delivery
- `Miniforge Biomass Transport Allocation -- Updated.gsheet` — master allocation tracker
**What it tracks:** Feedstock input (dry accepts, green logs), transport emissions
**Data source:** Biomass accepts sheet → tab `new-biomass-accepts-by-week`
**Sheet:** https://docs.google.com/spreadsheets/d/1V4AuvwLprFpDEeF2SCeEoMk8W_hcfG5oZ5Srr4CgpnI/edit
**My job:** Read the `new-biomass-accepts-by-week` tab via Playwright → pull relevant month's data → translate into the monthly PP biomass calc
**Note:** Full field mapping to be confirmed in a live walkthrough session

### 8. Consumables — Water
**Path:** `Consumables\Water\Water Consumption Logs\`
**What it tracks:** Water consumed at Fort Lupton
**Data source:** Bighorn weekly water log — Garrett fills weekly from water meter readings
**Sheet:** https://docs.google.com/spreadsheets/d/16ZGKG6rts2pUUqF-OA1yITQqVBUuHU_sUOyUk97YqEs/edit
**My job:** At PP close, read weekly entries for the month via Playwright → sum/translate into the monthly calc sheet

### 9. Embodied Emissions
**Path:** `Embodied Emissions\2026\[Month 26]\`
**Files:** `Cap Ex MRV [Month 26].gsheet`, `SP&C [Month 26].gsheet`, `Receipts\` subfolder

**SP&C:** Fixed value every month — apply fixed factor, no source data needed.

**CapEx:**
- **New purchases:** Arrive as invoices via email (procurement) — I search Gmail
- **Emission factors:** Use EF from prior purchases of the same category as precedent. Garrett handles anything genuinely new.
- **Logic:**
  1. Add new month's purchases to the running CapEx list with their EE (cost × EF)
  2. Total EE pool = cumulative sum of all items on the list
  3. Amortized rate = total pool ÷ lifetime throughput projection (kg CO2e / tDBM) — throughput is hardcoded in the sheet
  4. Monthly CapEx EE = rate × current month actual biomass throughput
- **I fill in via:** Playwright browser automation

### 10. Waste Disposal
**Path:** `Waste Disposal\`
**Files:**
- `MRV-Related Waste Pick ups.gsheet` — master tracker
- `Waste Disposal Manifests and Invoices\2026\[Month 26]\[Month 26] Prod Waste Disposal Emissions Calc Sheet.gsheet`
- Supporting folders: Manifests, Routing Docs
**What it tracks:** Waste disposal emissions from production operations

### 11. Vendor Delivery Emissions
**Path:** `Consumables\Vendor Delivery Emissions Folder\2026\`
**File:** `[Month 26] Vendor Delivery Emissions Calc Sheet.gsheet`
**What it tracks:** Emissions from vendor deliveries to the Fort Lupton facility
**Data source:** Derived from diesel and propane data already pulled (Agfinity + Buckeye) — no separate source needed
**My job:** Populate calc sheet from values already extracted in components 3 and 6

---

## Google Sheets Access

All calc sheets are Google Sheets (.gsheet) — not readable via File Stream. **Standard method: Playwright browser automation** — I open and edit them directly in the browser. No export/import step needed.

---

## PP Close Summary Structure (from Feb 26 export)

The summary sheet has 4 tabs:

### Tab: [Month] PP Summary
The main calculation sheet. Sections (each feeds the consolidated inventory):

| Section | Key Inputs | Key Output |
|---------|-----------|------------|
| **Biomass Transport** | Tonnes, Miles, Tonne-Miles; Log Handling EF | Total Emissions (MT CO2e) |
| **Pyrolyzer Up-Time** | Total Operating Hours, Production Hours, R+D Hours; RECs (kWh) | % Production, RD BCUs |
| **Equipment Amortization** | Total Biomass Consumed (kg); Amortization Factor (kg CO2e/MT biomass) | Amortized Embodied Emissions (MT) |
| **Spare Parts & Consumables** | EE Estimate per pyrolyzer operating hour (kgCO2e/hr) | SP+C Estimate for Period (MT) |
| **Propane Combustion** | Total PP Deliveries (L), Tank Level at PP Close (%), Fuel Meter Uncertainty (1.29%) | Total Propane Emissions (MT CO2e) |
| **Diesel Combustion** | Total Consumption (L/Gal/kg), Office Generator fills, Fuel Meter Uncertainty | Total Diesel Emissions (MT CO2e); BCUs Applied |
| **Gasoline Combustion** | Total Consumption (Gal/kg), Fuel Meter Uncertainty | Total Gasoline Emissions (MT CO2e) |
| **Electricity Usage** | Total kWh Consumed, Meter Uncertainty (2%), Non-pyrolysis baseline kWh/day, Days in PP; Retired RECs (kWh) | Remaining Emissions after RECs (MT CO2e) |
| **Tailgas Emissions** | Total Biomass Consumed (kg uncertainty-adjusted); Tailgas EF (MT CO2e/kg biomass) | Total Tailgas Emissions (MT) |
| **Water Emissions** | Total Water Consumed (gal/kg); EF (MT CO2e/gal) | Total Water Emissions (MT CO2e) |
| **Consumables Delivery** | Process + Embodied transport emissions | Remaining to Allocate (MT CO2e) |
| **Waste Disposal** | Transport process, Transport embodied, Disposal emissions | Remaining to Allocate (MT CO2e) |

**Right side — Output Allocation:**
| Output Type | Mass (kg) | % Output Mass | C Content (%) | C Content Mass (kg) | % C Content Mass | Total Emissions Allocated (MT CO2e) | kg Emissions/kg Material |
|-------------|-----------|---------------|---------------|---------------------|------------------|--------------------------------------|--------------------------|
| WODO | | | | | | | |
| Biochar | | | | | | | |
| Aqueous | | | | | | | |

**Bottom right — Consolidated Emissions Inventory:**
| Category | Total Emissions (MT CO2e) | % of Total |
|----------|--------------------------|------------|
| Biomass Transport | | |
| Propane | | |
| Diesel | | |
| Gasoline | | |
| Electricity | | |
| Tailgas | | |
| Water | | |
| Consumables Delivery | | |
| Waste Disposal | | |
| Capital Goods EE | | |
| SP+C EE | | |
| **Total** | | |

### Tab: Emission Factors
Reference table — EFs pulled into calculations. Do not edit unless annual EF update.

### Tab: DataTable
Intermediate calculation values pulled from component gsheets.

### Tab: DataCollection
Key MRV output values — these are the fields that feed downstream:
- Production Operating Hours
- Total BM Consumed (MT)
- WODO Yield (kg) + wt%C
- Biochar Yield (kg) + wt%C
- Aqueous Yield (kg)
- All emissions by category (MT CO2e)
- `[MRV]` prefixed fields: Biomass Miles, Raw Biomass Tonnes, Uncertainty-adjusted fuel/electricity quantities, Total Water Used

---

## Workflow Steps

### Step 1: Confirm data availability
Garrett notifies that electricity, pyrolysis up-time, and support travel are populated. All other components I pull myself.

### Step 2: Export PP Summary
Export the gsheet to xlsx → save to `Desktop\Claude\[Month 26 PP Summary].xlsx`

### Step 3: I read and verify the summary
- Check all 12 sections have values (no blanks where data expected)
- Verify consolidated total is reasonable vs. prior period
- Flag any zeroes or anomalies
- Read key MRV output values from DataCollection tab

### Step 4: Cross-check component totals
For any readable files (receipts, xlsx sub-files), verify spot values match what's in the summary.

### Step 5: Output — key values for injection batch CI
From DataCollection tab:
- WODO: mass (kg) + C content (%)
- Aqueous: mass (kg) + C content (%)
- Total emissions allocated to each output type (MT CO2e)
- kg Emissions / kg Material → this is the CI value for injection batch accounting

---

## Session Handoff Template

```
Phase: 1 - Production Period
Period: [Month 26]
Summary exported: [yes/no]
Sections verified: [list]
Anomalies flagged: [list or none]
Key CI outputs:
  WODO: [X kg CO2e/kg]
  Aqueous: [X kg CO2e/kg]
Next: [hand off to [[phase2a_injection_batch_data]] or flag blocker]
```
