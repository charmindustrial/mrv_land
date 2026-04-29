# AECN Injection Batch QA Checklist — Item-by-Item Reference

This document provides the complete specification for every checklist item in an AECN-only batch QA: what to check, which primary source to open, what values to extract, expected ranges, and common failure modes.

**Scope:** AECN oil batches only — both **truck** (direct AECN→Basco) and **rail** (AECN→SOPOR truck → SOPOR→Opelousas rail → Opelousas→Basco truck) delivery modes. No WODO, Aqueous, or Kerry items.

---

## Rail vs Truck Batch Reference (read first if QA'ing a rail batch)

Every section below has truck-batch defaults. Where rail batches differ, look for the **🚂 Rail** note inline in that section. The high-level differences are:

| Aspect | Truck batch | Rail batch |
|---|---|---|
| Delivery legs | 1 (AECN → Basco) | 3 (AECN→SOPOR truck, SOPOR→Opelousas rail, Opelousas→Basco truck) |
| Transport components in Certify | 2 (process + embodied) | **6** (process + embodied per leg) |
| BOLs | 1 per shipment | **3 BOLs IN to SOPOR** + scale tickets at offload truck-out |
| Authoritative mass source | BOL "Qty Shipped" page 3 | **Scale tickets at the offload truck-out** (each delivery truck weighed at Basco) |
| Offload truck count | 1 | Typically **4 trucks OUT** per railcar (varies) |
| Pyrolysis component names in Certify | `AECN Pyrolysis Process/Embodied Emissions` | `AECN pyrolysis (from rail loads) - process/embodied emissions` (signal to VVB) |
| Distance evidence | Google Maps (longest route) | **Email/written confirmation from rail logistics provider** (e.g., Watco). No Google Maps for rail. |
| Distance value applied to rail components | N/A | **Allocated distance** = full leg × upstream allocation fraction. Full SOPOR→Opelousas ≈ 2,199 mi. |
| Sister batches | None | **2-185 sister batches share a railcar** (typically 4 batches per railcar, e.g. 2-182/183/184/185 from GPRX 5188). Upstream allocation fractions across sisters should sum to ≈ 1.0. |
| Ops Notes filename | `2-XXX Ops Notes` | `2-XXX Ops Notes Rail` |
| Ops Notes shape | Single batch table | `Batch Composition` + `BOLs Loaded` (3 input BOLs) + 4-row offload table with `Upstream Allocation` fractions and pre-allocated distances |
| COBB tab | `Basco Injection -- COBB` | **`Basco Injection -- COBB`** (same tab — `COBB (with offload info)` is archived). `consumed_lot` follows `Rail_<RAILCAR>_<DATE>_offload_N`. `origin_quantity_kg` = full railcar mass; `offloaded_quantity_kg` = this batch's truck-out share. |

---

## Section 1: Batch Folder Completeness

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 1.1 | Batch folder exists with correct naming (e.g., 2-XXX) | Google Drive | Folder named with batch ID | Naming inconsistent |
| 1.2 | Scale Tickets subfolder present and populated | Drive > batch folder | Subfolder with full+empty PDFs | Subfolder empty or missing one ticket |
| 1.3 | Testing subfolder present with all required lab results | Drive > batch folder | CHN/CoA PDF(s) from SGS | Wrong batch's lab results |
| 1.4 | Ops Notes spreadsheet present and complete | Drive > batch folder | Google Sheet with all sections filled | Ops Notes partially complete |
| 1.5 | Injection site confirmed as Basco 6 — no references to Vaulted | BOLs, Ops Notes, Certify | All docs say Basco/Evangeline Parish | Legacy Vaulted references not cleaned up |

**Verifier reference:** VR Appendix 1

**Document location rule applies:** Documents may be in Drive OR Certify Sources. Only FAIL if absent from BOTH.

**🚂 Rail:** Ops Notes filename will be `<batch> Ops Notes Rail` (e.g., `2-182 Ops Notes Rail`). Item 1.4 should accept either filename pattern. Scale Tickets subfolder will contain N truck-out PDFs (typically 4) — one full + one empty per offload truck delivery, NOT per inbound shipment. Item 1.2 expects multiple PDF pairs.

---

## Section 2: Scale Tickets & Mass Determination

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 2.1 | Empty and full scale ticket images present for each truckload | Certify Sources or Drive Scale Tickets subfolder | Both PDFs readable with clear values | Only one ticket present, or image unreadable |
| 2.2 | Dates within 2 weeks of injection | Scale ticket PDFs | Date on tickets within 14 days of Ops Notes injection date | Stale tickets from prior shipment |
| 2.3 | Tractor and trailer numbers match between empty and full tickets | Scale ticket PDFs | Same tractor # and trailer # on both | Mismatch = different vehicle weighed = FAIL |
| 2.4 | Net mass correctly calculated in Ops Notes | Ops Notes vs scale tickets | Full gross - Empty gross (lbs) matches Ops Notes | Transcription error, wrong conversion |
| 2.5 | Injectate mass uses conservative value: MIN(scale ticket net, BOL mass) | Ops Notes, BOL | Smaller of the two used | Wrong mass selected |
| 2.6 | 1.29% sparging deduction applied | Ops Notes | Sparging loss = injectate x 0.0129 | Wrong sparging rate, or sparging not applied |
| 2.7 | All mass values consistent across scale tickets, Ops Notes, Certify | All sources | Values agree within rounding | Mass in Certify doesn't match Ops Notes |

**Verifier references:** VR Sec 5.1, GHG Stmt Sec C

**MANDATORY VERIFICATION SUB-TASK (2.1-2.3):** Open BOTH scale ticket PDFs. Read tractor #, trailer #, gross/tare, date from the image. Do not rely on Ops Notes alone.

**Key formula:** Net mass (kg) = (Full gross lbs - Empty gross lbs) / 2.20462

**AECN-specific notes:**
- Sparging is standard for AECN at Basco (1.29% deduction)
- Density field in Ops Notes Batch Composition is expected to be blank for AECN
- Row 14 in the template checks tractor and trailer NUMBERS matching — not weights. This has been confused before.

**🚂 Rail:**
- Items 2.1–2.3 apply to **each offload truck-out delivery** (typically 4 trucks-out per railcar). Expect N pairs of empty/full scale tickets (one pair per delivery truck), not 1.
- Item 2.5 (conservative MIN(scale net, BOL mass)) is replaced for rail: **scale tickets at the offload truck-out are authoritative for this batch's mass.** BOL conservativeness applies to the inbound 3-BOL aggregate vs. railcar received mass, not to the per-batch offload delivery.
- Mass chain to verify: sum of offload truck-out scale-ticket nets across N trucks for THIS batch = `offloaded_quantity_kg` in COBB = `Cargo Mass (kg)` in Ops Notes offload row = "Mass of Load" in Certify (allocated rail components). All four should agree within rounding.
- Sparging (1.29%) still applies — deducted from this batch's offload mass to get injectate mass.

---

## Section 3: Bills of Lading & Transportation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 3.1 | Truck BOL(s) present for each shipment | Drive or Certify Sources | At least 1 BOL per truck shipment | BOL missing from both Drive and Certify |
| 3.2 | If rail delivery: truck BOLs from AECN present (destination = SOPOR railyard) | Drive or Certify Sources | 3 BOLs per railcar | Wrong destination, missing BOLs |
| 3.3 | BOL mass matches or exceeds reported injectate mass | BOL page 3 "Qty Shipped" | BOL mass >= injectate mass | BOL mass < reported injectate |
| 3.4 | Origin and destination correct on BOL | BOL | AECN Quebec -> Basco, or AECN -> SOPOR -> Basco (rail) | Wrong origin/destination |
| 3.5 | Transportation distance consistent with known AECN route | Certify Datapoints | AECN truck ~2,197mi; AECN rail ~2,199mi | Distance significantly off |
| 3.6 | Transport mode = tanker truck or railcar (AECN modes) | Certify Datapoints | Tanker truck (direct) or railcar (via SOPOR) | Wrong mode recorded |
| 3.7 | Billing documents present and consistent with BOL | Drive or Certify Sources | Billing matches BOL shipment details | Billing for different shipment |

**Verifier references:** VR Appendix 1, VR Sec 3.5, PDD Sec A, Transport Emissions Acctg v1.1

**BOL authoritative mass:** Page 3, "Qty Shipped" field. (Rail: see 🚂 Rail note below — BOLs document the inbound side; offload mass authority is scale tickets.)

**AECN transport modes:**
- Direct truck: Tanker truck, AECN Quebec → Basco, ~2,197 mi, 1 BOL
- Rail: 3 truck legs total. AECN→SOPOR (≈107.5 mi single-truck × 3 trucks = 322.5 truck-mi total) + SOPOR→Opelousas (≈2,199 rail-mi) + Opelousas→Basco (≈42.9 truck-mi)

**🚂 Rail:**
- Item 3.1 expects 3 BOLs (AECN→SOPOR inbound), not 1. Each ~26 MT. Sum across 3 BOLs ≈ 78 MT total railcar load.
- Item 3.2 must verify destination on each of the 3 BOLs is **SOPOR railyard**, not Basco.
- Item 3.3 (BOL mass ≥ injectate): apply at the **railcar level** — sum of 3 BOL masses ≥ railcar received mass per Loads tab. NOT at the per-batch offload level (an offload is a fraction of the railcar).
- Item 3.4 origin/destination expectations: 3 BOLs at AECN→SOPOR + railcar inbound record AECN→Opelousas (Loads tab) + offload work order Opelousas→Basco. All three legs must be documented somewhere in Drive or Certify Sources.
- Item 3.5 distance: don't apply the 2,197 mi truck route to a rail batch. The 2,199 mi figure is **just the SOPOR→Opelousas rail leg**, not the full route. Rail components in Certify use **allocated distance** = full leg × this batch's upstream allocation fraction (e.g., 2199 × 0.2757 = 606.24 mi for 2-182).
- Item 3.6 mode: expect **6 transport components** in Certify (truck process+embodied for AECN→SOPOR and Opelousas→Basco; rail process+embodied for SOPOR→Opelousas), not 2.
- Item 3.7 billing: rail logistics provider (Watco) email or invoice is acceptable distance/route evidence. **There is no Google Maps for rail** — emails from the carrier are the authoritative source.

---

## Section 4: Bio-Oil Composition & Testing

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 4.1 | CHN analysis PDF(s) present in Testing subfolder | Drive > Testing | SGS Certificate of Analysis PDF | Wrong batch's lab report |
| 4.2 | Carbon content within expected AECN range | CHN PDF | Mean = 39.42%, SD = 6.09% (n=285). Flag if outside ~27.2%-51.6% | Outlier not flagged |
| 4.3 | Hydrogen and nitrogen values reported and reasonable | CHN PDF | Values present and within normal ranges | Values missing |
| 4.4 | Lab report references correct batch/sample ID | CHN PDF | Batch ID on certificate matches QA batch | Report for different batch |
| 4.5 | pH/conductivity (aqueous phase) | N/A for AECN | **Mark N/A** — AECN is not aqueous phase | Agent incorrectly checking pH here (pH is in Ops Notes, Section 5.5) |

**Verifier references:** VR Appendix 1, Biomass Feedstock Acctg v1.2, VR Sec 5.1

**AECN carbon content stats:** From MRV_AECN_Analysis.xlsx (n=285 MRV samples, updated March 2026). The 2-SD range (~27.2%-51.6%) is the flag threshold, not a hard pass/fail boundary.

**Note:** Carbon content used in the CO2e calculation (checked in Section 7) must match the lab report value here. Cross-reference.

---

## Section 5: Ops Notes Accuracy & Internal Consistency

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 5.1 | Correct batch ID and injection date | Ops Notes | Matches batch being QA'd | Wrong batch ID in header |
| 5.2 | All scale ticket values correctly transcribed | Ops Notes vs scale tickets | Values match ticket images | Transcription error |
| 5.3 | Oil and aqueous phase mass reconciliation | N/A for AECN | **Mark N/A** — AECN-only batches have no aqueous phase | |
| 5.4 | COBB values present and match | COBB tracker vs Ops Notes | origin_qty, BOL_number align | COBB row not found or values differ |
| 5.5 | pH measurement noted | Ops Notes > Batch Consumables | pH value present | pH missing — **pH is required for ALL batches including AECN** |
| 5.6 | Completion date present and matches COBB | Ops Notes vs COBB | Same date in both | Date mismatch |
| 5.7 | No erroneous density measurements | Ops Notes > Batch Composition | **Mark N/A** — density field is expected to be blank for AECN | Agent incorrectly flagging blank density as an issue |

**MANDATORY VERIFICATION SUB-TASK (5.4, 5.6):** Navigate to COBB tracker, verify cell A = batch ID before reading any values.

**CRITICAL — pH:** pH is required for ALL batches regardless of oil type. The agent has previously invented a rule that pH doesn't apply to AECN. It does. Find it in Ops Notes Batch Consumables section.

**CRITICAL — Density:** For AECN, the density field in Ops Notes Batch Composition IS expected to be blank. Mark 5.7 as N/A with note "Density field blank for AECN — expected behavior."

**🚂 Rail:**
- Item 5.4 (COBB lookup): rail batches are in **`Basco Injection -- COBB`** tab (NOT `COBB (with offload info)` — that tab is archived, max batch ~2-122). Find the row by `injection_batch` = target batch ID. Expected fields:
  - `consumed_lot` follows pattern `Rail_<RAILCAR>_<DATE>_offload_N` (e.g., `Rail_GPRX 5188_2.27.26_offload_1`)
  - `BOL_number` lists all 3 input BOLs as a comma-separated string (e.g., `2310-R, 2312-R, 2313-R`)
  - `origin_quantity_kg` = **full railcar mass** (e.g., 78,020 kg), shared across all sister batches
  - `offloaded_quantity_kg` = **this batch's truck-out share** (NOT the full railcar)
  - `quantity_consumed_in_injection` should equal `offloaded_quantity_kg` for the per-batch row
- Item 5.6 (completion date): COBB `injection_completion_date` should match Ops Notes injection date AND Certify removal date.
- Item 5.2 (transcription): the rail Ops Notes' offload table has multiple rows (one per delivery truck-out). Verify only the populated row(s) for THIS batch's offload number — unpopulated rows are zero by design and not a problem.
- The Loads tab (same workbook as COBB) holds the railcar inbound record: carrier (e.g., Watco), asset ID (e.g., GPRX5188), receive/dwell dates, total MT, work order matching `Rail_<RAILCAR>_<DATE>`. Cross-reference for completeness.

---

## Section 6: AECN Feedstock Emissions & Allocation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 6.1 | AECN process emissions LCA CI spreadsheet present | Certify Sources tab | Document present (check Sources tab, not just Datapoints) | Not checking Sources tab |
| 6.2 | LCA with stack emissions file present | Certify Sources tab | Document present | Same as above |
| 6.3 | Supporting GHG data file present for AECN production period | Certify Sources tab | Document present | Same as above |
| 6.4 | AECN pyrolysis process EF matches current value | Certify Datapoints | 0.10402 kgCO2e/kg (precise) / ~0.10 (display) | Wrong half-year EF, or using display value |
| 6.5 | AECN pyrolysis embodied EF applied | Certify Datapoints | 0.0212 kgCO2e/kg (precise) / ~0.02 (display) | Missing embodied EF entirely |
| 6.6 | Mass basis for pyrolysis EFs is Origin Bio-Oil Mass (pre-sparging) | Certify Components | EF applied to pre-sparging mass | EF applied to post-sparging mass (wrong) |

**Verifier references:** VR Appendix 1, Certify Datapoints, Certify Components

**Document location rule applies to 6.1-6.3.** Check Drive first, then Certify Sources. Only FAIL if absent from BOTH.

**On 6.6:** Pyrolysis EFs should be applied to the Origin Bio-Oil Mass (the mass produced by pyrolysis, before sparging deduction at the injection site). This is correct because the emissions were incurred to produce the full quantity. Verified March 31, 2026 via batch 2-166.

**EF precision:** Certify may show rounded values (0.10, 0.02). The precise values from the Standard EF Sheet are 0.10402 and 0.0212 respectively. Verify against the Standard EF Sheet, not the Certify display.

**🚂 Rail:**
- Pyrolysis component naming on rail batches is `AECN pyrolysis (from rail loads) - process emissions` and `... embodied emissions`. Items 6.4 and 6.5 should accept either the truck-batch naming (`AECN Pyrolysis Process/Embodied`) OR the rail-batch naming. Same EFs apply. The naming difference is a deliberate signal to the VVB to expect scale tickets as the authoritative mass source.
- Item 6.6 (mass basis = pre-sparging Origin Bio-Oil Mass): on rail batches, "Origin Bio-Oil Mass - AECN via Rail" datapoint should be **this batch's offloaded mass before sparging**, NOT the full railcar mass. Sparging deduction (1.29%) is applied at injection per offload, on this batch's share only.

---

## Section 7: Gross-to-Net Calculation

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 7.1 | Gross CO2e = injectate mass x carbon wt% (decimal) x 3.667 | Independent calc vs Certify | Match within rounding | Carbon % not as decimal (42 vs 0.42), unit mismatch |
| 7.2 | Process emissions correctly deducted | Certify Calculation View | AECN pyrolysis + transport deducted | Missing a component |
| 7.3 | Uncertainty discount correctly applied | Certify Calculation View | Present per Isometric Standard | Discount missing |
| 7.4 | Net removals consistent with BCU Quant and GHG Statement | Certify vs BCU Quant | Values align | Discrepancy |

**Verifier references:** GHG Stmt Sec E, Bio-oil Geol Storage v1.1, Isometric Standard v2.0 S3.7

**Formula verification:** Gross = mass_tonnes x carbon_decimal x 3.667. Always verify units are consistent (kg in -> kg CO2e, or tonnes in -> tCO2e). Carbon content must be a decimal (0.4140, not 41.40).

---

## Section 7a: Per-Component Uncertainty Verification

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 7a.1 | Layer 1 — Completeness: every AECN component has uncertainty on correct datapoint | Certify component modals + MRV Uncertainty Cheat Sheet | All required components have +/- values | Missing uncertainty on a component |
| 7a.2 | Layer 2 — Correctness: reported +/- matches expected value | Certify component modals (INPUTS section) | See Uncertainty Reference in SKILL.md | Wrong value, or value not actually checked |
| 7a.3 | Layer 3 — Discount presence and consistency | Certify Calculation View vs GHG Statement | Aggregate discount present in net calc | Discount missing or inconsistent |

**MANDATORY VERIFICATION SUB-TASK:** Open EACH component modal. Read the +/- from INPUTS section. Do not infer from aggregate calculations. +3 laziness penalty for avoidance.

**AECN components requiring uncertainty verification:**
- Injection Sequestration (Carbon Content + Mass of Product)
- Transport Process — AECN->Basco Tanker or AECN->SOPOR + Rail + Opelousas->Basco (Mass of Load per leg)
- AECN Pyrolysis Process Emissions (Bio-Oil Mass)
- AECN Pyrolysis Embodied Emissions (Bio-Oil Mass)

**🚂 Rail uncertainty methodology:**

**Core principle — per-removal framing.** A removal accounts only for the oil used in that removal — not the full railcar, not another batch's slice (sole exception: removals burdened by site emissions). For an AECN rail batch, the removal's mass is fixed by ONE outbound discrete weight at the Basco offload (one full + one empty scale ticket = one weighing event). Therefore Mass-of-load uncertainty on EVERY leg — AECN→SOPOR truck, SOPOR→Opelousas rail, Opelousas→Basco truck — is **±72.57 kg** for the removal. This is the correct value regardless of how many BOLs went IN to the railcar or how many trucks came OUT across all sister batches.

- Per-leg expected Mass-of-load uncertainty: ±72.57 kg per offload removal on each transport component (truck and rail alike). One outbound weighing → one discrete weight → 72.57 kg.
- Embodied components (Truck Embodied AECN→SOPOR, Rail Embodied SOPOR→Opelousas, Truck Embodied Opelousas→Basco) **do not have a Mass of Load datapoint** — embodied is per-mile, not per-T-mi (see KB Section 6 methodology). No mass-uncertainty input expected on embodied components. Don't FLAG missing mass uncertainty on embodied components.

**Conservatism precondition (N_offloads ≥ N_inbound_BOLs).** Because Charm rail movements typically discharge in MORE trucks than they're loaded with (e.g., 3 in / 4 out for a typical AECN railcar), the per-offload framing is automatically conservative on transport uncertainty: summed across sister batches, total mass uncertainty booked to the railcar's emissions = N_offloads × 72.57 ≥ N_inbound_BOLs × 72.57 = the inbound-weighing uncertainty the rail leg would otherwise carry. The verifier sees more mass uncertainty than the inputs strictly required — favorable conservatism.

If a railcar instead drew down in FEWER offloads than the BOLs loaded into it (N_offloads < N_inbound_BOLs), per-offload accounting would book LESS mass uncertainty than the inbound weighings produced — a deficit that must be made up by widening the discount. **The check for this lives in Section 8 🚂 Rail (last batch of railcar).** Don't validate per-offload uncertainty in Section 7a without confirming Section 8's last-batch railcar verification has been performed (or scheduled, if this batch isn't yet the last on its railcar).

---

## Section 8: Data Integrity & Anomaly Check

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 8.1 | No unexplained outliers in mass, carbon content, or calculated values | All sources | Values within expected AECN ranges | Outlier not investigated |
| 8.2 | Any spills/losses documented, unrecovered mass deducted, incident report filed | Ops Notes, batch folder | If spill occurred: documented and deducted | Spill not deducted from mass |
| 8.3 | If inventory reconciliation: carryover oil documented | Reconciliation spreadsheet | If multi-period allocation: documented | N/A for most single-batch AECN |

**Verifier reference:** GHG Stmt Sec C, VR Sec 3.5

**🚂 Rail:**
- Sister-batch sanity check: this batch's `Upstream Allocation` fraction in the Ops Notes offload table = `offloaded_quantity_kg` / `origin_quantity_kg` from COBB. Sum of allocation fractions across all populated sister-batch offload rows for the same railcar should ≈ 1.0 (small rounding OK; significantly less than 1.0 = oil left in railcar that should be documented).
- Cross-reference sister batches via shared `consumed_lot` prefix `Rail_<RAILCAR>_<DATE>_offload_*` in COBB. Verify no offload-N collision (each offload number used once per railcar).
- If `origin_quantity_kg` in COBB ≠ sum of 3 input BOL masses ± rounding, FLAG (likely a transcription error; for GPRX 5188: 3 BOLs at 26.01 + 26.00 + 26.01 = 78.02 MT exactly).
- **Last batch of railcar — N_offloads ≥ N_inbound_BOLs check (gates 7a per-offload uncertainty conservatism).** Identify whether this batch is the *last* batch on its railcar by inspecting its Ops Notes offload table: a railcar is fully drawn down when the running balance hits 0 or a residual that could only be documented loss (typically `Oil Left in Railcar (MT)` ≈ 0 or small documented loss; populated offload rows sum to ≈ Total Loaded Mass). On the last batch, count populated offload rows in the offload table and the BOL Number rows in the BOLs Loaded section:
    - **N_offloads ≥ N_BOLs** → per-offload uncertainty framing (±72.57 kg per removal on each leg, see Section 7a) is conservative ✓ — PASS.
    - **N_offloads < N_BOLs** → summed per-offload uncertainty < inbound-weighing uncertainty the rail leg actually carried; the variance propagation is under-discounted by (N_BOLs − N_offloads) × 72.57 kg. **FLAG to the user to review uncertainty discounting** for the railcar's removals and confirm the discount is widened to absorb the deficit.
    - If this batch is NOT the last batch on the railcar (running balance > documented-loss residual), defer this check until the railcar's final batch QA. Note in the checklist that the precondition for Section 7a's per-offload framing is pending verification.

---

## Section 9: Isometric Certify — Removal Component Mapping

| Item | Check | Primary Source | Expected | Common Failure |
|------|-------|---------------|----------|----------------|
| 9.1 | SEQUESTRATIONS: Gross injection sequestration matches internal gross | Certify Components | One sequestration entry for the AECN batch | Sequestration value wrong |
| 9.2 | ACTIVITIES — Transport: Process + embodied correct for AECN route | Certify Components | Tanker truck (direct) or tanker + rail (via SOPOR) | Wrong mode or missing a leg |
| 9.3 | ACTIVITIES — Injection: LCS and sample transport correct | Certify Components | Samples for MRV (<1 kgCO2e typically) | Often N/A for pure AECN (no LCS needed) |
| 9.4 | ACTIVITIES — Pyrolysis: AECN production process + embodied entries present | Certify Components | "AECN Production Process Emissions" + "AECN Production Embodied Emissions" | Missing one of the two |
| 9.5 | REDUCTIONS: All applicable BCU categories populated | Certify Components | 5 categories: injection diesel, injection waste, pre-treat diesel, pre-treat waste, transport | Missing BCU category |
| 9.6 | REDUCTIONS — BCU quantity >= corresponding activity emission | Certify Components + Calculation View | Transport BCU >= transport activity (at minimum) | BCU underfunding a category |
| 9.7 | COUNTERFACTUALS: Zero per protocol | Certify Components | 0 | Non-zero counterfactual |
| 9.8 | Net removal matches internal calculation | Certify Calculation View | Agrees with independent gross-to-net | Discrepancy |
| 9.9 | All Datapoints have descriptive source names | Certify Datapoints | No "Measurement XXXX" or "IMG_001" | Generic names = FLAG (not FAIL) |
| 9.10 | All Sources match files in batch folder on Drive | Certify Sources vs Drive | Same files in both | File in one but not the other |

**Verifier reference:** Certify Components, Certify Datapoints, Certify Sources, Certify Calculation View

**On 9.3 for AECN:** AECN oil does NOT require LCS pre-treatment (that's for Aqueous). Mark LCS items as N/A if no LCS was used. Sample transport emissions are typically present but small (<1 kgCO2e).

**On 9.5:** Zero-value BCU Datapoints (derived zeros) have no sources — this is expected, not an error.

**On 9.6:** BCU QA rule — BCU quantity (tCO2e) in Reductions MUST equal or exceed the corresponding diesel/process emission (tCO2e) in Activities. Check EVERY removal.

**On 9.9:** Generic/non-descriptive filenames are a FLAG with yellow fill, not a FAIL. The content is correct; the naming is a hygiene issue.

**🚂 Rail:**
- Item 9.2 (Activities — Transport): expect **6 components**, not 2: AECN→SOPOR Tanker Truck (Process + Embodied), SOPOR→Opelousas Rail (Process + Embodied), Opelousas→Basco Tanker Truck (Process + Embodied). Missing any of the 6 = FAIL.
- Item 9.4 (Activities — Pyrolysis): naming is `AECN pyrolysis (from rail loads) - process emissions` and `... embodied emissions` for rail batches. Same EFs as truck batches; the naming is a deliberate VVB signal. Accept either form.
- Item 9.5 (Reductions — BCU categories): for typical AECN batches without site-emission burdens, only `BCU's Transport` category applies. Other categories (injection diesel, injection waste, pre-treat diesel, pre-treat waste) appear only when removals are burdened with site emissions. Don't FAIL on missing categories absent a site-emission allocation.
- Item 9.6 (BCU ≥ activity): rail batches: BCUs offset transport **process** emissions only. Embodied emissions are NOT BCU-eligible (per protocol). Verify `BCU's Transport` quantity ≥ sum of three transport-process activities (AECN→SOPOR truck process + SOPOR→Opelousas rail process + Opelousas→Basco truck process). For 2-182: 1.594 = 0.264 + 1.225 + 0.105 = 1.594 ✓.
- Rail embodied EF: Standard EFs sheet 2026 value is **0.0000311307 MTCO₂e/mi** (per `2026 Railcar Embodied Emissions` tab: 65.37 MT CTGate ÷ 2.1M mi lifetime). If Certify shows the older 0.0000352240 value instead, that's a stale-EF FAIL on item 9.2 (Activities — Transport). Same shared datapoint feeds rail process components on multiple removals — a fix at the source datapoint propagates.
- Rail process EF: Standard EFs sheet 2026 value is **0.0000259104 MTCO₂e/(t·mi)** (= 0.0259 kgCO₂e/(t·mi) shown in Certify modal — matches).
- Item 9.10 (Sources match Drive): rail batches have additional source files vs truck batches — typically the rail logistics provider's email/invoice for distance, the railcar inbound documentation, the offload work order. Cross-reference against the Sources tab enumeration (per Gate 1's SOURCES TAB FIRST RULE).
