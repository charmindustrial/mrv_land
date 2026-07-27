export const meta = {
  name: 'deep-research-mrv',
  description: 'Deep research with enforced citation discipline: scope gate, 2-attempt limit, verbatim quotes, page numbers, PDF URLs',
  phases: [
    { title: 'Scope', detail: 'Decompose question into search angles' },
    { title: 'Search', detail: 'Parallel web searches per angle' },
    { title: 'Version Check', detail: 'Confirm current document versions and get PDF URLs' },
    { title: 'Extract', detail: 'Scope gate + 2-attempt extraction per source' },
    { title: 'Verify', detail: 'Adversarial 3-vote verification per claim' },
    { title: 'Synthesize', detail: 'Merge, rank, and produce cited report' },
  ],
};

// ─── SCHEMAS ──────────────────────────────────────────────────────────────────

const ANGLES_SCHEMA = {
  type: 'object',
  required: ['angles'],
  properties: {
    angles: {
      type: 'array',
      minItems: 5,
      maxItems: 5,
      items: {
        type: 'object',
        required: ['angle', 'query', 'rationale'],
        properties: {
          angle:     { type: 'string' },
          query:     { type: 'string' },
          rationale: { type: 'string' },
        },
      },
    },
  },
};

const SEARCH_SCHEMA = {
  type: 'object',
  required: ['angle', 'results'],
  properties: {
    angle: { type: 'string' },
    results: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'url', 'snippet', 'relevance'],
        properties: {
          title:     { type: 'string' },
          url:       { type: 'string' },
          snippet:   { type: 'string' },
          relevance: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
      },
    },
  },
};

const VERSION_SCHEMA = {
  type: 'object',
  required: ['original_url', 'is_current', 'current_version', 'current_pdf_url', 'publisher_page_url'],
  properties: {
    original_url:       { type: 'string' },
    is_current:         { type: 'boolean' },
    current_version:    { type: 'string' },
    current_pdf_url:    { type: 'string', description: 'Direct https URL to the current PDF on the publisher website (a plain downloadable link, NOT a viewer/browser page)' },
    publisher_page_url: { type: 'string', description: 'Publisher library page where version was confirmed' },
    notes:              { type: 'string' },
  },
};

// Schema for a single extraction attempt
const ATTEMPT_SCHEMA = {
  type: 'object',
  required: ['attempt_number', 'strategy', 'found', 'locations_searched'],
  properties: {
    attempt_number:    { type: 'integer', enum: [1, 2] },
    strategy:          { type: 'string', description: 'Describe the specific search strategy used (e.g. keyword search, table-of-contents navigation, section header scan)' },
    locations_searched:{ type: 'string', description: 'Which pages, sections, or headings were examined' },
    found:             { type: 'boolean' },
    // Required if found is true:
    verbatim_quote:    { type: 'string', description: 'Exact text as it appears in the source — single line only, no combining lines, no punctuation changes' },
    page_number:       { type: 'integer', description: 'Page number from the document own pagination, not a line number from text extraction' },
    section_reference: { type: 'string', description: 'Section heading and number as it appears in the document' },
    // Required if found is false:
    reason_not_found:  { type: 'string', description: 'Why the content was not found after this attempt' },
  },
};

const EXTRACT_SCHEMA = {
  type: 'object',
  required: ['source_url', 'pdf_url', 'document_version', 'tool_used', 'scope_applies', 'claims'],
  properties: {
    source_url:       { type: 'string' },
    pdf_url:          { type: 'string', description: 'Direct publisher PDF URL confirmed during version check' },
    document_version: { type: 'string' },
    tool_used:        { type: 'string', enum: ['Read', 'WebFetch', 'GoogleDrive'], description: 'How the document was opened. Read = curl-downloaded PDF read from disk (preferred for PDFs, gives real page numbers). WebFetch = fetched an HTML page as text. NO browser/Playwright/chrome. Bash grep/sed/pdftotext not permitted for extraction.' },
    // Scope gate
    scope_applies:    { type: 'boolean', description: 'Does the document scope cover the specific product, feedstock, or pathway being researched?' },
    scope_quote:      { type: 'string', description: 'Verbatim single-line quote from the document scope section confirming applicability or non-applicability' },
    scope_section:    { type: 'string', description: 'Section where scope was confirmed' },
    // Only populated if scope_applies is true:
    claims: {
      type: 'array',
      items: {
        type: 'object',
        required: ['claim', 'attempts'],
        properties: {
          claim:   { type: 'string', description: 'The substantive finding or requirement' },
          attempts: {
            type: 'array',
            minItems: 1,
            maxItems: 2,
            items: ATTEMPT_SCHEMA,
            description: 'One or two extraction attempts. Stop at first success. Second attempt must use a different strategy than the first.',
          },
          // Populated from the successful attempt:
          verbatim_quote:    { type: 'string' },
          page_number:       { type: 'integer' },
          section_reference: { type: 'string' },
          confirmed:         { type: 'boolean' },
        },
      },
    },
  },
};

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['claim', 'source_url', 'verdict', 'votes'],
  properties: {
    claim:      { type: 'string' },
    source_url: { type: 'string' },
    verdict:    { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] },
    votes: {
      type: 'array',
      minItems: 3,
      maxItems: 3,
      items: {
        type: 'object',
        required: ['vote', 'reasoning'],
        properties: {
          vote:      { type: 'string', enum: ['confirmed', 'refuted'] },
          reasoning: { type: 'string' },
        },
      },
    },
    surviving_quote:      { type: 'string', description: 'Verbatim quote from verified claim' },
    surviving_page:       { type: 'integer' },
    surviving_section:    { type: 'string' },
    surviving_pdf_url:    { type: 'string' },
  },
};

const REPORT_SCHEMA = {
  type: 'object',
  required: ['title', 'summary', 'findings', 'sources'],
  properties: {
    title:   { type: 'string' },
    summary: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['finding', 'verbatim_quote', 'page_number', 'section_reference', 'pdf_url', 'confidence'],
        properties: {
          finding:           { type: 'string' },
          verbatim_quote:    { type: 'string' },
          page_number:       { type: 'integer' },
          section_reference: { type: 'string' },
          pdf_url:           { type: 'string', description: 'Direct publisher PDF URL' },
          confidence:        { type: 'string', enum: ['high', 'medium', 'low'] },
          caveats:           { type: 'string' },
        },
      },
    },
    sources: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'version', 'pdf_url', 'publisher_page'],
        properties: {
          title:          { type: 'string' },
          version:        { type: 'string' },
          pdf_url:        { type: 'string' },
          publisher_page: { type: 'string' },
        },
      },
    },
    unverified_claims: { type: 'array', items: { type: 'string' } },
    not_found:         { type: 'array', items: { type: 'string' }, description: 'Topics searched but not found after exhausting attempts' },
  },
};

// ─── PHASE 1: SCOPE ───────────────────────────────────────────────────────────
phase('Scope')
const question = args || 'No research question provided'

const scopeResult = await agent(
  `Decompose this research question into exactly 5 distinct search angles. ` +
  `Each angle should approach the question from a different direction (e.g. regulatory text, ` +
  `secondary analysis, practitioner guidance, case studies, definitions/scope). ` +
  `Research question: ${question}`,
  { label: 'decompose', phase: 'Scope', schema: ANGLES_SCHEMA }
)

if (!scopeResult) return { error: 'Scope decomposition failed' }
const angles = scopeResult.angles
log(`Decomposed into ${angles.length} search angles`)

// ─── PHASE 2: SEARCH ──────────────────────────────────────────────────────────
phase('Search')
const searchResults = await parallel(
  angles.map(a => () => agent(
    `Search the web for: ${a.query}\n\nAngle: ${a.angle}\nRationale: ${a.rationale}\n\n` +
    `Return up to 8 results. Mark relevance high/medium/low. Prefer primary sources ` +
    `(regulatory bodies, standards organizations, official publishers) over secondary.\n\n` +
    `TOOLING (mandatory): Use the WebSearch tool only. Do NOT use any browser tool ` +
    `(Playwright, chrome-control, or any browser_* tool) — those open windows on the user's ` +
    `screen and interrupt their work. WebSearch returns results as text and opens nothing.`,
    { label: `search:${a.angle}`, phase: 'Search', schema: SEARCH_SCHEMA }
  ))
)

// Collect high/medium relevance URLs, deduplicate
const urlMap = new Map()
for (const sr of searchResults.filter(Boolean)) {
  for (const r of sr.results) {
    if (r.relevance !== 'low' && !urlMap.has(r.url)) {
      urlMap.set(r.url, r)
    }
  }
}
const candidates = Array.from(urlMap.values()).slice(0, 15)
log(`${candidates.length} unique sources to check (after dedup, top 15)`)

// ─── PHASE 3: VERSION CHECK ───────────────────────────────────────────────────
phase('Version Check')
const versionChecks = await parallel(
  candidates.map(c => () => agent(
    `You are checking whether a document URL points to the current published version.\n\n` +
    `Document URL: ${c.url}\nTitle: ${c.title}\n\n` +
    `Steps:\n` +
    `1. Use WebSearch to find the publisher's official library/standards page for this document\n` +
    `2. Use WebFetch on that page to read it as text\n` +
    `3. Confirm the current version number and publication date from that text\n` +
    `4. Identify the direct PDF download URL (a plain https link ending in .pdf or a download endpoint)\n` +
    `5. Record whether the original URL points to the current version\n\n` +
    `TOOLING (mandatory): Use ONLY WebSearch and WebFetch. Do NOT use any browser tool ` +
    `(Playwright, chrome-control, or any browser_* tool) — those open windows on the user's ` +
    `screen and interrupt their work. WebFetch retrieves page text over HTTP and opens nothing.\n\n` +
    `Return the publisher page URL and direct PDF URL as plain https links (not local file paths).`,
    { label: `version:${c.title.slice(0, 30)}`, phase: 'Version Check', schema: VERSION_SCHEMA }
  ))
)

const verified = versionChecks
  .filter(Boolean)
  .filter(v => v.current_pdf_url && v.current_pdf_url.startsWith('http'))

log(`${verified.length} sources version-confirmed with direct PDF URLs`)

// ─── PHASE 4: EXTRACT ─────────────────────────────────────────────────────────
phase('Extract')
const extractions = await pipeline(
  verified,
  v => agent(
    `You are extracting claims from a regulatory or standards document. ` +
    `Follow this exact protocol:\n\n` +
    `DOCUMENT: ${v.current_pdf_url}\n` +
    `VERSION: ${v.current_version}\n` +
    `RESEARCH QUESTION: ${question}\n\n` +
    `TOOLING (mandatory): Do NOT use any browser tool (Playwright, chrome-control, or any ` +
    `browser_* tool) — those open windows on the user's screen and interrupt their work.\n` +
    `For a PDF: first download it silently with Bash to a uniquely-named file in your scratchpad ` +
    `directory (shown in your system prompt; use /tmp if none), e.g. ` +
    `curl -sL "${v.current_pdf_url}" -o "$SCRATCH/src.pdf", then open that local file with the Read ` +
    `tool (Read renders PDF pages and reports real page numbers — use the pages parameter). ` +
    `For an HTML page, use WebFetch. curl-download is only for fetching the file; do NOT use ` +
    `grep/sed/pdftotext to extract the quoted text — read it with the Read tool.\n\n` +
    `STEP 1 — SCOPE GATE (run first, before any extraction attempts):\n` +
    `Open the document per the tooling rules above — NOT Bash grep, sed, or pdftotext for reading.\n` +
    `Find the document's stated scope section. Read it.\n` +
    `Determine: does this document's scope cover the specific product, feedstock, or pathway ` +
    `being researched in the question? Quote the scope section verbatim (single line only).\n` +
    `If scope does NOT apply: return scope_applies=false and stop. Do not attempt extraction.\n\n` +
    `STEP 2 — EXTRACTION (only if scope_applies=true):\n` +
    `Make up to 2 attempts to find the relevant text. Each attempt MUST use a different strategy:\n` +
    `- Strategy options: keyword search, table-of-contents navigation, section header scan, ` +
    `index lookup, definition section review\n` +
    `- Document exactly which pages, sections, or headings you examined in each attempt\n` +
    `- Stop at first success\n` +
    `- If both attempts fail, return found=false with reason\n\n` +
    `QUOTE RULES (non-negotiable):\n` +
    `- Quotes must be character-exact from the source\n` +
    `- Quote only within a single line — do not combine text across line breaks\n` +
    `- Do not modify punctuation, spelling, or spacing\n` +
    `- Record the page number from the document's own pagination (not a line number)\n\n` +
    `tool_used must be one of: Read (curl-downloaded PDF read from disk), WebFetch (HTML page), GoogleDrive`,
    { label: `extract:${v.current_version}`, phase: 'Extract', schema: EXTRACT_SCHEMA }
  )
)

// Filter to scope-applicable sources with at least one confirmed claim
const usable = extractions
  .filter(Boolean)
  .filter(e => e.scope_applies && e.claims && e.claims.some(c => c.confirmed))

log(`${usable.length} sources yielded confirmed claims after scope gate and extraction`)

// Flatten confirmed claims for verification
const claimsToVerify = []
for (const e of usable) {
  for (const c of e.claims.filter(c => c.confirmed)) {
    claimsToVerify.push({ ...c, source: e })
  }
}

// ─── PHASE 5: VERIFY ──────────────────────────────────────────────────────────
phase('Verify')
const verifications = await pipeline(
  claimsToVerify,
  c => parallel([1, 2, 3].map(i => () => agent(
    `You are an adversarial reviewer. Your job is to try to REFUTE this claim.\n\n` +
    `Claim: ${c.claim}\n` +
    `Alleged verbatim quote: "${c.verbatim_quote}"\n` +
    `Alleged source: ${c.source.pdf_url}, page ${c.page_number}, section ${c.section_reference}\n\n` +
    `Check: (1) Does this quote actually appear verbatim at this location? ` +
    `(2) Does this section actually apply to the product/pathway in the research question? ` +
    `(3) Is the claim an accurate reading of the quote, or does it overstate/misread it?\n\n` +
    `Default to refuted=true if you cannot verify.\n\n` +
    `TOOLING (mandatory): To check the source, download the PDF silently with Bash ` +
    `(curl -sL "${c.source.pdf_url}" -o "$SCRATCH/verify.pdf" into your scratchpad dir, or /tmp) ` +
    `then open it with the Read tool, or WebFetch an HTML source. Do NOT use any browser tool ` +
    `(Playwright, chrome-control, or any browser_* tool) — those open windows on the user's screen.`,
    { label: `verify:${i}:${c.claim.slice(0, 30)}`, phase: 'Verify', schema: { type: 'object', required: ['vote', 'reasoning'], properties: { vote: { type: 'string', enum: ['confirmed', 'refuted'] }, reasoning: { type: 'string' } } } }
  ))).then(votes => {
    const validVotes = votes.filter(Boolean)
    const confirmedCount = validVotes.filter(v => v.vote === 'confirmed').length
    const verdict = confirmedCount >= 2 ? 'confirmed' : 'refuted'
    return {
      claim: c.claim,
      source_url: c.source.source_url,
      verdict,
      votes: validVotes,
      surviving_quote: verdict === 'confirmed' ? c.verbatim_quote : null,
      surviving_page: verdict === 'confirmed' ? c.page_number : null,
      surviving_section: verdict === 'confirmed' ? c.section_reference : null,
      surviving_pdf_url: verdict === 'confirmed' ? c.source.pdf_url : null,
    }
  })
)

const confirmed = verifications.flat().filter(Boolean).filter(v => v.verdict === 'confirmed')
log(`${confirmed.length} claims survived adversarial verification`)

// ─── PHASE 6: SYNTHESIZE ──────────────────────────────────────────────────────
phase('Synthesize')
const report = await agent(
  `Synthesize a research report from these verified findings.\n\n` +
  `Research question: ${question}\n\n` +
  `Verified claims (${confirmed.length}):\n` +
  JSON.stringify(confirmed, null, 2) + '\n\n' +
  `Rules for the report:\n` +
  `- Every finding must include: the verbatim quote, page number, section reference, and direct PDF URL\n` +
  `- PDF URLs must be direct links to publisher-hosted PDFs, not local paths or search pages\n` +
  `- Do not combine findings from scope-incompatible sources\n` +
  `- List topics searched but not found in not_found\n` +
  `- Confidence: high = survived 3-vote verify + scope confirmed; medium = 2/3 votes; low = uncertain`,
  { label: 'synthesize', phase: 'Synthesize', schema: REPORT_SCHEMA }
)

return report
