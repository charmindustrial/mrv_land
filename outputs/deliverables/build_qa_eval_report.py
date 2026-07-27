from docx import Document
from docx.shared import Pt, Inches

doc = Document()

for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.15)
    section.right_margin = Inches(1.15)

def h1(text):
    p = doc.add_heading(text, level=1)
    p.runs[0].font.size = Pt(14)
    return p

def h2(text):
    p = doc.add_heading(text, level=2)
    p.runs[0].font.size = Pt(12)
    return p

def body(text):
    p = doc.add_paragraph(text)
    p.style.font.size = Pt(11)
    return p

def bold_lead(label, rest):
    p = doc.add_paragraph()
    r1 = p.add_run(label); r1.bold = True; r1.font.size = Pt(11)
    r2 = p.add_run(rest);  r2.font.size = Pt(11)
    return p

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        r1 = p.add_run(bold_prefix); r1.bold = True; r1.font.size = Pt(11)
        r2 = p.add_run(text);        r2.font.size = Pt(11)
    else:
        r = p.add_run(text); r.font.size = Pt(11)
    return p

# ── Title ─────────────────────────────────────────────────────────────────────
h1("AECN Batch QA Agent — Performance Evaluation")
p = doc.add_paragraph("Max Lavine, Charm Industrial MRV — May 2026")
p.runs[0].italic = True; p.runs[0].font.size = Pt(11)

# ── Background ────────────────────────────────────────────────────────────────
h2("Background: The System This Agent Operates Within")

body(
    "Charm Industrial produces bio-oil by pyrolyzing waste biomass and injects it permanently "
    "into deep geological formations. Because the carbon in that biomass was originally "
    "atmospheric CO₂, injecting the oil constitutes durable carbon dioxide removal (CDR). "
    "Buyers — corporations with net-zero commitments — pay for this removal in the "
    "form of carbon removal credits, each representing one verified metric ton of net CO₂ removed."
)

body(
    "The key word is verified. The Isometric Standard v2.0 §5.2 states: “Credits are "
    "Issued representing a specific Removal or Reduction. This process is undertaken once the "
    "net Removal or Reduction has been Verified against the respective Protocol.” "
    "Verification is therefore the revenue gate: no passing audit, no credits, no revenue. "
    "Each batch is worth approximately $10,000–$20,000 in credit revenue, representing "
    "on average about 29 tCO₂e of net removal (range: 23–40 tCO₂e across recent "
    "production batches)."
)

body(
    "The verifier audits an MRV package drawn from six primary sources: certified scale "
    "tickets, bills of lading, lab analysis reports, operations notes, a real-time "
    "lot-tracking database, and the Isometric Certify registry. Errors in any of them can "
    "trigger a verifier flag, delay credit issuance, or require a costly re-audit. "
    "The AECN Batch QA Agent automates Charm’s internal pre-submission QA pass by "
    "reading all six source categories, cross-checking 40+ data points against primary "
    "documents, and producing a PASS/FAIL/FLAG/N/A checklist with evidence citations for "
    "every item. It then runs an adversarial self-review and delivers the checklist for "
    "human approval before verifier submission."
)

# ── Performance ───────────────────────────────────────────────────────────────
h2("Performance")

bold_lead(
    "Accuracy. ",
    "The agent’s accuracy record spans 13 documented failure categories across "
    "approximately 40 production batches, each representing a real error that caused rework. "
    "Early failure modes included reading the wrong row from the lot-tracking database and "
    "generating false findings, declaring documents absent without checking the definitive "
    "source, and generating confident adversarial-review findings that had no basis in any "
    "source document. Each failure generated a structural fix rather than a verbal commitment. "
    "A citation-tag requirement forces every finding to reference a key in a structured "
    "source-read log; a pre-delivery audit script rewrites any uncited row before the "
    "checklist reaches a human reviewer. The accuracy trend is upward."
)

bold_lead(
    "Reliability. ",
    "The architecture is four sequential gates — source reads, cross-check and checklist "
    "build, adversarial self-review, delivery — with hard entry and exit conditions at "
    "each transition. Gate violations carry an explicit tracked penalty. Clean production runs "
    "complete in roughly 45–75 minutes of active session time, averaging about 316 turns "
    "across recent batches. The main reliability risk is context fatigue in long sessions, "
    "where evidence notes can drift toward generic phrasing; the adversarial self-review gate "
    "is specifically designed to catch this before delivery."
)

bold_lead(
    "Security and Data Privacy. ",
    "Two distinct threat models apply."
)

body(
    "The first is data integrity: a hallucinated PASS on an unverified item means a "
    "misreported net removal, which could result in invalid credits issued against a flawed "
    "calculation. Third-party verifiers and carbon market buyers rely on this data, making "
    "integrity failures both operationally and legally consequential. Structural controls "
    "include the citation-tag requirement, log-driven adversarial review (which cannot "
    "challenge values not recorded in source reads), and a pre-delivery audit script. The "
    "Certify registry is enforced read-only via policy, a system hook, and a permission seatbelt."
)

body(
    "The second is data privacy, and it is the more significant gap in a deployment context. "
    "The agent accesses commercially sensitive data: batch-level injection volumes (revealing "
    "production capacity to competitors), proprietary bio-oil chemical composition, supplier "
    "relationships embedded in shipping documents, credit issuance timing (market-sensitive), "
    "and financial data from the lot-tracking database. The prototype uses broad, unscoped "
    "credentials with no audit log of what data was accessed or transmitted. At one "
    "organization, the blast radius of a credential compromise is bounded by that "
    "organization’s own data. At 1,000 organizations, cross-tenant data leakage becomes "
    "a material risk the current architecture cannot contain. Any production deployment "
    "requires scoped credentials per tenant, read-only API access, session isolation, and "
    "audit logging — none of which are present in the prototype."
)

# ── PM Recommendations ────────────────────────────────────────────────────────
h2("Product Manager Recommendations")

body(
    "The core opportunity is cost reduction through three architectural changes. "
    "Using batch 2-186 as a representative clean production run ($146, 290 turns), "
    "current cost breaks into three components:"
)

bullet(
    "Cache reads: 61.3M tokens × $1.50/MTok = $92 (63% of cost). Each turn, "
    "the model re-reads its full ≈211k-token context — knowledge base, skill "
    "documentation, checklist structure — from the 1-hour prompt cache."
)
bullet("Cache writes: 1.1M tokens × $30/MTok = $33 (23%). Written once at session start.")
bullet("Output tokens: 280k tokens × $75/MTok = $21 (14%). Checklist text, evidence notes, reasoning.")

bold_lead(
    "Change 1 — Deterministic arithmetic for mass-chain checks (−$20, → ~$126/batch). ",
    "The mass-chain verification — confirming scale ticket weights, shipping documents, "
    "lot-tracker records, and the Certify calculation all agree on the same injected mass — "
    "is pure arithmetic the LLM currently reasons through across ~40 turns. A deterministic "
    "script (already prototyped and validated) eliminates those turns: "
    "40 turns × 211k tokens × $1.50/MTok = $12.66 saved on cache reads alone, "
    "with proportional output and cache-write reductions totaling ~$20. It also eliminates "
    "the confabulation errors responsible for $200–$375 outlier sessions."
)

bold_lead(
    "Change 2 — Model cycling: Sonnet for routine tasks, Opus for judgment calls (−$47, → ~$79/batch). ",
    "Routing 60% of turns to Claude Sonnet ($15/MTok output, $0.30/MTok cache reads "
    "vs. Opus’s $75/$1.50) reduces cache reads from $79 to $41 and output from $21 "
    "to $11, saving ~$47/batch. Opus is reserved for adversarial self-review, complex "
    "allocation judgment, and protocol interpretation — tasks where model capability "
    "is genuinely load-bearing."
)

bold_lead(
    "Change 3 — Direct API connections replacing browser automation (−$32, → ~$47/batch). ",
    "Most remaining turns are browser navigations: opening PDFs, reading spreadsheet rows, "
    "scraping the registry. Direct API calls to Google Sheets, Drive, and Certify would "
    "retrieve the same data in one round trip instead of 5–10 browser turns, cutting "
    "turn count by ~40% (100 turns). At the blended Sonnet/Opus cache-read rate "
    "($0.78/MTok): 100 turns × 211k tokens × $0.78/MTok = $16.46 saved on "
    "cache reads, plus $3.84 on output and proportional cache-write savings ≈ $32/batch."
)

body(
    "All three combined: ~$146 → ~$47/batch (68% reduction). Change 2 delivers the "
    "largest single cut because cache reads are 63% of current cost and Sonnet’s 5× "
    "cache-read discount applies to the dominant driver."
)

# ── Willingness to Pay ────────────────────────────────────────────────────────
h2("Willingness to Pay")

body(
    "Manual batch QA by a senior MRV analyst takes approximately one hour — roughly "
    "$130/batch fully loaded (base rate just under $100/hr × 1.3× for benefits "
    "and facilities). The agent at ~$165/batch is marginally more expensive today, but the "
    "value proposition is quality and consistency: it checks every item against every "
    "primary source every time, produces verifier-auditable citations, runs overnight, "
    "and catches errors a one-hour human spot-check might miss. A verifier query "
    "requiring re-audit costs meaningfully more than the $35 gap."
)

body(
    "Willingness to pay: $150–$175/batch at current costs — cost-neutral against "
    "human QA with a modest consistency premium. At the ~$47/batch target enabled by all "
    "three changes, a $150/batch price yields a 3× gross margin. At $100/batch, the "
    "customer saves $30/batch versus human QA and the margin remains healthy."
)

# ── Deployment Cost ───────────────────────────────────────────────────────────
h2("Deployment Cost")

bold_lead(
    "One organization (~25 batches/month): ",
    "$165 × 25 = ~$4,100/month today; ~$1,175/month optimized."
)

bold_lead(
    "1,000 organizations: ",
    "25,000 batches/month. ~$4.1M/month today; ~$1.2M/month optimized. Cache costs "
    "scale linearly — each organization’s session is independent, with no "
    "shared amortization of knowledge-base writes across tenants unless the architecture "
    "is redesigned."
)

bold_lead(
    "1,000,000 organizations: ",
    "$47/batch × 25M sessions/month = ~$1.2B/month — viable only with further "
    "cost reduction. Shared multi-tenant knowledge-base caching (amortizing the $33 "
    "per-session cache-write cost), lighter models for routine checks, and outcome-based "
    "pricing (per credit issued rather than per API call) could bring infrastructure cost "
    "to $5–$15/batch, supporting a $75–$100/batch price at scale."
)

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/outputs/deliverables/AECN_QA_Agent_Performance_Evaluation.docx"
doc.save(out)
print(f"Saved: {out}")
