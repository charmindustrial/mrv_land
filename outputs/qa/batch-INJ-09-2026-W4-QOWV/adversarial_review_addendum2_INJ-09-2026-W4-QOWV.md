# Adversarial review, second addendum: INJ-09-2026-W4-QOWV (weighing-record changes)

- **Scope:** only the checklist content changed after the first addendum: items 2.1, 3.5, 7.1, 7.3 and C.1 of `Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W4.xlsx`, and the source-read log keys behind them (`tote_weighing_records`, `pp_summary_sources.july_2026`, `totes[*].weighing_record / weighing_date / weighing_location`). Earlier reviews: `adversarial_review_INJ-09-2026-W4-QOWV.md` and `adversarial_review_addendum_INJ-09-2026-W4-QOWV.md`. Points settled there are not repeated.
- **Reviewer:** independent agent that did not build the checklist. Date 2026-10-06. No file was edited except this one.
- **Read in this review (all from files in the batch folder):**
  - Checklist rows 17 (2.1), 26 (3.5), 43 (7.1), 45 (7.3) and 54 (C.1), columns A–E.
  - Source-read log: the keys above, plus `ops_notes_totals` and `pp_summary_sources.live`.
  - `tote_weighing_records.json`, `recompute_qowv.py`, `recompute_output.txt`, `PENDING_ON_RETURN.md`.
  - Ops Notes export `source_exports/INJ-09-2026-W4_Ops_Notes.xlsx`, QOWV tab rows 1–54, values and formulas.
  - Injection tracker export `source_exports/bio_oil_injection_tracker_live_2026-10-06.xlsx`: 'Historical Tote Record' tab, all 2,094 rows (headings in row 2), and the column headings of the 'Basco Injection -- COBB' and 'COBB (with offload info)' tabs.
  - Inventory master export `source_exports/inventory_master_export.xlsx`: 'Q4 2025 -2026 Production Invent' tab (all 1,504 rows), 'Oil_inventory_data' tab (all rows), 'Claude C 2025 -2026 Production ' tab, and the headings of 'Data Entry Form'.
  - `source_exports/pp_summaries/`: June, both July summary files and the July output CSV compared cell by cell; `V2_Charm_BioOil_Mass_Weighted_CI_Jan-Jun_2026.xlsx` both tabs.
  - `knowledge-base/pdd_full.txt` line 450; CI policy memory `project_charm_h1_2026_ci_policy.md`; `skills/qa/batch-qa-charm/SKILL.md` Status Definitions.
- **Conventions:** counts marked "my count" come from my own scripted pass over the named file. Text in quotation marks is quoted from a source. Proposed checklist wording is new text, set off as indented lines without quotation marks. Figures marked ESTIMATE rest on a stated assumption.

## Verdicts

| Item | Status | Verdict |
|---|---|---|
| 2.1 | Pass | **Challenged (low).** Status and figures hold. The date range mixes in a record that is not under the tote's own tag; the weighing-location basis skips the production system's own location field |
| 3.5 | Flag | **Challenged.** Keep Flag, but the reasoning, the −11.008 kg figure, the "conservative" claim and the fix are wrong. The records already settle the production period |
| 7.1 | Pass | Upheld |
| 7.3 | Flag | **Challenged (low).** The copies claim holds cell for cell. The output-summary claim rests on a one-tab export; the sentence should say why the June copies matter |
| C.1 | Pass | **Challenged.** Drop "the open production-period question in 3.5": it has no effect on the net, and the direction the checklist implies is wrong |

---

## 3.5 Flag: CHALLENGED

### What holds (my recompute)

- (a)–(d) 42 of 42 against the inventory master 'Q4 2025 -2026 Production Invent' tab. 300022 is at row 410 and 301317 at row 741, so "rows 410-741" is right.
- Within this batch, exactly 8 totes have a weighing month different from their label (my count over all 42, using the 'Historical Tote Record' tab, and lot 4746's record under tag 300020 for 300022):
  - June-labelled (32): 28 weighed 2026-06-05 to 2026-06-29. 301215, 301210, 301228 and 301223 weighed 2026-07-01 (tracker 'Historical Tote Record' rows 1140, 1141, 1143, 1145).
  - July-labelled (8): 301297 weighed 2026-07-08, 301245 and 301242 2026-07-20, 301274 2026-07-21. 301305, 301331, 301312 and 301317 weighed 2026-08-31 (rows 1219, 1220, 1221, 1227).
  - February-labelled (2): 300022 (lot 4746, filed under tag 300020, row 840) weighed 2026-02-17, 300040 (row 841) 2026-02-23. Both inside February.
  - No tote in the batch was weighed before its labelled month. Nothing is missing from the checklist's list of eight, in either direction.
- The four June totes' net produced (Ops Notes QOWV D23, D26, D30, D31): 966.4 + 983.4 = 1,949.8; 1,949.8 + 1,005.4 = 2,955.2; 2,955.2 + 1,058.4 = 4,013.6 kg.
- CI gap: Ops Notes QOWV L18 0.1236896674 − L7 0.120947 = 0.0027426674. Then 4,013.6 × 0.0027426674 = 11.008 kg. The arithmetic is right; its use is not (below).
- Form/tote Date (Q4 tab column D) is blank for all eight. It is blank on every row labelled January–September 2026: 421 of 421 (my count). It is a gap across all 2026 production, not one specific to these totes.

### Challenge 1: the records already place the four June totes in June

The checklist treats the weighing date as possible evidence of the production month. Four records say otherwise, and the checklist cites none of them.

1. **The June CI was computed with these four totes as June output.** June PP Summary ('Jun 26 PP Summary' tab, `Jun2026_PP_Summary.xlsx`, the file Ops Notes QOWV M18 links to) N4, Aqueous "Mass of Output (kg)", reads 46,616.2. The 48 QOWV rows labelled 'June 2026 PP' in the Q4 tab sum to 46,616.2 kg (my count), and rows 659, 660, 661 and 663 (301215, 301210, 301228, 301223) are among them. The June PP Summary's Aqueous mass is built from the Q4 labels, not from weighing dates. Aqueous totals also tie exactly for January (30,830.4), February (37,125.6), March (46,683.2) and May (36,523.2); April does not (Q4 45,764.8 vs summary 43,912.0).
2. **Spray paint.** Q4 tab column S, headed "Production Period Spray Paint", reads 'Blue2606' for all four June totes and 'Purple2607' for all four July totes weighed 2026-08-31. Every June 2026 row carries Blue2606 (58 rows) and every July 2026 row Purple2607 (75 rows) (my count).
3. **Weighing after month-end is routine across the inventory.** Q4 label against weighing month, all tags with a 'Historical Tote Record' entry (my count):

   | Label | Weighed the next month | Dates |
   |---|---|---|
   | February 2026 PP | 3 | 2026-03-03 |
   | March 2026 PP | 24 | April |
   | April 2026 PP | 2 | 2026-05-01 |
   | May 2026 PP | 10 | 2026-06-01 |
   | June 2026 PP | 16 (10 QOWV, 6 WODO) | 2026-07-01 to 2026-07-03 |
   | July 2026 PP | 20 | 2026-08-07 to 2026-08-31 |

   Labels also run the other way: two May-labelled WODO totes were weighed in April (301055 on 2026-04-08, 301149 on 2026-04-20). One June-labelled WODO tote (301251) was weighed two months on, 2026-08-10. Weighing records summed by month do not match the period masses either: April weighings total 90,637.0 kg Aqueous against 43,912.0 kg in the April summary.
4. **ESTIMATE: little July output could exist by the time these totes were weighed.** June produced 46,616.2 kg Aqueous over 30 days (June PP Summary N4, and C57 "Days in Production Period"). ESTIMATE, hourly rate: 30 × 24 = 720 h; 46,616.2 ÷ 720 = 64.745 kg per hour. The latest of the four order stamps, OIL260701143701, reads 14:37:01. 340 of 354 OIL order stamps sit about 6 hours before their 'reported_on' time (my count), consistent with local Mountain time against UTC. ESTIMATE, output by then: 14:37:01 is 14.617 hours after midnight, and 14.617 × 64.745 = 946.4 kg. ESTIMATE, reading 'reported_on' 20:40:44 as local time: 20.679 hours, and 20.679 × 64.745 = 1,338.9 kg. Either way, at June's average rate, at most about one tote's worth (not 4,013.6 kg) could have been produced on 2026-07-01 before these weighings. ASSUMPTION: the early-July rate is close to June's average.

The same reasoning covers the four July totes weighed 2026-08-31. The Q4 tab has no QOWV rows labelled 'August 2026 PP'; its 16 August rows are all Whole Oil (my count).

### Challenge 2: the −11.008 kg figure is not what a July reassignment would produce, and "conservative" is unsupported

The four totes are inside the June Aqueous mass that sets the June CI (Challenge 1, point 1). The blended CI also counts them: `V2_Charm_BioOil_Mass_Weighted_CI_Jan-Jun_2026.xlsx`, 'CI Calculation' D12, reads 46,616.2 for June. Calling them July product while leaving both CIs unchanged counts their mass in June's denominator and also charges them the next period's CI. A consistent reassignment has to take them out of June's output, and that raises the June CI on the batch's other 28 June totes.

Every figure in this list is a hypothetical ESTIMATE, rechecked by the script run recorded at the end of this file, worked on the June PP Summary's own formulas: T4 `=(S4*1000)/N4`, S4 `=R4*$I$32`, R4 `=Q4/(SUM($Q$2+$Q$3+$Q$4))`, Q4 `=P4*N4`. Inputs are the June summary's stored values: N2 10778.0, N3 6247.5, N4 46616.2, P2 0.59446, P4 0.06621, Q2 6407.08988, Q3 5169.1815, I32 27.39205851 MT. ASSUMPTIONS: June's emissions stay in June; WODO and biochar masses are unchanged unless stated.
- ESTIMATE, June Aqueous mass without the four: N4 46,616.2 − 4,013.6 = 42,602.6 kg.
- ESTIMATE, new Q4: 42,602.6 × P4 0.06621 = 2,820.718.
- ESTIMATE, carbon-mass total: Q2 6,407.08988 + Q3 5,169.1815 = 11,576.27138; then 11,576.27138 + 2,820.718 = 14,396.989.
- ESTIMATE, June emissions × P4: I32 27.39205851 MT × 1,000 = 27,392.05851 kg; then 27,392.05851 × 0.06621 = 1,813.628.
- ESTIMATE, new June CI: 1,813.628 ÷ 14,396.989 = 0.125973 kg CO2e/kg.
- ESTIMATE, the batch's other 28 June totes: 7.1's June mass 31,300.8 − 4,013.6 = 27,287.2 kg. CI rise: 0.125973 − 0.123690 = 0.002283. Then 27,287.2 × 0.002283 = 62.30 kg higher.
- The four at the blended CI: 11.008 kg lower (shown above), rounded to 11.01.
- ESTIMATE, net: 62.30 − 11.01 = 51.29 kg CO2e **more** production emissions. On this reading the submission would understate emissions, not overstate them.
- ESTIMATE, all 16 June-labelled totes weighed in July moved out of June:
  - Aqueous, net weight from the Q4 tab, rows 653–663: 301213 1,009.4; 301247 964.4; 301225 970.4; 301296 989.4; 301217 989.4; 301215 983.4; 301210 966.4; 301228 1,058.4; 301208 1,019.4; 301223 1,005.4. Running sum: 1,009.4 + 964.4 = 1,973.8; + 970.4 = 2,944.2; + 989.4 = 3,933.6; + 989.4 = 4,923.0; + 983.4 = 5,906.4; + 966.4 = 6,872.8; + 1,058.4 = 7,931.2; + 1,019.4 = 8,950.6; + 1,005.4 = 9,956.0 kg.
  - WODO, Q4 tab rows 638–666: 301206 1,108.4; 301205 1,136.4; 301203 1,020.4; 301226 1,058.4; 301256 1,096.4; 301248 917.4. Running sum: 1,108.4 + 1,136.4 = 2,244.8; + 1,020.4 = 3,265.2; + 1,058.4 = 4,323.6; + 1,096.4 = 5,420.0; + 917.4 = 6,337.4 kg.
  - New masses: N2 10,778.0 − 6,337.4 = 4,440.6 kg; N4 46,616.2 − 9,956.0 = 36,660.2 kg.
  - Carbon-mass total: 4,440.6 × 0.59446 = 2,639.759; Q3 5,169.1815; 36,660.2 × 0.06621 = 2,427.272. Sum: 2,639.759 + 5,169.1815 = 7,808.9405; then 7,808.9405 + 2,427.272 = 10,236.2125.
  - New June CI: 1,813.628 ÷ 10,236.2125 = 0.177178. CI rise: 0.177178 − 0.123690 = 0.053488. On the same 27,287.2 kg: 27,287.2 × 0.053488 = 1,459.54 kg higher.
- The blended CI would move too. I have not computed that, because the 7.2 basis decision governs which June emissions figure it uses.

These figures show the checklist's counterfactual is neither a bound nor a direction. Challenge 1 shows the counterfactual does not arise.

### Challenge 3: "neither record gives a fill date" leaves out the production system's own production_date

The inventory master's 'Oil_inventory_data' tab (A1 "Microsoft SQL Server Import / Last updated 7 weeks ago") has a column headed 'production_date'. For the four June totes it reads 2026-07-01: 301223 at 20:37:14 (row 75), 301228 at 20:10:20 (row 77), 301210 at 18:41:13 (row 78), 301215 at 18:13:11 (row 79). Each carries the same order number as its weighing record, and each time sits 40 seconds to 3.5 minutes before the 'reported_on' time (301228 20:10:20 against 20:11:00; 301223 20:37:14 against 20:40:44). So Manufacturo's "production_date" is the weigh-in, not the fill. The same tab's column M, headed 'Production Period', reads 'June 2026 PP' for 301210 and 301228 and is blank for 301215 and 301223.

This is the real documentation issue. A verifier tracing these totes in Manufacturo sees a production_date of 2026-07-01 against a June CI. That keeps Flag, not Pass. It is not a Fail: the records that set the CI agree with each other (Challenge 1), so no misstatement is shown. The `batch-qa-charm` Flag definition fits: "Process hygiene or documentation issue that does NOT prevent verification".

### Challenge 4: the fix sends Garrett to answer a question the files already answer

Current: "Fix: confirm the production period of the eight totes in the production system". Proposed replacement for checklist D26 (new text):

> (a) tag 42 of 42; (b) fraction QOWV 42 of 42; (c) gross mass 42 of 42; (d) production period 42 of 42, each against the production inventory master row for the tag (rows 410-741 of the Q4 2025-2026 Production Inventory tab). Flag: no 2026 tote has a fill date (Form/tote Date is blank on all 421 rows labelled January-September 2026), and the production system dates 8 totes in the month after their label: Manufacturo's production_date and weighing record read 2026-07-01 for 301210, 301215, 301223 and 301228 (June 2026), and the weighing record reads 2026-08-31 for 301305, 301312, 301317 and 301331 (July 2026). These dates are the weigh-in, not the fill. The records place the totes in their labelled period: the June summary's Aqueous mass (N4, 46,616.2 kg) is the sum of the 48 QOWV rows labelled June 2026, these four included, so the June CI was computed with them as June output; they carry June's spray paint (Blue2606) and the four July totes July's (Purple2607); and weigh-ins after month-end are routine (10 May totes weighed 2026-06-01, 16 June totes 2026-07-01 to 07-03, 20 July totes in August). No change to the removal. Fix: record each tote's fill date, or the rule that assigns its production period, in the production inventory [log:inventory_master, totes, tote_weighing_records, pp_summary_sources.live, _derived_values_numeric].

Carry-through:
- Log `tote_weighing_records.june_totes_weighed_in_july`: remove `production_emissions_change_if_july_kg` (−11.008) and "Unresolved from the records read". Record the June summary N4 tie, the spray paint and the Oil_inventory_data production_date.
- `recompute_output.txt` "FINDING 3.5" lines and `recompute_qowv.py` lines 145–154: same change.
- `PENDING_ON_RETURN.md`: the Slack draft to Max says "(four June totes, if July product: −11.008 kg production emissions)", and the Garrett draft asks him to "confirm the production period of 301210, 301215, 301223, 301228 ... and 301305, 301312, 301317, 301331". Both need the new wording before sending.

---

## 2.1 Pass: CHALLENGED (low)

### What holds (my recompute)

- QOWV B54 `=SUM(B11:B52)` = 42,945.0 kg.
- Q4 tab gross equals ledger gross on 42 of 42 tags, one Q4 row each (my count).
- 'Historical Tote Record' holds 41 of the 42 tags under their own tag. Gross equals the ledger on 40; 301274 reads 1,080.0 (row 1181) against 1,036.0 (Ops Notes QOWV B40). Tote 300022 is not under its own tag; lot 4746 is under tag 300020 (row 840). Every count matches.
- 'Historical Tote Record' row 2 headings: "reported_quantity, reported_on, production_year, order_number, code, gross_weight, sectag, lot_number". There is no location column. The COBB tab adds 'weighing_order', 'weighing_date' and 'weighing_order_link', also with no location. "No record states where the totes were weighed" is true.

### Challenge A: the date range

"dated 2026-02-17 to 2026-08-31" sits beside "the 41 tags it carries under their own tag". The 41 own-tag records run 2026-02-23 17:45:26 (300040, row 841) to 2026-08-31 20:35:38 (301317, row 1227) (my count). 2026-02-17 is lot 4746's record under tag 300020. Proposed (new text):

> the tracker's Historical Tote Record, dated 2026-02-17 (lot 4746, filed under tag 300020) to 2026-08-31

### Challenge B: the location basis skips a production-system field

Log `tote_weighing_records.location_basis.recorded` reads "None" and rests the Fort Lupton inference on two Slack messages and the 'BGN' label. The inventory master's 'Oil_inventory_data' tab has 'site_location' and 'location' columns. 37 of the 42 tags, plus lot 4746, read site_location 'CHARM', location 'OPA' (my count). The four totes weighed 2026-08-31 and 300022's own tag are absent, because the pull predates them. Elsewhere in the tab the field names other sites, 'CHARM_LOUISIANA' (407 rows), 'CHARM_KANSAS' (28) and 'CHARM_TRANSIT' (1), and it follows the tote as it moves: lot LOT00004770, already shipped, reads 'CHARM_LOUISIANA' / 'Bio Oil Incoming' (row 350). So it records where the tote sat when the data was pulled, not where it was weighed. "Inferred, not recorded" stays honest. The inference should cite this field first. `knowledge-base/pdd_full.txt` line 450 reads "Charm produces bio-oil at our pyrolysis facility in Fort Lupton, CO", as the log quotes.

Fix: add the Oil_inventory_data site_location/location finding to `location_basis` and to each `totes[*].weighing_location`. The checklist parenthesis can stay as written.

---

## 7.1 Pass: UPHELD

- Ops Notes QOWV columns D, G and H (my recompute): June 32 totes, 31,300.8 kg, 3,871.5855 kg CO2e; July 8, 7,358.2 kg, 889.9522 kg; February 2, 1,866.8 kg, 248.3774 kg. Sum 5,009.9151 kg, equal to QOWV I54 5,009.915111. 40,525.8 × 0.123623 = 5,009.921 kg.
- The new sentence holds: all eight totes sit in the one aggregated component whatever their period. If 3.5 is reworded as proposed, "Eight totes' weighing records fall outside their labelled period (3.5)" still reads correctly.

## 7.3 Flag: CHALLENGED (low)

### What holds (my comparison)

- `Jul2026_PP_Summary.xlsx` and `Jul2026_PP_Summary_1nIz.xlsx` each have tabs 'Jun 26 PP Summary', 'Emission Factors', 'DataTable', 'DataCollection', the same as `Jun2026_PP_Summary.xlsx`.
- Both match June on every non-empty cell: 426 cells read as formulas and 425 read as stored values, with 0 differences and 0 cells present in one file only. The extra formula cell is 'Jun 26 PP Summary' C89 `=C84`, which has no stored value. The log's "all 425 non-empty cells, values and formulas alike" is off by one in formula view. The checklist's "cell-for-cell copies" is right.
- sha256 of the two July files matches the log (e0424eb3…, 8e2d6976…). They are not byte-identical to June (89a7e537…); the content is.
- `Jul2026_PP_Output_Summary_1k5le.csv`: the WODO and Aqueous rows have blank mass and "#DIV/0!" in every calculated cell. The biochar rows hold five readings: 82.72%, 82.29%, 80.67%, 85.25% and 82.78%.

### Challenge A: "unfilled template" rests on a one-tab export

A CSV export of a Google Sheet carries one tab. The log does not record how many tabs the sheet has. The claim holds for the tab read; for the whole file it is unverified. Fix: record the sheet's tab count in `pp_summary_sources.july_2026`, or limit the claim to the first tab (proposed wording below).

### Challenge B: say why the copies matter

A filled July summary would not hold the blended-CI derivation either. Under the CI policy, July product takes the Jan–Jun blended CI. So "No July summary fills that gap" is true but beside the point. The risk is that a verifier who opens the July file for the July totes finds June's CI. Proposed (new text):

> Both Drive files titled 'Jul 26 Production Period Summary' are cell-for-cell copies of June's (summary tab still named 'Jun 26 PP Summary', Aqueous CI 0.1236896674), so a verifier opening them for the 8 July totes finds June's CI, not the 0.120947 applied; the first tab of 'July 26 Production Period Output Summary' is an unfilled template.

## C.1 Pass: CHALLENGED

- The new phrase "and the open production-period question in 3.5" lists 3.5 among the errors the 4.076 t carries. With 3.5 settled by the records (above), it carries none. And the effect the checklist implies (3.5's "net +11.008 kg", which is 0.011 t on the net) has the wrong sign under a consistent reassignment. ESTIMATE: 51.29 kg more emissions (3.5 Challenge 2) is 51.29 ÷ 1,000 = 0.051 t lower on the net.
- Fix: delete ", and the open production-period question in 3.5". If a pointer is wanted, use (new text):

> 3.5 is a documentation flag and does not change the net.

- The rest of D54 was reviewed in the full review and first addendum and is unchanged in substance.

---

## Challenges in priority order

1. **3.5: keep Flag; rewrite the reason, drop the counterfactual, replace the fix.** The June PP Summary N4 (46,616.2 kg) equals the 48 June-labelled QOWV rows, these four included, so the June CI already treats them as June output. Spray paint (Blue2606 / Purple2607) agrees. Weigh-ins after month-end are routine across 2026. The −11.008 kg "conservative" figure ignores that the June and blended CIs both count these totes. ESTIMATE (arithmetic in 3.5 Challenge 2): a consistent reassignment gives 51.29 kg more emissions instead. The remaining flag is documentation: no 2026 tote has a fill date, and Manufacturo's production_date is the weigh-in (2026-07-01 for four June totes). Carry the change into the log, the recompute output and both drafts in `PENDING_ON_RETURN.md`.
2. **C.1: remove "the open production-period question in 3.5".**
3. **2.1 (low):** date range wording, and cite Oil_inventory_data site_location 'CHARM' / location 'OPA' in the weighing-location basis.
4. **7.3 (low):** the output-summary claim covers one exported tab; say the July copies show June's CI.

## Arithmetic check

Every derived figure in this file (running sums, rates, the hypothetical June re-cuts and their effects) was recomputed in one scripted pass during this review. The script read the Ops Notes QOWV tab, the June PP Summary stored values and the inventory master Q4 tab, and every figure matched as written.
