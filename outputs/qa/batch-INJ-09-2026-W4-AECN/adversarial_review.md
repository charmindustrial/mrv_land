# Gate 3 Adversarial Review: INJ-09-2026-W4-AECN

Removal rmv_1M3Z5YJN51S0SN1Q (Certify period 2026-09-19 to 2026-09-25). Checklist reviewed: `Batch_INJ-09-2026-W4-AECN_QA_Checklist.xlsx`, all 62 rows. Reviewed 2026-10-07 from the saved copies. Certify was not opened live; the saved captures and data pulls from this morning were used. My arithmetic: `adversarial_review_recompute.py`, output in `adversarial_review_recompute_output.txt` (parts cited below as "script part n"; each part is headed "=== n." in the output file).

## 1. Row counts

| Status | As delivered | After my recommendations |
|---|---|---|
| Pass | 30 | 30 |
| Fail | 9 | 13 |
| Flag | 18 | 14 |
| N/A | 5 | 5 |
| Total | 62 | 62 |

Status changes: 2.2, 7a.1, 8.2, 8.3 move Flag to Fail. Three more rows (2.6a, 7a.3, 9.6) keep their status but need their evidence corrected.

## 2. What I opened myself

Rules and role
- `skills/qa/adversarial-reviewer/SKILL.md` (full)
- `knowledge-base/Charm_Isometric_Knowledge_Base.md` (full)
- `skills/qa/batch-qa-aecn/references/checklist_structure.md` and `lessons_learned.md` (full)
- `skills/qa/batch-qa-aecn/SKILL.md` (status definitions, lines 270-300; uncertainty reference table)
- Memory files the QA cites as policy: `project_bcu_reduction_cap_policy.md`, `project_railcar_mass_policy.md`, `project_custody_upstream_emissions.md`
- `knowledge-base/isometric-pdfs/Transportation Emissions Accounting v1.1 — Isometric.pdf`, pages 9-12

Primary documents, W4
- All 28 W4 scale-ticket images in `drive_w4/Scale Tickets/` (ticket no., date, time, scale, axles, gross, tractor, trailer, commodity line), and the 4 W2 tickets in `drive_w2_215079/`. Transcriptions in my script part 1.
- Hashes of the 28 Drive tickets against the 28 Certify ticket files: 28 of 28 identical. BOL 2453-R, 2454-R, 2455-R in `bols/` identical to the Certify copies.
- All 12 BOL packages in `bols/`, every page (BOL, Shipping Details, weighbridge printout, TSCA form, Charm PO).
- `drive_w4/Testing/SR26-05719 W4 Kerry AECN QOWV COA.pdf` (all 3 pages)
- `drive_w4/RailLogix (Carville LA) to Basco B6 Truck Route - 136 mi.png`
- `source_exports/VVB_Guidance_September_1-30_run3.txt` (full)
- `source_exports/INJ-09-2026-W4_Ops_Notes_live_export_run3b_2026-10-07T0825Z.xlsx`, loaded with formulas and notes: every cell note on all tabs, AECN Rail (all cells including the J and M array formulas), Summary, AECN Truck. Compared with the 01:20Z export (17 changed cells, all Kerry or Kerry-driven totals).
- `source_exports/Standard_Emission_Factors_export_run3_2026-10-07T0213Z.xlsx`: 2026 tab rows 1-71, H1 and H2 2026 AECN Process Emissions tabs, 2026 Railcar Embodied Emissions tab, Truck and Trailer EE 2026 tab
- `source_exports/COBB_Bio-oil_Injection_Tracker_export_run3_2026-10-07T0122Z.xlsx`: Basco Injection -- COBB (all 56 W4 rows, import times), Loads tab
- `source_exports/certify_graphql_GetGhgEntryQAData_run3_...0123Z.json` and `..._run3recheck_...0826Z.json` (identical content; every component, input, uncertainty and linked source)
- `certify_run3/`: all 13 `modal_*.txt`, `calculation_view.yml`, `datapoints_tab.yml`, `sources_tab.yml`, `sources_enumeration_run3.json` (72 sources), `certify_sources_enumeration_run3.json`, `ghg_statements_run3.txt`, `source_GLEC_V3.2_library_run3.txt`, `files/_download_manifest_run3.json`
- `certify_run3/files/`: both Ops Notes copies (src_1M3VZCDQF1, src_1M3W1NWED1, with notes), FH 2026 LCA w Stack Emissions.xlsx, AECN Embodied Emissions Calc Sheet (1).pdf, Charm-RetirementCertificate-RD-EACs-20251218.pdf, _Bio-oil_loss_evidence.png, image (44).png, Opelousas Railyard to Basco.png, AECN to SOPOR (Baie Comeau) (2).png, Aug-05 and Sep-02 Mangrove route maps (all four hashed), GLEC_FRAMEWORK_v3_UPDATED_04_12_24.pdf pages 1-6
- `source_exports/MRV_AECN_Analysis.xlsx_run3.xlsx` (Summary Statistics), `AECN_COA_Solids_Content_Dataset_run3.xlsx` (Summary), `Charm_EAC_Verification_Inventory_tracker_run3.xlsx` (BCU Inventory, BCU AE Breakdown, GHG Statement BCU Usage), `Formation_Fluid_..._run3.pdf` page 5, `Rail_Logix_Lessons_Learned_run3.txt`
- `source_exports/September1-September30_Bio-Oil_GHG_Statement_Results_run3.xlsx` and `..._run3b_...0826Z.xlsx` (compared: 8 cells changed, W3 and W4 Kerry rows swapped), `..._GHG_Statement_Report_v1.7_run3.docx` (all text)

Prior weeks
- `../batch-INJ-09-2026-W3-AECN/source_exports/`: VVB guidance fetched 2026-09-29, INJ-09-2026-W3 Ops Notes, W2 Ops Notes export, W3 Certify data pull; `SR26-05599_W3_QOWV_AECN_COA.pdf`
- `../batch-INJ-09-2026-W2-AECN/SR26-05494_W2_QOWV_AECN_COA.pdf`

QA records used only to locate items, then checked against the files above
- The checklist; `batch_INJ-09-2026-W4-AECN_source_reads.json` (top-level keys, `policy`, `bcu_sources`); `run3_reads/vvb_guidance_w3_fetch_comparison_run3.json`; `run3_reads/rail_distance_evidence_search_run3.json`; `drive_folder_listing_run3.json`; `bols/_bol_copies_run3.json`; `vaulted_search.json`; `batch_timestamps.json`

Search I ran
- Google Drive, read only: `(fullText contains '2153' or fullText contains '2,153' or title contains 'Baton Rouge' or fullText contains 'Point Clair') and modifiedTime > '2026-09-10'`. 30 results on page one; none is a SOPOR-to-Baton Rouge rail distance record. The QA's own searches never tried 2153, Certify's figure.

Not opened, by rule or because my own arithmetic replaced it: `recompute_INJ-09-2026-W4-AECN.py`, `recompute_output.txt`, `build_checklist.py`, `build_source_reads.py`, `mass_chain/`, and the QA's files in the shared scratch folder.

## 3. Challenged items

### 2.2 Ticket dates within 2 weeks of injection: Flag, recommend Fail

The criterion (knowledge base, checklist section 2): "For each pair: dates within 2 weeks of injection [VR Sec 3.5]". Two pairs fail it:
- SHPX215079 offload 3: full ticket 1124426248529, "9-05-26", 09:29; empty 1312226248408, "9-05-26", 12:35, at Pilot Travel Center, Bunkie (I-49 Exit 40), next to the site. The oil was delivered on 5 September.
- SHPX215079 offload 4: full 1124426248533, "9-05-26", 14:20; empty 1124426249537, "9-06-26", 07:50.

At the 2026-09-25 injection date in Ops and COBB, the full weighs are 19.60 and 19.40 days old (script part 1). Nothing records where these 35,459.148 kg (script part 3; 13.24 % of the week's 267,807.1141 kg in Ops C46, script part 13) were held for three weeks. The September guidance also puts a railcar's close in the week its last offload happens: "The lost mass, loaded mass minus delivered mass, is quantified per railcar and recognised in the week in which the railcar's final offload is completed". SHPX215079's last offload was weighed on 5-6 September, inside W2's week (W2 Ops B3 2026-09-05 to B4 2026-09-12), yet the railcar closes in W4.

The batch-QA skill's Fail definition covers "missing required data", and its test reads: "does the evidence fully support the reported Net CDR value? If not, it's a FAIL." The evidence does not support dating 35.459 t of this removal to 19-25 September.

The note also says "Three railcars sit inside the window" without stating that SHPX215091 (all four full weighs 2026-09-17) and SHPX215039 offloads 1-2 (2026-09-18) were weighed before the Certify period opened on 2026-09-19 (see Observation 1).

Recommendation: Fail. Close it with a dated storage and injection record for offloads 3-4, plus a written basis in the guidance; otherwise move the two offloads to the week they were injected. 8.3 has the same root cause, and one fix closes both.

### 7a.1 Every component that needs uncertainty has it: Flag, recommend Fail

The Certify window for "SOPOR to Baton Rouge Rail Process Emissions" reads "Mass of load / Mass of load / 77,228.57 / kg / No sources", with no ± value. The same mass on the Baton Rouge truck leg reads "77,228.57 / ±290.28 / kg". The skill's uncertainty table requires one for "Transport — SOPOR->Opelousas Rail | Mass of Load | 72.57 kg per discrete weight", and the Baton Rouge rail leg is the same kind of leg. Layer 1 is "Every component requiring uncertainty has it".

The missing input works against conservatism. With it, the discount rises from 2.4428820922 to 2.4429028145 t (script part 7), so today's net is slightly overstated.

The QA kept Flag because the effect is inside "the 0.001 t tolerance". In the skill, that allowance belongs to a different rule ("Value in Certify doesn't match evidence = FAIL (always, no rounding tolerance beyond ~0.001 tCO2e)"). It covers rounding when matching values; it does not excuse a missing required input. The skill's Fail definition lists "missing required data" with no size floor. The QA also graded 2.7, an error in the safe direction, as Fail.

Recommendation: Fail. Enter ±290.28 kg in the same edit as the 3.5 distance fix.

### 8.2 Spills, losses and irregularities documented: Flag, recommend Fail

"AECN Bio-oil Loss - Upstream Emissions" (0.145 tCO₂e) is linked to two sources: `_Bio-oil_loss_evidence.png` and `INJ-09-2026-W4 Ops Notes - 2026-10-01`. Neither supports 0.145 t as reported:
- The linked Ops copy's loss column G10:G13 reads 341.42608, 66.69616, 223.91168 and −392.76368 kg, which totals 239.27024 kg. At Certify's own rate (0.229418 t per t) that is 0.054893 t, not 0.145 t (script part 13). Getting 0.145 t requires 632.03392 kg, which means dropping the −392.76 kg. Only the live sheet (`MAX(0, E13-F13)`) and report v1.7 do that, and neither is attached.
- The example image covers SHPX215053 only, labelled "(Opel to B6)". It uses the full-railcar upstream figure of 5.3728 t, which reproduces only on the 2,199 mi Opelousas rail distance (script part 10). The guidance states "the Opelousas distances are not applied to SHPX215053". The QA graded 2.7 Fail for breaking that same sentence.
- The BOLs behind three of the four loaded masses are not attached (3.1).

Skill rule: Fail for "conflicting evidence"; knowledge base: "Any issue where the evidence says something different from what's being reported ... is a FAIL." The amount is small and runs in the safe direction (0.145 against 0.144574 t on the guidance basis, script part 10), but the attached evidence gives a different number.

Recommendation: Fail. Attach the current Ops sheet (G13 = 0), a calculation for each railcar with SHPX215053 on 2,152 mi, and the nine missing BOLs. Then re-enter the loss as 0.144574 t, or document why 0.145 is kept.

### 8.3 Inventory reconciliation / carryover documented: Flag, recommend Fail

Knowledge base: "If inventory reconciliation applies: carryover oil from prior production periods documented and allocated [VR Sec 3.5]". The QA's own note concedes the gap: "Nothing records where the 35,459.148 kg sat in between." I confirmed the timeline from the tickets (2.2 above). Lessons learned, principle 7: "Missing evidence = FAIL. No exceptions." The cross-week clause the QA cites existed only in the guidance as fetched on 2026-09-29, and even there it covered loaded mass, not when the oil was injected: "Where a railcar is offloaded across more than one reporting week, the loaded mass is recorded once, in the week the railcar's first offload occurs, and subsequent weeks draw against the same shipment."

Recommendation: Fail, with the same fix as 2.2.

### 9.6 BCU does not exceed transport process emissions: Flag (keep), evidence needs correcting

The note says the BCU "sits 0.0002476 t below, so it does not exceed." The policy the QA cites reads: "Over-coverage of any size is a FAIL (INJ-09-2026-W3-QOWV: BCU 6,264 kg vs process 6,263.604 kg, 0.396 kg over, Fail; fix = enter the exact process figure, never round down either)." The knowledge base adds: "BCU quantity ... must equal, and never exceed". Today's 19.339 t is Certify's own process total of 19.3392476 t rounded down by 0.2476 kg (script part 6), so it already breaks the exact-figure rule before any correction.

Recommendation: keep Flag; the shortfall runs in the safe direction and the larger 1.2507709 t correction is already tied to 3.5 and 2.7. Add to the note that the current entry is also 0.2476 kg short of Certify's own total.

### 2.6a Filtration loss deduction: Pass (keep), quote is not word for word

The note gives 'Recommended value for filtration loss 0.196% per-load mean' as a quote. The dataset's Summary tab actually reads: A12 "Recommended value for filtration loss", B12 0.001959191176, C12 "per-load mean — best represents what is actually delivered". "0.196%" is not in those cells; it appears as "Proposed (fixed 0.196%)" on the 'Materiality (Sec 2)' tab. The dataset title 'AECN COA Solids Content Dataset (May 2025 - May 2026)' cannot be confirmed from the saved export; its B2 reads "2025-05-18 to 2026-05-18".

The arithmetic holds (Ops E46 518.1307085 kg; script part 4: 518.130709). Ops O7 uses 0.00196, the dataset's 0.001959191176 rounded up, which takes slightly more oil off the claim.

Recommendation: keep Pass and replace the quote with the cell-by-cell wording.

### 7a.3 Discount present and consistent: Pass (keep), one check left undone

The note says "The cross-check against the GHG statement waits for the September statement (7.4)." The knowledge base's Layer 3 asks to "Verify the discount value is consistent with the GHG Statement Section E", and the drafts the QA already read allow it now: results workbook W4 row M10 2.4429 against Certify 2.4428820922 t; workbook column M total 10.9981 t against report v1.7 Section E "Uncertainty Discounts" 11.00 (script part 12). Both agree to their rounding.

Recommendation: keep Pass and write this check into the note. Also note that Layer 3 rests on an incomplete set of inputs until 7a.1 is fixed.

## 4. Confirmed items

- 1.1 Pass: Drive listing shows W4 holding the Ops Notes, Scale Tickets/, Testing/, Kerry Oil/ and the RailLogix map; Ops 'AECN Rail'!B2 reads INJ-09-2026-W4; Certify period 2026-09-19 to 2026-09-25.
- 1.2 Pass: 28 ticket PDFs, a Full and an Empty in each of 14 offload folders; my hashes match the 28 Certify copies 28 of 28.
- 1.3 Pass: SR26-05719 page 2 is CLIENT ID "9-2026-W4-AECN"; pages 1 and 3 are W4 Kerry and QOWV.
- 1.4 Flag: confirmed the clause is in the 2026-09-29 guidance fetch and absent from today's; the live AECN Rail tab has no cell notes (notes only on AECN Truck H28 and Kerry D18); G46 note present in the 2026-10-01 Certify copy; row 9 headers "Arrival Date at Opelousas" / "Opel→Basco (mi)"; P13 'PARTIAL', Q13 'Y'; the 17 cells changed this morning are Kerry rows and the totals they feed.
- 1.5 Flag: page 5 of all 12 BOL packages is Charm PO Q42025 dated 10/2/2025, Ship To "838 SW Purity Springs Road, El Dorado, KS 67042"; every BOL ship-to is SOPOR Baie-Comeau.
- 2.1 Pass: 28 of 28 ticket images present and readable; all linked only to 'Bio-Oil Mass - AECN via Rail' (Certify data pull).
- 2.3 Pass: every pair matches on tractor and trailer from the images (CH1/KL720, CH2/KL188, CH1/KL192 for SHPX215079 offload 3); "RL" suffix differences confirmed on SHPX215053 offloads 1, 3, 4.
- 2.4 Pass: (full − empty) lb × 0.453592 equals Ops F28:F41 on all 14 rows to five decimals; total 268,199.8778 kg = A46 (script part 1).
- 2.5 Pass: SHPX215079 delivered 78,262.76368 kg against BOL 77,870 kg; over-draw 392.76368 kg = Ops J41; offload 4 carries 14,321.7608 kg; the other three railcars stay under their BOL totals (script part 3).
- 2.6 Pass: 267,807.11408 × 0.0129 = 3,454.711772 kg, equal to Ops D46 (script part 4).
- 2.7 Fail: Opelousas truck leg uses 267.80711 t (all four railcars); on the Opelousas mass of 190.57854 t it is 0.934496 t against Certify 1.313184 t, 0.378688 t over (script part 8). Breaks the guidance sentence quoted.
- 2.8 N/A: AECN Truck A28 = 0, B10:B24 blank.
- 3.1 Fail: 2497-R, 2498-R, 2500-R, 2459-R, 2460-R, 2461-R, 2465-R, 2466-R, 2467-R are absent from the 72 Certify sources and from the W4 folder listing; knowledge base rule quoted correctly.
- 3.2 Pass: all 12 BOLs ship to "CHARM Industrial Inc. /WATCO, Société du port ferroviaire de Baie-Comeau"; dates 2026-07-30 to 2026-08-31.
- 3.3 Pass: on all 12, full − tare = Product delivered = weighbridge Masse nette, and Product delivered ÷ 1,000 = Qty shipped; litres × density lands within 0.59 kg (allowance about 1.08 kg); railcar totals 77,570 / 77,640 / 77,770 / 77,870 kg (script part 2).
- 3.4 Flag: map origin "6045 Point Clair Rd, Carville, LA 70721" and end "4675 LA-115", against the Opelousas map's "4687 LA-115"; Ops M10 "RailLogix Load in Baton Rouge".
- 3.5 Fail: Certify "2,153 km" (1,337.8 mi, 60.8 % of 2,199); the guidance gives "2,152 (map evidence is added in drive)"; Ops K10 2152 under 'Rail (mi)'; report v1.7 "Its rail leg (2,152 mi)". On 2,152 mi: 4.306208 t against 2.676997 t (script part 8). Round trip M42 15,102.68824 mi against one way in W2 and W3 (Ops M formulas, no ×2): +0.235078 t. 1,946 mi = 10 × 42.9 × 2 + 4 × 136 × 2. Watco image text "The total milage for this move was 2199." names no railcar or date.
- 3.6 Pass: 5 process + 3 shared embodied transport components present (Certify data pull).
- 3.7 Flag: seller signature blank on 2497-R, 2498-R, 2500-R, 2461-R, 2465-R, 2466-R, 2467-R, 2453-R (signed on 2459-R, 2460-R, 2454-R, 2455-R); 2466-R correction header and hand-corrected density 1.1980 / 21,586 L; 2498-R CofA RS2-260825-1 (page 1) against RS2-260828-1; 2453-R "#0X-2026"; Loads tab rows 445-446 show 2497-R 25.73 and 2498-R 25.91 with CofA "RS2-280828-1" / "RS2-280825-1".
- 4.1 Pass: SGS SR26-05719.002 present in Drive Testing/ (presence in either place satisfies the knowledge base rule); the missing Certify link is carried by 9.10.
- 4.2 Pass: carbon 44.0 % "#"; dataset mean 39.420350877193, SD 6.09332409018271, n 285; band 27.23-51.61; 0.752 SD above mean (script part 11).
- 4.3 Pass: H 6.6 % "#", N "<0.75"; dataset H mean 6.87438596491228, SD 0.562848694875852.
- 4.4 Flag: LOCATION "FORT LUPTON, CO" on the AECN page; W3's SR26-05599.002 also prints Fort Lupton; sample and received dates as stated.
- 4.5 N/A: AECN is not aqueous.
- 4.6 Pass: density 1.203 g/cm³ against Waypoint report 24-200-0020, Lab No 98021, page 5, Specific Gravity 1.01 g/mL.
- 5.1 Flag: A3/A4 'Week Start (Sat)' / 'Week End (Sat)'; 2026-09-18 and 2026-09-25 are Fridays (script part 13).
- 5.2 Flag: transcription exact on all 28; labels confirmed: both SHPX215039 offload 2 tickets say "SHPX215039 O1"; 1186426267016 reads "SHPX215053"; mixed SHPX215053 labels; SHPX215079 tickets print no delivery site.
- 5.3 N/A: no aqueous phase.
- 5.4 Flag: COBB rows 3724-3737 (import 2026-10-05 12:24:22) match Ops masses, BOL totals and BOL lists; the same 14 rows appear at 903-916, 1833-1846, 2761-2774 (imports 2026-09-29 08:37, 09-29 11:54, 09-30 11:14); injection_ph 2.97 in the first three and blank in the latest.
- 5.5 Pass: G28:G41 and G46 = 2.97; O6 "2.0 - 4.0"; note text quoted correctly from AECN Truck H28 / Kerry D18.
- 5.6 Pass: COBB injection_completion_date 2026-09-25 on all 14; Ops A28:A41 2026-09-25; Certify period ends 2026-09-25.
- 5.7 N/A: density field blank for AECN, as the checklist guide directs.
- 6.1 Fail: the vendor workbook is in none of the 72 sources or the W4 listing; the W3 removal links it on the same datapoint (W3 Certify pull).
- 6.2 Pass: FH 2026 LCA w Stack Emissions.xlsx Sheet1 I10 0.004065098048 + I11 0.133052027800741 = I12 0.1371171258.
- 6.3 Fail: 'Supporting GHG data 30Jun2026 S.xlsx' is linked on W3 and absent from W4's 72 sources and the W4 folder.
- 6.4 Pass: sheet row 4 "Production Emissions for AECN Oil--H2 2026" 0.1371171258; H2 tab "applies to H2 2026 reporting periods from the Aug 1–31 2026 RP onward"; Certify 0.13712 adds 0.000769 t.
- 6.5 Pass: sheet row 5 0.02116; calc sheet "Total Embodied Emissions (T CO2e)/MT Bio Oil 0.02115941123"; Certify 0.02116.
- 6.6 Pass: both pyrolysis components use 267.80711 t (before sparging); delivered plus lost mass equals loaded mass on all four railcars, so pyrolysis is charged on everything that entered custody.
- 7.1 Pass: 263.8342716 × 0.44 × 3.667 = 425.691321 t, equal to Certify; my MOBI 263,834.2716 kg (script part 4, part 6).
- 7.2 Fail: activities 83.619739 t reproduce; on the evidence +1.250523 t (script part 8).
- 7.3 Pass: discount is the root-sum-square of one term per input: 2.4428820922 t, exactly Certify's figure (script part 7), 0.574 % of gross. It becomes 2.4429028 t once 7a.1 is fixed.
- 7.4 Flag: workbook totals (process 385.3341, site 20.5500, reductions 172.6573, net 1,743.96) against report v1.7 Section E (384.65, 20.48, 171.95, 1,744.01); W4 row matches Certify; morning edit swapped only the W3/W4 Kerry rows (script part 12).
- 7a.2 Pass: windows show ±1,015.98 kg (14 × 72.57), ±725.7 (10 × 72.57), ±290.28 (4 × 72.57), carbon ±0.176 (0.004 × 44.0).
- 8.1 Flag: zero steer readings on exactly the eight CH1/KL720 tickets named; all 28 tickets' axle readings add to their gross (script part 1); the ticket reads "The GROSS WEIGHT is the CERTIFIED WEIGHT and was weighed on a full length platform scale."; acid number 156 "#" against W2 61 and W3 47 (SR26-05494.002, SR26-05599.002).
- 8.4 Pass: four offloads against three BOLs for every railcar, including SHPX215079 across W2 and W4.
- 9.1 Pass: 425.691321 t (see 7.1).
- 9.2 Fail: every component recomputes from its own inputs (script part 6); the three wrong legs are as stated; Certify uses rounded factors (rail 0.02591 against sheet 0.025910374 kg per t-mi) and GLEC library factors on both Baton Rouge legs (script part 5).
- 9.3 N/A: no LCS; Standard EF sheet row 24 lists sample transport as "N/A Immaterial".
- 9.4 Pass: 267.80711 × 0.13712 = 36.721711 t; 267.80711 × 0.02116 = 5.666798 t.
- 9.5 Fail: 'Constant CO₂ reduction' 19.339 t shows "No sources"; the W3 BCU links the certificate; protocol quotes in the note are word for word (Transportation Emissions Accounting v1.1, page 9).
- 9.7 Pass: the Calculation view shows only Sequestrations, Adjustments, Activities and Uncertainty Discount.
- 9.8 Flag: 425.691321 − 83.619739 + 22.43942 − 2.4428821 = 362.068120 t. On the evidence, with the BCU at the corrected total and the loss at 0.144574 t, I get 362.069096 t; the QA gets 362.069035 t. The 0.00006 t gap comes only from whether the corrected Opelousas truck mass is treated as the same datapoint as the Opelousas rail mass. With the BCU left at 19.339 t: 360.817899 t (script part 8, part 13).
- 9.9 Flag: 'image (44).png' confirmed; three identical copies of the Standard EF workbook (one hash); GLEC PDF page 6 reads "v3.1 edition, revised and updated (2024)." against "GLEC V3.2 2025" on the sheet; four Mangrove maps with four different hashes, all "Opelousas, LA", 3,672.1 km.
- 9.10 Fail: older Certify copy K10 2199, L10 42.9, M42 7,598.344118, N42 1,201.2, no railyard split; the 2026-10-01 copy M42 7,551.344118; M13 note "about 390.76 kg" and "78,260.76 kg"; M10 note quoted correctly; W2 AECN Truck B10 holds 2499-T; all 11 datapoints listed show "—" or lack the needed source type in the Datapoints capture.
- S.1 Flag: EAC tracker row 16: 2765.361153 / 586.8777093 / 2178.483444; certificate "2,795" TERCs (29.638847 more); September row 171.9503 with note "revise if Sept site emissions change"; workbook reductions 172.6573, 0.7070 short (script part 12).

## 5. Observations (missed by the checklist)

1. **Oil weighed before the removal period.** All four SHPX215091 full weighs are dated 2026-09-17 (11:22 to 16:25; empties by 2026-09-18 07:02), and SHPX215039 offloads 1-2 on 2026-09-18. Both dates fall before the Certify period start of 2026-09-19 and inside W3's Ops week (2026-09-11 to 2026-09-18). Under the guidance sentence quoted in 2.2 ("recognised in the week in which the railcar's final offload is completed"), SHPX215091's close, including its 223.91168 kg loss, belongs to W3. The checklist calls these railcars "inside the window". Ask Ops to state the booking basis (delivery week or injection week) in the guidance.
2. **Late-September Baton Rouge loads.** The Rail Logix Lessons Learned record further loads after SHPX215053's four full weighs (2026-09-22 and 09-23): "9/24 Thursday ... Left yard at 0415 arrived at raillogix at 0645" and "9/25 Friday ... Started loading at 0840 ... Starting on the 2nd load at 0915 ... Last load is always light". None are in W4. COBB books SHPX215061 (Loads tab delivery date 2026-09-22), SHPX215067 and SHPX215073 in INJ-10-2026-W1 (completion 2026-10-02). The guidance says "Every other railcar in this Reporting Period was received at Opelousas". The September/October cut-off for oil moved on 24-25 September is undocumented, and the guidance sentence may be wrong.
3. **Empty return counted twice on the truck embodied leg.** The Standard EF sheet's tanker factor already includes empty running: Truck and Trailer EE 2026 B15 "Tanker Truck Total Embodied Emissions (MTCO2e)/Mile w/ Deadhead" 0.0002375605888 = 0.0001652020785 × 1.438 (B14 "2022 Deadhead Average % of Overall Mileage --Tanker Truck" 0.438). The guidance then counts the leg as a round trip ("The tanker leg is counted as a round trip, consistent with the treatment of the Opelousas leg"). On 1,946 mi that is 0.462293 t against 0.321483 t without the uplift: 0.140810 t charged twice, in the safe direction (script part 9). It is a standing method, so worth settling for all weeks.
4. **Railcar embodied basis.** The railcar factor is per mile travelled with no empty-return uplift: "Typical Annual Mileage (Cambridge Systematics)" 60,000, "Expected Lifetime Mileage" 2,100,000, "Embodied Emissions per Mile Traveled (MTCO2e)" 3.113066508e-05. A round trip (W4) therefore fits the factor; one way (W2 and W3, whose M formulas carry no ×2) charges only half the miles. When fixing 3.5, settle the basis rather than reverting W4 to one way.
5. **Acid number context for 8.1.** In the same SGS order (5506143), the W4 Kerry sample also reads 154 mg KOH/g "#" next to the AECN 156 "#", while W4 QOWV reads 36. A jump in two different oils in one lab run points to the run rather than the AECN oil.
6. **Site-component uncertainty inputs (for the site-emissions QA).** 'Argon Electricity Usage' (2,602.43355 kWh) carries no ±, while the knowledge base lists "Electricity → Grid Electricity Usage: 0.02 × Measured Value (2%)". Adding it raises this removal's discount by 0.0001189 t (script part 13). The REC-applied inputs (63,575.19 and 2,602.43 kWh) also carry none, while the knowledge base lists "Procured Power Electricity Usage: 0.02 × Measured Value (2%)". 7.3 and 7a.3 call the discount correct without noting either gap.
7. **Stale expected value in the rule files.** The knowledge base and `checklist_structure.md` give the AECN process factor as 0.10402; the Standard EF sheet's H2 2026 value is 0.1371171258. The QA used the sheet, correctly. The rule files need updating.
8. **AECN Truck tab label.** The header reads "BATCH HEADER — AECN Truck (Direct from Fort Lupton)"; AECN direct trucks come from Port-Cartier, Québec. The empty tab still carries N10:N12 = 2197 and N25 = 6591.
