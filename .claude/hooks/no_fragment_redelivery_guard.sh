#!/usr/bin/env bash
# no_fragment_redelivery_guard.sh -- thin wrapper, all logic in the .py file.
# See no_fragment_redelivery_guard.py for what this checks and why.

set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

if [ -z "$transcript_path" ]; then
  exit 0
fi

python3 "$HOOK_DIR/no_fragment_redelivery_guard.py" "$transcript_path"
exit $?
