# Charm Industrial — Isometric Registry VCM Project

**PDD:** "Charm Industrial Great Plains Bio-Oil Sequestration" v1.10 (2025/09/22)
**Protocol:** Bio Oil Geological Storage v1.0 (Isometric Certified)
**Crediting period:** 2024/03/01 - 2029/03/01 (5 years, max allowed)

## What Charm Does
Charm converts non-merchantable biomass to bio-oil via pyrolysis and permanently injects it into geological formations for carbon sequestration, earning credits on the Isometric voluntary carbon market registry.

## Supply Chain Overview

### Bio-Oil Sources
**1. Charm Industrial (Fort Lupton, CO)**
- Facility operational for carbon removal production from 8/12/24 (shared-use with R&D)
- Feedstocks: Non-merchantable woody biomass from CSFS-funded wildfire mitigation projects
  - MacArthur Gulch, Arkansas Mountain, Arroyo Chico (Ponderosa Pines/Douglas Firs)
- Biomass supplier: Altitude Forestry (Larkspur, CO)
- Pyrolysis produces 3 products: "oily" bio-oil, "aqueous" bio-oil (injectable since mid-2025), biochar
- R&D use is outside system boundary; emissions allocated by pyrolyzer up-time

**2. AECN (AE Cote-Nord Canada Bioenergy Inc., Port-Cartier, QC)**
- Commissioned 2018, expected to operate through 2042
- Feedstock: Sawdust and shavings from Arbec sawmill (waste product, no counterfactual use)
- LCA updated annually or after major operational changes

### Pre-Processing
- AJ's Services, El Dorado, KS
- Bio-oil treated to meet UIC/KDHE requirements before injection
- Consumables: liquid caustic soda (LCS), off-spec salt from nearby Morton factory

### Injection Sites

**KS — Vaulted Deep (Hutchinson, KS)**
- Storage: Underground salt caverns, 500+ feet deep, 10,000+ year durability
- Permit: Class V UIC, KS-05-155-003 (KDHE), valid 2022/08/02-2027/08/02
- Buffer Pool: 2% (Very Low Risk)

**LA — Basco 6 EW (Evangeline Parish, LA)**
- Former orphaned Class II SWD well, converted to Class V
- Storage: Lower Miocene sandstone formation ~3,500' below wellhead, 1,000+ year durability
- Permit: IMD 2025-05 EW (LDENR), valid 2025/08/08-2030/08/07; MASIP = 455 psi
- Buffer Pool: 5% (Low Risk)

## Carbon Accounting

### Gross Removal Calculation
1. Bio-oil sampled after sparging (before LCS/salt addition)
2. CHN tested at ISO-accredited lab -> carbon % by mass
3. Mass of Bio-Oil Injected = Total Injectate Mass - mass of LCS - mass of salt
4. Gross CO2e = Mass of Bio-Oil Injected x C% x (44/12)

### Net CDR
Net CDR = Gross sequestration - all project emissions (transport, pyrolysis, pre-processing, injection, embodied, consumables, sample transport, waste disposal)

### Emissions Factors / Tools
- Transport: GLEC v3.0 (Distance-Based Method, ton-miles)
- Embodied: GREET 2023, EcoInvent, NAICS Supply Chain EFs, USLCI, ICE, Athena
- Electricity: EPA eGrid, adjusted by Green-e for residual mix
- LCS: GREET emissions factor
- AECN process: GHGenius software (vendor LCA)
- Tailgas (Charm): compliance emissions testing per feedstock type

### Uncertainty Approach
- Method: Variance propagation (sensitivity analysis; parameters with >1% effect get uncertainty factors)
- Scale error: 160 lbs (truck), 0.28% (fuel meter), 2.045% (flow meter), 2% (utility meter), 0.4% RSD (LECO CHN instrument)

## Finite Timelines to Track
- Crediting period ends: 2029/03/01 (must re-validate to continue)
- Vaulted KS permit expires: 2027/08/02 (renewal needed)
- Basco 6 LA permit expires: 2030/08/07

## Additionality Demonstration
- **Financial:** Revenue only from CDR credits; biochar co-product revenue far below production cost; no 45Q tax credit
- **Environmental:** Sequesters carbon that would otherwise decompose/emit
- **Regulatory:** Compliant with UIC regulations but not required by them

## Leakage Assessment
- Charm feedstock: CSFS-funded wildfire mitigation -> no leakage risk
- AECN feedstock: SFI-certified, provincially-managed -> no leakage risk
