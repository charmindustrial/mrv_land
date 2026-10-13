#!/usr/bin/env bash
# research_citation_guard.sh
#
# PostToolUse hook for the research skill. After any Write operation that
# produces a research output (detected by file path under outputs/research/,
# OR content containing a "## Source List" / "### Source List" marker),
# scans the written content for citation-signal phrases that are not followed
# by a verbatim quoted string within ~250 characters.
#
# Exit 0  → pass (no violations or not a research output)
# Exit 2  → citation violation found; surfaces warning to Claude so it can fix
#
# This hook is a secondary seatbelt. The primary enforcement is the workflow
# in skills/research/SKILL.md (Steps 1–5). The hook catches egregious cases
# where a section/clause reference appears with no accompanying quote at all.
# It cannot catch nuanced paraphrase-as-citation; only workflow can do that.
#
# Registered as a PostToolUse hook in .claude/settings.json with matcher "Write".

set -euo pipefail

input="$(cat)"

tool_name="$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null || true)"
if [ "$tool_name" != "Write" ]; then exit 0; fi

file_path="$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
content="$(echo "$input" | jq -r '.tool_input.content // empty' 2>/dev/null || true)"

if [ -z "$content" ] || [ -z "$file_path" ]; then exit 0; fi

# Only scan text-based files; skip binaries
case "$file_path" in
  *.py|*.sh|*.xlsx|*.docx|*.pdf|*.png|*.jpg|*.jpeg|*.zip|*.skill) exit 0 ;;
esac

# Scope check: only act on research outputs.
# Triggers if: file is under outputs/research/, OR content has a Source List header.
is_research=0
case "$file_path" in
  */outputs/research/*|*/research/*) is_research=1 ;;
esac
if echo "$content" | grep -qE '^#{1,3} Source List$'; then
  is_research=1
fi
if [ "$is_research" -eq 0 ]; then exit 0; fi

# Write content to a temp file so Python can read it cleanly
TMPFILE="$(mktemp /tmp/citation_guard_XXXXXX.txt)"
echo "$content" > "$TMPFILE"
trap 'rm -f "$TMPFILE"' EXIT

# Run citation check via Python3
RESULT="$(python3 - "$file_path" "$TMPFILE" 2>&1 <<'PYEOF'
import sys, re

file_path = sys.argv[1]
content_file = sys.argv[2]
with open(content_file, 'r') as f:
    content = f.read()

# Citation-signal patterns: references to a section/clause/table number, OR
# phrases that assert what a document says (states/requires/specifies/etc.)
# followed by "that" or a noun phrase — not followed by a quote.
signal_re = re.compile(
    r'(?:'
    r'§\s*\d[\d.]*[a-z]?'                          # §3.2 or §3.2a
    r'|[Ss]ection\s+\d[\d.]*'                       # Section 3.2
    r'|[Cc]lause\s+\d[\d.]*'                        # Clause 4.1
    r'|[Aa]rticle\s+\d[\d.]*'                       # Article 2.3
    r'|[Tt]able\s+[A-Z]?\d+'                        # Table 5, Table A1
    r'|(?:[Ss]tates?|[Rr]equires?|[Ss]pecifies?'
    r'|[Pp]rovides?|[Mm]andates?|[Ss]tipulates?)'
    r'\s+(?:that\s+)?[^"\x27“”\n]'          # "states that X" without immediate quote
    r')',
    re.MULTILINE
)

# A valid citation has a quoted string nearby (within 250 chars forward from match)
quote_chars = {'"', "'", chr(96), '“', '”', '‘', '’'}
blockquote_re = re.compile(r'^\s*>', re.MULTILINE)

violations = []
for match in signal_re.finditer(content):
    start = match.start()
    window = content[start : start + 250]

    has_direct_quote = any(c in window for c in quote_chars)
    # Also check if a blockquote (> ...) starts on this line or the next
    line_start = content.rfind('\n', 0, start) + 1
    nearby_block = content[line_start : start + 400]
    has_blockquote = bool(blockquote_re.search(nearby_block))

    if not has_direct_quote and not has_blockquote:
        line_end = content.find('\n', start)
        if line_end == -1:
            line_end = len(content)
        line = content[line_start : line_end].strip()
        if len(line) > 110:
            line = line[:110] + '...'
        violations.append(f'  "{match.group(0).strip()}" — line: {line}')

if violations:
    cap = min(5, len(violations))
    print(f"CITATION GUARD: {len(violations)} citation-signal phrase(s) in '{file_path}' "
          f"not followed by a verbatim quote:")
    for v in violations[:cap]:
        print(v)
    if len(violations) > cap:
        print(f"  ... and {len(violations) - cap} more")
    sys.exit(1)

sys.exit(0)
PYEOF
)" && PYEXIT=0 || PYEXIT=$?

if [ "$PYEXIT" -ne 0 ]; then
    echo "research_citation_guard: Citation integrity warning" >&2
    echo "$RESULT" >&2
    echo "" >&2
    echo "Every §/Section/Clause/Table reference and 'states/requires/specifies' phrase" >&2
    echo "in a research output must be followed by a verbatim quoted string." >&2
    echo "Fix: add the exact text from the source in double quotes near each signal phrase," >&2
    echo "or move the paraphrase to follow a blockquote (> \"...\")." >&2
    exit 2
fi

exit 0
