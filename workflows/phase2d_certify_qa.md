---
phase: "2d"
title: "Certify QA"
type: phase
period: "{{current_rp}}"
status: not_started
depends_on: ["2a", "2b", "2c"]
trigger: "After Phase 2a, 2b, and 2c are complete"
---

# Phase 2d: Certify QA Check

**Trigger:** After [[phase2a_injection_batch_data]], [[phase2b_injection_emissions]], and [[phase2c_mangrove]] are complete
**Output:** Verified injection batch(es) ready for submission to Isometric Certify; QA checklist signed off

**Tool:** Isometric Certify (browser — Playwright session)
**Reference:** 9-section QA checklist (`Injection_Batch_QA_Checklist.xlsx` in Downloads)
**Protocol:** Bio-Oil Geological Storage v1.0/1.1/1.2; Isometric Standard v2.0

**Session type:** Playwright — keep focused on one batch at a time

---

## Pre-Session Checklist

Before opening Certify, confirm all of the following are done:
- [ ] Phase 2a complete: all batch ops notes verified, mass/carbon/pH confirmed
- [ ] Phase 2b complete: site emissions totals finalized in BCU Quant
- [ ] Phase 2c complete: all Mangrove events entered and evidenced
- [ ] Batch folder on Drive: complete with Scale Tickets, Testing PDFs, BOLs
- [ ] All source documents named descriptively (no "IMG_001", "Measurement XXXX")
- [ ] **EF verification:** All emission factors in Certify datapoints match the current Standard EF CSV (see Phase 2b EF Reference table). Until MG automates backend EF updates, check every EF datapoint against the CSV at the start of each RP. Key EFs to verify:
  - AECN production process EF (updated with each LCA refresh)
  - AECN production embodied EF
  - Transport EFs (tanker truck, flatbed, rail — process + embodied)
  - Fuel EFs (diesel, gasoline WTW)

---

## Section-by-Section QA

### Section 1: Batch Folder Completeness
- [ ] Folder named correctly (`2-XXX`, `K-XXXXX`, `3-XXX`, `4-XXX`)
- [ ] Scale Tickets subfolder: full + empty tickets present for each truck
- [ ] Testing subfolder: SGS COA PDF present
- [ ] Ops Notes file present
- [ ] Verifier reference: VR Appendix 1

### Section 2: Scale Tickets & Mass Determination
- [ ] Empty + full ticket images for each truckload
- [ ] Ticket pair dates within 2 weeks of injection date
- [ ] Tractor # matches between empty and full ticket
- [ ] Trailer # matches between empty and full ticket
- [ ] Net mass = full − empty (verify arithmetic)
- [ ] Injectate mass = MIN(scale ticket net, originating BOL mass)
- [ ] Sparging deduction: 1.29% applied to AECN only (NOT Charm WODO or QOWV)
- [ ] Aqueous (QOWV): LCS pre-treatment applied instead of sparging
- [ ] All mass values consistent: scale tickets ↔ Ops Notes ↔ Certify/dMRV

### Section 3: Bills of Lading & Transportation
- [ ] Truck BOL(s) present for each shipment
- [ ] Rail: 3 BOLs per railcar (standard)
- [ ] BOL mass ≥ reported injectate mass
- [ ] Origin/destination correct:
  - AECN truck: AECN → Basco
  - AECN rail: AECN → SOPOR → Basco
  - Charm: Fort Lupton CO → Basco
- [ ] Transport distances correct:
  - AECN truck: ~2,197 mi
  - AECN rail: ~2,199 mi (via SOPOR)
  - Charm flatbed: varies
- [ ] Transport mode in Certify > Datapoints matches oil type
- [ ] Billing docs present and consistent with BOL

### Section 4: Bio-Oil Composition & Testing (CHN)
- [ ] CHN analysis PDF in Testing subfolder
- [ ] Carbon content reasonable: AECN ~41–42%; Charm varies
- [ ] H and N values reported and reasonable
- [ ] Lab report references correct batch/sample ID
- [ ] If QOWV: pH and conductivity present, within permit range (UIC Permit / LDENR)
- [ ] Carbon content in CO2e calc matches lab report exactly

### Section 5: Ops Notes Accuracy
- [ ] Correct batch ID
- [ ] Correct injection date / completion date (matches COBB)
- [ ] Scale ticket values correctly transcribed
- [ ] Oil + aqueous mass consistency
- [ ] COBB values present and match
- [ ] pH noted
- [ ] No erroneous density measurements (density only for estimating AECN oil input)

### Section 6a: AECN Feedstock Emissions
Skip if no AECN in batch.
- [ ] Required files present: LCA CI spreadsheet, LCA with stack emissions, Supporting GHG data
- [ ] AECN pyrolysis process EF: **0.10 tCO2e/t** (verify matches GHG Statement)
- [ ] AECN pyrolysis embodied EF: **0.02 tCO2e/t** (verify matches GHG Statement)
- [ ] Baseline loss is positive

### Section 6b: Charm WODO
Skip if no Charm WODO in batch.
- [ ] CI calculated via spreadsheet method
- [ ] Production Period emissions correctly allocated
- [ ] Flatbed truck transport distance and emissions entered
- [ ] No sparging deduction, no LCS

### Section 6c: Charm QOWV (Aqueous)
Skip if no Charm QOWV in batch.
- [ ] CI via same spreadsheet method as WODO
- [ ] Production Period emissions correctly allocated
- [ ] Flatbed truck transport distance and emissions entered
- [ ] LCS pre-treatment: LCS mass + CI entered in Certify; aqueous mass adjusted

### Section 6d: Kerry Oil
Skip if no Kerry in batch.
- [ ] **STOP: Do not submit Kerry batches until methodology memo is approved**
- [ ] Methodology memo attached to batch folder and approved
- [ ] Kerry CI/EF per approved methodology
- [ ] Tote transport (flatbed); pre-treatment per methodology

### Section 7: Gross-to-Net Calculation
- [ ] Gross CO2e = injectate mass (kg) × carbon wt% (as decimal) × 3.664 / 1000 → tCO2e
- [ ] Units consistent throughout (kg→kg CO2e or t→tCO2e)
- [ ] Carbon as decimal (0.42, not 42)
- [ ] Process emissions deducted from gross (all oil types combined)
- [ ] Uncertainty discount applied per Isometric Standard v2.0
- [ ] Net removals consistent with BCU Quant spreadsheet and GHG Statement

### Section 8: Data Integrity & Anomaly Check
- [ ] No unexplained outliers in mass, carbon content, or calculated values
- [ ] Spills/losses: documented, unrecovered mass deducted, incident report filed
- [ ] Multi-period allocation: reconciliation spreadsheet verified if applicable

### Section 9: Isometric Certify — Removal Component Mapping

#### Site Emissions Allocation Convention
Site emissions from Phase 2b are not spread across all batches — they are loaded onto **1–2 designated batches** per reporting period. These batches carry the full site emissions burden under the "Bio-oil injection" removal activity group. All other batches in the period have only their batch-specific components (transport, pyrolysis, sequestration).

#### Certify Component Structure (per batch)

**SEQUESTRATIONS**
- [ ] Injection sequestration: gross CO2e matches internal gross (one entry per removal, covers all oil types)

**REMOVAL ACTIVITIES — Bio-oil injection** (batch-specific + site emissions if designated batch)

Batch-specific components (all batches):
- [ ] LCS and sample transport emissions (where applicable)

Site emission components (designated batch(es) only):
- [ ] `B6 Injection site diesel emissions` — matches Phase 2b diesel total
- [ ] `B6 Injection site gasoline emissions` — matches Phase 2b gasoline total
- [ ] `B6 Injection site water emissions - transport embodied emissions` — brine transport embodied
- [ ] `B6 Injection site water emissions - transport process emissions` — brine transport process
- [ ] `B6 Injection - Embodied Emissions` — matches Phase 2b embodied emissions (capital amortization + SP&C)
- [ ] `B6 Injection - Additional Emissions` — rollup of remaining site categories (support travel, sitework, railcar cleaning, argon, electricity, KS equipment transport, methanol, railcar loss)
- [ ] Sum of all site emission components matches Phase 2b grand total site emissions

**REMOVAL ACTIVITIES — Bio-oil transport** (all batches with transport)
- [ ] Process emissions per lot/mode:
  - `AECN to LA Tanker Truck Transport Process Emissions - AECN` (truck)
  - Railcar transport process emissions (rail)
  - Flatbed transport process emissions (Charm WODO/QOWV)
- [ ] Embodied emissions per lot/mode:
  - `AECN to LA Tanker Truck Transport Embodied Emissions - AECN` (truck)
  - Railcar transport embodied emissions (rail)
  - Flatbed transport embodied emissions (Charm)

**REMOVAL ACTIVITIES — Pyrolysis or other process** (all batches)
- [ ] Each oil type has an entry:
  - `AECN pyrolysis (from truck loads) - process emissions`
  - `AECN pyrolysis (from truck loads) - embodied emissions`
  - `Production Period [X] - process emissions` (Charm WODO/QOWV)
  - `Production Period [X] - embodied emissions` (Charm WODO/QOWV)

**REDUCTIONS**
- [ ] BCU categories populated or N/A:
  - `BCUs - Applied to Bio-Oil Transport Process Emissions`
  - Injection diesel, injection waste, pre-treat diesel, pre-treat waste (as applicable)

**COUNTERFACTUALS**
- [ ] Baseline correctly computed or zero per protocol

**LOSSES**
- [ ] Zero unless spill/loss documented in Section 8

#### Final Checks
- [ ] Net removal in Certify matches internal net calculation
- [ ] All Datapoints have descriptively named source docs (no generic names)
- [ ] All Sources in Certify match files in batch folder on Drive
- [ ] Designated site-emissions batch(es) identified and documented in handoff

---

## Final Submission Steps
- [ ] QA checklist fully signed off (all 9 sections)
- [ ] GHG Statement updated
- [ ] Submission to Isometric Certify
- [ ] Notify 350 Solutions (VVB) per standard process

---

## Session Handoff Template

```
Phase: 2d - Certify QA
Period: [RP name]
Batches QA'd: [list UIDs]
Batches remaining: [list UIDs]
Site emissions batch(es): [UID(s) carrying site emissions]
Failed sections: [list any issues found]
Blocked on: [missing docs, approvals needed]
Next: [specific batch + section to resume from]
```

---

## Confirmed Conventions
- **VVB:** 350 Solutions — always, every period.
- **Site emissions batches:** 1–2 batches per RP are designated to carry all site emissions. These are chosen by Garrett. All other batches only have batch-specific components (transport, pyrolysis, sequestration, reductions).
- **Kerry Oil:** Use same batch methodology as most recent prior period unless told otherwise. Kerry batches appear in COBB like any other.
- **Sign-off:** Garrett + Max both review before submission.
- **QA checklist:** Built by Max's Claude Code agent(s) — integration with my workflow TBD.

## Open Questions
- [ ] How to integrate with Max's QA checklist agent process — to be worked out.
- [ ] Any changes to the Certify datapoint structure for the new weekly batch format? *(deferred)*
