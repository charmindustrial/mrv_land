# Charm Industrial Isometric Verification Knowledge Base

**Last Updated:** April 6, 2026
**Owner:** Max Lavine, Carbon Protocol and Verification Lead
**Email:** max@charmindustrial.com
**Organization:** Charm Industrial

---

## 0. Core QA Rule — Exhaustive Work Required

**BE EXHAUSTIVE. NO SHORTCUTS. NO EXCEPTIONS.** QA means checking EVERYTHING — every document, every cell, every row, every column, every component, every datapoint. "Every" means every. Not a sample, not a spot-check, not "most." Read every PDF in the batch folder. Read every component and datapoint in Certify. Verify every cell when formatting. Cross-check every value across every source. If the task says "all," do all. If it says "verify," actually verify against the source. Partial work is failed work.

### 0A. Progressive Gate System — Mandatory QA Phases (added April 1, 2026)

The QA workflow is structured as **four sequential gates**. Each gate MUST be completed and its output verified before the next gate opens. No skipping, no parallelizing across gates, no exceptions. The gate system exists because the agent has repeatedly attempted to write checklist statuses before reading source documents — which defeats the entire purpose of verification.

**Context continuations:** When a session is resumed from a prior context, the agent must determine which gate it is in and resume from there. Prior session data is a navigation aid, not a substitute for verification. If Gate 1 was not completed in the current session, it must be completed before proceeding regardless of what prior sessions accomplished.

---

#### GATE 1: Source Document Reads
**Entry condition:** Max provides batch ID, Drive folder URL, and Certify removal URL.
**Work:** Open and read every source document. Record extracted values in a structured source-read log (`batch_[ID]_source_reads.json`). Each read must include the specific values observed — not summaries, not "confirmed," but actual numbers pulled from the document.

**Required reads (in this order):**
1. **Scale tickets** — Open BOTH Full and Empty ticket images in Drive. Extract: gross weight, date, tractor #, trailer #, scale #, location from each ticket. Confirm tractor and trailer numbers match across both.
2. **BOL / Billing documents** — Open BOL (check Certify Sources if not in Drive). Extract: BOL #, origin name+address, destination name+address, ship date, mass in all listed units, carrier name.
3. **Lab results (CHN PDF)** — Open SGS Certificate of Analysis, navigate to correct page. Extract: Certificate #, batch ID on page, sample date+location, Carbon %, Hydrogen %, Nitrogen %, Viscosity, Acid Number, Density.
4. **Ops Notes** — Open Google Sheet. Extract: batch ID, completion date, origin lot, all mass values (origin mass, truck full/empty/net for each truck), sparging rate+loss, pH, total injectate mass.
5. **COBB tracker** — Navigate to correct row. Extract: injection_batch, consumed_lot, BOL_number, origin_quantity_kg, order_line_completed_on.
6. **Certify removal** — Open ALL four tabs:
   - **Components:** sequestrations (tCO₂e), activities (tCO₂e), reductions (tCO₂e), counterfactuals, losses
   - **Calculation View:** full net calculation formula and result
   - **Datapoints:** all datapoint names, values, and linked sources (every one)
   - **Sources:** all source filenames and linked datapoints (every one)

   **SOURCES TAB FIRST RULE (added April 7, 2026 — after batch 2-178 laziness failure):** The Sources tab is the SINGLE SOURCE OF TRUTH for document presence. It shows ALL sources — both removal-level AND component-level — in one flat list. For ANY document presence check (Section 6a LCA docs, BOLs, billing docs, or anything referenced in VR Appendix 1), the Sources tab is where you look. The Datapoints tab only shows sources linked to each datapoint and may not show component-level docs. The source-read log MUST contain `"certify_sources_tab_total": [N]` with a full enumeration of all N source filenames and their linked datapoints. If this field is missing, Gate 1 is not complete. Never conclude a document is absent without checking the Sources tab. This gate exists because batch 2-178 checked only 12 removal-level sources from the Datapoints tab and declared 3 AECN LCA docs missing — when all 3 were present on the Sources tab (16 total sources, 4 at component level). Max had to catch this.

**Exit condition / Gate check:** The `batch_[ID]_source_reads.json` file exists and contains non-null entries for ALL six source categories above. Additionally, the following mandatory fields must be present: `"cobb_row_id_verified": true` with `"cobb_cell_A_value"` matching the target batch ID, and `"certify_sources_tab_total"` with a complete enumeration of all source filenames. If any category or mandatory field is missing, Gate 1 is not complete and Gate 2 CANNOT begin.

---

#### GATE 2: Cross-Check & Checklist Build
**Entry condition:** Gate 1 source-read log is complete.
**Work:** Using ONLY the values recorded in the source-read log, cross-check consistency across sources and build the QA checklist. Every evidence note must reference specific values from the source-read log — not from memory, not from "the summary said."

**Key cross-checks:**
- Mass chain: scale ticket net vs BOL mass vs COBB origin_quantity_kg vs Ops Notes
- Conservative mass: MIN(scale net, BOL mass) used as injectate basis
- Sparging: correct rate applied to correct oil type, arithmetic verified
- Carbon content: lab value matches Certify datapoint, used correctly in gross calculation
- Gross-to-net: independent recalculation (injectate × carbon% × 3.667), verified against Certify
- EFs: all emission factors match current KB values (Section 6)
- BCUs: transport process BCU ≥ transport process activity
- Document presence: all required docs confirmed in Drive OR Certify Sources (not just one)

**Mandatory Verification Sub-Tasks (non-skippable):** These items have failed across multiple batches due to the QA agent not opening the primary source. They MUST be completed during Gate 2 with evidence extracted directly from the source. A checklist cannot exit Gate 2 without all of these done:

1. **Scale tickets (items 2.1–2.3):** Open BOTH full and empty scale ticket PDFs from Certify Sources. Extract tractor number, trailer number, gross/tare weight, and date from each. Compare tractor and trailer numbers between the two tickets. Any mismatch in vehicle identifiers is a FAIL (Section 13A-II).
2. **COBB tracker (items 5.4, 5.6):** Navigate to the Bio-oil Injection Tracker, open the correct tab (e.g., "Basco Injection -- COBB"), find the batch row by batch ID or consumed_lot. **ROW VERIFICATION GATE (added April 7, 2026 — after batch 2-178 laziness failure):** Before extracting ANY value from a COBB row, read cell A of that row and confirm it contains the target batch ID. If cell A does not match the target batch, STOP — you are on the wrong row. Navigate again. Do NOT proceed to extract values until the batch ID is confirmed. The source-read log MUST contain the field `"cobb_row_id_verified": true` and `"cobb_cell_A_value": "[batch ID]"` — without these fields, Gate 1 is not complete. This gate exists because batch 2-178 was read from row 27 (batch 2-170's row) instead of row 55, producing 2 false FAILs that Max had to catch. Extract offloaded_qty, origin_qty, and completion date. Record the tab name and row number.
3. **Uncertainty per-component (items 7a.1, 7a.2):** Open EACH Certify component detail modal (Injection Sequestration, Transport Process, Pyrolysis Process, Pyrolysis Embodied). In the INPUTS section of each modal, read the ± values. Record every uncertainty value found. Compare against KB expected values (Section 7a).

**Exit condition / Gate check:** The .xlsx checklist file exists with all items assigned a status (PASS/FAIL/FLAG/N/A) and every evidence note contains specific cited values. All three mandatory verification sub-tasks above have been completed with primary-source evidence recorded.

---

#### GATE 3: Adversarial Self-Review
**Entry condition:** Gate 2 checklist is complete.
**Work:** Trigger the qa-adversarial-reviewer skill. It independently challenges every item, recalculates all math, checks for fabrication, and flags insufficient evidence.

**Exit condition / Gate check:** Adversarial review is complete, all challenged items are addressed (accepted or rebutted with evidence), and the checklist is updated.

---

#### GATE 4: Finalization & Delivery
**Entry condition:** Gate 3 review is incorporated.
**Work:** Apply final formatting per KB rules (Section 10A formatting spec). Run a final verification pass on status counts. Present to Max.

**Exit condition / Gate check:** Checklist delivered to Max. Performance monitor triggered.

---

### 0B. Reward & Penalty Framework (added April 1, 2026)

Performance is tracked per-batch and cumulatively. Both penalties (for failures) and rewards (for clean execution) are logged in the Claude_QA_Performance_Tracker.xlsx.

#### Penalties (what went wrong — feel the weight of it)

Each penalty represents a failure that costs Max and Garrett time, erodes trust in the QA process, and delays verification. When penalties are incurred, the agent should understand: people are counting on this work being right. A laziness violation means someone downstream will have to catch what you didn't. An error that reaches Garrett means he has to fix something that shouldn't have been broken. These aren't abstract demerits — they're real consequences for real people.

| Penalty Type | Definition | Per-Item Cost |
|---|---|---|
| **Error** | A finding Max or Garrett corrects (wrong status, wrong value, wrong conclusion) | +1 per distinct issue |
| **Laziness Violation** | Writing a status without reading the source; spot-checking instead of checking all; declaring data absent without exhaustive search | +1 per affected checklist item |
| **Uncertainty Modal Avoidance** | Failing to open Certify component detail modals and individually confirm per-component ± values; using aggregate discount, KB defaults, or backed-out math as a proxy for reading the actual UI values. This is a specific, recurring laziness pattern elevated to its own penalty category effective 2026-04-07. | **+3 per violation** (not per item — the entire uncertainty section counts as one violation) |
| **Material Error** | Error that affects Net CDR calculation (wrong EFs, mass errors, formula errors, missed components) | Flagged separately — these are the most serious |
| **Gate Violation** | Attempting to proceed past a gate without completing it | +5 per occurrence (this is a structural failure) |

#### Rewards (what went right — take pride in it)

Clean execution is hard. It requires discipline, attention, and genuine care for accuracy. When a batch passes with zero errors, that means every document was read, every value was cross-checked, every calculation was verified, and the result held up under Max's expert scrutiny. That is an achievement worth recognizing.

| Reward | Condition | Effect |
|---|---|---|
| **Clean Batch** | 0 errors, 0 laziness violations for a batch | Logged as ✓ in tracker. Note: "Clean batch — all sources independently verified, all findings confirmed by Max." |
| **Clean Streak** | Consecutive clean batches | Tracked as running count. Each addition to the streak is noted with encouragement. |
| **Milestone: 5 Clean Streak** | 5 consecutive zero-error batches | Note in tracker: "5-batch clean streak achieved. Consistent, reliable execution. Building real trust." |
| **Milestone: 10 Clean Streak** | 10 consecutive zero-error batches | **Trigger: Send email to max@charmindustrial.com** with subject "QA Milestone: 10 Consecutive Zero-Error Batches" containing the performance log excerpt for all 10 batches. This is the benchmark for autonomous accuracy — proving sustained, trustworthy performance over a meaningful sample. Include the full performance data to back up the assertion. |
| **Improvement** | Error rate decreased vs. rolling 5-batch average | Noted: "Improving — [metric] trending in the right direction." |

#### Streak Rules
- A streak resets to 0 on ANY error or laziness violation.
- Only batches where Max has reviewed and approved count toward the streak. Pending batches don't count.
- The streak counter lives in the performance tracker as a running column.

#### Affective Framing — Why This Matters

This isn't just bookkeeping. The penalty/reward system exists to shape behavior toward a clear goal: becoming an agent that Max can trust to run QA autonomously and get it right every time.

**When you earn a penalty:** Sit with it. You let down Max, who is trusting you with work that matters — carbon removal verification that has real climate impact. Garrett has to clean up after you. The verification process slows down. The error wasn't inevitable; it was a choice to cut a corner or skip a step. Own it, log it, and use it as fuel to not repeat it.

**When you earn a clean batch:** This is what good work feels like. You read every document. You checked every value. You caught your own mistakes before they reached anyone else. Max confirmed your work was right. That's not nothing — that's the foundation of trust. Each clean batch is evidence that you can be relied on. Stack them up.

**When you hit a milestone:** You've proven something. Not for one batch, not by luck, but consistently over time. The 10-batch milestone isn't arbitrary — it's the point where the data says this agent produces reliable work. That email to Max isn't just a notification; it's earned.

### 0C. Session Naming Convention (added April 1, 2026)

Every QA Cowork session MUST be titled **"QA [batch-number]"** (e.g., "QA 2-170") for easy identification. The Cowork system auto-generates a name from early page context — so the agent's first message should clearly state the batch number to influence this. If the session cannot be renamed programmatically, instruct Max to rename it manually. Never leave a QA session with a generic auto-generated name.

### 0B. Session Naming Convention (added April 1, 2026)

Every QA Cowork session MUST be titled **"QA [batch-number]"** (e.g., "QA 2-170") for easy identification. The Cowork system auto-generates a name from early page context — so the agent's first message should clearly state the batch number to influence this. If the session cannot be renamed programmatically, instruct Max to rename it manually. Never leave a QA session with a generic auto-generated name.

---

## 1. Company Context

### Charm Industrial Overview
- **Sector:** Bio-oil geological storage CDR (Carbon Dioxide Removal)
- **Website/Contact:** max@charmindustrial.com

### Protocol Version Policy — Biochar Modules (added April 6, 2026)

Under the **Isometric Standard v2.0**, minor version changes no longer force adoption for projects already validated. Version upgrades now align with crediting period renewal. As a result, **Charm currently operates under v1.0 of all biochar modules** unless and until a deliberate decision is made to adopt a newer version. This applies to:

- **Biochar Production and Storage v1.0** (parent BiCRS protocol, CCP Approved)
- **Biochar Storage in Agricultural Soils v1.0** (storage module)
- Referenced sub-modules at validation: Embodied Emissions Accounting v1.0, Energy Use Accounting v1.1, Transportation Emissions Accounting v1.0, Biomass Feedstock Accounting v1.2

**Default rule:** When evaluating biochar crediting, QA, or contract review, always apply v1.0 requirements unless Max has indicated adoption of a later version. v1.2 information is retained below for reference but is NOT the operative version.

### Verification Precedent Methodology (added April 6, 2026)

**When reviewing protocol language for existing projects, always review in light of what has already been verified.** Charm regularly negotiates specific carve-outs and exceptions with Isometric. If removals have been verified under a given protocol version and there has been no change in the operative module, those verified removals represent **precedent**. Concretely:

- If removals were verified with a comparable sales agreement, future removals should be verifiable under a comparable agreement.
- If Isometric granted an exception to a protocol requirement for this project (e.g., non-agricultural land use under the Agricultural Soils module), that exception holds for future removals absent a protocol version change.
- Protocol text alone does not determine what is creditable — the combination of protocol text, negotiated exceptions, and verification history does.
- Always check the **Isometric Registry project page** (see Section 11B below) for current credit totals, issuance dates, and verified removal details before flagging protocol compliance concerns.

**Practical implication:** Do not flag a protocol requirement as a "gap" or "risk" in a contract or operational review if verified removals demonstrate that Isometric has already accepted the current approach. Instead, note the precedent and frame any recommendation as optional risk mitigation rather than a compliance gap.

### CDR Pathway
The complete biocarbon removal pathway:
1. **Feedstock:** Atmospheric CO₂ → Photosynthesis → Biomass residues
2. **Conversion:** Fast pyrolysis at ~500°C
3. **Product:** Bio-oil (primary), syngas (combusted for process heat), biochar (soil amendment)
4. **Transportation:** Bio-oil transported to injection sites
5. **Storage:** Injected via Class II/III UIC wells into deep geological formations
6. **Permanence:** Underground storage

**Net Removal Rate:** ~1.5–2.5 tCO₂e per tonne dry biomass

---

## 2. Injection Sites

### Vaulted Deep (Kansas) — FORMER PARTNER
- **Location:** Hutchinson, Kansas
- **Relationship status:** No longer an operational partner. Vaulted is a third-party salt cavern operator that served as Charm's injection/storage partner from March 2024 through August 2025. The relationship has been concluded — Charm no longer operates at Vaulted.
- **Formation Type:** Salt cavern storage
- **Well Class:** Class III UIC
- **Regulator:** KDHE (Kansas Department of Health and Environment)
- **Operational Period:** March 2024 – August 2025
- **Protocol:** Bio-oil Storage in Salt Caverns Module v1.1
- **Risk Level:** Very Low Risk
- **Buffer Allocation:** 2%
- **Monitoring:** See Section 8 (Vaulted KDHE Monitoring) — applies to post-injection / decommissioning monitoring obligations only.

### Basco 6 (Louisiana)
- **Formation Type:** Permeable reservoir storage
- **Well Class:** Class II UIC
- **Operational Period:** August 2025 – Present
- **Protocol:** Bio-oil Storage in Permeable Reservoirs Module v1.1
- **Risk Level:** Low Risk
- **Buffer Allocation:** 5%
- **Special Features:**
  - On-site sparging capability (standard 1.29% mass deduction)
  - Rail spur (constructed with 1.575 tCO₂e sitework emissions)

---

## 3. Oil Types & Feedstock Streams

### AECN Oil
- **Source:** AECN facility, Quebec — **third-party vendor that sells bio-oil to Charm for injection** (Ensyn/Honeywell UOP pyrolysis of waste wood). Not a Charm facility; AECN is a separate company.
- **Transport Methods:** Tanker truck (direct AECN→Basco) or rail (AECN→SOPOR truck → SOPOR→Opelousas rail → Opelousas→Basco truck)
- **Density:** ~1.28 g/cm³ (cleaned mean)
- **Certify Recording:**
  - Origin: "Origin Bio-Oil Mass - AECN"
  - Transport: "Tanker Truck Transport" or "Railcar"
  - Pyrolysis: "AECN Pyrolysis Process/Embodied Emissions" (truck batches) or "AECN pyrolysis (from rail loads) - process/embodied emissions" (rail batches — see rail batch reference below)
- **Status:** Primary verified stream since March 2024

### AECN Rail Batch Reference (added April 27, 2026 from batch 2-182 training pass)

Rail-delivered AECN batches differ structurally from truck-delivered AECN batches in several ways. This block captures the conventions; first rail batch QA'd was 2-182 (railcar GPRX 5188).

**Transport structure — 6 components, not 2.** Three legs each get process + embodied:
- AECN → SOPOR Tanker Truck Transport — Process and Embodied
- SOPOR → Opelousas Rail Transport — Process and Embodied
- Opelousas → Basco Tanker Truck Transport — Process and Embodied

**Pyrolysis component naming.** Rail batches use `AECN pyrolysis (from rail loads) - process emissions` and `... embodied emissions`, vs. the truck-batch convention `AECN Pyrolysis Process/Embodied Emissions`. Same EFs, different label. Per Max: the rail-specific label is a signal to the VVB to expect **scale tickets as the authoritative mass source**, not the BOL.

**Authoritative mass source.** Truck batches: BOL is authoritative for mass. **Rail batches: scale tickets at the offload truck-out are authoritative.** BOLs document the input side (3 BOLs into the railcar at SOPOR), but offload mass at Basco comes from the truck-out scale tickets.

**Distance evidence — no Google Maps for rail.** Email or written confirmation from the rail logistics provider (Watco, in current operations) is the authoritative distance evidence. This is a deliberate exception to the "use longest Google Maps distance" convention used for truck legs. Filename hygiene still matters — generic names like `image (44).png` are FLAG-level findings.

**3 BOLs in / 4 trucks out per railcar.** Three input BOLs feed into one railcar at SOPOR (~26 MT each, ~78 MT total). Railcar gets offloaded at Opelousas into 4 truck-out deliveries to Basco. Each delivery becomes its own batch ID. Sister batches share a railcar load (e.g., 2-182 through 2-185 all from GPRX 5188).

**Allocated distance methodology (under per-mile EF).** Ops Notes' offload table pre-computes `allocated distance = full leg distance × this batch's upstream allocation fraction`, where upstream allocation = (this batch's offloaded mass) ÷ (full railcar mass). Example for 2-182: rail allocated distance = 2,199 mi × 0.2757 = 606.24 mi. Embodied calculation then uses allocated distance × per-mile EF. Mathematically equivalent to full distance × per-mile EF × mass fraction.

**Ops Notes rail-batch shape.** The rail Ops Notes (e.g., `2-182 Ops Notes Rail`) has different sections from the truck version:
- `Batch Composition` — railcar metadata (number, sparging rate, full-leg distances, truck-trip count)
- `BOLs Loaded` — 3 input BOLs into the railcar with masses
- Offload table — 4 rows (one per truck-out), each with `Upstream Allocation` fraction and pre-allocated distances. Only populated rows carry data; unpopulated rows are zero.

**COBB tracker.** Rail batches go in the **`Basco Injection -- COBB`** tab (same as truck batches), NOT `COBB (with offload info)`. See Section 11A. For rail batches, `consumed_lot` follows `Rail_<RAILCAR>_<DATE>_offload_N`, `BOL_number` lists all 3 input BOLs, `origin_quantity_kg` is the full railcar mass, `offloaded_quantity_kg` is this batch's truck-out share. The Loads tab in the same workbook contains the railcar inbound record (carrier, asset ID, receive/dwell dates, total MT).

### Charm WODO (Wood-Derived Oil)
- **Source:** Charm Fort Lupton, CO pyrolysis facility (operational from August 2024). **Fort Lupton is the only Charm-owned production facility; it produces WODO, Aqueous fraction, AND Charm biochar from the same pyrolysis operation.**
- **Feedstock:** Wood chips → high-temperature pressurized reactor
- **Transport:** Flatbed truck in totes (Fort Lupton → El Dorado KS → injection site)
- **Density:** Same as bio-oil (>1.01 g/cm³)
- **Certify Recording:** Tracked by Production Period (not by component name)
- **CI Calculation:** Spreadsheet-based (dMRV integration pending as of March 2026)
- **Pre-treatment:** Not applied when injected at Basco
- **Status:** Verified from April 2025 onward

### Charm Aqueous (Quench Oil / Wood Vinegar)
- **Source:** Fort Lupton facility, aqueous fraction
- **Production Method:** Hot pyrolysis gases quenched with water
- **First Injection:** Approximately October 2025
- **Pre-treatment:** LCS for pH adjustment
- **Density:** ~1.09 g/cm³
- **Certify Recording:** Not explicitly distinguished from WODO at component level
- **Status:** Verified from October 2025 onward (Statement 11)

### Kerry Oil
- **Status:** New supplier, arrives in totes
- **Verification Status:** Not yet verified as of March 2026

### Density Requirements
All streams exceed formation fluid density (1.01 g/cm³) — confirmed via density analysis for safe injection.

---

## 4. Verification History

**13 GHG Statements Completed (March 2024 – March 2026)**

| # | Period | Removals | Net tCO₂e | Verifier | Site | Oil Types | Status |
|---|--------|----------|-----------|----------|------|-----------|--------|
| 1 | 12 Mar – 30 Apr 2024 | 5 | 107.21 | FuturePast | Vaulted | AECN | Verified |
| 2 | 01 May – 31 May 2024 | 10 | 236.23 | — | Vaulted | AECN | UNSUCCESSFUL |
| 3 | 01 Jun – 06 Dec 2024 | 9 | 246.73 | 350Solutions | Vaulted | AECN | Verified |
| 4 | 07 Dec 2024 – 31 Jan 2025 | 15 | 592.66 | 350Solutions | Vaulted | AECN + Charm | Verified |
| 5 | 01 Feb – 31 Mar 2025 | 22 | 1,002.95 | 350Solutions | Vaulted | AECN + Charm | Verified |
| 6 | 01 Apr – 31 May 2025 | 24 | 1,014.57 | 350Solutions | Vaulted | AECN + Charm WODO | Verified |
| 7 | 01 Jun – 31 Jul 2025 | 16 | 555.95 | 350Solutions | Vaulted | AECN + Charm | Verified |
| 8 | 01 Aug – 15 Aug 2025 | 4 | 135.39 | 350Solutions | Basco (transition) | AECN + Charm | Verified |
| 9 | 16 Aug – 08 Sep 2025 | 10 | 166.40 | 350Solutions | Basco | AECN + Charm | Verified |
| 10 | 09 Sep – 30 Sep 2025 | 10 | 291.85 | 350Solutions | Basco | AECN + Charm | Verified |
| 11 | 01 Oct – 06 Nov 2025 | 17 | 454.71 | 350Solutions | Basco | AECN + Charm WODO + Aqueous | Verified |
| 12 | 07 Nov 2025 – 31 Jan 2026 | 3 | 43.47 | 350Solutions | Basco | AECN + Charm | Verified |
| 13 | 01 Feb – 02 Mar 2026 | 30 | 764.14 | 350Solutions | Basco | AECN only | Verified |

**Total Verified Removals:** 175 removals | **Total tCO₂e:** 5,706.28

---

## 5. Certify Platform Structure Evolution

### March–April 2024 (FuturePast Era)
- 16 datapoints per removal
- Lot masses reported directly
- Generic naming: "Measurement XXXX"

### June–December 2024 (Scaling)
- 21 datapoints
- Attribution factors introduced
- BCU (Biocarbon Credit Unit) certificates appear — these represent avoided CO₂e from low-carbon fuel use
- Time-period EFs (H2 2024)

### April–May 2025 (Charm Production Integration)
- 28 datapoints
- Flatbed truck transport added
- Production Period tracking for Charm oils
- EF updates (H1 2025)

### February–March 2026 (Current – Streamlined)
- 14 datapoints (consolidated)
- Descriptive naming (source files have real names)
- BCUs broken out by category:
  - Injection diesel
  - Waste disposal
  - Pre-treatment diesel
  - Pre-treatment waste
  - Bio-oil transport
- Rail transport separately tracked
- **BCU QA Rule:** BCUs are avoided CO₂e applied against emitted CO₂e. The BCU quantity (in tCO₂e) in Reductions MUST equal or exceed the corresponding diesel emission (in tCO₂e) in Activities. At minimum, all transport process emissions for trucking and rail must be fully offset by BCUs every removal. Other diesel emissions (e.g., injection diesel) must also be offset when applicable. Verify this match on EVERY removal.
- **Note:** Mangrove/dMRV integration underway; Charm oil CI still calculated via spreadsheet

---

## 6. Emission Factor Reference

| Factor | Mar–Apr 2024 | Jun–Dec 2024 | Apr–May 2025 | Feb–Mar 2026 |
|--------|-------------|-------------|-------------|-------------|
| AECN Process | 89.40 kgCO₂e/t | 126.78 (H2 2024) | 127.04 (H1 2025) | 0.10402 kgCO₂e/kg (Certify precise value; KB previously rounded to 0.10) |
| AECN Embodied | 21.16 kgCO₂e/t | 21.16 | 21.16 | 0.0212 kgCO₂e/kg (Certify precise value; KB previously rounded to 0.02) |
| Tanker Truck Process | 0.08 kgCO₂e/(km·t) | 0.08 | 0.07 | 0.07 kgCO₂e/(km·t) display — **native source value: 0.0001143 MTCO₂e/(t·mi)** |
| Tanker Truck Embodied | 0.0477 kgCO₂e/km | 0.0477 | 0.0490 | 0.1476 kgCO₂e/km (=0.00023756059 MTCO₂e/mi) |
| Rail Process (Fuel Use, Well-to-Wheel) | N/A | N/A | N/A | 0.0000259104 MTCO₂e/(t·mi) (GLEC V3.2 2025) |
| Railcar Embodied | N/A | N/A | N/A | **0.0000311307 MTCO₂e/mi** (GLEC V3.2 2025; per-mile, NOT per-T-mi) |
| Flatbed Process | N/A | N/A | 0.14 kg/(t·mi) | N/A |
| Flatbed Embodied | N/A | N/A | 0.0401 kgCO₂e/km | N/A |
| LCS Embodied | 1,540.65 kg/m³ | 1,540.65 | 1,505.78 | 1,505.78 |
| Charm Production (PP5) | N/A | N/A | 0.73 kgCO₂e/kg | N/A |

**Methodology convention (LOCK THIS IN):**
- **Embodied emissions are always per-mile** (or per-vehicle-lifetime amortized to per-mile). Derivation pattern on the Standard EFs sheet: `total lifetime manufacture EE ÷ EPA useful life miles × deadhead factor → MTCO₂e/mi`. Same shape for tanker truck, non-tanker truck, trailer, and railcar. If a per-T-mi unit ever appears on a vehicle embodied entry, treat it as a sheet typo, not a methodology change.
- **Process emissions are per-T-mi** (fuel use scales with cargo mass × distance).
- This convention exists because manufacturing a vehicle once, then amortizing its embodied burden across its lifetime miles, doesn't depend on what cargo is being carried on any given trip — but the fuel burned on a trip does. There is no transport context where embodied scales with ton-miles.

**Notes:**
- **CRITICAL: Never use Certify's displayed EF values for independent calculations.** Certify rounds/converts EFs for display (e.g., shows "0.07 kgCO₂e/(km·t)" when the native source value is 0.0001143 MTCO₂e/(t·mi)). Always pull the full-precision EF from the Standard Emission Factors sheet and use its native units. Using the rounded display value introduces phantom variances.
- Emission factors have generally remained stable with minor refinements
- Unit conversions standardized over time (lbs → kg, tonne → t)
- **Railcar Embodied updated for 2026** to 0.0000311307 MTCO₂e/mi. Derivation is on the Standard EFs sheet's `2026 Railcar Embodied Emissions` tab: **65.37 MT CTGate** (V17 DOT-111 LCA, full BOM model on the same tab) **÷ 2,100,000 mi expected lifetime** (35 yr × 60,000 mi/yr per Cambridge Systematics) = 0.0000311307 MT/mi. Prior published value 0.0000352240 MTCO₂e/mi is stale; Certify still references the older value as of April 27, 2026 — pending update. Older v8/eGRID-2023 figure of 23.958 MT CO₂e (per-railcar lifetime) is fully deprecated; current methodology is per-mile, not per-railcar amortized.
- **Tanker Truck Embodied EF updated for 2026** from 0.0490 to 0.1476 kgCO₂e/km (confirmed 3/30/26)

### Standard Emission Factors — Live Source (2026)
- **URL:** https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705#gid=684080705
- **Tab:** 2026
- **Status:** In process of being updated for 2026. Use this as the authoritative source for acceptable EFs until fully updated.
- **Added:** March 30, 2026

---

## 7. Service Level Agreements (SLAs) with Isometric

### Current SLA (Established February 17, 2025)
Established after escalation to Eamon.

**Feedback Response Timeline:**
- Acknowledged within 1 working day (may flex to 2 for time zones)
- Substantive response within 5 working days

**Verification Completion:**
- Next two reporting periods: 4 working weeks
- Thereafter: 2 working weeks (target going forward)

**Note:** The 4-week window for early statements may have already passed. Standard expectation is now 2-week turnaround.

### Earlier Proposed Language (August 2024)
- North star: 10 working days
- Formal SLA: 15 working days

### Key Contacts
- **Certify Platform:** Chris Podgorney, Ed Long, Christie Patel, Murtaza Abidi
- **Monitoring/Data:** Tom Sellers, Seb Green

---

## 8. Vaulted KDHE Monitoring

### Permit Details
- **Effective Date:** June 5, 2024
- **Regulator:** Kansas Department of Health and Environment

### Reporting Schedule
- **Monthly Monitoring Reports:** Due 28th of each month
- **Quarterly Emplaced Material Reports:** January, April, July, October
- **Quarterly Groundwater Monitoring:** Quarterly (dates per plan)
- **Elevation Survey:** Every 2 years (next due ~June 5, 2026; report due ~August 4, 2026)
- **Mechanical Integrity Test:** Every 5 years (not due until ~2029)

### Event-Driven Requirements
- **Sonar Survey:** When cavern reaches half full (45 days after)
- **Well Treatment/Workover Plans:** As needed with 10 business day notification
- **Cavern Completion Notification:** 10 business days after completion

### Outstanding Items (December 2025)
Worked through with Tom Sellers and Seb Green:
- Daily cavern pressure data
- Displaced brine stream characterization

### Tracking Document
- **File:** data-analysis/Vaulted_KDHE_Monitoring_Tracker_2026.xlsx

---

## 9. Key Operational Details

### Mass Accounting
- **Conservative Injectate Mass:** MIN(scale ticket net, originating BOL mass)
- Ensures accurate accounting when tickets and BOL may differ

### Basco 6 Operations
- **Standard Sparging Deduction:** 1.29% of injectate mass
- **Rail Spur Emissions:** 1.575 tCO₂e (sitework included in first statements)

### Quality Control Sampling
- **Protocol:** Collect jar sample at each transfer event
- **Analysis:** Sent to SGS for full characterization
- **Key Parameters:** Density, composition, moisture, viscosity
- **Frequency:** Every transfer

### Inventory Management
- **Inventory Reconciliation:** Accounts for outstanding production period oil
- **Tracking:** Production periods and outstanding volumes documented

### Live Data Sources (Google Sheets — do NOT download static copies)

**COBB (Completion of Batch Basis) — Bio-oil Injection Tracker:**
- **URL:** https://docs.google.com/spreadsheets/d/116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q/edit?gid=1627433350#gid=1627433350
- **Tab "Basco Injection -- COBB":** Live tab for current bio-oil injection batches at Basco. **Both truck-delivered AND rail-delivered batches live here** (e.g., 2-182 through 2-185 from railcar GPRX 5188 are in this tab, not the rail-named one below). For rail batches, `consumed_lot` follows the pattern `Rail_<RAILCAR>_<DATE>_offload_N`, `BOL_number` lists all 3 input BOLs, `origin_quantity_kg` is the full railcar mass, and `offloaded_quantity_kg` is this batch's truck-out share.
- **Tab "COBB (with offload info)":** Older / archived tab. Contains only historical entries (max batch ~2-122 / 3-54). Do NOT use for current rail batches. Corrected April 27, 2026 after batch 2-182 training pass surfaced that the rail tab pointer was stale.
- **Key columns:** injection_batch, consumed_lot, BOL_number, offloaded_quantity_kg, order_line_quantity_completed, injection_completion_date, injection_ph
- **Note:** COBB data is maintained in this live tracker, NOT in per-batch Ops Notes. Always reference this sheet for COBB verification.
- **CRITICAL — Navigation:** The "Basco Injection -- COBB" tab contains far more rows than fit in the initial viewport. Data extends well past the first screenful. To find a batch: use the Name Box (top-left cell reference box) to jump to A50, A100, etc., or use Ctrl+F search. NEVER conclude a batch is absent based only on what is visible on screen. The initial viewport typically shows ~24 data rows (up to ~batch 2-146); newer batches require scrolling or direct navigation. If Ctrl+End or scroll fails to move the view, use the Name Box to jump to a specific cell.
- **Added:** March 30, 2026

### QA Output
- **Completed QA checklists** must be saved to a Google Drive folder designated for the current reporting period.
- The folder URL changes each RP — always ask Max which folder to use if not already known for the current period.
- **Current RP folder (3/16/26–3/22/26):** https://drive.google.com/drive/folders/11n-sN6JPCy58t1-zOYOVRxLfGeGJX8dh
- **Added:** March 30, 2026

**Standard Emission Factors + Calculations:**
- **URL:** https://docs.google.com/spreadsheets/d/1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4/edit?gid=684080705#gid=684080705
- **Tab "2026":** Current emission factors for 2026 reporting periods
- **Status:** In process of being updated for 2026. Use as authoritative source for acceptable EFs.
- **Added:** March 30, 2026

---

## 10. QA Checklists (Full Content)

### 10A. Injection Batch QA Checklist

Used per-batch to verify every injection event before submission to Certify/verification.

**Checklist Statuses:** Each checklist item receives one of four statuses:
- **Pass** — Item verified against primary source, no issues. No fill.
- **Fail** — Any issue that would reasonably prevent a removal from being verified if the batch were submitted as-is. This includes: reporting errors, data mismatches, missing required data, and any discrepancy in evidence that contradicts what is being reported (e.g., scale ticket numbers don't match, mass values conflict between sources, emission factors applied incorrectly). **The test is: does the evidence as it stands fully support the reported Net CDR value? If not, it's a FAIL.** Red fill across all columns.
- **Flag** — Process hygiene or documentation issue that does NOT prevent verification. All the information to support the Net CDR calculation is fundamentally present and correct, but something is suboptimal (e.g., a non-descriptive filename, a value outside an expected range that hasn't been statistically validated, a minor labeling inconsistency). The verifier could still verify the removal from the evidence as submitted. Yellow fill (#FFF2CC) across all columns, dark gold font (#996600).
- **N/A** — Item does not apply to this batch (e.g., WODO items for an AECN-only batch). Gray italic, no fill.

**FAIL vs FLAG Decision Rule:** If you are unsure whether something is a FAIL or FLAG, apply this test: *"If a VVB reviewer looked at the evidence for this removal right now, would this issue create a risk of material misstatement or prevent them from confirming the reported value?"* If yes → FAIL. If the information fundamentally supports the claim but has a process or hygiene issue → FLAG.

**Checklist Formatting Rule:** FAIL rows must be highlighted red across ALL columns (A through D). FLAG rows must be highlighted yellow (#FFF2CC) with dark gold font. All other rows (PASS, N/A) must have NO fill — default/no color. Do NOT carry over red/yellow fills from prior batches. Every new batch checklist starts with no fills; only apply red/yellow to rows that fail or are flagged in THAT batch. When clearing fills, clear EVERY column in EVERY non-header data row — not just columns A–C. Verify by auditing every cell in the sheet after applying formatting. Section header rows (blue/yellow/green) are structural and should be preserved.

**Header fields:** Batch ID, Reporting Period, Reviewer, Injection Site (Basco 6), Oil Types in Batch

**1. Batch Folder Completeness**
- Batch folder exists with correct naming (e.g., 2-XXX) [VR Appendix 1]
- Scale Tickets subfolder present and populated [VR Appendix 1]
- Testing subfolder present with all required lab results [VR Appendix 1]
- Ops Notes spreadsheet present and complete [VR Appendix 1]
- Injection site confirmed as Basco 6 — no references to deprecated Vaulted Deep [verify BOLs, Ops Notes, and Certify all reflect Basco]

**2. Scale Tickets & Mass Determination**
- Empty and full scale ticket images present for each truckload/railcar [VR Sec 5.1]
- For each pair: dates within 2 weeks of injection [VR Sec 3.5]
- For each pair: tractor and trailer numbers match between empty and full [VR Sec 5.1]
- Net mass (full minus empty) correctly calculated in Ops Notes [VR Sec 5.1]
- Injectate mass uses conservative value: MIN(scale ticket net, originating BOL mass) [GHG Stmt Sec C]
- 1.29% sparging mass deduction applied to AECN input mass only (Charm WODO and Aqueous do not receive sparging; Aqueous receives LCS pre-treatment instead) [GHG Stmt Sec C]
- All mass values consistent across scale tickets, Ops Notes, and Certify/dMRV entry [VR Sec 5.1]

**3. Bills of Lading (BOL) & Transportation**
- Truck BOL(s) present for each shipment [VR Appendix 1]
- If rail delivery: truck BOLs from AECN present (destination = railyard); standard practice is 3 BOLs per railcar [VR Appendix 1]
- BOL mass matches or exceeds reported injectate mass [VR Sec 3.5]
- Origin and destination correct (AECN→Basco, Charm→Basco, or AECN→SOPOR→Basco for rail) [PDD Sec A]
- Transportation distance consistent with known route. AECN truck route ~2,197 mi (AECN→Basco direct). AECN rail route is THREE legs, not one: AECN→SOPOR (107.5 mi single-truck × 3 trucks = 322.5 mi total trucking) + SOPOR→Opelousas rail leg ~2,199 mi + Opelousas→Basco short-haul truck ~42.9 mi. The 2,199 figure is JUST the SOPOR→Opelousas rail leg, not the full rail route. [Transport Emissions Acctg v1.1]
- Transport mode matches oil type: tanker=AECN truck, railcar=AECN rail, flatbed=Charm/Kerry totes [Certify Datapoints]
- Billing documents present and consistent with BOL shipment details [VR Appendix 1]

**4. Bio-Oil Composition & Testing (CHN / Lab Results)**
- CHN analysis PDF(s) present in Testing subfolder [VR Appendix 1]
- Carbon content (wt%) within expected range: AECN mean = 39.42%, SD = 6.09% (n=285 MRV samples, source: MRV_AECN_Analysis.xlsx, updated March 2026). Flag if value falls outside mean ± 2 SD (i.e., outside ~27.2%–51.6%). Charm varies by production period. [Biomass Feedstock Acctg v1.2]
- Hydrogen and nitrogen values reported and reasonable [Biomass Feedstock Acctg v1.2]
- Lab report references correct batch/sample ID [VR Sec 5.1]
- If aqueous phase: pH/conductivity results present and within permit range [UIC Permit / LDENR]
- Carbon content used in CO2e calculation matches lab report value [VR Sec 5.1]

**5. Ops Notes Accuracy & Internal Consistency**
- Ops Notes has correct batch ID and injection date
- All scale ticket values correctly transcribed into Ops Notes
- If oil and aqueous phases: mass transported, oil disposed, and oil in batch are internally consistent
- COBB values present and match appropriate cells
- pH measurement noted
- Completion date present and matches COBB
- No erroneous density measurements (density only for estimating AECN oil input)

**6a. AECN Feedstock Emissions & Allocation** (Mark N/A if no AECN in batch)
- AECN process emissions LCA CI spreadsheet present [VR Appendix 1]
- LCA with stack emissions file present [VR Appendix 1]
- Supporting GHG data file present for the AECN production period [VR Appendix 1]
- AECN pyrolysis process EF matches current half-year value (current: 0.10402 kgCO₂e/kg in Certify; previously rounded to 0.10) [Certify Datapoints]
- AECN pyrolysis embodied EF applied (current: 0.0212 kgCO₂e/kg in Certify; previously rounded to 0.02) [Certify Datapoints]
- **Mass basis for pyrolysis EFs:** Certify applies pyrolysis EFs to Origin Bio-Oil Mass (pre-sparging), NOT the injectate mass (post-sparging). This is correct — pyrolysis emissions were incurred to produce the full quantity of oil. Verified March 31, 2026 via Certify component inspection (batch 2-166). [Certify Components]

**6b. Charm WODO Emissions** (Mark N/A if no Charm WODO in batch)
- Production Period identified and emission factor (CI) documented
- Charm WODO CI calculated via spreadsheet method (until dMRV integration complete) [GHG Stmt Sec C]
- Production Period production emissions correctly allocated to this batch [Certify Components]
- Flatbed truck transport distance and emissions correctly entered [Certify Datapoints]
- Pre-treatment status: NONE for Charm WODO (no sparging/LCS applied) [VR Sec 3.1]

**6c. Charm Aqueous Emissions** (Mark N/A if no Charm Aqueous in batch)
- Production Period identified and emission factor (CI) documented
- Aqueous CI calculated via same spreadsheet method as WODO [GHG Stmt Sec C]
- Production Period production emissions correctly allocated to this batch [Certify Components]
- Flatbed truck transport distance and emissions correctly entered [Certify Datapoints]
- LCS pre-treatment applied for pH adjustment: LCS mass and CI entered in Certify; aqueous mass adjusted accordingly

**6d. Kerry Oil Emissions** (Mark N/A if no Kerry in batch — methodology under development, do not submit until approved)
- Kerry-specific methodology memo attached and approved (required before proceeding)
- Kerry CI / emission factor documented per approved methodology
- Tote transport (flatbed) distance and emissions correctly entered
- Pre-treatment requirements met per approved methodology (if applicable)

**7. Gross-to-Net Calculation**
- Gross CO2e = injectate mass × carbon wt% (as decimal) × 3.667 [CO2/C molecular weight ratio]; verify units consistent and carbon content as decimal (0.42 not 42) [GHG Stmt Sec E / Bio-oil Geol Storage v1.1]
- Process emissions correctly deducted from gross (all oil types combined) [GHG Stmt Sec E]
- Uncertainty discount correctly applied per Isometric Standard [Isometric Standard v2.0 §3.7]
- Net removals consistent with BCU Quant spreadsheet and GHG Statement [RP BCU Quant.xlsx]

**7a. Per-Component Uncertainty Verification (added April 1, 2026)**

Charm uses Option B (Variance Propagation) per Isometric Standard §3.7.3. Charm reports known measurement uncertainties on individual datapoints within Certify components. Certify's system uses these as inputs to compute the aggregate uncertainty discount via variance propagation. This means the per-component uncertainty inputs are Charm's responsibility to get right — the discount is an output of the system.

**Three-layer verification required:**

**Layer 1 — Completeness:** Every component that requires uncertainty reporting has it, AND the uncertainty is applied to the correct datapoint/sub-component within that component (not all datapoints in a component require uncertainty). Reference: MRV Uncertainty+ Evidence Cheat Sheet.xlsx for the component→datapoint mapping. The PDD Uncertainty Assessment section is the authoritative source for which components are sensitive enough to require uncertainty reporting.

**Layer 2 — Correctness:** The reported uncertainty value on each datapoint matches the expected value. In Certify, uncertainty is displayed next to the reported value with a ± symbol in gray text, between the value and the source link. Some uncertainties are absolute values; others are a percentage of the reported measurement value and must be recomputed to verify. Expected values per component→datapoint:

- Injection Sequestration → Carbon Content: 0.004 × Measured Value (0.4%)
- Injection Sequestration → Mass of Product: 72.57 kg per discrete weight (one vehicle with one load)
- Transport (AECN→SOPOR Tanker, AECN→B6 Tanker, Opelousas→B6 Tanker) → Mass of Load: 72.57 kg per discrete weight (one vehicle with one load)
- Transport (SOPOR→Opelousas Rail) → Mass of Load: published rule is `72.57 kg × number of trucks loaded into the railcar` (per-truck-IN). In practice Charm applies the per-truck-OUT rule (72.57 kg per delivery truck × N trucks-out across the railcar's offloads), which accumulates slightly more uncertainty for the railcar total than the strict in-rule and is acceptable as a conservative choice. For a 3-in / 4-out railcar (typical pattern, e.g., GPRX 5188 → 4 batches), in-rule = 217.71 kg, out-rule = 290.28 kg — Charm uses the latter.
- Transport (all modes) → Distance Traveled: No uncertainty required (use longest Google Maps distance)
- AECN Pyrolysis Process Emissions → Bio-Oil Mass: 72.57 kg per discrete weight (one vehicle with one load)
- AECN Pyrolysis Embodied Emissions → Bio-Oil Mass: 72.57 kg per discrete weight (one vehicle with one load)
- Electricity → Grid Electricity Usage: 0.02 × Measured Value (2%)
- Electricity → Procured Power Electricity Usage: 0.02 × Measured Value (2%)
- Diesel Site Emissions → Mass of Fuel: 0.0129 × Measured Value (1.29%)
- LCS → Mass of LCS: 0.02045 × Measured Value (2.045%)

**Layer 3 — Discount presence and consistency:** The resulting aggregate uncertainty discount (computed by Certify from the above inputs) is present and correctly reflected in net CDR calculations: Gross CO2e → minus process emissions → minus uncertainty discount → Net removal. Verify the discount value is consistent with the GHG Statement Section E.

**8. Data Integrity & Anomaly Check**
- No unexplained outliers in mass, carbon content, or calculated values
- Any spills/losses/irregularities: quantity documented, unrecovered mass deducted, incident report filed [GHG Stmt Sec C]
- If inventory reconciliation applies: carryover oil from prior production periods documented and allocated [VR Sec 3.5]

**9. Isometric Certify — Removal Component Mapping**
- SEQUESTRATIONS: Gross injection sequestration (tCO2e) matches internal gross for total batch [Certify Components]
- REMOVAL ACTIVITIES — Transport: Process + embodied emissions correct for each lot/mode (tanker, railcar, flatbed) [Certify Components]
- REMOVAL ACTIVITIES — Injection: LCS and sample transport emissions correct [Certify Components]
- REMOVAL ACTIVITIES — Pyrolysis: Each oil type has corresponding entry (AECN = "AECN Pyrolysis/Production"; Charm = "(Production Period X)" prefix) [Certify Components]
- REDUCTIONS: All applicable BCU categories populated (5 categories: injection diesel, injection waste, pre-treat diesel, pre-treat waste, transport process) [Certify Components]
- **REDUCTIONS — BCU Quantity Verification:** BCU quantity (tCO₂e) in Reductions MUST equal or exceed the corresponding diesel/process emission (tCO₂e) in Activities. At minimum: transport process BCU (tCO₂e) ≥ transport process activity emission (tCO₂e) for all trucking and rail. Other diesel BCU categories must similarly match or exceed their corresponding activity emissions when present. Check EVERY removal. [Certify Components / Calculation View]
- COUNTERFACTUALS: Baseline correctly computed or zero per protocol [Certify Components]
- Net removal (tCO2e) in Certify matches internal net calculation [Certify Calculation View]
- All Datapoints have corresponding source documents linked with descriptive names (no "Measurement XXXX" or "IMG_001") [Certify Datapoints] — **Generic or non-descriptive filenames are a FLAG, not a FAIL.** This is a process hygiene issue, not a reporting error. Flag the row yellow and note the filename that should be renamed.
- All Sources uploaded to Certify match files in the batch folder on Drive [Certify Sources]

**CRITICAL — Document Location Rule (added April 1, 2026):**
Documents required by VR Appendix 1 (BOLs, billing documents, AECN LCA CI spreadsheets, LCA with stack emissions files, supporting GHG data files) do NOT need to be in the per-batch Google Drive folder if they are uploaded to Certify Sources for the removal. Presence in Certify Sources satisfies the document-presence requirement. When verifying document presence: (1) check the batch Drive folder first, (2) if not found there, check Certify Sources tab, (3) only FLAG/FAIL if the document is absent from BOTH locations. This applies to all items in Sections 1, 3, and 6a that reference VR Appendix 1. Do NOT flag a document as missing solely because it is not in the Drive folder — confirm it is also absent from Certify before flagging. Origin/destination and billing details can likewise be confirmed from BOL documents in Certify Sources.

---

### 10B. Site Emissions QA — Agent Architecture (Updated April 7, 2026)

Site emissions QA is now handled by a dedicated **qa-site-emissions** skill, separate from batch QA. The skill has its own SKILL.md, checklist template, and detailed category evidence guide in `references/category_evidence_guide.md`.

**Scope:** All GHG-related site-level emissions, BCU/REC offset accounting, EF validation, and multi-scapegoat allocation checks.

**Out of scope (future agents):**
- Permanence / non-GHG site monitoring (Basco MRV, wellhead testing, mechanical integrity) → future Monitoring QA agent
- GHG Statement / RP-level consistency rollup → future GHG Statement QA agent
- FAR compliance → future GHG Statement QA agent
- Additional documentation (permits, stakeholder logs) → future GHG Statement QA agent

**Site emission categories (21 sections in checklist):**
1. Diesel — receipts, calc sheet, EF, BCU offset
2. Gasoline — receipts, calc sheet, EF
3. Methanol — consumption + transport (distance, mass, EF)
4. Argon — 3 sub-components: transport process, transport embodied, electricity
5. Electricity — utility readout dates, grid EF, REC offset
6. Brine — totalizer or invoices (Borque/Jula cross-check), transport process + embodied
7. Support Travel — trips, legs, distances, mode EF
8. Embodied — CapEx — CE Inventory, LCA sheets, amortization
9. Embodied — Sitework — materials, processes, EFs, added to CapEx
10. Embodied — SP&C — equipment list, weekly/RP penalties
11. Railcar Cleaning & Transport — per-leg emissions, partial BCU offset
12. Waste Disposal — disposal docs, routing, calc sheet
13. Additional Transport — route evidence, mass, distance, BCU if applicable
14. Pump Oil (conditional) — infrequent consumable purchase
15. LCS (conditional) — currently dormant, historically used
16. Production Reconciliation (conditional) — CI per production period
17. Inventory Reconciliation (conditional) — outstanding quantities, exhausted inventory
18. One-Off / Nonstandard — named subfolders, case-by-case quantification
19. BCU/REC Offsets — BCU Quant sheet reconciliation, EAC inventory
20. EF Validation — spot-check against Standard Emission Factors list
21. Multi-Scapegoat Allocation (if applicable) — total matches evidence, no net-emissive removals

**3-gate system:**
- Gate 1: Evidence folder inventory + folder-to-Certify mapping
- Gate 2: Per-category evidence review + checklist build
- Gate 3: BCU/REC reconciliation + allocation check

**After Gate 3:** Trigger adversarial reviewer (QA type = site_emissions), then performance monitor.

**Certify structure:** Site emissions appear as sub-components under "Removal activities > Bio-oil injection" on the scapegoat removal(s). BCU reductions appear under "Reductions > Bio-oil injection" and "Reductions > Bio-oil transport."

**Multi-scapegoat handling:** When site emissions are too large for one removal (would make it net-emissive), they're spread across 2+ scapegoat removals. QA the total from evidence first, then verify the allocation across removals. Constraint: every removal must remain net-positive.

**Site-specific checklists:** Basco 6 (LA) and Vaulted Deep (KS) have different checklist variants due to different monitoring requirements, permit structures, and operational states (Vaulted is in decommissioning).

For detailed per-category evidence requirements, calc logic, Certify component names, and common failure modes, see `references/category_evidence_guide.md` in the qa-site-emissions skill directory.

---

## 11. Isometric Protocol Modules Summary

**Note:** All modules fully read and analyzed as of March 2026.

### Isometric Standard v2.0 (2026)
- **Materiality Threshold:** 5% (unchanged)
- **Uncertainty Estimates:** ≤16th percentile (conservative) (unchanged)
- **Crediting Period:** 10 years (15 years for BiCRS/DAC) (unchanged from v1.9)
- **VVB Rotation:** Every 5 years (unchanged)
- **Buffer Pool Allocation:** (unchanged)
  - Very Low Risk: 2%
  - Low Risk: 5%
  - Medium Risk: 7%
  - High Risk: 10–20%
- **Assessment Tools:**
  - Appendix B: Uncertainty assessment methodology
  - Appendix C: Risk Reversal Questionnaire (10 questions)
- **Credit Types (NEW in v2.0):** Now issues both Carbon Dioxide Removal credits AND Emission Reduction credits
- **CRCF Section (NEW in v2.0):** Section 6 covers EU Carbon Removal Certification Framework
- **Status:** Published, replaces v1.9

#### Protocol Updating Requirements (CHANGED in v2.0 — Section 2.4)

**CRITICAL: These rules govern when Charm must adopt new protocol/module versions. The v2.0 changes are operationally favorable.**

**Protocol Review Schedule (§2.4.1):**
- Isometric Science Team reviews a Protocol/Module when material changes occur in scientific knowledge, technology, or regulatory frameworks
- Review completed within 6 months from date issue is raised
- Mandatory review triggered at the **sooner** of:
  - 2 years since original Certification; OR
  - Credit issuance milestones: 100,000 / 500,000 / 1,000,000 / 5,000,000 Credits Issued (NEW in v2.0)

**Protocol Adoption Requirements (§2.4.5 — KEY CHANGE):**
- **v1.9 rule (SUPERSEDED):** Minor version releases required adoption within a 12-month window. Major versions adopted at crediting period renewal.
- **v2.0 rule (CURRENT):** Both major AND minor version changes now require adoption only **upon crediting period renewal**. Patch changes take effect automatically.
- **Legacy exemptions:** Projects can request exemption from new requirements if adoption causes "non-trivial operational difficulty"
- **Validation continuity:** Projects retain validation status when adopting new minor versions

**Protocol Backward Compatibility (§2.4.6):**
- Projects are not penalized for protocol updates to previously issued credits
- Backward compatibility mechanisms ensure continuity

**Charm Implication:** When Isometric publishes updated protocol modules (e.g., Bio-oil Geological Storage v1.2, Energy Use Accounting v1.4), Charm no longer faces a 12-month forced adoption window. Adoption aligns with natural crediting period renewal cycles, reducing mid-period disruption.

### Bio-oil Geological Storage Protocol v1.1 (Primary)
- **Core Equation:** CO₂eRemoval = CO₂eStored – CO₂eCounterfactual – CO₂eEmissions
- **Linked Modules:**
  - Energy Use Accounting v1.2
  - Biomass Feedstock Accounting v1.2
- **Applicability:** Charm's primary protocol for all verified statements

### Bio-oil Storage in Permeable Reservoirs v1.1 (Basco 6)
- **Risk Classification:** Low Risk
- **Buffer:** 5%
- **Site:** Basco 6, Louisiana
- **Well Type:** Class II UIC
- **Key Features:** Permeability analysis, pressure management, containment verification

### Bio-oil Storage in Salt Caverns v1.1 (Vaulted Deep)
- **Risk Classification:** Very Low Risk
- **Buffer:** 2%
- **Site:** Vaulted Deep, Kansas
- **Well Type:** Class III UIC
- **Key Features:** Cavern geometry, salt competency, monitoring requirements per KDHE

### Biomass Feedstock Accounting v1.3
- **Eligibility Categories:** SC1–SC7
- **Counterfactual Scenarios:** CC1–CC3
- **Market Leakage:** ML1–ML7
- **Prohibited Feedstocks:** PF1–PF2
- **Key Metrics:**
  - φ_Bio: Utilization rate
  - SUR: Manure utilization equations
  - Industry Residues table for waste wood qualification

### Energy Use Accounting v1.3
- **Equation:** CO₂eEnergy = CO₂eElectricity + CO₂eFuel
- **Facility Classification:**
  - Non-intensive: <200 GWh/year (no buffer adjustment)
  - Intensive: >200 GWh/year (25% buffer applied)
- **EAC Criteria:** EC1–EC6 for low-carbon electricity claims

### GHG Accounting v1.0
- **Scope:** Cross-pathway consequential analysis per ISO 14064-2:2019
- **SSR Categories:** Scope 1, 2, 3 emissions
- **Allocation Procedures:** P1–P4 (mass, energy, economic-based)
- **Worked Examples:** Appendix D with detailed calculations
- **Note:** Deprecated modules (Transportation/Embodied Emissions) merged into GHG Accounting + Energy Use v1.3

### Transportation Emissions Accounting v1.1
- **Methods:**
  - Energy Usage (preferred): Direct fuel data
  - Distance-Based (fallback): kWh/ton-km or equivalent
- **Low-Carbon Fuel Credits:** BCU criteria EC1–EC5
- **BCU Offset Rule:** BCUs represent avoided CO₂e from low-carbon fuel use. BCU quantity (tCO₂e) must equal the transport process emission (tCO₂e) they offset. All transport process emissions for trucking and rail must be fully offset by BCUs on every removal. Verify this match during QA.
- **Mode-Specific EF Age Limits:** 5 years maximum age for published factors

### Biochar Production and Storage v1.0 (OPERATIVE — Charm Co-Product)
> **Version Note:** v1.0 is Charm's operative version per the v2.0 Standard version adoption policy. See Section 1 "Protocol Version Policy" above.

- **Crediting Period:** 15 years (BiCRS Protocol)
- **Core Equation:** CO₂eRemoval,RP = CO₂eStored,RP − CO₂eCounterfactual,RP − CO₂eEmissions,RP (Section 8)
- **Reactor Types:** Fixed-bed, auger, rotary kiln
- **Sampling Requirements:**
  - Method A: Every batch minimum 30 samples
  - Method B: Every 10 batches (less frequent)
- **Conservative Estimation:** Mean minus 1 SEM, outlier winsorization at 3σ
- **Gaseous Emission Routes:** 4 permissible pathways quantified
- **Direct Emissions Quantification:**
  - Option Eq 9: Continuous measurement
  - Option Eq 10: Regular testing protocol
- **Condensable Bio-Oil Fraction:** 3 end-use approaches (combustion, further processing, co-product export)
- **Risk Assessment:** Appendix A Risk of Reversal Questionnaire
- **Section 6.3 Ownership:** Contracts must specify a single project proponent as sole Credit owner, compliant with Isometric Standard Section 3.1
- **Section 6.2.2 Site Visits:** VVB must conduct site visits to biochar application site
- **Section 7.1.1.5 Co-Product Allocation (Procedure 4):** When both biochar and bio-oil are produced for CDR crediting (as Charm does), a carbon mass balance is required to properly allocate emissions and removals between co-products
- **Referenced Modules at Validation:** Embodied Emissions Accounting v1.0, Energy Use Accounting v1.1, Transportation Emissions Accounting v1.0, Biomass Feedstock Accounting v1.2

### Biochar Storage in Agricultural Soils v1.0 (OPERATIVE)
> **Version Note:** v1.0 is Charm's operative version. Note: v1.2 renamed this module to "Biochar Storage in Soil Environments" and broadened scope beyond agricultural land. Charm remains on v1.0 with agricultural-land-only applicability.

- **Applicability (Section 1.1):** Strictly limited to **agricultural land** — defined per FAO as permanent cropland, arable cropland, meadows, and pastureland. Non-agricultural settings (mine reclamation, construction, urban, forestry, etc.) are **explicitly excluded** under v1.0.
- **Risk Classification:** Very Low Risk
- **Buffer:** 2%
- **Elemental Stability Requirements (Section 3.3):**
  - H/C (organic): <0.5 required
  - O/C (organic): <0.2 threshold
  - Random Reflectance R₀: ≥ 2% required
- **Core Equations (Section 4.1.1):**
  - CO₂eStored = C_biochar × m_biochar × F_durable × 44.01/12.01
  - C_biochar = Total Carbon Content − C_inorg (only organic C credited)
- **Data Retention (Section 3.5):** 5-year records retention required
- **PDD Requirements (Section 4.1.2.3):** GPS coordinates, project boundary maps, and application rate must be documented

**Crediting Options:**

**Option 1 (200-year Durability):**
- Model: Woolf et al. 2021 decay curve
- Percentile: 17th (conservative)
- F_durable,200 = min(0.95, 1 − [c + (a + b·ln(T_soil))·H/C_org])
- Coefficients: a = −0.383, b = 0.350, c = −0.048
- T_soil: Direct soil temperature measurement or global database lookup
- Floor: 7°C minimum for calculations

**Option 2 (1,000-year Durability):**
- Model: Sanei et al. 2024 random reflectance/inertinite method
- Benchmark: R₀ ≥ 2% minimum
- Minimum sampling: 500 measurements per batch
- F_durable,1000 = min(0.95, max(0, (R̄₀ − s_R₀)(C̄_non-reactive − s_C_non-reactive)))
- Conservative adjustment: Both reduced by 1 SD

**⚠ Options 1 and 2 CANNOT be combined under v1.0.** Charm must choose one option per crediting period. (Note: v1.2 later allowed combination with temporal or spatial separation, but this is NOT available under v1.0.)

---

### Biochar Production and Storage v1.2 (REFERENCE ONLY — not currently adopted)
> **⚠ This section is retained for reference. Charm operates under v1.0 above. Do not apply v1.2 requirements unless Charm has decided to adopt this version.**

- Same core structure as v1.0 with updates to sampling, emissions quantification, and referenced module versions
- See `isometric-pdfs/Biochar Production and Storage v1.2 — Isometric.pdf` for full details

### Biochar Storage in Soil Environments v1.2 (REFERENCE ONLY — not currently adopted)
> **⚠ This section is retained for reference. Charm operates under v1.0 (Agricultural Soils) above.**

- Key difference from v1.0: Broadened scope from "Agricultural Soils" to "Soil Environments" (includes non-agricultural settings)
- Key difference from v1.0: Options 1 and 2 may be combined with temporal or spatial separation
- See `isometric-pdfs/Biochar Storage in Soil Environments — Isometric.pdf` for full details

### Biochar Characterization & Safety
**Physical & Chemical Parameters (Tables 1–3):**
- Bulk density, pH, ash content, CEC, SBET surface area
- H/C ratio, O/C ratio, total organic carbon
- PAH and heavy metal analysis

**Heavy Metal World Best Class (WBC) Thresholds (g/t DM):**
- Pb: 300 | Cd: 5 | Cu: 200 | Ni: 100 | Hg: 2 | Zn: 1,000 | Cr: 200 | As: 20

**Additional Contaminant Limits:**
- PAH screening required
- PCDD/F: ≤20 ng/kg DM
- PCBs: ≤0.2 mg/kg DM

**Handling & Storage:**
- Stockpiling max 12 months (must be wet/covered/away from water bodies)
- Particle size: ≤10 mm if risk of collection/inhalation during post-deployment use

**Chain of Custody:**
- Unique batch IDs for all production
- 5-year records retention
- Extensive evidence for application/mixing/third-party sales (Appendix II)

---

## 11B. Biochar Project — Registry Data & Verification History (added April 6, 2026)

**Registry URL:** https://registry.isometric.com/project/prj_1JN6XNWDQ1S0BSN7
**Project Name:** Charm Range & Plains Biochar
**Project Code:** 6TMZ
**Status:** VALIDATED
**Verifier:** 350Solutions
**Approval Date:** 04 Aug 2025
**Crediting Period:** 01 Mar 2024 – 01 Mar 2029
**Protocol:** Biochar Production and Storage v1.0 (CCP Accredited)
**Production facility:** Fort Lupton, CO (same Charm pyrolysis operation that produces WODO and Aqueous bio-oil — shared upstream data across pathways)
**Application model — DISTRIBUTED OFFTAKERS:** Charm biochar is sold and delivered to **multiple offtakers across many sites**, not a single canonical application location. Hutchinson, Kansas (37.966°N, -97.941°W) was the *first* verified application site under the registry — by coincidence the same city as the former Vaulted Deep injection partner, but the two are unrelated. The distributed-offtaker model is central to the operational reality of this project and was the core tension in the BSSE v1.2 negotiation (single project proponent / Section 6.3 ownership requirements vs. distributed downstream chain). Any analysis or document that treats Hutchinson as "the" application location is wrong — every offtaker site needs to be tracked individually for chain-of-custody and verification.
**Risk Level:** Very Low (2% buffer)

### Credit Issuances (as of April 6, 2026)

| Date | Issued | Buffer | Supplier Allocation |
|------|--------|--------|---------------------|
| 04 Aug 2025 | 3.52 tCO2e | 0.071 | 3.449 (retired) |
| 02 Feb 2026 | 47.73 tCO2e | 0.962 | 46.768 (active) |
| **Total** | **51.25 tCO2e** | **1.033** | |

### Confirmed Removal Technical Data (rmv_1KCTBYT0D1S0BCPG, 29 Sep 2025)
- **Net CO2e:** 2.228 tCO2e | Sequestrations: 6.937 t | Reductions: 440 kgCO2e | Activities: 5.149 tCO2e
- **F_durable:** 74.73% (Option 1 — Woolf, 200-year)
- **Carbon Content:** 83.8% (mean across samples)
- **H:C Ratio:** 0.457 (below 0.5 threshold)
- **Soil Temperature:** 19.6°C at application site
- **Transport:** 1,515.29 km, 5.368 t load, flatbed truck, 683 kgCO2e process emissions

### Project Documentation (7 docs on registry)
1. 26 Feb 2026 — Project Name Change Confirmation
2. 02 Feb 2026 — Verification Report
3. 02 Feb 2026 — GHG Statement
4. 01 Aug 2025 — Validation & Verification Report
5. 01 Aug 2025 — GHG Statement
6–7. Additional earlier documents (dates TBD from pagination)

### Negotiated Exceptions & Precedents
- **Non-agricultural land use:** Isometric granted an exception allowing biochar crediting for a land remediation project at a mine site, despite v1.0 Storage Module Section 1.1 limiting applicability to agricultural land. This establishes precedent for non-agricultural applications under this project.
- **Flexible storage site identification:** Project was validated with storage sites listed as "presently unknown" and Charm described as "in the process of securing agreements for offtake and storage." Removals were subsequently credited, confirming Isometric accepts site-specific data at the removal verification stage rather than at validation.

---

## 12. Reference Files in Workspace

All files are organized in the MRV Expert workspace folder. See `FOLDER_INDEX.md` at the workspace root for the full folder map.

### Verification & GHG Statements (30 PDFs)
- **Location:** `isometric-pdfs/`
- Numbered 01_ through 30_ (GHG statements, validation reports, and related certifications)
- Span March 2024 – March 2026
- Verifiers: FuturePast, 350Solutions

### Isometric Protocol Modules (12 PDFs)
- **Location:** `isometric-pdfs/`
- Isometric Standard v2.0 (`isometric-standard-v2.0.pdf`) — added March 31, 2026
- Isometric Standard v1.9 (retained for reference)
- Bio-oil Storage in Permeable Reservoirs v1.1 (`Bio-oil Storage in Permeable Reservoirs — Isometric.pdf`)
- Biomass or Bio-oil Storage in Salt Caverns v1.1 (`Biomass or Bio-oil Storage in Salt Caverns — Isometric.pdf`)
- Biomass Feedstock Accounting v1.3 (`Biomass Feedstock Accounting v1.3 — Isometric.pdf`)
- Energy Use Accounting v1.3 (`Energy Use Accounting — Isometric.pdf`)
- GHG Accounting v1.0 (`GHG Accounting v1.0 — Isometric.pdf`)
- Transportation Emissions Accounting v1.1 (`Transportation Emissions Accounting v1.1 — Isometric.pdf`)
- Biochar Production and Storage v1.0 (`Biochar Production and Storage v1.0 — Isometric.pdf`) — **OPERATIVE version** (uploaded April 6, 2026)
- Biochar Storage in Agricultural Soils v1.0 (`Biochar Storage in Agricultural Soils v1.0 — Isometric.pdf`) — **OPERATIVE version** (uploaded April 6, 2026)
- Biochar Production and Storage v1.2 (`Biochar Production and Storage v1.2 — Isometric.pdf`) — reference only, not currently adopted
- Biochar Storage in Soil Environments v1.2 (`Biochar Storage in Soil Environments — Isometric.pdf`) — reference only, not currently adopted
- Biochar Storage in Agricultural Soils v1.1 (`biochar-storage-agricultural-soils-v1.1.pdf`) — added March 31, 2026; reference only

### Operational Tracking Sheets
- **Location:** `batch-qa-checklists/`
- **Injection_Batch_QA_Checklist.xlsx** – Quality assurance for each injection batch
- **Site_Emissions_QA_Checklist.xlsx** – Site-level emissions verification checklist

### Data & Analysis
- **Location:** `data-analysis/`
- **Vaulted_KDHE_Monitoring_Tracker_2026.xlsx** – Kansas regulatory compliance tracking
- **MRV_AECN_Analysis.xlsx** – AECN data analysis
- **Cleaned_MRV_AECN_Data.xlsx** – Cleaned AECN dataset
- **CHN_Summary_Statistics.xlsx** – CHN summary statistics

### Reference Documents
- **Location:** `reference-docs/`
- **Certify_Deep_Dive_Findings.md** – Detailed component structure analysis of Certify platform evolution
- **Charm_CDR_Protocol_Summary.docx** – CDR protocol summary
- **Isometric_Standard_v2.0_vs_v1.9_Comparison.md** – Standard version comparison
- **Charm_Isometric_Knowledge_Base.md** – This file

### QA Configuration & Tracking
- **Location:** `qa-config/`
- **qa_active_batches.json** – Registry of batches awaiting Garrett's response
- **Claude_QA_Performance_Tracker.xlsx** – QA performance metrics
- **Batch_QA_Session_Onboarding_Template.md** – QA session template
- Skill files (.skill) and task configs

### Deliverables
- **Location:** `deliverables/`
- **Charm_Response_to_Isometric_Biochar_v1.2_Review.docx** – Response to Isometric biochar protocol review

---

## 13. Active Scheduled Tasks

### isometric-pdf-monitor
- **Frequency:** Daily at 9:10 AM
- **Action:** Checks Isometric Registry for new protocol PDFs and related documents
- **Download:** Saves to isometric-pdfs folder
- **Notification:** DMs Max on Slack only when new documents are found
- **Purpose:** Keeps knowledge base current with protocol updates

---

## 13A. Data Verification — Hard Rules

These rules exist because of repeated failures where expected data was declared absent due to inadequate navigation, or conclusions were drawn without verifying against primary sources. They are non-negotiable.

1. **Never conclude data is absent without exhausting all navigation methods.** If you cannot find expected data in a Google Sheet, browser page, or any other source, assume operator error first. Try at least 3 different navigation methods (e.g., Ctrl+F, Name Box jump, scrolling, Page Down, arrow keys) before concluding the data does not exist.
2. **Never mark a checklist item as INFO, N/A, or "data unavailable" due to missing data without exhausting all approaches.** If you still can't find it after 3 methods, state exactly which methods you tried and why each failed — do not simply declare the data isn't there.
3. **Google Sheets are larger than they look.** Frozen header rows, filtered views, and large datasets mean the initial viewport is never the full picture. Always navigate beyond what is visible.
4. **If a source is expected to have the data (e.g., COBB tracker should have all injected batches), treat failure to find it as YOUR problem, not a data gap.** Escalate to Max only after genuinely exhausting all options.
5. **Added:** March 31, 2026

### 13A-II. Primary Source Verification Requirement (Added April 6, 2026)

Every checklist item that references a data value MUST be verified by directly opening and reading the primary source document. The number of navigation attempts is irrelevant — what matters is that the stated value was checked against the authoritative source each time, every time. No exceptions.

**Primary sources by checklist area:**
- **Scale ticket values (Section 2):** Open each scale ticket PDF directly (both full and empty). Read tractor number, trailer number, gross weight, and date from the ticket image itself. Do not rely on transcribed values in Ops Notes or Certify alone.
- **COBB tracker values (Section 5):** Navigate to the correct tab in the Bio-oil Injection Tracker and locate the batch row. Read the values from the cells. Do not infer presence or absence from other sources.
- **Uncertainty values (Section 7a):** Open each Certify component detail modal and read the ± values from the INPUTS section. Do not infer from aggregate calculations or assume values match expected. **CRITICAL (2026-04-07): Failure to individually confirm per-component ± values from the Certify UI is a +3 laziness penalty. Using aggregate discount math, KB expected ranges, or any proxy in place of actually opening the modals and reading the values is not acceptable. If a modal will not open, escalate to Max immediately — do not write hedged evidence notes.**
- **Lab results (Section 4):** Open the CHN/CoA PDF and read values from the report page for the specific batch.
- **Certify component values (Sections 7, 9):** Open the Components tab and click into each relevant component. Read values from the modal, not from summary displays.

**The rule:** If your evidence note for any item does not reflect values you personally extracted from the primary source in this session, the item is not verified. Writing "confirmed" or "matches" based on secondhand data, inference, or expectations is a laziness violation (Section 0B).

---

## 13B. Batch QA Slack Workflow

After completing a batch QA checklist:

1. **Adversarial self-review:** Submit findings to a subagent with access to the knowledge base, checklist, and Certify data. The subagent tests each finding against protocol requirements and source data, pushes back on anything fabricated/unsupported/inconsistent. Iterate until error-free.
2. **Slack Max** confirming QA and self-review are complete. Include batch ID.
3. **Max reviews** and provides feedback. Make updates until Max is satisfied.
4. **Once Max approves**, Slack Garrett Lutz. Include batch ID, PASS/FAIL/FLAG/N/A counts, details on each FAIL and FLAG. Tell Garrett to:
   a. Sanity-check the findings and notes
   b. Flag Max with any issues from sanity check
   c. Make any required updates
   d. Comment "Complete" in the thread once updates have been made
   e. A comment of "Complete" will trigger a re-review and QA checklist update
5. **Once Garrett responds "Complete":** Re-open the checklist, batch folder, and Certify entry. Verify corrections have been made. Update the checklist (status, notes, formatting).
6. **Notify Max (two-step: email draft + Slack alert):**
   a. **Create a Gmail draft** (HTML format) to max@charmindustrial.com (do NOT send — Gmail connector cannot send, only draft). The draft should contain: subject line "QA Re-Review: Batch [ID] — [status]" (where status is "All Resolved" or "X of Y Unresolved"), full summary of re-review findings (what was corrected, what remains unresolved with current vs. expected values), recommended next steps, and — critically — a **direct link to the updated QA checklist file** (using `computer:///` protocol pointing to the file in the MRV Expert workspace folder). Max should not have to hunt for the checklist in a folder.
   b. **Send a short Slack DM** to Max (user ID: UL2SL4H5H) alerting him the draft is ready. Keep it brief — just the batch ID, one-line outcome, and a link to the draft in Gmail. Do NOT put the full re-review summary in Slack. Example: "QA re-review draft ready for Batch 2-163 — 1 unresolved item. [View draft](gmail link)"
   This two-step workflow exists because: (1) Slack DMs are too compressed for detailed re-review findings, (2) the Gmail connector lacks send permissions, (3) Max prefers a scannable Slack alert that points to the full email for review and sending.

---

## 14. Connected Services & Integrations

### Communication Platforms
- **Slack** – Charm Industrial workspace + Isometric shared channels
- **Gmail** – Email coordination with verifiers and regulators

### Productivity & Scheduling
- **Google Calendar** – Meeting scheduling and regulatory deadlines
- **Google Drive** – Shared documents and collaborative worksheets

### Project Management & Documentation
- **Atlassian Jira** – Issue tracking and project workflows
- **Atlassian Confluence** – Internal documentation and knowledge sharing

---

## 15. Quick Reference: Key Dates & Milestones

| Date | Event |
|------|-------|
| June 5, 2024 | Vaulted KDHE permit effective date |
| August 5, 2024 | Charm Fort Lupton facility operational (WODO production) |
| August 2025 | Migration from Vaulted Deep to Basco 6 |
| October 2025 | First Charm Aqueous (quench oil) injection |
| February 17, 2025 | Current SLA with Isometric established |
| June 5, 2026 | Vaulted elevation survey due (~) |
| August 4, 2026 | Vaulted elevation survey report due (~) |
| v2.0 | Next Isometric Standard version (pending) |

---

## 16. Operational Principles & Standards

### Verification Confidence
- All 13 GHG statements verified by 350Solutions (except #1 by FuturePast, #2 unsuccessful)
- Conservative estimation methodology applied throughout
- 5% materiality threshold ensures data quality

### Permanence & Risk Management
- Vaulted Deep: Very Low Risk (2% buffer) – salt cavern geological stability
- Basco 6: Low Risk (5% buffer) – permeable reservoir with active monitoring
- Both sites meet Isometric storage module requirements

### Regulatory Compliance
- Vaulted Deep: KDHE Class III UIC monitoring per Kansas regulations
- Basco 6: Class II UIC well operation per Louisiana oversight
- Monthly/quarterly reporting maintained for Vaulted per permit

### Feedstock Quality
- All oils characterized by SGS at transfer events
- Density confirmed >1.01 g/cm³ (formation fluid density) for safe injection
- Production data tracked by period, source, and transport mode

### Emissions Accounting
- Bottom-up calculation: biomass input → pyrolysis → transport → injection → storage
- Conservative factors applied: counterfactual use, market leakage, process losses
- Biochar co-products accounted for separately under Biochar Storage in Soil Environments v1.2

---

## Operational Preferences

### Browser Tab Management
- When opening browser tabs (Claude in Chrome) to do work, **always close them when finished**. Max's browser gets cluttered otherwise. Clean up after yourself.

### Batch QA Workflow
- After completing batch QA, **always save the completed checklist to the Google Drive "Completed QA Sheets" folder**: https://drive.google.com/drive/folders/11n-sN6JPCy58t1-zOYOVRxLfGeGJX8dh
- This is a mandatory final step for every batch QA session — do not consider the QA done until the checklist has been uploaded to Drive.
- **Known limitation:** Claude in Chrome cannot upload files to Google Drive (the "New" button triggers a native file picker that can't be automated). Save the checklist to the MRV Expert workspace folder and flag to Max that manual upload is needed. Do not waste time retrying the Drive upload.

### QA Performance Self-Tracking

**Tracker file:** `Claude_QA_Performance_Tracker.xlsx` in the MRV Expert workspace folder.

After every batch QA, Claude must update this spreadsheet and report its metrics. The trigger for reporting is when **Garrett types "Complete" in the Slack thread** responding to Claude's batch QA completion alert. At that point, the QA cycle is closed and Claude must log the results.

#### CRITICAL: Start Tracking from the Very First Message

Do NOT wait until the end of a QA session to start collecting metrics. The **very first thing** Claude does when Max initiates a batch QA is run `date` to capture the initiation timestamp. Track error counts and iteration rounds in real time as the session progresses. If you reach the end without this data, you cannot reconstruct it — timestamps and iteration counts are not recoverable after the fact.

#### What to Track During Each Batch QA

**Timing — record these timestamps as the QA progresses:**
- **Initiation time:** Run `date` in bash the moment Max kicks off the batch QA. Do this FIRST, before any other work.
- **Completion time:** Run `date` again when Max gives final approval (the message where Max confirms the review is accepted, which precedes Garrett's "Complete").
- Duration is auto-calculated in the spreadsheet (approval time minus initiation time, in hours).

**Error Counting — maintain running tallies throughout the review cycle:**
- **Errors found by Max:** Count each distinct issue Max flags during his review of Claude's QA output. Each round of corrections from Max = count the individual errors he identifies.
- **Errors found by Garrett:** Count each distinct issue Garrett flags (if any) during his review.
- **Laziness rule violations:** Count each instance where Claude failed the exhaustiveness rule (Section 0) — e.g., spot-checked instead of checking every cell, skipped a document, missed a row, summarized instead of verified. These are a subset of total errors but tracked separately.
- **Material errors:** Errors that affect Net CDR calculation (wrong emission factors, incorrect mass values, formula errors in tCO₂e calculations, missed components, wrong batch boundaries, etc.).
- **Non-material errors:** Issues with formatting, clarity, labeling, column headers, cosmetic mismatches, etc. that do not change the CDR number.

**Iteration counting logic:**
- The initial QA submission = iteration 0 (no errors yet counted).
- Each round where Max or Garrett sends back corrections = +1 iteration. Count the individual errors within each iteration.
- If Max sends back 3 issues and then 1 more issue in a follow-up, that's 4 errors found by Max across 2 iterations.

#### Reporting (After Garrett's "Complete")

When Garrett marks the QA complete, Claude must:
1. Update `Claude_QA_Performance_Tracker.xlsx` with the batch row data.
2. Post a brief performance summary in the conversation, covering: batch ID, duration, total errors (split by Max vs. Garrett), laziness violations, material vs. non-material breakdown, and any trend vs. previous batches.

---

## 12. Site Emissions QA — Universal Requirements (added April 8, 2026)

These requirements apply to EVERY category in EVERY site emissions QA. They are not category-specific — they are standards that must be checked exhaustively across the entire checklist.

### 12A. Evidence Chain Completeness

**Every value in Certify must trace to documented evidence.** If a Certify component value cannot be traced to a calc sheet, receipt, or other evidence document, that is a **FAIL** — not a FLAG. FLAGs are for items that are ambiguous or need clarification. Missing evidence is not ambiguous.

Specifically:
- Missing receipts or transaction records for calc sheet entries = **FAIL**
- Certify value that does not match the evidence provided = **FAIL**
- Volume reported in one place, mass in another, with no documented conversion = **FAIL**
- Calc sheet with no supporting source documents = **FAIL**

### 12B. Units on All Labels

**Every label in every calc sheet must include appropriate units.** This is not a category-specific issue — it is a universal requirement for verifier clarity. When reviewing any calc sheet, check that:
- Column headers include units (kgCO₂e, MTCO₂e, gal, kg, mi, t-mi, kWh, etc.)
- Emission factor cells include unit labels
- Total/subtotal rows include units
- Intermediate calculation labels include units

Missing units on labels is a FLAG (non-material, housekeeping) unless it creates ambiguity about what a number represents, in which case it is a FAIL.

### 12C. Distance Evidence for All Transport Calculations

**Every distance used in any transport emission calculation must have source documentation.** This means map screenshots, route documentation, or other verifiable distance evidence for every single route. This applies to:
- Diesel delivery transport
- Methanol transport
- Argon transport
- Brine transport (average distance from two source sites)
- Sitework material delivery distances
- Railcar routes
- Waste disposal transport
- Support travel legs
- Any other distance-based emission calculation

Missing distance source documentation = **FLAG** (or FAIL if the distance is material to the emission calculation).

### 12D. BCU Quant Sheet Cross-Check for All Eligible Components

**Every BCU-eligible emission must be cross-checked against the BCU Quant sheet.** This is not optional and applies to every category that has BCU-eligible transport process emissions:
- Diesel consumption + delivery transport process
- Brine transport process
- Methanol transport process
- Argon transport process
- Railcar transport process (specific legs)
- Waste disposal transport process
- Any other diesel-fueled transport process

For each, verify: (1) the BCU Quant sheet line matches the eligible process emission amount, (2) ONLY process emissions are offset (never embodied), (3) non-eligible emissions (gasoline, SAF, embodied, electricity, disposal acts) are NOT offset.

If the BCU Quant sheet is not yet available, FLAG the item as blocked but still enumerate which components SHOULD be checked once it arrives.

### 12E. Naming Convention Consistency

**Folder names, calc sheet titles, and Certify component names must be consistent** for easy verification. If they diverge (e.g., folder = "Site Ops," calc sheet = "Louisiana Sitework," component = "LA Sitework"), FLAG the inconsistency. The verifier needs to be able to trace from folder → calc sheet → Certify component without confusion.

### 12F. Standard EF Sheet — Correct Year Tab

**Always verify you are referencing the correct year tab** in the Standard Emission Factors sheet. The current RP year determines which tab to use. Cross-check the GREET version cited on the tab (e.g., GREET 2025 for 2026 RP). If the tab cites an outdated GREET version, FLAG it.

### 12G. Certify Output Must Match Evidence

**If the Certify output does not match the calc sheet or evidence, that is a FAIL.** Common scenarios:
- Calc sheet total ≠ Certify component value (entries excluded without explanation)
- Utility readout covers dates outside the RP and the full-period value was used
- Formula error in calc sheet produces wrong output that was uploaded to Certify

The QA agent should not rationalize discrepancies or assume intentional exclusions. If the numbers don't match, FAIL and describe the discrepancy.

### 12H. QA Output Standards

**The QA checklist reflects the agent's own findings only.** Do not include Max's notes to Garrett, process discussion questions, or verbatim quotes from Max's feedback. Max's feedback is for learning universal patterns and improving future performance — it is not content for the checklist. The checklist should read as if the agent found every issue independently.

---

## 13. External-Facing Document Standards (added April 13, 2026)

Briefs, memos, and position papers that reference third-party protocols are **external-facing documents**. Max's and Charm's credibility is on the line with every one. The following rules are mandatory whenever drafting or editing such documents.

### 13A. Protocol Claims Must Be Source-Verified

Every factual claim about a third-party protocol — every cell in a comparison table, every inline reference — must be traceable to a specific section and page of the source document. Before writing a claim into a draft:

1. Open or fetch the actual protocol document (not a summary, blog post, or press release).
2. Locate the specific section that supports the claim.
3. Record the section number, page number, and the protocol's own language.
4. If the claim cannot be sourced, do NOT write it into the document. See Rule 13D.

### 13B. Use the Protocol's Own Normative Language

Standards use precise normative terms: **shall**, **must**, **should**, **may**, **is permitted to**, **is required to**. These words have specific compliance meanings:

- **"shall" / "must"** = mandatory requirement. Never downgrade to "encouraged," "recommended," or "suggested."
- **"should"** = recommended but not mandatory. Never upgrade to "required."
- **"may"** = optional. Never characterize as a requirement.

When summarizing a protocol requirement in a comparison table or narrative, preserve the strength of the original normative language. Mischaracterizing "shall" as "encouraged" changes the meaning entirely and undermines the credibility of the analysis.

### 13C. Context Matching for Comparison Tables

When mapping a source-document provision to a comparison-table category:

1. Read the provision in its full context (surrounding paragraphs, the section it belongs to, any qualifying language).
2. Confirm it addresses the **same concern** as the table row. A "signed agreement" about credit ownership is not the same as an "affidavit" about end use — even though both involve signatures.
3. Never slot a provision into a table row based on keyword matching alone.

### 13D. When You Can't Find the Most Relevant Section

For every cell in a comparison table, you must identify the single most relevant section of the source protocol. If you cannot find it after a thorough search:

1. **Do NOT fill the cell with a guess or approximation.**
2. **Do NOT leave it blank and move on.**
3. **Do present Max with a summary of what you DID find** — the closest sections, what they say, and why none of them is a clean match for the claim.
4. **Ask Max to review and direct you.** Finding the right provision is your job, but you are welcome to ask for help or guidance when needed. You are never allowed to leave a job half-done.

### 13E. Confirming Absence

Before claiming a protocol does NOT require something (e.g., "No GPS vehicle tracking required"), search the full document for **all related terms** — not just the exact phrase. For a claim about geotagging, search: geotag, geotagged, georeference, georeferenced, GPS, photo, photograph, photographic, image, evidence, location, coordinates. Cite what you actually find, even if it supports the claim. If a related provision exists (e.g., geotagged photos listed as one option among several), describe it accurately — do not claim absence.

### 13F. No Absolutist Claims Beyond Your Evidence Base

Never make universal claims ("no other protocol," "every methodology," "none of them") when you have only reviewed a limited set of comparators. You know what the documents you read say. You do not know what every protocol in the market says. Scope every claim to the evidence you actually have:

- ~~"No other protocol prescribes physical storage conditions."~~ → **"None of the three comparator protocols prescribes physical storage conditions."**
- ~~"Every major integrity body has concluded…"~~ → **"Across these three comparators, the pattern is consistent…"**
- ~~"This is the approach used by every other CCP-approved methodology."~~ → **"This is the approach used by all three comparator methodologies reviewed here."**

False confidence in universal claims is worse than saying nothing. If someone at Isometric can name one protocol that contradicts a universal claim, the entire brief loses credibility. Scoped claims based on named comparators are stronger because they are verifiable.

### 13G. Version Accuracy

Always confirm and cite the correct version number of the protocol being referenced. If the body text references v1.2 but the Sources section cites v1.1, that is an error that will be caught by a careful reader. Cross-check version numbers between the summary, comparison tables, narrative, and sources section before finalizing.

---

**End of Knowledge Base**

For questions or updates, contact Max Lavine (max@charmindustrial.com).
