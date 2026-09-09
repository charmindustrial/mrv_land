#!/bin/bash
# delta_baseline_guard.sh
#
# Stop hook for the MRV Expert workspace. Fires only when the turn just wrote or
# modified a Charm compliance/planning deliverable under outputs/deliverables/ or
# outputs/mrv-operational-documents/ (.docx/.md, modified in the last ~3 min).
#
# When it fires it enforces two things and blocks (exit 2) with a reason if either fails:
#
#   1. BASELINE-READ GATE. The session must have actually opened the operator's
#      current-state docs before the deliverable was finalized:
#        - the PDD  (Charm_PDD_v1.12*)                 -- opened via ANY tool_use
#        - the KB   (Charm_Isometric_Knowledge_Base.md) -- opened via ANY tool_use
#      Detection looks only at tool_use INPUTS in the transcript (not prose, not
#      tool results), so a passing mention of a filename does not satisfy the gate.
#      The PDD is a .docx, so "opened" counts whether it was read via python-docx in
#      Bash, the word MCP, or the Read tool. This is the exact step that was skipped:
#      building from the protocols without reading current state first.
#
#   2. DEFERRAL BLOCK. The final assistant message and the deliverable text must not
#      contain reader-directed primary-source-reading deferrals ("sweep the PDD",
#      "confirm the module text", "re-read the ... module", "to be confirmed against",
#      "go read", bracketed "[... re-read ...]"). Those hand Max the reading that is mine.
#
# FAIL-OPEN: any error, missing tool, or unparseable input exits 0. This guard can
# only ever block; it can never brick legitimate work on a script bug.
#
# Workspace root is self-derived from this script's location (../../), like
# workspace_hygiene_guard.sh, so it is portable across machines.

input="$(cat 2>/dev/null || true)"
command -v jq >/dev/null 2>&1 || exit 0

# Avoid stop-hook re-entry loops.
active="$(printf '%s' "$input" | jq -r '.stop_hook_active // false' 2>/dev/null || echo false)"
[ "$active" = "true" ] && exit 0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
[ -z "$SCRIPT_DIR" ] && exit 0
WORKSPACE="$(cd "$SCRIPT_DIR/../.." 2>/dev/null && pwd || echo "")"
[ -z "$WORKSPACE" ] && exit 0

# Scope: only act when cwd is inside the workspace.
cwd="$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null || echo "")"
case "$cwd" in "$WORKSPACE"|"$WORKSPACE"/*) : ;; *) exit 0 ;; esac

transcript="$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")"
[ -f "$transcript" ] || exit 0

# Circuit breaker: shared across every hook, see ~/.claude/hooks/lib/circuit_breaker.sh
SESSION_DIR="$(dirname "$transcript")"
source ~/.claude/hooks/lib/circuit_breaker.sh
cb_init "$SESSION_DIR/delta_baseline_block_count" 3
if cb_tripped "DELTA-BASELINE GUARD"; then
  echo "Manually confirm the PDD and KB were actually read before this deliverable ships." >&2
  exit 0
fi

DELIV_DIRS=("$WORKSPACE/outputs/deliverables" "$WORKSPACE/outputs/mrv-operational-documents")

# Did this turn touch a compliance/planning deliverable? (modified in last 3 min)
recent="$(find "${DELIV_DIRS[@]}" -type f \( -iname '*.docx' -o -iname '*.md' \) -mmin -3 2>/dev/null \
  | grep -Ev '/(~\$|\.~|\.gitkeep)' || true)"
[ -z "$recent" ] && exit 0

# Enumerate tool_use INPUTS only (active accesses), one per line: "<name>\t<input json>"
tooluses="$(jq -rs '.[]? | (.message.content[]? // empty) | select(.type=="tool_use") | "\(.name)\t\(.input|tostring)"' "$transcript" 2>/dev/null || true)"

# AUTHORSHIP GATE. A fresh mtime in the deliverable dirs is not enough on its own -- a
# stale file whose timestamp was bumped by git, a sync, or another window looks identical
# to one this session actually wrote. Only proceed if one of THIS session's own
# WRITE-class tool_uses actually named a deliverable path. Read-only turns (browser
# cleanup, searches, ps/kill, Reads) never wrote a deliverable, so they never trip this.
# Write-class = Write/Edit/MultiEdit/NotebookEdit, the word MCP writers, or a Bash command
# (python-docx/openpyxl heredoc) whose input references a deliverable dir.
# Caveat: the transcript is session-wide, not turn-scoped, so a deliverable written
# earlier this session can still gate a later turn -- an over-fire in the safe direction
# (toward reading the baseline), never a false alarm on read-only work.
authored="$(printf '%s' "$tooluses" \
  | grep -E '^(Write|Edit|MultiEdit|NotebookEdit|Bash|mcp__word__[a-z_]+)	' \
  | grep -E 'outputs/(deliverables|mrv-operational-documents)' || true)"
[ -z "$authored" ] && exit 0

pdd_ok=false; kb_ok=false
printf '%s' "$tooluses" | grep -q 'Charm_PDD_v1\.12' && pdd_ok=true
printf '%s' "$tooluses" | grep -q 'Charm_Isometric_Knowledge_Base\.md' && kb_ok=true

if [ "$pdd_ok" != "true" ] || [ "$kb_ok" != "true" ]; then
  missing=""
  [ "$pdd_ok" != "true" ] && missing="$missing the PDD (Charm_PDD_v1.12*)"
  [ "$kb_ok" != "true" ] && missing="$missing the knowledge base (Charm_Isometric_Knowledge_Base.md)"
  cb_block "BLOCKED by delta_baseline_guard: a Charm deliverable was written this turn, but the session never opened:${missing}. Read the operator's CURRENT-STATE docs first, then rebuild the deliverable as a DELTA — what does Charm already do (KB + PDD) vs. what actually changes. Do not enumerate protocol requirements wholesale as if this were a greenfield project. Open the missing doc(s), diff, and re-deliver."
fi

# Deferral scan: last assistant text (chat text plus the body of any
# Slack/Gmail/canvas message-sending tool call in the same turn -- see
# lib/transcript_text.py) + deliverable text.
last_asst="$(python3 - "$transcript" 2>/dev/null <<'PYEOF' || true
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/hooks/lib"))
from transcript_text import last_assistant_text
entries = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            pass
print(last_assistant_text(entries))
PYEOF
)"

deliv_text=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in
    *.md)   deliv_text="$deliv_text $(cat "$f" 2>/dev/null || true)" ;;
    *.docx) deliv_text="$deliv_text $(unzip -p "$f" word/document.xml 2>/dev/null | sed 's/<[^>]*>/ /g' || true)" ;;
  esac
done <<< "$recent"

scan_target="$last_asst $deliv_text"
hit="$(printf '%s' "$scan_target" | grep -oiE 'sweep the pdd|confirm the module text|to be confirmed against|re-read the [a-z ]{0,30}module|read the [a-z ]{0,30}module (first|before|and confirm)|\[[^]]*re-read[^]]*\]|go read the' | head -1 || true)"

if [ -n "$hit" ]; then
  cb_block "BLOCKED by delta_baseline_guard: the deliverable or final message defers primary-source reading to the reader (matched: \"$hit\"). That reading is yours. Open the source, read it, and state the finding directly. Remove the deferral and re-deliver."
fi

cb_clear
exit 0
