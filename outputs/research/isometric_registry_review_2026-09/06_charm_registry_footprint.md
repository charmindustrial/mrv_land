# Charm Bio-oil Geologic Storage — Public Registry Footprint

Prepared 2026-09-14 for the Isometric registry peer-comparison review, in the same shape as the peer deep dives so comparisons are like-for-like. Project: `Charm Bio-oil Geologic Storage` (Charm Industrial), pathway `Bio-oil Geological Storage`, project page https://registry.isometric.com/project/prj_1HZSSWBQM1S08H83.

How this was built. Three PDFs were downloaded from the registry's public document store into `raw/charm/` and read page-by-page with the Read tool (every page of all three). The GHG-entry page was opened in the headless browser (`playwright-mrv-4`), read-only: the calculation tree was expanded node by node and the datapoint table read from the page. Every quotation below is verbatim from a page or screen read this session, with the page number or screen location. Word counts are COMPUTED (count of whitespace-separated tokens in each page's text layer, via macOS's built-in PDF text reader); they are counts only — no quotation was taken from that text layer. Per-page counts are saved in `raw/charm/*_wordcount_by_page.json`.

---

## 0. Version check — public PDF vs internal Google Doc

**Public registry PDD** (`raw/charm/pdd.pdf`, linked from the project page as "Project Design Document | 20 Feb 2025"):
- Title page (p. 1): "Charm Industrial Bio-Oil Geologic Storage + Range & Plains Biochar Design Document" / "v1.11 – 2025/10/21". Every page footer reads "[ v1.11 – 2025/10/21]".
- File metadata Title: "[Without Biochar Appendix] Final V 1.11 Charm Industrial Bio Oil Geologic Storage PDD + Biochar.docx" (from `pdfinfo`).

**Internal document** (per `02_charm_pdd_baseline.md`, §1, built from Drive file `1V0v2atno-pVZQZ983EEy9sfmlci4cm_C`):
- "Title line "Charm Industrial Bio-Oil Geologic Storage + Range & Plains Biochar Design Document" followed by "v1.12 – 2025/12/01"".

**Verdict: MISMATCH.** Public = v1.11 (2025/10/21); internal = v1.12 (2025/12/01). The public file is also, by its own metadata title, the "[Without Biochar Appendix]" build.

### Section-level differences (from the two tables of contents)

Public TOC (p. 1, verbatim): "Section A: Key Project Data……. 2 / Section B: Protocol and Monitoring Data……. 7 / Section C: Duration and Crediting Period……. 51 / Section D: Environmental and Social Impacts …….52 / Section E: Stakeholder Input Process …….61 / Section F: Project Changes …….70 / Appendix 1: AECN Biomass Feedstock Information……. 72 / Appendix 2: Charm Biomass Feedstock Information – MacArthur Gulch……. 76 / Appendix 3: Charm Biomass Feedstock Information – Arkansas Mountain.... 81 / Appendix 4: Charm Biomass Feedstock Information – Arroyo Chico.... 86 / Appendix 5: GHG Statement Report……. 91 / Appendix 6: BCU Calculation Methodology……. 132 / Appendix 7: Basco 6 Bio-Oil Sequestration Site Permanence Monitoring and Permit Compliance Plan……. 135 / Appendix 8: Basco 6 Bio-Oil Sequestration Site Well Closure and Remediation Plan……. 144 / Appendix 9: Basco 6 EW Supplementary Subsurface Characterization……. 146".

Internal TOC (as tabulated in `02_charm_pdd_baseline.md` §1): Sections A–F, then "Appendix 1: AECN Biomass Feedstock Information" (72), "Appendix 2 … MacArthur Gulch" (76), "Appendix 3 … Arkansas Mountain" (81), "Appendix 4 … Arroyo Chico" (86), "Appendix 5: Charm Biomass Feedstock Information – Boulder Creek Watershed Project" (91), "Appendix 6: GHG Statement Report" (96), "Appendix 7: BCU Calculation Methodology" (137), "Appendix 8 – Basco 6 EW … Permanence Monitoring and Permit Compliance Plan" (140), "Appendix 9: … Well Closure and Remediation Plan" (149), "Appendix 10: Basco 6 Supplementary Subsurface Characterization" (151), "Appendix 11: Biochar Production and Storage PDD Appendix" (155).

| Difference | Public v1.11 (registry) | Internal v1.12 (Drive) |
|---|---|---|
| Top-level sections | 15 (A–F + Appendices 1–9) | 17 (A–F + Appendices 1–11) |
| Boulder Creek Watershed feedstock appendix | absent | present as Appendix 5 (TOC p. 91) |
| Biochar Production and Storage PDD appendix | absent (file metadata: "[Without Biochar Appendix]") | present as Appendix 11 (TOC p. 155) |
| GHG Statement Report appendix | Appendix 5, TOC p. 91 | Appendix 6, TOC p. 96 |
| BCU Calculation Methodology | Appendix 6, p. 132 | Appendix 7, p. 137 |
| Basco 6 Permanence Monitoring plan | Appendix 7, p. 135 | Appendix 8, p. 140 |
| Basco 6 Well Closure plan | Appendix 8, p. 144 | Appendix 9, p. 149 |
| Basco 6 Subsurface Characterization | Appendix 9, p. 146 | Appendix 10, p. 151 |
| Sections A–F page starts | A 2, B 7, C 51, D 52, E 61, F 70 | A 2, B 7, C 51, D 52, E 61, F 70 (identical) |
| Selected protocols (Section B) | p. 7: "Protocol Name:  Bio Oil Geological Storage" / "Protocol Version Number: v1.0"; "Biochar Production and Storage" v1.0; "Biochar Storage in Agricultural Soils" v1.0 | same three names and versions (baseline §2) |
| Total length | 149 pages, 53,269 computed words | ≥155 pages by its TOC, 58,881 computed words (baseline §1) |

Sections A–F have identical TOC page starts in both versions, so the structural difference between v1.11 and v1.12 is confined to the appendices: two appendices added (Boulder Creek; Biochar) and the rest renumbered. Text-level changes inside Sections A–F between v1.11 and v1.12 were not diffed (the internal .docx was not re-read this session; the two word counts use different extraction methods and are not directly comparable).

Note on the "Section F" page: the public TOC gives Section F at p. 70, but the heading "Section F" appears in the text layer of p. 66; the word-count table below uses the actual heading page (66).

---

## 1. Document size

### 1a. Public PDD (`raw/charm/pdd.pdf`)

- **Page count:** 149 (`pdfinfo`; Read tool rendered pages 1–149).
- **Computed word count:** 53,269 (sum of per-page counts; no page returned zero text).
- **Top-level sections:** 15.

| Section (public TOC heading) | Pages | Page count | Computed words |
|---|---|---|---|
| Title + Table of Contents | 1 | 1 | 146 |
| Section A – Key Project Data | 2–6 | 5 | 1,678 |
| Section B – Protocol and Monitoring Data | 7–50 | 44 | 14,962 |
| Section C – Duration and Crediting Period | 51 | 1 | 172 |
| Section D – Environmental and Social Impacts | 52–60 | 9 | 3,289 |
| Section E – Stakeholder Input Process | 61–65 | 5 | 1,924 |
| Section F – Project Changes | 66–71 | 6 | 2,115 |
| Appendix 1: AECN Biomass Feedstock Information | 72–75 | 4 | 1,254 |
| Appendix 2: Charm Biomass Feedstock Information – MacArthur Gulch | 76–80 | 5 | 1,468 |
| Appendix 3: Charm Biomass Feedstock Information – Arkansas Mountain | 81–85 | 5 | 1,487 |
| Appendix 4: Charm Biomass Feedstock Information – Arroyo Chico | 86–90 | 5 | 1,498 |
| Appendix 5: GHG Statement Report | 91–131 | 41 | 16,392 |
| Appendix 6: BCU Calculation Methodology | 132–134 | 3 | 1,169 |
| Appendix 7: Basco 6 Bio-Oil Sequestration Site Permanence Monitoring and Permit Compliance Plan | 135–143 | 9 | 3,889 |
| Appendix 8: Basco 6 Bio-Oil Sequestration Site Well Closure and Remediation Plan | 144–145 | 2 | 807 |
| Appendix 9: Basco 6 EW Supplementary Subsurface Characterization | 146–149 | 4 | 1,019 |
| **Total** | 1–149 | 149 | **53,269** |

Section B plus Appendix 5 = 14,962 + 16,392 = 31,354 words; 31,354 ÷ 53,269 = 0.589, i.e. 58.9% of the public document. (Section boundaries are page boundaries; where a section ends mid-page the words on that page are counted with the section that starts the page.)

### 1b. Most recent GHG Statement Report (`raw/charm/ghg_statement_report_2026-08-15.pdf`)

- Registry row: "15 Aug 2026 | GHG Statement Report". File metadata Title: "July Bio-Oil GHG Statement Report".
- **Page count:** 7. **Computed word count:** 1,582.
- Header (p. 1): "GHG Statement Report" / "Version 1.7". "Date of report" "8/11/26". Reporting Period "7/1/26-7/31/26".

| Section (heading as printed) | Pages | Computed words |
|---|---|---|
| Preamble (title, "Version 1.7", "Information requirements for verification are as follows:" …) | 1 | 139 |
| Section A – General Project Information | 1–2 | 163 |
| Section B – Project Details | 2 | 203 |
| Section C – Project Changes (C.1 Summary of changes; C.2 Impact of changes) | 3–4 | 565 |
| Section D – GHG Statement Methodology (D.1 Data; D.2 Calculations) | 4–6 | 346 |
| Section E – GHG Statement Results | 6–7 | 74 |
| Section F – GHG Statement Version Changes | 7 | 48 |
| Document History | 7 | 44 |
| **Total** | 1–7 | **1,582** |

Of the 346 words in Section D, most are the template's own italic prompts; Charm's answers in D.1 and D.2 are each the single line "Please see corresponding PDD Appendix" (pp. 5 and 6).

---

## 2. Calculation view and datapoints (GHG entry rmv_1KZBJBN9C1S0M5R5)

URL opened: https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=calculation-view — page title "159.49 tCO₂e GHG entry by Charm Industrial — Isometric — Isometric". This is the entry the project page links as its calculation example ("See GHG entry →").

Header block as read: "Certificates issued" | "1,000Y+" | "159.49 tCO₂e removed by Charm Industrial" | "rmv_1KZBJBN9C1S0M5R5" | Supplier "Charm Industrial" | Project "Charm Bio-oil Geologic Storage" | Tonnes removed "159.49 tCO₂e" | Sequestration date "19 Jul 2026 to 25 Jul 2026" | Reporting period "01 Jul 2026 to 31 Jul 2026" | Verification protocol version "Bio-oil Geological Storage v1.2" | Baseline protocol version "Bio-oil Geological Storage v1.0" | Verifier "350Solutions".

Three tabs: "Removal method", "Calculation view", "Datapoints".

**Removal method tab** (full text): "How carbon was removed / Biomass Carbon Removal and Storage (BiCRS) involves storing the carbon contained in waste biomass—organic material from living or recently living organisms. BiCRS works by halting or slowing the decomposition of biomass, enabling the carbon it contains to be stored long-term. This can be achieved by converting biomass into materials that decompose more slowly—such as biochar or bio-oil—or by storing it in environments where decomposition is slowed. For BiCRS to count as carbon removal, the biomass must be replenished to ensure additional carbon dioxide is drawn from the atmosphere." (Generic pathway text; nothing project-specific.)

### 2a. Calculation tree (every node expanded; values as displayed)

```
Net CO₂e Removed                                   159.491 t
= Sequestrations                                   193.725 t
    └ Injection sequestration                      193.725 t
+ Adjustments                                       20.929 tCO₂e
    ├ BCU - Transport Process                       10.115 tCO₂e
    └ Bio-oil processing                            10.814 tCO₂e
        ├ BCU - Diesel Site Emissions               10.002 tCO₂e
        ├ BCU - Waste Disposal Transport                80 kgCO₂e
        └ BCU - Additional Transport Process Emissions 732 kgCO₂e
- Activities                                        54.091 tCO₂e
    ├ Pyrolysis or other process                    17.069 tCO₂e
    │   ├ AECN pyrolysis (from rail loads) - process emissions   14.183 tCO₂e
    │   └ AECN pyrolysis (from rail loads) - embodied emissions   2.886 tCO₂e
    ├ Bio-oil transport                             10.511 tCO₂e
    │   ├ AECN to SOPOR Tanker Truck Transport Process Emissions        1.676 tCO₂e
    │   ├ SOPOR to Opelousas Rail Transport Process Emissions           7.770 tCO₂e
    │   ├ Opelousas to Basco - Tanker Truck Transport Process Emissions   669 kgCO₂e
    │   ├ Opelousas to Basco Tanker Truck Transport Embodied Emissions    143 kgCO₂e
    │   ├ SOPOR to Opelousas Rail Transport Embodied Emissions            120 kgCO₂e
    │   └ AECN to SOPOR Tanker Truck Transport Embodied Emissions         134 kgCO₂e
    └ Bio-oil injection                             26.511 tCO₂e
        ├ Basco Site Electricity Use (RECs)          1.850 tCO₂e
        ├ B6 Injection site diesel emissions        10.022 tCO₂e
        ├ B6 Injection site gasoline emissions         586 kgCO₂e
        ├ Support Travel                             6.781 tCO₂e
        ├ B6 Injection - Embodied Emissions          1.426 tCO₂e
        ├ Spare Parts and Consumables LA               483 kgCO₂e
        ├ Additional Transport: Rail Embodied Emissions     52 kgCO₂e
        ├ Additional Transport: Truck Embodied Emissions   420 kgCO₂e
        ├ Additional Transport: Rail Process Emissions      43 kgCO₂e
        ├ Additional Transport: Truck Process Emission     689 kgCO₂e
        ├ Waste Disposal: Transport Embodied                 8 kgCO₂e
        ├ Waste Disposal: Transport Process                 88 kgCO₂e
        └ Waste Disposal: Landfilling Emissions          4.065 tCO₂e
- Uncertainty Discount                               1.072 t
```

Node counts (as displayed): 1 root; 4 first-level terms (Sequestrations, Adjustments, Activities, Uncertainty Discount); 1 + 2 + 3 = 6 second-level nodes; 3 + 2 + 6 + 13 = 24 leaf emission/adjustment lines under the second level. Total emission lines under "Activities" (the project-emissions side): 2 + 6 + 13 = 21. Total adjustment lines under "Adjustments": 1 + 3 = 4. Arithmetic check on displayed values: 193.725 + 20.929 − 54.091 − 1.072 = 159.491 (matches the root).

Screenshot of the tree: `raw/charm/calc-view.png`. Page snapshot: `raw/charm/calc-view-snapshot.md`. Page text: `raw/charm/charm_ghg_entry_calcview_2026-09-14.txt`.

### 2b. Datapoints — "Datapoints (46)"

Table columns "Name | Value | Collection method | Sources". Collection method values: "Reported" (27 rows) or "Derived" (19 rows); 27 + 19 = 46. Source file names are shown as text (with "+ N more" expanders), not as download links. Rows in page order:

| # | Name | Value | Method | Sources (as shown) |
|---|---|---|---|---|
| 1 | Mass of Injectant (per injection) | 134.084 t | Reported | 2396-R.pdf + 19 more |
| 2 | Carbon Content of Bio-oil Injected (per injection) | 39.40 % | Reported | W4 Kerry-AECN SGS COA.pdf + 1 more |
| 3 | Constant CO₂ reduction | 10.115 tCO₂e | Reported | Charm-RetirementCertificate-RD-EACs-20251218.pdf |
| 4 | Constant CO₂ reduction | 10.002 tCO₂e | Reported | Charm-RetirementCertificate-RD-EACs-20251218.pdf |
| 5 | Constant CO₂ reduction | 80 kgCO₂e | Reported | Charm-RetirementCertificate-RD-EACs-20251218.pdf |
| 6 | Constant CO₂ reduction | 732 kgCO₂e | Reported | Charm-RetirementCertificate-RD-EACs-20251218.pdf |
| 7 | Bio-Oil Mass - AECN via Rail | 136.377 t | Reported | 2396-R.pdf + 19 more |
| 8 | Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) | 0.10 tCO₂e/t | Derived | Bioenergy AE Cote-Nord Canada - LCA CI calculation - 1Jul2025 to 31Dec2025 S.xlsx + 3 more |
| 9 | Carbon Intensity - AECN Pyrolysis Embodied Emissions (via Rail) | 0.02 tCO₂e/t | Derived | AECN Embodied Emissions Calc Sheet (1).pdf |
| 10 | Distance from AECN to Sopor Quebec (truck) | 107 mi | Derived | AECN to SOPOR (Baie Comeau) (2).png |
| 11 | Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck | 0.07 kgCO₂e/(km⋅t) | Derived | Standard Emission Factors + Calculations (8).xlsx |
| 12 | Distance from Sopor Quebec to Opelousas (rail) | 2,199 mi | Derived | image (44).png |
| 13 | Emission Factors - Rail Transport Fuel Use (Well to Wheel) | 0.02 kgCO₂e/(km⋅t) | Derived | GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf |
| 14 | Mass of load | 136.377 t | Reported | Full_Ticket_Rail_TILX200231_6.25.2026_offload_4_CAT1124426203267.pdf + 19 more |
| 15 | Distance from Opelousas to B6 (truck) | 43 mi | Derived | Opelousas Railyard to Basco.png |
| 16 | Allocated Distance Opelousas to B6 (truck) | 601 mi | Derived | Jul-18-2026-distance-route_map.png + 2 more |
| 17 | Emissions Factor - Vehicle Embodied Emissions - Tanker Truck | 0.1476 kgCO₂e/km | Derived | Standard Emission Factors + Calculations (8).xlsx |
| 18 | Allocated Distance Sopor Quebec to Opelousas (rail) | 3,844 mi | Reported | image (44).png |
| 19 | Emissions Factor - Vehicle Embodied Emissions -- Railcar | 0.0193 kgCO₂e/km | Derived | Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf |
| 20 | Aggregate Distance AECN to Sopor Quebec (truck) | 564 mi | Reported | AECN to SOPOR (Baie Comeau) (2).png |
| 21 | Basco Injection Electricity Usage (Grid) | 50,484.34 kWh | Derived | July 26 Louisiana Electricity.xlsx |
| 22 | Basco Injection REC Applied | 50,484.34 kWh | Derived | retirement-2026-07-22T09_16_04.pdf |
| 23 | Louisiana Grid | 0.46 kgCO₂e/kWh | Reported | Standard Emission Factors + Calculations - 2026 SPSO Electricity EFs_src_1KNMFRD6N1S0BZQ2.pdf |
| 24 | Louisiana RECS | 0.04 kgCO₂e/kWh | Reported | Standard Emission Factors + Calculations - 2026 SPSO Electricity EFs_src_1KNMFRD6N1S0BZQ2.pdf |
| 25 | Basco Diesel Used (Mass) | 2.590 t | Reported | 7.28.26.LA.Diesel.pdf + 15 more |
| 26 | Diesel emission factor | 3.87 kgCO₂e/kg | Reported | GLEC NA Fuel:Energy.png |
| 27 | Basco Injection Gasoline Usage (kg) | 157 kg | Derived | 7-1- 7-31 Gasoline Tracker LA.xlsx + 4 more |
| 28 | Emissions Factor - Gasoline - Combustion | 3.74 kgCO₂e/kg | Reported | GLEC NA Fuel:Energy.png |
| 29 | Basco Support Travel Emissions | 6.781 tCO₂e | Derived | Basco Support Travel Calc Sheet July 1 - July 31.xlsx |
| 30 | Basco Injection Embodied Emissions | 1.426 tCO₂e | Reported | Basco 6 Capital and Sitework Embodied Emissions Inventory July 1 - July 31.xlsx |
| 31 | Basco SP&C Emissions | 483 kgCO₂e | Derived | Basco Inj Operations SP+C Inventory July 1 - July 31.xlsx |
| 32 | Distance traveled | 1,656 mi | Reported | V2 July 2026 Additional Transport Emissions Calc Sheet.xlsx + 1 more |
| 33 | Emissions Factor - Vehicle Embodied Emissions -- Railcar | 0.0193 kgCO₂e/km | Derived | Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf |
| 34 | Distance traveled | 2,180 mi | Reported | V2 July 2026 Additional Transport Emissions Calc Sheet.xlsx |
| 35 | Emissions Factor - Vehicle Embodied Emissions - Non-Tanker Truck | 0.1198 kgCO₂e/km | Derived | Standard Emission Factors + Calculations (8).xlsx |
| 36 | Mass of load | 1,000 kg | Reported | — |
| 37 | Distance traveled | 1,656 mi | Reported | V2 July 2026 Additional Transport Emissions Calc Sheet.xlsx |
| 38 | Emission Factors - Rail Transport Fuel Use (Well to Wheel) | 0.02 kgCO₂e/(km⋅t) | Derived | GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf |
| 39 | Mass of load | 4.147 t | Reported | V2 July 2026 Additional Transport Emissions Calc Sheet.xlsx |
| 40 | Distance from Miniforge CO to Basco | 1,201 mi | Derived | CO to Basco Routing Map.png |
| 41 | Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Flatbed Truck | 0.09 kgCO₂e/(km⋅t) | Reported | Standard Emission Factors + Calculations (8).xlsx |
| 42 | Distance traveled | 40 mi | Reported | Screenshot 2026-08-10 at 11.38.11 AM.png |
| 43 | Mass of load | 15.694 t | Reported | V2Waste Disposal Emissions Calc Sheet - 7_26.xlsx |
| 44 | Distance traveled | 40 mi | Reported | Screenshot 2026-08-10 at 11.38.11 AM.png |
| 45 | Mass | 15.694 t | Reported | V2Waste Disposal Emissions Calc Sheet - 7_26.xlsx + 1 more |
| 46 | Landfilling Bio-Oil Contaminated Gravel | 0.26 kgCO₂e/kg | Reported | Standard Emission Factors + Calculations (5).xlsx |

Observations from the table itself: one datapoint (row 36, "Mass of load 1,000 kg") shows no source ("—"). Distinct source-file names visible without expanding the "+ N more" controls: 28. The "+ N more" counts visible sum to 19+1+19+3+19+2+15+4+1+1 = 84 additional files, so at least 28 + 84 = 112 evidence files sit behind this one removal's 46 datapoints (files can repeat across rows, so this is an upper bound on distinct files, not a count of them).

The "Datapoints" tab was not separately opened; the 46-row table above is the one rendered under the "Calculation view" tab, headed "Datapoints (46)". When a tree node is selected the same table filters to that node's inputs (for example, with "Sequestrations" selected the heading became "Datapoints (2)" and showed rows 1–2 only).

---

## 3. GHG Statement Report structure (15 Aug 2026 round)

File: `raw/charm/ghg_statement_report_2026-08-15.pdf`, 7 pages, 1,582 computed words (section table in §1b).

**Sections** (headings as printed): "Section A – General Project Information" (p. 1–2); "Section B – Project Details" (p. 2); "Section C – Project Changes" with "C.1 Summary of changes" (p. 3) and "C.2 Impact of changes" (p. 4); "Section D – GHG Statement Methodology" with "D.1 GHG Statement Methodology - Data" (p. 4–5) and "D.2 GHG Statement Methodology - Calculations" (p. 5–6); "Section E – GHG Statement Results" (p. 6–7); "Section F – GHG Statement Version Changes" (p. 7); "Document History" (p. 7).

**Preparer / period** (p. 1): "Garrett Lutz / Charm Industrial / Carbon Accounting Associate"; "Date of report" "8/11/26"; Reporting Period "7/1/26-7/31/26"; "Relevant project information if not included in PDD" "N/A".

**Batches / removals covered** (p. 2, Section B): "Injections ran across four weekly batches (INJ-07-2026-W1 through W4), covering nine removals totalling 710,723.48 kg of bio-oil injected." → 4 batches, 9 removals.

**Emission lines** (p. 6–7, Section E table, rows verbatim): "Gross Bio Oil Sequestered" 710,723.48 kg / 710.72 MT; "Gross CO2e Sequestered" 1,001,875.00 kg CO2e / 1,001.88 MT CO2e; under "Project Emissions": "Process Emissions" 170,605.00 / 170.61; "Site+Amortized Embodied Emissions" 26,510.00 / 26.51; "Uncertainty Discounts" 5,468.00 / 5.47; "Emissions Reductions" 74,998.00 / 75.00; "Total Emissions for Reporting Period (kg)" 202,583.00; "Total Emissions for Reporting Period (MT)" 202.58; "Net Removals for Reporting Period (kg)" 874,290.00; "Net Removals for Reporting Period (MT)" 874.29. → **4 emission lines** (Process; Site+Amortized Embodied; Uncertainty Discounts; Emissions Reductions) plus 2 gross lines and 2 totals. Arithmetic on the printed figures: 170,605 + 26,510 + 5,468 = 202,583 (matches "Total Emissions"); 1,001,875 − 202,583 + 74,998 = 874,290 (matches "Net Removals"), so the "Emissions Reductions" line is added back, not subtracted.

**Evidence documents referenced by name in the report:** 0. The report's only pointer to evidence is (p. 2) "All raw data and supporting documentation has been submitted either 1) directly to Isometric DMRV, or 2) directly to the VVB", and D.1 / D.2 each read "Please see corresponding PDD Appendix" (pp. 5–6). No file names, links or appendices are listed in the PDF.

**Project changes declared** (p. 3, C.1, three headed paragraphs): "Charm-Produced Bio-Oil Injections - Production Period MRV" ("Charm's integration of dMRV functionality for our CO production facility is not yet complete … Emissions for Charm oil have been computed and reported using the same spreadsheet-based method as outlined in the previous GHG Statement Report."); "Standard Bio-Oil Mass Deduction for Mass Lost to Sparging" ("… an average mass loss of 1.29% was observed across multiple samples. For all oil sparged on site, 1.29% of the input mass is deducted from the MOBI …"); "QOWV Batch Injected in June and Reported in July" ("One QOWV batch (rmv_1KZBTSNE81S0DJT1) was physically injected during the 2026-06-06 to 2026-06-13 window but is reported in this Reporting Period, within the INJ-07-2026-W1 batch."). Also p. 2: "Kerry Taste and Nutrition bio-oil transitioned from IBC tote delivery to bulk tanker delivery during this reporting period. … The filtration solids basis applied is 0.071%, taken from a May 2026 measurement of phase-separated Kerry calciner tar".

C.2 (p. 4) opens "Section is intentionally left blank. / No deviations occurred during this reporting period; therefore, no impact assessment is required." and is then followed by a three-row table (Period of change / Nature of change / Impact of change): "Use of spreadsheets, rather than Ledger API, to compute carbon intensity of Charm-produced bio-oil" — "De Minimis"; "Use of standard mass-loss based on empirical observation to account for mass change during sparging" — "De Minimis"; "June QOWV injection reported this period due to testing delay" — "N/A".

**Version log** (p. 7, Section F): one row, "8/14/26" / "874.29". Document History: "v1.6 June 2024 …", "v1.5 May 2024 …", "v1.4 November 2023 Public version" (the header says "Version 1.7"; the history table's latest row is v1.6).

---

## 4. Verification Report (15 Aug 2026 round)

File: `raw/charm/verification_report_2026-08-15.pdf`. **Page count: 32** — 31 numbered report pages ("page N of 31") plus a final Adobe Acrobat Sign audit page ("Verification Report / Final Audit Report / 2026-08-14 … Agreement completed. 2026-08-14 - 8:21:41 PM GMT"). Computed words: 7,615.

Cover (p. 1): "Verification Report / For Isometric"; "CDR Supplier Charm Industrial"; "Project Charm Bio-oil Geologic Storage"; "Verifiers Lily Schacht / Tim Hansen"; "Reporting Period July 1 – 31, 2026"; "Net CO₂e Removed 874.29 tonnes CO2e"; "Report Date August 14, 2026"; "Version V1.0" (page footers read "V1.2"; §6 Revision History p. 18 lists "Draft Version 1.0 (V1.0) August 13, 2026 N/A", "Version 1.1 (V1.1) Minor edits following internal QA", "Version 1.2 (V1.2) Minor edits following external review"). Document No. "350-IS.CHA.BO.18-VR" (p. 4).

**Structure** (Contents, p. 2): List of Tables; Acronyms and Chemical Definitions; 1. Introduction; 2. Technology Description (2.1 Changes since Validation and Previous Verification); 3. Verification Process (3.1–3.7); 4. Crediting Details (4.1, 4.2); 5. Verification Summary (5.1 Accuracy of the Opinion, 5.2 Verification Opinion, 5.3 Summary of Verification Findings, 5.4 Forward Action Requests & Recommendations); 6. Revision History; Appendix 1: Log of Findings (p. 19); Appendix 2: Documents Submitted for Review (p. 23); Appendix 3: Verifier Qualifications (p. 30).

**Opinion** (p. 12): "☒ Meets the requirements of Isometric Standard V1.8 and Bio-oil Geological Storage Protocol v1.2 (Kerry Bio-oil), v1.1 (AECN and Charm Bio-oil) for Verification". "By adhering to the requirements of the Isometric standard, protocols and modules, removals of 874.29 tonnes CO2e from Charm Industrial's Charm Bio-oil Geologic Storage have been verified in accordance with the validated PDD and the criteria listed in Section 3.5 with a reasonable level of assurance." Level (p. 8): "This verification was completed with a reasonable level of assurance. The materiality threshold of 5%, considering the totality of all omissions, errors, and misstatements, was applied to this audit."

**Findings count.** §5.3 (p. 13): "Assessment of the greenhouse gas removal statement identified no non-conformities, with only a few minor findings, clarifications, and non-material data issues (see Appendix 1). No significant findings that materially impacted the verified net carbon removals nor compliance with protocol standard were identified." Appendix 1 "Log of Findings" (pp. 19–22) has **7 findings**, all "Status" "Resolved", all "Resolved At" "14 Aug 2026":

| Issue Code | Date Issued | Type | Title | Resolution (verbatim) |
|---|---|---|---|---|
| ISS-86 | 13 Aug 2026 | Clarification Request | Thermal Oxidizer Temperature Excursions | "Explanation provided. Since the two reasons either mean there is a high or a low VOC concentration, can you add an indicator to the graph to show if the blower is off, which would allow us to distinguish between reason 1 and reason 2?" |
| ISS-85 | 12 Aug 2026 | Omission | Upload Mass evidence | "The converted file isn't visible. Acceptable for now considering it was provided in Google Drive, but please adjust for future reporting periods." |
| ISS-84 | 12 Aug 2026 | Clarification Request | No. of weeks / mo is not always 4 | "Will be adjusted in future reporting periods for more accurate emissions estimation" |
| ISS-83 | 12 Aug 2026 | Omission | Evidence for distance from carrier? | "Email evidence provided" |
| ISS-82 | 12 Aug 2026 | Clarification Request | Rail Mileage mismatch | "Explanation provided - small rounding error" |
| ISS-81 | 12 Aug 2026 | Omission | Map attached is a mismatch | "Clarification provided" |
| ISS-80 | 12 Aug 2026 | Clarification Request | AECN CI timing | "Charm will request more timely CI updates from AECN" |

So: 4 "Clarification Request" + 3 "Omission" = 7; 0 non-conformities; 0 corrective actions labelled as such. Example finding body (ISS-84, p. 20): "Just noting that the multiplier of weeks in the calculation sheet is currently 4. For July, it is a 4.5 week month. There should be 4 months per year where 5 weeks is used as the multiplier to be accurate. Noting this is non-material."

**Forward Action Requests** (Table 6, pp. 16–18): 4 rows, all typed "FAR (prior)" — two unnumbered ("NA") on Vaulted post-closure notification/monitoring, "ISS-36" (Basco site embodied-emissions allocation approach) and "ISS-34" (Nov 2025 PP embodied emissions allocations lagging forecast). Resolution column for the Vaulted FARs ends "July 2026: Compliance data has been collected in July and will be submitted for monitoring verification in August 2026"; for ISS-36/34: "July 2026: Updated amortization plan proposed and under review. To be implemented from August 2026 RP forward."

**Scope of detailed review** (Table 3, p. 10): 5 removals reviewed in detail — "rmv_1KZBJBN9C1S0M5R5 AECN Rail delivery Injection", "rmv_1KYT7WF6Q1S03R7Q AECN Rail delivery Injection", "rmv_1KYZ3JPB51S0VE5Q Kerry Bio-oil injection", "rmv_1KYWCXFBK1S0Y3NV Charm Aqueous Injection", "rmv_1KYWMYBJ51S0HH3N Charm Bio-oil Injection"; "representing two of the three weeks of injections and all process emissions. The operations sheet for the remaining removals (from Week 3) was compared to the Certify inputs to check for errors during data transfer." Table 4 (p. 11): "Net 874.29 / Sequestrations 1,001.88 / Activities -197.11 / Removal counterfactuals 0 / Losses 0 / Adjustments (Book and Claim Units) 75.00 / Uncertainty discount 0". Verification activities (Table 2, pp. 9–10): "August 12-13, 2026 Evidence Review and Verification", "August 13-14, 2026 Report Writing".

**Evidence footprint** (Appendix 2, pp. 23–28): "Table A4.1. Documents submitted on Isometric's Certify Platform" / "Appendix I: Reference Table" with columns "Source ID | File name". Computed count of rows beginning with a source ID (`src_…`): 27 + 34 + 34 + 34 + 34 + 20 = **183 rows** across pp. 23–28. Page 28 then reads "All sources referenced in the GHG Statement (capped at first 100 of 164 sources):" with nothing printed beneath it, and p. 29 reads "Table A4.2. Documents submitted through Google Drive / Pending" (the word "Pending" is highlighted). The 183-row table and the "164 sources" line do not agree; both are reported here as printed. Of the 183 rows, 25 are "INJ-07-2026-W1 Ops Notes.xlsx" through "INJ-07-2026-W4 Ops Notes.xlsx" (18 W1 + 5 W2 + 1 W3 + 1 W4 rows, by the row listing on p. 27), and the largest single family is rail scale tickets ("Empty_Ticket_Rail_…" and "Full_Ticket_Rail_…", pp. 25–26).

Protocols/modules applied (p. 8, §3.5): "Isometric Standard V1.8"; "Bio-oil Geological Storage Protocol v1.2 (Kerry Bio-oil), v1.1 (AECN and Charm Bio-oil)"; "Biomass Feedstock Accounting Module v1.3 (Kerry Feedstock), v1.2 (AECN and Charm feedstocks)"; "Biomass or Bio-oil Storage in Permeable Reservoirs v1.2"; "Embodied Emissions Accounting V1.0 (AECN and Charm Bio-oil)"; "Energy Use Accounting V1.2 (AECN and Charm Bio-oil), V1.3 (Kerry Feedstock)"; "Transportation Emissions Accounting V1.2 (AECN and Charm Bio-oil)"; "GHG Accounting V1.1 (Kerry Bio-oil)".

---

## 5. Document footprint — documents per verification round

Source: the project page's "Project documentation" table ("Showing 5 of 40", 8 pages), as recorded in `01_registry_census.md` and `raw/docs_charm_p2.jsonl`, `raw/docs_charm_p3.json` … `raw/docs_charm_p8.json` (page 1 from `raw/prj_1HZSSWBQM1S08H83.json`). 40 documents total.

| Submission date | Documents (titles as listed) | Count |
|---|---|---|
| 15 Aug 2026 | Verification Report; GHG Statement Report | 2 |
| 17 Jul 2026 | Verification Report; GHG Statement Report | 2 |
| 22 Jun 2026 | Verification Report; GHG Statement Report | 2 |
| 27 May 2026 | Verification Report; GHG Statement Report | 2 |
| 17 Apr 2026 | Verification Report; GHG Statement Report | 2 |
| 18 Mar 2026 | Verification Report; GHG Statement Report | 2 |
| 24 Feb 2026 | Verification Report; GHG Statement Report | 2 |
| 05 Dec 2025 | Verification Report; GHG Statement Report | 2 |
| 10 Nov 2025 | Name Change Confirmation | 1 |
| 02 Nov 2025 | Verification Report; GHG Statement Report | 2 |
| 09 Oct 2025 | Verification Report; GHG Statement Report | 2 |
| 24 Sep 2025 | GHG Statement Report; Verification Report | 2 |
| 03 Sep 2025 | GHG Statement Report; Verification Report | 2 |
| 04 Jul 2025 | GHG Statement Report; Verification Report | 2 |
| 06 Jun 2025 | GHG Statement Report; Verification Report | 2 |
| 17 Apr 2025 | GHG Statement Report; Verification Report | 2 |
| 20 Feb 2025 | PDD; Verification Report; GHG Statement | 3 |
| 21 Jan 2025 | Unsuccessful Verification Report | 1 |
| 18 Oct 2024 | No Public Comment Period; Charm Validation Report | 2 |
| 26 Jul 2024 | Charm Verification Report | 1 |
| 25 Jun 2024 | Charm Validation Report | 1 |
| 21 Jun 2024 | Charm GHG Statement Report | 1 |
| **Total** | | **40** |

Summary: 16 completed verification rounds each carry exactly 2 public documents (one GHG Statement Report + one Verification Report), except the 20 Feb 2025 round, which carries 3 (the PDD was posted with it). Rounds with a Verification Report: 17 (16 listed above + "Charm Verification Report" 26 Jul 2024); one "Unsuccessful Verification Report" (21 Jan 2025). Non-round documents: 1 PDD, 2 validation reports, 1 "No Public Comment Period", 1 "Name Change Confirmation". Arithmetic: 15 × 2 + 3 + 1 + 1 + 2 + 1 + 1 + 1 = 40. For comparison, the issuance table on the project page shows 18 issuance events (census: "18 issuance events, most recent 15 Aug 2026") against 17 Verification Reports in the document table; the registry does not state how the two map to each other.

---

## Source List

All read 2026-09-14.

Registry pages (headless browser `playwright-mrv-4`, read-only):
- https://registry.isometric.com/project/prj_1HZSSWBQM1S08H83 — project page (document table pages recorded in `raw/prj_1HZSSWBQM1S08H83.json`, `raw/docs_charm_p2.jsonl`, `raw/docs_charm_p3.json` … `raw/docs_charm_p8.json`, read earlier this session by the census pass; reused here for §5).
- https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=calculation-view — header, calculation tree (all nodes expanded), "Datapoints (46)" table. Captures: `raw/charm/calc-view.png`, `raw/charm/calc-view-snapshot.md`, `raw/charm/charm_ghg_entry_calcview_2026-09-14.txt`.
- https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=removal-method — "How carbon was removed" text.

PDFs (downloaded with curl to `raw/charm/`, read with the Read tool):
- https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KAERQ5A11S081G0/pdd.pdf → `raw/charm/pdd.pdf`, 149 pages, all read (pp. 1–149); quotes from pp. 1, 2, 7, 66, 80, 91, 113–129.
- https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1M02YCEEP1S0AVZB/ghg_statement_report.pdf → `raw/charm/ghg_statement_report_2026-08-15.pdf`, 7 pages, all read.
- https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1M02YD83Z1S0J5PN/verification_report.pdf → `raw/charm/verification_report_2026-08-15.pdf`, 32 pages, all read.

Word counts: `raw/charm/pdd_wordcount_by_page.json`, `raw/charm/ghg_statement_report_2026-08-15_wordcount_by_page.json`, `raw/charm/verification_report_2026-08-15_wordcount_by_page.json` (computed per page; counting only, no quotations taken from them).

Internal comparison document: `/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/research/isometric_registry_review_2026-09/02_charm_pdd_baseline.md` (§1 version line, TOC table and word counts; §2 protocol list), built earlier this session from Drive file `1V0v2atno-pVZQZ983EEy9sfmlci4cm_C`.
