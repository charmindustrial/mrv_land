# Charm PDD change surface — opportunity register rows 1–15

Prepared 2026-09-16 for Max Lavine. Maps each row of the 16-row opportunity register (`07_synthesis_charm_vs_geological_storage_peers.md`, Section 6) to the exact PDD text that would have to change for Charm to adopt the peer method. Row 16 is skipped per instruction (it is marked "Not applicable as a method" in the register itself).

**Source and access method:** Google Drive connector, `get_file_metadata` and `download_file_content` on file ID `1V0v2atno-pVZQZ983EEy9sfmlci4cm_C`. Metadata this session: `"title":"Final V 1.12 Charm Industrial Bio Oil Geologic Storage PDD + Biochar.docx"`, `"modifiedTime":"2026-09-11T23:27:23.942Z"`, `"fileSize":"1991632"`. The downloaded file decoded to exactly 1,991,632 bytes, confirming it is the same file `02_charm_pdd_baseline.md` profiled (same size, same modified time) — no new version has been uploaded since that baseline was written.

**Version confirmed:** the document's own title block, read this session, is:

> "Charm Industrial Bio-Oil Geologic Storage + Range & Plains Biochar Design Document
> v1.12 – 2025/12/01"

Still "v1.12 – 2025/12/01" — unchanged from the baseline profile.

**Word-count method used in this file (corrected and reproducible):** I extracted the document body this session with `python-docx`. For each table cell (`w:tc`), I take its direct child paragraphs (`w:p`), extract each paragraph's own text by joining that paragraph's `w:t` runs with no separator, and then join the paragraph texts within the cell with a newline. Any nested table inside a cell is walked the same way (its cells' texts joined by newline) and treated as one more "paragraph" in the parent cell's sequence, in document order. The whole-document text is built the same way over the body's top-level children (paragraphs and top-level tables), all joined by newline. Every word count in this file is `len(text.split())` — a whitespace-token count — run on that exact newline-joined text.

This method matters because concatenating a cell's runs *without* inserting a break between paragraphs (my error in the version under review) silently merges the last word of one paragraph with the first word of the next wherever there is no trailing space in the XML, undercounting the cell. Inserting a paragraph-boundary separator fixes this. I confirmed the fix against two independent figures given in review: whole-document count now reproduces exactly, and the uncertainty-justification cell count now reproduces exactly (both below). Where a count could not be reproduced exactly, I say so rather than adjust the number to match (see Row 7).

Every passage below is verbatim, confirmed present in my own extracted text this session by direct string search before being written into this file.

---

## Row 1 — Method B sampling (one Production Batch in ten, conservative estimate of the rest)

**Sections/appendices involved — two separate cells, not one:** (a) Section B > Monitoring Plan, the Kansas storage-parameters answer cell (this is the same cell as Row 14's TAN parameter, below); (b) Appendix 6: GHG Statement Report, the "GHG Statement Methodology - Data" answer cell (this is the same large cell as Row 5's Appendix 6 reference, below).

**Passage committing Charm to the heavier practice (cell a, Kansas storage-parameters cell, 3,231 words by my count):**

> "Per section 7.4.1.1.1 of the Bio-Oil Geological Storage protocol, a sample is taken for each injection batch and analyzed for C content to quantify the gross removal"

This quoted sentence is 27 words.

**Passage committing Charm to the heavier practice (cell b, Appendix 6 Data-source cell, 5,572 words by my count):**

> "Carbon content of the oil will be measured using Isometric Protocol Method A – Each injection batch will be sampled prior to the addition of salt and LCS and one sample will be sent to an analytic lab to measure the carbon content of that batch."

This quoted sentence is 46 words.

**Approx. word count of passages affected:** the two quoted sentences are 27 and 46 words (73 words total). They sit inside two different large answer cells — 3,231 words and 5,572 words respectively, each covering much more than carbon sampling — so the *edit itself* is small (two sentences, 73 words) inside cells that would not otherwise need touching.

**Does the PDD already license a lighter practice?** No. Nothing in the quoted text or its surrounding paragraph mentions Method B, sample count reduction, or a random-sampling schedule for carbon content specifically. (Contrast with TAN and displaced-brine below, which do carry step-down language — see rows 3 and 14.)

**Text-only or also changes what Charm measures/collects?** Both. The PDD sentences are a one-line rewrite (cite Method B, name the random-sampling cadence), but this also requires: (1) a documented random-sampling agreement with Isometric to be built and referenced, per the protocol text quoted in the register row itself ("A random sampling approach must be agreed and documented in the Project Design Document"), and (2) an actual change to what gets tested — Charm would stop lab-testing every injection batch and instead test roughly one in ten, which changes the monthly lab-report count, not just the document.

---

## Row 2 — Materiality exclusion of small sources (sum < 1%)

**Sections/appendices involved:** Section B > Project Boundary table (the boundary rows themselves) and the small emission lines that currently get calculated line-by-line: consumables embodied, consumables transport, sample transport, waste disposal.

**Passage(s) committing Charm to the heavier practice:**

> "the volume is measured by on-site staff using a flow-meter" (LCS/consumables embodied line, Section B boundary table)

> "Emissions are calculated for air shipment of samples based on a conservative estimate of the point-to-point distance between the sampling site and labs in Google maps." (sample transport)

> "Charm is using an emissions calculation approach that accounts for both the transport of the wastes to the disposal site, and the emissions impact of the disposal itself." (waste disposal, added per Section F)

**Approx. word count of passages affected:** these three quoted sentences total 64 words (10 + 26 + 28). Each sits in its own boundary-table cell; by my count the three cells run 69, 68, and 1,315 words respectively — the first two are almost entirely the quoted sentence (the cells are short, single-purpose fields), while the third (waste disposal, 1,315 words) is a much larger cell that the quoted sentence is only a small part of.

**Does the PDD already license a lighter practice?** No materiality carve-out language appears attached to these specific lines. The only materiality-style language in the PDD is the uncertainty screen ("increased by 20% ... greater than 1% of the original estimation" — see Row 3), which tests sensitivity of *uncertainty*, not a size-based exclusion of the *source itself* from the boundary.

**Text-only or also changes what Charm measures/collects?** Text-only if the underlying activity data keeps being collected for other reasons (it likely still needs to be tracked for cost/operations); the change is dropping these lines from the emissions calculation and removal deduction, i.e., an edit to the boundary table and the calculation methodology cells, not a change to what instruments exist on site.

---

## Row 3 — Single-parameter or zero uncertainty treatment

**Sections/appendices involved:** Section B > Uncertainty assessment > "Justification for your choice of uncertainty approach" answer cell.

**Passage committing Charm to the heavier practice:**

> "In the Sensitivity Analysis, the value of each source was arbitrarily increased by 20%, a value far higher than a reasonable expectation of measurement variance for any given parameter. These changes are compared against an estimated “Sample Removal” without this variance. Any parameter that, when increased by 20%, contributed to a change in the estimated removal that was greater than 1% of the original estimation was then subject to an Uncertainty Analysis, as specified in Section 2.5.7 of the Isometric Standard."

Followed by per-parameter half-width language, e.g.:

> "The maximum allowable error for a legal-for-trade truck scale is 160 lbs for a fully-loaded truck."

**Approx. word count of passages affected:** the "Justification for your choice of uncertainty approach" answer cell runs to 2,009 words by my count. That entire cell is the change surface for this row, since it justifies why each parameter is or is not propagated. Counting the distinct named parameter sub-headings inside that cell (in reading order: Bio Oil Process Emissions – AECN; Bio-Oil Transportation Fuel Emissions; Bio Oil Pre-Processing Fuel Emissions; Liquid Caustic Soda; Salt; Biomass Transportation Fuel Use; Processing and Pyrolysis Fuel Use; Processing and Pyrolysis Electricity Use; Pyrolysis Tailgas Emissions; Mass of Processed Biomass; Disposal of Process Wastes; Amortized Capital Embodied Emissions; Spare Parts and Consumables Embodied Emissions; Mass of Bio-Oil Produced), and excluding two headings that are not themselves separately measured parameters — "Bio Oil Pre-Processing Consumables Emissions" (a grouping header over the Liquid Caustic Soda and Salt sub-items, not a parameter of its own) and "Gross CO2e Sequestration" (restates the truck-scale and carbon-analyzer uncertainty already counted under transportation and carbon content, rather than introducing a new one) — gives **14 named parameters** in this cell.

**Does the PDD already license a lighter practice?** Partially. The PDD already runs its own 1%-of-net-removal screen (quoted above) and excludes GLEC transport factors from uncertainty treatment on exactly that basis: "There is no Uncertainty Factor calculated for this value. This is due to previous consultations with Isometric confirming that the GLEC factors are based on millions of miles of data" (confirmed present, search term "This is due to previous consultations with Isometric confirming that the GLEC factors are based on millions of miles of data" matched verbatim). So the licensing language for "some parameters may be dropped" already exists for at least one parameter (GLEC); the row's opportunity is applying that same screen result to the remaining half-widths (see the negative-search answer at the end of this file — the PDD does not show a pass/fail table for the other thirteen).

**Text-only or also changes what Charm measures/collects?** Text-only. Dropping a parameter from propagation because it fails the PDD's own 1% screen does not change any instrument, meter, or lab step — it changes only the "Modifications to Address Uncertainty" write-up and the calculation formula in the (external) Uncertainty Analysis sheet the PDD points to.

---

## Row 4 — Pointer-style GHG Statement Report for repeat periods

**Sections/appendices involved:** none of the internal PDD's own sections — the register's own text says the pointer-style report is a feature of Charm's separate monthly GHG Statement Report filing, not of this PDD document ("Charm's answers in D.1 and D.2 are each the single line 'Please see corresponding PDD Appendix'" — that quote is attributed in the synthesis file to the monthly report, not to this PDD; I searched this PDD's extracted text for "Please see corresponding" and got zero hits, confirming that sentence is not in this document).

**Passage committing Charm to the heavier practice:** not applicable — there is no PDD passage to change, because the practice already lives in the monthly report, which the register itself calls "already largely done."

**Approx. word count of passages affected:** 0 in this PDD.

**Does the PDD already license a lighter practice?** Not a PDD question — already implemented outside this document.

**Text-only or also changes what Charm measures/collects?** Neither — no PDD change needed. (Included per the register's own row for completeness, per the task's instruction to cover rows 1–15.)

---

## Row 5 — Monitoring plan and calculation workbook filed outside the PDD

**Sections/appendices involved — three separate cells, not one:** (a) Section B > Monitoring Plan, the short option-selection cell; (b) Section B > Monitoring Plan, the Kansas storage-parameters cell (same cell as Row 1's first quote and Row 14's TAN block); (c) Appendix 6: GHG Statement Report, the "GHG Statement Methodology - Data" cell (same cell as Row 1's second quote).

**Passage committing Charm to the heavier practice (cell a, option-selection cell, 43 words by my count — this is the entire cell, not an excerpt of a larger one):**

> "I have submitted a Monitoring Plan, which meets the requirements specified in the “Monitoring Plan Requirements” appendix of the relevant Protocol and its associated modules, and which describes any additional or modified parameters monitored which deviate from the default Monitoring Plan"

**The other two cells that would also need to move if the whole plan were filed outside the PDD:** cell (b), the Kansas storage-parameters cell holding every parameter's five-question write-up (TAN, density, brine taper, etc.), runs to 3,231 words by my count. Cell (c), the Appendix 6 Data-source cell, runs to 5,572 words by my count. The Appendix 6 "GHG Statement Methodology - Calculations" cell is a further, separate cell not measured in this file (the baseline profile gives 9,287 words for it by a different counting method, not re-verified here, so it is cited there and not repeated here as my own figure).

**Approx. word count of passages affected:** 43 words is the actual text that would change to relocate the plan's stated form; the 3,231-word and 5,572-word cells are the bulk of what physical content would move, but as whole cells, not new text to write.

**Does the PDD already license a lighter practice?** No — Charm has already chosen Option B (bespoke, in-document plan) over a default/pointer form; nothing in the option text or surrounding cell suggests the plan could instead be filed as a standalone document with the PDD merely referencing it, the way Great Plains does.

**Text-only or also changes what Charm measures/collects?** Text-only, in the sense that the underlying monitoring and calculation activity doesn't change — only its container does (move ~21,785 words, per the synthesis file's arithmetic, out of the PDD body and into a referenced spreadsheet/workbook). This requires an Isometric-approved PDD restructure (a Section F project change), not new instruments or new data.

---

## Row 6 — Embodied emissions passed once, or as a site-level per-tonne estimate

**Sections/appendices involved:** Section B > Project Boundary table, rows for "Embodied Emissions, Facilities/Equipment Pyrolysis – Charm," "Embodied Emissions from Injectate Transport to Pre-Processing," "Embodied Emissions, Facilities/Equipment Pre-Processing"; the Basco 6 monthly embodied-emissions inventory practice described in Section F.

**Passage committing Charm to the heavier practice:**

> "emission factors from reputable sources such as GREET database, the EcoInvent database, NAICS supply Chain Emission Factors, USLCI database, ICE database, and/or the Athena Impact Estimator. These values are amortized over the expected useful life of the equipment and improvements used"

> "a cost-based calculation is used based on the average cost and expected useful life of a DOT-111 railcar"

Contrast — Charm already uses a single-factor, one-time-input method for the Kansas site specifically:

> "0.0000351566 tons of steel and 0.000077 m3 of concrete per ton of waste injected, given their conservative estimate of a 2 million metric ton overall well capacity"

**Approx. word count of passages affected:** the three quoted sentences total 86 words (41 + 18 + 27); each sits in its own boundary-table cell, which by my count runs 40–120 words per cell — again close to the full cell content.

**Does the PDD already license a lighter practice?** Partially yes, for Kansas — the Vaulted per-tonne factor quoted above already is exactly this lighter method, adopted from the operator. For Charm's own sites (Fort Lupton, El Dorado, Basco), no equivalent single-factor language exists in the boundary table; the multi-database, amortized-inventory method is the only one described.

**Text-only or also changes what Charm measures/collects?** Both. Rewriting the boundary-table cells to a fixed per-tonne factor or a one-time pass is a text edit, but it also eliminates a recurring data-collection task: the monthly Basco embodied-emissions inventory update the PDD's monitoring section implies is ongoing ("These values are amortized ... over total expected facility biomass throughput" requires updating the denominator and inventory each period). Register row 6 itself notes this is already an open item with Charm's verifier (FARs "ISS-36" and "ISS-34"), so any PDD edit here follows, not precedes, that live review.

---

## Row 7 — Transport fuel from distance × standard factor, embodied folded into the factor

**Sections/appendices involved:** Section B > Project Boundary table rows "Fuel Use from Injectate Transport to Pre-Processing" and "Embodied Emissions from Injectate Transport to Pre-Processing" (and the parallel rows for consumables and to-injection-site transport).

**Passage committing Charm to the heavier practice:**

> "Emissions impact of transport calculated based on GLEC emission factors using cargo weight, vehicle type, and distance traveled with a correction for truck scale uncertainty detailed in the Uncertainty Analysis"

> "Because GREET does not provide comparable emission factors for the manufacturer of railcars, a cost-based calculation is used based on the average cost and expected useful life of a DOT-111 railcar"

> "the longest route is assumed to ensure a conservative estimate of removals"

**Approx. word count of passages affected:** by my count this session, the GLEC quote's cell (boundary table, "Fuel Use from Injectate Transport to Pre-Processing") is 30 words — the entire cell, a short self-contained field. The railcar-cost quote sits in the boundary table's "Embodied Emissions from Injectate Transport to Pre-Processing" cell together with the preceding truck-embodied paragraph; that combined cell is 84 words by my count. I flag a discrepancy here rather than paper over it: an earlier review of this file gave 92 and 81 words for what it identified as the same two passages. I re-extracted both cells with the corrected, newline-joined method described above and get 30 and 84, not 92 and 81. I was not able to identify which specific cells or paragraph boundaries would produce 92 and 81 from the source text, so I am reporting my own reproducible counts (30, 84) rather than adjusting them to match numbers I could not independently derive.

**Does the PDD already license a lighter practice?** No combined fuel-plus-embodied factor is mentioned anywhere in the boundary table; each transport leg carries separate fuel and embodied rows throughout.

**Text-only or also changes what Charm measures/collects?** Both, if adopted: folding embodied into a single per-mile or per-ton-mile factor is a text and formula change to several boundary rows, and it would eliminate the separate railcar cost-basis calculation input (average cost, useful life) as a tracked figure — a change to what gets calculated each period, not just how it reads.

---

## Row 8 — Calculated rather than metered injection electricity

**Sections/appendices involved:** Section B > Project Boundary/Monitoring, "Electricity Use from Injection (Vaulted)" row and the Kansas monitoring parameter for Vaulted electricity.

**Passage showing Charm's current (already-lighter, metered) practice:**

> "The reading on both meters is noted by site staff prior to and following injection"

**Approx. word count of passages affected:** 0 — this row is marked "Not applicable" in the register itself ("Charm already has meters at both sites"), and my search confirms the metered-reading sentence is present verbatim in the PDD, so there is no heavier passage to replace; adopting the peer's calculated method would be a *regression*, not an improvement, and the register agrees.

**Does the PDD already license a lighter practice?** N/A — Charm's existing practice already is the lighter-burden, higher-integrity one (direct meter read vs. NULIFE's calculated estimate, which the register notes NULIFE's own text flags as "lack of primary measured data").

**Text-only or also changes what Charm measures/collects?** No change proposed.

---

## Row 9 — Period-level meter reads instead of per-injection reads

**Sections/appendices involved:** Section B monitoring parameter for Vaulted electricity (Kansas, per-injection) vs. Basco electricity (already period-level).

**Passage committing Charm to the heavier practice (Kansas only):**

> "The reading on both meters is noted by site staff prior to and following injection"

**Approx. word count of passages affected:** this sentence is 15 words, inside the same monitoring-parameter cell already sized above.

**Does the PDD already license a lighter practice?** Not for Kansas. The PDD is silent on any option to step this reading down to a period aggregate; and per the register, "the per-injection read is Vaulted's, done for Vaulted's own monthly report — no Charm saving" — meaning even if the PDD text were rewritten, Charm doesn't control Vaulted's read cadence, so there is no real change surface to exploit here.

**Text-only or also changes what Charm measures/collects?** Not applicable for Kansas (the cadence is set by the operator, not by Charm's PDD text). For Basco, the period-level practice is already what the PDD describes, so no change is needed there either.

---

## Row 10 — Fewer datapoints and evidence files per removal

**Sections/appendices involved:** not a single PDD section — this is a Certify-entry and evidence-attachment practice, touched on in Section B > Data collection and storage.

**Passage committing Charm to the heavier practice:**

> "When data from such documents is entered manually, the document must be provided as a check against entry errors"

> "All data related to the calculation of removals will be transmitted from Charm's Ledger software to Isometric directly via API."

**Approx. word count of passages affected:** the first quoted sentence is 19 words within the Data collection and storage cell.

**Does the PDD already license a lighter practice?** No — the PDD requires a supporting document for every manually entered figure, with no stated threshold for consolidation (e.g., one diesel ledger instead of sixteen receipts).

**Text-only or also changes what Charm measures/collects?** Text-only for consolidation of duplicate evidence (e.g., one REC-certificate datapoint instead of four identical-file rows, one period diesel ledger instead of per-delivery receipts) — the underlying purchase/delivery events still happen, only the number of separate Certify entries and attached files would shrink. The scale-ticket and lab-result evidence described in protocol §8.3.2 ("weigh scale tickets for each delivery ... analytical results for each ... analysis") cannot be consolidated away, per the register's own applicability note.

---

## Row 11 — Single embodied method, one attribution factor, pre-existing sites excluded

**Sections/appendices involved:** Section B > Project Boundary table (all Charm-side embodied-emissions rows) and the Basco 6 conversion-of-an-existing-well treatment.

**Passage committing Charm to the heavier practice:** same as Row 6 —

> "emission factors from reputable sources such as GREET database, the EcoInvent database, NAICS supply Chain Emission Factors, USLCI database, ICE database, and/or the Athena Impact Estimator"

**Approx. word count of passages affected:** overlaps Row 6's count exactly (same sentence, same cell) — this row and Row 6 are two applications of the same underlying PDD text, as the register itself notes ("Overlaps rows 6 and 7").

**Does the PDD already license a lighter practice?** No single-method, single-attribution-factor language exists; six named databases are listed as acceptable sources without a stated preference order.

**Text-only or also changes what Charm measures/collects?** Text-only if Charm picks one database/method going forward — no new instrument is implied — but it is a substantive methodology change requiring the "Embodied Emissions Accounting Module" to actually be read before drafting (register flags this module as not yet read in this line of research).

---

## Row 12 — Mass from producer records (volume × density − moisture) rather than injection-site scale

**Sections/appendices involved:** Section B > Monitoring Plan > Injectate Characterization (mass determination) and the Kansas Vaulted-scale monitoring parameter.

**Passage committing Charm to the current (heavier-integrity, not heavier-burden) practice:**

> "weighing the delivery truck prior to and after injection on a certified scale"

> "The mass of consumables added to the bio-oil being processed are subtracted from the Total Injectate Mass to compute the Mass of Bio-Oil Injected"

**Approx. word count of passages affected:** 0 change proposed — the register marks this row "Not applicable" because Charm already receives scale tickets and weighs at Basco, and because the protocol text it quotes (§8.3.1.2) names the calibrated-scale method as primary, with the density/moisture route as a secondary option only "where such methods are viable and justified."

**Does the PDD already license a lighter practice?** N/A — no change recommended; adopting the peer's method here would lower measurement coverage of the sink, not lighten a burden without cost.

**Text-only or also changes what Charm measures/collects?** No change proposed.

---

## Row 13 — Supplier-side weigh tickets, no scale at the injection site

**Sections/appendices involved:** same as Row 12.

**Passage committing Charm to the current practice:**

> "weighing the delivery truck prior to and after injection on a certified scale"

**Approx. word count of passages affected:** 0 — register marks this "Not applicable," noting Charm's practice already matches the protocol's own preferred text ("weight of delivered bio-oil to the injection site").

**Does the PDD already license a lighter practice?** N/A — no change proposed; the peer's practice (TIRE) is the lower-integrity one here per the reverse list in the synthesis file (scale "calibration not confirmed in this case").

**Text-only or also changes what Charm measures/collects?** No change proposed.

---

## Row 14 — Storage monitoring left to the operator's permit programme rather than a bespoke PDD plan

**Sections/appendices involved:** Section B > Monitoring Plan, the Kansas storage-parameters cell (same cell as Row 1's first quote and Row 5's cell (b), 3,231 words by my count) and Appendix 8 (Basco 6 permanence plan).

**Passage committing Charm to the heavier practice — the Injectate Total Acid Number (TAN) parameter block, quoted in full:**

> "Injectate Total Acid Number
> Who is Testing?
> Charm team
> How Frequently?
> Every injection batch – Frequency may decrease if data shows significant consistency across batches
> How is Testing Performed?
> Sample is sent to an ISO-accredited analytical laboratory
> When is Testing Performed?
> Samples are pulled prior to injectate delivery and mailed to lab
> How are Results Recorded?
> Lab results are reported to Charm and input into the Charm Ledger corresponding with the injection batch for storage"

By my count, this full TAN block (question labels and answers together, as it appears between the "Injectate Total Acid Number" heading and the next parameter heading, "Injectate Density") is 75 words.

The Injectate Density parameter's block, same cell, has no comparable step-down language attached to it in the matched text.

**Approx. word count of passages affected:** the TAN block quoted above is 75 words; it sits inside the larger 3,231-word Kansas storage-parameters cell.

**Does the PDD already license a lighter practice?** **Yes, partially — this is the row where the PDD already contains its own licensing language.** Two step-downs are written into the text as read this session:

> "Every injection batch – Frequency may decrease if data shows significant consistency across batches" (Injectate TAN)

> "Frequency can be reduced once consistency between samples is statistically proven" (displaced brine, temperature/pH and chloride/conductivity parameters)

> "Every two weeks for 3 months. If measurements are consistent this can be changed to every month for 6 months, then quarterly for 2 years, and finally every 6 months if results remain consistent." (displaced brine % C by wt.)

These are already-written taper clauses; using them requires no new PDD text, only a documented consistency finding to trigger the existing language. The Injectate Density and Injectate conductivity/chloride parameters, by contrast, carry no such step-down clause in the matched text — adding one there would be a genuine text change.

**Text-only or also changes what Charm measures/collects?** For TAN and the three displaced-brine parameters: text-only in the sense that the license already exists — invoking it requires no PDD edit, just building the consistency case and (for a full switch to "operator's permit programme only") deleting the Charm-specific parameter rows. For density and chloride/conductivity: would require adding new step-down text plus actually reducing the sampling cadence, i.e., a real change to what gets collected each batch.

---

## Row 15 — Supplier eligibility re-attested every two years, not annually

**Sections/appendices involved:** Section B (third-party compliance affirmation) — the passage sits inside a compliance-monitoring parameter row.

**Passage committing Charm to the heavier practice:**

> "All third-party project participants are queried annually … required to return a signed affirmation"

**Approx. word count of passages affected:** the quoted clause is 13 words within its monitoring-table row.

**Does the PDD already license a lighter practice?** No — no two-year or reduced-cadence option is written for this parameter anywhere in the matched text.

**Text-only or also changes what Charm measures/collects?** Both. Changing "annually" to "every two years" is a one-word-class text edit, but it also changes an actual operational step — one fewer round of affirmation letters and signed responses collected from AECN, Vaulted, and the biomass suppliers every other year. The register notes this needs the Biomass Feedstock Accounting Module read first and calls the saving "small (one annual round of letters)."

---

## Two specific questions

### Does the PDD anywhere justify one sample per batch via low within-batch variation?

**No.** I searched my full extraction of the document body (49,527 words by the corrected method described at the top of this file) this session for each of the following terms and got these hit counts:

| Term searched | Hits |
|---|---|
| "within batch" | 0 |
| "within-batch" | 0 |
| "variation" | 1 — and that single hit is in the Appendix 10 reference list, in a geology citation: "S. P. Dutton, R. G. Loucks, and R. J. Day-Stirrat, 'Impact of regional variation in detrital mineral composition on reservoir quality in deep to Ultradeep Lower Miocene sandstones...'" — unrelated to bio-oil sampling. |
| "homogen" | 0 |
| "well mixed" (no hyphen) | 0 |
| "well-mixed" | 1 — but only as a requirement Charm says it *cannot* meet after consumables are added: "which precludes samples from being the “well-mixed and representative aliquot” required by section 7.4.1.1.1 of the Bio-Oil Geological Storage protocol" — this is Charm explaining why it samples *before* consumables are added, not a variation-based justification for one sample per batch. |
| "representative" | 7 — none of the seven hits justify single-sample-per-batch sufficiency on variation grounds; they cover public engagement ("representatives"), railcar life allocation, and the biochar composite-sampling procedure. |
| "sparg" | 4 — all describe the sparging process step and tank capacity, not a sampling-sufficiency argument. |

None of these searches turned up a passage arguing that within-batch variation is low enough to justify a single sample, which is the second of the two protocol-permitted routes to Method A single-sampling quoted in the synthesis file's Q1 ("Justification and evidence must be provided to demonstrate that the 'within batch' variation is likely to be minimal"). This PDD does not contain that justification anywhere in its body text.

### Does the PDD list which of the 14 uncertainty parameters passed or failed the 1%-of-net-removal sensitivity screen?

**No — not as a pass/fail table.** The PDD states the screening rule and then only lists the parameters that were *identified as requiring* further Uncertainty Analysis (i.e., the ones that failed the screen by exceeding 1%); it does not print a table showing the tested increase and resulting percentage change for every parameter, nor does it name which ones passed (stayed under 1%) apart from the one exception it calls out (GLEC transport factors, excluded on a different, data-volume basis, not by number). The full sensitivity-analysis passage, quoted in full as found in Section B > Uncertainty assessment > "Justification for your choice of uncertainty approach":

> "A Sensitivity Analysis has been carried out for each measured emissions source/parameter based on a Sample Calculation of one truckload of bio oil originated at AECN and transported to Kansas for Injection as well as the first Charm bio-oil injection in Kansas. In the Sensitivity Analysis, the value of each source was arbitrarily increased by 20%, a value far higher than a reasonable expectation of measurement variance for any given parameter. These changes are compared against an estimated “Sample Removal” without this variance. Any parameter that, when increased by 20%, contributed to a change in the estimated removal that was greater than 1% of the original estimation was then subject to an Uncertainty Analysis, as specified in Section 2.5.7 of the Isometric Standard. Note: What follows is in reference to AECN and Charm Kansas injections only. Sample calculations, sensitivity analysis and uncertainty assessment for injection operations in Louisiana can be found in the Basco 6 supplemental document Parameters Identified as requiring Uncertainty Analysis are listed below, along with a brief summary of the approach to identifying and measuring the associated measurement uncertainty. All calculations are included in the Uncertainty Analysis sheet included in the GHG Statement Supplemental Doc appended to this PDD."

The sentence "Parameters Identified as requiring Uncertainty Analysis are listed below" confirms the PDD only names the parameters on the failing (>1% impact) side of the screen, and explicitly hands off the actual per-parameter calculations to a document not included in this file ("the Uncertainty Analysis sheet included in the GHG Statement Supplemental Doc appended to this PDD" — that Supplemental Doc is one of the two documents `02_charm_pdd_baseline.md` already flagged as referenced but not contained in this file). Which of the 14 named parameters counted in Row 3 above were tested and found to pass (i.e., stayed under the 1% threshold and were therefore *not* subject to further Uncertainty Analysis) is not stated anywhere in this PDD's body text — the one exception is GLEC transport factors, and even that exclusion is justified by data-volume ("millions of miles of data"), not by a stated 20%-increase test result.

---

## Source note

Extraction file used for all searches and word counts in this document: `pdd_full_v2.txt`, produced this session from `pdd.docx` (the downloaded, decoded copy of Drive file `1V0v2atno-pVZQZ983EEy9sfmlci4cm_C`) via `python-docx`, using the corrected paragraph-boundary-preserving method described at the top of this file (paragraphs within a cell joined by a newline; nested tables recursed the same way). Not re-read in this session: "Supplemental Doc 3" (Basco 6 Combined Emissions Monitoring and Accounting Plan), the "GHG Statement Supplemental Doc" calculation/Uncertainty Analysis sheets, and the file's Word comments — all three are referenced by the PDD but are separate files/objects not contained in the downloaded document, consistent with what `02_charm_pdd_baseline.md` reported.
