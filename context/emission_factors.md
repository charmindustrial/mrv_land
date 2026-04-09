# Standard Emission Factors — 2026

Updated annually (~March) for the upcoming year. These factors underpin Charm's carbon removal credit accounting and must be defensible for third-party verification.

**File location:** Standard Emission Factors + Calculations - 2026.csv

## Key Sources
- GREET 2024/2025 (Argonne National Lab)
- GLEC Framework V3.2 2025
- USEPA / USDOT
- Green-E
- NAICS Supply Chain Emissions Factors
- ICE Database (for materials not in GREET)
- AECN-specific LCA (updated annually)

## Transport Emission Factors

| Item | Factor | Units | Source |
|------|--------|-------|--------|
| Diesel WTW | 3.87 | kgCO2e/kg fuel | GLEC V3.2 2025 |
| Gasoline WTW | 3.74 | kgCO2e/kg fuel | GLEC V3.2 2025 |
| LPG WTW | 3.63 | kgCO2e/kg fuel | GLEC V3.2 2025 |
| Tanker truck process | 1.143e-04 | MTCO2e/t-mi | GLEC V3.2 2025 |
| Flatbed truck process | 1.384e-04 | MTCO2e/t-mi | GLEC V3.2 2025 |
| Rail transport process | 2.5910374e-05 | MTCO2e/t-mi | GLEC V3.2 2025 |
| Tanker truck embodied | 2.3756059e-04 | MTCO2e/mi | GLEC V3.2 2025 |
| Non-tanker truck embodied | 1.927908256e-04 | MTCO2e/mi | GLEC V3.2 2025 |

## AECN Production

| Item | Factor | Units | Source |
|------|--------|-------|--------|
| AECN production process | 0.10402 | MTCO2e/MT oil | AECN LCA H1 2026 |
| AECN production embodied | 0.02116 | MTCO2e/MT oil | AECN info + NAICS |

## Grid Electricity & RECs

| Item | Factor | Units | Source |
|------|--------|-------|--------|
| Grid electricity — KS | 4.655516852e-04 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Grid electricity — CO | 4.890238251e-04 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Grid electricity — LA | 4.630140342e-04 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Wind RECs — KS | 1.002719674e-05 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Solar RECs — CO | 3.664154577e-05 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |
| Solar RECs — LA | 3.664154577e-05 | MTCO2e/kWh | Green-E/USEPA/GREET 2024 |

## Materials (Embodied Emissions)

| Material | EF | Unit | Source |
|---|---|---|---|
| Steel (virgin, stamped) | 2.818 | kgCO2e/kg | GREET 2025 |
| Stainless Steel | 0.720746 | kgCO2e/kg | GREET 2024 |
| Rubber | 3.372324 | kgCO2e/kg | GREET 2024 |
| HDPE | 1.702514 | kgCO2e/kg | GREET 2024 |
| LDPE | 1.980563 | kgCO2e/kg | GREET 2024 |
| Concrete (ready-mix) | 0.086234 | kgCO2e/kg | GREET 2024 |
| Liquid Caustic Soda (50% NaOH) | 0.9535517371 | kgCO2e/kg | GREET 2024 |
| Aluminum (NA cradle-to-gate) | 5.65 | kgCO2e/kg | ICE Database 4.0 |
| Limestone | 8.179 | kgCO2e/T | GREET 2025 |

## Other

| Item | Factor | Units |
|------|--------|-------|
| LCS (50% NaOH) | 0.9535517371 | MTCO2e/T LCS |
| Industrial machine (heavy, unspecified) | 2.067 | kgCO2e/kg (ecoinvent) |

## Rules
- Always reference EFs from the Standard EF CSV via cell formula — never hardcode in calc docs
- EFs are verified against Certify at the start of each reporting period
- Until Mangrove automates backend EF updates, this is a manual check
