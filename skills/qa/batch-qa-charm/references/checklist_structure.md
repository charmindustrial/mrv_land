# Charm WODO/Aqueous Injection Batch QA Checklist — Item-by-Item Reference

This document is the complete specification for every checklist item in a Charm-produced bio-oil injection batch QA: what to check, which primary source to open, what values to extract, expected ranges, and common failure modes.

The checklist applies Max's actual QA question framework for Charm-produced batches (WODO and Aqueous). Section 9 (LCS) is Aqueous-only; render it as N/A for WODO batches.

**Certify reads are API reads, never a browser.** "Certify <X> component → INPUTS → <field>" means that component's input row in `certify_removal_summary.md` (from `certify_read.py removal`), cited by its JSON path; the ± uncertainty is the input's `standard_deviation`. "→ linked sources" means the datapoint's source links and the dump's `sources` list. Per-component tCO2e is not in the API: compute it from the component's blueprint (`blueprints` in the full dump) and inputs, and reconcile the total to `removal.co2e_net_removed_kg`. Removal-level sources not linked to any datapoint are not visible via the API: a document absent from Certify and Drive is graded Fail as before, with the note "absent from Drive and the Certify API dump; confirm on the Sources tab (removal-level sources are not visible via the API)".

## Columns

- **A:** Item number
- **B:** Question (verbatim from Max's framework)
- **C:** Status (Pass / Fail / Flag / N/A)
- **D:** Evidence / Finding — specific values from specific sources, with `[log:KEY]` citation
- **E:** Reference (Isometric protocol section, Charm sheet name, or other anchor)

## Status fills

- PASS: no fill (default white)
- FAIL: red fill across all columns
- FLAG: yellow fill `#FFF2CC` across all columns, dark gold font `#996600`
- N/A: gray italic, no fill
- Section / sub-section headers: `#D6E4F0` (light blue), one neutral color, never yellow, never green, never a second tone

---

## SECTION 1 — Batch Folder (3 items)

### 1.1 Is there testing in the testing folder for the batch?

- **Primary source:** Drive folder → `Testing/` subfolder
- **What to extract:** lab report filenames, certificate IDs, Carbon %, Hydrogen %, Nitrogen %, density (if reported), viscosity (if reported), acid number (if reported)
- **Pass criteria:** at least one lab report covering the batch is present and the report contains carbon content for the relevant fraction(s)
- **Fail mode:** Testing folder empty, or lab report missing carbon content
- **Flag mode:** lab report present but filename non-descriptive

### 1.2 Are Ops Notes in the folder and fully completed?

- **Primary source:** Drive folder → Ops Notes Google Sheet
- **What to extract:** oil type, per-tote rows (tag, gross, tare, fraction, PP), Total Mass Transported, Total Oil Produced, Total Oil in Batch, uncertainty, LCS use (Aqueous), completion date, reviewer initials (if Ops convention includes them)
- **Pass criteria:** Ops Notes opens, every per-tote row is populated (no blanks for tag/gross/tare/fraction/PP), and every summary cell at the bottom (Total Mass Transported / Total Oil Produced / Total Oil in Batch / uncertainty) is populated with a value, not a formula error
- **Fail mode:** Ops Notes missing, blank per-tote rows, missing summary totals, formula errors visible
- **Flag mode:** present and populated but missing optional metadata (sample date, scale ID) — note as hygiene

### 1.3 Is the Bio-Oil Shipment Tracker in the batch folder and fully completed?

- **Primary source:** Drive folder → Bio-Oil Shipment Tracker (per-RP tab)
- **What to extract:** RP tote roster (tag, fraction, gross, PP, batch assignment), per-truck rows (N totes, mileage), computed RP Share / Allocated Miles / Batch Mileage Allocation cells (FORMULAS, not values)
- **Pass criteria:** Shipment Tracker exists in the batch folder, the per-RP tab covers the batch, every tote assigned to this batch appears with full metadata, computed cells are formulas
- **Fail mode:** Tracker missing, RP tab missing, totes missing from tracker, computed cells are hard-coded constants (defer item 3.3 for the explicit auditability check; 1.3 fails on completeness, 3.3 fails on auditability)
- **Flag mode:** tracker present but minor metadata gaps

---

## SECTION 2 — Ops Notes (4 items)

### 2.1 Is the "Total Mass Transported" value correctly computed as the sum of the gross weight of all totes?

- **Primary source:** Ops Notes — summary row + per-tote rows
- **Math:** Total Mass Transported (cell value) =? Σ Gross (across all per-tote rows)
- **What to extract:** reported Total Mass Transported, sum of per-tote Gross values, delta
- **Pass criteria:** delta ≤ 1 kg (rounding tolerance) AND the summary cell is a SUM formula referencing the per-tote Gross column (not a typed constant)
- **Fail mode:** delta > 1 kg, or summary cell is a hard-coded constant
- **Flag mode:** delta within tolerance but summary cell formula references the wrong range (e.g., misses a tote row at the bottom)

### 2.2 Is the "Total Oil Produced" value correctly computed as the sum of the net weight of oil in tote for all totes (gross − tare per tote)?

- **Primary source:** Ops Notes — summary row + per-tote Net-in-tote column
- **Math:** Total Oil Produced (cell value) =? Σ (Gross − Tare) across all per-tote rows
- **What to extract:** reported Total Oil Produced, sum of per-tote (Gross − Tare), delta. Spot-check 3 totes' Net-in-tote = Gross − Tare individually.
- **Pass criteria:** delta ≤ 1 kg AND per-tote Net-in-tote formula = Gross_cell − Tare_cell
- **Fail mode:** delta > 1 kg, or per-tote Net is hard-coded, or Net formula uses wrong columns
- **Flag mode:** within tolerance but minor sheet hygiene issues

### 2.3 Is the "Total Oil in Batch" value correctly computed?

**WODO branch:**
- **Math:** Total Oil in Batch =? Σ (Net-in-tote − Standard Loss) across all per-tote rows
- **What to extract:** Standard Loss value per tote, formula in the per-tote Net-in-injection-batch column
- **Pass criteria:** formula = Net-in-tote − Standard_Loss; delta ≤ 1 kg
- **Fail mode:** Standard Loss not applied; delta > 1 kg; constant value substituted for formula
- **Custody rule (2026-09-29):** upstream emissions of all oil in Charm custody are netted against removals. Production and transport emissions must be charged on the mass that entered custody on each leg, not only on the offloaded or injected mass; any lost mass (railcar loss, spill, standard loss, R&D removal) whose upstream emissions are not charged is a Fail, with the missing tCO2e computed.

**Aqueous branch:**
- **Math:** Total Oil in Batch =? Σ (Measured Pre-Unload − Measured Post-Unload) across all per-tote rows. **Standard Loss does NOT apply.**
- **What to extract:** pre-unload and post-unload measurement columns, per-tote loss values
- **Pass criteria:** formula uses measured pre/post values, not Standard Loss; delta ≤ 1 kg
- **Fail mode:** Standard Loss applied to Aqueous (wrong methodology); pre/post measurements absent or hard-coded

### 2.4 Is uncertainty correctly computed as 2.5 lb per tote, summed across totes, converted to kg?

- **Primary source:** Ops Notes uncertainty cell + per-tote count
- **Math:** Reported uncertainty (kg) =? (2.5 × N_totes) / 2.20462 ≈ 1.134 × N_totes kg
- **What to extract:** reported uncertainty, N_totes, computed expected value, delta
- **Pass criteria:** reported = computed expected (±0.01 kg)
- **Fail mode:** uncertainty value uses different per-tote spec (e.g., 0.5 lb), wrong N, wrong conversion factor, or constant unrelated to per-tote count
- **Common AECN-confusion check:** 72.57 kg per truck (rail-truck per-leg precision) is AECN, not Charm. Don't confuse the two. Charm uses 1.134 kg per tote.

---

## SECTION 3 — Bio-Oil Shipment Tracker (5 items)

### 3.1 Are totes for the RP correctly identified?

- **Primary source:** Bio-Oil Shipment Tracker — RP tab
- **What to extract:** RP tote roster (every tote tagged for the RP), cross-check against Ops Notes per-tote roster
- **Pass criteria:** every tote in Ops Notes for this batch's RP appears in the RP tab of the Tracker
- **Fail mode:** missing totes; misassigned totes from a different RP

### 3.2 Do all totes identified for RP match the Ops Notes for the applicable batch?

- **Primary source:** Shipment Tracker RP tab + Ops Notes per-tote rows
- **What to extract:** tote-by-tote match on: tag #, fraction, gross mass, production period
- **Pass criteria:** 100% match across all four attributes per tote
- **Fail mode:** any mismatch on tag / fraction / gross / PP

### 3.3 Are computed outputs (RP Share of Truck, RP Allocated Miles, Batch Mileage Allocation) auditable formulas rather than hard-coded values?

- **Primary source:** Shipment Tracker computed cells
- **Verification method:** read EACH computed cell with `drive_read.py rows`; its `formula` field must show a `=...` formula referencing tote counts and mileage inputs. A constant value (e.g., `0.5`, `545.0`) FAILs.
- **Pass criteria:** all three computed-cell types are formulas; formulas reference the expected inputs
- **Fail mode:** any of the three is a hard-coded constant — **auditability FAIL** (verifier cannot reconstruct without the formula)
- **Note:** record the formula text verbatim in the source-read log for the audit trail

### 3.4 Are computed outputs computed correctly?

- **Math (verify in each formula and reproduce independently):**
  - RP Share of Truck = N_totes_in_RP / N_totes_on_Truck
  - RP Allocated Miles = Mileage(one-way) × RP Share of Truck
  - Batch Mileage Allocation = (N_totes_in_Batch / N_totes_on_Truck(s)) × Mileage(one-way)
- **Pass criteria:** formula matches the spec; computed value reproduces the spec independently
- **Fail mode:** formula uses round-trip mileage instead of one-way, wrong denominator (truck capacity instead of N_totes_on_Truck), wrong allocation fraction
- **Common confusion check:** Process EFs use one-way distance × mass; Embodied EFs use one-way distance (no round-trip doubling for Charm-truck Process). Distance doubling applies only in specific Embodied scenarios where the truck round-trips for one customer — does NOT apply to Charm's per-batch Shipment Tracker (per workspace memory `feedback_process_vs_embodied_distance_doubling.md`).

### 3.5 Do the totes assigned to each batch match the Ops Notes on (a) tag, (b) fraction, (c) gross mass, (d) production period?

- This is the per-attribute verification underlying 3.2; render as a single Pass/Fail with sub-bullet evidence in column D listing any per-tote mismatches.
- **Pass criteria:** all four attributes match for every tote
- **Fail mode:** any mismatch on any attribute

---

## SECTION 4 — Certify Injection Sequestration (4 items)

### 4.1 Does the C content in the testing match the C content in the Sequestration component?

- **Primary source:** Testing lab report (Carbon %) + Certify Sequestration component → Datapoints → Carbon Content
- **What to extract:** lab C%, Certify C%, delta
- **Pass criteria:** values match to the precision Certify displays (typically 0.01% absolute)
- **Fail mode:** delta > 0.01% absolute; Certify shows a different value than the lab report
- **For multi-fraction batches (WODO + Aqueous in one injection):** the C content in the Sequestration is the weighted average — verify the weighting math

### 4.2 Is the C content properly evidenced (test copy + Ops Notes copy)?

- **Primary source:** Certify Sequestration component → linked sources (Certify API dump: datapoint source links + `sources` list)
- **What to extract:** filenames of attached evidence; confirm both (a) the lab report and (b) the Ops Notes appear as Sources for the C Content datapoint
- **Pass criteria:** both evidence types present and linked to the Carbon Content datapoint
- **Fail mode:** missing test copy, missing Ops Notes copy, or evidence linked at component level but not to the specific datapoint

### 4.3 Does the Mass of Product measurement uncertainty match the uncertainty value in Ops Notes?

- **Primary source:** Certify Sequestration component → INPUTS → Mass of Product uncertainty field; Ops Notes uncertainty value
- **Math:** Certify Mass-of-Product uncertainty =? Ops Notes uncertainty (1.134 × N_totes kg)
- **Pass criteria:** values match (±0.01 kg)
- **Fail mode:** mismatch; or uncertainty entered as percentage rather than absolute value

### 4.4 Does the C content have the appropriately computed 0.4% relative uncertainty?

- **Primary source:** Certify Sequestration component → INPUTS → Carbon Content uncertainty field
- **Math:** Expected uncertainty = 0.004 × reported C% (absolute, in same units as the C% datapoint)
- **Pass criteria:** Certify value = expected (±0.001 absolute or ±0.1% relative)
- **Fail mode:** value entered as 0.4 absolute (instead of 0.4%); value missing; wrong base

---

## SECTION 5 — Certify Transport Process Emissions (5 items)

### 5.1 Does the Transport Process emission use the correct and up-to-date Flatbed Truck emission factor?

- **Primary source:** Standard EFs sheet (2026 tab, column F) + Certify Transport Process component → INPUTS → Emission Factor
- **What to extract:** Standard EFs Flatbed Truck Process value, Certify EF value
- **Pass criteria:** values match in native units (Certify may display rounded)
- **Fail mode:** Certify uses a different EF than current 2026 tab; EF from prior year still in use
- **CRITICAL:** Don't use Certify's displayed EF for the math; pull full precision from Standard EFs sheet.

### 5.2 Is the Transport Process distance value correct and evidenced by a Google Maps route where the longest given value is used?

- **Primary source:** Certify Transport Process component → INPUTS → Distance; Google Maps Sources (attached to component)
- **What to extract:** Certify distance value, Google Maps screenshot route options (Maps typically shows 2–4 routes), confirm which value was used
- **Pass criteria:** Certify distance = the LONGEST of the Google Maps route options for the Charm origin → Basco route
- **Fail mode:** Certify uses a shorter Google Maps option (typically the default/fastest); distance from a different routing tool; distance not evidenced

### 5.3 Does the Mass of Load match the Total Mass Transported value in Ops Notes?

- **Primary source:** Certify Transport Process component → INPUTS → Mass of Load; Ops Notes Total Mass Transported
- **Math:** Certify Mass of Load =? Ops Notes Total Mass Transported
- **Pass criteria:** values match (±1 kg)
- **Fail mode:** mismatch; Certify uses Total Oil in Batch or Total Oil Produced (those are not the transport-EF basis — Total Mass Transported is gross, including tote tares)

### 5.4 Is the Mass of Load evidenced by a copy of the batch Ops Notes?

- **Primary source:** Certify Transport Process component → linked sources (Certify API dump: datapoint source links + `sources` list)
- **Pass criteria:** Ops Notes (PDF, screenshot, or live link) attached to the Mass of Load datapoint
- **Fail mode:** evidence missing; only BOL attached (BOL is not Ops Notes)

### 5.5 Does the uncertainty reported for Mass of Load match the uncertainty value in Ops Notes?

- **Primary source:** Certify Transport Process component → INPUTS → Mass of Load uncertainty; Ops Notes uncertainty value
- **Math:** Certify Mass-of-Load uncertainty =? Ops Notes uncertainty (1.134 × N_totes kg)
- **Pass criteria:** match (±0.01 kg)
- **Fail mode:** mismatch with Ops Notes; or different uncertainty than Mass of Product on Sequestration (they should be identical — same totes, same weighings)

---

## SECTION 6 — Certify Transport Embodied Emissions (3 items)

### 6.1 Does the Transport Embodied emission use the correct and up-to-date Non-Tanker Truck emission factor?

- **Primary source:** Standard EFs sheet (2026 tab) + Certify Transport Embodied component → INPUTS → Emission Factor
- **Pass criteria:** values match (native units)
- **Fail mode:** Certify uses a different EF; EF from prior year; tanker EF used instead of non-tanker

### 6.2 Does the aggregate distance transported match the Batch Mileage Allocation in the RP Bio-Oil Shipment Tracker?

- **Primary source:** Certify Transport Embodied component → INPUTS → Distance; Bio-Oil Shipment Tracker → Batch Mileage Allocation cell
- **Math:** Certify distance =? Shipment Tracker Batch Mileage Allocation
- **Pass criteria:** values match (±0.1 mi)
- **Fail mode:** Certify uses full one-way distance instead of allocated distance; mismatch with Shipment Tracker

### 6.3 Is the aggregate distance evidenced with the RP Bio-Oil Shipment Tracker, batch Charm Contents, and applicable route Google Map?

- **Primary source:** Certify Transport Embodied component → linked sources (Certify API dump: datapoint source links + `sources` list)
- **Pass criteria:** all THREE evidence types attached: (a) Shipment Tracker, (b) Charm Contents, (c) Google Maps route
- **Fail mode:** any of the three missing

---

## SECTION 7 — Certify Production Emissions (6 items, applied per Production Period)

### 7.1 Are there Production Emissions components for ALL Production Periods in the batch?

- **Primary source:** Charm Contents sheet (PP list for the batch) + Certify API dump components list (enumerate all Production Emissions components)
- **Math:** every PP that contributed mass has its production emissions captured — either its own component OR an aggregated component whose production-mass-weighted blended CI reconciles to the per-PP sum
- **Pass criteria:** every PP's production emissions are accounted for (per-PP component or aggregated mass-weighted component both pass)
- **Fail mode:** a PP's production emissions omitted entirely (system-boundary completeness FAIL). Aggregating multiple PPs into one mass-weighted component is NOT a fail and NOT a flag — no primary source requires per-PP component granularity (verified absent on INJ-06-2026-W1).
- **Render:** if 3 PPs in batch, items 7.2–7.6 render 3 times (one per PP) with sub-numbers (7.2.PP-A, 7.2.PP-B, etc.) OR consolidate into a single Pass/Fail with per-PP evidence in column D

### 7.2 Does the CI match the Ops Notes weighted-average CI across all totes in the injection?

- **Evidence standard (Max-stated, 2026-06-30):** The production CI is **no longer necessarily evidenced by a PP Summary.** The **Ops Notes** is used to show the production-mass-weighted average CI across all totes in the injection (e.g. WODO tab `H26 = I26/D26 = ΣPE / Σ net produced`). A standalone PP Summary doc is NOT required.
- **Primary source:** Ops Notes (per-tote CI column + weighted-average cell) + Certify Production Emissions component → INPUTS → CI
- **Math:** Certify PE CI =? Ops Notes weighted-average CI across the batch's totes (an aggregated component's blended CI must reconcile to Σ(per-tote net produced × per-tote CI) / Σ net produced). Per-fraction/per-PP CIs (WODO vs Aqueous, month-to-month) must each be applied to the correct totes.
- **CI basis (Max-stated, 2026-10-07):** "BCUs should be applied to diesel transport, including biomass transport process emissions and handling (not embodied emissions)." Every CI used must count biomass transport after its BCUs: in each monthly summary, read the consolidated-inventory biomass transport cell (I19); `=C11*F7` is right; `=C9*F7` counts BCU-offset emissions and is a Fail whenever the month has BCUs applied to biomass transport (C10 > 0). See lessons_learned FC-C13.
- **No re-valuing verified CIs (Max-stated, 2026-10-07):** the CI-basis check above never asks to recalculate a production-period CI that has already been used in a verified GHG statement. Those CIs stand as verified. Raising one means re-valuing statements already verified earlier in the year, which Max has ruled out (INJ-09-2026-W4-QOWV 7.2, dropped). Apply the C9/C11 check only to a production period whose CI has not yet been used in any verified statement. If you cannot tell, ask Max in one sentence that names the consequence ("this would re-value the [month] statements already verified: yes or no?"), never as a general method question.
- **Pass criteria:** Certify CI = Ops Notes weighted average (reconciles to the per-tote sum), and every CI behind it that has not yet been used in a verified statement counts biomass transport after its BCUs
- **Fail mode:** mismatch; wrong fraction's CI applied to the wrong totes (WODO CI on Aqueous totes, or vice versa); a monthly or blended CI that counts biomass transport before its BCUs

### 7.3 Is the CI evidenced (Ops Notes weighted-average across totes)?

- **Evidence standard (Max-stated, 2026-06-30):** CI evidence = the **Ops Notes** (weighted-average across all totes used in the injection), NOT a PP Summary. Do not FAIL this for "missing PP Summary."
- **Primary source:** Certify Production Emissions component → linked sources (Certify API dump: datapoint source links + `sources` list); Ops Notes
- **Pass criteria:** the Ops Notes (PDF/screenshot/live link) is attached and linked to the CI datapoint
- **Fail mode:** the CI datapoint has no source linked / the Ops Notes is not attached. (This typically clears together with the other Ops-Notes-linking items — 4.2 carbon content, 5.4 transport mass, 7.6 production mass — when the batch Ops Notes is uploaded and linked in Certify.)

### 7.4 Does the mass match the sum of Net Weight of Bio-Oil in Tote values for the PP (Ops Notes)?

- **Primary source:** Certify PE component → INPUTS → Mass; Ops Notes per-tote Net-in-tote column, filtered to the PP
- **Math:** Certify mass =? Σ Net-in-tote for totes whose PP column = this PP
- **Pass criteria:** match (±1 kg)
- **Fail mode:** mismatch; PE mass uses Net-in-injection-batch instead of Net-in-tote; or wrong PP filter

### 7.5 Does the uncertainty match the sum of uncertainties for the PP (Ops Notes)?

- **Primary source:** Certify PE component → INPUTS → Mass uncertainty; Ops Notes per-tote uncertainty
- **Math:** Certify PE uncertainty =? 1.134 × N_totes_in_PP kg
- **Pass criteria:** match (±0.01 kg)
- **Fail mode:** mismatch; uses batch-total uncertainty instead of per-PP slice; **OR no uncertainty present at all on the PE mass.** Production (pyrolysis) mass is a dominant input (can exceed 100% of net), so §6.5.1 requires its uncertainty and the §6.5 <1% omission carve-out does NOT apply. A required uncertainty input that is missing = FAIL (you cannot submit a removal missing a required input) — do NOT downgrade to FLAG on the grounds that the measurement error's marginal effect is small. (INJ-06-2026-W1 WODO 2026-06-25: PE mass had no uncertainty → FAIL.)

### 7.6 Is the mass evidenced with a copy of the Charm Contents sheet for the batch?

- **Primary source:** Certify PE component → linked sources (Certify API dump: datapoint source links + `sources` list)
- **Pass criteria:** Charm Contents (PDF or screenshot) attached, OR — for 2026 weekly time-block batches, where no standalone Charm Contents sheet exists — the batch Ops Notes attached to the production-mass datapoint, with its Production Period column carrying the per-period mass breakdown. Confirm Charm Contents is absent from BOTH the Drive batch folder (`drive_read.py ls` listing) and the Certify API `sources` list before relying on the Ops Notes. This basis has been accepted on every 2026 weekly WODO/Aqueous batch.
- **Fail mode:** neither Charm Contents nor an Ops Notes carrying the per-period masses is attached to the mass datapoint

---

## SECTION 8 — Other (1 item)

### 8.1 Are all diesel transport-process emissions offset by BCUs, and does the BCU total equal (never exceed) the transport-process sum?

**Hard rule (Max-stated, authoritative):** ALL diesel transport-process emissions must be offset with BCUs. A diesel transport-process emission with NO BCU offset is a **FAIL** (required reduction missing) — NOT N/A. (Confirmed on INJ-06-2026-W1 WODO 2026-06-25: 1.954 t diesel flatbed process with empty Reductions → FAIL.)

- **Primary source:** Certify Reductions → BCU components + Certify Activities → Transport Process emissions
- **Math:** Σ BCU tCO2e (transport-related) =? Σ Transport Process activity tCO2e (each computed from the component's blueprint and inputs in the Certify API dump)
- **Pass criteria:** every diesel transport-process emission is BCU-offset AND Σ BCU = Σ transport process activity (BCU never exceeds the emission it offsets) (Corrected 2026-09-28 per Max: "BCUs should never exceed the emission." The prior "MUST equal or exceed" wording was reversed.)
- **Fail mode:** a diesel transport-process emission has no BCU (Reductions empty for that lane), OR BCU < transport process activity (under-reduction), OR BCU > transport process activity (over-coverage, any size). Material — a missing or excess BCU changes net.
- **N/A:** only if the batch has NO diesel transport-process emissions at all (e.g., no transport leg). Absence of a BCU when a diesel transport-process emission EXISTS is a FAIL, not N/A.

---

## SECTION 9 — Aqueous Buffering (LCS) (1 item, Aqueous-only)

### 9.1 If LCS use is reported in Ops Notes, does a matching Certify component exist?

- **Primary source:** Ops Notes (search for LCS / Liquid Calcium Sulfate / buffer column) + Certify API dump components list
- **Pass criteria:**
  - If Ops Notes reports LCS mass and use → a matching Certify component MUST exist (correct mass, correct EF, evidenced with Ops Notes copy)
  - If Ops Notes reports NO LCS use → N/A
- **Fail mode:** Ops Notes reports LCS use but no Certify component; mismatch between Ops Notes LCS mass and Certify component mass
- **For WODO batches:** this item is N/A (LCS is Aqueous-only)

---

## Sidebar Observations

Append a sidebar block at the end of the checklist (after Section 9) titled "Sidebar Observations." This block has no Pass/Fail status — it captures:

- System-boundary observations (e.g., a Production Period in Ops Notes that ALSO appears in another batch — a likely Charm Contents error, not a per-batch FAIL)
- Density anomalies, viscosity outliers, acid number out-of-range
- Process hygiene flags (missing tare measurements documented; non-descriptive filenames flagged in 1.x already)
- Out-of-frame Certify component observations (e.g., an unexpected component that's not in this checklist's section coverage)

Each sidebar item: one-line observation + Drive/Certify reference. No `[log:KEY]` required, but cite the source.

---

## Citation Discipline (Mandatory — Reused from AECN)

Every PASS / FAIL / FLAG status in column D must cite a `[log:KEY]` from `batch_[ID]_source_reads.json`. See `skills/qa/batch-qa-aecn/SKILL.md` Citation Discipline section for full rules.

Pre-delivery audit: the audit script (`skills/qa/batch-qa-aecn/scripts/audit_checklist.py`, reused) catches missing citations and other gaps.

Per-batch `outputs/qa/batch-<id>/build_checklist.py` scripts can call into `skills/qa/batch-qa-aecn/scripts/checklist_lib.py` so the same `[log:KEY]` rules that `audit_checklist.py` enforces post-hoc are checked **before** the xlsx is written.
