# Isometric modules read — settling the "not determinable" rows

Prepared 2026-09-16 for Max Lavine. Follows on from `07_synthesis_charm_vs_geological_storage_peers.md` §6–§7. All quotes below are verbatim from the module/standard pages read this session in the headless `playwright-mrv` browser (public pages, no login). Full page text for each is saved under `raw/` as listed in each section. Where I could not find a passage on a topic, I say exactly what I searched.

**Important version-currency finding up front:** the modules that were "not read" in the prior synthesis have moved version since some of the peer documents cited them. The registry's live Modules list (`https://registry.isometric.com/modules`, read this session) no longer shows separate "Transportation Emissions Accounting" or "Embodied Emissions Accounting" modules — those topics are now sections **inside the GHG Accounting Module**. The two peer verification reports that cite "Embodied Emissions Accounting V1.0" and "Transportation Emissions Accounting V1.2" as stand-alone modules were referencing an older module structure; the current, certified module covering both is **GHG Accounting v1.1**.

---

## 1. GHG Accounting Module v1.1

URL: `https://registry.isometric.com/module/ghg-accounting/1.1`, read 2026-09-16. Status on the modules list: "Certified". Full text: `raw/module_ghg_accounting_v1.1_page_text_2026-09-16.txt`.

### Materiality (§5.0)

> "5.0 Materiality — SSRs that are not applicable to the project (i.e, not part of project emissions or leakage), or not relevant to the Reporting Period, may be excluded from the system boundary.
>
> Project Proponents may also exclude SSRs where the total emissions for that SSR, and all excluded SSRs collectively, are expected to be negligible. Negligible SSRs are those which fall below a Materiality threshold based on environmental significance of < 1% of net CO2e removals. The purpose of the Materiality threshold is to save resources being expended on GHG accounting for negligible SSRs, in a manner that is proportional to the principle of scientific rigor and evaluation of uncertainty that underpins the Isometric Standard."

> "Project Proponents must repeat the Materiality Assessment when any of the following occur:" [list follows in the source]

> "is < 1% individually and all excluded SSRs remain <1% collectively. Where the collective total exceeds 1%, the SSRs with the highest Materiality must be reinstated in the system boundary, in descending order, until the sum of SSRs becomes < 1%."

**Version note:** NULIFE's PDD cited "Isometric GHG Accounting (V1) Materiality Assessment (Section 4)". In the current v1.1 text read this session, the identical rule sits at **§5.0**, not §4. The rule itself (< 1% individually, < 1% collectively, reinstate in descending order if exceeded) is unchanged in substance from what NULIFE quoted.

### Emissions Amortization (§7.0) — answers the bio-oil protocol's "Section 7" pointer

> "7.0 Emissions Amortization — Emissions amortization refers to the process of allocating project emissions to removals on a temporal or per product output basis."

> "Project Proponents must declare the amortization approach applied to the Project's Establishment and End-of-Life emissions. Unless set out otherwise in the relevant Protocol, emission amortization may be undertaken:
> Over the anticipated Project lifetime as annual emissions, calculated as the total emissions to be amortized divided by the Project lifetime. Temporal allocations must include the replacement of any equipment or materials if expected component lifetime is shorter than the Project lifetime.
> Per tonne of CO2 sequestered, based on estimated total gross CO2 sequestration over the Project lifetime. This approach enables amortization of emissions for Projects that account for total CO2e removals on a batch basis. Project Proponents selecting this method must choose an amortization rate that, based on projected performance, can reasonably be expected to result in full allocation of all outstanding amortized emissions within the amortization cap."

> "Projects that initially choose to amortize emissions (options 2 or 3) may later elect to deduct the remaining unamortized emissions in full from a subsequent removal verification, thereby transitioning to a one-time deduction approach (option 1). This provides flexibility for projects that wish to simplify reporting or consolidate emissions accounting at a later stage."

> "Project Proponents must not amortize emissions over a period exceeding the amortization cap of 20 years or the anticipated project lifetime, whichever is shorter."

This directly answers register row 6 and open question Q5: **a one-time pass (TIRE's practice) and a fixed per-tonne factor (Great Plains' practice, already used by Charm at Kansas) are both named, protocol-sanctioned options** — option 1 (upfront/one-time, reachable even after starting on 2 or 3) and option 3 (per tonne). This is not "not determinable" any more.

### Embodied Emissions (§4.1) and Transportation Emissions (§4.2) — formerly separate modules, now inside GHG Accounting v1.1

> "4.1 Embodied Emissions — Embodied emissions refer to the life cycle GHG impacts associated with the production of materials, consumables, equipment, buildings and infrastructure related to the Project. Full life cycle emissions from raw materials extraction through to product end-of-life must be considered for all embodied emissions."

> "Where available, embodied emissions calculations must include the following life cycle stages... A1-A3 - Product Stage... A4 - Transport to Project Site... A5 - Construction Stage... C1-C4 - End of Life Stage..."

> "When reporting emissions of materials and products procured, for example, concrete and steel used in construction, Project Proponents must report at a minimum emissions related to modules A1-A3. Emissions related to A4, A5 and C1-C4 may be captured separately by Project Proponents where primary activity data flows for these stages are captured separately."

> "4.2 Transportation Emissions — ... a full cradle-to-grave GHG assessment is required for vehicles and infrastructure produced, constructed, and utilized for the CO2 removal project, in line with Section 4.1."

> "Project must calculate transportation emissions using the highest-ranked method for which data are available: Energy Usage Method... Distance-Based Method: uses the distance traveled, transport mode, and load weight with associated emissions factors (acceptable if data unavailable for (1))."

> Equation 3 (Distance-Based Method) defines "EF_Transportation, j = the weight- and distance-based emission factor for transportation for a specific vehicle type, or infrastructure asset where available, provided in appropriate units e.g. kg CO2e/tonne-km" — with no statement in the text read that this factor may or must include vehicle-manufacture embodied emissions in place of a separate line.

**Row 7 / Q6 verdict:** the module requires "a full cradle-to-grave GHG assessment... for vehicles... in line with Section 4.1" as a distinct requirement from the §4.2 transportation-emissions calculation. The text does not say a combined factor satisfies both; it treats them as two obligations (§4.1 for the vehicle's own lifecycle, §4.2 for the transport emissions of the load carried). **Module requires Charm's heavier practice (separate lines) — quote above; a single "already includes embodied" factor is not stated to be an acceptable substitute.**

### Pre-existing sites / converted assets (Procedure 2, §6.1) — answers part of row 11

> "Procedure 2: Divide the process into sub-processes — Where processes, or aspects of processes, are physically separable and dedicated exclusively to either the CDR product or the co-product, the process may be divided into sub-processes... Where the CDR process is a retrofit o an existing facility that was operational prior to the introduction of the CDR process, the CDR process may be considered a new sub-process of the facility. In this case, only the emissions directly associated with the CDR process should be allocated to it."

> "The CDR process is a retrofit to an existing facility that was operable prior to the introduction of the CDR process. Prior to the retrofit the existing facility must have been operational for purposes other than CDR."

> "Records of existing facility activities dating back three years prior to the CDR Project start date must be provided for infrastructure projects where a planning application was required. For all other projects, records of the existing facility activities dating back one year is required."

This is the rule NULIFE's "Excluded because the site was not built for this project. The site was built in 1970 for industrial use" relies on (Eligibility Criteria 1, "EC1", under Procedure 2). It is a named, certified pathway — **module permits the peer method, conditioned on 1–3 years of pre-existing-operation records**, which would also apply to Charm's Basco 6 conversion of an orphaned well if those records exist.

**Not found in this module:** a mass-based method at "§3.3" — that section number belongs to a different module (Embodied Emissions Accounting no longer exists as a stand-alone certified module; see §2 below for where NULIFE's cited method now sits).

---

## 2. Embodied Emissions — mass-based method (row 11, Q6)

NULIFE's PDD cites "Section 3.3 of the Embodied Emissions Accounting Module" for its mass-based method ("Overall mass of equipment, separated by material type, and material emissions factors", "Attribution factor 0.08%"). I searched the current Modules list (`https://registry.isometric.com/modules`, read this session) for "Embodied Emissions Accounting" — **it is not present as a certified, pending, or public-consultation module**; the 49 modules listed do not include it by that name. I searched the GHG Accounting v1.1 full text for "mass-based," "mass based," and "material type" — no hit beyond the general embodied-emissions text in §4.1 quoted above, which does not name a "mass-based method" or an "attribution factor" formula.

**Verdict: module silent (as currently structured) — searched "Embodied Emissions Accounting," "mass-based," "mass based," "attribution factor," "material type" in GHG Accounting v1.1 full text and in the Modules list; no hit for a stand-alone mass-based-method section.** NULIFE's citation is almost certainly to a prior, now-retired module version (the same "Section 4 vs Section 5" version drift seen in the Materiality citation, §1 above). This is a live open question for Isometric, not a "module requires/permits" answer — the section NULIFE cites appears to have been folded into or superseded by GHG Accounting v1.1's general embodied-emissions rules (§4.1), which state a lifecycle-stage requirement but not a single "mass-based method" formula.

---

## 3. Transportation Emissions Accounting — combined embodied-in-factor question (row 7, Q6)

Same finding as row 6 immediately above: no stand-alone "Transportation Emissions Accounting" module exists on the current Modules list. The content lives in GHG Accounting v1.1 §4.2 (quoted in full in §1). **Verdict: module requires Charm's heavier practice (separate embodied lines) — quote: "a full cradle-to-grave GHG assessment is required for vehicles and infrastructure produced, constructed, and utilized for the CO2 removal project, in line with Section 4.1."** The Distance-Based Method equation's emission factor is defined only as "weight- and distance-based... for a specific vehicle type" with no statement that it may substitute for the §4.1 vehicle-lifecycle assessment.

---

## 4. Energy Use Accounting Module v1.3

URL: `https://registry.isometric.com/module/energy-use-accounting/1.3`, read 2026-09-16. Status: "Certified". Full text: `raw/module_energy_use_accounting_v1.3_page_text_2026-09-16.txt`.

### Electricity metering requirement (§5.6) — answers row 8/9

> "5.6 Measurements - CO2eElectricity, RP — The primary measurement considered in calculation of electricity emissions is: Ei: total amount of electricity used by The Project in hour i.
>
> Measurements must be made using a utility grade power meter, or an independent power meter installed by The Project Proponent, with hourly reporting frequency at minimum. Preference is for meters with an accuracy of better than 2% of reading for total electricity consumption, as reported in units of kWh."

> "5.7 Required Records and Documentation - CO2eElectricity, RP — Electricity usage must be monitored for all operations within the gate at each location of utilization relevant to project operation... Allowable electricity records include, but are not limited to: On-site electricity meter readings... or Independent power meter readings... If other equipment or processes not related to the removal process are included in meter readings or utility bills, electricity usage may be allocated to such processes based on sub-metering data, equipment maximum electricity consumption ratings and operating hours for each sub-system, or by other justifiable allocation methods which must be reviewed and accepted during third party verification."

**Verdict:** the underlying **measurement** must be metered at hourly resolution at minimum ("hourly reporting frequency at minimum") — a period total with no metering behind it is not permitted. But nothing in §5.6–5.7 requires the number **reported to Isometric** to be per-injection rather than a period sum; allocation "to such processes" (i.e., splitting a shared meter across activities) is explicitly permitted "by other justifiable allocation methods which must be reviewed and accepted during third party verification." **Row 9 verdict: module permits the peer/Charm-Basco method (period-level reporting) provided the underlying meter is hourly-capable — quote above.** Charm's Basco practice (one period figure) and Vaulted's per-injection reads (done for Vaulted's own reporting, not Charm's requirement) are both consistent with this text; there is no saving available to Charm here (matches the prior synthesis's "no Charm saving" conclusion for row 9, now grounded in a quote instead of "not determinable").

---

## 5. Biomass Feedstock Accounting Module v1.3

URL: `https://registry.isometric.com/module/biomass-feedstock-accounting/1.3`, read 2026-09-16. **Version-currency note:** the Modules list shows v1.4 as "Under public consultation" (not yet certified); v1.3 is the version Charm's own verifier applies ("Biomass Feedstock Accounting Module v1.3 (Kerry Feedstock)," per the prior synthesis's verifier quote), so v1.3 is the version read in full here. Full text: `raw/module_biomass_feedstock_accounting_v1.3_page_text_2026-09-16.txt`.

### Supplier eligibility re-attestation frequency (row 15)

**Verdict: module silent — searched "revalidat," "affirmation," "attestation," "re-certif," "recertif," "review and," "annually," "every two years," "biennial," "two-year," "2 year," "each supplier," "every supplier," "per supplier" in the full v1.3 text; no hit describing a required re-attestation cadence for supplier eligibility.** The module's eligibility criteria (waste-status tests, market-price tests, baseline feedstock-generation-rate tests) each specify their own evidence windows (e.g. "2 years prior to the Project's first procurement date" for waste/bioenergy-use history), but none of these is a recurring "re-attest every N years" clause matching what Great Plains' verification report describes ("each supplier undergoes a full review and re-evidencing two years after initial certification"). That cadence appears to be a project- or verifier-level practice, not a Biomass Feedstock Accounting Module requirement as currently written. This is a genuine open item for Isometric, not a module-based saving Charm can claim on its own reading of the text.

---

## 6. Biomass or Bio-oil Storage in Salt Caverns Module v1.2

URL: `https://registry.isometric.com/module/salt-cavern-storage/1.2`, read 2026-09-16. Status: "Certified". Full text: `raw/module_salt_cavern_storage_v1.2_page_text_2026-09-16.txt`.

### Minimum monitoring list and cadence (row 14, part 1) — Table A2 Operational Monitoring Requirements

Selected rows, quoted as shown on the page (REQUIREMENT | MEASUREMENT METHOD | BASE FREQUENCY | REQUIRED BY THE PROTOCOL):

> "Emplacement pressure | Wellhead pressure sensors | Continuous | Required"
> "Emplacement rate and volume | Flow meter | Continuous | Required"
> "Injectate stream pH | pH meter | One sample per emplacement batch | Required under certain circumstances [If emplacing biomass slurry]"
> "Injectate stream temperature | Temperature sensor | Daily | Required"
> "Injectate conductivity or other salinity measurement | e.g., conductivity probe or other method | One sample per day | Required"
> "TOC of injectate | e.g., TOC analyzer | One sample per production batch | Required"
> "Analysis of bio-oil constituents | Gas chromatography–mass spectrometry | One sample per injection batch | Required under certain circumstances [If bio-oil is being injected]"
> "Average solids concentration of injectate | Weight of total solids | One sample per production batch | Required"
> "Total acid number (TAN) of bio-oil | Titration (ASTM D664-18e2, ASTM D3339-21, ASTM D974-22) | One sample per injection batch | Required under certain circumstances [If bio-oil is being injected]"
> "Density of injectate | Standard methodology | One sample per injection batch | Required"

**This settles row 14 for the Kansas leg directly: Charm's per-batch TAN and density testing are not "heavier than the module" — they are exactly what Table A2 requires ("Required," not "may be reduced") whenever bio-oil is being injected.** There is no protocol basis for stepping these down; any step-down Charm's own PDD allows ("Frequency may decrease if data shows significant consistency across batches") would need to be squared against this table's "Required" (not conditional-on-consistency) framing — that is a genuine internal question, not one this module text resolves either way from the passage read.

### Gas-alarm investigation requirement (R-GP4, Q7)

> "If gas detection alarms are activated at any monitored well, a 'Triggered Gas Investigation' is initiated (Section 3.1.3.1). The Operator must immediately investigate and identify as expeditiously as possible (or in accordance with permit requirements) the cause of the alarm or shutoff, and report the instance to Isometric. Where a Triggered Gas Investigation (Section 3.1.3.1) is already active, individual alarm events must be logged and reported but do not require a separate investigation unless they indicate a materially different or escalating condition."

**Verdict: module requires investigation of gas-detection alarms by default.** Vaulted's non-investigation of every LEL alarm at the shared Hutchinson site (per the peer verification report quoted in `07_synthesis...md`, "Vaulted is not investigating every gas detection alarm activation") stands against this default rule, and is only permissible because — per the same verification report — "Isometric is exempting Vaulted from the requirement to investigate every gas detection alarm activation" during active injection: i.e., the module's default is stricter than what Vaulted is currently doing, and Vaulted's practice rests on a documented, case-specific Isometric exemption, not a module allowance. Charm's PDD scoring the shared site "Total Risk Score | 0" sits on top of a site where the module's default monitoring obligation is currently being waived for the operator — this is the register's R-GP4 finding, now grounded in the module text rather than only in the peer verification report.

---

## 7. Biomass or Bio-oil Storage in Permeable Reservoirs Module v1.2

URL: `https://registry.isometric.com/module/permeable-reservoirs/1.2`, read 2026-09-16. Status: "Certified". Full text: `raw/module_permeable_reservoirs_v1.2_page_text_2026-09-16.txt`.

### Minimum monitoring list and cadence (row 14, part 2) — Table A.2 Operational Monitoring Requirements

> "Injection pressure | Wellhead pressure sensors | Continuous | Required"
> "Injection rate and volume | Flow meter | Continuous | Required"
> "Injectate stream pH | pH meter | One sample per injection batch | Required under certain circumstances [If a biomass slurry is injected]"
> "Injectate stream temperature | Temperature sensor | Daily | Required"
> "δ13C of C compounds in the injectate stream | e.g., IRMS | As per permit | Required under certain circumstances [If required by permit]"

This module's core operational list mirrors the Salt Caverns module's structure (continuous pressure/rate, daily temperature, per-batch pH) and is consistent with TIRE's PDD-quoted permit table cadence (quarterly fall-off tests etc. sit in a different section of TIRE's own permit, not reproduced verbatim on this page in the passage read).

---

## 8. Isometric Standard v2.1

URL: `https://registry.isometric.com/standard/2.1`, read 2026-09-16. Full text: `raw/module_isometric_standard_v2.1_page_text_2026-09-16.txt`.

### PDD content requirement, incl. monitoring plan (row 5)

> "3.2 Documentation — For a Project to be evaluated for the Isometric Registry, the Project Proponent must document Project characteristics in a Project Design Document (PDD)... The PDD must be consistent with ISO 14064-2:2019, and must include: ... a monitoring plan detailing the elements to be monitored, frequency of monitoring and reporting, including relevant Project activities in each step of the Project cycle, measurement equipment, methods and procedures, details on accuracy and calibration, the clear assignment of responsibilities of parties involved in monitoring and reporting to Isometric, and appropriate measures for quality assurance and quality control; and..."

**This settles the literal text: the monitoring plan is one of the things the PDD "must include."** The Standard's own words do not say a monitoring plan may instead be filed as a wholly separate document outside the PDD. That said, this is squarely why Great Plains' PDD points to a companion file — "Vaulted has submitted a completed monitoring plan alongside this PDD" — and its verifier accepted it ("Acceptable – PPD completed / updated appropriately and submitted," per the prior synthesis). I searched this Standard's full text for "outside the PDD," "separate document," "filed separately," and "alongside" — **no hit** for language explicitly authorizing a stand-alone monitoring-plan filing as equivalent to inclusion. **Verdict: module text requires Charm's heavier practice (monitoring plan inside the PDD) on its face; the peer practice of filing "alongside" is a verifier-accepted convention, not a textual carve-out I can quote from the Standard itself.**

### Project changes — approval vs. notification (Q3, Q7 context)

> "3.2 [operations-change clause] The Project Proponent is responsible for notifying Isometric of any changes to operations that could change the eligibility of their process. Following notification, the project's eligibility must be assessed at the project's next verification."

This is a **notification, not a prior-approval, requirement** — Isometric assesses eligibility at the *next* verification, after the fact. I searched the full Standard text for "revalidat," "amend the PDD," "update the PDD," "PDD update," "version of the PDD," and "resubmi[ssion]" looking for a distinct rule on **restructuring or reposting a PDD document itself** (as opposed to an operational change) — **no hit**. **Verdict: module silent on whether moving content out of the PDD body (e.g., Appendix 6, the monitoring plan) into a companion filing counts as an "operations change" needing only notification, or something requiring prior sign-off; the only general change rule found is the notify-then-assess-at-next-verification clause quoted above.**

---

## Register-row and open-question verdicts (summary table)

| Register row / Q | Topic | Verdict |
|---|---|---|
| Row 2 | Materiality exclusion of small sources | **Module permits — quote:** GHG Accounting v1.1 §5.0, "< 1% individually and all excluded SSRs remain <1% collectively." Same rule NULIFE used; renumbered from the "Section 4" NULIFE cited to §5.0 in the current v1.1. |
| Row 5 | Monitoring plan / calculation workbook filed outside the PDD | **Module requires Charm's heavier practice on its face — quote:** Isometric Standard §3.2, PDD "must include... a monitoring plan." No textual carve-out found for filing it "alongside" instead; peer practice rests on verifier acceptance, not Standard text. |
| Row 6 | Embodied emissions passed once vs. per-tonne factor | **Module permits both — quote:** GHG Accounting v1.1 §7.0, amortization options 1 (one-time), 2 (lifetime), 3 (per-tonne), with the further stated right to convert from 2/3 to option 1 later. Settles Q5. |
| Row 7 | Transport factor with embodied folded in | **Module requires Charm's heavier practice — quote:** GHG Accounting v1.1 §4.2, "a full cradle-to-grave GHG assessment is required for vehicles... in line with Section 4.1" as a requirement distinct from the §4.2 transportation-emissions calculation. |
| Row 9 | Period-level electricity meter reads | **Module permits — quote:** Energy Use Accounting v1.3 §5.6–5.7, "hourly reporting frequency at minimum" for the underlying meter, with allocation of usage "by other justifiable allocation methods" reviewed at verification. No requirement that the reported figure be per-injection. |
| Row 11 | Single embodied method / pre-existing-site exclusion | **Split verdict.** Pre-existing-site exclusion: **module permits — quote:** GHG Accounting v1.1 §6.1 Procedure 2, retrofit-of-existing-facility rule with EC1 (1–3 years of prior-operation records). Mass-based method at "§3.3": **module silent** — that section/module no longer exists under that name; searched "mass-based," "mass based," "attribution factor," "material type," no hit in GHG Accounting v1.1. |
| Row 14 | Storage monitoring left to the operator's permit vs. bespoke PDD plan | **Module requires per-batch testing whenever bio-oil is injected — quote:** Salt Caverns v1.2 Table A2, TAN and density "One sample per injection batch \| Required" (not conditional on consistency). Charm's practice matches the module's default; any step-down Charm's PDD allows is a Charm-internal question, not module-sanctioned relief. |
| R-GP4 | Vaulted's non-investigation of every gas alarm at shared Hutchinson site | **Module requires investigation by default — quote:** Salt Caverns v1.2, "The Operator must immediately investigate... the cause of the alarm." Vaulted's practice rests on a documented Isometric exemption, not a module allowance. |
| Row 15 | Supplier re-attestation frequency (annual vs. two-yearly) | **Module silent** — searched "revalidat," "affirmation," "attestation," "re-certif," "recertif," "annually," "every two years," "biennial," "2 year," "each/every/per supplier"; no recurring re-attestation cadence found in Biomass Feedstock Accounting v1.3. |
| Q4 | Materiality module section/table format | Answered — see row 2. Current section is §5.0, not "Section 4." |
| Q5 | Embodied amortization — one-time vs. per-tonne | Answered — see row 6. Both are certified options. |
| Q6 | Transport/embodied module minimums | Answered — see row 7. Module requires the separate vehicle-lifecycle assessment; combined-factor approach not textually sanctioned. |
| Q7 | Storage module minimums, Kansas leg | Answered — see row 14 and R-GP4. Per-batch TAN/density is the module's default; gas-alarm investigation is required by default, Vaulted's gap rests on an exemption. |

---

## What I could not find, stated plainly

- **Embodied Emissions Accounting Module, §3.3 mass-based method (row 11, second half):** this module no longer appears on the live Modules list (`https://registry.isometric.com/modules`, read this session — 49 modules shown, none named "Embodied Emissions Accounting"). I could not locate the mass-based-method text NULIFE cites anywhere in GHG Accounting v1.1. This needs an Isometric conversation, not further searching by me — the citation trail from NULIFE's PDD (written under an older module structure) to the current certified text is broken.
- **Supplier re-attestation cadence (row 15):** no module text found; see §5 above for the full list of terms searched.
- **Whether a companion monitoring-plan filing satisfies the Standard's "must include" language (row 5):** the Standard's own text does not carve this out; only verifier practice (Great Plains' accepted filing) supports it.
- **Whether restructuring the PDD document itself (moving Appendix 6 out) counts as an "operations change" needing only notification, or something else:** the only change-related rule found in the Standard is the general notify-then-assess-at-next-verification clause; nothing specific to PDD document restructuring.
- I did not open Bio-oil Geological Storage v1.1 (the version applied to AECN and Charm oil per the verifier) — only v1.0 and v1.2 were read, in this session and the prior one. This was out of scope for the eight documents assigned but is worth flagging since v1.1's section numbering was noted as "not determinable" in the prior synthesis and remains so.

## Sources read this session (2026-09-16, headless `playwright-mrv`, read-only)

- GHG Accounting v1.1 — `https://registry.isometric.com/module/ghg-accounting/1.1` — `raw/module_ghg_accounting_v1.1_page_text_2026-09-16.txt`
- Biomass Feedstock Accounting v1.3 — `https://registry.isometric.com/module/biomass-feedstock-accounting/1.3` — `raw/module_biomass_feedstock_accounting_v1.3_page_text_2026-09-16.txt`
- Biomass or Bio-oil Storage in Salt Caverns v1.2 — `https://registry.isometric.com/module/salt-cavern-storage/1.2` — `raw/module_salt_cavern_storage_v1.2_page_text_2026-09-16.txt`
- Biomass or Bio-oil Storage in Permeable Reservoirs v1.2 — `https://registry.isometric.com/module/permeable-reservoirs/1.2` — `raw/module_permeable_reservoirs_v1.2_page_text_2026-09-16.txt`
- Energy Use Accounting v1.3 — `https://registry.isometric.com/module/energy-use-accounting/1.3` — `raw/module_energy_use_accounting_v1.3_page_text_2026-09-16.txt`
- Isometric Standard v2.1 — `https://registry.isometric.com/standard/2.1` — `raw/module_isometric_standard_v2.1_page_text_2026-09-16.txt`
- Registry Modules list (for version/existence checks) — `https://registry.isometric.com/modules`
- Registry Protocols list (for version/existence checks) — `https://registry.isometric.com/protocols`

All pages were rendered web pages, not PDFs — no PDF download link was present on any module or standard page, matching the same pattern noted for the bio-oil protocol pages in the prior session.
