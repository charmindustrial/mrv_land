# MRV Expert — Folder Index

Last updated: 2026-06-29 (added `pdd-changelog` tool under `outputs/mrv-operational-documents/`). The workspace has four parent folders. Every skill, output, reference, and old artifact lives in exactly one of them. New work always lands in a predictable place.

> **Companion file:** `README.txt` at the workspace root is a plain-text version of the same information for quick scanning. **Whenever you change the folder structure, update BOTH this file AND README.txt in the same change.** Out-of-date docs mislead future agents and waste time.

## Top-Level Layout

```
MRV Expert/
├── README.txt         ← plain-text overview (keep in sync with this file)
├── FOLDER_INDEX.md    ← this file (richer markdown version)
├── CLAUDE.md          ← auto-loaded by Claude Code at session start; points to README + this file
├── .claude/skills/    ← Claude Code skill discovery (symlinks to canonical skills under skills/)
├── skills/            ← skill source (SKILL.md + .skill archive + skill-internal references)
├── outputs/           ← everything skills produce (data artifacts, prose deliverables)
├── knowledge-base/    ← shared reference material every skill reads from
└── archive/           ← old drafts, evals, superseded files
```

`.claude/skills/` is how Claude Code discovers this workspace's skills. Each entry is a symlink to the canonical skill folder under `skills/`. Edit the canonical `SKILL.md`, not the symlink. To add a new skill, drop it under `skills/<cluster>/<skill-name>/` and add a matching symlink in `.claude/skills/`.

## skills/ — Skill Source

Each skill folder has a visible `SKILL.md` (the canonical source) and a matching `.skill` archive (the packaged build artifact). Edit SKILL.md, then repackage the .skill.

```
skills/
├── brief-writer/                              ← writes briefs/responses/proposals/QBRs/reportbacks; asks audience first
├── charm-isometric-expert/                    ← knowledge-base librarian / expert
├── lca-model-builder/                         ← embodied emissions / capital goods LCA
├── forestry-biomass-screener/                 ← BFA v1.3 pre-screen + Certify fill for forestry projects
├── rec-eligibility-package/                   ← REC/EAC eligibility package builder (EC1–EC5, Energy Use Accounting v1.3, non-intensive) → Pre-Review Docs Drive folder
├── charm-isometric-expert/
│   ├── SKILL.md                               (the user-facing skill)
│   ├── charm-isometric-expert.skill
│   └── research/                              ← internal citation-methodology sub-skill (not user-triggerable)
│       ├── SKILL.md                           (read-first / verbatim-quote workflow)
│       └── research.skill
├── qa/                                         ← QA cluster
│   ├── batch-qa-aecn/                         (primary QA agent — AECN injection batches; truck and rail delivery modes)
│   ├── batch-qa-kerry/                        (primary QA agent — Kerry bio-oil injection batches; tote and tanker delivery modes)
│   ├── batch-qa-charm/                        (primary QA agent — Charm-produced bio-oil injection batches; WODO and Aqueous oil types)
│   ├── batch-qa-biochar/                      (primary QA agent — biochar removals; Range and Plains Biochar; soil storage; Protocol v1.2 + Soil Environments Module v1.3 — v1.0 checklist, every citation quote-backed)
│   ├── site-emissions-qa/                     (primary QA agent — site/non-batch emissions)
│   ├── adversarial-reviewer/                  (sub-agent — serves all QA primaries)
│   ├── garrett-completion-monitor/            (sub-agent — sweeps all batch-qa registries: AECN, Kerry, Charm)
│   └── performance-monitor/                   (sub-agent — serves all QA primaries)
├── data-analysis/                              ← data analysis cluster
│   └── wellhead-data-transform/               (Ignition SCADA → VVB format + compliance charts)
├── digests/                                    ← cross-team digest cluster
│   └── mrv-standup/                           (daily MRV-relevance sweep across ~33 Slack channels → self-DM)
├── comms/                                      ← external-party communication cluster
│   └── verifier-briefing/                     (proactive briefings to 350Solutions + Isometric; quarterly + pre-verification modes; Gmail draft → Max reviews before send)
└── automation/                                 ← scheduled-automation cluster
    ├── mrv-mailbox/                            (MRV mailbox reconcile cycle: request/remind/intake/route/ledger/Slack; gmail-mrv connection as g_mrv@; runs on macOS launchd)
    ├── kdhe-kora-request/                      (KDHE KORA request builder for Vaulted/Advantek monitoring; reads Vaulted_KDHE_Monitoring_Tracker as the single source of truth; requests only permit-required reports due & not received; drafts request .docx; draft only, Max submits via KORA portal)
    └── charm-350-credit-report/                (daily Charm bio-oil credit-submission report; watches #ext-proj-charm-350-isometric for a "GHG statement submitted" announcement, reads the under-verification statement in Certify READ-ONLY, isolates Charm-produced oil removals QOWV/WODO/Aqueous vs AECN, builds a linked spreadsheet to Drive, sends individual Slack DMs to Max/Garrett/Harris/John; idempotent on statement ID; config.json holds changeable facts; runs on macOS launchd at 15:00 local; NOT a QA process)
```

**QA sub-agents serve all QA primaries.** Today they support `batch-qa-aecn/`, `batch-qa-kerry/`, `batch-qa-charm/`, and `site-emissions-qa/`. As future application-specific QA agents (e.g., for new oil types, new emission categories) are added under `skills/qa/`, the same three sub-agents apply: every primary is subject to adversarial review, gets reported out to Garrett with completion monitoring, and is tracked against performance KPIs.

## outputs/ — What Skills Produce

```
outputs/
├── research/                                   ← findings docs, source lists, Playwright captures from web reads
├── lca-model-builder/                         ← DOT-111 models, BOMs, co-product analyses
├── qa/
│   ├── batch-<batch_id>/                      ← per-batch folder (AECN, Kerry, or Charm); see "QA per-batch layout" below
│   ├── batch-qa/                              ← LEGACY flat folder (Batches 2-162 through 2-185); kept for history, not the destination for new work
│   ├── site-emissions-qa/                     ← Site_Emissions_QA_*.xlsx + session briefs + screenshots/
│   └── performance-monitor/                   ← Claude_QA_Performance_Tracker.xlsx
├── data-analysis/                              ← cross-skill ad-hoc analyses
│   └── wellhead-data-transform/               ← cleaned SCADA, compliance charts, eval reports
├── digests/
│   └── mrv-standup/                           ← run-log.jsonl audit trail (digest itself lives in Slack DM)
├── automation/
│   └── mrv-mailbox/                           ← run-log.jsonl + ledgers/ (per-period reporting ledgers); mailbox cycle, gmail-mrv as g_mrv@
├── comms/
│   └── verifier-briefing/                     ← run-log.jsonl audit trail (drafts live in Gmail, never sent autonomously)
├── deliverables/                               ← finalized EXTERNAL documents only
│   ├── isometric/                             ← Isometric-bound briefs, responses, guidance requests, QBR
│   ├── feedstock-suppliers/                   ← onboarding materials (symlinks to operational-documents)
│   └── mangrove/                              ← Mangrove Systems (accounting-platform vendor): escalations, QBR memos
└── mrv-operational-documents/                  ← finalized INTERNAL Charm documents
    │                                            (feedstock onboarding, conference reportbacks, internal SOPs)
    ├── mrv-mailbox-automation/                 ← MRV mailbox (g_mrv@) automation: intake/routing spec,
    │                                             reporting-period ledger template, monthly request email
    └── pdd-changelog/                          ← PDD change-log tool (pdd_changelog.py) + README; on-demand
                                                  diff vs baseline → Draft rows in the Drive tracker
```

**`mrv-mailbox-automation/`** holds the design for auto-handling ancillary MRV reporting that arrives at g_mrv@charmindustrial.com: `Intake_Routing_Spec.md` (the operating spec — reporters, identification, routing, completion tracking, extensibility), `Reporting_Period_Ledger_TEMPLATE.xlsx` (the per-period tracking sheet, formula-driven status), and `Monthly_Request_Email_Template.md` (the request + reminder messages). Current streams: Community / Wellhead / Oxidizer; scale tickets reserved as a future stream. **Live as of 2026-06-26:** the mail connection (`gmail-mrv` in `.mcp.json`) is authorized as g_mrv@; the executable cycle is the `skills/automation/mrv-mailbox` skill, scheduled via macOS launchd (catches missed runs on wake). Auto-send is enabled with Max-approved copy; first live send July 1, 2026. Filing destinations: Basco MRV (wellhead) / CatOx Data (oxidizer) / Community Engagement; holiday list in `charm_holidays.json`.

**`pdd-changelog/`** holds `pdd_changelog.py` (+ `README.md`), an on-demand tool that diffs the PDD against a saved baseline and appends Draft rows to a standalone change-log tracker. It linearizes paragraphs and table cells, attributes each change to its section/appendix by text pattern, and surfaces only the changed sentences. Commands: `init` (set baseline + create tracker), `log` (diff → report → append Draft rows), `accept` (re-baseline). The baseline snapshot and `PDD_Change_Log.xlsx` live on the Drive mount at `My Drive/MRV/PDDs+Supplemental Docs/PDD Change Log/` (kept out of git to avoid the 2 MB baseline). The tracker feeds — does not replace — the PDD's own Section F.1 narrative and the per-appendix Document Revision tables; Max fills Rationale + Temporary/Permanent on each Draft row.

### QA per-batch layout

Every AECN or Kerry batch QA writes into its own folder at `outputs/qa/batch-<batch_id>/`. Contents:

```
outputs/qa/batch-2-190/
├── Batch_2-190_QA_Checklist.xlsx              ← the deliverable (review document)
├── Batch_2-190_Adversarial_Review.md          ← adversarial-reviewer output
├── batch_2-190_source_reads.json              ← Gate 1 source-document reads
├── batch_timestamps.json                      ← gate-by-gate timing for performance-monitor
├── build_checklist.py                         ← per-batch build script (kept for reproducibility)
├── token_cost.json                            ← per-batch token usage
└── screenshots/                               ← Playwright captures from the QA session (gitignored)
    ├── certify_components.png
    ├── ops_notes_full.png
    └── ...
```

The per-batch folder bundles checklist + adversarial review + source reads + screenshots, so a verifier or future agent can reconstruct the QA session from one location. Screenshots are evidence-pointers (regenerable from a Certify re-pull), so the `screenshots/` subfolder is gitignored — keep the repo lean.

### Routing rules

| Skill | Writes to |
|-------|-----------|
| charm-isometric-expert (research outputs) | `outputs/research/` |
| qa-batch-aecn | `outputs/qa/batch-<batch_id>/` (per-batch folder; e.g., `batch-2-190/`) |
| qa-batch-kerry | `outputs/qa/batch-<batch_id>/` (per-batch folder; same convention) |
| qa-site-emissions (and future site-QA primaries) | `outputs/qa/site-emissions-qa/` |
| adversarial-reviewer | same per-batch folder as the primary it's reviewing |
| garrett-completion-monitor | updates the primary's checklist in place |
| performance-monitor | `outputs/qa/performance-monitor/` |
| lca-model-builder | `outputs/lca-model-builder/` |
| forestry-biomass-screener | `outputs/mrv-operational-documents/` (pre-screen gap reports and Certify fill text) |
| rec-eligibility-package | Drive: `…/Grid Power RECs/Inventory+Docs/Pre-Review Docs/Q{quarter} {region} {year}/` (checklist + certificate + EC4 grid-region evidence; not a local `outputs/` dir) |
| wellhead-data-transform | `outputs/data-analysis/wellhead-data-transform/` |
| mrv-standup | `outputs/digests/mrv-standup/run-log.jsonl` (digest itself posts to Slack self-DM) |
| verifier-briefing | `outputs/comms/verifier-briefing/run-log.jsonl` (drafts live in Gmail; never sent autonomously) |
| mrv-mailbox | `outputs/automation/mrv-mailbox/run-log.jsonl` (ledgers live in Drive period folders; uses gmail-mrv connection as g_mrv@) |
| kdhe-kora-request | Drive `.../Vaulted/KDHE Requests/` (request `.docx` + per-request received-doc subfolders + the monitoring tracker; no local output cluster) |
| charm-350-credit-report | Drive `.../My Drive/Charm Bio-oil Credit Reports/` (per-period `.xlsx`); runtime state in `~/.charm-350-credit-report/` (ledger + run.sh + logs); report sends as Slack DMs |
| brief-writer | `outputs/deliverables/<audience>/` OR `outputs/mrv-operational-documents/` — **must ask the user which audience first** |
| charm-isometric-expert | reads the knowledge base; produces no artifacts of its own |

### Workspace hygiene (hook-enforced)

A PostToolUse hook at [`.claude/hooks/research_citation_guard.sh`](.claude/hooks/research_citation_guard.sh) enforces citation integrity in research outputs. After any `Write` to `outputs/research/` (or any file whose content contains a `## Source List` header), it scans the written text for citation-signal phrases — `§`, `Section N`, `Clause N`, `"states that"`, `"requires that"` — and checks whether each is followed by a verbatim quoted string within ~250 characters. Exits 2 with a specific violation list if any are found, prompting Claude to add the missing quotes before re-attempting the write.

Two **Stop hooks** gate factual integrity in the final response (and text deliverables) when Claude tries to end a turn:

- [`.claude/hooks/citation_integrity_stop.sh`](.claude/hooks/citation_integrity_stop.sh) — every section/clause citation (`§N.N`, `"states that"`, named protocol+version) must carry a verbatim quote that exists in a source read this session.
- [`.claude/hooks/numeric_integrity_stop.sh`](.claude/hooks/numeric_integrity_stop.sh) — every currency/rate/percentage figure must (a) appear in a source read this session, (b) wear an explicit assumption label (`ASSUMPTION` / `PLACEHOLDER` / illustrative / worked example, bound to the figure), or (c) be the checked result of shown arithmetic; every quoted string ≥ 40 chars must exist verbatim in a session-read source; and any `A op B = C` is recomputed and blocked if it doesn't add up. This closes the gap that let an RSB cost estimate ship a fabricated audit day-rate and an un-inflated 2016 figure presented as current. It **cannot** verify that a correctly-labeled number is the *right* number — that is on the author and on the global "No Fabricated Numbers or Facts" rule in `~/.claude/CLAUDE.md`.

Both hard-block (exit 2) with a fix list, and both self-disable after 3 blocks in one session so a false positive can't wedge a turn.

A PreToolUse hook at [`.claude/hooks/local_build_autoapprove.sh`](.claude/hooks/local_build_autoapprove.sh) stops permission prompts while building documents Max asked for, without granting any reach off the machine. It emits `permissionDecision: "allow"` for ONLY two narrow, provably-local cases:

- **Inline python** — a `python3`/`python` command whose code is carried in the command itself (a heredoc `<<` or `-c`), so the hook can scan it, AND that contains no network / shell-escape / external-send pattern (`urllib`, `requests`, `socket`, `smtplib`, `subprocess`, `os.system`, `eval(`, `curl`, `wget`, etc.). File-path runs (`python3 script.py`) are **not** auto-approved — their content is invisible to the hook, so they still prompt.
- **Excel/Word osascript** — an `osascript` command that references only `Microsoft Excel` or `Microsoft Word` (close/save) and nothing else (no `Mail`, `Messages`, `Slack`, browsers, `System Events` keystrokes, or `do shell script`).

Everything else falls through to the normal permission prompt — network-touching python, `curl`/`wget`, osascript to Mail/Slack/browsers — and all external sends (Slack, Gmail, Drive uploads run through MCP tools, which this Bash-only hook never sees). The hook **only ever emits `allow`, never `deny`**, so any other hook's deny still wins. To stay inside the no-prompt path, build documents with inline python heredocs rather than separate script files. Registered as the first `PreToolUse` `Bash` hook in `.claude/settings.json`.

A PreToolUse hook at [`.claude/hooks/workspace_hygiene_guard.sh`](.claude/hooks/workspace_hygiene_guard.sh) prevents loose binary captures and Certify scrapes from accumulating at the workspace root. It denies:

- `mcp__playwright__browser_take_screenshot` calls without a `filename` that routes under `outputs/`.
- `Write` calls targeting `.png` / `.jpg` / `.jpeg` / `.yml` / `.yaml` files at the workspace root.

**Portable by design.** The hook script lives in `.claude/hooks/` and is registered via `.claude/settings.json`; both are tracked in git, so the protection rides with the repo. The hook self-derives the workspace root from its own location (`<workspace>/.claude/hooks/...` → `<workspace>`), so cloning to a new machine "just works" with no global config to set up.

A SessionEnd hook at [`.claude/hooks/browser_cleanup_sessionend.sh`](.claude/hooks/browser_cleanup_sessionend.sh) closes the Playwright browser windows a session opened, so they don't accumulate across sessions (the "why do I have 4 Chromes open" problem). It is **precise, not a blanket kill**: it reads the session's own transcript for which Playwright MCP servers were actually used, maps each to its profile directory (`playwright` → `playwright-profile`, `playwright-mrv-2` → `playwright-profile-mrv-2`, etc.), and closes only those exact windows via `pkill` on the `--user-data-dir` path. A window opened by a different, still-running session (different profile) is never touched; a session that used no browser closes nothing. **Fail-open:** any error exits 0 without acting, so it can only ever close a leftover window, never brick a session. It runs at session end, not between turns, so a browser being used mid-task is never killed.

`.claude/skills/` stays gitignored because those entries are machine-specific absolute-path symlinks. Recreate them on a new machine with `ln -s ../../skills/<cluster>/<skill> .claude/skills/<skill>` for each skill (or whatever discovery setup exists at the time).

If a screenshot is genuinely needed elsewhere (e.g., evidence shipped with a brief in `outputs/deliverables/...`), use that path — anything under `outputs/` passes the hook.

### Audience rules for written work

`outputs/deliverables/` is for finalized **external** documents only. Audience subfolders inside it identify the recipient:
- `outputs/deliverables/isometric/` — anything bound for Isometric (briefs, responses, guidance requests, QBR briefs)
- `outputs/deliverables/mangrove/` — anything bound for Mangrove Systems (the accounting-platform vendor): escalations, QBR memos
- additional audience subfolders get added as needed (regulators, other verifiers, conferences if external-facing)

`outputs/mrv-operational-documents/` is for finalized **internal** Charm documents:
- Internal SOPs, checklists, onboarding documents
- Internal reportbacks (e.g., conference takeaways summarized for the Charm team)

**The brief-writer skill must explicitly ask the user which audience a brief is for** if there is any ambiguity, because audience drives both the composition (tone, framing, level of detail) and the storage destination.

### Dual-purpose documents

Some documents serve as both internal operational docs AND external deliverables. The feedstock onboarding checklist is the canonical example — Charm uses it internally to manage onboarding AND ships it to suppliers as part of that process. **Convention:**

1. File the canonical copy in `outputs/mrv-operational-documents/`
2. Place a symlink at `outputs/deliverables/<audience>/` pointing back to the canonical, so edits in one place stay in sync everywhere.

This keeps a single source of truth while making the file reachable from the audience-organized side too.

## knowledge-base/ — Shared Reference

Every skill reads from here. Files at the root, plus historical PDFs in a sub-folder.

```
knowledge-base/
├── Charm_PDD_v1.12_Bio_Oil_Geologic_Storage_Biochar.docx   ← AUTHORITATIVE — v1.12, supersedes earlier PDD versions
├── Charm_Isometric_Knowledge_Base.md                       ← the institutional knowledge document
├── Certify_Deep_Dive_Findings.md
├── Charm_CDR_Protocol_Summary.docx
├── ACS_Vaulted_KDHE_Permit_KS-05-155-002_SIGNED.pdf        ← AUTHORITATIVE — KDHE Class V UIC permit
│                                                              for Vaulted (Advantek), eff. 6/5/2024–6/5/2034.
│                                                              The source the KDHE monitoring tracker +
│                                                              kdhe-kora-request skill derive from.
├── Isometric_Standard_v2.0_vs_v1.9_Comparison.md
├── category_evidence_guide_v2.md
├── MRV_Uncertainty_Evidence_Cheat_Sheet.xlsx
├── isometric-findings-stats.xlsx                           ← failure-mode analysis of Isometric findings
│                                                              (ISS-16 through ISS-30): bucketed as Legitimate /
│                                                              Misunderstanding / Pending FAR, with root-cause
│                                                              grouping (EF versioning, BCU quant mismatch,
│                                                              component evidence, etc.). QA skills consult this
│                                                              to know what verifiers are flagging.
├── biochar_protocol_v1.2.txt                               ← plain-text scrapes of Isometric protocol /
├── soil_module_v1.3.txt                                       module registry pages, kept for fast text
├── book_and_claim_module_v1.txt                               search alongside the PDFs in isometric-pdfs/.
├── ghg_accounting_v1.1_allocation_text.txt                    Moved here from the workspace root 2026-07-23.
├── ghg_accounting_v1.1_allocation_text_p2.txt
├── lowox_clean.txt
├── lowox_module.txt
├── saba_atmospheric_benefit_tool.txt
├── v19_standard_snapshot.md                                ← full-text snapshot of Isometric Standard v1.9
├── pdd_full.txt                                            ← plain-text extraction of the v1.12 PDD .docx;
│                                                              part of the batch-qa-biochar build_checklist.py
│                                                              quote-verification corpus. Regenerate from the
│                                                              .docx if the PDD changes.
└── isometric-pdfs/                                          ← verification reports, GHG statements,
    │                                                           Isometric protocol modules, older PDD (file 22)
    └── Outdated Modules/                                    ← superseded module versions, preserved
```

The v1.12 PDD at the root is the canonical Project Design Document. Earlier versions (including `isometric-pdfs/22_2025-02-20_pdd.pdf`) are kept for historical reference only.

**Isometric module versioning.** Module PDFs are checked against the live Isometric registry. Current as of 2026-06-22: GHG Accounting **v1.1**, Energy Use Accounting **v1.3**, Bio-oil Geological Storage **v1.2**; BFA v1.3 and Transportation Emissions Accounting v1.1 confirmed current. When a newer version is pulled in, the superseded version is moved to `isometric-pdfs/Outdated Modules/` (never deleted). Being superseded does **not** mean Charm has adopted the new version — both are retained so a project can cite whichever version actually governs it.

## archive/ — Superseded / Deprecated

Old eval outputs, draft SKILL.md versions, retired update files, and prior brief-writer experiments. Not authoritative — kept for reference only.

```
archive/
├── brief-writer-eval-outputs/                  (reference for building the new brief-writer skill)
├── brief-writer-eval-v2/                       (same)
├── mrv-brief-writer-eval-review.html
├── mrv-brief-writer-eval-v2.html
├── lca-model-builder-SKILL-v17-update.md       (superseded by current SKILL.md)
├── lca-model-builder-update.skill              (superseded by current .skill archive)
├── SKILL_draft.md                              (site-emissions-qa draft, superseded)
├── Site_Emissions_QA_Template_draft.xlsx
├── screenshots/                                (Jira service-desk + GCP setup screenshots, May 2026; moved from workspace root 2026-07-23)
├── book_and_claim_module_v1_scrape_2026-06-30.txt  (superseded by the 2026-07-17 scrape now in knowledge-base/)
└── Runbear Receipts/                           (single empty upload log from June 2026; moved from workspace root 2026-07-23)
```

## Conventions for Adding New Work

**New skill:** create `skills/<cluster>/<skill-name>/` with `SKILL.md` (source) and `<skill-name>.skill` (packaged archive). If the skill produces artifacts, also create `outputs/<cluster>/<skill-name>/` as its output destination. Update this file.

**New output cluster (e.g., a new analysis subskill):** add it under the appropriate parent in `outputs/`. Mirror the structure with a sibling skill folder under `skills/`.

**New audience:** add a subfolder under `outputs/deliverables/` (external) or extend `outputs/mrv-operational-documents/` (internal). Update the brief-writer skill so it surfaces the new audience option to the user.

**Path references in SKILL.md:** prefer the explicit path under the workspace folder (e.g., `knowledge-base/Charm_Isometric_Knowledge_Base.md`) over vague language. The skill engine can find files via search either way, but explicit paths are faster and self-documenting.

**Whenever the structure changes, update both `README.txt` and `FOLDER_INDEX.md` in the same change.** No exceptions. Out-of-date docs mislead future agents and waste time.

## Outstanding Work

- **Resolve `#co` channel ID for mrv-standup registry.** Max requested it but no exact match exists in the channel index (only `#colorado-ski-snowboard` came back). On first run of the standup, ask Max which channel he meant and update `skills/digests/mrv-standup/SKILL.md`.
- **Extract shared root from `batch-qa-aecn` / `batch-qa-kerry` / `batch-qa-charm`.** The three batch-QA skills share ~70% of their structure (pre-flight gate, 4-gate workflow, Slack workflow, formatting spec, citation discipline, anti-patterns, key principles, working-with-Max). Each currently duplicates this scaffolding inline. Pulling the common spine into a `skills/qa/_batch-qa-common/` shared reference doc (or a root SKILL.md included by each branch) would remove the drift risk that already exists across the three — e.g., the Slack workflow's siren-emoji prefix rule was added to AECN/Kerry independently after the rule was introduced for AECN. Deferred from the 2026-05-12 Charm-skill build because it touches all three working skills.

## Recently Resolved (2026-07-23)

- **Workspace root cleanup.** 22 setup screenshots (Jira service desk + GCP, May 2026) moved to `archive/screenshots/`. Nine plain-text protocol/module scrapes moved to `knowledge-base/`. Of the two Book and Claim scrapes (both module v1.0), the newer 2026-07-17 one was kept as `knowledge-base/book_and_claim_module_v1.txt` and the 2026-06-30 one archived. `Runbear Receipts/` (one empty log file) archived. `.DS_Store` and two stale Office lock files deleted. `.playwright-mcp/` browser-download cache emptied (261 MB, ~4,000 files) — those were working downloads from QA sessions; the authoritative copies live in Drive. One file in that cache, `pdd_full.txt`, was load-bearing: `skills/qa/batch-qa-biochar/build_checklist.py` read it as part of its quote-verification corpus. It was regenerated from the authoritative `Charm_PDD_v1.12_...docx` into `knowledge-base/pdd_full.txt`, and the script's three source paths were re-pointed at `knowledge-base/`. The biochar checklist build was re-run and verifies clean (46 cited rows).

## Recently Resolved (2026-05-15)

- **Added `research/` citation-methodology sub-skill inside `charm-isometric-expert/`.** `skills/charm-isometric-expert/research/SKILL.md` defines the read-first / verbatim-quote / synthesize-last workflow for external document claims. Not user-triggerable — it is the citation discipline that `charm-isometric-expert` follows internally. `charm-isometric-expert/SKILL.md` now has a "Citation Standard" section that summarizes the rule and points to the sub-skill for the full workflow. Backed by `research_citation_guard.sh` (PostToolUse hook on Write) that flags citation-signal phrases without adjacent quoted text in written research outputs under `outputs/research/`.

## Recently Resolved (2026-05-06)

- **Built the `mrv-standup` skill in a new `digests/` cluster.** Daily weekday sweep of ~33 Charm + Isometric Slack channels (MRV core, verifier-facing, and adjacent/cross-team), tiered into Watch/FYI/Drop, posted to Max's self-DM. Designed to be invoked by a scheduled remote agent at 6:30am PT on weekday mornings; also runs ad-hoc. Channel registry and filter rules live in `skills/digests/mrv-standup/SKILL.md` (the version-controlled spec — calibration happens by editing the SKILL.md, not a separate config).

## Recently Resolved (2026-05-05)

- **Workspace hygiene cleanup.** Loose Playwright screenshots and Certify YAML scrapes (~36 files at the workspace root, accumulated across 2-186 / 2-188 / 2-190 QA sessions) moved into per-batch `outputs/qa/batch-<batch_id>/screenshots/` folders. Stragglers archived.
- **Per-batch QA folder convention documented.** AECN and Kerry batch QA now write to `outputs/qa/batch-<batch_id>/` (was previously documented as flat `outputs/qa/batch-qa/`). The legacy flat folder is kept for history (batches 2-162 through 2-185).
- **Added `workspace_hygiene_guard.sh` PreToolUse hook.** Denies Playwright screenshots and Write calls that would land .png/.yml at the workspace root. Hook lives in `.claude/hooks/` (tracked in git, rides with the repo, self-derives workspace path — portable to new machines with no setup).
- **Resolved duplicate `deliverables/` folder.** Top-level `deliverables/` (a leftover from before the `outputs/` reorganization) emptied and removed. The only deliverables folder is now `outputs/deliverables/` as the README always specified.
- **`.gitignore` updated** to ignore `.playwright-mcp/`, `outputs/**/screenshots/`, and root-level .png/.jpg/.yml/.yaml as a backstop to the hook.

## Recently Resolved (2026-04-24)

- **Built the brief-writer skill.** `skills/brief-writer/` now contains a full SKILL.md and packaged `.skill` archive. The skill asks audience and brief type up front via AskUserQuestion, reads from `knowledge-base/`, references prior brief patterns, and routes output to the correct `outputs/deliverables/<audience>/` or `outputs/mrv-operational-documents/` folder.
- **Renamed feedstock files for clarity.** `New_Feedstock_Oil_Source_Onboarding_Checklist.xlsx` → `Feedstock_Oil_Source_Process_Checklist.xlsx`. `New_Feedstock_Onboarding_Checklist.xlsx` → `Feedstock_Supplier_Onboarding_Template.xlsx`. Symlinks in `outputs/deliverables/feedstock-suppliers/` updated to match. The two files are distinct artifacts — process checklist (with reference index) vs. template (with filled supplier instances) — and intentionally kept separate.
