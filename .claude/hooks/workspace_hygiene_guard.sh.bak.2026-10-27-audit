#!/bin/bash
# workspace_hygiene_guard.sh
#
# PreToolUse hook for the MRV Expert workspace. Prevents loose binary captures
# and Certify scrapes from accumulating at the workspace root by denying:
#
#   1. Playwright `browser_take_screenshot` calls without an explicit filename
#      under `outputs/`.
#   2. `Write` tool calls that target the workspace root with .png / .jpg /
#      .jpeg / .yml / .yaml extensions.
#
# Workspace root is derived from this script's own location:
#     <workspace>/.claude/hooks/workspace_hygiene_guard.sh
# so the hook is portable across machines as long as the layout is preserved.
#
# Scoped: only acts when the tool's `cwd` is inside the workspace. No-op
# elsewhere — protects against the unlikely case where this script gets
# invoked from a different project context.
#
# Deny semantics: exit 2 with reason on stderr — surfaces to Claude so it can
# adapt and rewrite the call with the correct path.

set -euo pipefail

# Derive the workspace root from this script's location: ../../ from the script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"

input="$(cat)"

# Scope: only act when cwd is inside the workspace
cwd="$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null || echo "")"
case "$cwd" in
  "$WORKSPACE"|"$WORKSPACE"/*) : ;;
  *) exit 0 ;;
esac

tool_name="$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null || echo "")"

# Case 1: Playwright screenshot — require filename starting with outputs/
if [ "$tool_name" = "mcp__playwright__browser_take_screenshot" ]; then
  filename="$(echo "$input" | jq -r '.tool_input.filename // empty' 2>/dev/null || echo "")"
  if [ -z "$filename" ]; then
    echo "DENIED by workspace_hygiene_guard: browser_take_screenshot called without an explicit filename. In the MRV Expert workspace, screenshots must be saved under outputs/qa/batch-<batch_id>/screenshots/ (or outputs/qa/site-emissions-qa/screenshots/ for site emissions QA). Pass filename='outputs/qa/batch-<id>/screenshots/<descriptive_name>.png'." >&2
    exit 2
  fi
  # Reject paths that don't route into outputs/. Accept either "outputs/..." (relative) or absolute paths containing "/outputs/".
  case "$filename" in
    outputs/*|*/outputs/*) : ;;
    *)
      echo "DENIED by workspace_hygiene_guard: screenshot filename '$filename' does not route under outputs/. Save to outputs/qa/batch-<batch_id>/screenshots/<name>.png (or outputs/qa/site-emissions-qa/screenshots/<name>.png). The workspace root is not a valid screenshot destination." >&2
      exit 2
      ;;
  esac
fi

# Case 2: Write tool — deny .png/.jpg/.jpeg/.yml/.yaml at the workspace root
if [ "$tool_name" = "Write" ]; then
  file_path="$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")"
  if [ -n "$file_path" ]; then
    # Normalize: only act on absolute paths inside the workspace
    case "$file_path" in
      "$WORKSPACE"/*)
        rel="${file_path#$WORKSPACE/}"
        # If rel contains no "/", it's at the workspace root
        case "$rel" in
          */*) : ;;  # has a subfolder, ignore
          *)
            case "$rel" in
              *.png|*.jpg|*.jpeg|*.yml|*.yaml|*.PNG|*.JPG|*.JPEG|*.YML|*.YAML)
                echo "DENIED by workspace_hygiene_guard: Write to '$rel' at the workspace root is blocked. Binary captures and YAML scrapes belong under outputs/ (typically outputs/qa/batch-<batch_id>/screenshots/ for PNGs and outputs/qa/batch-<batch_id>/ for YAML). Move this write to the correct outputs/ subfolder." >&2
                exit 2
                ;;
              CLAUDE.md|README.txt|FOLDER_INDEX.md|.gitignore|.gitattributes|.mcp.json) : ;;
              *)
                # Added 2026-10-13: protocol scrapes and page-text dumps (.txt) kept
                # landing at the root because only images/YAML were blocked.
                echo "DENIED by workspace_hygiene_guard: Write to '$rel' at the workspace root is blocked. Only CLAUDE.md, README.txt, FOLDER_INDEX.md and the git/config files live at the root. Protocol or registry text scrapes go in knowledge-base/; research notes and page captures go in outputs/research/; scratch work goes in the session scratchpad. Write to the right folder instead." >&2
                exit 2
                ;;
            esac
            ;;
        esac
        ;;
    esac
  fi
fi

exit 0
