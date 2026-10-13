# Adversarial review: INJ-09-2026-W1 WODO, revised checklist (2026-09-29)

**Checklist:** `Charm_WODO_QA_Checklist_INJ-09-2026-W1.xlsx`, opened read-only with openpyxl (sheet `WODO QA INJ-09-2026-W1`).
**Sources read this session, all from disk:** Ops Notes live export and Certify-attached copy, `inventory_master_export.xlsx` (every tab searched), `pp_toteloss.xlsx`, `pp_feb/mar/may.xlsx`, `standard_efs_export.xlsx`, the COBB export in the W3-QOWV folder, the SGS PDF, the TERC retirement PDF, the routing-map PNG, the source-read log, `failure_category_review_late.md`, and `skills/qa/batch-qa-charm/references/lessons_learned.md`. Certify and Drive were not opened. Certify-side facts (modal inputs, attachment map) are taken from the 2026-09-21 log.
**Recompute:** `recompute_wodo.py` re-run: 15 lines `OK`, exit 0, output identical to `recompute_output.txt`. A separate, independent recompute reproduces every figure below.

**Step 0 (primary-source check):** passed. Every value-bearing row cites values that can only come from opening the source. No row relies on "deferred" or "not opened".

---

## 1. Challenged items

### 2.2: Flag. Recommendation: keep Flag, and correct the evidence and scope.

The status is right. The note understates the direct evidence, overstates the flag's reach, and misses a conflicting record.

1. **The direct statement of the basis is not cited.** The Tote Loss Dataset, already opened for 2.3, says the tare is assumed. In `pp_toteloss.xlsx`, tab `Charm WODO 2026`, I10 reads `Tote tare assumed (kg)` and J10 = `57.6`. The note infers "standard figure" from uniform values instead.
2. **The flag's reach is overstated.** D19 says `For WODO the standard tare sets both Total Oil Produced and Total Oil in Batch`. It does not set Total Oil in Batch:
   - The same dataset computes every loss as measured empty weight minus that same 57.6 kg: column F is `=C2-E2` with E = 57.6 on all 43 rows.
   - The standard loss is therefore the mean of (empty − 57.6) plus one SD.
   - Tare plus standard loss: 57.6 + 7.84 = 65.44 kg.
   - Mean measured empty weight: 57.6 + 4.7327 (dataset J2) = 62.3327 kg. Adding one SD: 62.3327 + 3.1052 = 65.4379 kg.
   - The 57.6 cancels out. Total Oil in Batch (14,075.28 kg, the sequestration mass) rests on 43 measured empty weights, not on the tare.
   - Only Total Oil Produced (14,177.2 kg, the pyrolysis mass at 7.4) carries the assumed tare.
3. **The 13-tag claim holds on one tab only.** D19 says `The same 57.6 kg tare appears per tote in the production inventory master for all 13 tags`. That is true of tab `Q4 2025 -2026 Production Invent`. The same workbook's tab `Oil_inventory_data` (A1: `Microsoft SQL Server Import`) row 5 records tag 301257 as `net_weight_kg` 1057.4 and `gross_weight` 1120.0.
   - That implies a tare of 1,120.0 − 1,057.4 = 62.6 kg.
   - Its gross is 1,120 − 1,115 = 5 kg above Ops Notes WODO!B22.
   - See Observation O1.
4. **The figure ignores pallet type.** In the Q4 tab, 57.6 kg sits on 69 WODO totes with Pallet Type `STEEL` and 31 with `PLASTIC`. This batch has 3 plastic (300055, 301143, 301302) and 13 − 3 = 10 steel. So the figure does not track a tote attribute the sheet itself records.

**Why Flag, not Fail:** SKILL.md Key classification guidance: `Tare value from manufacturer label rather than measured = FLAG`. The sequestration mass is shielded from the tare by the way the standard loss is built (point 2). The pyrolysis mass carries the assumption, and the 57.6 kg value is visible in the attached Ops Notes.

**Fix to D19:**
- Cite I10/J10.
- Limit the stated effect to Total Oil Produced and the pyrolysis mass (7.4).
- State the 301257 conflict.
- Change the fix to: attach the source of the 57.6 kg figure, or weigh the empty totes, and resolve tote 301257 (O1).

### 8.1: Fail. Recommendation: keep Fail. Correct the note, and hold the fix value until O1 is resolved.

**Status supported.** SKILL.md, BCU QA Rule: `Over-coverage (BCU > activity) is always a FAIL, whatever the size.`
- Recomputed: 14.926 × 1,201 = 17,926.126, and 17,926.126 × 0.1384 = 2,480.9758384 kg.
- BCU over by 2,481 − 2,480.9758384 = 0.0241616 kg. D51's "0.0242 kg" is correct.
- The inputs are Certify's own modal values (log `certify.components.1`: 14,926 kg, 1,201 mi, 0.1384). The 2026 tab row 7 native value is `0.0001384` MT CO2e/t-mi.
- SKILL.md also carries `no rounding tolerance beyond ~0.001 tCO2e` for Certify-versus-evidence mismatches. The BCU-specific "whatever the size" rule governs this item.

**Problems in D51:**
1. **Rounding error.** `2,480.97 kg` appears in D51, but 2,480.9758 does not round down to 2,480.97 at two decimals. Print 2,480.9758, as D51 does later in the same note. The same slip is in D36 (5.3) and in log `_derived_values.process_recomputed_kg` = 2480.97.
2. **Repeated calculation.** The same multiplication is written out twice in D51. Delete the first instance.
3. **No net effect stated.** Saying it shows Garrett this is a rule breach, not a change in credited tonnes. It displays as 19.081 t either way.
   - Sequestration: 14,075.28 × 0.573 = 8,065.13544, and 8,065.13544 × 3.667 = 29,574.8517 kg.
   - Activities: 2,480.9758 + 150.5022 = 2,631.4780, and 2,631.4780 + 10,220.1935 = 12,851.6715 kg.
   - Net now: 29,574.8517 + 2,481 = 32,055.8517; 32,055.8517 − 12,851.6715 = 19,204.1802; 19,204.1802 − 123 = 19,081.1802 kg.
   - With the BCU at 2,480.9758: 29,574.8517 + 2,480.9758 = 32,055.8275; 32,055.8275 − 12,851.6715 = 19,204.1560; 19,204.1560 − 123 = 19,081.1560 kg.
4. **The fix value depends on O1.** `Fix: enter the constant as 2,480.9758 kg` assumes Total Mass Transported = 14,926 kg.
   - If tote 301257's gross is 1,120 kg, the mass is 14,926 + 5 = 14,931 kg.
   - The emission is then 14.931 × 1,201 = 17,932.131, and 17,932.131 × 0.1384 = 2,481.8069 kg.
   - The 2,481 kg BCU would be 2,481.8069 − 2,481 = 0.8069 kg short. That is still a Fail, under SKILL.md 8.1's `ALL diesel transport-process emissions MUST be BCU-offset`, but the correct constant changes.
   - Resolve O1 before sending the fix to Garrett.

### STATUS SUMMARY (A61). Recommendation: counts stand; rewrite three sentences.

- **Counts verified from column C:** 27 Pass, 3 Flag (2.2, 7.2, 7.3), 1 Fail (8.1), 1 N/A (9.1). These match `27 Pass - 3 Flag - 1 Fail - 1 N/A  (32 items)`.
- **One sentence contradicts 8.1.** `All five Certify components independently recomputed from primary sources and reconcile exactly` names four components and the net. The fifth component, `BCU - Transport Process`, is the 8.1 Fail and does not reconcile to its emission at full precision. The revision created this contradiction. Rewrite it to say the four sequestration and emission components reconcile exactly, and the BCU component is 0.0242 kg over its emission (the 8.1 Fail).
- **The Fail is buried.** It appears mid-paragraph as `(8.1 FAIL)`, after the passes. The flags get a heading (`THREE FLAGS.`); the Fail gets none. Open the paragraph with a one-Fail heading naming 8.1, then the flags.
- **The 2.2 sentence** (`the 57.6 kg tote tare is a standard figure, not a per-tote weighing`) should carry the narrower scope from the 2.2 challenge.

### 5.3: Pass. Status stands; one figure is wrong.

D36 reads `= 2,480.97 kgCO2e`. The exact value is 2,480.9758384 (see 8.1), which does not round down to 2,480.97. Print 2,480.9758.

### 2.3 and 7.4: Pass. Status stands; cross-references are missing after the revision.

- **2.3 (D20)** already cites the Tote Loss Dataset. Add that tare plus standard loss (65.44 kg) matches mean + 1 SD of the 43 measured empty weights (65.4379 kg), so the 2.2 Flag does not reach Total Oil in Batch.
- **7.4 (D47)** is where the assumed tare lands: the pyrolysis mass is 14,177.2 kg. D47 cross-refers only the 7.2 label flag. Add a pointer to the 2.2 Flag for the tare basis.

### Source-read log: late additions

| Key | Checked against | Result |
|---|---|---|
| `cobb_injection_record` | COBB export, tab `Basco Injection -- COBB` | Verified. Rows 747–759 carry `INJ-09-2026-W1_oily_fraction`. The 13 security tags equal the ledger tags, and each appears once in the tab. `injection_completion_date` is 2026-09-04 on all 13 and `week_starting_injected` is 2026-08-31. `quantity_consumed_in_injection` sums to 14,177.2 kg. |
| `pp_summary_sources.wodo_row_M2` / `aqueous_row_M4` | `pp_feb/mar/may.xlsx` row 2 and row 4 | Values verified: Feb WODO 10,966 kg, 52.38 %, 9.31996088 MT, T2 0.8498961226, Aqueous T4 0.1330497939. Mar WODO 16,307, 51.06 %, 12.88358234, T2 0.790064533, Aqueous T4 0.1185251532. May WODO 11,130, 45.75 %, 7.043574746, T2 0.6328458891, Aqueous T4 0.1106615762. Citation fix: the values sit in N–T, and M2/M4 hold only the labels `WODO` / `Aqueous`. |
| `pp_summary_sources.period_length` | same files | Values verified: Feb 28, Mar 31, May 31. Citation fix: B57 holds the label `Days in Production Period` and the number is in C57. |
| `tote_tare_methodology.tare_distribution` | `inventory_master_export.xlsx` | Counts verified: WODO 57.6 × 100; QOWV 57.6 × 565 and 62.93 × 73. Gaps: the tab (`Q4 2025 -2026 Production Invent`) is not named; Whole Oil rows (57.6 × 37; 62.9 × 3, all three on 330-gal totes) are left out; the dataset's J10 `Tote tare assumed (kg)` is not recorded; the SQL-import conflict on 301257 is not recorded. The `result` field itself is supported. |
| `bcu_vs_process` | own recompute | Verified: 2,481 − 2,480.9758384 = 0.0241616 kg, recorded as 0.0242. |

### `failure_category_review_late.md`

- **Verified against the sheet and checklist:** FC-C1, FC-C3, FC-C6, FC-C7, FC-C8, FC-C12. For FC-C9, a text search of every cell finds no `n=3`, `Production Batch` or `sample size`.
- **FC-C10:** values verified. `= each summary's WODO row M2` is wrong: the CI is in T2, and M2 holds the label `WODO`.
- **FC-C5:** `13 of 13 tags, fraction, gross and period match the inventory master` holds against the Q4 tab only. The SQL-import tab gives 301257 a gross of 1,120.0 (O1).
- **Dating:** the header reads `Written 2026-09-28` and `checked against the delivered checklist`, but the FC-C11 line records a regrade on 2026-09-29. The file now describes the revised checklist. Update the header.
- **Missing categories:** the seven items under `Cross-cutting FCs reused from AECN / Kerry` (lessons_learned.md lines 163–173) are left out. The pre-flight asks for `every Failure Category from lessons_learned.md that applies`. `Wrong FAIL/FLAG Classification — Missing evidence = FAIL` bears directly on the 2.2 grading and is not addressed.

---

## 2. Confirmed items

- **Header B2–B10.** B5 `2026-09-21 (revised 2026-09-29: standard tare, BCU rule)` agrees with the 2.2 and 8.1 statuses. B10: 29.575 + 2.481 = 32.056; 32.056 − 12.852 = 19.204; 19.204 − 0.123 = 19.081. Activities: 12,851.6715 kg (see 8.1), which is 12.852 t.
- **1.1.** SGS PDF read: `Certificate of Analysis: SR26-05444.001`, client ID `9-2026-W1 WODO`, Carbon 57.3 % (m/m) by ASTM D5291 (Method C), H 7.4, N <0.75, 280.3 cSt, acid number 77, density 1.200. Matches D14.
- **1.2.** WODO rows 11–23 are populated. B25 14926, D25 14177.2, E25 101.92, F25 14075.28, H25 0.7208894223, I25 10220.19352, J25 14.74174. There are zero cell comments on Summary, WODO, the allocation tab or Whole Oil, in both the live export and the Certify copy. The copy's four comments are on AECN Rail D29/D34 and AECN Truck C19/C22.
- **1.3.** Allocation tab: COLA_35, 2026-09-01, C12 20, D6 `=COUNTA(WODO!A11:A23)` = 13, E12 0.65, B8 1201, G12 780.65, B16 `OK`.
- **2.1.** Arithmetic confirmed: the 13 gross weights sum to 14,926 (`=SUM(B11:B23)`), and A33 is `=B25`. Whether each gross value is right is O1.
- **2.3.** 13 × 7.84 = 101.92, and 14,177.2 − 101.92 = 14,075.28. Dataset: n 43 (J1 `=COUNT(A2:A44)`), mean 4.7327267, sample SD 3.1052173 (population SD 3.0688977), J5 `=ROUND(J2+J3,2)` = 7.84. The cross-reference noted above is still to be added.
- **2.4.** 2.5 × 0.453592 = 1.13398, and 13 × 1.13398 = 14.74174. J11:J23 read `=2.5*$L$4`.
- **3.1.** The Q4 tab has 20 COLA_35 rows. The 13 WODO rows are the ledger tags. The other 7 are QOWV `June 2026 PP`: 301224, 301221, 301295, 301213, 301247, 301296, 301217.
- **3.2.** B16 `=IF($D$14=$D$6,"OK","MISMATCH")` returns `OK`.
- **3.3.** Formulas read: D12 `=$D$6`, E12 `=IFERROR(D12/C12,"")`, F12 `=$B$8`, G12 `=IFERROR(E12*F12,"")`, G14 `=SUM(G12:G13)`.
- **3.4.** 13 / 20 = 0.65, and 0.65 × 1,201 = 780.65.
- **3.5.** Q4 tab against the ledger: tag, fraction, gross and period match on all 13. This passes as defined, since the item compares the shipment record with Ops Notes. The SQL-import conflict is a different record (O1).
- **4.1.** 14,075.28 × 0.573 = 8,065.13544 kg carbon, and 8,065.13544 × 3.667 = 29,574.85 kg, which is 29.575 t.
- **4.2.** Two sources per log `certify.attachment_map` (Certify not reopened). Attached Ops Notes sha256 `86cd007b…` recomputed this session. Cell-by-cell diff against the live export re-run: 0 differences on Summary, WODO, allocation and Whole Oil.
- **4.3.** Certify ±14.74174 kg equals J25.
- **4.4.** 0.004 × 57.3 = 0.2292. Summary G19 `=E19*H19` = 0.002292.
- **5.1.** 2026 tab row 7: `Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck`, 0.0001384 MT CO2e/t-mi, GLEC V3.2 2025, `Updated`.
- **5.2.** Map PNG read: `via US-287 S and US-287 S` 1,132 mi; `via US-287 S, US-287 S and I-20 E` 1,129 mi; `via I-70 E` 1,201 mi. 1,201 is the longest. Origin field reads `Your location`.
- **5.4.** One Ops Notes source per log attachment map.
- **5.5.** ±14.74 is the displayed form of 14.74174.
- **6.1.** 2026 tab row 12: `Vehicle Embodied Emissions --Non-Tanker Truck`, 0.0001927908256 MT CO2e/mi.
- **6.2.** 780.65 × 0.1927908256 = 150.50 kg, which is 0.151 t.
- **6.3.** Ops Notes and routing map are both on the datapoint (log). Absence of a Charm Contents sheet is recorded in `certify.charm_contents_note`.
- **7.1.** Per-period masses: 1,107.4 / 4,305.6 / 6,726.4 / 2,037.8 kg. Multiplied by L14 0.84989612258998, L15 0.7900645329689984, L17 0.6328458891234968 and L7 0.795241, they give 941.17 / 3,401.70 / 4,256.77 / 1,620.54, matching D44. The unrounded total equals Ops Notes I25 = 10220.19352.
- **7.2 (Flag).** I25 10,220.19352 / D25 14,177.2 = 0.72088942. The H column reads `=$L$14`, `=$L$15`, `=$L$17`, and `=$L$19` → `=$L$7`. PP Summary T2 values match. The W5 log carries `WODO Tote - Carbon Intensity` and `WODO Tote - Mass (Gross-Tote) for pyrolysis`. Flag supported.
- **7.3 (Flag).** M10–M18 carry `HYPERLINK(…,"PP Summary")`. The row K19/L19 (`July 2026 and later (Jan-Jun 2026 rolling)`, `=$L$7`) has no M19. 1,620.54 / 10,220.19 = 0.1586, which is 15.9 %. Flag supported.
- **7.5.** 10.220 / 12.852 = 0.7952, and 10.220 / 19.081 = 0.5356.
- **7.6.** Absence of a Charm Contents sheet per log. The Ops Notes source is on the `Mass` datapoint.
- **9.1 (N/A).** WODO headers A10:J10 have no LCS column. WODO batch.
- **Sidebar D56–D59.**
  - The `#` footnote text matches the PDF.
  - The Whole Oil tab row matches log `whole_oil_observation`.
  - The VVB text matches `vvb_guidance_sept_2026.txt`: `applies to Week 3 of this Reporting Period, INJ-09-2026-W3, covering 11 – 18 September 2026, and to that week alone`.
  - The map origin matches the image.
- **Formatting.**
  - Flag rows 19, 45 and 46 have #FFF2CC fill and #996600 font across A–E. Fail row 51 has #FFC7CE fill across A–E. N/A row 53 is gray (#808080) italic. Section rows are #D6E4F0.
  - The merged A61:E61 row has an explicit height of 195 with text wrap on.
  - No cell names Max.
- **Retirement certificate (8.1 evidence).** PDF read: `Amazon.com Services LLC`, `Charm Industrial, Inc`, `Dec 18, 2025`, vintage `2024`, `Renewable Diesel TERCS`, `2,795`, `Turner, Mason & Company`, `TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000`. Matches D51.

---

## 3. Observations (outside the checklist's current findings)

**O1: tote 301257 has two gross weights in Charm's own records.**
- **The two records:**
  - Tab `Oil_inventory_data` (A1 `Microsoft SQL Server Import … Last updated 5 weeks ago`), row 5: `301257`, production_date 2026-08-11 22:05:12, `net_weight_kg` 1057.4, `gross_weight` 1120.0.
  - The Q4 tab (row 725) and Ops Notes WODO!B22 carry 1115, with tare 57.6 and net 1057.4.
- **Context:**
  - The other 11 batch tags found in the SQL import match the Q4 tab exactly, with gross minus net = 57.6.
  - 301302 is not in the import.
  - Ten WODO totes in the import show the same pattern: gross above the Q4 tab, identical net. The gaps run from 1,243 − 1,241 = 2 kg (301241) to 1,129 − 1,123 = 6 kg (301251).
  - Nine of the ten are `July 2026 PP` and one, 301251, is `June 2026 PP`. Nine of the ten are on COLA_33. Only 301257 is in this batch.
  - The Q4 tab's Notes column reads `filtered in CO to 1000um into fresh tote` on all 13 batch totes. These files do not show whether either gross reading was taken before or after that transfer.
- **Effect if 1,120 kg is the as-shipped weight (arithmetic in 8.1, point 4):**
  - Total Mass Transported becomes 14,931 kg.
  - The process emission becomes 2,481.8069 kg, which is 2.482 t against Certify's 2.481 t.
  - The BCU becomes 0.8069 kg short (8.1).
  - Net oil is unchanged if the SQL net is right.
- **Recommendation:** establish which reading is the as-shipped scale weight before redelivery. If this cannot be settled, 2.1 should be graded Fail under the reviewer rule `Any issue where the evidence says something different from what's being reported (e.g., vehicle identifiers don't match, mass values conflict between sources, emission factors misapplied) is a FAIL`.

**O2: the required-step record is missing.**
- There is no `step_ledger.json` in this batch folder. The only one under `outputs/qa/` is in `batch-INJ-09-2026-W3-QOWV`.
- `run_gates.py` requires an entry for every step id in `charm_step_ledger.py` `REQUIRED_STEPS`, so delivery stays blocked until it is built.
- No file in the folder evidences `G4_render_in_excel` (an Excel PDF export).

**O3: the recompute output reads clean against a Fail.**
- `recompute_wodo.py` prints `BCU <= process (BCU QA Rule, checklist 8.1): False` but still exits 0.
- Its check labelled `bcu_matches_proc_at_display_precision` prints `OK`.
- A reader of `recompute_output.txt` sees 15 `OK` lines next to an 8.1 Fail. Rename that check, or have it print a line saying the 8.1 Fail is recorded. Adding it to the exit code would block delivery of a Fail meant for Garrett.

**O4: the tare carries no uncertainty.**
- The ±1.13398 kg per tote covers the gross weighing only (`=2.5*$L$4`). Nothing covers the assumed tare.
- Items 2.4, 4.3 and 7.5 are graded against the skill's stated `1.134 kg per tote (1 weighing event per tote)`, so their Pass stands.
- Whether the pyrolysis mass needs a tare term is not addressed in the checklist.

**O5: the May PP Summary has no biomass transport.**
- `pp_may.xlsx` C13 Tonnes 0.0, C14 Miles 0.0, and C5/C6/C7 0.0, while J4 Total Biomass Consumed is 50,923.01 kg.
- March shows C13 233.45 t and C14 598.4 mi.
- This falls outside the checklist's scope (the CI is evidenced by the Ops Notes weighted average) and was not examined further.
