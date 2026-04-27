# Isometric Standard v2.0 vs v1.9 — Change Summary

**Prepared for:** Charm Industrial MRV
**Date:** March 30, 2026
**Source:** [registry.isometric.com/standard](https://registry.isometric.com/standard)

---

## Major Changes

### 1. Scope Expansion: Emission Reduction Credits (NEW)

**v1.9:** Explicitly excluded "Emissions reductions (not removals)" and "Point source fossil fuel capture and storage" from scope. Only issued Carbon Dioxide Removal credits.

**v2.0:** Now issues **two credit types**:
- Carbon Dioxide Removal credits (one metric tonne CO2e net removal) — unchanged
- **Emission Reduction credits** (one metric tonne CO2e reduction of specified greenhouse gases) — NEW

The exclusion of "emissions reductions" has been removed. The exclusion of "point source fossil fuel capture and storage" and "REDD+" activities also appears removed. Enhanced Hydrocarbon Recovery and minimum durability failures remain excluded.

**Charm relevance: LOW.** Charm is a CDR pathway (bio-oil geological storage). This doesn't change Charm's operations, but it does significantly broaden the registry's scope and will bring new project types onto the platform. Worth monitoring for how this affects Isometric's bandwidth and verification queue times.

---

### 2. Crediting Period Extended

**v1.9:** "Maximum crediting periods are typically **5 years** (longer for biosphere protocols)."

**v2.0:** "Initial crediting periods typically span **10 years** maximum (**Biogenic Carbon Capture and Storage and Direct Air Capture protocols allow 15 years**; Biosphere protocols define periods per project)."

**Charm relevance: HIGH.** Charm's bio-oil geological storage falls under BiCRS. This means Charm may now qualify for a **15-year crediting period** instead of 5 years. This is a major operational improvement — fewer re-validations, longer planning horizons, and reduced administrative burden. Action item: confirm with Isometric whether Charm's current crediting period can be extended or whether this applies at next renewal.

---

### 3. Protocol Adoption Timelines Relaxed

**v1.9:** Minor version releases required adoption within a **12-month window** for subsequent verifications. Major versions adopted at crediting period renewal.

**v2.0:** Both major AND minor version changes now require adoption only **upon crediting period renewal**. Patch changes still take effect automatically.

Additional backward compatibility language: projects can request "legacy exemptions" from new requirements if adoption causes "non-trivial operational difficulty," and projects retain validation status when adopting new minor versions.

**Charm relevance: MODERATE-HIGH.** This is operationally favorable. When Isometric publishes updated protocol modules (e.g., Bio-oil Geological Storage v1.2, Energy Use Accounting v1.4), Charm no longer faces a 12-month forced adoption window. Adoption aligns with natural crediting period renewal cycles. Reduces mid-period disruption.

---

### 4. CRCF Section Added (NEW — Section 6)

**v1.9:** No CRCF section.

**v2.0:** New Section 6 covering the **EU Carbon Removal Certification Framework** (CRCF), including provisions for certification bodies, exclusion criteria, grievance systems, fraud remediation, internal monitoring, planning/reporting, delegated act requirements (GWP standards, quality assurance, climate adaptation considerations).

**Charm relevance: LOW-MODERATE.** Charm operates in the US, so EU CRCF compliance isn't directly required. However, this signals Isometric is positioning for EU market alignment. If Charm's credits are purchased by EU-based buyers seeking CRCF-compliant removals, this could become relevant. Worth tracking as EU CRCF regulatory details finalize.

---

## Significant Changes

### 5. GHG Statement Reporting — Separate Removals and Reductions

**v1.9:** GHG statements reported "claimed removals" as net CO2e including project emissions, removals, and counterfactual.

**v2.0:** Now requires removals and reductions to be submitted together but **reported separately**:
- Removals (with counterfactual and allocated emissions) in net CO2e tonnes
- Reductions (with counterfactual and allocated emissions) in net CO2e tonnes, with **gross reductions subdivided into avoided fossil CO2 and avoided non-CO2 greenhouse gases**

**Charm relevance: MODERATE.** Charm's GHG statements already report removals. The new subdivision requirement may require changes to how BCU (emission reduction) categories are reported. The five BCU categories currently used (injection diesel, injection waste, pre-treatment diesel, pre-treatment waste, bio-oil transport) may need to be further subdivided by gas type. Clarify with Isometric whether this applies to existing CDR-only projects or only to projects claiming both removals and reductions.

---

### 6. Financial Additionality — More Prescriptive IRR Requirements

**v1.9:** Required financial additionality demonstration via IRR analysis when carbon finance isn't the sole revenue source.

**v2.0:** Adds significantly more prescriptive requirements:
- Analysis must cover **10-year periods** (or justified alternatives) including non-depreciated residual values
- Existing subsidies, public financing, and tax incentives count as revenues
- Scenario analyses **must vary**: initial investment costs (if >20% of total), projected revenues for market changes, and any assumption/value representing >20% of costs/revenues or significantly impacting IRR (minimum ±20% variation)

**Charm relevance: LOW.** Charm likely passes additionality via the TRL exemption route (BiCRS at TRL 5-6, which is below the threshold). Even without TRL exemption, bio-oil geological storage CDR is clearly not common practice. The enhanced IRR requirements would only matter if Charm's additionality demonstration relies on the financial pillar, which it likely doesn't.

---

### 7. Protocol Review Milestones Added

**v1.9:** Mandatory protocol review after 2 years since certification.

**v2.0:** Adds **credit issuance milestones** as mandatory review triggers: 100,000; 500,000; 1,000,000; and 5,000,000 credits issued.

**Charm relevance: LOW (for now).** At ~5,700 tCO2e total verified removals, Charm is far from any of these thresholds. However, as the bio-oil geological storage pathway scales industry-wide, the 100k milestone could trigger a protocol review. Worth noting for long-term planning.

---

### 8. Environmental & Social Impact Requirements — Enhanced SDG Reporting

**v1.9:** Projects must explain consistency with relevant SDG objectives, including "qualitative assessments of positive impacts beyond SDG13 where applicable."

**v2.0:** Now requires projects to "demonstrate alignment with relevant UN Sustainable Development Goal objectives" and provide qualitative assessments using **"standardized tools/methods"** — implying more structured SDG reporting than before.

Also adds explicit requirements around "climate adaptation considerations" in the CRCF context.

**Charm relevance: LOW.** Charm's PDD already covers environmental/social impact. The "standardized tools/methods" language is new but the requirement itself is qualitative. May require minor PDD updates at next re-validation.

---

## Minor / Unchanged Areas

### Unchanged (confirming continuity for Charm)
- **Materiality threshold**: Remains 5%
- **Conservative estimate**: Remains ≤16th percentile (Options A/B/C unchanged)
- **Durability default**: Remains 1,000 years
- **Buffer pool framework**: Risk categorization and buffer sizing approach unchanged
- **VVB rotation**: Still 5 consecutive years max, 5 out of 7 years
- **VVB qualification**: ISO 14065 / IAF accreditation requirements unchanged
- **Modular framework**: Protocol-module version locking unchanged
- **Public consultation**: Still minimum 30 days
- **Science Network review**: Still typically 5-10 experts per module/protocol
- **Stakeholder consultation**: 14-day notice, 60-day grievance resolution — unchanged
- **Data sharing**: Public availability of quantification data — unchanged
- **100-year GWP**: Still uses IPCC's most recent Assessment Report (AR6)
- **ISO alignment**: Still ISO 14064-2:2019 for PDD, ISO 14064-3 / ISO 14065 for V&V
- **Cradle-to-grave GHG accounting**: System boundary requirements unchanged

---

## Action Items for Charm

1. **Crediting period (HIGH PRIORITY):** Confirm with Isometric whether Charm can extend to 15-year crediting period under v2.0 BiCRS provisions, and whether this applies at current or next renewal.

2. **Adoption timeline:** Confirm when v2.0 adoption is required. Under v2.0's own rules, major version changes require adoption at crediting period renewal — but this is a major version change *to the Standard itself*, so the transition timeline may differ.

3. **GHG statement format:** Clarify whether the separate removals/reductions reporting requirement changes anything for Charm's current CDR-only GHG statement structure, particularly around BCU subdivision.

4. **CRCF awareness:** Monitor EU CRCF delegated act developments for potential buyer-side requirements.

5. **No immediate operational changes needed** for ongoing verifications with 350Solutions at Basco 6 — the core verification mechanics, materiality thresholds, and uncertainty methodology are unchanged.
