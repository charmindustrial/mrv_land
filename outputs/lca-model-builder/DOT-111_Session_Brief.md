# DOT-111 Embodied Emissions Model — Session Brief

**Date**: 2026-04-08
**Model version**: V16
**Purpose**: Carry context into the next session. Upload this file at session start.

---

## Current State

The DOT-111 embodied emissions model is a materials-based cradle-to-grave Excel workbook that replaces the prior cost-based EEIO methodology. V16 is built and outputs are generated.

### Output Files (in MRV Expert folder)
- `DOT-111_Embodied_Emissions_Model_INTERNAL.xlsx` — V16, 156 formulas, 0 errors
- `DOT-111_Embodied_Emissions_Model.xlsx` — V16 external version, 152 formulas, 0 errors
- **Cradle-to-Grave total**: 14.34 MT CO₂e
- **Cradle-to-Gate total**: 66.19 MT CO₂e

### Build Script
- `build_dot111_v16.py` — Python/openpyxl script that generates both workbooks from scratch
- Located in session working directory (will need to be re-uploaded or rebuilt in new session)

---

## What's Been Done (V1–V16)

1. BOM decomposition of DOT-111 railcar into material groups: shell/heads (TC-128B steel), structural frame (A572-50), trucks/bogies, couplers, valves, coatings, insulation, miscellaneous
2. Emission factors sourced from R&D GREET2 2025 (Mat_Sum row 65, C.Iron row 81), ICE v2.0, EPA eGRID
3. Full lifecycle: A1-A3 (production), C1-C4 (end-of-life recycling credit at 96% steel recovery per GREET)
4. Truck component weights (wheels, axles, frames, wheelsets) reclassified as **unsourced engineering estimates** after exhaustive search proved no public authoritative sources exist (AAR MSRP standards are proprietary/paywalled)
5. Coupler weight similarly reclassified as unsourced estimate
6. All forum citations (trainorders.com), blog citations (train-wheels.com), and marketplace citations (made-in-china.com) removed
7. Internal version includes change notes, methodology narrative, and full source documentation
8. External version strips internal notes for verifier delivery

---

## Key Decisions & Precedents

### Sourcing Standard
- **Acceptable sources**: Manufacturer spec sheets, regulatory filings (49 CFR), peer-reviewed databases (GREET, ICE, GLEC, eGRID), government publications (FRA, DOT), academic papers
- **Manufacturer product listings with weights** (e.g., ship weight) ARE acceptable even if not a formal spec sheet
- **Proxies** are OK if the proxy source is linked and the analogy is justified
- **NOT sources**: Forum posts, blogs, marketplace listings, AI-generated content, unsourced web pages
- **Verifiability test**: "Can someone who has never seen the equipment click a link and verify this claim?"

### Classification Labels
Every value in the model gets one of:
- **SOURCED** — linked to a specific, verifiable document
- **DERIVED** — calculated from other values (inherits quality of parents)
- **ESTIMATE** — engineering judgment, no authoritative source; explicitly labeled as such
- **PROXY** — sourced value for an analogous item, with justification
- **PLUG** — placeholder pending better data

### Truck Component Weights (the hard-won lesson)
No publicly available authoritative source exists for individual freight car truck component weights. AAR M-107/M-208 and MSRP standards cover these but are proprietary. Standard Steel (Lonsdale et al. 2001) gives wheel load capacity (35,750 lbs) but NOT wheel mass. The 900 lb wheel weight, 2,300 lb wheelset, 10,000 lb complete truck — all are engineering estimates carried by industry convention. The model labels them honestly as such.

---

## Known Issues / Open Items

1. **Max has additional feedback on the model** — deferred from previous session ("I've got things to talk about"). Ask what's on his mind.
2. **B-stage modules (Use phase)** not yet explicitly declared — Isometric GHG Accounting v1.0 requires declaring all lifecycle modules even if zero. Should add a section noting B1-B7 = 0 with justification (railcars are passive assets, no operational energy).
3. **Amortization method not yet selected** — model presents total embodied emissions but doesn't specify which of the three Isometric amortization options Charm will use. This is a project-level decision, not a model decision.
4. **Shared infrastructure allocation** — if the railcar fleet serves multiple injection sites, proportional allocation per Isometric §4.1 would apply. Not yet modeled.
5. **A4-A5 (transport to site, installation)** — not yet included. Would need delivery distance from manufacturer to Charm's facility.

---

## Failure Modes to Watch For

These are patterns that have caused problems across V1-V16. The LCA skill documents them but worth restating:

1. Citing forums/blogs/marketplaces as authoritative sources
2. Presenting estimates as sourced values
3. Copying numbers from GREET without showing the unit conversion arithmetic
4. Algebraic errors in derived values where the note text doesn't match the formula result
5. Conflating load capacity with mass (e.g., wheel load rating ≠ wheel weight)
6. Calling derived-from-estimates "sourced"
7. Hard-coded magic numbers that can't be independently verified

---

## Skill Reference

The **lca-model-builder** skill is installed and contains:
- Full sourcing standard and classification system
- Isometric GHG Accounting v1.0 requirements (condensed from the 72-page PDF)
- GREET2 reference (sheet names, row numbers, conversion formulas)
- All seven failure modes
- DOT-111 current model state summary

The skill should auto-trigger for any LCA or embodied emissions work.
