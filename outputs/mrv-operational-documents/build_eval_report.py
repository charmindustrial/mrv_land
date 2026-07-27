"""Build AI Agent Evaluation Report as a formatted .docx."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "outputs/mrv-operational-documents/AI_Agent_Evaluation_Report_MRV_Batch_QA.docx"

doc = Document()

# ── Page margins ──────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.left_margin   = Inches(1.15)
section.right_margin  = Inches(1.15)

# ── Helpers ───────────────────────────────────────────────────
def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    # thin rule below
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F497D')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
    return p

def body(text, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    run.font.size = Pt(10)
    return p

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix + " ")
        r1.bold = True
        r1.font.size = Pt(10)
        r2 = p.add_run(text)
        r2.font.size = Pt(10)
    else:
        run = p.add_run(text)
        run.font.size = Pt(10)
    return p

def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)

# ── Title block ───────────────────────────────────────────────
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
tr = title_p.add_run("AI Agent Evaluation Report")
tr.bold = True
tr.font.size = Pt(16)
tr.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(2)
sub_p.paragraph_format.space_after  = Pt(2)
sr = sub_p.add_run("Charm Industrial MRV Batch QA Agent")
sr.bold = True
sr.font.size = Pt(12)

meta_p = doc.add_paragraph()
meta_p.paragraph_format.space_after = Pt(12)
mr = meta_p.add_run("Evaluator: AI Systems Expert  │  Date: May 2026  │  Classification: Internal / Presentation")
mr.font.size = Pt(9)
mr.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
mr.italic = True

# ── Section 1: Agent Overview ─────────────────────────────────
h1("Agent Overview")
body(
    "The subject is Charm Industrial’s MRV (Measurement, Reporting, Verification) batch QA agent — "
    "a production AI agent built on Claude Opus that independently verifies carbon dioxide removal (CDR) "
    "injection batches before they reach third-party verification. Each QA session reads 6+ primary source "
    "documents (scale tickets, bills of lading, lab results, operations notes, a live tracking spreadsheet, "
    "and the Isometric Certify registry), cross-checks mass chains and emission factor arithmetic, builds a "
    "structured Excel checklist with cited evidence, runs an adversarial self-review, and delivers findings "
    "to the operations team via Slack and Gmail."
)
body(
    "The system is not a single agent but a cluster: three primary QA agents (AECN, Kerry, and Charm-produced "
    "oil types), one site-emissions QA agent, and three sub-agents (adversarial reviewer, completion monitor, "
    "and performance tracker). All agents share a structured knowledge base, common formatting standards, and "
    "a penalty/reward framework that tracks error rates over time."
)

# ── Section 2: Performance ────────────────────────────────────
h1("Performance Evaluation")

h2("Accuracy")
body(
    "The system’s accuracy profile is unusually well-documented. A lessons_learned.md file captures "
    "13 distinct failure categories from real production sessions spanning approximately 40 batches. Each "
    "failure category triggered a structural mitigation — not a prompt adjustment, but an enforced code "
    "or schema change."
)
body(
    "Examples: a confabulated finding in batch 2-184 (a value invented during adversarial review with no "
    "counterpart in the source log) led to a mandatory [log:KEY] citation requirement, enforced by a "
    "pre-delivery audit script that rewrites unverified rows before the file is saved. A false 388-kg "
    "under-credit finding on the last offload of a railcar (batch 2-185) led to a documented conservatism "
    "policy now encoded in both the skill specification and the build-time validation library."
)
body(
    "The current architecture has ceiling-level accuracy protections: every status must cite a source-log key, "
    "adversarial review can only challenge logged values (no hypothetical challenges permitted), and a "
    "pre-delivery Python script verifies quoted numbers against source-log values before the checklist reaches "
    "a human. Each error became a permanent structural constraint rather than a retry instruction."
)
body("Known accuracy risks that remain:")
bullet(
    "The LLM still performs the most complex rail-batch mass allocation judgment calls, which are intrinsically difficult.",
    "(1)"
)
bullet(
    "Emission factor values in the skill documentation can drift out of sync with the live Standard Emission Factors "
    "sheet. The system mitigates this by requiring agents to open the live sheet every session, but this adds latency.",
    "(2)"
)
bullet(
    "First-session performance on a new batch type or reporting period is historically lower than on mature batch patterns.",
    "(3)"
)

h2("Reliability")
body(
    "The four-gate sequential workflow (source reads → cross-check + checklist build → adversarial review "
    "→ finalization) prevents the most common failure mode in agentic QA: writing conclusions before completing "
    "evidence collection. Gate violations carry a +5 penalty in the performance tracker; a pre-flight gate blocks "
    "every session from starting without reading the failure-category documentation. The system fails loudly by "
    "design — if a mandatory verification step is skipped, the adversarial reviewer is designed to catch it "
    "before delivery."
)
body(
    "Session length is a structural reliability risk. At 200–500 turns per QA session, context fatigue is "
    "documented and expected; the skill specification explicitly instructs the agent to flag degradation rather "
    "than push through with sloppy work. The adversarial reviewer provides a second independent check, but it "
    "operates within the same context window and cannot catch systematic drift the way a fresh human reviewer would."
)

h2("Security")
body("Three concerns at current state:")
bullet(
    "Google OAuth scopes are broad — the agent has read access to Drive, Gmail, Slack, and Google Calendar "
    "workspace-wide. In a regulated environment (CDR credits are financial instruments), this scope should be "
    "narrowed to specific shared drives and specific Slack channels.",
    "1."
)
bullet(
    "Batch source-read logs (batch_XXX_source_reads.json) are committed to a shared git repository in plaintext; "
    "they contain proprietary mass, emission, and supplier data. These should be encrypted at rest or stored in "
    "a secrets-aware backend.",
    "2."
)
bullet(
    "The Playwright browser automation layer that interacts with the Isometric Certify registry (a live financial "
    "registry) is controlled by policy and a hook — not by technical read-only API enforcement. A "
    "misconfiguration could write to a registry that controls real carbon removal credits.",
    "3."
)

# ── Section 3: Suggestions ────────────────────────────────────
h1("Inputs for the Building Team")
bullet(
    "The AECN, Kerry, and Charm agents share ~70% of their workflow structure but duplicate it inline. One "
    "divergence (the siren-emoji prefix rule for Slack delivery) already drifted out of sync between agents "
    "and required a separate fix. A shared common spine would eliminate this drift risk.",
    "Extract the shared spine across batch QA agents."
)
bullet(
    "A pilot script (compute_mass_chain.py) already handles mass-chain arithmetic deterministically for rail "
    "batches and has been validated. This pattern — LLM reads documents and populates a structured log; "
    "Python script performs all arithmetic — should replace every numeric verification currently done by "
    "the LLM. LLMs should not be doing emission factor multiplication; a script should.",
    "Expand the deterministic computation layer."
)
bullet(
    "Opus is appropriate for judgment calls (FAIL vs FLAG classification, evidence synthesis) but is expensive "
    "for structured extraction tasks (reading a scale ticket image, finding a value in a spreadsheet row). "
    "A Haiku-class model handles extraction; Opus handles synthesis. Splitting turns across model tiers could "
    "reduce per-session cost by 40–60% without accuracy loss.",
    "Cost-tier model selection."
)
bullet(
    "Browser automation against a live registry is fragile — DOM changes break selectors, session timeouts "
    "add latency, and the read-only guarantee relies on a hook rather than technical enforcement. If Isometric "
    "offers an API, that is the right interface; if not, a typed screen-scraping library is more maintainable "
    "than raw Playwright.",
    "Replace Playwright-based Certify reads with API integration."
)
bullet(
    "With 13 documented failure categories and known-good outputs from ~40 batches, the team has the raw material "
    "for a regression suite. Every structural mitigation should have a corresponding test that would have caught "
    "the original failure. Currently, the only automated check is the pre-delivery audit script, which runs per "
    "session, not continuously.",
    "Formalize a regression test suite."
)

# ── Section 4: Pricing ────────────────────────────────────────
h1("Pricing and Value")
body(
    "Value case: A human QA specialist performing equivalent work takes 4–8 hours per batch at $75–100/hour "
    "— $300–800 per batch. The agent completes a session in 2–4 hours of wall time at a current API "
    "cost of approximately $20–35 per session (200–500 turns at Claude Opus pricing, including input "
    "context). Net cost reduction: 10–20x per batch, with better auditability (every finding cites a "
    "source-log key) and no fatigue-driven quality variance."
)
body(
    "Willingness to pay (SaaS pricing): At $150–250 per batch QA — capturing roughly 30–50 cents of "
    "every dollar of value created — this is compelling for any organization with more than 20 injection "
    "batches per reporting period. A retainer of $2,500–5,000/month for unlimited batch QA would be "
    "competitive against a half-time QA FTE at $60–80K/year."
)

# ── Section 5: Scaling ────────────────────────────────────────
h1("Cost to Scale")

h2("1,000 Enterprise Users")
body(
    "Assuming each user represents a carbon removal operator running 10–20 batch QAs per month: "
    "10,000–20,000 sessions/month. At $30/session API cost: $300K–600K/month in API spend. "
    "With cost-tier optimization (tiered model selection above), this drops to ~$150–250K/month. "
    "Infrastructure (compute, storage, audit logging) adds 20–30%. A SaaS price of $150/session "
    "generates $1.5–3M/month revenue — healthy unit economics."
)

h2("1,000,000 Users")
body(
    "At current Opus pricing and architecture, 1M active users running 10 sessions/month = $300M/month "
    "in API spend. This is not viable without fundamental architecture changes: fine-tuned smaller models "
    "for the extraction layer, shared knowledge-base context caching across users, and deterministic "
    "arithmetic scripts replacing LLM computation for all numeric verification."
)
body(
    "With those optimizations — realistic target: $3–5/session — API spend becomes "
    "$30–50M/month. At a $25/session SaaS price, this is a $250M/month revenue business at "
    "breakeven on API cost, with infrastructure and margin on top. Feasible, but requires 18–24 "
    "months of architecture work to get there."
)
body(
    "The CDR market itself cannot sustain 1M users of this specific domain agent. The more interesting "
    "question is whether the architecture — sequential-gate evidence collection, log-driven adversarial "
    "review, structural failure-category enforcement — generalizes to analogous regulated-industry "
    "workflows: pharmaceutical batch release, environmental compliance auditing, financial trade verification. "
    "In those markets, 1M users is plausible, and the unit economics above apply."
)

# ── Footer note ───────────────────────────────────────────────
doc.add_paragraph()
fn = doc.add_paragraph()
fn.paragraph_format.space_before = Pt(8)
fnr = fn.add_run(
    "All performance observations are grounded in documented system behavior from production sessions, "
    "not estimated or generalized from industry benchmarks."
)
fnr.italic = True
fnr.font.size = Pt(9)
fnr.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

doc.save(OUT)
print(f"Saved: {OUT}")
