# SAF Methodology Session Handoff — 2026-06-18

## What we're building

A bespoke SAF credit methodology for Charm Industrial's bio-oil as a refinery co-processing feedstock. The credit framework is:

- **Registry**: 123 Carbon
- **Reporting standard**: SFC MBM (SFC-SPEC-001 v01, Oct 2024)
- **Upstream CDR methodology**: Isometric (already validated for Charm's biochar CDR pathway)
- **Bolt-on novel steps**: RSB normative references for the refinery co-processing and CI quantification steps

The methodology covers a 15-step production chain from biomass qualification through SAF credit retirement. The deck laying out each step with its normative reference is built and current.

---

## Completed deliverable

**File**: `outputs/mrv-operational-documents/SAF_Methodology_Normative_References_Deck.pptx`
**Build script**: `.claude/_scratch/build_saf_deck.py`

The deck is a 16-slide .pptx (title + 15 step slides). Each step slide has: normative reference (left column), what it is (right top), why it's being used (right bottom). Color coding: blue = Isometric existing CDR, orange = bolt-on novel, green = 123 Carbon/SFC MBM.

---

## The 15 steps and their normative references

### Steps 1–6, 10 — Existing CDR Methodology (Isometric)

**Step 1: Biomass Qualification**
- Biomass Feedstock Accounting v1.3, §2 (Sustainability Criteria SC1–SC7)
- Biomass Feedstock Accounting v1.3, §3 (Counterfactuals CC1–CC3 — wildfire feedstocks = CC2 zero counterfactual)
- Biomass Feedstock Accounting v1.3, §4 (Market Leakage)

**Step 2: Biomass Sourcing and Collection**
- Biomass Feedstock Accounting v1.3, §2.1 + Appendix 1 (monitoring plan — origin records, harvest authorization, mass)
- RSB-STD-03-001 v3.2, §A.5 (zero-emission treatment for waste/residues up to collection — bolt-on citation for the zero-upstream-CI premise)

**Step 3: Biomass Transport to Conversion Site**
- Transportation Emissions Accounting v1.1, §3.2 (Energy Usage Method — preferred: CO2e = F × EF)
- Transportation Emissions Accounting v1.1, §3.3 (Distance-Based Method — fallback: CO2e = D × W × EF)
- Transportation Emissions Accounting v1.1, Appendix 1 (EF currency: road max 3 yr, rail max 7 yr, full fuel cycle required)

**Step 4: Biomass Conversion (Pyrolysis)**
- Biochar Production and Storage v1.2, §9 (Pyrolysis Reactor System — acceptable technologies)
- Biochar Production and Storage v1.2, §10 (Emissions Testing — stack and non-condensable gas)
- Biochar Production and Storage v1.2, §11 (Condensable bio-oil fraction — volume measurement and quality)
- Energy Use Accounting v1.3, §4–§6 (facility energy: electricity §5, stationary fuel §6, CO2e_Energy aggregation §4)

**Step 5: Allocation of Tree-to-Gate Emissions to Co-Products**
- GHG Accounting v1.0, §6.1 (Co-product Emissions Allocation — four procedures)
- Biochar Production and Storage v1.2, §8.6.5.4 (energy content allocation — the BiCRS Protocol's specified method)
- ISO 14040:2006 / ISO 14044:2006 (LCA allocation principles — crosswalk reference)

**Step 6: Bio-Oil Transport to Refinery**
- Transportation Emissions Accounting v1.1, §3.3 (Distance-Based — AECN rail + Opelousas–Basco truck)
- Transportation Emissions Accounting v1.1, Appendix 1 (rail EF currency: max 7 yr)
- ISO 14083:2023 (GHG quantification for transport chain operations — external normative anchor)

**Step 10: Transport of Fuel(s) to Blend Point**
- Transportation Emissions Accounting v1.1, §3.2–§3.3 (same framework as Steps 3 and 6)
- Transportation Emissions Accounting v1.1, Appendix 1 (pipeline, ship, road guidance)
- ISO 14083:2023

### Steps 7–9, 11–12 — Bolt-On Novel (RSB / ISCC)

**Step 7: Refinery Co-Processing**
- RSB-STD-01-010 v2.8, §2.4 (co-processing documentation: mass balance §2.4.3, radiocarbon §2.4.4, flexible attribution §2.4.5)
- RSB-STD-03-001 v3.2, §B.10 (co-processing GHG calculation)

**Step 8: Allocation of Marginal Refinery Emissions**
- RSB-STD-01-010 v2.8, Annex IV formula [4] (AF = LHV_af ÷ Total energy output)
- RSB-STD-03-001 v3.2, §B.10 (emission intensity calculation)

**Step 9: Allocation of Biogenic Carbon Credit to SAF**
- RSB-STD-01-010 v2.8, §2.4.5 + Annex IV [1]–[3] (flexible/free attribution — operator designates which output receives biogenic credit)
- ISCC PLUS 203-2 v1.1, §6.2 (free attribution guardrails: chemical connectivity required, credits cannot exceed physical output)

**Step 11: Quantification of Tree-to-Wheel CI**
- RSB-STD-03-001 v3.2, §B.1 (well-to-wake formula: E = eec + el + ep + etd + eu)
- RSB-STD-03-001 v3.2, §A.1 / §A.5 / §A.10 (functional unit, EF hierarchy, GWP AR5: CO₂=1, N₂O=265, CH₄=28)

**Step 12: GHG Reductions vs. Fossil Baseline**
- RSB-STD-03-001 v3.2, §A.9 + Table 2 (savings formula; fossil comparator = 90 gCO₂eq/MJ)
- RSB-STD-03-002 v2.1 (fossil fuel baseline — aviation kerosene)

### Steps 13–15 — 123 Carbon / SFC MBM

**Step 13: Verification**
- SFC-SPEC-001 v01, §6.1.2 + §12 (third-party assessment — 350Solutions qualifies; §6.1.2 requires only "independent third-party," no ISO accreditation mandated)
- ISO 14064-3:2019 (GHG statement verification standard)

**Step 14: Credit Issuance**
- SFC-SPEC-001 v01, §5–§6 (Sustainability Profile §3.25: lifecycle GHG EFs, LHV, feedstock type, production process, batch ID)
- 123 Carbon registry protocols (credit format, unique ID, anti-double-counting ledger)

**Step 15: Credit Delivery, Retirement, Integrity**
- SFC-SPEC-001 v01, §4 + §6.1.3 (accounting principles; §6.1.3 = binding disclosure obligation for non-certified Solutions)
- 123 Carbon protocols (retirement, transfer chain, anti-double-counting)

---

## Key technical facts established in prior sessions

### SFC MBM (SFC-SPEC-001 v01)
- §6.1: ISCC and RSB are named certified schemes; non-certified Solutions fall under §6.1.2
- §6.1.2: tracking system "shall be transparent and verifiable"; "should be" a third-party registry OR internal ledger covered by independent third-party assessment → 350Solutions assurance statement satisfies this
- §6.1.3: binding obligation for non-certified Solutions to disclose underlying calculations, data sources, production processes in the buyer's Report
- §12: Report verification is optional

### Isometric module structure
Four cross-pathway accounting modules (apply to ALL CDR projects):
1. **Biomass Feedstock Accounting v1.3** — feedstock eligibility, counterfactuals, market leakage
2. **Transportation Emissions Accounting v1.1** — all transport legs, two calculation methods
3. **GHG Accounting v1.0** — overarching framework, co-product allocation, ISO 14064-2:2019 aligned
4. **Energy Use Accounting v1.3** — electricity and stationary fuel at project facility

One pathway-specific protocol (Charm's CDR methodology):
- **Biochar Production and Storage v1.2** — the BiCRS Protocol (NOT "BSSE"; BSSE = Biochar Storage in Soil Environments = irrelevant storage module referenced within this protocol). Covers pyrolysis reactor, emissions testing, bio-oil fraction guidance, co-product allocation.

### RSB key facts
- **RSB-STD-01-010 v2.8 Annex IV**: three-step flexible attribution calculation
  - Formula [1]: Output_eligiblecarbon = m_eligible_f × Carbon_content × ηCi
  - Formula [2]: TS_adv,fuel = Output_eligiblecarbon × (1 ÷ carbon fraction)
  - Formula [4]: WtG_adv,fuel = (WtG_eligible_f × m_eligible_f + WtG_inputs × AF) × (1/TS_adv,fuel)
  - Formula [5]: AF = LHV_af ÷ Total energy output
- **RSB-STD-03-001 v3.2 Table 1**: economic allocation mandatory at pyrolyzer for RSB-certified fuels (not binding for Charm's non-certified track, but disclose to verifiers)
- **RSB Global GHG threshold**: 65% savings vs. 90 gCO₂eq/MJ → must be ≤31.5 gCO₂eq/MJ (standard); ≤45.0 gCO₂eq/MJ (transitional 2026)
- **RSB CORSIA threshold**: 10% savings vs. 89 gCO₂eq/MJ → ≤80.1 gCO₂eq/MJ
- At 0.8 tCO₂e/t bio-oil CI: RSB Global fails even transitional threshold (45.3 gCO₂eq/MJ upstream alone); CORSIA passes easily (22.8 gCO₂eq/MJ)

### ISCC PLUS 203-2 v1.1 §6.2 — free attribution guardrails
- Chemical connectivity between input and designated output required
- Credited volume cannot exceed physical output
- Mass balance is site-specific

---

## Key source files

| Document | Local path |
|---|---|
| Biomass Feedstock Accounting v1.3 | `knowledge-base/isometric-pdfs/Biomass Feedstock Accounting v1.3 — Isometric.pdf` |
| Transportation Emissions Accounting v1.1 | `knowledge-base/isometric-pdfs/Transportation Emissions Accounting v1.1 — Isometric.pdf` |
| GHG Accounting v1.0 | `knowledge-base/isometric-pdfs/GHG Accounting v1.0 — Isometric.pdf` |
| Energy Use Accounting v1.3 | `knowledge-base/isometric-pdfs/Energy Use Accounting — Isometric.pdf` |
| Biochar Production and Storage v1.2 | `knowledge-base/isometric-pdfs/Biochar Production and Storage v1.2 — Isometric.pdf` |
| RSB-STD-01-010 v2.8 | `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/SAF FCC/RSB/Global Advanced Fuel Certification docs/rsb-std-01-010-rsb-standard-for-advanced-fuels-2.8.pdf` |
| RSB-STD-03-001 v3.2 | `~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/SAF FCC/RSB/Global Advanced Fuel Certification docs/rsb-std-01-003-01-v3.2.pdf` |
| SFC-SPEC-001 v01 | `.claude/_scratch/SFC_MBM_Specification.txt` |
| ISCC PLUS 203-2 v1.1 | `.playwright-mcp/ISCC-PLUS-203-2-Chain-of-Custody-v1-1.pdf` |

Prior session handoffs with full RSB/ISCC technical detail:
- `outputs/mrv-operational-documents/RSB_Session_Handoff_2026-06-01.md`
- `outputs/mrv-operational-documents/ISCC_RSB_CORSIA_Session_Handoff_2026-06-02.md`

---

## What's done / what's next

**Done:**
- 15-step normative reference deck built and correct
- All five Isometric modules read in full; module names confirmed from source
- RSB Annex IV flexible attribution formulas established
- ISCC PLUS 203-2 free attribution guardrails established
- SFC MBM non-certified track path confirmed (350Solutions viable)

**Possible next steps (Max to direct):**
- Worked CI example: plug Charm's actual bio-oil CI numbers into the Annex IV three-step formula
- Draft the methodology write-up document (prose version of the deck)
- Double-counting analysis: structure the CDR vs. SAF boundary to prevent simultaneous crediting
- 123 Carbon intake: understand what their proprietary protocol requires for novel FCC pathways
