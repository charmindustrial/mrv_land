# MRV Expert Workspace

Max Lavine's MRV (Measurement, Reporting, Verification) workspace for Charm Industrial. This file is auto-loaded by Claude Code at session start.

## Read these first

- `README.txt` — workspace conventions, folder layout, audience routing rules
- `FOLDER_INDEX.md` — same content in markdown, with routing tables

Read them whenever you're about to do non-trivial work in this folder.

## Hard rule (no exceptions)

**Any change to the folder structure must update BOTH `README.txt` AND `FOLDER_INDEX.md` in the same change.** Out-of-date docs mislead future agents and waste time. This rule comes from the workspace itself, not from Claude Code defaults — honor it.

## Skill discovery

Skills live in `.claude/skills/` as symlinks pointing to the canonical sources in `skills/`. Claude Code auto-discovers them when launched from this folder (or any subfolder).

When editing a skill, **edit the canonical `SKILL.md` under `skills/`, not the symlink.** The `.skill` archive next to each canonical SKILL.md is a Desktop build artifact — repackage it after edits if you still want Desktop to see the change.

## Audience routing

The brief-writer skill MUST ask the user which audience a brief is for before drafting (Isometric / feedstock-suppliers / other-external / internal Charm). Audience drives both composition and storage destination — see README.txt for the full routing table.
