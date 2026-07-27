# RSB Certification Session Handoff — 2026-06-01

## Purpose
This document captures everything accomplished in the 2026-06-01 session so the next session can continue without context loss. The outstanding task is building a scenario matrix comparing RSB Global and RSB ICAO CORSIA certification pathways.

---

## Source Documents (all open in Preview on Desktop)

| Document | Location | Key pages |
|---|---|---|
| RSB Principles & Criteria (RSB-STD-01-001) | `~/Desktop/RSB-Principles-and-Criteria.pdf` | 15-17 (Criterion 3.b thresholds, Criterion 3.c transitional pathway) |
| RSB Standard for Advanced Fuels v2.8 (RSB-STD-01-010) | `~/Desktop/rsb-std-01-010-v2.8.pdf` | 8-9 (§2.1.1 RSB P&C applicability); 26-29 (Annex IV formulas [1]-[8]) |
| RSB GHG Calculation Methodology v3.2 (RSB-STD-03-001) | `~/Desktop/rsb-std-01-003-01-v3.2.pdf` | 15-17 (Table 1 allocation; Table 2 fossil comparators) |
| RSB ICAO CORSIA v1.6 (RSB-STD-12-001) | `~/.../MRV Expert/.playwright-mcp/rsb-std-12-001-corsia-v1.6-real.pdf` | 14-16 (co-processing §3.4.5; energy allocation §3.4.7) |
| ICAO CORSIA LCA Methodology V8 (November 2025) | `~/.../MRV Expert/.playwright-mcp/corsia-lca-methodology-v8.pdf` | Chapter 6, ~p.123 (marginal approach for co-processing) |
| RSB Standard for Advanced Fuels v2.8 (Google Drive original) | `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/SAF FCC/RSB/Global Advanced Fuel Certification docs/rsb-std-01-010-rsb-standard-for-advanced-fuels-2.8.pdf` | |
| RSB GHG Methodology v3.2 (Google Drive original) | `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/SAF FCC/RSB/Global Advanced Fuel Certification docs/rsb-std-01-003-01-v3.2.pdf` | |
| RSB P&C (Google Drive original) | `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/SAF FCC/RSB/Global Advanced Fuel Certification docs/RSB-Principles-and-Criteria.pdf` | |

Text extractions (pdftotext, used for quote verification) are in `.playwright-mcp/`:
- `rsb-std-01-010-text.txt`
- `rsb-std-01-003-01-text.txt`
- `rsb-std-12-001-corsia-text.txt`
- `rsb-pc-text.txt`
- `corsia-lca-v8-text.txt`

---

## Work Accomplished This Session

### 1. RSB Project Plan v2.0
**File:** `outputs/mrv-operational-documents/Charm_RSB_Global_Certification_Project_Plan.docx`

Built from scratch using python-docx. Contains:
- Three Critical Open Items (OCI-1: GUI-01-013-01 scope; OCI-2: GUI-PG-2025-02 scope; OCI-3: refinery certification)
- Part 2: Full forestry residue feedstock requirements from RSB-GUI-01-013-01 and its Annex 1 (all 9 verification indicators, soil sensitivity matrix, no-go areas)
- Part 4: GHG framework including corrected Annex IV three-step flexible attribution calculation
- Part 7: Complete requirements checklist
- Part 8: Risk register

**Known corrections needed in the plan (not yet applied):**
- Section 4.5 (co-product allocation): currently says energy OR market value. Must be corrected to economic allocation only (market value) per RSB-STD-03-001 Table 1.
- Section 4.6 (GHG savings threshold): currently cited as "STD-01-003-01 v3.2 Table 2." Must be re-cited to RSB P&C Criterion 3.b (65% minimum), applying via STD-01-010 §2.1.1.
- The plan does not yet mention the transitional pathway (Criterion 3.c) or RSB CORSIA as a separate scheme consideration.

The build script (`/tmp/build_rsb_plan_v2.py`) was lost when temp files were cleared. Would need to be rebuilt from the saved .docx if edits are required.

### 2. RSB Global vs. CORSIA Comparison Document
**File:** `outputs/mrv-operational-documents/RSB_Global_vs_CORSIA_Attribution_Comparison.docx`

Covers: scheme overview, attribution mechanisms, worked example, strategic implications, primary source citations. This is the primary output from the CORSIA comparison work.

---

## Key Technical Findings (all sourced this session)

### GHG Thresholds

**RSB Global Advanced Fuels:**
- Standard requirement (Criterion 3.b, RSB P&C p.15): **65% minimum savings** for installations starting from 1 January 2021
- Fossil comparator (STD-03-001 Table 2): **90 gCO2e/MJ**
- Threshold: **≤31.5 gCO2e/MJ**
- Applies to RSB Global via STD-01-010 §2.1.1: "With the exception of Principle 6 and Principle 8, the RSB Principles & Criteria [RSB-STD-01-001] and related documents shall apply to any processing facility from the first collector onwards."

**Transitional pathway (Criterion 3.c, RSB P&C p.16-17):**
- Available until 1 January 2035; requires public roadmap + annual audits
- For installations starting from 1 January 2021: 50% by 2025, 60% by 2030, 65% by 2035
- 2026 transitional threshold: **≤45.0 gCO2e/MJ**

**RSB ICAO CORSIA:**
- Minimum: 10% reduction (RSB-STD-12-001, confirmed in text)
- Fossil comparator (STD-03-001 Table 2): **89 gCO2e/MJ**
- Threshold: **≤80.1 gCO2e/MJ**

### Attribution Method Differences

**RSB Global — Flexible Attribution (Annex IV, STD-01-010 v2.8):**
- Step 1: Output_eligiblecarbon = m_eligible_f × Carbon_content × ηCi [formula [1]]
- Step 2: TS_adv,fuel = Output_eligiblecarbon × Output_Carboncontent (= 1 ÷ carbon fraction) [formula [2]]
- Step 3: WtG_adv,fuel = (WtG_eligible_f × m_eligible_f + WtG_inputs × AF) × (1/TS_adv,fuel) [formula [4]]
- AF = LHV_af / Total energy output [formula [5]] — AF ≈ 2% for SAF in large refinery
- **Key: full bio-oil upstream (WtG_eligible_f × m_eligible_f) charged directly to TS_adv,fuel with no energy allocation discount**
- Operator freely designates which output receives biogenic credit

**RSB ICAO CORSIA — Mass Balance + Marginal Approach:**
- Bio-based proportion = material-specific conversion factor (§3.4.5.5); cannot transfer sustainability characteristic across material types
- "All the changes in energy use and emissions are then allocated to renewable fuel production" (ICAO LCA V8 Ch.6)
- Energy allocation among renewable fuel products (§3.4.7.1)
- **Key: bio-oil upstream spread across ALL bio-derived outputs by energy fraction**
- No free designation of output stream

### Co-Product Allocation at Charm's Pyrolyzer

**RSB Global:** Economic allocation (mandatory). STD-03-001 Table 1: "Economic allocation shall be applied to RSB GLOBAL Advanced Fuels despite the energy nature of some of the products involved."
- Split between bio-oil and biochar based on market prices
- High biochar price → more burden on biochar → lower bio-oil CI

**CORSIA:** Energy allocation (mandatory per §3.4.7.1): "energy-based allocation shall be used to assign emission burdens to all co-products in proportion to their contribution to the total energy content (measured as lower heating value) of products and co-products."

### Worked Example — 100 MT Bio-oil (5% of 2,000 MT FCC feed), 45% C, 0.8 tCO2e/t CI

**Assumptions (must be verified with actual refinery data):**
- ηCi = 0.80
- Total SAF from refinery = 400 t (20% of feed)
- Other renewable fuels from bio-oil = 60 t at avg 44,000 MJ/t
- 0.8 tCO2e/t assumed to be post-economic-allocation at pyrolyzer

| | RSB Global | CORSIA |
|---|---|---|
| Eligible SAF volume | **40.9 t** (free designation) | **20 t** (5% material-specific) |
| Bio-oil upstream per MJ SAF | **45.3 gCO2e/MJ** (full 80 tCO2e ÷ 40.9 t) | **22.8 gCO2e/MJ** (24.7% × 80 tCO2e ÷ 20 t) |
| GHG threshold | ≤31.5 gCO2e/MJ (standard) / ≤45.0 gCO2e/MJ (transitional 2026) | ≤80.1 gCO2e/MJ |
| Pass/fail at 0.8 tCO2e/t | **FAIL both** (45.3 > 45.0 before processing/transport) | **PASS** (22.8 << 80.1) |
| Max permissible bio-oil CI | ~0.38 tCO2e/t (assuming 10 gCO2e/MJ for other terms) | ~2.45 tCO2e/t (effectively non-binding) |

**Critical open question:** Is 0.8 tCO2e/t bio-oil pre or post economic allocation at pyrolyzer? If pre-allocation and biochar has higher market value, the actual RSB-compliant CI could be substantially lower — potentially enough to pass.

---

## Outstanding Task: Scenario Matrix

Max asked for a scenario matrix that sums up the RSB Global vs. CORSIA comparison. This should be the first task in the next session.

Suggested dimensions for the matrix:
- Scenario axis: RSB Global (standard) / RSB Global (transitional) / RSB ICAO CORSIA / RSB ICAO CORSIA + RSB P&C tier 2
- Variable axis: bio-oil CI at different economic allocation assumptions (pre-allocation, post-allocation at 3 price ratios)
- Output: eligible SAF volume, GHG intensity, pass/fail vs. threshold, max permissible CI

All formulas and source citations are in `outputs/mrv-operational-documents/RSB_Global_vs_CORSIA_Attribution_Comparison.docx`.

---

## Other Corrections Still Needed in Project Plan

1. Plan Part 4.5: Change "Energy allocation OR market value" to "Economic allocation (market value) only" — RSB Global biofuels mandatory per STD-03-001 Table 1
2. Plan Part 4.6: Re-source GHG savings threshold to RSB P&C Criterion 3.b (via STD-01-010 §2.1.1), not STD-01-003-01 Table 2
3. Plan: Add Criterion 3.c transitional pathway as a risk/option
4. Plan: Add RSB ICAO CORSIA as a distinct scheme (separate from RSB Global) with commercial implications

---

## RSB Document Number Note
RSB-STD-01-003-01 v3.2 (old number) = RSB-STD-03-001 v3.2 (new number as of February 2026). The file in the Drive folder still uses the old name. Both refer to the same GHG Calculation Methodology document.
