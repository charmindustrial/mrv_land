# Peer Profile — Vaulted Deep, Great Plains Organic Waste Sequestration (Biomass Geological Storage)

Prepared 2026-09-14 for the Isometric registry peer-comparison review. Every quote is verbatim from a document or registry page read this session; the page number given is the PDF page (1-indexed, as rendered by the Read tool), and for the verification report the printed "page N of 32" footer matches the PDF page. Charm-side quotes come from `02_charm_pdd_baseline.md` (read in full this session) and are labelled with that file's section number. Where a fact is not in any document read, this profile says "not stated".

Three documents were read cover to cover:

- **PDD** — "Vaulted Deep Great Plains Facility Organic Waste Sequestration: Isometric PDD / Version 0.8" (p.1). PDF metadata title: "[Redacted] 2025.09.12 Vaulted PDD.docx". 83 pages. Registry document-table date: 18 Sep 2025.
- **GHG Statement Report** dated "08/18/2026" for Reporting Period "07/11/2026 – 08/10/2026" (p.1). 3 pages. Registry document-table date: 31 Aug 2026 (the most recent of the 60 documents).
- **Verification Report** "IS.VAU.GP.04 - VR", "Rev: v1.2", "Report Date: August 28, 2026" (p.4), 350Solutions. 32 pages. Registry document-table date: 31 Aug 2026.

Plus the registry pages for removal `rmv_1M0ACG4FJ1S02V0A` (Removal method, Calculation view, Datapoints tabs).

A note on the earlier interrupted attempt: the three PDFs were already in `raw/vaulted_great_plains/` and were reused; a leftover headless browser from that attempt was holding the `playwright-mrv-2` profile lock and was stopped before browsing.

---

## 1. Document size

### 1a. PDD — 83 pages

**Word count: not computed.** The workspace's document-extraction guard blocks every command-line text-extraction route (`pdftotext`, and Python `pypdf`/`pdfplumber`/`PyMuPDF`) with the message "Read the PDF with the Read tool (pages=N-M); it renders the actual page." The Read tool rendered the 83-page PDD as page images, not text, so no whitespace-token count could be produced. The GHG Statement Report (below) was rendered as text and was counted. The size comparison for the PDD therefore rests on page counts and the page span of each section, which were read directly.

Top-level structure (section heading as printed, start page, page span):

| # | Section heading (verbatim) | Start page | Pages |
|---|---|---|---|
| A | "Section A – Key Project Data" | 1 | 3.5 (p.1–4) |
| B | "Section B – Protocol and Monitoring Data" | 4 | 13 (p.4–17) |
| C | "Section C – Duration & Crediting Period" | 17 | 1.5 (p.17–18) |
| D | "Section D – Environmental and social impacts" | 19 | 2.5 (p.19–21) |
| E | "Section E – Stakeholder Input Process" | 21 | 1.5 (p.21–22) |
| F | "Section F – Project Changes" | 23 | 1.5 (p.23–24) |
| App 1 | "Appendix 1: Biomass Feedstock Information – Mixed woody waste" | 24 | 4 (p.24–27) |
| App 2 | "Appendix 2: Biomass Feedstock Information – Manure, 4S Feeders" | 28 | 4 (p.28–31) |
| App 3 | "Appendix 3: Biomass Feedstock Information – Biosolids, City of Derby" | 32 | 4 (p.32–35) |
| App 4 | "Appendix 4: Biomass Feedstock Information – Manure, Pratt Feeders" | 36 | 4 (p.36–39) |
| App 5 | "Appendix 5: Biomass Feedstock Information – Manure, KM Feeders" | 40 | 5 (p.40–44; p.44 blank) |
| App 6 | "Appendix 6: Biomass Feedstock Information – Manure, Sellers Feedlot Inc" | 45 | 4 (p.45–48) |
| App 7 | "Appendix 7: Biomass Feedstock Information – Manure, Golden Belt Feeders" | 49 | 4 (p.49–52) |
| App 8 | "Appendix 8: Biomass Feedstock Information – Manure, Ford County Feeders" | 53 | 4 (p.53–56) |
| App 9 | "Appendix 9: Biomass Feedstock Information – Manure, J-Six Farms LLC" | 57 | 4 (p.57–60) |
| App 10 | "Appendix 10: Biomass Feedstock Information – Manure, Wilroads Feed Yard" | 61 | 4 (p.61–64) |
| App 11 | "Appendix 11: Biomass Feedstock Information – Manure, Tiffany Cattle Company" | 65 | 4 (p.65–68) |
| App 12 | "Appendix 12: Biomass Feedstock Information – Manure, Stone Post Dairy" | 68 | 5 (p.68–72) |
| App 13 | "Appendix 13: GHG Statement Information" | 73 | 4.5 (p.73–77) |
| App 14 | "Appendix 14: Groundwater Monitoring Plan" | 77 | 3.5 (p.77–80) |
| App 15 | "Appendix 15: Stakeholder Input Process Summary" | 80 | 2.5 (p.80–82) |
| App 16 | "Appendix 16: Grievance Mechanism" | 82 | 1.5 (p.82–83) |

Twenty-two top-level sections (six lettered + sixteen appendices). Twelve of the sixteen appendices (App 1–12, p.24–72, 49 pages = 59% of the document: 49 ÷ 83 = 0.590) are the Isometric feedstock template filled once per supplier. Ten of the twelve are cattle manure and repeat the same eligibility text nearly word for word (e.g. App 4 p.38 and App 10 p.63 both read "Decay rate of manure is heterogenous and highly dependent on numerous variables, but decay rate applied over 50 years almost certainly leads to a trivially small mass of residual organic carbon."). The Section B core (boundary, baseline, sampling plan, monitoring, reversals, uncertainty, storage well) is 13 pages.

The Isometric template's italic question prompts are retained throughout (e.g. p.1 "Please provide a brief description (50-100 words) of your carbon removal Project."), as in Charm's PDD.

### 1b. GHG Statement Report (31 Aug 2026 listing) — 3 pages, 960 computed words

Computed from the Read tool's text rendering, transcribed to `raw/vaulted_great_plains/ghg_statement_report_2026-08-31_text.txt` and counted with `wc -w` (whitespace tokens, page markers excluded): **960 words total**; pages 1–2 = 658 words; page 3 = 302 words. Most of that is the Isometric template's own prompts. Vaulted's answer text is: the practitioner names, the registry link, two dates, one sentence on software ("GHG Inventory Management Software- Vaulted has an in-house software, DataVault, with the intent to consolidate all files and evidence for loads. DataVault acts as Vaulted's main access point for loads with Sharepoint as a secondary location for file access." p.1), one link ("Document Status and Events Monday.com Board" p.2), "Yes" (p.2), and the results paragraph on p.3.

Sections (template headings): "General Information" (p.1–2); "GHG Statement Methodology - Data" (p.2) — no answer text under it; "GHG Statement Methodology - Calculations" (p.2–3) — answer is the single line "No changes have been made since the last submission period" (p.3); "GHG Statement Results" (p.3).

The template itself licenses this brevity: "After this document has been completed for the first time, it may be acceptable to refer back to relevant sections for subsequent Reporting Periods, for example if there have been no changes to the GHG Assessment scope, data collection methodology, calculation methodology or assumptions." (p.1). The results section closes: "Please refer to the original GHG Statement for a summary of assumptions and choices made." (p.3).

### 1c. Verification Report — 32 pages (for reference)

Sections per its Contents (p.2): 1 Key Project Data; 2 Verification Details; 3 Technical Aspects; 4 Crediting Details; 5 GHG Statement Verification; 6 Verification Opinion (6.1 Results Summary, 6.2 Critical Findings and Forward Action Requests, 6.3 Exemptions from Isometric); 7 Revision History; 8 References; Appendices 1–5.

---

## 2. Project design

**Protocol (PDD p.4):** "Protocol Name: Biomass Geological Storage" / "Protocol Version Number: v1.0.0". Registry removal page: "Verification protocol version / Biomass Geological Storage v1.1" and "Baseline protocol version / Biomass Geological Storage v1.0". Verification report p.5: "The Project has since updated to Biomass Geological Storage Protocol v1.1, corresponding to the update from Biomass or Bio-oil Storage in Salt Caverns Module v1.0 to v1.1."

**Modules (Verification report p.4, "Verification Type"):** "Isometric Standard v1.7 / Biomass Geological Storage Protocol v1.1 / Biomass Feedstock Accounting Module v1.3 / Biomass or Bio-oil Storage in Salt Caverns Module v1.1 / Energy Use Accounting v1.2 / Transportation Emissions Accounting v1.1 / Embodied Emissions Accounting v1.0". The PDD itself cites "Isometric's Biomass Feedstock Accounting module (currently v1.2)" (p.8) and "EC13 (of Biomass Feedstock Accounting module version 1.2)" (p.30 and each manure appendix).

**Feedstock (PDD p.1):** "Vaulted secures a range of organic wastes (including biosolids, livestock and agricultural waste, paper sludge, and others) through sustainable sourcing practices from the surrounding area." Twelve supplier appendices: one mixed woody waste (Evergreen Companies, p.24), one biosolids (City of Derby, p.32), ten cattle/dairy manure. Section F (p.23): "Additional biomass feedstock suppliers, 4S, City of Derby, Pratt Feeders, KM Feeders, Sellers Feedlot Inc, Golden Belt Feeders, Ford County Feeders, J-Six, Wilroads, Tiffany Cattle, and Stone Post Dairy have been added as Appendices 2 to 12." Verification report p.9: "For this reporting period manure from commercial feedlots and biosolids were used and found to be eligible."

**Processing (Verification report p.9):** "Delivered by dump truck, feedstocks are unloaded into a mixing area where every tenth load is sampled for analysis in accordance with Method B of the Biomass Geological Storage Protocol sampling guidance. Recovered brine from the salt caverns is added to the biomass to form a slurry, which is then ground in a slurry processing unit until all particles pass through a specified screen. The prepared slurry is injected into the salt caverns at low wellhead pressures (~80 psi), displacing cavern brine in a controlled process. The displaced brine is stored in tanks and either reused in slurry mixing or, when in excess, routed to a Class I injection well for disposal." PDD p.1: "Vaulted then minimally processes the waste on-site and geologically injects them".

**Transport (PDD p.14):** "Transportation fuel use distance travelled — Google maps: road miles between supplier and well site — 38 miles". Calculation view: "Biomass transport distance 91.73 km REPORTED — City of Derby Directions to Vaulted". Verification report p.9: "Delivered by dump truck".

**Storage type and site (PDD p.16):** "Vaulted operates a built and permitted injection well site in Hutchinson, Kansas. This site is a network of 60 salt caverns, with the total capacity to hold 2-3 million metric tons of organic waste. The wells are permitted under Class UIC V well permits by KDHE." "EPA Well Class: Class V", "Permit number: KS-05-155-003", "Permit validity start date: Feb 8th 2022", "Permit validity end date: Feb 8th 2027" (p.16–17). Location: "7513 KS-14, Hutchinson, KS 67501 / 37.96676121453887, -97.94108576138514 / 60 salt caverns covered under a Class V organic waste injection permit and 1 commercial Class I well for displaced brine injection" (p.1). This is the same Hutchinson site named in Charm's PDD as one of Charm's two injection sites.

**Crediting period (PDD p.17–18):** "Start date of Project: 2023-08-22"; "Start date of crediting period: 2023-08-22"; "Total length of crediting period: 5 years". Verification report p.4: "Crediting Period August 20th, 2023 – August 19th, 2028" (a two-day difference from the PDD; not reconciled in either document).

**Reporting cadence:** monthly, on an 11th-to-10th cycle. GHG Statement Report p.1: "07/11/2026 – 08/10/2026". Verification report Appendix 3 (p.25–26) lists consecutive periods "December 14, 2024 – January 10, 2025", "January 11 – February 10, 2025", … "July 11- August 10, 2026: No change." The registry document table shows a GHG Statement (Report) plus Verification Report pair roughly monthly from 09 Apr 2024 to 31 Aug 2026 (60 documents; see `01_registry_census.md`).

**Batch / removal definition:** a removal is one day's injected mass. Registry: "Sequestration date 10 Aug 2026"; "Reporting period 11 Jul 2026 to 10 Aug 2026"; "Mass of waste biomass 23.532 t REPORTED" with sources "Not Integrated Feed Organic" ×3. The verification report p.11 confirms the boundary of a period: "This verification covers the emplacement of biomass between July 11, 2026 – August 10, 2026. While the reporting period is defined by the dates of physical emplacement, associated activities—including biomass procurement, transportation, slurry processing, monitoring, and other operational procedures—may have occurred outside this timeframe." The PDD's "Sampling plan" (p.10) refers to "batches" as truckloads: "triplicate measurements for the first 25 batches Vaulted has then proceeded to conduct a triplicate measurement on every 10th batch." Verification report p.15: "Sampling Frequency — Acceptable – Samples taken every 10th batch." and p.9: "every tenth load is sampled".

**Estimated capacity (PDD p.4):** 2023 "2,000"; 2024–2028 "30,000 – 50,000" each year.

**Ownership (PDD p.3):** "Vaulted wholly owns Advantek Cavern Solutions LLC, which is the sole operator of the Great Plains Facility and takes ownership over, and liability for, all injected materials. Vaulted owns the carbon rights to all sourced organic waste, as signed over by each organic waste partner."

---

## 3. System boundary

**Boundary statement (PDD p.5–6):** "All activities undertaken to permanently sequester carbon, at the point of taking ownership of the organic waste, are included in the system boundary. Activities within the system boundary include waste transportation, processing, injection, monitoring, and sequestration activities. As a part of these activities, emissions associated with the procurement of all necessary equipment to run the facility are included, considering standard lifespans. Direct and embedded (upstream) emissions in fuels, materials, and infrastructure are included. Also included is the counterfactual use case of the organic waste biomass and any relevant replacement emissions." / "Excluded from the system boundary are all upstream inputs to biomass cultivation and production (all inputs into growing the biomass itself, as well as transportation and other processing activities involved in creating the waste). These upstream inputs were excluded because the biomass taken is waste – not purpose grown biomass – so these upstream activities occur without Vaulted's involvement." / "Also excluded is the avoided CO2 and methane emissions that would have occurred in the counterfactual scenario of the waste decomposing above-ground without Vaulted's intervention."

**Boundary table (PDD p.7–8), 11 rows.** Quantification method is taken from the PDD's sensitivity table (p.14–15), Appendix 13 (p.74–76), and the registry calculation view, since the boundary table itself only gives inclusion and gases.

| # | Row (verbatim) | Included | Gases | How quantified (source) | Frequency | Uncertainty treatment (PDD p.14–15) |
|---|---|---|---|---|---|---|
| 1 | Baseline — "Counterfactual Emissions: Fuel Use from Feedstock Sourcing" | "Included" | CO2, CH4, NO2 | Set to zero: "No additional fuel usage on part of waste supplier due to Vaulted activities. The emissions are 0." | n/a | none |
| 2 | Baseline — "Counterfactual Emissions: Electricity Use from Feedstock Sourcing" | Included | CO2, CH4, NO2 | Zero: "No additional electricity usage on part of waste supplier due to Vaulted activities. The emissions are 0." | n/a | none |
| 3 | Baseline — "Counterfactual Emissions: Replacement of Feedstock Function" | Included | CO2, CH4, NO2 | "This project meets sustainable feedstock sourcing eligibility criteria to allow for a replacement emissions value of 0 to be used." Exception: biosolids (App 3, p.35) — "Yes — Accounting for the feedstock replacement emissions in the GHG Assessment", via a seven-step fertilizer-offset method; calc view: "Replacement Emission 14.00 kgCO₂e/t STANDARD PUBLISHED VALUE — 2024-08 [Vaulted] [Derby] Replacement Emissions for Biosolids" | per removal (mass × factor) | not in sensitivity table |
| 4 | Baseline — "Counterfactual Emissions: Temporary Carbon Storage from Feedstock" | Included | CO2, CH4 | Zero: "Vaulted will demonstrate the counterfactual fate is incineration within 5 years, thus the counterfactual temporary storage in the baseline is 0" (woody); manure/biosolids: "Resulting counterfactual storage penalty is 0." (each appendix) | one-time per feedstock | none |
| 5 | Project — "Fuel Use from Feedstock Transport" | Included | CO2, CH4, NO2 | Calculated: distance × truck MPG × diesel factor. Sensitivity table: "Measured - Fuel use mpg provided by transport company"; "Google maps: road miles between supplier and well site". Calc view: "Biomass transport distance 91.73 km REPORTED", "Empty truck MPG 5.50 mi/gal STANDARD PUBLISHED VALUE", "Fully loaded truck MPG 5.00 mi/gal STANDARD PUBLISHED VALUE", "Diesel Carbon Intensity 3,442.99 kg/m³", "Carbon intensity of combustion 4.05 kgCO₂e/kg". App 13 p.76: "gas mileage and distance for biomass transportation was used instead of the actual gallons/liters, due to data limitations associated with a third-party transport company." | per removal | "20% increase in fuel use … -0.803%"; "8% increase in transportation distance … -0.321%" — "Therefore, the original value has been used." |
| 6 | Project — "Embodied Emissions from Feedstock Transport" | Included | CO2, CH4, NO2 | Not visible in the calculation view for rmv_1M0ACG4FJ1S02V0A (no vehicle-embodied datapoint). Not stated how quantified. | not stated | not in sensitivity table |
| 7 | Project — "Electricity Use from Biomass Pre-processing" | Included | CO2, CH4, NO2 | Measured meter readings × grid factor. Calc view: "Processing & Injection energy use 153.60 kWh REPORTED — final process energy use at the end of the audit period + 1 more"; "Grid emissions factor 0.52 kgCO₂e/kWh STANDARD PUBLISHED VALUE". App 13 p.74: "The site manager provided processing and office electricity readings before and after processing each truck load" | per removal (meter before/after) | "Injection electricity consumption — Measured with the electricity reader — 2.5% increase … -0.018%" |
| 8 | Project — "Embodied Emissions from Equipment and Consumables for Biomass Pre-processing" | Included | CO2, CH4, NO2 | Estimated by site manager, amortised over lifetime capacity. Sensitivity: "Site material: steel — Estimated by the site manager — 3.5E-05 ton"; "Site material: concrete — Calculated based on actual data provided by the site manager — 7.7E-05 m3". App 13 p.75–76: "Materials were allocated to each metric ton of waste based on a conservative estimate of lifetime processing waste capacity of 2,000,000 metric tons of waste." Not visible as a datapoint in the calc view. | one-time factor | "20% increase in steel used … -0.012%"; concrete "-0.002%" |
| 9 | Project — "Electricity Use from Biomass Injection" | Included | CO2, CH4, NO2 | Same meter as row 7 (one datapoint covers "Processing & Injection"). Office electricity separately: "Final Office Meter Readout 10,483.00 kWh REPORTED", "Beginning Office Meter Readout 10,466.48 kWh REPORTED" | per removal | as row 7 |
| 10 | Project — "Embodied Emissions from Equipment and Consumables for Biomass Injection" | Included | CO2, CH4, NO2 | as row 8 | one-time | as row 8 |
| 11 | Project — "Carbon Content of Injected Biomass" | Included | CO2e | "Primary negative emission from process." Mass (scale) × carbon content (lab, Method B sampling) × 44/12. See Part 4. | per removal mass; C content every 10th load | C content: "the standard error (0.095) is subtracted from the average carbon content for the unsampled trucks … total net CO2e removals are reduced by 1%"; scale: "measurements must be within 100 lb … The uncertainty of the measurement is 0.23% (considering a 20 ton load). Because the uncertainty is well-below the 1% significance threshold, it has not been accounted for." |

**Sources named in the GHG Statement Report (p.3) but not in the boundary table:** "38.737 tons of CO2 emissions from diesel consumption on site" (calc view: "Front loader diesel consumption 0 kg REPORTED" for this removal); "0.32281 tons of CO2 emissions from MRV lab sampling" (PDD sensitivity row "CO2 monitoring -Lab sampling — Calculated based on mass x distance emission factors — 0.0008 t*km"); "114.665 tons of CO2 from screening emissions at supplier's site" (Verification report App 3, p.25: "October 2024 – Emissions from a) additional biomass screening performed by suppliers and b) returned biomass loads were added to the GHG Statement."); "6.996 tons CO2 emissions from historical cavern propane (CH4,CO2)" (Verification report p.16: "Vaulted deducts a conservative estimate of CO2 and CH4 release from wellheads using a mass flux model"; App 3 p.25: "February 10 – March 11, 2026 – GHG Statement revised to include a one-time deduction of emissions to conservatively address prior potential emissions identified via investigation of gas monitoring data. The LCA will also include a line item for emissions occurring during emplacement going forward."). In the calculation view the datapoints tab lists "Audit Period Emission 12 kgCO₂e DERIVED" as a node under "Processing and Injection"; what it contains is not stated on the page.

**Uncertainty approach (PDD p.13):** "Yes — Variance propagation" ticked; "No — Conservative estimate of input parameters"; "No — Monte Carlo Simulations". Screening rule (App 13 p.76): "If the net CO2e removal did not change by >1%, the original estimate was kept. If parameter uncertainty introduced a change larger than 1%, then a full uncertainty analysis was performed on the parameter and the conservative parameter estimation was used in calculations." Result (App 13 p.76–77): "Among the parameters that significantly contribute to the calculation of removals, only the biomass carbon content was found to have some uncertainty due to not every truck being sampled for the carbon content of its biomass. For that reason, one standard error was deducted from the average carbon content of the biomass from unsampled trucks. The rest of the parameters have very little uncertainty because they are based on measured, primary data." Verification report p.13: "Carbon content was identified as the only parameter contributing to a >1% change in Removal."

**Models (PDD p.15):** "No models were used for quantification or monitoring of this Project."

**Leakage (PDD p.8–9):** "Vaulted measures and assesses all leakage risk across each stage of removal activities. The largest area of potential leakage with Vaulted's approach is in the biomass replacement, which is fully measured and accounted for as per the Biomass Accounting Framework."

---

## 4. Gross removal calculation

**Formula, as displayed in the registry calculation view (removal rmv_1M0ACG4FJ1S02V0A, tree reproduced from the page):**

```
Net CO₂e Removed 5.908 tCO₂e
= Sequestrations 6.621 tCO₂e
  └ Estimation Biomass Sequestration 6.621 t
      = Mass of waste biomass 23.532 t
        × Estimated discounted carbon content 0.076734
            = WINSORIZED MEAN (Estimated carbon content of injectant, 18 measurements)
              − WINSORIZED STANDARD ERROR (Estimated carbon content of injectant, 18 measurements)
        × CO2e eq mass of C 3.666667
− Activities 384 kgCO₂e
  ├ Collection and Transport 284 kgCO₂e
  │   ├ Biomass Transport Fuel Usage Full Emissions 149 kgCO₂e
  │   ├ Biomass Transport Fuel Usage Empty Emissions 135 kgCO₂e
  │   └ Biomass Transport Front Loader 0 kgCO₂e
  └ Processing and Injection 100 kgCO₂e
      ├ Process Energy Usage Emissions 79 kgCO₂e
      ├ Audit Period Emissions 12 kgCO₂e
      └ Office Energy Usage Emissions 9 kgCO₂e
− Counterfactuals 329 kgCO₂e
  └ Replacement Emission 329 kgCO₂e
```

The page draws the operator between Activities and Counterfactuals as "+" (they are summed together, then the sum is subtracted). Arithmetic check on the displayed figures: 23.532 × 0.076734 × 3.666667 = 6.6209 ≈ 6.621; 6.621 − 0.384 − 0.329 = 5.908; 284 + 100 = 384; 149 + 135 + 0 = 284; 79 + 12 + 9 = 100; 23.532 t × 14.00 kgCO₂e/t = 329.4 kg; (10,483.00 − 10,466.48) kWh × 0.52 = 8.59 kg ≈ 9; 153.60 × 0.52 = 79.87 ≈ 79 (rounding of the displayed factor).

**Carbon-content method.** PDD p.10, "Sampling plan": "Vaulted has chosen Method B (Sampling a Production Process) to measure carbon content. The specific sampling cadence can be viewed in the 'Vaulted Deep GHG Statement_12.20.23' spreadsheet. Here you will see that after an initial period of conducting triplicate measurements for the first 25 batches Vaulted has then proceeded to conduct a triplicate measurement on every 10th batch. / To comply with the random sampling requirement, Vaulted and Isometric have agreed that Isometric can contact the Great Plains Biomass Facility before 9am MT to request the first three batches that day to be sampled. Isometric may request this random sampling approximately 1 day every 3 weeks." The template prompt above it (p.10) reads: "Please describe and provide evidence for how your Project has complied with the sampling requirements laid out in section 7.3.3.1.1 Biomass Carbon Content Measurement. If Method B (Sampling a Production Process) has been chosen by the Project, then describe the agreed upon random sampling approach."

The 18 measurements feeding this removal (registry, "Estimated carbon content of injectant — REPORTED — 18 measurements", each sourced "Carbon Content"): 0.070900, 0.070200, 0.072600, 0.084600, 0.087400, 0.085000, 0.077800, 0.092900, 0.091100, 0.080400, 0.079200, 0.071900, 0.072300, 0.068100, 0.070800, 0.079600, 0.079500, 0.078500. Plain mean of these 18 = 0.078489; sample standard deviation = 0.007446; standard error = 0.007446 ÷ √18 = 0.001755; mean − SE = 0.076734, which equals the displayed "Estimated discounted carbon content 0.076734". So for this removal no value was altered by the outlier rule (App 13 p.76: "Winsorization was applied to identify outliers, based on 3 standard deviations above and below the mean and outliers were adjusted."). Carbon content is therefore about 7.7% by mass of wet waste — the removal is roughly one tonne of carbon per 13 tonnes of waste.

**Rolling average, not per-load.** App 13 p.76: "For biomass that was not sampled for its carbon content, one standard error was subtracted from the rolling average to work with conservative estimates, as dictated by the Isometric Standard." Verification report p.13: "Carbon content measurement of every delivery batch is cost prohibitive; therefore, a conservative determination of content is made following instructions in the Biomass Geological Storage Protocol. … New feedstocks are tested every batch for at least 30 samples."

**Mass.** App 13 p.74: "Truck loads were weighed on site using a well-calibrated scale and recorded by the site manager." PDD p.14: "Truck load — Measured using the on-site scale — As measured per delivery — … The scale is calibrated annually, measurements must be within 100 lb (confirmed by email, screenshot added to evidence base)." Registry: "Mass of waste biomass 23.532 t REPORTED — Not Integrated Feed Organic + 2 more" (the two "more" are also "Not Integrated Feed Organic"; the verification report Appendix 1 lists files "V9-vaulted-2026-08-10-18990-not_integrated_feed_organic-111274.jpg" and "...-111272.jpg").

**Adjustments to mass.** None stated. No brine, water, or consumable subtraction appears in the PDD, the GHG Statement Report, or the calculation tree. The verification report p.9 says brine is added to make slurry ("Recovered brine from the salt caverns is added to the biomass to form a slurry") but the tree multiplies carbon content by the delivered waste mass, so the added brine does not enter the gross figure. Returned material: PDD p.11 "Should injected solid particulates return with the displaced cavern brine, they will be captured and reinjected."; Verification report App 3 p.25: "returned biomass loads were added to the GHG Statement" (October 2024).

**Units.** GHG Statement Report p.3 reports mass in US tons ("13,326.56 US tons of waste") and removals in metric tons ("4,061.55 metric tons of gross CO2"). Verification report p.13: "All non-metric values are converted to the equivalent metric basis."

**Rounding (App 13 p.76):** "Net removals in t CO2e for each removal activity was rounded to the nearest 0.01t CO2e in line with Isometric requirements."

---

## 5. Monitoring plan

**Option (PDD p.11):** "Yes — Vaulted has submitted a completed monitoring plan alongside this PDD". The plan itself is not in the PDD; what follows is what the PDD, verification report and Appendix 14 state.

| Parameter | How often | Instrument / method | Evidence named | Source |
|---|---|---|---|---|
| Truck mass | every delivery | "on-site scale … calibrated annually, measurements must be within 100 lb" | "screenshot added to evidence base"; weigh-scale photos ("V9-vaulted-…not_integrated_feed_organic…jpg") | PDD p.14; VR App 1 p.21 |
| Carbon content | "every 10th batch", triplicate; first 25 batches triplicate; new feedstocks "every batch for at least 30 samples"; random request "approximately 1 day every 3 weeks" | "Measured at a laboratory following the required standards" | "Carbon Content" source records; lab SOP requested (VR ISS 132) | PDD p.10, p.14; VR p.13, p.24 |
| Transport fuel | per delivery | "Fuel use mpg provided by transport company"; distance "Google maps" | "City of Derby Directions to Vaulted"; "see screenshots" | PDD p.14; registry |
| Processing/injection electricity | per delivery | "electricity reader" before/after | "final process energy use at the end of the audit period" | PDD p.14, App 13 p.74; registry |
| Office electricity | per period | meter readout | "final office energy use at the end of the audit period" | registry |
| Front loader / on-site diesel | per delivery | "Measured on site" | "V9-vaulted-82-initial_process_energy_use-111194.jpg" | PDD p.15; VR App 1 |
| Cavern pressure | continuous / daily | "real time data acquisition of the injection and post injection pressure data"; "pressure gauges at the injection wells and monitoring wells" | "Daily pressure reported to KDHE monthly" | PDD p.11, p.16; VR p.16 |
| Cavern volume / fill | "quarterly sonar survey"; "Monitoring of injected material measured daily and reported monthly, confirmed by sonar quarterly" | sonar | sonar reports to KDHE | VR p.15–16 |
| Groundwater (chloride) | "Samples are taken and analyzed quarterly as stated in KDHE Permit # KS-05-155-002" | three 2-inch monitoring wells MW-1/2/3, drop-screen sampler; "All monitoring samples are tested for chloride concentration (mg/l)… Concentration should not exceed 250 mg/l" | "2026 Q2 Monitoring Wells Report.pdf"; "USDW Monitoring Well Data.xlsx" | PDD App 14 p.78–79; VR App 1 |
| Displaced brine TOC, temperature, pH, conductivity/Cl | as permit; "Brine TOC measured prior to emplacement, as required by Class V permit" | "pH and Temp meter - Hanna 98191"; "Resistivity meter - FANN 88C"; "Density meter - Fann 140 Mud Balance" (calibration certificates) | "TOC Schedule_AR06.xlsx", "AR-06 Displaced brine 6-25-26 (1).pdf" | VR p.15, App 1 p.21 |
| Wellhead gas | continuous LEL detectors; "monthly wellhead grab sampling program"; "minimum of three reactive grab samples … in each rolling six-month period" | "Ultima X5000 gas monitor"; lab speciation "CO2, CH4, N2, O2, and VOC … 0.01 vol% resolution" | "Gas certificate .pdf"; monthly grab results | VR p.30–31, App 1 |
| Surface elevation | "Bi-yearly elevation surveys to ensure ground stabilization" | survey | — | PDD p.19 |
| Mechanical integrity | "regular testing for mechanical integrity of the wells and cavern integrity … when a new cavern is opened, during pre-injection, injection, and post-injection" | "logging, monitoring, wireline, analysis of well returns, pressure testing" | KDHE monthly/quarterly reports | PDD p.10, p.16 |
| Regulatory reporting | monthly and quarterly | — | "Monthly and quarterly reports are submitted to KDHE showing that the site is running safely, including data on groundwater quality, emplaced material spec, volume of injected material, and pressures and stability in the subsurface caverns." | PDD p.16 |
| Supplier eligibility re-check | "each supplier undergoes a full review and re-evidencing two years after initial certification" | affidavits | supplier affidavits | VR p.24 (ISS 122) |
| LCA / emission factors | "Vaulted review's and updates the LCAs annually. The last update was October 2025." | — | LCA | VR p.24 (ISS 121) |

**Gas-monitoring exemption in force (Verification report p.18–19, p.29–32).** Requirement: "Section 3.1.1 of the Biomass or Bio-oil Storage in Salt Caverns Module (v1.1) requires that if gas detection alarms are activated, the operator must immediately investigate and identify the cause of the alarm and report the instance to the VVB." Non-compliance: "Vaulted is not investigating every gas detection alarm activation. LEL alarms at the site have been increasing in frequency, and Vaulted is not conducting a cause investigation following each event." Exemption: "During active injection, Isometric is exempting Vaulted from the requirement to investigate every gas detection alarm activation. In place of per-alarm investigation, Vaulted is subject to the ongoing monthly grab sampling program and the reactive sampling plan (minimum 3 grab samples per rolling 6-month period following alarm events)". Second explanatory note (R-C165-1, p.29–30): "Wells must have species-specific gas detectors (or equivalent sensors/imaging) capable of detecting, at minimum, CO₂, CH₄ and propane (C3H8), with alarms and injection shut-off systems." … "The wells are equipped with continuous LEL (lower explosive limit) detectors that provide the required alarm and injection shut-off function but cannot speciate gases". Gas composition: "the displaced gas is overwhelmingly legacy propane, at 30.6% to 91.41% mol, against CH₄ at 0.019% to 0.096% mol." Three Forward Action Requests remain "Open" (VR p.17, Table 4).

**Site visit cadence (VR p.5):** "This verification did not include a site visit." "As required by Section 6.2.2 of the Biomass Geological Storage Protocol v1.1, a biennial on-site review of operational infrastructure and data collection systems was conducted on August 11th, 2025."

---

## 6. Calculation view (registry, rmv_1M0ACG4FJ1S02V0A)

Tree with values: see Part 4. Registry header: "5.91 tCO₂e removed by Vaulted Deep"; "Sequestration date 10 Aug 2026"; "Reporting period 11 Jul 2026 to 10 Aug 2026"; "Verifier 350Solutions". The "Removal method" tab carries only the generic BiCRS paragraph ("Biomass Carbon Removal and Storage (BiCRS) involves storing the carbon contained in waste biomass…") and, on the project page, a "Project Design Document" card linking the PDD.

**Datapoints — 16 listed on the Datapoints tab (the Calculation-view table shows 15; the extra row on the Datapoints tab is "CounterFactual Emissions 0 kgCO₂e DERIVED").**

| # | Name | Value | Collection method | Source named |
|---|---|---|---|---|
| 1 | Mass of waste biomass | 23.532 t | REPORTED | "Not Integrated Feed Organic" + 2 more (same title) |
| 2 | CO2e eq mass of C | 3.666667 | CONSTANT | — |
| 3 | Biomass transport distance | 91.73 km | REPORTED | "City of Derby Directions to Vaulted" |
| 4 | Diesel Carbon Intensity | 3,442.99 kg/m³ | STANDARD PUBLISHED VALUE | "Diesel Emissions Factor" |
| 5 | Empty truck MPG | 5.50 mi/gal | STANDARD PUBLISHED VALUE | — |
| 6 | Front loader diesel consumption | 0 kg | REPORTED | — |
| 7 | Carbon intensity of combustion | 4.05 kgCO₂e/kg | STANDARD PUBLISHED VALUE | — |
| 8 | Fully loaded truck MPG | 5.00 mi/gal | STANDARD PUBLISHED VALUE | — |
| 9 | Final Office Meter Readout | 10,483.00 kWh | REPORTED | "final office energy use at the end of the audit period" |
| 10 | Beginning Office Meter Readout | 10,466.48 kWh | REPORTED | "initial office energy use at the start of the audit period" |
| 11 | Grid emissions factor | 0.52 kgCO₂e/kWh | STANDARD PUBLISHED VALUE | — |
| 12 | Audit Period Emission | 12 kgCO₂e | DERIVED | — |
| 13 | Processing & Injection energy use | 153.60 kWh | REPORTED | "final process energy use at the end of the audit period" + 1 more |
| 14 | Replacement Emission | 14.00 kgCO₂e/t | STANDARD PUBLISHED VALUE | "2024-08 [Vaulted] [Derby] Replacement Emissions for Biosolids" |
| 15 | Estimated carbon content of injectant | Multiple values (18 measurements, each REPORTED) | — | "Carbon Content" ×18 |
| 16 | CounterFactual Emissions (Datapoints tab only) | 0 kgCO₂e | DERIVED | — |

Counts by collection method (16 rows): REPORTED 7 (rows 1, 3, 6, 9, 10, 13, 15); STANDARD PUBLISHED VALUE 6 (rows 4, 5, 7, 8, 11, 14); DERIVED 2 (rows 12, 16); CONSTANT 1 (row 2). Named source documents: 7 distinct titles ("Not Integrated Feed Organic", "City of Derby Directions to Vaulted", "Diesel Emissions Factor", "final office energy use at the end of the audit period", "initial office energy use at the start of the audit period", "final process energy use at the end of the audit period", "2024-08 [Vaulted] [Derby] Replacement Emissions for Biosolids") plus "Carbon Content" for the measurements; 7 rows carry no source ("—").

Not present in this removal's tree: any embodied-emissions node (steel/concrete), any lab-sample-transport node, any screening-at-supplier node, any historical-propane node, any brine or Class I disposal node, any uncertainty-discount node. The GHG Statement Report for the same period does list totals for lab sampling, screening and propane at period level (p.3), so those are accounted somewhere other than this per-removal tree; where is not stated on the registry page.

---

## 7. Side-by-side with Charm

| Item | Charm (baseline file, section) | Vaulted Great Plains (this profile) | Resembles / differs |
|---|---|---|---|
| **1. PDD length** | "at least 155 pages long by its own table of contents"; "58,881 words in the document body" (baseline §1) | 83 pages; word count not computable (see 1a); Section B core 13 pages | **Differs — Charm's is longer.** Charm's TOC last entry starts at p.155 vs Vaulted 83 pages: at minimum 155 ÷ 83 = 1.87×. |
| **1. GHG Statement Report length** | Appendix 6 of the PDD "GHG Statement Report" 16,191 words; the two largest cells "Data" 5,856 and "Calculations" 9,287 words (baseline §1) | 3 pages / 960 words, of which Vaulted's answer text is a few lines and "No changes have been made since the last submission period" | **Differs — Charm's is far longer.** 16,191 ÷ 960 = 16.9×. Caveat: Charm's stand-alone monthly GHG Statement Report PDFs on the registry were not read this session; the 16,191 figure is the PDD appendix version. |
| **1. Structure** | 17 top-level sections; 4 near-identical feedstock appendices | 22 top-level sections; 12 near-identical feedstock appendices (59% of pages) | Resembles in template; Vaulted's bulk is supplier repetition, Charm's is Section B + Appendix 6 (52.9% of words). |
| **2. Protocol** | "Bio Oil Geological Storage v1.0" (+ two biochar protocols) (baseline §2) | "Biomass Geological Storage v1.0.0" (PDD p.4), verified under v1.1 | Differs — sister protocols, same module family (Salt Caverns, Feedstock, Transport, Energy Use). |
| **2. Feedstock** | Woody biomass → pyrolysis bio-oil; AECN sawmill residue; 5 feedstock appendices | Raw manure, biosolids, mixed woody waste; 12 supplier appendices | Differs — no conversion step; Vaulted injects the waste itself. |
| **2. Processing** | Pyrolysis (Fort Lupton), rail/truck to El Dorado KS pre-processing "where it is treated to fit the local regulatory requirements for injection" — sparging, salt + LCS addition (baseline §2, §4) | "minimally processes the waste on-site" (PDD p.1); brine slurry + grinding (VR p.9) | Differs — Vaulted has one site and no chemical treatment step. |
| **2. Transport** | Truck + rail, Quebec/Colorado → Kansas → Kansas or Louisiana; "the longest route is assumed" (baseline §3) | Dump truck, "38 miles" (PDD p.14) / "91.73 km" (registry) | Differs — one short truck leg. |
| **2. Storage** | Same Hutchinson caverns (permit "KS-05-155-003") plus Basco 6 Louisiana | Hutchinson caverns only, "Permit number: KS-05-155-003" (PDD p.16) | **Resembles** — identical Kansas site and permit number; Charm's PDD quotes Vaulted's description verbatim. |
| **2. Crediting period** | "2024/03/01", "5 years" (baseline §2) | "2023-08-22", "5 years" (PDD p.17–18) | Resembles. |
| **2. Reporting cadence** | Not fixed in PDD; "roughly monthly-to-bimonthly" (baseline §2); registry Charm removal shows "Reporting period 01 Jul 2026 to 31 Jul 2026" | Monthly, 11th–10th; 60 documents since Dec 2023 | Resembles (monthly). |
| **2. Batch definition** | Injection batch = a "Lot" or combined Lots, one CHN sample per batch; Charm removal `rmv_1KZBJBN9C1S0M5R5` "Sequestration date 19 Jul 2026 to 25 Jul 2026", 159.49 t | One day's deliveries: "Sequestration date 10 Aug 2026", 23.532 t waste, 5.91 tCO₂e | Differs — Vaulted removals are per-day and small; Charm's are weekly aggregates. |
| **3. Boundary rows** | 40-row table + 2 extra sources (waste disposal, thermal oxidizer); AECN and Charm variants of each (baseline §3) | 11-row table; 3 extra period-level sources (lab sampling, supplier screening, cavern propane) | Differs — Charm 40 vs Vaulted 11. |
| **3. Embodied emissions** | Inventory + LCA factors "amortized over the expected useful life"; per-mile truck and railcar embodied; grid-infrastructure embodied (baseline §3 rows 13, 21, 23, 26) | "Estimated by the site manager — 3.5E-05 ton" steel and "7.7E-05 m3" concrete per tonne, over "2,000,000 metric tons" lifetime (PDD p.15, App 13 p.75) | Differs — Vaulted uses two site-manager estimates; Charm maintains an inventory. |
| **3. Uncertainty** | 14 measurement half-widths, each "propagated to the calculation of the gross quantity" (baseline §3); registry Charm tree has an "Uncertainty Discount 1.072 t" node | Same 20%/1% screening rule; only carbon content passes; handled by "mean − standard error" inside the carbon-content node; no separate discount node | Resembles in rule; differs in scope (1 parameter vs 14). |
| **4. Gross formula** | "Mass of Bio Oil Injected × average C content of the sample … × 44/12" (baseline §4) | "Mass of waste biomass × (Winsorized mean − Winsorized SE) × 3.666667" | Resembles in form. |
| **4. Carbon sampling** | "a sample is taken for each injection batch … Isometric Protocol Method A" (baseline §4) | "Method B (Sampling a Production Process)… every 10th batch" (PDD p.10) | **Differs — Vaulted samples 1 in 10 loads; Charm samples every batch.** |
| **4. Mass adjustments** | Consumables (salt + LCS) subtracted; salt-residue 70% credit; tote standard loss 5.33 kg +25%; AECN upstream loss +25% (baseline §4) | None stated | Differs — Vaulted has no mass adjustments. |
| **5. Monitoring** | 19 Kansas storage parameters in five-question format; per-batch TAN, density, C; daily pH/temp; displaced-brine taper (baseline §5b) | Permit-driven KDHE programme (quarterly groundwater, quarterly sonar, monthly reports, daily pressure); monitoring plan "submitted … alongside this PDD" but not in the PDD | Differs — Charm writes the storage monitoring into the PDD; Vaulted refers out to the permit and a separate plan. Note Charm's Kansas rows are largely "Vaulted" as tester. |
| **6. Calculation view** | Charm removal: 46 datapoints; tree "Sequestrations 193.725 t + Adjustments 20.929 tCO₂e − Activities 54.091 tCO₂e − Uncertainty Discount 1.072 t"; sources include lab COA PDFs, scale tickets, REC certificates, GLEC, eGrid, embodied inventories (raw/ghg_entry_charm_rmv_1KZBJBN9C1S0M5R5.json) | 15–16 datapoints; 7 REPORTED, 6 STANDARD PUBLISHED VALUE, 2 DERIVED, 1 CONSTANT; 7 rows with no source | **Differs — Charm 46 vs Vaulted 16 datapoints (2.9×).** Charm's Adjustments node (BCU/REC credits) has no Vaulted counterpart. |

**Is the length difference protocol-required or added content?** Neither PDD says in so many words which parts exceed protocol minimums, so this cannot be settled from the text alone. What the documents do show:

- Both use the same Isometric PDD template with the same prompts (compare Vaulted p.1 "Please provide a brief description (50-100 words)…" with Charm's retained prompts, baseline §1). The template is the same length for both, so the difference is in answer text.
- Charm's extra length sits in Section B's Monitoring Plan (3,527 words), Appendix 6's Data and Calculations cells (5,856 + 9,287), Appendix 8 (which "Reproduces each protocol requirement block … in full and answers under it"), and the Basco 6 appendices (baseline §9). Vaulted answers the equivalent prompts with a "Yes" and a pointer: "Vaulted has submitted a completed monitoring plan alongside this PDD" (p.11); "Full sensitivity analysis and calculations can be found in the Vaulted GHG Statement_12.20.23." (p.15); "Refer to PDD Section B – Protocol and Monitoring Data." (App 13 p.74); "See Sensitivity Analysis tab in 'Vaulted Deep GHG Statement_12.20.23' spreadsheet." (App 13 p.77). The template explicitly allows the pointer style for the GHG Statement Report ("it may be acceptable to refer back to relevant sections for subsequent Reporting Periods", GHG Statement Report p.1).
- Charm's PDD covers a second injection site (Basco 6, Appendices 8–10) and a second product line (biochar, Appendix 11, plus two more protocols), which Vaulted's does not; those sections alone are 803 + 984 + 3,847 + 4,548 = 10,182 words (baseline §1).
- So: part of the gap is scope (two sites, three protocols, two feedstock origins, pyrolysis + pre-processing), part is Charm writing content into the PDD that Vaulted files as separate documents (monitoring plan, calculation spreadsheet). Whether the protocol requires the in-PDD version cannot be told from either PDD's text; the Vaulted verifier accepted the pointer style ("Acceptable – PPD completed / updated appropriately and submitted.", VR p.14).

---

## 8. Cost / complexity / overhead reducers visible in the peer

Each item: what the peer does (quote), what Charm does (baseline quote), and whether protocol text quoted in either PDD requires the heavier practice.

**8.1 Carbon content sampled 1 load in 10 (Method B) instead of every batch.**
Peer: "Vaulted has chosen Method B (Sampling a Production Process) to measure carbon content. … after an initial period of conducting triplicate measurements for the first 25 batches Vaulted has then proceeded to conduct a triplicate measurement on every 10th batch." (PDD p.10). Verifier: "Carbon content measurement of every delivery batch is cost prohibitive; therefore, a conservative determination of content is made following instructions in the Biomass Geological Storage Protocol." (VR p.13).
Charm: "Per section 7.4.1.1.1 of the Bio-Oil Geological Storage protocol, a sample is taken for each injection batch and analyzed for C content to quantify the gross removal" and "Carbon content of the oil will be measured using Isometric Protocol Method A" (baseline §4).
Protocol text: the Vaulted template prompt names two methods — "If Method B (Sampling a Production Process) has been chosen by the Project, then describe the agreed upon random sampling approach." (PDD p.10) — so Method B is a protocol-permitted option under Biomass Geological Storage §7.3.3.1.1. Whether Bio-oil Geological Storage §7.4.1.1.1 offers the same option is not quoted in either PDD; Charm's text says "a sample is taken for each injection batch" as the requirement it follows. Cannot tell from the text read whether Charm could elect a Method B equivalent.

**8.2 Rolling-average carbon content with a one-standard-error deduction replaces per-batch propagation of instrument error.**
Peer: "For biomass that was not sampled for its carbon content, one standard error was subtracted from the rolling average" (App 13 p.76); registry node "WINSORIZED MEAN − WINSORIZED STANDARD ERROR". Only one parameter is uncertainty-treated: "only the biomass carbon content was found to have some uncertainty … The rest of the parameters have very little uncertainty because they are based on measured, primary data." (App 13 p.76–77).
Charm: fourteen separately justified half-widths — truck scale "160 lbs", LECO ".4%", fuel meter ".28%", LCS flow meter "2.045%", electricity meter "2%", etc. — "These uncertainties are propagated to the calculation of the gross quantity of CO2e sequestered for each injection batch." (baseline §3, §4).
Protocol text: both PDDs apply the same Isometric Standard screening rule (Charm: "Any parameter that, when increased by 20%, contributed to a change in the estimated removal that was greater than 1% … was then subject to an Uncertainty Analysis"; Vaulted: "If parameter uncertainty introduced a change larger than 1%, then a full uncertainty analysis was performed"). Under that rule Vaulted's scale error "0.23% … has not been accounted for" (PDD p.14). Charm's PDD does not state that its 160 lb scale half-width exceeded the 1% screen; it propagates it anyway. The protocol text quoted requires analysis only above 1%, so Charm's fuller propagation reads as added conservatism, not a stated requirement.

**8.3 Fuel from distance × MPG instead of invoices, meters and scale-ticket cargo weights.**
Peer: "gas mileage and distance for biomass transportation was used instead of the actual gallons/liters, due to data limitations associated with a third-party transport company." (App 13 p.76); registry: "Empty truck MPG 5.50 mi/gal STANDARD PUBLISHED VALUE", "Fully loaded truck MPG 5.00 mi/gal STANDARD PUBLISHED VALUE".
Charm: "GLEC emission factors using cargo weight, vehicle type, and distance traveled with a correction for truck scale uncertainty" (baseline §3 row 22); site diesel "quantity of fuel purchased for production on site as documented by purchase invoices … adjusted for fuel pump uncertainty" (row 15).
Protocol text: Charm cites "the Distance Based Method outlined in the Isometric Transportation Emissions Accounting module" (baseline §3 row 12); Vaulted's PDD does not name the module section. Neither quoted text requires invoices over MPG; cannot tell from the text which is the module minimum.

**8.4 Embodied emissions from two site-manager estimates, no inventory.**
Peer: "Site material: steel — Estimated by the site manager — 3.5E-05 ton"; "Site material: concrete — Calculated based on actual data provided by the site manager — 7.7E-05 m3" (PDD p.15); "Materials were allocated to each metric ton of waste based on a conservative estimate of lifetime processing waste capacity of 2,000,000 metric tons" (App 13 p.75–76). No embodied node appears in the per-removal tree. Charm's own PDD already adopts these same two Vaulted factors for the Kansas site ("0.0000351566 tons of steel and 0.000077 m3 of concrete per ton of waste injected", baseline §3 row 36).
Charm (for its own sites): "emission factors from reputable sources such as GREET database, the EcoInvent database, NAICS supply Chain Emission Factors, USLCI database, ICE database, and/or the Athena Impact Estimator. These values are amortized over the expected useful life of the equipment" (baseline §3 row 21); truck and railcar per-mile embodied; rail "cost-based calculation … DOT-111 railcar" (row 23); Basco 6 "Capital and Sitework Embodied Emissions Inventory July 1 - July 31.xlsx" (registry Charm datapoints).
Protocol text: Vaulted's verifier lists "Embodied Emissions Accounting v1.0" as applied (VR p.4); neither PDD quotes what that module requires. Cannot tell from the text.

**8.5 Monitoring plan and calculation workbook kept outside the PDD; PDD answers by pointer.**
Peer: "Yes — Vaulted has submitted a completed monitoring plan alongside this PDD" (p.11); "The specific sampling cadence can be viewed in the 'Vaulted Deep GHG Statement_12.20.23' spreadsheet." (p.10); "Full sensitivity analysis and calculations can be found in the Vaulted GHG Statement_12.20.23." (p.15).
Charm: Monitoring Plan option "B – I have submitted a Monitoring Plan … which describes any additional or modified parameters monitored" with the 3,527-word plan written into Section B; Appendix 6 carries the 9,287-word Calculations cell (baseline §5, §1).
Protocol text: the Isometric template offers both routes (Vaulted ticked "Yes … submitted … alongside"; Charm ticked "B – I have submitted a Monitoring Plan"). Neither quoted text requires the plan to be inside the PDD. Verifier accepted Vaulted's (VR p.14 "PPD completed / updated appropriately").

**8.6 Monthly GHG Statement Report reduced to "No changes" plus a results paragraph.**
Peer: "No changes have been made since the last submission period" (GHG Statement Report p.3); the Data section has no answer text; 960 words total including template.
Charm: Appendix 6 restates roughly 30 emission lines "each written out four times (Data Source; Data Quality Assessment; Calculation Methodology; Justification; Unit/Frequency; Modifications to Address Uncertainty)" (baseline §9).
Protocol text: the template itself permits the short form — "After this document has been completed for the first time, it may be acceptable to refer back to relevant sections for subsequent Reporting Periods … if there have been no changes" (GHG Statement Report p.1). This is template text present in both projects' reports; the heavier practice is not required by it.

**8.7 No mass adjustments (no consumables subtraction, no standard-loss rules).**
Peer: gross = delivered wet mass × carbon fraction; no subtraction appears anywhere (Part 4).
Charm: "The mass of consumables added to the bio-oil being processed are subtracted from the Total Injectate Mass"; salt residue "70% (used as a conservative estimate)"; tote loss "5.33kg … increased by 25%"; AECN upstream loss "+25%" (baseline §4).
Protocol text: Charm's adjustments arise from its own process (salt, LCS, totes), which Vaulted's process does not have; brine added to Vaulted's slurry is not subtracted because the multiplier is delivered waste mass, not injected slurry mass. Not a protocol difference; a process-design difference.

**8.8 One site, one truck leg, one grid factor.**
Peer: single facility; transport "38 miles" (PDD p.14); one grid factor "0.52 kgCO₂e/kWh".
Charm: two pyrolysis origins, a pre-processing site, two injection sites, rail + truck, three grid regions ("RMPA", "SPP North", "Louisiana Grid" per baseline §3 and registry), REC derating, BCU purchases with a cap rule. Not a protocol matter; project geography.

**8.9 Removal-level tree carries 15–16 datapoints against Charm's 46.**
Peer: see Part 6. Charm: 46 datapoints including 20 scale tickets ("2396-R.pdf + 19 more"), lab COAs, four REC retirement certificates, GLEC, eGrid, embodied inventories (raw/ghg_entry_charm_rmv_1KZBJBN9C1S0M5R5.json). Protocol text: not stated in either PDD.

**8.10 Supplier eligibility by affidavit and literature factor, with copy-paste appendices.**
Peer: "Historic manure output rate: approximately 14,649 metric tons per year - implied by average head of cattle 1,500 (affidavit from 4S Feeders) and average manure per head of cattle (estimate in literature of 59 lbs per day per beef cow) but not directly measured" (App 2 p.29); "Historic manure utilization rate: 0 (affidavit …)"; the same three-bullet block repeated for ten suppliers. Re-check "two years after initial certification" (VR p.24).
Charm: four forestry appendices "repeating the same eligibility tables and EC14 justification" (baseline §9), each tied to a named CSFS project; annual "signed affirmation" from all third parties (baseline §5a).
Protocol text: both follow the Biomass Feedstock Accounting module template; neither quotes a requirement for annual vs biennial re-attestation. Cannot tell from the text.

### Where the peer is MORE burdensome, or lower-integrity, than Charm

- **Carbon-content coverage.** 1-in-10 sampling with a rolling average versus Charm's one CHN result per batch: the peer's gross figure for most loads rests on other loads' measurements (VR p.13: "Carbon content measurement of every delivery batch is cost prohibitive"). Lower measurement coverage than Charm.
- **Fuel by MPG assumption, not measured fuel.** App 13 p.76: "gas mileage and distance … instead of the actual gallons/liters". Charm uses invoiced fuel and scale-ticket cargo mass (baseline §3).
- **Embodied emissions by site-manager estimate.** "Estimated by the site manager" (PDD p.15) versus Charm's itemised inventory. Charm's own PDD nonetheless adopts Vaulted's two factors for the Kansas site.
- **Open gas-monitoring non-compliance with exemptions.** "Vaulted is not investigating every gas detection alarm activation. LEL alarms at the site have been increasing in frequency" (VR p.18); "The wells are equipped with continuous LEL … detectors that provide the required alarm and injection shut-off function but cannot speciate gases" (VR p.29). Three FARs "Open" (VR p.17). Reversal-risk score rose: PDD says "Risk Score 0" (p.13) but the verifier reports "Risk Assessment Questionnaire score was 2 which indicates a Low (1-3) – 5% risk" (VR p.14). Charm's Kansas storage relies on the same Vaulted site and its PDD scores "Total Risk Score | 0" (baseline §7); Charm's PDD contains no equivalent open finding.
- **Registry buffer rate.** Registry project page text (census, `01_registry_census.md` line 226): "The risk of reversal for this project has been assessed as very low. This means that 2% of certificates issued for this project are allocated to Vaulted Deep's buffer pool." The verifier's "Low (1-3) – 5%" (VR p.14) is a different band from the registry's stated 2%; not reconciled in the documents read.
- **Draft regulatory data accepted.** VR p.18 waiver: "this verification was performed using draft monitoring reports substantiated by primary data records (e.g., sensor data, weigh tickets and DAS logs), as final regulatory sign-off is not a prerequisite for completing a verification."
- **Wet-mass, low-carbon feedstock.** At a carbon fraction of 0.076734, the registry example runs 23.532 t waste → 6.621 tCO₂e gross → 5.908 net, i.e. 23.532 ÷ 5.908 = 3.98 t of waste hauled and weighed per net tCO₂e; the GHG Statement Report period shows 13,326.56 US tons hauled for 3,610.88 net t. The number of deliveries, weigh tickets and photos per tonne of CO₂e is therefore high — a per-removal document burden that scales with mass, not with credits. This is heavier logistics per credit than Charm's bio-oil (Charm's 134.084 t injectant → 159.49 tCO₂e net in the registry example).
- **Twelve supplier appendices** versus Charm's five, and each new manure supplier adds a four-page appendix (Section F, p.23–24).
- **Monthly verification cycle** (60 documents since Dec 2023) — same order as Charm's cadence, not lighter.
- **Cavern propane legacy deduction.** "6.996 tons CO2 emissions from historical cavern propane (CH4,CO2)" (GHG Statement Report p.3) — an emissions line Charm's own Kansas removals do not carry in the Charm PDD (the phrase does not appear in the baseline profile).
- **Displaced brine to a Class I disposal well.** "when in excess, routed to a Class I injection well for disposal" (VR p.9) — an operational stream and monitoring set Charm's Louisiana site does not have; Charm's Kansas removals share it via Vaulted.

---

## Source List

All read 2026-09-14.

| Source | Location | Pages / scope |
|---|---|---|
| Vaulted Great Plains PDD v0.8 | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K5FAGRQ41S0P42Y/pdd.pdf — local copy `raw/vaulted_great_plains/pdd.pdf` | all 83 pages (Read tool, page images, ranges 1–20, 21–40, 41–60, 61–80, 81–83) |
| GHG Statement Report, RP 07/11/2026–08/10/2026 | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1M1BN9E5B1S0EY2R/ghg_statement_report.pdf — local `raw/vaulted_great_plains/ghg_statement_report_2026-08-31.pdf`; text transcript `…_text.txt` | pages 1–3 (Read tool, text) |
| Verification Report IS.VAU.GP.04 - VR v1.2 | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1M1BN9TN61S0P7T2/verification_report.pdf — local `raw/vaulted_great_plains/verification_report_2026-08-31.pdf` | pages 1–32 (Read tool, ranges 1–20, 21–32) |
| Registry removal — Calculation view | https://registry.isometric.com/ghg-entry/rmv_1M0ACG4FJ1S02V0A?tab=calculation-view | root and each expanded node; saved `raw/vaulted_great_plains/calc_view_*.md` / `.txt` |
| Registry removal — carbon-content measurements | https://registry.isometric.com/ghg-entry/rmv_1M0ACG4FJ1S02V0A?tab=calculation-view&expression=cmp_1M0ACG4FJ1S0R7DS.carbon_contents&removal=rmv_1M0ACG4FJ1S02V0A (pages 1–2 of 18 rows) | saved `raw/vaulted_great_plains/calc_view_carbon_measurements.txt` |
| Registry removal — Removal method tab | https://registry.isometric.com/ghg-entry/rmv_1M0ACG4FJ1S02V0A?tab=removal-method | saved `raw/vaulted_great_plains/removal_method_tab.txt` |
| Registry removal — Datapoints tab | https://registry.isometric.com/ghg-entry/rmv_1M0ACG4FJ1S02V0A?tab=data-points | saved `raw/vaulted_great_plains/datapoints_tab.txt` |
| Charm PDD baseline profile | `02_charm_pdd_baseline.md` | full file (lines 1–353) |
| Registry census (Vaulted rows and document table) | `01_registry_census.md` lines 15, 23, 101, 214–259; `raw/docs_vaultedgp_p2.json` … `p12.json` | as listed |
| Charm registry removal (for side-by-side) | `raw/ghg_entry_charm_rmv_1KZBJBN9C1S0M5R5.json` (https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=calculation-view) | full file |

Not read: Vaulted's separate monitoring plan, the "Vaulted Deep GHG Statement_12.20.23" spreadsheet, the "Isometrics removals spreadsheet (gss_1M0APA59J1S0D6KP)", the 2023 validation report, earlier GHG Statement PDFs, Charm's stand-alone monthly GHG Statement Report PDFs.

Browser: `playwright-mrv-2` (headless), read-only navigation, snapshots, tab and tree-node clicks only; closed at the end of the session.
