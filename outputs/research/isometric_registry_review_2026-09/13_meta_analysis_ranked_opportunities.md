# What our pathway peers on the Isometric registry do that Charm does not

Prepared 18 September 2026 for Max Lavine and the Charm MRV team. Internal decision document.

**Scope.** "If other projects in our pathway on our registry are doing something, it is likely that we can do it too, as we are all following the same ruleset. How those rules are interpreted and acted upon differs. So the goal is to evaluate other projects in the same pathway on the same registry to see if they are doing things that we are not doing and could benefit from doing. That is the entirety of the scope." Every item below is a peer practice Isometric has validated and a verifier has accepted, which Charm does not currently use.

**Terms.** **PDD** = Project Design Document, the long document a project files once and updates. **SSR** = Source, Sink or Reservoir, one line in a project's emissions boundary. **ISO 17025** = the international standard for the competence of testing laboratories. **BCU** = Book and Claim Unit, a reduction credit Charm applies against certain emissions.

**The peers.** NULIFE GreenTech's Ontario Avenue project is the other bio-oil project on the registry. Vaulted Deep's TIRE project stores in a permeable reservoir, the same storage type as Basco 6, and is Charm's closest direct storage peer. Vaulted Deep's Great Plains project is the largest project in the pathway family.

---

| Item | Peer doing it | What Charm does | Status |
|---|---|---|---|
| Exclude sub-1% source categories from the emissions boundary | NULIFE GreenTech, Ontario Avenue | Calculates every small source line monthly | Available |
| Carbon-content testing at a non-accredited in-house or university lab | NULIFE GreenTech, Ontario Avenue | Sends every sample to an external accredited lab | Needs Isometric — added under the scope statement; strike if not wanted |
| Monitoring plan and calculation methodology filed as companion documents | Vaulted Deep, Great Plains | Carries both inside the PDD | In progress |
| Fixed per-tonne embodied factor for Basco 6, set once | Vaulted Deep, Great Plains | Rebuilds a dated inventory workbook every period | In progress |
| Transport emissions from a carrier-supplied fuel factor | Vaulted Deep, TIRE | Distance-based with a route map per leg | Needs Isometric |

---

## 1. Exclude sub-1% source categories from the emissions boundary

**What the peer does.** NULIFE excludes its smallest emission lines from the boundary under the materiality rule and shows the arithmetic in its own PDD. NULIFE PDD p.49:

> "Sum of SSRs excluded (must be < 1%) | 0.208 | 0.787965616 | still below the 1% threshold"

Eight boundary lines in that table carry the note:

> "They are excluded for regular Removal quantification, as per the materiality assessment."

The rule they rely on:

> "Project Proponents may also exclude SSRs where the total emissions for that SSR, and all excluded SSRs collectively, are expected to be negligible. Negligible SSRs are those which fall below a Materiality threshold based on environmental significance of < 1% of net CO2e removals. The purpose of the Materiality threshold is to save resources being expended on GHG accounting for negligible SSRs, in a manner that is proportional to the principle of scientific rigor and evaluation of uncertainty that underpins the Isometric Standard." — GHG Accounting Module v1.1 §5.0

The same section sets the level the test runs at:

> "The Materiality assessment should be undertaken for complete categories of SSRs… Examples of such categories include: Equipment and materials manufacture…; Feedstock transport: the end-to-end transportation of feedstock, covering all modes of transport used (e.g., road, rail, sea)."

**Verifier acceptance.** NULIFE Verification Report p.20: "No significant findings".

**What Charm does now.** Every small line is calculated and deducted each period. Charm PDD v1.12, Section B boundary table, waste disposal row:

> "Charm is using an emissions calculation approach that accounts for both the transport of the wastes to the disposal site, and the emissions impact of the disposal itself."

and, for sample transport:

> "Emissions are calculated for air shipment of samples based on a conservative estimate of the point-to-point distance between the sampling site and labs in Google maps."

**What Charm would gain.** The monthly waste-disposal calculation sheet, the per-event disposal manifest check, the BCU (Book and Claim Unit) cross-check that runs off it, and the sample-transport distance estimate all stop being produced.

**First step.** Build the materiality assessment at whole-category level, since the module tests categories rather than single lines, and check the collective total against the 1% cap before proposing anything to Isometric.

---

## 2. Carbon-content testing at a non-accredited in-house or university lab

*Added under the scope statement; strike if not wanted.*

**What the peer does.** NULIFE runs its carbon measurement at a university lab that is not accredited, and says so in the filed document. NULIFE PDD p.20:

> "Carbon wt% is determined by elemental analysis (ASTM D5921 or equivalent) using the University of Saskatchewan Chemical Engineering Lab (deemed an in-house lab that is not ISO17025 accredited lab*)."

The footnote on the same page names the route:

> "*An In-house lab is deemed acceptable by Isometric by supplying more information. Attachment 'Carbon content lab test requirements v1.0' is provided for more details on the procedures of the equipment."

That attachment is not published on the registry. The protocol clause it sits under:

> "Analysis must be completed by a qualified laboratory, as evidenced by accreditation to ISO 17025 or equivalent standards for laboratory quality management for the specific test method (ASTM D5291)." — Bio-oil Geological Storage v1.2 §8.3.1.1

**Verifier acceptance.** NULIFE Validation & Verification Report p.14, Uncertainty row, Comments column:

> "Monitoring plan robust, but external lab not ISO 17025 accredited. NuLife uses a lab that has provided the necessary details Isometric requested for non-ISO 17025 labs."

The same report at p.9 calls the arrangement "independent elemental carbon analysis", and the validation plan at p.30 sets the check as: "Confirm that the University of Saskatchewan Chemical Engineering Lab, an in-house lab, provides additional required information to Isometric for acceptability."

**What Charm does now.** Charm PDD v1.12, Appendix 6, GHG Statement Methodology – Data:

> "Carbon content of the oil will be measured using Isometric Protocol Method A – Each injection batch will be sampled prior to the addition of salt and LCS and one sample will be sent to an analytic lab to measure the carbon content of that batch."

**What Charm would gain.** The "or equivalent standards for laboratory quality management" clause opens a Charm-run or university-run lab as an alternative to an outside accredited lab on every batch — shorter turnaround and a cost Charm controls, on the route Isometric has already accepted once.

**First step.** Ask Isometric for "Carbon content lab test requirements v1.0" and judge the option against what it actually asks for.

---

## 3. Monitoring plan and calculation methodology filed as companion documents

**What the peer does.** Great Plains files its monitoring plan and its calculations as separate documents the PDD points to. Vaulted Great Plains PDD p.11:

> "Yes — Vaulted has submitted a completed monitoring plan alongside this PDD"

and p.15:

> "Full sensitivity analysis and calculations can be found in the Vaulted GHG Statement_12.20.23."

TIRE goes one step further on the same idea. Its PDD §E.1 "Monitoring requirements" (TIRE PDD p.53) presents the monitoring plan as a table summarizing the monitoring requirements stated in the facility's Class V UIC permit, with each row's evidence column naming permit-cadence documents — EPA quarterly reports, data-acquisition-system output, lab evidence, survey reports — rather than a document written for Isometric. That page carries no extractable text, so this describes it rather than quoting it. Basco 6 is a Class V well, which makes TIRE the direct precedent: the permit's own reporting table can stand as the monitoring plan.

**Verifier acceptance.** Vaulted Great Plains Verification Report p.14:

> "Acceptable – PPD completed / updated appropriately and submitted."

**What Charm does now.** Charm PDD v1.12, Section B Monitoring Plan, option-selection cell:

> "I have submitted a Monitoring Plan, which meets the requirements specified in the "Monitoring Plan Requirements" appendix of the relevant Protocol and its associated modules, and which describes any additional or modified parameters monitored which deviate from the default Monitoring Plan"

Both the monitoring plan and the calculation methodology sit inside the PDD body, in the storage-parameters cell and in Appendix 6.

**What Charm would gain.** A shorter PDD to keep internally consistent at every version bump. The monitoring and calculation work is unchanged — only its container moves.

**First step.** The open question is whether a companion filing satisfies this:

> "The PDD must be consistent with ISO 14064-2:2019, and must include: ... a monitoring plan detailing the elements to be monitored, frequency of monitoring and reporting, including relevant Project activities in each step of the Project cycle, measurement equipment, methods and procedures, details on accuracy and calibration, the clear assignment of responsibilities of parties involved in monitoring and reporting to Isometric, and appropriate measures for quality assurance and quality control" — Isometric Standard v2.1 §3.2

Searches of the Standard for "outside the PDD", "separate document", "filed separately" and "alongside" find no carve-out. Put that question to Isometric citing Great Plains' accepted filing, and fold the answer into the PDD restructure already under way.

---

## 4. Fixed per-tonne embodied factor for Basco 6, set once

**What the peer does.** Great Plains sets one embodied-emissions factor per tonne against lifetime capacity. Vaulted Great Plains PDD, Appendix 13, p.75–76:

> "Materials were allocated to each metric ton of waste based on a conservative estimate of lifetime processing waste capacity of 2,000,000 metric tons of waste."

This is not a one-time up-front deduction. It spreads evenly over lifetime capacity, so every tonne carries the same charge.

**Verifier acceptance.** Vaulted Great Plains Verification Report, Table 4 "Prior Findings" (p.17) and Table 5 "Exemptions From Isometric" (p.18) carry no embodied-emissions row.

**What Charm does now.** Charm already applies Vaulted's factor to its Kansas removals. Charm PDD v1.12, Appendix 6:

> "0.0000351566 tons of steel and 0.000077 m3 of concrete per ton of waste injected"

For Basco 6, the boundary-table row "Embodied Emissions from Injection Equipment (Charm)" has an empty quantification cell and refers out: "See the Combined Emissions Monitoring and Accounting Plan for the site, included in Supplemental Doc 3". A dated workbook is rebuilt every period instead, with open finding ISS-36 against it:

> "Updated amortization plan proposed and under review. To be implemented from August 2026 RP forward"

**What Charm would gain.** The monthly rebuild and the per-item life-cycle check both stop.

**First step.** This is in progress under ISS-36: the factor is being set against Basco's capacity — Charm PDD v1.12, storage-site details, Louisiana entry, permit "IMD 2025-05 EW": "Well/site storage capacity (total): Estimated range: 465,000 to 840,000 MT".

---

## 5. Transport emissions from a carrier-supplied fuel factor instead of per-leg distance evidence

**What the peer does.** TIRE prices transport off a fuel figure the carrier supplies. TIRE PDD p.23:

> "0.37 gallon/ton waste"

sourced as:

> "Measured - Fuel use mpg provided by transport company"

Distance appears once, as a fixed input (p.24):

> "Google maps: road miles between supplier and well site"
>
> "26.3 miles"

**Verifier acceptance.** None found. The TIRE verification report page read carries no finding on the transport method.

**What Charm does now.** Charm PDD v1.12, boundary row 12:

> "Distance Based Method outlined in the Isometric Transportation Emissions Accounting module, using scale tickets to document the mass transported"

with the routing rule:

> "When multiple routes are presented, the longest route is assumed to ensure a conservative estimate of removals"

Each leg needs its own route map, and the QA rule treats a missing one as a failure: "Distance Evidence for All Transport Calculations". The recurring failure it catches is on record — "the Douglas Tank PNG showed 1,759 mi while the calc sheet used 1,729 mi (30 mi gap caught only after opening the PNG)."

**What Charm would gain.** The route-map image per leg, and that mismatch failure mode, drop out of the truck legs.

**First step.** Rail legs likely stay distance-based, so scope the ask to truck. No verifier has accepted this on TIRE, so it goes to Isometric as a question, not a notification.

---

## Sources

**Charm.** PDD v1.12, 1 December 2025 (internal). Certify Log of Issues, ISS-36, read 16 September 2026.

**Peers.** NULIFE GreenTech, Ontario Avenue Bio-Oil Sequestration — PDD (87 pages, registry row 30 September 2025); Validation & Verification Report, 30 September 2025; Verification Report, 26 August 2026, Normec Verifavia. Vaulted Deep, Great Plains Organic Waste Sequestration — PDD v0.8 (83 pages, registry row 18 September 2025); Verification Report, 31 August 2026, 350Solutions. Vaulted Deep, TIRE Project — PDD, pp.23–24 and p.53; GHG Statement Reports RP1 and RP2; Verification Report V1.1, 28 August 2026.

**Rules.** Bio-oil Geological Storage protocol v1.2, page read 14 September 2026. Isometric Standard v2.1. GHG Accounting Module v1.1. Module and Standard pages read 16 September 2026.
