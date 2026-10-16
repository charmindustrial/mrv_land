#!/bin/bash
# doc_extraction_guard.sh
#
# PreToolUse hook — MRV Expert workspace.
# Blocks Bash commands that extract text from document files using
# pdftotext, grep, sed, awk, or cat on PDFs and text extractions.
#
# The citation integrity hook requires documents to be opened via
# Read, Google Drive, the Certify/Drive API tools, or Word. Bash extraction bypasses
# that chain and produces unverifiable citations.
#
# Exit 2 = deny with reason surfaced to Claude.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"

input="$(cat)"

tool_name="$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null || echo "")"
[ "$tool_name" = "Bash" ] || exit 0

# Scope: only act when cwd is inside the workspace
cwd="$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null || echo "")"
case "$cwd" in
  "$WORKSPACE"|"$WORKSPACE"/*) : ;;
  *) exit 0 ;;
esac

command="$(echo "$input" | jq -r '.tool_input.command // empty' 2>/dev/null || echo "")"

# Block pdftotext on any file
if echo "$command" | grep -qE 'pdftotext'; then
  echo "DENIED by doc_extraction_guard: pdftotext is blocked. Open PDFs using the Read tool (for local files; download web or Certify PDFs first with curl or certify_read.py source), or Google Drive (drive_read.py get, or the Drive MCP). Bash text extraction produces citations the citation integrity hook cannot verify." >&2
  exit 2
fi

# Block grep/sed/awk/cat targeting .pdf or known text extraction files
if echo "$command" | grep -qE '(grep|sed|awk|cat)\s.*\.(pdf|PDF)'; then
  echo "DENIED by doc_extraction_guard: grep/sed/awk/cat on PDF files is blocked. Open PDFs using the Read tool, or Google Drive (drive_read.py get, or the Drive MCP)." >&2
  exit 2
fi

# Block grep/sed/awk/cat targeting the .playwright-mcp text extraction files
if echo "$command" | grep -qE '(grep|sed|awk|cat)\s.*playwright-mcp/.*-text\.txt'; then
  echo "DENIED by doc_extraction_guard: Bash extraction from playwright-mcp text files is blocked. These are unverified extractions. Open the source PDF using the Read tool, or Google Drive MCP instead." >&2
  exit 2
fi

# Block python-based PDF text extraction (pypdf / PyPDF2 / pdfplumber / PyMuPDF).
# These bypass the Read tool, fail SILENTLY on pages that don't extract cleanly,
# and have produced false "not in the document" conclusions. PDFs must be read
# with the Read tool, which renders the actual page (reliable and visible).
if echo "$command" | grep -qiE '(pypdf|pdfreader|\.extract_text|pdfplumber|pymupdf|import fitz|fitz\.open)'; then
  echo "DENIED by doc_extraction_guard: python PDF text-extraction (pypdf/pdfplumber/PyMuPDF/etc.) is blocked — it fails silently on some pages and has produced false 'not in the document' calls. Read the PDF with the Read tool (pages=N-M); it renders the actual page. Then cite the page number + a verbatim line from what you read." >&2
  exit 2
fi

# Block ad-hoc grep/sed/awk/cat on Word/Google docs (unreliable text munging).
# python-docx is NOT blocked: it reads .docx structured XML reliably (no silent
# OCR-style failure like PDFs), so it's the sanctioned reader for local .docx.
# Native Google Docs (.gdoc/.gsheet) that aren't downloaded: use the Drive MCP.
if echo "$command" | grep -qiE '(grep|sed|awk|cat)\s.*\.(docx|doc|gdoc|gsheet)([^a-z]|$)'; then
  echo "DENIED by doc_extraction_guard: grep/sed/awk/cat on Word/Google docs is blocked. Read local .docx with python-docx (reliable structured text) or the Read tool; use the Google Drive MCP for native Google Docs." >&2
  exit 2
fi

exit 0
