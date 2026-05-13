# Batch QA Cost-Down Backlog

Filed 2026-05-07 from QA 2-201 session ($205 actual / ~$140-170 expected without mid-session detours / **revised target ~$110-150 after risk-cleared changes**).

**Decisions log (2026-05-08):**
- **L1: DONE.** `checklist_lib.py` shipped; pre-flight `[log:KEY]` validation + `_derived_values` auto-merge. Clean against 2-187/2-204/2-201.
- **L2 (Sonnet Drive extraction): PARKED.** Shifts integrity anchor to subagent schema fidelity. Sonnet misread → log inherits → audit can't catch. The silent-error mode FC10 was built to prevent. See `feedback_no_subagent_primary_source_extraction.md`.
- **L3 (sister-batch consolidation): PARKED.** Real cacheable surface is ~$5-10/batch, not $30-50. EFs and full-leg distances are shared; emissions and allocated distances are per-offload (= shared × per-offload mass × per-offload allocation). Caching the second bucket = silent-error mode. See `feedback_railcar_cache_methodology.md`.
- **L4 (Sonnet Certify modals): PARKED.** Same as L2.
- **L5, L6: GO.** Behavioral SKILL.md, zero architectural risk.

Envelope after L1+L5+L6: ~$110-150/batch clean. Original $60-100 depended on parked levers.

## Anchor data

Sister batches on Opus 4.7, $/batch by turn count:

| Batch | Turns | Cost |
|---|---|---|
| 2-187 | 228 | $127 |
| 2-204 | 229 | $136 |
| 2-186 | 290 | $146 |
| 2-192 | 297 | $179 |
| 2-188 | 320 | $181 (had rework) |
| 2-201 | 310 | $205 (had browser config detour + audit-fix loop) |
| 2-190 | 428 | $243 |
| 2-185 | 492 | $376 (FC11 rework) |

**Cost is dominated by cache reads** (~50%) which scale with turns × per-turn context size. Output is ~13%. Fresh input is negligible (cache hit rate is ~99%).

Pricing (Opus 4.7, $/M tokens):
- Input: $15
- Output: $75
- Cache read: $1.50
- Cache write 5m: $18.75
- Cache write 1h: $30

## Levers, prioritized

### 1. Auto-emit `_derived_values` + validate `[log:KEY]` citations on build (do first, free)

**Saves:** ~$15-25/batch
**Difficulty:** Pure engineering
**Risk:** Zero

**Today:** [log:KEY] tags are hand-written in evidence text. If a tag references a key that doesn't exist (e.g., `scale_tickets.derived.net_kg` when log has `net_weight_kg`), audit fails and the build_checklist + audit cycle re-runs ~5 times to clean up.

**Change:** In `skills/qa/batch-qa-aecn/scripts/audit_checklist.py` and per-batch `build_checklist.py`:
1. Pre-flight validation step: walk every `[log:KEY]` in ROWS, resolve against source-read log JSON, fail loudly with bad-key list BEFORE writing the xlsx.
2. Auto-emit a `_derived_values` block in source-read log: scan all evidence-text quoted numerics in the script's own ROWS data; for any quoted number that's a script-computed value (not raw from a source), automatically add a key to `_derived_values` with that value.
3. Common derived value names should be standardized — see `outputs/qa/batch-2-204/batch_2-204_source_reads.json` `_derived_values` block for the convention; same block in `batch-2-201` for the latest pattern.

**Files:**
- `skills/qa/batch-qa-aecn/scripts/audit_checklist.py` — main edit target
- `skills/qa/batch-qa-aecn/references/checklist_structure.md` — document the convention
- Any per-batch `outputs/qa/batch-*/build_checklist.py` — should inherit from a shared library

### 2. Sonnet subagent for Drive extraction (biggest single lever)

**Saves:** ~$30-50/batch
**Difficulty:** Skill refactor
**Risk:** Low (subagent returns values; main Opus session still cross-checks)

**Today:** Main Opus session does every Drive read in `SKILL.md` "Required reads" 1-5 (scale tickets, BOLs, lab CHN, Ops Notes, COBB). Heavy raw tool results (986KB scale ticket b64, 320KB COBB dump) live in main-session context for the rest of the run, paying cache-read tax on every subsequent turn.

**Change:** Refactor `SKILL.md` Gate 1 "Required reads" section to:
1. Spawn a Sonnet subagent at start of Gate 1 with explicit JSON schema for what to extract (scale ticket fields, BOL fields, CHN fields, Ops Notes fields, COBB fields).
2. Subagent does all the downloads, image reads, XLSX parses; returns one ~5KB structured JSON.
3. Main Opus session writes the source-read log from the JSON return, then does Certify reads + cross-checking + checklist build.

**Subagent invocation:** `Agent(subagent_type: "general-purpose", model: "sonnet", prompt: "...")`. The `model` parameter is already exposed by the Agent tool — no harness change needed.

**Why this compounds:** Sonnet ~3x cheaper on input/cache, ~5x on output. AND the raw bytes don't enter main session context, so the per-turn cache-read base shrinks for the entire rest of the run.

**Files:**
- `skills/qa/batch-qa-aecn/SKILL.md` — Gate 1 "Required reads" section
- New: `skills/qa/batch-qa-aecn/agents/drive-extractor.md` (or inline schema in SKILL.md)

### 3. Sister-batch consolidation for same-railcar QAs

**Saves:** ~$30-50 on offloads 2-4 of a railcar (compounding)
**Difficulty:** Skill refactor
**Risk:** Medium-low

**Today:** Each offload of a railcar re-extracts shared facts: 3 BOL masses, lab cert presence, EF values, full route distances, document presence checks. Same work 4 times for a 4-offload railcar.

**Change:** SKILL.md gains a "subsequent batch on railcar" branch. If `qa_active_batches.json` has a sister batch on the same railcar, the Drive extractor subagent gets a different prompt:
- Confirm 3 BOL filenames and masses still match prior batch's source-read log (don't re-download/re-parse PDFs).
- Confirm lab cert filename / EF values / route distances still match.
- Re-extract per-batch values: this offload's scale ticket pair, Cargo (kg), pH, allocation fraction, Net CDR.

Adversarial reviewer continues to challenge anything that smells templated. Add an explicit instruction to the reviewer to check at least one railcar-level value against primary source on subsequent-batch QAs.

**Files:**
- `skills/qa/batch-qa-aecn/SKILL.md` — branch logic for railcar continuations
- `skills/qa/adversarial-reviewer/SKILL.md` — sister-batch-aware challenges

### 4. Sonnet subagent for Certify modal capture

**Saves:** ~$15-25/batch
**Difficulty:** Skill refactor
**Risk:** Low

**Today:** Main session opens 9 component modals sequentially. Each one is a click → snapshot (saves 350-line yml) → grep → close cycle. ~30 turns total.

**Change:** Refactor SKILL.md Gate 2 "Mandatory Verification Sub-Tasks" item 3 (Uncertainty modals) to delegate to a Sonnet subagent with `playwright-mrv` MCP access. Subagent gets a list of 9 component IDs and returns one JSON blob with each component's inputs/EF/distance/mass/uncertainty.

**Verify before shipping:** Confirm `certify_readonly_guard.sh` hook fires for subagent tool calls. The hook matches `mcp__playwright(-mrv)?__.*` and runs PreToolUse, which should apply regardless of which agent issues the call. Test with a known-bad call (e.g., `browser_type`) from a subagent and confirm denial.

**Files:**
- `skills/qa/batch-qa-aecn/SKILL.md` — Gate 2 mandatory sub-task #3
- `~/.claude/hooks/certify_readonly_guard.sh` — verify subagent coverage (likely already works)

### 5. Tighter snapshots and re-grep over saved files

**Saves:** ~$10-15/batch
**Difficulty:** Behavioral (instructions in SKILL.md)
**Risk:** Zero

**Today:** Full-page Certify snapshots are 400+ lines; sometimes a fresh snapshot is taken when a saved one already has the value.

**Change:** SKILL.md should explicitly instruct:
- Use `target` / `depth` params on `browser_snapshot` to scope to specific regions where possible.
- After capturing a yml snapshot, re-grep over the saved file when looking up a value already captured. Don't re-snapshot.

### 6. Trim narration verbosity

**Saves:** ~$10/batch
**Difficulty:** Behavioral
**Risk:** Low

**Today:** ~1,170 output tokens per turn, with lots of post-tool-call status restating ("found 3 BOLs ✓, sum 76.58 MT ✓, matches Ops Notes ✓").

**Change:** SKILL.md communication-style note: one section-transition status line, not a status line after every tool call. Output is the priciest token dimension at $75/M.

Memory `feedback_communication_style.md` already pushes this direction; the skill spec should reinforce it.

## Cumulative target

| | Cost |
|---|---|
| Today (clean batch) | $130-180 |
| After lever 1 (audit fix) | $115-160 |
| After lever 2 (Drive sonnet) | $80-115 |
| After lever 3 (sister consolidation) | $50-85 (offloads 2+) |
| After levers 4-6 (modal sonnet, snapshots, narration) | **$60-100 (clean batch baseline)** |

## Implementation order

1. **Lever 1 first** — pure engineering, zero risk, unblocks faster QA iteration.
2. **Lever 2 next** — biggest single lever, validates the subagent pattern for use elsewhere.
3. **Lever 6 in parallel with 1+2** — pure communication-style change, no engineering.
4. **Lever 3** — compounding gains on multi-offload railcars.
5. **Lever 4** — same subagent pattern as Lever 2, applied to Certify side.
6. **Lever 5** — housekeeping pass once the structural changes settle.

## Generalizable note

The Sonnet-subagent-for-extraction pattern (Levers 2 + 4) isn't batch-qa-specific. Any skill that does mechanical extraction from primary sources before doing judgment work can use the same architecture. Worth documenting once and pointing other skills at it (`skills/qa/site-emissions-qa`, `skills/qa/batch-qa-kerry`, `skills/wellhead-data-transform`).

## Pointers for the new session

- This file: `skills/qa/batch-qa-aecn/COST_DOWN_BACKLOG.md`
- Today's anchor batch: `outputs/qa/batch-2-201/` (token_cost.json, source_reads.json, batch_timestamps.json, build_checklist.py)
- Sister anchor for "clean": `outputs/qa/batch-2-204/`
- Skill main spec: `skills/qa/batch-qa-aecn/SKILL.md`
- Skill checklist structure: `skills/qa/batch-qa-aecn/references/checklist_structure.md`
- Audit script: `skills/qa/batch-qa-aecn/scripts/audit_checklist.py`
- Token cost script: `skills/qa/batch-qa-aecn/scripts/compute_batch_token_cost.py`
