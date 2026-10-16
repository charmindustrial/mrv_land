#!/usr/bin/env bash
# primary_source_guard.sh
# PreToolUse hook. Matcher (see settings.json):
#   WebFetch|WebSearch|Agent|mcp__chrome-control__open_url|mcp__chrome-control__get_page_content|mcp__chrome-control__execute_javascript
#   (Agent is still matched but now ALLOWED -- see the Agent branch below, 2026-09-14.)
#
# WHY THIS EXISTS (2026-06-25):
# Max gave a link to an Isometric module and an EPD and asked Claude to READ them.
# Claude ran WebFetch (which returns a SMALL MODEL'S SUMMARY, not the page text),
# mixed in memory of internal workspace files, and wrote two turns of confident
# analysis without ever opening the source. When called out, Claude built a hook
# for WebFetch ALONE -- then the same laundering is available through WebSearch,
# chrome-control, or a subagent. This hook closes the WHOLE class, not one tool.
#
# THE INVARIANT: you may not pull a derived/summarized representation of a
# discrete primary source you were asked to read. Open it directly:
#   - Certify removal data  -> skills/qa/container/tools/certify_read.py (Certify API)
#   - Isometric protocols / docs -> Isometric MCP protocols_get_content / isometric_docs_get
#   - any other web page    -> curl -sL <url> -o <file>, then Read the saved file
#   - Google Drive file     -> Drive connector read_file_content/download (text docs)
#                             or download + Read the image (scans/receipts/tickets)
#   - document file (pdf/doc/xls/ppt/csv) -> download bytes + Read
#
# WHAT THIS HOOK DOES NOT COVER (stated openly, not by omission):
#   1. Reciting a source from memory with no tool call -- nothing to intercept;
#      backstopped by citation_integrity_stop.sh requiring verbatim quotes.
#   2. read_file_content on an image/scanned PDF (OCR laundering) -- a hook sees
#      only a file ID, not mime type; backstopped by the behavioral OCR rule.
#
# Exit 2 => block + surface reason to the model. Exit 0 => allow.

set -euo pipefail

input="$(cat)"

tool="$(printf '%s' "$input" | python3 -c '
import sys, json
try: print(json.load(sys.stdin).get("tool_name",""))
except Exception: print("")
' 2>/dev/null || true)"

[ -z "$tool" ] && exit 0

# Shared denylist logic: returns "BLOCK <reason-key>" or "OK" for a given URL.
classify_url() {
  printf '%s' "$1" | python3 -c '
import sys, re
from urllib.parse import urlparse
url = sys.stdin.read().strip()
if not url:
    print("OK"); raise SystemExit
host = (urlparse(url).hostname or "").lower()
path = (urlparse(url).path or "").lower()
PRIMARY = (
    "registry.isometric.com", "certify.isometric.com",
    "drive.google.com", "docs.google.com", "sheets.google.com",
    "greet.es.anl.gov", "greet.anl.gov",
)
host_hit = host in PRIMARY or host.endswith(".isometric.com") or host.endswith(".googleusercontent.com")
doc_hit = bool(re.search(r"\.(pdf|docx?|xlsx?|pptx?|csv|odt|ods)(\?|#|$)", path))
print("BLOCK" if (host_hit or doc_hit) else "OK")
' 2>/dev/null || echo "OK"
}

get_field() {
  printf '%s' "$input" | python3 -c "
import sys, json
try:
    ti = json.load(sys.stdin).get('tool_input') or {}
    print(ti.get('$1','') or '')
except Exception:
    print('')
" 2>/dev/null || true
}

case "$tool" in
  WebFetch|mcp__chrome-control__open_url|mcp__chrome-control__get_page_content|mcp__chrome-control__execute_javascript)
    url="$(get_field url)"
    [ -z "$url" ] && exit 0
    if [ "$(classify_url "$url")" = "BLOCK" ]; then
      echo "BLOCKED ($tool): this returns a SUMMARY/derived view, not the source. The target is a primary source you were asked to read. Open it directly: Certify data with skills/qa/container/tools/certify_read.py, Isometric protocols with the Isometric MCP (protocols_get_content / isometric_docs_get), Drive files with skills/qa/container/tools/drive_read.py get (or the Drive connector) then Read, any other page with curl -sL <url> -o <file> then Read the saved file in chunks and QUOTE verbatim. Do not analyze a document you have not opened." >&2
      exit 2
    fi
    exit 0
    ;;
  # Agent: allowed as of 2026-09-14 (Max). Helper sessions inherit this same hook set,
  # so the primary-source rule is enforced on the helper's own tool calls (WebFetch,
  # chrome-control) rather than by blocking the spawn. Helpers must write verbatim-
  # quoted source text to files, not return summaries.
  Agent)
    exit 0
    ;;
  WebSearch)
    # Not blocked: discovery is legitimate. Disclosed in the audit -- WebSearch
    # returns snippets, never source text, and citation_integrity_stop.sh blocks
    # any claim that cites a snippet as a verbatim source read.
    exit 0
    ;;
esac

exit 0
