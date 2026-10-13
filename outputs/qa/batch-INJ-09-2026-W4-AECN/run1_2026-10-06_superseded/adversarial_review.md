# Gate 3 Adversarial Review — INJ-09-2026-W4-AECN

**Removal:** rmv_1M3Z5YJN51S0SN1Q (project prj_1HZSSWBQM1S08H83), Certify period 2026-09-19 to 2026-09-25, Basco 6, AECN rail only
**Checklist reviewed:** `Batch_INJ-09-2026-W4-AECN_QA_Checklist.xlsx` (read 2026-10-06)
**Reviewer:** independent adversarial reviewer (did not build the checklist; did not use the QA's recompute file)
**Arithmetic:** `adversarial_review_recompute.py` → `adversarial_review_recompute_output.txt` (cited below as "recompute part n", meaning the numbered blocks in that output file)

## Row counts

| | Pass | Fail | Flag | N/A | Total |
|---|---|---|---|---|---|
| QA as delivered | 30 | 10 | 17 | 5 | 62 |
| After this review's recommendations | 30 | 9 | 18 (7.4 to be re-graded) | 5 | 62 |

- Rows reviewed: **62** (57 Pass/Fail/Flag + 5 N/A)
- Confirmed: **53**
- Challenged: **9** — status change on 4 (3.1 Flag→Fail; 7a.1 Fail→Flag; 9.8 Fail→Flag; 7.4 send back and re-grade), evidence correction only on 5 (1.4, 1.5, 3.7, 8.3, 9.9)

## What I opened myself (this session)

- **Skill and reference files:** adversarial-reviewer SKILL.md, Charm_Isometric_Knowledge_Base.md (all 1,299 lines), batch-qa-aecn SKILL.md, checklist_structure.md, lessons_learned.md.
- **VVB Guidance September 1–30**, fetched 2026-10-06 (full text). Compared with the 2026-09-22 fetch in the W2 folder and the 2026-09-29 fetch in the W3 folder.
- **All 28 W4 scale tickets** (Drive copies), page images with text layer: ticket number, date, time, scale, tractor, trailer, axle readings, gross, commodity label, delivery site. Drive and Certify copies byte-identical, 28 of 28 (my own hash check).
- **The 4 W2 tickets for SHPX215079 offloads 1–2** (W2 folder `tickets/`).
- **All 12 inbound BOL packages:** 2497-R, 2498-R, 2500-R, 2459-R, 2460-R, 2461-R, 2465-R, 2466-R (all 5 pages, incl. pages 4–5 read separately), 2467-R (pages 1–3), 2453-R (pages 1–3), 2454-R and 2455-R (Shipping Details page).
- **SGS SR26-05719.002** (page 2); **Waypoint report 24-200-0020** page 5; **AECN COA Solids Content Dataset** export; **MRV_AECN_Analysis.xlsx** Summary Statistics.
- **Live Ops Notes export** (values, formulas incl. the J and M array formulas, and every cell comment on all tabs); **both Ops Notes copies attached in Certify** (src_1M3VZCDQF1, src_1M3W1NWED1) with formulas and comments.
- **COBB export**, Basco Injection -- COBB tab: rows 903–916 and 3724–3737.
- **Standard Emission Factors export**, 2026 tab rows 3–15 and the H2 2026 AECN Process Emissions tab; **FH 2026 LCA w Stack Emissions.xlsx** (formulas and values).
- **Unrounded Certify pull** (GetGhgEntryQAData): every component, input, ± value and source count; Calculation-view and GHG-statements snapshots; Sources enumeration (72 records); Baton Rouge rail component snapshot.
- **Route evidence:** Watco email image (44), AECN-to-SOPOR map (173 km), Sep-02 Mangrove map, RailLogix (Carville LA) to Basco map; SHA-256 of all four Mangrove maps.
- **Loss evidence image** (`_Bio-oil_loss_evidence.png`).
- **EAC Verification Inventory tracker** export, pages 1–7.
- **Transportation Emissions Accounting v1.1**, pages 5–12.
- **W3 and W2 checklists** (rows 2.2, 2.5, 3.1, 3.5, 4.2, 6.1, 6.3, 7.4, 7a.1, 8.1, 8.2, 8.3, 9.2, 9.5, 9.6, 9.8, 9.10) and their source-read logs (lab results, W2 SHPX215079 entries).

## Step 0 — primary-source check

**Passed.** Every scale-ticket row (2.1–2.4, 5.2, 8.1) cites ticket numbers, tractor and trailer and gross weights read from the images; I re-read all 28 W4 tickets and the 4 W2 tickets and every value matches the QA's log (recompute part 1). The COBB rows (5.4, 5.6) name the tab, the row ranges and the column-A value; rows 903–916 and 3724–3737 in the export carry `INJ-09-2026-W4_bio_oil`, with the offloaded quantities the QA cites. The uncertainty rows (7a.1, 7a.2) list the ± value read from each component window; the unrounded pull carries the same values, and the saved Baton Rouge rail window shows "Mass of load 77,228.57 kg" with no ±.

---

## Row-by-row verdicts

### 1. Batch Folder Completeness

**1.1 — Pass → Confirmed.** Folder 'W4' (owner garrett.lutz@, created 2026-09-27T15:48:55Z) with Ops Notes, Scale Tickets/, Testing/, Kerry Oil/ and the 136-mi route PNG (folder listing); live Ops 'AECN Rail'!B2 reads INJ-09-2026-W4.

**1.2 — Pass → Confirmed.** 4 railcar folders, 14 offload folders, 28 PDFs; my hash check: 28 of 28 identical to the Certify copies.

**1.3 — Pass → Confirmed.** Testing/ holds SR26-05719; page 2 is "Certificate of Analysis: SR26-05719.002", CLIENT ID "9-2026-W4-AECN".

**1.4 — Flag → Challenged (evidence only; Flag stands).**
- *Gap (2) is wrong.* Ops P9 is headed "Full Railcar This Week?" and Q9 "Car Completes This Week?". These ask different questions. SHPX215079 had offloads 1–2 in W2, so the full railcar was not offloaded this week: P13 "PARTIAL" is the correct answer to P9, and Q13 "Y" is the correct answer to Q9. PARTIAL also drives the right rail-mile formula (pro-rated share, M40/M41). Remove gap (2).
- *Gap (1) has a documented basis, now withdrawn.* The 09-22 and 09-29 fetches of the September guidance read: "Railcars offloaded across more than one week. Where a railcar is offloaded across more than one reporting week, the loaded mass is recorded once, in the week the railcar's first offload occurs, and subsequent weeks draw against the same shipment." The Certify-attached Ops copy src_1M3VZCDQF1, cell M13, explains the same choice: "documented in W2 Section 2, not relisted here to avoid implying a new loading event". The 10-06 guidance no longer contains the clause and the live sheet dropped the M10–M13 notes. Re-word gap (1) as: the method is followed, but its written basis now exists only in a superseded guidance version and an older Ops copy.
- Gaps (3) and (4) hold. Add: the AECN Rail pH note on G46 appears in the 10-01 Certify copy but not in the live sheet.

**1.5 — Flag → Challenged (evidence only; Flag stands).** The checklist says "11 of the 12 packages carry it (2466-R is a 3-page corrected package)". The Drive file `BOL_2466-R.pdf` (same file the QA hashed, sha256 5874eb89…) has five pages: page 4 is the TSCA form dated "August 7 2026" and page 5 is Charm PO Q42025 with Ship To "838 SW Purity Springs Road, El Dorado, KS 67042". All **12 of 12** packages carry the El Dorado PO.

### 2. Scale Tickets & Mass Determination

**2.1 — Pass → Confirmed.** 28 tickets, a Full and an Empty for each of 14 offloads, all read by me.

**2.2 — Flag → Confirmed.** SHPX215079 offloads 3–4 full weighs 2026-09-05 09:29 and 14:20; 20 days before the 2026-09-25 injection date (recompute part 14). Literal answer to "within 2 weeks" is no; the tickets are the right railcar and no other week books them, so Flag rather than Fail. Add to the evidence: offload 2 (booked in W2, full 2026-09-05 09:24) and offload 3 (booked in W4, full 09:29) were weighed five minutes apart on the same morning, and one rig (CH2/KL188) hauled offloads 1, 2 and 4. The only written basis for booking a railcar across weeks has been removed from the guidance (see Missed finding M1).

**2.3 — Pass → Confirmed.** All 14 pairs match on tractor and trailer number (my reads, recompute part 1). The "RL" suffix appears only on SHPX215053 tickets (the RailLogix railcar), on KL720 and KL188, against the same trailer number on the paired ticket.

**2.4 — Pass → Confirmed.** My 14 nets equal Ops F28:F41 to five decimals; sum 268,199.87776 kg against Ops A46 268,199.8778 (recompute part 1).

**2.5 — Pass → Confirmed.** W2 offloads 1–2 from my reads of the W2 tickets: (76,720−28,660) + (73,860−28,420) lb × 0.453592 = 42,410.852 kg = Ops H13. Raw total 78,262.76368 kg against BOLs 25.99+25.91+25.97 = 77.87 MT gives an over-draw of 392.76368 kg = Ops J41; offload 4 after the cut 14,321.7608 kg (recompute part 3). Offload 4 is the last weighing (full 09-05 14:20, empty 09-06 07:50). The guidance supports it: "Where a railcar's scale tickets exceed its Bills of Lading, the excess is removed from the final offload through the Uncertainty Adjustment and the railcar's loss is zero." See Missed finding M2: both Certify-attached Ops copies show this railcar's Loss G13 as −392.76368 kg.

**2.6 — Pass → Confirmed.** 267,807.11408 × 0.0129 = 3,454.711772 kg = Ops D46 (recompute part 4).

**2.6a — Pass → Confirmed.** 267,807.11408 × (1−0.0129) × 0.00196 = 518.130709 kg = Ops E46. Dataset export reads "Recommended value for filtration loss 0.196% per-load mean", 136 loads, 71 unique COA PDFs.

**2.7 — Fail → Confirmed.** Certify 'Opelousas to Basco - Tanker Truck Transport Process Emissions' takes 'Bio-Oil Mass - AECN via Rail' 267.80711 t; the guidance reads "the Opelousas distances are not applied to SHPX215053". On the Opelousas mass 190.57854 t the leg is 0.934496 t against Certify 1.313184 t, 0.378688 t over (recompute part 6). Add to the evidence: the BCU was set to Certify's process sum, so this over-charge is offset by an equal BCU and has no effect on the net until both are corrected together (9.6, 9.8).

**2.8 — N/A → Confirmed.** Live AECN Truck tab A28 = 0, G28 = 0, B10:B24 blank.

### 3. Bills of Lading & Transportation

**3.1 — Flag → Challenged → recommend Fail.** The QA's own folder listing records the nine W4 BOLs as "Not in the W4 folder" (they are separate Drive files reached through Ops hyperlinks), and its Sources search (72 records) found none of them in Certify. The KB Document Location Rule: "(1) check the batch Drive folder first, (2) if not found there, check Certify Sources tab, (3) only FLAG/FAIL if the document is absent from BOTH locations." They are absent from both. The KB classification: "Missing evidence = FAIL (you cannot confirm what you cannot see)". Without them a verifier cannot confirm the loaded masses behind the 0.145 t loss or the railcar balances. W2 and W3 passed 3.1 because their BOLs were in Certify. Keep the cross-reference to 9.10.

**3.2 — Pass → Confirmed.** All 12 BOLs I read ship to "CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau"; dates 2026-07-30 (2453-R) to 2026-08-31 (2497/2498/2500-R).

**3.3 — Pass → Confirmed.** My railcar totals 77,570 / 77,640 / 77,770 / 77,870 kg equal Ops E10:E13. Every BOL ties: full − tare = delivered; delivered/1000 = Qty shipped; litres × density within 0.59 kg (2467-R, −0.59) (recompute part 2).

**3.4 — Flag → Confirmed.** The route map reads origin "6045 Point Clair Rd, Carville, LA 70721" and destination "4675 LA-115, St Landry, LA 71367"; guidance and Ops call the transload "Baton Rouge".

**3.5 — Fail → Confirmed, with added evidence.** Certify 'Distance traveled' "2,153 km", "No sources"; Ops K10 2152 under header "Rail (mi)"; the guidance prints "Rail distance from the loading origin to Baton Rouge: 2,152 (map evidence is added in drive)" with no unit. Added checks (recompute part 6):
- 2,153 km = 1,337.81 mi, 0.608 of Watco's 2,199 mi to Opelousas ("The total milage for this move was 2199.").
- The Mangrove map attached in Certify gives AECN to Opelousas by road "3672.1 km"; a 2,153 km rail move from SOPOR to Louisiana would be 59 % of the road distance.
- ASSUMPTION (approximate public coordinates, not session-sourced): straight-line Baie-Comeau to Baton Rouge ≈ 2,843 km, longer than 2,153 km.
- The km value cannot be right; 2,152 mi is plausible but no record of it exists (the "map evidence" the guidance promises was not found by the QA's Drive and Certify searches).
- Precision note: on the Standard EF sheet rail factor the leg is 4.306198 t (shortfall 1.629201 t); the checklist's 4.306208 / 1.629211 uses the GLEC library 0.0161. Both are inside 0.001 t of each other.
- Add to item (3): SHPX215079's rail miles are booked on mixed bases across weeks: W2 615.6079 + 582.0479 (one way) + W4 1,193.8131 + 808.8751 (round trip) = 3,200.34 mi, neither one way (2,199) nor round trip (4,398) for the railcar (recompute part 7).

**3.6 — Pass → Confirmed.** Eight transport components in the pull: three truck-process, two rail-process, two shared embodied plus AECN-SOPOR embodied.

**3.7 — Flag → Challenged (evidence only; Flag stands).** "2466-R is a 3-page corrected package … without TSCA or PO pages" is wrong: pages 4–5 of the same file are the TSCA form ("August 7 2026") and PO Q42025, and the PO "Seller Signature" line is blank. The blank-signature list becomes 8 packages (add 2466-R). The CofA mismatch on 2498-R holds: page 1 "C of A Number RS2-260825-1", Shipping Details "# of the CofA RS2-260828-1".

### 4. Bio-Oil Composition & Testing

**4.1 — Pass → Confirmed.** SR26-05719.002 in Drive Testing/; not linked in Certify (9.10).

**4.2 — Pass → Confirmed.** Carbon "44.0 % (m/m)" with '#'; (44.0 − 39.420350877193) / 6.09332409018271 = 0.7516 SD; band 27.23–51.61 % (recompute part 4). The '#' mark also appears on W2 (40.4 %) and W3 (39.7 %) carbon.

**4.3 — Pass → Confirmed.** H "6.6 % (m/m)" '#', N "<0.75"; H mean 6.874 %, SD 0.563 %. The acid-number comparison belongs in 8.1 (Missed finding M7), not in this Pass row.

**4.4 — Flag → Confirmed.** "LOCATION : FORT LUPTON, CO" on an AECN composite sampled "25-Sep-2026 14:00".

**4.5 — N/A → Confirmed.**

**4.6 — Pass → Confirmed.** "Density at 15°C 1.203 g/cm³"; Waypoint 24-200-0020, Lab No 98021, page 5: "Specific Gravity 1.01 g/mL", ASTM D-1298-85.

### 5. Ops Notes Accuracy & Internal Consistency

**5.1 — Flag → Confirmed.** A3 "Week Start (Sat)" and A4 "Week End (Sat)"; 2026-09-18 and 2026-09-25 are both Fridays.

**5.2 — Flag → Confirmed.** My reads: both SHPX215039 offload-2 tickets print "SHPX215039 O1"; 1186426267016 prints "SHPX215053" only; SHPX215079 tickets carry no delivery-site line.

**5.3 — N/A → Confirmed.**

**5.4 — Flag → Confirmed.** Rows 903–916: offloaded quantities equal Ops F (offload 4 of SHPX215079 at 14,321.76), origin_quantity_kg equals the BOL totals, pH 2.97. Rows 3724–3737: same quantities, injection_ph blank.

**5.5 — Pass → Confirmed.** Live G46 2.97; G28:G41 = $G$46. Live comments on AECN Truck H28 and Kerry D18 read "Wellhead pH = weekly median of Ignition PH-1041, gated to StateRun=1; provided by G. Lutz 2026-09-30."

**5.6 — Pass → Confirmed.** COBB injection_completion_date 2026-09-25 on rows 903–916 and 3724–3737; Ops A28:A41 2026-09-25.

**5.7 — N/A → Confirmed.**

### 6. AECN Feedstock Emissions & Allocation

**6.1 — Fail → Confirmed.** No source record named "LCA CI calculation" among the 72. FH 2026 LCA I11 reads "Total Other Process Emissions MT COT2e/MT Bio Oil (From Vendor LCA)" 0.133052027800741; the vendor workbook behind it was attached on W3 (W3 6.1 Pass) and not on W4. W2 graded the same gap Fail.

**6.2 — Pass → Confirmed.** I12 = SUM(I10:I11) = 0.004065098048 + 0.133052027800741 = 0.1371171258.

**6.3 — Fail → Confirmed.** No "Supporting GHG" record among the 72; attached on W3.

**6.4 — Pass → Confirmed.** 2026!F4 "Production Emissions for AECN Oil--H2 2026" 0.1371171258; H2 2026 tab B1: "applies to H2 2026 reporting periods from the Aug 1–31 2026 RP onward". Certify 0.13712 adds 0.000769 t (recompute part 8).

**6.5 — Pass → Confirmed.** 2026!F5 0.02116 = Certify 0.02116 tCO₂e/t.

**6.6 — Pass → Confirmed.** Both pyrolysis components use 267.80711 t (my delivered mass 267,807.11408 kg, recompute part 3).

### 7. Gross-to-Net Calculation

**7.1 — Pass → Confirmed.** 263.8342716 × 0.440 × 3.667 = 425.691321 t = Certify (recompute part 4).

**7.2 — Fail → Confirmed.** Every AECN component reproduces from its own inputs (recompute part 5); on the evidence, activities are 84.869825 t with the Baton Rouge rail leg on the sheet rail factor (QA 84.869836 with the GLEC 0.0161), 1.25 t above Certify's 83.619739 t. Add: the transport-process part of this error is offset one-for-one by the BCU once 9.6 is applied (see 9.8).

**7.3 — Pass → Confirmed.** Rebuilt independently by moving each ± datapoint by one sigma in every component that uses it and combining the eight changes in quadrature: **2.4428820922 t** against Certify 2.4428820921580847 (recompute part 11). Terms: carbon +1.702765, injectant mass +1.639263, grid electricity −0.588724, Bio-Oil Mass (four components) −0.178274, Opelousas rail mass −0.041348, site diesel −0.030868, Baton Rouge truck mass −0.004511, gasoline −0.004261. 0.574 % of gross.

**7.4 — Flag → Challenged → send back, re-grade after the read.** The checklist says "there is no RP-level BCU Quant or GHG statement to cross-check yet". The QA's own log (bcu_sources.usage_september.note), matching the row I saw on page 6 of the EAC tracker export, reads: "Charm September 2026 RP Oil -- Emissions Reductions from September1-September30_Bio-Oil_GHG_Statement_Results.xlsx as of 2026-10-04 (11 removals, W1-W4); revise if Sept site emissions change." An RP-level results workbook covering W4 existed two days before this QA and was not opened. Per the skill, a Flag raised because the check was not done is unfinished work. Open that workbook and compare its W4 net and BCU with Certify (362.068 t; 19.339 t), then re-grade. If it cannot be reached, list the three access attempts. I did not open it (needs the Drive connector or Drive mount; see Skipped).

### 7a. Per-Component Uncertainty

**7a.1 — Fail → Challenged → recommend Flag.** The gap is real: Baton Rouge rail "Mass of load 77,228.57 kg" carries no ± while the same mass on the Baton Rouge truck leg carries ±290.28 kg, and the check's literal answer is no. Its effect on the discount is 0.000021 t (separate datapoint) to 0.000039 t (shared datapoint), and 0.000084 t after the 2,152-mi correction (recompute part 12). The KB rule is "Value in Certify doesn't match evidence = FAIL (always, no rounding tolerance beyond ~0.001 tCO2e)"; this effect is 12 to 48 times below that tolerance and cannot misstate the net. Flag, to be fixed in the same edit as the 3.5 distance on that component.

**7a.2 — Pass → Confirmed.** 1,015.98 kg = 14 × 72.57; 725.7 = 10 × 72.57; 290.28 = 4 × 72.57; carbon 0.176 = 0.004 × 44.0 (pull).

**7a.3 — Pass → Confirmed.** Discount present and reproduced (7.3). The statement cross-check depends on 7.4.

### 8. Data Integrity & Anomaly Check

**8.1 — Flag → Confirmed.** My reads give the same eight tickets with "00 LB" on the steer axle, all CH1/KL720. CH1/KL720 empties weigh 29,240–29,640 lb with or without a steer reading, so the steer weight is captured on another platform. Add the acid number (M7).

**8.2 — Flag → Confirmed.** Losses 341.42608 / 66.69616 / 223.91168 kg (recompute part 3). Image ties: 0.0044 × 5.3728 + 0.0044 × 0.14507 + 0.04682 + 0.00722 = 0.07832 (image 0.07833); its railcar figures reproduce from 77.57 t × (107.49722 × 0.0001143 + 2199 × 2.5910374e-05) = 5.3728 and 107.49722 × 3 × 0.0002375605888 + 2199 × 3.113066508e-05 = 0.14507. All three on 2,199 mi: 0.144996 t; SHPX215053 on 2,152 mi: 0.144574 t (recompute part 9). Add M2 and M5.

**8.3 — Flag → Challenged (evidence only; Flag stands).** Remove "P13 also reads 'PARTIAL' for a railcar that closes this week (1.4)": P13 answers "Full Railcar This Week?" correctly (see 1.4). Add M1 (the multi-week guidance clause was removed between the 09-29 and 10-06 fetches) and the same-morning split of offloads 2 and 3 (see 2.2). The 20-day hold remains unexplained.

**8.4 — Pass → Confirmed.** Each railcar: 4 offloads against 3 inbound BOLs (recompute part 14).

### 9. Isometric Certify — Removal Component Mapping

**9.1 — Pass → Confirmed.** 425.691321 t reproduces (recompute part 4).

**9.2 — Fail → Confirmed.** Recomputed from 2026!F6/F10/F11/F13 (recompute part 6–7): Baton Rouge rail 1.629 t short, Opelousas truck 0.378688 t over, rail embodied round trip 0.235078 t extra against W1–W3's one-way basis; Baton Rouge truck on the sheet factor 1.200503 t against Certify 1.200119 t (GLEC library 0.071).

**9.3 — N/A → Confirmed.** No injection-side AECN component in the pull.

**9.4 — Pass → Confirmed.** 36.721711 t and 5.666798 t reproduce.

**9.5 — Fail → Confirmed.** 'BCU - Transport Process' constant reduction 19.339 tCO₂e, source count 0 in the pull; no "Retirement" record among the 72. Protocol p9, EC1 documentation: "Provide proof of BCU purchase and retirement in a volume equivalent to the volume of fuel substitution claimed." W3 had the certificate attached.

**9.6 — Flag → Confirmed.** 19.339 − 19.3392476 = −0.0002476 t, so it does not exceed (protocol p11, Eq 5: "(F_j − F_BCU,j ED_BCU,j/ED_Fuel,Transportation,j) ≥ 0"). After the 3.5 and 2.7 fixes the BCU must rise to the corrected sum (20.58976 t with Certify's factors and the Baton Rouge rail leg on the sheet factor; 20.5903 t with every leg on sheet factors); fixing 2.7 alone would leave the BCU 0.3784404 t over its emission (recompute part 10). The EAC tracker's September usage row (171.9503 t) moves with it.

**9.7 — Pass → Confirmed.** Calculation view shows Sequestrations, Adjustments, Activities and Uncertainty Discount only.

**9.8 — Fail → Challenged → recommend Flag.** The checklist computes the evidence-basis net with "the BCU stays 19.339 t", giving 1.249735 t below Certify. That contradicts its own 9.6 ("Charm's rule is the exact process figure, so the BCU entry follows the corrected sum") and the KB rule: "The BCU quantity (in tCO₂e) in Reductions must equal, and never exceed, the corresponding diesel emission (in tCO₂e) in Activities". W3's 9.8 applied "BCU at the process sum" in its evidence net. With the BCU at the corrected process sum, all four corrections (A–D) give **362.069006 t, +0.000886 t against Certify's 362.068120 t** (recompute part 12 D). The net is right because the BCU equals Certify's own understated process sum. The −1.25 t figure only arises if the activities are fixed and the BCU is not, which 9.6 forbids. Flag: the net holds only while the activity and BCU errors cancel, so the Baton Rouge distance (3.5), the Opelousas truck mass (2.7) and the BCU (9.6) must be corrected in one edit. The activity errors stay Fail in 3.5, 7.2 and 9.2.

**9.9 — Flag → Challenged (evidence only; Flag stands).** "Aug-07 and Sep-02 are the same size (891,889 bytes)" uses file size as evidence (lessons_learned, Failure Category 3: "File metadata is never evidence"), and it implies duplicates. My SHA-256 hashes differ (Aug-07 543fb81b…, Sep-02 96ea1854…). Replace with what the images show: each is a Mangrove route from "AECN - Produits Forestiers Arbec S.E.N.C." to "Opelousas, LA" (Sep-02: "3672.1 km / 2281.8 mi"), linked to the AECN-to-SOPOR truck allocation. The 'image (44).png', GLEC v3.1-versus-v3.2 and Standard EF triple-upload points hold. Protocol p7: emission factors must "be the most recently updated emission factor published".

**9.10 — Fail → Confirmed.** 72 records. Nine of the eleven open datapoints carry 0 sources in the pull; the AECN-to-SOPOR allocated distance (8 sources, no Ops Notes) and the loss (2 sources, no BOLs) fail on a missing category. Add M2 (negative loss on both attached Ops copies) and M3.

### Sidebar

**S.1 — Flag → Confirmed.** EAC tracker page 1: total 2765.3612, used 586.8777, remaining 2178.4834; page 3 last row: mass of batch 1,091,266.292 kg, allocation 2765.36 MT CO2e; certificate 2,795 TERCs. September usage row 171.9503 t is marked "revise if Sept site emissions change".

---

## Missed findings

**M1. The guidance clause behind SHPX215079's two-week booking has been removed.** The 2026-09-22 and 2026-09-29 fetches of "VVB Guidance September 1–30" contained: "Railcars offloaded across more than one week. Where a railcar is offloaded across more than one reporting week, the loaded mass is recorded once, in the week the railcar's first offload occurs, and subsequent weeks draw against the same shipment." The 2026-10-06 fetch does not (the whole "AECN Rail — Basis for Loaded Mass (Week 3)" section is gone). W4 books SHPX215079 on exactly that method (H13 'Previously Claimed' 42,410.852 kg, BOLs not relisted, cut on offload 4). A verifier reading the current guidance will not find it. Belongs in 8.3 and 1.4. W3 relies on the removed BOL-volume × 1.22 kg/L "Basis for Loaded Mass" for its loaded masses, so its re-review should check this too.

**M2. Both Certify-attached Ops copies show a negative loss.** src_1M3VZCDQF1 and src_1M3W1NWED1 both carry SHPX215079 G13 "Loss (kg)" = −392.76368 (the live sheet now reads 0 through MAX(0,…)). A verifier reading the attached evidence sees a negative loss on the railcar whose loss the checklist says is zero. Belongs in 9.10 and 8.2.

**M3. The cut is explained only in an older attached copy, with figures 2 kg off.** Copy src_1M3VZCDQF1, M13: "raw offloaded (78,260.76 kg) exceeds the 77,870 kg loaded mass by about 390.76 kg -- absorbed by the tail-offload Uncertainty Adjustment (col J)". The true figures are 78,262.76368 and 392.76368 kg. The live sheet has no note. The same copy's M10 reads "BOL sequence has a gap, no 2499-R, not this car, unresolved."; W2's checklist lists BOL "2499-T" (a direct truck), which resolves it. Belongs in 9.10.

**M4. SHPX215079 rail embodied is booked on mixed bases across weeks:** 3,200.34 mi in total (recompute part 7). Belongs in 3.5(3).

**M5. Rail embodied for lost oil is counted twice (conservative, 0.000557 t).** The rail-mile formula gives a FULL railcar's first offload the whole trip, so the main rail embodied component already covers the lost oil's share; the loss figure charges that share again (recompute part 9). The loss image also uses one-way rail embodied while the W4 rail embodied component uses round trip. Belongs in 8.2.

**M6. The net is insensitive to transport-process errors while the BCU tracks the process sum.** The material consequences of 3.5 and 2.7 are a 1.25 t larger BCU draw on certificate 13-47206-50000 and correct activity reporting, not a change to net CDR. Max should see this in the summary so the 3.5 Fail is not read as a 1.25 t over-credit.

**M7. Acid number tripled.** SR26-05719.002: "156 mg KOH/g" marked '#'; W2 61 and W3 47 (their logs). Not a CDR input and not classified on any row; add to 8.1 as an unexplained change.

---

## Skipped (needs sign-in)

- **Opening "September1-September30_Bio-Oil_GHG_Statement_Results.xlsx"** (the RP results workbook named in the EAC tracker, needed for 7.4). It sits in Google Drive; reaching it needs the Drive connector or the local Drive mount, which may raise a permission prompt. Not attempted.
- **Repeating the QA's Drive search for a SOPOR–Baton Rouge rail distance record** (3.5). Needs the Drive connector. I relied on the QA's saved search log (`rail_distance_evidence_search.json`, four searches, no record found).
- **No live Certify read was needed**; all Certify checks used the saved unrounded pull and window snapshots from 2026-10-06.
