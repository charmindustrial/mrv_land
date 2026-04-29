# MRV Expert — Folder Index

Last updated: 2026-04-24 (post brief-writer build + feedstock rename). The workspace has four parent folders. Every skill, output, reference, and old artifact lives in exactly one of them. New work always lands in a predictable place.

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
├── qa/                                         ← QA cluster
│   ├── batch-qa/                              (primary QA agent — AECN injection batches)
│   ├── site-emissions-qa/                     (primary QA agent — site/non-batch emissions)
│   ├── adversarial-reviewer/                  (sub-agent — serves all QA primaries)
│   ├── garrett-completion-monitor/            (sub-agent — serves all QA primaries)
│   └── performance-monitor/                   (sub-agent — serves all QA primaries)
└── data-analysis/                              ← data analysis cluster
    └── wellhead-data-transform/               (Ignition SCADA → VVB format + compliance charts)
```

**QA sub-agents serve all QA primaries.** Today they support `batch-qa/` and `site-emissions-qa/`. As future application-specific QA agents (e.g., for new oil types, new emission categories) are added under `skills/qa/`, the same three sub-agents apply: every primary is subject to adversarial review, gets reported out to Garrett with completion monitoring, and is tracked against performance KPIs.

## outputs/ — What Skills Produce

```
outputs/
├── lca-model-builder/                         ← DOT-111 models, BOMs, co-product analyses
├── qa/
│   ├── batch-qa/                              ← Batch_2-XXX_QA_Checklist.xlsx + adversarial reviews + Garrett-edited versions
│   ├── site-emissions-qa/                     ← Site_Emissions_QA_*.xlsx + session briefs
│   └── performance-monitor/                   ← Claude_QA_Performance_Tracker.xlsx
├── data-analysis/                              ← cross-skill ad-hoc analyses
│   └── wellhead-data-transform/               ← cleaned SCADA, compliance charts, eval reports
├── deliverables/                               ← finalized EXTERNAL documents only
│   ├── isometric/                             ← Isometric-bound briefs, responses, guidance requests, QBR
│   └── feedstock-suppliers/                   ← onboarding materials (symlinks to operational-documents)
└── mrv-operational-documents/                  ← finalized INTERNAL Charm documents
                                                 (feedstock onboarding, conference reportbacks, internal SOPs)
```

### Routing rules

| Skill | Writes to |
|-------|-----------|
| qa-batch-aecn (and future batch-QA primaries) | `outputs/qa/batch-qa/` |
| qa-site-emissions (and future site-QA primaries) | `outputs/qa/site-emissions-qa/` |
| adversarial-reviewer | same folder as the primary it's reviewing |
| garrett-completion-monitor | updates the primary's checklist in place |
| performance-monitor | `outputs/qa/performance-monitor/` |
| lca-model-builder | `outputs/lca-model-builder/` |
| wellhead-data-transform | `outputs/data-analysis/wellhead-data-transform/` |
| brief-writer | `outputs/deliverables/<audience>/` OR `outputs/mrv-operational-documents/` — **must ask the user which audience first** |
| charm-isometric-expert | reads the knowledge base; produces no artifacts of its own |

### Audience rules for written work

`outputs/deliverables/` is for finalized **external** documents only. Audience subfolders inside it identify the recipient:
- `outputs/deliverables/isometric/` — anything bound for Isometric (briefs, responses, guidance requests, QBR briefs)
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
├── Isometric_Standard_v2.0_vs_v1.9_Comparison.md
├── category_evidence_guide_v2.md
├── MRV_Uncertainty_Evidence_Cheat_Sheet.xlsx
└── isometric-pdfs/                                          ← 43 historical PDFs:
                                                                verification reports, GHG statements,
                                                                protocol modules, older PDD (file 22)
```

The v1.12 PDD at the root is the canonical Project Design Document. Earlier versions (including `isometric-pdfs/22_2025-02-20_pdd.pdf`) are kept for historical reference only.

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
└── Site_Emissions_QA_Template_draft.xlsx
```

## Conventions for Adding New Work

**New skill:** create `skills/<cluster>/<skill-name>/` with `SKILL.md` (source) and `<skill-name>.skill` (packaged archive). If the skill produces artifacts, also create `outputs/<cluster>/<skill-name>/` as its output destination. Update this file.

**New output cluster (e.g., a new analysis subskill):** add it under the appropriate parent in `outputs/`. Mirror the structure with a sibling skill folder under `skills/`.

**New audience:** add a subfolder under `outputs/deliverables/` (external) or extend `outputs/mrv-operational-documents/` (internal). Update the brief-writer skill so it surfaces the new audience option to the user.

**Path references in SKILL.md:** prefer the explicit path under the workspace folder (e.g., `knowledge-base/Charm_Isometric_Knowledge_Base.md`) over vague language. The skill engine can find files via search either way, but explicit paths are faster and self-documenting.

**Whenever the structure changes, update both `README.txt` and `FOLDER_INDEX.md` in the same change.** No exceptions. Out-of-date docs mislead future agents and waste time.

## Outstanding Work

(none currently — last cleared 2026-04-24)

Future work items get added here as they're identified.

## Recently Resolved (2026-04-24)

- **Built the brief-writer skill.** `skills/brief-writer/` now contains a full SKILL.md and packaged `.skill` archive. The skill asks audience and brief type up front via AskUserQuestion, reads from `knowledge-base/`, references prior brief patterns, and routes output to the correct `outputs/deliverables/<audience>/` or `outputs/mrv-operational-documents/` folder.
- **Renamed feedstock files for clarity.** `New_Feedstock_Oil_Source_Onboarding_Checklist.xlsx` → `Feedstock_Oil_Source_Process_Checklist.xlsx`. `New_Feedstock_Onboarding_Checklist.xlsx` → `Feedstock_Supplier_Onboarding_Template.xlsx`. Symlinks in `outputs/deliverables/feedstock-suppliers/` updated to match. The two files are distinct artifacts — process checklist (with reference index) vs. template (with filled supplier instances) — and intentionally kept separate.
