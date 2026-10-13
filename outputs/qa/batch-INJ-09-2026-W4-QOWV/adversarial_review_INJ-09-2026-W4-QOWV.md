# Adversarial review — INJ-09-2026-W4-QOWV (Aqueous, Basco 6)

- **Checklist reviewed:** `Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W4.xlsx` (33 items: Pass 22, Flag 4, Fail 6, N/A 1).
- **Certify removal:** `rmv_1M3SG7D701S0HZ1Z`. Certify was not opened. Certify values below are the component reads recorded in the source-read log on 2026-10-06, cross-checked against the component totals saved in `certify_initial_snapshot.yml`.
- **Reviewer:** independent agent that did not build the checklist. Date 2026-10-06.
- **Read in this review:**
  - The skill files `adversarial-reviewer/SKILL.md`, `batch-qa-charm/SKILL.md` and `references/checklist_structure.md`.
  - The checklist and the source-read log.
  - The live Ops Notes export (formula and value loads, all tabs), and the Ops Notes copy attached in Certify.
  - The inventory master export (Q4 2025-2026 Production Inventory tab).
  - The live Standard EFs export and the attached EF copies.
  - The six live period summaries and the V2 blended-CI workbook.
  - The six period-summary copies V2 names, which the QA agent had not opened. They are on the Drive mount at `My Drive/MRV/Removals Reporting/2026/Verified Periods/July 1 - July 31 RP/Charm BO MRV/H1 2026 Charm CI/`.
  - The seven other weeks' Ops Notes.
  - The raw injection-tracker export behind `cobb_w4_aqueous_rows.json`: `outputs/qa/batch-INJ-09-2026-W3-QOWV/source_exports/bio_oil_injection_tracker_export.xlsx`, tab 'Basco Injection -- COBB', taken 2026-09-28 23:28.
  - The 2026-09-28 copy of the W4 Ops Notes.
  - The lab certificate PDF, the retirement certificate PDF, the routing-map image and the VVB Guidance text.
  - The batch registry `qa_active_charm_batches.json` and the W2 and W3 QOWV checklists, for precedent.
- **Arithmetic:** every derived figure is shown below as two-number steps.

## Summary of verdicts

| Item | Status | Verdict |
|---|---|---|
| 1.1 | Pass | Agree. Wording change: file size used as evidence |
| 1.2 | Pass | Agree |
| 1.3 | Flag | Agree |
| 2.1 | Pass | Agree |
| 2.2 | Flag | Agree |
| 2.3 | Flag | **Challenge: change to Fail.** The note must also explain the tracker's offset on every row |
| 2.4 | Pass | Agree |
| 3.1 | Pass | Agree |
| 3.2 | Pass | Agree |
| 3.3 | Pass | Agree |
| 3.4 | Fail | Agree on Fail. **Challenge: the COLA-40 part and every corrected figure built on it** |
| 3.5 | Pass | Agree |
| 4.1–4.3 | Pass | Agree |
| 4.4 | Fail | Agree |
| 5.1 | Fail | Agree. Wording change: the fix figure |
| 5.2–5.5 | Pass | Agree |
| 6.1 | Fail | Agree. Wording change: the corrected embodied figure |
| 6.2 | Pass | Agree. Wording change: the corrected figure |
| 6.3 | Pass | Agree |
| 7.1 | Pass | Agree |
| 7.2 | Fail | **Challenge: the evidence note and the fix.** The comparison is not like for like. Fail kept, on a different ground |
| 7.3 | Flag | Agree. Wording change |
| 7.4–7.5 | Pass | Agree. Per-period figures missing (low) |
| 7.6 | Pass | Agree |
| 8.1 | Fail | Agree. Wording change: the fix figure |
| 9.1 | N/A | Agree |
| C.1 | Pass | Agree on the as-submitted reproduction. **Challenge: the corrected net** |

---

## Item by item

### Batch folder (items 1.1–1.3)

**1.1 Pass — Agree (wording).** Lab certificate page 3 was read: SR26-05719.003, Client ID '9-2026-W4-QOWV', sampled 25-Sep-2026 10:00. It reports:
- Carbon 7.9 % (m/m), marked '#'
- Hydrogen 7.9 %, marked '#'
- Nitrogen <0.75
- Kinematic viscosity 0.9020 cSt
- Acid number 36 mg KOH/g
- Density 1.039 g/cm³

The density threshold traces to the knowledge base, line 313: "All streams exceed formation fluid density (1.01 g/cm³)". The note should cite it.

Change: the note matches the Drive Testing copy to the Certify copy by "same size" (48,654 bytes). batch-qa-charm/SKILL.md says "File sizes are never evidence." Instead, state three things: the Drive copy could not be downloaded (sign-in wall); its presence comes from the folder listing; and the Ops Notes Summary tab F20 link points at the same Drive file id `1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ`.

**1.2 Pass — Agree.** The Ops Notes QOWV tab ledger (A11:A52) is fully populated. The totals row of the same tab (B54, D54, F54, H54, I54, J54) are all live sums. Cell notes exist at Ops Notes AECN Truck tab H28 and Kerry tab D18, and nowhere else.

Sidebar addition: the Ops Notes 'WODO Shipments & EE Allocation' tab A1 also carries a stale header, "INJ-09-2026-W2 - WODO Shipments & EE Mileage". Sidebar B57 names the Whole Oil tabs and omits this one.

**1.3 Flag — Agree.** The Ops Notes 'QOWV Shipments & EE Allocation' tab has nothing below the A19 note and no check row. The Whole Oil allocation tab carries one at A16: "Check - every batch tote is allocated to a truck". checklist_structure.md lists "totes missing from tracker" as a Fail mode, but W3 graded the same gap Flag, so the grade follows precedent.

Helpful addition for Garrett: the W3 workbook's allocation tab (2026-10-06 export, `source_exports/prior_weeks/INJ-09-2026-W3_Ops_Notes.xlsx`) now carries a 'B. TOTE -> TRUCK' block from row 19, one row per tote. That is the layout W4 needs.

### Ops Notes (items 2.1–2.4)

**2.1 Pass — Agree.** The 42 gross values on the Ops Notes QOWV tab re-sum to 42,945.0 kg, equal to B54. All 42 equal the inventory master's Gross Weight for the same tag.

**2.2 Flag — Agree.** Ops Notes QOWV tab column C reads 57.6 kg on all 42 rows, and the master's Tare Weight is 57.6 for all 42 tags. checklist_structure.md: "Tare value from manufacturer label rather than measured = FLAG". W2 and W3 gave the same grade.

**2.3 Flag — CHALLENGE: change to Fail, and add two points to the note.**

What I verified:
- Ops Notes QOWV tab F = IF(E="","",B−E) on all rows, and F54 is 34,179.5 kg.
- In the tracker export, row 871 (tote 301215) reads 821.4 kg and row 885 (tote 301274) reads 852.9 kg.
- Implied post-unload weights, using the ledger gross:
  - Tote 301215: 1041 − 57.6 = 983.4, then 983.4 − 821.4 = 162.0 kg. The Ops Notes QOWV tab E26 reads 442.5.
  - Tote 301274: 1036 − 57.6 = 978.4, then 978.4 − 852.9 = 125.5 kg. The Ops Notes QOWV tab E40 reads 169.5.
- The 2026-09-28 copy of the W4 Ops Notes has zero cell differences on the QOWV tab.

Grading:
- batch-qa-charm Status Definitions place "conflicting evidence" under Fail.
- adversarial-reviewer/SKILL.md: "Any issue where the evidence says something different from what's being reported (e.g., vehicle identifiers don't match, mass values conflict between sources, emission factors misapplied) is a FAIL".
- The checklist grades 4.4 Fail although that error is conservative. 2.3 stands on the same footing: two records give different post-unload weights for the same two totes.

Addition 1, the open question for Max. The registry's W2-QOWV notes (2026-10-05) read: "COBB doubled rows: Garrett says COBB not source of truth." This is Garrett's position and has not been ruled on. If Max adopts it for QOWV masses, the tracker comparison moves to the sidebar, and 2.3 rests on the 442.5 kg value that tote 301215 shares with tote 301166.

Addition 2, the tracker's offset on every row. 39 tracker rows equal the ledger's injected mass less 57.6 kg, counting row 896 against tote 300022. Row 867 (tote 301204) reads 1540.8; 1540.8 ÷ 2 = 770.4, and the ledger gives 828 − 57.6 = 770.4. So with that row's doubling removed, 39 + 1 = 40 rows are 57.6 kg low. Put arithmetically, the tracker equals (B − 57.6) − E, which takes the tote tare off a second time.

The two exception rows differ from the ledger by 821.4 − 598.5 = 222.9 kg (above it) and 866.5 − 852.9 = 13.6 kg (below it). Net gap to the ledger:
- 40 × 57.6 = 2304.0
- 2304.0 − 222.9 = 2081.1
- 2081.1 + 13.6 = 2094.7 kg below the ledger
- 34179.5 − 2094.7 = 32084.8 kg on the tracker
- 2094.7 × 0.079 = 165.4813, then 165.4813 × 3.667 = 606.82 kg CO2e of sequestration

Sidebar B61 mentions the pattern, but the note gives no reason for trusting the tracker on two rows while setting aside its offset on all of them. Add one sentence giving the reason.

**2.4 Pass — Agree.** 2.5 × 0.453592 = 1.13398, and 42 × 1.13398 = 47.62716 kg, equal to Ops Notes QOWV J54. On the skill's ÷ 2.20462 form: 2.5 ÷ 2.20462 = 1.1339823, and 42 × 1.1339823 = 47.6273. That is within ±0.01.

### Allocation tab (items 3.1–3.5)

**3.1 Pass — Agree.** The master's Ship Status for the 42 tags gives COLA_37 15, COLA_38 5, COLA_39 20 and COLA_40 2, equal to Ops Notes allocation tab D12:D15. I scanned all seven other weeks' Ops Notes myself (every tab and cell) for the 42 tags and found none.

**3.2 Pass — Agree.** My own comparison against the master: tag, fraction (QOWV), gross mass and production period agree on 42 of 42, and no tag appears twice.

**3.3 Pass — Agree.** Formula load of the Ops Notes allocation tab:
- E12:E15 `=D/C`
- F12:F15 `=$B$8`
- G12:G15 `=E*F`
- G17 `=SUM(G12:G15)`
- D6 `=COUNTA(QOWV!A11:A52)`

**3.4 Fail — Agree on Fail. CHALLENGE: the COLA-40 part and the corrected figures.**

The COLA-38 denominator is wrong, and that alone supports the Fail:
- In the master, Ship Status COLA_38 has 18 totes (12 Whole Oil, 6 QOWV), all shipped 2026-09-10.
- The INJ-10-2026-W2 Whole Oil allocation tab E6 reads "COLA_38 = 3 of 18 totes on the truck (12 DC Whole Oil + 6 BGN QOWV". INJ-10-2026-W3 uses 5 of 18.
- W4's Ops Notes allocation tab C13 reads 6.
- Shares claimed on that one truck: 5 ÷ 6 = 0.8333333333, 3 ÷ 18 = 0.1666666667 and 5 ÷ 18 = 0.2777777778. Then 0.8333333333 + 0.1666666667 = 1.0000000000, and 1.0000000000 + 0.2777777778 = 1.2777777778.

The COLA-40 count of 18 in Ops Notes allocation tab C15 is the documented physical count, not an error. The tab's A19 note reads: "physical counts are COLA-40=18/COLA-41=20". It adds: "only the COLA-40 Total-Totes-on-Truck denominator above uses the physical count (18)". And: "Live master now shows COLA-40=17/COLA-41=20 -- one short of the stated physical 18/20; flagged for Garrett to reconcile upstream." The master today shows COLA_40 17 and COLA_41 20.

batch-qa-charm/SKILL.md, Gate 1, step 0: "Any figure that does not tie to a source document may be a documented substitution — check the annotation before calling it an error." The 18 is annotated. The master is the record that is one short; it needs reconciling as a request, not as a correction to the tab.

Corrected allocation (C13 to 18, C15 kept at 18):
- 5 ÷ 18 = 0.2777777778, and 0.2777777778 × 1201 = 333.6111
- 2 ÷ 18 = 0.1111111111, and 0.1111111111 × 1201 = 133.4444
- 900.75 + 333.6111 = 1234.3611
- 1234.3611 + 1201 = 2435.3611
- 2435.3611 + 133.4444 = **2568.8055 mi**
- 3236.0278 − 2568.8055 = 667.2223 mi over-allocated on the tab

The checklist's 2576.6552 mi uses 17: 2 ÷ 17 = 0.1176470588, 0.1176470588 × 1201 = 141.2941, and 2435.3611 + 141.2941 = 2576.6552. Carry it as the alternative if the master's 17 proves right.

The note should also say the tab's 6 over-charges W4, so the error is conservative for this batch. Carry the new figure into 6.1, 6.2 and C.1.

**3.5 Pass — Agree.** Same 42-of-42 match on all four attributes as 3.2. The master rows for the 42 tags run from 410 to 741.

### Injection sequestration (items 4.1–4.4)

**4.1 Pass — Agree.** Certificate 7.9 % equals Certify 7.9 %, which equals Ops Notes Summary tab E20 0.079.

**4.2 Pass — Agree.** The Carbon Content datapoint is linked to the certificate PDF and the Ops Notes (log key `certify.attachment_map`). The attached Ops Notes copy has zero cell differences from the live export on the QOWV, allocation and Summary tabs (formula load, compared both directions).

**4.3 Pass — Agree.** Certify's 34,179.5 ± 47.62716 kg equals Ops Notes QOWV J54.

**4.4 Fail — Agree.**
- Expected value: 0.004 × 7.9 = 0.0316. Certify carries 0.03523: 0.03523 ÷ 0.0316 = 1.114873, so 11.4873 % high.
- Supporting ESTIMATE, from the discount by variance propagation, combining terms as the square root of the sum of squares:
  - Mass term on sequestration: 0.079 × 3.667 = 0.289693, then 0.289693 × 47.62716 = 13.7973.
  - Carbon term: 34179.5 × 3.667 = 125336.2265. Then 125336.2265 × 0.0003523 = 44.1560 at Certify's value, or 125336.2265 × 0.000316 = 39.6062 at 0.0316.
  - Transport term: 0.04762716 × 1201 = 57.20022, then 57.20022 × 0.1143 = 6.5380.
  - Pyrolysis term: 0.123623 × 47.62716 = 5.8878.
- Squares: 13.7973 × 13.7973 = 190.37; 44.1560 × 44.1560 = 1949.75; 39.6062 × 39.6062 = 1568.65; 6.5380 × 6.5380 = 42.75; 5.8878 × 5.8878 = 34.67.
- With 0.03523: 190.37 + 1949.75 = 2140.12; 2140.12 + 42.75 = 2182.87; 2182.87 + 34.67 = 2217.54. Square root 47.09, which matches Certify's 47 kg.
- With 0.0316: 190.37 + 1568.65 = 1759.02; 1759.02 + 42.75 = 1801.77; 1801.77 + 34.67 = 1836.44. Square root 42.85, which does not match.
- No cell in either load of the Ops Notes holds 0.03523 or 0.0003523, and the certificate states no uncertainty.
- Precedent: on INJ-08-2026-W5 WODO the registry records Garrett's reply: "4.4 is currently being fixed by Mangrove."

### Transport process (items 5.1–5.5)

**5.1 Fail — Agree. Wording change to the fix.** Standard EFs 2026 tab: F6 (Tanker) 0.0001143 and F7 (Flatbed) 0.0001384 MT CO2e/t-mi. The attached EF copy carries the same two values.

The component total saved in `certify_initial_snapshot.yml` (5.895 t) reproduces on the tanker factor: 42.945 × 1201 = 51576.945 t-mi, and 51576.945 × 0.1143 = 5895.2448 kg. The flatbed factor gives 51576.945 × 0.1384 = 7138.2492 kg.

Change: 7138.2492 kg holds on the sheet's factor. W2 and W3 instead used Certify's library factor (W3 note: "Component detail shows 'Flatbed, Northern America, WTW' at 0.086 kgCO2e/(km*t)"). On that factor:
- 1201 × 1.609344 = 1932.822144 km
- 42.945 × 1932.822144 = 83005.047 t-km
- 83005.047 × 0.086 = 7138.434 kg

That is 7138.434 − 7138.2492 = 0.1848 kg different, which affects the 8.1 fix.

**5.2 Pass — Agree.** The routing-map image shows three routes: via US-287 S 1,132 mi; via US-287 S and I-20 E 1,129 mi; via I-70 E 1,201 mi. Certify uses 1,201, the longest. The origin reads 'Your location'; Max's ruling on INJ-07-2026-W1 for this same map is recorded in the registry.

**5.3 Pass — Agree.** Certify's 42,945 kg equals Ops Notes QOWV B54.

**5.4 Pass — Agree.** The Ops Notes is linked to the Transport Mass datapoint (log key `certify.attachment_map`).

**5.5 Pass — Agree.** Certify's 47.627 kg is the display rounding of 47.62716.

### Transport embodied (items 6.1–6.3)

**6.1 Fail — Agree. Wording change.** Standard EFs 2026 tab: F11 (Tanker) 0.0002375605888 and F12 (Non-Tanker) 0.0001927908256 MT CO2e/mi. The snapshot total of 0.769 t reproduces on the tanker factor: 3236.03 × 0.23756 = 768.7513 kg. Non-Tanker on the same miles gives 3236.03 × 0.1927908256 = 623.8769 kg. W3's 6.1 was a Flag because the value there was right and the label wrong; here the value is wrong, so Fail is consistent.

Change: on the 3.4 correction, 2568.8055 × 0.1927908256 = **495.2421 kg**, in place of 496.7555 kg.

**6.2 Pass — Agree.** Certify's 3,236.03 mi equals the Ops Notes allocation tab G17, 3,236.027778, so the literal answer to the question is yes. W3 graded it Pass with the note "The Certify figure matches the tracker as submitted." alongside a 3.4 Fail, and W2 did the same.

This is consistent with 7.2 being a Fail. 3.4 tests the allocation inputs, and no item tests the CI inputs, so 7.2 carries them; W2 and W3 failed 7.2 for per-tote CI inputs.

Change: the corrected figure in the note becomes 2568.8055 mi.

**6.3 Pass — Agree on precedent.** W2 and W3 graded it Pass on the same basis. Nothing attached in Certify ties tags to trucks: the master is not attached, and the tab has no tote rows. 1.3 already carries this.

### Production emissions (items 7.1–7.6)

**7.1 Pass — Agree.** Per-period figures in the log match my recompute:
- June: 32 totes, 31,300.8 kg, 3,871.5855 kg CO2e
- July: 8 totes, 7,358.2 kg, 889.9522 kg CO2e
- February: 2 totes, 1,866.8 kg, 248.3774 kg CO2e

Certify: 40525.8 × 0.123623 = 5009.9211 kg, shown as 5.010 t.

**7.2 Fail — CHALLENGE: the evidence note and the fix. Keep Fail, on a different ground.**

What holds:
- Masses are identical in all six months. Unit: 241690.6 ÷ 1000 = 241.6906 t.
- Live: 30.886446606 ÷ 241.6906 = 0.1277933. V2 (log key `blended_ci_source`): 29.2318456 ÷ 241.6906 = 0.1209474.
- The Aqueous share (column R) is identical in each live summary and its copy, except March. March live: 5.533133432 ÷ 26.02926421 = 0.212574. March copy: 5.4427961 ÷ 25.67379126 = 0.211998. March WODO carbon content is 0.5106 live and 0.5134 in the copy.
- Ops Notes QOWV L13–L18 equal the live sheets.
- The registry for INJ-07-2026-W1 (2026-08-06) lists "Jan 2026 (6 totes, CI 0.931994)", which is the live January WODO value. So the live sheets already held today's figures before V2 read its copies.

What does not hold: the comparison is not like for like on basis. The 'Biomass Transport' line of each summary's emissions inventory is calculated two ways:
- **Copies** (Jan, Feb, Mar, Apr and Jun; May has no biomass transport): `I19 = C11*F7`. C11 is labelled 'Remaining Emissions to Allocate' and equals 'Total Emissions' (C9) less "BCU's Applied" (C10). In plain terms, the copies leave out biomass-transport emissions that BCUs covered.
- **Live sheets** (all six): `I19 = C9*F7`, the total before BCUs, under the header 'Consolidated Emissions Inventory (No GHG Neutralization)'.
- F7 is 1 in every month, in both versions.

Other differences, which are data revisions:
- March propane, cell I20: 17.33288553 in the copy, 15.57588484 live.
- May waste disposal, cell I27: 0.195401 in the copy, 0.858215 live. Cell C85 changed from 0.073646 to 0.73646.

Basis effect on Aqueous (live column R share × live C10, by month):
- Jan: 0.2244836035 × 2.369484895 = 0.531911
- Feb: 0.2172032236 × 1.703110865 = 0.369921
- Mar: 0.2125735629 × 2.112208715 = 0.449000
- Apr: 0.2243270523 × 0.9139 = 0.205012
- Jun: 0.2104968588 × 1.407746656 = 0.296326
- Running total: 0.531911 + 0.369921 = 0.901832; 0.901832 + 0.449000 = 1.350832; 1.350832 + 0.205012 = 1.555844; 1.555844 + 0.296326 = **1.852170 MT**

Live data on V2's basis: 30.886446606 − 1.852170 = 29.034277 MT. Data revisions alone: 29.034277 − 29.2318456 = −0.197569 MT.

CI on V2's basis with today's data: 29.034277 ÷ 241.6906 = **0.1201299**. That is below the 0.120947 applied: 0.120947 − 0.1201299 = 0.0008171, and 7358.2 × 0.0008171 = 6.0124 kg. On V2's basis, the July totes are over-charged.

The finding is that the ledger mixes two bases. June and February totes carry before-BCU CIs; July totes carry an after-BCU CI. Whichever basis governs, one group is off.
- **All totes before BCUs:** +50.3767 kg (the checklist's figure), giving 5009.9151 + 50.3767 = 5060.2918 kg.
- **All totes after BCUs:**
  - June: 27.39205851 − 1.407746656 = 25.984312, then 25.984312 × 0.2104968588 = 5.469616, then 5.469616 ÷ 46.6162 = 0.1173329.
  - February: 22.74162117 − 1.703110865 = 21.038510, then 21.038510 × 0.2172032236 = 4.569632, then 4.569632 ÷ 37.1256 = 0.1230857.
  - June change: 0.1236896674 − 0.1173329 = 0.0063567674, then 31300.8 × 0.0063567674 = 198.9719 kg.
  - February change: 0.1330497939 − 0.1230857 = 0.0099640939, then 1866.8 × 0.0099640939 = 18.6010 kg.
  - Total: 198.9719 + 18.6010 = 217.5729; 217.5729 + 6.0124 = 223.5853 kg lower. Then 5009.9151 − 223.5853 = 4786.3298 kg.

Proposed: keep Fail, because the evidence within one removal conflicts (Status Definitions: "conflicting evidence" sits under Fail). Rewrite the note around the two bases and give both outcomes. Replace the fix "recompute the Jan-Jun 2026 blended CI from the live summaries, set L7, and enter 0.124866 in Certify" with a question for Max: should production CI count biomass-transport emissions before or after their BCUs?

This should not go to Garrett as a correction:
- V2 is owned by max@ (log key `blended_ci_source`).
- V2 and its six source copies sit in the July RP's Verified Periods folder.
- Workspace memory `project_charm_h1_2026_ci_policy.md` names "QOWV/Aqueous 0.1209" and says the blended CI "governs product **produced July–December 2026**".
- The registry shows INJ-08-2026-W5 and INJ-09-2026-W1 WODO carrying "H2 2026 blended CI 0.795241".

**7.3 Flag — Agree (wording).** Precedent: the registry entry for INJ-09-2026-W1 WODO lists "7.3 blended H2 CI unlinked" as a Flag. Ops Notes QOWV M7 and M19 are empty, and M14 and M18 carry links. Add to the note that V2 is not among the six Certify sources, and give the link target's location (7.2). 7.3 concerns tracing the value and 7.2 the value itself, so the two grades are consistent.

**7.4 Pass — Agree (low).** Certify's 40,525.8 kg equals Ops Notes QOWV D54. checklist_structure.md allows the per-period items to be combined into one row "with per-PP evidence in column D". Add the period masses (31,300.8, 7,358.2 and 1,866.8 kg) or point to 7.1.

**7.5 Pass — Agree (low).** Add the per-period figures: 32 × 1.13398 = 36.28736; 8 × 1.13398 = 9.07184; 2 × 1.13398 = 2.26796 kg.

**7.6 Pass — Agree.** This meets checklist_structure.md's wording for "2026 weekly time-block batches, where no standalone Charm Contents sheet exists — the batch Ops Notes attached to the production-mass datapoint".

### BCUs (item 8.1)

**8.1 Fail — Agree. Wording change to the fix.**
- Shortfall: 5895.2448 − 5895 = 0.2448 kg.
- Precedent: W2-QOWV records "8.1 BCU verified PASS (6,454.494 = process)" after its sub-kilogram Fail was fixed.
- Retirement certificate read: 2,795 TERCs, retired Dec 18, 2025, vintage 2024, Amazon.com Services LLC on behalf of Charm Industrial, Inc.

Change: the checklist's fix reads "enter the constant as the exact process emission, 7,138.2492 kg". Proposed replacement: make the constant equal the corrected process component's own output. That is 7138.2492 kg on the sheet factor and 7138.434 kg on Certify's 0.086 kgCO2e/(km*t), as shown under 5.1.

### LCS (item 9.1)

**9.1 N/A — Agree.** My own scan of every text cell in all ten Ops Notes tabs for LCS, calcium, caustic, NaOH and buffer found nothing. Ops Notes Summary E12 and F12 read 0.0.

### Calculation check (item C.1)

**C.1 Pass — Agree on the as-submitted 4.07555 t. CHALLENGE: the corrected net of 4.30142 t.** That figure rests on two contested choices: the before-BCU CI (7.2) and a COLA-40 count of 17 (3.4). Proposed: a range, as an ESTIMATE.

All three cases assume:
- the Flatbed process factor, with the BCU equal to it, so the two cancel;
- Non-Tanker embodied emissions of 495.2421 kg;
- carbon uncertainty of 0.0316.

Discount terms, using the 4.4 figures:
- Transport on the flatbed factor: 57.20022 × 0.1384 = 7.9165, and 7.9165 × 7.9165 = 62.67.
- Pyrolysis term for each case:
  - Case 1: 5060.2918 ÷ 40525.8 = 0.1248659, then 0.1248659 × 47.62716 = 5.9470, and 5.9470 × 5.9470 = 35.37.
  - Case 2: 5.8878, squared 34.67 (from 4.4).
  - Case 3: 4786.3298 ÷ 40525.8 = 0.1181057, then 0.1181057 × 47.62716 = 5.6250, and 5.6250 × 5.6250 = 31.64.
- Common start: 190.37 + 1568.65 = 1759.02, then 1759.02 + 62.67 = 1821.69.
- Case totals: 1821.69 + 35.37 = 1857.06, square root 43.09. 1821.69 + 34.67 = 1856.36, square root 43.09. 1821.69 + 31.64 = 1853.33, square root 43.05.

Sequestration less embodied: 9901.5619 − 495.2421 = 9406.3198.

| Case | Pyrolysis | Steps | Net |
|---|---|---|---|
| 1. CI before BCUs | 5060.2918 | 9406.3198 − 5060.2918 = 4346.0280; 4346.0280 − 43.09 = 4302.9380 | **4.30294 t** |
| 2. Ops Notes L7 kept | 5009.921 | 9406.3198 − 5009.921 = 4396.3988; 4396.3988 − 43.09 = 4353.3088 | **4.35331 t** |
| 3. All totes after BCUs | 4786.3298 | 9406.3198 − 4786.3298 = 4619.9900; 4619.9900 − 43.05 = 4576.9400 | **4.57694 t** |

---

## Checklist completeness against checklist_structure.md

- All 32 framework items (1.1 through 9.1) are present, plus C.1, the header fields, columns A–E and the sidebar. Nothing required is missing.
- Low: the column B question text is not word for word on several items, where the structure calls for "verbatim from Max's framework":
  - 2.3 adds branch text.
  - 3.3 says 'Batch Share of Truck' for 'RP Share of Truck'.
  - 6.3 says 'Shipment Tracker' for 'RP Bio-Oil Shipment Tracker'.
  - 7.1 says 'captured' for 'components'.
  - 7.4 and 7.5 say 'periods' for 'PP that applies to the component (from Ops Notes)'.
- Low: the combined 7.4 and 7.5 rows lack per-period evidence.

## Observations (outside the 33 items)

1. **The live period summaries are mixed themselves.** Under the '(No GHG Neutralization)' header, biomass transport is counted before BCUs (`I19 = C9*F7`). Diesel (`I21 = C40*F7`) and consumables delivery (`I26 = C82*F7`) are still counted after BCUs. This bears on Max's 7.2 decision.
2. **May 2026 live summary, cell C85:** 0.73646 against 0.073646 in the copy, ten times higher, which may be a decimal-place error. It feeds the May monthly CIs.
3. **Sidebar B65 has the same basis issue.** WODO basis effect (live column R share × live C10):
   - Jan: 0.3845850183 × 2.369484895 = 0.911268
   - Feb: 0.4098195467 × 1.703110865 = 0.697968
   - Mar: 0.4949652912 × 2.112208715 = 1.045470
   - Apr: 0.5363493064 × 0.9139 = 0.490170
   - Jun: 0.436964323 × 1.407746656 = 0.615135
   - Running total: 0.911268 + 0.697968 = 1.609236; 1.609236 + 1.045470 = 2.654706; 2.654706 + 0.490170 = 3.144876; 3.144876 + 0.615135 = 3.760011
   - Then 63.297890142 − 3.760011 = 59.537879. Unit: 75649.6 ÷ 1000 = 75.6496 t. CI: 59.537879 ÷ 75.6496 = 0.7870217.
   - That is below the 0.795241059 applied. The sidebar's comparison figure, 0.8367247169, is the before-BCU number.
4. **Why 7.2 was missed:** in the source-read log, the `blended_ci_source` entry for the six copies gives the V2 file as its artifact path. The copies themselves were never opened.
5. **No saved record of the Certify component detail views.** 0.03523, the EF labels and the BCU constant appear in the log alone. They are corroborated arithmetically above, under 4.4, 5.1 and 6.1.

---

## Challenges in priority order

1. **7.2 — rewrite the note and the fix; keep Fail.** The copies count biomass transport after its BCUs (`=C11*F7`); the live sheets count it before them (`=C9*F7`). On V2's own basis, today's data give 0.1201299, below the 0.120947 applied. The ledger mixes the two bases: production emissions are +50.3767 kg with all totes before BCUs, and −223.5853 kg with all totes after. The basis decision is Max's; do not route a CI recompute to Garrett.
2. **2.3 — Flag to Fail.** Tote 301215's post-unload weight is 442.5 kg in the ledger against 162.0 kg implied by the tracker; tote 301274's is 169.5 against 125.5. Add Garrett's recorded position ("COBB not source of truth") as the open question for Max. Explain why the tracker's 57.6 kg offset on every row (2094.7 kg net, 606.82 kg CO2e) is set aside.
3. **3.4 — COLA-40's 18 is the documented physical count.** Keep Fail on COLA-38 (6 on the tab against 18 on the master; 1.2777777778 of one truck claimed). Corrected allocation 2568.8055 mi; carry it into 6.1 (495.2421 kg), 6.2 and C.1. Say the error is conservative for W4.
4. **C.1 — state the corrected net as a range.** 4.30294 / 4.35331 / 4.57694 t, depending on the 7.2 decision.
5. **Sidebar B65 — add the basis caveat.** WODO on V2's basis gives 0.7870217, against 0.795241059 applied.
6. **5.1 and 8.1 — fix wording.** The BCU should equal the corrected component's output: 7138.2492 kg on the sheet factor, 7138.434 kg on 0.086 kgCO2e/(km*t).
7. **7.3 — add wording.** V2 is not among the six Certify sources; give the link target's location.
8. **1.1 — wording.** Remove the file-size match; cite the shared Drive file id and knowledge base line 313.
9. **Low.** Per-period figures in 7.4 and 7.5; word-for-word question text in column B; add the stale 'WODO Shipments & EE Allocation' header to sidebar B57.
