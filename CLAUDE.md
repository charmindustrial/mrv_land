# MRV Expert Workspace

Max Lavine's MRV (Measurement, Reporting, Verification) workspace for Charm Industrial. This file is auto-loaded by Claude Code at session start.

## Read these first

- `README.txt` — workspace conventions, folder layout, audience routing rules
- `FOLDER_INDEX.md` — same content in markdown, with routing tables

Read them whenever you're about to do non-trivial work in this folder.

## Hard rules (no exceptions)

**When assigned a task, do it. Never redirect work back to Max or to a colleague that is Claude's job to do.** If genuinely blocked after exhausting every option, state exactly what was tried and exactly why each path failed — then stop. Enforced by `~/.claude/hooks/no_deferral_guard.sh`.

**Identifying a problem or limitation is not the end of the job — solving it is.** When something is broken, wrong, or constrained, do not stop at explaining why. Find the fix and implement it, or present concrete options and let Max choose.

**When citing what a document says, quote the exact text. Never paraphrase a clause and present it as what the document says.** If you haven't read the specific text in this session, say so. Do not characterize document content from memory or inference and present it as a citation. This applies to every document — specs, standards, protocols, methodology docs, everything.

**Before stating any fact about the state or configuration of an external system (Jira, Certify, or any other live tool), run the relevant API call or read the UI in the current session and quote the response. Never infer or recall system state from memory or prior sessions. If the API is blocked or inaccessible, say "I cannot verify this" and stop — do not guess.** This rule exists because inferred Jira state caused Max to make incorrect asks of colleagues and lose credibility with them.

**For any compliance review, gap analysis, or protocol check: read the source first, extract every requirement as a verbatim quote, then check each one against the work product. The gap list is derived from that requirements list — nothing goes in the gap list that does not trace to a verbatim quote already in hand. No quote = no gap. This is enforced by the citation integrity hook, which will block any finding that cites a requirement without a verbatim quote. The hook catches missing quotes; this rule prevents gaps with no citation at all.**

**When a hook fires and blocks a response, the only acceptable next output is the complete corrected work product — never an explanation of why the hook fired, never a patched fragment appended to the end.** Fix the triggering content, then re-deliver the entire thing. "The hook was a false positive" is not a valid response; rephrase and re-deliver regardless. This rule has been violated repeatedly and must be treated as a hard floor, not a preference.

**Any change to the folder structure must update BOTH `README.txt` AND `FOLDER_INDEX.md` in the same change.** Out-of-date docs mislead future agents and waste time. This rule comes from the workspace itself, not from Claude Code defaults — honor it.

## Skill discovery

Skills live in `.claude/skills/` as symlinks pointing to the canonical sources in `skills/`. Claude Code auto-discovers them when launched from this folder (or any subfolder).

When editing a skill, **edit the canonical `SKILL.md` under `skills/`, not the symlink.** The `.skill` archive next to each canonical SKILL.md is a Desktop build artifact — repackage it after edits if you still want Desktop to see the change.

## Audience routing

The brief-writer skill MUST ask the user which audience a brief is for before drafting (Isometric / feedstock-suppliers / other-external / internal Charm). Audience drives both composition and storage destination — see README.txt for the full routing table.

## Machine-portability notes (read before moving the workspace to a new machine)

Most of the workspace is portable — clone the repo and it just works. Two pieces are NOT portable and need manual touch-up on a fresh machine:

1. **`.claude/skills/` symlinks** — gitignored because they're absolute paths that don't survive a machine move. Recreate one symlink per skill: `ln -s ../../skills/<cluster>/<skill> .claude/skills/<skill>`. The README's SKILLS section lists every skill that needs one.

2. **`.claude/settings.json` Stop-hook absolute path** — the auto-sync hook is registered with a hardcoded absolute path:
   ```
   "command": "/Users/maxlavine/Desktop/Claude/Skills/MRV Expert/.claude/auto-sync.sh"
   ```
   On a new machine this path will be wrong and the auto-sync will silently fail (Stop hook errors don't surface to the session). Update the absolute path to match the new machine's clone location, OR change it to `bash "${CLAUDE_PROJECT_DIR}/.claude/auto-sync.sh"` if you trust Claude Code to always set that env var. (We left it absolute for the louder failure mode — fail-loudly-on-new-machine beats silent-failure-when-env-var-missing.)

The `workspace_hygiene_guard.sh` PreToolUse hook is already portable: it self-derives the workspace path from its own location, so cloning to a new path requires no changes.
