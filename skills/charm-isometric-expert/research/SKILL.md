---
name: research
description: >
  Internal methodology sub-skill for charm-isometric-expert. Not user-triggerable.
  Defines the citation standard and document-read workflow that charm-isometric-expert
  follows whenever making claims about what an external document says.
  Read this file at the start of any task that requires citing protocol text,
  standard clauses, regulatory language, or technical specifications.
---

# Research Skill

Answers questions requiring external documents, standards, specs, or technical frameworks. The core rule is non-negotiable: **every factual claim about what a source says must trace back to verbatim text you read in the current session.**

## Citation Rule (Hard — No Exceptions)

Every factual claim about what a document says requires two things:

1. **Document name + section identifier** — section number, page, table name, definition ID, or equivalent locator
2. **Verbatim quote** — exact text as it appears in the source, in double quotes

Paraphrasing after the quote is fine. Paraphrasing *instead of* the quote is not. If you cannot produce the verbatim text, you have not established what the document says.

This rule exists because confident-sounding paraphrase-as-citation has caused Max to circulate incorrect information. "The document says X" without a quote is worse than "I haven't read this document" — the former is unknown error, the latter is honest uncertainty.

**Valid citation:**
> Isometric Standard v2.0, §2.4.3: "A default emission factor may be applied where actual energy data is unavailable, provided the rationale is documented in the Monitoring Report." — The standard permits default EFs but requires documented rationale.

**Not a valid citation:**
> Section 2.4.3 requires documenting the rationale for default EF use. [No quote — paraphrase presented as citation]

---

## Step 1: Document Planning

Before reading anything, list every document needed to answer the question:

- Name each document
- Identify where to locate it (knowledge-base/, Google Drive, web URL, etc.)
- Identify which section, clause, table, or page is expected to be relevant
- Flag any document on the list that might not be accessible

If a document cannot be located, say so explicitly before proceeding. Do not substitute a different document without telling Max.

## Step 2: Locate and Read Each Document

Work through the list from Step 1. For each document:

**Local files** (knowledge-base/, outputs/, project files):
- Use the Read tool with the full path.

**Google Drive documents:**
- Use `mcp__claude_ai_Google_Drive__search_files` to locate, then `read_file_content` or `download_file_content`.
- For scanned images (scale tickets, BOLs, receipts, handwritten specs): download the raw JPG/PNG and Read the image directly. Do NOT rely on Drive's auto-OCR snippet — it misreads digits and layout on dense documents.

**Web documents** (standards bodies, regulatory sites, manufacturer specs, academic papers):
- Use Playwright (`browser_navigate`, `browser_snapshot`, `browser_evaluate`) per the workspace's browser usage rules.
- Navigate to the specific section or page; don't stop at the homepage or a search result.
- If the site requires login and you hit an SSO wall, surface the login step to Max with a clear handoff — don't silently skip the document.

**If a document is inaccessible:** State the access failure explicitly — what you tried, what you got. Do not proceed as if you read it, and do not characterize its content from memory.

## Step 3: Extract — Quote Per Claim

After reading each document, before synthesizing across documents, record for each relevant finding:

1. The section or page where you found it
2. The exact verbatim text, quoted
3. Your interpretation or note on relevance (after the quote, clearly separated)

Keep each document's findings separate at this stage. Synthesis comes later.

## Step 4: Synthesize

Only after all planned documents are read (or access failures are documented), synthesize:

- What the sources collectively say
- Where sources agree or conflict
- What remains unanswered (no source found, inaccessible, or out of scope)

Synthesis is analysis layered on top of quoted text — never a substitute for it.

## Step 5: Citation Audit (Self-Check Before Responding)

Before finalizing any response, scan every claim that characterizes what a document says:

- Is there a verbatim quote in this session backing it?
- Is the document name and section identified?
- If either is missing: fix it, or replace the claim with explicit uncertainty.

Any claim not grounded in a document read this session must be flagged inline:
> **[Unverified — not from a session read]**

Never omit this flag to clean up the response. The flag is the safety signal.

---

## Output Format

Structure responses as:

```
## [Research Question or Topic]

### [Short Finding Label]
"[Verbatim quote from source]"
— [Document name], [Section/Version]

[Analysis or interpretation of what this means for the question]

---

### Source List
| Document | Version | Access Method | Section(s) Read |
|----------|---------|---------------|-----------------|
| [Name]   | [e.g., v2.0] | [Read / Drive / Web] | [e.g., §3.2, Table 5] |
```

For multi-document research: group findings by topic or sub-question, not by document. The source list at the bottom is the complete audit trail of everything read.

For single-document lookups: the source list can be a single line.

---

## Scope

This skill covers any external document type — apply the same citation standard to all of them:

- **Protocol/standard documents:** Isometric Standard v1.9/v2.0, Bio-oil Geological Storage Protocol, GHG Accounting v1.0, Energy Use Accounting v1.3, and any other Isometric module; ISO, ASTM, EPA standards
- **Regulatory instruments:** federal and state regulations (40 CFR, 49 CFR, ORS, etc.), permits, enforcement orders (e.g., KDHE)
- **Technical specifications:** manufacturer spec sheets (GBRX, Wabtec, Argonne GREET), government lab publications, engineering databases
- **Scientific literature:** peer-reviewed papers, DOE/ANL reports, government lab publications
- **Web sources:** any page fetched via Playwright — must include URL and session date

Version matters for standards. Always confirm which version you are reading. Isometric Standard v1.9 and v2.0 differ materially on several thresholds; a citation to "the standard" without a version is incomplete.

---

## Structural Enforcement (Hard Gates — Not Policy)

Citation integrity is enforced by two hooks, not by workflow instructions alone:

### Stop hook: `citation_integrity_stop.sh` (primary gate)
Fires on every session stop. Checks the final response text.

**Gate 1 — Format**: every citation-signal phrase (§N.N, Section N.N, Clause N.N, Article N.N, Table N, "states/requires/specifies that …") must be accompanied by a verbatim quoted string within 500 chars. Missing quote → session blocked, exit 2.

**Gate 2 — Accuracy**: every verbatim quote longer than 15 chars must appear — exactly — in the corpus of text returned by source-read tool calls this session (Read, Google Drive read/download, Playwright snapshot, Word get_document_text). Quote not found in corpus → fabricated → session blocked, exit 2.

Gate 2 is the hard fabrication gate. A quote that doesn't appear in any document opened this session cannot complete. The only way to pass Gate 2 is to open the source document and use its actual text.

**Code blocks are excluded**: signals and quotes inside fenced code blocks and inline code are stripped before checking — they are illustrations, not claims.

### PostToolUse hook: `research_citation_guard.sh` (secondary seatbelt)
Fires on Write tool calls. Scans written files under `*/research/*` or containing a `## Source List` header for citation signals without nearby quotes. Catches egregious cases in written deliverables. Narrower scope than the Stop hook but provides a second check on research output files.

### What the hooks cannot catch
- A quote sourced from the knowledge base (`Charm_Isometric_Knowledge_Base.md`) rather than the primary source PDF. The knowledge base is derived from protocols; quoting it instead of the primary source passes Gate 2 but violates the workflow. Always verify against primary source PDFs before citing.
- Nuanced paraphrase that doesn't contain a citation-signal phrase. The workflow (Steps 1–5) is still the quality bar; the hooks are the structural floor.

---

## Anti-Patterns to Avoid

**1. Characterizing from memory.** "The Isometric Standard requires X" without a current-session read of the standard. Even if you know the domain, the rule is the same: open the document, find the text, quote it.

**2. Filename ≠ reading.** Locating a file in Drive or listing its name from a search result is not reading it. The file must be opened and the relevant section read before it can be cited.

**3. OCR snippets as primary source.** Drive's auto-OCR of images can misread digits and layout. Download the raw image and use Read. Image pixels are primary; OCR is derived.

**4. Paraphrase as citation.** "Section 4.2 states that monitoring must occur quarterly." Add the verbatim text. "Must occur quarterly" is your paraphrase — but did you read "quarterly monitoring is required" or "monitoring intervals shall not exceed 90 days"? Those are different claims.

**5. Skipping inaccessible documents.** Completing a synthesis when a planned document was inaccessible, without noting it. Inaccessibility is a result to report, not an obstacle to hide.

**6. Version assumptions.** Citing a standard without confirming which version you read. Always confirm the version; it belongs in the citation.

**7. Search-result characterization.** Reading a search snippet or abstract and treating it as if you read the document. Read the source, not the summary of the source.

---

## Working Notes

- Max knows this domain deeply. Skip CDR/MRV 101.
- For Isometric protocol questions, the knowledge base at `knowledge-base/` is a fast starting point, but always verify against the primary source PDFs in `knowledge-base/isometric-pdfs/` when quoting.
- Protocol module names in the knowledge base include version numbers; confirm the PDF version before citing.
- For web research: announce the site and intent on the first Playwright call to a new hostname in the session (per `feedback_playwright_new_domain_flag` in memory). One announcement per domain is enough.
- If Max says "don't worry about citing exactly" or similar, acknowledge but hold the citation standard — the rule exists because he's been burned by paraphrase-as-citation, not because he likes overhead.
