#!/bin/bash
# doc_extraction_guard.sh
#
# PreToolUse hook — MRV Expert workspace.
# Blocks Bash commands that extract text from document files using
# pdftotext, grep, sed, awk, or cat on PDFs and text extractions.
#
# The citation integrity hook requires documents to be opened via
# Read, Google Drive, Playwright, or Word. Bash extraction bypasses
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

# Second look (2026-10-27 audit). The line tests below fire on any line where
# grep/sed/awk/cat comes before ".pdf"/".docx" -- e.g. `ls *.pdf | grep 2024`,
# `pdfinfo a.pdf | grep Pages`, "sed" inside "--compressed" -- and on any
# mention of pdftotext or pypdf, e.g. `which pdftotext` or a page count. 69 of
# 155 refusals from 9/15 to 10/27 were of that kind. When a line test fires, this
# checks whether a document's text is really being pulled out: grep/sed/awk/cat
# with a document as a file it reads, pdftotext actually run, or a PDF library
# call that pulls text. It prints ALLOW only when plainly not; on any error the
# block stands. Page counts and rendering pages to images are allowed.
IFS= read -r -d '' CONFIRM_PY <<'PYEOF' || true
import sys, re, os, shlex

# Second look after the line test fired: is a document's text really being pulled
# out? Prints ALLOW only when it plainly is not; anything unclear stays BLOCK.

DOC = {'pdf': r'\.pdf\b', 'docx': r'\.(docx|doc|gdoc|gsheet)\b'}
TEXTCMD = {'grep', 'egrep', 'fgrep', 'zgrep', 'sed', 'gsed', 'awk', 'gawk', 'cat'}
PREFIX = {'sudo', 'command', 'time', 'nice', 'nohup', 'env', 'exec', 'do', 'then', 'else',
          'elif', 'if', 'while', 'until', '!', '{'}
SEPS = {';', ';;', '&', '&&', '|', '||', '(', ')', '|&'}


def split_heredocs(cmd):
    lines = cmd.replace('\\\n', ' ').split('\n')
    shell, bodies, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        shell.append(line)
        i += 1
        for _, tag in re.findall(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line):
            body = []
            while i < len(lines) and lines[i].strip() != tag:
                body.append(lines[i])
                i += 1
            i += 1
            bodies.append('\n'.join(body))
    return '\n'.join(shell), bodies


def inner_subs(tok):
    out = []
    for m in re.finditer(r'\$\(', tok):
        depth, j = 1, m.end()
        while j < len(tok) and depth:
            depth += {'(': 1, ')': -1}.get(tok[j], 0)
            j += 1
        out.append(tok[m.end():j - 1])
    out += re.findall(r'`([^`]*)`', tok)
    return out


def tokens(shell):
    lx = shlex.shlex(shell.replace('\n', ' ; '), posix=True, punctuation_chars=';&|()<>')
    lx.whitespace_split = True
    lx.commenters = ''
    return list(lx)


def pipelines(shell, depth=0):
    """List of pipelines; each pipeline is a list of simple commands (token lists)."""
    toks = tokens(shell)
    pls, cur, cmd = [], [], []
    for t in toks:
        if t in SEPS:
            if cmd:
                cur.append(cmd)
            cmd = []
            if t not in ('|', '|&'):
                if cur:
                    pls.append(cur)
                cur = []
        else:
            cmd.append(t)
            if depth < 4 and ('$(' in t or '`' in t):
                for s in inner_subs(t):
                    pls += pipelines(s, depth + 1)
    if cmd:
        cur.append(cmd)
    if cur:
        pls.append(cur)
    # bash -c / sh -c strings are shell too
    for pl in list(pls):
        for c in pl:
            for k, t in enumerate(c[:-1]):
                if os.path.basename(t) in ('bash', 'sh', 'zsh') and c[k + 1] == '-c' and k + 2 < len(c) and depth < 4:
                    pls += pipelines(c[k + 2], depth + 1)
    return pls


def head(c):
    """(command name, operand tokens, input-redirect files)"""
    i = 0
    while i < len(c) and (c[i] in PREFIX or re.match(r'^\w+=', c[i])):
        i += 1
    if i < len(c) and c[i] == 'timeout':
        i += 2
    if i >= len(c):
        return None, [], []
    name = os.path.basename(c[i])
    rest, redir, j = [], [], i + 1
    while j < len(c):
        t = c[j]
        if t in ('<', '>', '>>', '>&', '<<', '<<<'):
            if t == '<' and j + 1 < len(c):
                redir.append(c[j + 1])
            j += 2
            continue
        if re.fullmatch(r'\d', t) and j + 1 < len(c) and c[j + 1] in ('>', '>>', '<', '>&'):
            j += 1
            continue
        rest.append(t)
        j += 1
    return name, rest, redir


def file_operands(name, args):
    """Operands that are files (pattern / script / program removed). Also --include values."""
    argopts = {'grep': 'efmABCdD', 'egrep': 'efmABCdD', 'fgrep': 'efmABCdD', 'zgrep': 'efmABCdD',
               'sed': 'efl', 'gsed': 'efl', 'awk': 'Fvf', 'gawk': 'Fvf', 'cat': ''}[name]
    files, nonopt, inc, has_script = [], [], [], False
    i, endopts = 0, False
    while i < len(args):
        a = args[i]
        if not endopts and a == '--':
            endopts = True
        elif not endopts and a.startswith('--'):
            if a.startswith(('--include', '--file', '--regexp', '--expression')):
                if '=' in a:
                    v = a.split('=', 1)[1]
                else:
                    i += 1
                    v = args[i] if i < len(args) else ''
                if a.startswith('--include'):
                    inc.append(v)
                else:
                    has_script = True
        elif not endopts and a.startswith('-') and len(a) > 1:
            k = 1
            while k < len(a):
                ch = a[k]
                if name in ('sed', 'gsed') and ch == 'i':
                    if k + 1 == len(a) and i + 1 < len(args) and (args[i + 1] == '' or args[i + 1].startswith('.')):
                        i += 1
                    break
                if ch in argopts:
                    if ch in 'ef':
                        has_script = True
                    if k + 1 == len(a):
                        i += 1
                    break
                k += 1
        else:
            nonopt.append(a)
        i += 1
    if name == 'cat' or has_script:
        files = nonopt
    else:
        files = nonopt[1:]
    return files + inc


def shell_hits(shell, kind):
    rx = re.compile(DOC[kind], re.I)
    for pl in pipelines(shell):
        heads = [head(c) for c in pl]
        for n, (name, args, redir) in enumerate(heads):
            if name in TEXTCMD:
                if any(rx.search(f) for f in file_operands(name, args) + redir):
                    return True
            # a document's text piped into grep/sed/awk/cat downstream
            docarg = any(rx.search(a) for a in args + redir) or (
                kind == 'docx' and name == 'unzip' and any(a.startswith('word/') for a in args))
            if name in ('unzip', 'strings', 'textutil', 'cat', 'pdftotext') and docarg:
                if name == 'unzip' and not any(re.match(r'^-\w*[pc]', a) for a in args):
                    continue
                if any(h[0] in TEXTCMD for h in heads[n + 1:]):
                    return True
    return False


def code_hits(text, kind):
    """grep/sed/awk/cat run from inside a script (string or argv list) on a document."""
    ext = DOC[kind]
    if re.search(r'''["'](grep|egrep|fgrep|sed|awk|cat)\s[^"'\n]*''' + ext, text, re.I):
        return True
    if re.search(r'''["'](grep|egrep|fgrep|sed|awk|cat)["']\s*,[^\]\n]*''' + ext, text, re.I):
        return True
    return False


def pdftotext_run(text):
    for m in re.finditer(r'pdftotext', text):
        s, e = m.start(), m.end()
        before = text[:s]
        seg_start = max(before.rfind(ch) for ch in ';&|()\n`')
        prefix = before[seg_start + 1:].strip()
        in_sub = seg_start >= 0 and (before[seg_start] == '`' or before[max(0, seg_start - 1):seg_start + 1] == '$(')
        if re.match(r'^(which|command\s+-v|type|hash|whereis)\b', prefix):
            # P=$(which pdftotext) keeps the path to run it later: still a block
            if in_sub or re.search(r'=\s*\$?\($', before[:seg_start + 1]):
                return True
            continue
        after = text[e:]
        if re.match(r'\s+(-v|--version|-h|--help)(?![\w-])\s*($|[;&|)\n])', after):
            continue
        if re.match(r'''\s+[-"'$\w./~{<]''', after):
            return True
        if s > 0 and text[s - 1] in '"\'' and after[:1] == text[s - 1]:
            return True
    return False


def main():
    rule = sys.argv[1]
    cmd = sys.stdin.read()
    shell, bodies = split_heredocs(cmd)
    if rule == 'pdftotext':
        return 'BLOCK' if pdftotext_run(cmd) else 'ALLOW'
    if rule == 'pylib':
        sig = r'''(?i)extract|get_?text|gettext|textpage|search_for|pdfminer|pdfplumber|\.chars\b|\[\s*\d{2,3}(\s*,\s*\d{2,3}){4,}|["']\s*\+\s*["']'''
        use = (r'(?i)import\s+(pypdf|pypdf2|pdfplumber|fitz|pymupdf|pdfminer)|from\s+(pypdf|pypdf2|pdfplumber|fitz|pymupdf|pdfminer)'
               r'|pdfreader\s*\(|(fitz|pymupdf|pdfplumber)\.open|__import__|import_module')
        return 'BLOCK' if (re.search(use, cmd) and re.search(sig, cmd)) else 'ALLOW'
    if rule in ('pdf', 'docx'):
        if shell_hits(shell, rule):
            return 'BLOCK'
        # quoted strings and heredoc bodies may hold script code
        if any(code_hits(b, rule) for b in bodies) or code_hits(shell, rule):
            return 'BLOCK'
        return 'ALLOW'
    return 'BLOCK'


if __name__ == '__main__':
    try:
        print(main())
    except Exception:
        print('BLOCK')
PYEOF
confirm() {
  printf '%s' "$command" | /usr/bin/python3 -I -c "$CONFIRM_PY" "$1" 2>/dev/null || echo BLOCK
}

# Block pdftotext on any file
if echo "$command" | grep -qE 'pdftotext' && [ "$(confirm pdftotext)" != ALLOW ]; then
  echo "DENIED by doc_extraction_guard: pdftotext is blocked. Open PDFs using the Read tool (for local files), Playwright (for web PDFs), or Google Drive MCP. Bash text extraction produces citations the citation integrity hook cannot verify." >&2
  exit 2
fi

# Block grep/sed/awk/cat targeting .pdf or known text extraction files
if echo "$command" | grep -qE '(grep|sed|awk|cat)\s.*\.(pdf|PDF)' && [ "$(confirm pdf)" != ALLOW ]; then
  echo "DENIED by doc_extraction_guard: grep/sed/awk/cat on PDF files is blocked. Open PDFs using the Read tool, Playwright, or Google Drive MCP." >&2
  exit 2
fi

# Block grep/sed/awk/cat targeting the .playwright-mcp text extraction files
if echo "$command" | grep -qE '(grep|sed|awk|cat)\s.*playwright-mcp/.*-text\.txt'; then
  echo "DENIED by doc_extraction_guard: Bash extraction from playwright-mcp text files is blocked. These are unverified extractions. Open the source PDF using the Read tool, Playwright, or Google Drive MCP instead." >&2
  exit 2
fi

# Block python-based PDF text extraction (pypdf / PyPDF2 / pdfplumber / PyMuPDF).
# These bypass the Read tool, fail SILENTLY on pages that don't extract cleanly,
# and have produced false "not in the document" conclusions. PDFs must be read
# with the Read tool, which renders the actual page (reliable and visible).
if echo "$command" | grep -qiE '(pypdf|pdfreader|\.extract_text|pdfplumber|pymupdf|import fitz|fitz\.open)' && [ "$(confirm pylib)" != ALLOW ]; then
  echo "DENIED by doc_extraction_guard: python PDF text-extraction (pypdf/pdfplumber/PyMuPDF/etc.) is blocked — it fails silently on some pages and has produced false 'not in the document' calls. Read the PDF with the Read tool (pages=N-M); it renders the actual page. Then cite the page number + a verbatim line from what you read." >&2
  exit 2
fi

# Block ad-hoc grep/sed/awk/cat on Word/Google docs (unreliable text munging).
# python-docx is NOT blocked: it reads .docx structured XML reliably (no silent
# OCR-style failure like PDFs), so it's the sanctioned reader for local .docx.
# Native Google Docs (.gdoc/.gsheet) that aren't downloaded: use the Drive MCP.
if echo "$command" | grep -qiE '(grep|sed|awk|cat)\s.*\.(docx|doc|gdoc|gsheet)([^a-z]|$)' && [ "$(confirm docx)" != ALLOW ]; then
  echo "DENIED by doc_extraction_guard: grep/sed/awk/cat on Word/Google docs is blocked. Read local .docx with python-docx (reliable structured text) or the Read tool; use the Google Drive MCP for native Google Docs." >&2
  exit 2
fi

exit 0
