# Batch 2-182 — First Rail Batch Training Pass

**Date:** 2026-04-27
**Reviewer:** Claude QA Agent (training pass, not a graded QA)
**Removal:** rmv_1KQ7XY3Q81S0T52T
**Net CDR (per Certify):** 30.46 tCO₂e
**Date added (Certify):** 02 Apr 2026

## Purpose

This was an exploratory pass on the first rail batch the QA agent has seen. The goal was to surface rail-specific structural differences from truck batches and lock them into the batch-qa skill so the next rail batch goes smoother. Not a complete Gate 1; not a checklist; not handed to Garrett.

## Batch structure

- **Oil:** AECN, delivered by rail
- **Railcar:** GPRX 5188
- **Full railcar load:** 78.02 MT across 3 BOLs into SOPOR (2310-R: 26.01 MT, 2312-R: 26.00 MT, 2313-R: 26.01 MT)
- **This batch's offload:** 21,509.33 kg cargo → 21,231.86 kg injected (after 1.29% sparging = 277.47 kg loss), pH 3.1
- **Position in railcar:** Offload 1 of 4. Three more batches will come from the same railcar (likely 2-183, 2-184, 2-185). Rows 2–4 of the Ops Notes offload table are zero.
- **Upstream allocation fraction:** 21,509 / 78,020 = 0.2757
- **Distances** (from Ops Notes Batch Composition section):
  - AECN → SOPOR: 107.5 mi single-truck, × 3 trucks = 322.5 mi total
  - SOPOR → Opelousas (rail): 2,199 mi
  - Opelousas → Basco: 42.9 mi
- **Allocated distances** (full leg × 0.2757, written to the offload table for each batch):
  - Rail: 606.2422 mi
  - Truck Leg 1 (AECN → SOPOR): 88.91 mi
  - (Opelousas → Basco truck leg distance follows the same pattern but I didn't open its modal)

## How rail batches differ from truck batches — structural reference

### Component count
Truck batches: ~2 transport components (AECN→Basco truck process + embodied).
Rail batches: **6 transport components**, one process + one embodied per leg:
- AECN → SOPOR Tanker Truck Process / Embodied
- SOPOR → Opelousas Rail Process / Embodied
- Opelousas → Basco Tanker Truck Process / Embodied

### Pyrolysis component naming
Rail batches use `AECN pyrolysis (from rail loads) - process emissions` and `... embodied emissions` (vs. the truck convention `AECN Pyrolysis Process Emissions` / `AECN Pyrolysis Embodied Emissions`). **Same EFs, different label.** Per Max: the labeling is just a signal to the VVB to expect scale tickets as the authoritative mass source rather than the BOL.

### Authoritative mass source
- Truck batches: BOL is authoritative for mass.
- Rail batches: scale tickets are authoritative for mass. BOLs document the input side (3 BOLs into the railcar), but the offload mass at Basco comes from the truck-out scale tickets.

### Ops Notes layout
The rail Ops Notes (`2-182 Ops Notes Rail`) has a different shape from the truck version:
- A `Batch Composition` section with full-leg distances and railcar metadata
- A `BOLs Loaded` section listing the 3 input BOLs
- An offload table with up to 4 rows (one per truck-out from the railcar). Each row carries an `Upstream Allocation` fraction and a set of pre-allocated distances (full distance × allocation fraction).
- Only the populated row(s) carry data; unpopulated rows are zero.

### COBB tracker tab — KB CORRECTION NEEDED
The KB says rail batches go in `COBB (with offload info)`. Actually rail batches go in **`Basco Injection -- COBB`** — the same tab as truck batches. The `COBB (with offload info)` tab contains only older entries (max batch 2-122 / 3-54). 2-182, 2-183, 2-184, and 2-185 are all in `Basco Injection -- COBB`.

**Earlier in this pass I claimed COBB had not been populated. That was wrong** — the Drive MCP's natural-language read returned an abbreviated view that omitted the data tabs. After re-fetching as a binary xlsx and parsing locally, the row was found at row 59 in `Basco Injection -- COBB`. Section 5 cross-checks all pass cleanly:

| Field | COBB row 59 | Ops Notes / Certify |
|---|---|---|
| consumed_lot | Rail_GPRX 5188_2.27.26_offload_1 | matches |
| BOL_number | 2310-R, 2312-R, 2313-R | matches |
| offloaded_quantity_kg | 21,509.33264 | matches |
| origin_quantity_kg | 78,020.0 (full railcar) | = 26,010 + 26,000 + 26,010 ✓ |
| injection_completion_date | 2026-04-02 | matches Certify removal date |
| injection_ph | 3.1 | matches |

### Mass uncertainty methodology (per Max)
Standard rule on rail process Mass of Load = `72.57 kg × number of trucks loaded into railcar` (i.e., per truck-in). 2-182 had 3 BOLs in / 4 trucks out. Charm applies the per-truck-out rule (72.57 kg per truck-out), which over the full railcar accumulates 4 × 72.57 = 290.28 kg of uncertainty vs. 3 × 72.57 = 217.71 kg under the strict in-rule — slightly conservative, acceptable.

### Distance evidence convention
**There is no Google Maps for rail.** Email or written confirmation from the rail logistics provider (Watco, in this case Matt Bergeland) is the authoritative evidence. This batch's rail-distance source is `image (44).png` — a screenshot of an email from Matt confirming "the total milage for this move was 2199." Evidence type is acceptable; filename hygiene is a FLAG.

## Findings on this specific batch

### Rail Embodied — methodology question (only material item)

`SOPOR to Opelousas Rail Transport Embodied Emissions` (0.021 tCO₂e). The math is internally consistent under the OLDER per-mile methodology Certify is using:

- Allocated distance: 606.2422 mi (= 2199 × 0.2757) ✓
- EF: 0.0000352240 MTCO2e/mi (matches Standard EFs sheet older "Updated" entry from USDOT/USEPA/Cambridge Systematics) ✓
- Result: 606.2422 × 0.0000352240 = 0.02136 MT CO₂e ✓

**But:** the Standard EFs sheet has a newer "Updated" entry for railcar embodied at `0.0000311307 MT CO2e/T-mi` from GLEC V3.2 2025. The unit label on that newer entry is a typo — embodied emissions are always per-mile (per the Truck and Trailer EE 2026 derivation tables in the same sheet). Reading the value as `0.0000311307 MT CO2e/mi` instead of `/T-mi`:

- Same allocated-distance approach: 606.2422 × 0.0000311307 = **0.01887 tCO₂e**
- ~12% reduction vs current Certify value of 0.02136

**Resolution (per Max, 2026-04-27): the newer 0.0000311307 MT CO₂e/mi value is the up-to-date EF.** Certify is using the older stale value.

**Classification: FAIL — stale EF.**
- Correct value for 2-182: 606.2422 mi × 0.0000311307 = **0.01887 tCO₂e** (vs current Certify 0.02136 tCO₂e)
- Delta: ~12% reduction, ≈0.0025 tCO₂e on this batch
- Net headline impact: immaterial at one batch (0.07% of 30.46 tCO₂e), but the same shared datapoint feeds 4 rail process components — a single source-datapoint fix propagates to all four batches using it.

**Two follow-ups that aren't QA findings on 2-182 but should be tracked:**
1. **Unit-label typo on Standard EFs sheet:** newer entry reads `/T-mi`, should read `/mi`. Embodied is always per-mile.
2. **V17 LCA reconciliation (open):** neither published value reflects the V17 DOT-111 LCA's 65.37 MT CTGate. The implied lifetime mileage at 0.0000311307 MT/mi is ~2.10M mi. Whether to re-derive against V17 + a current EPA/AAR lifetime mileage figure is a separate decision.

### Rail Process EF — confirmed correct
- Certify shows 0.0259 kgCO₂e/(t·mi)
- Standard EFs sheet "Rail Transport Fuel Use (Well to Wheel)" = 0.000025910374 MTCO2e/T-mi (= 0.02591 kgCO₂e/T-mi) ✓ exact

### Tanker Truck Embodied EF — confirmed correct (per KB and sheet)
- 0.00023756059 MT CO₂e/mi (GLEC V3.2 2025) ✓
- Matches both the Standard EFs sheet and the KB Section 6 reference for 2026

### Distance evidence — acceptable
- Rail process distance source (`image (44).png`): email from Watco rail logistics specialist Matt Bergeland confirming 2199 mi for "this move." Evidence type appropriate. Filename hygiene = FLAG.
- Rail embodied has 5 sources on the distance datapoint (didn't open them; presumably support 2199 mi + the upstream allocation fraction derivation).

### COBB tracker — clean (with KB correction)
Row 59 in `Basco Injection -- COBB` (not `COBB (with offload info)` as the KB said). All Section 5 cross-checks against Ops Notes and Certify pass. Detail in the structural reference section above.

## What didn't get done in this pass

- Datapoints tab full enumeration
- Sources tab full enumeration (required for SOURCES TAB FIRST RULE — KB §0A Gate 1)
- Calculation View
- AECN→SOPOR truck process and embodied modals
- Opelousas→Basco truck process and embodied modals
- Pyrolysis (from rail loads) process and embodied modals
- Scale ticket PDFs (Drive subfolder)
- BOL PDFs
- CHN lab report
- COBB tracker offload-info tab (blocked / not populated)

## Updates locked in for future rail batches

1. **`lessons_learned.md` Failure Category 8**: embodied emissions are per-mile, never per-T-mi. Process emissions are per-T-mi. If a per-T-mi unit appears on a vehicle embodied entry it's a typo, not a methodology change.
2. **Source-read log scaffold** (`batch_2-182_source_reads.json`) captures the rail-batch structural notes (railcar number, BOLs in, offload position, upstream allocation fraction, allocated distances vs full distances).
3. The rail batch QA reference for the batch-qa skill should be updated separately with: 6-component transport structure, pyrolysis "(from rail loads)" naming convention, scale-ticket-as-authoritative-mass for rail, COBB rail-tab name, and the per-mile embodied / per-T-mi process methodology distinction.

## Recommended next actions

1. **Decide on the rail embodied EF magnitude** (which "Updated" entry is current; whether to re-derive against V17 LCA). This is the only material correctness question on this batch.
2. **Populate the COBB rail tab** for 2-182 so QA can complete Section 5.
3. **If running a graded QA on 2-182**, do it in a fresh session: I have the structural map now, but Gate 1 was only partially completed and several modals weren't opened.
4. **Update the batch-qa skill's checklist_structure.md** with rail-specific notes for Sections 2 (mass / scale tickets), 3 (BOLs — 3 in, scale tickets at offload), 5 (COBB rail tab), 6 (allocated distances vs full distances), and 7a (rail-leg uncertainty methodology). I can do this as a follow-up.
