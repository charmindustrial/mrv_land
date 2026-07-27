MRV EXPERT WORKSPACE — README
==============================

Last updated: 2026-07-27 (added automation/charm-350-credit-report skill —
              daily bio-oil credit-submission report, launchd 15:00 local)

This is Max Lavine's MRV (Measurement, Reporting, Verification) workspace
for Charm Industrial. It contains skills, outputs, shared knowledge, and
archived material for carbon removal verification work.

ANY AGENT OR USER WHO MODIFIES THE FOLDER STRUCTURE MUST UPDATE BOTH
THIS FILE (README.txt) AND FOLDER_INDEX.md TO REFLECT THE CHANGE.
That's the rule. Out-of-date readmes are worse than no readme.


TOP-LEVEL LAYOUT
----------------

Four parent folders, plus the readme files and Claude Code config:

    skills/            Skill source code (SKILL.md + .skill archive per skill)
    outputs/           Everything skills produce (data artifacts + prose)
    knowledge-base/    Shared reference material every skill reads from
    archive/           Old drafts, evals, superseded files
    .claude/           Claude Code workspace config (skills/ contains symlinks
                       to the canonical skills under skills/ — Claude Code auto-
                       discovers them when launched from this folder).
    CLAUDE.md          Auto-loaded by Claude Code at session start; points back
                       to this README and FOLDER_INDEX.md as source of truth.

Nothing else lives at the root except FOLDER_INDEX.md, this README.txt, and
CLAUDE.md. Loose files at the root are wrong — they should be in one of the
four content folders.


SKILLS/  --  WHAT EACH SKILL DOES
---------------------------------

    skills/brief-writer/
        Writes briefs, position papers, responses, protocol change
        proposals, guidance requests, conference reportbacks, and
        onboarding documents (.docx) for various audiences using the
        knowledge base. ALWAYS asks the user which audience first
        (Isometric / feedstock-suppliers / other-external / internal
        Charm) since audience drives both composition and storage.

    skills/charm-isometric-expert/
        Knowledge-base librarian. Loads Charm/Isometric institutional
        knowledge. Reads from knowledge-base/. Doesn't produce outputs
        of its own.

    skills/lca-model-builder/
        Embodied emissions / LCA model builder for capital goods
        (railcars, tanks). Outputs DOT-111 models and BOMs.

    skills/forestry-biomass-screener/
        Pre-screen and qualification tool for new forestry biomass
        sources under BFA v1.3. Given a Drive folder of initial evidence,
        maps each of the 8 Certify feedstock requirements to the documents
        that address them, identifies gaps, and generates a go-get-these-
        docs checklist for the biomass team. In fill mode, drafts ready-
        to-paste Certify submission text for each question. Reference
        project: Elk Meadow P2 (COWF-005).

    skills/rec-eligibility-package/
        REC/EAC eligibility package builder. Given a REC/EAC retirement
        certificate, assembles the Isometric Energy Use Accounting Module
        v1.3 eligibility package (EC1-EC5, non-intensive): creates a
        "Q{quarter} {grid region} {year}" subfolder in the Pre-Review Docs
        Drive folder, copies the EC checklist, gathers the docs proving
        each criterion (including the EC4 grid-region determination from
        EIA-860M + 45VH2-GREET Table 5), fills the checklist, and hands it
        to Max for review. Read-only on Certify.

    skills/charm-isometric-expert/
        Knowledge-base librarian / expert. Also contains:
        research/  -- internal citation-methodology sub-skill.
                      Not user-triggerable. Defines the read-
                      first / verbatim-quote workflow that
                      charm-isometric-expert follows whenever
                      citing protocol text, standards clauses,
                      or regulatory language. Backed by
                      research_citation_guard.sh (PostToolUse
                      hook) on written research outputs.

    skills/qa/                                   --- QA cluster ---
        batch-qa-aecn/             Primary: AECN injection batch QA
                                   (truck and rail delivery modes)
        batch-qa-kerry/            Primary: Kerry bio-oil injection batch QA
                                   (tote and tanker delivery modes; waste-product system boundary)
        batch-qa-charm/            Primary: Charm-produced bio-oil injection batch QA
                                   (WODO and Aqueous oil types; tote-based delivery)
        batch-qa-biochar/          Primary: biochar removal QA (Range and Plains Biochar;
                                   soil storage; Protocol v1.2 + Soil Environments Module v1.3).
                                   Holds Biochar_Removal_QA_Checklist_Template.xlsx (v1.0; every
                                   protocol/module/PDD citation carries its verbatim source quote)
                                   and build_checklist.py.
        site-emissions-qa/         Primary: site-level (non-batch) QA
        adversarial-reviewer/      Sub-agent: independent challenge of QA findings
        garrett-completion-monitor/ Sub-agent: monitors Garrett's Slack responses;
                                   sweeps AECN, Kerry, and Charm batch registries
        performance-monitor/       Sub-agent: tracks QA KPIs over time

        The three sub-agents serve ALL primary QA agents. As new
        application-specific QA primaries are added (new oil types,
        new emission categories, etc.), the same three sub-agents
        apply: every primary gets adversarial review, Garrett
        reporting/monitoring, and KPI tracking.

    skills/data-analysis/                        --- Data analysis cluster ---
        wellhead-data-transform/   Ignition SCADA → VVB-ready format
                                   with compliance charts.

        Future analysis sub-skills go here as siblings.

    skills/digests/                              --- Digests cluster ---
        mrv-standup/               Daily weekday sweep of ~33 Charm + Isometric
                                   Slack channels (MRV core, verifier-facing,
                                   and adjacent/cross-team), tiered into
                                   Watch/FYI/Drop, posted to Max's self-DM.
                                   Primary invocation = scheduled remote agent
                                   at 6:30am PT M-F. Also runs ad-hoc.

    skills/comms/                                --- Comms cluster ---
        verifier-briefing/         Proactive briefings to 350Solutions (Tim
                                   Hansen) + Isometric (Tom Sellers). Two modes:
                                   quarterly (90-day lookback, fires 15th of
                                   Jan/Apr/Jul/Oct) and pre-verification
                                   (targeted memo before verification opens).
                                   Output = Gmail draft + Slack DM to Max.
                                   NEVER sends autonomously.

    skills/automation/                           --- Automation cluster ---
        mrv-mailbox/               MRV mailbox (g_mrv@charmindustrial.com)
                                   reconcile cycle. One full pass per run:
                                   send the monthly request if owed, send
                                   3/5-business-day reminders, scan + identify
                                   + route new reporting (file Community; hand
                                   Wellhead/Oxidizer to their processing skills),
                                   update the reporting-period ledger, post a
                                   completion report to #team-mrv-alerts. Every
                                   run checks the ledger first, so a missed run
                                   is fully recovered by the next one. Uses the
                                   gmail-mrv connection (authorized as g_mrv@).
                                   Fired by macOS launchd (catches missed runs
                                   on wake); also runs ad-hoc. Operating spec +
                                   ledger template + email copy live in
                                   outputs/mrv-operational-documents/mrv-mailbox-automation/.
        kdhe-kora-request/         KDHE KORA request builder for Vaulted
                                   (Advantek) monitoring. Reads the monitoring
                                   tracker (the single source of truth), requests
                                   exactly the permit-required KDHE reports that
                                   are due and not yet received plus the standing
                                   event-driven list, drafts the request .docx,
                                   and on KDHE reply downloads the returned docs
                                   and updates the tracker. Scope = permit-required
                                   monitoring reporting ONLY (never non-permit
                                   items). Draft only; Max submits via the KORA
                                   portal. Tracker + requests live in Drive:
                                   .../Vaulted/KDHE Requests/.
        charm-350-credit-report/   Daily Charm bio-oil credit-submission report.
                                   One pass per run: check #ext-proj-charm-350-
                                   isometric for a NEW "GHG statement submitted"
                                   announcement; if none, do nothing. If there is
                                   one, read the under-verification GHG statement
                                   in Certify (READ-ONLY), identify the Charm-
                                   produced oil removals (QOWV/WODO/Aqueous, not
                                   AECN), build a linked spreadsheet (removal ID,
                                   date, tCDR, total) to Drive, and send it as
                                   individual Slack DMs to Max, Garrett, Harris
                                   Cohn, John Zalewski. Idempotent (dedups on GHG
                                   statement ID). Changeable facts live in the
                                   skill's config.json. Fired by macOS launchd
                                   daily at 15:00 local; also runs ad-hoc. NOT a
                                   QA process. Autonomous send authorized for this
                                   report + fixed recipients only.


OUTPUTS/  --  WHERE EACH SKILL'S WORK GOES
-------------------------------------------

    outputs/research/                       Research outputs: findings docs, source lists,
                                           Playwright captures from web document reads
    outputs/lca-model-builder/             DOT-111 models, BOMs, co-product analyses
    outputs/qa/batch-<batch_id>/           Per-batch folder (AECN, Kerry, or Charm). Contains
                                           checklist, adversarial review, source reads,
                                           build script, timestamps, and screenshots/.
                                           See PER-BATCH QA LAYOUT below.
    outputs/qa/batch-qa/                   LEGACY flat folder — Batches 2-162 through
                                           2-185 from before the per-batch convention.
                                           Kept for history; new work goes in batch-<id>/.
    outputs/qa/site-emissions-qa/          Site emissions QA spreadsheets, briefs,
                                           screenshots/
    outputs/qa/performance-monitor/        Claude_QA_Performance_Tracker.xlsx
    outputs/data-analysis/                 Cross-skill ad-hoc analyses
    outputs/data-analysis/wellhead-data-transform/   Cleaned SCADA, compliance charts
    outputs/digests/mrv-standup/           run-log.jsonl audit trail
                                           (the digest itself lives in Slack DM)
    outputs/automation/mrv-mailbox/        run-log.jsonl audit trail (mailbox
                                           cycle; ledgers live in Drive period
                                           folders, not here)
    outputs/deliverables/                  FINALIZED EXTERNAL DOCUMENTS
        outputs/deliverables/isometric/        Briefs/responses/QBR for Isometric
        outputs/deliverables/feedstock-suppliers/  Onboarding checklists (symlinks
                                                   to operational-documents — see below)
        outputs/deliverables/mangrove/         Escalations/QBR memos for Mangrove
                                                   Systems (accounting-platform vendor)
    outputs/mrv-operational-documents/     FINALIZED INTERNAL CHARM DOCUMENTS
                                           Feedstock onboarding, conference reportbacks,
                                           internal SOPs and checklists.
    outputs/mrv-operational-documents/pdd-changelog/
                                           PDD change-log tool (pdd_changelog.py) +
                                           workflow README. On-demand diff of the PDD
                                           vs a baseline; appends Draft rows to the
                                           tracker at My Drive/MRV/PDDs+Supplemental
                                           Docs/PDD Change Log/. Baseline + tracker
                                           live on the Drive mount, not in git.
    outputs/mrv-operational-documents/mrv-mailbox-automation/
                                           MRV mailbox (g_mrv@charmindustrial.com)
                                           automation: intake/routing spec, the
                                           reporting-period ledger template, and the
                                           monthly request email template. The design
                                           for auto-handling ancillary reporting
                                           (Community / Wellhead / Oxidizer; scale
                                           tickets later).


PER-BATCH QA LAYOUT
-------------------

Every AECN or Kerry batch QA writes into its own folder at outputs/qa/batch-<batch_id>/.
Example for batch 2-190:

    outputs/qa/batch-2-190/
        Batch_2-190_QA_Checklist.xlsx       <-- the deliverable (review document)
        Batch_2-190_Adversarial_Review.md   <-- adversarial-reviewer output
        batch_2-190_source_reads.json       <-- Gate 1 source-document reads
        batch_timestamps.json               <-- gate-by-gate timing
        build_checklist.py                  <-- per-batch build script
        token_cost.json                     <-- per-batch token usage
        screenshots/                        <-- Playwright captures (gitignored)

The per-batch folder bundles checklist + adversarial + source reads + screenshots so a
verifier or future agent can reconstruct the QA session from one location. Screenshots
are evidence-pointers (regenerable), so screenshots/ is gitignored to keep the repo
lean. The workspace_hygiene_guard.sh hook denies any Playwright screenshot or .png/.yml
write that would land at the workspace root — captures must route to outputs/.


ROUTING RULES
-------------

    Skill                       --> Writes to
    --------------------------------------------------
    research                    outputs/research/
    qa-batch-aecn               outputs/qa/batch-<batch_id>/
    qa-batch-kerry              outputs/qa/batch-<batch_id>/
    qa-site-emissions           outputs/qa/site-emissions-qa/
    adversarial-reviewer        same per-batch folder as primary it's reviewing
    garrett-completion-monitor  updates primary's checklist in place
    performance-monitor         outputs/qa/performance-monitor/
    lca-model-builder           outputs/lca-model-builder/
    forestry-biomass-screener   outputs/mrv-operational-documents/
                                  (pre-screen gap reports and Certify
                                   fill text; internal Charm use only)
    rec-eligibility-package     Drive: MRV/Procured Renewables/Grid Power
                                  RECs/Inventory+Docs/Pre-Review Docs/
                                  Q{quarter} {region} {year}/ (checklist +
                                  certificate + EC4 grid-region evidence;
                                  not a local outputs/ dir)
    wellhead-data-transform     outputs/data-analysis/wellhead-data-transform/
    mrv-standup                 outputs/digests/mrv-standup/run-log.jsonl
    verifier-briefing           outputs/comms/verifier-briefing/run-log.jsonl
                                (drafts live in Gmail; never sent autonomously)
                                  (digest itself posts to Slack self-DM)
    mrv-mailbox                 outputs/automation/mrv-mailbox/run-log.jsonl
                                (ledgers live in Drive period folders;
                                 uses gmail-mrv connection as g_mrv@)
    kdhe-kora-request           Drive: .../Vaulted/KDHE Requests/
                                (request .docx + per-request received-doc
                                 subfolders + the monitoring tracker; no
                                 local output cluster)
    charm-350-credit-report     Drive: .../My Drive/Charm Bio-oil Credit
                                 Reports/ (per-period .xlsx). Runtime state
                                 in ~/.charm-350-credit-report/ (ledger,
                                 run.sh, logs). Report sends as Slack DMs.
                                 Fired by launchd daily 15:00 local.
    brief-writer                outputs/deliverables/<audience>/
                                  OR outputs/mrv-operational-documents/
                                  *** MUST ask user which audience first ***
    charm-isometric-expert      no outputs of its own (reads only)


WORKSPACE HYGIENE (hook-enforced)
---------------------------------

A PostToolUse hook at .claude/hooks/research_citation_guard.sh enforces citation
integrity in research outputs. After any Write to outputs/research/ (or any file
containing a "## Source List" section), it scans the content for citation-signal
phrases (§, Section N, Clause N, "states that", "requires that") not followed by
a verbatim quoted string within ~250 chars. Exits 2 with an explanation if violations
are found, prompting Claude to fix citations before the file is finalized.

Two Stop hooks gate factual integrity in the final response (and text deliverables)
at the moment Claude tries to end a turn:
    - .claude/hooks/citation_integrity_stop.sh -- every section/clause citation
      (§N.N, "states that", named protocol+version) must carry a verbatim quote that
      exists in a source read this session.
    - .claude/hooks/numeric_integrity_stop.sh -- every currency/rate/percentage figure
      must appear in a source read this session, wear an explicit assumption label
      (ASSUMPTION / PLACEHOLDER / illustrative / worked example, bound to the figure),
      or be the checked result of shown arithmetic; every quoted string >= 40 chars
      must exist verbatim in a session-read source; and any "A op B = C" is recomputed.
      This closes the gap that let an RSB cost estimate ship a fabricated audit day-rate
      and an un-inflated 2016 figure presented as current. It cannot verify that a
      correctly-labeled number is the RIGHT number -- that discipline is on the author
      and on the global "No Fabricated Numbers or Facts" rule in ~/.claude/CLAUDE.md.
    Both hard-block (exit 2) with a fix list, and both self-disable after 3 blocks in
    one session so a false positive can't wedge the session.

A PreToolUse hook at .claude/hooks/local_build_autoapprove.sh stops permission
prompts while building documents Max asked for, without granting any reach off the
machine. It auto-approves ONLY two narrow, provably-local cases:

    - python whose code is INLINE in the command (a heredoc `<<` or `-c`) so the
      code is visible to the hook, AND contains no network/shell-escape/external-send
      pattern (urllib, requests, socket, smtplib, subprocess, os.system, curl, etc.).
      File-path python runs (python3 some_script.py) are NOT auto-approved — their
      content can't be inspected, so they still prompt.
    - osascript that only controls Microsoft Excel or Word (close/save) and references
      nothing else (no Mail, Messages, Slack, browsers, System Events keystrokes, or
      shell-out).

Everything else falls through to the normal prompt: network-touching python, curl/wget,
osascript to Mail/Slack/browsers, and all external sends (Slack, Gmail, Drive uploads
go through MCP tools, which this Bash hook never touches). The hook only ever emits
"allow"; it never denies, so any other hook's deny still wins. Build docs with inline
python heredocs (not separate script files) to stay inside the no-prompt path.

A PreToolUse hook at .claude/hooks/workspace_hygiene_guard.sh prevents loose binary
captures and Certify scrapes from accumulating at the workspace root. It denies:

    - mcp__playwright__browser_take_screenshot calls without a `filename` that
      routes under outputs/.
    - Write calls targeting .png / .jpg / .jpeg / .yml / .yaml files at the
      workspace root.

The hook lives INSIDE the workspace (.claude/hooks/) and is registered in
.claude/settings.json — both are tracked in git so the protection rides with the
repo. The hook self-derives its workspace path from its own location, making it
machine-portable: clone the repo on a new machine and the hook just works.

A SessionEnd hook at .claude/hooks/browser_cleanup_sessionend.sh closes the Playwright
browser windows a session opened, so they don't pile up across sessions (the "why do I
have 4 Chromes open" problem). It is PRECISE, not a blanket kill: it reads the session's
own transcript for which Playwright MCP servers were actually used, maps each to its
profile directory (playwright -> playwright-profile, playwright-mrv-2 -> playwright-
profile-mrv-2, etc.), and closes only those exact windows. A window opened by a
different, still-running session (different profile) is never touched, and a session that
used no browser closes nothing. Fail-open: any error exits 0 without acting, so it can
only ever close a leftover window, never brick a session. Runs at session end, not
between turns, so a browser mid-task is never killed.

.gitignore also blocks root-level .png/.jpg/.yml/.yaml as a backstop. If the hook
ever gets disabled, git won't accidentally commit the clutter.

(Note: .claude/skills/ remains gitignored because those are machine-specific
absolute-path symlinks. Recreate them on a new machine by re-running the skill
discovery setup, or with: ln -s ../../skills/<cluster>/<skill> .claude/skills/<skill>.)


AUDIENCE RULES FOR WRITTEN WORK
-------------------------------

outputs/deliverables/  is for finalized EXTERNAL documents only:
    - isometric/             Bound for Isometric (briefs, responses, QBR, guidance)
    - feedstock-suppliers/   Bound for feedstock suppliers (onboarding materials)
    - mangrove/              Bound for Mangrove Systems (accounting-platform vendor:
                             escalations, QBR memos)
    - (add new audiences as needed: regulators, conferences, other verifiers)

outputs/mrv-operational-documents/  is for finalized INTERNAL Charm documents:
    - Internal SOPs and checklists
    - Conference takeaways/reportbacks for the Charm team
    - Operational templates

DUAL-PURPOSE DOCUMENTS:
Some documents serve both as internal operational docs AND as external
deliverables — the feedstock onboarding checklist is the canonical
example (Charm uses it internally to manage onboarding AND ships it to
suppliers as part of the onboarding process). Convention:
    - File the canonical copy in outputs/mrv-operational-documents/
    - Place a symlink at outputs/deliverables/<audience>/ pointing back
      to the canonical so edits stay in sync.

The brief-writer skill MUST explicitly ask the user which audience a
brief is for if there is any ambiguity, because audience drives both
composition (tone, detail, framing) AND storage destination.


KNOWLEDGE-BASE/  --  SHARED REFERENCE
-------------------------------------

Every skill reads from here. Files at the root, plus historical PDFs.

    Charm_PDD_v1.12_Bio_Oil_Geologic_Storage_Biochar.docx
        AUTHORITATIVE Project Design Document. v1.12 supersedes all
        earlier PDD versions. Treat as source of truth.
    Charm_Isometric_Knowledge_Base.md
        Institutional knowledge: company context, sites, emission
        factors, verification history, SLAs, protocol summaries.
    Certify_Deep_Dive_Findings.md
        Detailed analysis of Certify component structure, oil type
        identification patterns, and operational evolution timeline.
    Charm_CDR_Protocol_Summary.docx
    Isometric_Standard_v2.0_vs_v1.9_Comparison.md
    category_evidence_guide_v2.md
    MRV_Uncertainty_Evidence_Cheat_Sheet.xlsx
    isometric-findings-stats.xlsx
        Failure-mode analysis of Isometric findings (ISS-16 through ISS-30):
        each finding bucketed as Legitimate / Misunderstanding / Pending FAR
        with root-cause grouping (EF versioning, BCU quant mismatch, component
        evidence, deadhead %, etc.). QA skills consult this to know what
        verifiers are flagging and what failure modes to watch for.
    biochar_protocol_v1.2.txt, soil_module_v1.3.txt,
    book_and_claim_module_v1.txt, ghg_accounting_v1.1_allocation_text.txt,
    ghg_accounting_v1.1_allocation_text_p2.txt, lowox_clean.txt,
    lowox_module.txt, saba_atmospheric_benefit_tool.txt,
    v19_standard_snapshot.md
        Plain-text scrapes of Isometric protocol and module registry
        pages, kept for fast text search alongside the PDFs in
        isometric-pdfs/. Moved here from the workspace root 2026-07-23.
    pdd_full.txt
        Plain-text extraction of the v1.12 PDD .docx. Part of the
        batch-qa-biochar build_checklist.py quote-verification corpus
        (with biochar_protocol_v1.2.txt and soil_module_v1.3.txt).
        Regenerate from the .docx if the PDD changes.
    isometric-pdfs/
        Verification reports, GHG statements, and Isometric protocol
        modules, plus the older v1.0/v1.1 PDD (file 22). The newer
        v1.12 PDD at the root supersedes file 22.
        Module versions are checked against the live Isometric registry.
        Current as of 2026-06-22: GHG Accounting v1.1, Energy Use
        Accounting v1.3, Bio-oil Geological Storage v1.2; BFA v1.3 and
        Transportation Emissions Accounting v1.1 confirmed current.
        Outdated Modules/
            Superseded module versions, preserved (NOT deleted) when a
            newer version is pulled in. A module being superseded does
            NOT mean Charm has adopted the new one -- we keep both so we
            can cite whichever version actually governs a given project.


ARCHIVE/  --  SUPERSEDED MATERIAL
---------------------------------

Old eval outputs, draft SKILL.md versions, retired update files. Kept
for reference only — not authoritative. Don't read from here for
current operations.

Also holds (moved from the workspace root 2026-07-23): screenshots/
(Jira service-desk + GCP setup captures, May 2026), the superseded
2026-06-30 Book and Claim scrape, and Runbear Receipts/ (one empty
upload log).


CONVENTIONS FOR ADDING NEW WORK
-------------------------------

NEW SKILL:
    Create skills/<cluster>/<skill-name>/ with:
        SKILL.md                <-- canonical source (edit this)
        <skill-name>.skill      <-- packaged archive (rebuild after edits)
    If the skill produces artifacts, also create
    outputs/<cluster>/<skill-name>/.
    Update README.txt and FOLDER_INDEX.md.

NEW OUTPUT CATEGORY:
    Create the folder under outputs/. Mirror its structure with a
    matching skill folder under skills/ if applicable.
    Update README.txt and FOLDER_INDEX.md.

NEW AUDIENCE FOR DELIVERABLES:
    Add a subfolder under outputs/deliverables/.
    Update brief-writer to surface the new audience option.
    Update README.txt and FOLDER_INDEX.md.

PATH REFERENCES IN SKILL.md:
    Prefer explicit paths (e.g., knowledge-base/Charm_Isometric_Knowledge_Base.md)
    over vague language. The skill engine can find files via search either
    way, but explicit paths are faster and self-documenting.


OUTSTANDING WORK
----------------

- Resolve #co channel ID for the mrv-standup registry. Max requested
  it but no exact match exists in the channel index (only
  #colorado-ski-snowboard). On the first standup run, ask Max which
  channel he meant and update skills/digests/mrv-standup/SKILL.md.

- Extract shared root from batch-qa-aecn / batch-qa-kerry /
  batch-qa-charm. The three batch-QA skills share ~70% of their
  structure (pre-flight gate, 4-gate workflow, Slack workflow,
  formatting, citation discipline). Each currently duplicates this
  scaffolding inline. Pulling the common spine into a shared
  reference (skills/qa/_batch-qa-common/ or equivalent) would remove
  the drift risk that already exists across the three. Deferred from
  the 2026-05-12 Charm-skill build because it touches all three
  working skills.


REMEMBER
--------

If you change the folder structure, UPDATE THIS FILE AND FOLDER_INDEX.md
in the same change. Both files must reflect reality. Out-of-date readmes
mislead future agents and waste time.
