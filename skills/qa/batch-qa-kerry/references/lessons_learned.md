# Kerry Batch QA — Lessons Learned

This file records anticipated and observed failure categories specific to Kerry batch QA. Each entry has a name, an applicable-batch-type tag, the specific failure it prevents, and the mitigation. Read this file as part of the Pre-Flight Gate; print the applicable Failure Categories to chat before Gate 1 begins.

**Format conventions:**
- **FC-K[N]** prefix distinguishes Kerry-specific failure categories from AECN's FC[N].
- "Applies to" tag indicates which batch types the lesson applies to (tote, tanker, both, or first-of-mode).
- "Trigger" describes the operational condition that activates the failure mode.
- "Mitigation" describes the structural defense built into the skill.

For lessons that apply across all oil types (AECN, Kerry, future WODO/Aqueous), see `skills/qa/batch-qa/references/lessons_learned.md` — that's the AECN file but most of FC1–FC10 are oil-agnostic and apply to Kerry as well.

---

## FC-K1 — Tote tare from manufacturer label rather than measured

**Applies to:** Tote mode batches.

**Trigger:** The tote weighing log shows a tare value identical to the manufacturer's nominal label (e.g., "275 kg per IBC" — a round number that matches the IBC tank's spec sheet) for every tote, with no per-tote weighing date. Or the tare column is omitted entirely and the agent infers tare from a default.

**Failure mode:** Manufacturer-nominal tare overstates net mass (real empty totes weigh more than the nominal due to residue, water, label additions, scuff weight). Using nominal tare inflates MOBI and over-credits the Kerry portion. Verifier-side, this is a measurement-evidence gap: tare must be measured for the specific totes used in this batch.

**Mitigation:**
- Section 2.2 (tote mode) requires per-batch measured-tare evidence: a tare reading paired with a weighing date and location for each tote serial.
- If the tare is nominal (no per-batch measurement), the item is FLAG (not PASS). It becomes FAIL if the methodology memo or operational SOP requires measured tare.
- Adversarial reviewer challenges any tote in the source-read log whose tare has no `weighing_date` or whose tare equals a round nominal value (275, 300 kg etc.) without per-batch evidence.

**Why this lesson exists:** Anticipated from the AECN scale-ticket discipline — AECN's empty scale ticket is a real measurement, not a vehicle-spec lookup. Kerry tote tares need the same level of rigor; using nominal labels is a shortcut that breaks the verifier's expectation.

---

## FC-K2 — Confusing gross-transported mass with MOBI for transport-EF basis

**Applies to:** Tote mode batches.

**Trigger:** In Certify, the Mass of Load datapoint on the Flatbed Transport Process component is set to MOBI (sum of tote nets) rather than BOL gross mass (oil + tote tares + deck items).

**Failure mode:** Transport process emissions are calculated as Mass × Distance × EF (per T-mi). Using MOBI alone undercounts the load because the truck actually hauled more than just the oil — it hauled the totes themselves and any deck items. Under-reporting transport process emissions inflates Net CDR.

**Mitigation:**
- Section 2.5 (mass transported convention in SKILL.md) specifies: transport-EF basis = BOL gross mass (tote mode) or BOL oil-only mass (tanker mode).
- Section 8.2 verifies the Certify Flatbed Transport Process Mass of Load datapoint matches BOL gross (not MOBI) in tote mode.
- Source-read log records both `mobi_kg` and `bol_gross_kg` separately; cross-check at Gate 2.
- Adversarial reviewer challenges any transport-EF mass basis that equals MOBI in tote mode without an explicit reconciliation showing tote tares were zero (which they aren't).

**Why this lesson exists:** Anticipated from AECN's tanker truck convention where Mass of Load = oil-only (because the tanker's tare is excluded by convention; tanker embodied is per-mile). For Kerry tote shipments, the totes ARE the cargo conveyance and their mass IS being moved by the truck — so the per-T-mi process EF must apply to the gross load, not just the oil.

---

## FC-K3 — Per-tote count mismatch across BOL, weighing log, and Ops Notes

**Applies to:** Tote mode batches.

**Trigger:** Count of tote serials on the BOL ≠ count of tote weighing records ≠ count of net entries in Ops Notes. Often 1-tote off (e.g., BOL lists 8 totes, weighing log has 7, Ops Notes shows 8 nets — one tote skipped during weighing or a phantom net entered).

**Failure mode:** A missing weighing means MOBI is computed from N−1 nets, missing the mass of the unweighed tote. A phantom Ops Notes net adds mass that wasn't actually weighed. Either way, the mass chain breaks and MOBI is wrong by one tote's worth (~0.5–1.4 MT for typical IBC totes).

**Mitigation:**
- Section 2.5 (tote mode) requires explicit per-tote reconciliation: count(totes on BOL) = count(serials weighed) = count(nets in Ops Notes). All three must match exactly. Mismatch = FAIL.
- Source-read log enumerates every tote serial; Gate 1 exit check verifies count consistency before allowing Gate 2.
- Adversarial reviewer cross-references the three counts independently.

**Why this lesson exists:** Anticipated from AECN's rail-batch sister-row reconciliation pattern — when batches share a railcar, sister-batch counts must reconcile or oil is unaccounted for. Kerry tote shipments have a similar reconciliation requirement, just at the per-tote level rather than per-offload.

---

## FC-K4 — Applying AECN sparging math to Kerry mass

**Applies to:** Both tote and tanker modes.

**Trigger:** Ops Notes, COBB, Certify, or the QA checklist shows a 1.29% sparging deduction applied to Kerry MOBI before computing gross CO2e. Or the Kerry credit math subtracts 1.29% anywhere in the chain.

**Failure mode:** Kerry enters the homogenization tank un-sparged. Sparging is applied to the AECN portion only, before homogenization, and the AECN production batch QA owns the sparging deduction. Applying 1.29% to Kerry mass under-credits Kerry by ~1.3% — a material error that compounds across batches.

**Mitigation:**
- Section 6 (Gross-to-Net Calculation) explicitly verifies: Gross CO2e = MOBI × C_decimal × 3.667, with MOBI un-sparged.
- Section 2 (Mass Quantification) does NOT include a sparging item.
- SKILL.md Key Formulas section states: "No sparging deduction. Kerry enters the homogenization tank un-sparged."
- Adversarial reviewer challenges any sparging-related deduction appearing in Kerry's gross-to-net path.

**Why this lesson exists:** Anticipated from the AECN-Kerry homogenization fact pattern. Max confirmed 2026-05-04: Kerry "is added to and homogenized with sparged AECN just like WODO is" — which means the AECN side has already been sparged before Kerry enters the tank. Kerry's mass is what the supplier delivered; sparging losses don't apply to it.

---

## FC-K5 — Upstream Kerry production component appears in Certify

**Applies to:** Both tote and tanker modes.

**Trigger:** Certify Components tab shows any of: "Kerry Production Process Emissions", "Kerry Production Embodied Emissions", "Kerry Biomass Sourcing", "Kerry Pyrolysis [Process|Embodied]", or any feedstock-allocation component tagged to Kerry.

**Failure mode:** Kerry's VVB-validated waste boundary excludes biomass sourcing and production emissions entirely. The presence of any upstream production component indicates either (a) Certify has been misconfigured for Kerry, treating it like AECN, or (b) the Kerry methodology has been silently revised and the QA hasn't been updated. Either way, the credit math is wrong: an upstream component that shouldn't exist is reducing Net CDR.

**Mitigation:**
- Section 8.4 (Certify Component Mapping — No upstream production) explicitly checks for the absence of these components. Presence = FAIL (system-boundary violation).
- SKILL.md System Boundary section spells out the in-scope/out-of-scope split unambiguously.
- Adversarial reviewer cross-references the Components list against the in-scope component list (Sequestration, Flatbed Transport Process+Embodied, Injection-site, BCUs); anything else for Kerry is a finding.

**Why this lesson exists:** This is the Kerry-specific structural distinction from AECN. AECN has full upstream production components (Pyrolysis Process + Embodied) by design. Kerry doesn't. An agent that's been doing AECN QA may carry over the AECN component expectation list and miss that for Kerry, those components shouldn't exist.

---

## FC-K6 — Counterfactual ≠ 0 in Certify

**Applies to:** Both tote and tanker modes.

**Trigger:** Certify Components tab shows a non-zero Counterfactuals value for the Kerry removal.

**Failure mode:** Kerry's waste boundary handles the counterfactual by excluding upstream entirely (no biomass sourcing or production emissions are credited or debited). It does NOT handle the counterfactual by adding an offsetting counterfactual emission. If Certify shows a non-zero counterfactual for Kerry, the methodology is being applied incorrectly — likely double-counting (excluding upstream AND adding a CC2/CC3 counterfactual), which under-credits Kerry.

**Mitigation:**
- Section 8.5 (Counterfactuals) verifies counterfactual = 0. Non-zero = FAIL.
- SKILL.md System Boundary section states: "No counterfactual emissions component is expected (the methodology accounts for the waste status by excluding upstream entirely, not by adding an offsetting counterfactual)."
- Adversarial reviewer cross-references the Counterfactuals datapoint against the expected zero.

**Why this lesson exists:** The Biomass Feedstock Accounting Module v1.3 distinguishes between (a) waste/SC5-classified feedstocks where upstream is excluded and (b) feedstocks where upstream is included with a CC1/CC2/CC3 counterfactual offset. Kerry uses path (a). An agent or Certify configurer who's familiar with path (b) might mistakenly add a counterfactual to Kerry — that's the failure to catch.

---

## FC-K7 — Mode misdetection at Gate 1

**Applies to:** First-of-mode batches and any batch where Drive contents are atypical.

**Trigger:** Gate 1 mode detection (tote vs tanker) is wrong — e.g., a tanker batch is processed as tote because the agent sees a single weighing record and assumes tote-mode N=1; or a tote batch is processed as tanker because the agent finds one consolidated weighing PDF and skips the per-tote enumeration.

**Failure mode:** Wrong mode → wrong Section 2 path → wrong mass chain checks → wrong uncertainty convention. Section 6a's expected uncertainty (1.13 kg vs N × 1.13 kg) gets applied incorrectly. Per-tote reconciliation (FC-K3) is skipped on a real tote batch, missing tote-count mismatches.

**Mitigation:**
- Gate 1 explicitly records `delivery_mode: "tote"` or `"tanker"` in the source-read log; this is a Gate 1 exit check.
- SKILL.md Gate 1 specifies the mode-detection criteria: tote weighing log + multi-tote BOL → tote; full+empty scale ticket pair + single oil-mass BOL → tanker. Ambiguous cases must be escalated to Max.
- Adversarial reviewer verifies the recorded mode matches the source-read artifacts (tote serials present → tote mode; tractor/trailer numbers on a single full+empty pair → tanker mode).

**Why this lesson exists:** Kerry is the first oil type in this skill family with two delivery modes that look superficially similar at the Drive folder level (both flatbed truck). Mode disambiguation needs to be deliberate, not assumed.

---

## FC-K8 — Single-fix laziness (deliver the whole chain, not just what was surfaced)

**Applies to:** All batches, every gate, every Max-correction or Garrett-correction pass.

**Trigger:** Max or Garrett surfaces an issue in a checklist evidence note. Agent fixes only the surfaced item and re-delivers, leaving downstream items that share the same root cause untouched and now contradicting the corrected item.

**Failure mode:** Re-delivery contains internal contradictions. User catches the next dependent item, has to call out the same class of issue a second time. Erodes trust per-iteration faster than the original error did.

**Real example (K-002, 2026-05-06):** Max flagged the 4,619 vs 4,618 contradiction across items 1.4 and 1.5. Agent fixed those two and re-delivered. Item 1.7 still said "evidence value confirms reported value end-to-end" referencing the same `4,619 = sum of per-tote nets` claim that had just been refuted. Max called it out: "Fixing one thing because I find it is bush league. Child behavior. If there's an issue, it's on YOU to follow the thread ALL THE WAY DOWN."

**Mitigation (lock this in):**

1. **Identify the root cause** of any flagged finding before patching.
2. **Go back through the checklist row by row** and re-read every evidence note that cites the number, filename, datapoint name, or claim behind the original finding, re-opening the underlying documents myself rather than trusting memory of which rows reference what.
3. **Audit every hit.** For each match, ask: does this item's status/reasoning still hold given the corrected understanding? If not, fix it in the same pass.
4. **Audit dropped findings too** when restructuring the checklist (v1 → v2 → v3). Real findings can fall through restructuring cracks alongside spurious ones — re-check each prior version's findings list against the new structure before re-delivering.
5. **Re-run the audit script** after edits — fixed evidence may have new citation tags or quoted numerics.
6. Only then re-deliver.

This applies on first delivery, on Max-correction passes, AND on Garrett-correction passes. The standard isn't "fix what was named" — it's "deliver a product that's internally consistent." Adversarial-review (Gate 3) MUST include this dependency-thread audit pass for any item that changed since the previous draft.

---

## Cross-skill lessons (apply equally to Kerry)

For lessons that apply across all oil types, read the AECN file at `skills/qa/batch-qa/references/lessons_learned.md`. Notable carry-overs:

- **FC1 (AECN):** Sources tab is the truth (not Datapoints tab). COBB tracker larger than viewport — verify cell A before reading row values. Applies identically to Kerry.
- **FC3 (AECN):** Scale tickets MUST be opened as images (in tanker-mode Kerry batches). Uncertainty modals MUST be opened.
- **FC8 (AECN):** Vehicle Embodied EFs are PER-MILE, not per-T-mi. Applies to Kerry flatbed embodied identically.
- **FC10 (AECN):** Every evidence note MUST cite `[log:KEY]` to source-read log. Adversarial review log-driven only. "Blocking" requires ≥3 enumerated tooling-path attempts. All apply to Kerry.

When a Kerry-specific lesson contradicts an AECN lesson, the Kerry lesson wins for Kerry batches. (Notable: FC11 in AECN — railcar last-offload conservatism — does NOT apply to Kerry, which has no rail mode.)
