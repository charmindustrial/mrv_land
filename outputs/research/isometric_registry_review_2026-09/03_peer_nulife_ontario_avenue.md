# Peer profile — Ontario Avenue Bio-Oil Sequestration (NULIFE GreenTech)

Prepared 2026-09-14 for the Isometric registry peer-comparison review. Pathway on the registry: "Bio-oil Geological Storage". Every quote below is verbatim from a document or web page read this session; page numbers are PDF page numbers as rendered by the Read tool. Charm quotes are taken from `02_charm_pdd_baseline.md` (the Charm PDD profile) and are labelled "Charm baseline".

Documents read in full this session (all three local copies match the registry copies byte-for-byte: identical Content-Length and MD5 hash, checked 2026-09-14):
- **PDD** — "Isometric Project Design Document / Version 1.7" (template version), project title "NULIFE GreenTech Ontario Avenue Bio-Oil Sequestration". Registry row "30 Sep 2025 | PDD". 87 pages. `raw/nulife_pdfs/nulife_pdd.pdf`.
- **GHG Statement Report** — "GHG Statement Report / Version 1.7 / Date: August 19th, 2026", reporting period "26 Jun 2026 to 22 Jul 2026", statement `ggs_1M0B8VWHZ1S0JJAK`. Registry row "26 Aug 2026 | GHG Statement Report" (the newest of 18 documents). 12 pages. `raw/nulife_pdfs/nulife_ghg_2026-08-26.pdf`.
- **Verification Report** — Normec Verifavia, "Date Report Issued 25.08.2026", "Report Version V2.0". Registry row "26 Aug 2026 | Verification Report" (the newest). 28 pages. `raw/nulife_pdfs/nulife_verification_2026-08-26.pdf`.
- **Registry pages** — project page; removal `rmv_1M0B59RM61S0BW9G` Calculation view, Removal method and Datapoints tabs (text saved to `raw/nulife_pdfs/rmv_1M0B59RM61S0BW9G_calc_and_datapoints_2026-09-14.txt`).

Redactions: the PDD blacks out the injection partner's name, the injection site location, the provincial regulator's name and permit codes. Where a quote contains a redaction it is shown as `[redacted]`.

---

## 1. Document size

### 1a. PDD

**Page count:** 87 (pdfinfo, and the last page rendered by Read is the Biomass Feedstock Appendix "Document History" table).

**Word count: NOT COMPUTED.** No sanctioned tool in this session could produce a machine text dump of the PDF. Four attempts, each failing for a named reason, are recorded in `raw/nulife_pdfs/README_text_extraction_2026-09-14.txt` (Bash text extraction is blocked by the workspace hook and was not worked around; headless Playwright rendered the PDF URL as a 0-byte snapshot; the pdf-viewer tool twice reported "Viewer never connected"; Word raised a macOS "Grant File Access" dialog, which I cancelled rather than grant permissions on Max's machine). I did not estimate a word count. Sizes below are in pages, from the rendered pages themselves.

**Top-level sections and size in pages** (a section that starts and ends mid-page is counted on both pages, so the column does not sum to 87):

| Section (document heading) | Pages | Size (pages) | Notes |
|---|---|---|---|
| Title block + Section A – Key Project Data (A.1–A.9) | 1–4 | 4 | |
| Section B – Protocol and Monitoring Data (B.1–B.14) | 4–51 | 47 | B.4 Project Boundary p6–12 (boundary table p7–12); B.9 Monitoring Plan p19–36; B.10 Data collection and storage p36–45; B.11 Reversals p45–47; B.12 Uncertainty p47–49; B.14 Storage site overview p49–51 |
| Section C – Duration & Crediting Period | 51–53 | 3 | |
| D – Environmental and social impacts | 53–66 | 14 | |
| E – Stakeholder Input Process | 66–68 | 3 | |
| Section F – Project Changes | 68–69 | 2 | F.1 blank, F.2 "N/A", F.3 table empty |
| Document History (template) | 70 | 1 | |
| Biomass Feedstock Accounting PDD Appendix, Version 1.1 | 70–87 | 18 | Three feedstocks, each answered through A3–A8: effluent sludge p70–76, oat hulls p77–82, waste bran p82–87 |

Total top-level sections: 8 (six lettered sections, the template history table, one feedstock appendix). There is no GHG Statement appendix, no BCU appendix, no permanence/closure/subsurface appendix. The injection site is covered inside B.9 and B.14.

### 1b. GHG Statement Report (26 Aug 2026 row)

**Page count:** 12. **Word count: NOT COMPUTED** (same reason as above).

| Section | Pages | Size (pages) | Content in one line |
|---|---|---|---|
| Header + Section A – General Project Information | 1–2 | 2 | practitioner, RP, statement ID, "Yes" to boundary confirmation |
| Section B – Project Details | 2–3 | 2 | the same 13-step HTL description as PDD A.6, then "Please refer to the PDD for the project details. Currently there are no additional details beyond what is included in the PDD." (p3) |
| Section C – Project Changes | 4 | 1 | "No changes." (p4) |
| Section D – GHG Statement Methodology | 5–9 | 5 | data-collection bullets per input, one data-flow diagram, formulas |
| Section E – GHG Statement Results | 9–12 | 4 | "Total Tonnes removed 150.45 tCO₂e. See Isometric Certify for a breakdown of the results." (p10), uncertainty text, materiality table image |
| Section F – GHG Statement Version Changes | 12 | 1 | one row: "August 19th, 2026 | 150.45" |

The template itself sets the expectation of brevity (p1): "After this document has been completed for the first time, it may be acceptable to refer back to relevant sections for subsequent Reporting Periods, for example if there have been no changes to the GHG Assessment scope, data collection methodology, calculation methodology or assumptions."

### 1c. Verification Report (26 Aug 2026 row)

28 pages. Sections: 1 Key Project Data (p4–6), 2 Means of Validation and Verification (p7–10), 3 Technical Aspects (p11–15), 4 GHG Statement (p15–17), 5 Verification Opinion (p18–21), 6 Document Versioning (p21), Appendix I Reference Table (p21–25), Appendix II Log of Issues (p25, all "N/A"), Appendix III (p26), Appendix IV team competence (p26–28). Appendix I lists the Certify sources for the four removals in the statement: I counted 88 `src_` rows (6 + 20 + 22 + 23 + 17 across p21–25).

---

## 2. Project design

**Protocol and modules.**
- PDD B.1 (p5): "Protocol Name: Bio Oil Geological Storage" / "Protocol Version Number: V1.1". The project page now shows "Current protocol version Bio-oil Geological Storage v1.2" and "Baseline protocol version Bio-oil Geological Storage v1.1".
- Verification Report p4: "Isometric Standard v2.1 / Protocol: Bio-oil Geological Storage v1.2 / Modules: Biomass Feedstock Accounting v1.3 / Energy Use Accounting v1.3 / Biomass or Bio-oil Storage in Salt Caverns v1.2 / GHG Accounting v1.1". p15: "Since the previous verification, the project has transitioned to the latest Isometric Standard (V2.1), Bio-oil Geological Storage Protocol (V1.2)".
- Modules named in the PDD text: "Section 5.1 of V1.2 Energy Use Accounting Module" (p23); "Section 3.3 of the Embodied Emissions Accounting Module" (p26); "Transportation Module Section 5.0" (p23); "Biomass Feedstock Accounting module" (p14); "Isometric GHG Accounting (V1) Materiality Assessment (Section 4)" (p12); "Monitoring Plan: Bio-Oil Geologic Storage module Monitoring Plan (Section 11.2)" (p20); "Bio-Oil/Biomass Storage in Salt Caverns module" (p28).

**Feedstock (PDD Biomass Feedstock Appendix A1, p70–71).** "The project relies on local waste biomass from the Saskatoon & area." Three feedstocks: "Feedstock 1: [redacted] provides us with effluent sludge from their [redacted] Canola Crushing Plant which is 30km away from NULIFE's site." "Feedstock 2: Oat Hulls consist primarily of the outer covering of oats". "Feedstock 3: Waste Bran. [redacted] us with their waste oat bran from their oat milk production plant in Saskatoon, which is 9km away from NULIFE's site." Registry Feedstocks table: "Bran Waste | Biomass | 02 Apr 2026", "Effluent Sludge | Biomass | 02 Apr 2026", "Oat Hulls | Biomass | 02 Apr 2026". The verified statement used only sludge: "The biomass feedstock used for this reporting period is an effluent sludge from two regional canola crushing plants." (GHG Statement p5).

**Oil production (PDD A.6, p3).** "NULIFE's Hydrothermal Liquefaction (HTL) process is a continuous thermo-chemical process that breaks down and liquefies high-moisture organic materials. The exothermic reaction occurs under high pressure (2,900 – 3,700 psig) and temperature (290 - 375°C), using water as a catalyst to reform the biomass carbon into long-chain hydrocarbons (bio-oil)." Heat source: "The current processor heat source is electric heaters." Fuel: "Currently the HTL system does not utilize fuel to convert biomass into bio-oil." (p22). Facility: "1725 Ontario Avenue, Saskatoon, SK, Canada, S7K 1S9" (p1).

**Transport (PDD A.6 step 9, p3–4).** "The bio-oil liquid is transported to the injection site by a third-party road transport company." Vehicle types (p25): "Vehicle type used: sludge feedstock, bio-oil and wastewater: tanker truck. / Vehicle type used: dry feedstock, consumables: flat bed truck. / Vehicle type used: sample delivery: car." Distances in the verified removal: bio-oil 347.00 km, biomass 329.00 km (Datapoints tab).

**Storage type and site (PDD B.14, p50–51).** "The injection facility utilizes underground caverns that were originally designed for high pressure gas storage up to 3,000 psi." "NULIFE is utilizing the injection site's Cavern #1 for bio-oil storage. Cavern #1 was previously used for waste disposal purposes. It is currently ~66% full." "Well Class (if applicable): Salt Cavern." "Permit validity start date: 2006". Site named only as "the site contains 5 underground salt caverns. These salt caverns were originally developed in the 1960s for natural gas storage" (p17) within "the Prairie Evaporite Formation" (p18). Registry summary: "The bio-oil is transported to a third-party injection site for sequestration into a Canadian underground salt cavern."

**Crediting period.** PDD C.1/C.3 (p51, 53): "Start date of Project: August 1, 2025" / "Start date of crediting period: Aug 1, 2025" / "Total length of crediting period: 5 years." The registry and Verification Report state a different, longer period: "Crediting period 01 Jun 2025 to 01 Jun 2035" (project page) and "01 Jun 2025 to 01 Jun 2035" (Verification Report p4, p15). The PDD text and the registry disagree on both start date and length; I cannot tell from the documents which controls.

**Reporting cadence.** No cadence is stated in the PDD (text search of the pages read: no phrase defining a reporting-period length). Observed: the latest RP is "26 Jun 2026 to 22 Jul 2026" (GHG Statement p1) with 4 removals; the registry Issuances table shows eight issuance dates since 30 Sep 2025 (30 Sep 2025, 26 Nov 2025, 29 Dec 2025, 20 Mar 2026, 19 May 2026, 18 Jun 2026, 27 Jul 2026, 26 Aug 2026), i.e. roughly monthly in 2026.

**Batch definition.** Two units:
- Production unit: "Each HTL Production Run, which is defined as a day of operation, is tested for carbon wt% with three (3) unique samples of bio-oil." (PDD B.12, p48). "NULIFE's HTL Production Runs are labelled by their production run date (year-month-date). Example of naming system: 2024-09-04." (p36).
- Removal unit: the injected tank load blending several runs — "Bio-oil production batches are blended in NULIFE's external storage tank prior to shipment for injection." (p20); "The combination of operational data from multiple HTL production batches will result in a total mass of bio-oil for injection. For example: Trial A had 500kg and Trial B had 500kg, thus the total mass for CO₂e Stored calculations would be 1,000kg." (p21). The verified removal's "Sequestration date 17 Jul 2026 to 22 Jul 2026" is a 6-day window for one 18.36 t truck delivery (Datapoints: "Injection Mass 18.360 t"). Verification Report p14: "Bio-oil samples are collected three times per day."

---

## 3. System boundary table

Source: PDD B.4 table, p7–12, plus quantification detail from B.9/B.10 and the Datapoints tab. "How quantified" is my classification of the PDD's own words (measured / calculated / default factor / sampled). Uncertainty treatment is from B.12 (p47–49) unless stated.

| # | Flux (PDD wording) | Incl./Excl. | How quantified (PDD quote) | Frequency | Uncertainty treatment |
|---|---|---|---|---|---|
| 1 | Baseline: "Counterfactual emissions. Fuel use from feedstock sourcing" | Excluded | "These emissions are 0." (p7) | — | — |
| 2 | Baseline: "Counterfactual emissions. Electricity use for feedstock sourcing" | Excluded | "These emissions are 0." (p8) | — | — |
| 3 | Baseline: "Counterfactual emissions. Replacement of feedstock" | Included | "When relevant, NULIFE will demonstrate that these emissions can be considered 0 due to eligibility criteria in the Biomass Accounting Module." (p8). Sludge: "C1 exemption" (p76); oat hulls: "C3 Exemption" (p82); bran: "C1 exemption" (p87) | per feedstock, once | — |
| 4 | Baseline: "Counterfactual emissions. Temporary carbon storage from feedstock" | Included | "NULIFE will demonstrate the quantity of stored carbon, on a per feedstock basis." (p8). Sludge and bran: landfill "decay rate utilized is 19% per year" (p74, p85); oat hulls: "the baseline we subtract from our calculation of net CO2e removal is zero" (p80). Datapoint "Constant removal counterfactual adjustment 1 kgCO₂e REPORTED" | per feedstock, once | Model: "The only use of models for the quantification of this delivery is feedstock/baseline CO2e Decay Rate counterfactual" (p49) |
| 5 | "Fuel Use from feedstock transport" | Included | Calculated: "Mass-Distance-Based method formula selected... MASS is monitored for each feedstock delivery and quantified based on documentation such as the Bill of Lading... DISTANCE... Google Maps" (p23); factor "GLEC mass x distance emissions factor includes the return trip impacts" | per delivery | "a 5% increase in transport distance is added via standard deviation to account for potential extension of routes" (p48) |
| 6 | "Fuel Use from bio-oil transport" | Included | Calculated: "MASS is calculated based on the scale ticket at the injection site." (p23); Google Maps distance; GLEC factor 0.07 kgCO₂e/(km⋅t) | per injection load | same 5% distance |
| 7 | "Fuel Use from wastewater transport" | Included | Calculated: "MASS is calculated based on the scale ticket at the injection site" [sic, p24]; B.10: "The transport company provides a bill of lading invoice with pick up volume." (p38) | per disposal event | same 5% distance |
| 8 | "Fuel Use from consumable (Sodium Hydroxide and Hydrogen Peroxide from the same supplier) transport." | Included in table; excluded from removals | "Note: These emissions were considered for the Net negativity example on Certify. They are excluded for regular Removal quantification, as per the materiality assessment." (p24) | — | — |
| 9 | "Fuel Use from consumable (activated carbon) transport." | Included in table; excluded from removals | same materiality note (p41) | — | — |
| 10 | "Embodied Emissions for Transport" | Included | Default factor inside GLEC: "The emissions factors used for truck transport include embodied emissions from truck manufacture and fuel production and the impacts of fuel use, on a tonnekm basis." (p9). No separate line in the calculation view | — | — |
| 11 | "Electricity Use for HTL Conversion - Primary Power Meter" | Included | Measured: "Total electricity consumption (kWh) is measured per HTL production run... using a power meter... The power meter accounts for +99% of kWh at the HTL site." (p22); grid factor "Saskatchewan grid electricity emissions factor" (p22); RECs: "RECs are acquired from SaskPower... For electricity consumed, per production batch, RECs are applied to reduce equivalent grid-based emissions." (p23) | per production run | "Grid Electricity/Procured Power Electricity Usage: The datapoint is accurate primary data and does not require an uncertainty discount." (GHG Statement p11) |
| 12 | "Electricity Use for HTL Conversion - Non power meter equipment log" | Included in table; excluded from removals | "manual calculations are recorded for kWh based on equipment specifications and recorded time used per HTL production run" (p22); "will be removed from regular CDR quantification, as per the Materiality assessment" (p39) | — | — |
| 13 | "Electricity Use for HTL Conversion - sampling equipment (Carbon wt% & GC gas analysis)" | Included in table; excluded from removals | "Electricity consumption is calculated on a kWh per sample basis" (p22); materiality note (p39) | — | — |
| 14 | "Electricity Use for Injection Site" | Included | Calculated, not metered: "Pump details provided by the Injection Partner. Details provided include pump horsepower and number of hours of operation to inject the relevant batch of material. The details are used to convert energy usage into kWh." (p25); "RECs are not applied to these emissions." (p23) | per injection batch | "At the injection site, a 20% increase in electricity usage is assumed due to the lack of primary measured data from the injection site." (p48) |
| 15 | "Embodied Emissions for HTL Conversion Site Equipment" | Included | Default factors × mass: "the mass based method has been selected: Overall mass of equipment, separated by material type, and material emissions factors." (p26); "emissions are allocated over the project lifetime" (p26), "which is 25 years" (GHG Statement p5). Calculation view: "Attribution factor 0.08% DERIVED" on every embodied line | once, amortized | — |
| 16 | "Embodied Emissions for Injection Site Equipment" | Included | "storage infrastructure is shared amongst multiple entities thus Project Proponent must allocate a percentage of the embodied emissions of that storage infrastructure proportional to the mass of stored material to the total storage capacity" (p26); datapoint "kgCO2e/kg of injectant emission factor (injection site equipment embodied emissions) <0.01 kgCO₂e/kg" | per injected tonne | — |
| 17 | "Embodied Emissions for HTL Conversion Site Construction" | Excluded | "Excluded because the site was not built for this project.The site was built in 1970 for industrial use." (p10) | — | — |
| 18 | "Embodied Emissions for Injection Site Construction" | Excluded | "The site was built in 1960 for natural gas storage." (p10) | — | — |
| 19 | "Embodied Emissions for HTL Conversion Site consumables." | Included in table; excluded from removals | Municipal water, hydrogen peroxide, sodium hydroxide, activated carbon — each carries "They are excluded for regular Removal quantification, as per the materiality assessment." (p26–27) | — | — |
| 20 | "Carbon Content of Injected bio-oil" | Included (the sink) | Sampled + measured mass: "At least three carbon wt % samples are taken per HTL production batch. Each sample is tested in duplicates. Mass of bio-oil is determined via mass measured per HTL production batch." (p10) | 3 samples per production run | "does not require an uncertainty discount" (p48) — see Part 4 |
| 21 | "CH₄ content of HTL tailgas" | Included | Sampled: "wt% CH4 of the tailgas is tested via GC gas analysis. The mass is determined through material balance." (p10); "GC analysis is performed, at minimum, per feedstock per unique operational parameter." (p21); Datapoints: "Mass flow of Gas 4.126 t", "Conion of warming potential (Methane) 0.34 %", GWP "27.000000" | per feedstock/operating condition | — |
| 22 | "CO₂ content of HTL tailgas" | Excluded | "uses an emissions factor of 0 because it is biogenic CO2." (p11) | — | — |
| 23 | "Staff Travel - Transport Emissions from Transport of test samples to lab" | Included in table; excluded from removals | "Distance based method using an appropriate emissions factor for gasoline car transport" (p11); "quantified by using NULIFE's vehicle reimbursement logs" (p24); materiality note (p44) | monthly logs | — |
| 24 | "Staff Travel and Surveys" | Included in table; excluded from removals | "Staff travel related to operators round trips to work are included." (p11); materiality note (p44) | — | — |
| 25 | "Sample Delivery - Injection Site to Nulife" | Excluded | "Purolator (Canadian road courier) is used for transport, so the transport movement was already taking place regardless... Due to the extremely small mass (< 0.25kg) of the samples, the marginal emissions for moving a package is nearly zero." (p11) | — | — |
| 26 | "Equipment Transport from supplier to end use Site (i.e. Nulife site)" | Included | "Transport emissions between the supplier location and NULIFE's site are calculated based on a round trip and the mass of the steel, stainless steel and plastic." (p12); Datapoints: 8.00 km × 28.439 t and 8.00 km × 1.600 t, flat deck 0.08 kgCO₂e/(km⋅t) | once, amortized | — |
| 27 | "Wastewater Disposal" | Included in table; excluded from removals | "Wastewater Treatment Emissions = Water Disposed x EF" (p27); "They are excluded for regular Removal quantification, as per the materiality assessment." (p28) | — | — |
| — | End-of-life of equipment (not a B.4 row; in Datapoints) | Included | "Mass (end of Life disposal of Steel/Stainless Steel/Polyethylene Plastic) 1.600 t", "Carbon emission factor (end of life disposal - landfill) 0.05 kgCO₂e/kg", distances 13.20 km and 1.00 km; GHG Statement p5: "End of life scenarios are applied for each material using the mass x EF formula." | once, amortized | — |

Materiality screen (PDD p49 and GHG Statement p12, the same table image dated "September 10, 2025", "Protocol: GHG Accounting V1.0", "CO2e Removal (tCO2e) 41.88"): 14 rows marked "exclude", with the closing line "Sum of SSRs excluded (must be < 1%) | 0.208 | 0.787965616 | still below the 1% threshold". Rows retained: biomass transport (wet), wastewater transport, tailgas methane, clean-power/grid electricity, bio-oil transport, injection-site embodied, injection electricity. The stated rule (p49 image): "If materiality of the SSR is < 1%, then the emissions associated with the SSR may be excluded from the GHG Statement boundary, provided that the total exclusions make up < 1% collectively."

Boundary description (B.4, p6): "All activities undertaken to permanently sequester carbon, at the point of taking ownership of the organic waste, are included in the system boundary." Upstream exclusion: "Excluded from the system boundary are all upstream inputs to biomass cultivation and production... because the biomass taken is waste – not purpose-grown biomass". Also (p7): "Methane emissions that would have occurred in the counterfactual scenario of the waste decomposing without NULIFE's intervention are excluded."

Uncertainty approach (B.12, p47–48): "Variance propagation (selected)". "The Isometric Certify Sensitivity Analysis flagged two items with an impact on net removal of > 20%. These items are mass of product (bio-oil) and Carbon content of product (bio-oil)." "The remaining data points do not impact net removals by greater than 1%, thus further analysis is not required." Verified result: "Uncertainty Discount 45 kg" on "Sequestrations 47.591 t" (Calculation view), which is 45 ÷ 47,591 = 0.00095, i.e. 0.09% (my arithmetic).

---

## 4. Gross removal calculation

**Formula.** GHG Statement p9–10: "CO2 Stored / Bio-oil Mass x Bio-oil weighted average carbon wt% value x Scientific Value. / The scientific value of 3.67 CO₂e eq mass of C is used to convert bio-oil carbon into CO₂." PDD p20: "The emissions factor of 3.67 CO₂e eq mass of C is used to convert bio-oil carbon into CO₂." Verification Report p13 writes it as "1 MT CO₂ sequestered = 1 MT of bio-oil × carbon fraction × (molecular weight conversion of C to CO₂)".

Check against the verified removal (my arithmetic from the Datapoints tab): 17.607 t × 0.737100 × 44/12 = 47.586 t, against the displayed "Sequestrations 47.591 t" — a 0.01% difference attributable to the displayed rounding of the inputs.

**Carbon content — method and sampling.** PDD B.9 (p20):
- "As per section 7.4.1.1.1, 'Method A: measure every batch' has been selected. Bio-oil production batches are blended in NULIFE's external storage tank prior to shipment for injection."
- "Carbon wt% is determined by elemental analysis (ASTM D5921 or equivalent) using the University of Saskatchewan Chemical Engineering Lab (deemed an in-house lab that is not ISO17025 accredited lab*)." and "*An In-house lab is deemed acceptable by Isometric by supplying more information. Attachment 'Carbon content lab test requirements v1.0' is provided".
- "A minimum of 3 samples are taken per HTL production batch, as per the minimum samples per batch requirements in Section 7.4.1.1.1."
- "Samples are dried in an oven, to remove moisture, before preparation for elemental analysis."
- "Samples are driven, bi-weekly, to the lab which is 6km away."
- "Each sample is tested for carbon wt% in duplicates and the average of the two samples is utilized for each of the three samples."
- Outlier rule: "In the case of carbon outliers (variance between the duplicate samples), the lab technician is asked to re-run samples to re-assess. The variance is +/- 5 wt%".
- "Regardless of how many samples are tested, we take a weighted average of all samples assessed, which includes all duplicates."
- Missing data (p48): "During one HTL production run, August 5, 2025, there is a gap in elemental analysis data. For this trial, the conservative value of 70% carbon is assumed, which is 5% less than the weighted average for the entire HTL production run."
Verified datapoint: "Carbon Content of Product 0.737100 REPORTED — Carbon Content Of Product Batch #027.xlsx".

**Mass measurement.** PDD p20–21: "Bio-oil Mass is determined by density measurement including a deduction for moisture content of the bio-oil. / Mass of bio-oil is measured in kg and allocated per HTL production run." "The density of bio-oil is determined via ASTM D4052 or equivalent... A bio-oil density value is determined for bio-oil from each feedstock source." "The moisture content (wt %) of bio-oil is determined by ASTM E-1756 through onsite testing. This is tested on three bio-oil samples from every HTL production run and the average of the three samples is utilized." The scale is deliberately not used for the sink: "The existing protocol implies the option to use the scale at the injection site for this calculation. Due to varying moisture levels in the bio-oil and the commercial impracticality of entirely removing the moisture, the injection site scale will record a higher mass and result in an over statement of CO₂e stored." (p21). B.10 (p37): "Liters of bio-oil production are measured and recorded as a cubic meter value... Using the density of the bio-oil, the cubic meter value (moisture deducted) is converted into kilograms". In the verified removal the sink mass is "Bio Mass Products 17.607 t" while the scale-ticket mass used for transport and injection lines is "Injection Mass 18.360 t" (Datapoints tab), so the sink mass is 0.753 t (4.1%) below the scale mass (my arithmetic).

**Adjustments.** None of the following appear in the PDD text read: consumables subtraction, tote or container standard loss, salt residue credit, filtration loss, upstream loss allocation. The only adjustments are the moisture deduction above and the counterfactual "Constant removal counterfactual adjustment 1 kgCO₂e". Verification Report p16: "Removal counterfactuals <0.01 tCO₂e / Losses 0 / Adjustments N/A".

**Uncertainty on gross.** PDD p48: "Mass of Product: The datapoint is accurate primary data and does not require an uncertainty discount. Bio-oil mass is measured data, with high certainty. Original values are used without a standard deviation." and "Carbon content of product: The datapoint is accurate primary data and does not require an uncertainty discount." The registry nevertheless shows "Uncertainty Discount 45 kg" (Calculation view); the documents do not say which input generates it.

---

## 5. Monitoring plan

Option chosen (PDD B.9, p19): "B – I have submitted a Monitoring Plan..."; "Option B selected. The following data highlights how the monitoring plan slightly deviates from the default monitoring plan outlined in the protocol."

### 5a. Emissions-side and sink-side (PDD B.9 p20–28, B.10 p36–45)

| Parameter | Frequency | Instrument / source (quote) | Evidence produced |
|---|---|---|---|
| Bio-oil carbon wt% | 3 samples per production run (day), each in duplicate; lab runs "bi-weekly" | "elemental analysis (ASTM D5921 or equivalent) using the University of Saskatchewan Chemical Engineering Lab" (p20) | "Certify Uploaded Source: Excel file or screenshot of the Carbon wt% data including the calculated average" (p37) |
| Bio-oil volume, density, moisture | per production run; density "for bio-oil from each feedstock source" | "ASTM D4052" density; "ASTM E-1756 through onsite testing" moisture (p21) | "Excel file or screenshot of the Trial Report" (p37) |
| Tailgas mass flow | per production run | "Flow per HTL production run measured via material balance remainder analysis." (p21); "calculated on a per HTL production batch basis by deducting the output quantities of bio-oil, water soluble oil and biochar" (p38) | Trial Report |
| Tailgas CO₂/CH₄ concentration | "at minimum, per feedstock per unique operational parameter" | "GC Analysis at the University of Saskatchewan Chemical Engineering Lab" (p21) | "Excel file or screenshot of the calculated GC results" (p38) |
| Operation time | per production run | "Measured per HTL production batch in start up, operation and cooldown sections. Measured in hours." (p22) | Trial Observations spreadsheet |
| HTL electricity | per production run | "Power Meter logs are recorded on the Programmable Logic Controller (PLC)" (p38) | "PLC software evidence of kWh consumption" (GHG Statement p6) |
| RECs | per production batch, "volumetric matching" | "SaskPower's newly launched Renewable Subscription Service program" (p23) | "REC procurement evidence" (GHG Statement p6); datapoint "Green Power Block Usage - Batch #27.pdf" |
| Feedstock mass and distance | per delivery | "Bill of Lading" + "Google Maps" (p23) | BOL, map screenshot |
| Bio-oil transport / injection mass | per load | "The injection site provides an injection statement including ticket with delivery mass based on arrival and departure weight." (p42) | scale ticket |
| Wastewater mass and distance | per disposal event | "bill of lading invoice with pick up volume" (p38); Google Maps | BOL, map screenshot |
| Injection electricity | per injection batch | "specifications on their primary pump and its horsepower along with frequency the pump is running" (p42) | "Calculated data quantifying the kWh value via excel file or screenshot" (p42) |
| Injection-site fuel | none | "Currently there is no documented fuel usage for the injection site. The injection pumping and brine pumping is electric powered." (p25) | — |
| Embodied equipment | once; "reviewed at each Crediting Period renewal" (p26) | "determined based on equipment lists" (p26) | "Equipment list with mass values" (p37) |
| Consumables (water, H₂O₂, NaOH, activated carbon) | per production run | flow rate × time (water); volumes/masses recorded; "Consumable Tracking Excel Sheet" (p40) | Trial Report — all excluded by materiality |

### 5b. Storage-side (PDD B.9 "Monitoring Plan: Bio-Oil/Biomass Storage in Salt Caverns module", p28–36)

"An expectations document is provided to the injection partner outlining the monitoring plan requirements pertaining to the required testing for brine and gas as well as reversal notification." (p28)

Pre-injection baseline:
- Brine pH — Injection Partner — "Historic monthly data is accessible, which is used for the baseline." — "EPP444 method by ISO17025 certified Lab in Saskatoon SK." — "Permit pH requirement: 2.0 – 12.5." (p28)
- Brine chloride — Injection Partner — historic monthly — "Extractable Organic halogens (as chlorides) Method: EOX.A by ISO17025 certified Lab" — "Permit chloride requirement: ≤ 100 mg/L." (p28)
- Brine carbon wt% — NULIFE — "Once" — "Elemental analysis (carbon wt%) at the University of Saskatchewan." — "Permit requirement: Not required." (p29)
- Brine temperature — "recorded as part of the analysis package provided by the injection partner." (p29)
- Baseline gas — "Baseline tedlar bag gas sample taken at discharge brine tank prior to 1st injection." "Frequency? At least once." "GC testing to be done at the University of Saskatchewan." (p29)

Injectant: "The Injection Partner is not required to test each delivery of material, unless there are identified abnormalities" (p29). NULIFE adds:
- Injectant pH — NULIFE — "pH meter or strip" — "Per injection batch" — "Sampled during truck loading procedure at NULIFE site." (p30)
- Injectant chloride — NULIFE — "Per injection batch" — EOX.A or TOX "Rad-113 by an ISO 17025 certified lab" — with the taper "Once consistency of organic chloride results has been established, the frequency of analysis will be reduced." (p30)
- δ13C — "University of Waterloo Isotope Lab" — "One sample per feedstock type is the stated requirement in the protocol." — "δ13Carbon signature testing is useful but not required under the protocol." (p30)
- Injectant temperature — "NULIFE records a temperature reading for each bio-oil shipment." (p30)

Displaced brine:
- wt% carbon — NULIFE — "Measurement shall occur every two weeks for 3 months, if the measurements are consistent this can be changed to every month for 6 months, then quarterly for 2 years, and finally every 6 months if these are still consistent." (p31)
- pH and chloride — Injection partner — "Monthly, as per permitting requirements." (p31)
- Temperature — "not currently a required test under the permitting requirements." (p31)

Gas: "A fixed gas monitor testing for hydrocarbon gases and CO₂ will eventually be placed at the brine tank... If carbon bearing gas is detected above 0.01vol%, it could indicate biogas formation and will be investigated." (p31) "Note: NULIFE is still investigating the appropriate gas monitor and we anticipate implementation for Q4 2025. In the near term, NULIFE will utilize the brine tank gas testing port to capture tedlar gas bag samples for GC analysis... We will capture a gas sample every two weeks for 3 months. If the measurements are consistent this can be changed to every month for 6 months until the gas monitor is installed." (p32)

Cavern integrity (injection partner, under CSA Z341.2, p32–35): Internal well integrity "Pressure testing, scan casing testing... Monitoring frequency? Every 5 years"; external well integrity "There is no way of knowing the outside integrity"; MIT "See attachment CSA Z341 Annex C"; cavern temperature "Not required by CSA Z341.2"; cavern pressure "The injection partner logs the cavern pressure daily"; sonar "Annually"; subsidence "It is not required to be done routinely"; USDW "8 monitoring wells around the facility that get tested annually"; salt permeability "Not required on an ongoing basis"; caprock "not relevant for the cavern zone utilized"; faults "Not an ongoing requirement".

Reversals (p36): "the Injection Partner has confirmed that they will contact NULIFE on the same day as the event. The Protocol states that the VVB should be notified but it is more appropriate for NULIFE to be notified"; "a report will be made within 1-3 business days".

Data storage (p44–45): "NULIFE uses Microsoft OneDrive to store internal and external data." "Internal data, such as Carbon wt% values and injection site scale tickets are stored for at least 5 years." Transfer to registry (p36): "The relevant data from each HTL production run is manually entered into a primary Ontario Avenue CDR Excel spreadsheet. The relevant data is then transferred into Isometric's Certify platform".

---

## 6. Calculation view (rmv_1M0B59RM61S0BW9G)

Header: "45.83 tCO₂e removed by NULIFE GreenTech"; "Sequestration date 17 Jul 2026 to 22 Jul 2026"; "Reporting period 26 Jun 2026 to 22 Jul 2026"; "Verification protocol version Bio-oil Geological Storage v1.2".

**Tree as shown** (panel text, verbatim values):
```
Net CO₂e Removed        45.835 t
  = Sequestrations      47.591 t
  − Activities           1.709 tCO₂e
  + Counterfactuals      1 kgCO₂e
  − Uncertainty Discount 45 kg
```
Check: 47.591 − 1.709 + 0.001 − 0.045 = 45.838 t vs displayed 45.835 t (0.003 t difference from rounding of the displayed components). The Verification Report (p16) gives this removal as "47.591 tCO₂e" sequestration, "1.709 tCO₂e" activities and "45 kg" uncertainty discount, matching.

The diagram itself is a zoomable graphic ("⌘ + scroll to zoom / View full screen"); the activity line items are not exposed as text. Reconstructing them from the datapoints with the PDD formulas (my arithmetic): bio-oil transport 18.360 t × 347 km × 0.07 = 446 kg; biomass transport 28.000 t × 329 km × 0.07 = 645 kg; wastewater transport 23.100 t × 7.5 km × 0.07 = 12 kg; tailgas methane 4.126 t × 0.34% × 27 = 379 kg; HTL electricity 6,037 kWh × 0.01 = 60 kg (procured-power factor; grid factor shown 0.63 but offset by RECs "on a volumetric matching basis"); injection electricity 158 kWh × 0.67 = 106 kg (127 kg if the PDD's +20% is applied); embodied and end-of-life lines at "Attribution factor 0.08%" of ~130 t of material-EF product, i.e. on the order of tens of kg. Sum ≈ 1.65–1.7 t, consistent with "Activities 1.709 tCO₂e". This reconstruction is mine; the registry text does not itemize.

**Datapoints — count and collection method.** Datapoints tab: "Datapoints (45)" (the calculation-view list says "Datapoints (44)" and omits the counterfactual row). By collection method: **37 REPORTED, 8 DERIVED**. All eight DERIVED rows are "Attribution factor 0.08%" with source "—". Full list with values and source file names is in `raw/nulife_pdfs/rmv_1M0B59RM61S0BW9G_calc_and_datapoints_2026-09-14.txt`.

Grouped:
- Sink (2): "Bio Mass Products 17.607 t" ← "Isometric Ontario Avenue Primary CDR Batch #027.xlsx"; "Carbon Content of Product 0.737100" ← "Carbon Content Of Product Batch #027.xlsx".
- Counterfactual (1): "Constant removal counterfactual adjustment 1 kgCO₂e" ← "LD Constant Removal Counterfactual Adjustment.pdf.xlsx".
- Transport (9): biomass mass/distance/EF; bio-oil mass/distance/EF; wastewater mass/distance/EF. Mass sources: "2025-07-27- Feedstock sludge Delivery- Batch #27.pdf", "2026-07-27 - Delivery Injection Site Batch #27.pdf", "2026-07-27 - Waste Water Transport- Batch #27.pdf". Distances: three .png map captures. EF: "GLEC_FRAMEWORK_v3.1_March_2025_1-3.pdf".
- Tailgas (3): mass flow ← Primary CDR Batch #027.xlsx; "Conion of warming potential (Methane) 0.34 %" ← "Methane tailgas 0.34%.pdf"; GWP 27 ← "Global-Warming-Potential-Values (August 2024).pdf".
- HTL electricity (4): grid kWh ← "2026-07-27 Power Usage - Batch #27.pdf"; procured kWh ← "2026-07-27 Green Power Block Usage - Batch #27.pdf"; grid EF 0.63 ← "En84-294-2025-eng_src_1KKF85N801S0C74F.pdf"; REC EF 0.01 ← "2026-03 NULIFE Ontaro Ave REC Details.xlsx + 2 more".
- Injection (4): kWh ← "2026-07-27 - Injection Site Electricity Consumption Batch #27.pdf"; grid EF 0.67 ← "2024-05 Canada Emission Factors and Reference Values.pdf"; injection mass ← delivery pdf; embodied EF ← "2025-08-19 Injection Site Embodied Emissions.xlsx + 1 more".
- HTL embodied + end-of-life (14 REPORTED + 8 DERIVED): masses ← "2025-09-22_1725_Ontario_Avenue_Embodied_Emissions_LCA.xlsx"; material EFs ← "2025-07 NULIFE GreenTech EF Sphera screenshots.pdf + 2 more"; landfill EF ← "2025-07-29 LCA Sources NULIFE.xlsx + 2 more"; four short distances (8, 8, 13.2, 1.0 km) ← .png maps; flat-deck EF ← GLEC.

**Sources named.** Batch-specific evidence for this removal is seven files: two "Batch #27" delivery/electricity PDFs from the injection site, one power-usage PDF, one green-power PDF, one wastewater-transport PDF, one feedstock-delivery PDF (dated 2025-07-27 in the file name), one carbon-content .xlsx, one primary CDR .xlsx. Everything else is a standing reference (GLEC, Canadian emission-factor publications, Sphera screenshots, LCA workbook, map .png files, GWP table, REC details). The Verification Report's Appendix I lists 88 `src_` rows across the four removals of the statement (my count, p21–25).

---

## 7. Side-by-side with Charm

Charm quotes are from `02_charm_pdd_baseline.md` (Charm baseline). Peer quotes are from the pages cited above.

### 7.1 Document size — DIFFERS (peer is much shorter)
- Charm baseline: "**Word count:** 58,881 words in the document body"; "the last entry is 'Appendix 11: Biochar Production and Storage PDD Appendix……. 155'. So the document is at least 155 pages long"; "**Top-level sections:** 17 (six lettered sections + eleven appendices)."
- Peer: 87 pages, 8 top-level sections, word count not computed (Part 1). GHG Statement Report 12 pages.
- What is missing from the peer relative to Charm, and whether it is protocol-required:
  - No embedded GHG Statement appendix (Charm baseline: "App 6 | Appendix 6: GHG Statement Report | 96 | 16,191"). The peer files the GHG Statement as a separate 12-page document whose template says "GHG Statement calculations (provided separately)" (p1) and whose body says "Details on specific calculation formulas can be found in Isometric Certify software in the LCA section." (p5). The template quote in Part 1b permits referring back once the first statement is done. From the text: the extra length in Charm's Appendix 6 is not shown to be protocol-required; the peer meets the same template by pointing to Certify.
  - No permanence/closure/subsurface appendices (Charm baseline App 8–10, 3,847 + 803 + 984 computed words). The peer's storage is a third-party permitted cavern and it answers the cavern module inside B.9 (p28–36) and B.14 (p49–51). Charm's Appendix 8 exists because Charm operates its own well under the Permeable Reservoirs module ("The following deviations from the Protocol are required on account of the project design", Charm baseline). Protocol-required for Charm's Louisiana well; not applicable to a salt-cavern-only project.
  - No BCU appendix (Charm baseline App 7) — the peer has no fuel use to offset: "Currently the HTL system does not utilize fuel" (p22).
  - No biochar appendix (Charm App 11) — not in the peer's pathway.
  - Feedstock appendices: peer 3 (18 pages) vs Charm 5 (Charm baseline: "Four near-identical feedstock appendices (2–5...)" plus Appendix 1). Both follow the same module template ("This Appendix must be completed for each feedstock type and feedstock provider used in this Project." p70). Length here is driven by feedstock count, which the module requires.
  - Change log: Charm baseline "Section F change log (2,100 computed words) — five dated entries"; peer F.1 blank, F.2 "N/A", F.3 empty (p68–69), and GHG Statement C.1 "No changes." The peer is one year old with no recorded changes.
- Where the peer is longer: D – Environmental and social impacts runs 14 pages (p53–66) against Charm baseline "Section D... 3,192" words; the peer's text is corporate-policy prose (e.g. the environmental policy bullet list p54–55). I cannot tell from the text whether that added length is required.

### 7.2 Project design — DIFFERS on production, transport, storage operator; RESEMBLES on protocol family and batch layering
- Protocol: Charm baseline "Protocol Name: Bio Oil Geological Storage / Protocol Version Number: v1.0" (plus two biochar protocols); peer "Protocol Version Number: V1.1" (p5), verified under v1.2. Resembles (same protocol).
- Feedstock: Charm baseline "non-sawmill quality Ponderosa Pines and Douglas Firs from a wildfire mitigation project" and AECN "sawdust and shavings from a lumber mill"; peer "effluent sludge from their [redacted] Canola Crushing Plant", "Oat Hulls", "waste oat bran" (p70–71). Differs — wet industrial food wastes, sourced "Typically... within a 40km radius of the Saskatoon Plant" (p7).
- Oil production: Charm pyrolysis at Fort Lupton plus purchased AECN oil; peer single HTL plant with electric heaters, no fuel (p3, p22). Differs.
- Transport: Charm baseline "a combination of rail and truck to transport the bio-oil to our pre-processing site in Kansas where it is treated"; peer: direct tanker truck from the HTL site to the injection site, no pre-processing step, no consumables added to the oil (p3–4, p25). Differs.
- Storage: Charm baseline salt caverns at Vaulted (Class UIC V, "KS-05-155-003") and its own Basco 6 permeable-reservoir well; peer third-party salt cavern in Saskatchewan permitted since "2006" under CSA Z341.2 (p51). Resembles the Kansas leg; the peer has no self-operated well.
- Crediting period: Charm baseline "Start date of crediting period: 2024/03/01 / Total length of crediting period: 5 years"; peer PDD "Aug 1, 2025 / 5 years" (p53) but registry "01 Jun 2025 to 01 Jun 2035". Differs on the registry-recorded length (10 years shown for the peer).
- Reporting cadence: Charm baseline "The PDD does not state a fixed calendar cadence... implying roughly monthly-to-bimonthly periods in practice"; peer likewise unstated, observed roughly monthly (Part 2). Resembles.
- Batch definition: Charm baseline "Once a given Lot, or batched combination of several split Lots, is injected it is then logged as a Removal" and Production Period "the month of January 2025"; peer production run = "a day of operation" (p48), removal = blended tank shipment. Resembles in layering (production unit feeding injection unit), differs in granularity (day vs month).

### 7.3 System boundary — DIFFERS (fewer active lines, materiality exclusions, calculated injection power)
- Charm baseline: "**The boundary table** (Section B) lists 40 rows" (43 numbered in the baseline listing), with roughly 30 emission lines quantified in Appendix 6, plus waste disposal and thermal oxidizer lines.
- Peer: 27 rows in B.4 (Part 3), of which 6 are excluded outright, 8 are "Included" in the table but "excluded for regular Removal quantification, as per the materiality assessment", leaving ~11 active quantified lines plus embodied/end-of-life detail. Verified activities total "1.709 tCO₂e" on "47.591 t" sequestered = 3.6% (my arithmetic).
- Quantification style: Charm baseline lines are measured × factor with per-line uncertainty ("This quantity is adjusted for fuel pump uncertainty", "adjusted for meter uncertainty"); peer lines are measured × GLEC/Canadian factors with two blanket conservatism rules — "a 20% increase in electricity usage is assumed" at the injection site and "a 5% increase in transport distance" (p48).
- Injection-site electricity: Charm baseline "The reading on both meters is noted by site staff prior to and following injection"; peer "Pump details provided by the Injection Partner... horsepower and number of hours" (p25). Differs — peer is calculated, not metered.
- Transport embodied: Charm baseline separate lines ("Per-mile embodied emissions are calculated based on GREET", railcar "cost-based calculation"); peer relies on the GLEC factor's included embodied share (p9) with no separate line. Differs.
- Sample transport: Charm baseline includes it ("Emissions are calculated for air shipment of samples"); peer includes staff sample driving in the table but excludes it by materiality, and excludes courier delivery of brine/gas samples outright (p11). Differs.
- Uncertainty: Charm baseline "Fourteen separately justified measurement half-widths, each propagated"; peer two flagged items, both declared "does not require an uncertainty discount" (p48). Differs.

### 7.4 Gross removal — RESEMBLES on formula and Method A; DIFFERS on lab, sampling count, mass basis, adjustments
- Formula: Charm baseline "multiplying the Mass of Bio Oil Injected by the average C content of the sample... multiplied by 44/12"; peer "Bio-oil Mass x Bio-oil weighted average carbon wt% value x Scientific Value... 3.67" (GHG Statement p9–10). Resembles.
- Sampling frequency: Charm baseline "Per section 7.4.1.1.1... a sample is taken for each injection batch" and "one sample will be sent to an analytic lab to measure the carbon content of that batch"; peer "A minimum of 3 samples are taken per HTL production batch, as per the minimum samples per batch requirements in Section 7.4.1.1.1." (p20), "Each sample is tested in duplicates" (p48). Differs — the peer reads the same protocol section as requiring three samples per batch and takes them per production day, not per injection batch. I did not read the protocol this session and cannot say which reading is correct.
- Lab: Charm baseline "CHN testing by an ISO accredited laboratory", "LECO instrument"; peer "University of Saskatchewan Chemical Engineering Lab (deemed an in-house lab that is not ISO17025 accredited lab*)" (p20). Differs.
- Mass: Charm baseline "weighing the delivery truck prior to and after injection on a certified scale" less consumables; peer volume × density − moisture (p20–21), explicitly not the scale. Differs. The peer's approach yields a sink mass below the scale mass (17.607 t vs 18.360 t).
- Adjustments: Charm baseline salt residue "70%", tote standard loss "5.33kg", AECN upstream loss "+25%", consumables subtraction; peer none (Part 4). Differs.
- Uncertainty on gross: Charm baseline "160 lbs" scale half-width and ".4%" analyzer RSD propagated; peer "Original values are used without a standard deviation." (p48), registry discount 45 kg (0.09%). Differs.

### 7.5 Monitoring plan — RESEMBLES in structure (Option B, same cavern-module parameter list, same brine-carbon taper); DIFFERS in who tests and how often
- Both select Option B (Charm baseline "B – I have submitted a Monitoring Plan"; peer p19).
- Displaced-brine carbon: Charm baseline "Every two weeks for 3 months. If measurements are consistent this can be changed to every month for 6 months, then quarterly for 2 years, and finally every 6 months"; peer "every two weeks for 3 months, if the measurements are consistent this can be changed to every month for 6 months, then quarterly for 2 years, and finally every 6 months" (p31). Resembles (near-identical wording).
- Injectant pH/temperature: Charm baseline Vaulted "One sample per day of injection" with "Injectate will not be injected if the pH reading is below 4.0"; peer NULIFE "Per injection batch... Sampled during truck loading procedure at NULIFE site" with "pH meter or strip" (p30) and no acceptance threshold beyond "Permit pH requirement: 2.0 – 12.5". Differs.
- Injectant TAN and density per batch (Charm baseline "ISO-accredited analytical laboratory") — no TAN line in the peer plan; density is per feedstock source (p21). Differs.
- Gas alarm routing: Charm baseline "more appropriate for the well operator to notify Charm... rather than the VVB"; peer "it is more appropriate for NULIFE to be notified" (p36). Resembles.
- Cavern integrity: Charm baseline lists Vaulted's programme including "Daily readouts of pressures", "Quarterly groundwater testing", "Bi-yearly elevation surveys"; peer relies on the partner's CSA Z341.2 permit: MIT "Every 5 years", sonar "Annually", groundwater "annually", subsidence not routine (p33–35). Differs — sparser cadence.
- Fixed gas monitor: peer "still investigating the appropriate gas monitor" (p32); Charm baseline relies on the operator's existing "wellhead gas alarm". Differs.
- Charm's Louisiana programme (Charm baseline: "Continuous recording devices", "Wellhead gas detection... every 6 mos", "Corrosion monitoring... 6 month", annual MIT/falloff/tracer) has no counterpart — the peer operates no well.

### 7.6 Calculation view — RESEMBLES in tree shape; DIFFERS in datapoint count and sources
- The tree shape (net = sequestrations − activities + counterfactuals − uncertainty) is Isometric's rendering and is common to both. The Charm removal captured in `raw/ghg_entry_charm_rmv_1KZBJBN9C1S0M5R5.json` was not part of this task and I did not re-read it; no Charm datapoint count is asserted here.
- Peer: 45 datapoints, 37 REPORTED / 8 DERIVED, seven batch-specific evidence files (Part 6). Charm baseline per-batch documents (Section 6 of the baseline): "Bill of Lading / scale ticket / invoice at origin; rail or truck routing record; Vaulted 'inspection report/weight scale ticket form' (mass, pH, temperature); LCS flow-meter and salt scale records; lab reports for C content (CHN), TAN, density; ledger entry for each" plus Production Period data. Differs — the peer's per-removal evidence set is smaller and has no consumables or pre-processing records.

---

## 8. Cost / complexity / overhead reducers

For each: the peer's method (quote), Charm's corresponding practice (Charm baseline quote), and whether protocol text quoted in either PDD requires the heavier practice.

1. **Materiality exclusion of 14 small sources.** Peer: "Sum of SSRs excluded (must be < 1%) | 0.208 | 0.787965616 | still below the 1% threshold" (p49 image) and, on eight lines, "They are excluded for regular Removal quantification, as per the materiality assessment." Charm baseline quantifies consumables embodied ("When liquid caustic soda (LCS) is added... measured... using a flow-meter"), consumables transport, sample shipping ("Emissions are calculated for air shipment of samples"), waste disposal, and treats only the thermal oxidizer as "De minimis". Protocol text: the peer quotes the GHG Accounting module rule permitting exclusion (p12: "Carbon Flux/emission sources that are labelled 'included' in the table above may be omitted from removal data, as per the requirements of section."). Neither PDD quotes text requiring the heavier practice.

2. **No pre-processing stage and no consumable additions to the oil.** Peer: bio-oil goes "to the injection site by a third-party road transport company" (p3) and is offloaded "into the injectant tank through a connected hose" (p4); no salt, no caustic, no sparging. Charm baseline: "transportation of injectate to and from pre-processing, the pre-processing itself" with LCS flow-meter, salt scale, "Salt residue credit", "Tote standard loss", El Dorado electricity/diesel and thermal oxidizer. Requirement: this is a process-design difference (Kansas injection acceptance criteria), not a protocol requirement quoted in either PDD.

3. **Injection-site electricity calculated from pump specification, with a flat +20%, instead of metered.** Peer p25 and p48 (quotes in Part 3). Charm baseline: "The reading on both meters is noted by site staff prior to and following injection" and Vaulted's "monthly MRV Report". Requirement: neither PDD quotes protocol text requiring metering; the peer's own text calls it "the lack of primary measured data".

4. **Single-source, single-tier embodied-emissions method with one amortization factor.** Peer: "the mass based method has been selected: Overall mass of equipment, separated by material type, and material emissions factors" (p26), "Attribution factor 0.08% DERIVED" on every embodied line, materials limited to "steel, stainless steel and polyethylene plastic" (p10). Charm baseline: "emission factors from reputable sources such as GREET database, the EcoInvent database, NAICS supply Chain Emission Factors, USLCI database, ICE database, and/or the Athena Impact Estimator... amortized over the expected useful life of the equipment", plus per-mile truck embodied, cost-based railcar embodied, AECN facility cost-based method. Requirement: the peer cites "Section 3.3 of the Embodied Emissions Accounting Module" as offering the mass-based method; no quoted text requires the multi-database approach.

5. **Transport embodied emissions folded into the GLEC factor rather than separate lines.** Peer p9: "The emissions factors used for truck transport include embodied emissions from truck manufacture and fuel production". Charm baseline: separate "Embodied Emissions from Feedstock Transport", "Embodied Emissions from Injectate Transport" lines using GREET per-mile and railcar cost. Requirement: not quoted in either PDD.

6. **No uncertainty discounts on the two sink inputs; two blanket conservatism rules instead of fourteen half-widths.** Peer p48 quotes in Parts 3–4; registry discount 45 kg (0.09% of gross). Charm baseline: "Each of these values are used as the half-width of a uniform distribution of error... propagated to the calculation of the gross quantity". Requirement: both PDDs cite Standard "Section 2.5.7 'Uncertainty'"; neither quotes text that mandates a discount on measured primary data.

7. **Mass by volume × density − moisture from the producer's own records, no scale-ticket reconciliation, no consumables subtraction, no loss allocations.** Peer p20–21, p37. Charm baseline: certified scale, "mass of consumables added... are subtracted", salt residue, tote loss, AECN "+25%" loss allocation "allocated against the oldest BOL first". Requirement: the peer itself says "The existing protocol implies the option to use the scale at the injection site" (p21), i.e. the scale is an option, not a mandate, in the peer's reading; nothing quoted requires the loss allocations (they arise from Charm's multi-supplier, tote-based logistics).

8. **In-house university lab accepted for carbon content instead of an ISO 17025 lab.** Peer: "deemed an in-house lab that is not ISO17025 accredited lab*... An In-house lab is deemed acceptable by Isometric by supplying more information" (p20). Charm baseline: "CHN testing by an ISO accredited laboratory". Requirement: not quoted in either PDD. (This is also a lower-assurance choice — see the burden list below.)

9. **Storage monitoring piggybacks on the injection partner's permit programme.** Peer: brine pH/chloride "Monthly, as per permitting requirements" by the partner (p31); MIT "Every 5 years" (p33); sonar "Annually" (p35); "The Injection Partner is not required to test each delivery" (p29). Charm baseline: Vaulted programme with "Daily readouts", "Quarterly groundwater testing", "Bi-yearly elevation surveys" and, for Basco 6, six-monthly corrosion/gas checks, annual MIT/falloff/tracer. Requirement: Charm's Louisiana items are quoted in the Charm baseline as arising from the Permeable Reservoirs module and LDENR; the peer has no self-operated well. For the salt-cavern leg, neither PDD quotes a protocol cadence.

10. **Spreadsheet + OneDrive data handling, manual Certify entry.** Peer p36, p44–45 (quotes in Part 5). Charm baseline: "Ledger software", "AWS relational database... backed up in S3", "daily snapshots", "transmitted... to Isometric directly via API". Requirement: not a protocol matter in either text; Charm's is a capital/engineering cost, the peer's a labour cost.

11. **Shorter documentation set.** PDD 87 pages vs ≥155; GHG Statement 12 pages pointing to Certify ("See Isometric Certify for a breakdown of the results.", p10; "Please refer to the PDD for the project details.", p3); Section F empty. Charm baseline Appendix 6 is 16,191 computed words of repeated per-line methodology. Requirement: the GHG Statement template (p1) permits referring back after the first completion.

12. **Fewer evidence files per removal.** Seven batch-specific files for rmv_1M0B59RM61S0BW9G (Part 6); Verification Report Appendix I: 88 source rows for four removals. Charm baseline per-batch set listed in Part 7.6. Requirement: not quoted.

13. **Single feedstock type per statement and a fixed local supplier radius.** "Typically, this waste is within a 40km radius of the Saskatoon Plant." (p7); the verified statement used sludge only. Charm baseline: five feedstock appendices, two producers, rail + truck legs. Design difference, not protocol.

**Where the peer is MORE burdensome or LOWER-integrity than Charm**
- More burdensome: three carbon samples per production day, each in duplicate ("three (3) unique samples... Each sample is tested in duplicates", p48; Verification Report p14 "Bio-oil samples are collected three times per day") versus Charm's one sample per injection batch. Moisture tested "on three bio-oil samples from every HTL production run" (p21). Tailgas GC per feedstock/operating condition and a per-run material-balance tailgas mass (p21). δ13C isotope testing that is "not required under the protocol" (p30). Injectant pH and chloride per batch tested by NULIFE itself (p30). Staff commuting tracked (then excluded). A separate pre-injection brine-carbon baseline and tedlar-bag gas sampling programme (p29, p32).
- Lower integrity (the peer's own text): carbon lab "not ISO17025 accredited" (p20); injection electricity "lack of primary measured data" (p48); a production run with no carbon data filled by "the conservative value of 70% carbon is assumed" (p48); fixed gas monitor not yet installed ("we anticipate implementation for Q4 2025", p32); external well integrity "There is no way of knowing the outside integrity" (p33); cavern temperature not measured ("the injection partner can predict the temperature inside the cavern", p34); MIT only "Every 5 years" (p33); wastewater transport mass described inconsistently ("scale ticket at the injection site" p24 vs "bill of lading invoice with pick up volume" p38); registry crediting period (10 years) disagrees with the PDD (5 years); the datapoint label "Conion of warming potential (Methane)" is a typo carried into the registry. Verification Report p8 also records that Normec's "on-site visit was conducted on the 20th of August 2025" — one year before the RP verified — and p20 "No significant findings".
- Neutral/ambiguous: the peer's sink mass is below the scale mass (17.607 t vs 18.360 t), which is conservative for the sink but means the transport/injection lines are computed on a higher mass than the sink — internally consistent with the PDD's stated reason ("the moisture must be accounted for", p21).

---

## Source List

All read 2026-09-14.

- https://registry.isometric.com/project/prj_1JQEQKCF91S06HAJ — project page (Summary, Project details, Feedstocks table, Project documentation table page 1 "Showing 5 of 18", Certificates Issuances table, Reversal risk). Read via playwright-mrv headless browser; two accessibility snapshots and one innerText/table extraction.
- https://registry.isometric.com/ghg-entry/rmv_1M0B59RM61S0BW9G?tab=calculation-view — Calculation view tab (innerText).
- https://registry.isometric.com/ghg-entry/rmv_1M0B59RM61S0BW9G?tab=removal-method — Removal method tab (innerText).
- https://registry.isometric.com/ghg-entry/rmv_1M0B59RM61S0BW9G?tab=data-points — Datapoints tab, reached by clicking the "Datapoints" tab (innerText). Saved to `raw/nulife_pdfs/rmv_1M0B59RM61S0BW9G_calc_and_datapoints_2026-09-14.txt`.
- https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1K6DV5H3Z1S069JC/pdd.pdf — PDD, local copy `raw/nulife_pdfs/nulife_pdd.pdf` (1,188,344 bytes, MD5 matches server header), pages 1–87 read with the Read tool in five chunks (1–20, 21–40, 41–60, 61–80, 81–87).
- https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1M0ZJNP5H1S0JYG1/ghg_statement_report.pdf — GHG Statement Report (registry row 26 Aug 2026), local copy `raw/nulife_pdfs/nulife_ghg_2026-08-26.pdf` (353,611 bytes, MD5 matches), pages 1–12 read.
- https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1M0ZJPF4D1S01HYN/verification_report.pdf — Verification Report (registry row 26 Aug 2026), local copy `raw/nulife_pdfs/nulife_verification_2026-08-26.pdf` (1,001,514 bytes, MD5 matches), pages 1–28 read in two chunks (1–20, 21–28).
- `/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/research/isometric_registry_review_2026-09/02_charm_pdd_baseline.md` — Charm PDD profile, read in full (353 lines).
- `/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/research/isometric_registry_review_2026-09/01_registry_census.md` — lines matching "NULIFE"/"Ontario" only (rows 14, 51, project block at line 292 ff.).
- `raw/docs_nulife_p2.json`, `raw/docs_nulife_p3.json`, `raw/docs_nulife_p4.json` — documentation-table pages 2–4 (13 of the 18 rows) from the earlier census run.
- `raw/nulife_pdfs/README_text_extraction_2026-09-14.txt` — record of why no machine word count exists.
- Not read: the protocol, module and Standard texts themselves; the PDD's attachments (sensitivity analysis, "Carbon content lab test requirements v1.0", REC details, feedstock letters); the 15 older GHG Statement / Verification Reports; the Charm calculation-view JSON in `raw/`.
