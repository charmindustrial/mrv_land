# Adversarial Review — INJ-08-2026-W4 (AECN rail)

## Step 0: Primary Source Verification Check
All 55 rows checked against the requirement that evidence notes contain values that could only come from directly opening the primary source.
- Scale tickets (2.1-2.4): all 8 tickets individually opened via CAT Scale OCR text layer this session; tractor/trailer/gross weight/date read from the actual filled-in ticket text, not template labels. PASSES primary-source check.
- COBB (5.4, 5.6): tab named, cell A confirmed = batch ID before extraction, row numbers (609-612) cited. PASSES.
- Uncertainty (7a.1, 7a.2): 6 component modals opened individually, ± values read directly from each modal's INPUTS section and cross-tabulated. PASSES.
- No item found with "not verified," "deferred," or "match assumed" language substituting for actual verification.

## Step 1: Independent recomputation (spot-checked highest-risk items)
- 2.4 net mass, offload_1: (71,400-28,580) lb × 0.453592 = 19,422,809,440 / 1,000,000 = 19,422.80944 kg — long-multiplication redone independently, matches exactly.
- 2.4 net mass, offload_3: (77,960-29,400) × 0.453592 = 22,026.42752 kg — matches exactly.
- 7.1/9.1 gross CO2e: 76,566.28926 × 0.404 × 3.667 = 113,430.5074 kg = 113.4305 t → rounds to 113.431 (4th decimal is 5 followed by non-zero digits, rounds up). Matches Certify.
- 6.4/9.4 pyrolysis process: 77.71845 t × 0.13711712584901084 = 10.65652 t → rounds to 10.657 (4th decimal 5, followed by 2, rounds the 3rd decimal up). Matches Certify. Cross-checked the EF itself: 0.13711712584901084 truncates to 0.1371171 at 7 decimals, exactly matching the VVB Guidance's stated factor (0.0040651+0.1330520=0.1371171) — independently reconciled from two different primary sources (Certify modal + VVB Guidance doc), not just one.
- 9.2 SOPOR-Opelousas rail process: 77.71845 t × 2,199 mi × 0.02591 kg/(t·mi) = 4,428.09 kg = 4.428 t. Matches Certify exactly, redone independently.
- 9.2 AECN-SOPOR embodied: 321.0889211 mi × 0.23756 kg/mi = 76.28 kg = 0.076 t. Matches Certify, confirms the aggregate-vs-single-leg distance selection logic (embodied uses aggregate vehicle-miles, process uses single-leg distance × mass) is applied correctly rather than assumed.

No arithmetic error found in any recomputed chain.

## Step 2: FAIL vs FLAG classification test applied to every non-Pass row
- 3.7 (BOL date discrepancy): mass/routing unaffected, matches an established FLAG-tier precedent (batch 2-181) — correctly not a FAIL.
- 5.5 (pH gap): pH is not a Certify datapoint (confirmed absent from the 16 enumerated datapoints) — does not risk misstating the reported value — correctly FLAG not FAIL.
- 7.4 / 9.8 (0.001t rounding gap, RP-level deferral): both trace to a documented, immaterial cross-tab display rounding artifact and an open reporting period — correctly FLAG, not FAIL (no risk of material misstatement — 0.001t on a 100.274t removal is ~0.001%).
- 9.9 (one generic filename among 26 sources, redundant with a descriptive file already covering the same datapoint): correctly FLAG per the generic-filename-is-hygiene rule, not FAIL.
No FLAG identified that should have been a FAIL under the "would a VVB reviewer's confirmation of the reported value be at risk" test — in every flagged case the underlying reported number is independently reconstructable and correct.

## Step 3: N/A checks cross-referenced against oil type / delivery mode
- 4.5, 5.3, 5.7: AECN-only rail batch, no aqueous phase, density field expected blank — all correctly N/A per the documented AECN-specific rules.
- 8.3: railcar SHPX215076 has zero prior-week claims and is fully closed within this single week (verified via the Ops Notes cell comment on Previously Claimed = 0 and 4-of-4 offloads populated) — correctly N/A, not a skipped check (there is genuinely no cross-week inventory to reconcile, unlike sister batches with partial railcars).
- 9.3: no LCS component present in Certify Components tree (verified directly) — correctly N/A for AECN.

## Step 4: Checked for fabrication / unsupported claims
- No "per protocol" citation lacks a specific reference.
- No "historical data shows" claim lacks a dataset reference (carbon range cites MRV_AECN_Analysis.xlsx mean/SD/n explicitly, disclosed as carried forward from prior-session primary reads rather than re-opened this session — an honest disclosure, not a fabricated claim).
- Every EF cited traces to either a live Certify component modal read this session or the VVB Guidance document read in full this session — none traces only to SKILL.md.
- Both negative claims in the checklist (1.5 "no Vaulted references," 8.2 "no spill/loss events") are backed by a documented exhaustive read of the specific sources checked, not an unsupported absence assertion.

## Observations (not scope-expanding new findings, noted per protocol)
- The Scope row's disclosure of a second, out-of-scope "AECN Truck" removal for the same week is a good practice (avoids silently omitting a known adjacent removal) — no action needed since Max provided only the rail URL.
- The 1-day offset between the Ops week boundary (Sat 15 Aug) and the stated Certify period boundary (16 Aug) is the same pattern seen on the immediately prior weekly batch (W3: Ops week 8/8-8/15 vs Certify period 9-15 Aug) — a consistent, harmless calendar-convention artifact, not a period-misassignment risk (injection_completion_date, which governs period assignment, falls within the stated window on every offload).

## Conclusion
**0 items challenged. 55 of 55 rows confirmed** with independently reconstructed evidence (not rubber-stamped). Checklist is internally consistent, every Pass is grounded in a session-read primary source, every Flag reflects a real-but-immaterial finding, no Flag warrants escalation to Fail, no N/A is a disguised skip. Gate 3 complete, no revisions required to the checklist.
