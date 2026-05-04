# Batch 2-189 — Adversarial QA Review

**Reviewer:** Adversarial sub-agent
**Date:** 2026-05-01
**Subject checklist:** `Batch_2-189_QA_Checklist.xlsx` (51 Pass / 0 Fail / 2 Flag / 4 N/A)
**Net CDR under review:** 29.64 tCO2e (Certify rmv_1KQB5KCQG1S0JYZ2)
**Position in railcar TIMX201060:** consumed_lot offload_3 (3rd physical pull). Last-offload reconciliation belongs to 2-188 — NOT in scope here.

---

## 1. Challenged Items

### 1.1 — Item 7a.2 (Layer 2 — Correctness of ± values)

- **Current Status:** Pass.
- **Issue:** The evidence note says "±72.57 kg per discrete weight is the correct value on every leg (truck process + rail process + truck process)." That is **almost** right but glosses the KB's explicit wrinkle on the rail leg. KB Section 7a (lines 567–568) distinguishes the truck legs (one-vehicle / one-load → 72.57 kg) from the rail leg, where the rule is `72.57 × N_inbound_BOLs` (in-rule) or, as Charm actually books it, `72.57 × N_offloads` (out-rule). Per-offload framing yields 72.57 on a single offload only because Charm stripes the railcar's total uncertainty across offloads — it isn't "one discrete weight" the way the truck legs are. The evidence note conflates the two cases. Under the per-offload framing this is still numerically correct (72.57 on this one leg of this one removal); it is the *justification* in the note that is loose.
- **Log keys:** `certify_components.SOPOR_to_Opelousas_Rail_Process.mass_uncertainty_kg`; KB ref Section 7a.
- **Recommendation:** Keep status Pass (the value 72.57 is what Certify shows and is consistent with the per-offload accounting model documented in lessons_learned.md §11), but tighten the evidence note to say: "Truck legs: 72.57 kg = one discrete weight, direct KB rule. Rail leg: 72.57 kg per offload = the per-offload allocation of the railcar out-rule (72.57 × N_offloads), conservative iff N_offloads ≥ N_inbound_BOLs — precondition deferred to 2-188 QA." That matches the framing used elsewhere in the checklist (8.3) and avoids implying that the rail-leg datapoint is structurally identical to the truck-leg datapoint.

### 1.2 — Item 4.2 (Carbon content within expected AECN range)

- **Current Status:** Pass.
- **Issue:** Evidence cites "AECN expected range (mean 39.42%, ±2 SD ~27.2%-51.6%)". The source-read log records `lab_results.carbon_normal_range_2sd: "27.2-51.6 (mean 39.42, SD 6.09, n=285)"` — i.e., the agent has a documented range with sample size and SD. This is fine on its face, but the checklist note doesn't cite the dataset/source for the range (date updated, where it lives). Per skill doc, "expected range" claims need a documented source. Minor.
- **Log key:** `lab_results.carbon_normal_range_2sd`.
- **Recommendation:** Keep Pass; consider adding "(per AECN historical CHN dataset, n=285, recorded in source-read log)" so the range isn't a bare assertion to a downstream reader.

### 1.3 — Item 9.9 (Source-filename hygiene)

- **Current Status:** Flag.
- **Issue:** Three sub-findings bundled:
  1. Four generic/screenshot filenames — correctly Flag (matches skill doc: filename hygiene = Flag, not Fail).
  2. "Billing Truck 2314-T Corrections (1).pdf" filename "-T" suffix where COBB lists "2314-R" — correctly Flag (filename hygiene; content is the right BOL).
  3. Rail PROCESS EF datapoint sourced from filename "Standard Emission Factors + Calculations - 2026 Railcar **Embodied** Emissions.pdf". Same filename also linked to the rail Embodied EF datapoint. The agent flags this as "possibly wrong source link if PDF is single-tab." Per the source-read log, `ef_verification.rail_process` confirms the EF *value* (0.0259 / 0.0000259104) matches the 2026 GLEC value, so the EF itself is correct. The filename mismatch is a Flag-worthy hygiene issue: a verifier opening the PDF expecting Process-EF backup may only find Embodied data.
- **Log keys:** `certify_sources_full_enumeration` (entry for "Standard Emission Factors + Calculations - 2026 Railcar Embodied Emissions.pdf"); `certify_components.SOPOR_to_Opelousas_Rail_Process.ef_source_filename_concern`; `ef_verification.rail_process`.
- **Recommendation:** Keep Flag. The bundle is appropriately classified, but the third sub-finding deserves an explicit note that the PDF should be opened to confirm both Process and Embodied tabs are present — if only Embodied is in the file, the Process EF datapoint has no backing source and that escalates to FAIL. Suggest adding: "Action for Garrett: verify PDF contains both Process and Embodied tabs; if Process tab missing, re-export and re-link." This converts a vague hygiene Flag into a closeable action item.

### 1.4 — Item 5.4 (COBB origin_quantity_kg stale)

- **Current Status:** Flag.
- **Issue:** Note correctly identifies COBB row 66 origin_quantity_kg = 71,010 vs. corrected aggregate 80,610 kg, and correctly characterizes it as Garrett-side data-provenance (verifier reads Ops Notes / Certify, both of which use the corrected value). However, the agent should also have noted that COBB row 64 (sister batch 2-187) shows pH "33" instead of "3.3" per `cobb_sister_rows.2-187_row_64.ph_typo_flag`. That typo isn't on 2-189's row, so it doesn't belong on this checklist — but it confirms COBB has multiple data-quality issues across rail-sister rows and reinforces that the 71,010-stale flag isn't an isolated entry.
- **Log key:** `cobb_2-189_row.origin_quantity_kg`; `cobb_sister_rows.2-187_row_64.ph_typo_flag`.
- **Recommendation:** Keep Flag as-is on 2-189. The 2-187 pH typo is out of scope for this checklist (separate batch, separate row).

### 1.5 — Items 8.2 / 8.3 / 2.5 (Last-offload mechanics deferred to 2-188)

- **Current Status:** Pass.
- **Issue:** None — the deferral framing is correct per Max's reminder and per `ops_notes.railcar_balance_check.fc11_policy_check_result`. The 15.22 MT railcar imbalance noted in the source-read log is real, but it lives on 2-188 (the last/4th physical pull). 2-189 is a non-last raw-scale-ticket batch and is independent of last-offload reconciliation.
- **Log key:** `ops_notes.railcar_balance_check`; `cobb_sister_rows.2-188_row_65`.
- **Recommendation:** Keep Pass. **However**, I would add a one-line note on 8.3 explicitly stating "Max anticipated post-correction-policy outcome: 2-189 Cargo could re-baseline to ~31.4 MT (per 2-186 registry note); current Certify/Ops Notes/COBB all carry 21.8 MT and reconcile internally. If 2-188's reconciliation triggers a 2-189 Cargo refresh, this batch's Net CDR will recompute." This is documented in `is_last_offload_of_railcar_per_max_note_in_2-186` and the agent's note doesn't surface that contingency, which is exactly the kind of context Max said to refresh on at 2-189 QA.

---

## 2. Confirmed Items (independent verification)

- **2.1** — Both ticket pairs Read directly from JPG pixels per OCR-not-primary rule. Axle-vs-cert sums match (77,120 lb, 29,060 lb). Log: `scale_tickets.full_ticket`, `scale_tickets.empty_ticket`.
- **2.3** — Tractor CH2 / Trailer KL-188 on both tickets. Log: `scale_tickets.tractor_trailer_match`.
- **2.4 / 5.2** — Verified: (77,120 − 29,060) × 0.453592 = 21,799.63152 kg. Exact match to Ops Notes offload_3. Log: `ops_notes.offload_table.2.cargo_mass_kg`.
- **2.6** — Verified sparging: 21,799.63152 × 0.0129 = 281.21525 kg loss; 21,518.41627 kg post-sparge injectate. Exact. Log: `ops_notes.offload_table.2.sparging_loss_kg`.
- **3.5 / Allocations** — Verified allocation fraction 21,799.63 / 80,610 = 0.27043332 (Ops Notes 0.27043334, rounding-ok). Rail allocated = 2,199 × 0.27043334 = 594.683 mi; truck-1 allocated = 322.5 × 0.27043334 = 87.2148 mi. Exact match.
- **6.4 / 6.5 / 7.1 / 7.2** — Independent recalc reproduces Certify within rounding: gross seq 32.589 t, activities 4.394 t, BCU 1.617 t, net 32.589 − 4.394 + 1.617 − 0.171 = 29.641 t = Certify Net. Log: `certify_calculation_view.independent_check`.
- **8.1 / 9.2** — Rail embodied EF 0.03113 / 0.0000311307 confirmed as 2026 GLEC value (NOT stale 0.0352240 from 2-182). Log: `ef_verification.rail_embodied.fix_status`.
- **9.6** — BCU 1.617 t = exact sum of three transport process activities (0.268 + 1.242 + 0.107). Equality satisfies BCU ≥ activity rule. Log: `certify_components.BCUs_Applied_to_Bio_Oil_Transport_Process`.
- **All Pass items in Sections 1, 3, 4, 5, 6, 7, 7a, 9 not separately challenged above** — reviewed against source-read log entries and KB references; evidence notes contain the specific values needed to confirm primary-source verification.
- **All N/A items (4.5, 5.3, 5.7, 9.3)** — correctly N/A: AECN-only, non-aqueous, no LCS pre-treatment, density not collected. Log: `oil_type`.

---

## 3. Observations (not in scope of any checklist item)

- **Railcar mass-balance gap (15.22 MT) is real but not 2-189's burden.** `ops_notes.railcar_balance_check.unaccounted_kg = 15,220.18` reflects either (a) the 4th offload row needing population, (b) "Oil Left in Railcar" needing fill-in, or (c) Max's anticipated 2-189 Cargo re-baseline path. Belongs entirely on 2-188 QA. Calling out here so the parent agent can confirm 2-188 is queued.
- **Sister-batch contagion of stale COBB origin_qty.** Rows 63 (2-186), 64 (2-187), 65 (2-188), 66 (2-189) all carry origin_quantity_kg = 71,010 (pre-correction). Garrett-side cleanup; not verifier-impacting on any single batch since Certify uses Ops Notes Cargo, not COBB origin_qty.
- **Carbon uncertainty math sanity-checked**: 41.3 × 0.004 = 0.1652. Matches `certify_components.Injection_sequestration.carbon_uncertainty_pct`. Item 7a.1 evidence is supported.

---

## 4. Summary (≤600 words)

**(a) Adversarial findings.** I challenged five items. Four are evidence-tightening recommendations on already-correct status assignments (7a.2 framing is loose on the rail-leg uncertainty rationale; 4.2 should cite the carbon-range source; 9.9's third sub-finding needs a clearer Garrett action; 8.3 should surface the Max-anticipated 2-189 Cargo re-baseline contingency). One — 5.4 — is fine as-is. Independent recomputation of every numerical claim reproduced Certify exactly: 21,799.63 kg Cargo, 21,518.42 kg post-sparge injectate, 32.589 t gross seq, 4.394 t activities, 1.617 t BCU, 0.171 t uncertainty discount, **29.641 t Net = 29.64 displayed**. All EFs match the 2026 KB values (rail embodied 0.0000311307 confirmed corrected, not the stale 0.0352240 carried by 2-182). Allocation fraction 0.27043334 is internally consistent across rail-allocated mi (594.68), truck-1 allocated mi (87.21), and Cargo / corrected-BOL ratio (21,799.63 / 80,610). BCU offset = exact sum of three transport process activities. Tractor/trailer match confirmed via direct pixel Read. Three layers of Section 7a uncertainty all tie out (±72.57 kg, ±0.4% carbon, 171 kg aggregate discount).

**(b) Accepted vs rebutted.** Accepted (no change to status): 51 Pass, 4 N/A. The two existing Flags (5.4 COBB origin_qty stale, 9.9 filename hygiene) are correctly classified — both are process-hygiene issues with no risk of material misstatement under the FAIL-vs-FLAG test (verifier reads Ops Notes/Certify, both of which carry the correct corrected values). Recommended evidence-note tightening on 7a.2, 4.2, 8.3, and 9.9 sub-finding 3, but no status changes. No items downgraded; no Pass converted to Fail or Flag; no N/A converted to applicable. The agent's primary-source verification is demonstrated throughout — scale tickets Read from pixels (not Drive OCR), COBB row 66 navigated with cell-A and tab-name verification, every Section 7a component modal opened individually for ± value reads. No fabrication detected. No lazy notes detected. The deferral of last-offload mechanics (railcar mass balance, FC9 conservatism precondition) to 2-188's QA is correct per Max's framing and per the lessons-learned doc.

**(c) Recommendation.** **Proceed to Max review.** The checklist accurately reports a clean batch with two correctly-classified hygiene flags and zero material findings. Net CDR 29.64 tCO2e is supported by independent recomputation. The only caveat the parent agent should surface to Max is the contingency in 8.3: per Max's 2-186 registry note, this batch's Cargo could re-baseline to ~31.4 MT under post-correction policy at the time of 2-188's last-offload reconciliation. That isn't a 2-189 finding — it's a known-future path that 2-188 QA will resolve — but Max asked for a refresh on it at 2-189 QA, and the current checklist text doesn't mention it.
