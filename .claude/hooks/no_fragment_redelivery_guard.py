"""no_fragment_redelivery_guard -- Stop hook.

Project rule (CLAUDE.md, "Hard rules"): when a Stop hook blocks a response,
the ONLY acceptable next output is the complete corrected work product --
never a rebuttal of the hook, never a fragment that leans on an earlier
message ("the summary above stands", "not re-sending"), and it must open
with the literal line "**FINAL — supersedes everything above.**". There is
no batch-QA carve-out anywhere in that rule -- it applies to every
hook-triggered redo.

2026-09-24: this guard and ~/.claude/hooks/final_marker_receipt_guard.sh used
to carry two different definitions of when the marker is owed -- this one
required it on every redo, the other rejected it on anything that was not a
green-gated batch QA delivery -- and alternately blocked the same message
forever (session 5a66d183, lines 2820/2823/2833/2986/2989/2993/2996/3001/
3037). A same-day attempt to resolve this by keeping the batch-QA test (this
guard would only require the marker when a locally-ported
_is_batch_qa_delivery() said so, while the receipt guard required BOTH a real
redo AND that same batch-QA test) reproduced the identical deadlock, because
this guard's analyse() never actually consulted that batch-QA test -- it kept
requiring the marker unconditionally regardless of the docstring's claim.
Reverted both the dead-code half-measure and the batch-QA test itself: there
is no batch-QA carve-out in CLAUDE.md's rule, so there should not be one here.

Both guards now import the single shared answer from
~/.claude/hooks/lib/final_marker_obligation.py (owes_marker()): the marker is
owed, full stop, whenever a genuine Stop/SubagentStop hook-feedback entry
precedes the message in the current turn with no clean marked re-delivery
since -- no batch QA test involved.

This fires only when the message being finished is itself a redo after a
Stop-hook block earlier in this same exchange (owes_marker() detects this via
a "Stop hook feedback" pseudo-user message earlier in the turn) -- it never
touches a normal first-pass response.

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

sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
from final_marker_obligation import MARKER, owes_marker

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
    text = re.sub(r'["\u201c][^"\u201c\u201d]*["\u201d]', '', text)
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
    # GUARD_CONTRACT rule 12 (2026-10-27 audit): the message in the hook
    # input wins when the transcript file has not caught up to it. Judged from
    # the file alone, a correct re-send could be blocked for the previous
    # draft's missing marker. The live message comes after everything in the
    # file, so it is judged as standing at the end.
    live = os.environ.get('HOOK_LAST_ASSISTANT_MESSAGE', '')
    if live.strip() and ' '.join(live.split()) != ' '.join((final_text or '').split()):
        final_text, final_idx = live, len(entries)
    if final_idx is None:
        return []

    # Whether this message owes (and may use) the FINAL marker is answered
    # in exactly one shared place now -- lib/final_marker_obligation.py --
    # so this guard and final_marker_receipt_guard.sh cannot disagree about
    # the same message again.
    if not owes_marker(entries, final_idx):
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
    # Shared per-turn block budget: work out a name for the current turn so that
    # every guard counts its blocks against the same budget (lib/circuit_breaker.py).
    sys.path.insert(0, os.path.expanduser('~/.claude/hooks/lib'))
    try:
        from transcript_text import turn_key_from_path as _tk_from_path
        _turn = _tk_from_path(transcript_path)
    except Exception:
        _turn = None
    brk = Breaker(
        state_file=os.path.expanduser('~/.claude/hooks/.no_fragment_redelivery_block_streak'),
        label='NO-FRAGMENT-REDELIVERY GUARD',
        max_strikes=3, turn_key=_turn, transcript_path=transcript_path
    )

    if not violations:
        brk.clear()
        return 0

    if brk.tripped():
        return 0

    lines = [
        '─' * 72,
        'NO-FRAGMENT REDELIVERY — hook feedback answered with a fragment',
        '─' * 72,
        'A Stop hook fired earlier in this exchange. Per CLAUDE.md, the ONLY',
        'acceptable next output is the complete corrected work product, opening',
        'with the exact line "%s". Arguing' % MARKER,
        'with the hook, or saying an earlier message "stands" instead of resending',
        'it in full, is not compliant.',
        '',
    ] + ['  ' + v for v in violations] + [
        '',
        'Fix: re-send the whole work product now, corrected, marker line first.',
        'A tighter re-send is fine as long as nothing that already passed is',
        'dropped -- this guard checks for the marker and for dismissals, not length.',
        '─' * 72,
    ]
    brk.block_and_exit(lines)  # exits the process; never returns


if __name__ == '__main__':
    sys.exit(main())
