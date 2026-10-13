# Adversarial review — INJ-09-2026-W3-QOWV

- **Checklist:** `Charm_Aqueous_QOWV_QA_Checklist_INJ-09-2026-W3.xlsx`, 33 items; B63 reads "Pass 26 | Flag 2 | Fail 4 | N/A 1 (33 items)".
- **Removal:** rmv_1M38CNSFV1S0B7V7, Aqueous (QOWV), 37 IBC totes, Fort Lupton CO → Basco 6.
- **Reviewer:** Claude, Gate 3 adversarial review, 2026-09-28. Read-only, files on disk only. No browser, Certify or Drive.
- **Limit:** Certify datapoint values, sources and links (Sections 4–8) come from the QA agent's source-read log (`certify.component_by_key`, `certify.attachment_map`). `certify_components_snapshot.yml` holds component totals: 9.038, 6.264, 0.331, 4.978, BCU 6.264, removal "3.69 tCO₂e". I tested these against the on-disk sources. I did not re-read the registry.
- **If every recommendation is adopted:** Pass 23, Flag 4, Fail 5, N/A 1.

---

## Challenged Items

### 1. Item 3.2 — "Do all totes identified for RP match the Ops Notes for the applicable batch?"
**Current status:** Pass

**Issue:**
- The skill defines 3.2 as the per-attribute match. `checklist_structure.md` 3.2: "Pass criteria: 100% match across all four attributes per tote" and "Fail mode: any mismatch on tag / fraction / gross / PP". Its 3.5 entry: "This is the per-attribute verification underlying 3.2". `SKILL.md` line 178: "every tote in Ops Notes appears in Shipment Tracker with matching tag #, fraction, gross mass, PP. Any mismatch = FAIL."
- Tote 301154 fails on period: QOWV!G24 "MFO Lot 301154 (LOT00301154), June 2026" against inventory row 601 col B "May 2026 PP". 3.2 meets its written Fail mode.
- The QA agent re-scoped 3.2 to roster membership: "the 37 tags the production inventory master places on the four shipping orders are exactly the 37 tags in the QOWV ledger, with no extra or missing tote". The inventory cannot show that. The four orders carry 114 totes in the inventory (col N 2025-12-01: 40; col N 2025-12-02: 36; col L "COLA-31": 20; col L "COLA_32": 18), and the "Injection Batch Number" column (V, header V2) is blank on all 37 rows. Nothing in the inventory says which of the 114 were injected in W3.
- The QA agent's own Drive search lists a "Bio-oil Injection Tracker" among sheets holding these tags (`drive_fulltext_search_results.txt`: "Other sheets returned: … Bio-oil Injection Tracker …"). It was not opened. No other injection record appears in the log.

**Recommendation:** **Fail.** Same root cause as 3.5 and 7.2; one correction set clears all three, and each row should say so. Suggested D23 content (my wording, not a source quote): per-attribute result against the production inventory Q4 2025-2026 tab — tag 37/37, fraction QOWV 37/37, gross 37/37, production period 36/37, with tote 301154 (G24 June 2026 vs inventory B601 May 2026 PP) cross-referenced to 3.5. Drop "no extra or missing tote" unless the Bio-oil Injection Tracker is opened and lists these 37 tags, and only these, against INJ-09-2026-W3.

### 2. Item 8.1 — BCU against transport process
**Current status:** Fail

**Arithmetic (mine):** 37.682 t × 1,201 mi × 1.609344 km/mi × 0.086 kg CO₂e/(t·km) = 6,263.604 kg. On the EF sheet (2026!F7 = 0.0001384 MT CO₂e/t-mi): 37.682 × 1,201 × 0.0001384 × 1,000 = 6,263.442 kg. BCU constant 6,264 kg (log `certify.component_by_key.bcu`). Over by 0.396 kg (Certify basis) or 0.558 kg (sheet basis). The QA agent's figures are right.

**Does the Fail follow from the rule as written?** Yes. `project_bcu_reduction_cap_policy.md`: "over-coverage is always a FAIL", quoting Max 2026-08-26: "BCUs should NEVER exceed the process emission they're offsetting." No size tolerance.

**Is the note honest about what it tests?** On the test, yes: "The BCU exceeds the emission it offsets … A reduction offsets an emission that occurred and cannot exceed it, whatever the size." On the question, no. B50 is not the skill's question and the note does not say so. `checklist_structure.md` 8.1 reads "does the BCU total ≥ the transport-process sum?", with Pass criteria "Σ BCU ≥ Σ transport process activity (BCU may exceed; never less)". `SKILL.md` line 495 reads "MUST equal or exceed". Under that wording 6,264 ≥ 6,263.604 passes. `SKILL.md` line 201 reads "total BCUs = sum of transport process emissions", which matches the reworded question. E50 ("BCU cap: reduction must not exceed the emission it offsets") names no source.

**The fix is partly wrong:** "entering 6,263 kg (or the exact figure) clears it". 6,263 kg under-covers by 0.604 kg. That fails the reworded question's own "equal" test and breaks standing rule (b).

**Recommendation:** **Keep Fail.** D50 should state (my wording) that the row applies the BCU cap policy in `project_bcu_reduction_cap_policy.md` (Max quote above), that this policy reverses the ≥ wording in `checklist_structure.md` 8.1 and `SKILL.md` line 495, and that the row would pass under that written wording. Fix to state: enter the constant as the exact process emission, 6,263.604 kg on the current 0.086 factor, or 6,263.442 kg if the factor moves to the sheet's F7. Delete the 6,263 kg option. Put the policy source in E50.

### 3. Item 7.2 — CI applied to the totes
**Current status:** Fail

**Confirmed:** QOWV!H24 "=$L$18" → 0.1236896674 (K18 = 2026-06-01). Inventory B601 "May 2026 PP" calls for L17 = 0.1106615762 (K17 = 2026-05-01). 930.4 kg × (0.1236896673712938 − 0.1106615762401743) = 12.1213 kg CO₂e. Corrected production emissions 4,965.7294 kg, weighted CI 0.1396798206, net +0.0121 t. All 36 other H references agree with their inventory period (Appendix A).

**Fail or Flag:** Fail. `SKILL.md` line 362: "Value in Certify doesn't match evidence = FAIL (no rounding tolerance beyond ~0.001 tCO2e)". 0.0121 t is twelve times that line. Line 196 requires "each fraction's CI applied to the correct totes". Neither the skill nor the knowledge base exempts an error that lowers the net. A search of the knowledge base for "conservativ" returns the MIN-mass rule, the rail uncertainty rule, percentile and biochar estimation items, and two general statements (lines 1040, 1060). None grades a net-lowering error as Flag.

**Two Fails or one:** Two is right, three by the skill's wording. 3.5 ("any mismatch on any attribute") and 7.2 ("must each be applied to the correct totes") are separate questions with separate Fail modes, and 3.2 fails as well (challenge 1). Each row should state one error, one correction.

**Issue — fix incomplete:** "Relabelling G24 as May 2026 and pointing H24 at $L$17 clears this and 3.5 together" changes the Ops Notes, not Certify. Certify's CI datapoint holds 0.140021 (log). After the sheet fix H50 becomes 0.1396798, and 7.2 then fails on mismatch. The Certify-attached copy (src_1M38GJXY31S0WZNQ, identical today to the live export) goes out of date.

**Recommendation:** **Keep Fail.** Fix steps (my wording): Ops Notes G24 → May 2026 and H24 → =$L$17; Certify CI datapoint (QOWV Pyrolysis Emissions - Carbon Intensity (Weighted)) → 0.139680, giving pyrolysis 4.966 t; re-attach the corrected Ops Notes. If 2.2 is corrected too (C29 = 62.93): CI 0.1396771, mass 35,545.47 kg, pyrolysis 4.965 t.

### 4. Item 3.4 — COLA-32 denominator
**Current status:** Fail

**Confirmed:**
- Allocation tab C15 = 17.0.
- Inventory: 18 rows with col L "COLA_32", 17 QOWV plus row 742 (tag 301310, "Whole Oil", "August 2026 PP", note "filtered in CO to 1000um into fresh tote").
- INJ-08-2026-W5 allocation row 15: "COLA_32 | 2026-08-20 | 18.0 | 5.0 | 0.2777777778".
- INJ-09-2026-W1 "Whole Oil Shipments & EE Alloca" C12 = 18.0 and E6: "COLA_32 = 1 of 18 totes on the truck (the other 17 are BGN QOWV, not in this batch)".
- 3/17 × 1,201 = 211.9412 mi; 3/18 × 1,201 = 200.1667 mi; difference 11.7745 mi × 0.0001927908256 MT/mi = 2.270 kg. Total 1,716.5273 → 1,704.7528 mi.
- The other shared trucks use one denominator across batches: Truck 1 = 40 (INJ-08-2026-W5 row 16; INJ-09-2026-W2 row 12); Truck 2 = 36 (INJ-08-2026-W3 row 16, W4 row 17, W5 row 12); COLA-31 = 20 (INJ-08-2026-W5 row 20).
- No record on disk supports 17. The physical-count correction on disk (INJ-09-2026-W4 allocation A19) concerns COLA-40/41, not COLA-32.

**Fail for 0.00227 t:** Right, under `SKILL.md` line 362: Certify embodied 0.331 t against 0.329 t supported.

**6.2 Pass:** Right. 6.2 asks whether Certify matches the tracker: Certify 1,716.53 mi vs G17 1,716.527288 mi.

**Issue — fix incomplete:** "Setting C15 to 18 corrects it" fixes the tab, not Certify. Certify's "QOWV Embodied Distance (CO to B6) [Certify input]" stays at 1,716.53 mi, so 6.2 fails once the tab is fixed. Minor: the log cites the INJ-09-2026-W1 sentence at A6. It sits in E6.

**Recommendation:** **Keep Fail.** Fix steps (my wording): C15 → 18; Certify embodied distance → 1,704.75 mi, giving embodied 0.329 t; re-attach the corrected Ops Notes.

### 5. Item 1.3 — Shipment Tracker complete
**Current status:** Pass

**Issue:**
- `checklist_structure.md` 1.3 Pass criteria include "every tote assigned to this batch appears with full metadata". Its Fail modes include "totes missing from tracker". `SKILL.md` line 457 expects "Tote rows: tag #, fraction, gross mass, production period, batch assignment".
- The allocation tab lists no tote of this batch. Its one tote block starts at A58 "--- Shipment 2025-12-10 --- (14 of 35 totes on this truck are W4-relevant)", and E60:E73 read "INJ-05-2026-W4".
- C12:C15 (40, 36, 20, 17) and D12:D15 (9, 10, 15, 3) are typed numbers. Nothing in the workbook ties a tag to a truck.
- The tag-to-truck record on disk is the inventory master (col L Ship Status, col N Date Shipped). It is not among the six Certify sources (log `certify.certify_sources_enumeration`).
- Item 3.4 shows the cost: C15 = 17 is wrong, and nothing a verifier receives could show it.
- The same workbook's Whole Oil allocation tab has a check the QOWV tab lacks: A16 "Check - every batch tote is allocated to a truck", B16 `=IF($D$14=$D$6,"OK","MISMATCH")`.
- The counts-without-totes layout is standing: the QOWV allocation tabs of INJ-08-2026-W1 to W5 and INJ-09-2026-W4 hold zero tote rows.

**Recommendation:** **Flag.** Not Fail: tag, gross and period for every tote sit on QOWV!A11:G47 of the same attached workbook. Truck assignment is the missing field. D15 should state (my wording): the allocation tab carries truck-level counts, with no tote-to-truck assignment for this batch (rows 58–73 belong to INJ-05-2026-W4); the tag-to-truck record is inventory master col L/N, which is not attached in Certify; add a per-tote truck column, or attach the inventory extract to the embodied distance datapoint.

### 6. Item 5.2 — route evidence
**Current status:** Pass

**Issue:** The route figures check out from the image: "via US-287 S and US-287 S … 1,132 miles", "via US-287 S, US-287 S and I-20 E … 1,129 miles", "via I-70 E … 1,201 miles". Certify's 1,201 mi (log) is the longest. But the origin field reads "Your location" (`screenshots/routing_map_left_panel.png`), and the datapoint is titled "Distance from Miniforge CO to Basco". The origin pin on the full map sits just north of Denver, which fits Fort Lupton, but the image never names the start point. Knowledge base 10A defines Flag as a "Process hygiene or documentation issue that does NOT prevent verification", and lists "a minor labeling inconsistency" among its examples.

**Recommendation:** **Flag.** D34 should add (my wording) that the origin shows as Your location, and that the route should be re-captured with the Fort Lupton facility address as origin. Per the log the same image is on INJ-09-2026-W2-QOWV, so one re-capture fixes both.

### 7. Item C.1 — net recompute
**Current status:** Pass

**Arithmetic confirmed:**
- Sequestration: 30,808.5 × 0.08 × 3.667 = 9,037.982 kg.
- Process: 6,263.604 kg.
- Embodied: 1,716.527288 × 0.0001927908256 = 330.931 kg.
- Pyrolysis: 35,550.8 × 0.140021 = 4,977.859 kg.
- BCU: 6,264 kg.
- Discount: one-standard-deviation estimate 39.263 kg.
- Net: 3,690.325 kg = 3.690 t (3.69059 t with the displayed 39 kg).
- `recompute_qowv.py`: 31 lines "OK", exit 0.

**Issues:**
- (a) "independent of Certify's arithmetic … from the live 2026 EF sheet". The net line in `recompute_qowv.py` uses `proc_certify_t`, built from Certify's 0.086 (`glec_km_t = proc["inputs"]["ef_kgco2e_per_km_t"]`), and `pyro_t`, built from Certify's CI (`pyro["inputs"]["ci_tco2e_per_t"]`). It does not use F7 0.0001384 or H50. On F7 the net is 3.69049 t, still 3.690. The result stands; the wording does not.
- (b) "31 of 31 checks OK" includes `bcu_within_1kg_of_proc_both_bases`, which passes the +0.396 kg over-coverage that 8.1 fails.
- (c) The reproduced 3.690 t carries the errors in 2.2, 3.4, 7.2 and 8.1. With production-record inputs (301154 at L17, 120509 tare 62.93, COLA-32 = 18, BCU = process emission) the net is 3.70517 t, 0.01485 t higher.
- (d) "Counterfactuals are zero, as the protocol requires" cites no protocol section.

**Recommendation:** **Keep Pass** as a reproduction of Certify from the Ops Notes as submitted. Rewrite D54:
- state that the process factor and CI are Certify's, and give the sheet-basis net of 3.69049 t;
- state that 3.690 t carries the 2.2, 3.4, 7.2 and 8.1 errors, and that the production-record net is 3.705 t;
- change the BCU check to BCU ≤ process emission, equal at display precision;
- cite the protocol section, or drop "as the protocol requires".

### 8. Sidebar B59 — lab "#" mark
**Current status:** none (sidebar)

**Issue:** "This is inherent to the low carbon content of the aqueous fraction under ASTM D5291 and appears on the QOWV certificate every week." Page 2 of the same PDF (SR26-05599.002, AECN) reads "Carbon ASTM D5291 (Method C) 39.7 % (m/m) -- -- #" and "Hydrogen ASTM D5291 (Method C) 7.0 % (m/m) -- -- #". The same mark appears at 39.7 % carbon, so the evidence does not show low carbon as the cause. No prior-week certificate is in the folder or the log, so "every week" has no source.

**Recommendation:** Rewrite B59 (my wording) to state that SR26-05599.001 marks Carbon 8.0 % with the lab footnote "Result is outside of test method limits and/or analytical range used in method precision study" (COA page 1), and that the AECN result on page 2 (39.7 % C, 7.0 % H) carries the same mark. Drop the cause and "every week", or cite prior certificates.

---

## Confirmed Items

- **1.1 Pass** — COA page 1: "Certificate of Analysis: SR26-05599.001", "CLIENT ID : 9-2026-w3-QOWV", "Carbon … 8.0 % (m/m)", Hydrogen 9.1, Nitrogen <0.75, Density 1.047 g/cm³, sampled 17-Sep-2026 10:00. PDF sha256 5cefa571…a31486 matches the log. The Certify copy screenshot shows the same 8.0 %.
- **1.2 Pass** — QOWV!A11:A47 hold 37 rows, B–J filled. B50 37682, D50 35550.8, F50 30808.5, H50 0.1400207787, I50 4977.850701, J50 41.95726. Zero cell comments and no hidden rows on all 10 tabs.
- **2.1 Pass** — Sum of B11:B47 = 37,682.0 = B50 `=SUM(B10:B48)`. Gross equals inventory col I on 37/37 (Appendix A).
- **2.2 Flag** — D = B − C on all 37 rows; D50 = 35,550.8. C29 = 57.6 vs inventory J45 = 62.93 (K45 = 956.07). Effect 5.33 kg × 0.1575553395 = 0.8398 kg CO₂e, below the ~0.001 t Fail line (`SKILL.md` line 362). Label tare is graded "FLAG" (line 374). Prior-week claims hold: INJ-07-2026-W1 used 57.6 on 15 such totes, INJ-08-2026-W4 used 57.6 on 120534, INJ-08-2026-W5 used 62.9 on 19. Flag is the right grade.
- **2.3 Pass** — F = `IF(E="","",B-E)`. Sum = 30,808.5 = F50. E runs from 145.0 (E24) to 322.0 (E32). No Standard Loss anywhere on the tab. Summary!E12 = 0.0, F12 = 0.0.
- **2.4 Pass** — J = `2.5*$L$4` with L4 = 0.453592 → 1.13398. 37 × 1.13398 = 41.95726 = J50.
- **3.1 Pass** — Truck split from inventory col L/N: 9 dated 2025-12-01, 10 dated 2025-12-02, 15 "COLA-31", 3 "COLA_32", matching D12:D15. The 19 December totes also appear on the inventory's "Shipment Tracker (Nov 2025+)" tab under "Truck 1" (rows 19–52) and "Truck 2" (rows 65–93); that tab's C6 = 40 and C7 = 36 match C12:C13. None of the 37 tags appears in any cell of the 9 prior-week workbooks.
- **3.3 Pass** — E12:E15 `=D12/C12` … `=D15/C15`; G12:G15 `=E12*F12` … `=E15*F15`; G17 `=SUM(G12:G15)`; F12:F15 `=$B$8`; D6 `=COUNTA(QOWV!A11:A48)` → 37.
- **3.5 Fail** — Tag 37/37, fraction "QOWV" 37/37, gross 37/37, MFO lot 37/37, period 36/37. G24 reads "June 2026"; inventory row 601 reads B "May 2026 PP", C "5/1-5/31", S "Pink2605". All 50 May-period rows carry "Pink2605"; all 58 June rows carry "Blue2606". May QOWV net sum 36,523.2 kg including 301154 against May summary "36,523"; June 46,616.2 kg against "46,616". Fail per "any mismatch on any attribute".
- **4.1 Pass** — Certify 8 % (log) = COA 8.0 % = Summary!E20 0.08.
- **4.2 Pass** — Log attachment map: Carbon Content → Ops Notes + COA. The attached Ops Notes copy matches the live export on all 10 tabs, values and formulas, 0 differences (my cell-by-cell comparison).
- **4.3 Pass** — Certify ±41.95726 kg (log) = J50.
- **4.4 Pass** — 0.004 × 8.0 = 0.032 = Certify (log). Summary!G20 `=E20*H20` → 0.00032.
- **5.1 Pass** — Certify 0.086 kg CO₂e/(t·km) (log). 2026!F7 = 0.0001384 MT CO₂e/t-mi, G7 "GLEC V3.2 2025". 0.086 × 1.609344 / 1,000 = 0.000138404. Process 6,263.604 kg vs 6,263.442 kg: 0.00016 t apart, inside the ~0.001 t line. Same factor, Pass defensible.
- **5.3 Pass** — Certify 37,682 kg (log) = B50.
- **5.4 Pass** — Log attachment map: "QOWV Transport Mass (CO to B6) [Certify input]" → "INJ-09-2026-W3 Ops Notes.xlsx".
- **5.5 Pass** — Certify ±41.96 kg (display) = 41.95726.
- **6.1 Flag** — Certify 0.19279 kg CO₂e/mi = 2026!F12 0.0001927908256 MT/mi. That is the non-tanker row, built in "Truck and Trailer EE 2026"!B21 as `=B12*(1+B20)` with B20 = 0.167. The tanker row F11 = 0.0002375605888 would give 407.78 kg. 1,716.527288 × 0.0001927908256 = 330.931 kg = 0.331 t. The datapoint is labelled "Tanker Truck", a labelling fault → Flag.
- **6.2 Pass** — Certify 1,716.53 mi vs G17 1,716.527288 mi, within ±0.1 mi.
- **6.3 Pass** — Log: Ops Notes and routing map both linked to the embodied distance datapoint. No Charm Contents in `batch_folder_listing.txt`. Standing rule (c) applies.
- **7.1 Pass** — Group sums: PP#8 14 totes / 2,087.8603 kg; Sep 2025 5 / 635.3404; Apr 2026 16 / 2,033.6217; May 2026 1 / 105.9474; June-labelled 1 / 115.0809. Total 4,977.8507 = I50. 35,550.8 × 0.140021 = 4,977.8586 kg → 4.978 t. No H cell points at L19 or L7.
- **7.3 Pass** — M10, M16, M17, M18 and M21 are HYPERLINKs whose file IDs match the log's summary IDs. The summary files' Aqueous "Kg Emissions/Kg Material" values (0.1576, 0.1314, 0.1107, 0.1237, 0.1287) agree with L10, L16, L17, L18 and L21 to 4 decimals (Appendix B). INJ-09-2026-W2 QOWV!K21:M23 are empty.
- **7.4 Pass** — Certify 35,550.8 kg (log) = D50.
- **7.5 Pass** — Certify ±41.96 kg (display). 4.978 / 3.690 = 134.9 %; the snapshot shows "134.91%".
- **7.6 Pass** — Standing rule (c) applies; Ops Notes linked to "QOWV Pyrolysis Mass [Certify input]" (log). Trim "or any 2026 weekly QOWV batch": the log's `charm_contents` check covers this batch's folder and Certify sources.
- **9.1 N/A** — My text search of every text cell on all 10 tabs found no LCS, calcium, caustic, NaOH, buffer, lime or sulfate. The "pH" hits are "pH range (target)" labels and "pH" headers. Summary!E12/F12 = 0.0. The snapshot lists 5 components, none for LCS.

---

## Observations

1. **Week window.** QOWV!A3 "Week Start (Sat)", B3 = 2026-09-11, is a Friday; B4 = 2026-09-18 is a Friday too. INJ-09-2026-W2 QOWV!B4 = 2026-09-12, so the W2 and W3 windows share 11–12 Sep. The Certify window is 12–18 Sep (log). No tag appears in both weeks, but no per-tote injection date exists to show nothing was injected on 11 Sep, outside the Certify window.
2. **Summary masses match the inventory for May and June, not for April, PP#8 or September.** April summary "43,912" vs inventory April QOWV net 45,764.8 kg (47 totes); PP#8 "77,076" vs 76,217.12 kg (80); Sep 2025 "41,010" vs PP#10 44,931.0 kg (46). The 3.5 check holds for May and June but cannot serve as a general test. The April, PP#8 and September gaps sit outside this checklist.
3. **Look-alike tote.** Inventory row 610: tag 301159, "June 2026 PP", gross 988.0, tare 57.6, net 930.4, "COLA_36", shipped 2026-09-03. Its masses equal 301154's, a plausible source of the mislabel. The label format "MFO Lot 301154 (LOT00301154), June 2026" suggests it was copied from the MFO lot record, which is not on disk. Nothing on disk supports June.
4. **More support for 2.2.** Column C is 57.6 on all 37 rows, a nominal figure; `SKILL.md` line 206 asks to "verify gross/tare were measured (not nominal)". Two more records give 62.93 kg for 120509: the inventory's "Shipment Tracker (Nov 2025+)" tab row 19 (Truck 1, tare 62.93). And the same W3 workbook's Whole Oil ledger copies inventory tares: C11 = 62.9 for 301352 (inventory row 747 J = 62.9), C14 = 62.9 for 301307 (row 746). Add both to D18.
5. **2.3 method.** Column B equals inventory gross (col I) on 37/37: it is the Fort Lupton production weighing. There is no Basco pre-unload weighing. `checklist_structure.md` 2.3 names "Measured Pre-Unload − Measured Post-Unload". Standing rule (f) accepts the method in use, but D19 should say B is the production gross, so a reader does not take it for a pre-unload weighing. 19 totes waited about 9.5 months between shipping and injection (Sidebar B60).
6. **The skill still holds the reversed BCU rule.** `checklist_structure.md` 8.1 ("≥"), `SKILL.md` line 495 ("MUST equal or exceed") and knowledge base lines 323 and 590 conflict with `SKILL.md` line 201 ("=") and the BCU cap policy. The policy file says the Charm skill was "not yet checked". Until the text is corrected, each new batch's 8.1 starts from the reversed wording.
7. **Shared-truck totals across the batches on disk.** Truck 2: INJ-08-2026-W3 1 + W4 2 + W5 23 + this batch 10 = 36 of 36. Truck 1: INJ-08-2026-W5 3 + INJ-09-2026-W2 18 + 9 = 30 of 40. COLA-31: 2 + 15 = 17 of 20. COLA_32: 5 + INJ-09-2026-W1 Whole Oil 1 + 3 = 9 of 18. No truck is over-allocated by tote count.
8. **No pH recorded.** QOWV!L6 "2.0 - 4.0" is a target. AECN Rail G28 and G46, under the "pH" headers G27 and G45, are blank. The 9.1 N/A rests on the absence of any LCS entry, which the item wording accepts.
9. **COA location field.** "LOCATION : FORT LUPTON, CO" appears on both the QOWV and the AECN certificate, so it records Charm's entry, not where the sample was drawn. A verifier may ask.
10. **Lab precision.** The lab marks the 8.0 % result as outside its precision study. The 0.4 % in 4.4 is Charm's standard (knowledge base 7a: "Carbon Content: 0.004 × Measured Value (0.4%)"), not a lab-stated precision for this result.
11. **BCU reuse not checked.** No file on disk ties this removal's 6.264 t to a drawdown of the 2,795 TERCs on certificate "TERC1012_2024_DF_RENEWABLE_DIESEL-13-47206-50000". No checklist item tests reuse of one certificate across removals.
12. **Claims I could not check from disk.** 5.2's "byte-identical to the map attached on INJ-09-2026-W2-QOWV"; 6.1's "titled '... - Flatbed Truck' on INJ-09-2026-W2-QOWV"; Sidebar B61's reading of the VVB guidance (document not on disk).

---

## Appendix A — per-tote check, Ops Notes QOWV tab vs inventory "Q4 2025 -2026 Production Invent"

| Ops row | Tag (A) | Gross B | Tare C | Period label (G) | H ref | Inv row | Inv period (B) | Inv gross (I) | Inv tare (J) | Paint (S) | Ship status (L) | Shipped (N) | Match |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 11 | 301009 | 1013 | 57.6 | April 2026 | =$L$16 | 515 | April 2026 PP | 1013 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 12 | 301082 | 1066 | 57.6 | April 2026 | =$L$16 | 517 | April 2026 PP | 1066 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 13 | 301103 | 1014 | 57.6 | April 2026 | =$L$16 | 551 | April 2026 PP | 1014 | 57.6 | Red2604 | COLA_32 | 2026-08-20 | OK |
| 14 | 301112 | 1005 | 57.6 | April 2026 | =$L$16 | 548 | April 2026 PP | 1005 | 57.6 | Red2604 | COLA_32 | 2026-08-20 | OK |
| 15 | 301114 | 1027 | 57.6 | April 2026 | =$L$16 | 535 | April 2026 PP | 1027 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 16 | 301115 | 1032 | 57.6 | April 2026 | =$L$16 | 539 | April 2026 PP | 1032 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 17 | 301121 | 1027 | 57.6 | April 2026 | =$L$16 | 521 | April 2026 PP | 1027 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 18 | 301122 | 996 | 57.6 | April 2026 | =$L$16 | 523 | April 2026 PP | 996 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 19 | 301123 | 1009 | 57.6 | April 2026 | =$L$16 | 528 | April 2026 PP | 1009 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 20 | 301126 | 1043 | 57.6 | April 2026 | =$L$16 | 534 | April 2026 PP | 1043 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 21 | 301139 | 1005 | 57.6 | April 2026 | =$L$16 | 529 | April 2026 PP | 1005 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 22 | 301145 | 1064 | 57.6 | April 2026 | =$L$16 | 536 | April 2026 PP | 1064 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 23 | 301150 | 1035 | 57.6 | April 2026 | =$L$16 | 524 | April 2026 PP | 1035 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 24 | 301154 | 988 | 57.6 | June 2026 | =$L$18 | 601 | May 2026 PP | 988 | 57.6 | Pink2605 | COLA-31 | 2026-08-18 | **MISMATCH: period** |
| 25 | 301169 | 1015 | 57.6 | May 2026 | =$L$17 | 596 | May 2026 PP | 1015 | 57.6 | Pink2605 | COLA_32 | 2026-08-20 | OK |
| 26 | 301176 | 996 | 57.6 | April 2026 | =$L$16 | 530 | April 2026 PP | 996 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 27 | 301179 | 1029 | 57.6 | April 2026 | =$L$16 | 531 | April 2026 PP | 1029 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 28 | 301198 | 1035 | 57.6 | April 2026 | =$L$16 | 532 | April 2026 PP | 1035 | 57.6 | Red2604 | COLA-31 | 2026-08-18 | OK |
| 29 | 120509 | 1019 | 57.6 | July 2025 | =$L$10 | 45 | 2025 PP#8 | 1019 | 62.93 | Purple257 | Shipped | 2025-12-01 | **MISMATCH: tare** |
| 30 | 015178 | 1049 | 57.6 | July 2025 | =$L$10 | 86 | 2025 PP#8 | 1049 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 31 | 015152 | 993 | 57.6 | July 2025 | =$L$10 | 87 | 2025 PP#8 | 993 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 32 | 120507 | 1015 | 57.6 | July 2025 | =$L$10 | 88 | 2025 PP#8 | 1015 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 33 | 015181 | 960 | 57.6 | July 2025 | =$L$10 | 89 | 2025 PP#8 | 960 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 34 | 015185 | 1055 | 57.6 | July 2025 | =$L$10 | 96 | 2025 PP#8 | 1055 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 35 | 015176 | 907 | 57.6 | July 2025 | =$L$10 | 97 | 2025 PP#8 | 907 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 36 | 015151 | 943 | 57.6 | July 2025 | =$L$10 | 109 | 2025 PP#8 | 943 | 57.6 | Purple257 | Shipped | 2025-12-01 | OK |
| 37 | 015175 | 1006 | 57.6 | July 2025 | =$L$10 | 110 | 2025 PP#8 | 1006 | 57.6 | Purple257 | Shipped | 2025-12-01 | OK |
| 38 | 015164 | 975 | 57.6 | July 2025 | =$L$10 | 113 | 2025 PP#8 | 975 | 57.6 | Purple257 | Shipped | 2025-12-01 | OK |
| 39 | 015166 | 1053 | 57.6 | July 2025 | =$L$10 | 115 | 2025 PP#8 | 1053 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 40 | 015191 | 1067 | 57.6 | July 2025 | =$L$10 | 117 | 2025 PP#8 | 1067 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 41 | 015174 | 1044 | 57.6 | July 2025 | =$L$10 | 118 | 2025 PP#8 | 1044 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 42 | 015200 | 972 | 57.6 | July 2025 | =$L$10 | 119 | 2025 PP#8 | 972 | 57.6 | Purple257 | Shipped | 2025-12-02 | OK |
| 43 | 245161 | 1050 | 57.6 | September 2025 | =$L$21 | 193 | 2025 PP#10 | 1050 | 57.6 | Pink259 | Shipped | 2025-12-01 | OK |
| 44 | 245189 | 1022 | 57.6 | September 2025 | =$L$21 | 197 | 2025 PP#10 | 1022 | 57.6 | Pink259 | Shipped | 2025-12-01 | OK |
| 45 | 245195 | 1084 | 57.6 | September 2025 | =$L$21 | 198 | 2025 PP#10 | 1084 | 57.6 | Pink259 | Shipped | 2025-12-01 | OK |
| 46 | 245104 | 1047 | 57.6 | September 2025 | =$L$21 | 200 | 2025 PP#10 | 1047 | 57.6 | Pink259 | Shipped | 2025-12-01 | OK |
| 47 | 245105 | 1022 | 57.6 | September 2025 | =$L$21 | 205 | 2025 PP#10 | 1022 | 57.6 | Pink259 | Shipped | 2025-12-01 | OK |

Every Ops Notes period label agrees with its own H reference. Inventory date ranges: "2025 PP#8" = "7/1-7/31", "2025 PP#10" = "9/1-9/30". All 37 tags appear once each in the inventory.

## Appendix B — period CI constants, Ops Notes QOWV tab vs summary files

| Period | K cell | L value (full) | Summary file | Aqueous mass | Emissions (MT CO₂e) | Kg Emissions/Kg Material | Totes as entered | Totes per inventory |
|---|---|---|---|---|---|---|---|---|
| PP#8 (Jul 2025) | K10 "PP#8" | 0.1575553395 | PP8_head.csv | 77,076 | 12.144 | 0.1576 | 14 | 14 |
| Sep 2025 (PP#10) | K21 `=DATE(2025,9,1)` | 0.1286895670 | Sep2025_head.csv | 41,010 | 5.278 | 0.1287 | 5 | 5 |
| Apr 2026 | K16 2026-04-01 | 0.1314184532 | Apr2026_head.csv | 43,912 | 5.771 | 0.1314 | 16 | 16 |
| May 2026 | K17 2026-05-01 | 0.1106615762 | May2026_head.csv | 36,523 | 4.042 | 0.1107 | 1 | **2** |
| Jun 2026 | K18 2026-06-01 | 0.1236896674 | Jun2026_head.csv | 46,616 | 5.766 | 0.1237 | 1 | **0** |
