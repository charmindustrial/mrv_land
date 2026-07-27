#!/usr/bin/env bash
# primary_source_guard.sh
# PreToolUse hook. Matcher (see settings.json):
#   WebFetch|WebSearch|Agent|mcp__chrome-control__open_url|mcp__chrome-control__get_page_content|mcp__chrome-control__execute_javascript
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
#   - web page / registry  -> Playwright: browser_navigate + browser_evaluate
#                             '() => document.body.innerText', then read the text
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
      echo "BLOCKED ($tool): this returns a SUMMARY/derived view, not the source. The target is a primary source you were asked to read. Open it directly with Playwright (browser_navigate + browser_evaluate '() => document.body.innerText', then read the saved text in chunks and QUOTE verbatim), or for Drive use the Drive connector. Do not analyze a document you have not opened." >&2
      exit 2
    fi
    exit 0
    ;;
  Agent)
    blob="$(printf '%s' "$input" | python3 -c '
import sys, json
try:
    ti = json.load(sys.stdin).get("tool_input") or {}
    print(((ti.get("prompt","") or "") + " " + (ti.get("description","") or "")))
except Exception:
    print("")
' 2>/dev/null || true)"
    # Deny only if the subagent is being pointed at a primary source to read/extract.
    if printf '%s' "$blob" | grep -Eiq '(registry|certify)\.isometric\.com|drive\.google\.com|docs\.google\.com|\.(pdf|docx?|xlsx?|pptx?|csv)([^a-z]|$)'; then
      echo "BLOCKED (Agent): primary-source reading/extraction stays in the main session (subagent extraction is parked). Open the source yourself with the first-party read path and quote verbatim; do not delegate the read to a subagent that returns a summary." >&2
      exit 2
    fi
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
