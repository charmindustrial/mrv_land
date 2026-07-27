#!/bin/bash
# Auto-sync MRV Expert workspace → charmindustrial/mrv_land:max-mrv-skills
# Fires on Claude Code Stop event. Logs to ~/.claude/auto-sync.log.
# Always exits 0 — failures are logged, never propagated.

LOG="$HOME/.claude/auto-sync.log"
WORKSPACE="/Users/maxlavine/Desktop/Claude/Skills/MRV Expert"

cd "$WORKSPACE" 2>/dev/null || exit 0
[ -z "$(git status --porcelain 2>/dev/null)" ] && exit 0

count=$(git status --porcelain | wc -l | tr -d ' ')
files=$(git status --porcelain | awk '{$1=""; print substr($0,2)}' | head -5 | paste -sd ", " -)
suffix=""
[ "$count" -gt 5 ] && suffix=" (+$((count-5)) more)"

{
  echo ""
  echo "--- $(date) ---"
  git add -A 2>&1
  git commit -m "Auto-sync: ${count} file(s) — ${files}${suffix}" 2>&1
  git push origin max-mrv-skills 2>&1
} >> "$LOG" 2>&1

exit 0
