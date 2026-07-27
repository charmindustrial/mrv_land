# Site Emissions QA Checklist — Item-by-Item Reference

Per-category specification for site emissions QA: what to check, which primary source to open, what values to extract into the source-read log, expected ranges, and common failure modes. This file is read during the Pre-Flight Gate and is the operational map for Gate 2 work.

**Scope:** All site-level emissions for a Charm Industrial bio-oil injection RP — diesel, gasoline, methanol, argon, electricity, brine, support travel, embodied (CapEx + sitework + SP&C), railcar cleaning & transport, waste disposal, additional transport, plus conditional categories (pump oil, LCS, production / inventory reconciliation, one-offs). Cross-cutting: BCU/REC offsets, EF validation.

**Source-read log key convention:** Citations follow the pattern `[log:category.evidence_files.<file>.extracted_values.<field>]` or `[log:category.derived.<computation>]`. Multi-source citations are comma-separated inside one tag. See SKILL.md Citation Discipline (Rule 1) for the full grammar.

---

## Phase Mode Applicability

| Section | Phase 1 (Pre-Certify) | Phase 2 (Post-Certify) | Full |
|---|---|---|---|
| 1. Drive folder inventory | Required | Reused from Phase 1 log | Required |
| 2. Per-category Layer 3 (Drive ↔ calc sheet) | Required | Reused | Required |
| 3. Per-category Layer 1 (Certify component value) | Pending | Required | Required |
| 4. Per-category Layer 2 (Certify-attached evidence) | Pending | Required | Required |
| 5. BCU Quant internal math (sheet self-consistency) | Required | Reused | Required |
| 6. BCU Quant → Certify Reductions reconciliation | Pending | Required | Required |
| 7. REC kWh-to-kWh consumption check (Drive-side) | Required | Reused | Required |
| 8. REC procurement / EAC inventory verification | Pending | Required | Required |
| 9. Multi-scapegoat allocation across removals | Pending | Required | Required |
| 10. EF validation against Standard EF Sheet 2026 tab | Required | Reused | Required |

`Pending` rows in Phase 1 must carry a `[log:KEY]` to the calc-sheet authoritative value preserved for Phase 2 comparison.

---

## Section 1: Diesel

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 1.1 | Diesel calc sheet present and singular | Drive > Diesel folder | calc sheet xlsx, no `_bak` duplicate | `_bak` left in folder, period mismatch in filename |
| 1.2 | Every receipt PDF opened and matched to calc sheet row | Drive > Diesel > Receipts | per receipt: vendor, station, date, gallons, transaction ID, product grade | Filename matched but PDF unopened (Anti-Pattern 6) |
| 1.3 | Calc sheet TOTAL CO2e formula traced | Calc sheet formula cell | formula text, constituent inputs, dimensional check (units cancel) | Surface read of output cell (Anti-Pattern 8) |
| 1.4 | Diesel volume-to-mass conversion correct | Calc sheet | density used (kg/gal), per-row math | EF (3.87 kgCO2e/kg) applied as if per-gallon — diesel ~3.2× understatement (Apr 2026 Basco) |
| 1.5 | Diesel EF matches Standard EF Sheet 2026 tab | Standard EF Sheet, Diesel row | value 3.87 kgCO2e/kg fuel, source GLEC V3.2 2025 | Wrong EF year tab |
| 1.6 | Diesel delivery transport (process + embodied), if applicable | Calc sheet, distance evidence | mass, distance, EF, both process and embodied components | Embodied erroneously offset by BCUs |
| 1.7 | Calc-sheet output reconciles to BCU Quant | BCU Quant sheet, Site Diesel Emissions row | BCU Quant value matches calc sheet output | Calc-sheet revision drifted from BCU Quant |
| 1.8 | Diesel column labels include units | Calc sheet headers | each header read verbatim with unit | Units missing on Gallons / Price / kg columns |

**MANDATORY VERIFICATION SUB-TASKS:**
- **Receipt-by-receipt** (sub-task 1 of Gate 2): open every PDF in Receipts subfolder, extract gallons + transaction ID, sum and compare to calc-sheet `Total Delivered (gal)`.
- **Formula trace** (sub-task — Calc Sheet Surface Read): open the Total CO2e formula cell, record the formula and the constituent input cells.
- **EF read** (sub-task 5 of Gate 2): open Standard EF Sheet 2026 tab, Diesel row, record cell + value + source.

**`[log:KEY]` examples:**
- `[log:diesel.evidence_files.0.extracted_values.gallons]`
- `[log:diesel.derived.total_gal_sum, diesel.derived.density_kg_per_gal, diesel.derived.ef_kg_per_kg, diesel.derived.recomputed_total_kg_co2e]`
- `[log:standard_ef_sheet_reads.diesel_wtw.value]`

**Verifier reference:** VR Sec 2.5.5

---

## Section 2: Gasoline

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 2.1 | Every receipt PDF opened and matched | Drive > Gasoline > Receipts | per receipt: vendor, date, gallons, transaction ID, **product grade (Unleaded Regular / Plus / Premium)** | Sample of one (Anti-Pattern 7) — Apr 2026 caught Unleaded Plus mixed with Regular only when all 5 receipts opened |
| 2.2 | Calc sheet math: gal × density × EF | Calc sheet formula cell | density 2.76335 kg/gal (Measurement Canada), EF 3.74 kgCO2e/kg, total CO2e | Density step skipped |
| 2.3 | Gasoline EF matches Standard EF Sheet 2026 tab | Standard EF Sheet | 3.74 kgCO2e/kg fuel, GLEC V3.2 2025 | Wrong year tab |
| 2.4 | No transport emissions for gasoline | Calc sheet | absence of transport rows | Transport erroneously included |
| 2.5 | No BCU offset applied to gasoline (gasoline is NEVER BCU-eligible) | BCU Quant + Certify Reductions (Phase 2) | gasoline absent from BCU offsets | BCU erroneously applied |
| 2.6 | Calc-sheet output reconciles to BCU Quant | BCU Quant sheet | match | Drift |

**MANDATORY VERIFICATION SUB-TASKS:** Receipt-by-receipt; EF read.

**`[log:KEY]` examples:**
- `[log:gasoline.evidence_files.4.extracted_values.product_grade]`
- `[log:gasoline.derived.recomputed_total_kg_co2e, bcu_quant_sheet.gasoline_total_kg]`

---

## Section 3: Methanol

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 3.1 | Methanol receipts present | Drive > Methanol > Receipts | per receipt: vendor, date, quantity (gal or kg), transaction ID | N/A possible — mark N/A if no methanol activity |
| 3.2 | Consumption emissions correct | Calc sheet | qty × Methanol EF (1.398801 kgCO2e/gal per Standard EF Sheet 2026 tab) | EF not validated |
| 3.3 | Transport emissions correct (process + embodied) | Calc sheet, distance evidence | mass, distance, flatbed truck process EF, non-tanker embodied EF | Embodied erroneously offset by BCUs |
| 3.4 | Distance evidence in folder for transport | Drive > Methanol > Distances or equivalent | PNG with origin, destination, distance — extract values | Filename matched but PNG unopened (Anti-Pattern 6) |
| 3.5 | BCU offset applied to transport process only | BCU Quant + Certify Reductions (Phase 2) | process portion offset, consumption + embodied NOT offset | BCU on consumption / embodied |

**`[log:KEY]` examples:**
- `[log:methanol.evidence_files.distance_png.extracted_values.distance_mi]`
- `[log:standard_ef_sheet_reads.methanol.value]`

---

## Section 4: Argon

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 4.1 | Argon receipts present (cylinder rentals EXCLUDED) | Drive > Argon > Receipts | only consumption invoices, no rental-only invoices | Cylinder rentals included (no emissions burden) |
| 4.2 | Three sub-components present: transport process, transport embodied, electricity | Calc sheet | each sub-component's mass / distance / kWh + EF + emissions | Only one or two sub-components |
| 4.3 | Transport distance evidence | Drive > Argon > Distances | PNG, distance value | Filename match only |
| 4.4 | Argon electricity not double-counted with site electricity | Calc sheet, electricity sheet | argon kWh attributed to argon, not to site | Double-counting |
| 4.5 | RECs offset argon electricity | Calc sheet, BCU Quant | REC kWh = consumed kWh for argon ops | Mismatch |
| 4.6 | BCUs applied only to transport process (not embodied, not electricity) | BCU Quant | correct allocation | BCU on embodied or electricity |

---

## Section 5: Electricity

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 5.1 | Utility readout dates match RP exactly | Drive > Electricity > utility xlsx | meter #, account #, period start, period end, daily kWh values for every day in RP | Partial period or extra days |
| 5.2 | Total kWh sum correct | Utility readout, summed | sum of daily kWh = stated total | Sum miscomputed |
| 5.3 | EF applied — LA grid or LA Solar RECs | Calc sheet, Standard EF Sheet 2026 tab | grid 0.0004630140342 MTCO2e/kWh OR REC 0.00003664154577 MTCO2e/kWh (LA Solar) | Wrong region or vintage |
| 5.4 | REC kWh = consumed kWh (kWh-to-kWh match) | Calc sheet | total kWh consumed = REC kWh offset | Mismatch |
| 5.5 | REC procurement evidence (if available) | Drive > Electricity | EAC certificate / broker confirmation | Procurement-side may not be visible — focus on kWh match |
| 5.6 | Calc-sheet output reconciles to BCU Quant | BCU Quant | match | Drift |

**`[log:KEY]` examples:**
- `[log:electricity.evidence_files.utility_xlsx.extracted_values.total_kwh, electricity.derived.recomputed_kg_co2e]`
- `[log:standard_ef_sheet_reads.la_solar_recs.value]`

---

## Section 6: Brine

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 6.1 | Volume evidence: totalizer or invoices | Drive > Brine > Receipts or totalizer | invoice or totalizer reading with volume (bbl / gal / L), date, vendor (Bourque) | Wrong vendor name (Borque vs Bourque) |
| 6.2 | If invoices: cross-check with Jula's copies | Drive folder + Jula's copies | invoice count match | Missing invoice |
| 6.3 | Volume math (bbl → gal → L → kg) | Calc sheet | 42 gal/bbl, 3.78541 L/gal, brine density | Wrong density |
| 6.4 | Distance evidence for brine transport | Drive > Brine > Distances or equivalent | PNG with origin (Bourque, Duson LA), destination (Basco), distance | Distance evidence missing (Apr 2026 Basco) |
| 6.5 | Transport process EF + embodied EF | Standard EF Sheet 2026 tab | flatbed truck process 0.0001384 MTCO2e/t-mi; non-tanker embodied 0.0001927908256 MTCO2e/mi | Wrong EF |
| 6.6 | BCU offset applied to transport process only | BCU Quant | process offset, embodied NOT offset | BCU on embodied |
| 6.7 | Calc-sheet output reconciles to BCU Quant (process + embodied separately) | BCU Quant | match both | Lumped together |

**MANDATORY VERIFICATION SUB-TASK:** Distance evidence verification (sub-task 2 of Gate 2): open distance PNG, extract distance.

---

## Section 7: Support Travel

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 7.1 | All trips for the RP listed | Calc sheet | per trip: employee, dates, origin airport, destination airport, lodging city, leg distances (mi), trip days | Missing trip |
| 7.2 | Air emissions per trip | Calc sheet, source PNG | DEN→DFW→BTR RT = 453 kg CO2e (Apr 2026 reference) — open the source PNG to verify the value | PNG unopened |
| 7.3 | Driving math (Airport ↔ Lodging) | Calc sheet | distance / 24.4 mpg × 2.76335 kg/gal × 0.00374 MTCO2e/kg | Wrong density or EF |
| 7.4 | Driving math (Lodging ↔ Site) | Calc sheet | trip days × daily RT mileage × ... | Days × mileage error |
| 7.5 | Distance evidence for every active route | Drive > Support Travel | PNGs for Alexandria↔Basco, BTR↔Alexandria, DEN→BTR (active in Apr 2026) | All PNGs missing (Apr 2026 Basco — FAIL) |
| 7.6 | Total reconciles to BCU Quant | BCU Quant | match | Drift |
| 7.7 | NO BCU applied to Support Travel (NEVER BCU-eligible — SAF + gasoline, not diesel) | BCU Quant + Certify Reductions (Phase 2) | absent | BCU erroneously applied |

**MANDATORY VERIFICATION SUB-TASK:** Distance evidence verification.

---

## Section 8: Embodied — CapEx

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 8.1 | CE Inventory updated for current operations | CapEx xlsx | full equipment list, total pool size MT | Missing newly-added equipment |
| 8.2 | LCA docx opened for every item added this RP | Drive > Embodied > Documentation | weight (kg), EF (with units + source year), GWP calculation | Filename only "Pass" (Apr 2026 — Failure Category 13) |
| 8.3 | EF unit interpretation consistent across LCAs | LCAs | "MTCO2e/T Steel" treated identically (per metric tonne, GREET convention) | Inconsistent interpretation (Apr 2026 Kerry Tank vs Catch Tank) |
| 8.4 | All EFs sourced from Standard EF Sheet | Standard EF Sheet 2026 tab | every cited EF appears on the sheet | Off-list ecoinvent EF (Apr 2026 — Triton Shaker, 60kW Generator) |
| 8.5 | Pool size = sum of line items | CapEx xlsx | sum reconciles | Sum drift |
| 8.6 | Penalty/MT formula uses GROSS removals (not net) | CapEx xlsx | pool ÷ 5y_gross_removals = penalty/MT | Net used instead of gross |
| 8.7 | RP penalty = penalty/MT × RP gross removals | CapEx xlsx | reconciles | Wrong period removals |
| 8.8 | Calc-sheet RP penalty matches BCU Quant CapEx value | BCU Quant | match | Drift (Apr 2026 — 60 kg gap from stale BCU sheet) |
| 8.9 | Rental equipment treatment documented | LCA + invoice | full unit GWP rationale OR pro-rated | Methodology unstated (Apr 2026 — generator/shaker/catch tank rented 2 days, added at full unit GWP) |

**MANDATORY VERIFICATION SUB-TASKS:** LCA documentation verification (sub-task 3 of Gate 2); EF read.

---

## Section 9: Embodied — Sitework

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 9.1 | All materials and processes documented | Sitework calc sheet, supporting invoices | per item: date, equipment, hours/qty, fuel rate, GWP | Missing materials |
| 9.2 | All EFs cited and sourced | Sitework calc sheet | EFs with year + source attribution | EF not cited |
| 9.3 | All assumptions and constants documented | Sitework calc sheet | gallons/hour, mpg, density, etc. | Constant not sourced |
| 9.4 | Diesel emissions broken out from non-diesel | Sitework calc sheet | separate totals | Lumped |
| 9.5 | Diesel portion reported as RP component (BCU-eligible) | BCU Quant | diesel total appears | Missing |
| 9.6 | Non-diesel remainder added to CapEx Inventory for amortization | CapEx xlsx | row matching this RP's sitework non-diesel | Not yet added |
| 9.7 | Activity dates within RP | Calc sheet | every row's date in RP window | March-dated activity in April RP (Apr 2026) |
| 9.8 | Distance evidence for transport rows | Drive > Sitework > Distances | every PNG opened, distance extracted | Filename match only (Apr 2026 — Douglas Tank 1,729 mi vs PNG 1,759 mi) |
| 9.9 | Excavator / equipment model identified by vendor | Vendor invoice | model + fuel rate from manufacturer source | Model assumed, no vendor confirmation (Apr 2026 — JC Construction) |
| 9.10 | Site address consistent across documents | Invoices, distance maps | single canonical Basco well site address | 4687 vs 4675 LA-115 inconsistency (Apr 2026) |

**MANDATORY VERIFICATION SUB-TASKS:** Distance evidence verification (every PNG opened); EF read.

---

## Section 10: Embodied — SP&C

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 10.1 | Equipment list current | SP&C xlsx | all parts and consumables active for current operations | Outdated list |
| 10.2 | Per-item formula: cost × NAICS factor × qty / replacement weeks | SP&C xlsx | each row's components | Math error |
| 10.3 | Total weekly penalty reconciles | SP&C xlsx | sum of per-item weekly penalties | Sum drift |
| 10.4 | RP penalty scaling explicit | SP&C xlsx | weekly × weeks_in_RP OR per-RP formula stated | Weekly mistaken for RP value (Apr 2026 — potential 4-5× understatement) |
| 10.5 | NAICS factors current (1.4.0, 2024 USD basis) | Standard EF Sheet 2026 tab | every cited NAICS row matches | Stale NAICS version |
| 10.6 | Calc-sheet output matches BCU Quant SP&C value | BCU Quant | match | Drift |

---

## Section 11: Railcar Cleaning & Transport

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 11.1 | Calc sheet has no formula errors (#NAME?, #REF!) | Railcar xlsx | every formula cell evaluated | Sheet shipped with #NAME? errors (Apr 2026 — Failure 8 from March pattern) |
| 11.2 | Trip details: railcar, origin, destination, miles, dates | Calc sheet | per trip: GPRX number, origin/destination, mi | Missing trip |
| 11.3 | Distance evidence in folder | Drive > Railcar > Receipts (or Distances) | PNG / email screenshot — opened, distance extracted | Filename match only |
| 11.4 | Rail distance evidence: email IS authoritative per KB §3 | Per KB | email/written confirmation from rail logistics provider acceptable; no Google Maps required | Wrong-flag "lower-rigor" on email evidence (Apr 2026 — caught at second pass) |
| 11.5 | Process EF + embodied EF (per KB §6) | Standard EF Sheet 2026 tab | rail process 0.0000259104 MTCO2e/T-mi; railcar embodied 0.0000311307 MTCO2e/mi | Wrong vintage |
| 11.6 | Calc-sheet output matches BCU Quant Railcar Movement (diesel + non-diesel split) | BCU Quant | match | Drift |
| 11.7 | BCU eligibility documented for unloaded vs loaded movements | Calc sheet | rationale stated | Unloaded movement BCU ambiguity (Apr 2026) |

---

## Section 12: Waste Disposal

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 12.1 | Disposal documentation present | Drive > Waste Disposal | calc sheet + Manifests subfolder with ticket(s) | Missing manifest |
| 12.2 | Actual disposal ticket opened (not just calc sheet) | Manifest PDF/PNG | ticket #, date, gross/tare/net weight (or 00 lb if unweighed), material classification, transport vendor, customer code, disposal facility address | Calc sheet read without opening ticket (Apr 2026 — Failure Category 14) |
| 12.3 | Material classification on ticket matches calc-sheet treatment | Ticket vs calc sheet | ticket "C&D" should not be calc-sheet "Bio-Oil Contaminated Gravel" without rationale | Mismatch (Apr 2026 — caught only at second pass) |
| 12.4 | Mass derivation methodology stated (scale ticket OR volume × density) | Calc sheet | one method consistently applied | Two tables with different mass values (9.135 MT vs 9.063 MT in Apr 2026) |
| 12.5 | Activity date within RP | Ticket | date in RP window | March-dated activity in April RP (Apr 2026) |
| 12.6 | Distance evidence | Drive > Waste Disposal > Manifests | PNG opened, distance + facility address extracted | Filename match; city label wrong (Apr 2026 — Crowley vs Carencro) |
| 12.7 | Three components computed: transport process, transport embodied, disposal | Calc sheet | each present | Component missing |
| 12.8 | Disposal EF correct for material type | Standard EF Sheet 2026 tab | bio-oil contaminated gravel landfill EF 0.000259 (or appropriate alternative) | Wrong EF |
| 12.9 | Upstream emissions for bio-oil portion (if applicable) | Calc sheet | included with rationale, OR explicitly excluded with rationale | Methodology silent (Apr 2026) |
| 12.10 | Waste Disposal present in BCU Quant sheet | BCU Quant | row exists with diesel/non-diesel split | **MISSING from BCU Quant entirely** (Apr 2026 — substantive FAIL) |

**MANDATORY VERIFICATION SUB-TASK:** Manifest / scale ticket verification (sub-task 4 of Gate 2).

---

## Section 13: Additional Transport

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 13.1 | Distance evidence for every route | Drive > category folder | PNG opened | Filename match only |
| 13.2 | Mass + distance inputs to calc sheet | Calc sheet | per trip | Missing |
| 13.3 | Fuel type identified (determines BCU eligibility) | Calc sheet | diesel vs non-diesel | Assumed |
| 13.4 | Process emissions BCU-eligible if diesel; embodied NEVER eligible | BCU Quant | correct allocation | BCU on embodied |

---

## Section 14: Pump Oil (Conditional)

If no pump oil purchased this RP → Mark N/A with note. Otherwise: same receipt-based pattern as Diesel/Gasoline (open every receipt, extract values, calc-sheet math, EF validation).

---

## Section 15: LCS (Conditional)

Currently dormant per KB. Mark N/A unless reactivated. If active: same pattern as Methanol (consumption + transport + EF).

---

## Section 16: Production / Inventory Reconciliation (Annual)

Annual rollup, not present in monthly RP folders. Mark N/A unless this is the annual RP.

---

## Section 17: One-Off / Nonstandard

If named subfolders present (e.g., "KS Decomm", "Methanol Flush"): per-event documentation, methodology, EFs sourced, assumptions documented.

---

## Section 18: BCU/REC Offsets

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 18.1 | BCU Quant sheet present and current for RP | Drive root | sheet exists, dated correctly | Stale or missing |
| 18.2 | Internal sum check (Phase 1) | BCU Quant | sum of all components, diesel/non-diesel split | Sum drift |
| 18.3 | Every BCU-eligible site emission category present in BCU Quant | BCU Quant + skill U3 list | full coverage of: Site Diesel, Diesel Delivery Process, Brine Process, Methanol Process, Argon Process, Railcar Process, Waste Disposal Process, additional diesel transport | Missing category (Apr 2026 — Waste Disposal absent) |
| 18.4 | BCU Quant → Certify Reductions reconciliation (Phase 2) | BCU Quant + Certify Reductions tab | every BCU application traces to a quant-sheet line, totals reconcile | Trace gap |
| 18.5 | NO BCU applied to ineligible components | BCU Quant + Certify Reductions (Phase 2) | gasoline / support travel / embodied / electricity all absent from BCU offsets | BCU applied to ineligible (critical FAIL) |
| 18.6 | REC kWh = consumed kWh | Calc sheet | match | Mismatch |

---

## Section 19: EF Validation

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 19.1 | Standard EF Sheet 2026 tab confirmed | EF Sheet | tab name "2026 / GLEC V3.2 2025 / GREET 2025" | Wrong year tab — invalidates every EF check |
| 19.2 | Every EF cited in any calc sheet → recorded in `standard_ef_sheet_reads` | EF Sheet | full list, no sampling | EF cited without log entry |
| 19.3 | Per-EF spot check: cell, value, units, source | EF Sheet | each EF cross-referenced | Wrong row read |

**Verifier reference:** VR Appendix 1, VR Sec 2.5.5

---

## Section 20: Multi-Scapegoat Allocation (if applicable)

| Item | Check | Primary Source | Expected Extracted Values | Common Failure |
|------|-------|---------------|---------------------------|----------------|
| 20.1 | Total site emissions = sum across scapegoats | Certify (Phase 2) | total reconciles | Drift |
| 20.2 | No removal net-emissive | Certify Calculation View (Phase 2) | sequestrations - activities + reductions > 0 for each | Net-emissive |
| 20.3 | Allocation logic stated and reasonable | Calc sheet or methodology memo | rationale documented | Arbitrary split |

---

## Output Format

The checklist xlsx columns:
- **A:** Checklist Item
- **B:** Status (Pass / Fail / Flag / N/A / Pending)
- **C:** Evidence Notes (specific values + `[log:KEY]` citation)
- **D:** Certify Component (or "Pending Certify entry" in Phase 1)
- **E:** Verifier Reference
- **F:** Phase Resolved

File naming: `Site_Emissions_QA_[Site]_[RP].xlsx` (same file across phases — do not produce a Phase 2 file).

---

## Working Up

This file is reference material; the operational reads happen in Gate 1 (source-read log) and Gate 2 (per-category sub-tasks). The audit script (`scripts/audit_checklist.py`) enforces the citation discipline structurally — see SKILL.md Citation Discipline section for invocation.
