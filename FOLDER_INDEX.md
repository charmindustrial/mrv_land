# MRV Expert — Folder Index

Last updated: 2026-10-16 (QA moved off Playwright — Certify and Drive are read through APIs by `skills/qa/container/tools/`; added `skills/qa/container/` to run the QA skills in GCP; see "Recently Resolved (2026-10-16)"). Previously: 2026-10-13 (third full workspace clean-up; added `automation/workspace-tidy`, a weekly scheduled sweep (Mondays 07:00 Pacific, through `~/.claude/scheduled/`) that keeps the root clean and saves + pushes the folder to GitHub; widened `workspace_hygiene_guard.sh` to block every new root file, not just images/YAML; fixed the GitHub backup hook, which had silently failed since 2026-04-29 — see "Recently Resolved (2026-10-13)"). Previously: 2026-10-01 (RETIRED `automation/resume-echo-review` at Max's request: launchd job unloaded, plist moved to `~/.claude/scheduled/plist-backups/retired/`, cloud routine `resume-echo-artifact-publish` disabled, `.claude/skills` symlink removed; skill folder, registry and audit trail kept as a record. All scheduled jobs now run through `~/.claude/scheduled/` — see its README.md). Previously: 2026-09-13 (added `skills/orchestrator-mode` — interactive "boss" mode that turns a Claude Code window into a coordinator planning/delegating/unblocking other "worker" windows without editing anything itself; NOT a scheduled automation, invoked by hand; boss window must be switched to the Fable model at low reasoning effort via `/model`; worker count is task-dependent, never fixed in advance; see the skill's SKILL.md for the full procedure). Previously: 2026-09-03 (added `automation/resume-echo-review` — twice-daily applicant screen for the open MRV Analyst Lever posting, building on the one-time manual "Resume Echo Audit." Fired 9am/17:00 by launchd; also runs ad-hoc. STRICTLY READ-ONLY on Lever and LinkedIn — `~/.claude/hooks/certify_readonly_guard.sh` hard-blocks writes to `hire.lever.co` the same way it does `registry.isometric.com`. Persistent candidate verdicts in `skills/automation/resume-echo-review/candidate_registry.json` (git-tracked, like the QA batch registries); audit trail in `outputs/automation/resume-echo-review/`; alerts via a macOS desktop notification, deliberately never Slack — see the skill's SKILL.md). Previously: 2026-09-02 (retired `automation/mrv-mailbox` — email-based RP-close ancillary data request, paused since 2026-06-30 and never resumed — moved to `archive/mrv-mailbox-superseded/`; replaced by `automation/ancillary-data-request`, a Slack-based version posting the monthly asks in #mrv-ops-la and alerting finished products to #team-mrv-alerts. Not yet live: AUTO_POST_APPROVED is false pending Max's go-ahead on the first post). The workspace has four parent folders. Every skill, output, reference, and old artifact lives in exactly one of them. New work always lands in a predictable place.

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
├── orchestrator-mode/                          ← interactive "boss" mode for coordinating multiple Claude Code sessions; NOT a scheduled automation — Max invokes it by hand. Boss window (Fable model, low reasoning effort, set via /model) plans, spawns and delegates pieces directly to "teammate" sessions (ListAgents/SendMessage) or in-session helpers (Agent tool), unblocks them, and winds a teammate down (TaskStop) the instant its piece is done — never edits files or changes state itself. Depends on the one-time global setting CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in ~/.claude/settings.json (added 2026-09-13). Teammate count is task-dependent, decided fresh each time; session resume does not bring teammates back. Origin: 2026-09-11 Slack conversation with Brian Jamieson.
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
│   ├── batch-qa-biochar/                      (primary QA agent — biochar removals; Range and Plains Biochar; agricultural-soil storage. **Governing versions, read from Certify 2026-07-29: Biochar Production and Storage Protocol v1.0 — both baseline and current — plus Biochar Storage in Agricultural Soils Module v1.0, on Isometric Standard v1.7.** The registry's latest, Protocol v1.3 / Standard v2.1, is not adopted here. `Biochar_Removal_QA_Schema_v2.0.xlsx` is the current schema: 8 tabs — How to use, Mass Basis Ladder, **Recorded Reference Values**, Per-Removal Checks (61 checks / 8 sections), Batch-Level Checks (19 cross-removal), Datapoint Evidence Map (16 Certify datapoints), Findings Log (CAR/CL), Sources. Recorded Reference Values holds what was actually read out of Certify and the delivery-notes workbook on 2026-07-29 **with values**, so every check is a comparison against a recorded fact rather than an instruction to go read a source — refresh that tab each round, never carry stale values forward. All 55 citation quotes machine-verified against session-read sources and all 23 arithmetic claims recomputed. `Biochar_Removal_QA_Checklist_Template.xlsx` v1.0 is **superseded** — it cites v1.2/v1.3 section numbers that don't match the registered version and asserts a 0% buffer pool where the governing module sets 2%; `build_checklist.py` builds that superseded template, not v2.0)
│   ├── site-emissions-qa/                     (primary QA agent — site/non-batch emissions)
│   ├── adversarial-reviewer/                  (sub-agent — serves all QA primaries)
│   ├── garrett-completion-monitor/            (sub-agent — sweeps all batch-qa registries: AECN, Kerry, Charm)
│   ├── performance-monitor/                   (sub-agent — serves all QA primaries)
│   └── container/                             (not a skill — runs the QA skills in GCP: Cloud Run job `qa-runner` in `charm-mrv`, started by an operator via `qa_run.sh` or the `qa-trigger` endpoint; Certify and Drive read through the API; never sends Slack/Gmail. See `container/README.md` and `container/CONTAINER_MODE.md`)
├── data-analysis/                              ← data analysis cluster
│   └── wellhead-data-transform/               (Ignition SCADA → VVB format + compliance charts)
├── digests/                                    ← cross-team digest cluster
│   └── mrv-standup/                           (daily MRV-relevance sweep across ~33 Slack channels → #team-mrv-alerts, never a DM)
└── automation/                                 ← scheduled-automation cluster
    ├── resume-echo-review/                     (RETIRED 2026-10-01, no longer scheduled. Was: twice-daily applicant screen for the open "MRV Analyst" Lever posting, building on the one-time manual "Resume Echo Audit" (2026-09-03). Reads every candidate in Lever's "New applicant" stage; new ones go through Gate 1 — resume copies posting/materials language, or the candidate's own LinkedIn contradicts the resume, either disqualifies, no exceptions — then, if clean, Gate 2 — any MRV/carbon-accounting/ESG/LCA/related sustainability experience or degree, not disqualifying, just sets review priority. Updates the persistent artifact and `candidate_registry.json`, drops any candidate whose Lever stage has moved off "New applicant" since the last pass, and alerts Max via a macOS desktop notification — deliberately NOT Slack, see SKILL.md's "Why desktop notification, not Slack." Read-only on Lever and LinkedIn — `~/.claude/hooks/certify_readonly_guard.sh` hard-blocks writes to `hire.lever.co` the same way it does `registry.isometric.com`. Fired by macOS launchd daily at 9:00 and 17:00 local; also runs ad-hoc. Registry + config live in the skill folder, git-tracked like the QA batch registries; run.sh/logs/temp files in `~/.resume-echo-review/`.)
    ├── ancillary-data-request/                 (RP-close reconcile cycle for the three cross-functional ancillary data streams — Community/Alison, Wellhead/Casey, Oxidizer/Evan. 1st of the month: three separate tagged asks posted as top-level messages in #mrv-ops-la, each expecting a threaded reply with a link to the prior month's data. Every run — fired every 3 hours — scans each thread for a qualifying reply from the tagged reporter, routes Wellhead → wellhead-data-transform and Oxidizer → tox-sparging-analysis for processing (Community files as submitted, no processing), uploads the finished product to the Processed Ancillary Data Drafts Drive folder, and alerts Garrett + Max in #team-mrv-alerts per item — noting when the period's last item lands. Stops there — human review + the final drop into the reporting package folder are Max's/Garrett's step. AUTO_POST_APPROVED gate in references/config.json controls whether the monthly asks actually send; runs on macOS launchd. Replaces the retired mrv-mailbox automation as of 2026-09-02 — see archive/mrv-mailbox-superseded/.)
    ├── kdhe-kora-request/                      (KDHE KORA request builder for Vaulted/Advantek monitoring; reads Vaulted_KDHE_Monitoring_Tracker as the single source of truth; requests only permit-required reports due & not received; drafts request .docx; draft only, Max submits via KORA portal)
    ├── charm-350-credit-report/                (daily Charm bio-oil credit-submission report; watches #ext-proj-charm-350-isometric for a "GHG statement submitted" announcement, reads the under-verification statement in Certify READ-ONLY, lists every removal grouped by oil source (Charm-produced QOWV/WODO/Aqueous, AECN, Kerry) with subtotals and a grand total, builds a linked spreadsheet to Drive, sends individual Slack DMs to Max/Garrett/Harris/John; idempotent on statement ID; config.json holds changeable facts; runs on macOS launchd at 15:00 local; NOT a QA process)
    ├── eac-inventory-monitor/                  (daily BCU + REC headroom check on the "Charm EAC Verification Inventory tracker" Sheet; STRICTLY READ-ONLY on the sheet; BCU Inventory tab "Total Attributes Remaining" alerts below 200, RECs Inventory tab "Volume Remaining" alerts below 50; skips every row the sheet has HIDDEN — hidden = expired or fully drawn down — plus any still-visible REC row past its Expiry Date; reads row visibility straight from the Sheets API via the shared max@ token at ~/.basco-intake/token.json rather than guessing; posts ONE alert to #team-mrv-alerts tagging Max when low, silent otherwise; thresholds/IDs in config.json; runs on macOS launchd at 08:00 local)
    ├── aecn-lca-processor/                     (processes a new half-yearly AECN carbon-intensity LCA submission from J-C Amado, j-c@viridiglobal.com, into Drive: archives the old `LCA -- [BH/FH] [year] Data` folder to Deprecated/, builds the new one, pulls the two attached workbooks from the email, runs a MANDATORY reconciliation of the raw Supporting Data against the LCA calc's own stated totals before anything downstream uses the number, fills the Stack Emissions Template — CI value is the no-allocation Total, i.e. net of the coproduct-displacement credit Charm's accounting policy doesn't count — and pushes the result into the live "Standard Emission Factors + Calculations" Sheet that batch-qa-aecn reads from. Manually triggered — nothing watches Max's inbox for this. Validated end-to-end against the real H1 2026 submission 2026-08-26, which also surfaced a real gap: the sheet's AECN tab had been renamed ahead of the data landing, leaving it mislabeled with stale contents.)
    ├── pace-report-generate/                   (weekly MRV Pace Report generator; copies the Drive template, names it for the following day (Thursday), carries each person's "Top 3 I'll Focus On Next Week" items from the current live report into "Last Week's Focus - Did It Land" on the matching tab of the new one — Max stays with Max, Garrett stays with Garrett — then posts the link to #team-mrv asking the team to fill out their section; config.json holds channel/folder IDs; runs on macOS launchd Wednesdays at 15:00 local; hands off to pace-report-finalize)
    ├── workspace-tidy/                         (weekly clean-up of this folder + GitHub backup check. `tidy.py --apply` deletes known junk (guard-script `<property object…>` files, empty root folders, stale Office lock files, browser captures past 7/30 days), MOVES anything else unknown at the root to `archive/root-sweep/<date>/` and output folders found inside `skills/` to `archive/misrouted/<date>/` — never deletes possible work — then commits and pushes to GitHub and fails if GitHub is still behind. Scheduled job `workspace-tidy` in `~/.claude/scheduled/`, Mondays 07:00 Pacific; a Claude job, not a plain script, because macOS blocks launchd-started scripts from touching ~/Desktop. Also runs ad-hoc: "tidy the workspace".)
    └── pace-report-finalize/                   (completion watcher for MRV Pace Report threads; sweeps every pending cycle left by pace-report-generate, and for each one checks #team-mrv for a reply signaling the team is done — flexible phrase matching, any team member; on completion, moves the superseded report into the Deprecated subfolder and posts the new report as a hyperlinked "MRV Pace" message to #team-strategery; self-healing via state.json, no per-cycle scheduled task needed; runs on macOS launchd weekdays ~9:00/12:00/15:00/18:00 local)
```

**QA sub-agents serve all QA primaries.** Today they support `batch-qa-aecn/`, `batch-qa-kerry/`, `batch-qa-charm/`, and `site-emissions-qa/`. As future application-specific QA agents (e.g., for new oil types, new emission categories) are added under `skills/qa/`, the same three sub-agents apply: every primary is subject to adversarial review, gets reported out to Garrett with completion monitoring, and is tracked against performance KPIs.

## outputs/ — What Skills Produce

```
outputs/
├── research/                                   ← findings docs, source lists, saved page text from web reads
├── lca-model-builder/                         ← DOT-111 models, BOMs, co-product analyses
├── qa/
│   ├── batch-<batch_id>/                      ← per-batch folder (AECN, Kerry, or Charm); see "QA per-batch layout" below
│   ├── batch-qa/                              ← LEGACY flat folder (Batches 2-162 through 2-185); kept for history, not the destination for new work
│   ├── site-emissions-qa/                     ← Site_Emissions_QA_*.xlsx + session briefs + screenshots/
│   └── performance-monitor/                   ← Claude_QA_Performance_Tracker.xlsx
├── data-analysis/                              ← cross-skill ad-hoc analyses
│   └── wellhead-data-transform/               ← cleaned SCADA, compliance charts, eval reports
├── digests/
│   └── mrv-standup/                           ← run-log.jsonl audit trail (digest itself posts to #team-mrv-alerts)
├── automation/
│   ├── resume-echo-review/                    ← run-log.jsonl audit trail (new/removed candidates, run summaries); candidate verdicts live in skills/automation/resume-echo-review/candidate_registry.json — git-tracked business data, not throwaway runtime state, same treatment as the QA batch registries under skills/qa/
│   ├── workspace-tidy/                        ← run-log.jsonl: what each weekly sweep deleted and moved
│   └── ancillary-data-request/                ← run-log.jsonl audit trail; the per-period ledger lives at ~/.ancillary-data-request/ledgers/ (runtime state, like the other launchd-fired automations), not here
├── deliverables/                               ← finalized EXTERNAL documents only
│   ├── isometric/                             ← Isometric-bound briefs, responses, guidance requests, QBR
│   ├── feedstock-suppliers/                   ← onboarding materials (symlinks to operational-documents)
│   ├── mangrove/                              ← Mangrove Systems (accounting-platform vendor): escalations, QBR memos
│   ├── saf-diligence/                         ← anyone doing external diligence on Charm's SAF methodology
│                                                  (prospective buyers, 123 Carbon, methodology developers)
│   └── relae-diligence/                       ← Charm's response to Relae's MMRV diligence questions for the Salesforce bio-oil offtake (October 2026)
└── mrv-operational-documents/                  ← finalized INTERNAL Charm documents
    │                                            (feedstock onboarding, conference reportbacks, internal SOPs)
    └── pdd-changelog/                          ← PDD change-log tool (pdd_changelog.py) + README; on-demand
                                                  diff vs baseline → Draft rows in the Drive tracker
```

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
└── screenshots/                               ← captures from older browser-based QA runs (gitignored)
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
| mrv-standup | `outputs/digests/mrv-standup/run-log.jsonl` (digest itself posts to #team-mrv-alerts) |
| resume-echo-review (RETIRED 2026-10-01) | `outputs/automation/resume-echo-review/run-log.jsonl`; candidate verdicts in `skills/automation/resume-echo-review/candidate_registry.json`; report is the published "Resume Echo Audit" artifact; alerts via macOS desktop notification only, never Slack |
| ancillary-data-request | `outputs/automation/ancillary-data-request/run-log.jsonl`; runtime state + per-period ledger in `~/.ancillary-data-request/` (`references/config.json` for IDs, `ledgers/` for state); asks post in `#mrv-ops-la`, alerts post in `#team-mrv-alerts`, finished products upload to the Processed Ancillary Data Drafts Drive folder |
| kdhe-kora-request | Drive `.../Vaulted/KDHE Requests/` (request `.docx` + per-request received-doc subfolders + the monitoring tracker; no local output cluster) |
| charm-350-credit-report | Drive `.../My Drive/Charm Bio-oil Credit Reports/` (per-period `.xlsx`); runtime state in `~/.charm-350-credit-report/` (ledger + run.sh + logs); report sends as Slack DMs |
| eac-inventory-monitor | no file outputs (read-only check); runtime state in `~/.eac-inventory-monitor/` (`config.json`, `check_eac_inventory.py`, `run.sh`, logs); only output is a Slack alert to `#team-mrv-alerts` when an inventory is low |
| aecn-lca-processor | Drive: `.../AECN/LCAs/` (new period folder + `Deprecated/` archive of the old one); also edits the live "Standard Emission Factors + Calculations" Sheet (a separate file, found by search — not a fixed path). No local `outputs/` dir. Manual trigger only. |
| pace-report-generate | Drive: `.../MRV/Team/OKRs + Pace Reports/2026/Pace Reports/` (new weekly `.xlsx`); runtime state in `~/.pace-report/` (`state.json` pending-cycles list, generate-run.sh, logs); posts to `#team-mrv`. Fired by launchd Wednesdays 15:00 local. |
| pace-report-finalize | No file outputs of its own — moves the prior week's `.xlsx` into that folder's `Deprecated/Past` subfolder and posts to `#team-strategery`; shares `~/.pace-report/state.json` with pace-report-generate. Fired by launchd weekdays ~9/12/15/18:00 local. |
| workspace-tidy | `outputs/automation/workspace-tidy/run-log.jsonl`; moved items go to `archive/root-sweep/<date>/` and `archive/misrouted/<date>/`; commits + pushes to GitHub. Fired Mondays 07:00 Pacific via `~/.claude/scheduled/`. |
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

- `Write` calls targeting `.png` / `.jpg` / `.jpeg` / `.yml` / `.yaml` files at the workspace root.
- `Write` calls creating any other file at the workspace root except `CLAUDE.md`, `README.txt`, `FOLDER_INDEX.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (added 2026-10-13: protocol scrapes and page-text dumps kept landing there as `.txt`).

Files written by scripts or other programs never pass through this hook; the weekly `workspace-tidy` sweep catches those.

**Portable by design.** The hook script lives in `.claude/hooks/` and is registered via `.claude/settings.json`; both are tracked in git, so the protection rides with the repo. The hook self-derives the workspace root from its own location (`<workspace>/.claude/hooks/...` → `<workspace>`), so cloning to a new machine "just works" with no global config to set up.

The SessionEnd hook [`.claude/hooks/browser_cleanup_sessionend.sh`](.claude/hooks/browser_cleanup_sessionend.sh) (closed the Playwright windows a session opened) is **no longer registered** in `.claude/settings.json`: QA reads Certify and Drive through APIs (`skills/qa/container/tools/`), so sessions open no browser. The script is kept for reference.

`.claude/skills/` stays gitignored because those entries are machine-specific absolute-path symlinks. Recreate them on a new machine with `ln -s ../../skills/<cluster>/<skill> .claude/skills/<skill>` for each skill (or whatever discovery setup exists at the time).

If a screenshot is genuinely needed elsewhere (e.g., evidence shipped with a brief in `outputs/deliverables/...`), use that path — anything under `outputs/` passes the hook.

### Audience rules for written work

`outputs/deliverables/` is for finalized **external** documents only. Audience subfolders inside it identify the recipient:
- `outputs/deliverables/isometric/` — anything bound for Isometric (briefs, responses, guidance requests, QBR briefs)
- `outputs/deliverables/mangrove/` — anything bound for Mangrove Systems (the accounting-platform vendor): escalations, QBR memos
- `outputs/deliverables/saf-diligence/` — anyone doing external diligence on Charm's SAF methodology (no single named party — covers prospective buyers, 123 Carbon, and prospective third-party methodology developers)
- `outputs/deliverables/relae-diligence/` — Charm's response to Relae's MMRV diligence questions for the Salesforce bio-oil offtake (October 2026)
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
├── biochar_storage_ag_soils_v1.0.txt                       ← Biochar Storage in Agricultural Soils
│                                                              Module **v1.0** full text, scraped from the
│                                                              registry 2026-07-29. The storage module the
│                                                              biochar project is actually registered
│                                                              against (Protocol v1.0 §8.1 names it by
│                                                              version), so this — not soil_module_v1.3.txt
│                                                              — is the citation source for biochar QA.
│                                                              Protocol companion text lives at
│                                                              outputs/research/biochar_protocol_v1.0_registry.txt
├── biochar_protocol_v1.2.txt                               ← plain-text scrapes of Isometric protocol /
├── soil_module_v1.3.txt                                       module registry pages, kept for fast text
├── book_and_claim_module_v1.txt                               search alongside the PDFs in isometric-pdfs/.
├── ghg_accounting_v1.1_allocation_text.txt                    Moved here from the workspace root 2026-07-23.
├── ghg_accounting_v1.1_allocation_text_p2.txt
├── lowox_clean.txt
├── lowox_module.txt
├── saba_atmospheric_benefit_tool.txt
├── v19_standard_snapshot.md                                ← full-text snapshot of Isometric Standard v1.9
├── isometric_standard_v1.9.txt                             ← registry page text of Isometric Standard v1.9 /
├── isometric_standard_v2.0.txt                                v2.0 / v2.1, GHG Accounting v1.1 (full) and
├── isometric_standard_v2.1.txt                                Bio-oil Geological Storage v1.2, scraped
├── ghg_accounting_v1.1_full.txt                               2026-07-28 to 2026-08-24. Moved here from the
├── bio_oil_geological_storage_v1.2.txt                        workspace root 2026-10-13 (was bogs_page.txt etc.)
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
├── Runbear Receipts/                           (single empty upload log from June 2026; moved from workspace root 2026-07-23)
├── deliverable-backups/isometric/              (working "_backup_" copies of Tier 0/1/2 PDD files made before edits, Sept–Oct 2026; moved out of outputs/deliverables/isometric/ 2026-10-13)
├── superseded-versions/isometric/              (older numbered versions of the RSB/ISCC deck (v1–v9) and PDD v1.12 Coverage Inventory (v1–v6); the current one stays in outputs/deliverables/isometric/)
├── misrouted/<date>/                           (output folders the weekly tidy found inside skills/, kept with their original path)
└── root-sweep/<date>/                          (anything the weekly tidy found loose at the workspace root)
```

## Conventions for Adding New Work

**New skill:** create `skills/<cluster>/<skill-name>/` with `SKILL.md` (source) and `<skill-name>.skill` (packaged archive). If the skill produces artifacts, also create `outputs/<cluster>/<skill-name>/` as its output destination. Update this file.

**New output cluster (e.g., a new analysis subskill):** add it under the appropriate parent in `outputs/`. Mirror the structure with a sibling skill folder under `skills/`.

**New audience:** add a subfolder under `outputs/deliverables/` (external) or extend `outputs/mrv-operational-documents/` (internal). Update the brief-writer skill so it surfaces the new audience option to the user.

**Path references in SKILL.md:** prefer the explicit path under the workspace folder (e.g., `knowledge-base/Charm_Isometric_Knowledge_Base.md`) over vague language. The skill engine can find files via search either way, but explicit paths are faster and self-documenting.

**Whenever the structure changes, update both `README.txt` and `FOLDER_INDEX.md` in the same change.** No exceptions. Out-of-date docs mislead future agents and waste time.

## Outstanding Work

- **Resolve `#co` channel ID for mrv-standup registry.** No exact match exists in the channel index (only `#colorado-ski-snowboard` came back). The standup skips it until a channel ID is identified and added to `skills/digests/mrv-standup/SKILL.md`.
- **Extract shared root from `batch-qa-aecn` / `batch-qa-kerry` / `batch-qa-charm`.** The three batch-QA skills share ~70% of their structure (pre-flight gate, 4-gate workflow, Slack workflow, formatting spec, citation discipline, anti-patterns, key principles, working-with-Max). Each currently duplicates this scaffolding inline. Pulling the common spine into a `skills/qa/_batch-qa-common/` shared reference doc (or a root SKILL.md included by each branch) would remove the drift risk that already exists across the three — e.g., the Slack workflow's siren-emoji prefix rule was added to AECN/Kerry independently after the rule was introduced for AECN. Deferred from the 2026-05-12 Charm-skill build because it touches all three working skills.

## Recently Resolved (2026-10-16)

- **QA reads Certify and Drive through APIs, not Playwright.** Every QA skill, reference doc, the Knowledge Base and the step-ledger descriptions now use `skills/qa/container/tools/certify_read.py` (read-only Certify REST) and `drive_read.py` (Drive API; Drive MCP connector as the workstation fallback). Rules, gates and penalties were translated, not removed. A document absent from both Drive and the Certify API dump is still a Fail (the API cannot see removal-level sources, so the note says to confirm on the Sources tab).
- **Browser config removed.** 84 Playwright / chrome-control permission entries and the SessionEnd `browser_cleanup_sessionend.sh` registration removed from `.claude/settings.json`; hook messages that pointed at Playwright now point at the API tools; the dead Playwright-screenshot case was removed from `workspace_hygiene_guard.sh`.
- **Removed the comms cluster** (`skills/comms/verifier-briefing`). **`mrv-standup` now posts to #team-mrv-alerts** (`C0944NQH1RP`) instead of a DM, and skips its own earlier digests when scanning that channel. Nothing in this codebase DMs Garrett or Max.
- **Added `skills/qa/container/`** — runs the QA skills in GCP (`charm-mrv`, Cloud Run job `qa-runner`), operator-started via `qa_run.sh` or the `qa-trigger` endpoint, one Claude session per gate, per-mode Knowledge Base slices, robustness tests in the image build, `parity_check.py` for Mac-vs-container comparison. See `skills/qa/container/README.md`.

## Recently Resolved (2026-10-13)

- **Third workspace clean-up, now automated.** Deleted 258 `<property object at 0x…>` files at the root (left by an intermediate version of `~/.claude/hooks/lib/circuit_breaker.py` on 2026-09-24, fixed the same minute), two empty stray folders (`Expert/` here and `Skills/MRV/` beside this folder, from a folder-creation command that split the path at the space in "MRV Expert" on 2026-09-29), 49 stale Office lock files, an empty 2-byte `nulife_pdd_pdfjs_pages.txt`, and 1,048 browser captures in `.playwright-mcp/` past their age limit. Moved five protocol scrapes to `knowledge-base/`, two Certify page captures to `outputs/research/`, two Vaulted TIRE text extractions to `outputs/research/isometric_registry_review_2026-09/raw/tire/`, the one-off `scripts/write_slack_context.py` next to the ToX workbook it edits in `outputs/data-analysis/tox-analysis/` (root `scripts/` folder removed), backups and superseded versions out of `outputs/deliverables/isometric/` into `archive/`, and the `outputs/` + `temp/` folders found inside `skills/data-analysis/wellhead-data-transform/` into `archive/misrouted/2026-10-13/` (its August 2026 processed workbook differs from the one in `outputs/mrv-operational-documents/wellhead/`, so it was kept, not merged).
- **GitHub backup restored.** The auto-sync Stop hook command was an unquoted path containing a space, so the shell split it and it never ran: the last backup reached GitHub on 2026-04-29. Command now quoted. Compiled-Python files (`__pycache__/`, `*.pyc`) added to `.gitignore`.
- **Weekly sweep added** — `skills/automation/workspace-tidy/` (see the skills tree above).

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
