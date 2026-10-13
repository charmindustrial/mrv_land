NULIFE GreenTech, Ontario Avenue Bio-Oil Sequestration (prj_1JQEQKCF91S06HAJ) — raw files, 2026-09-14

Files in this folder
- nulife_pdd.pdf — PDD, 87 pages (pdfinfo), registry row "30 Sep 2025 | PDD", URL .../pjd_1K6DV5H3Z1S069JC/pdd.pdf
- nulife_ghg_2026-08-26.pdf — GHG Statement Report, 12 pages, registry row "26 Aug 2026 | GHG Statement Report", URL .../pjd_1M0ZJNP5H1S0JYG1/ghg_statement_report.pdf
- nulife_verification_2026-08-26.pdf — Verification Report, 28 pages, registry row "26 Aug 2026 | Verification Report", URL .../pjd_1M0ZJPF4D1S01HYN/verification_report.pdf
- rmv_1M0B59RM61S0BW9G_calc_and_datapoints_2026-09-14.txt — verbatim innerText captures of the removal's Calculation view, Removal method and Datapoints tabs (browser, read-only)

Why there is no machine-extracted text file for the three PDFs
All three PDFs were read in full, page by page, with the Read tool (which renders each page). A machine text dump (needed only for a computed word count) was attempted four ways and none produced text:
1. Bash pdftotext — blocked by the workspace hook doc_extraction_guard.sh ("pdftotext is blocked. Open PDFs using the Read tool..."). Python PDF libraries are blocked by the same hook. Not worked around.
2. Playwright (headless) navigating to the PDD URL — snapshot file came back 0 bytes (headless Chromium does not render the PDF).
3. pdf-viewer MCP display_pdf + get_text — twice: "Viewer never connected ... The iframe likely failed to mount" (no interactive viewer in this session).
4. Microsoft Word (sanctioned reader) opening the PDF — Word raised a macOS "Grant File Access" dialog for the nulife_pdfs folder; granting file-system permissions on Max's machine was not appropriate, so the dialog was cancelled and the stray pdd.pdf document closed without saving. Max's own open Word document was left untouched.
The Google Drive connector's upload tool needs the whole file as base64 inside the call (1.2 MB PDF -> ~1.6 MB argument), which is not feasible.
Consequence: page counts are exact; word counts for the peer documents are NOT computed (stated as "not computed" in 03_peer_nulife_ontario_avenue.md). Per-section sizes are given in pages.
