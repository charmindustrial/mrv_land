# Charm WODO/Aqueous Batch QA — Lessons Learned

This file accumulates real failures from real QA sessions on Charm-produced bio-oil batches. Each Failure Category (FC-C-N) is a class of mistake to prevent on the next batch. Read this file at the Pre-Flight Gate of every Charm batch QA and print the applicable FCs to chat before Gate 1 begins.

This is a starter set, seeded from the AECN and Kerry skills' Failure Categories where the same failure mode applies to Charm, plus Charm-specific gotchas anticipated from the checklist structure. Add real-session FCs as they surface — each one earns its place by having burned a real batch.

---

## FC-C1 — Confusing WODO and Aqueous Standard-Loss treatment

**The failure:** Applying Standard Loss to an Aqueous tote, or omitting Standard Loss on a WODO tote.

**Why it happens:** WODO and Aqueous share most of the QA structure; it's tempting to copy a WODO checklist into an Aqueous batch (or vice versa) without re-reading Section 2.3.

**Mitigation:** At Gate 1, record `oil_type: "WODO"` or `"Aqueous"` explicitly in the source-read log. At Gate 2, when checking item 2.3, branch on `oil_type` first, THEN evaluate the math:
- WODO: Σ (Net-in-tote − Standard Loss)
- Aqueous: Σ (Pre-Unload − Post-Unload) — no Standard Loss

**Detection:** If the Ops Notes per-tote formula for net-in-batch references a "Standard Loss" column AND `oil_type == "Aqueous"`, FAIL 2.3 with FC-C1 citation.

---

## FC-C2 — A Production Period's emissions omitted entirely (NOT "lacks its own component")

**The failure:** The injection batch covers multiple Production Periods; one PP's production emissions are not captured anywhere in Certify.

**IMPORTANT — what this is NOT:** It is NOT a finding that multiple PPs are aggregated into one component. There is **no primary source requiring one Certify component per production period** — that "convention" lived only in this skill's own scaffolding and was DROPPED on INJ-06-2026-W1 (2026-06-25) after a verify-against-real-source check found nothing behind it. An aggregated component carrying a production-mass-weighted blended CI that reconciles to the per-PP sum is fully acceptable. Do not flag aggregation.

**Why the real failure happens:** PP coverage is enumerated in Charm Contents. Easy to miss a PP's emissions entirely if it contributed a small mass slice.

**Mitigation:** At Gate 2, confirm every PP's production emissions are accounted for — sum the per-PP (mass × CI) and confirm it equals the total in the production-emissions component(s), whether those are per-PP or one aggregated component. A PP whose emissions appear in NO component = FAIL. Aggregation that reconciles = PASS.

**Detection:** `Σ(per-PP mass × per-PP CI)` over Charm Contents/Ops Notes ≠ total production-emissions tCO₂e in Certify → investigate (a PP may be omitted). Equality (even via one blended-CI component) = pass.

---

## FC-C3 — Hard-coded RP Share / Allocated Miles / Batch Mileage Allocation

**The failure:** The Bio-Oil Shipment Tracker's computed cells display a number but contain a typed constant, not a formula. Looks fine on screen; un-auditable in practice.

**Why it happens:** Manual override during data entry without restoring the formula.

**Mitigation:** Item 3.3 is non-skippable. Read EACH computed cell (RP Share, RP Allocated Miles, Batch Mileage Allocation) with `drive_read.py rows` on the downloaded Tracker and read its `formula` field. Quote the formula verbatim in the source-read log: `shipment_tracker_cells_are_formulas: {rp_share: "=B2/B3", rp_allocated_miles: "=...", batch_mileage_allocation: "=..."}`. A constant ("0.5", "545.0") triggers FAIL 3.3 with FC-C3 citation.

**Detection:** source-read log field `shipment_tracker_cells_are_formulas` shows any value that is not a `=...` formula string.

---

## FC-C4 — LCS use in Ops Notes without matching Certify component (Aqueous)

**The failure:** Aqueous batch Ops Notes records LCS use (mass / volume of buffer). No corresponding Certify component exists in the emissions accounting.

**Why it happens:** LCS is optional buffering; not every Aqueous batch uses it. Easy to skip the Certify-side check on batches that DON'T use LCS, then carry that skip into a batch that DOES.

**Mitigation:** At Gate 1, search Ops Notes for "LCS" / "Liquid Calcium Sulfate" / buffer columns. Record `lcs_use_kg: [value]` or `lcs_use_kg: null` in the source-read log. At Gate 2, if `lcs_use_kg != null`, verify a matching Certify component exists with the reported mass and a correct EF. Missing component = FAIL 9.1 with FC-C4 citation. For WODO batches, render 9.1 as N/A.

**Detection:** `oil_type == "Aqueous"` AND `lcs_use_kg != null` AND no Certify component contains "LCS" or "Liquid Calcium Sulfate" → FAIL 9.1.

---

## FC-C5 — Tote roster mismatch (Shipment Tracker vs Ops Notes)

**The failure:** A tote appears in Ops Notes with one set of attributes (tag, fraction, gross, PP) and in the Shipment Tracker with different attributes — same tag but different fraction, or same fraction but different gross, etc.

**Why it happens:** Two independently maintained sheets with manual entry; one is updated and the other isn't.

**Mitigation:** At Gate 2, do an explicit per-tote per-attribute comparison (item 3.5) and write the mismatches to the evidence note. Any mismatch on any attribute = FAIL 3.5 with FC-C5 citation, listing the specific totes and attributes.

**Detection:** for each tote in Ops Notes, look up the corresponding row in Shipment Tracker by tag #. Compare fraction, gross, PP. Any non-match = FAIL.

---

## FC-C6 — Using non-longest Google Maps route for transport distance

**The failure:** Certify Distance for Transport Process uses the default Google Maps route (typically the fastest) instead of the longest of the displayed route options.

**Why it happens:** Google Maps presents 2–4 route options when you query; the default is the fastest, not the longest. The Charm convention is the longest (conservative for transport emissions).

**Mitigation:** At Gate 2, when evaluating item 5.2, open the Google Maps evidence; record ALL displayed route options in the source-read log: `google_maps_options: [{route: "I-10", distance_mi: 540}, {route: "I-20", distance_mi: 568}, ...]`. Verify Certify uses the MAX of these.

**Detection:** Certify distance < max(google_maps_options.distance_mi) → FAIL 5.2 with FC-C6 citation.

---

## FC-C7 — Mass of Load using Total Oil Produced or Total Oil in Batch (instead of Total Mass Transported)

**The failure:** Certify Transport Process Mass of Load matches Total Oil Produced or Total Oil in Batch, not Total Mass Transported. Under-reports transport emissions (the truck hauled tote tare mass too).

**Why it happens:** Three similar "Total" values in Ops Notes; easy to grab the wrong one. The transport-EF basis is GROSS (oil + tote tares), not net oil.

**Mitigation:** At Gate 2, item 5.3, verify Certify Mass of Load = Ops Notes Total Mass Transported specifically. Not Total Oil Produced (which is net of tare) and not Total Oil in Batch (which is net of tare AND standard loss/measured loss). Quote the cell name in evidence.

**Detection:** Certify Mass of Load == Total Oil Produced or Total Oil in Batch → FAIL 5.3 with FC-C7 citation.

---

## FC-C8 — Mistaking AECN per-truck precision (72.57 kg) for Charm per-tote precision (1.134 kg)

**The failure:** Applying AECN's per-truck uncertainty spec (72.57 kg per leg) to Charm batches, which use per-tote weighing (1.134 kg per discrete weight).

**Why it happens:** The AECN skill is the most-used and most-internalized; its precision spec is the "default" recalled from memory.

**Mitigation:** Charm uses Kerry-style per-tote precision: 2.5 lb / 2.20462 ≈ 1.134 kg per tote. For an N-tote batch, aggregate Mass-of-Product uncertainty = N × 1.134 kg. Verify against the formula Charm uses in Ops Notes uncertainty cell — that's the authoritative computation, and it should match this spec.

**Detection:** Reported uncertainty / N_totes ≠ 1.134 kg (within ±0.01) → investigate before assigning 2.4 status.

---

## FC-C9 — Re-litigating internal terminology (PP/PB slash, n=3 samples) as v1.2 issues

**The failure:** Flagging Charm's "Production Period/Production Batch" terminology or n=3 sample sizing as v1.2 protocol contradictions.

**Why it happens:** Both phrasings sound like methodology deviations to a fresh reader.

**Mitigation:** Both are settled internal-terminology choices, documented in workspace memories:
- `project_charm_batch_definitions.md` — PP/PB slash is operationally correct
- `project_charm_sample_size_policy.md` — n=3 is procedural standard

Do NOT raise either as a checklist FAIL or FLAG. If they surface in Ops Notes or Certify, no action.

**Detection:** any temptation to write "verify methodology" or "v1.2 contradiction" about PP/PB or n=3 → STOP, check memory, drop.

---

## FC-C10 — Treating PP Summary CI as one-size-fits-all across fractions

**The failure:** Using the WODO CI from a PP Summary as the CI for the Aqueous Production Emissions component (or vice versa) when the same PP produced both fractions.

**Why it happens:** PP Summary may list multiple fractions side-by-side; if you grab the first CI without checking which fraction, you may use the wrong one.

**Mitigation:** At Gate 2, item 7.2, when reading a PP Summary, identify the FRACTION columns explicitly. The Aqueous PE component matches the Aqueous CI in the PP Summary; the WODO PE component matches the WODO CI. Don't cross-wire.

**Detection:** if the Charm Contents sheet shows a PP contributed both WODO and Aqueous mass, expect TWO PE components for that PP (or one component aggregating both with a weighted CI). Investigate before assigning 7.2 status.

---

## FC-C11 — Inventing a rule vs. applying one Max actually stated (INJ-06-2026-W1 WODO)

**The failure (two-sided, same root):**
1. **Invented:** flagged 7.1 as a deviation from a "one Certify component per Production Period" convention. Max never stated this; it lived only in this skill's own scaffolding. When challenged it collapsed — no primary source. → DROP. Aggregating PPs into one mass-weighted component that reconciles to the per-PP sum is fine.
2. **Wrongly discarded a real rule:** then, over-correcting, dropped item 8.1 (diesel transport-process emission with no BCU) to N/A by leaning on "the protocol has no reductions term." But Max HAD stated — and the skill HAD recorded — that **all diesel transport-process emissions must be offset with BCUs.** That rule is authoritative. Absence of the BCU = FAIL, not N/A.

**The principle:** distinguish what Max told you (authoritative → belongs in the KB/skill, apply it) from what you inferred (never present as a rule). The knowledge base is how the agent learns over time, so it must hold only accurate rules. When a finding is challenged, separate the fabrication from the fact — don't throw out both. Curate the KB: delete fabrications, preserve and apply Max-stated rules.

**Detection:** before citing any "convention/requirement," ask "did Max state this, or is it only in my skill docs?" If only the skill docs and you can't trace it to a Max instruction or a primary source, it is not a rule — drop the finding and fix the skill doc.

---

## FC-C12 — Using marginal-uncertainty math to omit a dominant emission's uncertainty (INJ-06-2026-W1 WODO 7.5)

**The failure:** argued the pyrolysis PP mass could skip its uncertainty input under Bio-oil Geological Storage v1.2 §6.5 ("Input variables may be omitted ... if they contribute to a < 1% change in the net CO₂e removal") by computing the *marginal* effect of the mass measurement error (~0.13% of net) and calling that the input's "contribution."

**Why it's wrong:** the pyrolysis emission is 10.831 tCO₂e = **133% of net** (and ~84% of total emissions) — a dominant input by any reading. The <1% carve-out is for genuinely negligible inputs, not for re-labeling a major emission's small measurement error as "negligible contribution." §6.5.1 requires uncertainty on measured input variables (incl. weigh-scale masses); a dominant one is not omittable.

**Mitigation:** for the §6.5 <1% test, judge the input's contribution to the removal by the **magnitude of the term it drives** (its tCO₂e as a share of net/emissions), not the arithmetic size of its measurement error. Pyrolysis, transport, sequestration mass — all material → uncertainty required.

**Severity = FAIL, not FLAG.** A required uncertainty input that is missing means the removal cannot be submitted as-is (same as a missing required component/BCU). Do NOT grade it FLAG by pointing at the small marginal effect of the measurement error — that is the same flawed lens that produced the omission error in the first place. Required input missing → FAIL.

**Detection:** if an input drives an emission/sequestration term that is a non-trivial fraction of net, it does NOT qualify for the §6.5 omission carve-out, regardless of how small its ± looks; and if the required uncertainty is then absent, that is a FAIL.

---

## FC-C13 — Production CI counts biomass transport before its BCUs (INJ-09-2026-W4-QOWV 7.2)

**The rule (Max-stated, 2026-10-07):** "BCUs should be applied to diesel transport, including biomass transport process emissions and handling (not embodied emissions)."

**The failure:** the live monthly Production Period Summaries put biomass transport into the consolidated inventory at its total, before BCUs (`I19 = C9*F7`, "Total Emissions"), while the BCUs on process and log handling sit at C10. The CI they produce, copied into the Ops Notes monthly constants, counts emissions the BCUs already offset. The Jan–Jun 2026 blended CI (V2 workbook) was built on the right basis (`I19 = C11*F7`, "Remaining Emissions to Allocate" = embodied only). On W4 the June and February totes overstated production emissions by 219.64 kg (package versions) or 223.58 kg (linked sheets, blend rebuilt); the same constants appear in INJ-08-2026-W5 (QOWV and WODO), INJ-09-2026-W1 WODO, W2 QOWV and W3 QOWV. Local copies of the Jul-Dec 2025 summaries use `C9*F7` too; on the 2026-10-06 Ops Notes exports that reaches the 2025 QOWV product in W5, W2 and W3 (estimate about 726 kg).

**Mitigation / detection:** for every monthly CI a batch uses, open its summary and read the I19 formula. `C11*F7` (after BCUs) is correct; `C9*F7` is a FAIL on 7.2 whenever the month has BCUs applied to biomass transport (C10 > 0); with C10 = 0 the two formulas give the same figure (e.g. May 2026, C9 = 0). In each summary C10 = SUM(C5,C7) (process + handling) and C11 = C9-C10 (embodied). Recompute the CI with I19 = C11 and quantify the change. Embodied biomass transport is never offset and must stay in. Two versions of the Jan-Jun 2026 summaries exist: the Google Sheets the Ops Notes link, and the July RP package versions reworked 2026-08-11 that the blend was built from; check which one a CI comes from.

**Scope limit (Max, 2026-10-07):** the rule above does NOT reach back into CIs already used in verified statements. The W4 7.2 finding asked to recalculate the June and February 2026 CIs, which had already gone through verification earlier in the year. I had put the rule to Max as a general question about BCUs and never said that applying it meant re-valuing verified statements. He dropped the finding: "You did not ask whether we should go back and re-value already verified statements from earlier in the year, and that is in fact what responding to this would entail." Raise this check only on a CI not yet used in any verified statement, and when asking Max for a ruling, state what the ruling would force before asking.

---

## FC-C14 — Using COBB as a cross-check (INJ-09-2026-W4-QOWV 2.3)

**The rule (Max-stated, 2026-10-07):** "On COBB, I defer to Garrett. He works directly with the team that uses COBB and I do not, so if they have changed up he would know that first." Garrett's recorded position (#team-mrv-alerts, 2026-10-05): "COBB is not source of truth heree" (W2 QOWV) and "cobb not source of truth here" (W3 QOWV).

**The failure:** a conflict between the Ops Notes and the injection tracker's COBB tabs (consumed quantity, injection entries) was graded as a Fail. COBB is not a record that can contradict the ledger.

**Mitigation / detection:** read COBB if the step list asks for the injection record, but do not raise or grade a finding on COBB alone. A conflict counts only when a source of record disagrees: Ops Notes, the BGN inventory (Q4 production tab), or the production system's own weighing (Oil_inventory_data, Historical Tote Record). The order among those three is not yet ruled; Garrett's view is "BGN Inv takes precedent over oil inv data" (routed to Max 2026-10-05).

---

## Cross-cutting FCs reused from AECN / Kerry

These apply identically to Charm batches; see the AECN/Kerry skills' `lessons_learned.md` for full text:

- **"Verify X" Cop-Outs** — Checklist reports completed work, not instructions
- **Treating Feedback as Case-Specific** — Extract the universal principle and apply everywhere
- **Process Conversations in QA Output** — No "Per Max:" citations; evidence comes from documents
- **Wrong FAIL/FLAG Classification** — Missing evidence = FAIL
- **File Metadata as Evidence** — File sizes never count
- **Not Reading the Certify Sources List** — the Certify API dump's `sources` list is the authoritative inventory (removal-level sources unlinked to any datapoint are not visible via the API: check Drive, then Fail as before, with a note to confirm on the Sources tab)
- **Pre-Flight Gate Skip** — Skipping the lessons-learned read causes the next session to re-make a logged failure

---

## How to add a new Failure Category

When a real session surfaces a new failure mode:

1. Number it FC-C-N (next sequential)
2. Write: The failure / Why it happens / Mitigation / Detection
3. Add it to the print-to-chat list in the Pre-Flight Gate
4. If the failure could have been caught by a check in `checklist_structure.md`, update that item too — `lessons_learned.md` is the registry of failures, `checklist_structure.md` is the prevention layer
