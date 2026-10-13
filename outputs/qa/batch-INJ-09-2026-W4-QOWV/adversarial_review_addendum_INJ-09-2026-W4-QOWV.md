# Adversarial review addendum — INJ-09-2026-W4-QOWV (injection-tracker changes)

- **Scope:** only the checklist content the QA agent changed after reading the injection tracker live. That covers checklist items 1.1, 2.3 and 3.1, and sidebar notes B61–B64 of `Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W4.xlsx`. The full review is `adversarial_review_INJ-09-2026-W4-QOWV.md`.
- **Reviewer:** independent agent that did not build the checklist. Date 2026-10-06. Nothing in the checklist or the source-read log was edited.
- **Read in this review:**
  - Rules: `adversarial-reviewer/SKILL.md`, and from `batch-qa-charm/SKILL.md` the Status Definitions and the FAIL vs FLAG rule.
  - Live injection tracker export `source_exports/bio_oil_injection_tracker_live_2026-10-06.xlsx`, opened read-only with stored values. Read: the 'Basco Injection -- COBB' tab, all 29 named columns and all 3,805 rows (my count); the 'Historical Tote Record' tab; and a tag search of every tab.
  - `cobb_w4_aqueous_rows_live.json`. The 2026-09-28 export `../batch-INJ-09-2026-W3-QOWV/source_exports/bio_oil_injection_tracker_export.xlsx` (same tab) and `cobb_w4_aqueous_rows.json`.
  - Ops Notes export `source_exports/INJ-09-2026-W4_Ops_Notes.xlsx`: QOWV tab rows 1–54, and the cell notes in every tab.
  - Inventory master export `source_exports/inventory_master_export.xlsx`: tab 'Q4 2025 -2026 Production Invent', plus a search of every tab. The search found the 'Oil_inventory_data' and 'Claude C 2025 -2026 Production' tabs relevant.
  - Both lab certificate PDFs: sha256, a byte comparison, and pages 1–3 read as images. Also the Drive file itself, downloaded through the Drive connector and hashed.
  - Source-read log `batch_INJ-09-2026-W4-QOWV_source_reads.json`, entries `cobb_injection_record` and `testing`.
  - Charm batch registry `skills/qa/batch-qa-charm/qa_active_charm_batches.json` (search for "source of truth").
- **Arithmetic** is shown as two-number steps. Counts marked "my count" come from my own scripted pass over the named files.
- **Proposed wording** for checklist cells is new text, set off as indented lines without quotation marks. Only text inside quotation marks is quoted from a source.

## Verdicts

| Item | Status | Verdict |
|---|---|---|
| 1.1 | Pass | Agree |
| 2.3 | Fail | Agree on Fail. **Challenge: the 301274 reasoning is wrong.** The note should also give Garrett's recorded position, the 301274 effect, and a wider fix |
| 3.1 | Pass | **Challenge: change to Flag.** The tag 300020 description puts the error in the wrong record |
| Sidebar B61 | — | **Challenge:** misreads the fourfold repeat and misses tag 300020's July injection |
| Sidebar B62 | — | Agree. One wording change |
| Sidebar B63 | — | **Challenge:** the pH is a weekly wellhead figure applied to every product, and the newest import has none |
| Sidebar B64 | — | Agree. One wording change |
| Not in checklist | — | 301274's 1,080.0 kg comes from the production system. Tag 300020 is recorded as injected twice. Both are covered under 2.3 and 3.1 |

---

## 1.1 Pass — Agree

Checked:
- sha256 of `Drive_Testing_COA_1Viar0c3xdOh.pdf` and `Certify_attached_COA_src_1M3VZ8S8W1S013HS.pdf`: both `276ccd65301889cf4e037a09ee2f397d6e2224f336dbfc0895947baf766943f6`. `cmp` finds no byte difference.
- I downloaded Drive file `1Viar0c3xdOh-pwkpbsNY0buJPDH5AGEJ` myself through the Drive connector. It hashes to the same sha256, so the local "Drive" copy is that Drive file. Drive metadata: title 'SR26-05719 W4 Kerry AECN QOWV COA.pdf', parent `1sbuy0NI_yqQmXd4e326PCZ5VmaSUHnsM`. `batch_folder_listing.txt` names that parent "[folder] Testing" in the W4 folder.
- Certificate page 3, read as an image: "Certificate of Analysis: SR26-05719.003", CLIENT ID "9-2026-W4-QOWV", LOCATION "FORT LUPTON, CO", SAMPLED "25-Sep-2026 10:00", ANALYSED "28-Sep-2026 14:29 - 28-Sep-2026 23:23". Results:
  - Carbon "7.9 % (m/m)", ASTM D5291 (Method C), marked "#"
  - Hydrogen "7.9", marked "#"
  - Nitrogen "<0.75"
  - Kinematic Viscosity "0.9020 cSt"
  - Acid Number "36 mg KOH/g"
  - Density at 15°C "1.039 g/cm³"
- Page 1 is SR26-05719.001, CLIENT ID "9-2026-W4-KERRY". Page 2 is SR26-05719.002, CLIENT ID "9-2026-W4-AECN".
- Knowledge base line 313: "All streams exceed formation fluid density (1.01 g/cm³) — confirmed via density analysis for safe injection." The checklist quotes the first clause correctly.

Every figure in checklist D13 matches. The note writes 0.902 where the certificate prints 0.9020; that is the same value. This addendum settles the "file size" point from the full review: the match is now by content hash.

## 2.3 Fail — Agree on Fail. CHALLENGE: the 301274 reasoning, two missing points, and the fix

### What I recomputed, and it holds

Ops Notes QOWV tab, ledger rows 11–52:
- F = B − E.
- Column E runs from 164.5 kg (E18, E23, E32) to 442.5 kg (E17, E26).
- F54 is 34,179.5 kg.
- Kept in totes: 40,525.8 − 34,179.5 = 6,346.3 kg.

Tracker, 'Basco Injection -- COBB' tab, compared with the ledger tote by tote in all four blocks and in the 2026-09-28 copy (rows 856–897):
- **301215.** Tracker gross 1,041.0 kg equals Ops Notes QOWV B26. The tracker quantity is 821.4 kg in every block and in the 2026-09-28 copy.
  - Implied post-unload weight: 1,041.0 − 57.6 = 983.4, then 983.4 − 821.4 = 162.0 kg. Ops Notes QOWV E26 reads 442.5 kg.
  - Injected on the tracker's figure: 1,041.0 − 162.0 = 879.0 kg. Ledger: 598.5 kg. Gap: 879.0 − 598.5 = 280.5 kg.
  - Sequestration: 280.5 × 0.079 = 22.1595, then 22.1595 × 3.667 = 81.2589 kg CO2e. Matches the checklist.
- **301274.** Tracker gross 1,080.0 kg; quantity 852.9 kg in every block and in the 2026-09-28 copy.
  - Implied post-unload weight: 1,080.0 − 57.6 = 1,022.4, then 1,022.4 − 852.9 = 169.5 kg. This equals Ops Notes QOWV E40, as the checklist says.
- **The 57.6 kg offset.** On every other tote, tracker quantity = (ledger gross − 57.6) − ledger post-unload weight. The 'Historical Tote Record' tab shows where this comes from: its `reported_quantity` is gross − 57.6 (for 301215: 1,041.0 − 57.6 = 983.4, the figure it records). The tracker then subtracts the full post-unload weight, tote shell included. The checklist's "standard tote tare taken off a second time" is correct.
- **301166.** Tracker quantity 593.9 kg. Ledger: 651.5 − 57.6 = 593.9. The tracker agrees.

Grade. The `batch-qa-charm` Status Definitions put "conflicting evidence" under Fail. The key classification guidance reads "Value in Certify doesn't match evidence = FAIL (no rounding tolerance beyond ~0.001 tCO2e)". 301215 alone is 81.2589 kg, or 0.0813 t. Against the net removal in checklist D54 ("4.07555 t", which is 4,075.55 kg): 81.2589 ÷ 4,075.55 = 0.0199, which is 2.0 %. Fail is correct. It is also consistent with 4.4, which is graded Fail although that error is conservative.

### Challenge 1 — "the production record sides with the Ops Notes" is wrong for 301274

There are two production records, and they disagree. Charm's production system, Manufacturo, holds the higher figure in two places:
- **Inventory master, 'Oil_inventory_data' tab, row 39** (a database pull; A1 reads "Last updated 7 weeks ago"): lot 301274, security_tag 301274, production_date 2026-07-21 20:34:06, work order `OIL260721143336`, container_itag `CHARM10009434`, net_weight_kg 1,022.4, gross_weight **1,080.0**.
- **Tracker, 'Historical Tote Record' tab, row 1181:** reported_quantity 1,022.4, reported_on 2026-07-21 20:35:05, order_number `OIL260721143336`, gross_weight **1,080.0**, sectag 301274.
- **Inventory master, 'Q4 2025 -2026 Production Invent' tab, row 694:** gross **1,036.0**, tare 57.6, net 978.4, COLA_40, shipped 2026-09-17. The Notes column is blank. Ops Notes QOWV B40 copies this 1,036.0.

Across the other totes, the production system agrees with the ledger (my count):
- 'Oil_inventory_data' holds 37 of the 42 tags. For 36 of them, gross and net equal the ledger. The exception is 301274.
- 'Historical Tote Record' holds 40 tags under their own security tag, all with gross equal to the ledger. Tote 300022 is filed under tag 300020 (see 3.1). 301274 is the other exception.

So the tracker's 1,080.0 is the production system's own weighing, not a stray tracker entry. Nothing in the files shows which weighing is right.

What changes if 1,080.0 governs, with E40 left at 169.5 kg:
- Gross, net produced and injected each rise by 1,080.0 − 1,036.0 = 44.0 kg:
  - Total Mass Transported: 42,945.0 + 44.0 = 42,989.0 kg (Ops Notes QOWV B54)
  - Total Oil Produced: 40,525.8 + 44.0 = 40,569.8 kg (Ops Notes QOWV D54)
  - Total Oil in Batch: 34,179.5 + 44.0 = 34,223.5 kg (Ops Notes QOWV F54)
- Sequestration: 44.0 × 0.079 = 3.476, then 3.476 × 3.667 = 12.746492 kg CO2e higher.
- Production emissions. 301274 is July 2026 product at 0.120947 (Ops Notes QOWV H40): 44.0 × 0.120947 = 5.321668 kg CO2e higher.
- Transport process: 0.044 × 1,201 = 52.844 t-mi. On the flatbed factor: 52.844 × 0.1384 = 7.3136096 kg higher. 8.1 requires the BCU to move with it.
- Net effect with the BCU matched: 12.746492 − 5.321668 = 7.424824 kg CO2e higher. The submitted figure is conservative for this tote too.

Proposed wording for the 301274 sentence in checklist D19 (new text):

> Tote 301274: the tracker's gross is 1,080.0 kg against 1,036.0 kg in the Ops Notes (B40), 1,080.0 − 1,036.0 = 44.0 kg apart. The 1,080.0 is Manufacturo's production weighing (order OIL260721143336, 2026-07-21), recorded in the inventory master's Oil_inventory_data tab (row 39) and the tracker's Historical Tote Record tab (row 1181). The 1,036.0 comes from the master's Q4 2025-2026 Production Inventory tab (row 694). On 1,080.0 the tracker implies the same 169.5 kg post-unload weight as E40 (1,080.0 − 57.6 = 1,022.4; 1,022.4 − 852.9 = 169.5). If 1,080.0 governs, gross, net produced and injected each rise 44.0 kg: sequestration 44.0 × 0.079 × 3.667 = 12.746492 kg CO2e higher, production emissions 44.0 × 0.120947 = 5.321668 kg higher, so with the BCU matched the submission is conservative by 12.746492 − 5.321668 = 7.424824 kg.

### Challenge 2 — add Garrett's recorded position, and show the Fail does not depend on it

The registry's INJ-09-2026-W2-QOWV notes read: "COBB doubled rows: Garrett says COBB not source of truth." The full review asked for this to be put to Max, and checklist D19 still omits it. Add one sentence:
- If Max rules the tracker is not a source of truth, the 301215 comparison moves to the sidebar. 301215's 442.5 kg, the same as 301166's (Ops Notes QOWV E17), still needs confirming.
- The 301274 conflict stays in either case, because the 1,080.0 sits in the production system, not only in the tracker. The Fail stands on 301274 whatever Max rules.

### Challenge 3 — the fix reaches beyond Total Oil in Batch

Current fix in checklist D19: "confirm 301215's post-unload weighing and 301274's gross weighing and correct whichever record is wrong". Proposed:
- 301274: confirm which weighing governs, Manufacturo order OIL260721143336 (1,080.0) or the Q4 production inventory row 694 (1,036.0). Correct the losing record.
- If 1,080.0 governs, Ops Notes QOWV B40 changes. That carries into:
  - 2.1 and 5.3: transport mass 42,989.0 kg
  - 2.2 and 7.4: pyrolysis mass 40,569.8 kg (7.5's uncertainty is per tote and does not change)
  - 2.3 and 4.3: injected mass 34,223.5 kg
  - 8.1: the BCU
- 301215: confirm the post-unload weighing. If 162.0 governs, Ops Notes QOWV E26 changes and F54 becomes 34,179.5 + 280.5 = 34,460.0 kg.
- If both tracker-side figures govern, F54 is 34,460.0 + 44.0 = 34,504.0 kg. Sequestration rises by 280.5 + 44.0 = 324.5 kg of oil, then 324.5 × 0.079 = 25.6355, then 25.6355 × 3.667 = 94.0054 kg CO2e.
- Add a cross-reference sentence to checklist D17 (item 2.1) and D18 (item 2.2) pointing to 2.3. Keep their status: 2.3 carries the Fail.

### Low — wording

Checklist D19 says "on every other tote the tracker sits exactly 57.6 kg below the ledger". That holds in the three later imports. In the first import (rows 861–902), 301204 reads 1,540.8 kg: 1,540.8 ÷ 2 = 770.4, its figure in the later imports. Proposed wording (new text):

> on every other tote (in the first import, all but 301204, whose row is doubled; sidebar)

## 3.1 Pass — CHALLENGE: change to Flag, and correct the tag 300020 description

### What holds

- Tracker blocks start at rows 861, 1791, 2719 and 3682, with 42 rows each. 4 × 42 = 168.
- Security tag equals the ledger tag on 41 of 42 in every block (my count).
- The 42nd row reads security_tag 300020, consumed_lot 4746, quantity 666.4 kg, gross 1,012.0 kg. Ledger tote 300022 (Ops Notes QOWV row 51): gross B51 1,012.0, injected F51 724. Check: 724 − 57.6 = 666.4.
- Completion date is 2026-09-25 on all 168 rows.
- Tote 300040 (lot `LOT00004760`) reads 688.4 kg. Check: 746 − 57.6 = 688.4.
- None of the 42 tags appears in any other batch's row on the COBB tab.
- None appears in the W4 bio-oil, whole-oil or calciner rows. The W4 whole-oil tags are 301307, 301319, 301320, 301321, 301328, 301334, 301352 and 301353, and the calciner lot is `WILA004_offload_1`.

### The challenge

Checklist D22 (item 3.1) and sidebar B61 present tag 300020 as a tracker error ("which is tote 300022's lot"). The records point the other way:

| Record | Lot 4746 (gross 1,012.0) | Lot 4770 (gross 1,085.0) |
|---|---|---|
| Inventory master 'Oil_inventory_data' (Manufacturo pull) | tag **300020**, row 360, 2026-02-17, work order WO00001655 | tag 300020, row 350, 2026-02-24, WO00001665, COLA25 |
| Tracker 'Historical Tote Record' | sectag **300020**, row 840, 2026-02-17, WO00001655 | sectag 300020, row 850, 2026-02-24, WO00001665 |
| Inventory master 'Claude C 2025 -2026 Production' | tag **300020**, row 410 | tag 300020, row 420 |
| Inventory master 'Q4 2025 -2026 Production Invent' | tag **300022**, row 410, COLA_37, 2026-09-09 | tag 300020, row 420, COLA_25, 2026-07-16 |
| Ops Notes QOWV tab | tag **300022**, row 51, "MFO Lot 4746 (LOT00004746), February 2026" | — |
| Tracker COBB tab | tag **300020**, W4 rows 901, 1831, 2759, 3722 | tag 300020, `INJ-20260726_aqueous_fraction`, 883.0 kg, completed 2026-07-31, rows 455, 1380, 2308, 3271 |

- Manufacturo assigned security tag 300020 to two lots. Tag 300022 appears only in the Q4 production inventory tab and the Ops Notes. Neither 'Oil_inventory_data' nor 'Historical Tote Record' has any row under 300022.
- As a result, the tracker records tag 300020 as injected twice: in the July batch INJ-20260726 (lot 4770) and in W4 (lot 4746).
- No mass is counted twice: the lots and weights differ. But the custody identifier for this tote is inconsistent. Anyone tracing tag 300022 back to production finds no production record. Anyone tracing tag 300020 finds two injections.

Grading. The lot number (4746) and the weights (gross 1,012.0, net 954.4) agree in every record, so a verifier can confirm the reported mass through the lot. That meets the Flag definition: "Process hygiene or documentation issue that does NOT prevent verification". If Max treats the metal security tag as the custody key, this becomes the reviewer skill's "vehicle identifiers don't match" case, which is a Fail. Either way it cannot stay an ungraded remark inside a Pass.

Proposed: status Flag, and this wording for the tracker sentence in checklist D22 (new text):

> 41 of 42 security tags match the ledger. The 42nd carries tag 300020 on lot 4746 (666.4 kg, gross 1,012.0, which is tote 300022's lot and gross; 724 − 57.6 = 666.4). Manufacturo's production records give tag 300020 for both lot 4746 (2026-02-17) and lot 4770 (2026-02-24); only the Q4 production inventory tab and the Ops Notes give 300022. The tracker therefore records tag 300020 as injected in INJ-20260726 (lot 4770, 883.0 kg, 2026-07-31) and again here. Lot and mass agree in every record. Fix for Garrett: confirm the metal tag on lot 4746's tote and correct Manufacturo or the Q4 tab to match.

## Sidebar notes

### B61 — CHALLENGE

Holds:
- The block start rows.
- 301204 at 1,540.8 kg in the first block and 770.4 kg in the other three.
- Lot 4770 shipped on COLA_25 on 2026-07-16 (inventory master 'Q4 2025 -2026 Production Invent' row 420).
- W4 bio-oil: 14 rows in each block.

Two corrections:
1. **The four blocks are four separate import snapshots, stacked on one tab.** The tab's 'Import Time' column, which `cobb_w4_aqueous_rows_live.json` did not capture, gives:

   | Import | Tab rows | W4 aqueous block | pH on W4 rows | 301204 |
   |---|---|---|---|---|
   | 2026-09-29 08:37:20 | 3–926 | 861–902 | 2.97 | 1,540.8 |
   | 2026-09-29 11:54:56 | 927–1854 | 1791–1832 | 2.97 | 770.4 |
   | 2026-09-30 11:14:57 | 1855–2817 | 2719–2760 | 2.97 | 770.4 |
   | 2026-10-05 12:24:22 | 2818–3805 | 3682–3723 | blank | 770.4 |

   - Every batch is repeated this way. For example, INJ-20260726_aqueous_fraction has 65 rows in each import (my count).
   - The newest import is rows 2818–3805. The tab header reads "Last updated 23 hours ago".
   - So "the first block still reads 1,540.8" means the oldest snapshot does. The newest snapshot reads 770.4.
   - W4 whole oil is not a uniform repeat: 10 rows in the first import (301307 and 301321 each appear twice, once with no tag or gross) and 8 in each later one.
2. "Every copy of tote 300022 carries security_tag 300020, a different tote" should follow 3.1: the tag comes from Manufacturo's production record, and tag 300020 is also recorded as injected in INJ-20260726.

Proposed wording for B61 (new text):

> Bio-oil Injection Tracker (live export 2026-10-06), COBB tab: the tab holds four stacked import snapshots (2026-09-29 08:37, 2026-09-29 11:54, 2026-09-30 11:14, 2026-10-05 12:24), so every batch appears four times; the W4 aqueous blocks start at rows 861, 1791, 2719 and 3682. The oldest snapshot reads 1,540.8 kg for 301204, twice the 770.4 kg in the later three. Tote 300022 carries security_tag 300020 in every snapshot, as in Manufacturo's production record, and tag 300020 is also injected in INJ-20260726 (lot 4770; 3.1). Elsewhere consumed quantity is the Ops Notes net injected mass less 57.6 kg. Certify uses the ledger figures.

### B62 — Agree (wording)

Name-based comparison of the 2026-09-28 rows with each live block, over the 19 columns both exports share:
- The only changes are injection_ph (blank to 2.97 in the first three imports) and 301204's quantity (1,540.8 to 770.4 in the last three imports).
- 301215, 301274 and the 300020 row are unchanged on every shared column.
- `tote_gross_weight` is a column new to the live export, so 301274's 1,080.0 is new information since 2026-09-28, not an unchanged entry.

Proposed ending for B62 (new text):

> ...the 301215, 301274 and 300020 quantities did not change; 301274's gross (1,080.0 kg) is visible for the first time (2.3).

Separately, the `field_diffs_vs_0928` list in `cobb_w4_aqueous_rows_live.json` compares columns by position. Columns 14–16 carry different headers in the two exports:
- 2026-09-28: 'Proportion of Origin Consumed', 'Origin Mass', 'Consumed Origin Mass'
- Live: 'tote_gross_weight', 'weighing_order', 'weighing_date'

Its "weighing_date 0 → None" entries are therefore not real changes; 'Consumed Origin Mass' reads 0 in both exports. The checklist does not rely on them.

### B63 — CHALLENGE

Holds: Ops Notes QOWV K6 reads 'pH range (target)' and L6 reads '2.0 - 4.0'. 2.97 is inside that range.

Corrections:
- The newest import (2026-10-05 12:24:22) has no pH on any W4 row. The same holds for W1, W2 and W3: in each week, pH is filled in the three older imports and blank in the 2026-10-05 import (W1 2.89, W2 2.92, W3 2.7). "The tracker now records" overstates it.
- The tracker puts 2.97 on every W4 row: aqueous, bio-oil, whole oil and calciner. It is the same figure as Ops Notes AECN Truck H28 and Kerry D18. Both carry the cell note "Wellhead pH = weekly median of Ignition PH-1041, gated to StateRun=1; provided by G. Lutz 2026-09-30." It is a weekly wellhead figure for the site, not a QOWV measurement.

Proposed wording for B63 (new text):

> pH: the tracker carries injection_ph 2.97 on every W4 row (all products) in its three older imports and none in the newest (2026-10-05). It is the weekly wellhead pH also in Ops Notes AECN Truck H28 and Kerry D18 (cell note: 'Wellhead pH = weekly median of Ignition PH-1041, gated to StateRun=1; provided by G. Lutz 2026-09-30'), inside the QOWV!L6 target '2.0 - 4.0'. The QOWV tab records only the target; adding the same 2.97 there would match the other tabs.

### B64 — Agree (wording)

- 442.5 − 57.6 = 384.9 kg residue each. Batch residue 6,346.3 kg (shown under 2.3).
- The tracker agrees for 301166 (593.9 = 651.5 − 57.6) and contradicts 301215.
- "Roughly 37 % of the tote" mixes bases. 301166's net oil is 1,094.0 − 57.6 = 1,036.4 kg; 301215's is 1,041.0 − 57.6 = 983.4 kg.
  - 301166: 384.9 ÷ 1,036.4 = 0.3714 of its net oil
  - 301215: 384.9 ÷ 983.4 = 0.3914 of its net oil

Proposed wording for B64 (new text):

> about 385 kg of residue each (384.9 ÷ 1,036.4 = 0.3714 of 301166's net oil; 384.9 ÷ 983.4 = 0.3914 of 301215's)

---

## Challenges in priority order

1. **2.3: rewrite the 301274 reasoning; keep Fail.**
   - Manufacturo's production weighing (order OIL260721143336, 2026-07-21) gives 1,080.0 kg, in both the inventory master's 'Oil_inventory_data' tab row 39 and the tracker's 'Historical Tote Record' tab row 1181. Only the Q4 production inventory tab row 694 and the Ops Notes give 1,036.0.
   - If 1,080.0 governs, transport, pyrolysis and injected masses each rise 44.0 kg, and the submission is conservative by 12.746492 − 5.321668 = 7.424824 kg CO2e.
   - Add Garrett's "COBB not source of truth" position. The 301274 conflict survives it, so the Fail does not rest on the tracker alone.
   - Widen the fix to 2.1, 2.2, 4.3, 5.3, 7.4 and 8.1.
2. **3.1: Pass to Flag.**
   - Manufacturo assigns tag 300020 to both lot 4746 and lot 4770. Tag 300022 exists only in the Q4 tab and the Ops Notes.
   - The tracker records tag 300020 as injected in INJ-20260726 (883.0 kg, 2026-07-31) and in W4.
   - Lot and mass agree everywhere, so Flag, or Fail if Max treats the security tag as the custody key.
3. **B61: say the four blocks are four stacked import snapshots** (Import Time column), the newest being 2026-10-05 12:24:22. Carry the 300020 correction.
4. **B63: pH.** The newest import has none, and 2.97 is the site's weekly wellhead pH applied to every product.
5. **Low:** B62 wording on 301274's newly visible gross; D19 "every other tote" wording for 301204; B64 percentage basis; the positional column comparison in `cobb_w4_aqueous_rows_live.json`.
