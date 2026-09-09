#!/usr/bin/env bash
# citation_integrity_stop.sh
#
# Stop hook — hard structural gate on citation integrity.
# Fires on every session stop. Self-scopes: no-op if the response
# contains no citation-signal phrases.
#
# GATE 1 (Format): Every citation-signal phrase in the response
#   (§N.N, Section N.N, Clause N.N, Article N.N, Table N,
#    "states/requires/specifies/mandates that", named protocol + version)
#   must be accompanied by a verbatim quoted string within 500 chars.
#
# GATE 2 (Accuracy): Every verbatim quote longer than 15 chars in the
#   response must appear — exactly — in the corpus of text returned by
#   source-read tool calls this session (Read, Google Drive read/download,
#   Playwright snapshot, Word get_document_text).
#
# If Gate 1 fails: the response asserts document content without quoting. Blocked.
# If Gate 2 fails: a quote cannot be found in any opened document. Fabricated. Blocked.
# If no signals: exit 0, response passes through.
#
# Exit codes: 0 = pass, 2 = block (feeds stderr back to Claude as error context).
#
# This makes confabulation structurally impossible:
# you cannot complete a response that claims to cite a source
# unless (a) you produced a verbatim quote AND
#         (b) that quote actually appears in a document you opened this session.

set -euo pipefail

input="$(cat)"
hook_event="$(echo "$input" | jq -r '.hook_event_name // empty' 2>/dev/null || true)"
transcript_path="$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null || true)"

# For SubagentStop, Claude Code also provides agent_transcript_path -- a file
# scoped to ONLY that one subagent's own turns/tool calls (isSidechain:true,
# tagged with that agent's id), isolated from the parent session's transcript.
# Confirmed empirically 2026-08-27 by dumping a real SubagentStop input: the
# main transcript_path is shared across parent + every subagent, so without
# this, a reviewer sub-agent's claims could be "verified" by documents the
# PARENT session read earlier, not anything the reviewer itself opened. Use
# the isolated transcript when present so review claims are checked against
# what that subagent actually did.
if [ "$hook_event" = "SubagentStop" ]; then
  agent_transcript_path="$(echo "$input" | jq -r '.agent_transcript_path // empty' 2>/dev/null || true)"
  if [ -n "$agent_transcript_path" ] && [ -f "$agent_transcript_path" ]; then
    transcript_path="$agent_transcript_path"
  fi
fi

if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
  exit 0
fi

python3 - "$transcript_path" "$hook_event" <<'PYEOF'
import json, re, sys, os
hook_event = sys.argv[2] if len(sys.argv) > 2 else ''

transcript_path = sys.argv[1]

# ── Circuit breaker: shared across every hook, see lib/circuit_breaker.py ────
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from circuit_breaker import Breaker
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash

session_dir = os.path.dirname(transcript_path)
brk = Breaker(
    state_file=os.path.join(session_dir, 'citation_block_count'),
    label='CITATION INTEGRITY',
    max_strikes=3,
)
if brk.tripped():
    sys.exit(0)

def block(lines):
    brk.block_and_exit(lines)

reset_block_count = brk.clear

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
    sys.exit(0)  # Can't read transcript; fail open rather than block

# ── Build tool-use index: id → name (and inputs) ─────────────────────────────
tool_uses = {}
tool_use_inputs = {}
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict):
        continue
    content = msg.get('content', [])
    if not isinstance(content, list):
        continue
    for item in content:
        if isinstance(item, dict) and item.get('type') == 'tool_use':
            tid = item.get('id', '')
            if tid:
                tool_uses[tid] = item.get('name', '')
                tool_use_inputs[tid] = item.get('input', {})

# ── Gate S (SubagentStop only): a review verdict with ZERO tool calls ────────
# Added 2026-08-27. Every gate below this point only runs once "wrote_files"
# is True -- which requires SOME tool call referencing a deliverable. A
# reviewer sub-agent (e.g. adversarial-reviewer) that opens nothing at all
# calls no tool whatsoever, so wrote_files stays False and the early exit
# right below would let it pass through completely unchecked -- the single
# worst case (total non-engagement, not just weak verification) would be
# invisible to every other gate in this file. Catch it here, before that exit.
if hook_event == 'SubagentStop' and not tool_uses:
    REVIEW_VERDICT_RE = re.compile(
        r'###?\s*(?:\d\.\s*)?(?:Confirmed Items|Challenged Items)\b|'
        r'(?:^|\n)\s*-?\s*Verified:|Current Status:',
        re.IGNORECASE)
    _last_for_gate_s = ''
    for _entry in reversed(entries):
        _msg = _entry.get('message', {})
        if not isinstance(_msg, dict) or _msg.get('role') != 'assistant':
            continue
        _content = _msg.get('content', [])
        if isinstance(_content, list):
            _parts = [c.get('text', '') for c in _content
                      if isinstance(c, dict) and c.get('type') == 'text']
            if _parts:
                _last_for_gate_s = '\n'.join(_parts)
                break
        elif isinstance(_content, str) and _content:
            _last_for_gate_s = _content
            break
    if REVIEW_VERDICT_RE.search(_last_for_gate_s):
        block([
            "─" * 72,
            "CITATION INTEGRITY BLOCK — Gate S: Verdict With No Tool Use",
            "─" * 72,
            "This response reads like a completed review (Confirmed/Challenged Items,",
            "'Verified:', 'Current Status:') but this subagent made ZERO tool calls --",
            "nothing was opened, so nothing could have been verified.",
            "",
            "Action: open the primary source(s) / the checklist file before writing",
            "a verdict on any item.",
            "─" * 72,
        ])

# ── Exit early if no file-writing happened this session ─────────────────────
# The hook's job is to protect deliverables. If no files were written,
# this is a conversational session and the hook should not run.
# The PostToolUse-on-Write hook already enforces at write time.
WRITE_TOOLS = {
    'Write', 'Edit',
    'mcp__word__create_document', 'mcp__word__insert_text',
    'mcp__word__replace_text', 'mcp__word__save_document',
}
# Tools that PUBLISH text directly (not necessarily to local disk): a Google
# Sheet/Doc via the Drive API, a Slack canvas. Citations in the text they
# publish must be gated too — that text lives in the tool_use input.
PUBLISH_TOOLS = {
    'mcp__claude_ai_Google_Drive__create_file',
    'mcp__claude_ai_Slack__slack_create_canvas',
    'mcp__claude_ai_Slack__slack_update_canvas',
}
wrote_files = any(name in WRITE_TOOLS or name in PUBLISH_TOOLS
                  for name in tool_uses.values())
# A deliverable can also be produced by a Bash heredoc (openpyxl/python-docx)
# or named in a Write/Edit path. Those citations must be gated too — so do NOT
# exit early if any tool call this session touched an .xlsx/.docx/.csv/.md file.
_DELIV_REF_RE = re.compile(r'\.(?:xlsx|docx|csv|md)\b', re.IGNORECASE)
if not wrote_files:
    for _tid, _inp in tool_use_inputs.items():
        if not isinstance(_inp, dict):
            continue
        _nm = tool_uses.get(_tid, '')
        _blob = _inp.get('command', '') if _nm == 'Bash' else _inp.get('file_path', '')
        if isinstance(_blob, str) and _DELIV_REF_RE.search(_blob):
            wrote_files = True
            break
if not wrote_files:
    sys.exit(0)

# ── Build corpus from source-read tool results ───────────────────────────────
# These tools return actual document text as their result.
SOURCE_READ_TOOLS = {
    'Read',
    'mcp__claude_ai_Google_Drive__read_file_content',
    'mcp__claude_ai_Google_Drive__download_file_content',
    'mcp__word__get_document_text',
    'mcp__playwright__browser_snapshot',
    'mcp__playwright-mrv__browser_snapshot',
    'mcp__playwright-mrv-2__browser_snapshot',
    'mcp__playwright-mrv-3__browser_snapshot',
    'mcp__playwright-mrv-4__browser_snapshot',
}

corpus_parts = []
read_file_paths = set()  # Track paths Read this session so we can reload from disk

# Index tool_use inputs by id so we can get the file_path arg for Read calls
tool_use_inputs = {}
for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict):
        continue
    content = msg.get('content', [])
    if not isinstance(content, list):
        continue
    for item in content:
        if isinstance(item, dict) and item.get('type') == 'tool_use':
            tid = item.get('id', '')
            if tid:
                tool_use_inputs[tid] = item.get('input', {})

for entry in entries:
    msg = entry.get('message', {})
    if not isinstance(msg, dict):
        continue
    content = msg.get('content', [])
    if not isinstance(content, list):
        continue
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get('type') != 'tool_result':
            continue
        tid = item.get('tool_use_id', '')
        tool_name = tool_uses.get(tid)
        if tool_name not in SOURCE_READ_TOOLS:
            continue
        # Track file paths for Read calls so we can reload current content
        if tool_name == 'Read':
            fp = tool_use_inputs.get(tid, {}).get('file_path', '')
            if fp:
                read_file_paths.add(fp)
        result = item.get('content', '')
        if isinstance(result, str):
            corpus_parts.append(result)
        elif isinstance(result, list):
            for r in result:
                if isinstance(r, dict) and r.get('type') == 'text':
                    corpus_parts.append(r.get('text', ''))

# Reload every file that was Read this session from disk (current content).
# This handles the case where Claude edits a file after reading it: the transcript
# corpus only has the pre-edit snapshot, but a quote from the edited content is
# legitimate. Reading from disk gives the hook the current post-edit text.
# PDFs are extracted with pdftotext (binary files can't be read as text).
import os, subprocess as _sp
for fp in read_file_paths:
    try:
        if not os.path.isfile(fp):
            continue
        if fp.lower().endswith('.pdf'):
            try:
                r = _sp.run(['pdftotext', fp, '-'],
                            capture_output=True, text=True, timeout=30)
                if r.returncode == 0 and r.stdout:
                    corpus_parts.append(r.stdout)
            except Exception:
                pass  # pdftotext unavailable or failed; fall through silently
        else:
            with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
                corpus_parts.append(fh.read())
    except Exception:
        pass  # Can't read the file; fall back to transcript-only for this path

# Also scan the session tool-results directory for oversized output files saved to disk.
# Large Playwright snapshots and Drive downloads are saved as .txt files with a
# "Output has been saved to /path/..." message instead of inline content.
# Context compaction also removes Read call records, breaking read_file_paths tracking.
# Reading the whole tool-results directory fixes both problems.
tool_results_dir = os.path.join(session_dir, 'tool-results')
if os.path.isdir(tool_results_dir):
    for fname in os.listdir(tool_results_dir):
        if fname.endswith('.txt') or fname.endswith('.md'):
            fpath = os.path.join(tool_results_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
                    corpus_parts.append(fh.read())
            except Exception:
                pass

raw_corpus = '\n'.join(corpus_parts)

# Strip Read tool line-number prefixes ("123\t") — Read returns "N\tline_text"
stripped_corpus = re.sub(r'^\d+\t', '', raw_corpus, flags=re.MULTILINE)

# Normalize typographic punctuation to ASCII equivalents (smart quotes, apostrophes, dashes)
# Drive/Word documents use curly quotes; responses often use straight quotes.
def normalize_punct(text):
    return (text
        .replace('‘', "'").replace('’', "'")   # ' '  → '
        .replace('“', '"').replace('”', '"')   # " "  → "
        .replace('–', '-').replace('—', '-')   # – —  → -
        .replace('…', '...')                        # …    → ...
    )

stripped_corpus = normalize_punct(stripped_corpus)

# Normalized corpus: collapse all whitespace runs to single space, for fuzzy matching
norm_corpus = re.sub(r'\s+', ' ', stripped_corpus).strip()

# ── Gate 3: Citation signals inside written deliverables (.xlsx/.docx) ───────
# Runs BEFORE the chat-text gates so their early exits (no chat citation signals)
# cannot skip it. Closes the blind spot where citations are written into a
# spreadsheet/doc via openpyxl/python-docx in a Bash heredoc: such citations sit
# in a binary file (never read by the chat gates) and often inside a fenced code
# block (stripped before scanning). Every section/clause/table citation in a
# deliverable must be backed by a verbatim quote — in its own row/paragraph —
# that exists in a source document opened this session.
try:
    proj_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')
    DELIV_PATH_RE = re.compile(r'[\w./\-]+\.(?:xlsx|docx|csv|md)', re.IGNORECASE)
    deliverable_paths = set()
    for tid, inp in tool_use_inputs.items():
        if not isinstance(inp, dict):
            continue
        name = tool_uses.get(tid, '')
        if name in ('Write', 'Edit'):
            fp = inp.get('file_path', '')
            if fp.lower().endswith(('.xlsx', '.docx', '.csv', '.md')):
                deliverable_paths.add(fp)
        elif name == 'Bash':
            cmd = inp.get('command', '')
            if isinstance(cmd, str):
                for m in DELIV_PATH_RE.finditer(cmd):
                    deliverable_paths.add(m.group(0))

    def _resolve(p):
        cands = [p]
        if proj_dir and not os.path.isabs(p):
            cands.append(os.path.join(proj_dir, p))
        for cand in cands:
            if cand and os.path.isfile(cand):
                return cand
        return None

    def _extract_blocks(path):
        # One block per spreadsheet ROW or document PARAGRAPH. Pairing is checked
        # WITHIN a block — a quote three rows away cannot back a citation.
        if path.lower().endswith('.xlsx'):
            import openpyxl
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            blocks = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    blocks.append(' | '.join(str(c) for c in row if c is not None))
            return blocks
        if path.lower().endswith('.csv'):
            import csv as _csv
            with open(path, 'r', encoding='utf-8', errors='replace', newline='') as fh:
                return [' | '.join(c for c in row) for row in _csv.reader(fh)]
        if path.lower().endswith('.docx'):
            import zipfile as _zip
            with _zip.ZipFile(path) as z:
                xml = z.read('word/document.xml').decode('utf-8', 'ignore')
            return [re.sub(r'<[^>]+>', ' ', p) for p in xml.split('</w:p>')]
        if path.lower().endswith('.md'):
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                return re.split(r'\n\s*\n', fh.read())   # markdown paragraphs
        return []

    DELIV_SIGNAL_RE = re.compile(
        r'(?:§\s*\d[\d.]*[a-z]?|[Ss]ection\s+\d[\d.]*|[Cc]lause\s+\d[\d.]*'
        r'|[Aa]rticle\s+\d[\d.]*|[Tt]able\s+[A-Z]?\d+)')
    DELIV_QUOTE_RE = re.compile(r'[""\"]([^""\"\n]{10,})[""\"]')

    def _quote_in_corpus(qt):
        if len(qt) < 15:
            return False
        norm_qt = re.sub(r'\s+', ' ', normalize_punct(qt)).strip()
        return qt in raw_corpus or qt in stripped_corpus or norm_qt in norm_corpus

    deliv_violations = []
    deliv_fabricated = []

    def _scan_blocks(label, blocks):
        # A citation in a block passes only if a corpus-verified quote sits in
        # the SAME block. Any quoted string not found in the corpus = fabricated.
        for block in blocks:
            block = normalize_punct(block)
            if not block:
                continue
            sigs = list(DELIV_SIGNAL_RE.finditer(block))
            qs = [m.group(1).strip() for m in DELIV_QUOTE_RE.finditer(block)]
            backed = any(_quote_in_corpus(q) for q in qs)
            for q in qs:
                if len(q) >= 15 and not _quote_in_corpus(q):
                    deliv_fabricated.append((label, q[:150]))
            if sigs and not backed:
                for sig in sigs:
                    ls = block.rfind('|', 0, sig.start())
                    seg = block[ls + 1:][:120].strip() if ls != -1 else block[:120].strip()
                    deliv_violations.append((label, seg))

    # (a) deliverables written to disk (.xlsx/.csv/.docx/.md)
    for raw_path in deliverable_paths:
        path = _resolve(raw_path)
        if not path:
            continue
        try:
            blocks = _extract_blocks(path)
        except Exception:
            continue
        _scan_blocks(os.path.basename(path), blocks)

    # (b) text PUBLISHED through an MCP tool (Google Sheet/Doc via Drive, Slack
    #     canvas, Word text args). That text never touches local disk — it lives
    #     in the tool_use input. Gather every string value and scan line-by-line
    #     (line granularity keeps tabular publishes from laundering one quote
    #     across many rows).
    PUBLISH_SCAN_TOOLS = PUBLISH_TOOLS | {
        'mcp__word__create_document', 'mcp__word__insert_text', 'mcp__word__replace_text',
    }

    def _all_strings(obj):
        if isinstance(obj, str):
            yield obj
        elif isinstance(obj, dict):
            for v in obj.values():
                yield from _all_strings(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from _all_strings(v)

    for tid, inp in tool_use_inputs.items():
        if tool_uses.get(tid) not in PUBLISH_SCAN_TOOLS or not isinstance(inp, dict):
            continue
        blob = '\n'.join(_all_strings(inp))
        if not blob:
            continue
        label = tool_uses.get(tid, 'published').split('__')[-1]
        _scan_blocks(label, blob.split('\n'))

    if deliv_violations or deliv_fabricated:
        _lines = [
            "─" * 72,
            "CITATION INTEGRITY BLOCK — Gate 3: Unbacked Citation in a Deliverable",
            "─" * 72,
        ]
        if deliv_violations:
            seen = []
            for f, s in deliv_violations:
                if (f, s) not in seen:
                    seen.append((f, s))
            _lines.append(f"{len(seen)} citation(s) written into a deliverable file with NO verbatim")
            _lines.append("quote backing them (section/clause/table reference, no quote in the same row):")
            _lines.append("")
            for f, s in seen[:6]:
                _lines.append(f'  ↳ [{f}] {s}')
            if len(seen) > 6:
                _lines.append(f'  … and {len(seen) - 6} more')
        if deliv_fabricated:
            _lines.append("")
            _lines.append("Quote(s) in a deliverable not found in any opened source document:")
            for f, q in deliv_fabricated[:5]:
                _lines.append(f'  ↳ [{f}] "{q}"')
        _lines += [
            "",
            "Rule: a citation written into an .xlsx/.docx deliverable is held to the",
            "same standard as one in chat — backed by exact verbatim source text.",
            "Building via openpyxl/Bash is NOT an exemption. Put the verbatim quote",
            "in the file (e.g. a quote column), or remove the normative citation.",
            "─" * 72,
        ]
        block(_lines)
except SystemExit:
    raise
except Exception:
    pass  # Gate 3 fails open: never hard-crash the stop hook on extraction issues

# ── Get last assistant message text ─────────────────────────────────────────
# Includes the body of any Slack/Gmail/canvas message-sending tool call in
# that same turn, not just plain chat text -- see lib/transcript_text.py for
# why (a report delivered purely via slack_send_message was invisible to a
# check that only ever looked at type=='text' content blocks).
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from transcript_text import last_assistant_text
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash
last_text = last_assistant_text(entries)

if not last_text:
    sys.exit(0)

# ── Strip code blocks before signal/quote detection ─────────────────────────
# Citations inside fenced code blocks and inline code are examples/illustrations,
# not real document claims, and should not trigger the gate.
def strip_code_blocks(text):
    text = re.sub(r'```[\s\S]*?```', '', text)   # fenced code blocks
    text = re.sub(r'`[^`\n]+`', '', text)         # inline code
    return text

scannable = strip_code_blocks(last_text)

# ── Extract all verbatim quotes (needed by Gate 0 and Gate 1) ────────────────
QUOTE_RE = re.compile(r'[""]([^\""\n]{10,})[""]')
quote_matches = list(QUOTE_RE.finditer(scannable))
quote_texts  = [m.group(1).strip() for m in quote_matches]
quote_starts = [m.start() for m in quote_matches]

# Identifiers like ASTM method codes (D5865) or a cert/section number
# (No. 0518.01) that, if shared between a signal and an earlier quote's
# surroundings, mean this signal is a RESTATEMENT of an already-backed
# citation, not a new unbacked one. Used by Gate 0 and Gate 1 -- a Gap N
# reference in a closing summary, or a repeated citation late in a long
# message, restating something already fully quoted earlier should not
# need its own separate nearby quote.
IDENT_RE = re.compile(
    r'\b[A-Za-z]{1,4}\d{3,6}(?:\.\d{1,3})?\b'                       # ASTM-style: D5865
    r'|\bNo\.?\s*\d{2,6}(?:\.\d{1,3})?\b'                            # cert number: No. 0518.01
    r'|§\s*\d[\d.]*[a-z]?'                                           # §4.2
    r'|\b(?:Section|Clause|Article|Table|Gap)\s*[A-Z]?\d[\d.]{0,6}\b',  # Section 4.2, Gap 3
    re.IGNORECASE)

def _idents_near(pos, radius=200):
    lo, hi = max(0, pos - radius), min(len(scannable), pos + radius)
    return set(m.group(0).lower() for m in IDENT_RE.finditer(scannable[lo:hi]))

quote_idents = [_idents_near(qs) for qs in quote_starts]

# ── Gate 0: Gap assertions must cite a requirement ───────────────────────────
# A gap assertion claims that something required by a protocol/document is
# absent from a work product. Every such assertion must be backed by a verbatim
# quote establishing the requirement. Without a quote, the gap is invented.
#
# Trigger phrases: "is absent", "is missing", "not in the work plan",
# "no mention of", "no step", "Gap N —", "Gap N:", etc.
GAP_SIGNAL_RE = re.compile(
    r'(?:'
    r'(?:Gap|Finding|Deficiency)\s+\d+\s*[—:\-]'
    r'|\bthis\s+(?:is\s+a\s+)?gap\b'
    r')',
    re.IGNORECASE | re.MULTILINE
)

gap_signals = list(GAP_SIGNAL_RE.finditer(scannable))
if gap_signals:
    missing_gap_quotes = []
    for sig in gap_signals:
        sig_pos = sig.start()
        window_start = sig_pos - 300
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
            missing_gap_quotes.append(snippet)

    if missing_gap_quotes:
        seen = []
        deduped = []
        for s in missing_gap_quotes:
            if s not in seen:
                seen.append(s)
                deduped.append(s)
        missing_gap_quotes = deduped

        _lines = [
            "─" * 72,
            "CITATION INTEGRITY BLOCK — Gate 0: Gap Assertion Without Requirement Quote",
            "─" * 72,
            "The following gap/finding assertions appear without a verbatim quote",
            "establishing the requirement that is supposedly missing:",
            "",
        ]
        for s in missing_gap_quotes[:5]:
            _lines.append(f'  ↳ {s}')
        if len(missing_gap_quotes) > 5:
            _lines.append(f'  … and {len(missing_gap_quotes) - 5} more')
        _lines += [
            "",
            'Rule: every gap or finding assertion ("is absent", "is missing",',
            '"not in the work plan", "no mention of", "Gap N —", etc.) must be',
            'accompanied by a verbatim quote from the source establishing the',
            'requirement that is supposedly unmet. No quote = no gap.',
            "",
            "Action: open the source document, locate the requirement, quote it",
            "verbatim, then state the gap.",
            "─" * 72,
        ]
        block(_lines)

# ── Gate 1: Citation signal detection ────────────────────────────────────────
# Signals: section/clause references, and "states/requires/etc. that" phrases.
# Named protocol references (e.g. "Bio-oil Protocol v1.1") are NOT signals by
# themselves — only when paired with a section number or predicate verb.
SIGNAL_RE = re.compile(
    r'(?:'
    r'§\s*\d[\d.]*[a-z]?'
    r'|[Ss]ection\s+\d[\d.]*'
    r'|[Cc]lause\s+\d[\d.]*'
    r'|[Aa]rticle\s+\d[\d.]*'
    r'|[Tt]able\s+[A-Z]?\d+'
    r'|(?:[Ss]tates?|[Rr]equires?|[Ss]pecifies?|[Mm]andates?|[Pp]rovides?|[Ss]tipulates?)'
      r'\s+that\s+[^”””\'\n]'
    r')',
    re.MULTILINE
)

signals = list(SIGNAL_RE.finditer(scannable))
if not signals:
    sys.exit(0)  # No citation signals → Gates 1 and 2 are no-ops (Gate 0 already ran)

# IDENT_RE / _idents_near / quote_idents are defined once, above, right after
# quote_starts -- shared with Gate 0.

# ── Gate 1 check: each signal must have a nearby quote ───────────────────────
missing_quote_signals = []
for sig in signals:
    sig_pos = sig.start()
    window_start = sig_pos - 250
    window_end   = sig_pos + 500
    nearby = any(window_start <= qs <= window_end for qs in quote_starts)
    if not nearby:
        # Second chance: a signal whose surrounding identifiers (an ASTM
        # method code, a cert number) match an earlier quote's surroundings
        # is restating a citation already backed earlier in this message --
        # not missing one. Added 2026-08-31 after exactly this false
        # positive: "A2LA Cert. No. 0518.01" / ASTM D5865 etc. quoted in
        # full once, then re-flagged on a later restatement of the same
        # numbers that fell outside the +/-250/500 char window above.
        sig_idents = _idents_near(sig_pos)
        if sig_idents and any(sig_idents & qi for qi in quote_idents):
            continue
        # Extract the line containing the signal for the error message
        line_start = scannable.rfind('\n', 0, sig_pos) + 1
        line_end   = scannable.find('\n', sig_pos)
        if line_end == -1:
            line_end = sig_pos + 150
        snippet = scannable[line_start:line_end].strip()[:120]
        missing_quote_signals.append(snippet)

if missing_quote_signals:
    # Deduplicate lines that appear more than once (multiple signals on same line)
    seen = []
    deduped = []
    for s in missing_quote_signals:
        if s not in seen:
            seen.append(s)
            deduped.append(s)
    missing_quote_signals = deduped

    _lines = [
        "─" * 72,
        "CITATION INTEGRITY BLOCK — Gate 1: Missing Verbatim Quote",
        "─" * 72,
        "The following citation-signal phrases appear in the response without",
        "a verbatim quoted string nearby:",
        "",
    ]
    for s in missing_quote_signals[:5]:
        _lines.append(f'  ↳ {s}')
    if len(missing_quote_signals) > 5:
        _lines.append(f'  … and {len(missing_quote_signals) - 5} more')
    _lines += [
        "",
        'Rule: every §/Section/Clause/Table reference and every phrase of the form',
        '"[document] states/requires/specifies that …" must be accompanied by the',
        'exact verbatim text from the source, in double quotes, within 500 chars.',
        "",
        "Action: open the source document, locate the exact text, and quote it.",
        "─" * 72,
    ]
    block(_lines)

# ── Gate 2: Every quote must exist in the opened-document corpus ─────────────
if not corpus_parts:
    block([
        "─" * 72,
        "CITATION INTEGRITY BLOCK — Gate 2: No Source Documents Opened",
        "─" * 72,
        f"Response contains {len(signals)} citation-signal phrase(s) and",
        f"{len(quote_texts)} quoted string(s), but no source documents were",
        "opened this session via Read, Google Drive, Playwright, or Word.",
        "",
        "A quote that cannot be traced to an opened document is fabricated.",
        "Action: open the source document first, then re-read and re-respond.",
        "─" * 72,
    ])

fabricated = []
for qt in quote_texts:
    if len(qt) < 15:
        continue  # Too short to verify reliably — skip
    qt_norm_punct = normalize_punct(qt)
    norm_qt = re.sub(r'\s+', ' ', qt_norm_punct).strip()

    # Check 1: exact match against raw corpus (handles PDFs / Drive docs)
    if qt in raw_corpus:
        continue
    # Check 2: exact match against line-number-stripped corpus (handles Read tool output)
    if qt in stripped_corpus:
        continue
    # Check 3: whitespace-normalized match (handles minor whitespace differences)
    if norm_qt in norm_corpus:
        continue

    fabricated.append(qt[:150])

if fabricated:
    _lines = [
        "─" * 72,
        "CITATION INTEGRITY BLOCK — Gate 2: Quote Not Found in Any Opened Document",
        "─" * 72,
        "The following quote(s) do not appear verbatim in any document opened",
        "this session via Read, Google Drive, Playwright, or Word:",
        "",
    ]
    for q in fabricated[:5]:
        _lines.append(f'  ↳ "{q}"')
    if len(fabricated) > 5:
        _lines.append(f'  … and {len(fabricated) - 5} more')
    _lines += [
        "",
        "These quotes are fabricated — they were not in the text of any source",
        "read this session. Fabricated quotes are blocked unconditionally.",
        "",
        "Action:",
        "  1. Open the source document (Read / Drive / Playwright).",
        "  2. Locate the exact passage.",
        "  3. Copy the verbatim text into the response.",
        "─" * 72,
    ]
    block(_lines)

# All gates passed.
reset_block_count()
sys.exit(0)
PYEOF

# Propagate Python exit code
exit $?
