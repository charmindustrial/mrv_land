# Isometric Modules — Key Requirements for Charm Industrial

## 1. Energy Use Accounting Module v1.3

### Core Formula
`CO2e Energy,RP = CO2e Electricity,RP + CO2e Fuel,RP`

### Electricity — EAC (REC) Rules
**Non-Intensive Facilities (<=200 GWh/year):** 12-month temporal matching (18 months permitted under documented market constraints)
**Intensive Facilities (>200 GWh/year):** Hourly matching mandatory where available

### Fuel
`CO2e Fuel,RP = SUM(m_fuel,k x f_fuel,k)` — full life-cycle (well-to-wheel for transport fuels)

### BCUs for Low-Carbon Fuels
Must demonstrate additionality; verified per ISCC CORSIA, RSB CORSIA (aviation), ISCC EU, RSB EU RED (road/marine).

### Monitoring
- Electricity: utility-grade power meters, hourly minimum, <=2% accuracy
- Fuel: mass, volume, or heating value via meters, container weights, utility bills, or manufacturer specs
- Records: minimum 5 years retention including calibration documentation

## 2. Biomass Feedstock Accounting Module v1.3

### Three Dimensions Required
1. **Sustainability Criteria** — reviewed every reporting period
2. **Counterfactual Storage** — carbon that would remain stored absent project receives no credits; assessments valid 10 years
3. **Market Leakage Evaluation** — multiple pathways (ML1-ML7)

### Critical Equations
```
CO2eCounterfactual = CO2eFeedstock - CO2eCounterfactualEmissions
CO2eCounterfactualEmissions = min(15-year emissions, feedstock CO2e - 50-year storage)
```

### Prohibited Feedstocks
- Produced for bioenergy
- Suitable for long-lived wood products
- Substantial market leakage risks from land-use change or production incentives

## 3. Biomass or Bio-oil Storage in Salt Caverns Module v1.1 / v1.2

**Applies to:** Vaulted Deep (Hutchinson, KS) — Charm's KS injection site

### Reversal Risk & Buffer Pool
- **Very Low Risk** -> **2% buffer pool**

### Monitoring Requirements
**Per Injection Batch:** Total carbon content, pH, temperature, chloride concentration, density, TAN, water content
**System Integrity:** Annual corrosion monitoring; annual external mechanical integrity testing
**Migration/Reversal:** Continuous cavern pressure; periodic sonar surveys; quarterly fill depth; displaced brine analysis per batch

## 4. Bio-oil Storage in Permeable Reservoirs Module v1.1

**Applies to:** Basco 6 EW (Evangeline Parish, LA) — Charm's LA injection site

### Reversal Risk & Buffer Pool
- **Low Risk** -> **5% buffer pool** (higher than salt cavern's 2%)

### Required Site Characterization
Adequate sequestration zone volume, porosity, permeability; confining system; freedom from transmissive faults/fractures; no seismic risks.

### Operational Monitoring
**Injection Parameters (per batch):** pH, density, viscosity, TAN, carbon content, delta-13C signature, MASIP continuous monitoring
**System Integrity:** Corrosion monitoring every 6 months; annual mechanical integrity demonstrations

## Complete Module Registry (early 2026)

| Module | Version | Status |
|--------|---------|--------|
| Energy Use Accounting | v1.3 | Certified |
| GHG Accounting | v1.1 | Certified |
| Embodied Emissions Accounting | v1.0 | Certified |
| Transportation Emissions Accounting | v1.1 | Certified |
| Environmental and Social Safeguards | v1.0 | Pending |
| Biomass Feedstock Accounting | v1.3 | Certified |
| Bio-oil Storage in Permeable Reservoirs | v1.1 | Certified |
| Biomass and Bio-oil Storage in Permeable Reservoirs | v1.0 | Pending |
| Biomass or Bio-oil Storage in Salt Caverns | v1.1 | Certified |
| Biomass or Bio-oil Storage in Salt Caverns | v1.2 | Pending |
| Biochar Storage in Soil Environments | v1.2 | Certified |
