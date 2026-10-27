#!/usr/bin/env bash
# Blocks `open` calls with https://charmindustrial.slack.com URLs.
# Forces use of slack://channel?team=T9KJZKGR4&id=...&message=... instead.

# Claude Code hands a check its call as JSON on standard input. This used to
# read a CLAUDE_TOOL_INPUT setting that is never provided, so it could not
# fire at all (found 2026-10-27).
CMD="$(jq -r '.tool_input.command // empty' 2>/dev/null || true)"

if printf '%s' "$CMD" | grep -qE '(^|[;&|[:space:]])open[[:space:]]+[^;&|]*https://charmindustrial\.slack\.com'; then
  echo "BLOCKED: Use slack:// protocol to open Slack threads, not https://. Correct format: open \"slack://channel?team=T9KJZKGR4&id=CHANNEL_ID&message=MESSAGE_TS\"" >&2
  exit 2
fi

exit 0
