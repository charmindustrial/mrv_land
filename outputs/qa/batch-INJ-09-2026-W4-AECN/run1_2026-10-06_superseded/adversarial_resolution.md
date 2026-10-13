# INJ-09-2026-W4-AECN — Gate 3 resolution

Reviewer file: adversarial_review.md (independent agent, finished 2026-10-06T19:42Z), with adversarial_review_recompute.py and adversarial_review_recompute_output.txt. Status rows at review: 62 (57 Pass/Fail/Flag + 5 N/A). Challenged 9, confirmed 53; 7 missed findings. Each point was checked against its source before the checklist changed.

## Challenged rows

| Row | Reviewer | Resolution | Checked this session |
|---|---|---|---|
| 3.1 | Flag → Fail | Accepted. Nine W4 BOLs are absent from the W4 batch folder and from the 72 Certify sources; KB rule "(3) only FLAG/FAIL if the document is absent from BOTH locations." Row rewritten as Fail. | KB line 645 (log policy.kb_document_location_rule_text); drive_folder_listing.json; certify.presence_checks.w4_new_bols |
| 7a.1 | Fail → Flag | Accepted. Missing ± on the Baton Rouge rail mass moves the discount 2.4428820922 → 2.4429028145 t (2.442586 → 2.442640 t after the other corrections), far inside 0.001 t; no misstatement risk to the net. Row kept as a finding, graded Flag. | recompute FINDING 7a.1 and CORRECTIONS B-C |
| 9.8 | Fail → Flag | Accepted. The checklist's 360.818 t left the BCU at 19.339 t, contradicting its own 9.6 (BCU follows the exact process figure). With the BCU at the corrected transport sum 20.5897707 t the evidence net is 362.069035 t, +0.001035 t against Certify (reviewer 362.069006 t on the sheet rail factor). Row now states both figures and that the four fixes must land in one edit. | recompute CORRECTIONS E (new) |
| 7.4 | Flag → send back | Accepted and done. Opened the September results workbook: Drive text index first (a connector download was corrupted in copying and discarded), then the file itself from the local Drive copy (a first local search had silently not run; rerun, it found the file; row 10 values and formulas agree with the text) and, found in the same search, the GHG Statement Report v1.7. W4 AECN row matches Certify (net 362.07, reductions 22.4390, discount 2.4429, process 63.0690). The two drafts disagree at RP level (process 384.65 vs 385.33 t; site 20.48 vs 20.55; reductions 171.95 vs 172.66; net 1,744.01 vs 1,743.96), and the report's W4 site figure 20.482 t lags Certify 20.550448 t. Re-graded Flag. | source_exports/September1-September30_Bio-Oil_GHG_Statement_Results_drive_text_2026-10-06.txt; source_exports/September_GHG_Statement_Report_v1.7_and_RailLogix_doc_drive_text_2026-10-06.txt |
| 1.4 | Evidence fix | Accepted. P9 "Full Railcar This Week?" and Q9 "Car Completes This Week?" confirmed in the live export; P13 PARTIAL with Q13 Y is correct, gap removed. Gap (1) reworded: method follows the 2026-09-29 guidance clause that the 2026-10-06 version no longer holds. Added: G46 pH note present in the 10-01 Certify copy, gone from the live sheet; row-9 headers still name Opelousas over SHPX215053's Baton Rouge figures. | log ops_notes.railcar_headers_row9, vvb_guidance.removed_since_2026_09_29, certify.ops_notes_copies |
| 1.5 | Evidence fix | Accepted. BOL_2466-R.pdf has 5 pages (mdls: 5); pages 4-5 read: TSCA dated "August 7 2026", PO Q42025 Ship To El Dorado KS. All 12 packages carry the PO. The log's earlier "3 pages" reading was wrong and is corrected. | drive_files/BOL_2466-R.pdf pages 4-5 (image read) |
| 3.7 | Evidence fix | Accepted. 2466-R's PO seller signature is blank; blank list is 8 of 12. | same |
| 8.3 | Evidence fix | Accepted. P13 sentence removed; added the removed guidance clause (quoted from the 09-29 fetch) and the same-morning weighing of W2 offload 2 (1124426248528, 09:24) and W4 offload 3 (1124426248529, 09:29). | W2 log scale_tickets.SHPX215079; W3 folder guidance fetch 2026-09-29 |
| 9.9 | Evidence fix | Accepted. Aug-07 and Sep-02 maps share a size but their SHA-256 differ (543fb81bda1c, 96ea18544055); the size sentence is replaced. | log certify.mangrove_map_hashes |

## Missed findings

| # | Finding | Where it went | Checked |
|---|---|---|---|
| M1 | Multi-week clause and "Basis for Loaded Mass" section removed from the September guidance after 2026-09-29 | 1.4, 2.2, 8.3 | 09-29 fetch contains both; 10-06 fetch contains neither (text search) |
| M2 | Both attached Ops copies show SHPX215079 loss G13 −392.76368 kg; live G13 now MAX(0, E13−F13) gives 0; statement report says "no negative loss is applied" | 8.2, 9.10 | both copies read with openpyxl; live formula read |
| M3 | Older copy M13 gives "about 390.76 kg" / "78,260.76 kg"; M10 "no 2499-R, unresolved" answered by W2's BOL 2499-T | 9.10 | copy M10/M13 text read; W2 log carries 2499-T |
| M4 | SHPX215079 rail miles 3,200.34412 across W2 (one way) and W4 (round trip) | 3.5 | recompute section 11 |
| M5 | Rail embodied on lost oil counted twice, 0.000557 t (conservative) | 8.2 | recompute section 11 |
| M6 | Net is insensitive to the transport errors while the BCU tracks the process sum; the material effect is a 1.2507707 t larger BCU draw | 7.2, 9.6, 9.8, S.1 | recompute CORRECTIONS E |
| M7 | Acid number 156 vs 61 (W2) and 47 (W3) | moved from 4.3 to 8.1 | W2 log lab_results.acid_number_mgKOHg 61; W3 47 |

## Further reads prompted by the review

- Second Drive search pass for a SOPOR–Baton Rouge rail distance record: none. The statement report v1.7 states "Its rail leg (2,152 mi)" without a source; added to 3.5.
- EAC tracker September usage 171.9503 t matches the statement report (171.95) but is 0.7070 t below the results workbook's 172.6573 t; added to S.1.

## Result

Checklist rebuilt (same file name): Pass 30 / Fail 9 / Flag 18 / N/A 5 (62 rows). Recompute exit 0, 0 arithmetic mismatches, every FINDING routed to a Fail or Flag row. Citation audit 57 rows, 0 failures. Attachment gate: 19 gaps, all named in Fail row 9.10.
