"""no_fragment_redelivery_guard -- Stop hook.

Project rule (CLAUDE.md, "Hard rules"): when a Stop hook blocks a response,
the ONLY acceptable next output is the complete corrected work product --
never a rebuttal of the hook, never a fragment that leans on an earlier
message ("the summary above stands", "not re-sending"), and it must open
with the literal line "**FINAL — supersedes everything above.**".

This fires only when the message being finished is itself a redo after a
Stop-hook block earlier in this same exchange (detected by a "Stop hook
feedback" pseudo-user message immediately preceding it in the transcript)
-- it never touches a normal first-pass response.

Run directly (not via a bash heredoc): a heredoc embedding this much Python
inside a `$(...)` command substitution was found to break bash's own parser
on certain quote/paren combinations -- see git history. A standalone file
invoked as `python3 no_fragment_redelivery_guard.py TRANSCRIPT_PATH` sidesteps
that fragility entirely, matching stale_drive_read_guard.py's split.

Releases itself after MAX_STREAK consecutive fires so a mis-firing guard
cannot hold the session hostage. Fails open on any error. Exit 2 -> reason on
stderr feeds back to Claude as error context.

analyse(final_text) -> list[str] of violation lines (empty = pass)
"""

import json
import os
import re
import sys

MARKER = '**FINAL — supersedes everything above.**'

DISMISSAL_PATTERNS = [
    (r'\babove stands\b', 'refers back to a prior message instead of resending it'),
    (r'\bnot\s+re-?sending\b', 'explicitly declines to resend the full work product'),
    (r'\balready\s+passed\b.{0,40}\bnothing\s+else\s+changed\b', 'dismisses the hook instead of complying'),
    (r'\bstands\s+as\s+(?:previously\s+)?(?:delivered|sent|written)\b', 'refers back instead of resending'),
    (r'\bno\s+need\s+to\s+resend\b', 'explicitly declines to resend'),
    (r'\bthe\s+summary\s+above\b', 'refers to a prior message as if still current'),
]


def _strip_quoted(text):
    """Citing the offending phrase (explaining what an earlier response got
    wrong) is not committing the same offense -- drop quoted spans and
    markdown blockquote lines before scanning, so only the assistant's own
    live prose can trip these patterns."""
    text = re.sub(r'["“][^"“”]*["”]', '', text)
    return '\n'.join(
        line for line in text.splitlines() if not line.lstrip().startswith('>')
    )


def analyse(final_text):
    if not final_text or not final_text.strip():
        return []

    violations = []
    if not final_text.strip().startswith(MARKER):
        violations.append('Missing required opening line: %s' % MARKER)

    scannable = _strip_quoted(final_text)
    for pattern, why in DISMISSAL_PATTERNS:
        if re.search(pattern, scannable, re.IGNORECASE):
            violations.append('Dismissal fragment detected (%s): matched /%s/' % (why, pattern))

    return violations


# ------------------------------------------------------------- transcript walk

def _text_of(entry):
    msg = entry.get('message', {})
    if not isinstance(msg, dict):
        return None
    content = msg.get('content', [])
    if isinstance(content, list):
        parts = [c.get('text', '') for c in content
                 if isinstance(c, dict) and c.get('type') == 'text']
        return '\n'.join(parts) if parts else None
    if isinstance(content, str) and content:
        return content
    return None


def _role_of(entry):
    msg = entry.get('message', {})
    return msg.get('role') if isinstance(msg, dict) else None


def _load_entries(transcript_path):
    entries = []
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def check_transcript(transcript_path):
    """Return violation lines for the transcript's final message, or []
    if this isn't a hook-triggered redo / nothing to flag."""
    entries = _load_entries(transcript_path)

    final_text = None
    final_idx = None
    for i in range(len(entries) - 1, -1, -1):
        if _role_of(entries[i]) == 'assistant':
            t = _text_of(entries[i])
            if t:
                final_idx = i
                final_text = t
                break
    if final_idx is None:
        return []

    # Was this message a redo after a Stop-hook block? Look at the nearest
    # preceding entry that carries text (skip tool-result-only user entries,
    # which are not hook feedback -- hook feedback is real inserted text).
    prev_hook_feedback = None
    for i in range(final_idx - 1, -1, -1):
        e = entries[i]
        if _role_of(e) != 'user':
            continue
        t = _text_of(e)
        if t is None:
            content = e.get('message', {}).get('content', [])
            if isinstance(content, list) and any(
                isinstance(c, dict) and c.get('type') == 'tool_result' for c in content
            ):
                continue
            break
        prev_hook_feedback = t
        break

    if not prev_hook_feedback or 'stop hook feedback' not in prev_hook_feedback.lower():
        return []  # not a hook-triggered redo -- nothing to check

    return analyse(final_text)


def main():
    if len(sys.argv) < 2:
        return 0
    transcript_path = sys.argv[1]
    if not transcript_path or not os.path.isfile(transcript_path):
        return 0

    try:
        violations = check_transcript(transcript_path)
    except Exception:
        return 0  # fail open

    sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
    from circuit_breaker import Breaker
    brk = Breaker(
        state_file=os.path.expanduser('~/.claude/hooks/.no_fragment_redelivery_block_streak'),
        label='NO-FRAGMENT-REDELIVERY GUARD',
        max_strikes=3,
    )

    if not violations:
        brk.clear()
        return 0

    if brk.tripped():
        return 0

    brk._write(brk.count + 1)

    print('─' * 72, file=sys.stderr)
    print('NO-FRAGMENT REDELIVERY — hook feedback answered with a fragment', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    print('A Stop hook fired earlier in this exchange. Per CLAUDE.md, the ONLY', file=sys.stderr)
    print('acceptable next output is the complete corrected work product, opening', file=sys.stderr)
    print('with the exact line "%s". Arguing' % MARKER, file=sys.stderr)
    print('with the hook, or saying an earlier message "stands" instead of resending', file=sys.stderr)
    print('it in full, is not compliant.', file=sys.stderr)
    print('', file=sys.stderr)
    for v in violations:
        print('  ' + v, file=sys.stderr)
    print('', file=sys.stderr)
    print('Fix: re-deliver the ENTIRE work product now, corrected, starting with the', file=sys.stderr)
    print('FINAL marker line and nothing before it. Do not summarize what changed --', file=sys.stderr)
    print('send the whole thing.', file=sys.stderr)
    print('─' * 72, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
