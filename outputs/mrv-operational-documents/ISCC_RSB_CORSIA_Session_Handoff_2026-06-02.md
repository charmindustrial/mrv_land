# SAF Certification Schemes Session Handoff — 2026-06-02

## Purpose
Comprehensive summary of research conducted 2026-06-02 comparing ISCC PLUS, RSB Global Advanced Fuels, and RSB ICAO CORSIA certification pathways for Charm Industrial bio-oil as a SAF input. Intended to enable synthesis work in a new session without re-reading source documents.

---

## Source Documents

| Document | Version | Location | Key Pages |
|---|---|---|---|
| ISCC PLUS | V3.4.2, March 2024 | `.playwright-mcp/ISCC-PLUS.pdf` | p.6-9 (Scope, FSC), p.97 (GHG allocation), p.100 (GHG table) |
| ISCC PLUS 203-2 Chain of Custody | V1.1, Nov 2025 | `.playwright-mcp/ISCC-PLUS-203-2-Chain-of-Custody-v1-1.pdf` | p.4 (CoC def), p.17 (chem connectivity), p.21 (guardrails), p.26 (free attribution) |
| ISCC PLUS 202-5 Waste and Residues | V1.1, Nov 2025 | `.playwright-mcp/ISCC-PLUS-202-5-Waste-and-Residues-v1-1-1.pdf` | p.3 (residue definitions) |
| ISCC EU 202-3 Forest Biomass Principle 1 | Current | `.playwright-mcp/ISCC-EU-202-3-Forest-Biomass-ISCC-Principle-1.pdf` | p.6 (intro), p.11 (Level A/B), p.12-15 (harvesting criteria) |
| ISCC EU 202-4 Forest Biomass Principles 2-6 | Current | `.playwright-mcp/ISCC-EU-202-4-Forest-Biomass-ISCC-Principle-2-6.pdf` | p.7 (third-party audits), p.10 (management plan) |
| RSB GHG Calculation Methodology | V3.0, June 2025 (filed as V3.2) | `~/Desktop/rsb-std-01-003-01-v3.2.pdf` | p.15-16 (Table 1 allocation), p.34-35 (co-processing, flexible allocation) |
| RSB Standard for Advanced Fuels | V2.8 | Drive: MRV/SAF FCC/RSB/Global Advanced Fuel Certification docs/ | Annex IV (flexible attribution formulas) |
| RSB ICAO CORSIA | V1.6, June 2025 | `.playwright-mcp/rsb-std-12-001-corsia-v1.6-real.pdf` | p.14-16 (§3.4.5 co-processing, §3.4.7 energy allocation) |
| ICAO CORSIA LCA Methodology | V8, Nov 2025 | `.playwright-mcp/corsia-lca-methodology-v8.pdf` | Ch.6 (marginal approach, pp.123-126) |

Text extractions in `.playwright-mcp/`:
- `iscc-plus-current-text.txt` (V3.4.2)
- `iscc-plus-203-2-text.txt`
- `iscc-plus-202-5-text.txt`
- `iscc-eu-202-3-text.txt`
- `iscc-eu-202-4-text.txt`
- `rsb-std-01-003-01-text.txt`
- `rsb-std-12-001-corsia-text.txt`
- `corsia-lca-v8-text.txt`

---

## CORSIA (RSB ICAO CORSIA V1.6)

### Is free allocation of biogenic inputs to SAF output allowed?
**No.** RSB-STD-12-001 V1.6, §3.4.5.5, p.15:
> "Keep the mass balance material specific. It is not permitted to transfer the sustainability characteristic from one type of material to another type of material."

The bio-based proportion of each output is fixed by the material-specific conversion factor of the actual process. Operators cannot freely designate which output receives the biogenic credit.

### Allocation method at refinery
Marginal approach mandated. ICAO CORSIA LCA V8, Ch.6:
> "The marginal approach allocates all changes in inputs and outputs in a scenario with co-processing of biogenic feedstocks vs. a scenario without co-processing of biogenic feedstocks."
> "Since renewable fuels are only produced from the co-processing units, energy allocation was used among products for this process."

### GHG threshold
- Minimum 10% reduction vs. fossil comparator (89 gCO2e/MJ)
- Threshold: ≤80.1 gCO2e/MJ

---

## RSB Global Advanced Fuels (RSB-STD-01-003-01 V3.0 / RSB-STD-03-001)

**Note:** Document uses both numbers — RSB-STD-03-001 on cover page, RSB-STD-01-003-01 in footer. Same document. File named rsb-std-01-003-01-v3.2.pdf but internal text says Version 3.0, effective 24 June 2025. This is a Final Draft.

### Is free allocation of biogenic inputs to SAF output allowed?
**Yes, via Annex IV Flexible Attribution.** RSB-STD-01-010 V2.8, Annex IV (referenced in RSB-STD-01-003-01 §B.11). Operator can freely designate which output receives biogenic credit. Processing emissions are allocated by energy among biogenic and fossil inputs.

### Co-product allocation at pyrolyzer (bio-oil vs. biochar)
**Economic allocation mandatory.** RSB-STD-01-003-01 Table 1 (p.15-16):
> "Economic allocation shall be applied to RSB GLOBAL Advanced Products and RSB GLOBAL Advanced Fuels despite the energy nature of some of the products involved."

Economic value = market value as specified by the participating operator. Higher biochar market value → more burden on biochar → lower bio-oil CI.

This applies to intermediate products (bio-oil) not just final fuels. RSB-STD-01-003-01 §A.8 (p.15):
> "emissions shall be proportionally allocated between the fuel or its intermediate product and the co-products."
> "An intermediate product is the product of a specific stage within a larger, more complex production process that is further processed in sequential processes or stages to produce the system boundary's primary product."

Biochar is a co-product (not a waste/residue) because it is intentionally produced and sold. Wastes/residues receive zero allocation.

### GHG thresholds
- Standard: 65% minimum savings (Criterion 3.b, RSB P&C p.15), fossil comparator 90 gCO2e/MJ → threshold ≤31.5 gCO2e/MJ
- Transitional pathway (Criterion 3.c, RSB P&C p.16-17): available until 2035, requires public roadmap + annual audits. 2026 threshold: 50% savings → ≤45.0 gCO2e/MJ
- Both apply via RSB-STD-01-010 §2.1.1

---

## ISCC PLUS (V3.4.2, March 2024)

### Is ISCC primarily a sustainability certification, not a GHG methodology?
**Yes.** V3.4.2 p.5-6: GHG emissions savings are "on a voluntary basis under ISCC PLUS." V3.4.2 pp.6-7:
> "sector, such as the EU Reporting Obligation or the minimum GHG emission saving requirement, do not apply under ISCC PLUS."

GHG quantification is add-on 205-01 — entirely optional.

### Is free allocation of biogenic credit to SAF output allowed?
**Yes.** ISCC PLUS 203-2 p.26:
> "Under Free Attribution Approach, the system user can attribute the sustainability characteristics from the certified input materials to the products, within the system boundary and the guardrails described in Chapter 6.2. This attribution can be done irrelevant of the proportion of the certified input material to the other inputs and categorisation of the products. System users can freely attribute the sustainability characteristics from the certified input(s) to one (or multiple) products that can be attributed to."

Guardrails (203-2 p.21): chemical connectivity required, credits cannot exceed physical output, site-specific mass balance.

### GHG CI quantification — what methods are acceptable?
When add-on 205-01 is applied, emission factors can come from RED defaults, Ecoinvent, or other relevant databases or peer-reviewed literature. GREET not named but would likely qualify. ISO 14040/44 or ISO 14064/67 accepted methodologies. Energy or mass allocation both acceptable. Cradle-to-gate scope permitted if disclosed on sustainability declaration.

### Is there a GHG minimum savings threshold?
**No.** V3.4.2 pp.6-7 explicitly excludes the minimum GHG saving requirement from ISCC PLUS. V3.4.2 p.100 table confirms: ISCC PLUS column = "Voluntary application of addon 'GHG Emissions'" with no threshold.

### Co-product allocation at pyrolyzer (bio-oil vs. biochar)
V3.4.2 p.97:
> "The most suitable allocation method should always be used, e.g. if the main product is used energetically an energetic allocation should be applied."

Energy or mass both permitted. Carbon-mass balance (Charm's current method) is a form of mass allocation — allowed, but auditor could challenge it as less suitable than energy for an energetically-used product. ISCC PLUS is more flexible here than RSB (which mandates economic allocation).

### Forestry biomass — whole logs from wildfire fuel reduction

**Material classification:**
ISCC PLUS 202-5 p.3: Forestry residues = bark, tree tops, branches, leaves, needles. Whole logs = forest biomass (primary product), full requirements apply. Tops/branches/bark = forestry residues, lighter requirements.

**ISCC EU 202-3 and 202-4 apply to ISCC PLUS globally** (not EU-only). V3.4.2 pp.6-7 carve-out covers only minimum GHG saving requirement and EU Reporting Obligation — not land/forestry sustainability criteria.

**No-go areas (ISCC EU 202-3 Principle 1):**
Cannot source from primary forests, old growth forests, highly biodiverse forests, designated nature protection areas, peatland, wetlands. Primary forest defined by ABSENCE of human activity. Actively managed fuel reduction areas show human activity → NOT primary forest → eligible.

**Level A risk assessment (ISCC EU 202-3 p.11-14):**
If national/sub-national law confirms compliance with harvesting criteria, no further site-level action needed. Key criterion (e) explicitly allows above-increment harvest "temporarily justified due to documented forest pests, storms or other natural disturbances." US wildfire fuel reduction treatment plans + grant documentation satisfy Level A.

**Who needs ISCC certification:**
- First Gathering Point (FGP) = Charm's direct biomass supplier = must be ISCC certified
- Individual foresters upstream of FGP submit annual self-declarations to FGP — no standalone ISCC cert required
- Forest must be in ISCC-certified supply chain OR be FSC FM certified (V3.4.2 p.8)

**FSC FM pathway (V3.4.2 pp.8-9):**
FSC FM covers Principles 2-6 compliance only. ISCC EU 202-3 Principle 1 (no-go areas, land use, carbon stock) still requires separate additional verification even for FSC-certified forests. FGP must track: FSC FM certificate, origin, wood species, volumes.

**No additional forestry certification (FSC/PEFC/SFI) required** beyond the ISCC supply chain certification — unless choosing the FSC FM pathway as an alternative to full ISCC certification for the forest source.

---

## End-to-End ISCC PLUS Requirements Mapped to Charm's System

| Step | Requirement | Source | Harmony/Friction |
|---|---|---|---|
| 1. Biomass sourcing | FGP must be ISCC certified OR forest must be FSC FM certified. Individual foresters self-declare to FGP. Forest management plan or equivalent required. Level A risk assessment via treatment plans. | V3.4.2 p.8-9; 202-3 p.11; 202-4 p.10 | **Friction:** FGPs likely need new certification |
| 2. Biomass transport | Chain of custody maintained by each ISCC-certified entity, sustainability declarations forwarded | 203-2 p.4 | **Harmonizes** with existing traceability |
| 3. Biomass conversion | Charm's pyrolyzer must be ISCC certified as processing unit. All inputs/outputs/losses documented. | 203-2 p.21 | **Friction:** Charm needs ISCC certification |
| 4. Pyrolyzer co-product allocation | Energy or mass allocation acceptable. Energy preferred for energetically-used products. Carbon-mass balance permitted but auditor risk. | V3.4.2 p.97 | **Partial friction:** allocation method risk |
| 5. Bio-oil transport | Chain of custody maintained. Each entity ISCC certified. | 203-2 p.4 | **Harmonizes** |
| 6. FCC refinery | Refinery must be ISCC certified. Chemical connectivity bio-oil→SAF must be demonstrable. | 203-2 p.17 | **Friction:** Refinery needs ISCC certification |
| 7. Refinery emission allocation | Energy or mass allocation acceptable. No mandatory marginal approach. | V3.4.2 p.97 | **Harmonizes:** more permissive than CORSIA |
| 8. Biogenic credit allocation to SAF | Free attribution — operator freely designates which output receives biogenic credit, subject to chemical connectivity + physical output guardrails | 203-2 p.26, p.21 | **Strong advantage** vs. CORSIA |
| 9. Fuel transport | Chain of custody + sustainability declarations throughout | 203-2 p.4 | **Harmonizes** |
| 10. CI quantification | Voluntary add-on 205-01. Flexible emission factor sources (RED, Ecoinvent, peer-reviewed). Cradle-to-gate permitted. | V3.4.2 p.97, p.100 | **Harmonizes:** no mandated tool/formula |
| 11. GHG reduction vs. baseline | No minimum savings threshold. No required FF comparator. | V3.4.2 pp.6-7, p.100 | **Strong advantage** vs. RSB (65%/transitional) and CORSIA (10%) |
| 12. Verification | Single ISCC certification body covers sustainability + GHG in one audit. No separate VVB. | 202-4 p.7 | **Harmonizes:** simpler than current dual-track |

---

## Comparative Summary: ISCC PLUS vs. RSB Global vs. CORSIA

| Issue | ISCC PLUS | RSB Global Advanced Fuels | RSB ICAO CORSIA |
|---|---|---|---|
| Free biogenic credit allocation to SAF | YES — free attribution | YES — Annex IV flexible attribution | NO — material-specific conversion factor only |
| GHG minimum threshold | NONE | 65% (or 50-60% transitional to 2035) | 10% |
| Pyrolyzer allocation method | Energy or mass (flexible) | Economic (market value) mandatory | Energy mandatory |
| Refinery allocation method | Energy or mass (flexible) | Economic mandatory | Energy/marginal mandatory |
| Emission factor sources | RED, Ecoinvent, other relevant DBs | RED, ISCC, or individual calc per ISO 14040/44/64/67 | CORSIA methodology |
| GHG quantification requirement | Voluntary add-on | Mandatory when certifying | Mandatory |
| Supply chain certification | Every entity ISCC certified (or FSC FM for forest source) | Participants certified under RSB | Participants certified under RSB CORSIA |
| Forestry certification | ISCC FGP + (full ISCC or FSC FM for forest) | RSB-GUI-01-013-01 forestry requirements | N/A (not a forestry biomass pathway) |
| Verification body | ISCC CB covers all | RSB CB + VVB for GHG | RSB CB + VVB for GHG |

---

## Open Questions / Not Yet Researched

1. ISCC EU 202-3 Annex II (risk assessment template) — what specific evidence is required for US forest sourcing areas
2. ISCC EU 205 "GHG Emissions" system document — detailed GHG calculation formulas and allocation rules
3. RSB-GUI-PG-2025-02 — RSB Proactive Guidance on Co-Processing GHG Calculations (referenced in RSB methodology for co-processing rules)
4. RSB-STD-01-010 V2.8 Annex IV — full flexible attribution formulas (referenced but Annex IV not fully read this session)
5. Whether GREET specifically qualifies as a "relevant database" under ISCC PLUS §11.1 — not verbatim confirmed
6. Specific CI numbers for Charm's bio-oil under each scheme — worked example not completed in this session

---

## Prior Session Context (RSB-specific)

From RSB_Session_Handoff_2026-06-01.md: RSB Global vs. CORSIA comparison document and project plan already exist in `outputs/mrv-operational-documents/`. Key finding: at 0.8 tCO2e/t bio-oil CI, RSB Global fails even the transitional 2026 threshold (45.3 gCO2e/MJ upstream alone > 45.0 gCO2e/MJ threshold), while CORSIA passes easily (22.8 gCO2e/MJ << 80.1 gCO2e/MJ threshold). The open question from that session: is 0.8 tCO2e/t pre- or post-economic-allocation at the pyrolyzer?
