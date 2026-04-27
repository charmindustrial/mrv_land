MRV EXPERT WORKSPACE — README
==============================

Last updated: 2026-04-24 (post brief-writer build + feedstock rename)

This is Max Lavine's MRV (Measurement, Reporting, Verification) workspace
for Charm Industrial. It contains skills, outputs, shared knowledge, and
archived material for carbon removal verification work.

ANY AGENT OR USER WHO MODIFIES THE FOLDER STRUCTURE MUST UPDATE BOTH
THIS FILE (README.txt) AND FOLDER_INDEX.md TO REFLECT THE CHANGE.
That's the rule. Out-of-date readmes are worse than no readme.


TOP-LEVEL LAYOUT
----------------

Four parent folders, plus this readme and the longer FOLDER_INDEX.md:

    skills/            Skill source code (SKILL.md + .skill archive per skill)
    outputs/           Everything skills produce (data artifacts + prose)
    knowledge-base/    Shared reference material every skill reads from
    archive/           Old drafts, evals, superseded files

Nothing else lives at the root except FOLDER_INDEX.md and this README.txt.
Loose files at the root are wrong — they should be in one of the four folders.


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

    skills/qa/                                   --- QA cluster ---
        batch-qa/                  Primary: AECN injection batch QA
        site-emissions-qa/         Primary: site-level (non-batch) QA
        adversarial-reviewer/      Sub-agent: independent challenge of QA findings
        garrett-completion-monitor/ Sub-agent: monitors Garrett's Slack responses
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


OUTPUTS/  --  WHERE EACH SKILL'S WORK GOES
-------------------------------------------

    outputs/lca-model-builder/             DOT-111 models, BOMs, co-product analyses
    outputs/qa/batch-qa/                   Batch_2-XXX QA checklists + adversarial reviews
    outputs/qa/site-emissions-qa/          Site emissions QA spreadsheets, briefs
    outputs/qa/performance-monitor/        Claude_QA_Performance_Tracker.xlsx
    outputs/data-analysis/                 Cross-skill ad-hoc analyses
    outputs/data-analysis/wellhead-data-transform/   Cleaned SCADA, compliance charts
    outputs/deliverables/                  FINALIZED EXTERNAL DOCUMENTS
        outputs/deliverables/isometric/        Briefs/responses/QBR for Isometric
        outputs/deliverables/feedstock-suppliers/  Onboarding checklists (symlinks
                                                   to operational-documents — see below)
    outputs/mrv-operational-documents/     FINALIZED INTERNAL CHARM DOCUMENTS
                                           Feedstock onboarding, conference reportbacks,
                                           internal SOPs and checklists.


ROUTING RULES
-------------

    Skill                       --> Writes to
    --------------------------------------------------
    qa-batch-aecn               outputs/qa/batch-qa/
    qa-site-emissions           outputs/qa/site-emissions-qa/
    adversarial-reviewer        same folder as primary it's reviewing
    garrett-completion-monitor  updates primary's checklist in place
    performance-monitor         outputs/qa/performance-monitor/
    lca-model-builder           outputs/lca-model-builder/
    wellhead-data-transform     outputs/data-analysis/wellhead-data-transform/
    brief-writer                outputs/deliverables/<audience>/
                                  OR outputs/mrv-operational-documents/
                                  *** MUST ask user which audience first ***
    charm-isometric-expert      no outputs of its own (reads only)


AUDIENCE RULES FOR WRITTEN WORK
-------------------------------

outputs/deliverables/  is for finalized EXTERNAL documents only:
    - isometric/             Bound for Isometric (briefs, responses, QBR, guidance)
    - feedstock-suppliers/   Bound for feedstock suppliers (onboarding materials)
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
    isometric-pdfs/
        43 historical PDFs: verification reports, GHG statements,
        protocol modules, and the older v1.0/v1.1 PDD (file 22).
        The newer v1.12 PDD at the root supersedes file 22.


ARCHIVE/  --  SUPERSEDED MATERIAL
---------------------------------

Old eval outputs, draft SKILL.md versions, retired update files. Kept
for reference only — not authoritative. Don't read from here for
current operations.


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

(none currently — last cleared 2026-04-24)

Future work items get added here as they're identified.


REMEMBER
--------

If you change the folder structure, UPDATE THIS FILE AND FOLDER_INDEX.md
in the same change. Both files must reflect reality. Out-of-date readmes
mislead future agents and waste time.
