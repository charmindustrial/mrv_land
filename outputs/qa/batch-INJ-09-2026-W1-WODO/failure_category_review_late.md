# INJ-09-2026-W1 WODO — Failure Category review (late)

Written 2026-09-29. The pre-flight step "print the applicable FCs to chat before Gate 1 begins" (skills/qa/batch-qa-charm/references/lessons_learned.md) was not done in the 2026-09-21 session. Each FC below is checked against the checklist (Charm_WODO_QA_Checklist_INJ-09-2026-W1.xlsx, revised 2026-09-29).

| FC | Applies | Checklist item and result |
|---|---|---|
| FC-C1 Standard Loss by oil type | Yes (WODO) | 2.3 Pass: F = D − E with E = $L$8 = 7.84 kg/tote; Standard Loss applied, as WODO requires |
| FC-C2 A period's emissions omitted | Yes (4 periods) | 7.1 Pass: Feb, Mar, May 2026 and July 2026 (blended CI) all carried in one aggregated component |
| FC-C3 Hard-coded allocation cells | Yes | 3.3 Pass: D12 '=$D$6', E12 '=IFERROR(D12/C12,"")', F12 '=$B$8', G14 '=SUM(G12:G13)' |
| FC-C4 LCS without component | No (WODO) | 9.1 N/A |
| FC-C5 Tote roster mismatch | Yes | 3.5 Pass: 13 of 13 tags, fraction, gross and period match the Q4 inventory tab; 2.1 Fail: 301257's gross is 1,120 kg on the Oil_inventory_data tab against 1,115 kg in the Ops Notes and Q4 tab |
| FC-C6 Non-longest route | Yes | 5.2 Pass: 1,201 mi, the longest of 1,132 / 1,129 / 1,201 |
| FC-C7 Mass of Load basis | Yes | 5.3 Pass: 14,926 kg = Total Mass Transported (gross) |
| FC-C8 Per-tote precision | Yes | 2.4 Pass: 13 × 1.13398 = 14.74174 kg |
| FC-C9 PP/PB wording, n=3 | Yes | Not raised anywhere in the checklist |
| FC-C10 Fraction CI cross-wiring | Yes | WODO CIs used (Feb 0.8498961226, Mar 0.790064533, May 0.6328458891 = each summary's WODO row 2), not the Aqueous rows 4 (0.1330497939, 0.1185251532, 0.1106615762) |
| FC-C11 Invented vs stated rule | Yes | 8.1: BCU 2,481 kg against process 2,480.9758 kg, graded Pass on 2026-09-21 under the older "equal or exceed" wording; regraded Fail 2026-09-29 under the stated rule that a BCU must not exceed the emission |
| FC-C12 Dominant input uncertainty | Yes | 7.5 Pass: pyrolysis mass carries ±14.74 kg |

Cross-cutting FCs (lessons_learned.md, "Cross-cutting FCs reused from AECN / Kerry"):

| FC | Checklist result |
|---|---|
| "Verify X" cop-outs | No row instructs a check instead of reporting one |
| Treating feedback as case-specific | The 2026-09-28 findings on INJ-09-2026-W3-QOWV (standard tare, BCU over-coverage) were applied here: 2.2 Flag, 8.1 Fail |
| Process conversations in QA output | No row quotes Max or cites a conversation |
| Wrong FAIL/FLAG classification | 2.1 graded Fail for a mass conflict between sources; 2.2 graded Flag for a label tare, per SKILL.md "Tare value from manufacturer label rather than measured = FLAG" |
| File metadata as evidence | No row relies on file size or date as evidence |
| Not reading the Sources tab | Sources tab read in the 2026-09-21 session, 6 sources enumerated |
| Pre-flight gate skip | The FC list was not printed before Gate 1; this file is the late substitute |
