# Peer Profile — Vaulted Deep, TIRE Project (Biomass Geological Storage)

Prepared 2026-09-14. Every quote is verbatim from a document read this session, with the page number of the PDF as downloaded (raw/tire/). Charm quotes are from `02_charm_pdd_baseline.md` (read in full this session), which itself quotes the Charm PDD v1.12. Where a figure is computed rather than quoted, it says "computed" and shows the arithmetic. Where the documents do not say something, this profile says "not stated".

How the files were read: the six TIRE PDFs were already in `raw/tire/` from an interrupted earlier attempt (`tire_pdd.pdf`, `tire_ghg1.pdf`, `tire_ghg2.pdf`, `tire_vvr1.pdf`, `tire_ver2.pdf`, `tire_pcs.pdf`); every page of the first five was read with the Read tool. `tire_pcs.pdf` (Public Comment Summary, 1 page, PDF title "[No Comments Received] [Vaulted TIRE]- Project Public Comment Summary") was not opened beyond its metadata. The workspace's `doc_extraction_guard.sh` blocks `pdftotext`, `grep/sed/awk/cat` on PDFs and python PDF-text libraries, so no extracted `.txt` copies could be saved into `raw/tire/` and no machine word count could be produced from the PDFs — see Section 1 for what was done instead.

---

## 1. Document size

### 1a. PDD (`tire_pdd.pdf`)

- **Page count:** 65 pages in the file (`pdfinfo`: "Pages: 65"). The file is two Isometric-rendered documents joined: a "Project design document" whose own footer runs "1 / 60" to "60 / 60" (footer label "PROJECT DESIGN"), followed by a 5-page "Feedstock: LACity_Biosolids" document whose footer runs "1 / 5" to "5 / 5" (footer label "FEEDSTOCK"). The file was rendered by "Chromium" on "Tue Jun 16 14:03:42 2026 PDT" (pdfinfo).
- **Word count:** not computed (extraction blocked). The guard blocks every text-extraction route available in Bash, the Read tool returned this PDF as page images (not text), and the coordinator instructed that the block not be worked around. As a size proxy, page counts per section are given below.
- **Section list** (headings as printed, with the file pages they occupy):

| Section (as printed) | Sub-items | File pages | Pages |
|---|---|---|---|
| Title page ("Vaulted Deep / Project design document / TIRE Project") | — | 1 | 1 |
| "Section A: Project setup" | A.1 Protocol requirements; A.2 Ownership; A.3 Technical description; A.4 Project participants; A.5 Project locations; A.6 Removal capacity | 2–7 | 6 |
| "Section B: Protocol & monitoring data" | B.1 Boundaries; B.2 (system boundary table); B.3 (GHG statement approach); B.4 Baseline; B.5 Leakage; B.6 Financial additionality; B.7 Common practice additionality; B.8 Environmental additionality; B.9 Regulatory additionality; B.10 Regulatory compliance; B.11–B.12 Durability; B.13 Reversals; B.14–B.15 Uncertainty; B.16 Proxies & models; B.17 Data collection and storage | 8–33 | 26 |
| "Section C: Environmental & social impacts" | C.1–C.4 Environmental & social impact; C.5 Sustainable development; C.6 Project closure | 34–40 | 7 |
| "Section D: Stakeholder input process" | D.1 Stakeholder consultation; D.2 (grievance mechanism) | 41–52 | 12 |
| "Section E: Pathway-specific" | E.1 Monitoring requirements; E.2–E.4 Applicability; E.5–E.6 Environmental and social safeguarding; E.7 Biomass spills | 53–60 | 8 |
| "Feedstock: LACity_Biosolids" | A.1–A.7 Feedstock requirements (EC1, EC13, EC15, counterfactual, replacement emissions) | 61–65 | 5 |

Largest single blocks by page: Section D stakeholder text (12 pages, of which D.2 largely repeats D.1 — the same "Within 14 days of grievance received…" bullet list appears on p.45 and again on p.51), the B.14 sensitivity table (pp.23–29, 7 pages), the E.1 monitoring table (pp.53–57, 5 pages), and the B.16 fracture-modelling narrative (pp.30–32, 3 pages).

Several passages are redacted with black bars (e.g. p.4 land-application site name, p.7 capacity note, p.15 whole paragraphs of B.6 Financial additionality, p.30 modelling-software name, p.36 PFAS paragraph, p.58 site address).

### 1b. GHG Statement Reports

- **RP1 report (`tire_ghg1.pdf`)** — 5 pages (pdfinfo "Pages: 5"; Creator "Microsoft Word"). Sections: "General Information" (p.1–2); "GHG Statement Methodology - Data" (p.2–3); "GHG Statement Methodology - Calculations" (p.3–4); "GHG Statement Results" (p.4–5). Word count not computed (same block); the whole substantive answer text fits on roughly three pages, and the Results answer is one paragraph plus nine bullet lines (p.5).
- **RP2 report (`tire_ghg2.pdf`)** — 4 pages (pdfinfo "Pages: 4"), page 4 blank. The Data section answer is one sentence: "No changes have been made since the last submission period" (p.2). The Calculations section answer is a two-paragraph "Baseline Calculations" note (p.3). Results is one paragraph plus nine bullets (p.3).

### 1c. Verification reports (read for context)

- `tire_vvr1.pdf` "Validation and Verification Report" v1.3, June 17 2026, 44 pages; pages 31–37 are a file list ("Appendix 3: Files Reviewed"), pages 38–44 verifier CVs.
- `tire_ver2.pdf` "Vaulted Deep Isometric Standard Project Verification Report" V1.1, August 28 2026, 22 pages.

---

## 2. Project design

**Protocol / modules.** Registry project page: "Current protocol version / Biomass Geological Storage v1.1" (`raw/prj_1K7HK8Q4S1S0D4W4.json`, read this session). PDD A.1 (p.2): "This Project meets the eligibility criteria for the Biomass Storage in Permeable Reservoirs protocol." and "All feedstocks used in this project accord with the framework set out in the Biomass Feedstock Accounting module v.1.2." PDD B.2 (p.9): "Vaulted does not credit avoided emissions in alignment with the Isometric Protocol v1.7 Section 2.5.2." E.1 rows cite "§4.1.1 Permeable Reservoirs Module v1.0" and "Protocol §7.3.3 Biomass Geological Storage v1.1" (p.54). The validation report lists the full set (vvr1 p.6): "Isometric Standard v1.1 / Biomass Geological Storage Protocol v1.1 / Embodied Emissions Accounting v1.0 / Energy Use Accounting v1.2 / Transportation Emissions Accounting v1.1 / Biomass Feedstock Accounting v1.2 / Biomass Storage in Permeable Reservoirs v1.0".

**Feedstock.** Registry Feedstocks table: "LACity_Biosolids | Biomass | 17 Jun 2026". PDD B.1 (p.8): "1. Digested sludge from digestors at the Terminal Island Water Reclamation Plant through pipeline directly to the mixing pit. 2. Class A biosolids delivered by truck from the Hyperion Water Reclamation Plant located 26.3 miles away at El Segundo, CA." and "CRUs will only be generated from additional volumes sourced from the Hyperion facility and other facilities in the future." Feedstock doc A.1 (p.62): "The feedstock is a biosolid derived from the City of Los Angeles' waste water treatment process."

**Processing.** PDD A.3 (p.4): "The wetcake is mixed with digested sludge, HPE and brine (depending on availability), slurrified and injected into deep underground formation around 4,900 ft." Validation report (vvr1 p.7): "Biosolids received at the TIRE facility undergo minimal pre-treatment prior to injection." and "No thermal, chemical, or biological transformation of the biomass is performed as part of Project operations."

**Transport.** PDD B.3 (p.11): "Biosolids Transportation involved CNG consumption, where the quantity was estimated based on distance from the supplier site to TIRE, accounting for inbound and outbound journeys, and the mpg of the delivery truck used for that specific delivery."

**Storage type and site.** PDD A.3 (p.4): "The facility has 4 wells, (2-injection wells and 2-monitoring wells), 2 injection pumps (~600HP), pre-injection tank and screener." and "The permitted injection interval is from 3,800 ft – 7,500 ft, which is a sequence of sand and shale layers." Permit (p.18): "Class V UIC | R9UIC-CA5-FY11-3R CA". A.5 (p.6): "TIRE facility is in the NW corner of the Terminal Island Water Reclamation Plant, San Pedro, CA with a total acreage of 0.38 acres (1,524.46 sq-meters)".

**Crediting period.** Registry: "CREDITING PERIOD / 03 Jan 2026 to 03 Jan 2031". PDD B.1 (p.8): "This project will generate CRUs over a period of 5 years and is expected to provide durability of 1,000+ years." A.6 (p.7): estimated capacity "30607" metric tonnes for each of 2026–2030.

**Reporting cadence.** PDD B.17 (p.33): Data Vault "after batched internal approval, automatically shares this data with Isometric for each monthly verification period." Actual periods so far: RP1 "1/3/2026 – 2/20/2026" (ghg1 p.1); RP2 "2/21/2026 – 7/10/2026" (ghg2 p.1). Baseline is also re-evaluated periodically (B.4 p.14): "the ultimate baseline (historical volumes + cushion) will be evaluated monthly or quarterly for the first year".

**Batch definition.** Not defined as a term in the PDD. The operative unit is the truck load: B.17 (p.32) "TOC sampling from trucks follows Method B … with three samples taken at different locations within the truck" and (p.33) "Data Vault enables load by load tracking of all relevant data inputs". The registry's public calculation view is for one removal of "2.07 tCO₂e removed from TIRE Project on 09 Jul 2026" (project page). Crediting is applied at weekly resolution: ghg1 (p.5) "The baseline of 916.5 tons of waste per week was subtracted from the total amount sequestered during the audit period".

**Ownership structure** (relevant to who collects data). A.2 (p.2–3): "GeoEnvironment currently owns the TIRE injection facility. Advantek Waste Management Services (AWMS) owns the company GeoEnvironment" and "Vaulted Deep currently owns all rights to carbon credits from TIRE via an offtake agreement with AWMS and GeoEnvironment". B.17 (p.33): "ASWM and GeoEnvironment will have no involvement in data collection and storage."

---

## 3. System boundary table

PDD B.2 (pp.9–10) lists 13 rows (4 baseline, 9 project). Quantification detail is not in the B.2 table itself; it comes from B.3 (p.11–12) and the B.14 sensitivity table (pp.23–29), whose "Data used" and "Initial assumption" columns are the only place the PDD says how each input is obtained.

| # | B.2 row (verbatim) | Incl. | Gases | How quantified (verbatim source) | Sampling / frequency | Uncertainty treatment (B.14) |
|---|---|---|---|---|---|---|
| 1 | Baseline — "Counterfactual Emissions: Fuel Use from Feedstock Sourcing" | Included | CO2, CH4, N2O | "No additional fuel usage on part of waste supplier due to Vaulted activities. No incremental emissions relative to baseline." (p.9) → zero | — | not in table |
| 2 | Baseline — "Counterfactual Emissions: Electricity Use from Feedstock Sourcing" | Included | CO2, CH4, N2O | "No additional electricity usage … No incremental emissions relative to baseline." (p.9) → zero | — | not in table |
| 3 | Baseline — "Counterfactual Emissions: Replacement of Feedstock Function" | Included | CO2, CH4, N2O | "This project meets sustainable feedstock sourcing eligibility criteria and assesses replacement emissions where necessary." (p.10); Feedstock A.6 (p.65): "Accordingly, Vaulted does not account for replacement emissions." → zero | — | not in table |
| 4 | Baseline — "Counterfactual Emissions: Temporary Carbon Storage from Feedstock" | Included | CO2, CH4 | Model: "Using a two-pool biosolids decay model, which assigns a literature-backed k (decay) rate to a fast (labile) carbon pool and a slow (recalcitrant) carbon pool, Vaulted calculates counterfactual remaining mass of C and CO2e at 15 and 50 years" (B.3 p.12). Feedstock A.4 (p.63) describes it as "a three-pool biosolids decay model … and a mineral-associated organic carbon pool" and (p.64) "Vaulted discounts 1% of embodied feedstock carbon before crediting." The GHG reports apply "Counterfactual (2.92%)" (ghg1 p.5; ghg2 p.3). | Once (model), applied per RP | not in table |
| 5 | Project — "Fuel Use from Feedstock Transport" | Included | CO2, CH4, N2O | "Measured - Fuel use mpg provided by transport company" — "0.37 gallon/ton waste" (p.23); distance "Google maps: road miles between supplier and well site" — "26.3 miles" (p.24); EF "GHG emissions of 1 MJ of CNG, WTW" "GREET 2023" "0.00007 37 t CO2/MJ" (p.27–28) | Per delivery (distance fixed) | "20% increase in fuel use" → "-0.32%"; "original value has been used" |
| 6 | Project — "Embodied Emissions from Feedstock Transport" | Included | CO2, CH4, N2O | EF "GHG emissions of transporting 1 mt over 1 km, vehicle and road infrastructure embodied only" — "customized from ecoinvent 3.10" — "0.00003807 t CO2e/t*km" (p.28) | Default factor | "-0.18%" |
| 7 | Project — "Electricity Use from Biomass Pre-processing" | Included | CO2, CH4, N2O | "Measured with the electricity reader" "As measured per delivery" (p.24–25); B.17 (p.32–33): "Meter readouts of the facility's power consumption can be taken from the power room, and the facility manager reports this data daily." EF "From eGRID data" "0.000268 t CO2e/kWh" (p.27) | Daily reading | "±-2.5% … If electricity use was increased by 2.5%, total net CO2e removals would decrease by 0.14%. Because the uncertainty is well-below the 1% significance threshold, it has not been accounted for." |
| 8 | Project — "Embodied Emissions from Equipment and Consumables for Biomass Pre-processing" | Included | CO2, CH4, N2O | "Site material: steel" — "Estimated by the LCA expert based on information presented in the site summary document" — "7.3E-05 t/t waste" (p.25); "GHG emissions of using the screener during 1 day" "customized from ecoinvent 3.10" "0.01448558 t CO2e/day" (p.28); lubricant "0.9 gallon of lubricant per day" and "30 gallon of waste per week" "calculated from purchase records" (p.26); B.3 (p.11): "Given the age of the TIRE facility and its associated equipment, EoL emissions will be the only thing accounted for. Materials were allocated to each metric ton of waste based on a conservative estimate of lifetime processing waste capacity of 1,600,000 metric tons of waste." | Estimate / purchase records | steel "High uncertainty, based on expert judgment … up to the fifth significant figure (<1%)" |
| 9 | Project — "Electricity Use from Biomass Injection" | Included | CO2, CH4, N2O | Same meter as row 7; plus "HPE electricity consumption" — "Estimated, using sludge pump power consumption as a proxy" — "101 kWh/day" (p.25); B.17 (p.33): "Power consumption from the pumps used to displace HPE and digested sludge to the site is not quantified in our meter; however, pump specifications are available." | Daily / proxy | "High uncertainty, based on proxies … (<1%)" |
| 10 | Project — "Embodied Emissions from Equipment and Consumables for Biomass Injection" | Included | CO2, CH4, N2O | As row 8 (EoL only, amortised over 1,600,000 t) | — | as row 8 |
| 11 | Project — "Carbon Content of Injected Biomass" | Included | CO2e | Mass: "Measured at the scale of the biosolids provider" "As measured per supplier" (p.24). Carbon: "TOC % from loads determined through laboratory analysis" (p.26); B.17 (p.32): "Incoming biomass carbon content is measured at a laboratory, a third-party based in Kansas, following the required standards." | Mass every load; carbon "Method B … first 10 trucks … every 10th truck" (p.11) | Scale: "Scales tend to be calibrated annually, with measurements within 100 lb (not confirmed in this case …). The uncertainty of the measurement would be 0.23% (considering a 20 ton load). Because the uncertainty is well-below the 1% significance threshold, it has not been accounted for." Carbon: "Using Method B to incorporate the average, mean standard error to establish baseline with first 10 trucks and every 10th truck after." |
| 12 | Project — "Site Decommissioning and Well Plugging" | Included | CO2e, CH4, N2O | "CO2 included as the primary emission from decommissioning equipment, well plugging and consumables due to electricity consumption." (p.10). No quantity or method given elsewhere in the PDD; the verification report treats end-of-life as "Included as embodied emissions and allocated over the project lifetime" (ver2 p.9) and RP2 reports "CO2eEnd-of-Life, RP | 0.00" (ver2 p.11). | not stated | not in table |
| — | Not in B.2 but quantified: foreign-material handling, pump maintenance, lab-sample transport | — | — | "Foreign material production" "Measured at the site" "6000 lbs/week" (p.26) with diesel; "Pump maintenance emissions" "Waste water measured and lubricant calculated from purchase records" (p.26); B.3 (p.11): "Lab sampling emissions were calculated based on the weight of the samples and distance to lab." | weekly / per purchase | each "<1%" |

**Uncertainty approach (B.15, p.29):** "No | Conservative estimate of input parameters / Yes | Variance propagation / No | Monte Carlo Simulations". Method statement (p.29): "The change in net CO2e removal induced by each parameter was calculated by varying each parameter independently and observing the impact on net CO2e removals. All the parameters are included in the calculation of the net CO2e removals even if they contribute less than 1% change in the removal. The 1% threshold was applied consistently across all parameters." The only parameter breaching 1% is the grid factor: "GHG emissions of electricity in LADWP … 27.79 … -1.24%" (p.27). The RP2 verifier line: "Uncertainty Discount | 0.00 | Project sensitivity analysis determined that uncertainty in the assessed input parameters did not result in a material change to net removals; therefore no separate uncertainty deduction was applied." (ver2 p.11).

**Boundary statement (B.2 p.9):** "All activities undertaken to permanently sequester carbon, at the point of taking ownership of the organic waste are included in the project boundary." and "Emissions associated with activities occurring at the TIRE facility that are below the Project crediting baseline are not included in the Project LCA."

---

## 4. Gross removal calculation

**Formula.** The PDD does not write out an equation. The validation report does (vvr1 p.11): "Net CO₂e Removal = CO₂e Stored – Baseline and Counterfactual Adjustments – Project Emissions – Leakage Deductions" with "CO₂e Stored represents the quantity of biogenic carbon injected and stored within the geologic formation". Its Table 3 (vvr1 p.14): "CO₂ stored is quantified based on the mass of injected biosolids and measured carbon content, converted to CO₂e."

**Worked RP1 figures (ghg1 p.5):** "Vaulted geologically sequestered 6,242.77 US tons of waste during this audit period. The baseline of 916.5 tons of waste per week was subtracted … The baseline for this audit period is 3,666 US tons of waste across 4 weeks, leading to creditable waste volumes sequestered to 2,576.77 US tons of waste, equivalent to 517.59 metric tons of gross CO2." Then nine emission lines totalling "97.73 tons of CO2e" and "427.52 net tons of CO2e removed".
Computed check (mine, not in the document): 2,576.77 US tons × 0.907185 t/US ton = 2,337.6 t; 517.59 t CO2 × 12/44 = 141.16 t C; 141.16 ÷ 2,337.6 = 6.04 % carbon by wet mass. That implied fraction sits inside the PDD's assumed range "TOC % for biosolids data outside of TIRE range from 5-7%. TOC for TIRE is assumed the average of this range and used for this process until real data is obtained" (p.26).
Internal inconsistency in the same paragraph: "across 4 weeks" (ghg1 p.5) versus 3,666 ÷ 916.5 = 4.0 weeks, while the RP2 report says "The first verification contained seven weeks" (ghg2 p.3) and the RP1 dates 1/3–2/20/2026 span 7 weeks. The document does not reconcile this.

**Carbon-content method and frequency.** B.3 (p.11): "Isometric's Sampling Method A was conducted, obtaining 30 initial samples. Calculations have since shifted based off Isometric's Method B, where the first 10 trucks of the feedstock will be tested to establish a baseline of carbon content, and every 10th truck is tested to represent the untested trucks." B.17 (p.32): "three samples taken at different locations within the truck. After an initial period of conducting triplicate measurements for the first 10 batches Vaulted will then proceeded to conduct a triplicate measurement on every 10th batch." E.1 (p.54): "Total Carbon Content of Injectate | … | TOC analyser; GC; or equivalent | … | Per batch | Lab Evidence (TOC); Loads (Integrated Evidence)". The validator's file list shows the pattern: many "not_integrated_feed_organic" PDFs and a smaller number of "carbon_content" PDFs, e.g. "src_1KKH8ZPXX1S0GAEB_V3-vaulted-2-2026-01-03-1530-carbon_content-95275.pdf" (vvr1 p.31).

**Mass measurement.** B.17 (p.32): "Biosolids truck loads are weighed at an external facility using calibrated equipment, and the recorded weights are provided to us regularly along with supporting documentation. No scale is available on site to perform truck weighing." E.7 (p.60): "the protocol's mass measurement methodology, which uses the difference between truck arrival and departure weights on a calibrated scale to determine delivered mass (Section 7.3.3.1)".

**Adjustments.**
- Baseline subtraction: B.4 (p.13) "The historical baseline will be a simple average of volumes of biosolids injected over the last five years, excluding emergency or Class B volumes." plus cushion (p.13–14): "To ensure that there is less than a 10% probability of crediting volumes that are non-additional, Vaulted calculates a 'cushion' volume that is added to the baseline." RP2 (ghg2 p.3): "The new baseline volume will now be 933.79 US tons/week. Because the previous audit period had a falsely low cushion, an additional 15 US tons/week will be added for the number of weeks equivalent to the length of the previous audit period."
- Counterfactual storage deduction: "Counterfactual (2.92%)" (ghg1 p.5, ghg2 p.3).
- Spills: E.7 (p.60) "the lost quantity will be deducted from the delivered biomass quantity for the relevant batch in the GHG Statement, as required by Section 7.3.3.3."
- Rounding: B.3 (p.12) "Net removals in t CO₂e for each removal activity was rounded to the nearest 0.01t CO₂e in line with Isometric requirements."
- No moisture, consumable-mass, filtration or tote-loss adjustment is described anywhere in the PDD or GHG reports (the words "moisture" and "filtration" do not appear in any page read).

---

## 5. Monitoring plan

Source: E.1 "Monitoring requirements" (pp.53–57), introduced as "The following table summarizes monitoring requirements for the facility as stated in the Class V UIC Permit for the TIRE facility." Attached file: "Monitoring Requirements.xlsx". Columns: Parameter / Parameter Description / Measurement Method / Monitoring Phase / Monitoring Frequency / Required Evidence / Isometric Module Reference.

| Parameter (verbatim) | Method (verbatim) | Frequency | Evidence |
|---|---|---|---|
| Injection Wellhead Pressure / MASIP | "Continuous pressure sensor / DAS with automatic shut-off alarm" | Continuous | "EPA Quarterly Reports; DAS Output" |
| Injection Rate & Injected Volume | "Continuous flow meter / mass meter; DAS" | Continuous | same |
| Injectate Temperature | "Temperature probe/sensor (calibrated)" | Continuous | same |
| Injectate Density | "ASTM D 4052-22 or ASTM D7042-21a (surface density); density at reservoir conditions calculated from T, P, salinity" | Daily | "EPA Quarterly Reports; Lab Evidence" |
| Injectate Viscosity | "Industry standard viscosity measurement" | Daily | EPA Quarterly Reports |
| Average Solids Concentration | "Industry standard gravimetric or optical solids analysis" | Daily | EPA Quarterly Reports |
| Total Carbon Content of Injectate | "TOC analyser; GC; or equivalent" | "Per batch" | "Lab Evidence (TOC); Loads (Integrated Evidence)" |
| Gas Detection — Wellhead / Facility | "Gas monitors (≥0.01 vol% resolution); automatic shut-off system" | Continuous | "DAS Output; Alarm Logs" |
| Internal Mechanical Integrity Test | "Standard annular pressure test; corrosion inspection per API / ASTM" | "Upon completion; when construction modified; then per UIC permit cadence performed annually" | "MIT Report; UIC Permit; Testing Data" |
| Annulus Pressure Monitoring | "Continuous pressure sensor / DAS" | Continuous | "Continuous Monitoring Data; EPA Quarterly Reports" |
| Pressure Fall-Off Test / External MIT | "Downhole pressure gauge; step-rate test (SRT) and pressure fall-off analysis" | Quarterly | "EPA Quarterly Reports; SRT/PFO Data" |
| Reservoir Pressure — Continuous | "Downhole pressure sensor; DAS; or fibre-optic system" | Continuous | "DAS Output; EPA Quarterly Reports" |
| Reservoir Temperature — Continuous | "Fibre-optic DTS; downhole temperature sensor/logger" | Continuous | same |
| Injectate Plume Confinement Monitoring | "Pressure fall-off test (indirect); advanced pressure transient analysis; reservoir simulation comparison" | "Monthly (indirect); Quarterly (pressure transient analysis)" | "EPA Quarterly Reports; Modelling Reports" |
| Pre-existing Fracture & Fracture Development Monitoring | "Step-rate test (SRT); pressure fall-off (PFO); microseismic monitoring; well logs" | "Pre-injection (SRT); Regularly during operation (PFO)" | "SRT Data; PFO Reports; Monitoring Logs" |
| Microseismic Monitoring | "Seismic network; microseismic sensors; or national USGS programme" | Quarterly | "Microseismic Reports; EPA Quarterly Reports" |
| Surface Displacement / Subsidence | "InSAR / SAR (satellite interferometry); tiltmeters; GPS instruments" | "Baseline (pre-injection); periodic during operation; per permit post-injection" | "Survey Reports; GPS / InSAR Data" |
| Reservoir / Fracture Simulation Model | "Industry-accepted reservoir simulation software; fracture simulation; comparison to field data" | Quarterly | "Modelling Reports submitted to Isometric and VVB" |
| Zone of Endangering Influence Evaluation | "Updated reservoir model; site characterisation review" | Quarterly | "AOR Re-evaluation Report" |
| Biodegradation Process Evaluation — Gas & Formation Fluids | "Wellhead/brine gas sampling; GC-MS; geochemical lab analysis" | Quarterly | "Lab Reports; Monitoring Logs" |

Other monitoring statements: B.12 (p.20) "Access to sensor calibration certificates can be found here" with files "Certificate of Calibration for Unit RM-0013.pdf, … RM-0012.pdf, … RM-0011.pdf" (p.21); B.13 (p.23) "A copy of the Gas Monitoring Data for the verification period can be found here / A copy of the Gas Monitoring SOP can be found here"; C.6 (p.40) "The simulation model is updated and run every quarter"; B.10 (p.18) "Vaulted submits quarterly monitoring reports to the EPA in line with Class V UIC permit requirements." Twenty of the table's rows carry a module reference; none of the emissions-side inputs (electricity, fuel, propane, lubricant) appear in E.1 — those are described only in B.14 and B.17.

Verifier's file list for RP2 shows the evidence actually reviewed (ver2 p.19): calibration certificates RM-0010 to RM-0013, seven "TIRE_Project_Summary" PDFs dated 20260227 to 20260724, "Continuous Monitoring Data - Q2 2026.xlsx", the UIC permit, and "Q2_2026_TIRE_EPA_Quarterly_Report_April_to_June.pdf".

---

## 6. Calculation view (registry)

Read 2026-09-14 with the plain `playwright` server (the assigned `mrv-3` profile was held by another session; the coordinator redirected me). Raw captures: `raw/tire/ghg_entry_calc_view.json`, `ghg_entry_calc_view_snapshot.md`, `ghg_entry_tree_expanded.md`, `ghg_entry_carbon_3_measurements.json`, `ghg_entry_carbon_318_measurements_p1.json`, `ghg_entry_removal_method.json`, `ghg_entry_datapoints.json`.

**Entry header:** "2.07 tCO₂e removed by Vaulted Deep / rmv_1KYD9KRCD1S02J7Q"; "Sequestration date 09 Jul 2026"; "Reporting period 21 Feb 2026 to 10 Jul 2026"; "Verification protocol version Biomass Geological Storage v1.1"; "Verifier 350Solutions". One removal = one day's delivery: "Mass of waste biomass 7.242 t".

**Tree (each node expanded by clicking it; labels and values verbatim):**

```
Net CO₂e Removed 2.070 tCO₂e
 = Sequestrations 2.217 tCO₂e
     = Sample With History Biomass Sequestration 2.217 t
         = Mass of waste biomass 7.242 t × Mean carbon content 0.083500 × CO2e eq mass of C 3.666667
 − Activities 148 kgCO₂e
     = Collection and Transport 38 kgCO₂e
         = Biomass Transport Fuel Usage Full Emissions 19 kgCO₂e
         + Biomass Transport Fuel Usage Empty Emissions 17 kgCO₂e
         + Foreign Material Transportation Emission 2 kgCO₂e
     + Processing and Injection 110 kgCO₂e
         = Pump Maintenance Emission 3 kgCO₂e
         + Energy Emissions From Receiving HPE 1 kgCO₂e
         + Counterfactual C Storaget 22 kgCO₂e        (label as shown on the page)
         + Propane Emissions 1 kgCO₂e
         + Process Energy Usage Emissions 82 kgCO₂e
         + Biomass Carbon Content Lab Testing 1 kgCO₂e
```
Computed checks: 7.242 × 0.0835 × 3.666667 = 2.2172 t (page shows 2.217); 19 + 17 + 2 = 38; 3 + 1 + 22 + 1 + 82 + 1 = 110; 38 + 110 = 148; 2.217 − 0.148 = 2.069 (page shows 2.070, rounding). "Mean carbon content 0.083500" is the mean of the three per-load measurements (0.0829 + 0.0835 + 0.0841) ÷ 3 = 0.0835. There is no Adjustments branch and no Uncertainty Discount branch; the counterfactual deduction (22 kg = 0.99 % of 2.217 t, computed) sits inside Activities. Note the 22 kg ÷ 2,217 kg = 0.99 % here versus "Counterfactual (2.92%)" in both GHG reports — the two figures are not reconciled in any document read.

**Datapoints table ("Datapoints (12)"), verbatim rows `Name | Value | Collection method | Sources`:**

| # | Name | Value | Collection method | Sources |
|---|---|---|---|---|
| 1 | Mass of waste biomass | 7.242 t | REPORTED | "Not Integrated Feed Organic" |
| 2 | CO2e eq mass of C | 3.666667 | CONSTANT | — |
| 3 | Biomass transport distance | 17.24 km | REPORTED | "Hyperion- City of LA Directions to TIRE" |
| 4 | CNG Carbon Intensity | 2,338.21 kg/m³ | REPORTED | — |
| 5 | Fully loaded truck MPG | 5.00 mi/gal | STANDARD PUBLISHED VALUE | — |
| 6 | Empty truck MPG | 5.50 mi/gal | STANDARD PUBLISHED VALUE | — |
| 7 | Propane Emission | 1 kgCO₂e | DERIVED | — |
| 8 | Processing & Injection energy use | 305.04 kWh | REPORTED | "initial process energy use at the start of the audit period" + "final process energy use at the end of the audit period" |
| 9 | Grid emissions factor | 0.27 kgCO₂e/kWh | STANDARD PUBLISHED VALUE | — |
| 10 | Lab Sampling Emission | 1 kgCO₂e | REPORTED | "SDK Laboratories Distance To Tire" |
| 11 | Carbon content measurements of injectant | Multiple values | — | link "3 measurements": 0.082900, 0.083500, 0.084100, each sourced "Carbon Content" |
| 12 | Historical carbon content measurements of injectant | Multiple values | — | link "318 measurements" ("Showing 10 of 318"; first ten 0.0805–0.0848, each sourced "Carbon Content") |

**Counts:** 12 datapoints. Collection method: REPORTED 6 (rows 1, 3, 4, 8, 10, and the two measurement sets are each labelled "REPORTED" on their own pages — counting the table column only: 5 REPORTED, 3 STANDARD PUBLISHED VALUE, 1 CONSTANT, 1 DERIVED, 2 with "—" whose detail pages say "REPORTED"). Sources column: 4 rows name a source document (rows 1, 3, 8, 10), 6 rows show "—", 2 rows link to measurement lists.

**Observations from the tree:** the transport distance in the registry is "17.24 km" while the PDD says "26.3 miles" (p.8, p.24) — 26.3 miles × 1.609 = 42.3 km, so the registry value is not the PDD's round-trip or one-way road distance; not reconciled in the documents. The per-load "Mean carbon content 0.083500" (8.35 %) is above the PDD's assumed "6%" placeholder (p.26). The "Removal method" tab and the `?tab=datapoints` URL both rendered only the generic BiCRS paragraph ("Biomass Carbon Removal and Storage (BiCRS) involves storing the carbon contained in waste biomass…"); the datapoint table lives inside the Calculation view tab.

**Compared with Charm's entry (census record):** Charm's tree has four branches — "Net CO₂e Removed 159.491 t = Sequestrations 193.725 t + Adjustments 20.929 tCO₂e − Activities 54.091 tCO₂e − Uncertainty Discount 1.072 t" — and "Datapoints (46)" with per-source file names such as "2396-R.pdf + 19 more" and "GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf". TIRE's has two branches, 12 datapoints, and four named source documents.

---

## 7. Side-by-side with Charm

| Item | Charm (baseline quote) | TIRE (peer quote) | Resembles / differs |
|---|---|---|---|
| 1 Size | "58,881 words … at least 155 pages long by its own table of contents" | 65-page file ("1 / 60" + "1 / 5"); word count not computable here | Differs — TIRE is much shorter by page count (65 vs ≥155). See length note below. |
| 2 Protocol | "Protocol Name: Bio Oil Geological Storage / Protocol Version Number: v1.0" + Biochar protocols; storage in salt caverns (Vaulted GP) and permeable reservoir (Basco 6) | "Biomass Geological Storage v1.1"; "Biomass Storage in Permeable Reservoirs protocol" | Differs in protocol; resembles in storage class (permeable reservoir, like Charm's Basco 6) |
| 2 Feedstock / processing | "non-merchantable woody biomass … pyrolysis" and purchased AECN bio-oil; pre-processing at El Dorado with salt and LCS | "biosolid derived from the City of Los Angeles' waste water treatment process"; "minimal pre-treatment" | Differs — TIRE has no conversion step and no consumables added for spec |
| 2 Crediting period | "Start date of crediting period: 2024/03/01 … Total length of crediting period: 5 years" | "03 Jan 2026 to 03 Jan 2031" | Resembles (5 years) |
| 2 Reporting cadence | "The PDD does not state a fixed calendar cadence … roughly monthly-to-bimonthly periods in practice" | "for each monthly verification period" (stated); actual RPs of 7 and 20 weeks | Resembles in stated intent; TIRE's second RP was longer |
| 2 Batch | "Once a given Lot, or batched combination of several split Lots, is injected it is then logged as a Removal" | "load by load tracking"; one registry removal = one day's load (2.07 t) | Differs — TIRE's unit is the truck load; Charm's is a blended injection batch with lot lineage |
| 3 Boundary rows | 40 rows in the table plus two sources only in Appendix 6 | 13 rows in B.2; three further quantified items only in B.3/B.14 | Differs — roughly one-third the row count |
| 3 Quantification | mixture of measured (invoices, meters, scale tickets), vendor LCA, GREET/GLEC factors, stack testing, cost-based embodied | measured electricity meter; supplier scale; supplier-reported mpg; ecoinvent/GREET/eGRID factors; steel by "expert judgment"; HPE by "proxy" | Resembles in structure; TIRE relies more on estimates/proxies for small items |
| 3 Uncertainty | "Variance propagation" with 14 separately justified half-widths propagated to every batch | "Variance propagation" ticked, but every input judged "<1%" and "has not been accounted for"; verifier: "Uncertainty Discount | 0.00" | Differs — same box ticked, no discount applied at TIRE |
| 4 Gross formula | "multiplying the Mass of Bio Oil Injected by the average C content … multiplied by 44/12" | not written in PDD; verifier: "CO₂e Stored … mass of injected biosolids and measured carbon content, converted to CO₂e" | Resembles in arithmetic; TIRE additionally subtracts a weekly baseline volume before crediting |
| 4 Carbon sampling | "a sample is taken for each injection batch" (Method A) | "the first 10 trucks … and every 10th truck is tested" (Method B) | Differs — TIRE samples ~1 in 10 loads |
| 4 Mass | "weighing the delivery truck prior to and after injection on a certified scale" at the injection site | "weighed at an external facility … No scale is available on site" | Differs — TIRE uses the supplier's scale |
| 4 Adjustments | consumables subtraction, salt-residue credit, tote standard loss, upstream loss +25% | baseline subtraction, 2.92% counterfactual, spill deduction | Differs — TIRE's adjustments are volume/baseline-side, not mass-loss-side |
| 5 Monitoring | 19 Kansas parameters in five-question format; per-batch TAN, density, C; daily pH/temp; displaced-brine taper; Louisiana six-monthly gas/corrosion, annual MIT/falloff/tracer | 20 permit-derived parameters, most continuous or quarterly; daily density/viscosity/solids; per-batch TOC; gas detection continuous with auto shut-off | Resembles in count; TIRE's is a restatement of the UIC permit ("as stated in the Class V UIC Permit") rather than a bespoke Isometric plan |
| 6 Calculation view | "Datapoints (46)"; tree with Sequestrations, Adjustments, Activities, Uncertainty Discount; sources such as "2396-R.pdf + 19 more" | "Datapoints (12)"; two branches (Sequestrations, Activities); one removal = "Mass of waste biomass 7.242 t"; counterfactual inside Activities; 4 named source documents | Differs — TIRE's entry is roughly one-quarter the datapoint count, with no Adjustments or Uncertainty Discount branch |

**Length comparison.** Shorter. The Charm PDD is "at least 155 pages" and 58,881 computed words; the TIRE PDD is 65 file pages. Is the difference protocol-required or added content? The documents do not say in so many words. What can be quoted: (a) TIRE's document is the Isometric web-form render, where each answer sits under the protocol's own prompt (e.g. "B.2 Projects must define their system boundary and outline all GHGs considered across all sources, sinks and reservoirs (SSRs)…", p.9), so the prompts themselves are template content on both sides; (b) the largest Charm blocks are "Appendix 6: GHG Statement Report … 16,191" words and "Section B – Protocol and Monitoring Data … 14,978" words, whereas TIRE's equivalent GHG Statement Report is a separate 5-page document that says "Please refer to the TIRE PDD for a detailed explanation of assumptions and choices made." (ghg1 p.5) and its second edition says "No changes have been made since the last submission period" (ghg2 p.2); (c) Charm carries content with no TIRE counterpart — four feedstock appendices ("Appendices 2–5, computed at 1,450 / 1,469 / 1,480 / 1,471 words"), a biochar appendix ("App 11 … 4,548"), two storage sites, and a change log ("Section F change log (2,100 computed words)"); TIRE has one feedstock (5 pages), one site, one pathway. The GHG-report template TIRE uses states "After this document has been completed for the first time, it may be acceptable to refer back to relevant sections for subsequent Reporting Periods" (ghg1 p.1) — that is a template permission, and TIRE used it. Beyond those quotes, I cannot tell from the text how much of Charm's extra length is required by its protocols versus voluntarily added.

---

## 8. Cost / complexity / overhead reducers visible in the TIRE documents

Each row: what TIRE does (quote), what Charm does (baseline quote), and whether protocol text quoted in either PDD requires the heavier practice.

| # | Reducer at TIRE | Charm practice | Does quoted protocol text require the heavier practice? |
|---|---|---|---|
| R1 | **Carbon sampled on 1 load in 10 (Method B).** "the first 10 trucks of the feedstock will be tested to establish a baseline of carbon content, and every 10th truck is tested to represent the untested trucks." (p.11). Verifier accepted: "Yes, we collected 30 method A and then moved to method B." (vvr1 p.21). | "Per section 7.4.1.1.1 of the Bio-Oil Geological Storage protocol, a sample is taken for each injection batch and analyzed for C content" and "Isometric Protocol Method A". | Neither PDD quotes protocol text forbidding Method B for its pathway. The verifier's own gloss (vvr1 p.21): "Method A (detailed sampling of individual batches) must be completed for the first 30 batches before transitioning to Method B (periodic sampling)." Whether Charm's Bio-Oil protocol offers the same option is not stated in either document. |
| R2 | **No on-site weighing; supplier weigh tickets used.** "Biosolids truck loads are weighed at an external facility using calibrated equipment … No scale is available on site to perform truck weighing." (p.32) | "Mass is monitored by Scale Tickets provided by the injection well personnel … weighing the delivery truck prior to and after injection on a certified scale". | TIRE's own E.7 quotes the protocol as "the difference between truck arrival and departure weights on a calibrated scale to determine delivered mass (Section 7.3.3.1)" — which describes weighing at the receiving site; the PDD does not explain how a supplier-side weight meets that. Charm's practice is the one matching the quoted text. |
| R3 | **No uncertainty discount.** Every input assessed "<1%" and "has not been accounted for" (pp.24–28); "Uncertainty Discount | 0.00" (ver2 p.11). | "These uncertainties are propagated to the calculation of the gross quantity of CO2e sequestered for each injection batch." and a Charm registry entry with "Uncertainty Discount 1.072 t". | TIRE quotes no protocol threshold; its "1% threshold was applied consistently across all parameters" is its own rule. Charm cites "Section 7.4 of the Isometric Standard" for an Uncertainty Factor on one factor only. Cannot tell from the quoted text whether a discount is mandatory. |
| R4 | **Three-page GHG Statement Report, and a one-line second edition.** "No changes have been made since the last submission period" (ghg2 p.2); "Please refer to the TIRE PDD for a detailed explanation" (ghg1 p.5). | "Appendix 6: GHG Statement Report … 16,191" words inside the PDD, with "roughly 30 emission lines, each written out four times". | The template itself permits it: "After this document has been completed for the first time, it may be acceptable to refer back to relevant sections for subsequent Reporting Periods" (ghg1 p.1). Charm's longer form is not shown to be required. |
| R5 | **Embodied emissions passed once, then zero.** "Total embodied emissions are passed upfront, with EoL emissions being the primary embodied emissions considered given the facility's age." (ghg1 p.4); RP2: "0 tons of CO2 emissions from embedded carbon" (ghg2 p.3); verifier: "embodied emissions were only passed in the first verification, and no other emissions are to be addressed during this reporting period" (ver2 p.17). | "These values are amortized over the expected useful life of the equipment and improvements used, which is estimated in terms of total expected facility biomass throughput" — a per-tonne charge every period, plus railcar/truck per-mile embodied. | Neither PDD quotes Embodied Emissions Accounting module text on amortisation method. Not determinable from quoted text. |
| R6 | **Single flat transport distance and supplier-reported mpg.** "26.3 miles" "Google maps: road miles between supplier and well site" and "0.37 gallon/ton waste" "Measured - Fuel use mpg provided by transport company" (pp.23–24). | "Distance Based Method outlined in the Isometric Transportation Emissions Accounting module, using scale tickets to document the mass transported" and "When multiple routes are presented, the longest route is assumed", with GLEC factors, truck-scale uncertainty correction and per-mile embodied emissions for trucks and rail. | Charm cites the module's "Distance Based Method"; TIRE uses a fuel-based figure. No quoted text says either is mandatory. |
| R7 | **Monitoring plan is the permit table.** "The following table summarizes monitoring requirements for the facility as stated in the Class V UIC Permit" (p.53). | Option "B – I have submitted a Monitoring Plan … which describes any additional or modified parameters monitored which deviate from the default Monitoring Plan" with per-batch TAN, density, daily pH/temperature, displaced-brine analyses, and Appendix 8 reproducing each protocol requirement block. | Charm's bio-oil protocol module requires injectate chemistry (pH, TAN, density) that has no analogue in the biosolids module rows quoted by TIRE; the difference is pathway-driven, not shown to be voluntary. |
| R8 | **No consumable mass to subtract, no salt/LCS, no tote losses.** No such adjustment appears in the PDD or GHG reports. | "The mass of consumables added to the bio-oil being processed are subtracted from the Total Injectate Mass"; salt-residue 70% rule; "standard loss (which came out to 5.33kg) is assumed for each tote". | Pathway-driven — TIRE adds nothing to the waste that must be netted out. Not a protocol choice. |
| R9 | **Zero replacement emissions on one email.** "City of LA staff have confirmed via the attached Waste Partner Form that … will not increase use of synthetic fertilizer" (p.14) and files "Fertilizer Replacement Email Screenshot.png" (p.15). Verifier initially pushed back: "validation requires more formal documentation to create an auditable record" (vvr1 p.22), then accepted "Isometric's leakage assessment and added text". | "replacement emissions are considered 0 based on Biomass Feedstock Sourcing criterion C1: The feedstock currently serves no purpose." with SFI certificate and CSFS program documents. | Both PDDs cite the same module criteria; neither quotes text on evidence standard. |
| R10 | **Data flows by API from one in-house system with one person responsible.** "The Vaulted site/facility manager will be located at TIRE, and will oversee everything from internal data management, lab analysis, to operational data." and "It is now connected to Isometric's dMRV system via API." (p.33) | "All data related to the calculation of removals will be transmitted from Charm's Ledger software to Isometric directly via API." and "Datapoints are double-checked by Charm's MRV team prior to Ledger entry". | Resembles; no protocol text quoted. |
| R11 | **Stakeholder engagement deferred by exemption.** "An exemption from the pre-project timing element of this requirement is granted to Vaulted (TIRE)" (vvr1 p.30); "Stakeholder engagement activities have not yet been implemented" (vvr1 p.19). | Charm Section E "Stakeholder Input Process … 1,792" words describing completed engagement. | Standard §3.7/3.8 requires it per the exemption note; TIRE obtained an ad-hoc exemption. |
| R12 | **HPE pumping electricity by proxy, not metered.** "Power consumption from the pumps used to displace HPE and digested sludge to the site is not quantified in our meter; however, pump specifications are available." (p.33) | "The reading on both meters is noted by site staff prior to and following injection" (Vaulted GP) and utility meters at Charm sites. | Not determinable from quoted text. |
| R14 | **Twelve datapoints and four source files per removal in the registry.** Registry entry: "Datapoints (12)"; sources named on only four rows ("Not Integrated Feed Organic", "Hyperion- City of LA Directions to TIRE", "initial process energy use at the start of the audit period" / "final process energy use at the end of the audit period", "SDK Laboratories Distance To Tire"); grid factor, truck MPG and the 44/12 constant carried as "STANDARD PUBLISHED VALUE" / "CONSTANT" with no source file; site electricity entered as two meter readings for the whole period ("initial … at the start of the audit period" and "final … at the end of the audit period") rather than per load. | Charm entry: "Datapoints (46)" with per-source evidence lists such as "2396-R.pdf + 19 more", "W4 Kerry-AECN SGS COA.pdf + 1 more", "Standard Emission Factors + Calculations (8).xlsx", "GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf". | No protocol text on datapoint evidencing is quoted in either PDD; not determinable. |
| R13 | **Propane and lubricant from historical purchase records (later corrected).** FARs: "Historical propane purchase records are currently used as a proxy for estimating propane consumption within the LCA." (vvr1 p.19), status "Resolved" in RP2 (ver2 p.14). | "Vendor invoices" per purchase, "corrected for fuel pump uncertainty". | Verifier cited "Isometric Standard v1.0 §2.5.5" and required contemporaneous records — i.e. the heavier practice was required and TIRE was moved to it. |

**Where TIRE is more burdensome or lower-integrity than Charm (from the text):**

- **Baseline machinery Charm does not carry.** TIRE must maintain a five-year historical weekly baseline, a simulated "cushion", Class A/B tagging of every load, emergency-load exclusion and periodic re-evaluation: "Any emergency loads will be noted in Certify and in monthly verification reports if they occur." (p.13); "the ultimate baseline (historical volumes + cushion) will be evaluated monthly or quarterly for the first year" (p.14). RP2 had to correct RP1: "the previous audit period had a falsely low cushion" (ghg2 p.3). Charm's baseline rows are all "Excluded" or zero.
- **Only credits the increment.** RP2: 21,927.76 US tons injected, "18,780.8 US tons of waste across 20 weeks" assigned to baseline, "8,933.361 US tons" creditable (ghg2 p.3) — computed share creditable = 8,933.361 ÷ 21,927.76 = 40.7 %. Charm credits every tonne it injects.
- **Heavier subsurface programme.** Quarterly fall-off tests, quarterly reservoir/fracture model updates, quarterly ZEI evaluation, quarterly microseismic, quarterly gas/formation-fluid sampling, and InSAR/GPS subsidence (E.1 pp.55–57), versus Charm Louisiana's "every 6 mos" wellhead gas, annual MIT/falloff/tracer.
- **Lower-integrity points visible in the text (peer weaker than Charm):**
  - Carbon content on ~10 % of loads (R1) versus Charm's every batch.
  - Mass from a supplier scale with calibration "not confirmed in this case" (p.24) versus Charm's certified scale at the injection site.
  - Steel embodied "Estimated by the LCA expert … High uncertainty, based on expert judgment" (p.25); HPE electricity "based on proxies" (p.25).
  - Carbon content assumption "6%" "used for this process until real data is obtained" (p.26) written into the validated PDD.
  - Counterfactual deduction stated three ways: "two-pool" model (B.3 p.12), "three-pool" model and "discounts 1%" (Feedstock p.63–64), and "Counterfactual (2.92%)" in both GHG reports — the documents do not reconcile these.
  - Fertiliser-replacement zero rests on "Fertilizer Replacement Email Screenshot.png" (p.15), which the verifier called less "robust" than a signed statement (vvr1 p.22).
  - "NOTE to Isometric: Lab reports are forthcoming." left in the validated PDD (E.5 p.59).
  - Open ownership FAR: "The current ownership amendment will not be admissible for the next reporting period and Vaulted will need to provide a new amendment to remain in compliance" (ver2 p.18).

---

## Source List

All read 2026-09-14.

- Charm baseline: `/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/research/isometric_registry_review_2026-09/02_charm_pdd_baseline.md` — read in full (lines 1–353).
- Census entry and saved project-page capture: `01_registry_census.md` (TIRE rows and the "TIRE Project — Vaulted Deep" documentation list); `raw/prj_1K7HK8Q4S1S0D4W4.json`; `raw/docs_tire_p2.json` — read in full.
- TIRE PDD: https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVAA1X881S0Q1CZ/pdd.pdf — local `raw/tire/tire_pdd.pdf`, pages 1–65 read (Read tool, three passes: 1–20, 21–40, 41–60, 61–65).
- GHG Statement Report, RP1 (17 Jun 2026 row): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVBBX6RT1S0A41A/ghg_statement_report.pdf — local `raw/tire/tire_ghg1.pdf`, pages 1–5.
- GHG Statement Report, RP2 (01 Sep 2026 row): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1M1FC4PRQ1S0HC6Y/ghg_statement_report.pdf — local `raw/tire/tire_ghg2.pdf`, pages 1–4.
- Validation and Verification Report (17 Jun 2026): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVBSZVB01S0XHP2/validation_and_verification_report.pdf — local `raw/tire/tire_vvr1.pdf`, pages 1–44.
- Verification Report (01 Sep 2026): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1M1FC57011S0RNY8/verification_report.pdf — local `raw/tire/tire_ver2.pdf`, pages 1–22.
- Public Comment Summary (02 Feb 2026): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KH0V2VKY1S0G3CY/public_comment_summary.pdf — local `raw/tire/tire_pcs.pdf`, metadata only (1 page; title "[No Comments Received] [Vaulted TIRE]- Project Public Comment Summary").
- Registry project page: https://registry.isometric.com/project/prj_1K7HK8Q4S1S0D4W4 — via the saved capture `raw/prj_1K7HK8Q4S1S0D4W4.json` (taken earlier this session by the census pass).
- Registry GHG entry, read live with the plain `playwright` server (headless, read-only; navigation, snapshots, `innerText` reads and node-expanding clicks only):
  - https://registry.isometric.com/ghg-entry/rmv_1KYD9KRCD1S02J7Q?tab=calculation-view (tree expanded node by node; datapoints table)
  - https://registry.isometric.com/ghg-entry/rmv_1KYD9KRCD1S02J7Q?tab=removal-method
  - https://registry.isometric.com/ghg-entry/rmv_1KYD9KRCD1S02J7Q?tab=datapoints
  - https://registry.isometric.com/ghg-entry/rmv_1KYD9KRCD1S02J7Q?tab=calculation-view&expression=cmp_1KYD9KRCD1S09B6J.injectant_carbon_content_measurements&removal=rmv_1KYD9KRCD1S02J7Q (all 3 rows)
  - https://registry.isometric.com/ghg-entry/rmv_1KYD9KRCD1S02J7Q?tab=calculation-view&expression=cmp_1KYD9KRCD1S09B6J.historical_carbon_content_measurements&removal=rmv_1KYD9KRCD1S02J7Q (first page only, "Showing 10 of 318")
  - Captures saved: `raw/tire/ghg_entry_*.json`, `raw/tire/ghg_entry_calc_view_snapshot.md`, `raw/tire/ghg_entry_tree_expanded.md`.
- Not done: PDD word count (extraction blocked; page ranges given instead, per coordinator instruction). The `playwright-mrv-3` profile was not used after the clash was found.
- Guard consulted: `/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/.claude/hooks/doc_extraction_guard.sh` (to confirm which extraction routes are permitted).
