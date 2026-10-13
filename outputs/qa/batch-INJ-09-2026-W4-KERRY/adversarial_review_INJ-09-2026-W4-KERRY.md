# Adversarial review — INJ-09-2026-W4-KERRY

- **Batch:** INJ-09-2026-W4-KERRY · Kerry · tanker (one CAT Scale full + empty pair) · Basco 6 · Certify removal rmv_1M3T2J3V51S0NCHH
- **Checklist reviewed:** `Kerry_Batch_INJ-09-2026-W4_QA_Checklist.xlsx`, 25 rows + 7 sidebar notes
- **Reviewer:** independent adversarial reviewer (did not build the checklist), 2026-10-06
- **Method:** saved files on disk; no website or browser opened, no sign-in. Every image, PDF and workbook named below was opened directly. Arithmetic was redone from the ticket images and source workbooks, separately from `recompute_kerry.py`.
- **Quotation marks** mark text copied from text sources (workbooks, Certify text captures, VVB guidance text, knowledge base, skill files, earlier checklists). Values read from the ticket images, the route image and the PDFs (CoA, retirement certificate) are stated without quotation marks, with their location.

## Result

**32 entries: 27 upheld, 5 challenged.**

| Row | Current | Proposed | Why |
|---|---|---|---|
| 1.5 | Pass | **Flag** | Kerry solids constant 0.00071 is below the AECN constant 0.00196 on the same sheet. The July VVB guidance says Kerry is "materially higher". A cell note on record reports a lab figure 10x higher. Both earlier Kerry tanker checklists recorded the mismatch; this one drops it. |
| 1.7 | Fail | Fail (stands) | Fail is supported; no documented method contradicts it. Four evidence corrections needed: COBB quantity sits on both WILA003 and WILA004; a Certify claim was never read; the 14-day ticket-date rule goes unnamed; the transport and BCU knock-on goes unstated. |
| 2A.6 | Pass | Pass (stands) | Cites the COBB WILA004 quantity as support while 1.7 cites the same number on WILA003 as evidence against. |
| 3.6 | Pass | Pass (stands) | Paraphrase of the July guidance presented as what it "states". Replace with the verbatim text. |
| S.4 | sidebar | sidebar (stands) | Cell addresses point at header labels, not at the cells holding the values. |

Proposed counts after fixes: **Pass 23 | Fail 1 | Flag 1 | N/A 0.**

## Independent recompute

| Quantity | Working | Result | Certify |
|---|---|---|---|
| Full ticket axles | 12,280 + 31,920 = 44,200; 44,200 + 29,800 = 74,000 | 74,000 lb | — |
| Empty ticket axles | 11,780 + 13,840 = 25,620; 25,620 + 8,680 = 34,300 | 34,300 lb | — |
| Ticket net | 74,000 − 34,300 = 39,700 lb; 39,700 × 0.453592 = 18,007.6024 kg | 18,007.6024 kg | 18.0076 t |
| Filtration loss | 18,007.6024 × 0.00071 = 12.7854 kg | 12.7854 kg | — |
| MOBI | 18,007.6024 − 12.7854 = 17,994.817 kg | 17,994.817 kg | 17,994.817 kg |
| Sequestration | 17.994817 × 0.579 = 10.418999; 10.418999 × 3.667 = 38.20647 t | 38.20647 t | 38.206 t |
| Transport process | 18.0076024 × 1,090 = 19,628.2866 t·mi; 19,628.2866 × 0.0001143 = 2.24351 t | 2.24351 t | 2.244 t |
| Transport embodied | 1,090 × 0.0002375605888 = 0.25894 t | 0.25894 t | 0.259 t |
| Activities | 2.24351 + 0.25894 = 2.50245 t | 2.50245 t | 2.502 t |
| BCU vs process | 2,243.513 − 2,243.51 = 0.003 kg below the emission | not over | 2,243.51 kg |
| Uncertainty discount | 72.57 / 17,994.817 = 0.0040328; square root of (0.004 squared plus 0.0040328 squared) is 0.0056801; 38.20647 × 0.0056801 = 0.21702 t. Process mass term: 72.57 / 18,007.6024 = 0.0040300; 2.24351 × 0.0040300 = 0.0090413 t. Square root of (0.21702 squared plus 0.0090413 squared) is 0.21721 t | 0.2172 t | 217 kg |
| Net | 38.20647 + 2.24351 = 40.44998; 40.44998 − 2.50245 = 37.94753; 37.94753 − 0.217 = 37.73053 t | 37.7305 t | 37.730 t |

## Row-by-row

### 1.1 — Upheld
- **Opened:** Certify-attached CoA PDF (`source_exports/Certify_attached_COA_src_1M3VZ8S8W1S013HS.pdf`) page 1; `certify_modal_injection_sequestration.txt`; W4 Ops Notes live export, Summary tab.
- **Showed:** CoA page 1: certificate SR26-05719.001, client ID 9-2026-W4-KERRY, sampled 25-Sep-2026 07:00, carbon 57.9 % (m/m) by ASTM D5291 Method C. Modal: carbon 57.9 with ±0.2316 %. Summary C19 'SR26-05719.001', D19 `=DATE(2026,9,25)`, E19 0.579.

### 1.2 — Upheld
- **Opened:** `certify_sources_tab.txt` and `.yml`; `certify_calculation_view.txt`; sequestration modal text; file fingerprints (sha256) of the Certify and Drive CoA copies.
- **Showed:** Sources tab links "SR26-05719 W4 Kerry AECN QOWV COA.pdf" to "Carbon Content of Bio-oil Injected (per injection)". The Ops Notes source links "Allocated Kerry Oil Gross Mass" plus "+ 2 more". The modal shows "2 sources" on carbon. Both CoA copies fingerprint 276ccd65301889cf…, identical files.

### 1.3 — Upheld
- **Opened:** sequestration modal text; W4 Ops Notes Summary tab; knowledge base Section 7a.
- **Showed:** 57.9 × 0.004 = 0.2316; modal "±0.2316". Summary G19 `=E19*H19` → 0.002316. Knowledge base: "Injection Sequestration → Carbon Content: 0.004 × Measured Value (0.4%)".

### 1.4 — Upheld
- **Opened:** sequestration modal; `certify_datapoints_tab.txt`; W4 Ops Notes Kerry and Summary tabs.
- **Showed:** modal mass of product 17,994.817 kg with "±72.57". Datapoints "17.995 t". Kerry C18 `=A18-B18` → 17994.817; Summary G11 `=Kerry!C18` → 17994.817; Summary B19 `=G11`.

### 1.5 — Challenged (Pass → Flag)
- **Opened:** W4 Ops Notes live export and the Certify-attached copy (src_1M3W1NWED1S0K0MP), Kerry and AECN Rail tab constants, with cell notes; `CAR-474_Solids_Loading_Kerry_source_0.071pct.xlsx`; July VVB guidance text; Aug W5 Ops Notes (`w3_kerry_cross_check/INJ-08-2026-W5_Ops_Notes_live_20261006T1831Z.xlsx`), Kerry tab O5 and its cell note; INJ-08-2026-W3-KERRY and INJ-07-2026-W4-KERRY checklists.
- **Showed:** the arithmetic ties: Kerry E10 `=C10-D10` 39,700; F10 `=E10*M4` 18,007.6024; B18 `=A18*$M$5` 12.7853977; C18 `=A18-B18` 17,994.817; Summary E11 0.0. Kerry M5 0.00071 matches CAR-474 'MANITOWOC CALCINER PHASE' 0.071 (SGS). Kerry-tab values match between the live and Certify-attached copies; C10 and D10 differ in form (plain number vs hyperlinked number), same values.
- The constant conflicts with the governing explanation and with an open note on record. See Challenge 1.

### 1.6 — Upheld
- **Opened:** both W4 ticket images; sequestration modal; batch-qa-kerry SKILL.md, Uncertainty Reference.
- **Showed:** both tickets are CAT Scale (Certified Automated Truck Scale) tickets: scale 1895 at Wilson Township WI, scale 3199 at Lake Village AR. Modal "±72.57". SKILL.md: "Tanker mode (commercial truck scale): one discrete weighing event (the full + empty ticket pair). Uncertainty = **72.57 kg** on Mass of Product and on Mass of Load."

### 1.7 — Challenged (Fail upheld; evidence needs correcting)
- **Opened:** both W4 ticket images; W2 tickets (`Sept_W2_Full_Scale_Ticket_Kerry.jpg`, `Sept-W2-Empty-Scale-Ticket-Kerry.pdf`); W3 tickets (`Sept-W3-Full-Scale-Ticket-Kerry.pdf`, `Sept-W3-Empty-Scale-Ticket-Kerry.pdf`); Kerry and Summary tabs of the W2, W3 and W4 Ops Notes exports (values, formulas, cell notes); `COBB_live_calciner_rows_20261006T1842Z.txt` and the COBB export, 'Basco Injection -- COBB' tab; `Removal_Batch_CrossRef_Sep2026_live_20261006T1834Z.xlsx`; July, August and September VVB guidance texts, each read in full; knowledge base Sections 10 and 11; Certify Sources tab text.
- **Showed:** each dated fact in parts (a) to (e) checks against the files.
  - (a) Full ticket: 9-09-26, 09:27, Wilson Township WI, 74,000 lb. Empty ticket: 9-11-26, 13:20, Lake Village AR, 34,300 lb. Tractor 07 and trailer 1013 on both. W4 Kerry A10 is 2026-09-25, 16 days after the full ticket. COBB `injection_completion_date` 2026-09-23 is 14 days after it.
  - (b) COBB W4 row: 'INJ-09-2026-W4_calciner', 'WILA004_offload_1', `order_line_completed_on` 2026-09-24 18:04:36.
  - (c) COBB W3 row: 'WILA003_offload_1', 2026-09-12 14:17:56, `offloaded_quantity_kg` 18007.6024. W3 Ops Notes Kerry: B10 'WILA003', C10 76680, D10 34420, C17 → 19155.18807. W3 tickets: full 9-16-26 09:59 Wilson Township WI, 76,680 lb; empty 9-18-26 22:06 Lake Village AR, 34,420 lb.
  - (d) Both July phrases quoted in the row appear verbatim in the July text. The August and September texts have no Kerry section, so the negative claim holds. Sensitivity: 76,680 − 34,420 = 42,260 lb; 42,260 × 0.453592 = 19,168.7979 kg; 19,168.7979 × 0.00071 = 13.6098 kg; 19,168.7979 − 13.6098 = 19,155.1881 kg; 19.1551881 × 0.579 = 11.0908539; 11.0908539 × 3.667 = 40.67016 t; 40.67016 − 38.20647 = 2.46369 t; 2.46369 / 38.20647 = 0.0645; 0.0645 × 100 = 6.45 %. Knowledge base Section 11, Isometric Standard v2.0, lists the materiality threshold as "5% (unchanged)".
  - (e) W4 Kerry M5 has no cell note or link in either the live or the Certify-attached copy. CAR-474 is not among the 8 Certify sources.
- **No documented method contradicts the Fail.** The July tank-hold text ("the associated removal is not considered complete until the tank is empty") allows a load to wait in the tank. No text in the July, August or September guidance explains a later truck being credited before an earlier one. The W3 and W4 Kerry tabs carry one cell note each, both on pH (W3 D17, W4 D18).
- Corrections needed: see Challenge 2.

### 2A.1 — Upheld
- **Opened:** `certify_modal_transport_process.txt`; Standard EFs live export, 2026 tab; both W4 tickets; July guidance; INJ-08-2026-W3-KERRY checklist.
- **Showed:** modal EF 0.1143 kgCO₂e/(t⋅mi), labelled "Emissions Factor - Truck Transport Fuel Use (Well to Wheel) - Tanker Truck". Standard EFs live export, 2026 tab, row 6: 'Truck Transport Fuel Use (Well to Wheel) -- Tanker Truck', 0.0001143, 'GLEC V3.2 2025'. Both tickets show commodity TANKER, trailer 1013. July guidance: "Kerry calciner oil is delivered to the Basco injection site in bulk tanker trailers rather than in IBC totes". This departs from checklist_structure.md 8.2 ("Kerry uses **flatbed truck** (totes or tanker), NOT tanker truck"). The vehicle evidence supports the departure, and the QA logged the cross-batch question in S.6. INJ-08-2026-W3-KERRY 2A.1 used the same factor: "'Truck Transport Fuel Use (Well to Wheel) -- Tanker Truck' = 0.0001143".

### 2A.2 — Upheld
- **Opened:** `Certify_attached_StdEFs_src_1KWZ2NVQM1S08AWN.xlsx`, 2026 tab.
- **Showed:** row 5 'Truck Transport Fuel Use (Well to Wheel) -- Tanker Truck' 0.0001143. The Sources tab links this file to the process EF datapoint.

### 2A.3 — Upheld
- **Opened:** `Certify_attached_src_1KT1W9XED1S08J0H_Kerry_to_Basco_Distance.png`; process modal; W4 full ticket.
- **Showed:** route image runs from 4343 Expo Dr, Manitowoc WI 54220 to 4687 LA-115, St Landry LA 71367, with three options: 1,059, 1,071 and 1,090 miles; the 1,090-mile option is via I-55 S. Modal distance 1,090 mi, the longest. The full ticket was weighed on I-43 at Wilson Township WI.

### 2A.4 — Upheld
- **Opened:** Sources tab text; the route image.
- **Showed:** "Kerry to Basco Distance.png" is linked to "Route Distance Kerry to Basco". The image's longest option is 1,090 miles.

### 2A.5 — Upheld
- **Opened:** process modal; W4 Ops Notes Summary and Kerry tabs.
- **Showed:** modal mass of load "Allocated Kerry Oil Gross Mass", 18.0076 t with "±0.07257". Summary B11 `=Kerry!A18` → 18007.6024. Kerry A18 `=SUMIFS(F10:F15,B10:B15,"<>")` → 18007.6024.

### 2A.6 — Challenged (Pass stands; one sentence to fix)
- **Opened:** both W4 ticket images; W4 Kerry tab; COBB export, 'Basco Injection -- COBB' tab.
- **Showed:** 39,700 × 0.453592 = 18,007.6024 kg; tractor 07 and trailer 1013 on both tickets. But the closing sentence ("COBB WILA004 offloaded_quantity_kg carries 18007.6024 as well.") offers COBB as corroboration. The same number sits on the WILA003 row (COBB export rows 1786 for W3 and 1790 for W4), and 1.7(c) uses it as evidence the pair is WILA003's. See Challenge 3.

### 2A.7 — Upheld
- **Opened:** process modal.
- **Showed:** "±0.07257" t, which is 72.57 kg for one CAT weighing (SKILL.md tanker rule quoted under 1.6).

### 2B.1 — Upheld
- **Opened:** `certify_modal_transport_embodied.txt`; Standard EFs live export, '2026' and 'Truck and Trailer EE 2026' tabs (values and formulas).
- **Showed:** modal EF 0.23756 kgCO₂e/mi. 2026 tab row 11: 0.0002375605888 MT CO2e/mi, with D11 `='Truck and Trailer EE 2026'!B17`. On that tab, B15 `=B12*(1+B14)` with deadhead B14 0.438 gives 0.0002375605888. The Datapoints tab shows "0.1476 kgCO₂e/km": 0.2375605888 / 1.60934 = 0.147614. Per mile, not per ton-mile.

### 2B.2 — Upheld
- **Opened:** `Certify_attached_StdEFs_src_1KVJRSYT91S09G2E.xlsx`.
- **Showed:** same fingerprint (d49871d1…) as src_1KWZ2NVQM1S08AWN. 2026 tab row 10 'Vehicle Embodied Emissions --Tanker Truck' 0.0002375605888.

### 2B.3 — Upheld
- **Opened:** embodied modal.
- **Showed:** distance datapoint Route Distance Kerry to Basco at 1,090 mi with one source, the same datapoint the process component uses.

### 2B.4 — Upheld
- **Opened:** Sources tab text; route image.
- **Showed:** same source and image as 2A.4.

### 2C.1 — Upheld
- **Opened:** `certify_modal_bcu.txt`; `Certify_attached_src_1M1MFJPW11S08KY2_Charm-RetirementCertificate-RD-EACs-20251218.pdf`; Components capture in `certify_initial_snapshot.yml`.
- **Showed:** BCU constant reduction 2,243.51 kgCO₂e. Recomputed process emission 2,243.513 kg; 2,243.513 − 2,243.51 = 0.003 kg, so the BCU sits below the emission and never over. Certificate PDF: on behalf of Charm Industrial, Inc; retired Dec 18, 2025; vintage 2024; Renewable Diesel TERCS; 2,795 retired; verification body Turner, Mason & Company. Embodied carries no BCU; the removal has one BCU component.

### 3.1 — Upheld
- **Opened:** CoA page 1.
- **Showed:** density at 15 °C 1.201 g/cm³ by ASTM D4052, above 1.01.

### 3.2 — Upheld
- **Opened:** CoA pages 1 and 2; INJ-07-2026-W4-KERRY checklist.
- **Showed:** hydrogen 6.4 % (m/m) by ASTM D5291 Method C; the AECN sample (SR26-05719.002) reads 6.6. No Kerry range exists, so the "within expected range" half cannot be tested, and the note says so. INJ-07-2026-W4-KERRY 3.2 was passed on the same basis: "No range test is applied: Kerry has no established baseline dataset".

### 3.3 — Upheld
- **Opened:** CoA page 1.
- **Showed:** nitrogen <0.75 % (m/m) by ASTM D5291 Method C. Optional: add a sentence matching 3.2 stating that no Kerry range exists and the range half was not tested.

### 3.4 — Upheld
- **Opened:** CoA page 1.
- **Showed:** kinematic viscosity at 40 °C 545.2 cSt by ASTM D445.

### 3.5 — Upheld
- **Opened:** CoA page 1.
- **Showed:** acid number 154 mg KOH/g by ASTM D664 Method A, marked #; carbon and hydrogen are also marked #. The page 1 footnote defines # as a result outside the test method limits and/or the analytical range used in the method precision study.

### 3.6 — Challenged (Pass stands; citation wording)
- **Opened:** W4 Ops Notes Kerry tab with cell notes; COBB export; July guidance text.
- **Showed:** Kerry D18 2.97, cell note 'Wellhead pH = weekly median of Ignition PH-1041, gated to StateRun=1; provided by G. Lutz 2026-09-30.'; G10 `=$D$18`; M6 '2.0 - 4.0'. COBB `injection_ph` 2.97 on 'Basco Injection -- COBB' rows 1790 and 2718, blank on row 3681. The note's last sentence presents a paraphrase as what the July guidance "states". See Challenge 4.

### S.1 — Upheld
- **Opened:** `certify_initial_snapshot.yml` (Components tab); W4 Summary tab.
- **Showed:** "4 components": Injection sequestration 38.206; Kerry to Basco Tanker Truck Transport Process Emissions 2.244; Kerry to Basco Tanker Truck Transport Embodied Emissions 0.259; BCUs 2.244. No production, biomass or counterfactual component. Summary E11 0.0.

### S.2 — Upheld
- **Opened:** W2 tickets; W2, W3, Aug W5, Sep W1 and Oct W1 Ops Notes exports; COBB rows.
- **Showed:** W2 full ticket 8-31-26, Wilson Township WI, 75,520 lb; W2 empty ticket 9-02-26, Port Barre LA, 35,320 lb. W2 Kerry A10 2026-09-09. COBB WILA002 quantity 17000. W3 net 19168.79792. The Aug W5 and Sep W1 Kerry tabs hold no ledger rows; Oct W1 has no Kerry tab. The W4 pair appears in no other week.

### S.3 — Upheld
- **Opened:** CoA pages 1 and 2; W4 tickets.
- **Showed:** location FORT LUPTON, CO on both .001 and .002; SGS order 5506143; both W4 tickets read DELIVERY SITE: CHARM.

### S.4 — Challenged (cell addresses)
- **Opened:** W4 Kerry tab.
- **Showed:** the label points are right, but C9, F9, A17 and C17 are header cells. The values sit in C10 (74000), F10 (18007.6024), A18 (18007.6024) and C18 (17994.817). I10:K10 are blank, as stated. See Challenge 5.

### S.5 — Upheld
- **Opened:** `batch_folder_listing.txt`; Sources tab text (8 sources); COBB rows; INJ-07-2026-W4-KERRY and INJ-08-2026-W3-KERRY checklists.
- **Showed:** no Bill of Lading in the Drive listing or the Certify sources. COBB `BOL_number` 'WILA004', `origin_quantity_kg` 20000. The 20,000 kg cannot be the loaded oil: 20,000 × 2.20462 = 44,092 lb of oil, and 34,300 + 44,092 = 78,392 lb would be needed on the full ticket (ignoring fuel), against 74,000 lb printed. Sidebar placement matches both earlier Kerry tanker checklists, which recorded the missing BOL as an open question. Optional addition: the skill's conservative test MIN(ticket net, BOL oil-only mass) has no second figure.

### S.6 — Upheld
- **Opened:** Standard EFs live export, 2026 tab rows 6, 7, 11 and 12; INJ-07-2026-W4-KERRY and INJ-08-2026-W3-KERRY checklists.
- **Showed:** INJ-07-2026-W4-KERRY used 'Flatbed Truck' 0.0001384 for process and 'Non-Tanker Truck' 0.0001927908256 for embodied. Flatbed set on this removal: 19,628.2866 × 0.0001384 = 2.71655 t; 2.71655 − 2.24351 = 0.47304 t more process. Embodied: 1,090 × 0.0001927908256 = 0.21014 t; 0.25894 − 0.21014 = 0.04880 t less. Matches the note. Optional addition: INJ-08-2026-W3-KERRY used the tanker factors, so the three Kerry tanker batches checked split one flatbed (July) to two tanker (August, this batch).

### S.7 — Upheld
- **Opened:** COBB export, 'Basco Injection -- COBB' tab.
- **Showed:** 'KC_0001' to 'KC_0004' under 'K-001' and 'KC_0006' to 'KC_0008' under 'K-002' (rows 52–55 and 137–139, repeated in later blocks). The W4 calciner row repeats at rows 1790, 2718 and 3681, with `injection_ph` blank on 3681.

## Challenges and proposed fixes

**Challenge 1 — 1.5: Pass → Flag.**
- *Evidence.* July VVB guidance: "Kerry calciner oil measures materially higher in solids than AECN oil, so applying the AECN value to a Kerry load would understate the filtered mass and correspondingly overstate the mass credited as injected. Using Kerry’s own measured solids content is both the feedstock-accurate and the conservative treatment." On the same W4 Ops Notes, the AECN constant (AECN Rail tab, N7 'Filtration Solids Content', O7) is 0.00196 against Kerry M5 0.00071: 0.00196 / 0.00071 = 2.76 times higher. The Kerry deduction is therefore smaller than the AECN value would give, the opposite of what the guidance tells the verifier.
- The Aug W5 Ops Notes Kerry O5 note records an unresolved lab question: "DISCREPANCY TO CONFIRM WITH THE LAB: the Slack announcement of CAR-474 (steven.rowland, #chemical-analysis-notifs 2026-05-29 10:42 MDT) quotes 'Kerry Manitowoc Calciner Phase Separated Tar - 0.71% solids'" … "i.e. 10x this value for Kerry", and "Confirm with Steven Rowland before this constant is ever changed." A 0.71 % value would fit the guidance's "materially higher".
- INJ-08-2026-W3-KERRY S.4 recorded the same mismatch: "the guidance's stated rationale doesn't match the numbers" … "Worth flagging to Garrett as a documentation-consistency item". INJ-07-2026-W4-KERRY S.6 also recorded it. This checklist drops it.
- *Effect at 0.71 %:* 18,007.6024 × 0.0071 = 127.854 kg filtration; 18,007.6024 − 127.854 = 17,879.748 kg MOBI; 17.879748 × 0.579 = 10.352374; 10.352374 × 3.667 = 37.96216 t sequestration; 38.20647 − 37.96216 = 0.24431 t lower; 0.24431 / 38.20647 = 0.0063945; 0.0063945 × 100 = 0.64 %.
- *Effect at the AECN constant:* 18,007.6024 × 0.00196 = 35.2949 kg; 18,007.6024 − 35.2949 = 17,972.3075 kg; 17.9723075 × 0.579 = 10.405966; 10.405966 × 3.667 = 38.15868 t; 38.20647 − 38.15868 = 0.04779 t; 0.04779 / 38.20647 = 0.00125; 0.00125 × 100 = 0.125 %.
- Both effects sit below the 5 % materiality threshold, so Flag, not Fail. The direction is over-crediting if the lab confirms 0.71 %.
- *Fix.* Set 1.5 to Flag. Keep the arithmetic sentences, then add the following.

  Proposed wording — Flag on the filtration constant: M5 0.00071 matches CAR-474 'MANITOWOC CALCINER PHASE' 0.071 (SGS), but the July 2026 VVB guidance says Kerry calciner oil measures materially higher in solids than AECN oil, while this sheet's AECN constant (AECN Rail O7) is 0.00196. The Aug W5 Ops Notes Kerry O5 note records an open lab question ('0.71% solids', '10x this value for Kerry'). At 0.71 % (0.0071), sequestration would be 37.96216 t, 0.24431 t below the reported 38.20647 t (arithmetic above).

  Cite the W5 file and the July guidance in column E. Raise it with Garrett as a lab confirmation (Steven Rowland, CAR-474).

**Challenge 2 — 1.7: Fail stands; correct the evidence.**
- (a) **The COBB quantity does not tell the loads apart.** Part (c) says COBB's WILA003 figure of 18,007.6024 kg "is this pair's net". The COBB export ('Basco Injection -- COBB' rows 1786 and 1790) carries 18007.6024 on both WILA003 and WILA004, so the quantity cannot show which load is which; the timing does. *Fix:* state that both rows carry the same figure, and add the timing pattern. COBB WILA002 `order_line_completed_on` 2026-09-02 19:41:31 falls on the W2 empty ticket date (9-02-26), so the completion timestamp follows the post-offload empty weighing. On that pattern, WILA003's 2026-09-12 14:17:56 fits this pair's empty ticket (9-11-26), not the empty the W3 Ops Notes credits (9-18-26).
- (b) **A claim about Certify that was not read.** The row says "the W3 removal (rmv_1M3SWNGK51S0GH00) credits WILA003 with a later pair". That describes the W3 Certify removal, but the QA read the W3 Ops Notes and the cross-reference sheet, not the W3 removal. *Fix:* say the W3 Ops Notes, the batch record that the Removal–Batch Cross-Reference maps to removal rmv_1M3SWNGK51S0GH00, credits WILA003 with the later pair. Alternatively, read the W3 removal's Mass of Injectant live (skipped here because it needs sign-in).
- (c) **The ticket-date rule goes unnamed.** The knowledge base checklist reads "For each pair: dates within 2 weeks of injection [VR Sec 3.5]". checklist_structure.md (tanker 2.5) reads "Date on tickets within 14 days of Ops Notes injection date". INJ-07-2026-W4-KERRY 1.7 applied it: "Both ticket dates fall within 14 days of the 25 Jul injection". *Fix:* state that the full ticket is 16 days before the Ops Notes row date (outside 14 days) and 14 days before COBB injection completion (at the limit). Note that the July tank-hold text is the documented passage that could allow such a lag, and that the September guidance does not restate it.
- (d) **The knock-on goes unstated.** Under the 16–18 Sep pair: 19.1687979 × 1,090 = 20,893.9897 t·mi; 20,893.9897 × 0.0001143 = 2.38818 t process; 2.38818 − 2.24351 = 0.14467 t more process, and the BCU would need the same 0.14467 t more. Embodied is unchanged. *Fix:* add these figures to 1.7, and add a see-1.7 cross-reference to 2A.5, 2A.6, 2A.7 and 2C.1, which rest on the same ticket pair.
- (e) **Strengthen part (e).** The Aug W5 Kerry O5 carried the citation the July guidance describes ("Cell is hyperlinked to the test", plus the CAR-474 source note). The W2, W3 and W4 tanker tabs each hold M5 as a plain 0.00071 with no note or link, so the citation was lost when the tab changed to the tanker layout.

**Challenge 3 — 2A.6: Pass stands; fix one sentence.** Replace "COBB WILA004 offloaded_quantity_kg carries 18007.6024 as well." with the following.

Proposed wording — COBB carries 18,007.6024 kg on both the WILA003 and WILA004 rows, so it does not confirm which load this is (see 1.7).

`recompute_kerry.py` has the same split: its output counts "Ticket net vs COBB WILA004 quantity" as OK while a 1.7 FINDING line cites "COBB carries 18,007.6024 kg on WILA003, the same figure as this pair's net".

**Challenge 4 — 3.6: Pass stands; quote, don't paraphrase.** Replace "The July 2026 VVB guidance states the Kerry pH is the shared AECN-injection value." with the July 2026 VVB guidance text: "However, this means that we do not have an independent pH value that is specific to Kerry. Rather, the pH measured over the course of the month’s AECN injections is net of Kerry oil as well."

**Challenge 5 — S.4: fix cell addresses.** Rewrite as follows.

Proposed wording — Header C9 'Gross Mass (lb) — transport' sits over C10, 74,000 lb, the full-vehicle ticket weight rather than the oil transported. Header F9 'Net Injected (kg) — MOBI' sits over F10, and header A17 'Σ Net Injected (kg)' sits over A18, both 18,007.6024 kg pre-filtration, while header C17 'MOBI (kg)' sits over C18, 17,994.817 kg, the figure in Certify.

The sidebar placement can stay; INJ-08-2026-W3-KERRY handled a mislabelled Kerry tab the same way (its S.3).

## Observations (not checklist rows; for Max to weigh)

1. **The W3 carbon sample predates the arrival of W3's credited truck.** W3 Ops Notes Summary C19 'SR26-05599.003', D19 `=DATE(2026,9,16)`. The truck the W3 Ops Notes credits was weighed full at Wilson Township WI at 09:59 on 9-16-26. If W3 samples are drawn at Basco, that sample came from oil already in the tank, such as this W4 pair (empty ticket 9-11-26), which supports 1.7. *Caveat:* sampling location is not established by the files. The W4 CoA gives location FORT LUPTON, CO, and the W3 CoA was not saved.
2. **Drive upload date of the W4 empty ticket.** `batch_folder_listing.txt` records the W4 empty ticket as "created 2026-09-14T19:13:59Z", two days before the W3-credited truck's full weighing, and the W4 'Kerry Oil/' folder as "created 2026-09-30T17:02:37Z". The date comes from Drive's file record, not from the ticket. It is consistent with 1.7.
3. **COBB W4 row is out of order internally.** `order_line_completed_on` 2026-09-24 18:04:36 falls after `injection_completion_date` 2026-09-23. It could be added to 1.7(b).
4. **Uncertainty convention and the lab's #.** Carbon 57.9 % carries the # mark (definition under 3.5). Row 1.3 applies the knowledge base's 0.4 % convention. INJ-07-2026-W4-KERRY recorded the same # in its sidebar (S.4). Not a challenge.
5. **Discount and net reproduce.** See the recompute table. The 25-row Kerry checklist has no row for either; no change needed.

## Skipped (needs a live system or sign-in)

- **W3 Certify removal rmv_1M3SWNGK51S0GH00:** its Mass of Injectant and ticket sources were not read, so what the W3 removal credits is unconfirmed (Challenge 2b).
- **The Slack message cited in the Aug W5 O5 note** (steven.rowland, #chemical-analysis-notifs, 2026-05-29): not opened, per instruction. The 0.71% figure is quoted from the cell note.
- **Live re-reads after the QA's export times (18:26Z to 18:42Z):** W4 Ops Notes (for any note added to M5), COBB and the Drive folder. All checks used the saved exports.
- **CAR-474 original lab report:** the saved CAR-474 file is the summary workbook, which carries no date. The 2026-05-28 measurement date comes from the W5 cell note.
