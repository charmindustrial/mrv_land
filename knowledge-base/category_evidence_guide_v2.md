# Site Emissions Category Evidence Guide

Detailed evidence requirements, calculation logic, common failure modes, and Certify component mapping for each site emission category. The QA agent should read this file at the start of every site emissions QA session.

## IMPORTANT: Universal Requirements Apply to Every Category

Before reviewing any individual category below, remember that the Universal Cross-Cutting Requirements in SKILL.md (U1–U8) apply to ALL categories. For every category you review:

- **U1 — Units:** Read every column header and labeled cell in the calc sheet. Report which have units and which don't.
- **U2 — Distance evidence:** If the category involves transport, verify distance evidence exists in the Drive folder. Missing distance evidence = FAIL.
- **U3 — BCU cross-check:** If the category has BCU-eligible emissions, cross-check against the BCU Quant sheet. The BCU-eligible components are: diesel consumption, diesel delivery transport process, brine transport process, methanol transport process, argon transport process, railcar transport process, waste disposal transport process, and any additional diesel-fueled transport process.
- **U4 — Missing evidence = FAIL:** Never classify missing evidence as FLAG. If you can't independently confirm a value, it's a FAIL.
- **U5 — Certify match:** The Certify component value must exactly match the evidence. Any mismatch = FAIL.
- **U6 — Naming consistency:** Check that folder names, sheet names, and Certify component names are traceable.
- **U7 — Correct EF year tab:** Confirm you're reading from the correct year tab in the Standard EF Sheet before citing any EF.
- **U8 — Output standards:** Report your own findings with specific values. Never write "verify X" — do it and report what you found.

These are not repeated in every category section below to avoid redundancy, but they must be checked for every category.

## Table of Contents

1. [Diesel](#1-diesel)
2. [Gasoline](#2-gasoline)
3. [Methanol](#3-methanol)
4. [Argon](#4-argon)
5. [Electricity](#5-electricity)
6. [Brine](#6-brine)
7. [Support Travel](#7-support-travel)
8. [Embodied Emissions — CapEx](#8-embodied-emissions--capex)
9. [Embodied Emissions — Sitework](#9-embodied-emissions--sitework)
10. [Embodied Emissions — SP&C](#10-embodied-emissions--spc)
11. [Railcar Cleaning & Transport](#11-railcar-cleaning--transport)
12. [Waste Disposal](#12-waste-disposal)
13. [Additional Transport](#13-additional-transport)
14. [Pump Oil](#14-pump-oil-conditional)
15. [LCS](#15-lcs-conditional)
16. [Production / Inventory Reconciliation](#16-production--inventory-reconciliation-conditional)
17. [One-Off / Nonstandard Emissions](#17-one-off--nonstandard-emissions)
18. [BCU/REC Offsets](#18-bcurec-offsets)
19. [Emission Factor Validation](#19-emission-factor-validation)

---

## 1. Diesel

**Drive subfolder:** `Diesel`

**Evidence required:**
- All fuel receipts/invoices for the reporting period
- Calculation spreadsheet aggregating receipts into total mass consumed (fuel EFs are denominated in kg CO₂e per kg fuel — calc sheets include standard volume-to-mass conversions)
- Emission factor source documentation

**Calc logic:**
- Fuel emission factors are computed in terms of mass: kg CO₂e / kg fuel
- Calc sheets convert volume (gallons) to mass using standard density, then apply EF
- Total mass consumed × diesel EF (kg CO₂e/kg) = total diesel site emissions
- Diesel delivery transport has separate process and embodied components
- Check: receipt count matches calc sheet entries
- Check: sum of receipt volumes matches calc sheet total
- Check: volume-to-mass conversion is correct
- Check: EF matches current-year Standard Emission Factors list

**Certify components:**
- "Diesel Site Emissions" or "B6 Injection site diesel emissions" (in Removal Activities > Bio-oil injection)
- May also have diesel delivery transport components: "B6 Injection Diesel Delivery - Transport Process Emissions" and "B6 Diesel Delivery - Tanker Truck Embodied Emissions"

**BCU offset:** Diesel consumption emissions AND delivery transport process emissions are offset by BCUs. Delivery transport embodied emissions are NOT BCU-eligible (they are not actual emissions from diesel combustion). Verify BCU reduction component exists in Certify Reductions and matches BCU Quant sheet.

**Common failure modes:**
- Missing receipts (receipt count in folder ≠ entries in calc sheet)
- Calc sheet includes receipts from outside the reporting period
- Wrong EF vintage (using prior year's factor)
- Volume-to-mass conversion error
- BCU offset applied to delivery embodied emissions (ineligible)
- BCU offset not matching the diesel + delivery process emission values

**Checklist items:**
1. All receipts accounted for in Diesel subfolder
2. All receipts accounted for in calc sheet
3. Correct math in calc sheet (volume-to-mass conversion, EF application)
4. EF matches Standard Emission Factors list for current year
5. Diesel delivery transport distance and mass correct (if applicable)
6. Diesel delivery transport process emissions correct (if applicable)
7. Diesel delivery transport embodied emissions correct and NOT offset by BCUs
8. Certify component value matches calc sheet output
9. BCU offset correctly applied to eligible components only (consumption + delivery process)

---

## 2. Gasoline

**Drive subfolder:** `Gasoline`

**Evidence required:**
- All fuel receipts for the reporting period
- Calculation spreadsheet (uses volume-to-mass conversion, same as diesel)

**Calc logic:**
- Same mass-based EF approach as diesel: volume → mass → mass × EF = emissions
- Calc sheets include standard volume-to-mass conversions
- Same receipt-to-calc-sheet reconciliation pattern as diesel
- **Gasoline has NO transport emissions** — it is picked up by the vehicle that uses it (delivered in the same gas tank that goes to get it)

**Certify components:**
- "B6 Injection site gasoline emissions" (in Removal Activities > Bio-oil injection)

**BCU offset:** **NEVER.** Gasoline is NOT diesel and is NOT eligible for BCU offset. BCUs are exclusively for diesel-based emissions. If you see BCUs applied to gasoline, that is a FAIL — an erroneous reduction that corrupts the CDR calculation.

**Common failure modes:**
- Receipt gaps, wrong EF, math errors (same pattern as diesel)
- Volume-to-mass conversion error
- BCUs erroneously applied to gasoline (this would be a critical FAIL)
- Transport emissions erroneously included (gasoline has none)

**Checklist items:**
1. All receipts accounted for in Gasoline subfolder
2. All receipts accounted for in calc sheet
3. Correct math in calc sheet (volume-to-mass conversion, EF application)
4. EF matches Standard Emission Factors list
5. No transport emissions included (gasoline is self-delivered)
6. No BCU offset applied (gasoline is NEVER BCU-eligible)
7. Certify component value matches calc sheet output

---

## 3. Methanol

**Drive subfolder:** `Methanol`

**Evidence required:**
- Purchase receipts/invoices
- Calculation spreadsheet with consumption and transport emissions
- Transport distance evidence (route screenshot or documentation)

**Calc logic:**
- Methanol has BOTH consumption emissions AND transport emissions
- Consumption: quantity × methanol EF = consumption emissions
- Transport: mass × distance × transport EF = transport emissions
- Total methanol emissions = consumption + transport

**Certify components:**
- "Methanol Emissions" (in Removal Activities > Bio-oil injection)

**BCU offset:** Methanol is delivered by truck, so transport process emissions ONLY may be offset with BCUs. Transport embodied emissions and consumption emissions are NOT BCU-eligible.

**Common failure modes:**
- Missing transport distance documentation
- Transport mass doesn't match purchase quantity
- Transport emissions calculated separately from consumption but both rolled into one Certify component
- BCUs applied to consumption or embodied emissions (only transport process is eligible)
- Typo: "Transport emissoins" appears in historical checklists — don't let spelling errors mask real issues

**Checklist items:**
1. All receipts accounted for in Methanol subfolder
2. All receipts accounted for in calc sheet
3. Consumption emissions recomputed (quantity × methanol EF — cite inputs and result)
4. Transport distance documented (evidence in folder)
5. Transport mass correct (matches purchase quantity × density)
6. Transport process emissions recomputed (mass × distance × process EF — cite inputs and result)
7. Transport embodied emissions recomputed (distance × embodied EF — cite inputs and result)
8. All EFs match Standard Emission Factors list (consumption EF, transport process EF, transport embodied EF)
9. Total rollup verified (consumption + transport process + transport embodied = calc sheet total)
10. Certify component value matches calc sheet total

---

## 4. Argon

**Drive subfolder:** `Argon`

**Evidence required:**
- Purchase receipts (exclude cylinder rental invoices — no emissions burden)
- Calculation spreadsheet with consumption, transport, and electricity components
- Transport distance evidence

**Calc logic:**
- Argon has THREE emission sub-components:
  1. Transport process emissions: mass × distance × process EF
  2. Transport embodied emissions: mass × distance × embodied EF
  3. Electricity usage for argon operations (often offset by RECs)
- Cylinder rental invoices have NO emissions burden — should not be in calc sheet

**Certify components:**
- "Argon Emissions" (main consumption/process)
- "Argon Transport Process Emissions"
- "Argon Transport - Embodied Emissions"
- "Argon Electricity Usage (RECs)" (may be in activities and/or reductions)

**BCU offset:** BCUs offset delivery transport process emissions ONLY. RECs offset argon electricity, which is the sole emissive input (electricity is the only energy consumed in argon operations). Transport embodied emissions are NOT BCU-eligible.

**Common failure modes:**
- Including cylinder rental invoices in emissions calc (these are financial, not physical)
- Missing one of the three sub-components
- Transport distance or mass incorrect
- Argon electricity not separated from site electricity
- BCUs applied to transport embodied or electricity (only transport process is eligible for BCUs; electricity uses RECs)

**Checklist items:**
1. All receipts accounted for in Argon subfolder (cylinder rentals excluded)
2. All receipts accounted for in calc sheet
3. Production electricity recomputed (argon mass × ASU kWh/kg × electricity EF — cite inputs and result; note grid vs RECs EF)
4. Transport distance documented (evidence in folder)
5. Transport mass correct (CF → kg conversion chain documented)
6. Transport process emissions recomputed (mass × distance × process EF — cite inputs and result)
7. Transport embodied emissions recomputed (distance × embodied EF — cite inputs and result)
8. All EFs match Standard Emission Factors list (ASU kWh/kg source, grid EF, RECs EF, transport process EF, transport embodied EF)
9. Total rollup verified (production + transport process + transport embodied = calc sheet total)
10. Certify component values match calc sheet outputs (all sub-components — clarify which Certify components are additive vs overlapping)

---

## 5. Electricity

**Drive subfolder:** `Electricity`

**Evidence required:**
- Utility bill/readout for the reporting period
- REC procurement documentation (if applicable)

**Calc logic:**
- Total kWh for RP × applicable emission factor = electricity emissions
- **Important nuance on RECs:** RECs do not simply subtract from a gross number. Instead, for each kWh offset by a REC, the generator emission factor is swapped from the grid EF to the renewable generator's emission profile. This is a substitution, not a subtraction. The result is the same (near-zero emissions for offset kWh), but the mechanism matters for verification.
- All grid-region and REC emission factors are included in the Standard Emission Factors list, updated annually
- Date range on utility readout must match RP dates exactly

**Certify components:**
- "Basco Site Electricity Use (RECs)" or "B6 Injection site electricity emissions (RECs applied)"

**REC offset:** Yes — electricity is offset by RECs. Verify that the REC offset quantity in kWh matches the consumed electricity in kWh for all relevant components.

**Common failure modes:**
- Utility readout dates don't cover full RP (partial period)
- Utility readout includes dates outside RP
- Wrong grid EF or REC generator EF (region or vintage mismatch)
- REC kWh ≠ consumed electricity kWh
- Argon electricity counted here AND in argon category (double-counting)

**Checklist items:**
1. Dates covered by utility readout match RP dates
2. Total kWh includes all dates in period
3. Grid emission factor correct (GLEC NA or regional, source documented)
4. REC offset applied and documented (if applicable)
5. Net electricity emissions correctly calculated
6. No double-counting with argon electricity
7. Certify component value matches calc output

---

## 6. Brine

**Drive subfolder:** `Brine`

**What brine is:** Waste brine is brought to the Basco site for use as a flush fluid to clear injection equipment. It is NOT waste disposal — it is an input material with associated transport emissions.

**Evidence required:**
- Volume records: either totalizer values OR invoices from Borque
- If invoices: cross-check with copies sent by Jula to ensure all invoices received from Borque are present
- Transport distance evidence

**Calc logic:**
- Because brine is a waste product, only transport emissions are accounted for (no production/embodied emissions for the brine itself)
- Transport emissions are scaled per gallon of brine delivered
- Brine is sourced from two sites and the vendor does not trace which delivery comes from where, so an **average distance** is used — this average is defined in the Standard Emission Factors sheet
- All brine calc inputs (average distance, per-gallon EFs) are in the Standard Emission Factors sheet
- Process and embodied transport emissions must be computed separately even though both are denominated per gallon — this is because process emissions are BCU-eligible but embodied are not
- Two methods for volume: totalizer readings or invoice aggregation

**Certify components:**
- "B6 Injection site water emissions - Transport process emissions"
- "B6 Injection site water emissions - transport embodied emissions"
- Or: "BCU's - Brine Transport Emissions" (in Reductions, if BCU applied to process emissions)

**BCU offset:** Transport process emissions ONLY are BCU-eligible. Embodied emissions are not.

**Common failure modes:**
- Totalizer values that don't make sense (sanity check against historical periods)
- Invoice count mismatch (Borque sent 5 but only 2 in folder — cross-check with Jula's copies)
- Invoice volumes don't sum to calc sheet total
- Missing either process or embodied transport component
- Confusing brine with waste disposal — brine is an input flush fluid, not waste

**Checklist items:**
1. If totalizer values used: total makes sense (sanity check)
2. If invoices used: cross-check with Jula's copies — all Borque invoices present
3. If invoices used: total reflects sum of invoiced volumes
4. Transport distance correct and documented
5. Transport process emissions correctly calculated
6. Transport embodied emissions correctly calculated
7. EFs match Standard Emission Factors list
8. Certify component values match calc outputs (both process and embodied)
9. BCU offset applied if applicable (check BCU Quant sheet)

---

## 7. Support Travel

**Drive subfolder:** `Support Travel`

**Evidence required:**
- Calculation spreadsheet listing all trips in the reporting period
- Each trip: origin, destination, legs, distances, mode of transport
- Distance evidence (route screenshots, maps)

**Calc logic:**
- For each trip: distance × transport EF = trip emissions
- Sum of all trip emissions = total support travel emissions
- Multi-leg trips: sum distances per leg

**Certify components:**
- "Support Travel" (single component, often the largest site emission)

**BCU offset:** **NEVER.** Support travel uses SAF (sustainable aviation fuel) for air travel and gasoline for passenger car travel. Neither fuel is diesel, so BCUs do not apply. If you see BCUs applied to support travel, that is a FAIL.

**Common failure modes:**
- Missing trips (trip not in calc sheet that occurred during RP)
- Wrong distances (particularly multi-leg trips)
- Wrong transport mode EF (driving vs flying, SAF vs gasoline)
- Support travel can be very large (18+ tCO₂e in complex periods) — verify carefully
- BCUs erroneously applied (support travel is never BCU-eligible)

**Checklist items:**
1. All trips in the reporting period included in calc sheet
2. Legs and distances correct for each trip
3. Correct transport mode EF applied per leg
4. Correct sum of emissions for period
5. Distance evidence present for each route
6. Certify component value matches calc sheet total

---

## 8. Embodied Emissions — CapEx

**Drive subfolder:** `Embodied Emissions` (CapEx section)

**Evidence required:**
- CE (Capital Equipment) Inventory spreadsheet — fully updated
- LCA sheets for each line item (only new items will have LCA docs in the current RP's documentation — existing items' LCA docs are linked but filed in prior periods)
- Amortization schedule

**Calc logic:**
- Each capital item has an LCA sheet computing its GWP (Global Warming Potential)
- Line item GWP = LCA sheet value × unit count
- Amortization pool = sum of all current line item GWPs
- **Amortization factor = pool / amortization period / GROSS removals for RP** (not net — this is a common error)
- Emission penalty = amortization factor × gross removal

**Sitework → CapEx flow (important):** Sitework projects feed into CapEx through a specific process:
1. Sitework emissions are summed in a calc sheet based on contractor billing and/or estimates
2. The calc sheet breaks out **diesel emissions within the sitework** from **non-diesel emissions**
3. **Diesel emissions** from sitework are reported as a separate component in the RP they were incurred, so they can be offset with BCUs
4. **Non-diesel emissions** (the remainder) are added to the Embodied Emissions inventory to be amortized over time
5. In these cases, the sitework calc sheet and supporting documentation also serve as the LCA documentation for the non-diesel remainder

**Certify components:**
- "B6 Injection - Embodied Emissions" or "B6 Injection - Capital Embodied Emissions"

**Common failure modes:**
- CE Inventory not updated with new equipment or new sitework
- LCA sheet GWP × unit count ≠ line item in inventory
- Amortization pool doesn't sum correctly
- **Factor computed using net removals instead of gross** (must use gross)
- Sitework non-diesel remainder not added to inventory
- Sitework diesel portion not broken out for separate RP reporting/BCU offset
- LCA docs not linked for line items

**Checklist items:**
1. CE Inventory fully updated for current operations
2. LCA sheets completed for each line item (new items have docs in current RP, existing items linked)
3. Line item GWP matches LCA sheet × unit count
4. Amortization pool matches sum of current GWPs
5. Amortization factor computed using GROSS removals (not net)
6. Emission penalty properly computed
7. Any new sitework: non-diesel remainder added to inventory for amortization
8. Any new sitework: diesel portion broken out for separate RP reporting and BCU offset
9. Certify component value matches computed penalty

---

## 9. Embodied Emissions — Sitework

**Drive subfolder:** `Site Ops` or named subfolder (e.g., "February Basco Sitework")

**Important:** Sitework emissions are NOT independent of CapEx. See the Sitework → CapEx flow described in Section 8 above. The key distinction:
- **Diesel emissions within sitework** → reported as a component in the current RP (BCU-eligible)
- **Non-diesel emissions** → added to CapEx inventory for amortization (the calc sheet + supporting docs serve as LCA documentation)

**Evidence required:**
- Documentation of all materials and processes (contractor billing, estimates)
- Emissions calculation with cited EFs and assumptions
- Clear breakout of diesel vs. non-diesel emissions in the calc sheet
- Evidence that non-diesel remainder was added to CapEx Inventory

**Calc logic:**
1. Sum all sitework emissions from contractor billing/estimates
2. Break out diesel emissions from non-diesel emissions
3. Diesel emissions → reported in current RP as separate component (BCU-eligible)
4. Non-diesel emissions → added to Embodied Emissions inventory for amortization
5. Non-diesel portion netted against the RP in which sitework was completed

**Certify components:**
- "LA Sitework" or site-specific name (for the RP-reported portion)

**Common failure modes:**
- Missing materials or processes from the emissions calc
- EFs not cited or sourced
- Assumptions/constants not documented
- Diesel not broken out from non-diesel
- Non-diesel remainder not added to CapEx Inventory
- Diesel portion not reported as separate BCU-eligible component

**Checklist items:**
1. All materials and processes documented
2. All materials and processes included in emissions calc
3. All emission factors cited and sourced
4. All assumptions and/or constants cited and sourced
5. Diesel emissions clearly broken out from non-diesel in calc sheet
6. Diesel portion reported as RP component (BCU-eligible)
7. Non-diesel remainder added to CapEx Inventory for amortization
8. Non-diesel emissions netted against RP completed
9. All project emissions summed properly
10. Certify component value matches computed total

---

## 10. Embodied Emissions — SP&C

**Drive subfolder:** Within `Embodied Emissions` (SP&C section)

**Evidence required:**
- Equipment list for current operations
- Weekly and RP penalty calculations

**Calc logic:**
- Equipment list defines what spare parts and consumables are needed for ongoing operations
- Weekly penalty computed from equipment replacement cycles and GWP values
- RP penalty = weekly penalty × weeks in RP

**Certify components:**
- "Spare Parts and Consumables LA" or "B6 Injection - SP&C Emissions"

**Common failure modes:**
- Equipment list outdated (not reflecting current operations)
- Missing data or erroneous data in equipment list
- Weekly penalty computation error
- RP penalty doesn't match weeks × weekly rate

**Checklist items:**
1. Equipment list is up to date for current operations
2. Weekly and RP penalties computed properly
3. Certify component value matches computed RP penalty

---

## 11. Railcar Cleaning & Transport

**Drive subfolder:** `Railcar`

**Evidence required:**
- Route distance evidence (screenshots, maps) for all relevant routes
- Calculation spreadsheet with mass, distance, and emissions
- BCU separation documentation

**Calc logic:**
- Railcar cleaning emissions from cleaning activities
- Transport: mass × distance × EF for each leg
- Rail transport may have multiple legs (truck > rail > truck)
- BCUs may be separated — some legs offset, some not (e.g., "2nd Leg No BCU")

**Certify components:**
- "Railcar Cleaning and Transport" or "Railcar Cleaning + Transport"
- May have BCU-separated variants: "Railcar Cleaning and Transport 2nd Leg (No BCU)"
- "Railcar Movement"

**BCU offset:** Rail transport **process emissions ONLY** get BCUs. Embodied emissions and cleaning emissions are NOT BCU-eligible. Some legs may be offset and others not (e.g., "2nd Leg No BCU"). Check BCU Quant sheet carefully.

**Common failure modes:**
- Missing route distance evidence
- BCU separation not correctly reflected in Certify (wrong legs offset)
- BCUs applied to embodied emissions or cleaning (only process is eligible)
- Mass or distance input errors in calc sheet
- Multi-leg routing not properly decomposed
- Cleaning emissions incorrectly computed

**Checklist items:**
1. All relevant route distances have evidence in folder
2. All mass and distance inputs in calc sheet with evidence
3. Emissions correctly computed per leg
4. BCUs separated on the sheet and correctly input into Certify
5. Certify component value(s) match calc sheet
6. BCU offset amounts match BCU Quant sheet

---

## 12. Waste Disposal

**Drive subfolder:** Within `Site Ops` or dedicated `Waste Disposal` subfolder

**Evidence required:**
- Documentation for all disposals during the RP
- Routing distance evidence for each destination (may be more than one destination per event)
- Calculation spreadsheet detailing each disposal event
- For bio-oil disposals: upstream emission documentation (production CI, transport to last point of residence)

**Calc logic — THIS IS MORE COMPLEX THAN OTHER CATEGORIES:**

Each disposal event includes up to three emission components:

**Component 1: Transport emissions (always present)**
- Emissions from transporting waste from generation point to disposal destination
- A single disposal event may involve more than one destination/distance
- Computed as normal transport emissions:
  - Process: Mass × Distance × Transport Process EF → **BCU-eligible**
  - Embodied: Distance × Transport Embodied EF → **NOT BCU-eligible**

**Component 2: Disposal emissions (always present)**
- Emissions from the act of disposal itself
- There are multiple different disposal emission factors — the correct one must be chosen based on the physical nature of the disposal method
- Computed as: Mass × Disposal EF
- **NOT BCU-eligible**

**Component 3: Upstream emissions (conditional — applies when disposing of bio-oil or bio-oil-contaminated product)**
- When bio-oil is disposed of (e.g., spill, material deterioration in a rail car), the upstream emissions must be accounted for because the oil never becomes part of an injection batch (where those emissions would normally be counted)
- Upstream emissions include:
  1. Bio-oil production emissions (computed using the relevant production CI)
  2. Bio-oil transport to the last point of residence before disposal (computed like normal batch transport)
- These are computed the same way as normal batch upstream emissions, but they accrue to the disposal site emission rather than to a batch
- **This is often the largest component of disposal emissions when it applies**
- Almost always required when bio-oil itself is disposed of (spills, deteriorated material)
- Not all disposal events require upstream emissions (e.g., disposing of contaminated water or debris does not)

**Total disposal emissions = transport + disposal + upstream (if applicable)**

Can be VERY large in some periods (40+ tCO₂e observed). Large values may require splitting across multiple scapegoats.

**Certify components:**
- "B6 Injection site waste disposal emissions"

**Common failure modes:**
- Missing disposal documentation
- New routing distances not evidenced
- Wrong disposal EF chosen (must match physical nature of disposal method)
- Missing upstream emissions on bio-oil disposal (this is often the largest component and easy to overlook)
- Upstream CI not matching the production period's actual CI
- Upstream transport distance not matching actual route to last point of residence
- Calc sheet doesn't account for all disposal events or all three components
- Transport process vs. embodied not separated (needed for BCU eligibility)
- Large values not properly split across scapegoats

**Checklist items:**
1. Documentation for all disposals present in evidence folder
2. Documentation for all routing distances present (may be multiple destinations)
3. All disposal events accounted for in calc sheet
4. Per event — Transport process emissions correct (Mass × Distance × EF) — BCU-eligible
5. Per event — Transport embodied emissions correct (Distance × EF) — NOT BCU-eligible
6. Per event — Disposal EF correctly chosen for physical disposal method
7. Per event — Disposal emissions correct (Mass × Disposal EF)
8. Per event — Upstream emissions included if bio-oil or bio-oil-contaminated material disposed
9. If upstream: production CI matches relevant production period
10. If upstream: transport to last point of residence correctly computed
11. All EFs match Standard Emission Factors list
12. Total disposal emissions = transport + disposal + upstream (where applicable)
13. Certify component value matches calc sheet total

---

## 13. Additional Transport

**Drive subfolder:** May be within `Support Travel` or dedicated subfolder

**Evidence required:**
- Route distance evidence
- Mass and distance inputs with evidence
- BCU documentation if applicable

**Calc logic:**
- Same pattern as other transport: mass × distance × EF
- Process and embodied computed separately
- BCU eligibility depends on the transport type — only diesel-fueled transport process emissions are BCU-eligible. Verify the fuel type before assuming BCU applicability.

**Certify components:**
- Various — may be named by specific transport activity

**Common failure modes:**
- BCUs applied to ineligible transport (non-diesel fuel, or embodied emissions)
- Missing route distance evidence

**Checklist items:**
1. All relevant route distances have evidence in folder
2. All mass and distance input into calc sheet with evidence
3. Transport fuel type identified (determines BCU eligibility)
4. If diesel-fueled: process emissions BCU-eligible; embodied NOT eligible
5. If non-diesel-fueled: NO BCU eligibility
6. BCUs separated and correctly input into Certify (if applicable)
7. Certify component value matches calc sheet

---

## 14. Pump Oil (Conditional)

**Drive subfolder:** Dedicated subfolder when applicable

**Evidence required:**
- Purchase receipts
- Calculation spreadsheet

**Calc logic:**
- Same receipt-to-calc pattern as diesel/gasoline
- Logged as a consumable when purchased (infrequent)

**Certify components:**
- Named component when present

**Status:** Mark N/A if no pump oil purchased this RP.

**Checklist items:**
1. All receipts accounted for in folder (or confirmed no purchase this RP → N/A)
2. All receipts accounted for in calc sheet
3. Correct math in calc sheet

---

## 15. LCS (Conditional)

**Drive subfolder:** Dedicated subfolder when applicable

**Evidence required:**
- Purchase receipts
- Calculation spreadsheet with consumption and transport
- Transport distance evidence

**Calc logic:**
- Same pattern as methanol (consumption + transport)
- Currently dormant but historically used and may return

**Certify components:**
- Named component when present

**Status:** Mark N/A if LCS not part of current process.

**Checklist items:**
1. All receipts accounted for in folder (or confirmed not in use → N/A)
2. All receipts accounted for in calc sheet
3. Correct math in calc sheet
4. Transport distance correct
5. Transport mass correct
6. Transport emissions correct

---

## 16. Production / Inventory Reconciliation (Conditional)

**Drive subfolder:** Root-level file (e.g., "RP Summary Inventory Reconciliation.xlsx")

**Note:** Production reconciliation and inventory reconciliation are the same process. This happens annually and is specific to Charm bio-oil production (the Charm WODO/Aqueous batch QA agent will eventually own the production side, but the reconciliation emission accrues to site emissions).

**Evidence required:**
- Reconciliation spreadsheet (root-level file in the site emissions folder)
- Carbon intensity for each production period and oil type
- Production vs. shipment comparison

**Calc logic:**
- Reconciles Charm bio-oil production emissions across oil types and production periods
- Outstanding oil quantities identified from production vs. shipment comparison
- CI per production period × outstanding oil quantity = reconciliation emission
- For production periods with exhausted inventory: reconciliation emission computed
- Reconciliation emissions included in site total

**Certify components:**
- "Inventory Reconciliation" or rolled into other components

**Common failure modes:**
- Wrong CI applied to a production period
- Outstanding quantities incorrectly computed
- Missing reconciliation for exhausted inventory periods

**Checklist items:**
1. Reconciliation documentation present
2. Outstanding oil quantities correctly identified from production vs. shipment comparison
3. Carbon intensity for each production period and oil type correctly applied
4. For exhausted inventory periods: reconciliation emission computed
5. Reconciliation emissions correctly included in site total
6. Certify component value matches computed reconciliation (if dedicated component)

---

## 17. One-Off / Nonstandard Emissions

**Drive subfolder:** Named subfolders specific to the activity (e.g., "KS Decomm", "Methanol Flush", "Opelousas Cleanup")

**Evidence required:**
- Case-by-case documentation of the activity
- Quantification methodology with cited EFs and assumptions
- Supporting calculation spreadsheets

**Calc logic:**
- No standard formula — each one-off is quantified based on its specific activity
- Must have transparent methodology, sourced EFs, and documented assumptions
- Lump sum entries must have supporting quantification spreadsheets

**Certify components:**
- Named by activity (e.g., "KS Decommissioning Activity", "Opelousas Cleanup Operations")

**Common failure modes:**
- Insufficient documentation of methodology
- EFs not sourced
- Assumptions not documented or not conservative
- Large values (can be 4-7+ tCO₂e) without proportionate evidence depth

**Checklist items:**
1. Activity documentation present in dedicated subfolder
2. Quantification methodology clearly documented
3. All emission factors cited and sourced
4. All assumptions and constants documented
5. Calculations correct
6. Certify component value matches quantification output
7. If lump sum: supporting quantification spreadsheet present

---

## 18. BCU/REC Offsets

**Drive evidence:** BCU Quant sheet (root-level file, e.g., "Feb-Mar RP BCU Quant.xlsx")

**Scope note:** This section covers only BCUs/RECs applied to site emission components. Batch-specific BCUs (e.g., BCUs applied to bio-oil transport process emissions) are in scope for the batch QA agent.

**CRITICAL — BCU eligibility rule:** Only **transport process emissions from diesel-fueled transport** are BCU-eligible. This means:
- Diesel site consumption → BCU-eligible
- Diesel delivery transport process → BCU-eligible
- Brine transport process → BCU-eligible
- Railcar transport process → BCU-eligible (specific legs only)
- Methanol transport process → BCU-eligible (delivered by truck)
- Waste disposal transport process → BCU-eligible
- Argon transport process → BCU-eligible

**NEVER BCU-eligible:**
- ANY embodied transport emissions (regardless of fuel)
- Gasoline emissions (not diesel)
- Support travel (SAF and gasoline, not diesel)
- Electricity (uses RECs, not BCUs)
- Disposal emissions (the disposal act itself)
- Cleaning emissions

**There is no automated guardrail in Certify or elsewhere that prevents applying BCUs to ineligible components.** An erroneous BCU reduction that slips through will corrupt the overall CDR calculation. Be very careful.

**What to verify:**
- BCU Quant sheet is present and current for this RP
- Every site-emission BCU application in Certify Reductions traces to a specific line in the quant sheet
- Reconcile quantities against the BCU Quant sheet — **note that Certify Reductions totals will NOT exactly match quant sheet site-emission totals because Certify doesn't differentiate between BCUs applied to injection batches vs. site emissions.** You must trace line-by-line rather than relying on totals.
- BCU quantities are allocated correctly across eligible site emission categories only
- No BCUs applied to ineligible components (check every single one)
- REC offset value in kWh matches consumed electricity kWh for all relevant components (you may not have visibility into procurement records — focus on the kWh-to-kWh match)
- EAC (Energy Attribute Certificate) inventory sheet is updated

**Certify Reductions structure (typical):**
- Under "Bio-oil injection": "BCUs - Applied to injection site emissions", "BCUs - Applied to injection site diesel emissions"
- Under "Bio-oil transport": "BCUs - Applied to Bio-Oil Transport Process Emissions" (this is a batch BCU — out of scope for this agent)
- Additional BCU components as needed per period

**Common failure modes:**
- **BCUs applied to ineligible components** — most dangerous failure mode, corrupts CDR calculation
- BCU quant sheet line items don't trace to Certify reduction components
- Mixing up batch BCUs with site emission BCUs
- Missing BCU for a site emission category that should be offset
- REC kWh offset ≠ consumed electricity kWh
- EAC inventory not updated

**Checklist items:**
1. BCU Quant sheet present for this RP
2. Every Certify BCU reduction component traces to quant sheet line
3. Quant sheet totals match Certify Reductions totals
4. BCU allocation across categories is correct
5. REC offset kWh matches consumed electricity kWh for all relevant components
6. EAC inventory sheet updated

---

## 19. Emission Factor Validation

**Reference:** Standard Emission Factors list for current year (in Drive or Certify)

**What to verify:**
- Check EVERY emission factor used across EVERY category — no sampling, no spot-checking
- Each EF must match the Standard Emission Factors list for the current year
- Note the vintage/source of each validated EF
- Flag any EFs that appear outdated or don't match the standard list
- An incorrect EF propagates through every calculation it touches, so this check is exhaustive by design

**Verifier reference:** VR Appendix 1, VR Sec 2.5.5

**Checklist items:**
1. Standard Emission Factors spreadsheet present and version-controlled for current year
2. Diesel EF matches current year standard
3. Gasoline EF matches current year standard
4. Methanol EF matches current year standard
5. Argon EF matches current year standard
6. Electricity grid EF matches current year standard (GLEC NA or regional)
7. Brine transport EFs (process + embodied) match current year standard
8. Support travel EFs match current year standard (per transport mode)
9. Waste disposal EF matches current year standard
10. Railcar transport EFs match current year standard
11. All other category-specific EFs validated against standard list
12. ALL EFs current for the RP (note any pending updates per FAR)
