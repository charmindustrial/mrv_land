#!/usr/bin/env bash
# Blocks `open` calls with https://charmindustrial.slack.com URLs.
# Forces use of slack://channel?team=T9KJZKGR4&id=...&message=... instead.

TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

if echo "$TOOL_INPUT" | grep -q '"open ' && echo "$TOOL_INPUT" | grep -qE '"open [^"]*https://charmindustrial\.slack\.com'; then
  echo "BLOCKED: Use slack:// protocol to open Slack threads, not https://. Correct format: open \"slack://channel?team=T9KJZKGR4&id=CHANNEL_ID&message=MESSAGE_TS\"" >&2
  exit 2
fi

exit 0
