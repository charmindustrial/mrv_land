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

**See also (authoritative implementation specs):**
- Per-item AECN spec: `skills/qa/batch-qa/references/checklist_structure.md` (item-by-item, with truck/rail differentials)
- Site emissions QA spec: `skills/qa/site-emissions-qa/SKILL.md` + `references/category_evidence_guide.md`
- Adversarial review pass: `skills/qa/adversarial-reviewer/SKILL.md`
- Certify structure history (oil types, EF evolution, component naming): `knowledge-base/Certify_Deep_Dive_Findings.md`
- Lessons learned (failure patterns from prior batches): `skills/qa/batch-qa/references/lessons_learned.md`

---

## Status Taxonomy

Every checklist item gets one of four statuses:

- **PASS** — verified against primary source; evidence note cites specific values
- **FAIL** — would prevent a verifier from confirming the reported value (risk of material misstatement). Includes: evidence contradicts reporting, mass values disagree across sources, EFs misapplied, required document missing
- **FLAG** — process/hygiene issue but the underlying value is supportable (e.g., generic source filenames like "Screenshot 2026-XX-XX.png", non-descriptive datapoint names). Does not block submission
- **N/A** — item does not apply to this batch type / oil type / site

**FAIL vs FLAG decision rule:** *Would a VVB reviewer be blocked from confirming the reported value if submitted as-is?* If yes → FAIL. If no → FLAG.

**Evidence rule:** Every status is a claim that needs grounding.
- PASS requires the evidence note to cite specific values from primary sources — not "confirmed," not "matches"
- N/A requires a one-line reason why the item doesn't apply
- FLAG requires identifying the hygiene issue
- FAIL requires the contradiction or gap, with the value/source that triggered it

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
- [ ] Carbon content within expected range for oil type:
  - **AECN:** mean 39.42%, SD 6.09%, n=285 (per `Charm_Isometric_Knowledge_Base.md` / `MRV_AECN_Analysis.xlsx`). FLAG values outside ±2σ (~27.2%–51.6%); investigate before PASS
  - **Charm WODO:** range varies by production period — confirm against current PP CI calc
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
*Execution: backed by `skills/qa/batch-qa/qa-batch-aecn` skill — covers truck + rail. Run skill for AECN-only batches; for mixed batches, run skill for AECN portion + manual passes for other oil types below.*

Skip if no AECN in batch.
- [ ] Required files present: LCA CI spreadsheet, LCA with stack emissions, Supporting GHG data
- [ ] AECN pyrolysis process EF: **0.10 tCO2e/t** (verify matches GHG Statement)
- [ ] AECN pyrolysis embodied EF: **0.02 tCO2e/t** (verify matches GHG Statement)
- [ ] Baseline loss is positive

### Section 6b: Charm WODO
*Execution: **manual** — Max's `qa-batch-aecn` skill is AECN-only by design. Parallel `qa-batch-charm-wodo` skill not yet authored.*

Skip if no Charm WODO in batch.
- [ ] CI calculated via spreadsheet method
- [ ] Production Period emissions correctly allocated
- [ ] Flatbed truck transport distance and emissions entered
- [ ] No sparging deduction, no LCS

### Section 6c: Charm QOWV (Aqueous)
*Execution: **manual** — Max's `qa-batch-aecn` skill is AECN-only by design. Parallel `qa-batch-charm-aqueous` skill not yet authored.*

Skip if no Charm QOWV in batch.
- [ ] CI via same spreadsheet method as WODO
- [ ] Production Period emissions correctly allocated
- [ ] Flatbed truck transport distance and emissions entered
- [ ] LCS pre-treatment: LCS mass + CI entered in Certify; aqueous mass adjusted

### Section 6d: Kerry Oil
*Execution: **manual** + methodology gate. Skill not authored — parallel `qa-batch-kerry` deferred until methodology memo is fully approved.*

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
- [ ] Uncertainty discount applied per Isometric Standard v2.0 (aggregate — see 7a for per-component)
- [ ] Net removals consistent with BCU Quant spreadsheet and GHG Statement

### Section 7a: Per-Component Uncertainty Verification (AECN)

Per-component uncertainty is the single most-skipped check. Required even when the aggregate discount in Section 7 looks reasonable — aggregate can mask a missing component-level input.

- [ ] **Layer 1 — Completeness:** every AECN component has uncertainty on the correct datapoint (no missing ± inputs)
- [ ] **Layer 2 — Correctness:** reported ± matches the expected value per `skills/qa/batch-qa/SKILL.md` Uncertainty Reference + `knowledge-base/MRV_Uncertainty_Evidence_Cheat_Sheet.xlsx`
- [ ] **Layer 3 — Discount presence:** aggregate discount in Calculation View consistent with GHG Statement (cross-check Section 7)

**Required to verify per component (open each component's modal in Certify, read ± from the INPUTS section):**
- Injection Sequestration (Carbon Content + Mass of Product)
- Each Transport leg, process side (Mass of Load per leg)
  - Truck: 2 components (process + embodied for AECN→Basco)
  - Rail: 6 components (3 legs × process+embodied) — embodied side has no Mass of Load datapoint, do not flag
- AECN Pyrolysis Process Emissions (Bio-Oil Mass)
- AECN Pyrolysis Embodied Emissions (Bio-Oil Mass)

**Method:** Do NOT infer ± from aggregate Calculation View. Open each component modal individually. Per Max's spec: avoidance = automatic FAIL.

**🚂 Rail-batch note:** Per-offload framing means Mass-of-load uncertainty = ±72.57 kg per removal on each leg, regardless of inbound BOL count. Conservatism precondition (N_offloads ≥ N_inbound_BOLs) is checked on the *last* batch of a railcar; defer if not the last batch yet. See `skills/qa/batch-qa/references/checklist_structure.md` Section 7a 🚂 Rail.

### Section 8: Data Integrity & Anomaly Check
- [ ] No unexplained outliers in mass, carbon content, or calculated values
- [ ] Spills/losses: documented, unrecovered mass deducted, incident report filed
- [ ] Multi-period allocation: reconciliation spreadsheet verified if applicable

### Section 9: Isometric Certify — Removal Component Mapping

#### Site Emissions Allocation Convention
*Execution: site-emission components on the designated batch(es) are backed by `skills/qa/site-emissions-qa` skill. Run that skill once per RP, against the scapegoat removal(s). Output is checklist + 3-layer evidence map (Certify component value ↔ Certify source doc ↔ Drive folder evidence).*

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
- **Site emissions batches:** 1–2 batches per RP are designated to carry all site emissions. Chosen by Garrett. All other batches only have batch-specific components (transport, pyrolysis, sequestration, reductions).
- **Kerry Oil:** Use same batch methodology as most recent prior period unless told otherwise. Kerry batches appear in COBB like any other.
- **Sign-off:** Garrett + Max both review before submission.
- **Status taxonomy:** PASS / FAIL / FLAG / N/A (definitions at top of doc; FAIL vs FLAG decision rule = "would VVB be blocked from confirming the value?")
- **QA execution coverage today:**
  - AECN batches → `skills/qa/batch-qa/qa-batch-aecn` (4-gate workflow, truck + rail)
  - Site emissions per RP → `skills/qa/site-emissions-qa` (3-gate, 3-layer evidence map)
  - Adversarial pass on completed checklist → `skills/qa/adversarial-reviewer`
  - Performance tracking → `skills/qa/performance-monitor`
  - WODO / QOWV / Kerry batches → manual (skills not yet authored)
- **Source of truth for per-item AECN spec:** `skills/qa/batch-qa/references/checklist_structure.md`. Where this workflow doc and that file disagree on AECN specifics, the skill spec wins.

## Open Questions
- [ ] **Multi-oil-type skill coverage** — author parallel skills for WODO/QOWV/Kerry, or generalize the existing `qa-batch-aecn` skill to handle conditional logic by oil type? Deferred until Gaia hosting decision lands.
- [ ] **Certify export gaps** — sent ask to Iso about null linkage fields (Removal Component → Component ID, Removal ID, computed flux, uncertainty). Architecture for Gaia execution layer depends on response.
- [ ] **Gaia hosting** — once Iso responds, decide between (a) export-based pipeline if linkages get populated, (b) hybrid export+scrape, or (c) API integration if Certify exposes one.
- [ ] **Certify datapoint structure for new weekly batch format** *(deferred)*
