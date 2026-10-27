#!/usr/bin/env bash
# input_file_write_guard.sh
#
# PreToolUse hook (Bash | Write | Edit).
#
# The failure this closes: the screener was handed a source spreadsheet to PULL
# document links FROM, and instead WROTE status back into it — modifying the
# user's master. Nothing in the request or the skill authorised that. An input
# is not a deliverable.
#
# RULE: under the biomass "Prospective" tree, the ONLY files any tool may write
# are the screener's own outputs:
#     "* BFA v1.3 Pre-Screen.docx"  and  "*Gap*Checklist*.xlsx"
# Every other file under that tree that ALREADY EXISTS is an input the user
# provided (the master tracker, grant docs, SOWs, W-9s, evidence packages, …)
# and is READ-ONLY. Writing to one is denied. Named belt: .claude/protected_inputs.txt.
#
# Creating a NEW screener output is allowed. Reading anything is allowed.
# Writes OUTSIDE the biomass tree (repo, scratchpad, skills, hooks) are untouched.
#
# Deny semantics: exit 2 + reason on stderr (surfaces to Claude to adapt).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
input="$(cat)"

HOOK_TOOL="$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null || echo "")"
HOOK_CMD="$(echo "$input" | jq -r '.tool_input.command // empty' 2>/dev/null || echo "")"
HOOK_FP="$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null || echo "")"
export HOOK_TOOL HOOK_CMD HOOK_FP HOOK_DIR="$SCRIPT_DIR"

python3 <<'PYEOF'
import os, re, sys, glob

script_dir = os.environ.get("HOOK_DIR", ".")
tool = os.environ.get("HOOK_TOOL", "")
cmd  = os.environ.get("HOOK_CMD", "")
fp   = os.environ.get("HOOK_FP", "")

TREE = "Feedstocks/Biomass/Prospective"
BIOMASS_ROOT = os.path.expanduser(
    "~/Library/CloudStorage/GoogleDrive-max@charmindustrial.com/My Drive/MRV/Feedstocks/Biomass/Prospective")

def is_output(bn):
    b = bn.lower()
    # screener deliverables (any project, standardized or legacy naming)
    if b.endswith(".docx") and "pre-screen" in b:
        return True
    if b.endswith(".xlsx") and "gap" in b and "checklist" in b:
        return True
    return False

# named registry (explicit belt)
reg = []
try:
    for ln in open(os.path.join(script_dir, "..", "protected_inputs.txt")):
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            reg.append(ln)
except Exception:
    pass

# dynamic: every existing file under the tree that is NOT an output is protected
protected_basenames = set()
if os.path.isdir(BIOMASS_ROOT):
    for p in glob.glob(os.path.join(BIOMASS_ROOT, "**", "*"), recursive=True):
        if os.path.isfile(p):
            bn = os.path.basename(p)
            if not is_output(bn) and not bn.startswith("~$"):
                protected_basenames.add(bn)

def protected(s):
    bn = os.path.basename(s.rstrip("/"))
    for pat in reg:
        if pat in s:
            return f"matches protected-inputs registry entry '{pat}'"
    if TREE in s and bn and not is_output(bn):
        return "is a pre-existing input under the biomass Prospective tree (read-only)"
    if bn in protected_basenames and not is_output(bn):
        return "is a pre-existing input file (read-only)"
    return None

def deny(target, reason):
    print("─"*72, file=sys.stderr)
    print("INPUT FILE WRITE — blocked", file=sys.stderr)
    print("─"*72, file=sys.stderr)
    print(f"Refusing to write to:  {target}", file=sys.stderr)
    print(f"Reason: this file {reason}.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Files the user provides are INPUTS to read from, never deliverables to", file=sys.stderr)
    print("modify. The screener writes ONLY its own outputs (Pre-Screen .docx and the", file=sys.stderr)
    print("per-project Gap Checklist .xlsx). If a status belongs somewhere, put it in", file=sys.stderr)
    print("that project's OWN gap checklist — never the source.", file=sys.stderr)
    print("─"*72, file=sys.stderr)
    sys.exit(2)

# ── Write / Edit / NotebookEdit ───────────────────────────────────────────────
if tool in ("Write", "Edit", "NotebookEdit"):
    if fp:
        r = protected(fp)
        if r:
            deny(fp, r)
    sys.exit(0)

# ── Bash: resolve write TARGETS from the command ──────────────────────────────
if tool == "Bash" and cmd:
    targets = []  # (display, resolved)

    def resolve_var(var):
        out = []
        for m in re.finditer(r'\b' + re.escape(var) + r'\s*=\s*([^\n]+)', cmd):
            for q in re.findall(r'''['"]([^'"]+)['"]''', m.group(1)):
                out.append(q)
        return out

    for m in re.finditer(r'\.(?:save|to_excel|to_csv)\(\s*([^)\s,]+)', cmd):
        arg = m.group(1).strip()
        qm = re.match(r'''['"]([^'"]+)['"]''', arg)
        if qm:
            targets.append((qm.group(1), qm.group(1)))
        elif re.match(r'^[A-Za-z_]\w*$', arg):
            for frag in resolve_var(arg):
                targets.append((f"{arg} -> {frag}", frag))
    for m in re.finditer(r'''open\(\s*([^,]+),\s*['"][wa]''', cmd):
        arg = m.group(1).strip()
        qm = re.match(r'''['"]([^'"]+)['"]''', arg)
        if qm:
            targets.append((qm.group(1), qm.group(1)))
        elif re.match(r'^[A-Za-z_]\w*$', arg):
            for frag in resolve_var(arg):
                targets.append((f"{arg} -> {frag}", frag))
    for m in re.finditer(r'>>?\s*("(?:[^"]+)"|\'(?:[^\']+)\'|[^\s;|&]+)', cmd):
        t = m.group(1).strip('"\'')
        targets.append((t, t))
    for m in re.finditer(r'\b(?:cp|mv|tee)\b[^\n]*?("(?:[^"]+)"|\'(?:[^\']+)\')', cmd):
        t = m.group(1).strip('"\'')
        targets.append((t, t))
    for m in re.finditer(r'''(?:shutil\.copy\w*|copyfile)\([^)]*?,\s*['"]([^'"]+)['"]''', cmd):
        targets.append((m.group(1), m.group(1)))

    for disp, resolved in targets:
        r = protected(resolved)
        if r:
            deny(disp, r)

    # registry belt for idioms not parsed above
    write_verb = re.search(r'\.save\(|\.to_excel\(|\.to_csv\(|open\([^)]*,\s*[\'"][wa]|>>?\s|\b(?:cp|mv|tee)\b', cmd)
    if write_verb:
        for pat in reg:
            if pat in cmd and (
                re.search(r'(?:save|to_excel|to_csv|open|>|cp|mv|tee)[^\n]{0,80}' + re.escape(pat), cmd)
                or re.search(re.escape(pat) + r'[^\n]{0,40}(?:["\']\s*\)|>>?)', cmd)):
                deny(pat, f"matches protected-inputs registry entry '{pat}'")

sys.exit(0)
PYEOF
