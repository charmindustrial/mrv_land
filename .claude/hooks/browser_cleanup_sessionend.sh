#!/bin/bash
# browser_cleanup_sessionend.sh
#
# SessionEnd hook for the MRV Expert workspace. Closes the Playwright browser
# windows THIS session opened, so they don't pile up across sessions (the "why do
# I have 4 Chromes open" problem).
#
# PRECISION: it does NOT blanket-kill every Playwright window. It scans this
# session's own transcript for which Playwright MCP servers were actually used,
# maps each to its profile directory, and closes only those. A window opened by a
# different, still-running session (which uses a different profile) is never touched.
#
# Server -> profile mapping (profile = "playwright-profile" + servername minus the
# leading "playwright"):
#   playwright        -> playwright-profile
#   playwright-mrv    -> playwright-profile-mrv
#   playwright-mrv-2  -> playwright-profile-mrv-2   (and -3, -4)
#
# FAIL-OPEN: any error, missing tool, or unparseable input exits 0 without acting.
# This hook can only ever close a leftover window; it can never brick a session.

input="$(cat 2>/dev/null || true)"
command -v jq >/dev/null 2>&1 || exit 0

transcript="$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")"
[ -f "$transcript" ] || exit 0

# Distinct Playwright MCP server names used in this session's tool_use calls.
servers="$(jq -rs '.[]? | (.message.content[]? // empty) | select(.type=="tool_use") | .name' "$transcript" 2>/dev/null \
  | grep -oE 'mcp__playwright[a-z0-9-]*__' \
  | sed -E 's/^mcp__//; s/__$//' \
  | sort -u || true)"
[ -z "$servers" ] && exit 0

profile_base="/Users/maxlavine/.claude"

while IFS= read -r server; do
  [ -z "$server" ] && continue
  # Strip the leading "playwright" to build the profile suffix.
  suffix="${server#playwright}"
  profile="playwright-profile${suffix}"
  # Close only the window bound to this exact profile dir. Exact match on the
  # user-data-dir path so playwright-profile-mrv-2 never matches playwright-profile.
  pkill -f "user-data-dir=${profile_base}/${profile}$" 2>/dev/null || true
  pkill -f "user-data-dir=${profile_base}/${profile} " 2>/dev/null || true
done <<< "$servers"

exit 0
