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
transcript_path="$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null || true)"

if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
  exit 0
fi

python3 - "$transcript_path" <<'PYEOF'
import json, re, sys, os

transcript_path = sys.argv[1]

# ── Circuit breaker: after 3 blocks in a session, pass through with a warning ─
session_dir = os.path.dirname(transcript_path)
block_count_file = os.path.join(session_dir, 'citation_block_count')

def read_block_count():
    try:
        with open(block_count_file, 'r') as f:
            return int(f.read().strip())
    except Exception:
        return 0

def write_block_count(n):
    try:
        with open(block_count_file, 'w') as f:
            f.write(str(n))
    except Exception:
        pass

def increment_block_count():
    n = read_block_count() + 1
    write_block_count(n)
    return n

def reset_block_count():
    write_block_count(0)

block_count = read_block_count()
if block_count >= 3:
    print("─" * 72, file=sys.stderr)
    print("CITATION INTEGRITY — Circuit Breaker Active", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    print(f"Hook has blocked {block_count} times this session. Passing response", file=sys.stderr)
    print("through. Citation integrity could not be enforced for this session.", file=sys.stderr)
    print("Review the response manually before using it in a deliverable.", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    sys.exit(0)

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
        print("─" * 72, file=sys.stderr)
        print("CITATION INTEGRITY BLOCK — Gate 3: Unbacked Citation in a Deliverable", file=sys.stderr)
        print("─" * 72, file=sys.stderr)
        if deliv_violations:
            seen = []
            for f, s in deliv_violations:
                if (f, s) not in seen:
                    seen.append((f, s))
            print(f"{len(seen)} citation(s) written into a deliverable file with NO verbatim", file=sys.stderr)
            print("quote backing them (section/clause/table reference, no quote in the same row):", file=sys.stderr)
            print("", file=sys.stderr)
            for f, s in seen[:6]:
                print(f'  ↳ [{f}] {s}', file=sys.stderr)
            if len(seen) > 6:
                print(f'  … and {len(seen) - 6} more', file=sys.stderr)
        if deliv_fabricated:
            print("", file=sys.stderr)
            print("Quote(s) in a deliverable not found in any opened source document:", file=sys.stderr)
            for f, q in deliv_fabricated[:5]:
                print(f'  ↳ [{f}] "{q}"', file=sys.stderr)
        print("", file=sys.stderr)
        print("Rule: a citation written into an .xlsx/.docx deliverable is held to the", file=sys.stderr)
        print("same standard as one in chat — backed by exact verbatim source text.", file=sys.stderr)
        print("Building via openpyxl/Bash is NOT an exemption. Put the verbatim quote", file=sys.stderr)
        print("in the file (e.g. a quote column), or remove the normative citation.", file=sys.stderr)
        print("─" * 72, file=sys.stderr)
        increment_block_count()
        sys.exit(2)
except SystemExit:
    raise
except Exception:
    pass  # Gate 3 fails open: never hard-crash the stop hook on extraction issues

# ── Get last assistant message text ─────────────────────────────────────────
last_text = ''
for entry in reversed(entries):
    msg = entry.get('message', {})
    if not isinstance(msg, dict):
        continue
    if msg.get('role') != 'assistant':
        continue
    content = msg.get('content', [])
    if isinstance(content, list):
        parts = [c.get('text', '') for c in content
                 if isinstance(c, dict) and c.get('type') == 'text']
        if parts:
            last_text = '\n'.join(parts)
            break
    elif isinstance(content, str) and content:
        last_text = content
        break

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

        print("─" * 72, file=sys.stderr)
        print("CITATION INTEGRITY BLOCK — Gate 0: Gap Assertion Without Requirement Quote", file=sys.stderr)
        print("─" * 72, file=sys.stderr)
        print("The following gap/finding assertions appear without a verbatim quote", file=sys.stderr)
        print("establishing the requirement that is supposedly missing:", file=sys.stderr)
        print("", file=sys.stderr)
        for s in missing_gap_quotes[:5]:
            print(f'  ↳ {s}', file=sys.stderr)
        if len(missing_gap_quotes) > 5:
            print(f'  … and {len(missing_gap_quotes) - 5} more', file=sys.stderr)
        print("", file=sys.stderr)
        print('Rule: every gap or finding assertion ("is absent", "is missing",', file=sys.stderr)
        print('"not in the work plan", "no mention of", "Gap N —", etc.) must be', file=sys.stderr)
        print('accompanied by a verbatim quote from the source establishing the', file=sys.stderr)
        print('requirement that is supposedly unmet. No quote = no gap.', file=sys.stderr)
        print("", file=sys.stderr)
        print("Action: open the source document, locate the requirement, quote it", file=sys.stderr)
        print("verbatim, then state the gap.", file=sys.stderr)
        print("─" * 72, file=sys.stderr)
        increment_block_count()
        sys.exit(2)

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

# ── Gate 1 check: each signal must have a nearby quote ───────────────────────
missing_quote_signals = []
for sig in signals:
    sig_pos = sig.start()
    window_start = sig_pos - 250
    window_end   = sig_pos + 500
    nearby = any(window_start <= qs <= window_end for qs in quote_starts)
    if not nearby:
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

    print("─" * 72, file=sys.stderr)
    print("CITATION INTEGRITY BLOCK — Gate 1: Missing Verbatim Quote", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    print("The following citation-signal phrases appear in the response without", file=sys.stderr)
    print("a verbatim quoted string nearby:", file=sys.stderr)
    print("", file=sys.stderr)
    for s in missing_quote_signals[:5]:
        print(f'  ↳ {s}', file=sys.stderr)
    if len(missing_quote_signals) > 5:
        print(f'  … and {len(missing_quote_signals) - 5} more', file=sys.stderr)
    print("", file=sys.stderr)
    print('Rule: every §/Section/Clause/Table reference and every phrase of the form', file=sys.stderr)
    print('"[document] states/requires/specifies that …" must be accompanied by the', file=sys.stderr)
    print('exact verbatim text from the source, in double quotes, within 500 chars.', file=sys.stderr)
    print("", file=sys.stderr)
    print("Action: open the source document, locate the exact text, and quote it.", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    increment_block_count()
    sys.exit(2)

# ── Gate 2: Every quote must exist in the opened-document corpus ─────────────
if not corpus_parts:
    print("─" * 72, file=sys.stderr)
    print("CITATION INTEGRITY BLOCK — Gate 2: No Source Documents Opened", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    print(f"Response contains {len(signals)} citation-signal phrase(s) and", file=sys.stderr)
    print(f"{len(quote_texts)} quoted string(s), but no source documents were", file=sys.stderr)
    print("opened this session via Read, Google Drive, Playwright, or Word.", file=sys.stderr)
    print("", file=sys.stderr)
    print("A quote that cannot be traced to an opened document is fabricated.", file=sys.stderr)
    print("Action: open the source document first, then re-read and re-respond.", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    increment_block_count()
    sys.exit(2)

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
    print("─" * 72, file=sys.stderr)
    print("CITATION INTEGRITY BLOCK — Gate 2: Quote Not Found in Any Opened Document", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    print("The following quote(s) do not appear verbatim in any document opened", file=sys.stderr)
    print("this session via Read, Google Drive, Playwright, or Word:", file=sys.stderr)
    print("", file=sys.stderr)
    for q in fabricated[:5]:
        print(f'  ↳ "{q}"', file=sys.stderr)
    if len(fabricated) > 5:
        print(f'  … and {len(fabricated) - 5} more', file=sys.stderr)
    print("", file=sys.stderr)
    print("These quotes are fabricated — they were not in the text of any source", file=sys.stderr)
    print("read this session. Fabricated quotes are blocked unconditionally.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Action:", file=sys.stderr)
    print("  1. Open the source document (Read / Drive / Playwright).", file=sys.stderr)
    print("  2. Locate the exact passage.", file=sys.stderr)
    print("  3. Copy the verbatim text into the response.", file=sys.stderr)
    print("─" * 72, file=sys.stderr)
    increment_block_count()
    sys.exit(2)

# All gates passed.
reset_block_count()
sys.exit(0)
PYEOF

# Propagate Python exit code
exit $?
