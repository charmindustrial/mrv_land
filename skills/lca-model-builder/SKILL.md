---
name: lca-model-builder
description: >
  Life Cycle Assessment model builder for Charm Industrial capital goods (railcars, tanks, equipment).
  Builds materials-based cradle-to-grave embodied emissions Excel models using BOM decomposition,
  GREET2 emission factors, and regulatory/manufacturer specifications. ALWAYS trigger this skill when:
  building or modifying an LCA or embodied emissions model, constructing a Bill of Materials for
  capital equipment, selecting or applying emission factors from GREET2 or ICE databases, computing
  cradle-to-gate or cradle-to-grave GHG totals, working with 49 CFR tank car specifications,
  reviewing or QAing an existing embodied emissions spreadsheet, or when the user mentions
  "embodied emissions," "materials-based," "BOM," "emission factors," "GREET2," "cradle-to-gate,"
  "cradle-to-grave," "capital goods LCA," or "railcar emissions model." Also trigger when the user
  asks to update, fix, or extend the DOT-111 model specifically. When in doubt about whether a task
  involves LCA modeling, use this skill.
---

# LCA Model Builder — Charm Industrial

## Purpose

Build and maintain materials-based cradle-to-grave embodied emissions models for Charm Industrial
capital goods. The primary use case is quantifying the lifecycle GHG footprint of transport and
injection assets (railcars, tanks, equipment) using a Bill of Materials approach rather than
cost-based EEIO.

## Sourcing Standard

This is the most important section of this skill. Every claim in a model must pass this test:

**"Can someone who has never seen the equipment click a link or look up a cited document and
verify this claim?"**

If the answer is no, the value is an unsourced estimate and must be labeled as such.

### What counts as a source

- **Regulatory documents**: 49 CFR, state permits, KDHE orders — cite section number
- **Manufacturer spec sheets**: GBRX, Wabtec, Amsted Rail — cite document title and date
- **Peer-reviewed papers and government reports**: FRA, DOE, Argonne National Lab (GREET)
- **Industry standards (public)**: AAR standards that are freely accessible (e.g., OT-24)
- **Engineering databases**: eFunda, Engineering Toolbox — for physical constants with ASTM/ASME backing

### What does NOT count as a source

- **Forums**: trainorders.com, railroad.net, Reddit, Stack Exchange, Quora — these are opinions
- **Marketplace listings**: made-in-china.com, Alibaba, Amazon product pages
- **Blogs and informal websites**: train-wheels.com, hobbyist sites, wikis without citations
- **Unsourced manufacturer claims**: A manufacturer page that states a value without citing a standard is not authoritative — it's marketing
- **Your own assertions dressed up as facts**: Saying something is "standard," "typical," "industry practice," or "commonly used" does NOT make it sourced. If there's no document behind the claim, it's an estimate.

### How to handle unsourced values

When no authoritative public source exists for a value:

1. State "ESTIMATE. No authoritative public source found."
2. Explain the basis for the estimate (geometry calculation, analogy, professional judgment)
3. If a proprietary standard likely contains the answer, say so: "AAR MSRP Section G covers wheel specifications but is not publicly available."
4. Never fabricate authority. Never use "standard" or "typical" without a verifiable citation.
5. Mark the cell with estimate formatting (red font in the Excel model).

### Derived values

A value derived via formula from other values inherits the classification of its weakest input.
If you derive axle weight from an estimated wheelset and an estimated wheel weight, the axle weight
is "DERIVED from estimates" — not "DERIVED from sourced values."

## Model Architecture

### Section Structure (Excel)

| Section | Content |
|---------|---------|
| 1 | Configuration header (car type, tare, service, GRL) |
| 2A | Component unit weights, geometry inputs, counts |
| 2B | BOM mass calculations (formulas referencing 2A) |
| 3A | Raw GREET2 emission factor values with unit conversions |
| 3B | Derivation assumptions (steel mix, grid factor, fabrication energy) |
| 3C | Applied emission factors (formulas referencing 3A/3B) |
| 4 | Cradle-to-gate emissions (BOM × EFs) |
| 5 | End-of-life credit calculation |
| 6 | Summary totals (CTGrave, CTGate, comparison to EEIO) |
| 7 | Methodology notes and version changelog |
| 8 | Source list with URLs |

### Key Principles

- **Tare weight is the anchor.** The manufacturer-specified tare weight (e.g., GBRX spec) is the
  one sourced total. The BOM must reconcile to tare via a residual/plug category.
- **Every cell is a formula or a labeled input.** No magic numbers buried in formulas.
  Every derived value must be an auditable Excel formula referencing named input cells.
- **The plug absorbs what you can't itemize.** Ladders, walkways, platforms, stiffening rings,
  piping connections — items with no public mass data go into the plug. Apply structural steel EF.
  Report plug as % of tare in methodology notes.
- **Two output files:** Internal (with EEIO comparison section) and External (without).

### Emission Factor Sources (Priority Order)

1. **R&D GREET2 2025** (Argonne National Lab) — primary source for materials EFs
   - Mat_Sum sheet row 65: GHGs in grams per lb → multiply by 2.20462 / 1000 = kgCO₂e/kg
   - C.Iron sheet row 81: per-lb columns (G=cast, I=forged); per-ton uses SHORT TONS
2. **ICE v2.0** (University of Bath) — for materials not in GREET2 (mineral wool, paint)
3. **EPA eGRID** — US average grid emission factor (convert lbs to kg: ÷ 2.20462)

### Source Classification Labels

Use these exact labels in source notes:

- **SOURCED** = value directly from a cited document a third party can verify
- **DERIVED** = formula from sourced inputs (or "DERIVED from estimates" if inputs are estimates)
- **ESTIMATE** = engineering estimate with stated basis and honest uncertainty acknowledgment
- **PROXY** = emission factor from an analogous material (state the analogy and why)
- **PLUG** = residual to reconcile BOM with sourced tare weight

## Active Model: DOT-111 Embodied Emissions

### Current State (V16)

- **Build script**: `build_dot111_v16.py` (generates both Excel files)
- **CTGrave**: ~14.34 MT CO₂e
- **CTGate**: ~66.19 MT CO₂e
- **Current EEIO value being replaced**: 23.958 MT CO₂e (cost-based, v8)
- **Tare**: 39,168 kg (86,350 lbs per GBRX Jan 2021 spec)
- **Plug**: ~8.6% of tare (miscellaneous structural steel)

### Key Sourced Values

- Tare weight: 86,350 lbs — GBRX spec sheet (Jan 2021)
- Tank OD: 9'-10 3/4" (3.016 m) — GBRX spec
- Tank outside length: 53'-4 7/8" (16.28 m) — GBRX spec
- Shell thickness: 7/16" (11.11 mm) — 49 CFR 179.201-1
- Jacket thickness: 11 gauge (3.038 mm) — 49 CFR 179.200-4
- Draft gear: 386 lbs — Wabtec Mark 50 product page
- Steel density: 7,850 kg/m³ — eFunda (ASTM A516 Gr 70)
- US steel mix: 33% BF-BOF / 67% EAF — Hasanbeigi & Springer 2019
- Grid EF: 0.367 kgCO₂e/kWh — EPA eGRID 2023
- Recycling rate: 96% — GREET2 Mat_Sum B19
- Service life: 50 years — AAR Rule 88 / OT-24

### Key Estimated Values (no authoritative public source)

- Wheel: 900 lbs — unsourced engineering estimate
- Wheelset: 2,300 lbs — unsourced engineering estimate
- Truck assembly: 10,000 lbs per truck — unsourced engineering estimate
- Coupler: 200 kg — unsourced engineering estimate
- Brake cylinders: 50 kg each, count of 4 — unsourced engineering estimates
- Insulation density: 140 kg/m³ — estimate (mid-range 80-200 per Engineering Toolbox)
- Coil banks: 4 banks × 50 m pipe — unsourced engineering estimates
- All valve/fitting weights — unsourced engineering estimates

### Open Items

1. **Brass EoL treatment**: Top fittings (350 kg) use brass EF for production but are counted
   in steel recyclable mass for EoL credit. Structural fix: separate brass recyclable mass with
   brass-specific recycling credit. Impact: ~+0.49 MT CO₂e.
2. **Insulation head coverage**: Cylinder-only formula omits ~181 kg of head insulation,
   absorbed by plug at steel EF instead of mineral wool EF. Impact: ~+0.21 MT (1.4%).
3. **Authoritative truck component sources**: AAR MSRP Sections G and S likely contain
   wheel, axle, and truck specifications but are proprietary. If Charm can access these
   standards, the truck section estimates could be upgraded to sourced values.

## Failure Modes to Avoid

These are patterns that have occurred in previous iterations and must not recur:

1. **Fake authority**: Using "standard," "typical," "industry practice" without a verifiable
   source. This is the #1 failure mode. If you catch yourself writing these words, stop and
   ask: "Where's the document?"

2. **Forum/blog citations**: Treating forum posts, marketplace listings, hobbyist websites,
   or unattributed manufacturer claims as authoritative sources. They are not. If the only
   "source" is a forum post, the value is an unsourced estimate.

3. **Fabricated specifics**: Inventing precise details (e.g., "6.5" x 12" Class F forged axle")
   that sound authoritative but have no source. Round numbers with honest uncertainty are
   better than precise numbers with fabricated provenance.

4. **Broken derivation chains**: Writing a formula that doesn't match the described algebra.
   Always trace the math: if the formula says `(A/2 - 2*B)/2` and the note says "yields ~550,"
   compute it and verify.

5. **Source note doesn't support the value**: Citing a real source but the source doesn't
   actually contain the specific number claimed. The Standard Steel paper gives wheel LOAD
   capacity (35,750 lbs), not wheel MASS. Don't conflate them.

6. **Calling derived-from-estimates "sourced"**: If the parent values are estimates, the
   derived value is also uncertain. Label it "DERIVED from estimates."

## GREET2 Reference

When working with the uploaded GREET2 file:

- **Location**: Check for uploaded .xlsm file in uploads directory
- **Mat_Sum sheet**: Row 65 has per-lb GHG values. Columns vary by material.
  Conversion: value_in_grams_per_lb × 2.20462 / 1000 = kgCO₂e/kg
- **C.Iron sheet**: Row 81. Column G = cast iron, Column I = wrought/forged iron.
  Per-lb columns (NOT per-ton which uses short tons).
- **Recycling rate**: Mat_Sum cell B19 (96% for steel)
- **Always show the conversion arithmetic** in source notes so a reviewer can verify.
