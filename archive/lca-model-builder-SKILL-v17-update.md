---
name: lca-model-builder
description: >
  Life Cycle Assessment model builder for Charm Industrial capital goods (railcars, tanks, equipment).
  Builds materials-based cradle-to-grave embodied emissions Excel models using BOM decomposition,
  emission factors from GREET/GLEC/ICE/eGRID, and regulatory/manufacturer specifications. ALWAYS
  trigger this skill when: building or modifying an LCA or embodied emissions model, constructing
  a Bill of Materials for capital equipment, selecting or applying emission factors, computing
  cradle-to-gate or cradle-to-grave GHG totals, working with 49 CFR tank car specifications,
  reviewing or QAing an existing embodied emissions spreadsheet, or when the user mentions
  "embodied emissions," "materials-based," "BOM," "emission factors," "GREET," "GLEC," "ICE,"
  "cradle-to-gate," "cradle-to-grave," "capital goods LCA," or "railcar emissions model." Also
  trigger when the user asks to update, fix, or extend the DOT-111 model specifically. When in
  doubt about whether a task involves LCA modeling, use this skill.
---

# LCA Model Builder — Charm Industrial

## Purpose

Build and maintain materials-based cradle-to-grave embodied emissions models for Charm Industrial
capital goods. The primary use case is quantifying the lifecycle GHG footprint of transport and
injection assets (railcars, tanks, equipment) using a Bill of Materials approach rather than
cost-based EEIO.

## Pre-Build Requirements

Before writing any code or producing any output, the builder must have or obtain answers to these
five questions. If Max hasn't specified them, ask before building.

1. **Asset**: What equipment is being modeled? (e.g., DOT-111 tank car)
2. **EoL method**: Cut-off (recycled content) or avoided burden? Default: cut-off.
3. **EF databases + versions**: Which databases and which versions? (e.g., GREET2 2025, ICE v4.1,
   eGRID 2023). Always use the latest available version. Using an outdated version is a failure.
4. **Audience**: External (verifier-facing) or internal (MRV team review)?
   - External: no internal comparisons, no verbose methodology deep-dives, no prior-version
     references. The reader is a third-party verifier, not the MRV team.
   - Internal: comparison sections and detailed methodology notes are acceptable.
5. **Non-steel materials**: What categories? (e.g., insulation, brass, coatings, rubber)

## Sourcing Standard

This is the most important section of this skill. Every claim in a model must pass this test:

**"Can someone who has never seen the equipment click a link or look up a cited document and
verify this claim?"**

If the answer is no, the value is an unsourced estimate and must be labeled as such.

### Source verification is mandatory, not optional

Before any value goes into the model with a source citation:

1. **Open the source.** Fetch the URL, open the PDF, read the GREET cell. Actually look at it.
2. **Confirm the source says what you claim it says.** If the sheet says "thermal conductivity"
   and you're citing it for density, that's a bogus citation. If the GREET column header says
   "Recycled Lead" and you're citing it for rubber, that's wrong.
3. **If you can't verify the source, don't cite it.** Label the value as an ESTIMATE instead
   of attaching an unverified URL. An honest estimate is better than a fake citation.

This step is non-negotiable. The build script includes automated GREET verification that will
fail the build if values don't match. But GREET is only one source — every other URL must also
be verified by reading the actual page before including it. There is no excuse for citing a
page that doesn't say what you claim it says.

### What counts as a source

- **Regulatory documents**: 49 CFR, state permits, KDHE orders — cite section number
- **Manufacturer spec sheets and product listings**: GBRX, Wabtec, Amsted Rail — cite document
  title and date.
- **Peer-reviewed papers and government reports**: FRA, DOE, Argonne National Lab (GREET)
- **Industry standards (public)**: AAR standards that are freely accessible (e.g., OT-24)
- **Engineering databases**: eFunda, Engineering Toolbox — for physical constants with ASTM/ASME backing
- **EPDs (Environmental Product Declarations)**: Manufacturer EPDs verified per ISO 14025/EN 15804
  (e.g., Knauf Insulation EPD for mineral wool density). These are third-party verified documents.
- **Proxies from sourced analogues**: Acceptable when no direct source exists, BUT the proxy
  itself must be sourced and linked, and the note must explain why the analogy is reasonable.

### What does NOT count as a source

- **Forums**: trainorders.com, railroad.net, Reddit, Stack Exchange, Quora
- **Blogs and hobbyist sites**: wikis without citations, enthusiast pages
- **Your own assertions dressed up as facts**: Saying something is "standard," "typical,"
  "industry practice," or "commonly used" does NOT make it sourced. If there's no document
  behind the claim, it's an estimate.
- **Fake-authority ranges**: Stating "80–200 kg/m³" or "1.3–2.0 GJ/t" without a source for
  the range is dressing up an estimate with false precision. Either cite where the range
  comes from or say "unsourced engineering estimate."
- **Previous model versions**: "Carried from V16" is not a source. Every value must have an
  independent justification that a reviewer can verify without access to prior models.

### How to handle unsourced values

1. State "ESTIMATE. No authoritative public source found."
2. Explain the basis for the estimate (geometry calculation, analogy, professional judgment)
3. If a proprietary standard likely contains the answer, say so: "AAR MSRP Section G covers
   wheel specifications but is not publicly available."
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
| 1 | Physical specifications (car type, tare, dimensions, thicknesses) |
| 2 | Non-steel material inputs & geometry |
| 3 | Material mass breakdown (non-steel items + steel residual) |
| 4A | Raw EF reference values (GREET2 with cell refs) |
| 4B | Derivation assumptions (steel mix, grid factor, fabrication energy) |
| 4C | Applied EFs (formulas referencing 4A/4B) |
| 5 | Cradle-to-gate emissions (BOM × EFs) |
| 6 | End-of-life method & cradle-to-grave total |
| 7 | Methodology notes (concise, audience-appropriate) |
| 8 | Key sources with URLs |

### Key Principles

- **Tare weight is the anchor.** The manufacturer-specified tare weight (e.g., GBRX spec) is the
  one sourced total. The BOM must reconcile to tare via a residual category.
- **Steel is the residual.** Steel mass = tare minus identified non-steel materials. Do NOT
  itemize individual steel sub-components (coil banks, truck assemblies, couplers, etc.) unless
  they use a different EF than the blended steel EF. If it's steel and it gets the steel EF,
  it belongs in the residual. Breaking out steel sub-components creates unsourced estimates that
  add complexity without changing the result.
- **Every cell is a formula or a labeled input.** No hard-coded values buried in formulas.
  If a value is computed (e.g., 118.75 inches = 9 feet × 12 + 10.75 inches), the Excel cell must
  contain the formula, not the result. A reviewer must be able to click on any cell and trace its
  inputs back to labeled source cells.
- **One output file by default.** No internal/external split unless specifically requested.
- **Sources are inline.** Every value row carries its own source citation in the derivation
  column and URL in column G. A separate "Key Sources" section at the bottom is acceptable
  as a summary reference list but is not the primary citation mechanism.

### Emission Factor Sources

**Always use the latest available version of every EF database.** Before building, confirm you
have the current version. Using an outdated version when a newer one exists is a failure — it
signals that the model wasn't built with care. When in doubt, search for the current version.

- **R&D GREET2** (Argonne National Lab) — US-focused materials and energy EFs
  - Mat_Sum sheet row 65: GHGs in grams per lb → multiply by 2.20462 / 1000 = kgCO₂e/kg
  - C.Iron sheet row 81: per-lb columns (G=cast, I=forged); per-ton uses SHORT TONS
  - **Verify every column header before using a value.** GREET has 70+ material columns and
    they are not labeled intuitively. Col AQ is recycled lead, not rubber. Col BU is rubber.
    Read the header at row 44 to confirm.
- **GLEC Framework** — transport and logistics emission factors
- **ICE** (University of Bath) — materials not covered by GREET (mineral wool, paint, etc.)
  - As of April 2026, current version is **v4.1**. Do NOT use v2.0.
  - Check for newer versions before each build.
- **EPA eGRID** — US grid emission factors (convert lbs to kg: ÷ 2.20462)

### EoL Method Consistency

The end-of-life method must be consistent with the production EF approach:

- **Cut-off (recycled content)**: Use when the production EF already reflects recycled content
  (e.g., a blended US steel EF with 67% EAF). No EoL recycling credit. CTGrave = CTGate.
  This is the default for Charm models. The rationale: adding an avoided-burden EoL credit
  on top of a recycled-content production EF double-counts the recycling benefit.
- **Avoided burden**: Use only with virgin-only production EFs. Requires net scrap balance,
  grade-specific virgin/recycled splits, and scrap market displacement factors per World Steel
  LCI methodology (p17). If you don't have those data inputs, don't use this method.

If you're unsure, default to cut-off. It's conservative (higher emissions) and requires fewer
data inputs.

### Source Classification Labels

Use these exact labels in source notes:

- **SOURCED** = value directly from a cited document a third party can verify
- **DERIVED** = formula from sourced inputs (or "DERIVED from estimates" if inputs are estimates)
- **ESTIMATE** = engineering estimate with stated basis and honest uncertainty acknowledgment
- **PROXY** = value from a sourced analogue applied to a different component. The proxy source
  must be linked and the analogy must be justified in the note.
- **PLUG** = residual to reconcile BOM with sourced tare weight

## Build Verification

The build script must include automated verification that runs before producing output files.
If verification fails, the build fails — no output. This is not optional.

Minimum verification checks:
1. **GREET cell verification**: Every GREET value in the model is checked against the actual
   GREET2 file. Column headers must match expected materials. Row 65 values must match within
   floating-point tolerance.
2. **Classification consistency**: SOURCED rows (except sub-components) must have a URL.
   Derivation text saying "unsourced" cannot co-exist with SOURCED classification.
3. **Formula error check**: No #VALUE!, #REF!, #NAME?, #DIV/0!, #NULL!, #N/A in any cell.
4. **BOM reconciliation**: Tare minus non-steel minus steel residual must equal zero.

The verification function should be embedded in the build script itself (not a separate script
that can be skipped). Build to a temp file, verify, then move to final path only if clean.

## Active Model: DOT-111 Embodied Emissions

### Current State (V17)

- **Build script**: `build_dot111_v17.py` (generates Excel model with built-in verification)
- **Method**: Steel + marginal materials. Steel = tare − non-steel. Cut-off EoL (no recycling credit).
- **CTGrave = CTGate**: ~65.37 MT CO₂e
- **Tare**: 39,168 kg (86,350 lbs per GBRX Jan 2021 spec)
- **Non-steel**: ~8% of tare (insulation, brass, coatings, rubber)
- **EF sources**: GREET2 2025 (metals, rubber), ICE v4.1 (mineral wool, coatings), eGRID 2023

### Key Sourced Values

- Tare weight: 86,350 lbs — GBRX spec sheet (Jan 2021)
- Tank OD: 9'-10 3/4" (3.016 m) — GBRX spec
- Tank outside length: 53'-4 7/8" (16.28 m) — GBRX spec
- Shell thickness: 7/16" (11.11 mm) — 49 CFR 179.201-1
- Jacket thickness: 11 gauge (3.038 mm) — 49 CFR 179.200-4
- Steel density: 7,850 kg/m³ — AZoM (ASTM A516 Gr 70)
- US steel mix: 33% BF-BOF / 67% EAF — Hasanbeigi & Springer 2019
- Grid EF: 0.367 kgCO₂e/kWh — EPA eGRID 2023
- Recycling rate: 96% — GREET2 Mat_Sum B19
- Service life: 50 years — AAR Rule 88 / OT-24
- Insulation thickness: 4 inches — UTLX build spec
- Insulation density: 113 kg/m³ — ESTIMATE, midpoint of Knauf EPD range (25–200 kg/m³)
- Mineral wool EF: 1.25 kgCO₂e/kg — ICE v4.1
- Coatings EF: 2.152 kgCO₂e/kg — ICE v4.1
- Brass composition: Cu 70% / Zn 30% — Copper Dev. Assn. (C26000)

### V16 → V17 Changes (for reference, not for inclusion in external models)

V16 decomposed the BOM into 25+ components with individual weights. Most component weights
(wheels, axles, trucks, couplers, brakes, valves) were unsourced engineering estimates. V17
recognizes that a DOT-111 is ~93% steel and simplifies to steel + 4 non-steel categories.
Coil banks and other steel sub-components were removed from the BOM because they're steel,
they get the steel EF, and itemizing them added complexity without changing the result. The
EoL method was changed from avoided burden to cut-off because the blended production EF
already reflects recycled content, making an additional EoL credit a double-count.

## Failure Modes to Avoid

These are patterns that have occurred in previous iterations. They are listed here because they
actually happened, not as theoretical concerns. Each one cost hours of rework.

1. **Citing a source that doesn't say what you claim.** This is the #1 failure mode. Example:
   citing an Engineering Toolbox page about thermal conductivity as a source for density.
   Example: citing GREET column AQ (recycled lead) as rubber. The fix is simple: open the
   source and read it before citing it. Every time.

2. **Fake-authority ranges.** Stating "80–200 kg/m³" or "1.3–2.0 GJ/t" without sourcing the
   range. This dresses up an estimate with false precision. If you have a source for the range,
   cite it. If you don't, say "unsourced engineering estimate" without the range.

3. **Using outdated EF database versions.** ICE v2.0 when v4.1 exists. This signals carelessness.
   Always check for the latest version before building.

4. **Breaking out steel sub-components.** If a component is steel and gets the blended steel EF,
   it belongs in the steel residual. Itemizing it separately (e.g., coil banks, truck assemblies)
   creates unsourced estimates that add complexity without changing CTGrave. The only reason to
   break out a component is if it uses a different EF than the bulk category.

5. **EoL method inconsistent with production EF.** Using a blended (recycled-content) production
   EF AND giving an avoided-burden EoL credit double-counts the recycling benefit.

6. **Audience-inappropriate content.** Verbose methodology deep-dives, internal comparison
   sections, prior-version references in an external-facing model. The verifier doesn't care
   about V16. A separate "Key Sources" section that duplicates inline citations is redundant
   noise (though a concise reference list is fine).

7. **Hard-coded derived values.** If 118.75 inches = 9 feet × 12 + 10.75 inches, the cell must
   contain the formula =9*12+10.75, not the number 118.75. Same for 0.4375 (must be =7/16).

8. **Fabricated specifics.** Inventing precise details that sound authoritative but have no
   source. Round numbers with honest uncertainty are better than precise numbers with
   fabricated provenance.

9. **Calling derived-from-estimates "sourced."** If the parent values are estimates, the derived
   value is also uncertain. Label it "DERIVED from estimates."

10. **Saying "0 errors, clean build" without checking substance.** Formula parse checks
    (no #VALUE! errors) are necessary but not sufficient. The build can be formula-clean and
    still have bogus citations, wrong GREET columns, or outdated EFs. Substance verification
    (source content matches claims) is separate from formula verification.

## Isometric GHG Accounting v1.0 — Governing Standard

All LCA models built by this skill will be evaluated against the **Isometric GHG Accounting
Module v1.0** (https://registry.isometric.com/Module/ghg-accounting/1.0). A condensed summary
of requirements is in `references/ghg-accounting-v1.0-summary.md`. Key points that directly
affect model construction:

### Principles (ISO 14064-2:2019)
Six principles govern: Relevance, Completeness, Consistency, Accuracy, Transparency,
Conservativeness. The last two are most operationally important for model building:
- **Transparency**: Every value must be traceable. Aligns with the sourcing standard above.
- **Conservativeness**: When two options of equal data quality exist, choose the one that
  results in higher emissions (lower net removals).

### Lifecycle Coverage
Embodied emissions must cover **full A1-C4** per ISO 21930 / EN 15804:
- A1-A3: Product stage (raw materials, transport to factory, manufacturing)
- A4-A5: Construction (transport to site, installation)
- B1-B7: Use stage (maintenance, repair, replacement, operational energy)
- C1-C4: End of life (deconstruction, transport, waste processing, disposal)

All modules must be declared, even if zero. Missing modules must be justified.

### Data Quality
Isometric assesses data on five criteria (Reliability, Completeness, Age, Geography,
Technology), each rated High/Medium/Low. For our BOM-based models:
- Manufacturer specs with weights → **High** reliability for activity data
- Geometry-derived masses from regulatory dimensions → **Medium** reliability
- Engineering estimates with no source → **Low** reliability (must be labeled)
- GREET/ICE emission factors → **High** reliability for EFs
- EF age limits: most current available; >6 years = Low quality

### Materiality
An SSR may be excluded if < 1% of net removals. All excluded SSRs collectively must also
be < 1%. EEIO/spend-based is acceptable for screening only — not for final accounting of
included items.

### Amortization
Capital goods emissions may be amortized three ways: (1) single deduction, (2) annual over
design life, (3) per tonne removed. Design life must come from manufacturer info or industry
best practice. Cap: 20 years (v1.1). Must report residual emission debt at every verification.

### Reputable EF Sources (Isometric-approved)
GREET, CA-GREET, UK DESNZ/DEFRA, Ecoinvent, LCA Commons, OpenLCA/SimaPro/GaBi.
For Charm models specifically, use: **GREET, GLEC, ICE (latest version), EPA eGRID**.

---

## GREET2 Reference

When working with the uploaded GREET2 file:

- **Location**: Check `lca-model-builder/Emission Factor Databases/` in the MRV Expert folder
- **Mat_Sum sheet**: Row 65 has per-lb GHG values. Columns vary by material.
  Conversion: value_in_grams_per_lb × 2.20462 / 1000 = kgCO₂e/kg
- **Column verification is mandatory.** Read the header at row 44 before using any value.
  Known correct mappings: B=Virgin Steel, C=Recycled Steel, BE=Copper, BF=Zinc, BU=Rubber.
  Known trap: AQ=Recycled Lead (NOT rubber).
- **C.Iron sheet**: Row 81. Column G = cast iron, Column I = wrought/forged iron.
  Per-lb columns (NOT per-ton which uses short tons).
- **Recycling rate**: Mat_Sum cell B19 (96% for steel)
- **Always show the conversion arithmetic** in source notes so a reviewer can verify.
