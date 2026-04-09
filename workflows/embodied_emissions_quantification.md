---
phase: "embodied"
title: "Embodied Emissions"
type: ad_hoc
status: ongoing
trigger: "New equipment purchase, receipt, or sale/return"
---
[[wood_treated]]
[[steel]]
[[concrete]]
[[industrial_machines]]
# Embodied Emissions Quantification

**Triggers:**
- New equipment purchase invoice received (from procurement team)
- Equipment physically received on site
- Item sold/moved/returned (sold item invoice from procurement team)

**Output:** Updated GWP value in the capital equipment inventory; updated amortized EE for the current reporting period

**File location:** `G:\...\Removals Reporting\2026\[RP Name]\Site Emissions\Embodied Emissions\Basco 6 Capital and Sitework Embodied Emissions Inventory [RP].xlsx`

---

## Inventory Structure

The workbook has five sheets:

| Sheet | Purpose |
|---|---|
| **KS Equipment** | Capital equipment at Kansas (Fort Lupton) production facility |
| **LA Equipment** | Capital equipment at Louisiana injection site |
| **Items Sold + Moved/Rentals Returned** | Equipment removed from active inventory |
| **Amortization** | Total GWP pool, lifetime throughput projection, amortized rate |
| **[RP] Amortization** | Period-specific amortization: rate × period gross removals = EE |

---

## LCA Method Hierarchy

Apply in this order — use the first method that has sufficient data:

1. **Material EFs (preferred)** — determine item material composition (mass + material type) and apply GREET/ICE emission factors per the 2026 Standard EF CSV
2. **Manufacturer LCA** — if manufacturer provides a verified LCA document, use their reported GWP directly
3. **NAICS Supply Chain EF (last resort)** — apply the relevant NAICS cost-based EF × purchase price (2022 USD) if neither material data nor manufacturer LCA is available

---

## Material Emission Factors (2026)

**Per-material detail (formulas, worked examples, weight sourcing):** `workflows/lca_materials/`

From `Standard Emission Factors + Calculations - 2026.csv`:

| Material | EF | Unit | Source |
|---|---|---|---|
| Steel (virgin, stamped) | 2.818 | MTCO2e/T | GREET 2025 |
| Stainless Steel | 0.720746 | MTCO2e/T | GREET 2024 |
| Rubber | 3.372324 | MTCO2e/T | GREET 2024 |
| HDPE | 1.702514 | MTCO2e/T | GREET 2024 |
| LDPE | 1.980563 | MTCO2e/T | GREET 2024 |
| Concrete (ready-mix) | 0.086234 | MTCO2e/T | GREET 2024 |
| Liquid Caustic Soda (50% NaOH) | 0.9535517371 | MTCO2e/T | GREET 2024 |
| Aluminum (North America cradle-to-gate) | 5.65 | kgCO2e/kg | ICE Database 4.0 |
| Limestone | 8.179 | kgCO2e/T | GREET 2025 |

**Rule:** Always reference these from the Standard EF CSV via cell formula — never hardcode in the calc doc.

---

## Step 1: New Equipment — Quantify GWP

### Trigger: Invoice received from procurement

1. Identify the item from the invoice (name, model, quantity)
2. Determine whether it's a **KS** or **LA** item based on delivery address / ops team confirmation
3. Determine material composition:
   - Check manufacturer spec sheet or SDS for material type and weight
   - If a single dominant material (e.g., steel tank): `GWP = mass (kg) × EF (kgCO2e/kg)`
   - If mixed materials: apply each material EF proportionally by mass
4. If material data is unavailable, check whether a manufacturer LCA document exists
5. If neither: apply NAICS cost-based EF (see Step 1b below)
6. **Create the LCA doc:** Save a PDF or DOCX showing the calculation:
   - Item name, model, source document (SDS / spec sheet / invoice)
   - Mass breakdown by material
   - EF applied (cite 2026 Standard EF CSV)
   - Resulting GWP (kgCO2e)
   - File in: `[RP]\Site Emissions\Embodied Emissions\Documentation\`

### Step 1b: NAICS Cost-Based (last resort only)

1. Identify the most specific applicable NAICS code for the item
2. Look up the NAICS Supply Chain EF (kgCO2e/2022 USD) from the Standard EF CSV
3. Always convert invoice price to 2022 USD using the BLS PPI deflator — required regardless of purchase year
4. `GWP = price (2022 USD) × NAICS EF (kgCO2e/USD)`
5. Document the NAICS code, conversion, and result in the LCA doc

---

## Step 2: Add to Inventory

Once GWP is determined:

1. Open the relevant equipment sheet (KS or LA)
2. Add a new row:

| Column | Content |
|---|---|
| Equipment Name | Descriptive name matching the invoice |
| Manufacturer | From invoice |
| Make/Model | From invoice |
| LCA Doc | Filename of the LCA doc saved in Documentation\ |
| Unit GWP | kgCO2e per unit (from Step 1) |
| Number of Units | From invoice |
| Total GWP | = Unit GWP × Number of Units (formula, not hardcoded) |

3. Verify the total GWP pool on the Amortization sheet updates correctly (it should sum the Total GWP column)

---

## Step 3: Equipment Received on Site

When ops team confirms equipment is received:

1. Cross-check against the invoice entry already in the inventory
2. Confirm quantity matches
3. If there's a discrepancy (e.g., 2 units invoiced, 1 received), update Number of Units to reflect what was actually received and note the discrepancy
4. No separate action needed if quantities match

---

## Step 4: Update Amortization

After any inventory change (add or remove):

1. Go to the **Amortization** sheet
2. Verify the total pool (sum of all active GWP) has updated
3. The amortization rate = `pool (kg CO2e) ÷ lifetime gross removals projection (MT CO2e)` — the denominator is **hardcoded** in the sheet; do not change it without explicit direction from Garrett
4. Go to the **[RP] Amortization** sheet for the current period
5. Confirm: `Period EE = amortization rate (kgCO2e/MT) × period gross removals (MT CO2e)`
6. The period gross removals come from the batch CI data (Phase 2a output)

---

## Step 5: Item Sold, Moved, or Returned

**Trigger:** Procurement team sends a sold item invoice or Garrett is notified of a move/return

1. Find the item in KS or LA Equipment sheet
2. Cut the row and paste into **Items Sold + Moved/Rentals Returned** sheet
3. Add a "Status" column entry: `Sold`, `Move to [location]`, or `Rental (giving back)`
4. Record the `CO2e Unamortized` value — this is carried forward for tracking but removed from the active pool
5. The total pool on Amortization sheet will decrease automatically
6. Recalculate the amortization rate for the current and all future periods

---

## SP&C (Spare Parts & Consumables)

**File:** `Basco Inj Operations SP+C Inventory [RP].xlsx`

SP&C uses the NAICS cost-based approach for all items (small consumables typically lack material LCAs).

**When to recalculate:** Any time the inventory changes — both when a new part type is added AND when an existing item is reordered (quantity or cost change). Otherwise static between periods.

**Calculation:**
- Each item: `kg CO2e/week = Unit Cost (2022 USD) × NAICS EF (kgCO2e/USD) × qty/week`
- Sum all items → total kg CO2e/week
- Multiply by **number of weeks in the reporting period** → period SP&C EE
- Period length varies, so this value changes each RP even when inventory is unchanged

**NAICS EF source:** Standard EF CSV, "Embodied Emissions -- NAICS Supply Chain Emissions Factors" rows. Match item to most specific applicable NAICS code.

---

## Output of This Workflow

- Updated GWP value per new item (kgCO2e)
- Updated amortization rate
- Period embodied EE (kgCO2e) for the current RP
- LCA documentation file saved to Documentation\

Feeds into: [[phase2b_injection_emissions]] (Site Emissions, Embodied Emissions category)

---

## Confirmed Conventions

- **Material EFs always preferred** over NAICS cost-based — only use NAICS if no material data and no manufacturer LCA exists
- **LCA doc required for every new capital item** — filename goes in the "LCA Doc" column
- **Amortization denominator is hardcoded** — do not change the lifetime throughput projection without explicit instruction
- **Sold items are rare** — always triggered by a procurement invoice, not by ops team reports alone
- **KS vs LA distinction matters** — each site has its own equipment sheet; do not mix them

## LCA Doc Format
- Format is ad hoc per item — Garrett will walk through each new item type as it comes in.

## CSV Mirror Convention

Whenever an `.xlsx` inventory file is created or updated, also export each sheet as a CSV in the same directory:
- `LA Equipment.csv`, `KS Equipment.csv`, `Amortization.csv`, `[RP] Amortization.csv`
- Use `openpyxl` with `data_only=True` to resolve formulas to their cached values
- This lets Claude read inventory data directly via the Read tool without needing Python

## Open Questions
- [ ] None remaining.
