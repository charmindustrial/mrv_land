#!/usr/bin/env bash
# precedent_grounding_guard.sh
#
# Stop hook — structural gate on forestry-biomass PRE-SCREEN deliverables.
#
# The failure this closes: the screener shipped MUST-HAVE gap items
# (grant-recipient EINs, a "letter on CSFS letterhead") that the validated
# precedent — Elk Meadow P2, feedstock COWF-005 — never actually required.
# The skill already said "operational guidance is subordinate to the validated
# precedent," and that prose rule was ignored. Prose is not a control. This is.
#
# RULE: In every screener output written this session
#   - "* BFA v1.3 Pre-Screen.docx"
#   - "*Gap_Checklist*.xlsx" / "*Gap Checklist*.xlsx"
# every MUST-HAVE item must carry a precedent anchor in its own text block —
# a reference to what COWF-005 / Elk Meadow P2 did (required it, or lacked the
# equivalent). An item with no anchor is an ungrounded requirement → BLOCK.
#
# It does NOT touch Max's shared "Outstanding Documents Checklist" tracker
# (different structure, not a screener output).
#
# Accepted anchors (case-insensitive): "COWF-005", "Elk Meadow", "ISS-38/39/40",
# or the literal token "PRECEDENT:" (lets a genuinely novel must-have ship only
# once its precedent basis is written down explicitly).
#
# Exit codes: 0 = pass, 2 = block (stderr feeds back to Claude).

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

[ -z "$transcript_path" ] || [ ! -f "$transcript_path" ] && exit 0

python3 - "$transcript_path" <<'PYEOF'
import json, os, sys, re, time, glob

transcript_path = sys.argv[1]
session_dir = os.path.dirname(transcript_path)

# ── circuit breaker: shared across every hook, see ~/.claude/hooks/lib/circuit_breaker.py
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
brk = Breaker(state_file=os.path.join(session_dir, 'precedent_block_count'),
              label='PRECEDENT GROUNDING', max_strikes=3, turn_key=_turn, transcript_path=transcript_path)
def _bc():
    return brk.count
def _set_bc(n):
    brk._write(n)
if brk.tripped():
    print("Manually confirm every MUST-HAVE traces to COWF-005 before use.", file=sys.stderr)
    sys.exit(0)

# ── session start time, to only judge files touched THIS session ──────────────
session_start = None
try:
    with open(transcript_path) as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            ts = e.get('timestamp')
            if ts:
                try:
                    session_start = time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S"))
                    break
                except Exception:
                    pass
except Exception:
    pass
if session_start is None:
    session_start = time.time() - 6*3600  # fallback: last 6h

ANCHOR = re.compile(r'cowf-?005|elk\s*meadow|iss-?3[89]|iss-?40|precedent:', re.I)

# ── authorship gate: a recent mtime alone is not proof THIS session wrote it ──
# This file's own docstring says "screener output written this session", but
# the check below only ever verified a TIME WINDOW against the whole shared
# Drive folder -- any file matching the glob, touched by ANY process (another
# concurrent Claude Code session running the same biomass-screener skill on a
# different project, a sync, a manual edit) within that window looked
# identical to one this session actually wrote. That let an unrelated
# session's "Genesee South" screener block every response in a completely
# different conversation, repeatedly, with no connection to what was
# actually said here. Same failure class no_deferral_guard.sh already
# guards against (a stale/foreign file bumped by something else) -- missing
# here. Found 2026-09-02 on a real case. Now requires this session's own
# transcript to reference the file's basename via a write-class tool call
# (Write/Edit/MultiEdit/NotebookEdit, an Office MCP writer, or a Bash
# command) before it counts as a target at all.
# Write-detection (tool names + the "did this Bash call actually write"
# check) lives in one shared place now -- see lib/write_detection.py for why:
# four copies of this same logic already drifted apart once (2026-09-10).
try:
    from write_detection import WRITE_TOOL_NAMES, PUBLISH_TOOL_NAMES, is_real_write
except Exception:
    WRITE_TOOL_NAMES, PUBLISH_TOOL_NAMES = set(), set()
    def is_real_write(_): return False
authored_blob_parts = []
builder_blob_parts = []
try:
    with open(transcript_path) as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            msg = e.get('message', {})
            if not isinstance(msg, dict):
                continue
            for item in (msg.get('content') or []):
                if not isinstance(item, dict) or item.get('type') != 'tool_use':
                    continue
                name = item.get('name', '')
                # ensure_ascii=False (2026-10-27 audit): the screener's file names
                # carry an em dash ("Genesee South — BFA v1.3 Gap Checklist.xlsx");
                # escaped to \u2014 here, no such name could ever match below.
                inp_blob = json.dumps(item.get('input', ''), ensure_ascii=False)[:5000]
                if name in WRITE_TOOL_NAMES or name in PUBLISH_TOOL_NAMES:
                    authored_blob_parts.append(name + ' ' + inp_blob)
                elif name == 'Bash' and is_real_write(inp_blob):
                    authored_blob_parts.append(name + ' ' + inp_blob)
                if name == 'Bash' and 'build_deliverables.py' in inp_blob:
                    # The skill's one builder writes both files into the folder it
                    # is given; its command names that folder, not the files
                    # (2026-10-27 audit: so the files the skill requires were
                    # never counted as this session's).
                    builder_blob_parts.append(inp_blob)
except Exception:
    pass
authored_blob = '\n'.join(authored_blob_parts).lower()
builder_blob = '\n'.join(builder_blob_parts).lower()

def session_authored(path):
    if os.path.basename(path).lower() in authored_blob:
        return True
    folder = os.path.basename(os.path.dirname(path)).lower()
    return bool(folder) and folder in builder_blob

# ── find screener outputs under the biomass Prospective tree ──────────────────
# 2026-10-27 audit: the Prospective folder moved to Biomass/Current/CO/Prospective
# (after 9/09) while this still named Biomass/Prospective, so the check found no
# file and could not block at all. Search the whole Biomass tree (~120 files).
roots = [
    os.path.expanduser("~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/Feedstocks/Biomass"),
]
# Replay test set (~/.claude/hooks/tests/replay/run.py): the case's fixture
# files stand in for the Drive folder.
if os.environ.get('CLAUDE_HOOK_REPLAY') == '1' and os.environ.get('CLAUDE_HOOK_FIXTURES'):
    roots = [os.environ['CLAUDE_HOOK_FIXTURES']]
targets = []
for root in roots:
    if not os.path.isdir(root):
        continue
    for pat in ("**/*BFA v1.3 Pre-Screen.docx", "**/*Gap_Checklist*.xlsx", "**/*Gap Checklist*.xlsx"):
        for p in glob.glob(os.path.join(root, pat), recursive=True):
            bn = os.path.basename(p)
            if bn.startswith("~$"):
                continue  # Word/Excel lock file
            if "Outstanding Documents Checklist" in bn:
                continue  # Max's shared tracker, not a screener output
            if not session_authored(p):
                continue  # not referenced by this session's own tool calls
            try:
                if os.path.getmtime(p) >= session_start - 5:
                    targets.append(p)
            except Exception:
                pass
targets = sorted(set(targets))
if not targets:
    sys.exit(0)

violations = []  # (file, item_label, snippet)

def check_items(fname, items):
    for label, text in items:
        t = (text or "").strip()
        if len(t) < 3:
            continue
        if not ANCHOR.search(t):
            snip = re.sub(r'\s+', ' ', t)[:140]
            violations.append((os.path.basename(fname), label, snip))

# ── DOCX pre-screens ──────────────────────────────────────────────────────────
def scan_docx(path):
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except Exception as ex:
        # cannot parse -> do not silently pass; surface as a soft note, not a block
        print(f"[precedent-guard] WARN: python-docx unavailable, skipped {os.path.basename(path)}: {ex}", file=sys.stderr)
        return
    doc = Document(path)
    body = doc.element.body
    in_region = False
    items = []            # (label, text)
    cur_label = None
    cur_buf = []
    def flush():
        nonlocal cur_label, cur_buf
        if cur_label is not None:
            items.append((cur_label, " ".join(cur_buf)))
        cur_label, cur_buf = None, []
    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            para = Paragraph(child, doc)
            txt = para.text.strip()
            low = txt.lower()
            # region start / end
            if re.search(r'\bmust-?have\b', low) and 'evidence' not in low and len(txt) < 80:
                in_region = True
                flush()
                continue
            if in_region and (low.startswith('should-have') or low.startswith('should-have') or
                              'evidence coverage' in low or low.startswith('2 — evidence') or
                              low.startswith('closed') or low.startswith('note') and cur_label is None):
                # 'should-have' or evidence section ends the must-have region
                if low.startswith('should-have') or 'evidence coverage' in low or low.startswith('2 — evidence'):
                    flush(); in_region = False; continue
            if in_region:
                style = (para.style.name or "")
                if style.startswith('List Number'):
                    flush(); cur_label = txt; cur_buf = [txt]
                else:
                    if cur_label is not None:
                        cur_buf.append(txt)
        elif tag == 'tbl':
            if in_region:
                tbl = Table(child, doc)
                rows = list(tbl.rows)
                for r in rows[1:]:  # skip header
                    cells = [c.text for c in r.cells]
                    rowtext = " | ".join(cells)
                    # label = the "Document" cell (usually col 1)
                    lbl = cells[1] if len(cells) > 1 and cells[1].strip() else rowtext[:40]
                    items.append((lbl, rowtext))
    flush()
    check_items(path, items)

# ── XLSX gap checklists ───────────────────────────────────────────────────────
def scan_xlsx(path):
    try:
        import openpyxl
    except Exception as ex:
        print(f"[precedent-guard] WARN: openpyxl unavailable, skipped {os.path.basename(path)}: {ex}", file=sys.stderr)
        return
    wb = openpyxl.load_workbook(path, data_only=True)
    items = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            if not row:
                continue
            first = str(row[0]).strip().upper() if row[0] is not None else ""
            if first in ("MUST-HAVE", "MUST HAVE"):
                rowtext = " | ".join("" if c is None else str(c) for c in row)
                # label = the item column (col C / index 2 if present)
                lbl = ""
                if len(row) > 2 and row[2]:
                    lbl = str(row[2])[:40]
                items.append((lbl or rowtext[:40], rowtext))
    check_items(path, items)

for p in targets:
    try:
        if p.lower().endswith('.docx'):
            scan_docx(p)
        elif p.lower().endswith('.xlsx'):
            scan_xlsx(p)
    except Exception as ex:
        print(f"[precedent-guard] WARN: could not scan {os.path.basename(p)}: {ex}", file=sys.stderr)

if violations:
    if not brk.claim_or_release():
        sys.exit(0)  # shared per-turn block budget already spent -- stand down
    print("─"*72, file=sys.stderr)
    print("PRECEDENT GROUNDING — response blocked", file=sys.stderr)
    print("─"*72, file=sys.stderr)
    print("These MUST-HAVE items assert a requirement with NO tie to the validated", file=sys.stderr)
    print("precedent (Elk Meadow P2 / COWF-005). Every must-have must say what the", file=sys.stderr)
    print("precedent actually did — required it, or lacked the equivalent. If it is a", file=sys.stderr)
    print("genuinely novel requirement, read COWF-005, then state the basis with a", file=sys.stderr)
    print("'PRECEDENT:' note. Ungrounded must-haves are how the EIN / letterhead", file=sys.stderr)
    print("over-calls shipped.", file=sys.stderr)
    print("", file=sys.stderr)
    for fn, lbl, snip in violations:
        print(f"  • [{fn}] {lbl}", file=sys.stderr)
        print(f"      {snip}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Fix: for each item, either ground it against COWF-005 or drop it, and", file=sys.stderr)
    print("rebuild the deliverable.", file=sys.stderr)
    try:
        from guard_footer import print_footer
        print_footer()   # the ONE shared re-send instruction (lib/guard_footer.py)
    except Exception:
        pass
    print("─"*72, file=sys.stderr)
    sys.exit(2)

sys.exit(0)
PYEOF
