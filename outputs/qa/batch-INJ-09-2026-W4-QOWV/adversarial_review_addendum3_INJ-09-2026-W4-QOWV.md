# Adversarial review, third addendum: INJ-09-2026-W4-QOWV (BCU and COBB rulings)

- **Scope:** what changed after the 2026-10-07 rulings: checklist rows 7.2, 2.3, 3.1, 7.3, C.1 and the sidebar; the recompute's 7.2 and 2.3 lines; `cross_batch_bcu_basis_scan.txt`; the drafts in `PENDING_ON_RETURN.md`; and the new skill text (lessons_learned FC-C13, FC-C14; checklist_structure 7.2). Points settled in the three earlier reviews are not repeated, except where the checklist still contradicts one.
- **Reviewer:** independent agent that did not build the checklist. 2026-10-07. No file edited except this one. `recompute_qowv.py` was run with its output sent to a scratch file; it matches `recompute_output.txt` line for line, exit 0.
- **Read in this review:**
  - Checklist rows 19, 22, 44, 45, 54 and 57-65, columns A-E.
  - Log keys `max_rulings`, `pp_summary_basis`, `blended_ci_source`, `pp_summary_sources`, `cobb_injection_record`; `pp_summary_basis_comparison.json`; `gate_receipt.json`; `status_counts.json`.
  - The six live summary exports in `source_exports/pp_summaries/` (formulas and stored values) and V2, both tabs.
  - The six package summaries V2 was built from, in `~/Downloads/July 1 - July 31 RP/Charm BO MRV/H1 2026 Charm CI/` (same sha256 as the files under `Final Reporting Package July 1 - July 31 RP`), and `Biomass Transport Emissions.xlsx` in its June folder.
  - Dated local downloads of the live summaries: `~/Downloads/Charm Production Docs/{January, March, April} 2026 Production Period/`, `~/Downloads/{Feb, May, Jun} 26 Production Period Summary.xlsx`; and the 2025 summary copies under `~/Downloads/Charm Production Docs/` and `~/Downloads/July 1 - July 31 RP/Charm BO MRV/Charm Production Docs/`.
  - Ops Notes export, QOWV tab rows 1-54 and K-M constants; the seven exports in `source_exports/prior_weeks/`.
  - Inventory master export: 'Oil_inventory_data' and 'Q4 2025 -2026 Production Invent' tabs. Injection tracker export: tab list and 'Historical Tote Record'.
  - INJ-09-2026-W1 WODO checklist D18; `qa_active_charm_batches.json` (INJ-07-2026-W1); memory `project_charm_h1_2026_ci_policy.md`.
- **Conventions:** "my recompute" means a scripted pass over the named files. Text in double quotation marks is quoted from its source. Proposed wording is set off as indented blocks. ESTIMATE marks figures resting on local copies rather than the sheets the Ops Notes link.

## Verdicts

| Item | Status | Verdict |
|---|---|---|
| 7.2 | Fail | **Status upheld; note and fix challenged.** The C11 = embodied mapping, the June and February CIs, −217.5714 kg and V2's 0.1209473832 all reproduce. The note's account of which version was edited is reversed by the files; the corrected CI mixes two versions of the June summary; the −6.0121 kg remainder's causes go unstated; the fix covers two of five affected months |
| 2.3 | Fail | **Status upheld (Fail, not Flag); wording challenged.** Two citations are conversations, one quote is not verbatim, "similar conflict" overstates the W1 case, and the files show which record is probably wrong |
| 3.1 | Flag | Upheld |
| 7.3 | Flag | Upheld (one optional sentence) |
| C.1 | Pass | **Upheld; the two "on the evidence" nets challenged (low)** |
| Sidebar B62 | — | **Challenged:** the reach leaves out July-December 2025 product, and "Jan-Jun" takes in May |
| Sidebar B63 | — | **Challenged (low):** the blend in use did not draw on the live May sheet |
| Recompute 7.2 / 2.3 lines | — | Figures upheld; **challenged (low)** on what the script computes versus copies from the log |
| Cross-batch scan | — | Every figure reproduces; **scope challenged** |
| `PENDING_ON_RETURN.md` | — | **Challenged:** reversed edit-order claim, a stale "checks green", and Garrett bullets that run ahead of a decision |
| Skill text (FC-C13, FC-C14, structure 7.2) | — | **Challenged (low)** |

---

## 7.2 Fail: STATUS UPHELD, FOUR CHALLENGES

### What holds (my recompute)

- **"After BCUs" leaves embodied emissions.** In all six live summaries: B5 'Process Emissions', B6 'Embodied Emissions', B7 'Log Handling Emissions'; C9 `=SUM(C5:C7)` ('Total Emissions'); C10 `=SUM(C5,C7)` ("BCU's Applied"); C11 `=C9-C10` ('Remaining Emissions to Allocate'). C11 equals C6 to within 1e-8 in every month; F7 = 1 in all six. The ruling reads "BCUs should be applied to diesel transport, including biomass transport process emissions and handling (not embodied emissions)"; C10 holds process (C5) and handling (C7), and C11 holds embodied (C6).
- **May is handled correctly.** C5, C6, C7, C13, C14 and C15 are 0 in both the live and the package file, so I19 is 0 on either formula. May's after-BCU CI is 0.1106615762, equal to Ops Notes L17. The scan shows no May change; the sidebar says "(May has none)".
- **Live I19** reads `=C9*F7` in all six months. Ops Notes L13-L18 equal the six live Aqueous CIs (T4) to 1e-9; M14 and M18 link the February and June sheets.
- **June after BCUs:** 27.39205851 - 1.485923335 = 25.906135175 MT; 25.906135175 + 0.07817667978 = 25.98431186 MT; 25.98431186 × 0.2104968588 = 5.469616 MT = 5,469.616 kg; 5,469.616 ÷ 46,616.2 = **0.1173329448**.
- **February after BCUs:** 22.74162117 - 1.797501254 = 20.944119916 MT; 20.944119916 + 0.0943903882 = 21.0385103 MT; 21.0385103 × 0.2172032236 = 4.569632 MT = 4,569.632 kg; 4,569.632 ÷ 37,125.6 = **0.1230857** (checklist 0.1230857484).
- **Batch effect:** 0.1236896674 - 0.1173329448 = 0.0063567226; 31,300.8 × 0.0063567226 = 198.9705 kg. 0.1330497939 - 0.1230857484 = 0.0099640455; 1,866.8 × 0.0099640455 = 18.6009 kg. 198.9705 + 18.6009 = 217.5714 kg; 5,009.9151 - 217.5714 = 4,792.3437 kg; 4,792.3437 ÷ 40,525.8 = 0.1182541425.
- **V2 is after BCUs in every month.** Package files: I19 `=C11*F7` for January-April and June; May `=C9*F7` with C9 = 0. Their Aqueous S4 values, equal to V2 'CI Calculation' E7:E12, as a running sum: 4.28455461 + 4.55598869 = 8.8405433; 8.8405433 + 5.4427961 = 14.2833394; 14.2833394 + 5.565843396 = 19.849182796; 19.849182796 + 3.915108003 = 23.764290799; 23.764290799 + 5.467554803 = 29.231845602 MT = 29,231.845602 kg. 29,231.845602 ÷ 241,690.6 = 0.1209473831 (V2 D19 0.1209473832). WODO 0.7952410589.
- **Blend rebuilt from the live sheets after BCUs:** 29,034.276454 kg ÷ 241,690.6 = 0.1201299366. 0.120947 - 0.1201299366 = 0.0008170634; 7,358.2 × 0.0008170634 = 6.0121 kg lower. WODO 0.7870217283.

### Challenge A: the account of which version was edited is reversed by the files

Checklist D44: "The live summaries have been edited since the 2026-08-11 copies". Log `pp_summary_basis.result`: "The live inputs also changed (June: tonnes 109.03 -> 129.1156462585034, miles 354.5 -> 405.5)". Downloads of the live sheets made before the package files were saved already hold today's values:

| Local download of the live sheet | File time | Against today's live export |
|---|---|---|
| Charm Production Docs/January 2026 … Summary.xlsx | 2026-07-11 03:15 | I19 `=C9*F7`; C5-C7, C9, I20 equal; I28 2.929223405 vs 2.9291752 |
| Charm Production Docs/March 2026 … Summary.xlsx | 2026-07-11 03:14 | I19 `=C9*F7`; propane I20 15.57588484 equal |
| Charm Production Docs/April 2026 … Summary.xlsx | 2026-07-16 21:47 | every cell read equal; T4 0.1314184532 |
| Feb 26 Production Period Summary.xlsx | 2026-08-10 21:17 | I19 `=C9*F7`; T4 0.1330497939 |
| May 26 Production Period Summary.xlsx | 2026-08-11 02:02 | I19 `=C9*F7`; C85 0.73646; T4 0.1106615762 |
| Jun 26 Production Period Summary.xlsx | 2026-08-11 02:05 | I19 `=C9*F7`; C13 129.1156462585034, C14 405.5 |

The six package files were last modified on 2026-08-11 between 11:28 (February) and 22:39 (June), after every download above. The June package file's C13 109.03 and C14 354.5 match 'Biomass Transport Emissions.xlsx' beside it (modified 22:38; 'Monthly Totals' row 14: 5 loads, 109.0340136 t, 354.5 mi). Since 2026-08-11 02:05 the June live sheet has changed in J6 (biomass amortization factor), 65.51595 → 66.81, which moved its T4 from 0.123429378 to 0.1236896674. The first review drew the same direction from the INJ-07-2026-W1 registry entry (adversarial_review line 226); the checklist still states the reverse.

So the package files are the later, reworked set, and the sheets the Ops Notes link (M13-M18) were not brought into line. The Fail does not depend on this; the note's account does.

**Fix:** replace the D44 sentence, `pp_summary_basis.result`, `ruling_2026_10_07.note` and the `PENDING_ON_RETURN.md` "Still open" line with:

> V2 was built from the six xlsx summaries in the July RP package's H1 2026 Charm CI folder (saved 2026-08-11), not from the Google Sheets the Ops Notes link (M13-M18). Downloads of those sheets dated 2026-07-11 to 2026-08-11 already hold today's values, so the two sets diverged when the package files were reworked.

### Challenge B: the corrected CI mixes two versions of the June summary; "so it stands" hides it

The fix takes June and February from the live sheets and July from V2, which was built from the package files. The package's own June and February files are already after BCUs and give different CIs:

- June: package T4 **0.117288728** vs live after-BCU 0.1173329448. Cause: embodied miles, C14 354.5 vs 405.5 (C6 0.06834434768 vs 0.07817667978).
- February: package T4 **0.1227182507** vs 0.1230857484. Cause: the embodied factor per mile, 6.44927e-05 vs 0.0001927908256.

The files favour the package versions for these two months:

- The February live sheet's C5 (1.4172200170521543) and C6 (0.09439038819643568) are typed numbers. 10,240.02902 t-mi × 0.0001384 = 1.41722 and 489.6 mi × 0.0001927908256 = 0.0943904: the 2026 factors. The same sheet's 'Emission Factors' tab lists E3 0.000135156 and E6 6.44927e-05. The package's 'Biomass Transport Emissions.xlsx', 'EmissionFactors' D9, reads: "First day the 2026 EFs apply. Feb 2026 and earlier = 2025 EFs."
- The package's June inputs trace to that workbook's per-load table ('Allocation' row 7: Elk Meadows, June 2026, 5 loads). The live sheet's C13 and C14 are typed, and no file read here derives them.

Outcomes for this batch (my recompute; production emissions = June 31,300.8 kg + February 1,866.8 kg + July 7,358.2 kg, each × its CI; the discount uses the recompute script's own function):

| Version | June CI | Feb CI | July CI | Production emissions | Change vs 5,009.9151 | Weighted CI |
|---|---|---|---|---|---|---|
| Package files throughout (V2's) | 0.117288728 | 0.1227182507 | 0.120947 | 3,671.2310 + 229.0904 = 3,900.3214; + 889.9522 = **4,790.2737 kg** | −219.6414 kg | 0.1182030632 |
| Live sheets throughout (blend rebuilt) | 0.1173329448 | 0.1230857484 | 0.1201299366 | 3,672.6150 + 229.7765 = 3,902.3915; + 883.9401 = **4,786.3316 kg** | −223.5835 kg | 0.1181057894 |
| Checklist (mixed) | 0.1173329448 | 0.1230857484 | 0.120947 | 3,672.6150 + 229.7765 = 3,902.3915; + 889.9522 = **4,792.3437 kg** | −217.5714 kg | 0.1182541425 |

Net on the evidence (sequestration 9,901.5619 kg - embodied 495.2421 kg = 9,406.3198 kg):
- Package: 9,406.3198 - 4,790.2737 = 4,616.0461; 4,616.0461 - 43.0509 (discount) = 4,572.9952 kg = **4.57300 t**.
- Live: 9,406.3198 - 4,786.3316 = 4,619.9882; 4,619.9882 - 43.0503 = 4,576.9379 kg = **4.57694 t**.
- Mixed: 9,406.3198 - 4,792.3437 = 4,613.9761; 4,613.9761 - 43.0513 = 4,570.9248 kg = **4.57092 t**.

The mix gives the highest emissions of the three: 4,792.3437 - 4,790.2737 = 2.0700 kg above the package version (June 0.1173329448 - 0.117288728 = 0.0000442168, × 31,300.8 = 1.3840 kg; February 0.1230857484 - 0.1227182507 = 0.0003674977, × 1,866.8 = 0.6860 kg; 1.3840 + 0.6860 = 2.0700) and 4,792.3437 - 4,786.3316 = 6.0121 kg above the live version. So it errs conservative. It still prices June product at two June CIs inside one figure: the June totes at the live June sheet, the June month inside the July blend at the package June file.

**Fix:** keep Fail. Replace from "The 8 July 2026 totes carry L7" to "whether to rebuild it is the blend owner's call" with:

> The 8 July 2026 totes carry L7 = 0.120947, the QOWV result of 'V2_Charm_BioOil_Mass_Weighted_CI_Jan-Jun_2026.xlsx' (0.1209473832), built from the package versions of the six summaries, which count biomass transport after its BCUs. The June and February CIs come from the live sheets. On one version throughout, production emissions are 4,790.2737 kg (package files: June 0.117288728, February 0.1227182507) or 4,786.3316 kg (live sheets, blend rebuilt to 0.1201299366); June and February from the live sheets with July from V2 gives 4,792.3437 kg. The files favour the package versions for June and February: the February live sheet's typed biomass-transport values use 2026 factors where its own factor tab and the package's biomass-transport workbook ("Feb 2026 and earlier = 2025 EFs") give 2025 ones, and the package's June inputs (109.03 t, 354.5 mi) trace to a per-load workbook while the live sheet's (129.1156462585034 t, 405.5 mi) trace to no file read. Which version governs is a decision for the MRV lead, V2's owner.

### Challenge C: the −6.0121 kg remainder is data differences, not newer data

Both sides of the rebuild are after BCUs. QOWV after-BCU emissions, live minus package, converted to the July totes as kg × 7,358.2 ÷ 241,690.6 (my recompute):

- March propane, I20 15.57588484 live vs 17.33288553 package (Aqueous share 0.2125735629 vs 0.2119981441): −358.662 kg; 358.662 × 7,358.2 ÷ 241,690.6 = **10.9194 kg lower**.
- May C85, 0.73646 live vs 0.073646 package (the factor of ten the sidebar flags): +126.607 kg; 126.607 × 7,358.2 ÷ 241,690.6 = **3.8545 kg higher**.
- January and February embodied biomass transport on 2026 vs 2025 factors: +18.790 and +13.644 kg; 18.790 × 7,358.2 ÷ 241,690.6 = 0.5721 kg and 13.644 × 7,358.2 ÷ 241,690.6 = 0.4154 kg higher.
- June +2.061 kg → 2.061 × 7,358.2 ÷ 241,690.6 = 0.0627 kg higher; April −0.009 kg → 0.0003 kg lower.
- Net: −197.569 kg; 197.569 × 7,358.2 ÷ 241,690.6 = 6.0149 kg lower. L7's rounding: 0.1209473832 - 0.120947 = 0.0000003832; 7,358.2 × 0.0000003832 = 0.0028 kg. 6.0149 - 0.0028 = 6.0121 kg.

The rebuilt figure therefore rests on a March propane change no file explains, partly offset by a probable decimal slip in May.

**Fix:** if the rebuilt figure stays in D44 and C.1, add:

> The rebuilt figure differs from V2 mainly through March propane (15.57588484 vs 17.33288553 MT, 10.9194 kg lower on the July totes) and May C85 (0.73646 vs 0.073646, 3.8545 kg higher).

### Challenge D: the fix covers two of five affected months, and edits summaries behind verified removals

D44 fix: "set the June and February summaries' I19 to C11*F7, carry the new CIs into Ops Notes L18 and L14, and enter the new weighted CI in Certify." The Garrett draft says the same.

- The January, March and April live sheets read the same `=C9*F7` with C10 above zero (2.369484895, 2.112208715, 0.9139) and feed Ops Notes L13, L15 and L16, which the scan finds on W5, W1, W2 and W3. Correcting two leaves the five on two bases.
- The CI policy memory quotes Garrett: "The production blended CI is applied to July Periods --> All periods before this have already had CIs verified and are being used as such." Editing a summary in place changes the evidence behind removals already verified with it.
- If the package versions govern (Challenge B), setting the live sheets' I19 to C11*F7 yields June 0.1173329448 and February 0.1230857484, not the package's 0.117288728 and 0.1227182507.

**Fix:** replace the D44 fix with:

> Fix for this removal: once the governing version is chosen, carry the after-BCU June and February CIs into Ops Notes L18 and L14 and the weighted CI into Certify. The live summaries for January-April and June 2026 (and the July-December 2025 summaries, sidebar) count biomass transport before its BCUs and back other removals; correcting them, and whether earlier removals are restated, is a cross-batch decision for the MRV lead.

---

## 2.3 Fail: UPHELD AS FAIL, THREE CHALLENGES

### What holds

- **Both 1,080.0 records are production-system weighings, not COBB tabs.**
  - Inventory master 'Oil_inventory_data' row 39 (A1 "Microsoft SQL Server Import", last updated 2026/08/17 14:06): aqueous_fraction, lot 301274, security_tag 301274, production_date 2026-07-21 20:34:06, OIL260721143336, net 1022.4, gross 1080.0.
  - Injection tracker 'Historical Tote Record' row 1181 (same import header, 2026/10/05 12:22): 1022.4, 2026-07-21 20:35:05, OIL260721143336, aqueous_fraction, gross 1080.0, sectag 301274.
  - The tracker's COBB tabs are separate ('Basco Injection -- COBB', 'COBB (with offload info)'). All three carry the same import header; the checklist's line between the weighing record and the injection record holds.
- Q4 row 694: 301274 gross 1036.0, net 978.4, COLA_40. Ops Notes B40 1036.0, E40 169.5.
- If 1,080.0: 1,080.0 - 1,036.0 = 44.0 kg. Sequestration: 44.0 × 0.079 = 3.476; 3.476 × 3.667 = 12.746492 kg CO2e higher. Production emissions: 44.0 × 0.120947 = 5.321668 kg higher. Net: 12.746492 - 5.321668 = 7.424824 kg higher.
- **No checklist finding rests on COBB alone.** 2.1 cites the Historical Tote Record. 3.1 cites Oil_inventory_data rows 360 (lot 4746, tag 300020, 1012.0, WO00001655) and 350 (LOT00004770, tag 300020, 1085.0, COLA25) and Historical Tote Record rows 840 and 850, all as stated. The 301215 COBB conflict is gone; sidebar B61 keeps the Ops Notes' own 442.5 kg reading.

### Challenge A: the files show which record is probably wrong

| Tag | BGN inventory (Q4 tab) gross / net | Production system gross / net, work order |
|---|---|---|
| 301227 | row 738: 1070.0 / 1012.4 | 1070.0 / 1012.4, OIL260721133028 (Oil_inventory_data row 42, Historical Tote Record row 1178) |
| 301277 | row 693: 1070.0 / 1012.4 | 1036.0 / 978.4, OIL260721142141 (rows 40 and 1180) |
| 301274 | row 694: **1036.0 / 978.4** | **1080.0 / 1022.4**, OIL260721143336 (rows 39 and 1181) |

The BGN figure for 301274 is the production system's weighing of 301277, and the BGN figure for 301277 is 301227's. Each production record carries its own work order. A row slip in the BGN inventory fits; no file read fits 1036.0 as 301274's own weighing. The first addendum concluded "Nothing in the files shows which weighing is right"; these rows answer that.

**Fail, not Flag.** Two production records give different masses for a tote in this removal, and the evidence points at the reported one. An unsettled source hierarchy picks which record governs; it does not correct a transcription slip. The error is conservative: the removal is understated by 7.424824 kg.

**Fix:** add to D19:

> The BGN rows look shifted: 301274's 1,036.0 / 978.4 kg is the production system's weighing of tote 301277 (OIL260721142141; Oil_inventory_data row 40, Historical Tote Record row 1180), and BGN's 301277 row (693) carries 301227's 1,070.0 / 1,012.4 kg (row 738; OIL260721133028).

and change the fix line to:

> Confirm 301274's weighing; if OIL260721143336 stands, correct Q4 rows 693 and 694 and Ops Notes B40.

Observation outside this batch: if the production weighing of 301277 stands, BGN's 1,070.0 - 1,036.0 = 34.0 kg too much goes with 301277 (COLA_40, shipped 2026-09-17) into whichever batch holds it.

### Challenge B: "a similar conflict" overstates the W1 case

INJ-09-2026-W1 WODO checklist D18: "Tote 301257 is 1,115 kg gross in the Ops Notes (WODO!B22) and on the inventory's Q4 tab (row 725), but 1,120 kg on the inventory workbook's Oil_inventory_data tab (row 5, a 'Microsoft SQL Server Import'); all three give net 1,057.4 kg, so the difference is the tare (57.6 vs 62.6 kg)." Garrett's reply (log `max_rulings`): "These are all acceptable discrepancies-BGN Inv takes precedent over oil inv data, rounding error here, red herring". That was a 5 kg tare difference with net equal in all three records. 301274 differs by 44.0 kg in net produced and injected mass.

**Fix:** drop "Operations' recorded view on a similar conflict (INJ-09-2026-W1 WODO, 2026-10-05) is that the BGN inventory takes precedence over the production system's data; that source hierarchy is not yet settled" and use:

> The order among the Ops Notes, BGN inventory and production-system records is not yet ruled (batch-qa-charm FC-C14).

### Challenge C: conversation citations and a quote that is not verbatim

D19: "(operations position, adopted as the Charm rule 2026-10-07: 'COBB not source of truth')".
- Garrett's words (log `max_rulings.cobb`): "COBB is not source of truth heree" and "cobb not source of truth here". The checklist's quote matches neither.
- Max's words: "On COBB, I defer to Garrett." That is a deferral, not an adoption.
- lessons_learned cross-cutting list: "Process Conversations in QA Output — No "Per Max:" citations; evidence comes from documents".

**Fix:** cite the written rule, as 7.2 does with E44:

> The injection tracker's COBB tabs are not a source of record for this check (batch-qa-charm FC-C14).

No row says "per Max". 7.2's "(Charm BCU scope rule, 2026-10-07)", with E44 pointing to batch-qa-charm 7.2, is the right pattern.

---

## 3.1 Flag: UPHELD

Rows checked as cited: Oil_inventory_data 350 and 360, Historical Tote Record 840 and 850, Q4 410 (tag 300022, lot 4746, 1012.0, COLA_37) and 420 (tag 300020, lot 4770, 1085.0, COLA_25). "Lot numbers and weights agree in every production record, so no mass is counted twice" rests on distinct lots, not on COBB.

## 7.3 Flag: UPHELD

M7 and M19 are empty; M14 and M18 carry links. Optional addition:

> V2's own sources are the package summaries, not the sheets M13-M18 link, so a verifier following both finds two versions of each January-June summary (7.2).

## C.1 Pass: UPHELD; "ON THE EVIDENCE" NETS CHALLENGED (low)

4.07555 t as submitted reproduces. 4.57092 t uses the mixed CI and 4.57694 t the rebuilt blend (7.2 Challenges B and C). **Fix:**

> … production CIs on the 7.2 ruled basis: 4.57300 t with the package summaries throughout (June 0.117288728, February 0.1227182507, July 0.120947), 4.57694 t with the live sheets throughout (blend rebuilt to 0.1201299366, which carries the May C85 value in the sidebar); the fix as written gives 4.57092 t.

## Sidebar B62: CHALLENGED

B62: "The 7.2 basis reaches beyond this batch: the live Jan-Jun 2026 summaries count biomass transport before its BCUs … Any batch carrying Jan-Jun 2026 product at those monthly CIs overstates production emissions."

1. **May.** May product at the May CI is not overstated (C10 = 0); the sentence should name January-April and June 2026 product.
2. **2025 product is left out.** Every July-December 2025 summary copy read has the same basis, and its Aqueous CI equals the CI on the other weeks' totes:

| Month (Ops label) | Copy read (file time) | I19 | C10 | Aqueous CI | ESTIMATE after BCUs |
|---|---|---|---|---|---|
| Jul 2025 (PP#8) | July 1 - July 31 RP/…/Charm Production Docs/July 2025 … (2026-07-10) | `=C9*F7` | 2.09 | 0.1575553395 = W4 L10 | 0.1499571195 |
| Aug 2025 (PP#9) | Charm Production Docs/August 2025 … (2026-07-11) | `=C9*F7` | 1.185481759 | 0.1105698239 | 0.1064167602 |
| Sep 2025 (PP#10) | Charm Production Docs/September 2025 … (2026-07-11) | `=C9*F7` | 2.1172 | 0.1286895670 = W4 L21 | 0.1161827606 |
| Oct 2025 | July 1 - July 31 RP/…/October 2025 … (2026-07-10) | `=C9*F7` | 1.0499 | 0.1110176229 | 0.1063296701 |
| Nov 2025 | Charm Production Docs/November 2025 … (2026-07-11) | `=C9*F7` | 1.313113619 | 0.1392140548 = W4 L11 | 0.1309400966 |
| Dec 2025 | Charm Production Docs/December 2025 … (2026-07-11) | `=C9*F7` | 2.12828 | 0.1630616644 = W4 L12 | 0.1422148751 |

ESTIMATE, other weeks' Ops Notes, net produced at each 2025 CI × (CI before − CI after):
- INJ-08-2026-W5 QOWV (50 totes): Jul 2025 37,171.2 × 0.00759822 = 282.4350; Sep 2025 2,941.2 × 0.0125068064 = 36.7850; Aug 2025 1,981.8 × 0.0041530637 = 8.2305; Nov 2025 6,080.4 × 0.0082739582 = 50.3090. 282.4350 + 36.7850 = 319.2200; + 8.2305 = 327.4505; + 50.3090 = 377.7595 kg lower.
- INJ-09-2026-W2 QOWV (18 totes): Jul 2025 1,842.4 × 0.00759822 = 13.9990; Sep 2025 12,705.4 × 0.0125068064 = 158.9040; Aug 2025 994.0 × 0.0041530637 = 4.1281; Oct 2025 1,961.8 × 0.0046879528 = 9.1968. 13.9990 + 158.9040 = 172.9030; + 4.1281 = 177.0311; + 9.1968 = 186.2279 kg lower.
- INJ-09-2026-W3 QOWV (19 totes): Jul 2025 13,246.3 × 0.00759822 = 100.6483; Sep 2025 4,937.0 × 0.0125068064 = 61.7461. 100.6483 + 61.7461 = 162.3944 kg lower.
- Together: 50 + 18 + 19 = 87 totes; 48,174.6 + 17,503.6 = 65,678.2; 65,678.2 + 18,183.3 = 83,861.5 kg; 377.7595 + 186.2279 = 563.9874; 563.9874 + 162.3944 = 726.3818 kg lower, beyond the scan's figures.
- W5's one PP#7 tote (1,058.1 kg at 0.1373671128) is untested: the PP#7 copies use an older layout with no biomass-transport block (C10 typed 18.71).

**Fix:**

> The 7.2 basis reaches beyond this batch. The live summaries for January-April and June 2026 count biomass transport before its BCUs (May has none), for WODO and Aqueous alike, and so do the July-December 2025 summary copies read, whose Aqueous CIs equal the Ops Notes constants (L10-L12, L21). Batches carrying that product at those CIs overstate production emissions. In the other weeks' Ops Notes exported 2026-10-06 (not Certify): W5, W1, W2 and W3 for 2026 product (cross_batch_bcu_basis_scan.txt), and W5, W2 and W3 QOWV for 2025 product (87 totes, ESTIMATE 726.3818 kg). The blends in use (QOWV 0.120947, WODO 0.795241059) are after BCUs.

## Sidebar B63: CHALLENGED (low)

B63: "No W4 tote is May product, but the May CI and the Jan-Jun blend both draw on that sheet." V2 drew on the package May file, which reads C85 0.073646 (V2 E11 3.915108003 = package May S4). A blend rebuilt from the live sheet would carry 0.73646 (3.8545 kg higher on this batch's July totes, 7.2 Challenge C). **Fix:**

> … but the May CI draws on that sheet, and a blend rebuilt from the live sheets would carry it (3.8545 kg higher on the July totes, 7.2).

## Recompute 7.2 and 2.3 lines: FIGURES UPHELD, CHALLENGED (low)

- `recompute_qowv.py` line 122 takes the after-BCU CIs and the rebuilt blend from the log (`pp_summary_basis.after_bcu_ci`, `after_bcu_live_blend`); no line opens a summary. Lines 143-146 print the 2.3 effect from the log's `if_1080` values instead of computing it, and take 1,080.0 from `cobb_injection_record.gross_conflicts.301274.tracker_gross_kg` while labelling it the production system's weighing. Every value is right by my recompute.
- **Fix:** compute (I32 − I19 + C11×F7) × R4 × 1000 ÷ N4 from `source_exports/pp_summaries/` for each month, compute the 2.3 effect from 44.0 kg, and read 1,080.0 from Oil_inventory_data row 39. Move `gross_conflicts` and `tag_300020` out of the `cobb_injection_record` log key, since neither rests on COBB.

## Cross-batch scan: FIGURES REPRODUCE, SCOPE CHALLENGED

My recompute matches every line: W5 QOWV 28 totes, 28,077.2 kg, −376.1361 kg; W5 WODO 10, 10,645.0 kg, −673.4743 kg; W1 WODO 11, 12,139.4 kg, −346.5237 kg; W2 QOWV 20, 19,138.0 kg, −27.1177 kg; W3 QOWV 18, 17,362.2 kg, −72.2455 kg; W4 34 totes, 31,300.8 + 1,866.8 = 33,167.6 kg, −217.5714 kg; INJ-10 W1-W3 none. The twelve monthly before/after CIs on its first line, "month CIs before -> after BCUs (live summaries)", match mine to 1e-9.

Scope: the file states neither its source nor its limits. It reads the Ops Notes exported 2026-10-06 (`prior_weeks/`, seven weeks), not Certify, and its first line lists January-June 2026 CIs and no others. **Fix:** add a first line:

> Source: Ops Notes exports dated 2026-10-06 for INJ-08-2026-W5 to INJ-10-2026-W3, not Certify. Tests totes at the January-June 2026 monthly CIs; 2025 product is in the sidebar.

The same scope belongs in FC-C13's list of affected batches.

## PENDING_ON_RETURN.md: CHALLENGED

1. "Still open" 7.2: "the live summaries were edited after the 2026-08-11 copies the blend was built from" — reversed (7.2 Challenge A).
2. DM: "Delivery checks green." `gate_receipt.json` (generated 2026-10-06T22:51:51Z) covers checklist sha256 0c0a301d… and source reads c0254a81…; the current files are 7aa30544… and a6ccc579…. Rerun the gates before sending, or drop the phrase.
3. DM 7.2: "(−217.5714 kg production emissions on your ruling)". Replace with:
   > −219.6414 kg on the package summaries, −223.5835 kg on the live sheets; pick one.
4. Garrett 7.2 bullet: the June and February figures, and whether the summaries are edited, wait on that choice and on the cross-batch decision (7.2 Challenges B and D). Hold the bullet until both are made.
5. Garrett 2.3 bullet: add:
   > The BGN rows look shifted: 1,036.0 kg is 301277's weighing (OIL260721142141), and BGN's 301277 row carries 301227's 1,070.0 kg.

## Skill text: CHALLENGED (low)

- checklist_structure 7.2 and FC-C13 grade I19 `=C9*F7` a Fail:
  > checklist_structure 7.2: `=C11*F7` is right, `=C9*F7` counts BCU-offset emissions and is a Fail.
  > FC-C13: `C11*F7` (after BCUs) is correct; `C9*F7` is a FAIL on 7.2.

  May 2026 reads `=C9*F7` in both versions with C9 = 0 and is correct. **Fix:**
  > Fail when I19 exceeds C11×F7, that is `=C9*F7` with C10 above zero. Also confirm C10 = SUM(C5,C7), since C11 holds embodied emissions alone when C10 holds process and handling.
- FC-C13: "On W4 the June and February totes overstated production emissions by 217.57 kg; the same constants appear in INJ-08-2026-W5 (QOWV and WODO), INJ-09-2026-W1 WODO, W2 QOWV and W3 QOWV." Add the 2025 summaries and W5, W2 and W3 QOWV 2025 product.
- FC-C14 quotes Garrett as "COBB is not source of truth." The source reads "COBB is not source of truth heree"; mark the cut or quote in full.

---

## Challenges in priority order

1. **7.2: the corrected CI mixes two versions of the June summary**, and the note says the July blend "stands". On one version throughout, production emissions are 4,790.2737 kg (package summaries, favoured by the files for June and February) or 4,786.3316 kg (live sheets). Put the choice to the MRV lead; keep Fail.
2. **7.2: the live sheets were not edited after the package files.** Downloads dated 2026-07-11 to 2026-08-11 02:05 hold today's live values; the package files were saved 2026-08-11 11:28-22:39. Correct D44, the log and PENDING.
3. **7.2: the fix covers two of five affected months** and edits summaries behind verified removals. Limit the batch fix to Ops Notes L14/L18 and Certify; route the summaries to a cross-batch decision.
4. **2.3: add the shifted-row evidence** (BGN's 1,036.0 for 301274 is 301277's weighing; BGN's 1,070.0 for 301277 is 301227's). Keep Fail. Replace the conversation citations and the non-verbatim quote with FC-C14; drop "similar conflict".
5. **Sidebar B62 and the scan: 2025 product is left out** (ESTIMATE 87 totes, 726.3818 kg lower on W5, W2 and W3 QOWV); "Jan-Jun" takes in May; the scan states no scope.
6. **PENDING:** "Delivery checks green" is stale against the current file hashes; the Garrett 7.2 bullet runs ahead of the two decisions.
7. **7.2 and C.1:** name the −6.0121 kg drivers (March propane 10.9194 kg lower, May C85 3.8545 kg higher); add the package-version net 4.57300 t.
8. **Low:** B63 wording; the recompute copies its 7.2 and 2.3 figures from the log; skill-rule wording for May and the FC-C14 quote; optional 7.3 sentence.

## Arithmetic check

Every derived figure above was recomputed in scripted passes over the named files during this review: the six live summaries, the six package summaries, the dated local downloads, the 2025 copies, the W4 and seven prior-week Ops Notes exports, the inventory master and the injection tracker. The ESTIMATE figures rest on the 2025 copies, whose Aqueous CIs equal the Ops Notes constants to 1e-9 but are not the sheets the Ops Notes link.
