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
# Which transcript this hook is about, and whose counters it belongs to, are
# decided in ONE place: ~/.claude/hooks/lib/subagent_scope.sh. It picks the
# subagent's own transcript on SubagentStop AND exports CLAUDE_HOOK_AGENT_SCOPE,
# so this guard's circuit breaker and the shared per-turn block budget land in
# the same per-worker file every other guard uses. Those two steps used to be
# hand-copied into all fifteen guards, and five copies did the first without the
# second -- see that file's header for the 2026-09-17 failure it caused.
source ~/.claude/hooks/lib/subagent_scope.sh
hook_scope_resolve "$input"
transcript_path="$HOOK_TRANSCRIPT_PATH"
hook_event="$HOOK_EVENT_NAME"

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
# Shared per-turn block budget: work out a name for the current turn so that
# every guard counts its blocks against the same budget (lib/circuit_breaker.py).
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from transcript_text import turn_key_from_path as _tk_from_path
    _turn = _tk_from_path(transcript_path)
except Exception:
    _turn = None
brk = Breaker(
    state_file=os.path.join(session_dir, 'citation_block_count'),
    label='CITATION INTEGRITY',
    max_strikes=3, turn_key=_turn, transcript_path=transcript_path
)
if brk.tripped():
    sys.exit(0)

def block(lines):
    brk.block_and_exit(lines)

reset_block_count = brk.clear

# ── Load transcript ──────────────────────────────────────────────────────────
import datetime as _dt

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
tool_use_times = {}   # tool_use id → when that call was made (epoch seconds)


def _entry_epoch(entry):
    ts = entry.get('timestamp')
    if not isinstance(ts, str) or not ts:
        return None
    try:
        return _dt.datetime.strptime(ts[:19], '%Y-%m-%dT%H:%M:%S').replace(
            tzinfo=_dt.timezone.utc).timestamp()
    except Exception:
        return None


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
                tool_use_times[tid] = _entry_epoch(entry)

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
# Write-detection (tool names + the "did this Bash call actually write"
# check) lives in one shared place now -- see lib/write_detection.py for why:
# four copies of this same logic already drifted apart once (2026-09-10).
try:
    from write_detection import WRITE_TOOL_NAMES, PUBLISH_TOOL_NAMES, is_real_write, write_targets as _write_targets
except Exception:
    WRITE_TOOL_NAMES, PUBLISH_TOOL_NAMES = set(), set()
    def is_real_write(_): return False
    def _write_targets(_): return []

def _is_excluded_deliverable_path(p):
    """Memory files, hook state, scratch/tmp output are never deliverables --
    regardless of write detection. Fix 2026-09-16: Gate 3 was flagging a
    memory file under ~/.claude/.../memory/ that was only READ, and a
    subagent scratchpad report under /private/tmp/.../scratchpad/, because a
    single Bash command that performed a real write ALSO mentioned those
    other paths -- is_real_write() gates the whole command, not the specific
    path, so every path-looking string in that command was swept in."""
    if not p:
        return False
    pp = str(p).replace('\\', '/')
    home_claude = os.path.expanduser('~/.claude')
    if pp.startswith(home_claude) or '/.claude/' in pp:
        return True
    if pp.startswith('/private/tmp/') or pp.startswith('/tmp/') or '/private/tmp/' in pp:
        return True
    if re.search(r'(^|/)scratchpad(/|$)', pp):
        return True
    return False
wrote_files = any(name in WRITE_TOOL_NAMES or name in PUBLISH_TOOL_NAMES
                  for name in tool_uses.values())
_DELIV_REF_RE = re.compile(r'\.(?:xlsx|docx|csv|md)\b', re.IGNORECASE)
if not wrote_files:
    for _tid, _inp in tool_use_inputs.items():
        if not isinstance(_inp, dict):
            continue
        _nm = tool_uses.get(_tid, '')
        if _nm != 'Bash':
            continue  # a non-Bash, non-WRITE_TOOL_NAMES/PUBLISH_TOOL_NAMES call is a read, not a write
        _blob = _inp.get('command', '')
        if isinstance(_blob, str) and _DELIV_REF_RE.search(_blob) and is_real_write(_blob):
            wrote_files = True
            break
if not wrote_files:
    sys.exit(0)

# ── Build corpus from everything read this session ───────────────────────────
# One shared builder for this hook and numeric_integrity_stop.sh:
# ~/.claude/hooks/lib/source_corpus.py. This hook's own copy never looked at a
# web page at all (no WebFetch, no shell fetch in its tool list), and a PDF
# opened with the Read tool arrives as page images, so nothing from it landed
# here either. On 2026-09-22 that combination reported passages read minutes
# earlier as invented, four times over one turn.
import os, subprocess as _sp
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from source_corpus import build_corpus, sentence_around as _sentence_around
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash

# tool_use_inputs (tool id -> its arguments) is already built above.
# include_user_text=True since 2026-09-24: a quote of Max's own typed words, or
# of the coordinator's task prompt in a worker, is a quote of something given
# this session (fire-mining cluster 19). source_file: the session's workers /
# coordinator and its tool-results folder count too (clusters 15 and 18).
_corpus = build_corpus(entries, tool_uses, tool_use_inputs, session_dir,
                       include_user_text=True, source_file=transcript_path)
corpus_parts = _corpus.parts
# Documents no reader on this machine could turn into text: quotes taken from
# them cannot be checked, so they are not called fabricated. Say so instead.
unindexed_sources = _corpus.unindexed

raw_corpus = '\n'.join(corpus_parts)

# Strip Read tool line-number prefixes ("123\t") — Read returns "N\tline_text"
# Padded "   12\t", "12→" and "L12:" forms too, not only an unpadded "12\t".
stripped_corpus = re.sub(r'^[ \t]*(?:L\d+:[ \t]?|\d+(?:\t|\u2192))', '', raw_corpus,
                         flags=re.MULTILINE)

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

    # Not deliverables, so never Gate 3 targets (fire-mining cluster 18, 23
    # wrong blocks): skill files, the knowledge base, anything under .claude,
    # memory folders, hook/agent reports, and working notes or ledgers
    # (*_notes.md, *_ledger.*). They hold Claude's working notes and rules,
    # not claims sent to anyone. Checked on the path as written AND on the
    # real path, because a relative save target hides the folder it is in.
    # Folder names are matched on the path INSIDE the workspace, and with
    # case: the workspace itself sits under ".../Claude/Skills/MRV Expert/",
    # so a plain search for "skills/" would have excused every file in it.
    _GATE3_SKIP_RE = re.compile(
        r'(?:^|/)(?:skills|knowledge-base|\.claude|memory|reports)/'
        r'|(?:_notes\.md|_ledger\.[A-Za-z0-9]+)$')
    _ws_root = (proj_dir or os.getcwd()).rstrip('/')

    def _inside_ws(path):
        pp = str(path).replace('\\', '/')
        if _ws_root and pp.startswith(_ws_root + '/'):
            return pp[len(_ws_root) + 1:]
        return pp

    def _gate3_excluded(p):
        if _is_excluded_deliverable_path(p):
            return True
        cands = [p]
        base_dir = proj_dir or os.getcwd()
        if base_dir and not os.path.isabs(p):
            cands.append(os.path.join(base_dir, p))
        for cand in cands:
            for form in (cand, os.path.realpath(cand)):
                if _is_excluded_deliverable_path(form) or _GATE3_SKIP_RE.search(_inside_ws(form)):
                    return True
        return False

    def _written_by_call(path, call_epoch):
        """Could the command at this moment have produced this file? A file
        last modified BEFORE the command ran was not written by it."""
        if call_epoch is None:
            return True  # no clock to judge by: fail open, check the file
        cands = [path]
        if proj_dir and not os.path.isabs(path):
            cands.append(os.path.join(proj_dir, path))
        for cand in cands:
            try:
                # A minute of slack: the transcript's clock and the file
                # system's are not the same clock.
                if os.path.getmtime(cand) >= (call_epoch - 60):
                    return True
            except Exception:
                continue
        return False

    for tid, inp in tool_use_inputs.items():
        if not isinstance(inp, dict):
            continue
        name = tool_uses.get(tid, '')
        if name in ('Write', 'Edit'):
            fp = inp.get('file_path', '')
            if fp.lower().endswith(('.xlsx', '.docx', '.csv', '.md')) and not _gate3_excluded(fp):
                deliverable_paths.add(fp)
        elif name == 'Bash':
            cmd = inp.get('command', '')
            # A command that merely MENTIONS a filename (a grep, a read-only
            # openpyxl load) never proved this session authored it -- that was
            # the 2026-09-16 fix. Memory files and scratchpads are excluded
            # categorically for the same reason. Harvest ONLY the file the command actually saved to, not every
            # filename it mentions. Gating on is_real_write() and then taking
            # every name was the 2026-09-17 false alarm: one command opened v5
            # of a document read-only and saved v6, and this gate demanded
            # verbatim quotes for v5, which the worker never wrote. The target
            # list lives in lib/write_detection.py so no hook re-derives it.
            if isinstance(cmd, str):
                for target in _write_targets(cmd):
                    if not DELIV_PATH_RE.fullmatch(target):
                        continue
                    if _gate3_excluded(target):
                        continue
                    # A command cannot have written a file that is OLDER than
                    # the command. Second half of the 2026-09-17 fix: taking
                    # only the save target stopped v5 being swept in, but a
                    # command can still quote someone else's save inside text
                    # it is writing -- a report doing exactly that had this
                    # gate demanding quotes for a document finished hours
                    # earlier by another worker. The file's own clock settles
                    # it, and settles the v5 case a second way for free.
                    if not _written_by_call(target, tool_use_times.get(tid)):
                        continue
                    deliverable_paths.add(target)

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
    # Pair quote marks sequentially first, filter by length AFTER pairing --
    # a length threshold baked into the pairing regex itself makes a short
    # genuine quote's closing mark get stolen by the next quote's opening
    # mark, stitching two real short quotes into one fake long one.
    DELIV_QUOTE_RE = re.compile(r'[""\"]([^""\"\n]*)[""\"]')

    def _quote_in_corpus(qt):
        if len(qt) < 15:
            return False
        norm_qt = re.sub(r'\s+', ' ', normalize_punct(qt)).strip()
        return (qt in raw_corpus or qt in stripped_corpus or norm_qt in norm_corpus
                or _corpus.has_quote(qt))   # honest '...', markdown, line numbers (cluster 12)

    deliv_violations = []
    deliv_fabricated = []

    def _scan_blocks(label, blocks, src_path=None):
        # A citation in a block passes only if a corpus-verified quote sits in
        # the SAME block. Any quoted string not found in the corpus = fabricated.
        for block in blocks:
            block = normalize_punct(block)
            if not block:
                continue
            sigs = list(DELIV_SIGNAL_RE.finditer(block))
            qms = [m for m in DELIV_QUOTE_RE.finditer(block) if len(m.group(1).strip()) >= 10]
            qs = [m.group(1).strip() for m in qms]

            def _ok(i, _qms=qms, _qs=qs, _block=block):
                # Claude's own earlier words count only under the narrow
                # self-attribution rule, and never the file being checked
                # (source_corpus.own_quote_ok).
                return (_quote_in_corpus(_qs[i]) or
                        (len(_qs[i]) >= 15 and _corpus.own_quote_ok(
                            _qs[i], _sentence_around(_block, _qms[i].start(), _qms[i].end()),
                            exclude_path=src_path)))
            oks = [_ok(i) for i in range(len(qs))]
            backed = any(oks)
            for i, q in enumerate(qs):
                if unindexed_sources:
                    continue   # a source we could not read; never call it invented
                if len(q) >= 15 and not oks[i]:
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
        _scan_blocks(os.path.basename(path), blocks, src_path=path)

    # (b) text PUBLISHED through an MCP tool (Google Sheet/Doc via Drive, Slack
    #     canvas, Word text args). That text never touches local disk — it lives
    #     in the tool_use input. Gather every string value and scan line-by-line
    #     (line granularity keeps tabular publishes from laundering one quote
    #     across many rows).
    PUBLISH_SCAN_TOOLS = PUBLISH_TOOL_NAMES | {
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

    # Which publishes to judge (2026-10-05). This loop used to scan every
    # publish call in the WHOLE session. A Google Doc created, found wanting,
    # trashed and re-created three times kept getting blocked for text that
    # only the trashed copies held -- every re-send was judged on all three
    # versions, and earlier turns' publishes were judged again forever. Rule
    # now: only publishes made this turn, only the LAST version of each
    # document (same title + folder for a create, same file id for an edit),
    # and never a file this turn moved to the trash.
    _turn_start = 0
    for _i, _e in enumerate(entries):
        _m = _e.get('message', {})
        if not isinstance(_m, dict) or _m.get('role') != 'user':
            continue
        _c = _m.get('content', [])
        if isinstance(_c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in _c):
            continue
        _turn_start = _i
    _turn_ids, _results = [], {}
    for _e in entries[_turn_start:]:
        _m = _e.get('message', {})
        _c = _m.get('content', []) if isinstance(_m, dict) else []
        if not isinstance(_c, list):
            continue
        for _it in _c:
            if not isinstance(_it, dict):
                continue
            if _it.get('type') == 'tool_use' and _it.get('id'):
                _turn_ids.append(_it['id'])
            elif _it.get('type') == 'tool_result':
                _rc = _it.get('content', '')
                if isinstance(_rc, list):
                    _rc = ' '.join(x.get('text', '') for x in _rc if isinstance(x, dict))
                _results[_it.get('tool_use_id', '')] = _rc if isinstance(_rc, str) else ''
    _trashed = set()
    for _tid in _turn_ids:
        _nm = tool_uses.get(_tid, '')
        _in = tool_use_inputs.get(_tid, {})
        if isinstance(_in, dict) and ('trash' in _nm or 'delete' in _nm):
            for _k in ('fileId', 'file_id', 'id', 'documentId'):
                if _in.get(_k):
                    _trashed.add(str(_in[_k]))

    def _created_id(_tid):
        _m = re.search(r'"id"\s*:\s*"([^"]+)"', _results.get(_tid, ''))
        return _m.group(1) if _m else None

    _latest = {}
    for _tid in _turn_ids:
        _in = tool_use_inputs.get(_tid, {})
        if tool_uses.get(_tid) not in PUBLISH_SCAN_TOOLS or not isinstance(_in, dict):
            continue
        _fid = next((str(_in[k]) for k in ('fileId', 'file_id', 'documentId', 'document_id')
                     if _in.get(k)), None)
        if _fid:
            _key = ('file', _fid)
        elif _in.get('title'):
            _key = ('new', str(_in.get('title')), str(_in.get('parentId', '')))
        else:
            _key = ('call', _tid)
        _latest[_key] = _tid
    _publish_ids = [t for t in _latest.values()
                    if _created_id(t) not in _trashed
                    and str(tool_use_inputs.get(t, {}).get('fileId', '')) not in _trashed]

    for tid in _publish_ids:
        inp = tool_use_inputs.get(tid, {})
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
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from transcript_text import strip_inline_code as strip_code_blocks
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash
try:
    from recap import is_narrative, is_heading_line
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash

scannable = strip_code_blocks(last_text)

# ── Extract all verbatim quotes (needed by Gate 0 and Gate 1) ────────────────
# Pair quote marks sequentially first, filter by length AFTER pairing -- see
# DELIV_QUOTE_RE above for why the length test must never gate the pairing.
QUOTE_RE = re.compile(r'[""]([^\""\n]*)[""]')
# Pair first (above), THEN filter to real quotes (>=10 chars stripped) -- a
# length filter here, after pairing, is safe; it must never sit inside the
# pairing regex itself (that was the original bug). Filter the match list
# once so quote_texts/quote_starts/quote_idents stay index-aligned.
quote_matches = [m for m in QUOTE_RE.finditer(scannable) if len(m.group(1).strip()) >= 10]
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
            # A bare heading, or a recap of an earlier/reported gap finding
            # ("Max said Gap 3 was missing a quote"), is not a live unbacked
            # gap assertion. Exemption-gap review, 2026-09-24.
            if is_heading_line(snippet) or is_narrative(snippet):
                continue
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

# ── Own-document pointers (fire-mining cluster 21, 11 wrong blocks) ─────────
# "§3 of this brief", "line 12 of sec_1_2_6.md" (a file written this session),
# "§4.1 SFC MBM: 22 requirement rows", "word counts §1=661", "Section 1 is
# unchanged" point into Claude's OWN output -- where something sits in the
# document being built, how long a section is -- not at an outside source, so
# there is nothing to quote. Exempt: a reference followed by "of this/my/our
# <document word>", one on a line that names a file this session wrote, and
# one followed by a count or status word rather than a claim.
_OWN_DOC_AFTER_RE = re.compile(
    r'\s*(?:,\s*)?(?:of|in)\s+(?:(?:this|my|our)\s+(?:brief|memo|report|document|doc|draft|'
    r'message|reply|summary|file|deck|notes?|rfp|checklist|workbook|sheet|review|write-?up)'
    # "the" only with words that always mean Claude's own working text --
    # "the report" or "the document" can be an outside source.
    r'|the\s+(?:notes|draft|summary|write-?up|ledger|reply|message|checklist))\b',
    re.IGNORECASE)
_OWN_DOC_LINE_RE = re.compile(r'\b(?:doc|document|file|draft)\s+lines?\s+\d', re.IGNORECASE)
_OWN_DOC_COUNT_RE = re.compile(
    r'[^.\n"]{0,40}?(?:=\s*\d|\b\d[\d,]*\s+(?:\w+\s+)?(?:rows?|words?|lines?|paragraphs?|'
    r'references?|items?|cells?|characters|chars)\b|\b(?:is\s+)?(?:unchanged|untouched)\b|'
    r'\blines?\s+\d)', re.IGNORECASE)
_written_names = _corpus.written_basenames()

def _own_doc_pointer(sig, line):
    after = scannable[sig.end():sig.end() + 80]
    if _OWN_DOC_AFTER_RE.match(after) or _OWN_DOC_COUNT_RE.match(after):
        return True
    if _OWN_DOC_LINE_RE.search(line):
        return True
    # A file this session wrote, named right at the reference: "§3 of
    # sec_1_2_6.md", "sec_1_2_6.md §3". Merely naming the file somewhere on
    # the line is not enough -- the same line may also cite an outside rule.
    after_low = after.lower()
    before_low = scannable[max(0, sig.start() - 40):sig.start()].lower()
    for n in _written_names:
        if not n:
            continue
        if re.match(r'\s*(?:,\s*)?(?:of|in)\s+`?' + re.escape(n), after_low):
            return True
        if before_low.rstrip(' `:,').endswith(n):
            return True
    return False

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
        # A bare heading, or a recap of an earlier/reported citation signal
        # ("Max said Section 4.2 requires that ..."), is not a live unbacked
        # claim. Exemption-gap review, 2026-09-24.
        if is_heading_line(snippet) or is_narrative(snippet):
            continue
        if _own_doc_pointer(sig, scannable[line_start:line_end]):
            continue
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
for _qi, qt in enumerate(quote_texts if not unindexed_sources else []):
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
    # Check 4: honest '...' elision, markdown, line-number prefixes (cluster 12)
    if _corpus.has_quote(qt):
        continue
    # Check 5: Claude's own earlier message or a file it wrote -- ONLY when the
    # sentence says so or names the file (clusters 14/19). A repeated invented
    # quote with no such attribution still fails here.
    _qm = quote_matches[_qi]
    if _corpus.own_quote_ok(qt, _sentence_around(scannable, _qm.start(), _qm.end())):
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
    _lines += _corpus.note_lines()
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
