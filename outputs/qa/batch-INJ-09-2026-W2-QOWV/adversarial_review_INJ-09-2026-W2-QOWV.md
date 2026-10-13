# Adversarial Review: INJ-09-2026-W2-QOWV (Aqueous)

- **Checklist reviewed:** `outputs/qa/batch-INJ-09-2026-W2-QOWV/Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W2.xlsx` (opened read-only; not modified)
- **Reviewer:** independent adversarial reviewer (Claude sub-agent), 2026-09-29
- **Scope:** files on disk. Certify values were checked against the source-read log, not Certify itself.
- **Sources opened for this review:** knowledge base; `adversarial-reviewer/SKILL.md`; `batch-qa-charm/SKILL.md`; `checklist_structure.md`; source-read log; W2 Ops Notes export of 2026-09-22 (`source_exports/INJ-09-2026-W2_Ops_Notes.xlsx`); W2 Ops Notes export of 2026-09-28 (`batch-INJ-09-2026-W3-QOWV/source_exports/prior_weeks/INJ-09-2026-W2_Ops_Notes_1OEJvg.xlsx`); seven Production Period Summary exports; Standard EFs export; inventory master export (tabs `Q4 2025 -2026 Production Invent`, `Archive- 2024-2025 Production I`, `Oil_inventory_data`, `Shipment Tracker (Nov 2025+)`); Bio-oil Injection Tracker export (tabs `Basco Injection -- COBB` rows 758-797, `Historical Tote Record`); SGS certificate PDF; retirement certificate PDF; route map PNG; `recompute_qowv.py` (run: exit 0) and `recompute_output.txt`.
- **Note on figures:** every figure not quoted from a file is either shown with its arithmetic or labelled COMPUTED. COMPUTED means a sum I ran over the named column of the named file.

## Step 0: primary-source check

Every Certify-based item cites values read from the component windows, and those values are in the log. Three gaps:

1. **August 2025 summary (PP#9) is not on disk.** The log's `pp9_summary` records `"action": "csv_export_read"` and has no `artifact_path`. The PP#9 CI used in 3.5 and 7.2 cannot be checked against a saved file.
2. **The Certify-attached copy of the Ops Notes is not on disk.** Items 4.2, 5.4, 6.3, 7.3 and 7.6 confirm the attachment from the Sources-tab listing. Item 7.3 also asserts what the attached file contains (see challenge 7.3).
3. **`recompute_qowv.py` does not recompute the 7.2 figures.** Its last line prints `x['total_effect_kg']`, `x['pe_corrected_kg']` and `x['ci_corrected']` from the log's `tote_inventory_crosscheck`. It reads the 2026-09-22 export and no later one.

---

## 1. Challenged Items

### 3.5 and 3.2: production-period mismatches (Fail)

- **Current status:** Fail (both)
- **Issue:** The Fail is right: the Ops Notes and the inventory disagree on 8 totes. The reasoning for which record is right does not hold for 3 of the 8.

**(a) The tie test was run on the periods the totes leave, not the ones they join.** D26 reads: "The production summaries confirm the inventory: the December 2025 summary's Aqueous Mass of Output reads 19,161.0 kg ... and the October 2025 summary reads 42,860 kg". The summaries for the periods the totes would move into do not tie to the inventory. Inventory figures are COMPUTED: sums of column K `Net Weight (kg)` over QOWV rows of tab `Q4 2025 -2026 Production Invent` with that column B period. Summary figures are each file's row 4 `Mass of Output (kg)`.

| Period | Inventory, COMPUTED (totes) | Summary Aqueous | Ties? |
|---|---|---|---|
| December 2025 | 19161.0 kg (20) | 19,161.0 | Yes, without the 5 ledger-December totes |
| October 2025 (`2026 PP#11`) | 42860.2 kg (43) | 42,860 | Yes, without 228470 and 228485 |
| May 2026 | 36523.2 kg (38) | 36,523.2 | Yes, without 301108 (not cited in the checklist) |
| `2025 PP#10` (September file) | 44931.0 kg (46) | 41,010 | **No**: without 228470/228485, 44,931.0 − 1,072.4 = 43,858.6; 43,858.6 − 889.4 = 42,969.2 |
| `April 2026 PP` | 45764.8 kg (47) | 43,912.0 | **No**: without 301108, 45,764.8 − 989.4 = 44,775.4 |
| `2025 PP#8` | 76217.1 kg (80) | 77,076 | **No** |

**(b) For 228470, 228485 and 301108, the production-date records agree with the Ops Notes, not the inventory.**

- *228470.* `Historical Tote Record` row 611: `reported_on` 2025-10-08 14:58, order `WO00001397`, lot `LOT00003968`. `Oil_inventory_data` row 505: `production_date` 2025-10-08.
- *228485.* `Historical Tote Record` row 613: 2025-10-08 15:16, `WO00001399`, `LOT00003972`. `Oil_inventory_data` row 503: 2025-10-08.
- *Lot sequence.* The last September production is Historical Tote Record rows 603-605 (2025-09-30, lots 3930-3934). October lots 3948-3954 follow at rows 606-609 (2025-10-03); the inventory labels those same lots "2026 PP#11" / Blue2510 at its rows 223-226. Lots 3956-3974 come next, at rows 610-614 (2025-10-03 to 2025-10-08). Yet inventory rows 227-231 label lots 3956-3974 "2025 PP#10" / Pink259, as do archive rows 778 and 780.
- *301108.* `Historical Tote Record` row 1042: `reported_on` 2026-05-01 16:15, order `OIL260501101214`. `Oil_inventory_data` row 174 has `production_date` 2026-05-01, but its own `Production Period` field reads "April 2026 PP". Inventory row 557 also reads "April 2026 PP" (Red2604). The records conflict.

**(c) The inventory is well supported for the five "December 2025" totes.**

- All five shipped 2025-12-01 (inventory column N).
- The December label traces to the Louisiana receiving entries. `Oil_inventory_data` rows 449 and 451-454 give each tote `production_date` 2025-12-01, with `site_location` "CHARM_LOUISIANA" and `location` "Bio Oil Incoming". That is the receiving date, not a production date.
- Production dates:
  - 015162: `Historical Tote Record` row 469, 2025-07-28; inventory D111, 2025-07-28.
  - 228490: row 590, 2025-09-19.
  - 245140: inventory D179, 2025-08-29; archive row 717, PP 9.
  - 245103 and 245142: no Historical Tote Record entry. Their support is the inventory (rows 194, 191) and the archive (rows 735, 731, PP 10).

**(d) The gross differences come from different weighings, not a typing error.** The ledger's 945.6, 1,071.6, 1,051.6 and 1,013.6 are the Louisiana receiving weights (`Oil_inventory_data` rows 451-454, column `gross_weight`). The inventory's figures are production weights (Historical Tote Record row 469 reads 946.0 for 015162).
- Difference per tote: 946.0 − 945.6 = 0.4 kg. Four totes: 4 × 0.4 = 1.6 kg of injectant.
- Sequestration effect, conservative: 1.6 × 0.083 = 0.1328; 0.1328 × 3.667 = 0.487 kg CO2e.

- **Recommendation:** Keep Fail, since the two records disagree on all 8 totes whichever is right. Rewrite D23 and D26:
  - drop "The production summaries confirm the inventory";
  - show the tie results for every period;
  - state the December labels as wrong, with the evidence in (c);
  - state that for 228470, 228485 and 301108 the production-date records side with the Ops Notes, and that this is unresolved.

### 7.2: CI effect (Fail)

- **Current status:** Fail
- **Issue:**
  1. **The arithmetic reproduces.** On the inventory's periods for all 8 totes, with PP#9 at 0.11057, I get an overstatement of 103.4783 kg. Production emissions: 4,650.1228 − 103.4783 = 4,546.6445 kg. CI: 4,546.6445 ÷ 36,641.6 = 0.1240842239. The checklist has 103.4781, 4,546.6447 and 0.1240842287; both round to 0.124084.
     - Per-tote effects: 4.8896, 33.9046, 34.8533, 52.1767, 32.8597, -18.9514, -15.7174 and -20.5369 kg. They match the log except 245140, where the log has 52.1765 (52.1767 − 52.1765 = 0.0002 kg).
  2. **The all-8 basis is not established** (see 3.5 (b)). The corrected figure depends on the basis chosen:

     | Basis | Overstatement | Production emissions | CI |
     |---|---|---|---|
     | Inventory for all 8 (checklist) | 103.4783 kg | 4,650.1228 − 103.4783 = 4,546.6445 kg | 0.1240842239 |
     | Five December totes (production dates) | 158.6840 kg | 4,650.1228 − 158.6840 = 4,491.4388 kg | 0.1225775846 |

     The five-tote figure: 4.8896 + 33.9046 = 38.7942; 38.7942 + 34.8533 = 73.6475; 73.6475 + 52.1767 = 125.8242; 125.8242 + 32.8597 = 158.6839. It reads 158.6840 kg before rounding. The inventory basis gives higher emissions, so it is the conservative choice.
  3. **The live sheet has moved.** The 2026-09-28 export differs from the 2026-09-22 export in 11 QOWV cells:
     - G11 "MFO Lot not assigned, July 2025", H11 0.1575553394801048
     - G12 "MFO Lot 3868 (LOT00003868), September 2025", H12 0.12868956697570233
     - G13 "MFO Lot not assigned, September 2025", H13 0.12868956697570233
     - G14 "MFO Lot not assigned, August 2025", H14 0.11056982394624702
     - G15 "MFO Lot not assigned, September 2025", H15 0.12868956697570233
     - H50 is now `' '` (the weighted-average formula is gone)

     G19 ("... May 2026"), G47 and G48 ("... October 2025") are unchanged. That sheet computes I50 = 4491.438649 kg and a CI of 4,491.438649 ÷ 36,641.6 = 0.1225775798. The checklist's fix, "relabel G11:G15, G19, G47 and G48 to the inventory periods ... change Certify's 'QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)' to 0.124084", would override three rows the sheet has left as they are. It would also put a CI in Certify that the current Ops Notes does not show.
  4. **PP#9 CI.** The checklist's 0.11057 is "6,541 kg CO2e over 59,157 kg", built from a summary's rounded display figures, and that summary is not on disk. The 09-28 sheet's H14 holds 0.11056982394624702. With that value the all-8 overstatement is 103.4785 kg (103.4785 − 103.4783 = 0.0002 kg), which is immaterial, but the source is not preserved. The archive's PP 9 Aqueous total (COMPUTED over column M) is 59157.4 kg over 61 totes, which supports the mass.
- **Recommendation:** Keep Fail. Base the finding on the five December totes alone (158.6840 kg, far above the 0.001 tCO2e tolerance), and give both corrected CIs in D44 (table in point 2) instead of one.
  - Before any Certify change, one ruling is needed on which record sets a tote's period. The QA agent should take it to Max with the evidence in 3.5 (b).
  - Then set Certify's CI to whatever the re-attached Ops Notes computes, and restore H50.
  - Save the August 2025 summary to `source_exports/`.
  - Add PP#9, September 2025 and October 2025 to K10:M20 with links.
  - Make `recompute_qowv.py` compute the correction from the inventory export instead of printing it from the log.

### 3.4: Batch mileage allocation (Pass)

- **Current status:** Pass
- **Issue:** D25 reads "Truck 1: 18/40 = 0.45 share x 1,201 mi = 540.45 mi". Allocation tab A12 reads "Truck 1 (CO_AQUEOUS_12.01.25)", with C12 = 40 totes. The records on disk show two trucks, not one:
  - **Receiving record.** `Oil_inventory_data`, column `shipping_order_number`, lists two orders on 2025-12-01. "CO_AQUEOUS_12.01.25" has 20 totes; 9 are in this batch (245140, 245142, 228485, 228470, 245165, 245112, 245121, 245164, 245144). "CO_AQUEOUS_12.1.25_T2" has 20 totes; 9 are in this batch (228490, 015162, 245103, 228432, 228410, 245157, 245107, 245172, 015170).
  - **No order in that record holds more than 20 totes** (33 orders beginning "CO" or "COLA"). COLA_34 carries 20 totes in the inventory.
  - **Source of the 40.** The figure matches the inventory tab `Shipment Tracker (Nov 2025+)`, whose row 1 reads "Shipment Tracker — totes grouped by Date Shipped (col M of Q4 2025-2026 Production Inventory Master)". Its truck numbers group totes by ship date, not by vehicle. Its "Truck 2" of 2025-12-02 (36 totes) is orders "CO_AQUEOUS_12.2" (18) plus "CO_AQUEOUS_12.2_02" (18).
  - **Governing rule.** The knowledge base (§6) states: "Embodied emissions are always per-mile (or per-vehicle-lifetime amortized to per-mile)." The Charm skill gives "RP Share of Truck = N_totes_in_RP / N_totes_on_Truck".
  - **Per-truck figures.**
    - Share per truck: 9 ÷ 20 = 0.45. Miles per truck: 0.45 × 1,201 = 540.45.
    - Both trucks: 540.45 + 540.45 = 1,080.90 mi. Add COLA_34: 1,080.90 + 1,201 = 2,281.90 mi.
    - Embodied emissions: 2,281.90 × 0.0001927908256 = 0.43993 t, against Certify's 0.336 t. Understated by 0.43993 − 0.33574 = 0.10419 t, in the non-conservative direction.
    - Transport process emissions are unaffected, since they scale with mass × distance.
- **Recommendation:** Fail, unless a bill of lading shows both orders moved on one vehicle. Split row 12 into two rows (20 totes and 9 batch totes each). Change Certify's "QOWV Embodied Distance (CO to B6)" to 2,281.9 mi. Item 6.2 stays Pass (Certify equals the tab), but its value moves with this fix. The "2 shipping orders" in D15 and D22 become 3.

### 8.1: BCU versus process emission (Fail)

- **Current status:** Fail
- **Issue:** BCU 6,454 kg against process emissions of 6,454.327 kg on the EF-sheet factor and 6,454.494 kg on the 0.086 factor. The shortfall is 0.327 to 0.494 kg: 0.327 ÷ 1,000 = 0.000327 tCO2e, and 0.494 ÷ 1,000 = 0.000494 tCO2e.
  - The Charm skill's key classification allows "no rounding tolerance beyond ~0.001 tCO2e". `checklist_structure.md` 8.1 attaches "any size" to over-coverage, not to under-coverage: "BCU < transport process activity (under-reduction), OR BCU > transport process activity (over-coverage, any size)". The shortfall is inside the tolerance and lowers net by at most 0.000494 t, so it is conservative.
  - The recommended fix, "enter the constant as the exact process emission, 6,454.494 kg on the current 0.086 factor", carries its own risk. 0.0001384 MT/t-mi is 0.1384 kg/t-mi, and 0.1384 ÷ 1.609344 = 0.0859978 kg/(t·km). D33 itself calls 0.086 "Certify's display units", and the knowledge base (§6) states: "Never use Certify's displayed EF values for independent calculations. Certify rounds/converts EFs for display". If Certify stores the sheet value, 6,454.494 kg exceeds the emission by 6,454.494 − 6,454.327 = 0.167 kg. The Charm skill's BCU QA Rule says: "Over-coverage (BCU > activity) is always a FAIL, whatever the size."
- **Recommendation:** Flag. Enter 6,454.327 kg, the EF-sheet figure. It is at or below the process emission on either factor, so it cannot over-cover.

### C.1: independent recompute (Pass)

- **Current status:** Pass
- **Issue:**
  1. **D54 answers a different question.** It reads: "This reproduces the removal as submitted, so 4.484 t carries the 3.5/7.2 CI error (net 0.10348 t low)". The item asks whether net recomputes from source values, and the checklist's own 7.2, plus 3.4 above, find two inputs wrong.
     - Net from the submitted inputs, holding Certify's 41 kg discount fixed, is 4,484.37 kg (EF-sheet basis).
     - Corrected figures:

       | Period basis | Net, CI fixed | Net, CI and 3.4 fixed |
       |---|---|---|
       | Inventory | 4,484.37 + 103.4783 = 4,587.85 kg | 4,587.85 − 104.194 = 4,483.66 kg |
       | Five December totes | 4,484.37 + 158.684 = 4,643.05 kg | 4,643.05 − 104.194 = 4,538.86 kg |

     - The submitted 4.484 t matches the inventory-basis figure because two errors offset: production overstated by 103.4783 kg, embodied understated by 104.194 kg.
  2. **The discount explanation does not reproduce Certify's 41 kg.** D54's "sqrt(0.004^2 + 0.00138^2) = 0.00423 of the 9.512 t sequestration = 0.0402 t, or 40.2 kg" does not give 41 kg; my figure for that route is 40.243 kg. Add the process-mass uncertainty (7.163 kg) and the pyrolysis-mass uncertainty (5.469 kg): the square root of the sum of the three squares is 41.240 kg, which rounds to 41. The 41 kg is Certify's figure used as an input, and `recompute_qowv.py` takes it from the log.
- **Recommendation:** Fail, with the figures above and the offsetting-error note. State the discount as taken from Certify, not reproduced.

### 7.1: production periods captured (Pass)

- **Current status:** Pass. Keep it: all 38 totes' 36,641.6 kg is in the single component, so no period is left out.
- **Issue:** D43 reads "July 2025 (1 tote), September 2025 (10), October 2025 (2), December 2025 (5), April 2026 (6), May 2026 (14)". Those are the ledger labels that 3.5 finds wrong.
- **Recommendation:** Correct the evidence to state the counts on each basis:
  - Inventory: PP#8 2, PP#9 1, PP#10 15, April 7, May 13.
  - Production dates: July 2, August 1, September 13, October 2, April 6, May 14.

### 7.3: CI evidence (Flag)

- **Current status:** Flag. Keep it: the item's pass condition (Ops Notes attached to the CI datapoint) is met per the log.
- **Issue:** D45 reads "which holds the per-tote CI column and the weighted-average cell" and "12 of 38 totes".
  - In the 09-28 export, H50 is `' '`, and H11:H15 are typed constants with no link. PP#9's 0.11056982394624702 has no entry in K10:M20.
  - Typed, unlinked CIs now cover rows 11-15 (5 totes) and 36-48 (13 totes): 5 + 13 = 18 totes.
  - D45 says the linked periods' rows "reference it by cell ($L$12, $L$16, $L$17)". Row 36 (015170, July) holds a typed 0.1575553394801048 rather than `=$L$10`.
  - No copy of the attached file is on disk, so its contents are not shown.
- **Recommendation:** Update D45 to the 09-28 state. Download the Certify-attached Ops Notes into `source_exports/` and confirm which version is attached.

### 1.2: Ops Notes complete (Pass)

- **Current status:** Pass
- **Issue:** D14 reads "Summary cells all resolve to values, no formula errors: ... weighted CI 0.1269082907". In the most recent export on disk (09-28), H50 is `' '`. `checklist_structure.md` 1.2 lists "missing summary totals" as a fail mode.
- **Recommendation:** Re-export the live sheet. If H50 is still blank, mark Fail. If it has been restored, keep Pass and cite the new value.

### Sidebar B58: lab certificate footnote (no status)

- **Issue:** B58 reads "The lab certificate carries the '#' footnote against QOWV Carbon 8.3 % and Hydrogen 9.9 %".
  - On page 1 (SR26-05494.001, QOWV), the "#" mark sits at the end of the Carbon row, and the Hydrogen row (9.9 % (m/m)) carries none.
  - On page 2 (SR26-05494.002, AECN), both Carbon (40.4) and Hydrogen (7.0) carry the mark.
  - The footnote reads "# - Result is outside of test method limits and/or analytical range used in method precision study".
- **Recommendation:** Change B58 to name Carbon without Hydrogen.

---

## 2. Confirmed Items

- **1.1 (Pass).** Certificate SR26-05494.001, page 1: Client ID "9-2026-W2-QOWV", "Oil - QOWV", sampled 05-Sep-2026 12:00. Carbon 8.3, Hydrogen 9.9, Nitrogen <0.75, viscosity 0.9420 cSt, acid number 41, density 1.047 g/cm³.
- **1.3 (Pass).** The allocation tab is complete: rows 12-13, D6 `=COUNTA(QOWV!A11:A48)` gives 38, B8 = 1201, G15 = 1,741.45. The shipping-order count is corrected under 3.4.
- **2.1 (Pass).** B50 `=SUM(B10:B48)` = 38,830.4. My re-sum of B11:B48 matches (row 10 is a header).
- **2.2 (Flag).** C11:C48 all read 57.6.
  - Inventory QOWV tare values: 566 rows at 57.6 (365 steel, 200 plastic, 1 blank) and 73 at 62.93 (41 steel, 32 plastic). No comment on J2 "Tare Weight (kg)".
  - The archive tab's tare, 57.6062 kg, is a pound-based standard: 127 × 0.453592 = 57.6062.
  - D50 = 36,641.6.
- **2.3 (Pass).** F11 `=IF(E11="","",B11-E11)`. F50 = 31,250.9. Column E ranges 144.0 to 368.0. Summary E12 "Sparging Loss (kg)" = 0.0 and F12 "Filtration Loss (kg)" = 0.0. See Observation 1 on how column E is defined.
- **2.4 (Pass).** J = `2.5*$L$4` with L4 = 0.453592: 2.5 × 0.453592 = 1.13398 kg per tote, and 1.13398 × 38 = 43.09124.
- **3.1 (Pass).** 18 + 20 = 38 batch totes, equal to the 38 ledger rows. The injection tracker holds 38 rows (760-797) under "INJ-09-2026-W2_aqueous_fraction", all dated 2026-09-05.
- **3.3 (Pass).** E12 `=D12/C12`, E13 `=D13/C13`, G12 `=E12*F12`, G13 `=E13*F13`, G15 `=SUM(G12:G13)`, F12/F13 `=$B$8`. All are formulas; C12 and D12 are typed inputs.
- **4.1 (Pass).** 8.3% in the log's window read, on the certificate, and in Summary E21 (0.083).
- **4.2 (Pass).** The log's `attachment_map` links "Carbon Content of Bio-oil Injected (per injection)" to the Ops Notes and the certificate.
- **4.3 (Pass).** The log's 43.09124 kg matches J50 = 43.09124.
- **4.4 (Pass).** 0.004 × 8.3 = 0.0332. Summary G21 `=E21*H21` = 0.000332 (as a fraction).
- **5.1 (Pass).** EF sheet 2026 tab, row 7, "Truck Transport Fuel Use (Well to Wheel) -- Flatbed Truck", 0.0001384 MT CO2e/t-mi, GLEC V3.2 2025. 38.8304 × 1,201 = 46,635.31 t-mi, and 46,635.31 × 0.0001384 = 6.45433 t.
- **5.2 (Pass).** Map PNG shows options of 1,132, 1,129 and 1,201 miles; 1,201 ("via I-70 E") is the longest and is the figure used.
- **5.3 (Pass).** 38,830.4 kg = B50.
- **5.4 (Pass).** The log links "QOWV Transport Mass (CO to B6) [Certify input]" to the Ops Notes.
- **5.5 (Pass).** The log's 43.09 kg is 43.09124 rounded for display.
- **6.1 (Pass).** EF sheet row 12, "Vehicle Embodied Emissions --Non-Tanker Truck", 0.0001927908256 MT CO2e/mi. 1,741.45 × 0.0001927908256 = 0.33574 t.
- **6.2 (Pass).** Certify's 1,741.45 mi = G15. The value changes with the 3.4 fix.
- **6.3 (Pass).** The log shows two sources on "QOWV Embodied Distance (CO to B6) [Certify input]": the Ops Notes and "CO to Basco Routing Map.png".
- **7.4 (Pass).** 36,641.6 kg = D50.
- **7.5 (Pass).** The log's 43.09 kg on the pyrolysis mass. The input is dominant: 4.650 ÷ 4.484 = 1.037, i.e. pyrolysis emissions exceed net.
- **7.6 (Pass).** The log links "QOWV Pyrolysis Mass [Certify input]" to the Ops Notes. No Charm Contents sheet appears in the log's Drive-folder or Certify Sources listings.
- **9.1 (N/A).** I searched every cell string in all 10 tabs for "lcs", "calcium" and "buffer": zero hits. The workbook has zero cell comments.
- **Sidebars.**
  - B56: allocation tab A56 reads "--- Shipment 2025-12-10 --- (14 of 35 totes on this truck are W4-relevant)", followed by 14 rows (58-71) assigned "INJ-05-2026-W4".
  - B57: the October file's tab is named "September PP Summary"; its WODO is 14,227.0 against 12,630.0 in the September file.
  - B59: tracker rows 760-764 carry the tag in `consumed_lot` with `security_tag` blank.
  - B60: ship dates 2025-12-01 and 2026-08-26.

## 3. Observations (not raised by the checklist)

1. **The injection tracker disagrees with the Ops Notes on injected mass.**
   - On all 38 rows (760-797), `quantity_consumed_in_injection` equals Net Oil Produced minus Empty Tote Weight (D − E). The Ops Notes' Net Oil Injected is B − E, so the tracker is 57.6 kg lower per tote. Example: 015162 is 598.0 against 655.6 (655.6 − 598.0 = 57.6).
   - Rows 776, 777, 780 and 784 (301132, 301133, 301156, 301195) are doubled; for example, 1,420.8 = 2 × 710.4.
   - Totals:
     - tracker column: 32253.2 kg (COMPUTED);
     - doubled amounts: 710.4 + 839.4 = 1,549.8; 1,549.8 + 823.4 = 2,373.2; 2,373.2 + 817.9 = 3,191.1;
     - tracker without the doubling: 32,253.2 − 3,191.1 = 29,062.1 kg;
     - Ops Notes and Certify: 31,250.9 kg.
   - Which is right depends on whether column E ("Empty Tote Weight (kg)") includes the 57.6 kg tote, and no file on disk defines it. If the tracker's reading were right:
     - the injectant would be overstated by 38 × 57.6 = 2,188.8 kg;
     - sequestration by 2,188.8 × 0.083 = 181.67, then 181.67 × 3.667 = 666.2 kg CO2e;
     - that is 0.6662 ÷ 4.484 = 0.149 of net.
   - The QA agent should get the Basco weighing method for column E and add the tracker's quantity to the 2.3 comparison.
2. **The live Ops Notes changed after the export the checklist and recompute use** (see 7.2 (3)). The editor cannot be identified from disk. The checklist, revised 2026-09-29, describes the 2026-09-22 state.
3. **The route map's origin box reads "Your location"**, not a named address. The pin sits near Denver. The 5.2 note does not mention this.
4. **The truck grouping in 3.4 may affect other batches.** Any batch that used truck counts from the date-grouped `Shipment Tracker (Nov 2025+)` tab may be affected. Its "Truck 2" on 2025-12-02 (36 totes) is two shipping orders of 18 in the receiving record.
5. **Status counts if these recommendations are adopted:** Pass 23, Flag 3, Fail 6, N/A 1 (33 items). The changes are 1.2 Pass→Fail, 3.4 Pass→Fail, C.1 Pass→Fail and 8.1 Fail→Flag. B62 currently reads "Pass 26 | Flag 2 | Fail 4 | N/A 1 (33 items)".
