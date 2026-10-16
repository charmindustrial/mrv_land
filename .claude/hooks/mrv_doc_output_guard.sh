#!/usr/bin/env bash
# mrv_doc_output_guard.sh
#
# PreToolUse hook — fires before ANY MRV document output tool:
#   Slack canvas, Word docs, file writes (Write/Edit), Google Drive creates.
#
# GATE A — Citation Integrity on document content:
#   Every §/Section/Clause/Table reference and every "states/requires/etc. that"
#   phrase in the outgoing content must be accompanied by a verbatim quoted
#   string within 500 chars (Gate A1), AND that quote must appear exactly in
#   a source document opened this session (Gate A2).
#   Prevents uncited claims from ever reaching a deliverable.
#
# GATE B — Correction Audit:
#   If this same document-write tool has already fired this session (i.e. we
#   are in a correction loop), the current turn's assistant text MUST contain
#   an explicit audit — a numbered or bulleted list that enumerates every
#   instance of the problem being corrected and confirms each is fixed.
#   Prevents partial fixes (acknowledging the easy one, skipping the rest).
#
# Exit 0 → pass
# Exit 2 → block (reason surfaced to Claude)
#
# Tools covered:
#   mcp__claude_ai_Slack__slack_create_canvas
#   mcp__claude_ai_Slack__slack_update_canvas
#   mcp__word__create_document
#   mcp__word__insert_text
#   mcp__word__replace_text
#   Write  (document files only — .md, .csv, .txt, .docx, .xlsx under outputs/)
#   Edit   (document files only — same scope)
#   mcp__claude_ai_Google_Drive__create_file

set -euo pipefail

input="$(cat)"
tool_name="$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null || true)"
transcript_path="$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null || true)"
tool_input="$(echo "$input" | jq -c '.tool_input // {}' 2>/dev/null || echo '{}')"

if [ -z "$tool_name" ]; then exit 0; fi
if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then exit 0; fi

python3 - "$tool_name" "$transcript_path" <<PYEOF
import json, re, sys

tool_name      = sys.argv[1]
transcript_path = sys.argv[2]

# ── Document output tools and how to extract their content ───────────────────
# Maps tool_name → list of input field names to try (first non-empty wins)
DOC_WRITE_TOOLS = {
    'mcp__claude_ai_Slack__slack_create_canvas': ['content'],
    'mcp__claude_ai_Slack__slack_update_canvas': ['content'],
    'mcp__word__create_document':                ['content', 'text'],
    'mcp__word__insert_text':                    ['text', 'content'],
    'mcp__word__replace_text':                   ['new_text', 'content', 'text'],
    'Write':                                     ['content'],
    'Edit':                                      ['new_string'],
    'mcp__claude_ai_Google_Drive__create_file':  ['content'],
}

if tool_name not in DOC_WRITE_TOOLS:
    sys.exit(0)

# ── Re-parse tool_input from stdin (passed via heredoc env) ─────────────────
import os, subprocess
raw_input = subprocess.run(
    ['jq', '-c', '.tool_input // {}'],
    input=open('/dev/stdin', 'rb').read() if False else b'',
    capture_output=True
)
# Use a simpler approach: re-read from transcript last entry
# Actually, parse from the transcript's last tool_use entry for this tool

# ── Load transcript ──────────────────────────────────────────────────────────
entries = []
try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
except Exception:
    sys.exit(0)

# ── Extract doc content: find the LAST pending tool_use for this tool ────────
doc_content = ''
for entry in reversed(entries):
    msg = entry.get('message', {})
    if not isinstance(msg, dict):
        continue
    if msg.get('role') != 'assistant':
        continue
    content_list = msg.get('content', [])
    if not isinstance(content_list, list):
        continue
    for item in reversed(content_list):
        if not isinstance(item, dict):
            continue
        if item.get('type') != 'tool_use':
            continue
        if item.get('name') != tool_name:
            continue
        inp = item.get('input', {})
        for field in DOC_WRITE_TOOLS[tool_name]:
            val = inp.get(field, '')
            if val:
                doc_content = val
                break
        if doc_content:
            break
    if doc_content:
        break

# For Write/Edit: skip non-document files
if tool_name in ('Write', 'Edit'):
    # Try to get file_path from the same tool_use
    file_path = ''
    for entry in reversed(entries):
        msg = entry.get('message', {})
        if not isinstance(msg, dict): continue
        if msg.get('role') != 'assistant': continue
        for item in (msg.get('content', []) or []):
            if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == tool_name:
                file_path = item.get('input', {}).get('file_path', '')
                break
        if file_path: break
    # Only gate document-type output files
    doc_extensions = ('.md', '.csv', '.txt', '.docx', '.xlsx', '.rst')
    is_output = 'outputs/' in file_path or 'deliverables/' in file_path
    is_doc_ext = any(file_path.endswith(e) for e in doc_extensions)
    if not (is_output and is_doc_ext):
        sys.exit(0)

if not doc_content:
    sys.exit(0)

# ── Build tool-use index: id → name ─────────────────────────────────────────
tool_uses = {}
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict): continue
    for item in (msg.get('content', []) or []):
        if isinstance(item, dict) and item.get('type') == 'tool_use':
            tid = item.get('id', '')
            if tid:
                tool_uses[tid] = item.get('name', '')

# ── Build corpus from source-read tool results ───────────────────────────────
SOURCE_READ_TOOLS = {
    'Read',
    'mcp__claude_ai_Google_Drive__read_file_content',
    'mcp__claude_ai_Google_Drive__download_file_content',
    'mcp__word__get_document_text',
}  # certify_read.py / drive_read.py output is opened with Read, so it is covered above

corpus_parts = []
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict): continue
    for item in (msg.get('content', []) or []):
        if not isinstance(item, dict): continue
        if item.get('type') != 'tool_result': continue
        tid = item.get('tool_use_id', '')
        if tool_uses.get(tid) not in SOURCE_READ_TOOLS: continue
        result = item.get('content', '')
        if isinstance(result, str):
            corpus_parts.append(result)
        elif isinstance(result, list):
            for r in result:
                if isinstance(r, dict) and r.get('type') == 'text':
                    corpus_parts.append(r.get('text', ''))

raw_corpus   = '\n'.join(corpus_parts)
stripped_corpus = re.sub(r'^\d+\t', '', raw_corpus, flags=re.MULTILINE)
norm_corpus  = re.sub(r'\s+', ' ', stripped_corpus).strip()

# ── Strip code blocks before scanning ────────────────────────────────────────
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from transcript_text import strip_inline_code as strip_code_blocks
except Exception:
    def strip_code_blocks(text):
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`\n]+`', '', text)
        return text

scannable = strip_code_blocks(doc_content)

# ── GATE A1: Citation signals must have nearby verbatim quotes ───────────────
SIGNAL_RE = re.compile(
    r'(?:'
    r'§\s*\d[\d.]*[a-z]?'
    r'|[Ss]ection\s+\d[\d.]*'
    r'|[Cc]lause\s+\d[\d.]*'
    r'|[Aa]rticle\s+\d[\d.]*'
    r'|[Tt]able\s+[A-Z]?\d+'
    r'|(?:[Ss]tates?|[Rr]equires?|[Ss]pecifies?|[Mm]andates?|[Pp]rovides?|[Ss]tipulates?)'
      r'\s+(?:that\s+)?[^"""\'\n]'
    r')',
    re.MULTILINE
)

QUOTE_RE = re.compile(r'[""]([^\""\n]{10,})[""]')

signals     = list(SIGNAL_RE.finditer(scannable))
quote_matches = list(QUOTE_RE.finditer(scannable))
quote_texts   = [m.group(1).strip() for m in quote_matches]
quote_starts  = [m.start() for m in quote_matches]

# Identifiers (ASTM-style codes, cert numbers, §/Section/Clause/Article/Table/
# Gap N) that, if shared between a signal and an earlier quote's surroundings,
# mean this signal restates an already-backed citation rather than
# introducing a new unbacked one. Mirrors citation_integrity_stop.sh's Gate 0/
# Gate 1 fix (2026-08-31) -- this file has the identical window-only check and
# the identical false-positive risk on a long document that correctly cites
# something once and restates it later.
IDENT_RE = re.compile(
    r'\b[A-Za-z]{1,4}\d{3,6}(?:\.\d{1,3})?\b'
    r'|\bNo\.?\s*\d{2,6}(?:\.\d{1,3})?\b'
    r'|§\s*\d[\d.]*[a-z]?'
    r'|\b(?:Section|Clause|Article|Table|Gap)\s*[A-Z]?\d[\d.]{0,6}\b',
    re.IGNORECASE)

def _idents_near(pos, radius=200):
    lo, hi = max(0, pos - radius), min(len(scannable), pos + radius)
    return set(m.group(0).lower() for m in IDENT_RE.finditer(scannable[lo:hi]))

quote_idents = [_idents_near(qs) for qs in quote_starts]

missing_quote_signals = []
for sig in signals:
    sig_pos = sig.start()
    window_start = sig_pos - 250
    window_end   = sig_pos + 500
    nearby = any(window_start <= qs <= window_end for qs in quote_starts)
    if not nearby:
        sig_idents = _idents_near(sig_pos)
        if sig_idents and any(sig_idents & qi for qi in quote_idents):
            continue
        line_start = scannable.rfind('\n', 0, sig_pos) + 1
        line_end   = scannable.find('\n', sig_pos)
        if line_end == -1:
            line_end = sig_pos + 150
        snippet = scannable[line_start:line_end].strip()[:120]
        missing_quote_signals.append(snippet)

if missing_quote_signals:
    seen, deduped = [], []
    for s in missing_quote_signals:
        if s not in seen:
            seen.append(s); deduped.append(s)
    print('─' * 72, file=sys.stderr)
    print('DOC OUTPUT BLOCK — Gate A1: Citation Signal Without Verbatim Quote', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    print(f'The following citation-signal phrases appear in the document content', file=sys.stderr)
    print(f'without a verbatim quoted string nearby:', file=sys.stderr)
    print('', file=sys.stderr)
    for s in deduped[:5]:
        print(f'  ↳ {s}', file=sys.stderr)
    print('', file=sys.stderr)
    print('Rule: every §/Section/Clause/Table reference and every phrase of the', file=sys.stderr)
    print('form "[doc] states/requires/specifies that …" must be accompanied by', file=sys.stderr)
    print('the exact verbatim text from the source, in double quotes, ≤500 chars.', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    sys.exit(2)

# ── GATE A2: Verbatim quotes must exist in opened-document corpus ────────────
if signals and not corpus_parts:
    print('─' * 72, file=sys.stderr)
    print('DOC OUTPUT BLOCK — Gate A2: No Source Documents Opened', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    print('Document content contains citation signals and quoted strings, but no', file=sys.stderr)
    print('source documents were opened this session via Read/Drive/Word (API tool output is opened with Read).', file=sys.stderr)
    print('Open the source document first, then re-draft.', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    sys.exit(2)

fabricated = []
for qt in quote_texts:
    if len(qt) < 15:
        continue
    norm_qt = re.sub(r'\s+', ' ', qt).strip()
    if qt in raw_corpus: continue
    if qt in stripped_corpus: continue
    if norm_qt in norm_corpus: continue
    fabricated.append(qt[:150])

if fabricated:
    print('─' * 72, file=sys.stderr)
    print('DOC OUTPUT BLOCK — Gate A2: Quote Not Found in Any Opened Document', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    print('The following quote(s) in the document content do not appear verbatim', file=sys.stderr)
    print('in any document opened this session:', file=sys.stderr)
    print('', file=sys.stderr)
    for q in fabricated[:5]:
        print(f'  ↳ "{q}"', file=sys.stderr)
    print('', file=sys.stderr)
    print('These quotes are fabricated. Open the source, locate the exact passage,', file=sys.stderr)
    print('and copy the verbatim text into the document before writing.', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    sys.exit(2)

# ── GATE B: Correction audit required on repeat writes ───────────────────────
# Count how many times this tool has already been called this session
prior_calls = 0
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict): continue
    if msg.get('role') != 'assistant': continue
    for item in (msg.get('content', []) or []):
        if isinstance(item, dict) and item.get('type') == 'tool_use':
            if item.get('name') == tool_name:
                prior_calls += 1

# If this is a repeat write (correction), require explicit audit in current turn text
if prior_calls > 0:
    # Get current turn assistant text (text blocks before this tool call)
    current_turn_text = ''
    for entry in reversed(entries):
        msg = entry.get('message', {})
        if not isinstance(msg, dict): continue
        if msg.get('role') != 'assistant': continue
        content_list = msg.get('content', [])
        if isinstance(content_list, list):
            parts = [c.get('text', '') for c in content_list
                     if isinstance(c, dict) and c.get('type') == 'text']
            if parts:
                current_turn_text = '\n'.join(parts)
                break

    # Audit present if text contains BOTH an audit-signal phrase AND a list with ≥ 2 items.
    # Phrase-only check is too easy to fake with a single sentence; list structure forces
    # actual enumeration of what was found and fixed.
    AUDIT_PHRASE_RE = re.compile(
        r'(?i)('
        r'instance[s]?\s+(found|fixed|of\b)'
        r'|found\s+\d+\s+instance'
        r'|all\s+instance'
        r'|every\s+instance'
        r'|instances?:'
        r'|\bfixed\s+all\b'
        r'|\bchanges?\s+made\b'
        r'|\bissues?\s+fixed\b'
        r'|\bcorrection[s]?\s+made\b'
        r'|\bfollowing\s+(instance|issue|problem|error)[s]?\b'
        r'|AUDIT\s*:'
        r'|corrections?\s+applied'
        r')'
    )
    LIST_ITEM_RE = re.compile(r'^\s*(?:\d+[.)]\s+\S|\*\s+\S|-\s+\S|•\s+\S)', re.MULTILINE)

    has_phrase = bool(AUDIT_PHRASE_RE.search(current_turn_text))
    has_list   = len(LIST_ITEM_RE.findall(current_turn_text)) >= 2

    if not (has_phrase and has_list):
        print('─' * 72, file=sys.stderr)
        print('DOC OUTPUT BLOCK — Gate B: Correction Audit Required', file=sys.stderr)
        print('─' * 72, file=sys.stderr)
        print(f'This is a repeat {tool_name} call ({prior_calls} prior call(s) this', file=sys.stderr)
        print(f'session), indicating a correction cycle.', file=sys.stderr)
        print('', file=sys.stderr)
        print('Before writing a corrected document, your response MUST contain BOTH:', file=sys.stderr)
        print('  1. An audit-signal phrase (e.g. "AUDIT:", "instances found:", "corrections applied",', file=sys.stderr)
        print('     "fixed all instances of X", "following issues fixed")', file=sys.stderr)
        print('  2. A numbered or bulleted list with at least 2 items enumerating what was found/fixed', file=sys.stderr)
        print('', file=sys.stderr)
        print('A single-sentence "here is the revised section" does NOT satisfy Gate B.', file=sys.stderr)
        print('You must itemize every instance corrected before calling this tool.', file=sys.stderr)
        print('─' * 72, file=sys.stderr)
        sys.exit(2)

sys.exit(0)
PYEOF

exit $?
