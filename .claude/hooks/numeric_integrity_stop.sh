#!/usr/bin/env bash
# numeric_integrity_stop.sh
#
# Stop hook — hard structural gate on NUMBERS and SOURCE QUOTES in the
# final chat response and in text deliverables (.md/.csv) written this session.
#
# Companion to citation_integrity_stop.sh. That hook gates section/clause
# citations (§N.N + verbatim quote). This one closes the gap that let an
# RSB cost estimate ship a fabricated "$1-2k/day" audit rate and an
# un-inflated 2016 figure presented as current: quantitative claims and bare
# source quotes that carry NO citation signal, so the citation hook is silent.
#
# GATE Q (Quotes): every quoted string >= 40 chars in the response must appear
#   verbatim (whitespace/punctuation-normalized) in the corpus of text read
#   this session. A quote that cannot be found was misquoted or invented.
#
# GATE N (Numbers): every "claim number" in the response — currency ($/€/£,
#   USD/EUR), a rate (X/yr, X/tonne, X/day, X gCO2e/MJ), or a percentage —
#   must be one of:
#     (a) present in a source read this session (incl. Max's own messages and
#         command output), OR
#     (b) within 200 chars of an explicit assumption marker
#         (ASSUMPTION / ESTIMATE / PLACEHOLDER / ~ / approx / worked example …), OR
#     (c) the checked result of an arithmetic expression shown in the response.
#   Otherwise the number is unsourced and unlabeled — blocked.
#
# GATE A (Arithmetic): every "A op B = C" written in the response is recomputed.
#   If C does not follow from A and B (>1.5% off), the shown math is wrong — blocked.
#
# This is the mechanical half of the global "No Fabricated Numbers or Facts"
# rule. It cannot know whether a *labeled* number is the right number — but it
# CAN force every bare number to trace to a source read this session or wear an
# assumption label, and it CAN recompute any arithmetic that is shown. Both
# together make the day-rate/vintage failure structurally hard to repeat.
#
# GATE D (Deliverable numbers, added 2026-08-27): the three gates above only
# ever saw the chat response and .md/.csv Write output. A QA batch checklist
# is an .xlsx file whose evidence notes ARE the claims — a weight pulled off a
# scale ticket, a temperature from an ops note, a volume from a test doc — and
# until now those numbers were invisible to this hook by explicit design ("does
# NOT extract numbers from binary .docx or .xlsx bodies"). That exclusion is
# exactly why an agent could write a QA finding backed by a specific weight it
# never actually read anywhere, and nothing here would catch it: the citation
# hook (citation_integrity_stop.sh) only fires on §/Section-style citations,
# not bare numeric evidence notes, and this hook skipped spreadsheets entirely.
# Gate D closes that: it scans every row of every .xlsx (and paragraph of every
# .docx) written or referenced this session with the SAME rule as Gate N above
# — every claim number must be sourced, labeled, or the checked result of shown
# arithmetic — applied per row, so a derived/computed figure (a mass sum, a CI
# calculation) is allowed exactly when its arithmetic is shown and checks out,
# per Max's explicit call on this design (a strict "must appear verbatim
# everywhere" rule would misfire constantly on legitimate computed values).
# Gate D also widens what counts as a "claim number" beyond currency/rate/percent
# to the units a QA evidence note actually uses: lb, kg, MT, gal, psi, ppm, °F/°C,
# and any comma-grouped figure (e.g. "29,510"). It does NOT attempt to verify
# alphanumeric identifiers (tractor/trailer numbers, ticket IDs) — those aren't
# regex-extractable as "numbers" reliably; that remains the adversarial-reviewer
# skill's job (see its SKILL.md primary-source-check section).
#
# Exit codes: 0 = pass, 2 = block (stderr feeds back to Claude as error context).

set -euo pipefail

input="$(cat)"
hook_event="$(echo "$input" | jq -r '.hook_event_name // empty' 2>/dev/null || true)"
transcript_path="$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null || true)"

# For SubagentStop, Claude Code also provides agent_transcript_path -- a file
# scoped to ONLY that one subagent's own turns/tool calls, isolated from the
# parent session's transcript (see citation_integrity_stop.sh for the same
# change and how this was confirmed empirically 2026-08-27). Use it so a
# reviewer sub-agent's numeric claims are checked against what it itself read.
if [ "$hook_event" = "SubagentStop" ]; then
  agent_transcript_path="$(echo "$input" | jq -r '.agent_transcript_path // empty' 2>/dev/null || true)"
  if [ -n "$agent_transcript_path" ] && [ -f "$agent_transcript_path" ]; then
    transcript_path="$agent_transcript_path"
  fi
fi

if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
  exit 0
fi

python3 - "$transcript_path" <<'PYEOF'
import json, re, sys, os, subprocess as _sp

transcript_path = sys.argv[1]
session_dir = os.path.dirname(transcript_path)

# ── Circuit breaker: shared across every hook, see lib/circuit_breaker.py ────
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from circuit_breaker import Breaker
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash

brk = Breaker(
    state_file=os.path.join(session_dir, 'numeric_block_count'),
    label='NUMERIC INTEGRITY',
    max_strikes=3,
)
if brk.tripped():
    sys.exit(0)

block_count = brk.count
def _write_bc(n):
    if n == 0:
        brk.clear()
    else:
        brk._write(n)

# ── Load transcript ──────────────────────────────────────────────────────────
entries = []
try:
    with open(transcript_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try: entries.append(json.loads(line))
                except json.JSONDecodeError: pass
except Exception:
    sys.exit(0)  # can't read transcript; fail open

# ── Index tool_use id → (name, input) ────────────────────────────────────────
tool_names, tool_inputs = {}, {}
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict): continue
    for item in (msg.get('content') or []):
        if isinstance(item, dict) and item.get('type') == 'tool_use':
            tid = item.get('id', '')
            if tid:
                tool_names[tid] = item.get('name', '')
                tool_inputs[tid] = item.get('input', {})

# ── Only run when a deliverable was produced (mirror citation hook) ──────────
WRITE_TOOLS = {'Write', 'Edit', 'mcp__word__create_document', 'mcp__word__insert_text',
               'mcp__word__replace_text', 'mcp__word__save_document'}
PUBLISH_TOOLS = {'mcp__claude_ai_Google_Drive__create_file',
                 'mcp__claude_ai_Slack__slack_create_canvas',
                 'mcp__claude_ai_Slack__slack_update_canvas'}
wrote = any(n in WRITE_TOOLS or n in PUBLISH_TOOLS for n in tool_names.values())
_DELIV_RE = re.compile(r'\.(?:xlsx|docx|csv|md)\b', re.IGNORECASE)
if not wrote:
    for tid, inp in tool_inputs.items():
        if not isinstance(inp, dict): continue
        blob = inp.get('command', '') if tool_names.get(tid) == 'Bash' else inp.get('file_path', '')
        if isinstance(blob, str) and _DELIV_RE.search(blob):
            wrote = True; break
# Scope: only run when this session actually produced work product. A purely
# conversational turn (incidental numbers like "meeting at 3pm", "5 batches")
# must NOT trip the gate — that noise is what gets a hook routed around. The
# global "No Fabricated Numbers" rule in ~/.claude/CLAUDE.md covers chat-only
# figures; this hook protects deliverables, matching citation_integrity_stop.sh.
if not wrote:
    sys.exit(0)

# ── Build corpus of everything READ / GIVEN this session ─────────────────────
SOURCE_READ_TOOLS = {
    'Read', 'WebFetch',
    'mcp__claude_ai_Google_Drive__read_file_content',
    'mcp__claude_ai_Google_Drive__download_file_content',
    'mcp__word__get_document_text',
    'mcp__playwright__browser_snapshot', 'mcp__playwright-mrv__browser_snapshot',
    'mcp__playwright-mrv-2__browser_snapshot', 'mcp__playwright-mrv-3__browser_snapshot',
    'mcp__playwright-mrv-4__browser_snapshot',
    'Bash',  # pdftotext / grep / python calc output — legitimate sourced/computed values
}
corpus_parts, read_paths = [], set()
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict): continue
    role = msg.get('role', '')
    for item in (msg.get('content') or []):
        if not isinstance(item, dict): continue
        t = item.get('type')
        # (1) numbers/quotes the USER supplied are given inputs, not fabrications
        if role == 'user' and t == 'text':
            corpus_parts.append(item.get('text', '') or ''); continue
        # (2) results of source-read / command tools
        if t == 'tool_result':
            name = tool_names.get(item.get('tool_use_id', ''))
            if name not in SOURCE_READ_TOOLS: continue
            if name == 'Read':
                fp = tool_inputs.get(item.get('tool_use_id', ''), {}).get('file_path', '')
                if fp: read_paths.add(fp)
            res = item.get('content', '')
            if isinstance(res, str):
                corpus_parts.append(res)
            elif isinstance(res, list):
                for r in res:
                    if isinstance(r, dict) and r.get('type') == 'text':
                        corpus_parts.append(r.get('text', '') or '')

# Reload Read files from disk (current content; PDFs via pdftotext)
for fp in list(read_paths):
    try:
        if not os.path.isfile(fp): continue
        if fp.lower().endswith('.pdf'):
            r = _sp.run(['pdftotext', fp, '-'], capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and r.stdout: corpus_parts.append(r.stdout)
        else:
            with open(fp, encoding='utf-8', errors='replace') as fh: corpus_parts.append(fh.read())
    except Exception: pass

# Session tool-results dir (oversized outputs saved to disk)
tr_dir = os.path.join(session_dir, 'tool-results')
if os.path.isdir(tr_dir):
    for fn in os.listdir(tr_dir):
        if fn.endswith(('.txt', '.md')):
            try:
                with open(os.path.join(tr_dir, fn), encoding='utf-8', errors='replace') as fh:
                    corpus_parts.append(fh.read())
            except Exception: pass

def norm_punct(s):
    return (s.replace('‘',"'").replace('’',"'").replace('“','"')
             .replace('”','"').replace('–','-').replace('—','-')
             .replace('…','...'))

raw_corpus = norm_punct(re.sub(r'^\d+\t', '', '\n'.join(corpus_parts), flags=re.MULTILINE))
norm_corpus = re.sub(r'\s+', ' ', raw_corpus).strip()
# number-search corpus: drop thousands separators so "15,000" matches "15000"
num_corpus = re.sub(r'(?<=\d),(?=\d)', '', raw_corpus)

# ── Extract the FINAL response: assistant text after the last real user turn ──
last_user = -1
for i, entry in enumerate(entries):
    msg = entry.get('message', {})
    if not isinstance(msg, dict): continue
    if msg.get('role') != 'user': continue
    content = msg.get('content')
    if isinstance(content, str) and content.strip():
        last_user = i
    elif isinstance(content, list) and any(
            isinstance(c, dict) and c.get('type') == 'text' and (c.get('text') or '').strip()
            for c in content):
        last_user = i

# Includes the body of any Slack/Gmail/canvas message-sending tool call, not
# just plain chat text -- see lib/transcript_text.py for why (a report
# delivered purely via slack_send_message was invisible to a check that only
# ever looked at type=='text' content blocks).
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from transcript_text import _is_message_tool, _tool_input_text
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash

resp_parts = []
for entry in entries[last_user+1:]:
    msg = entry.get('message', {})
    if not isinstance(msg, dict) or msg.get('role') != 'assistant': continue
    for item in (msg.get('content') or []):
        if not isinstance(item, dict): continue
        if item.get('type') == 'text':
            resp_parts.append(item.get('text', '') or '')
        elif item.get('type') == 'tool_use' and _is_message_tool(item.get('name', '')):
            t = _tool_input_text(item.get('input', {}))
            if t:
                resp_parts.append(t)

# Add text deliverables (.md/.csv) written this session
for tid, inp in tool_inputs.items():
    if not isinstance(inp, dict): continue
    if tool_names.get(tid) in ('Write',) :
        fp = inp.get('file_path', '')
        if fp.lower().endswith(('.md', '.csv')) and os.path.isfile(fp):
            try:
                with open(fp, encoding='utf-8', errors='replace') as fh:
                    resp_parts.append(fh.read())
            except Exception: pass

response = norm_punct('\n'.join(resp_parts))
if not response.strip():
    sys.exit(0)

# Strip fenced code blocks and inline code (build scripts, paths — not prose claims)
resp_scan = re.sub(r'```.*?```', ' ', response, flags=re.DOTALL)
resp_scan = re.sub(r'`[^`]*`', ' ', resp_scan)
norm_resp = re.sub(r'\s+', ' ', resp_scan).strip()

def in_corpus_text(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s) >= 3 and s.lower() in norm_corpus.lower()

violations = []

# ── GATE Q: quoted strings >= 40 chars must exist in the corpus ──────────────
passed_quote_spans = []
for m in re.finditer(r'"([^"]{40,})"', resp_scan):
    q = m.group(1).strip()
    if in_corpus_text(q):
        passed_quote_spans.append((m.start(), m.end()))
    else:
        snippet = (q[:80] + '…') if len(q) > 80 else q
        violations.append(('QUOTE', f'Quoted text not found in any source read this session: "{snippet}"'))

def inside_passed_quote(pos):
    return any(a <= pos <= b for a, b in passed_quote_spans)

# ── Assumption-marker detector ───────────────────────────────────────────────
# STRICT set only. Deliberately EXCLUDES hedge words ("roughly", "about",
# "approx", "~") and document-type words ("estimate") — a hedge is not a
# declared assumption; fabrication routinely hides behind "about $X". A number
# passes here only if it wears an explicit not-sourced label, bound tightly to
# the figure (same clause, ≤60 chars) — not merely somewhere in the paragraph.
ASSUMPTION_RE = re.compile(
    r'\bassum\w*|\bplaceholder|\billustrativ|\bhypothetical|\bballpark|\bguess\w*|'
    r'\bunsourced|not (?:yet )?sourced|worked example|order of magnitude|'
    r'\bTBD\b|to be confirmed|\bnotional\b|\bindicative\b|\bstand-?in\b',
    re.IGNORECASE)
def near_assumption(pos, text, window=60):
    lo, hi = max(0, pos-window), min(len(text), pos+window)
    return bool(ASSUMPTION_RE.search(text[lo:hi]))

# ── GATE A: recompute shown arithmetic "A op B = C" ──────────────────────────
def to_num(tok):
    tok = tok.replace(',', '').strip()
    mult = 1.0
    m = re.match(r'^([\d.]+)\s*(k|K|m|M|bn|B)?$', tok)
    if not m: return None
    val = float(m.group(1)); suf = m.group(2)
    if suf in ('k', 'K'): mult = 1e3
    elif suf in ('m', 'M'): mult = 1e6
    elif suf in ('bn', 'B'): mult = 1e9
    return val * mult

ARITH_RE = re.compile(
    r'[\$€£]?\s*([\d,]+(?:\.\d+)?(?:[kKmMbB]|bn)?)\s*([×x\*/÷+\-])\s*'
    r'[\$€£]?\s*([\d,]+(?:\.\d+)?(?:[kKmMbB]|bn)?)\s*=\s*[\$€£]?\s*([\d,]+(?:\.\d+)?(?:[kKmMbB]|bn)?)')
for m in ARITH_RE.finditer(norm_resp):
    a, op, b, c = to_num(m.group(1)), m.group(2), to_num(m.group(3)), to_num(m.group(4))
    if None in (a, b, c): continue
    try:
        if op in ('×', 'x', '*'): expect = a * b
        elif op in ('/', '÷'): expect = a / b if b else None
        elif op == '+': expect = a + b
        elif op == '-': expect = a - b
        else: expect = None
    except ZeroDivisionError:
        expect = None
    if expect is None or expect == 0: continue
    if abs(c - expect) / abs(expect) > 0.015:
        violations.append(('ARITHMETIC',
            f'Shown arithmetic does not compute: {m.group(0).strip()} '
            f'(expected ≈ {expect:,.2f}).'))

# ── GATE N: claim numbers must be sourced, labeled, or computed ──────────────
# Currency, explicit-currency-word amounts, per-unit rates, gCO2e/MJ, percentages.
# Also QA-measurement units (added 2026-08-27 alongside Gate D below): a QA
# finding -- in chat/subagent prose, not only a spreadsheet row -- routinely
# asserts a weight/volume/temperature ("tare weight 29,510 lb") with none of
# the patterns above. Without this, Gate N would see zero "claim numbers" in
# exactly the sentence a QA reviewer's report is built from, regardless of
# whether that number was ever actually sourced.
QA_UNIT_NUM_RE = re.compile(
    r'\d[\d,]*(?:\.\d+)?\s?(?:lbs?|kgs?|MT|mt\b|gal(?:lons?)?|psi|ppm|°F|°C|degF|degC|'
    # Carbon-removal quantities -- the actual units this workspace's numbers
    # are usually in. Missing here meant a bare figure like "47.3 tCDR" or
    # "12,000 BCUs" (no thousands comma, so BARE_NUM_RE misses it too) shipped
    # with no sourcing check at all. Found 2026-09-02 on review.
    r't ?CO2e?|t ?CDR|BCUs?|EACs?)',
    re.IGNORECASE)
BARE_NUM_RE = re.compile(r'(?<![\w.-])\d{1,3}(?:,\d{3})+(?:\.\d+)?(?![\w-])')
NUM_PATTERNS = [
    re.compile(r'[\$€£]\s?\d[\d,]*(?:\.\d+)?\s?(?:k|K|M|bn|billion|million|thousand)?'),
    re.compile(r'\d[\d,]*(?:\.\d+)?\s?(?:USD|EUR|GBP|euros?|dollars?)', re.IGNORECASE),
    re.compile(r'\d[\d,]*(?:\.\d+)?\s?(?:/|per\s)\s?(?:yr|year|tonne|tonnes|t\b|MT|MJ|day|unit|kWh|km|mile|gal)', re.IGNORECASE),
    re.compile(r'\d[\d,]*(?:\.\d+)?\s?gCO2e/MJ', re.IGNORECASE),
    re.compile(r'\d[\d.]*\s?%'),
    QA_UNIT_NUM_RE,
    BARE_NUM_RE,
]
def num_candidates(raw):
    """Numeric strings to search for in the corpus for this figure."""
    digits = re.search(r'\d[\d,]*(?:\.\d+)?', raw)
    if not digits: return []
    core = digits.group(0)
    plain = core.replace(',', '')
    cands = {core, plain}
    low = raw.lower()
    if plain.replace('.', '').isdigit():
        try:
            base = float(plain)
            if 'k' in low or 'thousand' in low: cands.add(str(int(base*1e3)))
            if re.search(r'\bm\b|million', low): cands.add(str(int(base*1e6)))
            if 'bn' in low or 'billion' in low: cands.add(str(int(base*1e9)))
        except ValueError: pass
    return [c for c in cands if c]

def value_in_corpus(cands):
    for c in cands:
        esc = re.escape(c)
        if re.search(r'(?<![\d.])' + esc + r'(?![\d.])', num_corpus):
            return True
    return False

seen = set()
for pat in NUM_PATTERNS:
    for m in pat.finditer(norm_resp):
        raw = m.group(0).strip()
        pos = m.start()
        key = (raw, pos)
        if key in seen: continue
        seen.add(key)
        if inside_passed_quote(pos):            # number inside a verified quote
            continue
        cands = num_candidates(raw)
        if not cands: continue
        # percentages are checked leniently (only block if clearly unsourced AND unlabeled)
        if value_in_corpus(cands):              # (a) appears in a source read this session
            continue
        if near_assumption(pos, norm_resp):     # (b) explicitly labeled an assumption
            continue
        # (c) result of verified arithmetic — approximated: appears as an RHS in resp
        if re.search(r'=\s*[\$€£]?\s*' + re.escape(cands[0]), norm_resp):
            continue
        snippet_lo = max(0, pos-45)
        ctx = norm_resp[snippet_lo:pos+len(raw)+15].strip()
        violations.append(('NUMBER',
            f'Unsourced, unlabeled figure "{raw}" — not found in any source read '
            f'this session and no assumption label nearby. Context: …{ctx}…'))

# ── GATE D: scan .xlsx / .docx deliverable bodies, row/paragraph by row ──────
# (QA_UNIT_NUM_RE / BARE_NUM_RE now defined once, above, as part of NUM_PATTERNS)

def _resolve_deliv(p):
    cands = [p]
    proj_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')
    if proj_dir and not os.path.isabs(p):
        cands.append(os.path.join(proj_dir, p))
    for cand in cands:
        if cand and os.path.isfile(cand):
            return cand
    return None

def _extract_blocks(path):
    if path.lower().endswith('.xlsx'):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        blocks = []
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                blocks.append(' | '.join(str(c) for c in row if c is not None))
        return blocks
    if path.lower().endswith('.docx'):
        import zipfile as _zip
        with _zip.ZipFile(path) as z:
            xml = z.read('word/document.xml').decode('utf-8', 'ignore')
        return [re.sub(r'<[^>]+>', ' ', p) for p in xml.split('</w:p>')]
    return []

deliverable_paths = set()
for tid, inp in tool_inputs.items():
    if not isinstance(inp, dict): continue
    name = tool_names.get(tid, '')
    if name in ('Write', 'Edit'):
        fp = inp.get('file_path', '')
        if fp.lower().endswith(('.xlsx', '.docx')):
            deliverable_paths.add(fp)
    elif name == 'Bash':
        cmd = inp.get('command', '')
        if isinstance(cmd, str):
            for m in re.finditer(r'[\w./\-]+\.(?:xlsx|docx)', cmd, re.IGNORECASE):
                deliverable_paths.add(m.group(0))

for raw_path in deliverable_paths:
    path = _resolve_deliv(raw_path)
    if not path:
        continue
    try:
        blocks = _extract_blocks(path)
    except Exception:
        continue
    fname = os.path.basename(path)
    for block in blocks:
        block = norm_punct(block or '')
        block_norm = re.sub(r'\s+', ' ', block).strip()
        if not block_norm:
            continue

        # Recompute any arithmetic shown within this row/paragraph first, so a
        # verified result is exempt below exactly like Gate A exempts it in chat.
        arith_results = set()
        for m in ARITH_RE.finditer(block_norm):
            a, op, b, c = to_num(m.group(1)), m.group(2), to_num(m.group(3)), to_num(m.group(4))
            if None in (a, b, c): continue
            try:
                if op in ('×', 'x', '*'): expect = a * b
                elif op in ('/', '÷'): expect = a / b if b else None
                elif op == '+': expect = a + b
                elif op == '-': expect = a - b
                else: expect = None
            except ZeroDivisionError:
                expect = None
            if expect is None: continue
            if expect != 0 and abs(c - expect) / abs(expect) > 0.015:
                violations.append(('ARITHMETIC',
                    f'[{fname}] shown arithmetic does not compute: '
                    f'{m.group(0).strip()} (expected ≈ {expect:,.2f}).'))
            else:
                arith_results.add(m.group(4).strip())

        claimed_spans = []
        for pat in NUM_PATTERNS:
            for m in pat.finditer(block_norm):
                raw = m.group(0).strip()
                pos, endpos = m.start(), m.end()
                if any(pos < e and s < endpos for s, e in claimed_spans):
                    continue
                claimed_spans.append((pos, endpos))
                cands = num_candidates(raw)
                if not cands:
                    digits = re.search(r'\d[\d,]*(?:\.\d+)?', raw)
                    if not digits: continue
                    cands = [digits.group(0), digits.group(0).replace(',', '')]
                if value_in_corpus(cands):                       # (a) sourced this session
                    continue
                if near_assumption(pos, block_norm):             # (b) labeled assumption
                    continue
                if any(rr == cands[0] or rr in cands for rr in arith_results):  # (c) verified arithmetic result
                    continue
                if re.search(r'=\s*[\$€£]?\s*' + re.escape(cands[0]), block_norm):
                    continue
                ctx = block_norm[:160]
                violations.append(('NUMBER',
                    f'[{fname}] unsourced figure "{raw}" — not found in any source read '
                    f'this session, no assumption label, not a shown-correct calculation. '
                    f'Row/paragraph: …{ctx}…'))

# ── Verdict ──────────────────────────────────────────────────────────────────
if not violations:
    _write_bc(0)
    sys.exit(0)

_write_bc(block_count + 1)
by_gate = {}
for g, msg in violations:
    by_gate.setdefault(g, []).append(msg)

print("─" * 72, file=sys.stderr)
print("NUMERIC / QUOTE INTEGRITY — response blocked", file=sys.stderr)
print("─" * 72, file=sys.stderr)
print("Every number and source quote in a deliverable must trace to a source read", file=sys.stderr)
print("this session, wear an explicit assumption label, or (numbers) be the checked", file=sys.stderr)
print("result of shown arithmetic. The following did not:", file=sys.stderr)
print("", file=sys.stderr)
labels = {'QUOTE': 'FABRICATED / MISQUOTED SOURCE TEXT',
          'NUMBER': 'UNSOURCED, UNLABELED FIGURES',
          'ARITHMETIC': 'ARITHMETIC THAT DOES NOT COMPUTE'}
for g in ('QUOTE', 'NUMBER', 'ARITHMETIC'):
    if g not in by_gate: continue
    print(f"  [{labels[g]}]", file=sys.stderr)
    for msg in by_gate[g][:12]:
        print(f"   • {msg}", file=sys.stderr)
    if len(by_gate[g]) > 12:
        print(f"   • …and {len(by_gate[g])-12} more", file=sys.stderr)
    print("", file=sys.stderr)
print("Fix: for each item, either (1) read the primary source and quote/cite the", file=sys.stderr)
print("actual figure, or (2) label it ASSUMPTION/ESTIMATE/PLACEHOLDER and show the", file=sys.stderr)
print("derivation inline. Then re-deliver the COMPLETE corrected response.", file=sys.stderr)
print("─" * 72, file=sys.stderr)
sys.exit(2)
PYEOF
