# Batch 2-188 Adversarial Review

Independent challenge of every Pass/Fail/Flag/N/A on the Batch 2-188 QA checklist before delivery to Max. Per FC10, every challenge cites a specific source-read log key.

---

## 1. BCU Finding — Pressure Test

**Headline math.** ✓ Confirmed.
- 5.582 − 1.129 = 4.453 t excess [log:certify_components.BCUs_Applied_to_Bio_Oil_Transport_Process_Process.bcu_minus_transport_process_excess_t = 4.453].
- 2-188 transport process: 0.187 + 0.867 + 0.075 = 1.129 t [log:_derived_sums.transport_process_total_t = 1.129].
- Net inflation: actual 25.504 t vs sister-pattern-expected 21.051 t → 4.453 t over-credit, 17% [log:_derived_sums.net_tco2e_independent_recalc_displayed_form, expected_net_if_bcu_matched_transport_process_t].

**Sister pattern claim.** ✓ Confirmed.
- 2-186 BCU=1.621, 2-187 BCU=1.612, 2-189 BCU=1.617 [log:sister_batch_bcu_pattern]. Verified directly from Certify components view per log note.
- 2-189 transport breakdown 0.268+1.242+0.107 = 1.617 t [log:_derived_sums._2-189_transport_process_breakdown_t.sum] — exact match to its BCU. So "BCU = transport process" is verified, not assumed, on at least 1 of 3 sisters with reads recorded.

**Alternate hypotheses tested.**
- ✗ "5.582 covers the railcar's TOTAL transport process." Sum of sister-pattern BCUs = 1.621+1.612+1.617+1.129 = 5.979 t. 2-188's 5.582 ≠ 5.979, so it isn't a railcar-aggregate roll-up either. Hypothesis rejected.
- ✗ "Mass uncertainty value 5,581.52 kg is the modal kg display being misread." Per [log:certify_components...value_kg = 5581.52, value_t = 5.582], both kg and t representations are explicit and consistent with each other (5,581.52 / 1000 = 5.582). Not a unit-of-display misread.
- ⚠ "Wrong certificate linked." Plausible. BCU file is **Charm-A4-2024-10-24-63-1976.pdf** [log:certify_sources_full_enumeration], whereas sisters use **Charm-A3-2024-10-24-64-1976.pdf**. Different certificate batches almost certainly carry different baked-in tCO2e values. This is exactly the kind of allocation error that produces this signature.

**Verdict on the BCU finding:** Math is right, sister pattern is solid, no alternate hypothesis rescues 5.582 t as legitimate. The 7.4 / 8.1 / 9.5 / 9.8 Fails are warranted. **CONFIRMED.**

---

## 2. FC11 Last-Offload Policy

✓ Confirmed.
- 80,610 − (21,854.06 + 21,736.13 + 21,799.63) = 80,610 − 65,389.82 = 15,220.18 kg [log:scale_tickets.fc11_policy_check_result; ops_notes.railcar_balance_check].
- Sum of 4 offloads = 80,610.00 kg = exact BOL aggregate [log:ops_notes.railcar_balance_check.sum_of_4_offload_cargo_kg].

⚠ **One challenge worth surfacing.** The "is 2-188 actually the last physical pull" question. The log evidence [log:is_last_offload_evidence] is that 2-188's Ops Notes file shows all 4 offload rows populated and 2-189's shows the 4th row blank. That is operator-side workflow evidence, not a physical timestamp. The consumed_lot suffix `_offload_4` matches 2-188, but Max's prior memory note (per the prompt) flagged that suffix can be misleading. Per FC10, no log key records the actual physical chronology, so I can't escalate this further — but it's worth Max confirming with Garrett that 2-188 was physically the last truck pulled from TIMX201060 before the FC11 back-calc lands on this batch's removal. If it was actually 2-189 that was last, the policy belongs on 2-189's Cargo (kg) and 2-188's would revert to raw 16,274.88 kg — material direction-of-error: ~1,055 kg of mass would shift, with downstream ripple through Sequestrations / transport / pyrolysis / uncertainty on both batches.

---

## 3. Scale Ticket Reads

✓ Confirmed. All values reconcile.
- Full ticket #1312226091780, axle sum 10,200+27,880+27,500=65,580 = certified gross [log:scale_tickets.full_ticket].
- Empty ticket #1312226091790, axle sum 9,700+11,640+8,360=29,700 = certified gross [log:scale_tickets.empty_ticket].
- Net 35,880 lb × 0.453592 = 16,274.88096 kg ✓ [log:scale_tickets.computed_net_kg].
- Both tickets at Pilot Bunkie LA scale 3122, dated 4-01-26, Tractor CH1 / Trailer KL-192. Tractor/trailer match across both events.

---

## 4. FC9 Conservatism Precondition

✓ Confirmed. N_offloads (4) ≥ N_inbound_BOLs (3) [log:ops_notes.fc9_conservatism_precondition_check]. Per-leg ±72.57 kg framing is conservative. Section 7a Pass values are valid.

---

## 5. Hygiene FLAGs (5.4 + 9.9 and the 2.7 FLAG)

✓ Classifications correct.
- 5.4 / 2.7: COBB row 65 carries TWO stale values — origin_quantity_kg = 71,010 (pre-correction) AND offloaded_quantity_kg = 5,620.18 (pre-correction policy back-calc against the old 71,010 BOL aggregate) [log:cobb_2-188_row, cobb_stale_value_explanation]. Verifier reads Ops Notes / Certify (post-correction 80,610 → 15,220.18). Garrett-side data-provenance flag, not verifier-impacting → FLAG correct.
- 9.9: 4 generic filenames (consistent with sisters) — KB explicit "Generic or non-descriptive filenames are a FLAG, not a FAIL" → FLAG correct.

---

## 6. Component Math Recompute

All independent recalcs verified to match Certify display.

| Component | Calc | Result | Certify | Match |
|---|---|---|---|---|
| Sequestrations | 15.02384 × 0.42 × 3.667 | 23.139 t | 23.139 | ✓ |
| AECN→SOPOR truck process | 15.220179 × 107.5 × 0.0001143 | 0.1870 t | 0.187 | ✓ |
| SOPOR→Opelousas rail process | 15.220179 × 2199 × 0.0000259104 | 0.8672 t | 0.867 | ✓ |
| Opelousas→Basco truck process | 15.220179 × 42.9 × 0.0001143 | 0.0746 t | 0.075 | ✓ (round) |
| Pyrolysis process | 15.220179 × 0.10402 | 1.5832 t | 1.583 | ✓ |
| Pyrolysis embodied | 15.220179 × 0.02116 | 0.3221 t | 0.322 | ✓ |

[log:certify_components.* independent_recalc fields all align].

---

## 7. Other Anomalies

⚠ **9.6 worth a second look.** 9.6 is currently Pass on the rationale "BCU 5.582 ≥ transport process 1.129, KB rule satisfied" [log:certify_components, KB Section 7a]. Strictly, the KB rule says "BCU MUST equal or **exceed** corresponding activity emission." So technically Pass. But given that the OVER-application is the headline material finding flagged as Fail on 9.5 / 7.4 / 8.1 / 9.8, leaving 9.6 as Pass-with-note is consistent — the rule is met, the magnitude is wrong elsewhere. No change.

✓ All other items: 23 sources / 18 unique files / 15 datapoints — counts internally consistent [log:certify_sources_tab_total, certify_sources_tab_unique_files, certify_datapoints._note_count]. Filename "-T" inconsistency on 2314-R is a known recurring sister-batch flag, not new.

✓ FC9 Section 7a uncertainty values verified per discrete-weight count = 1 → ±72.57 kg correct on every mass-input leg.

---

## Final Verdict

**DELIVER AS-IS.** 

The headline BCU material finding (4 rows: 7.4 / 8.1 / 9.5 / 9.8) is rigorous and survives every alternate-hypothesis test attempted within the recorded log. Math is exact. Sister pattern is verified-by-direct-Certify-read on 2-186/2-187/2-189. Source-file divergence (Charm-A4 vs Charm-A3) corroborates that this is a wrong-certificate-linked allocation error, not a phantom.

One soft escalation for Max's awareness when delivering: the chronology assumption that 2-188 is the physical last offload rests on Ops Notes row-population state, not on a recorded physical-chronology source. If Garrett confirms physical order differs, the FC11 policy lands on a different batch and 2-188's mass values would shift. Worth one sentence in the Slack thread to Garrett alongside the BCU question.
