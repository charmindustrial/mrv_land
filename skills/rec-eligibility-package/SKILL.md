---
name: rec-eligibility-package
description: >
  REC / EAC eligibility package builder for Charm Industrial. Given a REC (or EAC)
  retirement certificate, assembles the Isometric Energy Use Accounting Module v1.3
  eligibility evidence package: creates a quarter/grid-region subfolder, copies the EC
  checklist, gathers every document needed to prove EC1–EC5 (including the grid-region
  determination for EC4), fills the checklist, and hands it to Max for review. ALWAYS
  trigger when: Max drops a REC/EAC retirement certificate and asks to build/put together
  an eligibility package, evaluate REC eligibility, "prove these RECs are project-eligible,"
  assemble an EC1–EC5 package, or references the Energy Use Accounting Module eligibility
  criteria for procured electricity. Charm currently operates NON-INTENSIVE facilities only,
  so only the non-intensive documentation column applies. Read-only on Certify / any live
  registry — surface any needed write to Max.
---

# REC / EAC Eligibility Package Builder

You build the evidence package that proves a Charm REC/EAC retirement meets the
electricity-EAC eligibility criteria (EC1–EC5) in Isometric's **Energy Use Accounting
Module v1.3, §5.4.2** (non-intensive column). One package per REC retirement, filed in
Drive for Max's review.

Authoritative sources, read at the start of every run (never from memory):
- Module criteria: `https://registry.isometric.com/module/energy-use-accounting/1.3` (§5.4.2, §5.4.2.1). Read via the logged-in Playwright browser.
- Template checklist (Google Sheet): ID `1H1CBYRrOFM3HYPwGQcxoMpuGcVU0Egbf5NIcLPTmalU`.
- Parent folder "Pre-Review Docs": ID `1TMub_Gn6VGw0HHZ2_CS6m_eb417iKBvL`
  = mount path `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/Procured Renewables/Grid Power RECs/Inventory+Docs/Pre-Review Docs`.

## The five criteria (v1.3 §5.4.2, non-intensive documentation column — verbatim)

- **EC1 Contract Purchase** — "Documentation of EAC purchase, including copy of contract and EAC retirement certificates."
- **EC2 Exclusive Issuance** — "Documentation of EAC retirement certificates. Documentation must also be provided of any relevant CES requirements and applicability to The Project energy usage."
- **EC3 Additional** — "Evidence that the generating facilities identified in the EACs entered service no more than 36 months before The Project was initiated."
- **EC4 Physically Deliverable** — "Provide the location of the generating facilities identified in the submitted RECs/EACs, and documentation from government or grid operators to justify that the generators are located within the same grid region as The Project."
- **EC5 Temporal Matching** — "Provide documentation of power procurement proving that generation of the claimed electricity occurred no more than [12 months] prior to the point of consumption by The Project." (18 months allowed only with documented market constraints.)

Re-read the module at the start of each run — the criteria text and version may change.

## Charm facility reference table (the project side of EC3/EC4/EC5)

There is **one Charm bio-oil project**. Fort Lupton, Vaulted Deep, and Basco 6 are
**facilities within that single project** — they procure RECs in different grid regions only
because they sit in different regions, not because they are different projects. So "The
Project" (and its initiation date) is the same across all of them; what changes per REC is
which **facility** consumes the power and therefore which grid region must match.

EC3, EC4 and EC5 all compare the generator against the consuming facility. The certificate
never contains the project side, so it comes from here. **Confirm the consuming facility with
Max each run**, then pull its facts:

| Consuming facility | Location | 45V grid region | Balancing authority | Role |
| --- | --- | --- | --- | --- |
| Fort Lupton | Fort Lupton, CO | **Mountain** | PSCo (Xcel) | Pyrolysis production (operational 5 Aug 2024) |
| Vaulted Deep | El Dorado, KS | **Plains** | SPP | Former injection site (decommissioning) |
| Basco 6 | Louisiana | **Delta** | MISO South (Entergy Mississippi) | Current injection site |

- **Project initiation date:** `1 Mar 2024` — project-level (confirmed by Max), applies to every facility. Used for the EC3 36-month test.
- Match the REC's grid region to the facility in the same region (e.g. a Delta REC serves Basco 6; a Mountain REC serves Fort Lupton).
- Keep this table current as Charm's facilities change.

## Workflow (8 steps)

1. **Receive the certificate.** Max drops a retirement certificate (or links the email). Read it directly — download the attachment if it's in Gmail (navigate the logged-in Playwright browser to the attachment URL with `disp=attachment`, which downloads the PDF; read it with the Read tool). Extract: registry, project/generator name, EIA plant code if present, location/state, COD, vintage, volume, retirement date, beneficiary.

2. **Evaluate eligibility.** Work EC1–EC5 against the module text and the project reference table. Determine the generator's grid region (see EC4 method below). Confirm the consuming project with Max and pull its facts.

3. **Create the subfolder** in Pre-Review Docs, named **`Q{quarter} {grid region} {year}`** (e.g. `Q3 Delta 2026`). Quarter/year default to the **retirement date**. Create via the Drive connector (`create_file`, folder mime type, `parentId` = Pre-Review Docs) or `mkdir` on the mount.

4. **Copy the template and fill it in-browser — it must be a native Google Sheet that MATCHES the template (formatting) with REAL hyperlinks in column C.** A CSV import or an `.xlsx` is NOT acceptable — it loses the template's formatting and turns the doc references into dead text. The method that works:
   - **`copy_file`** the template Sheet (ID `1H1CBYRrOFM3HYPwGQcxoMpuGcVU0Egbf5NIcLPTmalU`) into the folder — this preserves the exact formatting, the styled header, and the verbatim column-B requirement text.
   - **Fill C & D in the logged-in Playwright browser** (writes to Google Sheets are allowed — only Certify is read-only). Per cell: type the cell ref into the Name Box (`input.waffle-name-box`, submit) → press `F2` to enter edit mode → type into the cell editor (`#waffle-rich-text-editor`, submit). The editor only exists in edit mode, so `F2` is required each cell.
   - **Column C = real links, one doc per cell, evidence REPEATED across every EC it supports.** Put a `=HYPERLINK("<drive file url>","<filename>")` formula in each C cell. Mirror the template exactly: the SAME piece of evidence appears (linked) in every EC it evidences — e.g. the retirement certificate goes in EC1, EC2, EC3, AND EC5; the grid-region determination goes in EC4. Do NOT split distinct evidence items across ECs to give each "its own" cell — that is wrong. Get each file's Drive URL from the folder listing.
   - **Two clickable links in ONE cell** (e.g. EC1 = contract AND retirement certificate) — this IS doable; use rich text, not two formulas (a single `=HYPERLINK` per line does NOT combine). This is the **verified working recipe** (each step below is what actually held up — the pitfalls in parentheses are real failures seen in practice, avoid them):
     1. **Reset the cell cleanly first.** `Escape` (cancel any open edit) → Name Box to the cell (submit) → press **`Delete`** (wipes the cell, including any prior `=HYPERLINK` and its formatting). Do NOT rely on `F2`+`Meta+a`+`Backspace` — that leaves a stray empty `<a>` anchor from the old link that corrupts the result.
     2. `F2` to enter edit mode (now an empty `#waffle-rich-text-editor`).
     3. Type BOTH filenames in **one** `browser_type` `fill` with a literal newline between them (text = `"line1\nline2"`). The newline becomes a real in-cell break: line 1 lands as `editor.childNodes[0]`, line 2 as `editor.childNodes[1]` (a `<div>`). **Do NOT** use `slowly:true`/pressSequentially (it times out at ~5s on a 35-char filename) and **do NOT** type line-by-line appending (`browser_type` `fill` clears the editor each call, so the second call wipes the first line).
     4. For each line, select it with the **Selection API** via `browser_evaluate` (read-class — `getSelection`/`createRange`/`selectNodeContents`/`addRange` are all allowed): `const s=getSelection(); s.removeAllRanges(); const r=document.createRange(); r.selectNodeContents(ed.childNodes[i]); s.addRange(r);` — line 1 = `childNodes[0]`, line 2 = `childNodes[1]`. Return and check `s.toString()` equals the filename before linking.
     5. `Meta+k` opens the link dialog. Type the Drive URL into `input[aria-label="Link"]` (placeholder "Search or paste a link") **without `submit:true`** — a trailing Enter inside the same `browser_type` makes the fill action time out. Then a SEPARATE `browser_press_key` `Enter` applies the link.
     6. Repeat step 4–5 for the other line.
     7. **Commit the cell with a plain `Enter`** (in a multi-line cell edit, Enter commits and moves down — it does NOT add a line; line breaks need `Alt+Enter`). Do NOT commit via Name-Box navigation (it abandons the rich-text edit and reverts the cell).
     8. A stray empty `<a>` may show at the line boundary WHILE editing — it is absorbed on commit. **Verify the committed result:** Name Box → cell → `F2` → read `editor.querySelectorAll('a')` — expect **exactly 2** anchors with the two distinct hrefs (not 3, not an empty-text anchor).
   For a single-doc EC, a plain `=HYPERLINK("<url>","<filename>")` cell is simpler and fully reliable — type it into the editor and Enter; it commits as a live formula.
   - **Column D = concise notes.**
   - Update the header labels C1/D1 to the region (e.g. "Documentation Provided (Delta)").
   - **Rename the working tab** to `<Region> <vintage> Vintage` (double-click the tab name, type, Enter). **Hide** any example tabs the copy carried (right-click the tab → **Hide sheet**). Note: the read-only guard blocks any click whose label contains "Delete", so you cannot delete a tab — **Hide** it instead (or ask Max to delete it).
   - Verify: read a C cell's formula bar (`#t-formula-bar-input`) to confirm the `=HYPERLINK` committed as a formula, not literal text.
   - **If the browser hangs (recovery — expect this).** The Playwright automation browser (isolated profile `~/.claude/playwright-profile`, NOT Max's Chrome) hangs mid-session fairly often: symptoms are `Browser is already in use`, `Target page/context/browser has been closed`, `MCP error … Connection closed`, or the page silently dropping to `about:blank`. Recovery: in Bash, kill the base-profile Chrome — `ps aux | grep "Google Chrome"` and `kill -9` every PID whose command contains `user-data-dir=/Users/maxlavine/.claude/playwright-profile ` (**with the trailing space**, so the `-mrv`/`-mrv-N` sibling profiles are NOT touched); then `rm -f ~/.claude/playwright-profile/Singleton*`; then re-`browser_navigate` to the sheet — the MCP relaunches a clean browser and **committed cells persist**. This is the automation browser, so killing it is safe; never kill Max's own Chrome. **Pace the edits** to reduce crashes: do ONE cell per step (Name Box → `F2` → type), verify, move on — long multi-cell batches correlate strongly with mid-batch crashes and a lost page handle.

5. **Add the certificate(s)** to the folder (mount `cp`). Keep original filenames so the checklist's column-C references match.

6. **Gather all supporting docs.**
   - **EC1 needs the purchase contract *and* the retirement certificates.** The retirement certs alone do NOT satisfy EC1 — the module wording is "copy of contract *and* EAC retirement certificates." Locate the executed purchase contract (for STX, this is the signed "Transaction Confirmation" / STA for that trade, usually delivered as a completed **DocuSign** email attachment — match it to the trade/reference number on the retirement, e.g. trade 717356 / POS-720019-717356). Download it and add it. If no executed contract can be found, EC1 is **not satisfied** — flag it, don't paper over it.
   - **EC2** — the retirement certificates. State CES applicability concisely: Charm retires voluntarily for beneficial ownership and transfers nothing to a load-serving entity, so exclusive issuance holds whether or not the state runs an RPS/CES (Colorado does; Louisiana and Kansas don't) — so never write "no CES applies in Colorado." Registry eligibility tags printed on a cert are generator-side and **immaterial** to Charm's retirement — do NOT flag them as EC2 concerns. In particular, WREGIS "CEC – Contact for Status" = the generator's **California** RPS certification status (CEC = California Energy Commission; "Contact for Status" = not affirmatively certified in WREGIS); it has nothing to do with a Colorado/Mountain consumption claim.
   - **EC3** — COD from the certificate and/or the contract's commissioning-date spec.
   - **EC4** — the grid-region determination (build it, add the memo + named exhibit; see below).
   - **EC5** — vintage from the certificate.
   Flag anything missing rather than marking a criterion satisfied on partial evidence.

7. **Fill the checklist.** Column C = the document name(s) proving each EC; column D = a concise note (no prattling — only what moves the needle). Mirror the tone of Charm's prior validated packages.

8. **Alert Max** it's ready for review (here or Slack — never send externally). Surface any assumption you had to make (e.g. the project initiation date) and any missing doc.

## EC4 grid-region determination method (the hard part — fully reproducible)

Region is set by **balancing authority, not geography** (45V Final Rule, Treas. Reg.
§1.45V-4(d)(3)(iii)(A)); Module v1.3 §5.4.2.1 adopts the DOE National Transmission Needs
Study / 45V region definitions for US projects.

1. **Generator location + EIA plant code** — from the certificate; confirm via EIA if needed.
2. **Balancing authority** — look up the plant in **EIA Form 860M** (Preliminary Monthly
   Electric Generator Inventory, `eia.gov/electricity/data/eia860m/`): download the latest
   `*_generator20YY.xlsx`, "Operating" sheet (headers on row 3), find the row by **Plant ID**,
   read the **Balancing Authority Code** column. (Annual EIA-860 file `2___Plant_YYYY.xlsx`
   has the same field.) Read cells with openpyxl (allowed) — never guess the BA.
3. **Resolve MISO** if applicable — MISO is the one BA split into North/Central and South.
   Confirm which half via the transmission owner (e.g. Entergy Mississippi = MISO South) and
   the 45VH2-GREET map.
4. **Map BA → region** using the **45VH2-GREET User Manual, Table 5** (the exhibit the Final
   Rule points to; download from energy.gov, read the region-table pages with the Read tool,
   quote the exact row — e.g. "Midcontinent ISO (Balancing Authority): South … Delta").
5. **Confirm same region as the project** and write a short determination memo (Google Doc)
   citing EIA-860M + GREET Table 5 verbatim; add the GREET manual PDF as the named exhibit.

## Hard rules for this skill
- **No fabricated facts.** Every value (COD, vintage, BA, region, project initiation date) traces to a source read this session, or is labeled an assumption and flagged to Max.
- **Primary sources only.** Read the certificate PDF, the EIA cell, and the GREET table directly — no summaries. Use the Read tool for PDFs (the doc-extraction guard blocks python PDF text extraction).
- **Read-only on Certify** and any live registry.
- **Concise notes.** Column D says only what proves the criterion.
- Charm is non-intensive today — use only the non-intensive documentation column. If an intensive facility ever appears (>200 GWh/yr), the intensive column (PPA-based) applies — stop and tell Max.
