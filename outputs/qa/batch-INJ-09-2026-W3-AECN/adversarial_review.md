# Gate 3 Adversarial Review — INJ-09-2026-W3-AECN

**Removal:** rmv_1M3MMSA7X1S0R377 (Certify period 2026-09-12 to 2026-09-18) · **Oil:** AECN, rail · **Site:** Basco 6
**Reviewed:** 2026-09-29 · **Checklist:** `Batch_INJ-09-2026-W3-AECN_QA_Checklist.xlsx`

**Row count:** the checklist carries **62** status rows (37 Pass, 11 Flag, 9 Fail, 5 N/A), not 57.
**Result:** 9 rows challenged, 53 confirmed.
- Two status changes are recommended: 3.3 and 8.3, both Flag to Fail.
- 2.5 stays Fail once its correction location is settled.
- Six rows keep their status but carry a wrong or missing statement.

**Derived figures:** every number I computed is printed, with its formula, in `adversarial_review_recompute_output.txt`. The script that produces it is `adversarial_review_recompute.py`. Below, "[R#]" points to the line in that output.

## What I opened myself

- All 20 W3 scale tickets, read from the page images. I also read the four W2 ticket photos for SHPX215046 offloads 3-4 and the W2 empty ticket 1312226246373.
- All 9 BOLs: pages 1-3 of each, plus page 5 of 2456-R, 2457-R, 2458-R, 2462-R, 2463-R, 2464-R, 2468-R, 2469-R and 2470-R.
- The SGS certificate SR26-05599, both pages.
- The formation fluid report, page 5.
- The TERC certificate, the railcar embodied sheet, the AECN embodied calc sheet, the Watco email image, both route maps, and GLEC pages 6 and 96.
- The transport protocol v1.1, pages 8-12.
- The September and August guidance texts.
- The Ops Notes (the Drive copy and the Certify copy), read twice: once with formulas and cell comments, once as values.
- The W2 live Ops Notes, the COBB export, the Standard EF 2026 tab, the LCA files, the filtration dataset, the carbon statistics and the EAC tracker.
- The saved Certify component windows and calculation view.
- A fresh read-only pull of **W2's** Certify removal (rmv_1M2RKR58N1S0F02M) through the Isometric connector, saved as `adversarial_review_W2_certify_graphql_2026-09-29.json`.
- File fingerprints: 20 of 20 tickets, 9 of 9 BOLs and the certificate are identical between the Drive and Certify copies.

**Step 0 (primary source check):** passed.
- Scale tickets: rows 2.1-2.3 carry tractor, trailer, weight and date for each ticket, and all of them match the images.
- COBB: rows 5.4 and 5.6 name the tab, rows 1776-1785 and the column A value "INJ-09-2026-W3_bio_oil".
- Uncertainty: rows 7a.1 and 7a.2 carry the ± values from each component window (±725.7 kg, ±0.15883 %).

## Verdicts on the requested judgment calls

| Row | Current | Verdict |
|---|---|---|
| 2.3 | Fail | **Right status.** The note's claim about which way the error runs is wrong: Charm's published KL720 standard empty would lower the credited net. |
| 2.5 | Fail | **Right in substance, wrong location.** The over-draw arithmetic holds, and W2's Certify still carries the raw figure today. But the note pins the correction on W2 offload 4 while failing W3, and W2 already fails the same kilograms. |
| 2.7 / 7.1 / 9.1 / 9.8 | Fail ×4 | **Right.** The R&D reading of K46 matches the workbook's own labels and formula. Four literal check failures, one cause, one fix. |
| 3.3 | Flag | **Should be Fail.** SHPX215046 fails the check literally, and the published W3 method conflicts with the Ops Notes and Certify. |
| 3.5 | Fail | **Right.** |
| 8.1 | Flag | **Right status.** The note misses a third axle-split anomaly on an empty ticket. |
| 9.6 | Fail | **Right status.** The suggested fix (14,634 kg) rounds down, which the BCU cap policy rules out. |
| Passes in 2, 7a, 9 | Pass | **All hold.** 7.3 and 7a.3 pass on evidence the QA never produced. I reproduced the discount exactly. |

---

## 1. Challenged Items

### 2.3 — Tractor and trailer match (Fail)
- **Issue:** The mismatch is real. Full ticket 1124426254565 reads "9-11-26", "12:40", "TRACTOR # CH1", "TRAILER # KL720", "GROSS WEIGHT 72640 LB". Empty ticket 1312226255533 reads "9-12-26", "09:14", "TRACTOR # CH2", "TRAILER # KL720", "GROSS WEIGHT 29640 LB". The September guidance has no substitution section, and neither Ops Notes copy has a cell comment. Fail is correct.
  - The note then says the three CH1+KL720 empties on file (29,360, 29,460 and 29,480 lb) point to the credited net being understated.
  - That comparison ignores Charm's own published conservative method. The August guidance defines the "Trailer Standard Empty Weight" method for exactly this trigger: "(b) the empty ticket's tractor and/or trailer do not match the Full ticket". It publishes "KL720 8 29,515 130 29,645", where 29,645 lb is the mean plus one standard deviation.
  - With the published 29,645 lb empty, the net is **19,502.18804 kg** [R1]. That is **2.26796 kg below** the credited 19,504.456 kg [R2], about 0.0033 tCO2e of gross [R3].
  - So under the method Charm has already had verified, the credited figure is slightly **high**, not low. The three-ticket comparison is an ad hoc range. The skill warns against using such ranges as evidence.
- **Recommendation:** Keep **Fail**.
  - Replace the direction sentence with the published-method comparison above.
  - Fix route: apply the KL720 standard (29,645 lb) with a cell note and add the method and this application to the September guidance, or find the CH1+KL720 empty for that trip.
  - Either change moves Ops F35, F46 and Certify's two mass datapoints by about 2.27 kg [R2r] (touches 2.4, 2.7 and 7.1).

### 2.5 — Conservative injectate mass / railcar over-draw (Fail)
- **What holds:**
  - W3 offloads 1-2 are 21,055.74064 and 20,992.23776 kg (from tickets 1124426249539/1312226249422 and 1312226249425/1124426250543).
  - W2 offloads 3-4 are 20,810.80096 and 14,841.53024 kg. The photos read "74320 LB"/"28440 LB" and "61980 LB"/"29260 LB".
  - The four total 77,700.3096 kg [R4] against BOLs 2462-R/2463-R/2464-R, whose weigh-ticket nets read "25 940", "25 900" and "25 840" kg (Ops E11 77,680). That is **20.3096 kg over** [R5].
  - The W2 offload 4 full ticket reads "9-07-26" "10:55" and the empty reads "9-08-26" "07:07". Offload 4 is last by number and by time.
  - The note dates its W2 Certify reading to 2026-09-22. My read-only pull today shows W2's "Bio-Oil Mass - AECN via Rail" at **155.86328 t** and "Mass of Injectant" at **211.2522262 t**. Those equal W2's raw sums (W2 log `rail_scale_net_sum_kg` 155863.28304), so the raw 14,841.53024 kg is still booked today.
- **Issue 1 — the note contradicts itself on where the correction goes.**
  - It names W2 offload 4 as the policy location ("its policy value is 14,821.22064 kg") and then fails W3 because "nothing in W3 absorbs the difference."
  - If offload 4 in W2 is the correct location, W3's reported values are right and the defect sits in W2's removal.
  - W2's checklist (row 2.5, Fail) already charges the same 20.3096 kg and says: "The deduction has to be applied in Certify, here or in W3, and the two weeks must agree on where." Two Fails on two removals for one error risk a double correction of 40.6192 kg [R6].
- **Issue 2 — Charm's recorded railcar policy note points the other way.**
  - The note from the 2-204 correction (`feedback_railcar_last_offload_signal.md`) reads: "FC11 reconciliation lands on the RP's *last-reported* batch from a given railcar — not necessarily the railcar's *physical-last* batch."
  - Both weeks sit in the open September period, and W3 is the last-reported batch for SHPX215046. Under that note the correction lands on **W3 offload 2**, which becomes **20,971.92816 kg** [R7], a gross effect of 0.029128 tCO2e at 39.7 % [R8].
  - FC11's text ("On the last offload of the railcar") and COBB row 1731 (14,821.22064) point to W2 offload 4 instead.
  - The same policy note says an offload table outside the normal 1→2→3→4 order is to be raised for a decision before a finding is written. The checklist picks one reading without saying the other exists.
- **Issue 3 — a missing caveat.** The over-draw arithmetic rests on W2's two SHPX215046 tickets. W2's live Ops Notes (exported today, cell M12) says: "LD3 only candidate CAT ticket (1124426250545, 74,320 lb, 9-07-26) is confirmed mislabeled (printed SHPX215046OFFLOAD3, actually belongs to another car per Garrett) ... LD4 has no resolvable ticket after a wide Gmail harvest." The note treats both W2 figures as settled and does not mention this.
- **Recommendation:** Settle one location and state it identically in both checklists.
  - **Option A (recorded last-reported rule):** keep **Fail** on W3. Correct W3 offload 2 to 20,971.92816 kg [R7]. Close W2's 2.5 with no W2 change.
  - **Option B (FC11 text and COBB):** correct W2 offload 4 to 14,821.22064 kg. W3's 2.5 becomes **Flag**, pointing to W2.
  - Either way, add the W2 M12 caveat to the note.

### 3.3 — BOL mass matches or exceeds reported injectate mass (Flag → recommend Fail)
- **Issue 1 — the check fails literally.** The rail rule reads: "Item 3.3 (BOL mass ≥ injectate): apply at the railcar level — sum of 3 BOL masses ≥ railcar received mass". SHPX215046 received 77,700.3096 kg [R4] against 77,680 kg of BOLs. The note itself says SHPX215046 "does not" pass. A check that fails for one of three railcars cannot rest at Flag.
- **Issue 2 — the published method and the reported figures disagree.**
  - The September guidance, which the verifier is given, states: "the mass loaded at origin is derived from the volume recorded on the Bill of Lading and a bio-oil density of 1.22 kg/L". It also states: "the ops notes present both together so the balance for each railcar can be inspected directly."
  - The Ops Notes E10:E12 and Certify's AECN-SOPOR allocated distance use weigh-ticket masses instead.
  - On the guidance basis, GPRX5102 loads 79,298.78 kg [R9] and TILX200231 loads 79,030.38 kg [R10]. They would then show railcar losses of **1,480.54 kg** [R11] and **1,575.01 kg** [R12], where the Ops Notes shows 121.75648 and 64.63008 kg.
  - The allocated AECN-SOPOR distance would fall from 818.80 mi [R13] to 807.12 mi [R14].
  - A verifier following the published method cannot reproduce the Certify figure. The Ops basis is the conservative one: 0.0028 tCO2e more emission [R15].
  - Separately, GPRX5102's 77,940 kg (Ops E10) matches neither published basis. The BOL metric-tons figures "25.99", "25.99" and "25.97" come to 77.95 t [R19], and the volume basis gives 79,298.78 kg [R9].
- **Issue 3 — one statement is not supported by the guidance.** The note says "on the guidance basis the SHPX215046 over-draw would not show." The guidance's multi-week clause reads: "the loaded mass is recorded once, in the week the railcar's first offload occurs".
  - SHPX215046's first offload was weighed "9-06-26", inside W2's Ops week (W2 Ops Notes B3 2026-09-05 to B4 2026-09-12), and W2 booked it first.
  - So SHPX215046 takes W2's basis, "the metric-tons figure stated on the Bill of Lading": "25.94", "25.90" and "25.84" come to 77.68 t [R20]. On that basis the over-draw still shows.
- **Issue 4 — incomplete.** The note says "Loaded mass enters Certify only through the AECN-SOPOR allocation fractions". It also enters the SHPX215046 rail allocated distances, M32 596.0552738 and M33 594.257606, which are each offload's mass divided by 77,680 and multiplied by 2,199.
- **Recommendation:** Upgrade to **Fail**. Delete the SHPX215046 sentence and add the loss figures above. The fix is to make the guidance and the Ops Notes agree (rebase the Ops loaded masses, or correct the guidance text) before submission.

### 8.3 — Inventory reconciliation / carryover documented (Flag → recommend Fail)
- **Issue:** The finding is correct and verified.
  - W3 H11 "Previously Claimed (kg)" = 0.0 against W2's 35,652.3312 kg (W2 Ops F12).
  - F11 = 42,047.9784, G11 is blank and P11 = "PARTIAL".
  - The guidance says "subsequent weeks draw against the same shipment."
  - The formula chain shows what this hides. F11 is "=SUMIF($C$28:$C$43,A11,$F$28:$F$43)+H11", and G11 fills only when F11 is at least 95 % of E11. With H11 = 35,652.3312, F11 becomes 77,700.3096 [R4] and G11 shows 20.3096 kg over [R5].
  - The attached Ops Notes therefore misstates the railcar balance and hides a mass-balance breach that changes Net CDR. That meets the Fail test ("prevent them from confirming the reported value"). The words in M11 ("W2 consumed offload_3/offload_4") do not repair the numbers.
- **Recommendation:** Upgrade to **Fail**. Fix: H11 = 35,652.3312 kg (or the W2 figure after the 2.5 decision).

### 9.6 — BCU does not exceed transport process emissions (Fail)
- **Issue:** The Fail is right.
  - The three booked process components are 2.424477007, 11.242612671 and 0.967560497 t. They sum to 14.634650 t [R21], against the BCU constant "14,635 kgCO₂e": 0.35 kg over [R22].
  - The knowledge base rule reads: "Over-coverage of any size is a FAIL".
  - The note's fix ("An input of 14,634 kgCO2e complies") rounds down. Charm's recorded BCU cap policy note (`project_bcu_reduction_cap_policy.md`) reads: "fix = enter the exact process figure, never round down either."
  - The protocol text is quoted correctly. Page 11 reads: "at maximum, an amount of BCUs may be used for each journey, j, such that: (F_j − F_BCU,j ED_BCU,j/ED_Fuel,Transportation,j) ≥ 0".
- **Recommendation:** Keep **Fail**. Change the fix to **14,634.650 kgCO₂e** [R23].

### 7.3, 7a.3 and 9.8 — Uncertainty discount (Pass, Pass, Fail)
- **Issue:** All three notes say the discount "was not re-derived" or "not independently reproduced", and two of them Pass on that basis. It can be reproduced from the component windows.
  - Sequestration: 282.999147 t with relative spread from "±725.7" kg on 194,394.38206 kg and "±0.15883" on 39.7 %, giving 1.548559 t [R24].
  - The five mass-driven activities share one mass datapoint (±725.7 kg on 197,321.59 kg), giving 0.168686 t [R25].
  - Combined: **1.5577199676 t** [R26], which matches Certify's 1.5577199676321056 to 10 digits.
  - With the corrected Mass of Injectant (193,491.9399 kg) the discount becomes **1.553904 t** [R27].
  - 9.8's internal net then becomes **248.327129 t** [R30], not 248.323303 t.
  - 7a.3 also asks for consistency with the GHG statement, which does not exist yet (7.4). That part is deferred, the same as 7.4.
- **Recommendation:** 7.3 **Pass**, 7a.3 **Pass** (GHG-statement part deferred to period close) and 9.8 **Fail**, each with the reproduction above in place of the "not re-derived" wording.

### 8.1 — No unexplained outliers (Flag)
- **Issue:** The two zero steer-axle full tickets are verified. Ticket 1124426253554 reads "STEER AXLE 00 LB", "DRIVE AXLE 25680 LB", "TRAILER AXLE 45580 LB" and "GROSS WEIGHT 71260 LB". Ticket 1124426254565 reads 00 / 22160 / 50480 / 72640. Flag is the right status. Each ticket states: "The GROSS WEIGHT is the CERTIFIED WEIGHT and was weighed on a full length platform scale", so the net stands.
- The note checks full tickets and stops there. The **empty** ticket 1312226254521 (TILX200231 offload 1) reads "STEER AXLE 3880 LB", "DRIVE AXLE 16900 LB". The other nine empties read between 9,420 lb (1312226253493) and 10,640 lb (1312226255533) on the steer. That is a third axle-split anomaly, and it is not mentioned.
- **Recommendation:** Keep **Flag**. Add the certification sentence and the empty-ticket anomaly.

---

## 2. Confirmed Items

| Row | Status | What I verified |
|---|---|---|
| 1.1 | Pass | Ops 'AECN Rail'!B2 "INJ-09-2026-W3". The Drive listing shows the Ops Notes, Scale Tickets/, Testing/, an empty Completed QA Checklists/ and Kerry Oil/. Certify started 2026-09-12, completed 2026-09-18. |
| 1.2 | Pass | 20 ticket PDFs in 4 + 2 + 4 offload folders, all opened. 20 of 20 identical to the Certify copies. |
| 1.3 | Pass | Page 2 "Certificate of Analysis: SR26-05599.002", "CLIENT ID : 9-2026-w3-AECN". |
| 1.4 | Flag | G28:G37 empty. M10 and M12 read "Mileage (AECN->SOPOR / Rail / Opel->Basco) intentionally left BLANK" while J/K/L hold 107.5 / 2199 / 42.9. H11 = 0. Zero cell comments in both copies. |
| 1.5 | Pass | "vaulted" has 0 hits in the Ops, component and BOL text dump. All 9 BOLs ship to SOPOR Baie-Comeau. |
| 2.1 | Pass | 20 of 20 tickets present and read. All 20 are sources on both "Mass of Injectant (per injection)" and "Bio-Oil Mass - AECN via Rail" (30 sources each). |
| 2.2 | Pass | Earliest weigh "9-06-26 10:44" (1124426249539), latest "9-13-26 08:36" (1312226256537). Injection 2026-09-18, so 12 days at most. |
| 2.4 | Pass | All 10 nets match, e.g. (73,140 − 28,760) × 0.453592 = 20,130.41296. They sum to 197,321.59184 [R41], matching A46 197,321.5918. |
| 2.6 | Pass | D46 2,545.448535. C46 × 0.0129 reproduces it (2,545.448534, [R42]). |
| 2.6a | Pass | E46 381.7612409, reproduced as 381.76124 [R43]. Dataset Summary B12 "Recommended value for filtration loss" 0.001959191176, so 0.00196 rounds up (conservative). |
| 2.7 | Fail | K28:K37 sums to 194,394.38206 [R44], which equals Certify's Mass of Injectant. F46 "=C46-D46-E46-K46" = 193,491.9399. K45 reads "Mass Removed for R&D (kg)" and K46 "=R4*R5*R3" = 902.4421693 [R45]. Summary B17 (AECN MOBI) = 193,491.9399. The R&D reading follows the workbook's own labels. 2.7, 7.1, 9.1 and 9.8 each fail literally from this one cause. One fix: Mass of Injectant = 193,491.9399 kg. |
| 2.8 | N/A | AECN Truck A28 = 0 and B10:B24 are blank. |
| 3.1 | Pass | Weigh-ticket nets (page 3): "25 990", "25 980", "25 970", "25 940", "25 900", "25 840", "25 920", "25 900", "25 700" kg. These equal Ops E17:E25. 9 of 9 identical to Certify. |
| 3.2 | Pass | Each BOL reads "CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau". Three BOLs per railcar, dated 2026-08-03 to 2026-08-11. |
| 3.4 | Pass | Each BOL reads "From /De : BioEnergie AE Côte-Nord Canada, 175 Portage des Mousses, Port-Cartier". Carrier "Transport Baie-Comeau". The map runs 4687 LA-115 to "Acadiana Railway, 1224 Cortez St". |
| 3.5 | Fail | Each allocated-distance datapoint carries "INJ-09-2026-W3 Ops Notes.xlsx" and nothing else. The maps and the email sit on the full-distance datapoints. M10/M12 contradict J/K/L. Certify's 818.69019 mi does not reproduce: I get 818.80 [R13], 818.77 [R16], 818.75 [R17], 818.73 [R18] and 807.12 mi [R14]. The email reads "The total milage for this move was 2199." with no railcar or date. W2's rail allocated datapoint (read today) carries "Aug-01-2026-distance-route_map.png", "Aug-05-2026-distance-route_map.png" and "Aug-08-2026-distance-route_map.png". None of these is among W3's 43 sources, even for the shared SHPX215046. |
| 3.6 | Pass | Six transport components: process and embodied for each of the three legs. |
| 3.7 | Flag | Page 5 seller signature is blank on 2462-R, 2463-R, 2464-R, 2468-R, 2469-R and 2470-R, and signed on 2456-R, 2457-R and 2458-R. 2457-R page 2 is hand-corrected "19 282" to "19 290" and "21 673" to "21 666", with the printed "25 988" / "25.99" unchanged, against weigh ticket PC0039389 "MASSE NETTE : 25 980 KG". 2458-R reads "correction poid vide/empty truck", with a page 1 tare of 19130 against page 2's 19 460. |
| 4.1 | Pass | SR26-05599.002, SGS order 5494492, present in Drive and Certify (identical). |
| 4.2 | Pass | "Carbon ... 39.7 % (m/m) ... #". Mean 39.420350877193, SD 6.09332409018271, n 285, giving a band of 27.23 to 51.61 % (log `carbon_range`). The "#" also appears on the AECN carbon results for W1 (50.4 %) and W2 (40.4 %), so it is routine, not a divergence between weeks. |
| 4.3 | Pass | "Hydrogen ... 7.0 ... #", "Nitrogen ... <0.75". |
| 4.4 | Flag | "LOCATION : FORT LUPTON, CO" on the AECN page. W2 printed the same. |
| 4.5 | N/A | Not an aqueous oil. |
| 4.6 | Pass | "Density at 15°C ... 1.192 g/cm³" against Waypoint 24-200-0020, page 5, Lab No 98021, "Specific Gravity 1.01 g/mL". |
| 5.1 | Pass | B2 "INJ-09-2026-W3", B3 2026-09-11, B4 2026-09-18. Rows 28-37 are dated 2026-09-18. |
| 5.2 | Flag | Labels read "SHPX215046 O4" (1124426253554) and "SHPX215046 3" (1124426255569), plus "TIMX200231 O1", "TILX2000231 O1" and "TILX2000231 O2". These look like labels carried over by the same truck and trailer: CH1/KL192 printed "SHPX215046 4"/"SHPX215046 O4" on W2's 9-07/9-08 tickets, and CH2/KL188 printed "SHPX215046 3" on 9-07. Each pair's empty names the booked railcar ("GPRX5102 O2", "TILX200231 4"). The GPRX5102 and TILX200231 balances close within 121.75648 and 64.63008 kg (Ops G10, G12). Flag holds. |
| 5.3 | N/A | AECN only. |
| 5.4 | Flag | COBB rows 1776-1785, column A "INJ-09-2026-W3_bio_oil". Row 856 has 61,207.70448 consumed against 20,402.56816 offloaded. GPRX5102 origin 77,950 against 77,940. |
| 5.5 | Fail | G28:G37 and G46 are empty. COBB injection_ph is empty on rows 1776-1785. The pH check is required for every batch. |
| 5.6 | Pass | COBB injection_completion_date 2026-09-18 on all 10 rows. Ops rows and Certify end date agree. |
| 5.7 | N/A | AECN density field expected blank (checklist rule). |
| 6.1 | Pass | Summary E19 0.13305202780074143, "no energy allocation to filter cake co-product". Period H3/H4 2026-01-01 to 2026-06-30. |
| 6.2 | Pass | Sheet1 I12 0.1371171258, made up of I10 0.004065098048 and I11 0.133052027800741. |
| 6.3 | Pass | B1 "Inputs for LCA CI calculation for the period 1 Jan to 30 June 2026". I12 10,334,884.34 L. |
| 6.4 | Pass | 2026 tab row 4 "Production Emissions for AECN Oil--H2 2026", F4 0.1371171258. Certify 0.13712 adds 0.000567 t (log `recompute.findings`, conservative). The August guidance reads: "It governs every AECN removal in this period and in subsequent H2 2026 periods." |
| 6.5 | Pass | Row 5 F5 0.02116. The calc sheet reads "Total Embodied Emissions (T CO2e)/MT Bio Oil 0.02115941123". |
| 6.6 | Pass | Both pyrolysis components use Bio-Oil Mass 197,321.59 kg, which equals C46 (before sparging). |
| 7.1 | Fail | Certify's gross reproduces as 282.999147 t [R31], so Certify uses 3.667. The corrected gross is 281.685373 t [R29], an overstatement of 1.313774 t [R32]. |
| 7.2 | Pass | Activities total 46.438990 t [R28], shown as 46.439. |
| 7.4 | Flag | The statements list's latest row reads "01 Aug 2026 to 31 Aug 2026 13 GHG entries", "Certificates issued". There is no September row. Same deferral as W2. |
| 7a.1 | Pass | Component windows: sequestration "±0.15883" % and "±725.7" kg. Both pyrolysis components and the three process legs "±725.7" kg. Embodied components have distance and factor inputs only. |
| 7a.2 | Pass | 10 weighings × 72.57 = 725.7 kg (one weighing per offload, FC9). Carbon 0.15883 against 0.1588 expected: 0.00003 higher [R33], which adds discount (conservative). |
| 8.2 | Pass | G10 121.75648 kg (0.156 %), G12 64.63008 kg (0.083 %) (log `_derived_values.loss_calc`). The guidance discloses no spill. |
| 8.4 | Pass | 4 offloads against 3 BOLs for each railcar (SHPX215046: 2 in W2, 2 in W3). |
| 9.1 | Fail | 282.999147 against 281.685373 internal [R29]. Same cause as 2.7. |
| 9.2 | Pass | Process 2.424477, 11.242613 (11.242775 at the sheet factor, log `recompute.lines`) and 0.967560. Embodied 0.194488, 0.173964 and 0.203826. Rail allocated 5,588.31 mi [R40], built from the full 2,199 mi for each full railcar plus SHPX215046's W3 share of 1,190.31 mi [R39]. 858 = 42.9 × 2 × 10. The railcar sheet reads "65.37", "2100000", "0.0000311307". |
| 9.3 | N/A | No injection-side component. |
| 9.4 | Pass | 197.32159 × 0.13712 = 27.056736. 197.32159 × 0.02116 = 4.175325. |
| 9.5 | Pass | Certificate: "Number of TERCs Retired 2,795", "Each TERC represents one metric ton of carbon dioxide equivalent (“tCO2e”) reduced." Protocol page 9: "the use of Book and Claim Units (BCUs) for low-carbon fuels to substitute for some, or all, of project fuel usage is permitted." |
| 9.7 | Pass | The calculation view lists "Sequestrations 282.999 t", "Adjustments 14.635 tCO₂e", "Activities 46.439 tCO₂e" and "Uncertainty Discount 1.558 t", and no counterfactual term. |
| 9.9 | Flag | "image (44).png" is generic. "Standard Emission Factors + Calculations (8).xlsx" is uploaded twice, identical. GLEC page 6 reads "v3.1 edition, revised and updated (2024)" against the sheet's "GLEC V3.2 2025". Page 96 reads "US average (diesel): 16.1 g CO2e/t-km". |
| 9.10 | Pass | 43 source records under 42 names (my read of the saved Certify data). Tickets 20/20, BOLs 9/9 and the certificate are identical. |
| S.1 | Flag | BCU Inventory row 16: H 2765.361153, I 414.9274093, J 2350.433744. The certificate says 2,795. The last usage row (55) is "Charm August 2026 RP Oil". |

---

## 3. Observations (not raised in the checklist)

1. **The R&D removal has no record behind it.** K46 rests on a typed-in "200" gallons (R4). No file, date, offload or purpose is linked, and the September guidance does not mention it. Once Certify is corrected to 193,491.9399 kg, a verifier will see a 902 kg deduction with no evidence. The deduction is conservative but unexplained. The 200 gal measurement also adds no uncertainty to Mass of Injectant.
2. **Railcar losses carry no upstream emissions.** Transport-process and pyrolysis components use offloaded mass (197,321.59 kg). The 186.38656 kg lost from GPRX5102 and TILX200231 [R34] carries none of its pyrolysis (0.02950 t [R35]), AECN-SOPOR fuel (0.00229 t [R36]) or rail fuel (0.01062 t [R37]) emissions, 0.0424 t in all [R38]. The August guidance charged the spill railcar GPRX5139 "on the full loaded mass". Whether ordinary losses should be treated the same way is an open question.
3. **The PO pages do not match the BOLs.** Page 5 of every BOL carries a PO headed "PO # Q42025" with a line "Q32025", "Ship To ... El Dorado, KS 67042", dated "10/2/2025". Row 3.7 does not mention either mismatch.
4. **A unit error in the Ops Notes.** M10 says 2457-R's tare "was hand-corrected 19,282->19,290 lb". The BOL field is "Tanker Tare wt(empty) (Kg)".
5. **The week labels are wrong.** The Ops Notes label B3/B4 "(Sat)", but 2026-09-11 and 2026-09-18 are Fridays. W2's Ops week (Sat 2026-09-05 to Sat 2026-09-12) overlaps W3's by two days, 09-11 and 09-12. Four TILX200231 weighs fall in both windows.
6. **The knowledge base is out of date.** Sections 6 and 10A still say the AECN process factor is "current: 0.10402". The H2 2026 value on the Standard EF sheet is 0.1371171258, and the checklist correctly used it.
7. **W2 is still open in Certify today.** Besides the raw offload 4 mass, W2's two allocated-distance datapoints ("Allocated Distance AECN to Sopor Quebec (truck)" and "... Sopor Quebec to Opelousas (rail)") carry maps and BOLs but not the Ops Notes. That is the gap W2's row 3.5 raised.
8. **Dependency thread for whichever fixes are accepted:**
   - 2.3 standard tare: F35 −2.26796 kg [R2].
   - 2.5 Option A: F33 −20.3096 kg [R5].
   - 2.7 R&D correction: Mass of Injectant −902.44216 kg (log `_derived_values.moi_delta_calc`).
   - Each flows into F46, both Certify mass datapoints, the discount (7.3, 7a.3), gross (7.1, 9.1), net (9.8) and, for the Bio-Oil Mass changes, the transport process sum and therefore the exact BCU figure (9.6).
   - Recompute all of them in one pass after the decisions. Do not patch row by row.
