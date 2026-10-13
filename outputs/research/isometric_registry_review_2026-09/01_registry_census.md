# Isometric public registry census — 2026-09-14

Read-only survey of https://registry.isometric.com/projects and every project page listed there, taken on 2026-09-14 with the headless browser. Nothing was typed into or submitted to the registry. Every number below is copied from a registry page read today; the page URL is given next to it or in the Source List at the end. Raw page captures (full page text, tables and links exactly as read) are in the `raw/` folder next to this file, one JSON file per project (`raw/prj_<id>.json`), plus `raw/list_table_view.json` (the list in table form) and `raw/docs_*.json` (the extra pages of the document tables for the four geological-storage projects).

## Headline answers

**(a) How many projects in total: 75.** The list page header reads `Active projects (75)`; the Table view showed 50 rows on page 1 and 25 rows on page 2 with the `Next page` button disabled; the filter panel's Status counts (`Canceled (2)`, `Under validation (39)`, `Validated (33)`, `Validation unsuccessful (1)`) sum to 75, and its Pathway counts (`BiCRS (48)`, `Biosphere (6)`, `DAC (2)`, `EW (13)`, `Marine (5)`, `Superpollutants (1)`) also sum to 75. All 75 project pages were opened and captured. The registry lists canceled and unsuccessful projects under this same `Active projects (75)` heading, so 75 is everything the public registry shows, not only live projects.

**(b) How many are "verified": the registry does not use the word "verified" as a project status.** Its project status labels, exactly as shown on the list cards and in the filter panel, are `Validated`, `Under validation`, `Validation unsuccessful` and `Canceled`. The closest thing to "verified" at project level is `Validated`, which is what a project gets once Isometric has approved its validation report (each Validated project page shows an `Approval date`). **33 projects carry the `Validated` label.** Of those 33, **29 have a non-zero `Certificates issued` figure** (which means at least one GHG statement has passed verification and produced certificates) and 4 show `0.00` issued (`Burnsville`, `Helix`, `Project Dourado`, `ZX-24 Vulkaneifel` — their cards read `Certificates expected 2026` / `2027`). If "verified" is meant as "has verified removals with certificates issued", the answer is 29; if it is meant as the registry's own approval status, it is 33. Both readings are used below.

The figure the registry ranks projects by is the field it calls **`Certificates issued`** (Table view column header) / `certificates issued` (list cards) / `ISSUED` (project page header). On each project page the Certificates block reads `Issued`, `Retired`, `Buffer pool`, `Crediting period`, and the Issuances table has columns `Issue date | Issued | Buffer pool | Supplier allocation`. The `Issued` number is the gross number of certificates issued for the project, of which a slice goes to the buffer pool and the rest to the supplier — e.g. Charm's page: `Issued 8,426.77`, `Buffer pool 315.808`, and the Reversal risk text: "This means that 5% of certificates issued for this project are allocated to Charm Industrial's buffer pool. To date, this project has contributed 315.808 certificates to the buffer pool". One certificate corresponds to one tonne of CO2e on the GHG-entry pages (the entry linked from Charm's page is titled `159.49 tCO₂e removed by Charm Industrial` and shows `Tonnes removed 159.49 tCO₂e`). Only the registry's own `Issued` figure is used for ranking; nothing was recomputed.

**(c) Certificates issued per `Validated` project, ranked highest to lowest** — see the ranked table in the next section (33 rows).

**(d) Where Charm sits:** `Charm Bio-oil Geologic Storage` is **rank 5 of 33** Validated projects with **`8,426.77` certificates issued** (`Retired 5,105.13`, `Buffer pool 315.808`, 18 issuance events, most recent `15 Aug 2026`). Charm's second project, `Charm Range & Plains Biochar`, is **rank 22 of 33** with `101.03` issued (`Retired 3.449`, 3 issuance events, most recent `08 Sep 2026`). Within the BiCRS (biomass carbon removal and storage) family only, Charm Bio-oil is 3rd behind Vaulted Deep's Great Plains project (`70,234.61`) and Graphyte's Loblolly project (`20,444.62`). Within the two geological-storage pathway labels only (`Bio-oil Geological Storage` and `Biomass Geological Storage`, four projects), Charm is 2nd behind Vaulted Great Plains. Summed `Issued` across all 33 Validated projects, as read: 173,256.30 certificates; Charm Bio-oil is 4.9% of that (arithmetic on the registry figures above).

## Ranked table — all 33 `Validated` projects by `Certificates issued`

Figures are the registry's own `Issued` / `Retired` values from each project page (same `Issued` value appears in the list Table view). `Issuance events` is the N in the Issuances table's `Showing … of N`; `Most recent issue` is the top row's `Issue date`. `Approval date` and verifier (`Current verifier` / `Validated by`) are from the Project details block. A blank cell means the project page does not show that field at all (for example `Project Bhumisara` and `ERW Deployment: Seoni & North Chhattisgarh, India` show `Issued` and `Retired` but no `Buffer pool` line, and their Issuances table has no `Buffer pool` column).

| Rank | Project | Supplier | Pathway (registry `Protocol` label) | Location | Certificates issued | Retired | Buffer pool | Issuance events | Most recent issue | Approval date | Verifier | URL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Great Plains Organic Waste Sequestration | Vaulted Deep | Biomass Geological Storage | USA | 70,234.61 | 16,523.692 | 1,409.081 | 252 | 31 Aug 2026 | 22 Dec 2023 | 350Solutions | https://registry.isometric.com/project/prj_1HHYZFVGW1S044ZY |
| 2 | Reforesting the Brazilian Amazon Project 1 | Mombak | Reforestation | BRA | 21,771.53 | 0 | 2,286.012 | 3 | 01 Jul 2026 | 01 Jul 2026 | 350Solutions | https://registry.isometric.com/project/prj_1KA95092G1S093EM |
| 3 | Loblolly Project | Graphyte | Subsurface Biomass Carbon Removal and Storage | USA | 20,444.62 | 13,237.05 | 1,022.246 | 12 | 08 Jul 2026 | 07 Nov 2024 | 350Solutions | https://registry.isometric.com/project/prj_1J4P33N6W1S0RKE2 |
| 4 | US Southeast Enhanced Weathering Project | Lithos | Enhanced Weathering in Agriculture | USA | 12,332.95 | 1,397.302 | 246.661 | 4 | 18 Aug 2026 | 22 May 2026 | 350Solutions | https://registry.isometric.com/project/prj_1JY1YXDBS1S01Y05 |
| 5 | Charm Bio-oil Geologic Storage | Charm Industrial | Bio-oil Geological Storage | USA | 8,426.77 | 5,105.13 | 315.808 | 18 | 15 Aug 2026 | 20 Aug 2024 | 350Solutions | https://registry.isometric.com/project/prj_1HZSSWBQM1S08H83 |
| 6 | Humboldt Sawmill Company (HSC) | Pacific Biochar | Biochar Production and Storage | USA | 6,967.97 | 3,199.354 | 139.363 | 8 | 26 Jun 2026 | 16 Dec 2025 | 350Solutions | https://registry.isometric.com/project/prj_1JXCRW5ST1S0EEKH |
| 7 | Darjeeling Revival: Monsoon Harvest | Alt Carbon | Enhanced Weathering in Agriculture | IND | 6,579.94 | 919 | 131.6 | 1 | 29 Apr 2026 | 29 Apr 2026 | 350Solutions | https://registry.isometric.com/project/prj_1JZJY8NY61S0RH07 |
| 8 | Bioenergie Frauenfeld | Bioenergie Frauenfeld | Biochar Production and Storage | CHE | 6,065.36 | 7.006 | 60.654 | 1 | 04 Aug 2026 | 04 Aug 2026 | Normec Verifavia | https://registry.isometric.com/project/prj_1KP390EAC1S0WTMV |
| 9 | Nova Scotia Mineral OAE Project | Planetary | Ocean Alkalinity Enhancement from Coastal Outfalls | CAN | 4,853.6 | 2,059 | 97.075 | 4 | 30 Mar 2026 | 31 Mar 2025 | 350Solutions | https://registry.isometric.com/project/prj_1H502CZZH1S0VMYW |
| 10 | Darjeeling Revival: Alt x MOL | Alt Carbon | Enhanced Weathering in Agriculture | IND | 2,986.72 | 0 | 59.735 | 2 | 14 Apr 2026 | 22 Sep 2025 | 350Solutions | https://registry.isometric.com/project/prj_1JYCV03BW1S0RTE5 |
| 11 | Burney Forest Power v1.2 | Biochar Solutions | Biochar Production and Storage | USA | 2,821.91 | 0 | 56.439 | 1 | 17 Jul 2026 | 17 Jul 2026 | 350Solutions | https://registry.isometric.com/project/prj_1KESD32TS1S0ZHGV |
| 12 | TIRE Project | Vaulted Deep | Biomass Geological Storage | USA | 2,774.85 | 0 | 55.936 | 2 | 01 Sep 2026 | 17 Jun 2026 | 350Solutions | https://registry.isometric.com/project/prj_1K7HK8Q4S1S0D4W4 |
| 13 | Project Bhumisara | Earthrevive Technologies | Biochar Production and Storage | IND | 2,089.21 | 0 |  | 1 | 28 Aug 2026 | 28 Aug 2026 | Carbon Check | https://registry.isometric.com/project/prj_1KRAVH8Y81S0WQ8Z |
| 14 | Ontario Avenue Bio-Oil Sequestration | NULIFE GreenTech | Bio-oil Geological Storage | CAN | 1,404.08 | 329.619 | 14.052 | 8 | 26 Aug 2026 | 30 Sep 2025 | Normec Verifavia | https://registry.isometric.com/project/prj_1JQEQKCF91S06HAJ |
| 15 | New England WAE Project | CREW Carbon | Wastewater Alkalinity Enhancement | USA | 1,374.73 | 280 | 27.504 | 8 | 24 Aug 2026 | 30 Apr 2025 | 350Solutions | https://registry.isometric.com/project/prj_1JFA3YY9P1S0YVKR |
| 16 | ERW Deployment: Seoni & North Chhattisgarh, India | Mati | Enhanced Weathering in Agriculture | IND | 492.4 | 100 |  | 2 | 17 Jun 2026 | 17 Jun 2026 | Earthood | https://registry.isometric.com/project/prj_1JKR5RQG81S0Y2CZ |
| 17 | Project Serra da Mantiqueira | InPlanet | Enhanced Weathering in Agriculture | BRA | 389.42 | 81.025 | 7.789 | 2 | 18 Mar 2026 | 23 Dec 2024 | 350Solutions | https://registry.isometric.com/project/prj_1J7NQMR9V1S04P0D |
| 18 | La Perla | Silica | Enhanced Weathering in Agriculture | MEX | 322.54 | 0 | 6.451 | 1 | 24 Aug 2026 | 24 Aug 2026 | Verifit | https://registry.isometric.com/project/prj_1K3MGXD4A1S0S3H8 |
| 19 | Project Araçari | InPlanet | Enhanced Weathering in Agriculture | BRA | 319.97 | 0 | 6.4 | 1 | 04 Nov 2025 | 04 Nov 2025 | 350Solutions | https://registry.isometric.com/project/prj_1JQ775W7D1S0WYSA |
| 20 | Project Carcará | Terradot | Enhanced Weathering in Agriculture | BRA | 204.95 | 44.3 | 4.099 | 1 | 17 Mar 2026 | 29 Aug 2025 | 350Solutions | https://registry.isometric.com/project/prj_1K10D531D1S0DEV9 |
| 21 | DMS Georgia | Rewind | Subsurface Biomass Carbon Removal and Storage | GEO | 108.92 | 60 | 5.453 | 1 | 01 May 2026 | 01 May 2026 | Normec Verifavia | https://registry.isometric.com/project/prj_1KFDNVSDZ1S0QA39 |
| 22 | Charm Range & Plains Biochar | Charm Industrial | Biochar Production and Storage | USA | 101.03 | 3.449 | 2.042 | 3 | 08 Sep 2026 | 04 Aug 2025 | 350Solutions | https://registry.isometric.com/project/prj_1JN6XNWDQ1S0BSN7 |
| 23 | Kvina River CDR Project | CarbonRun | River Alkalinity Enhancement | NOR | 76.69 | 23.002 | 1.534 | 1 | 20 Jan 2026 | 20 Jan 2026 | 350Solutions | https://registry.isometric.com/project/prj_1K39D0N8S1S0TMKX |
| 24 | Hampton Roads WAE Project | CREW Carbon | Wastewater Alkalinity Enhancement | USA | 49.53 | 0 | 0.991 | 1 | 18 Dec 2025 | 18 Dec 2025 | 350Solutions | https://registry.isometric.com/project/prj_1K3S0527T1S0KYXT |
| 25 | Project Cajueiro | Mombak | Enhanced Weathering in Agriculture | BRA | 46.94 | 46 | 0.939 | 1 | 01 Apr 2026 | 01 Apr 2026 | 350Solutions | https://registry.isometric.com/project/prj_1JZ0ZD3JN1S0SHW9 |
| 26 | Project Agneerath | Earthrevive Technologies | Biochar Production and Storage | IND | 5.6 | 0 | 0.112 | 1 | 17 May 2026 | 17 May 2026 | Carbon Check | https://registry.isometric.com/project/prj_1KC8T0EGS1S0H36R |
| 27 | Project Nandani | Ground Up | Biochar Production and Storage | IND | 4.97 | 0 | 0.1 | 1 | 17 Apr 2026 | 17 Apr 2026 | Enviance | https://registry.isometric.com/project/prj_1JWX91R5E1S00PN0 |
| 28 | Deep Sky Alpha | Deep Sky | Direct Air Capture | CAN | 3.02 | 1 | 0.061 | 1 | 28 Jun 2026 | 30 Sep 2025 | 350Solutions | https://registry.isometric.com/project/prj_1HCHT9G2H1S05MYP |
| 29 | A Biochar Project at Satyapura | Equilibrium | Biochar Production and Storage | IND | 1.47 | 0 | 0.03 | 1 | 30 Jan 2026 | 30 Jan 2026 | Enviance | https://registry.isometric.com/project/prj_1K3VWSDS61S0QKV7 |
| 30 | Burnsville | Carba | Biochar Production and Storage | USA | 0.00 |  |  |  |  | 25 Jun 2026 | 350Solutions | https://registry.isometric.com/project/prj_1JRZWM3BP1S071QG |
| 31 | Helix | Planeteers | Biogenic Carbon Capture and Storage | DEU | 0.00 |  |  |  |  | 12 Dec 2025 | Normec Verifavia | https://registry.isometric.com/project/prj_1K4SN1CT61S0NZ7N |
| 32 | Project Dourado | InPlanet | Enhanced Weathering in Agriculture | BRA | 0.00 |  |  |  |  | 01 Apr 2026 | 350Solutions | https://registry.isometric.com/project/prj_1K21RKWYX1S0NWN6 |
| 33 | ZX-24 Vulkaneifel | ZeroEx | Enhanced Weathering in Agriculture | DEU | 0.00 |  |  |  |  | 28 Mar 2025 | EcoEngineers | https://registry.isometric.com/project/prj_1JMAPP8SA1S0BQAJ |

Ranks 30–33 (`Burnsville`, `Helix`, `Project Dourado`, `ZX-24 Vulkaneifel`) are `Validated` but show `0.00` certificates issued and no Certificates/Issuances block on their pages; they are approved projects that have not yet had a verified GHG statement produce certificates.

## Charm's position, spelled out

| Charm project | Rank among 33 Validated | Rank among 29 Validated with certificates | Certificates issued | Retired | Buffer pool | Issuance events | Most recent issue | Approval date | Crediting period | Verifier | Protocol version shown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Charm Bio-oil Geologic Storage | 5 | 5 | 8,426.77 | 5,105.13 | 315.808 | 18 | 15 Aug 2026 | 20 Aug 2024 | 01 Mar 2024 to 28 Feb 2029 | 350Solutions | Bio-oil Geological Storage v1.2 |
| Charm Range & Plains Biochar | 22 | 22 | 101.03 | 3.449 | 2.042 | 3 | 08 Sep 2026 | 04 Aug 2025 | 01 Mar 2024 to 01 Mar 2029 | 350Solutions | Biochar Production and Storage v1.0 |

Ranks among the 29 with certificates are the same as among the 33 because the four zero-certificate projects sit at the bottom.

## Full table — all 75 projects

Status and pathway are the registry's own labels. `Location` is the three-letter code from the Table view; the free-text location shown on the project page (where the page shows one) is in the CSV. Certificate figures for `Under validation`, `Canceled` and `Validation unsuccessful` projects show `0.00` in the Table view and the project pages have no Certificates block. Full detail, including PDD and calculation-view links for every project, is in `01_registry_census.csv`.

| # | Project | Supplier | Pathway (registry `Protocol` label) | Family tag on page | Location | Status | Certificates issued | Retired | Issuance events | Most recent issue | Public documents | Most recent document | Durability | URL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A Biochar Project at Satyapura | Equilibrium | Biochar Production and Storage | BICRS | IND | Validated | 1.47 | 0 | 1 | 30 Jan 2026 | 7 | 30 Jan 2026 | 200Y+ | https://registry.isometric.com/project/prj_1K3VWSDS61S0QKV7 |
| 2 | B10 - Brondal #1 | B10 | Biochar Production and Storage | BICRS | ZAF | Under validation | 0.00 |  |  |  | 2 | 05 Jan 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JTZ7NRK81S0GA0S |
| 3 | Bharat Biochar Initiative | FusionPact | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 27 Apr 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K4PWG5T01S0PWMF |
| 4 | Bigadan - BioCCS | Bigadan | Biogenic Carbon Capture and Storage | BICRS | DNK | Under validation | 0.00 |  |  |  | 0 |  | 1,000Y+ | https://registry.isometric.com/project/prj_1KJQ2NM0R1S09256 |
| 5 | Biochar production using dead areca nut biomass | Earthtree Enviro | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 19 May 2026 | 200Y+ | https://registry.isometric.com/project/prj_1K56VP7FE1S0QDSH |
| 6 | Bioenergie Frauenfeld | Bioenergie Frauenfeld | Biochar Production and Storage | BICRS | CHE | Validated | 6,065.36 | 7.006 | 1 | 04 Aug 2026 | 5 | 04 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KP390EAC1S0WTMV |
| 7 | Burney Forest Power v1.2 | Biochar Solutions | Biochar Production and Storage | BICRS | USA | Validated | 2,821.91 | 0 | 1 | 17 Jul 2026 | 5 | 21 Aug 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KESD32TS1S0ZHGV |
| 8 | Burnsville | Carba | Biochar Production and Storage | BICRS | USA | Validated | 0.00 |  |  |  | 3 | 25 Jun 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JRZWM3BP1S071QG |
| 9 | Capital Link's Berthoud Facility | Capital Link Green | Biochar Production and Storage | BICRS | USA | Under validation | 0.00 |  |  |  | 2 | 30 Sep 2025 | 200Y+ | https://registry.isometric.com/project/prj_1JYENJXB71S0CR1B |
| 10 | Carboneers & Terrafront High Tech Biochar | Carboneers | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 27 Mar 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JF8BBG921S010M4 |
| 11 | Carboneyes: Udongo | Carboneyes | Biochar Production and Storage | BICRS | KEN | Under validation | 0.00 |  |  |  | 2 | 19 Jun 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KFTFVQTY1S08RE0 |
| 12 | CarbonZero.eco - Williams | CarbonZero | Biochar Production and Storage | BICRS | USA | Under validation | 0.00 |  |  |  | 2 | 09 Apr 2026 | 200Y+ | https://registry.isometric.com/project/prj_1K48633C61S0WY58 |
| 13 | Chara Mattampally | Sow & Reap Chara | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 14 Sep 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KMMPMZJV1S0H2YW |
| 14 | Charm Bio-oil Geologic Storage | Charm Industrial | Bio-oil Geological Storage | BICRS | USA | Validated | 8,426.77 | 5,105.13 | 18 | 15 Aug 2026 | 40 | 15 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1HZSSWBQM1S08H83 |
| 15 | Charm Range & Plains Biochar | Charm Industrial | Biochar Production and Storage | BICRS | USA | Validated | 101.03 | 3.449 | 3 | 08 Sep 2026 | 9 | 08 Sep 2026 | 200Y+ | https://registry.isometric.com/project/prj_1JN6XNWDQ1S0BSN7 |
| 16 | Climate smart rice farming in India | Mitti Labs | Rice Methane Reduction | SUPERPOLLUTANTS | IND | Under validation | 0.00 |  |  |  | 1 | 07 Sep 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KT1H7QB71S0NVJV |
| 17 | Cocoa Biochar Carboneers | Carboneers | Biochar Production and Storage | BICRS | GHA | Under validation | 0.00 |  |  |  | 2 | 05 Jan 2026 | 200Y+ | https://registry.isometric.com/project/prj_1K2YPGE781S0A3Q0 |
| 18 | Corigin-1: BioChar Q3-25 | Corigin | Biochar Production and Storage | BICRS | USA | Under validation | 0.00 |  |  |  | 2 | 05 Jan 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K051N4HQ1S02170 |
| 19 | Darjeeling Revival Project | Alt Carbon | Enhanced Weathering in Agriculture | EW | IND | Validation unsuccessful | 0.00 |  |  |  | 3 | 07 Nov 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JCZCRW2S1S06KN0 |
| 20 | Darjeeling Revival: Alt x MOL | Alt Carbon | Enhanced Weathering in Agriculture | EW | IND | Validated | 2,986.72 | 0 | 2 | 14 Apr 2026 | 7 | 14 Apr 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JYCV03BW1S0RTE5 |
| 21 | Darjeeling Revival: Monsoon Harvest | Alt Carbon | Enhanced Weathering in Agriculture | EW | IND | Validated | 6,579.94 | 919 | 1 | 29 Apr 2026 | 5 | 29 Apr 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JZJY8NY61S0RH07 |
| 22 | Deep Sky Alpha | Deep Sky | Direct Air Capture | DAC | CAN | Validated | 3.02 | 1 | 1 | 28 Jun 2026 | 5 | 29 Jun 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1HCHT9G2H1S05MYP |
| 23 | DMS Georgia | Rewind | Subsurface Biomass Carbon Removal and Storage | BICRS | GEO | Validated | 108.92 | 60 | 1 | 01 May 2026 | 4 | 01 May 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KFDNVSDZ1S0QA39 |
| 24 | Drobonso Carbon | Nordic Carbon Partners | Biochar Production and Storage | BICRS | GHA | Under validation | 0.00 |  |  |  | 2 | 11 May 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K9W3ZCY71S0NRMS |
| 25 | EcoFix Kenya | Terraton | Biochar Production and Storage | BICRS | KEN | Under validation | 0.00 |  |  |  | 2 | 14 Jul 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K4XA2FF31S0T7V9 |
| 26 | Enable Earth, Chiang Rai | Enable Earth | Biochar Production and Storage | BICRS | THA | Canceled | 0.00 |  |  |  | 1 | 20 Apr 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KBECJX991S0EDE4 |
| 27 | ERW Deployment: Seoni & North Chhattisgarh, India | Mati | Enhanced Weathering in Agriculture | EW | IND | Validated | 492.4 | 100 | 2 | 17 Jun 2026 | 5 | 17 Jun 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JKR5RQG81S0Y2CZ |
| 28 | Great Plains Organic Waste Sequestration | Vaulted Deep | Biomass Geological Storage | BICRS | USA | Validated | 70,234.61 | 16,523.692 | 252 | 31 Aug 2026 | 60 | 31 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1HHYZFVGW1S044ZY |
| 29 | Green Carbon - Kapadvanj Industrial Biochar | Green Carbon | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 11 May 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KCNW12WM1S0AY3D |
| 30 | Green Carbon - Nagpur Industrial Biochar (1 & 2) | Green Carbon | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 08 Jun 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KHT9B45F1S0HY3H |
| 31 | Hampton Roads WAE Project | CREW Carbon | Wastewater Alkalinity Enhancement | MARINE | USA | Validated | 49.53 | 0 | 1 | 18 Dec 2025 | 4 | 18 Dec 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1K3S0527T1S0KYXT |
| 32 | Helix | Planeteers | Biogenic Carbon Capture and Storage | BICRS | DEU | Validated | 0.00 |  |  |  | 4 | 28 Jan 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K4SN1CT61S0NZ7N |
| 33 | Humboldt Sawmill Company (HSC) | Pacific Biochar | Biochar Production and Storage | BICRS | USA | Validated | 6,967.97 | 3,199.354 | 8 | 26 Jun 2026 | 12 | 26 May 2026 | 200Y+ | https://registry.isometric.com/project/prj_1JXCRW5ST1S0EEKH |
| 34 | INTERCARBO | Interholco | Biochar Production and Storage | BICRS | COG | Under validation | 0.00 |  |  |  | 2 | 11 Aug 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JVC6T3VR1S0AJ5P |
| 35 | Kalinga Restoration Project | Longstraw Carbon | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 09 Sep 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KNRMXT1M1S0XG77 |
| 36 | KARBOTECH one | agriCARBON | Biochar Production and Storage | BICRS | CZE | Under validation | 0.00 |  |  |  | 2 | 23 Jan 2026 | 200Y+ | https://registry.isometric.com/project/prj_1JPMVNV6K1S0WWRZ |
| 37 | KFL - atmosfair Mafia Island biochar | Kisiwa Farming | Biochar Production and Storage | BICRS | TZA | Under validation | 0.00 |  |  |  | 2 | 26 May 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KA8WSNN61S09FHS |
| 38 | Kvina River CDR Project | CarbonRun | River Alkalinity Enhancement | MARINE | NOR | Validated | 76.69 | 23.002 | 1 | 20 Jan 2026 | 4 | 20 Jan 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K39D0N8S1S0TMKX |
| 39 | La Perla | Silica | Enhanced Weathering in Agriculture | EW | MEX | Validated | 322.54 | 0 | 1 | 24 Aug 2026 | 4 | 24 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K3MGXD4A1S0S3H8 |
| 40 | Landscape Legacy: Ecological Restoration in the Brazilian Amazon | re.green | Reforestation | BIOSPHERE | BRA | Under validation | 0.00 |  |  |  | 1 | 28 May 2026 | 60Y+ | https://registry.isometric.com/project/prj_1KNSEH7NT1S052MH |
| 41 | Loblolly Project | Graphyte | Subsurface Biomass Carbon Removal and Storage | BICRS | USA | Validated | 20,444.62 | 13,237.05 | 12 | 08 Jul 2026 | 22 | 08 Jul 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1J4P33N6W1S0RKE2 |
| 42 | Miombo Renewal | Carbon Ventures Africa | Reforestation | BIOSPHERE | COD | Under validation | 0.00 |  |  |  | 3 | 08 Mar 2026 | 40Y+ | https://registry.isometric.com/project/prj_1K9A90ZPH1S0ZJ9S |
| 43 | MobiChar x GA | Alcom Carbon Markets | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 1 | 01 Jul 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KCEM5PTM1S0MK7X |
| 44 | Morobe Markham Reforestation | Morobe Markham Reforestation | Reforestation | BIOSPHERE | PNG | Under validation | 0.00 |  |  |  | 1 | 22 Jun 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K7F70BKD1S04GWB |
| 45 | Moser River | CarbonRun | River Alkalinity Enhancement | MARINE | CAN | Under validation | 0.00 |  |  |  | 2 | 15 Sep 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1K09XZV1B1S023XT |
| 46 | Murudagiri Biochar Project | Equilibrium | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 25 Jun 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KQSRWYTB1S0R69E |
| 47 | MVC Biochar | Carbono Capital | Biochar Production and Storage | BICRS | CHL | Under validation | 0.00 |  |  |  | 2 | 03 Sep 2025 | 200Y+ | https://registry.isometric.com/project/prj_1K1T6SHXE1S0F3H4 |
| 48 | New England WAE Project | CREW Carbon | Wastewater Alkalinity Enhancement | MARINE | USA | Validated | 1,374.73 | 280 | 8 | 24 Aug 2026 | 16 | 24 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JFA3YY9P1S0YVKR |
| 49 | Northern Uganda Mini Grid and Carbon Removal Project | Mandulis Energy | Biochar Production and Storage | BICRS | UGA | Under validation | 0.00 |  |  |  | 1 | 11 Sep 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KWZ35D2D1S02X0A |
| 50 | Nova Scotia Mineral OAE Project | Planetary | Ocean Alkalinity Enhancement from Coastal Outfalls | MARINE | CAN | Validated | 4,853.6 | 2,059 | 4 | 30 Mar 2026 | 16 | 31 Mar 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1H502CZZH1S0VMYW |
| 51 | Ontario Avenue Bio-Oil Sequestration | NULIFE GreenTech | Bio-oil Geological Storage | BICRS | CAN | Validated | 1,404.08 | 329.619 | 8 | 26 Aug 2026 | 18 | 26 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JQEQKCF91S06HAJ |
| 52 | Patagonia WoodCell I | Patagonia Green | Subsurface Biomass Carbon Removal and Storage | BICRS | CHL | Under validation | 0.00 |  |  |  | 2 | 10 Sep 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KVN4NCR11S0HD23 |
| 53 | Project Agneerath | Earthrevive Technologies | Biochar Production and Storage | BICRS | IND | Validated | 5.6 | 0 | 1 | 17 May 2026 | 5 | 17 May 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KC8T0EGS1S0H36R |
| 54 | Project AgniChar | Sarva Foam | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 05 Sep 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KQC94VAH1S0MWXR |
| 55 | Project Araçari | InPlanet | Enhanced Weathering in Agriculture | EW | BRA | Validated | 319.97 | 0 | 1 | 04 Nov 2025 | 4 | 04 Nov 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JQ775W7D1S0WYSA |
| 56 | Project Bhumisara | Earthrevive Technologies | Biochar Production and Storage | BICRS | IND | Validated | 2,089.21 | 0 | 1 | 28 Aug 2026 | 4 | 28 Aug 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KRAVH8Y81S0WQ8Z |
| 57 | Project Cajueiro | Mombak | Enhanced Weathering in Agriculture | EW | BRA | Validated | 46.94 | 46 | 1 | 01 Apr 2026 | 4 | 01 Apr 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JZ0ZD3JN1S0SHW9 |
| 58 | Project Carcará | Terradot | Enhanced Weathering in Agriculture | EW | BRA | Validated | 204.95 | 44.3 | 1 | 17 Mar 2026 | 5 | 17 Mar 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K10D531D1S0DEV9 |
| 59 | Project Dourado | InPlanet | Enhanced Weathering in Agriculture | EW | BRA | Validated | 0.00 |  |  |  | 3 | 01 Apr 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K21RKWYX1S0NWN6 |
| 60 | Project Earthstone | Anglo American | Enhanced Weathering in Agriculture | EW | BRA | Under validation | 0.00 |  |  |  | 2 | 24 May 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K8BE4BSR1S06DWN |
| 61 | Project Juniper | Clairity | Direct Air Capture | DAC | USA | Canceled | 0.00 |  |  |  | 2 | 25 May 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JQCK4WZX1S0ANXP |
| 62 | Project Kalki - Facility 1 | Earthrevive Technologies | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 1 | 01 Sep 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1KXZV12FG1S0M4XP |
| 63 | Project Nandani | Ground Up | Biochar Production and Storage | BICRS | IND | Validated | 4.97 | 0 | 1 | 17 Apr 2026 | 4 | 17 Apr 2026 | 200Y+ | https://registry.isometric.com/project/prj_1JWX91R5E1S00PN0 |
| 64 | Project Serra da Mantiqueira | InPlanet | Enhanced Weathering in Agriculture | EW | BRA | Validated | 389.42 | 81.025 | 2 | 18 Mar 2026 | 6 | 18 Mar 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1J7NQMR9V1S04P0D |
| 65 | Project Tapir | Gigafex | Biochar Production and Storage | BICRS | CRI | Under validation | 0.00 |  |  |  | 2 | 09 Mar 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K1GX4BDK1S0FZVC |
| 66 | Reforesting Degraded Appalachian Mine and Agricultural Lands | Living Carbon | Reforestation | BIOSPHERE | USA | Under validation | 0.00 |  |  |  | 1 | 08 Sep 2026 | 40Y+ | https://registry.isometric.com/project/prj_1JQ76PQZX1S04S93 |
| 67 | Reforesting the Brazilian Amazon Project 1 | Mombak | Reforestation | BIOSPHERE | BRA | Validated | 21,771.53 | 0 | 3 | 01 Jul 2026 | 4 | 01 Jul 2026 | 100Y+ | https://registry.isometric.com/project/prj_1KA95092G1S093EM |
| 68 | Sifuri Halisi TZ001-B | Dark Earth Carbon | Biochar Production and Storage | BICRS | TZA | Under validation | 0.00 |  |  |  | 2 | 23 Apr 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K6G4S1PJ1S0TR4Z |
| 69 | TIRE Project | Vaulted Deep | Biomass Geological Storage | BICRS | USA | Validated | 2,774.85 | 0 | 2 | 01 Sep 2026 | 6 | 01 Sep 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1K7HK8Q4S1S0D4W4 |
| 70 | Treehouse Plant 1 | Sitos Group | Biochar Production and Storage | BICRS | USA | Under validation | 0.00 |  |  |  | 2 | 21 Sep 2025 | 200Y+ | https://registry.isometric.com/project/prj_1JQEW95GA1S0D2FD |
| 71 | Tupande | Terraton | Biochar Production and Storage | BICRS | KEN | Under validation | 0.00 |  |  |  | 2 | 24 Jul 2026 | 200Y+ | https://registry.isometric.com/project/prj_1KRHHE8G71S0VYD8 |
| 72 | U.S. Agroforestry & Reforestation using Long-term Leases | Propagate | Reforestation | BIOSPHERE | USA | Under validation | 0.00 |  |  |  | 2 | 23 Jul 2025 | 60Y+ | https://registry.isometric.com/project/prj_1JYDZZ4MS1S0MF77 |
| 73 | US Southeast Enhanced Weathering Project | Lithos | Enhanced Weathering in Agriculture | EW | USA | Validated | 12,332.95 | 1,397.302 | 4 | 18 Aug 2026 | 8 | 18 Aug 2026 | 1,000Y+ | https://registry.isometric.com/project/prj_1JY1YXDBS1S01Y05 |
| 74 | Varhad Industrial Cotton Stalk Biochar Project | Varhad | Biochar Production and Storage | BICRS | IND | Under validation | 0.00 |  |  |  | 2 | 08 Aug 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JYGSV7SE1S03PH9 |
| 75 | ZX-24 Vulkaneifel | ZeroEx | Enhanced Weathering in Agriculture | EW | DEU | Validated | 0.00 |  |  |  | 3 | 28 Mar 2025 | 1,000Y+ | https://registry.isometric.com/project/prj_1JMAPP8SA1S0BQAJ |

Pathway labels used by the registry and how many projects carry each (from the `Protocol` column): `Biochar Production and Storage` 39; `Enhanced Weathering in Agriculture` 13; `Reforestation` 6; `Subsurface Biomass Carbon Removal and Storage` 3; `Biogenic Carbon Capture and Storage` 2; `Bio-oil Geological Storage` 2; `Direct Air Capture` 2; `Biomass Geological Storage` 2; `Wastewater Alkalinity Enhancement` 2; `River Alkalinity Enhancement` 2; `Rice Methane Reduction` 1; `Ocean Alkalinity Enhancement from Coastal Outfalls` 1.

## Geological-storage pathway family

The registry uses two separate pathway labels for this family, quoted exactly as shown in the list cards and the `Protocol` column: **`Bio-oil Geological Storage`** (2 projects) and **`Biomass Geological Storage`** (2 projects). Both sit under the page badge `BICRS`. Adjacent but differently labelled pathways that were NOT counted in the family: `Subsurface Biomass Carbon Removal and Storage` (Graphyte Loblolly, Rewind DMS Georgia, Patagonia WoodCell I) and `Biogenic Carbon Capture and Storage` (Bigadan, Helix).

### Charm Bio-oil Geologic Storage — Charm Industrial — `Bio-oil Geological Storage`

- Project page: https://registry.isometric.com/project/prj_1HZSSWBQM1S08H83
- Status `Validated`; `Certificates issued` 8,426.77; `Retired` 5,105.13; `Buffer pool` 315.808; Crediting period `01 Mar 2024 to 28 Feb 2029`; Approval date `20 Aug 2024`; Project code `7BDE`; Verifier `350Solutions`; Location code `USA`; Durability `1,000Y+`.
- Protocol versions shown: `Bio-oil Geological Storage v1.2` (https://registry.isometric.com/protocol/bio-oil-geological-storage/1.2); `Bio-oil Geological Storage v1.0` (https://registry.isometric.com/protocol/bio-oil-geological-storage/1.0)
- Registry summary text: "Charm produces bio-oil, a carbon rich liquid made from unmerchantable wildfire prevention residues in Colorado and procures bio-oil produced by third parties, made from forest products processing residuals. A combination of rail and truck is used to transport bio-oil to injection well sites that are converted oil assets. Permanent sequestration will occur in multiple locations, such as Kansas and Louisiana."
- Project Design Document (PDD) link (the `Project Design Document` card under Removal method): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KAERQ5A11S081G0/pdd.pdf
- Public calculation view (the `See GHG entry →` link in the Calculation overview section): https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=calculation-view
  - Caption shown: "Calculations demonstrating 159.49 tCO₂e removed from Charm Bio-oil Geologic Storage on 25 Jul 2026"
  - Figures shown in the overview: Net CO₂e Removed | 159.491 t | Sequestrations | 193.725 t | + | Adjustments | 20.929 tCO₂e | - | Activities | 54.091 tCO₂e | - | Uncertainty Discount | 1.072 t
- Issuance events: 18 (Issuances table `Showing … of 18`); most recent `Issue date` 15 Aug 2026. First page of the Issuances table as read (`Issue date | Issued | Buffer pool | Supplier allocation`): 15 Aug 2026 / 874.29 / 43.716 / 830.574; 17 Jul 2026 / 647.05 / 32.353 / 614.697; 22 Jun 2026 / 425.59 / 21.281 / 404.309; 27 May 2026 / 490.82 / 24.547 / 466.273; 17 Apr 2026 / 612.99 / 30.658 / 582.332; 18 Mar 2026 / 764.14 / 38.216 / 725.924; 24 Feb 2026 / 43.47 / 2.174 / 41.296; 05 Dec 2025 / 454.71 / 22.739 / 431.971; 02 Nov 2025 / 291.85 / 14.594 / 277.256; 09 Oct 2025 / 166.4 / 8.324 / 158.076
- Feedstocks table (`Name | Category | Validated`): Kerry Inc 1-01 / Biomass / 12 Feb 2026 (Showing 1 of 1)
- Reversal risk text: "The risk of reversal for this project has been assessed as low. This means that 5% of certificates issued for this project are allocated to Charm Industrial's buffer pool. To date, this project has contributed 315.808 certificates to the buffer pool which holds a total of 317.85 certificates. Charm Industrial has no reversals to date."
- **Public documents exposed on the project page: 40** (matches `Showing … of 40`; every page of the table was read). Full list (`Submission date | Title | Download`):

| Submission date | Title | Download URL |
|---|---|---|
| 15 Aug 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1M02YD83Z1S0J5PN/verification_report.pdf |
| 15 Aug 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1M02YCEEP1S0AVZB/ghg_statement_report.pdf |
| 17 Jul 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KXRNS8G91S0SSQB/verification_report.pdf |
| 17 Jul 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KXRNRYWZ1S0JG01/ghg_statement_report.pdf |
| 22 Jun 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KVQC8PD81S08MGG/verification_report.pdf |
| 22 Jun 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KVQC8D0B1S01AS6/ghg_statement_report.pdf |
| 27 May 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KSN371CW1S0T22P/verification_report.pdf |
| 27 May 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KSN36JMH1S06D71/ghg_statement_report.pdf |
| 17 Apr 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KPDXAEH71S0A9VB/verification_report.pdf |
| 17 Apr 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KPDXA3401S0PMZP/ghg_statement_report.pdf |
| 18 Mar 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KM0TBCWP1S05701/verification_report.pdf |
| 18 Mar 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KM0TAY1Q1S0HJ4C/ghg_statement_report.pdf |
| 24 Feb 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KJ7FNC8K1S080WT/verification_report.pdf |
| 24 Feb 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KJ7FMPR71S0MC15/ghg_statement_report.pdf |
| 05 Dec 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KBQVZ3401S0QYJP/verification_report.pdf |
| 05 Dec 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KBQVXRYM1S049Q1/ghg_statement_report.pdf |
| 10 Nov 2025 | Name Change Confirmation | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KBPZDQ501S00QEN/name_change_confirmation.pdf |
| 02 Nov 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K954MG821S08X3H/verification_report.pdf |
| 02 Nov 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K932MWVR1S0DJV9/ghg_statement_report.pdf |
| 09 Oct 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K754XTWF1S0E7XG/verification_report.pdf |
| 09 Oct 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K754X6XY1S0TK1V/ghg_statement_report.pdf |
| 24 Sep 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K5XPY1641S0E8WM/ghg_statement_report.pdf |
| 24 Sep 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K5XPX61T1S0TM0Z/verification_report.pdf |
| 03 Sep 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K5XPWF8W1S06Z5A/ghg_statement_report.pdf |
| 03 Sep 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K4B0GBQK1S0CY1S/verification_report.pdf |
| 04 Jul 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JZB23HYC1S05270/ghg_statement_report.pdf |
| 04 Jul 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JZB2326B1S0HDBB/verification_report.pdf |
| 06 Jun 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JX26FRZY1S0NKWF/ghg_statement_report.pdf |
| 06 Jun 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JX26EDE81S01Z0T/verification_report.pdf |
| 17 Apr 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JS1XGMYG1S0F650/ghg_statement_report.pdf |
| 17 Apr 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JS1XCTS11S0VH9B/verification_report.pdf |
| 20 Feb 2025 | PDD | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KAERQ5A11S081G0/pdd.pdf |
| 20 Feb 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JMMPK1VE1S0MD3M/verification_report.pdf |
| 20 Feb 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1JMKXT4ED1S0Q66C/ghg_statement.pdf |
| 21 Jan 2025 | Unsuccessful Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1KBCN7QYB1S01YQ5/unsuccessful_verification_report.pdf |
| 18 Oct 2024 | No Public Comment Period | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K5EFE6HW1S0YZBB/no_public_comment_period.pdf |
| 18 Oct 2024 | Charm Validation Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1K1V3H4Q71S08NF8/charm_validation_report.pdf |
| 26 Jul 2024 | Charm Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1J41VNE1Q1S00M5G/charm_verification_report_2024-07-26.pdf |
| 25 Jun 2024 | Charm Validation Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1J41VMWBR1S0CZ9V/charm_validation_report_2024-06-25.pdf |
| 21 Jun 2024 | Charm GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H31MW3T81S0R67B/prj_1HZSSWBQM1S08H83/pjd_1J41SZMF81S05NJH/charm_ghg_statement_report_2024-06-21.pdf |

### Great Plains Organic Waste Sequestration — Vaulted Deep — `Biomass Geological Storage`

- Project page: https://registry.isometric.com/project/prj_1HHYZFVGW1S044ZY
- Status `Validated`; `Certificates issued` 70,234.61; `Retired` 16,523.692; `Buffer pool` 1,409.081; Crediting period `21 Aug 2023 to 20 Aug 2028`; Approval date `22 Dec 2023`; Project code `01P4`; Verifier `350Solutions`; Location code `USA`; Durability `1,000Y+`.
- Protocol versions shown: `Biomass Geological Storage v1.1` (https://registry.isometric.com/protocol/biomass-geological-storage/1.1); `Biomass Geological Storage v1.0` (https://registry.isometric.com/protocol/biomass-geological-storage/1.0)
- Registry summary text: "Vaulted deploys slurry injection technology to geologically sequester organic wastes for the purpose of permanent carbon removal. Vaulted owns and operates a built and permitted injection well site in Hutchinson, Kansas. This site hosts a network of 60 salt caverns, with the total capacity to hold 2-3 million metric tons of organic waste and room to expand beyond that. Vaulted secures a range of organic wastes (including biosolids, livestock and agricultural waste, paper sludge, and others) through sustainable sourcing practices from the surrounding area. Vaulted then minimally processes the waste on-site and geologically injects them, permanently (10,000+ years) sequestering the carbon."
- Project Design Document (PDD) link (the `Project Design Document` card under Removal method): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K5FAGRQ41S0P42Y/pdd.pdf
- Public calculation view (the `See GHG entry →` link in the Calculation overview section): https://registry.isometric.com/ghg-entry/rmv_1M0ACG4FJ1S02V0A?tab=calculation-view
  - Caption shown: "Calculations demonstrating 5.91 tCO₂e removed from Great Plains Organic Waste Sequestration on 10 Aug 2026"
  - Figures shown in the overview: Net CO₂e Removed | 5.908 tCO₂e | Sequestrations | 6.621 tCO₂e | - | Activities | 384 kgCO₂e | + | Counterfactuals | 329 kgCO₂e
- Issuance events: 252 (Issuances table `Showing … of 252`); most recent `Issue date` 31 Aug 2026. First page of the Issuances table as read (`Issue date | Issued | Buffer pool | Supplier allocation`): 31 Aug 2026 / 3,610.88 / 72.454 / 3,538.426; 31 Jul 2026 / 2,571.84 / 51.59 / 2,520.25; 30 Jun 2026 / 4,968.77 / 99.626 / 4,869.144; 29 May 2026 / 4,223.87 / 84.698 / 4,139.172; 29 Apr 2026 / 5,419.4 / 108.637 / 5,310.763; 10 Apr 2026 / 5,024.4 / 100.777 / 4,923.623; 27 Feb 2026 / 4,466.84 / 89.602 / 4,377.238; 31 Jan 2026 / 1,374.32 / 27.551 / 1,346.769; 31 Jan 2026 / 1,932.92 / 38.749 / 1,894.171; 19 Dec 2025 / 4,534.37 / 90.923 / 4,443.447
- Feedstocks table (`Name | Category | Validated`): Clark County Feeders / Biomass / 29 May 2026; City of Winfield_Biosolids / Biomass / 11 Feb 2026; City of Goddard_Biosolids / Biomass / 11 Feb 2026; Buffalo Feeders / Biomass / 17 Oct 2025; Tiffany Cattle Co-Herrington_Old Manure / Biomass / 30 Sep 2025 (Showing 5 of 21)
- Reversal risk text: "The risk of reversal for this project has been assessed as very low. This means that 2% of certificates issued for this project are allocated to Vaulted Deep's buffer pool. To date, this project has contributed 1,409.081 certificates to the buffer pool which holds a total of 1,465.017 certificates. Vaulted Deep has no reversals to date."
- **Public documents exposed on the project page: 60** (matches `Showing … of 60`; every page of the table was read). Full list (`Submission date | Title | Download`):

| Submission date | Title | Download URL |
|---|---|---|
| 31 Aug 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1M1BN9TN61S0P7T2/verification_report.pdf |
| 31 Aug 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1M1BN9E5B1S0EY2R/ghg_statement_report.pdf |
| 31 Jul 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KYWFXC5D1S0AE73/verification_report.pdf |
| 31 Jul 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KYWFX0J21S034FS/ghg_statement_report.pdf |
| 30 Jun 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KWCE7X9A1S0QB7A/verification_report.pdf |
| 30 Jun 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KWCE7K1G1S0G1G0/ghg_statement_report.pdf |
| 28 May 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KSSZZ5K91S0DM43/verification_report.pdf |
| 28 May 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KSSZYQ701S0SZ8E/ghg_statement_report.pdf |
| 29 Apr 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KQCP0J241S0W8G4/verification_report.pdf |
| 29 Apr 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KQCP04ZK1S06BA6/ghg_statement_report.pdf |
| 10 Apr 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KNWQF1AZ1S0YHT8/verification_report.pdf |
| 10 Apr 2026 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KNWQDSD01S0Q82Y/ghg_statement.pdf |
| 27 Feb 2026 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KJFW1QEQ1S0K8E9/ghg_statement.pdf |
| 27 Feb 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KJFVZTA61S0F8J6/verification_report.pdf |
| 31 Jan 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KG9R07DG1S0P8VG/verification_report.pdf |
| 31 Jan 2026 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KG9QZQZ01S02KZV/ghg_statement.pdf |
| 19 Dec 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KCW8Z3QV1S0JCZT/verification_report.pdf |
| 19 Dec 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KCW8YAWC1S0QECV/ghg_statement.pdf |
| 28 Nov 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KB5FSPTR1S0J2YJ/verification_report.pdf |
| 28 Nov 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1KB5FS5CB1S0YE2X/ghg_statement.pdf |
| 30 Oct 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K8TJGW8N1S00ABN/verification_report.pdf |
| 30 Oct 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K8TJG33J1S0CNG0/ghg_statement.pdf |
| 29 Sep 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K6BC05QE1S0ADJD/verification_report.pdf |
| 18 Sep 2025 | PDD | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K5FAGRQ41S0P42Y/pdd.pdf |
| 29 Aug 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K3V98DKN1S0A0J4/ghg_statement.pdf |
| 29 Aug 2025 | Biannual Validation and Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K3V96HD01S0PBPF/biannual_validation_and_verification_report.pdf |
| 31 Jul 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K1GRHC571S0830Y/verification_report.pdf |
| 31 Jul 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K1GRG7D61S0ME59/ghg_statement.pdf |
| 30 Jun 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JZ1BQ2CB1S0GMWA/verification_report.pdf |
| 30 Jun 2025 | GHG Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JZ1BF9S61S09B50/ghg_statement.docx |
| 30 May 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JWH1C6P31S04NN9/verification_report.pdf |
| 30 May 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JWH1AV5Q1S0H0SM/ghg_statement_report.pages |
| 06 May 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JTJABDZH1S0B512/ghg_statement_report.docx |
| 06 May 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JTJAA4B71S0QG5D/verification_report.pdf |
| 01 Apr 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JQRX9EY81S07EGM/ghg_statement_report.docx |
| 01 Apr 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JQRX83CX1S0KSMZ/verification_report.pdf |
| 28 Feb 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JN614F2Q1S0SDHD/verification_report.pdf |
| 28 Feb 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JN613JCF1S05RNR/ghg_statement_report.pdf |
| 30 Jan 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JKV19ARC1S0R62T/verification_report.pdf |
| 30 Jan 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JJWB89YE1S0PQBX/ghg_statement_report.pdf |
| 27 Dec 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JG6F1SP11S0EV2K/verification_report.pdf |
| 27 Dec 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JG6EW2SJ1S0V66Y/ghg_statement_report.pdf |
| 16 Dec 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JF7ECW501S0YMZY/ghg_statement_report.pdf |
| 16 Dec 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JF7EBXV31S0B049/verification_report.pdf |
| 02 Dec 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JE4AA6FJ1S0ECSG/ghg_statement_report.pdf |
| 29 Nov 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JE49NR2R1S0ST9X/verification_report.pdf |
| 28 Oct 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JBA0ZNTV1S0HJCQ/verification_report.pdf |
| 28 Oct 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1JBA0V85E1S0XXH2/ghg_statement_report.pdf |
| 01 Oct 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1J9C3GVXH1S0B5GZ/2024-10-01_verification_report.pdf |
| 01 Oct 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1J9C391V81S03VSN/2024-10-01_ghg_statement_report.pdf |
| 29 Aug 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1J6FQY7RC1S0F6W2/2024-08-29_ghg_statement_report.pdf |
| 29 Aug 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1J6FPPK911S0M893/2024-08-29_verification_report.pdf |
| 12 Aug 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1J531MFXS1S0T6CH/2024-08-12_verification_report.pdf |
| 12 Jul 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1J2KH9C5J1S0K413/2024-07-12_verification_report.pdf |
| 09 Apr 2024 | Verification Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1HV41T48T1S0BCNE/2024-04-09_verification_statement.pdf |
| 09 Apr 2024 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1HV41GXTC1S042Y4/2024-04-09_verification_report.pdf |
| 09 Apr 2024 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1HV2CB2501S0E5R6/2024-04-09_ghg_statement_report.pdf |
| 22 Dec 2023 | No Public Comment Period | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1K5EFFAV21S0692N/no_public_comment_period.pdf |
| 22 Dec 2023 | Validation and Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1HJ9EJ2K91S0MYZM/validation_and_verification_report_2023-12-22.pdf |
| 22 Dec 2023 | Validation and Verification Statement | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1HHYZFVGW1S044ZY/pjd_1HJ9EH83D1S01A3Z/validation_and_verification_statement_2023-12-22.pdf |

### Ontario Avenue Bio-Oil Sequestration — NULIFE GreenTech — `Bio-oil Geological Storage`

- Project page: https://registry.isometric.com/project/prj_1JQEQKCF91S06HAJ
- Status `Validated`; `Certificates issued` 1,404.08; `Retired` 329.619; `Buffer pool` 14.052; Crediting period `01 Jun 2025 to 01 Jun 2035`; Approval date `30 Sep 2025`; Project code `GHYZ`; Verifier `Normec Verifavia`; Location code `CAN`; Durability `1,000Y+`.
- Protocol versions shown: `Bio-oil Geological Storage v1.2` (https://registry.isometric.com/protocol/bio-oil-geological-storage/1.2); `Bio-oil Geological Storage v1.1` (https://registry.isometric.com/protocol/bio-oil-geological-storage/1.1)
- Registry summary text: "NULIFE GreenTech utilizes patented Hydrothermal Liquefaction (HTL) technology to convert waste biomass into carbon dense bio-oil. The Ontario Avenue project is in Saskatoon, SK, Canada. The Project utilizes wet and dry waste biomass from local food processing facilities. The bio-oil is transported to a third-party injection site for sequestration into a Canadian underground salt cavern. This project is the first commercial deployment of NULIFE’s modular and rapidly deployable HTL technology. The Ontario Avenue site will act as a showcase facility to validate unmatched biomass feedstock flexibility and versatile output capabilities for a range of high-value co-products."
- Project Design Document (PDD) link (the `Project Design Document` card under Removal method): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1K6DV5H3Z1S069JC/pdd.pdf
- Public calculation view (the `See GHG entry →` link in the Calculation overview section): https://registry.isometric.com/ghg-entry/rmv_1M0B59RM61S0BW9G?tab=calculation-view
  - Caption shown: "Calculations demonstrating 45.83 tCO₂e removed from Ontario Avenue Bio-Oil Sequestration on 22 Jul 2026"
  - Figures shown in the overview: Net CO₂e Removed | 45.835 t | Sequestrations | 47.591 t | - | Activities | 1.709 tCO₂e | + | Counterfactuals | 1 kgCO₂e | - | Uncertainty Discount | 45 kg
- Issuance events: 8 (Issuances table `Showing … of 8`); most recent `Issue date` 26 Aug 2026. First page of the Issuances table as read (`Issue date | Issued | Buffer pool | Supplier allocation`): 26 Aug 2026 / 150.45 / 1.507 / 148.943; 27 Jul 2026 / 205.43 / 2.056 / 203.374; 18 Jun 2026 / 125.04 / 2.502 / 122.538; 19 May 2026 / 296.87 / 5.94 / 290.93; 20 Mar 2026 / 271.86 / 5.439 / 266.421; 29 Dec 2025 / 58.54 / 1.171 / 57.369; 26 Nov 2025 / 240.19 / 4.805 / 235.385; 30 Sep 2025 / 55.7 / 1.114 / 54.586
- Feedstocks table (`Name | Category | Validated`): Bran Waste / Biomass / 02 Apr 2026; Effluent Sludge / Biomass / 02 Apr 2026; Oat Hulls / Biomass / 02 Apr 2026 (Showing 3 of 3)
- Reversal risk text: "The risk of reversal for this project has been assessed as very low. This means that 1% of certificates issued for this project are allocated to NULIFE GreenTech's buffer pool. To date, this project has contributed 14.052 certificates to the buffer pool which holds a total of 14.052 certificates. NULIFE GreenTech has no reversals to date."
- **Public documents exposed on the project page: 18** (matches `Showing … of 18`; every page of the table was read). Full list (`Submission date | Title | Download`):

| Submission date | Title | Download URL |
|---|---|---|
| 26 Aug 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1M0ZJPF4D1S01HYN/verification_report.pdf |
| 26 Aug 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1M0ZJNP5H1S0JYG1/ghg_statement_report.pdf |
| 27 Jul 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KYJ3FWS31S0QDQJ/verification_report.pdf |
| 27 Jul 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KYJ3CRKG1S0QADN/ghg_statement_report.pdf |
| 18 Jun 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KVDKA95S1S0YP9Z/verification_report.pdf |
| 18 Jun 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KVDK9P9E1S0QCJN/ghg_statement_report.pdf |
| 19 May 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KS0GWC311S0W3TJ/verification_report.pdf |
| 19 May 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KS0GTVRG1S0MT38/ghg_statement_report.pdf |
| 20 Mar 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KM67E0FS1S03F62/verification_report.pdf |
| 20 Mar 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KM67DJCG1S0FTAD/ghg_statement_report.pdf |
| 29 Dec 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KDNK1MWV1S0VMBE/verification_report.pdf |
| 29 Dec 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KDNK0SW21S07ZFS/ghg_statement_report.pdf |
| 26 Nov 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KB0D23981S0N8WQ/ghg_statement_report.pdf |
| 26 Nov 2025 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1KB0CZ52A1S0X3CG/verification_report.pdf |
| 30 Sep 2025 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1K6DW6TCV1S0HK5S/ghg_statement_report.pdf |
| 30 Sep 2025 | Validation & Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1K6DVDDF91S0FVKZ/validation_%26_verification_report.pdf |
| 30 Sep 2025 | PDD | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1K6DV5H3Z1S069JC/pdd.pdf |
| 11 Aug 2025 | Public Comment Summary | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1JPQG0XPF1S01KTD/prj_1JQEQKCF91S06HAJ/pjd_1K2FJMSMD1S0P55S/public_comment_summary.pdf |

### TIRE Project — Vaulted Deep — `Biomass Geological Storage`

- Project page: https://registry.isometric.com/project/prj_1K7HK8Q4S1S0D4W4
- Status `Validated`; `Certificates issued` 2,774.85; `Retired` 0; `Buffer pool` 55.936; Crediting period `03 Jan 2026 to 03 Jan 2031`; Approval date `17 Jun 2026`; Project code `B9B1`; Verifier `350Solutions`; Location code `USA`; Durability `1,000Y+`.
- Protocol versions shown: `Biomass Geological Storage v1.1` (https://registry.isometric.com/protocol/biomass-geological-storage/1.1)
- Registry summary text: "Vaulted deploys slurry injection technology to geologically sequester organic wastes for the purpose of permanent carbon removal. The TIRE facility is a biosolids injection well co-located with the City of LA's Terminal Island wastewater treatment plant. Over the course of its operations over ten years, the site has safely and effectively injected more than 450,000 tons of biosolids. Vaulted has waived fees for waste volumes over the 5-year baseline to enable the city to send additional volumes to the site. Vaulted only credits those volumes over the baseline."
- Project Design Document (PDD) link (the `Project Design Document` card under Removal method): https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVAA1X881S0Q1CZ/pdd.pdf
- Public calculation view (the `See GHG entry →` link in the Calculation overview section): https://registry.isometric.com/ghg-entry/rmv_1KYD9KRCD1S02J7Q?tab=calculation-view
  - Caption shown: "Calculations demonstrating 2.07 tCO₂e removed from TIRE Project on 09 Jul 2026"
  - Figures shown in the overview: Net CO₂e Removed | 2.070 tCO₂e | Sequestrations | 2.217 tCO₂e | - | Activities | 148 kgCO₂e
- Issuance events: 2 (Issuances table `Showing … of 2`); most recent `Issue date` 01 Sep 2026. First page of the Issuances table as read (`Issue date | Issued | Buffer pool | Supplier allocation`): 01 Sep 2026 / 2,347.33 / 47.285 / 2,300.045; 17 Jun 2026 / 427.52 / 8.651 / 418.869
- Feedstocks table (`Name | Category | Validated`): LACity_Biosolids / Biomass / 17 Jun 2026 (Showing 1 of 1)
- Reversal risk text: "The risk of reversal for this project has been assessed as very low. This means that 2% of certificates issued for this project are allocated to Vaulted Deep's buffer pool. To date, this project has contributed 55.936 certificates to the buffer pool which holds a total of 1,465.017 certificates. Vaulted Deep has no reversals to date."
- **Public documents exposed on the project page: 6** (matches `Showing … of 6`; every page of the table was read). Full list (`Submission date | Title | Download`):

| Submission date | Title | Download URL |
|---|---|---|
| 01 Sep 2026 | Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1M1FC57011S0RNY8/verification_report.pdf |
| 01 Sep 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1M1FC4PRQ1S0HC6Y/ghg_statement_report.pdf |
| 17 Jun 2026 | Validation and Verification Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVBSZVB01S0XHP2/validation_and_verification_report.pdf |
| 17 Jun 2026 | GHG Statement Report | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVBBX6RT1S0A41A/ghg_statement_report.pdf |
| 17 Jun 2026 | PDD | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KVAA1X881S0Q1CZ/pdd.pdf |
| 02 Feb 2026 | Public Comment Summary | https://storage.googleapis.com/isometric--production--eu--public-documents/spl_1H43SYY631S0Z8YR/prj_1K7HK8Q4S1S0D4W4/pjd_1KH0V2VKY1S0G3CY/public_comment_summary.pdf |

### Public calculation / removals view — what it shows (not analysed)

Only the Charm entry was opened; the other three entries are linked above and were not opened.

- URL opened: https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=calculation-view — page title `159.49 tCO₂e GHG entry by Charm Industrial — Isometric — Isometric`.
- The page has three tabs: `Removal method`, `Calculation view`, `Datapoints`.
- Header block as read: CERTIFICATES ISSUED | 1,000Y+ | 159.49 tCO₂e removed by Charm Industrial | rmv_1KZBJBN9C1S0M5R5 | GHG ENTRY DETAILS | Supplier | Charm Industrial | Project | Charm Bio-oil Geologic Storage | Tonnes removed | 159.49 tCO₂e | Sequestration date | 19 Jul 2026 to 25 Jul 2026 | Reporting period | 01 Jul 2026 to 31 Jul 2026 | VERIFICATION DETAILS | Verification protocol version | Bio-oil Geological Storage v1.2 | Baseline protocol version | Bio-oil Geological Storage v1.0 | Verifier | 350Solutions
- `Calculation view` shows the same tree as the project page's Calculation overview (`Net CO₂e Removed 159.491 t` = `Sequestrations 193.725 t` + `Adjustments 20.929 tCO₂e` − `Activities 54.091 tCO₂e` − `Uncertainty Discount 1.072 t`), drawn as a zoomable diagram with a `View full screen` control.
- `Datapoints` is a table headed `Datapoints (46)` with columns `Name | Value | Collection method | Sources`. Collection method values seen: `REPORTED` and `DERIVED`. The Sources column lists the file names of the evidence behind each value (for example `2396-R.pdf + 19 more`, `W4 Kerry-AECN SGS COA.pdf + 1 more`, `Standard Emission Factors + Calculations (8).xlsx`, `GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf`); the file names are shown as text, not as download links (no link elements were present other than supplier, project, protocol and verifier links). The first datapoint rows read: `Mass of Injectant (per injection) 134.084 t REPORTED`, `Carbon Content of Bio-oil Injected (per injection) 39.40 % REPORTED`, `Bio-Oil Mass - AECN via Rail 136.377 t REPORTED`, `Carbon Intensity - AECN Pyrolysis Process Emissions (via Rail) 0.10 tCO₂e/t DERIVED`. The full captured text is in `raw/ghg_entry_charm_rmv_1KZBJBN9C1S0M5R5.json`.
- Each project page also exposes, per row of its Project documentation table, a downloadable `GHG Statement Report` PDF and `Verification Report` PDF for every verification round (Charm: 40 documents; Vaulted Great Plains: 60; NULIFE: 18; Vaulted TIRE: 6 — all listed above with direct download URLs).

## How I confirmed completeness

1. The list page header reads `Active projects (75)` and the card list rendered 75 `data-project-id` cards (counted in the page, not scrolled).
2. The Table view (`/projects?view=table`) showed 50 rows on page 1 and 25 rows on page 2 (`/projects?view=table&page=1`); the `Next page` button on page 2 was disabled. 50 + 25 = 75.
3. The Filter panel had no box checked; its Status counts (2 + 39 + 33 + 1) and Pathway counts (48 + 6 + 2 + 13 + 5 + 1) each total 75, and Region counts (11 + 34 + 23 + 6 + 1) also total 75.
4. All 75 project pages (`/project/<id>`) were opened and captured; each page's `Issued` value was checked against the Table view's `Certificates issued` value for the same project and all 75 matched; each page's `Current protocol version` (minus the version number) matched the Table view's `Protocol` label for all 75.
5. For the four geological-storage projects every page of the Project documentation table was read until `Next page` was disabled; the number of rows collected equals the table's `of N` total in each case (40, 18, 60, 6) with no duplicate URLs.
6. Search was not used to find projects; the enumeration relies on the list, the table view and the filter counts agreeing.

Caveat: the `Issuance events` and `Most recent issue` columns come from the first page of each project's Issuances table (sorted newest first) and the table's `of N` count; the later pages of those tables were not read. The `Retired` figure is the project page's own `Retired` total.

## Source List

All read 2026-09-14 via the headless browser (read-only).

- https://registry.isometric.com/projects (card list and Filter panel)
- https://registry.isometric.com/projects?projectId=prj_1HZSSWBQM1S08H83 (Charm card opened in the list, showing the `See more →` link)
- https://registry.isometric.com/projects?view=table
- https://registry.isometric.com/projects?view=table&page=1
- https://registry.isometric.com/project/prj_1K3VWSDS61S0QKV7  — A Biochar Project at Satyapura
- https://registry.isometric.com/project/prj_1JTZ7NRK81S0GA0S  — B10 - Brondal #1
- https://registry.isometric.com/project/prj_1K4PWG5T01S0PWMF  — Bharat Biochar Initiative
- https://registry.isometric.com/project/prj_1KJQ2NM0R1S09256  — Bigadan - BioCCS
- https://registry.isometric.com/project/prj_1K56VP7FE1S0QDSH  — Biochar production using dead areca nut biomass
- https://registry.isometric.com/project/prj_1KP390EAC1S0WTMV  — Bioenergie Frauenfeld
- https://registry.isometric.com/project/prj_1KESD32TS1S0ZHGV  — Burney Forest Power v1.2
- https://registry.isometric.com/project/prj_1JRZWM3BP1S071QG  — Burnsville
- https://registry.isometric.com/project/prj_1JYENJXB71S0CR1B  — Capital Link's Berthoud Facility
- https://registry.isometric.com/project/prj_1JF8BBG921S010M4  — Carboneers & Terrafront High Tech Biochar
- https://registry.isometric.com/project/prj_1KFTFVQTY1S08RE0  — Carboneyes: Udongo
- https://registry.isometric.com/project/prj_1K48633C61S0WY58  — CarbonZero.eco - Williams
- https://registry.isometric.com/project/prj_1KMMPMZJV1S0H2YW  — Chara Mattampally
- https://registry.isometric.com/project/prj_1HZSSWBQM1S08H83  — Charm Bio-oil Geologic Storage
- https://registry.isometric.com/project/prj_1JN6XNWDQ1S0BSN7  — Charm Range & Plains Biochar
- https://registry.isometric.com/project/prj_1KT1H7QB71S0NVJV  — Climate smart rice farming in India
- https://registry.isometric.com/project/prj_1K2YPGE781S0A3Q0  — Cocoa Biochar Carboneers
- https://registry.isometric.com/project/prj_1K051N4HQ1S02170  — Corigin-1: BioChar Q3-25
- https://registry.isometric.com/project/prj_1JCZCRW2S1S06KN0  — Darjeeling Revival Project
- https://registry.isometric.com/project/prj_1JYCV03BW1S0RTE5  — Darjeeling Revival: Alt x MOL
- https://registry.isometric.com/project/prj_1JZJY8NY61S0RH07  — Darjeeling Revival: Monsoon Harvest
- https://registry.isometric.com/project/prj_1HCHT9G2H1S05MYP  — Deep Sky Alpha
- https://registry.isometric.com/project/prj_1KFDNVSDZ1S0QA39  — DMS Georgia
- https://registry.isometric.com/project/prj_1K9W3ZCY71S0NRMS  — Drobonso Carbon
- https://registry.isometric.com/project/prj_1K4XA2FF31S0T7V9  — EcoFix Kenya
- https://registry.isometric.com/project/prj_1KBECJX991S0EDE4  — Enable Earth, Chiang Rai
- https://registry.isometric.com/project/prj_1JKR5RQG81S0Y2CZ  — ERW Deployment: Seoni & North Chhattisgarh, India
- https://registry.isometric.com/project/prj_1HHYZFVGW1S044ZY  — Great Plains Organic Waste Sequestration
- https://registry.isometric.com/project/prj_1KCNW12WM1S0AY3D  — Green Carbon - Kapadvanj Industrial Biochar
- https://registry.isometric.com/project/prj_1KHT9B45F1S0HY3H  — Green Carbon - Nagpur Industrial Biochar (1 & 2)
- https://registry.isometric.com/project/prj_1K3S0527T1S0KYXT  — Hampton Roads WAE Project
- https://registry.isometric.com/project/prj_1K4SN1CT61S0NZ7N  — Helix
- https://registry.isometric.com/project/prj_1JXCRW5ST1S0EEKH  — Humboldt Sawmill Company (HSC)
- https://registry.isometric.com/project/prj_1JVC6T3VR1S0AJ5P  — INTERCARBO
- https://registry.isometric.com/project/prj_1KNRMXT1M1S0XG77  — Kalinga Restoration Project
- https://registry.isometric.com/project/prj_1JPMVNV6K1S0WWRZ  — KARBOTECH one
- https://registry.isometric.com/project/prj_1KA8WSNN61S09FHS  — KFL - atmosfair Mafia Island biochar
- https://registry.isometric.com/project/prj_1K39D0N8S1S0TMKX  — Kvina River CDR Project
- https://registry.isometric.com/project/prj_1K3MGXD4A1S0S3H8  — La Perla
- https://registry.isometric.com/project/prj_1KNSEH7NT1S052MH  — Landscape Legacy: Ecological Restoration in the Brazilian Amazon
- https://registry.isometric.com/project/prj_1J4P33N6W1S0RKE2  — Loblolly Project
- https://registry.isometric.com/project/prj_1K9A90ZPH1S0ZJ9S  — Miombo Renewal
- https://registry.isometric.com/project/prj_1KCEM5PTM1S0MK7X  — MobiChar x GA
- https://registry.isometric.com/project/prj_1K7F70BKD1S04GWB  — Morobe Markham Reforestation
- https://registry.isometric.com/project/prj_1K09XZV1B1S023XT  — Moser River
- https://registry.isometric.com/project/prj_1KQSRWYTB1S0R69E  — Murudagiri Biochar Project
- https://registry.isometric.com/project/prj_1K1T6SHXE1S0F3H4  — MVC Biochar
- https://registry.isometric.com/project/prj_1JFA3YY9P1S0YVKR  — New England WAE Project
- https://registry.isometric.com/project/prj_1KWZ35D2D1S02X0A  — Northern Uganda Mini Grid and Carbon Removal Project
- https://registry.isometric.com/project/prj_1H502CZZH1S0VMYW  — Nova Scotia Mineral OAE Project
- https://registry.isometric.com/project/prj_1JQEQKCF91S06HAJ  — Ontario Avenue Bio-Oil Sequestration
- https://registry.isometric.com/project/prj_1KVN4NCR11S0HD23  — Patagonia WoodCell I
- https://registry.isometric.com/project/prj_1KC8T0EGS1S0H36R  — Project Agneerath
- https://registry.isometric.com/project/prj_1KQC94VAH1S0MWXR  — Project AgniChar
- https://registry.isometric.com/project/prj_1JQ775W7D1S0WYSA  — Project Araçari
- https://registry.isometric.com/project/prj_1KRAVH8Y81S0WQ8Z  — Project Bhumisara
- https://registry.isometric.com/project/prj_1JZ0ZD3JN1S0SHW9  — Project Cajueiro
- https://registry.isometric.com/project/prj_1K10D531D1S0DEV9  — Project Carcará
- https://registry.isometric.com/project/prj_1K21RKWYX1S0NWN6  — Project Dourado
- https://registry.isometric.com/project/prj_1K8BE4BSR1S06DWN  — Project Earthstone
- https://registry.isometric.com/project/prj_1JQCK4WZX1S0ANXP  — Project Juniper
- https://registry.isometric.com/project/prj_1KXZV12FG1S0M4XP  — Project Kalki - Facility 1
- https://registry.isometric.com/project/prj_1JWX91R5E1S00PN0  — Project Nandani
- https://registry.isometric.com/project/prj_1J7NQMR9V1S04P0D  — Project Serra da Mantiqueira
- https://registry.isometric.com/project/prj_1K1GX4BDK1S0FZVC  — Project Tapir
- https://registry.isometric.com/project/prj_1JQ76PQZX1S04S93  — Reforesting Degraded Appalachian Mine and Agricultural Lands
- https://registry.isometric.com/project/prj_1KA95092G1S093EM  — Reforesting the Brazilian Amazon Project 1
- https://registry.isometric.com/project/prj_1K6G4S1PJ1S0TR4Z  — Sifuri Halisi TZ001-B
- https://registry.isometric.com/project/prj_1K7HK8Q4S1S0D4W4  — TIRE Project
- https://registry.isometric.com/project/prj_1JQEW95GA1S0D2FD  — Treehouse Plant 1
- https://registry.isometric.com/project/prj_1KRHHE8G71S0VYD8  — Tupande
- https://registry.isometric.com/project/prj_1JYDZZ4MS1S0MF77  — U.S. Agroforestry & Reforestation using Long-term Leases
- https://registry.isometric.com/project/prj_1JY1YXDBS1S01Y05  — US Southeast Enhanced Weathering Project
- https://registry.isometric.com/project/prj_1JYGSV7SE1S03PH9  — Varhad Industrial Cotton Stalk Biochar Project
- https://registry.isometric.com/project/prj_1JMAPP8SA1S0BQAJ  — ZX-24 Vulkaneifel
- https://registry.isometric.com/ghg-entry/rmv_1KZBJBN9C1S0M5R5?tab=calculation-view — Charm GHG entry (calculation view)
- Documentation-table pages (cursor URLs) read for the four geological-storage projects — recorded in `raw/docs_charm_p3..p8.json`, `raw/docs_nulife_p2..p4.json`, `raw/docs_vaultedgp_p2..p12.json`, `raw/docs_tire_p2.json` (each file stores the exact URL it was read from); Charm page 2 is `raw/docs_charm_p2.jsonl` (read from the cursor URL ending `documents-after=W3siLXByb2plY3RfZG9jdW1lbnQuc3VibWlzc2lvbl9kYXRlIjogIjIwMjYtMDYtMjIifSwgeyItcHJvamVjdF9kb2N1bWVudC5pZCI6ICJwamRfMUtWUUM4UEQ4MVMwOE1HRyJ9XQ==`).
