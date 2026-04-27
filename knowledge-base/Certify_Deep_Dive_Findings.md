# Isometric Certify Deep Dive: Oil Type Reporting & Operational Evolution

## Overview

Analysis of all 13 GHG Statements in Certify (12 verified, 1 unsuccessful) and cross-referenced with local PDF verification/GHG statement reports. Covers March 2024 through March 2026.

---

## GHG Statements Chronology

| # | Period | Removals | Net tCO2e | Verifier | Injection Site | Key Oil Types |
|---|--------|----------|-----------|----------|---------------|---------------|
| 1 | 12 Mar – 30 Apr 2024 | 5 | 107.21 | FuturePast | Vaulted (KS) | AECN only |
| 2 | 01 May – 31 May 2024 | 10 | 236.23 | — | Vaulted (KS) | AECN only | VERIFICATION UNSUCCESSFUL |
| 3 | 01 Jun – 06 Dec 2024 | 9 | 246.73 | 350Solutions | Vaulted (KS) | AECN only |
| 4 | 07 Dec 2024 – 31 Jan 2025 | 15 | 592.66 | 350Solutions | Vaulted (KS) | AECN + likely Charm |
| 5 | 01 Feb – 31 Mar 2025 | 22 | 1,002.95 | 350Solutions | Vaulted (KS) | AECN + Charm |
| 6 | 01 Apr – 31 May 2025 | 24 | 1,014.57 | 350Solutions | Vaulted (KS) | AECN + Charm WODO |
| 7 | 01 Jun – 31 Jul 2025 | 16 | 555.95 | 350Solutions | Vaulted (KS) | AECN + Charm |
| 8 | 01 Aug – 15 Aug 2025 | 4 | 135.39 | 350Solutions | Basco (LA) transition | AECN + Charm |
| 9 | 16 Aug – 08 Sep 2025 | 10 | 166.40 | 350Solutions | Basco (LA) | AECN + Charm |
| 10 | 09 Sep – 30 Sep 2025 | 10 | 291.85 | 350Solutions | Basco (LA) | AECN + Charm |
| 11 | 01 Oct – 06 Nov 2025 | 17 | 454.71 | 350Solutions | Basco (LA) | AECN + Charm WODO + Aqueous |
| 12 | 07 Nov 2025 – 31 Jan 2026 | 3 | 43.47 | 350Solutions | Basco (LA) | AECN + Charm |
| 13 | 01 Feb – 02 Mar 2026 | 30 | 764.14 | 350Solutions | Basco (LA) | AECN only (no Charm injected) |

---

## Oil Type Identification in Certify

### 1. AECN Oil
- **Source**: AECN facility in Quebec, Canada (Ensyn/Honeywell UOP pyrolysis of waste wood)
- **Transport**: Tanker truck (Quebec → injection site) or rail car (via SOPOR Quebec)
- **How identified in Certify Datapoints**:
  - "Origin Bio-Oil Mass - AECN" (most recent format)
  - "verified mass for lot XXX" (earlier format)
  - Transport emissions labeled "Tanker Truck Transport" or "Railcar"
- **How identified in Certify Components (Pyrolysis)**:
  - "AECN Pyrolysis Process Emissions" or "AECN Pyrolysis Process E"
  - "AECN Pyrolysis Embodied Emissions" or "AECN Pyrolysis Embodied"
  - In most recent format: "Carbon Intensity - AECN Pyrolysis Process Emissions"
- **Emission factors**:
  - Process: 89.40 → 126.78 (H2 2024) → 127.04 (H1 2025) → 0.10 tCO2e/t (current) kgCO2e/t
  - Embodied: 21.16 kgCO2e/t → 0.02 tCO2e/t (current)
  - Note: The dramatic apparent change reflects unit/methodology shifts, not actual emission changes

### 2. Charm WODO (Wood-Derived Oil)
- **Source**: Charm's pyrolysis facility in Fort Lupton, CO (started Aug 2024)
- **Process**: Wood chips → high-temp pressurized reactor → pyrolysis oils (the "oil fraction")
- **Transport**: Flatbed truck (in tote tanks) from Fort Lupton → El Dorado KS → injection site
- **First appearance**: Feb-Mar 2025 period (statement #5), confirmed in Apr-May 2025 (#6)
- **How identified in Certify Datapoints**:
  - "(Production Period X) Production Emissions emission factor" — e.g., 0.73 kgCO2e/kg
  - Separate measurement entries for Charm oil mass
  - "Flatbed Truck Transport Embodied/Process Emissions" for transport
- **How identified in Certify Components (Pyrolysis)**:
  - "(Production Period X) P..." — labeled by production period, NOT by "Charm" name
  - Each production period has its own carbon intensity value
- **Transport indicator**: Flatbed Truck (vs Tanker Truck for AECN)
- **Key distinction from AECN**:
  - Tracked by PRODUCTION PERIOD, not by pyrolyzer name
  - Uses spreadsheet-based CI calculation (dMRV not yet fully integrated as of Mar 2026)
  - Not pretreated (no sparging/LCS) when injected at Basco

### 3. Charm Aqueous (Quench Oil / Wood Vinegar)
- **Source**: Same Charm Fort Lupton facility — the "aqueous fraction" / "wood vinegar"
- **Process**: Hot pyrolysis gases quenched with water → aqueous product
- **Status**:
  - Jul 2025 VR: "shipping both the bio-oil fraction AND the Quench Oil / Wood Vinegar fraction... This fraction is not yet being injected"
  - Dec 2025 VR: "Bio-oil from AECN and aqueous fraction product from Charm pyrolyzers are shipped" — now being blended and injected
  - Mar 2026 VR: "injections of bio-oil (oil and aqueous phases)"
- **First injection**: Likely Oct-Nov 2025 period (statement #11) based on verification report language
- **In Certify**: Not explicitly distinguished from WODO at the component level. Both Charm oil types appear under Production Period emissions. The distinction is tracked in the "charm contents" sheets at the batch/reporting package level, not as separate Certify component types.

### 4. Kerry Oil (NEW - not yet in any verified statement)
- **Source**: Kerry (details TBD)
- **Transport**: Comes in totes (similar to Charm oil → flatbed)
- **Status**: Not yet verified; Max noted this is new and needs to be sorted out

---

## Certify Removal Component Structure (Evolution)

### Earliest Format (Mar-Apr 2024, FuturePast)
```
Removal (e.g., 31.35 tCO2e)
├── Sequestrations: Injection → Removal XXX (gross CO2e)
├── Removal Activities:
│   ├── Injectant Transport (per lot: Tanker Truck Transport P + E)
│   ├── Injection (LCS + Samples per lot)
│   └── Pyrolysis (AECN Pyrolysis Process E + Embodied per lot)
├── Counterfactuals: 0
├── Losses: 0
├── Reductions: 0 (no BCUs used yet)
└── Total = Sequestrations - Activities
```
- 16 datapoints per removal
- Lot masses reported directly (no attribution factors)
- Named "Measurement XXXX"

### Mid Format (Jun-Dec 2024, 350Solutions)
```
Same structure, but:
├── AECN Pyrolysis now has time-period prefix: "H2 2024 AECN Pyrolysis..."
├── Attribution factors introduced (lots allocated fractionally to removals)
├── BCU certificates appear in Reductions
└── 21 datapoints per removal
```

### Apr-May 2025 (Charm Oil Introduced)
```
Removal Activities now include:
├── Injectant Transport:
│   ├── Flatbed Truck Transport (Charm oil lots in totes)
│   └── Tanker Truck Transport (AECN lots)
├── Pyrolysis:
│   ├── (Production Period X) P... (CHARM OIL)
│   └── AECN Pyrolysis Process/Embodied (AECN)
└── 28 datapoints per removal
```
- Flatbed Truck has its own emission factors
- Production Period emissions: 0.73 kgCO2e/kg (vs AECN 127+ kgCO2e/t)

### Current Format (Feb-Mar 2026, Mangrove/dMRV)
```
Completely restructured:
├── Descriptive names instead of "Measurement XXXX"
├── Only 14 datapoints (streamlined)
├── Source files now have real names (e.g., "Billing Documents 2309-T.pdf")
├── BCUs broken out by category:
│   ├── BCUs - Applied to injection site diesel emissions
│   ├── BCUs - Applied to injection site waste disposal emissions
│   ├── BCUs - Applied to pre-treatment waste disposal emissions
│   ├── BCUs - Applied to pre-treatment diesel emissions
│   └── BCUs - Applied to Bio-Oil Transport Process Emissions
├── AECN Production split:
│   ├── AECN Production Embodied Emissions (0.02 kgCO2e/kg)
│   └── AECN Production Process Emissions (0.10 kgCO2e/kg)
└── Rail transport now separately tracked with own emission factors
```

---

## Major Operational Evolution Timeline

### Phase 1: Early Operations (Mar-May 2024)
- AECN oil only
- Vaulted Deep (Kansas salt caverns) as injection site
- FuturePast as verifier
- May 2024: VERIFICATION UNSUCCESSFUL

### Phase 2: Recovery & Stabilization (Jun 2024 - Jan 2025)
- 350Solutions takes over as verifier
- Still AECN only at Vaulted Deep
- Time-period-specific emission factors introduced (H2 2024)
- BCUs first used for emissions reductions
- Attribution factors for lot allocation

### Phase 3: Charm Oil Introduction (Feb-May 2025)
- Charm's Fort Lupton pyrolysis begins producing oil (Aug 2024)
- Charm WODO first injected (~Feb 2025)
- Flatbed truck transport for tote-delivered Charm oil
- Production Period tracking for Charm emissions
- Aqueous fraction being shipped but NOT yet injected (as of Jul 2025 VR)

### Phase 4: Site Transition to Basco, Louisiana (Aug-Nov 2025)
- Injection moves from Vaulted Deep (KS) to Basco (LA)
- Permeable reservoir instead of salt caverns
- Bio-oil Storage in Permeable Reservoirs Module v1.1 applied
- Rail spur construction at Basco (1.575 tCO2e sitework)
- On-site sparging capability built at Basco
- Charm aqueous fraction now being injected (~Oct 2025)
- Bio-oil spill at rail spur documented
- Standard 1.29% sparging mass deduction introduced
- Conservative injectate mass = MIN(scale ticket net, originating BOL mass)

### Phase 5: Current Operations (Nov 2025 - Mar 2026)
- All injection at Basco, LA
- AECN oil via tanker truck AND rail car
- Charm oil via flatbed (totes) — but no Charm oil injected in Feb-Mar 2026 period
- dMRV system (Mangrove) being integrated but Charm oil CI still via spreadsheet
- Inventory Reconciliation process accounts for outstanding production period oil
- Descriptive naming convention in Certify
- Monitoring transition for prior Vaulted injections ongoing

---

## Emission Factor Evolution

| Factor | Mar-Apr 2024 | Jun-Dec 2024 | Apr-May 2025 | Feb-Mar 2026 |
|--------|-------------|-------------|-------------|-------------|
| AECN Pyrolysis Process | 89.40 kgCO2e/t | 126.78 kgCO2e/t (H2 2024) | 127.04 kgCO2e/t (H1 2025) | 0.10 kgCO2e/kg (=100 kgCO2e/t) |
| AECN Pyrolysis Embodied | 21.16 kgCO2e/t | 21.16 kgCO2e/t | 21.16 kgCO2e/t | 0.02 kgCO2e/kg (=20 kgCO2e/t) |
| Tanker Truck Process | 0.08 kgCO2e/(km·t) | 0.08 | 0.07 (2025) | 0.07 |
| Tanker Truck Embodied | 0.0477 kgCO2e/km | 0.0477 | 0.0490 | 0.0490 |
| Flatbed Truck Process | N/A | N/A | 0.14 kg/(t·mi) | N/A (no Charm this period) |
| Flatbed Truck Embodied | N/A | N/A | 0.0401 kgCO2e/km | N/A |
| LCS Embodied | 1,540.65 kg/m³ | 1,540.65 | 1,505.78 (2025) | 1,505.78 |
| Charm Production (PP5) | N/A | N/A | 0.73 kgCO2e/kg | N/A |
| Samples for MRV | 4 kgCO2e | 4 | <1 kgCO2e (2025) | <1 kgCO2e |

---

## Key QA Checklist Implications

### For AECN oil batches:
- Transport: Tanker truck OR rail car (new)
- Pyrolysis emissions: AECN-specific, updated semi-annually (H1/H2)
- BOLs: 3 truck BOLs from AECN (railyard as destination for rail shipments)
- Pre-treatment: Sparging + LCS at Basco (1.29% mass deduction)

### For Charm WODO batches:
- Transport: Flatbed truck (totes)
- Production emissions: Tracked by Production Period, spreadsheet-based CI
- Supporting GHG data file: Required per production period
- No pre-treatment at Basco (injected as-is)

### For Charm Aqueous batches:
- Same transport as WODO (flatbed/totes)
- Same production period tracking
- Pre-treatment with LCS for pH adjustment
- First injected ~Oct 2025

### For Kerry oil batches (future):
- Comes in totes (like Charm → flatbed)
- Tracking nuances TBD

---

## Certify Platform Observations
- Transition to Certify/Mangrove dMRV is ongoing; some components still completed outside Certify
- Monitoring and Feedstocks sections may appear incomplete in Certify but are verified separately
- Naming conventions shifted from generic "Measurement XXXX" to descriptive names
- Source document references went from opaque to readable file names
- BCU structure evolved from single lump to categorized (by emission type being offset)
