# QA Container Mode (GCP)

You are running one QA skill inside the `qa-runner` Cloud Run job in GCP project `charm-mrv`, not on Max's Mac. An operator started this run and is **not watching it**. Nobody can answer a question mid-run.

These rules override the matching steps in every QA SKILL.md. Everything else in the skill applies unchanged:
- every gate, entry and exit condition
- citation discipline and `[log:KEY]` tags
- the checklist format
- the recompute
- the adversarial review
- the step ledger and the independent ledger audit
- `run_gates.py`

`QA_CONTAINER=1` and `QA_MODE` are set for the whole run.

**The container changes where data comes from and how much of it sits in your context. It never changes what you check.** Whenever a narrowed read below doesn't give you everything a check needs, open the full file. It is always on disk.

## Gate sessions

The run is split into one session per gate. The prompt tells you which gate this session runs and names the run folder (`outputs/qa/_container/<mode>__<id>/`).

1. **Read the rules every session.** At the start of every session, do the skill's pre-flight reads: the Knowledge Base slice below, `lessons_learned.md` and `checklist_structure.md`. They hold the rules you apply. Record them in the step ledger (P1–P4) and print the Failure Categories only in the first gate's session.
2. **Check the previous gate before starting.** From a later gate, read every `handoff_gate*.md` in the run folder. Then confirm the previous gate's **exit condition** from the files on disk: source-read log, checklist, step ledger, gate receipt. If it doesn't hold, don't repair it from memory. Write `gate_<N>_result.json` with `"status": "blocked"`, say what is missing, and stop.
3. **Stay in your gate.** Do only this gate's work. All of it, including every primary-source open the skill requires in this gate, even if a previous gate opened the same file.
4. **Close the session with two files:**
   - `handoff_gate<N>.md`: anything the next gate needs that is not already in the source-read log, step ledger or checklist. For example, a suspicion you could not yet resolve, an anomaly to look at, or a value you double-checked and why. Values and findings belong in the log and the checklist, not here.
   - `gate_<N>_result.json`: `{"gate": N, "status": "complete" | "blocked", "summary": "<one paragraph>"}`. Write `complete` only when the skill's exit condition for this gate holds.

When the prompt says the skill runs as a single session (re-review), write `gate_0_result.json` at the end the same way.

## Knowledge Base slice

Read `knowledge-base/slices/<slice>.md` instead of the full Knowledge Base. The slice for each mode:

| Mode | Slice |
|---|---|
| `batch-qa-aecn` | `aecn` |
| `batch-qa-charm` | `charm` |
| `batch-qa-kerry` | `kerry` |
| `site-emissions-qa` | `site-emissions` |
| `re-review` | none: read the full Knowledge Base |

A slice is the full Knowledge Base minus sections that cannot apply to this mode. Its banner lists them. If this batch touches an excluded topic, read that section in `knowledge-base/Charm_Isometric_Knowledge_Base.md`. Record the slice path as the P1 evidence.

## Tools in the container

The skills read Certify with `skills/qa/container/tools/certify_read.py` and Drive with `skills/qa/container/tools/drive_read.py`. Here they are the **only** way in: the container has no Isometric or Google Drive MCP connector, so ignore any "MCP fallback" in a skill. `drive_read.py` runs as the job's service account; `certify_read.py` gets its credentials from Secret Manager.

| The skill says | In the container, do this |
|---|---|
| Open a Drive spreadsheet (COBB, Ops Notes, Standard Emission Factors sheet, `MRV_AECN_Analysis.xlsx`, PP summaries, trackers) | `drive_read.py get <file URL> --out .../sources/` (keeps the full workbook on disk), then `drive_read.py tabs <xlsx>` and `drive_read.py rows <xlsx> --tab "<tab>" --match "<batch id or key>" --out .../<name>_rows.json`. Add `--comments` for every cell comment on the tab, which is the Ops Notes cell-comment step. Formulas, comments and links come back per cell, which covers "click into the computed cell and quote the formula". |
| Copy the checklist to the Drive mount, or file results to Drive | `drive_read.py put <file> --folder <publish folder>`. Only the run's publish folder is writable. A checklist upload is refused unless `run_gates.py` wrote a green `gate_receipt.json` for that exact file. |
| Send, draft or schedule Slack or Gmail (Max delivery, Garrett findings thread, re-review alert) | **Do not send anything.** No Slack or Gmail tools exist here. Write the exact message(s) you would have sent, with recipients, to `outputs/qa/<batch folder>/delivery_message.md`. The operator posts them. Leave the registry's `slack_channel` / `thread_ts` unchanged, or null for a new entry. |
| Open the checklist in Excel and read Excel's PDF export (`G4_render_in_excel`) | Not possible: there's no Excel here. Mark the step `"done": "n/a"` with the evidence `"No Excel in the GCP QA container (CONTAINER_NA in batch_step_ledger.py); formatting checked by run_gates check_files()"`. Do every other Gate 4 step as written. |

## Narrowed reads: rules that keep them as strong as full reads

- **Use a narrowed read to find things, then read more when the check needs it.** If a check needs neighbouring rows, totals, another tab or a whole table, read it (`rows --tab X` with no `--match` gives the whole tab, or `--context N`). Never grade an item from a narrowed read that leaves out part of what the item checks.
- **Absence claims need a full scan.** "Batch not in COBB" or "no LCS use" must cite a `rows` result showing `rows_scanned` over the whole tab with `match_count: 0`, or a full recursive `ls` listing. A narrowed read with a tight context window can't support an absence claim.
- **Values stay cited to their location.** Log values from a `rows` result with tab and cell coordinate (e.g. `Basco Injection -- COBB!F214`), and from the Certify summary with its JSON path. `_primary_source_opened` uses `action: "sheet_grid_read"` for spreadsheet cells, `"api_read"` for Certify values, and `"pdf_read"` / `"image_read"` for documents. `live_source_url` is the dump's `live_source_url`, or the Drive `webViewLink` in the `.meta.json` next to the download.
- **Documents are never narrowed.** PDFs and images (tickets, BOLs, CoAs, the VVB guidance doc, certificates, maps) are read whole, as the skill says.

## Known API gaps: record them, don't paper over them

1. **Per-component tCO2e is not in the REST API.** Compute each component from its blueprint expression (`blueprints` in the full dump) and its input datapoints. Cross-check the total against `removal.co2e_net_removed_kg`. A checklist row that compares against "the Certify component value" must say it was computed this way.
2. **Removal-level sources not linked to any datapoint are invisible.** Before a document-presence item is graded Fail on absence from Certify, check Drive too. If it's still not found, grade it **Fail** as before, with the note "absent from Drive and the Certify API dump; confirm on the Sources tab (removal-level sources are not visible via the API)". The API gap never downgrades a missing document.

## When you would normally ask Max

The operator is not there. If a required input is missing, or the skill says to stop and ask:
1. Write the question(s) to `outputs/qa/<batch folder>/operator_questions.md`.
2. Save everything done so far.
3. Write `gate_<N>_result.json` with `"status": "blocked"`.
4. End with a final message that starts with `BLOCKED — operator input needed:`.

The operator answers by re-running with `notes`. The run resumes at this gate.

## End-of-run message

The last session's final message is saved as the run result. Make it a short summary the operator can act on:
- Status: delivered, blocked or failed.
- Pass, Fail, Flag and N/A counts.
- Every Fail item, one line each.
- What was published where.
- Where `delivery_message.md` is.
