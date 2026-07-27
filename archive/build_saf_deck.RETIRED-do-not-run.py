#!/usr/bin/env python3
"""Build SAF Methodology Normative References deck."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

OUT = "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/mrv-operational-documents/SAF_Methodology_Normative_References_Deck.pptx"

# Color palette
NAVY    = RGBColor(0x1F, 0x36, 0x64)
BLUE    = RGBColor(0x2E, 0x75, 0xB6)   # Existing CDR / Isometric
ORANGE  = RGBColor(0xC0, 0x60, 0x20)   # Bolt-On (novel methodology)
GREEN   = RGBColor(0x37, 0x86, 0x3C)   # 123 Carbon
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
DARK    = RGBColor(0x1A, 0x1A, 0x1A)
LGRAY   = RGBColor(0xF4, 0xF6, 0xF9)
MGRAY   = RGBColor(0xD0, 0xD5, 0xDE)
TGRAY   = RGBColor(0x55, 0x65, 0x75)
LBLUE   = RGBColor(0xBF, 0xD7, 0xED)

OWNER_COLOR = {'isometric': BLUE, 'bolton': ORANGE, '123carbon': GREEN}
OWNER_LABEL = {
    'isometric': 'Existing CDR Methodology',
    'bolton': 'Bolt-On — Novel',
    '123carbon': '123 Carbon',
}

STEPS = [
    {
        'num': 1,
        'name': 'Biomass Qualification',
        'owner': 'isometric',
        'refs': [
            ('Biomass Feedstock Accounting v1.3, §2.1 — Sustainability Criteria', 'SC1–SC7, feedstock-type-specific; reviewed every Reporting Period'),
            ('Biomass Feedstock Accounting v1.3, §2 — Prohibited Feedstocks', 'Categorical gate: food/feed crops and purpose-grown BiCRS feedstocks have no path through the Module'),
            ('Biomass Feedstock Accounting v1.3, §4 — Market Leakage Emissions', 'Sourcing-driven market-shift assessment; valid 10 years'),
            ('Charm PDD v1.12, §B — Project Eligibility', 'Validated precedent for Charm\'s CDR project'),
        ],
        'what': [
            'Three eligibility gates from BFA v1.3, all source-agnostic: (1) Sustainability Criteria SC1–SC7 (§2.1), feedstock-type-specific, reviewed every Reporting Period; (2) Prohibited Feedstocks — categorically ineligible regardless of other criteria; (3) Market Leakage (§4), sourcing-driven market-shift assessment valid 10 years',
            'Prohibited Feedstocks gate, verbatim: "food / feed crops and purpose grown BiCRS feedstocks ... have no path through the Module." Counterfactual Storage (§3) is the one gate excluded — it removes the durably-stored fraction from crediting, a removals concept with no role in a fuel-displacement claim',
        ],
        'why': [
            'Every eligibility gate except counterfactual storage carries into the SAF claim; the gates are source-agnostic, so SAF qualification sits on the same footing as the CDR claim without being tied to one validated source',
            'Charm\'s CDR project already cleared these same gates under the PDD, so qualification is established precedent — the SAF claim reuses the determination rather than re-running it',
        ],
    },
    {
        'num': 2,
        'name': 'Biomass Sourcing and Collection',
        'owner': 'isometric',
        'refs': [
            ('Biomass Feedstock Accounting v1.3, §2.1 + Appendix 1', 'Monitoring-plan requirements: feedstock origin, harvest authorization, species, mass per batch'),
            ('Charm PDD v1.12, §B — Monitoring Plan', 'Validated precedent: the same traceability framework already applied for Charm\'s CDR project'),
            ('RSB-STD-03-001 v3.2, §A.5', 'Zero-emission treatment for waste and residues up to point of collection (bolt-on citation)'),
        ],
        'what': [
            'BFA v1.3 §2.1 and Appendix 1 set the monitoring-plan framework: records of feedstock origin, harvest authorization, species, and mass for each supply-chain batch — source-agnostic, not tied to one biomass source',
            'Collection-stage emissions are zero: wildfire fuel-reduction biomass qualifies as a waste/residue, and RSB §A.5 explicitly states "Waste and residues shall be considered to have zero emissions up to the process of collecting those materials"',
        ],
        'why': [
            'The monitoring-plan framework is reusable for the SAF claim; Charm\'s CDR project already runs this traceability under the PDD, so no new sourcing documentation is needed',
            'Zero collection-stage emissions are the upstream CI floor; RSB §A.5 provides the external normative text confirming this treatment is standard across certification systems',
        ],
    },
    {
        'num': 3,
        'name': 'Biomass Transport to Conversion Site',
        'owner': 'isometric',
        'refs': [
            ('Charm PDD v1.12, §B — Project Boundary & Monitoring Plan', 'As-validated transport legs and emissions monitoring to the conversion site'),
            ('Underlying: Transportation Emissions Accounting v1.1, §3.2–§3.3', 'Energy Usage Method (preferred): CO2e = F × EF; Distance-Based (fallback): CO2e = D × W × EF'),
            ('Transportation Emissions Accounting v1.1, Appendix 1', 'EF currency: road max 3 yr, rail max 7 yr; full fuel cycle required'),
        ],
        'what': [
            'The PDD sets the project boundary and monitoring plan for the truck and rail legs to the conversion site; the underlying Transportation module gives the two calculation methods — Energy Usage preferred, Distance-Based fallback',
            'Appendix 1 sets EF currency rules by mode: road EFs no older than 3 years, rail no older than 7 years; EFs must cover combustion plus upstream fuel production (well-to-wheel, not just tailpipe)',
        ],
        'why': [
            'The legs to the conversion site are already inside Charm\'s validated PDD boundary; the same monitoring and calculation transfer to the SAF claim unchanged',
            'The underlying Transportation module explicitly covers multimodal freight, so the AECN rail and truck legs are both within scope under one reference',
        ],
    },
    {
        'num': 4,
        'name': 'Biomass Conversion (Pyrolysis)',
        'owner': 'isometric',
        'refs': [
            ('Charm PDD v1.12, §B — Technical Description of Project Activity', 'As-validated description of Charm\'s pyrolysis operation producing bio-oil'),
            ('Charm PDD v1.12, Appendix 7 — BCU Calculation Methodology', 'Validated mass and energy accounting for the conversion step'),
            ('Underlying: Biochar Production and Storage v1.2, §9–§11', 'Pyrolysis reactor system (§9), emissions testing (§10), condensable bio-oil fraction measurement (§11)'),
            ('Underlying: Energy Use Accounting v1.3, §4–§6', 'Facility energy: electricity (§5), stationary fuel (§6), CO2e_Energy aggregation (§4)'),
        ],
        'what': [
            'The pyrolysis step produces bio-oil — the SAF feedstock — measured and characterized per the PDD\'s technical activity description and Appendix 7. The underlying protocol §11 governs measurement of the condensable bio-oil fraction; §9–§10 cover the reactor and emissions testing',
            'Energy Use Accounting v1.3 quantifies processing emissions: §5 electricity (behind-the-meter, grid-rate, or EAC), §6 stationary fuel combustion, aggregated into CO2e_Energy at §4',
        ],
        'why': [
            'This is Charm\'s existing validated conversion methodology — no new development. The same reactor and energy accounting that supports the CDR claim quantifies the bio-oil\'s production-stage CI',
            'Bio-oil is the product carried forward to the refinery; §11 is the protocol provision governing how the condensable bio-oil fraction is measured and characterized',
        ],
    },
    {
        'num': 5,
        'name': 'Allocation of Tree-to-Gate Emissions to Co-Products',
        'owner': 'isometric',
        'refs': [
            ('Charm PDD v1.12, Appendix 7 — BCU Calculation Methodology', 'As-validated co-product allocation across the pyrolysis output streams'),
            ('Underlying: GHG Accounting v1.0, §6.1', 'Co-product emissions allocation framework — four procedures'),
            ('Underlying: Biochar Production and Storage v1.2, §8.6.5.4', 'Energy-content allocation — the protocol\'s specified method'),
            ('ISO 14040 / 14044:2006', 'LCA allocation principles (crosswalk reference)'),
        ],
        'what': [
            'Appendix 7 of the PDD is Charm\'s validated method for splitting tree-to-gate emissions across the pyrolysis output streams; the underlying GHG Accounting v1.0 §6.1 sets the four-procedure framework and §8.6.5.4 specifies energy-content allocation',
            'Energy-content allocation apportions production emissions by the energy carried in each output stream — the protocol\'s own specified method, not an external choice',
        ],
        'why': [
            'The PDD\'s validated allocation is the basis; citing it first keeps the SAF CI consistent with the as-validated CDR accounting on the same physical process',
            'Note: RSB-STD-03-001 v3.2 Table 1 mandates economic allocation for RSB-certified biofuels — not binding here, but disclose to verifiers as a cross-scheme difference',
        ],
    },
    {
        'num': 6,
        'name': 'Bio-Oil Transport to Refinery',
        'owner': 'isometric',
        'refs': [
            ('Charm PDD v1.12, §B — Project Boundary & Monitoring Plan', 'The validated transport-accounting method Charm applies to bio-oil shipment legs'),
            ('Underlying: Transportation Emissions Accounting v1.1, §3.3', 'Distance-Based Method: CO2e = D × W × EF (rail + truck)'),
            ('ISO 14083:2023', 'GHG quantification for transport-chain operations (external anchor)'),
        ],
        'what': [
            'The bio-oil shipment to the FCC refinery uses the same transport-accounting method Charm\'s PDD validates for bio-oil movement — rail plus truck, calculated as distance × mass × mode-specific EF. The refinery endpoint is SAF-specific, but the method is unchanged',
            'ISO 14083:2023 is the international standard for GHG quantification across transport chains — a consistent external anchor across the transport steps',
        ],
        'why': [
            'The transport-accounting method is already validated in Charm\'s CDR PDD; only the destination differs for the SAF pathway, so the calculation carries over without new methodology',
            'Using the same underlying Transportation module across all bio-oil transport legs keeps the methodology internally consistent and simplifies verifier review',
        ],
    },
    {
        'num': 7,
        'name': 'Refinery Co-Processing into Fuel Co-Products',
        'owner': 'bolton',
        'refs': [
            ('RSB-STD-01-010 v2.8, §2.4', 'Requirements for co-processing biogenic and fossil feedstocks — three documentation options'),
            ('RSB-STD-03-001 v3.2, §B.10', 'Co-processing GHG calculation methodology'),
        ],
        'what': [
            'RSB §2.4 establishes three options for documenting biogenic fractions in co-processing: mass balance (§2.4.3), radiocarbon analysis (§2.4.4), or flexible attribution (§2.4.5)',
            'RSB-STD-03-001 §B.10 defines the GHG calculation framework for determining the bio-based share of refinery output and the associated emission intensities for each co-product stream',
        ],
        'why': [
            'RSB has the most developed published normative framework specifically for FCC-style co-processing of biogenic and fossil feedstocks — this is the coverage gap that the existing Isometric modules do not address',
            'Flexible attribution (§2.4.5) is the pathway that enables free designation of which output receives the biogenic carbon credit in Step 9; this step establishes the normative basis for that attribution',
        ],
    },
    {
        'num': 8,
        'name': 'Allocation of Marginal Refinery Emissions to Co-Products',
        'owner': 'bolton',
        'refs': [
            ('RSB-STD-01-010 v2.8, Annex IV formula [4]', 'Outlet energy fraction: AF = LHV_af ÷ Total energy output'),
            ('RSB-STD-03-001 v3.2, §B.10', 'Co-processing emission intensity calculation'),
        ],
        'what': [
            'Annex IV formula [4] allocates refinery processing emissions to SAF using outlet energy fraction: AF = LHV_af ÷ Total energy output. AF is the fraction of total refinery energy output attributable to SAF; processing emissions flow to SAF proportionally',
            'At typical FCC scales (bio-oil = ~5% of feed, SAF = ~20% of bio-derived output), AF is approximately 2% — meaning only ~2% of incremental refinery processing emissions are attributed to the SAF stream',
        ],
        'why': [
            'Published normative formula with explicit variables and a defined calculation — fully auditable by any verifier familiar with RSB',
            'Outlet energy fraction is physically grounded: it attributes refinery processing load to each product in proportion to its share of total energy output, consistent with established LCA energy allocation practice',
        ],
    },
    {
        'num': 9,
        'name': 'Allocation of Biogenic Carbon Credit to Fuel Co-Products',
        'owner': 'bolton',
        'refs': [
            ('RSB-STD-01-010 v2.8, §2.4.5 + Annex IV [1]–[3]', 'Flexible (free) attribution — normative requirement and three-step calculation'),
            ('ISCC PLUS 203-2 v1.1, §6.2', 'Free attribution guardrails: chemical connectivity, credits cannot exceed physical output, site-specific mass balance'),
        ],
        'what': [
            'RSB §2.4.5 is the normative requirement: the operator designates which output receives the biogenic carbon attribute. Annex IV formulas [1]–[3] calculate: (1) eligible carbon output, (2) attributed advanced fuel volume, (3) GHG intensity per MJ of that SAF',
            'ISCC PLUS 203-2 §6.2 articulates free attribution guardrails: chemical connectivity between input and output required; credited volume cannot exceed physical output; mass balance is site-specific',
        ],
        'why': [
            'Free attribution is the mechanism that makes SAF credit economics viable for FCC co-processing: operator can designate the SAF output as the recipient of the full bio-oil biogenic carbon credit, rather than spreading it across all refinery outputs by mass or energy fraction',
            'ISCC 203-2 guardrails are cited as a cross-reference to add auditor-facing clarity on the conditions under which free attribution holds — these guardrails are substantively consistent between RSB Annex IV and ISCC 203-2',
        ],
    },
    {
        'num': 10,
        'name': 'Transport of Fuel(s) to Blend Point',
        'owner': 'isometric',
        'refs': [
            ('Underlying: Transportation Emissions Accounting v1.1, §3.2–§3.3', 'Same two-method framework as Steps 3 and 6 (Energy Usage / Distance-Based)'),
            ('Transportation Emissions Accounting v1.1, Appendix 1', 'Mode-specific EF guidance: pipeline, ship, road'),
            ('ISO 14083:2023', 'GHG quantification for transport-chain operations'),
        ],
        'what': [
            'Quantifies finished-fuel transport from the refinery to the blend point. This leg is downstream of Charm\'s CDR PDD boundary, so it borrows the Transportation Emissions Accounting method rather than routing through the PDD',
            'Appendix 1 covers pipeline, ship, and road modes — all relevant for downstream SAF logistics depending on refinery location and blend point',
        ],
        'why': [
            'No new methodology work: the same transport-accounting method used upstream applies to the downstream fuel leg, even though this leg sits outside the validated CDR boundary',
            'Using one transport method across all legs keeps EF sourcing rules and calculations consistent end-to-end',
        ],
    },
    {
        'num': 11,
        'name': 'Quantification of Tree-to-Wheel CI',
        'owner': 'bolton',
        'refs': [
            ('RSB-STD-03-001 v3.2, §B.1', 'Well-to-wake central formula: E = eec + el + ep + etd + eu'),
            ('RSB-STD-03-001 v3.2, §A.1 / §A.5 / §A.10', 'Functional unit, emission factor hierarchy, GWP values'),
        ],
        'what': [
            '§B.1 central formula aggregates all lifecycle components into a single CI in gCO₂eq/MJ (LHV, dry basis); §A.2 sets the well-to-wake system boundary for aviation biofuels',
            '§A.5 emission factor sourcing hierarchy: EU Annex IX primary; national government publications secondary; Ecoinvent/peer-reviewed LCA databases tertiary. GWP (AR5): CO₂=1, N₂O=265, CH₄=28',
        ],
        'why': [
            'Published normative formula with defined functional unit, GWP values, and system boundary — provides auditable structure for aggregating the Isometric-derived upstream CI components into the SAF CI metric',
            'GREET (Argonne/DOE) qualifies under "national government publications" for a US-origin pathway, giving the methodology a defensible emission factor sourcing policy that verifiers recognize',
        ],
    },
    {
        'num': 12,
        'name': 'Quantification of GHG Reductions vs. Fossil Fuel Baseline',
        'owner': 'bolton',
        'refs': [
            ('RSB-STD-03-001 v3.2, §A.9 + Table 2', 'GHG savings formula; fossil comparator = 90 gCO₂eq/MJ (well-to-wake)'),
            ('RSB-STD-03-002 v2.1', 'Fossil fuel baseline calculation methodology — aviation kerosene'),
        ],
        'what': [
            'Saving [%] = (E_F − E) ÷ E_F × 100; RSB Global fossil comparator for biofuels = 90 gCO₂eq/MJ, confirmed in RSB-STD-03-001 v3.2 Table 2 (effective June 2025)',
            'RSB-STD-03-002 derives the 90 gCO₂eq/MJ fossil baseline from a lifecycle analysis of conventional jet fuel production and combustion',
        ],
        'why': [
            '90 gCO₂eq/MJ is the most widely cited SAF fossil baseline and provides a credible, verifier-recognized anchor even if RSB certification is not ultimately pursued',
            'Publishing the % reduction vs. this baseline gives buyers a number they can benchmark against other SAF products; the RSB methodology is publicly available and verifiable without a certification body',
        ],
    },
    {
        'num': 13,
        'name': 'Verification of Quantified Reductions',
        'owner': '123carbon',
        'refs': [
            ('SFC-SPEC-001 v01, §6.1.2 + §12', 'Third-party assessment requirements for non-certified Solutions'),
            ('ISO 14064-3:2019', 'Requirements and guidance for verification and validation of GHG statements'),
        ],
        'what': [
            'SFC MBM §6.1.2 requires a transparent and verifiable tracking system with independent third-party assessment; §12 allows optional Report verification',
            'ISO 14064-3:2019 is the international standard for third-party verification of GHG statements — defines verifier requirements, procedures, and statement of assurance',
        ],
        'why': [
            'SFC MBM\'s non-certified track criteria drive the verification requirement; §6.1.2 is the binding obligation and ISO 14064-3 is its established normative framework',
            '350Solutions qualifies as the "independent third-party" under §6.1.2 — plain text standard; §6.1.2 specifies only independence, not ISO accreditation of the assessor body',
        ],
    },
    {
        'num': 14,
        'name': 'Credit Issuance on Registry',
        'owner': '123carbon',
        'refs': [
            ('SFC-SPEC-001 v01, §5–§6', 'Solution registration and Sustainability Profile (§3.25) requirements'),
            ('123 Carbon registry protocols', 'Credit format, unique identifier assignment, and anti-double-counting ledger'),
        ],
        'what': [
            'SFC MBM §5 defines the Sustainability Profile that must accompany each credit: lifecycle GHG emission factors, LHV, feedstock type, production process, batch ID',
            '123 Carbon registry governs credit issuance format, unique identifier assignment, and the ledger that prevents double-counting across credit streams',
        ],
        'why': [
            '123 Carbon is the named registry; SFC MBM §5–§6 define exactly what information must appear on each credit at issuance — the methodology must be designed to produce all these outputs at batch level',
            'Registry-level issuance provides the double-counting protection required for running parallel CDR and SAF accounting on the same production process',
        ],
    },
    {
        'num': 15,
        'name': 'Credit Delivery, Retirement, and Integrity',
        'owner': '123carbon',
        'refs': [
            ('SFC-SPEC-001 v01, §4 + §6.1.3', 'General accounting principles and non-certified Solution disclosure requirements'),
            ('123 Carbon protocols', 'Credit retirement, transfer chain, and anti-double-counting provisions'),
        ],
        'what': [
            '§4 general accounting principles (relevance, transparency, completeness, accuracy, consistency, conservativeness) govern the full claim lifecycle from issuance through retirement',
            '§6.1.3 requires non-certified Solutions to disclose underlying calculations, data sources, and production processes in the buyer\'s Report',
        ],
        'why': [
            '§6.1.3 is the binding disclosure obligation for non-certified Solutions — the methodology must produce all required elements in a form that is documentable and transferable to the buyer',
            'Anti-double-counting provisions protect Charm and the buyer from the primary integrity risk: the same GHG reduction claimed simultaneously in both the CDR and SAF credit streams',
        ],
    },
]


# ── helpers ──────────────────────────────────────────────────────────────────

def rect(slide, l, t, w, h, fill=None, line_width=0):
    shp = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    shp.line.width = Emu(line_width)
    if line_width == 0:
        try:
            shp.line.fill.background()
        except Exception:
            pass
    return shp


def tb(slide, l, t, w, h):
    return slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))


def para(tf, text, size, bold=False, color=DARK, align=PP_ALIGN.LEFT, first=False, space_before=0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if space_before:
        p.space_before = Pt(space_before)
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p


# ── presentation ─────────────────────────────────────────────────────────────

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

blank = prs.slide_layouts[6]  # blank layout


# ── title slide ───────────────────────────────────────────────────────────────

ts = prs.slides.add_slide(blank)
rect(ts, 0, 0, 13.33, 7.5, fill=NAVY)

t = tb(ts, 0.8, 1.9, 11.5, 1.0)
t.text_frame.word_wrap = True
para(t.text_frame, 'SAF Methodology Framework', 38, bold=True, color=WHITE, first=True)

t = tb(ts, 0.8, 3.0, 11.5, 0.6)
para(t.text_frame, 'Step-by-Step Normative References', 22, color=LBLUE, first=True)

t = tb(ts, 0.8, 3.75, 10, 0.4)
para(t.text_frame, 'Bio-Oil  →  FCC Co-Processing  →  SAF Credit   |   Charm Industrial   |   June 2026', 12, color=RGBColor(0x8B, 0xAD, 0xCA), first=True)

# Legend
legend = [
    ('Steps 1–6, 10   Charm CDR Methodology — validated PDD v1.12 (underlying Isometric protocols cited beneath)', BLUE),
    ('Steps 7–9, 11–12   Bolt-On — Novel Methodology (RSB / ISCC normative references)', ORANGE),
    ('Steps 13–15   123 Carbon (SFC MBM Framework)', GREEN),
]
for i, (label, color) in enumerate(legend):
    dot = rect(ts, 0.8, 5.15 + i * 0.45, 0.22, 0.22, fill=color)
    t = tb(ts, 1.18, 5.12 + i * 0.45, 11, 0.3)
    para(t.text_frame, label, 12.5, color=WHITE, first=True)


# ── step slides ───────────────────────────────────────────────────────────────

for step in STEPS:
    sl = prs.slides.add_slide(blank)
    color = OWNER_COLOR[step['owner']]
    owner_lbl = OWNER_LABEL[step['owner']]

    # Header bar
    rect(sl, 0, 0, 13.33, 1.5, fill=color)

    # Step counter
    t = tb(sl, 0.35, 0.12, 4, 0.32)
    para(t.text_frame, f'STEP {step["num"]} OF 15', 9, bold=True, color=WHITE, first=True)

    # Step name
    t = tb(sl, 0.35, 0.43, 9.8, 0.95)
    t.text_frame.word_wrap = True
    para(t.text_frame, step['name'], 26, bold=True, color=WHITE, first=True)

    # Owner badge (top-right)
    badge = rect(sl, 10.55, 0.38, 2.5, 0.68, fill=WHITE)
    btf = badge.text_frame
    btf.word_wrap = True
    btf.margin_top = Pt(4)
    btf.margin_left = Pt(6)
    btf.margin_right = Pt(6)
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    br = bp.add_run()
    br.text = owner_lbl
    br.font.size = Pt(10)
    br.font.bold = True
    br.font.color.rgb = color

    # ── Left column: Normative Reference ──
    rect(sl, 0.25, 1.65, 5.85, 5.6, fill=LGRAY)

    t = tb(sl, 0.42, 1.73, 5.55, 0.3)
    para(t.text_frame, 'NORMATIVE REFERENCE', 8, bold=True, color=color, first=True)

    t = tb(sl, 0.42, 2.08, 5.55, 5.0)
    tf = t.text_frame
    tf.word_wrap = True
    first_ref = True
    for (ref_name, ref_clause) in step['refs']:
        para(tf, ref_name, 12.5, bold=True, color=DARK, first=first_ref, space_before=(0 if first_ref else 10))
        first_ref = False
        para(tf, ref_clause, 10.5, color=TGRAY, space_before=2)

    # ── Right column: WHAT ──
    t = tb(sl, 6.45, 1.7, 6.6, 0.3)
    para(t.text_frame, 'WHAT IT IS', 8, bold=True, color=color, first=True)

    t = tb(sl, 6.45, 2.05, 6.6, 2.35)
    tf = t.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(step['what']):
        para(tf, f'•  {bullet}', 11.5, color=DARK, first=(i == 0), space_before=(0 if i == 0 else 7))

    # Divider
    rect(sl, 6.45, 4.5, 6.6, 0.025, fill=MGRAY)

    # ── Right column: WHY ──
    t = tb(sl, 6.45, 4.57, 6.6, 0.3)
    para(t.text_frame, 'WHY IT\'S BEING USED', 8, bold=True, color=color, first=True)

    t = tb(sl, 6.45, 4.92, 6.6, 2.35)
    tf = t.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(step['why']):
        para(tf, f'•  {bullet}', 11.5, color=DARK, first=(i == 0), space_before=(0 if i == 0 else 7))


prs.save(OUT)
print(f'Saved: {OUT}')
