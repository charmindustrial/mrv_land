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

# Shared per-turn block budget: work out a name for the current turn so that
# every guard counts its blocks against the same budget (lib/circuit_breaker.py).
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from transcript_text import turn_key_from_path as _tk_from_path
    _turn = _tk_from_path(transcript_path)
except Exception:
    _turn = None
brk = Breaker(
    state_file=os.path.join(session_dir, 'numeric_block_count'),
    label='NUMERIC INTEGRITY',
    max_strikes=3, turn_key=_turn, transcript_path=transcript_path
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
# Write-detection (tool names + the "did this Bash call actually write"
# check) lives in one shared place now -- see lib/write_detection.py for why:
# four copies of this same logic already drifted apart once (2026-09-10).
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from write_detection import WRITE_TOOL_NAMES, PUBLISH_TOOL_NAMES, is_real_write
except Exception:
    WRITE_TOOL_NAMES, PUBLISH_TOOL_NAMES = set(), set()
    def is_real_write(_): return False

def _is_excluded_deliverable_path(p):
    """Memory files, hook state, scratch/tmp output are never deliverables --
    see citation_integrity_stop.sh's Gate 3 fix (2026-09-16) for why: a Bash
    command's is_real_write() check gates the WHOLE command, so any other
    path-looking string it merely mentions (a cat'd memory file, a
    scratchpad report) was being swept into the harvested deliverable set."""
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
wrote = any(n in WRITE_TOOL_NAMES or n in PUBLISH_TOOL_NAMES for n in tool_names.values())
_DELIV_RE = re.compile(r'\.(?:xlsx|docx|csv|md)\b', re.IGNORECASE)
if not wrote:
    for tid, inp in tool_inputs.items():
        if not isinstance(inp, dict): continue
        if tool_names.get(tid) != 'Bash':
            continue  # a non-Bash, non-WRITE_TOOL_NAMES/PUBLISH_TOOL_NAMES call is a read, not a write
        blob = inp.get('command', '')
        if isinstance(blob, str) and _DELIV_RE.search(blob) and is_real_write(blob):
            wrote = True; break
# Scope: only run when this session actually produced work product. A purely
# conversational turn (incidental numbers like "meeting at 3pm", "5 batches")
# must NOT trip the gate — that noise is what gets a hook routed around. The
# global "No Fabricated Numbers" rule in ~/.claude/CLAUDE.md covers chat-only
# figures; this hook protects deliverables, matching citation_integrity_stop.sh.
if not wrote:
    sys.exit(0)

# ── Build corpus of everything READ / GIVEN this session ─────────────────────
# One shared builder, used by this hook and citation_integrity_stop.sh alike:
# ~/.claude/hooks/lib/source_corpus.py. Two copies of this list used to exist
# and both were blind to the same two things -- a PDF opened with the Read tool
# (the result is page images, so no text ever arrived) and a web page fetched
# in the shell (only whatever the command printed arrived, tags and all). On
# 2026-09-22 that reported passages read minutes earlier as invented, four
# times over one turn. Fixing it in one place is the point.
sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
try:
    from source_corpus import build_corpus, sentence_around as _sentence_around
except Exception:
    sys.exit(0)  # shared library missing/broken -- fail open, never crash
# source_file: the session's other transcripts (workers, coordinator) and its
# tool-results folder are read too -- a worker often did the reading (2026-09-24).
_corpus = build_corpus(entries, tool_names, tool_inputs, session_dir,
                       source_file=transcript_path)
corpus_parts = _corpus.parts
# Text the system put into the conversation rather than a person typing it
# (2026-10-27 audit, 31 findings): a coordinator's mid-task message to a
# worker ("Whole document target 4,000-5,500 words"), a loaded skill's rules,
# Max's CLAUDE.md shown in a system note. Claude was handed these words, so
# quoting them or their figures is quoting a source. Hook feedback stays out:
# it repeats the flagged text back.
try:
    from source_corpus import _variants as _sc_variants
    for _e in entries:
        _m = _e.get('message', {})
        if not isinstance(_m, dict) or _m.get('role') != 'user':
            continue
        _c = _m.get('content')
        if isinstance(_c, str):
            _txts = [_c]
        elif isinstance(_c, list):
            _txts = [_x.get('text', '') or '' for _x in _c
                     if isinstance(_x, dict) and _x.get('type') == 'text']
        else:
            _txts = []
        for _t in _txts:
            _st = (_t or '').strip()
            if not _st or 'hook feedback' in _st[:200].lower():
                continue
            if _e.get('isMeta') or _st.startswith('<'):
                corpus_parts.extend(_sc_variants(_t))
except Exception:
    pass
# Documents no reader on this machine could turn into text. Quotes cannot be
# checked against them, so quotes are NOT reported at all this run -- saying
# nothing beats calling an honest quote invented.
unindexed_sources = _corpus.unindexed

def norm_punct(s):
    return (s.replace('‘',"'").replace('’',"'").replace('“','"')
             .replace('”','"').replace('–','-').replace('—','-')
             .replace('…','...'))

# Read's line-number prefixes come as "12\t", padded "   12\t" or "12→" (and
# "L12:" in some tools); strip every form, not only the unpadded tab one.
raw_corpus = norm_punct(re.sub(r'^[ \t]*(?:L\d+:[ \t]?|\d+(?:\t|\u2192))', '',
                               '\n'.join(corpus_parts), flags=re.MULTILINE))
norm_corpus = re.sub(r'\s+', ' ', raw_corpus).strip()
norm_corpus_lower = norm_corpus.lower()
# number-search corpus: drop thousands separators so "15,000" matches "15000"
num_corpus = re.sub(r'(?<=\d),(?=\d)', '', raw_corpus)
# A figure a spreadsheet shows as "7.56496E+4" is also searchable as 75649.6
# (2026-10-27 audit: a workbook's own value was reported as unsourced).
def _e_expand(mm):
    try:
        v = float(mm.group(0))
    except ValueError:
        return ''
    return ('%.10f' % v).rstrip('0').rstrip('.')
_e_extra = [_e_expand(mm) for mm in re.finditer(r'(?<![\w.])\d+(?:\.\d+)?[eE][+-]?\d{1,2}(?![\w])', num_corpus)]
if _e_extra:
    num_corpus += '\n' + ' '.join(x for x in _e_extra if x)

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

resp_sources = []  # list of (label, raw_text); kept SEPARATE per source so a
# quote/number/arithmetic delimiter pair can never straddle two of them.
# Bug fixed 2026-09-16: chat text and a .md deliverable used to be joined
# into ONE buffer before Gate Q paired up quote marks, so a stray " in the
# chat reply paired with an unrelated " later in the deliverable and
# everything in between -- including the deliverable's own headings -- was
# flagged as one fabricated "quote" (real evidence: e2e_project_report.md
# writer blocked twice on a "quote" spanning from chat prose into the
# report's own "## Test 2 - attribution" heading). label=None means
# chat/message text; it stays unprefixed to match this hook's prior message
# format for chat-only findings (see test c below).
chat_parts = []
for entry in entries[last_user+1:]:
    msg = entry.get('message', {})
    if not isinstance(msg, dict) or msg.get('role') != 'assistant': continue
    for item in (msg.get('content') or []):
        if not isinstance(item, dict): continue
        if item.get('type') == 'text':
            chat_parts.append(item.get('text', '') or '')
        elif item.get('type') == 'tool_use' and _is_message_tool(item.get('name', '')):
            t = _tool_input_text(item.get('input', {}))
            if t:
                chat_parts.append(t)
if chat_parts:
    resp_sources.append((None, '\n'.join(chat_parts)))

# Add text deliverables (.md/.csv) written this session -- each file is its
# OWN source, never concatenated with chat text or with another file.
_src_paths = {}   # label -> path, so a file is never used to vouch for itself
for tid, inp in tool_inputs.items():
    if not isinstance(inp, dict): continue
    if tool_names.get(tid) in ('Write',) :
        fp = inp.get('file_path', '')
        if (fp.lower().endswith(('.md', '.csv')) and os.path.isfile(fp)
                and not _is_excluded_deliverable_path(fp)):
            try:
                with open(fp, encoding='utf-8', errors='replace') as fh:
                    resp_sources.append((os.path.basename(fp), fh.read()))
                _src_paths[os.path.basename(fp)] = fp
            except Exception: pass

if not any((t or '').strip() for _, t in resp_sources):
    sys.exit(0)

# ── Shared by the Gate Q additions below (2026-10-27 audit) ─────────────────
try:
    from source_corpus import contains_quote as _contains_quote, normalize_for_match as _nfm
except Exception:
    def _contains_quote(q, pieces): return False
    def _nfm(t): return t or ''
_EDIT_DESC_RE = re.compile(
    r'\b(?:(?:old|new|original|revised|updated|current) (?:wording|sentence|text|line|paragraph|version)|'
    r'before|after|was|is now)\s*\**\s*:\s*\**\s*>?\s*$|'
    r'\b(?:now reads|reads now|now says|rewrote (?:it|this|that|them) (?:to|as)|'
    r'changed (?:it |this |that )?to|replaced (?:it |this |that )?with)\b',
    re.IGNORECASE)
# A heading over a list of the new wording: "Section 2 now reads:" then items.
_EDIT_DESC_LIST_RE = re.compile(r'\b(?:now reads|now says|reads now)\s*\**\s*:\s*\**\s*\n', re.IGNORECASE)
_FN_RE = re.compile(r'(?<=[a-z]{3})\d{1,2}(?=[\s,.;:)]|$)')
_own_edit_cache, _fn_cache = [], []


def _own_edit_pieces():
    if not _own_edit_cache:
        texts = []
        for _tid, _inp in tool_inputs.items():
            if not isinstance(_inp, dict):
                continue
            if tool_names.get(_tid) in ('Write', 'Edit', 'MultiEdit'):
                for _k in ('content', 'new_string', 'old_string'):
                    if isinstance(_inp.get(_k), str):
                        texts.append(_inp[_k])
                for _ed in (_inp.get('edits') or []):
                    if isinstance(_ed, dict):
                        texts += [v for v in (_ed.get('new_string'), _ed.get('old_string')) if isinstance(v, str)]
        try:
            for _p in list(_corpus.own_files):
                _t = _corpus._file_text(_p)
                if _t:
                    _own_edit_cache.append(_t)
        except Exception:
            pass
        _own_edit_cache.extend(_nfm(t) for t in texts if t)
        _own_edit_cache.append('')
    return _own_edit_cache


def _fn_parts():
    if not _fn_cache:
        _fn_cache.extend(_FN_RE.sub('', p) for p in _corpus.norm_parts())
        _fn_cache.append('')
    return _fn_cache


def in_corpus_text(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return len(s) >= 3 and s.lower() in norm_corpus_lower

violations = []

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

# Counts of Claude's OWN text -- "Read the full rewrite (6,598 words)", "2,700
# chars", "4 pages" -- describe the message or file itself, so no source could
# ever hold them (fire-mining cluster 24). Exempt only when the unit is
# words/chars/characters/lines/pages/bytes AND the sentence is about the
# message/report/file, with no rule words (must, shall, limit, ...).
OWN_COUNT_UNIT_RE = re.compile(r'\s*\)?\s*(?:words?|chars?|characters|lines|pages|bytes)\b', re.IGNORECASE)
OWN_TEXT_NOUN_RE = re.compile(
    r'\b(?:message|reply|answer|response|report|summary|file|document|doc|draft|'
    r'rewrite|re-?cut|version|text|memo|brief|notes?|output|section|deck|'
    r'transcript|write-?up|chat|page)s?\b', re.IGNORECASE)
RULE_WORD_RE = re.compile(
    r'\b(?:must|shall|required?|requires|limit|maximum|minimum|at least|no more than)\b',
    re.IGNORECASE)
def own_text_count(text, start, end):
    if not OWN_COUNT_UNIT_RE.match(text[end:end + 24]):
        return False
    sent = _sentence_around(text, start, end)
    return bool(OWN_TEXT_NOUN_RE.search(sent)) and not RULE_WORD_RE.search(sent)

# A division shown as a percentage -- "23/36=63.9" -- is right when the result
# is 100 times the ratio (fire-mining cluster 10: blocked as "expected 0.64").
def arithmetic_ok(a, op, b, c, expect):
    if abs(c - expect) / abs(expect) <= 0.015:
        return True
    if op in ('/', '÷'):
        pct = 100.0 * expect
        return abs(c - pct) / abs(pct) <= 0.015
    return False

# ── GATE A helpers: recompute shown arithmetic "A op B = C" ──────────────────
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

# ── Whole-expression check (added 2026-10-27) ────────────────────────────────
# ARITH_RE sees only the last two numbers before "=", so a correct sum of four
# terms ("14.708 + 1.915 + 0.764 + 8.880 = 26.267"), a product with a
# bracket, a leading minus or a right side that is itself a product was
# reported as wrong math (audit 2026-10-27: 54 of 55 arithmetic findings were
# this). Before reporting, the WHOLE expression on each side of the "=" is
# worked out; the finding is dropped only when that whole expression gives
# the shown result. Wrong math stays wrong at any length.
_XNUM = r'[\$€£]?\d[\d,]*(?:\.\d+)?(?:\s?(?:k|K|M|bn)\b)?%?'
_XTOK = re.compile(r'\s*(?:(' + _XNUM + r')|([×x\*/÷+\-−])|(\()|(\)))')


def _xnum(tok):
    t = tok.replace('$', '').replace('€', '').replace('£', '').replace(',', '').strip()
    pct = t.endswith('%')
    t = t.rstrip('%').strip()
    mult = 1.0
    for suf, mv in (('bn', 1e9), ('k', 1e3), ('K', 1e3), ('M', 1e6)):
        if t.endswith(suf):
            t, mult = t[:-len(suf)].strip(), mv
            break
    v = float(t) * mult
    return v / 100.0 if pct else v


def _xeval(s):
    """Value of an arithmetic expression written in prose, or None.
    Needs at least one operator; numbers, × x * / ÷ + - −, brackets only."""
    s = s.replace('**', ' ')
    s = re.sub(r',\s+(?=[×÷])', ' ', s)            # "0.5133, × 44/12"
    pos, out, ops = 0, [], 0
    s = s.rstrip()
    while pos < len(s):
        m = _XTOK.match(s, pos)
        if not m or m.end() == pos:
            return None
        if m.group(1):
            if out and out[-1] not in ('*', '/', '+', '-', '('):
                return None
            out.append(repr(_xnum(m.group(1))))
        elif m.group(2):
            op = m.group(2)
            if op == 'x':
                # a letter x is "times" only between two numbers
                if not out or out[-1] in ('*', '/', '+', '-', '('):
                    return None
            op = {'×': '*', 'x': '*', '÷': '/', '−': '-'}.get(op, op)
            out.append(op)
            if len(out) > 1:
                ops += 1
        elif m.group(3):
            out.append('(')
        else:
            out.append(')')
        pos = m.end()
    if not ops:
        return None
    try:
        v = eval(' '.join(out), {'__builtins__': {}}, {})
        return float(v)
    except Exception:
        return None


def _xclose(lhs, rhs_val, rhs_txt):
    if rhs_val is None or lhs is None:
        return False
    cands = [rhs_val]
    if rhs_txt.strip().endswith('%'):
        cands.append(rhs_val * 100.0)            # "0.13 ÷ 6.669 = 1.9%"
    for r in cands:
        for l in (lhs, lhs * 100.0):              # a ratio written as a percentage
            if l == 0 and r == 0:
                return True
            if l and abs(r - l) / abs(l) <= 0.015:
                return True
            # a correctly rounded result: 1.949 shown as "1.9"
            mm = re.search(r'\d[\d,]*(?:\.(\d+))?', rhs_txt)
            if mm and len(re.sub(r'^[0.,]*', '', mm.group(0).replace(',', ''))) >= 2:
                d = len(mm.group(1) or '')
                if abs(r - l) <= 0.5 * 10 ** (-d) * 1.0001:
                    return True
    return False


def whole_expression_ok(text, eq_pos):
    """True when the full expression left of the '=' at eq_pos gives the full
    expression (or number) right of it."""
    left = text[max(0, eq_pos - 260):eq_pos]
    # stop at the previous "=", ":", ";", "|", newline or sentence end
    cut = max(left.rfind(ch) for ch in ('=', ':', ';', '|', '\n', '≈'))
    if cut >= 0:
        left = left[cut + 1:]
    right = text[eq_pos + 1:eq_pos + 200]
    rcut = min([k for k in (right.find(ch) for ch in ('=', ';', '|', '\n', '≈')) if k >= 0] or [len(right)])
    right = right[:rcut]
    # right side: longest leading expression or number
    rm = re.match(r'\s*\**\s*((?:' + _XNUM + r'|[\s×\*/÷+\-−()]|(?<=\d) x (?=\d))+)', right)
    if not rm:
        return False
    rtxt = rm.group(1).rstrip(' (').strip()
    while rtxt and rtxt[-1] in '×*/÷+-−(':
        rtxt = rtxt[:-1].strip()
    rv = _xeval(rtxt) if re.search(r'\d\s*[×\*/÷+\-−]\s*[\(\d\$€£]', rtxt) else None
    if rv is None:
        n = re.match(_XNUM, rtxt)
        if not n:
            return False
        rtxt = n.group(0)
        try:
            rv = _xnum(rtxt) if not rtxt.endswith('%') else _xnum(rtxt[:-1])
        except ValueError:
            return False
    # left side: the LONGEST stretch before the "=" that is a whole expression
    starts = [i for i, ch in enumerate(left)
              if (ch in '0123456789($€£' or (ch in '-−' and left[i + 1:i + 2].isdigit()))
              and (i == 0 or left[i - 1] in ' \t("\'*')]
    for st in starts:
        lv = _xeval(left[st:])
        if lv is not None:
            return _xclose(lv, rv, rtxt)
    return False

# ── GATE N helpers: claim numbers must be sourced, labeled, or computed ──────
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
            # Only a "k" written as a multiplier ("15k", "15 K"). Any "k" used
            # to count, so "0.33 kg" was also searched as "330" -- with every
            # tool result now in the corpus, some unrelated 330 always turned
            # up and an unsourced figure passed (found 2026-09-24).
            if re.search(r'\d\s?k\b', low) or 'thousand' in low: cands.add(str(int(base*1e3)))
            if re.search(r'\d\s?m\b|million', low): cands.add(str(int(base*1e6)))
            if 'bn' in low or 'billion' in low: cands.add(str(int(base*1e9)))
        except ValueError: pass
    return [c for c in cands if c]

# ── Gate N: more ways a figure can be shown to trace (2026-10-27) ────────────
# Audit of every block since 9/15. Each is a check the figure must PASS, not a
# label it can wear.
# (1) "= X" anywhere: every spelling of X is tried ("4,445" and "4445"). Only
#     the first spelling in a random order used to be tried, so "= 4,445 gal"
#     was reported as unsourced about half the time. "= **109" (bold) and
#     "= −0.119" (signed) count.
def shown_result(cands, text):
    for c in cands:
        if re.search(r'=\s*\**\s*[−+-]?\s*[\$€£]?\s*' + re.escape(c) + r'(?!\d)', text):
            return True
    return False


# (2) The working written next to the figure, and it checks out:
#     after it, in brackets  -- "60.0% (3.52 ÷ 5.867)", "44.9% (98.988 ÷ 220.667 = 0.4486)"
#     before it              -- "9000 × (200 − 37.0)/(530 − 200), then gives 4,445.5"
#     A sum that does not give the figure does not count.
_DERIV_AFTER = re.compile(r'\**[^()\n]{0,60}?\(\s*=?\s*((?:[^()\n]|\([^()\n]{1,60}\)){3,160}?)\s*\)')
_DERIV_BEFORE = re.compile(r'((?:[\d\$€£(]|[−-](?=\d))(?:[^=\n.;:]|\.(?=\d)){2,160}?)\s*(?:=|≈|,?\s*(?:then\s+)?(?:gives|giving|comes to|equals|works out to)(?:\s+about)?)\s*\**\s*[−+-]?\s*\**\s*$')


def _fig(raw):
    d = re.search(r'\d[\d,]*(?:\.\d+)?', raw)
    if not d:
        return None, None
    return float(d.group(0).replace(',', '')), d.group(0) + ('%' if raw.rstrip().endswith('%') else '')


def _matches_fig(val, fig, txt):
    if val is None or fig is None:
        return False
    return _xclose(val, fig, txt) or _xclose(abs(val), fig, txt)


def derivation_follows(text, raw, end):
    m = _DERIV_AFTER.match(text, end)
    if not m or re.search(r'[.!?]\s', text[end:m.start(1)]):
        return False
    inner = m.group(1).split('=')[0]
    fig, txt = _fig(raw)
    return _matches_fig(_xeval(inner), fig, txt)


def derivation_precedes(text, raw, start):
    seg = text[max(0, start - 200):start]
    m = _DERIV_BEFORE.search(seg)
    if not m:
        return False
    fig, txt = _fig(raw)
    expr = m.group(1)
    # longest stretch that is a whole expression
    for i in range(len(expr)):
        if i and expr[i - 1] not in ' (':
            continue
        v = _xeval(expr[i:])
        if v is not None:
            return _matches_fig(v, fig, txt)
    return False


def derived_anywhere(text, raw):
    """The working for this figure is shown beside ANY mention of it in the
    message (a figure worked out once and repeated later counts)."""
    for mm in re.finditer(r'(?<![\d.,])' + re.escape(raw) + r'(?![\d])', text):
        if derivation_follows(text, raw, mm.end()) or derivation_precedes(text, raw, mm.start()):
            return True
    return False


# (3) A rounded form of a more precise figure in a source: "2,568.8" for
#     "2,568.8055555555557", "190,578" for "190,578.54" (rounded or cut off at
#     the shown decimals). Only for figures with five or more significant
#     digits, where a chance match is not credible. Also the same value with
#     trailing zeros: "13,720" for "13,720.00", "158.684" for "158.6840".
def rounded_from_source(cands):
    for c in cands:
        if ',' in c:
            continue
        mm = re.fullmatch(r'(\d+)(?:\.(\d+))?', c)
        if not mm:
            continue
        tz = r'(?:\.0+)?' if mm.group(2) is None else r'0+'
        if re.search(r'(?<![\d.])' + re.escape(c) + tz + r'(?![\d.])', num_corpus):
            return True
        sig = len((mm.group(1) + (mm.group(2) or '')).lstrip('0'))
        if mm.group(2) is None:
            sig = len(mm.group(1).rstrip('0'))
        if sig < 5:
            continue
        dec = len(mm.group(2) or '')
        x = float(c)
        half = 0.5 * 10 ** (-dec)
        for ip in range(int(x - half), int(x + 2 * half) + 1):
            for hit in re.finditer(r'(?<![\d.])' + str(ip) + r'\.(\d+)(?![\d])', num_corpus):
                if len(hit.group(1)) <= dec:
                    continue
                y = float(hit.group(0))
                if x - half <= y < x + 2 * half:
                    return True
    return False


def value_in_corpus(cands):
    for c in cands:
        esc = re.escape(c)
        if re.search(r'(?<![\d.])' + esc + r'(?![\d.])', num_corpus):
            return True
    return False

# ── Run Gates Q, A, N once PER SOURCE -- never across a joined buffer ────────
for src_label, src_text in resp_sources:
    src_text = norm_punct(src_text or '')
    if not src_text.strip():
        continue
    # Strip fenced code blocks and inline code (build scripts, paths — not prose
    # claims) -- EXCEPT a bare identifier (filename, tool name) inside a single
    # backtick span, which is citation evidence, not illustrative code. Shared
    # with citation_integrity_stop.sh / verification_integrity_guard.sh /
    # self_conduct_claim_guard.sh / mrv_doc_output_guard.sh so this behavior
    # can't drift apart between callers again -- see lib/transcript_text.py.
    sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
    try:
        from transcript_text import strip_inline_code as _strip_inline_code_shared
    except Exception:
        sys.exit(0)  # shared library missing/broken -- fail open, never crash
    resp_scan = re.sub(r'```.*?```', ' ', src_text, flags=re.DOTALL)
    resp_scan = _strip_inline_code_shared(resp_scan)
    norm_resp = re.sub(r'\s+', ' ', resp_scan).strip()
    prefix = f'[{src_label}] ' if src_label else ''

    # ── Gate Q: two more honest forms of a quote (2026-10-27 audit) ──────────
    # (a) Claude describing its OWN edit: "Section 2 now reads: "...""",
    #     "Before: "..." After: "..."", "so I rewrote it to "..."". The words
    #     must really be in a file this session wrote or an edit it made (old or
    #     new text); the label must sit before the quote in the same paragraph
    #     or list.
    # (b) A source with a footnote number glued to a word ("propagation
    #     rules8, where") quoted without it.
    def _edit_quote_ok(q, start, _txt=resp_scan):
        pre = _txt[max(0, start - 600):start]
        pre = pre.split('\n\n')[-1]
        if not (_EDIT_DESC_RE.search(pre[-160:]) or _EDIT_DESC_LIST_RE.search(pre)):
            return False
        return _contains_quote(q, _own_edit_pieces())

    def _footnote_ok(q):
        return _contains_quote(_FN_RE.sub('', q.lower()), _fn_parts())

    # ── GATE Q: quoted strings >= 40 chars must exist in the corpus ──────────
    passed_quote_spans = []
    # A quoted passage lives on ONE line. Allowing the pattern to run across a
    # line break made the closing quote of one bullet pair up with the opening
    # quote of the next, so two short quoted phrases in a list were read as one
    # long fabricated quote spanning the text between them -- 2026-09-17, a real
    # handoff message blocked over the stitched-together string
    # '. - The CORSIA contrast sentence, appearing once. - The FCC gloss:'.
    # Excluding the newline makes that pairing impossible.
    # Pair quote marks sequentially first (so a short genuine pair like
    # "which worker is this" is consumed as its own pair), THEN apply the
    # 40+ char length test to each pair -- length must never gate the pairing
    # itself, or a real short quote's closing mark gets stolen by the next
    # phrase's opening mark, stitching two genuine short quotes into one
    # fabricated-looking long one. An odd trailing quote pairs with nothing.
    for m in re.finditer(r'"([^"\n]*)"', resp_scan):
        q = m.group(1).strip()
        if len(q) < 40:
            continue
        # Also accepted: the quote with honest '...' elision, markdown or line
        # numbers (cluster 12), and -- only when the sentence says it is
        # quoting Claude's own earlier message or names the file -- Claude's
        # own earlier words (clusters 14/19; see source_corpus.own_quote_ok).
        if (in_corpus_text(q) or _corpus.has_quote(q)
                or _corpus.own_quote_ok(q, _sentence_around(resp_scan, m.start(), m.end()),
                                        exclude_path=_src_paths.get(src_label))
                or _edit_quote_ok(q, m.start()) or _footnote_ok(q)):
            passed_quote_spans.append((m.start(), m.end()))
        else:
            snippet = (q[:80] + '…') if len(q) > 80 else q
            violations.append(('QUOTE', f'{prefix}Quoted text not found in any source read this session: "{snippet}"'))

    # Gate N below works on norm_resp (whitespace collapsed), so the spans
    # found above -- measured in resp_scan -- are re-located in norm_resp.
    # Comparing positions from two different texts let a figure far from any
    # quote count as "inside a verified quote" (found 2026-09-24: "0.33 kg"
    # passed unchecked once more quotes began to pass).
    _norm_spans = []
    for _a, _b in passed_quote_spans:
        _qn = re.sub(r'\s+', ' ', resp_scan[_a:_b]).strip()
        if _qn:
            _i = norm_resp.find(_qn)
            while _i != -1:
                _norm_spans.append((_i, _i + len(_qn)))
                _i = norm_resp.find(_qn, _i + 1)

    def inside_passed_quote(pos, _spans=_norm_spans):
        return any(a <= pos <= b for a, b in _spans)

    # ── GATE A: recompute shown arithmetic "A op B = C" ──────────────────────
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
        if (not arithmetic_ok(a, op, b, c, expect)
                and not whole_expression_ok(norm_resp, m.start() + m.group(0).index('='))):
            violations.append(('ARITHMETIC',
                f'{prefix}Shown arithmetic does not compute: {m.group(0).strip()} '
                f'(expected ≈ {expect:,.2f}).'))

    # ── GATE N: claim numbers must be sourced, labeled, or computed ──────────
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
            if own_text_count(norm_resp, pos, m.end()):   # a count of Claude's own text
                continue
            # (c) result of verified arithmetic — approximated: appears as an RHS in resp
            if shown_result(cands, norm_resp):           # (c) shown as a result, any spelling
                continue
            if derived_anywhere(norm_resp, raw):       # working beside it checks out
                continue
            if rounded_from_source(cands):             # rounded form of a sourced figure
                continue
            snippet_lo = max(0, pos-45)
            ctx = norm_resp[snippet_lo:pos+len(raw)+15].strip()
            violations.append(('NUMBER',
                f'{prefix}Unsourced, unlabeled figure "{raw}" — not found in any source read '
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
        if fp.lower().endswith(('.xlsx', '.docx')) and not _is_excluded_deliverable_path(fp):
            deliverable_paths.add(fp)
    elif name == 'Bash':
        cmd = inp.get('command', '')
        # A Bash command merely MENTIONING a deliverable's filename (grep, cat,
        # openpyxl load_workbook for a read) is not proof this session authored
        # it -- only an actual write ACTION is. Without this gate, any read of
        # another session's file inside a Bash call caused this hook to treat
        # that unrelated file as this session's own deliverable and scan it
        # (real bug, 2026-09-16: a QOWV checklist read-only via openpyxl in
        # Bash got flagged for 33 "unsourced figures" it never wrote).
        # Even when the command DOES write for real, it can also mention an
        # unrelated path (a memory file merely cat'd, a scratchpad report) --
        # exclude those categorically, they are never deliverables.
        if isinstance(cmd, str) and is_real_write(cmd):
            for m in re.finditer(r'[\w./\-]+\.(?:xlsx|docx)', cmd, re.IGNORECASE):
                if not _is_excluded_deliverable_path(m.group(0)):
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
            if (expect != 0 and not arithmetic_ok(a, op, b, c, expect)
                    and not whole_expression_ok(block_norm, m.start() + m.group(0).index('='))):
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
                if own_text_count(block_norm, pos, endpos):      # a count of Claude's own text
                    continue
                if any(rr == cands[0] or rr in cands for rr in arith_results):  # (c) verified arithmetic result
                    continue
                if shown_result(cands, block_norm):
                    continue
                if derived_anywhere(block_norm, raw):
                    continue
                if rounded_from_source(cands):
                    continue
                ctx = block_norm[:160]
                violations.append(('NUMBER',
                    f'[{fname}] unsourced figure "{raw}" — not found in any source read '
                    f'this session, no assumption label, not a shown-correct calculation. '
                    f'Row/paragraph: …{ctx}…'))

# ── Verdict ──────────────────────────────────────────────────────────────────
# A quote finding is only honest when every source could actually be read. If a
# PDF could not be turned into text, drop the quote findings and say so.
if unindexed_sources:
    violations = [v for v in violations if v[0] != 'QUOTE']

if not violations:
    _write_bc(0)
    sys.exit(0)

# Claim this turn's next block slot. False means guards have already bounced
# this same turn three times, and this one stands down (lib/circuit_breaker.py).
if not brk.claim_or_release():
    sys.exit(0)
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
for _n in _corpus.note_lines():
    print(_n, file=sys.stderr)
print("", file=sys.stderr)
print("Fix: for each item, either (1) read the primary source and quote/cite the", file=sys.stderr)
print("actual figure, or (2) label it ASSUMPTION/ESTIMATE/PLACEHOLDER and show the", file=sys.stderr)
print("derivation inline.", file=sys.stderr)
try:
    from guard_footer import print_footer
    print_footer()   # the ONE shared re-send instruction (lib/guard_footer.py)
except Exception:
    pass
print("─" * 72, file=sys.stderr)
sys.exit(2)
PYEOF
