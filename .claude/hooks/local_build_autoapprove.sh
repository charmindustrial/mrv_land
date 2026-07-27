#!/usr/bin/env bash
# local_build_autoapprove.sh  —  PreToolUse hook on Bash
#
# Purpose: stop prompting Max while building documents he explicitly asked for,
# WITHOUT granting any ability to reach outside this machine or run arbitrary code.
#
# It emits a "permissionDecision: allow" ONLY for two narrow, provably-local cases:
#   1. Python whose code is INLINE in the command (heredoc `<<` or `-c`) so the code
#      can be scanned, AND that code contains no network / shell-escape / external-send
#      patterns. (File-path python runs are NOT auto-approved — their content can't be
#      seen here, so they still prompt.)
#   2. AppleScript (osascript) that only controls Microsoft Excel or Word (close/save),
#      and references nothing else (no Mail, Messages, Slack, browsers, System Events
#      keystrokes, or shell-out).
#
# Everything else — curl/wget, network-touching python, subprocess/shell escapes,
# osascript to Mail/Messages/Slack/browsers, and ALL MCP external sends (Slack, Gmail,
# Drive create_file) — gets NO decision here and falls through to the normal permission
# prompt. External-facing actions keep asking, by design.
#
# A "deny" from any other hook still wins over this "allow". This hook never denies.

input=$(cat)

tool=$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)
[ "$tool" = "Bash" ] || exit 0

cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)
[ -n "$cmd" ] || exit 0

approve() {
  reason=$(printf '%s' "$1" | jq -R -s '.')
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":%s}}\n' "$reason"
  exit 0
}

# Anything that can reach off-machine or run arbitrary shell. If present -> do NOT approve.
# (bare "http" is deliberately excluded so URLs inside document text don't trip the gate.)
EXTERNAL_RE='socket|urllib|requests|httplib|http\.client|httpx|smtplib|ftplib|poplib|imaplib|telnetlib|urlopen|webbrowser|xmlrpc|paramiko|boto3|googleapiclient|slack_sdk|sendmail|subprocess|os\.system|os\.popen|os\.exec|os\.fork|\bpty\b|\bsocketserver\b|\beval\(|\bexec\(|\bcompile\(|\b__import__\(|\bcurl\b|\bwget\b|\bssh\b|\bscp\b|\bsftp\b|\btelnet\b|\bnc \b'

# ---- Case 1: inline python (heredoc or -c) ----
if printf '%s' "$cmd" | grep -qE '(^|[;&|[:space:]])(/usr/bin/)?python3?([[:space:]].*)?(<<|[[:space:]]-c([[:space:]]|["'"'"']))'; then
  if printf '%s' "$cmd" | grep -qiE "$EXTERNAL_RE"; then
    exit 0   # has external / shell reach -> normal prompt
  fi
  approve "Local document build (inline python, no network or shell-escape detected) — auto-approved."
fi

# ---- Case 2: osascript controlling only Excel/Word ----
if printf '%s' "$cmd" | grep -qE '(^|[;&|[:space:]])osascript([[:space:]]|$|<<)'; then
  if printf '%s' "$cmd" | grep -qiE 'Microsoft (Excel|Word)' \
     && ! printf '%s' "$cmd" | grep -qiE 'do shell script|System Events|keystroke|key code|\bMail\b|Messages|Slack|Safari|Google Chrome|\bChrome\b|Notification|tell application "Finder"'; then
    approve "Local Excel/Word control (close/save) — auto-approved."
  fi
  exit 0   # any other osascript -> normal prompt
fi

exit 0
