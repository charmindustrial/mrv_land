# INJ-09-2026-W3-AECN — Gate 3 resolution

Reviewer file: adversarial_review.md (independent agent, 2026-09-29). Status rows at review: 62 (57 Pass/Fail/Flag + 5 N/A). Challenged 9, confirmed 53. Every challenge below was checked against its source before the checklist changed.

| Row | Reviewer | Resolution | Evidence checked this session |
|---|---|---|---|
| 2.3 | Keep Fail; direction claim wrong | Accepted. Direction sentence replaced with Charm's published method: KL720 standard 29,645 lb gives 19,502.18804 kg, 2.26796 kg below the credited 19,504.456 kg. Fix routes stated. | VVB Guidance August 1 - August 31 (1_dYfx8sZERQI5fMPAtIaOsYNE5aQupm7AYHoIFsEH7Y), Trailer Standard Empty Weight section: "KL720 8 29,515 130 29,645"; trigger "(b) the empty ticket’s tractor and/or trailer do not match the Full ticket". Log: vvb_guidance.august_standard_tare |
| 2.5 | Settle one correction location | Accepted. Recorded rule "FC11 reconciliation lands on the RP's *last-reported* batch from a given railcar — not necessarily the railcar's *physical-last* batch" places it on W3 offload 2 (20,971.92816 kg). Fail kept on W3; row says the correction is made once and the other week's finding closed; W2 M12 caveat added. Out-of-order offload table raised in the delivery message, as the same rule requires. | memory feedback_railcar_last_offload_signal.md (read); W2 live Ops Notes M12 (export 2026-09-29); W2 Certify data pulled today (adversarial_review_W2_certify_graphql_2026-09-29.json: Mass of Injectant 211.2522262 t, rail mass 155.86328 t) |
| 3.3 | Flag → Fail | Accepted. SHPX215046 fails the railcar-level check literally. "Would not show" sentence removed (multi-week clause keeps SHPX215046 on W2's metric-ton basis). Guidance-basis losses 1,480.54 / 1,575.01 kg and the SHPX215046 rail allocations added. | vvb_guidance.quote_multi_week; _derived_values.guidance_basis_loss_calc; Ops M32/M33 |
| 8.3 | Flag → Fail | Accepted. H11 = 0 against W2's 35,652.3312 kg misstates the attached railcar balance. | w2_live_ops.F12; ops_notes.railcars |
| 9.6 | Keep Fail; fix must not round | Accepted. Fix is the exact process figure 14,634.650 kgCO2e; targets after the 2.5 and 2.3 corrections added (14,633.144 / 14,632.976). | memory project_bcu_reduction_cap_policy.md: "fix = enter the exact process figure, never round down either" |
| 7.3, 7a.3, 9.8 | Discount can be re-derived | Accepted. Recompute section 8 reproduces 1.5577199676 t independently; 9.8 net now 248.327129 t with the discount re-derived on the corrected mass (1.553904 t). | recompute_output.txt section 8 and CORRECTIONS |
| 8.1 | Keep Flag; add empty ticket | Accepted. TILX200231 offload 1 empty (steer 3,880, drive 16,900 lb) added with the ticket's certification sentence. | tickets/Full_Ticket_Rail_GPRX5102_8.5.2026_offload_2.pdf: "The GROSS WEIGHT is the CERTIFIED WEIGHT and was weighed on a full length platform scale." |

Observations:
1. R&D removal has no record behind it: verified (only Q4, R4, Q5, K45/K46 mention it; September guidance silent). Added to 2.7.
2. Railcar losses carry no upstream emissions (0.042411 t): verified; August spill precedent quoted. Added as sidebar S.2 (Flag).
3. PO pages ship to El Dorado, KS: verified on BOL_2456-R and BOL_2470-R page 5. 1.5 → Flag; 3.7 updated.
4. M10 "lb" for a kg field: verified on BOL_2457-R page 2 ("Tanker Tare wt(empty) (Kg)"). Added to 3.7.
5. "(Sat)" week labels on Fridays: verified (2026-09-11 and 2026-09-18 are Fridays). 5.1 → Flag.
6. Knowledge base and checklist_structure 6.4 still give 0.10402 as the AECN process factor: reference-document staleness, not a batch finding; reported separately.
7. W2 still open in Certify with raw offload 4: used in 2.5.
8. Dependency thread: recompute CORRECTIONS section gives every downstream figure for corrections A, B, C in one pass.


Addendum 2026-09-29T23:11:50Z: 2.5 settled by the MRV lead's ruling that the back-calculation applies to the last load. The cut goes on SHPX215046 offload 4 (booked in W2, 14,821.22064 kg); W3's offloads 1-2 stay raw. 2.5 and 3.3 moved to Flag pointing to W2; 8.3 stays Fail with the corrected H11 target (35,632.0216 kg after W2's fix); 9.6 and 9.8 figures updated (recompute CORRECTIONS A and B). Counts now 35 Pass / 9 Fail / 14 Flag / 5 N/A.

Addendum 2026-09-29T23:29:01Z: custody ruling — upstream emissions of all oil in Charm custody are netted against removals. The 186.38656 kg railcar losses carry 0.042411 t uncharged (pyrolysis 0.029501, truck 0.002290, rail 0.010620): 6.6, 7.2, 8.2 and 9.2 now Fail; S.2 removed; 9.6 BCU ceiling 14,647.560 kgCO2e once charged; 9.8 net 248.297628 t. Counts 31 Pass / 13 Fail / 13 Flag / 5 N/A.
