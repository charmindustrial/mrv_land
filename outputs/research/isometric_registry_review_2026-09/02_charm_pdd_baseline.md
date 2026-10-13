# Charm Industrial PDD — Baseline Profile

Prepared 2026-09-14 for the Isometric registry peer-comparison review. Every quote below is verbatim from the document text read this session. Section references are to the document's own headings (Section A–F, Appendix 1–11) and, where a section is a single long table cell, to the row label inside that table (e.g. "Section B > Monitoring Plan").

Access method: the Google Drive connector's `download_file_content` on file ID `1V0v2atno-pVZQZ983EEy9sfmlci4cm_C` returned the file as a base64-encoded Word document (the file is a .docx stored in Drive, not a native Google Doc). I decoded it, extracted every paragraph and table cell in document order (including merged cells and the protocol-requirement tables in Appendix 8, which a first-pass extractor had dropped: first pass 51,431 computed words, full pass 58,881 computed words, difference 58,881 − 51,431 = 7,450), and read the full text in chunks. The headless browser was not needed. Word comments (22 in the file's comments part) are not part of the document body and were not read.

Two items the document references but does not contain: "Supplemental Doc 3" (the Basco 6 "Combined Emissions Monitoring and Accounting Plan") and the "GHG Statement Supplemental Doc" (calculation sheets). Wherever the PDD hands off to those, this profile says so.

---

## 1. Document length and structure

**Word count:** 58,881 words in the document body (all paragraphs and table cells, including the Isometric template's own question prompts, which the document retains in every table). Charm's answer text alone is smaller, but the template prompts are part of the document as submitted so they are counted.

**Page count:** Not stored in the file's properties (no app.xml). The document's own Table of Contents gives page starts; the last entry is "Appendix 11: Biochar Production and Storage PDD Appendix……. 155". So the document is at least 155 pages long by its own table of contents; the exact total is not determinable from the file.

**Version/date shown:** Title line "Charm Industrial Bio-Oil Geologic Storage + Range & Plains Biochar Design Document" followed by "v1.12 – 2025/12/01". Drive filename: "Final V 1.12 Charm Industrial Bio Oil Geologic Storage PDD + Biochar.docx". Drive last-modified 2026-09-11.

**Top-level sections:** 17 (six lettered sections + eleven appendices).

| # | Section (document heading) | TOC page | Approx. words |
|---|---|---|---|
| — | Title + Table of Contents | 1 | 180 |
| A | Section A – Key Project Data | 2 | 1,708 |
| B | Section B – Protocol and Monitoring Data | 7 | 14,978 |
| C | Section C – Duration & Crediting Period | 51 | 312 |
| D | Section D – Environmental and social impacts | 52 | 3,192 |
| E | E – Stakeholder Input Process | 61 | 1,792 |
| F | Section F – Project Changes | 70 | 2,100 |
| App 1 | Appendix 1: AECN Biomass Feedstock Information | 72 | 1,238 |
| App 2 | Appendix 2: Charm Biomass Feedstock Information – MacArthur Gulch | 76 | 1,450 |
| App 3 | Appendix 3: Charm Biomass Feedstock Information – Arkansas Mountain | 81 | 1,469 |
| App 4 | Appendix 4: Charm Biomass Feedstock Information – Arroyo Chico | 86 | 1,480 |
| App 5 | Appendix 5: Charm Biomass Feedstock Information – Boulder Creek Watershed Project | 91 | 1,471 |
| App 6 | Appendix 6: GHG Statement Report | 96 | 16,191 |
| App 7 | Appendix 7: BCU Calculation Methodology | 137 | 1,138 |
| App 8 | Appendix 8 – Basco 6 EW Bio-oil Sequestration Site Permanence Monitoring and Permit Compliance Plan | 140 | 3,847 |
| App 9 | Appendix 9: Basco 6 Bio-Oil Sequestration Site Well Closure and Remediation Plan | 149 | 803 |
| App 10 | Appendix 10: Basco 6 Supplementary Subsurface Characterization | 151 | 984 |
| App 11 | Appendix 11: Biochar Production and Storage PDD Appendix | 155 | 4,548 |

All word counts in this profile are COMPUTED from the extracted text (count of whitespace-separated tokens, table markup removed), not taken from the document. Section B and Appendix 6 together: 14,978 + 16,191 = 31,169 words; 31,169 ÷ 58,881 = 0.529; 0.529 × 100 = 52.9% of the document. Within Section B, the largest single table cells (same counting method) are: the Monitoring Plan answer cell, 3,527 words; the Data collection and storage answer cell, 1,762 words; the Uncertainty assessment "Justification for your choice of uncertainty approach" cell, 2,067 words. Within Appendix 6: "GHG Statement Methodology - Data" answer cell, 5,856 words; "GHG Statement Methodology - Calculations" answer cell, 9,287 words — the two largest cells in the document.

Sub-headings inside appendices: Appendix 8 has 7 sub-sections (Permitting; Site Characterization and Feasibility Requirements; Well construction requirements; Injection and injectant operation & monitoring; System Integrity Monitoring; Migration and Storage Reversal Monitoring; Post-injection Monitoring Plan, with 5 further sub-headings). Appendix 9 has 5. Appendix 10 has 4 plus Attachments and References. Appendix 11 has 7 (Key Project Process Data; Environmental Safeguards; Storage in Agricultural Soils; Characterization Requirements; Sampling Procedure; Biochar Durability method; Environmental Monitoring - Site selection).

---

## 2. Project basics

**Project title (Section A > Title):** "Charm Industrial Great Plains Bio-Oil Sequestration"

**Pathway (Section A > Description):** "Charm produces bio-oil at our pyrolysis facility in Fort Lupton, CO from non-merchantable woody biomass sourced from government-funded wildfire mitigation/management projects. Charm procures pyrolysis bio-oil produced by AE Cote-Nord Canada Bioenergy Inc (AECN) from waste material produced by a nearby lumber mill. … We are using a combination of rail and truck to transport the bio-oil to our pre-processing site in Kansas where it is treated to fit the local regulatory requirements for injection before being transported to one of two injection sites: Vaulted in Hutchinson, KS or Charm's own injection site in Evangeline Parish, LA."

**Protocols cited (Section B > Selected Certified Protocol):**
- "Protocol Name:  Bio Oil Geological Storage" / "Protocol Version Number: v1.0"
- "Protocol Name: Biochar Production and Storage" / "Protocol Version Number: v1.0"
- "Protocol Name: Biochar Storage in Agricultural Soils" / "Protocol Version Number: v1.0"

**Modules cited by name in the text (with version where the text gives one):**
- "Isometric Biomass Feedstock Accounting Module v1.2" (Section B > Baseline scenario)
- "Transportation Emissions Accounting module v1.1" (Section F, 2/19/25 entry)
- "Energy Use Accounting module Section 5 and the eligibility criteria outlined in Section 6" (Section F, 4/8/25 entry) — no version number given
- "Salt Cavern Storage module Section 3.1.1" and "Biomass or Bio-Oil Storage in Salt Caverns module" (Section B > Monitoring Plan; Section F) — no version given
- "Isometric's Bio-oil Storage in Permeable Reservoirs ('Protocol') module" (Appendix 8) — no version given
- Isometric Standard sections cited: 2.5.2, 2.5.3, 2.5.4, 2.5.7, 3.1, 3.5, 3.7, 5.6.1, 7.4
- Bio-Oil Geological Storage protocol sections cited: 7.4.1.1.1, 7.4.3.5, 7.3.3.1 (the last in the Appendix 8 requirement text)

**Sites (Section A > Project Location(s)):**
- Pyrolysis: "Charm Industrial, 2360 S Rollie Ave, Fort Lupton, CO 80621"; "Lot 3, Thomas Subdivision, Fort Lupton, CO 80621 (ancillary biomass storage site for Charm pyrolysis)"; "Produits Forestiers Arbec S.E.N.C., 175 Bd du Portage des Mousses, Port-Cartier, QC G0W 1X0, Canada"
- Pre-processing: "838 SW Purity Springs Rd El Dorado, KS 67042"
- Injection: "Underground Cavern Stabilization, 7513 KS-14, Hutchinson, KS 67501" and "Evangeline Parish, Louisiana / 30.916251, -92.297908"

**Participants (Section A > Project Participants):** Charm Industrial ("The carbon removal company who will fund and manage the offtake, transportation and treatment of the bio-oil and sell the CDR credits"); Carbon Removal Co., Inc. dba Vaulted Deep ("Injection well operator"); AE Cote-Nord Canada Bioenergy Inc. ("Bio-Oil Vendor"). Appendices 2–5 add Altitude Forestry as "Biomass Supplier".

**Feedstock types:**
- AECN (Appendix 1): "sawdust and shavings from a lumber mill adjacent to the bio-oil provider, AECN … A small portion (10%) of the feedstock consists of chipped unmerchantable roundwood that had been previously harvested and transported to AECN."
- Charm (Appendices 2–5): "non-sawmill quality Ponderosa Pines and Douglas Firs from a wildfire mitigation project managed by the Colorado State Forest Service (CSFS)" — four named projects: McArthur Gulch, Arkansas Mountain, Arroyo Chico II, Boulder Creek Watershed.

**Storage type:**
- Kansas (Section B > Storage well overview): "'Vaulted operates a built and permitted injection well site in Hutchinson, Kansas. This site is a network of 60 salt caverns, with the total capacity to hold 2-3 million metric tons of organic waste. The wells are permitted under Class UIC V well permits by KDHE.'" Permit "KS-05-155-003", valid "2022/08/02" to "2027/08/02".
- Louisiana (same table): "Charm has converted the formerly orphaned Basco 6 Class II SWD to a permitted Class V for the purpose of injecting the bio-oil into subsurface geologic formations. The wellbore configuration … is completed in the Lower Miocene formation from 3,492-3,534' KB." Permit "IMD 2025-05 EW", valid "8/8/2025" to "8/7/2030". Capacity "Estimated range: 465,000 to 840,000 MT".
- Biochar (Appendix 11): "Charm will claim 200-year durability biochar carbon credits" via application to agricultural soils.

**Crediting period (Section C):** "Start date of Project: 2024/03/01"; "Start date of crediting period: 2024/03/01"; "Total length of crediting period: 5 years". No operational closure date given.

**Reporting-period cadence:** The PDD does not state a fixed calendar cadence. It defines the term: "A Reporting Period designates the reporting of all removals completed between a start and end date and the reporting of associated CDR calculations" (Appendix 6 > Calculations). Section F refers to "the April/May Reporting Period", implying roughly monthly-to-bimonthly periods in practice. Production Periods for Charm bio-oil are defined separately: "An example Production Period would be the month of January 2025" (Appendix 11 > Sampling Procedure), and Section F says "starting with Production Period 7, which covers June production".

**Estimated capacity (Section A):** 2024: "10,000"; 2025: "25,000"; 2026–2028: "TBD – 25,000 +".

---

## 3. System boundary and every emission source / sink / reservoir

**Boundary description (Section B > Project Boundary):** "All project activities undertaken to permanently sequester carbon are considered within the system boundary including: transportation of biomass feedstock to pyrolysis, the process of pyrolysis itself, transportation of injectate to and from pre-processing, the pre-processing itself, injection and monitoring activities. Embodied emissions associated with equipment procured or contracted by Charm for the purposes of project execution are included. The emissions resulting from the direct and induced use of energy (fuel, electricity) and the embodied emissions of non-waste consumables are included."

Upstream exclusion: "The harvesting of the biomass and transportation to the collection site is not contingent on the project, so upstream emissions associated with these processes are not included in the project boundary." (Charm feedstock) and "the upstream emissions associated with growing, harvesting, transporting and producing the biomass are not included within the boundary." (AECN)

**The boundary table** (Section B) lists 40 rows. Each row below gives the flux name, inclusion, gases, and how the PDD says it is quantified.

Baseline rows (8):
1. Counterfactual Fuel Use, Feedstock Sourcing – AECN — Excluded — "There is no additional fuel usage on the part of the feedstock supplier due to project activities."
2. Same – Charm — Excluded — same reasoning.
3. Counterfactual Electricity Use – AECN — Excluded.
4. Same – Charm — Excluded.
5. Replacement of Feedstock Function – AECN — Excluded — "replacement emissions are considered 0 based on Biomass Feedstock Sourcing criterion C1: The feedstock currently serves no purpose."
6. Same – Charm — Excluded — same criterion C1.
7. Temporary Carbon Storage from Feedstock – AECN — Included, CO2, CH4 — "Research on sawdust piles (Pier and Kelly, 1997) has shown that due to anaerobic conditions within the pile, the total global warming potential of pile emissions within 15 years would be greater than the emissions from a total release of biogenic carbon due to the production of methane. Charm is only calculating removal credits in terms of the release of biogenic carbon." Appendix 1 gives the number: "we are assigning the sawmill residues used by AECN as a pyrolysis feedstock a counterfactual storage discount of 0."
8. Temporary Carbon Storage – Charm — Included, CO2, CH4 — "it has a counterfactual storage value of 0 per EC14 in the Isometric Biomass Feedstock Accounting module."

Project rows (32), with quantification method:
9. Feedstock Sustainable Sourcing – AECN — Included, N/A gases — documentary (Provincial Management Plan, SFI certificate).
10. Feedstock Sustainable Sourcing – Charm — Included, N/A — documentary (CSFS program).
11. Fuel Use from Feedstock Transport – AECN — Included — "provided as part of bio oil vendor LCA" (vendor-supplied factor).
12. Fuel Use from Feedstock Transport – Charm — Included — calculated: "Distance Based Method outlined in the Isometric Transportation Emissions Accounting module, using scale tickets to document the mass transported. Additional fuel used in feedstock handling is calculated per ton of feedstock based on an average fuel consumption factor for lumber handling".
13. Embodied Emissions from Feedstock Transport – Charm — Included — default factor: "Per-mile embodied emissions are calculated based on GREET emissions levels for the manufacture of medium-and-heavy-duty trucks and trailers and divided by EPA expected useful life in mileage".
14. Fuel Use from Biomass Pyrolysis – AECN — Included — vendor LCA.
15. Fuel Use from Biomass Pyrolysis – Charm — Included — measured (invoices) × factor: "GLEC emission factors for fuel combustion in terms of TCO2e/kg fuel multiplied by the quantity of fuel purchased for production on site as documented by purchase invoices. This quantity is adjusted for fuel pump uncertainty".
16. Electricity Use from Biomass Pyrolysis – AECN — Included — vendor LCA.
17. Electricity Use from Biomass Pyrolysis – Charm — Included — measured (utility meter) × factor: "kWh usage multiplied by the per kWh emissions for the RMPA grid subregion as reported by the EPA eGrid emissions factors, modified by Green-e to show residual grid mix … supplemented by a per-kWh addition to account for the embodied emissions associated with grid infrastructure … This quantity is adjusted for meter uncertainty".
18. Stack Emissions from Biomass Pyrolysis – AECN — Included, CH4, NO2 — modeled: "Charm is using an analysis of the same technology pyrolyzing woody biomass as reported by their LCA software provider (GHGenius) to the Canadian Government".
19. Stack Emissions from Biomass Pyrolysis – Charm — Included, CH4, NO2 — sampled then scaled: "For each type of feedstock processed, Charm has a tail gas composition testing performed by a qualified practitioner. This data is used by Charm's engineering team to calculate a quantity of tailgas emitted per kg of biomass processed. This quantity is then scaled based on the biomass throughput recorded for production."
20. Embodied Emissions, Facilities/Equipment Pyrolysis – AECN — Included — cost-based: "applying per-dollar-spent supply chain emissions factors to the cost of construction and equipment and dividing that total by the expected lifetime production of the facility".
21. Embodied Emissions, Facilities/Equipment Pyrolysis – Charm — Included — inventory + LCA factors: "emission factors from reputable sources such as GREET database, the EcoInvent database, NAICS supply Chain Emission Factors, USLCI database, ICE database, and/or the Athena Impact Estimator. These values are amortized over the expected useful life of the equipment and improvements used, which is estimated in terms of total expected facility biomass throughput".
22. Fuel Use from Injectate Transport to Pre-Processing — Included — calculated: "GLEC emission factors using cargo weight, vehicle type, and distance traveled with a correction for truck scale uncertainty".
23. Embodied Emissions from Injectate Transport to Pre-Processing — Included — GREET per-mile for trucks; "Because GREET does not provide comparable emission factors for the manufacturer of railcars, a cost-based calculation is used based on the average cost and expected useful life of a DOT-111 railcar".
24. Electricity Use from Injectate Pre-Processing — Included — measured × SPP North eGrid factor, same structure as row 17.
25. Fuel Use from Injectate Pre-Processing — Included — invoices × GLEC, "corrected for fuel pump uncertainty".
26. Embodied Emissions, Facilities/Equipment Pre-Processing — Included — inventory + LCA factors, amortized.
27. Embodied Emissions from Consumables, Pre-Processing — Included — measured (flow meter) × GREET: "When liquid caustic soda (LCS) is added to the bio oil, the volume is measured by on-site staff using a flow-meter. … The salt added to the oil is not included because it is an incidental waste-product (off-spec/non-saleable salt) from a salt production facility".
28. Fuel Use from Consumables Transport to Pre-Processing — Included — GLEC distance-based.
29. Embodied Emissions from Consumables Transport — Included — GREET per-mile.
30. Fuel Use from Processed Injectate Transport to Injection Site — Included — GLEC distance-based.
31. Embodied Emissions from Injectate Transport (second listing, same method) — Included.
32. Electricity Use from Injection (Vaulted) — Included — operator-reported: "The Well Operator is required to provide a report on energy usage specific to Charm emplacements."
33. Electricity Use from Injection (Charm) — inclusion column blank — "See the Combined Emissions Monitoring and Accounting Plan for the site, included in Supplemental Doc 3".
34. Fuel Use from Injection (Vaulted) — Included — "monthly report on energy usage specific to Charm emplacements … corrected for fuel pump uncertainty". Appendix 6 then notes Vaulted's own PDD "does not report any fuel use, therefore fuel use is not accounted for here."
35. Fuel Use from Injection (Charm) — blank — Supplemental Doc 3.
36. Embodied Emissions from Injection Equipment (Vaulted) — Included — "Vaulted … reported the embodied emissions associated with the injection equipment on their site divided by the estimated well capacity to arrive at a quantity of embodied emissions per emplaced tonne of material." Appendix 6 gives the values: "0.0000351566 tons of steel and 0.000077 m3 of concrete per ton of waste injected, given their conservative estimate of a 2 million metric ton overall well capacity."
37. Embodied Emissions from Injection Equipment (Charm) — blank — Supplemental Doc 3.
38. Water use from Injection (Charm) — blank — Supplemental Doc 3.
39. Fuel Use from Consumables Transport to Injection Site (Charm) — blank — Supplemental Doc 3.
40. Embodied Emissions from Consumables Transport to Injection Site (Charm) — blank — Supplemental Doc 3.
41. Carbon Content of Injected Bio Oil (Vaulted) — Included, CO2 — the sink; see Part 4.
42. Carbon Content of Injected Bio Oil (Charm) — blank — Supplemental Doc 3.
43. Transport Emissions from Transport of Test Samples to Lab — Included — "Emissions are calculated for air shipment of samples based on a conservative estimate of the point-to-point distance between the sampling site and labs in Google maps."

(Rows 33, 35, 37–40, 42 — seven Basco 6 rows — have empty Included/Excluded and gas columns in the table; the PDD delegates them entirely to Supplemental Doc 3, which is not in this document.)

Two further sources appear only in Appendix 6, not in the boundary table: **Disposal of Process Waste** (transport + "Emissions from Material Disposal and Decomposition", added per Section F 2/19/25: "Site operations began to generate bio-oil process wastes in H2 of 2024") and **Thermal Oxidizer Emissions** at El Dorado, which the Monitoring Plan treats as "De minimis as a potential source of GHG emissions" and monitors "indirectly in terms of site production capacity".

**Uncertainty treatment (Section B > Uncertainty assessment):** Option ticked: "Variance propagation". Screening rule: "the value of each source was arbitrarily increased by 20% … Any parameter that, when increased by 20%, contributed to a change in the estimated removal that was greater than 1% of the original estimation was then subject to an Uncertainty Analysis". Parameters and their stated half-widths:
- AECN process emissions: "An Uncertainty Factor has been calculated for this emissions factor based on process and data quality considerations as outlined in Section 7.4 of the Isometric Standard."
- GLEC transport factors: "There is no Uncertainty Factor calculated for this value. This is due to previous consultations with Isometric confirming that the GLEC factors are based on millions of miles of data".
- Truck scales: "The maximum allowable error for a legal-for-trade truck scale is 160 lbs for a fully-loaded truck … using 160 lbs as the half-width of a uniform distribution of scale error."
- Fuel meters: "The maximum allowable error for a legal-for-trade fuel meter is .28%".
- LCS flow meter: "2.045% as the uncertainty for a calibrated flow meter" (Dias, Filho, and de Lucca 2013).
- Carbon analyzer: "The relative standard deviation reported by the manufacturer of the LECO instrument used to measure carbon is .4%."
- Electricity meter: "The Colorado Code of Regulations (page 41) requires that the maximum measurement error for a service meter is 2%."
- Biomass scale: "calibrated Class III scale with a tolerance of +/- 25 lbs"; finished bio-oil scale: "+/- 2.5 lb".
- Hotflow hours: "the measurement uncertainty for time in hotflow is no greater than 1%" (engineering judgement).
- Basco 6: "Sensitivity analysis and uncertainty modifications for Basco 6 Louisiana injection operations are included in the … Basco 6 Supplemental Doc".

Routing conservativeness applied throughout: "When multiple routes are presented, the longest route is assumed to ensure a conservative estimate of removals".

---

## 4. Gross removal calculation

**Formula (Section B > Monitoring Plan > Injectate Characterization):** "The injectate C content is computed by multiplying the Mass of Bio Oil Injected by the average C content of the sample as established by lab testing. This is then multiplied by 44/12 to convert the C content to the equivalent in CO2e."

**Mass:** "Mass is monitored by Scale Tickets provided by the injection well personnel. / These values are measured by weighing the delivery truck prior to and after injection on a certified scale" and "The mass of consumables added to the bio-oil being processed are subtracted from the Total Injectate Mass to compute the Mass of Bio-Oil Injected".

**Carbon content and sampling point:** "Bio-oil is sampled after the sparging process, but prior to the addition of consumables, and samples are sent to an ISO accredited analytical laboratory for the quantification of C content / Bio-oil is sampled at this point in the process because the addition of consumables causes phase separation, which precludes samples from being the 'well-mixed and representative aliquot' required by section 7.4.1.1.1 of the Bio-Oil Geological Storage protocol".

**Sampling frequency:** "Per section 7.4.1.1.1 of the Bio-Oil Geological Storage protocol, a sample is taken for each injection batch and analyzed for C content to quantify the gross removal". Appendix 6 restates: "Carbon content of the oil will be measured using Isometric Protocol Method A – Each injection batch will be sampled prior to the addition of salt and LCS and one sample will be sent to an analytic lab to measure the carbon content of that batch."

**Lab method:** "CHN testing by an ISO accredited laboratory" (Section B > Uncertainty). Instrument named: "the LECO instrument used to measure carbon".

**Adjustments to mass:**
- Consumables subtraction (salt + LCS) as above.
- Salt residue credit (Section F, 9/9/25): "multiple rounds of samples have been taken which show that the residue ranges from roughly 75-85% salt, with the remainder composed of entrained bio-oil. From the April/May Reporting Period on, 70% (used as a conservative estimate) of the estimated mass of the remaining residue may be counted towards the total salt added to the subsequent injection batch, provided the tank is not cleaned in between batches."
- Tote standard loss (Section F, 9/9/25): "This was computed by taking the full and empty weights of 59 bio-oil totes and taking the average. That average was then increased by 25% to ensure that the estimate would be conservative. Rather than take the empty weight of each individual tote, this standard loss (which came out to 5.33kg) is assumed for each tote of 'oily fraction' Charm bio-oil used. There will be an annual revision of this estimate".
- Upstream loss allocation for AECN (Section F, 9/9/25): "upstream emissions are allocated to injection batches by subtracting the Mass of Bio Oil Injected from the estimated Input Mass. Because the Input Mass is an estimate, that loss estimate is increased by 25% in order to ensure removals are accounted for conservatively … The emissions are allocated against the oldest BOL first".
- Filtration loss: the words "filtration" / "Filtration" do not appear anywhere in the document text (text search, 0 hits). No filtration adjustment is described in this PDD.

**Uncertainty on gross:** "The maximum allowable error for a legal-for-trade truck scale is 160 lbs for a fully-loaded truck. The relative standard deviation reported by the manufacturer of the LECO instrument used to measure carbon is .4%. Each of these values are used as the half-width of a uniform distribution of error for their respective associated measurements. These uncertainties are propagated to the calculation of the gross quantity of CO2e sequestered for each injection batch."

**Basco 6 gross calculation:** delegated — "Carbon Content of Injected Bio Oil (Charm) … See the Combined Emissions Monitoring and Accounting Plan for the site, included in Supplemental Doc 3".

---

## 5. Monitoring plan

**Option chosen (Section B > Monitoring Plan):** "B – I have submitted a Monitoring Plan, which meets the requirements specified in the 'Monitoring Plan Requirements' appendix of the relevant Protocol and its associated modules, and which describes any additional or modified parameters monitored which deviate from the default Monitoring Plan".

### 5a. Emissions-side monitoring (who / how often / instrument / evidence)

| Parameter | Frequency | Instrument / source | Evidence produced |
|---|---|---|---|
| Biomass delivery mass (Charm) | each delivery | "Scale Tickets provided by a certified truck scale for each delivery" | scale ticket |
| Biomass stockpile consumption | each Production Period | "measuring the linear feet of raw logs before and after processing" | log-length records |
| Pyrolyzer up-time (allocation basis) | continuous | "logged automatically using telemetry" | telemetry |
| Diesel / propane / gasoline (CO) | per purchase | "Vendor invoices" | invoices |
| Electricity (CO) | per Production Period | "Total facility usage reported by power utility less estimated G+A usage" | utility portal data |
| Water (CO) | continuous | "flow meter" | meter reading |
| Tailgas (CO) | "for each type of feedstock processed" | "tailgas composition testing performed by a qualified practitioner" | stack test report |
| AECN process emissions | "at least annually, or in light of major operational changes" | vendor LCA (GHGenius) | LCA document |
| Bio-oil transport mass | per load | "Bill of Lading, Scale Ticket and Invoice documents provided by the bio-oil producer, or by weighing each container" | BOL / ticket / invoice |
| Transport distance | per route | "Google Maps … longest route"; rail: "provided by the transport provider" | route record |
| El Dorado electricity | monthly | "utility invoices" | invoices |
| El Dorado diesel | per delivery | "invoices the vendor provides" | invoices |
| LCS addition | each batch | "flow meter" | ledger entry |
| Salt addition | each batch | "digital scale" | ledger entry |
| Consumables deliveries | each delivery | "invoiced quantities" + Google Maps | invoices |
| Thermal oxidizer | indirect | "monitored indirectly in terms of site production capacity" | — |
| Vaulted electricity | each injection, reported monthly | "The reading on both meters is noted by site staff prior to and following injection" | "monthly MRV Report" |
| Injectate mass | each load | Vaulted certified scale | scale ticket |
| Regulatory compliance (third parties) | annual | "All third-party project participants are queried annually … required to return a signed affirmation" | signed affirmation |

### 5b. Storage-side monitoring, Kansas (Section B > "Monitoring Plan parameters relevant to the Biomass or Bio-oil Storage in Salt Caverns module")

Pre-injection baseline, all "Once", "Prior to first emplacement", results "reported to and stored by Charm": brine pH (Vaulted, "pH meter"), brine temperature (Vaulted, "Thermometer"), brine conductivity/chloride (Vaulted, "Electrical Conductivity meter"), brine TOC (Vaulted, "TOC analyser or shipment to an ISO-certified analytical laboratory"), wellhead gas composition (Charm, "Gas samples collected at wellhead and sent to ISO-certified analytical laboratory").

Injectate and operational:
- Injectate pH — Vaulted — "One sample per day of injection" — "pH meter" — "recorded on the inspection report/weight scale ticket form … Values are input into the Charm Ledger". Acceptance rule: "Injectate will not be injected if the pH reading is below 4.0".
- Injectate temperature — Vaulted — "One sample per day of injection" — "Thermometer" — same form.
- Injectate conductivity/chloride — Charm — "For each injection batch" — "field notes and records of how much salt is added".
- Injectate TAN — Charm — "Every injection batch – Frequency may decrease if data shows significant consistency across batches" — "ISO-accredited analytical laboratory".
- Injectate density — Charm — "Every injection batch" — "ISO-accredited analytical laboratory; lab to report results relative to specific temperature".

Displaced brine:
- % C by wt — Vaulted — "Every two weeks for 3 months. If measurements are consistent this can be changed to every month for 6 months, then quarterly for 2 years, and finally every 6 months if results remain consistent."
- Temperature and pH — Vaulted — "Initially, after each injection. Frequency can be reduced once consistency between samples is statistically proven".
- Chloride/conductivity — Vaulted — "Initially, once per day of emplacement. Frequency can be reduced once consistency between samples is statistically proven".

Cavern integrity (Vaulted responsibility, no frequencies given in the PDD): "Internal Well Integrity / External Well Integrity / Cavern Temperature / Cavern Pressure / Cavern Volume and Fill (Sonar Survey) / Wellhead Gas Composition / Gas Isotope Stability if Wellhead Gas Composition is outside of normal average baseline range / Surface Subsidence / USDW Quality / Salt permeability / Porosity and Permeability of caprock and any interbeds / Existing subsurface features such as faults". Vaulted's quoted PDD text adds: "Quarterly groundwater testing … Monthly reporting on total volume of emplaced material / Daily readouts of pressures and stability of the subsurface caverns / Bi-yearly elevation surveys".

Reversal notification: "the well operator has affirmed that they will contact Charm within a 2-hour period" of a gas alarm; "Reports will be made between 1 and 3 business days from the identification of a gaseous release per Section 5.6.1 of the Isometric Standard".

### 5c. Storage-side monitoring, Louisiana (Appendix 8)

- "LDENR issued the MASIP at 455 psi. Continuous recording devices will capture flowrate, injection volume, tubing, annulus and bottomhole pressures, and bottomhole temperature for regulatory reporting."
- "Injectant samples will be taken at a frequency mandated by LDENR to confirm pH, density, viscosity, TAN and carbon content and/or as required by the approved UIC permit."
- "Production batches, representing a change in biomass feedstock or pyrolysis process, will extend the above analysis to include major anions and cations."
- "Wellhead gas detection will be performed every 6 mos to confirm no gas leakage at surface."
- "Corrosion monitoring will be performed at a 6 month frequency. Witnessed mechanical integrity tests will be conducted annually per LDENR. A pressure falloff test will be performed annually."
- "Vertical migration will be monitored annually via radioactive tracer survey."
- "Charm does not operate an offset well in the immediate vicinity of the Basco 6 EW. As a result, Charm will estimate the radius of the pressure front throughout operations."
- Not expected: "Groundwater monitoring … is not anticipated to be required by LDENR."; "A seismic monitoring program … is not expected to be required by LDENR."
- Baseline geochemistry recorded (Appendix 10): bicarbonate 502 mg/L, pH 7.7, δ13C of DIC +5.4‰, methane 0.045–1.2 % v/v, etc., with methods (EPA 2320B-2011, ASTM D1946, Isotech Lab 2024).

### 5d. Biochar monitoring (Appendix 11)

"Charm will submit 3 replicates per Production Period for analysis of C content, moisture content, and H:Corg." One-time at validation: O:Corg, volatile matter, ash, PAH. Labs: Soil Control Labs (ASTM D5373, D4373, D1762-84), Eurofins (PCB/PCDD/F), BSK Associates (EPA 8270E). Reactor safety: "DPs are calibrated weekly"; SCADA checks "at 60hz". Storage sites: "At the conclusion of each growing season following biochar application Charm may contact the offtaker to collect information".

---

## 6. Batch / reporting structure

**Custody unit — the "Lot" (Section B > Data collection and storage):** "Once a given batch of bio-oil comes into Charm's custody, as defined by issuance of a Bill of Lading, scale ticket and invoice document as discussed earlier in this section, the batch becomes a 'Lot' in the Ledger. / The software is designed to measure and track Lots as they are split and combined, maintaining a clear mass balance and chain of custody as they move between transport modes (e.g. truck to railcar to truck) and are stored, batched, and treated along the pathway to injection. Once a given Lot, or batched combination of several split Lots, is injected it is then logged as a Removal."

**Removal calculation:** "When a Removal is completed, the CHN testing associated with that removal assigns it a C and CO2e content, from which both process emissions and either all or a portion of site emissions for the reporting period in which the Removal is claimed, are deducted in order to compute the Net CDR for a given Removal".

**Two emission classes (Appendix 6 > Calculations > "Additional Summary: Lot Emissions vs. Site Emissions"):** "Lot Emissions are emissions that can be clearly associated with a particular lot of bio oil … Site Emissions are emissions that cannot be associated with a specific lot of oil, but are associated with a particular processing site. These emissions are accrued to the site and deducted from removals associated with the site each reporting period."
- Lot Emissions listed: pyrolysis process and embodied emissions, feedstock transport, injectate transport to pre-processing (fuel + embodied), LCS embodied, transport to injection site (fuel + embodied), injection equipment embodied, "Carbon Content of Injected Biomass (contra-emission)", sample transport.
- Site Emissions listed: pre-processing electricity and fuel, consumables delivery (fuel + embodied), injection electricity and fuel.

**Production Period vs Reporting Period:** "A Production Period designates all of the CO2e emitted and pyrolysis products produced during a particular period at Charm's pyrolysis facility produced between a start date and end date / All emissions produced during a given Production Period are allocated to the injectable pyrolysis products produced during that period / As injectable pyrolysis products are sequestered, the allocated emissions are deducted from the Net CDR associated with the removal. This calculation is made during the Reporting Period during which the injection occurs". From Section F: "starting with Production Period 7, which covers June production, we began to allocate emissions to all 3 products" (biochar, oily, aqueous).

**Documents produced per injection batch (drawn from Sections B and Appendix 6):** Bill of Lading / scale ticket / invoice at origin; rail or truck routing record; Vaulted "inspection report/weight scale ticket form" (mass, pH, temperature); LCS flow-meter and salt scale records; lab reports for C content (CHN), TAN, density; ledger entry for each. Per month from Vaulted: "a monthly report including / Weight of product delivered by Charm as documented by weight scale tickets / Energy consumed on site associated with the processing and injection of product delivered by Charm". Per Production Period (Charm oil): biomass throughput log, up-time telemetry, fuel invoices, utility usage, water meter, embodied-emissions inventory updates, and (biochar) 3 lab replicates.

**Data transfer to registry (Appendix 6 > General Information):** "All data related to the calculation of removals will be transmitted from Charm's Ledger software to Isometric directly via API."

**Storage (Section B):** "Ledger data is stored in an AWS relational database. It is backed up in S3 … Most data is stored indefinitely … Charm maintains daily snapshots of the relational database for the past 30 days."

**Data QA (Section B):** "Datapoints are double-checked by Charm's MRV team prior to Ledger entry to catch and investigate potential indicators of errors and nonconformities"; "When data from such documents is entered manually, the document must be provided as a check against entry errors".

---

## 7. Leakage, buffer pool, durability / reversal, conservativeness

**Leakage (Section B > Leakage Assessment):** "Charm accounts for all potential leakage across all stages of the project. Based on these assessments we have concluded that there is no identifiable leakage related to this project." Grounds: Charm feedstock "offtake of these products does not present a leakage risk as defined by the Isometric Biomass Feedstock Accounting module"; AECN "all wood processed by the mill is harvested from Provincially-owned lands under the Provincial Management Plan for Quebec forests."

**Buffer pool:** The phrase "buffer pool" does not appear in the document (text search, 0 hits). The PDD does not describe a buffer-pool contribution or rate.

**Reversal risk (Section B > Reversals):** Questionnaire: Q1 "Yes", Q2 "Yes" (closed/impermeable system), Q3–9 "N/A", Q10 "0", Q11 "0", "Total Risk Score | 0". The overall-risk pick-list cell shows the four options but no marked selection; the score of 0 corresponds to the "Very low (0)" band in the template. Supporting note: "the oil does not contain compounds that would support the microbial life required for anaerobic decay. This is confirmed by a peer-reviewed chemical characterization of pyrolysis bio-oil from multiple feedstocks (Negahdar et al., 2016) and a specific analysis of pyrolysis oil commissioned by Charm".

**Durability (Section B > Durability Assessment):** Kansas, quoting Vaulted: "sealed salt caverns 500+ feet underground for permanent (10,000+ year) geologic storage … Vaulted injects at minimal pressure (80 psig at the wellhead, which maintains total pressure – injection plus hydrostatic – below 0.75 psi / ft to the cavern top)". Louisiana: "the Lower Miocene zone penetrated by the Basco 6 EW possesses the characteristics required for bio-oil storage on a 1000+ year timeline." Biochar: "200-year durability … as per Option 1 in section 4.1.1".

**Reversal handling:** Kansas — "Any identified reversal will be promptly reported to Isometric and the VVB and investigated by Charm"; Louisiana — "Any deviations from baseline measurements attributed to Charm's operations will be reported to LDENR with plans for corrective action, with operations resuming with LDENR approval."

**Conservativeness deductions / choices stated in the text:**
- Longest Google Maps route (every transport line).
- AECN dryer stack: "Charm assumes the full quantity of estimated emissions in order to ensure a conservative estimate of removals."
- Sample shipping: "Road distances are used despite the transport assumption being air freight."
- Rail embodied: "Journey distance is doubled to account for an unloaded round-trip".
- Truck embodied: "modified to include the average 'deadhead' or unloaded journey distance".
- AECN facility cost: "The figure provided exceeds what has been described in the public record, ensuring a conservative estimate".
- Upstream loss allocation "+25%"; tote loss "+25%"; salt residue "70% (used as a conservative estimate)".
- BCU cap (Appendix 7): "We will purchase and retire a quantity of BCUs whose avoided emissions will be less than or equal to the emissions generated as a result of fossil diesel usage." and "Net CO2eFD may only be a positive value or zero. It may never be a negative value."
- REC treatment (Section F, 4/8/25): "Net CDR calculations will only include the grid emissions that are not matched by an equivalent volume of verifiable RECs"; "The volume of consumption matched by each REC is reduced by a derating factor which is equal to the grid-region T+D losses quantified by USEPA eGrid".
- All measurement uncertainties expressed as 1 standard deviation and propagated (Part 3).
- Biochar: "Charm will voluntarily take the additional precaution of constraining the rate of biochar application to agricultural soils to no more than 4 tonnes/acre."

---

## 8. Where the PDD goes beyond, or departs from, protocol requirements

The document explicitly labels the following as additions, alternatives, or deviations:

**Additions beyond the protocol (text says so):**
- Monitoring Plan Option B chosen (Part 5), i.e. a bespoke plan rather than the default.
- BCU method (Appendix 7): "Charm is using a calculation method that is different from the equations in 4.2.1 of the Transportation Emissions Accounting Module." and Section F: "Per Section 4.2.2, Charm has elected to use a bespoke calculation approach which has been reviewed and approved by Isometric."
- Biochar application cap: "Charm will voluntarily take the additional precaution of constraining the rate of biochar application to agricultural soils to no more than 4 tonnes/acre."
- Waste-disposal emissions accounting (not a listed boundary row): "Charm is using an emissions calculation approach that accounts for both the transport of the wastes to the disposal site, and the emissions impact of the disposal itself."
- Sample-shipping emissions, embodied grid-infrastructure emissions, truck/rail embodied emissions, and equipment/facility embodied emissions are all included; the PDD does not say whether the protocol requires each, so I cannot tell from the text which of these are voluntary.

**Departures from the protocol default (text says so):**
- Gas-alarm notification routing (Section B): "Charm, Isometric, and the VVB have agreed that it is more appropriate for the well operator to notify Charm regarding a wellhead gas alarm being triggered rather than the VVB as prescribed in Salt Cavern Storage module Section 3.1.1."
- Appendix 8 opens: "The following deviations from the Protocol are required on account of the project design" — no monitoring well ("formation fluid analytes … will not be available after bio-oil injection operations commence"); no isotopes/fingerprint per batch ("unless mandated by LDENR … time and cost prohibitive"); corrosion monitoring by pressure not visual ("Pulling the equipment from the well … every 6 months unnecessarily jeopardizes the well's completion"); migration inferred not measured ("Plume development will be inferred from the Warner-Lehr model"); no continuous inline GHG/VOC detectors ("prohibitively expensive"); no groundwater or seismic program expected.
- Frequency step-downs on displaced-brine parameters ("Frequency can be reduced once consistency between samples is statistically proven") and TAN ("Frequency may decrease if data shows significant consistency across batches").

**Cannot tell from the text:** whether the per-batch TAN and density testing, the daily pH/temperature checks, the annual third-party compliance affirmation, or the tote/salt-residue standard-loss methods exceed protocol minimums. The PDD describes them without saying whether the protocol requires them.

---

## 9. Administratively heaviest parts (from the text, no editorializing)

1. **Appendix 6, "GHG Statement Methodology – Calculations" (9,287 computed words) and "– Data" (5,856 computed words).** Roughly 30 emission lines, each written out four times (Data Source; Data Quality Assessment; Calculation Methodology; Justification; Unit/Frequency; Modifications to Address Uncertainty). Most of the boilerplate on GLEC, GREET, ATRI, EPA "reputable source" status is repeated per line.

2. **Section B > Monitoring Plan (3,527 computed words), Kansas storage parameters.** Nineteen named parameters each answered in a five-question format ("Who is Testing? / How Frequently? / How is Testing Performed? / When is Testing Performed? / How are Results Recorded?"). Per-batch lab tests: C content, TAN, density. Per-day-of-injection: pH, temperature. Displaced brine on a five-stage taper from fortnightly to semi-annual.

3. **Per-injection-batch document set.** BOL + scale ticket + invoice at origin; routing record; Vaulted inspection/scale form; LCS and salt records; three lab reports (CHN, TAN, density); ledger entries for each; plus a standardized sample-shipping emissions entry. All entered into the Ledger with source documents attached ("the document must be provided as a check against entry errors").

4. **Charm bio-oil Production Period data set (Section B > Data collection and storage).** "collecting data for biomass handling and delivery emissions, biomass throughput, pyrolysis machine up-time, energy usage, usage of non-energy consumables and pyrolysis outputs" plus log linear-feet measurements, water flow meter, embodied-emissions inventory updates with LCA per new item, hotflow-hour telemetry, and allocation across three products.

5. **Section B > Uncertainty assessment (2,067 computed words).** Fourteen separately justified measurement half-widths, each propagated.

6. **Appendix 8 (3,847 computed words).** Reproduces each protocol requirement block (2.1, 2.2, 2.3, 3.1.1, 3.1.2 ×2, 3.2) in full and answers under it; six-monthly corrosion and wellhead gas, annual MIT, falloff test, and tracer survey; continuous recording of six wellhead parameters.

7. **Four near-identical feedstock appendices (2–5, computed at 1,450 / 1,469 / 1,480 / 1,471 words)** repeating the same eligibility tables and EC14 justification for each named forestry project.

8. **Section F change log (2,100 computed words)** — five dated entries listing every PDD section touched, plus three standard-loss / allocation rules introduced 9/9/25.

---

## Source List

- **Document:** "Charm Industrial Bio-Oil Geologic Storage + Range & Plains Biochar Design Document", version line "v1.12 – 2025/12/01". Drive filename: "Final V 1.12 Charm Industrial Bio Oil Geologic Storage PDD + Biochar.docx". File created in Drive 2026-01-31; last modified 2026-09-11 (Drive metadata). Document core properties show original creation 2024-02-26.
- **URL:** https://docs.google.com/document/d/1V0v2atno-pVZQZ983EEy9sfmlci4cm_C/edit?tab=t.0#heading=h.gjdgxs (Drive view URL: https://drive.google.com/file/d/1V0v2atno-pVZQZ983EEy9sfmlci4cm_C/view)
- **Access method:** Google Drive connector, `get_file_metadata` and `download_file_content` (file ID 1V0v2atno-pVZQZ983EEy9sfmlci4cm_C). Returned base64 .docx (1,991,632 bytes). Decoded and text-extracted locally in document order including all table cells; two independent extraction passes reconciled to 58,881 words. No browser used.
- **Not read (not in this file):** "Supplemental Doc 3" / Basco 6 Combined Emissions Monitoring and Accounting Plan; "GHG Statement Supplemental Doc" calculation sheets; the separate PDD change log; the 22 Word comments in the file's comments part; the 2 embedded images.
