# Kerry Injection Batch QA Checklist — Item-by-Item Reference

This document provides the complete specification for every checklist item in a Kerry-only batch QA: what to check, which primary source to open, what values to extract, expected ranges, and common failure modes.

**Scope:** Kerry oil batches only — both **tote** (flatbed truck delivers totes; per-tote weighing) and **tanker** (tanker truck with a bulk tanker trailer; full + empty scale ticket pair; the current mode since July 2026) delivery modes. No AECN, WODO, or Aqueous items.

**System boundary (settled — don't re-litigate):** Kerry is waste-derived per VVB-validated methodology. Biomass sourcing and production emissions are out-of-scope; only transport and injection-site emissions are in-scope. No upstream production components are expected in Certify; counterfactuals = 0.

---

## Tote vs Tanker Batch Reference (read first)

Every section below has tote-batch defaults. Where tanker batches differ, look for the **🚛 Tanker** note inline. The high-level differences:

| Aspect | Tote batch | Tanker batch |
|---|---|---|
| Delivery legs | 1 (Kerry origin → Basco) | 1 (Kerry origin → Basco) |
| Transport components in Certify | 2 (flatbed process + embodied) | 2 (tanker truck process + embodied) |
| Transport EFs (Standard EFs 2026 tab) | Flatbed Truck fuel use; Non-Tanker Truck embodied | Tanker Truck fuel use; Tanker Truck embodied |
| Mass artifacts | Tote weighing log (per-tote serial, gross, tare, net) | Full + empty scale ticket pair (one weighing event) |
| Authoritative mass source | Sum of per-tote nets | Scale ticket net (Full gross − Empty gross) |
| Tote count | Multiple per truckload (varies) | N/A (one tanker = one weighing) |
| Per-weighing uncertainty | 1.13 kg per tote (Charm tote scale) | 72.57 kg per tanker (commercial truck scale) |
| Summed Mass-of-Product uncertainty | N totes × 1.13 kg | 72.57 kg |
| Lab testing convention | Per-tote SGS CHN (current practice) | Tanker-level SGS CHN (going forward) |
| BOL "Qty Shipped" basis | Gross transported (oil + tote tares + deck items) | Oil-only mass |
| Transport-EF mass basis | BOL gross (NOT MOBI alone — see FC-K2) | BOL oil-only mass (= MOBI in tanker mode) |

**Mode detection at Gate 1:**
- If Drive contains a tote weighing log + BOL lists multiple totes → tote mode
- If Drive contains a single full + empty scale ticket pair + BOL lists single oil-mass → tanker mode
- Ambiguous → ask Max before proceeding

---

## Section 1: Batch Folder Completeness

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 1.1 | Batch folder exists with correct naming | Google Drive | Folder named with Kerry batch ID | Naming inconsistent |
| 1.2 | Mass quantification subfolder present and populated | Drive > batch folder | Tote Weighing subfolder (tote mode) OR Scale Tickets subfolder (tanker mode), with all required artifacts | Subfolder empty or missing artifacts |
| 1.3 | Testing subfolder present with all required lab results | Drive > batch folder | SGS CoA(s) — N CoAs for tote mode (one per tote, OR consolidated cert with per-tote rows), 1 CoA for tanker mode | Wrong batch's lab results |
| 1.4 | Ops Notes spreadsheet present and complete | Drive > batch folder | Google Sheet with Kerry mass IN, AECN mass IN, completion date, pH | Ops Notes partially complete |

**Verifier reference:** VR Appendix 1

**Document location rule applies:** Documents may be in Drive OR Certify Sources (the Certify API dump's `sources` list). Only FAIL if absent from BOTH — except that removal-level sources not linked to any datapoint are not visible via the API, so an absence from both is graded Fail as before, with the note "absent from Drive and the Certify API dump; confirm on the Sources tab (removal-level sources are not visible via the API)".

**Note on injection site:** Basco 6 only — no other Kerry injection site exists.

---

## Section 2: Mass Quantification

### Tote mode (default)

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 2.1 | Per-tote weighing records present (gross, tare, net) for every tote | Drive Tote Weighing subfolder or Certify Sources | One record per tote with gross_lb, tare_lb, net_kg, weighing date+location, tote serial # | Missing tote(s); illegible scale readout; missing serial |
| 2.2 | Tote tare measured (not assumed nominal) | Tote weighing log | Tare value recorded with weighing date for THIS batch's totes | Tare = manufacturer nominal label (e.g., "275 kg per IBC") → FLAG (FC-K1) |
| 2.3 | Net mass per tote: net = gross − tare; sum of nets = MOBI | Per-tote log | Independent recalculation matches | Transcription error; wrong unit conversion |
| 2.4 | Conservative MOBI: MIN(Σ tote nets, BOL oil-only mass) used as Kerry credit basis | Per-tote log + BOL | Smaller of the two used; document which leg was lower | Wrong mass selected |
| 2.5 | Per-tote reconciliation: count(totes on BOL) = count(serials weighed) = count(nets in Ops Notes) | All sources | Counts match exactly | Mismatch = FAIL (FC-K3) |

### 🚛 Tanker mode

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 2.1 | Empty and full scale ticket images present | Certify Sources or Drive Scale Tickets subfolder | Both PDFs readable with clear values | Only one ticket present; image unreadable |
| 2.2 | Tractor and trailer numbers match between empty and full tickets | Scale ticket PDFs | Same tractor # and trailer # on both | Mismatch = different vehicle weighed = FAIL |
| 2.3 | Net mass calculated correctly: Net_kg = (Full_gross_lb − Empty_gross_lb) / 2.20462 | Scale tickets | Independent recalculation matches Ops Notes | Transcription error; wrong conversion |
| 2.4 | Conservative MOBI: MIN(scale ticket net, BOL oil-only mass) used as Kerry credit basis | Scale tickets + BOL | Smaller of the two used | Wrong mass selected |
| 2.5 | Dates within 2 weeks of injection | Scale ticket PDFs | Date on tickets within 14 days of Ops Notes injection date | Stale tickets from prior shipment |

**Verifier references:** VR Sec 5.1, GHG Stmt Sec C

**MANDATORY VERIFICATION SUB-TASK (2.1–2.3, both modes):** Open every weighing artifact. Read values from the document. Do not rely on Ops Notes alone.

**Key formulas:**
- Per-tote net (kg) = (Gross_full_lb − Tare_empty_lb) / 2.20462
- Sum of nets across N totes = MOBI candidate (tote mode)
- Scale ticket net (kg) = (Full_gross_lb − Empty_gross_lb) / 2.20462 (tanker mode)
- Conservative MOBI = MIN(net candidate, BOL oil-only mass)

**No sparging deduction on Kerry.** Kerry enters the homogenization tank un-sparged. The 1.29% sparging deduction belongs to the AECN portion only and is QA'd by the AECN skill on the AECN production batch. If a sparging deduction is applied to Kerry mass anywhere (Ops Notes, Certify inputs, Certify net calculation) → FAIL.

**Mass transported (transport-EF basis):**
- Tote mode: BOL gross mass (oil + tote tares + deck items). Used as the Mass of Load datapoint on the flatbed process component. **NOT MOBI alone** (see FC-K2).
- Tanker mode: BOL oil-only mass = MOBI (analog of AECN tanker truck).

---

## Section 3: Bills of Lading & Transportation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 3.1 | BOL(s) present for each shipment | Drive or Certify Sources | At least 1 BOL per truckload | BOL missing from both Drive and Certify |
| 3.2 | BOL mass consistent with mass artifacts | BOL + mass artifacts | Tote mode: BOL gross ≥ MOBI + Σ(tote tares). Tanker mode: BOL oil-only ≥ MOBI. | BOL mass < reported mass |
| 3.3 | Origin and destination correct on BOL | BOL | Kerry origin (current confirmed = ~1,090 mi from Basco) → Basco | Wrong origin/destination |
| 3.4 | Transportation distance consistent with confirmed Kerry route | Certify Datapoints | **1,090 mi** (Garrett confirmed 2026-05-04 for current single origin). Second origin pending. | Distance significantly off; wrong origin used |

**Verifier references:** VR Appendix 1, VR Sec 3.5, PDD Sec A, Transport Emissions Acctg v1.1

**Kerry transport convention:**
- Mode: tanker truck for tanker deliveries (current); flatbed truck for tote deliveries. Rail not applicable.
- Single leg: Kerry origin → Basco, **1,090 mi** (current confirmed origin).
- If a second origin is added in the future, this section's expected distance will need updating; surface as a FLAG until the route reference is updated.

**BOL convention:**
- Tote mode: BOL "Qty Shipped" reflects gross transported (oil + tote tares + deck items).
- Tanker mode: BOL "Qty Shipped" reflects oil-only mass.

---

## Section 4: Bio-Oil Composition & Testing

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 4.1 | CHN analysis PDF(s) present | Drive > Testing or Certify Sources | Tote mode (current): N CoAs (one per tote) OR consolidated certificate with per-tote rows. Tanker mode (going forward): single CoA for the shipment. | Wrong batch's lab report; missing per-tote sample |
| 4.2 | Carbon content reported and used in Certify | CHN PDF + Certify | Lab carbon % matches Certify "Carbon Content of Bio-oil Injected" datapoint. **No historical Kerry range yet** — until n ≥ ~30 samples accumulate, FLAG-with-note ("Kerry baseline not yet established") rather than PASS-against-range. | Carbon % mismatch between lab and Certify; agent invents an expected range |
| 4.3 | Lab report references correct batch/sample ID | CHN PDF | Batch ID on certificate matches QA batch (or per-tote sample IDs match per-tote serials in tote mode) | Report for different batch; per-tote sample-to-serial mismatch |

**Verifier references:** VR Appendix 1, Biomass Feedstock Acctg v1.2, VR Sec 5.1

**Kerry baseline carbon range:** Not yet established. AECN's range (mean 39.42%, SD 6.09% from n=285 MRV samples) does NOT apply to Kerry — different feedstock chain, different expected range. Until Kerry has its own n ≥ ~30 dataset, item 4.2 starts as FLAG-with-note rather than against-range. Once baseline is established, update this reference and the SKILL.md.

**Note on density/viscosity:** Kerry is homogenized with sparged AECN at Basco. Density and viscosity per-batch are operational compatibility checks (not credit math); convention TBD by Garrett.

---

## Section 5: Ops Notes Accuracy & Internal Consistency

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 5.1 | Correct batch ID and injection date | Ops Notes | Matches batch being QA'd | Wrong batch ID in header |
| 5.2 | Mass values correctly transcribed (Kerry mass IN, AECN mass IN, total injectate) | Ops Notes vs mass artifacts | Kerry mass IN matches Σ tote nets (tote mode) or scale ticket net (tanker mode); AECN mass IN matches AECN side's documentation; total injectate = Kerry IN + sparged-AECN IN | Transcription error; commingled Kerry+AECN mass not separated |
| 5.3 | COBB values present and match | COBB tracker vs Ops Notes | `consumed_lot` follows `kc_NNNN`; origin_qty, BOL_number align with Ops Notes | COBB row not found; values differ; wrong consumed_lot pattern |
| 5.4 | Completion date present and matches COBB | Ops Notes vs COBB | Same date in both | Date mismatch |

**MANDATORY VERIFICATION SUB-TASK (5.3, 5.4):** Read the COBB `Basco Injection -- COBB` tab with `drive_read.py rows` (absence needs a full-tab scan: `rows_scanned` over the whole tab, `match_count: 0`). Verify cell A = batch ID before reading any values. Verify `consumed_lot` field shows `kc_NNNN` pattern.

**pH measurement:** required for all batches per workspace memory. Find in Ops Notes Batch Consumables section. If pH is missing, Section 5 includes a FAIL.

---

## Section 6: Gross-to-Net Calculation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 6.1 | Gross CO2e = MOBI (tonnes) × carbon wt% (decimal) × 3.667 | Independent calc vs Certify | Match within rounding | Carbon % not as decimal (42 vs 0.42); unit mismatch; sparging deduction erroneously applied to MOBI |
| 6.2 | Process emissions correctly deducted (transport process + embodied; injection-site process + embodied; injection electricity) | Certify API dump: components + blueprint-computed net calc | Only in-scope components present | Upstream Kerry production component appears (FAIL — system-boundary violation); component missing |
| 6.3 | Uncertainty discount correctly applied | Certify API dump: discount = `removal.co2e_net_removed_without_discount_kg` − `removal.co2e_net_removed_kg`; undiscounted net vs blueprint-computed gross-to-net | Present per Isometric Standard S3.7 | Discount missing |

**Verifier references:** GHG Stmt Sec E, Bio-oil Geol Storage v1.1, Isometric Standard v2.0 S3.7

**Formula verification:** Gross = MOBI_tonnes × carbon_decimal × 3.667. Carbon content must be a decimal (e.g., 0.4140, not 41.40). MOBI is the conservative selection from Section 2.4 — un-sparged.

**Critical Kerry-specific check:** The Kerry sequestration credit is based on un-sparged MOBI. Do NOT subtract 1.29% from MOBI before computing gross. The sparging deduction is applied to the AECN portion of the mixed injection, on the AECN production batch.

---

## Section 6a: Per-Component Uncertainty Verification

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 6a.1 | Layer 1 — Completeness: every Kerry component has uncertainty on correct datapoint | Certify API summary: per-component input table | All required components have +/- values (`standard_deviation`) | Missing uncertainty on a component |
| 6a.2 | Layer 2 — Correctness: reported +/- matches expected value | Certify API summary: per-component inputs (`standard_deviation`, cited by JSON path) | See Uncertainty Reference in SKILL.md | Wrong value; value not actually checked |
| 6a.3 | Layer 3 — Discount presence and consistency | Certify API dump discount (`removal.co2e_net_removed_without_discount_kg` − `removal.co2e_net_removed_kg`) and net vs GHG Statement | Aggregate discount present in net calc | Discount missing or inconsistent |

**MANDATORY VERIFICATION SUB-TASK:** Read EACH component's inputs from the Certify API. Read the +/- (`standard_deviation`) of every input, cited by JSON path. Do not infer from aggregate calculations. +3 laziness penalty for not reading each component's input ± values from the Certify API.

**Kerry components requiring uncertainty verification:**
- Injection Sequestration (Carbon Content + Mass of Product)
- Transport — Process (Mass of Load): tanker truck (tanker mode) or flatbed (tote mode)
- Transport — Embodied (no Mass of Load — per-mile only): tanker truck or flatbed
- Injection-site components (electricity, pumping — same as AECN convention)

**Per-weighing precision follows the SCALE, not the oil type** (Max, 2026-08-10). Charm's tote scale is 2.5 lb ≈ **1.13 kg** per discrete weight; a commercial truck scale (e.g. CAT Scale) is **72.57 kg** per discrete weight. Kerry in totes gets 1.13 kg; Kerry by tanker gets 72.57 kg, the same as an AECN tanker. Read the scale name off the ticket before choosing.

**Tote-mode summed uncertainty:** With N totes weighed, Mass-of-Product uncertainty = N × 1.13 kg (additive convention, consistent with Charm WODO and AECN per-truck rule). Same N × 1.13 kg uncertainty applies to the Mass of Load on the flatbed process component.

**Tanker-mode uncertainty:** One discrete weighing event on a commercial truck scale. Mass-of-Product = **72.57 kg**. Mass of Load on the tanker truck process component = **72.57 kg**. Settled on INJ-07-2026-W4, the first Kerry tanker batch.

**Embodied components have no Mass of Load datapoint** — per-mile, mass-independent (same convention as AECN railcar embodied to avoid Failure Category 8 from the AECN lessons_learned).

---

## Section 7: Data Integrity & Anomaly Check

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 7.1 | No unexplained outliers in mass, carbon content, or calculated values | All sources | Values within expected ranges (mass: per-tote <~1.4 MT for IBC totes; carbon: no Kerry baseline yet → FLAG-with-note) | Outlier not investigated |
| 7.2 | Any spills/losses documented, unrecovered mass deducted, incident report filed | Ops Notes, batch folder | If spill occurred: documented and deducted | Spill not deducted from mass |

**Custody rule (2026-09-29):** upstream emissions of all oil in Charm custody are netted against removals. Production and transport emissions must be charged on the mass that entered custody on each leg, not only on the offloaded or injected mass; any lost mass (railcar loss, spill, standard loss, R&D removal) whose upstream emissions are not charged is a Fail, with the missing tCO2e computed.


**Verifier reference:** GHG Stmt Sec C, VR Sec 3.5

**Kerry baseline note:** No historical Kerry dataset yet exists (Kerry is a new supplier). Outlier checks on carbon content and mass should be FLAG-with-note rather than PASS-against-range until baselines accumulate. Update this section once n ≥ ~30 samples are available.

---

## Section 8: Isometric Certify — Removal Component Mapping

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 8.1 | SEQUESTRATIONS: Gross injection sequestration matches internal gross | Certify Components | One sequestration entry for the Kerry batch | Sequestration value wrong |
| 8.2 | ACTIVITIES — Transport: Process + embodied for Kerry → Basco, vehicle class matching the delivery mode | Certify Components | 2 components: tanker mode "Kerry to Basco Tanker Truck Transport Process/Embodied Emissions"; tote mode "Flatbed Truck Transport Process/Embodied" | Missing one of the two; vehicle class not matching the delivery mode (e.g., flatbed factors on a tanker load) |
| 8.3 | ACTIVITIES — Injection: electricity, pumping, embodied present | Certify Components | Injection-site emissions analogous to AECN at Basco | Missing component; wrong grid factor |
| 8.4 | NO upstream production components | Certify Components | Kerry Production Process and Kerry Production Embodied components ABSENT (per VVB-validated waste boundary) | If present → FAIL (system-boundary violation) |
| 8.5 | COUNTERFACTUALS: zero | Certify Components | 0 (waste boundary excludes upstream entirely; no offsetting counterfactual) | Non-zero counterfactual = FAIL (system-boundary violation) |

| 8.6 | REDUCTIONS: BCU Transport quantity = transport process activity (never exceeds) | Certify API dump: components + blueprint-computed tCO2e | BCU Transport = transport process emission | BCU underfunded, or BCU exceeds the emission (any size) |
| 8.7 | Net removal matches internal calculation | Certify API dump: `removal.co2e_net_removed_kg` | Agrees with independent gross-to-net | Discrepancy |
| 8.8 | All Datapoints have descriptive source names | Certify Datapoints | No "Measurement XXXX" or "IMG_001" | Generic names = FLAG (not FAIL) |
| 8.9 | All Sources match files in batch folder on Drive | Certify Sources vs Drive | Same files in both | File in one but not the other |

**Verifier reference:** Certify Components, Certify Datapoints, Certify Sources, Certify net calculation (all read via the Certify API dump)

**On 8.2 (Transport mode, ruling 2026-10-06):** Kerry used to travel in totes on flatbeds and now travels in bulk tanker trailers. Tanker deliveries take the Tanker Truck fuel-use and Tanker Truck embodied factors; tote deliveries take the Flatbed Truck fuel-use and Non-Tanker Truck embodied factors. Never railcar. Read the commodity on the scale tickets ("TANKER") to confirm the vehicle.

**On 8.4 (No upstream production):** This is the most distinctive Kerry check. Kerry's VVB-validated boundary excludes biomass sourcing and production emissions entirely. If Certify shows any of:
- "Kerry Production Process Emissions"
- "Kerry Production Embodied Emissions"
- "Kerry Biomass Sourcing"
- Any pyrolysis or feedstock component associated with Kerry

→ FAIL. The component should not exist; its presence indicates the Kerry methodology has been misapplied in Certify.

**On 8.5 (Counterfactuals):** The waste boundary excludes upstream rather than offsetting it with a counterfactual emission. Counterfactual = 0 is correct. Non-zero counterfactual = FAIL.

**On 8.6 (BCU = activity, never more):** BCUs offset transport process emissions only. Over-coverage is a FAIL (Corrected 2026-09-28 per Max: "BCUs should never exceed the emission." The prior "MUST equal or exceed" wording was reversed.). Embodied emissions are NOT BCU-eligible (per protocol).

**On 8.8:** Generic/non-descriptive filenames are a FLAG with yellow fill, not a FAIL. The content is correct; the naming is a hygiene issue.

**On 8.9:** Document Location Rule applies — the doc may be in Drive OR Certify Sources. Only FAIL if absent from BOTH. Certify Sources are read from the API dump's `sources` list and Drive from a `drive_read.py ls --recursive` listing; a Drive file missing from the API list may be a removal-level source not linked to any datapoint, which the API cannot see — grade that Flag ("not visible via Certify API; confirm on the Sources tab"), never Fail on that alone.
