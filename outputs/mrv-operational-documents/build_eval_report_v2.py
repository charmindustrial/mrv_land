"""Build AI Agent Evaluation Report — tight, 3-page target."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "outputs/mrv-operational-documents/AI_Agent_Evaluation_Report_v2.docx"

doc = Document()
section = doc.sections[0]
section.top_margin    = Inches(0.85)
section.bottom_margin = Inches(0.85)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)

NAVY = RGBColor(0x1F, 0x49, 0x7D)
BLUE = RGBColor(0x2E, 0x74, 0xB5)
GRAY = RGBColor(0x59, 0x59, 0x59)

def rule_below(p):
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '4')
    bot.set(qn('w:space'), '1');    bot.set(qn('w:color'), '1F497D')
    pBdr.append(bot); pPr.append(pBdr)

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text.upper())
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = NAVY
    rule_below(p)

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(1)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = BLUE

def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(4)
    p.add_run(text).font.size = Pt(10)

def bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(bold_prefix + " "); r1.bold = True; r1.font.size = Pt(10)
    p.add_run(text).font.size = Pt(10)

# ── Title ──────────────────────────────────────────────────────
tp = doc.add_paragraph()
tp.paragraph_format.space_after = Pt(1)
tr = tp.add_run("AI Agent Evaluation Report")
tr.bold = True; tr.font.size = Pt(15); tr.font.color.rgb = NAVY

sp = doc.add_paragraph()
sp.paragraph_format.space_after = Pt(1)
sp.add_run("Charm Industrial — MRV Batch QA Agent").font.size = Pt(11)

mp = doc.add_paragraph()
mp.paragraph_format.space_after = Pt(8)
mr = mp.add_run("Evaluator: AI Systems Expert  │  May 2026  │  Internal / Presentation")
mr.italic = True; mr.font.size = Pt(9); mr.font.color.rgb = GRAY

# ── 1. Background ──────────────────────────────────────────────
h1("Background")
body(
    "Charm Industrial converts agricultural waste into bio-oil via pyrolysis, then injects it into deep "
    "underground rock formations for permanent CO₂ storage. The output is a carbon removal credit — a "
    "financial instrument sold to corporations for verified climate impact and independently audited by "
    "third-party verifiers before issuance. The numbers must be right: an error that reaches the auditor "
    "risks a formal finding, delays credit issuance, or misstates the volume of carbon removed."
)
body(
    "Verifying a single injection batch means reconciling data across 6+ primary sources: certified weigh "
    "tickets, supplier bills of lading, lab carbon-content analysis, operations notes, a live shipment "
    "tracker, and the Isometric Certify registry (which holds the final credit calculation). A human "
    "analyst doing this manually takes 30–60 minutes, cross-referencing 2–4 sources per line across a "
    "~57-item checklist. Under time pressure, some items get spot-checked rather than fully verified."
)

# ── 2. Agent ───────────────────────────────────────────────────
h1("Agent Architecture")
body(
    "The MRV Batch QA Agent is a Claude Opus-based AI agent that opens every source document, extracts "
    "values into a structured log, and builds a fully-cited QA checklist. It runs a four-gate sequential "
    "workflow — source reads → checklist build → adversarial self-review → delivery audit — where each "
    "gate has hard entry and exit conditions. Every checklist status cites a specific key in the "
    "source-read log; a pre-delivery audit script verifies every quoted number against that log before "
    "the checklist reaches the human reviewer. A performance tracker logs each session: turn count, "
    "duration, corrections required, and whether the batch was approved clean on first pass."
)

# ── 3. Performance ─────────────────────────────────────────────
h1("Performance")

h2("Accuracy")
body(
    "3 batch QAs have formal completion records in the performance tracker. 2 of 3 (67%) were approved "
    "clean on first pass — zero corrections, zero violations, 57 items fully verified. The third (batch "
    "2-184) required 5 correction iterations and incurred 9 laziness-violation penalties. Both clean "
    "batches completed in under 55 minutes of agent active time, with the adversarial reviewer issuing "
    "zero challenges. 13 failure categories are documented with the batch where the error first occurred "
    "and the structural fix applied — each error class encoded as a hard constraint, not a prompt instruction."
)

h2("Cost per Session — Actual")
body(
    "Session cost is dominated by Anthropic's prompt caching layer. The agent reads large documents "
    "each session and accumulates a growing conversation history; by mid-session the model re-reads "
    "100K–350K cached tokens per turn at $1.50/M, with cache writes adding $30–96/session at $30/M. "
    "Across 10 logged sessions the average is $194 and the median $180. Most sessions land in the "
    "$145–205 range; two outliers (a major-error recovery session and a three-sub-session QA) reach "
    "$243 and $376 respectively. No downward learning trend is detectable (R² = 0.002) — cost is "
    "driven by batch complexity and whether errors occur, not by accumulated familiarity. "
    "Full breakdown with live formulas in the supporting Excel."
)

h2("Reliability")
body(
    "The four-gate structure prevents the most common agentic QA failure: writing conclusions before "
    "reading evidence. The pre-flight requirement to print all applicable failure categories to chat "
    "before Gate 1 makes session preparation visible — if the list doesn't appear, the session is "
    "blocked. Context fatigue at 400+ turns is a documented risk; the agent is instructed to flag "
    "degradation rather than produce degraded work silently."
)

h2("Security")
bullet("Credential scope.", "Agent has workspace-wide OAuth read access to Drive, Gmail, Slack, and Calendar. Should be scoped to specific shared drives and QA channels.")
bullet("Data exposure.", "Source-read logs (batch_XXX_source_reads.json) containing supplier mass and emissions data are committed to a shared git repo in plaintext. Encrypt at rest.")
bullet("Registry write risk.", "Playwright interaction with the live Isometric Certify credit registry is governed by policy and a hook — not technical write-prevention. A read-only API or typed scraping library removes the risk entirely.")

# ── 4. Recommendations ────────────────────────────────────────
h1("Recommendations")
bullet("Extract the shared skill spine.", "AECN, Kerry, and Charm batch QA agents duplicate ~70% of their structure. One formatting rule already drifted out of sync before being caught. Shared scaffold eliminates drift.")
bullet("Expand deterministic computation.", "A pilot script already handles mass-chain arithmetic for rail batches. Extend this pattern to all numeric checks — the LLM reads and logs; Python verifies. Cuts both errors and session length.")
bullet("Tier model selection.", "Opus is right for judgment calls (FAIL vs FLAG, multi-source conflict). Haiku-class handles extraction (reading a cell, parsing a PDF field). Estimated 40–60% cost reduction with no quality loss on judgment items.")
bullet("Replace Playwright on the Certify registry.", "Browser automation is fragile and the only thing preventing writes is a hook. A read-only API client is the correct interface.")
bullet("Build a regression suite.", "13 documented failure categories + 7 sessions of known-good output = a ready-made test corpus. No automated testing exists today outside the per-session audit script.")

# ── 5. Value and Pricing ──────────────────────────────────────
h1("Value and Pricing")
body(
    "A human analyst takes 30–60 min at $75–100/hr loaded = $37–100/batch. The agent's median cost "
    "of ~$196 is higher, but the comparison is not equivalent: a human in that time is spot-checking; "
    "the agent opens every primary source for all 57 items and produces a fully-cited, audit-ready "
    "deliverable. The senior analyst receives a finished product to approve, not a task to perform."
)
body(
    "SaaS pricing: $250–400/session — above current API cost, below the cost of equivalent manual "
    "thoroughness. For operators running 20+ batches per reporting period, a $3,000–6,000/month retainer "
    "competes favorably against manual review cost and inconsistency risk."
)

# ── 6. Cost to Scale ──────────────────────────────────────────
h1("Cost to Scale")

h2("1,000 Enterprise Users")
body(
    "At 15 sessions/user/month: 15,000 sessions × $196 = $2.94M/month API cost. Model tiering "
    "(recommendation 3) reduces this to ~$1.8M/month. At $350/session SaaS price: $5.25M/month revenue, "
    "~$3.45M contribution after API cost. See supporting Excel for sensitivity analysis."
)

h2("1,000,000 Users — Optimization Path and TAM")
body(
    "At current architecture: 1M × 15 sessions × $196 = $2.94B/month. Not viable. Three levers bring "
    "cost to $4–8/session: (1) fine-tuned Haiku-class model for extraction turns ($1.25/M output vs "
    "$75/M, ~60× cheaper on ~60% of turns); (2) context compression between gates, cutting cache-read "
    "volume by ~65% and saving $42–145/session; (3) deterministic arithmetic scripts removing ~40 "
    "reasoning-heavy turns per session. Combined, achievable in 18–24 months at production scale."
)
body(
    "The CDR market cannot support 1M users. The broader opportunity is sustainability claim "
    "verification — any regulated performance claim requiring a multi-source evidence chain audited "
    "by a third party. Key segments and estimated addressable entities:"
)
bullet("EU CSRD", "~50,000 large companies required to report annually by 2025–2026, expanding to hundreds of thousands of SMEs.")
bullet("US IRA clean energy credits (45Q/45V/45Z)", "~8,000 eligible facilities with annual verified GHG accounting requirements.")
bullet("Voluntary Carbon Market", "~10,000 registered projects (VERRA, Gold Standard) each requiring annual third-party verification.")
bullet("Compliance carbon and fuel markets", "EU ETS, CA-ETS, RGGI, US RFS/RINs, CA LCFS: ~30,000+ regulated installations and pathway certificates.")
bullet("RECs, SAF credits, BCUs, EACs", "~15,000 certificate generators requiring mass-balance and provenance evidence chains.")
body(
    "Total addressable entities: ~100,000–200,000 by 2028. At 10 sessions/entity/month: 1M–2M "
    "sessions/month — the 1M-user scenario is achievable within sustainability verification alone. "
    "At $25/session (optimized SaaS) and $6/session API cost: ~76% gross margin. "
    "Full TAM model with live formulas in the supporting Excel."
)

doc.save(OUT)
print(f"Saved: {OUT}")
