#!/usr/bin/env bash
# no_fragment_redelivery_guard.sh -- thin wrapper, all logic in the .py file.
# See no_fragment_redelivery_guard.py for what this checks and why.

set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

input="$(cat)"
transcript_path="$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null || true)"

if [ -z "$transcript_path" ]; then
  exit 0
fi

python3 "$HOOK_DIR/no_fragment_redelivery_guard.py" "$transcript_path"
exit $?
