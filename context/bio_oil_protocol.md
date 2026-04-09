# Bio-Oil Geological Storage Protocol (v1.0 / v1.1 / v1.2)

**Protocol page:** https://registry.isometric.com/protocol/bio-oil-geological-storage

| Version | Status | Notes |
|---------|--------|-------|
| v1.0 | Certified (historical) | Charm's original crediting period |
| v1.1 | Certified | Adoption deadline Sept 13, 2025; used in Apr-May 2025 verification |
| v1.2 | Pending Certification | Current/upcoming version as of early 2026 |

## Eligibility Requirements
- Net-negative CO2e impact (net removal after all emissions)
- Sustainably sourced biomass per Biomass Feedstock Accounting Module
- No net environmental or socioeconomic harm
- Demonstrated additionality
- Storage duration >1,000 years in permitted geologic formations
- Located in US (or equivalent regulatory regime)
- Current UIC permits specifically authorizing bio-oil injection

**Ineligible:** bio-oil used for enhanced hydrocarbon recovery; non-compliant biomass sourcing.

## Core Calculation Formula
```
CO2eRemoval,n = CO2eStored,n - CO2eCounterfactual,n - CO2eEmissions,n
```
Calculated per injection batch.

### Emissions Categories
1. **Establishment** — equipment manufacture, transport, construction (amortized over project life)
2. **Operations** — feedstock sourcing, processing, conversion, injection, monitoring
3. **End-of-Life** — decommissioning
4. **Leakage** — market-induced emissions from biomass diversion
5. **Direct Emissions** — tailgas methane from pyrolysis

## Critical Measurement Requirements

### Bio-oil Carbon Content
- Minimum 1 sample per injection batch; 3 sub-samples per batch (or justified alternative)
- NREL procedure required for vapor pressure >3 psi; ASTM D5291 acceptable as alternative
- ISO 17025-accredited laboratory analysis mandatory
- Conservative estimation allowed after 30-batch baseline; random monthly sampling verification

### Mass Measurement
- Calibrated truck scales (legal-for-trade certified, NIST Handbook 44 compliant)
- Arrival/departure weight documentation required
- Alternative: calibrated flow meters with density measurement

## Uncertainty Options
- **(A)** Conservative estimates at <=16th/>=84th percentile
- **(B)** Variance propagation (Charm's current approach)
- **(C)** Monte Carlo

## Verification Requirements
- Independent third-party VVBs; site visits minimum every 2 years
- Materiality threshold: 5%
- Verifier expertise: biomass conversion AND geologic storage required
- Max 5 consecutive years per VVB, then rotation required

## Referenced Modules (v1.2 protocol)
| Module | Version | Category |
|--------|---------|----------|
| Energy Use Accounting | v1.3 | Cross-pathway Accounting |
| GHG Accounting | v1.0 | Cross-pathway Accounting |
| Biomass Feedstock Accounting | v1.3 | Feedstocks |
| Bio-oil Storage in Permeable Reservoirs | v1.1 | Storage |
| Biomass or Bio-oil Storage in Salt Caverns | v1.1 / v1.2 | Storage |
