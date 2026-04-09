---
phase: "2b"
title: "Injection Emissions"
type: phase
period: "{{current_rp}}"
status: complete
depends_on: ["2a"]
trigger: "After Phase 2a batch data is verified"
---

# Phase 2b: Injection Emission Data

**Trigger:** After Phase 2a batch data is verified
**Output:** Complete site emissions breakdown for the reporting period — gasoline, diesel, and all other emission categories — ready for BCU Quant spreadsheet and Mangrove

---

## Emission Categories

Based on Feb-Mar RP structure. Confirm if any categories are added/removed for new periods.

| Category | Tracker File Location | Emission Factor Used |
|----------|----------------------|----------------------|
| Site Diesel | `[RP]\Site Emissions\Diesel\` | Diesel WTW: 0.00387 MTCO2e/kg |
| Site Gasoline | `[RP]\Site Emissions\Gasoline\` | Gasoline WTW: 0.00374 MTCO2e/kg |
| Argon | `[RP]\Site Emissions\Argon\Receipts\` | ASU electricity intensity × grid EF (see tracker) |
| Brine | `[RP]\Site Emissions\Brine\` | TBD |
| Railcar Cleaning | `[RP]\Site Emissions\Railcar Cleaning\` | TBD |
| Electricity | `[RP]\Site Emissions\Electricity\` | Grid EF by state (LA) |
| Support Travel | `[RP]\Site Emissions\Support Travel\` | By mode (air, ground) |
| Basco Sitework | `[RP]\Site Emissions\[Month] Basco Sitework\` | Diesel, crane, limestone |
| Embodied Emissions | `[RP]\Site Emissions\Embodied Emissions\` | NAICS Supply Chain EFs |
| KS Equipment Transport | `[RP]\Site Emissions\KS Equipment Additional Transport Emissions\` | Flatbed truck EF |
| Methanol | `[RP]\Site Emissions\Methanol (NONE)\` | (zero if no methanol flush) |
| Railcar Loss Emissions | `[RP]\Railcar Loss Emissions\` | TBD |

**Base path:** `G:\.shortcut-targets-by-id\17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b\Removals Reporting\2026\[RP Name]\Site Emissions\`

---

## Step-by-Step

### Step 1: Gasoline Tracker

**File:** `[RP]\Site Emissions\Gasoline\[tracker].xlsx`
**Receipts:** `[RP]\Site Emissions\Gasoline\Receipts\`

For each purchase entry:
- Date, Invoice #, Gallons purchased
- Formula: `=gallons × density_factor × EF` (uses cell ref $J$2 or equivalent — never hardcode)
- Verify formula references emission factor cell, not hardcoded number
- Cross-check each row against its receipt file

Current period (Mar 3 - Apr 1) entries:
| Date | Invoice | Gallons |
|------|---------|---------|
| Mar 3 | 660985 | 22.316 |
| Mar 6 | 1119 | 22.007 |
| Mar 12 | E/4191914 | 17.615 |
| Mar 17 | E/4193506 | 12.5006 |
| Mar 30 | 813314 | 18.295 |

### Step 2: Diesel Tracker

**File:** `[RP]\Site Emissions\Diesel\[tracker].xlsx`
**Receipts:** `[RP]\Site Emissions\Diesel\Receipts\`

Same structure as gasoline — date, invoice, gallons, formula-driven emissions.

Current period (Mar 3 - Apr 1) entries:
| Date | Invoice | Gallons | Receipt File |
|------|---------|---------|-------------|
| Mar 13 | 36747114800 | 62.869 | 3.13.26 Fuel.pdf |
| Mar 29 | 36938149060 | 57.842 | 3.29.26 LA Fuel.pdf |
| Mar 30 | 36949105180 | 52.403 | 3.30.26 LA Fuel.pdf |
| Mar 30 | 013317 | 10.484 | 3.30.26 LA Fuel.pdf |

### Step 3: Other Site Emissions Categories

For each category tracker:
- Read current xlsx file
- Verify entries are complete for the reporting period
- Check formulas reference EF cells (not hardcoded)
- Flag any missing data or gaps

#### Argon (Daigle Welding Supply)
- **Source:** Receipt PDFs in `[RP]\Site Emissions\Argon\Receipts\`
- **Two product types — different handling:**
  - **Liquid cylinder (AR230L):** Liter quantity stated directly on invoice ("230 LITER LIQUID ARGON") — enter as-is, no conversion
  - **Compressed K-pack (ARK12PK):** CF quantity on invoice ("3000CF INERT GAST") — convert to liters via: `CF × 0.02832 × 1.784 ÷ 1.4` (e.g. 3000 CF → 108.3 L)
- **Verifier note:** Add two-case explanation note to row 1 of each new tracker (see Mar 3–Apr 1 sheet row 1 as template)
- **Tracker structure:** New xlsx copy each period; columns: Date, Invoice, Qty (L), Qty (kg), Production Emissions
- **Calc:** Production emissions = kg × ASU electricity intensity (H2) × grid EF (H3), net of RECs; plus transport process + embodied; all via cell references
- **EFs:** H2=17.17 kWh/kg, H3=0.3656 kg CO2e/kWh, H4=0.0368 (RECs EF), H8=1.4 kg/L density, journey distance=42.1 mi

### Step 4: BCU Quant Spreadsheet

**File:** `[RP]\[RP name] BCU Quant.xlsx`
- Template-based, but batch numbers and values change each period
- Primary purpose: Garrett's tracking sheet to record BCUs as they're entered in Mangrove and Certify
- Verify totals are populated and consistent with tracker outputs
- Cross-check against prior period for reasonableness

**Key output cell values needed:**
- Total Site Diesel (MT CO2e)
- Total Site Gasoline (MT CO2e)
- Total per category (MT CO2e)
- Grand Total Site Emissions (MT CO2e)

### Step 5: Embodied Emissions — Period Amortization

**File:** `[RP]\Site Emissions\Embodied Emissions\Basco 6 Capital and Sitework Embodied Emissions Inventory [RP].xlsx`
**Tab:** `[Month] [YY] Amortization` (e.g., "March 26 Amortization")
**Depends on:** Phase 2a output (verified batch data)

#### 5a: Build the batch table

From Phase 2a verified output, collect one row per batch UID:

| Column | Field | Source |
|--------|-------|--------|
| A | Batch # | COBB `injection_batch` (Phase 2a Step 1) |
| B | MOBI (kg) | Final injectate mass after sparging/LCS (Phase 2a Step 5) |
| C | C Content | Carbon wt% as decimal from SGS COA (Phase 2a Step 3) |
| D | Molar Mass | Constant `3.666666667` (= 44 ÷ 12, CO2-to-C ratio) |
| E | Gross Removal (kg CO2e) | Formula: `= B × C × D` |
| F | C Content Uncertainty Add | Formula: `= C × $J$2` where J2 = Uncertainty RSD (currently 0.004) |

- Kerry batches: group by range if sharing a single CHN report (e.g., "Kc-0001 - Kc-0004")
- AECN: one row per UID
- Charm WODO/QOWV: one row per UID

#### 5b: Sum and cross-check

- Sum column E → period gross removals (kg CO2e)
- Convert to MT: `÷ 1000`
- Cross-check against `Amortization` sheet current RP row (column B = Gross Removals MT, column D = Kg Penalty/RP)
- The Amortization sheet rate is in B5 (`Kg Penalty/MT`): `= Total Pool (B1) ÷ Est Lifetime Gross Removals (B2) × 1000`

#### 5c: Calculate period embodied emissions

- Period Capital EE (kg CO2e) = `Amortization!B5 × period gross removals (MT)`
- Period SP&C EE: from the SP&C inventory file (see [[embodied_emissions_quantification]] SP&C section) — `total kg CO2e/week × weeks in RP`
- Total Period EE = Capital EE + SP&C EE
- Verify both values are recorded in the Amortization sheet RP row (columns D and E)

#### 5d: Verify consistency

- [ ] Batch count in amortization tab matches total batches from Phase 2a
- [ ] Each MOBI value matches Phase 2a verified injectate mass
- [ ] Each C Content matches SGS COA value exactly
- [ ] Gross removal sum is consistent with BCU Quant gross total
- [ ] Amortization rate has not changed from prior period (unless inventory was updated — see [[embodied_emissions_quantification]])

---

## Emission Factors Reference

All from `Standard Emission Factors + Calculations - 2026.csv` (GLEC V3.2 2025 / GREET 2024–2025):

| Item | Factor | Units | Source |
|------|--------|-------|--------|
| Diesel WTW | 3.87 | kgCO2e/kg fuel | GLEC V3.2 2025 |
| Gasoline WTW | 3.74 | kgCO2e/kg fuel | GLEC V3.2 2025 |
| LPG WTW | 3.63 | kgCO2e/kg fuel | GLEC V3.2 2025 |
| Tanker truck process | 1.143e-04 | MTCO2e/t-mi | GLEC V3.2 2025 |
| Flatbed truck process | 1.384e-04 | MTCO2e/t-mi | GLEC V3.2 2025 |
| Rail transport process | 2.5910374e-05 | MTCO2e/t-mi | GLEC V3.2 2025 |
| Tanker truck embodied | 2.3756059e-04 | MTCO2e/mi | GLEC V3.2 2025 |
| Non-tanker truck embodied | 1.927908256e-04 | MTCO2e/mi | GLEC V3.2 2025 |
| Railcar embodied | Needs updating | MTCO2e/t-mi | GLEC V3.2 2025 |
| AECN production process | 0.10402 | MTCO2e/MT oil | AECN LCA H1 2026 (0.10380 baseline + uncertainty) |
| AECN production embodied | 0.02116 | MTCO2e/MT oil | AECN info + NAICS |
| Grid electricity — KS | 4.655516852e-04 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Grid electricity — CO | 4.890238251e-04 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Grid electricity — LA | 4.630140342e-04 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Wind RECs — KS | 1.002719674e-05 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Solar RECs — CO | 3.664154577e-05 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Solar RECs — LA | 3.664154577e-05 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| LCS (50% NaOH) | 0.9535517371 | MTCO2e/T LCS | GREET 2024 |

**EF Verification Rule:** At the start of each reporting period, verify that all EFs in Certify match the current Standard EF CSV. EFs are updated annually (or when AECN LCA is refreshed). Flag any stale values in Certify for correction — until Mangrove (MG) automates backend EF updates, this is a manual check.

**Rule:** Always use cell references (e.g. $J$2, $N$4) in calc sheets — never hardcode numeric EF values.

---

## Output of This Phase

- Total emissions per category (MT CO2e)
- Grand total site emissions for the period
- Verified receipt-to-tracker linkage for diesel and gasoline
- BCU Quant populated
- Period amortization tab populated with per-batch gross removals
- Period embodied emissions (capital + SP&C) calculated

Feeds into: [[phase2c_mangrove]] and [[phase2d_certify_qa]].

---

## Session Handoff Template

```
Phase: 2b - Injection Emissions
Period: [RP name]
Categories completed: [list]
Categories remaining: [list]
BCU Quant status: [not started / partial / complete]
Blocked on: [missing receipts, exports, etc.]
Next: [specific next step]
```

---

## Confirmed Conventions
- **Emission categories are included only when applicable** — omit categories with zero activity for cleanliness (e.g., no railcar cleaning if no rail batches, no KS equipment transport if no moves). Do not add placeholder zero-value entries.
- **Support travel:** Garrett enters this manually — too nuanced to automate. Skip in my workflow.
- **Sitework:** Data comes from ops team invoices/activity. Currently manual. Future goal: automate via invoice parsing. For now, verify the tracker is populated before starting Phase 2b.
- **Argon:** Always present.

## Per-Tracker Deep Audit Checklist (from Max's Mar RP review)

Every site emissions tracker must pass these checks before Phase 3a:

### All Trackers
- [ ] EF values match the 2026 Standard EF CSV (check every cell reference, not just the value)
- [ ] EF source labels cite the correct version (e.g., "GLEC V3.2 2025" not "V3.0 2024")
- [ ] All emissions totals have units labeled (kg CO2e, MT CO2e)
- [ ] Naming consistency: folder name ↔ calc sheet name ↔ Certify component name must align
- [ ] All formulas resolve (no #REF, #VALUE, or errors from extra spaces)

### Sitework (LA Sitework)
- [ ] Every invoice has a corresponding emissions calculation (no missing items)
- [ ] Transport emissions included for all deliveries/pickups (e.g., cleanout transport)
- [ ] Aggregate/material EFs updated to 2026 SEF
- [ ] Distance evidence: Google Maps screenshots for all site↔vendor routes
- [ ] Folder renamed to match Certify component name

### Railcar Movement
- [ ] Naming matches Certify component
- [ ] Embodied emissions EF sourced and current
- [ ] All distances have cited sources (screenshots or references)

### Methanol
- [ ] All cell labels include units

### SP&C
- [ ] All formulas checked for typos (e.g., extra spaces in SUM functions)
- [ ] If sheet is uploaded to Certify as evidence, verify the Certify copy also resolves correctly

### CapEx EE
- [ ] Weight assumptions documented with source
- [ ] Only include receipts if using cost-based LCA (not needed for material-based)
- [ ] EF labels match the actual material (e.g., don't label treated lumber EF as "Steel")
- [ ] All EFs traceable to Standard EF CSV

### Electricity
- [ ] Date range matches RP exactly — exclude days outside the reporting period

### Diesel
- [ ] Every fuel purchase has a matching receipt/transaction record
- [ ] Confirm whether fuel was delivered (→ delivery emissions) or picked up (→ no delivery emissions)

### Gasoline
- [ ] All receipts present and matched
- [ ] Confirm fuel card (WEX) status — any changes to tracking method?

### Support Travel
- [ ] EF table references updated to current version and source
- [ ] Garrett confirms all trips are entered

## Open Questions
- [ ] None remaining.
