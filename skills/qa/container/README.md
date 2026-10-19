# QA in GCP (container mode)

Runs the existing QA skills (`batch-qa-aecn`, `batch-qa-charm`, `batch-qa-kerry`, `site-emissions-qa` and the re-review from `garrett-completion-monitor`) as Claude Code in headless mode, inside the Cloud Run job `qa-runner` in GCP project `charm-mrv`. The skills themselves don't change. An operator always starts a run; nothing is scheduled.

## Starting a run

**CLI** (needs `gcloud` and operator IAM from `deploy.sh`):

```bash
skills/qa/container/qa_run.sh batch-qa-aecn --batch INJ-09-2026-W4-AECN \
  --certify "https://registry.isometric.com/account/certify/project/prj_.../removal/rmv_.../edit" \
  --drive "https://drive.google.com/drive/folders/..." --wait

skills/qa/container/qa_run.sh site-emissions-qa --rp "2026-09-01 to 2026-09-30" --site "Basco 6" \
  --certify "<scapegoat removal URL(s), comma-separated>" --drive "<RP Site Emissions folder>"

skills/qa/container/qa_run.sh re-review --batch INJ-09-2026-W4-AECN      # after Garrett says he's done
skills/qa/container/qa_run.sh status <execution name>
```

**HTTP** (`qa-trigger` service; the caller needs `run.invoker`):

```bash
URL=$(gcloud run services describe qa-trigger --project=charm-mrv --region=us-central1 --format='value(status.url)')
curl -X POST "$URL/run" -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{"mode":"batch-qa-aecn","batch_id":"INJ-09-2026-W4-AECN","certify_url":"...","drive_folder":"..."}'
curl "$URL/status/<execution>" -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

Inputs and the required fields for each mode are defined in `qa_inputs.py`. Optional fields:
- `publish_folder` — where results go. Defaults to the batch Drive folder.
- `cobb_row`
- `notes` — answers to a blocked run's questions.

## What a run does

1. Takes a lock in `gs://charm-mrv-qa-state`, so only one QA run edits the registries and the tracker at a time.
2. Pulls the state: `outputs/qa/**` and `skills/qa/*/qa_active*.json`.
3. Runs the skill **one Claude session per gate**: Gates 1–4 for batch QA, 1–3 for site emissions, one session for a re-review. [CONTAINER_MODE.md](CONTAINER_MODE.md) is appended to every session's system prompt. It maps every Playwright, Drive connector, Drive mount, Slack and Gmail step to the container tools:
   - `tools/certify_read.py`: read-only Certify REST.
   - `tools/drive_read.py`: Drive as the job's service account. It can write only to the run's publish folder, and won't upload a checklist without a green `gate_receipt.json`.

   A gate that ends blocked or failed stops the run. The next run resumes at that gate; `--start-gate N` forces a re-run from gate N.
4. Pushes the state back. Writes `runs/<execution>/summary.json` (turns and cost for each gate) and one transcript per gate.

**The run never sends Slack or Gmail.** It writes the messages it would have sent to `outputs/qa/<batch folder>/delivery_message.md`, and the operator posts them.

**If the run needs an answer**, it stops with `BLOCKED — operator input needed:`. The questions are also saved in `operator_questions.md`. Re-run with the answers in `--notes`; the skill resumes from the gate it reached.

## Deploying

```bash
QA_OPERATORS="user:max@charmindustrial.com,user:garrett.lutz@charmindustrial.com" skills/qa/container/deploy.sh
```

Before the first deploy:
1. Create the secrets `iso-prod-client-secret` and `iso-prod-jwt` in `charm-mrv` Secret Manager from a Certify API credential (Certify → Team settings). `anthropic-api-key` already exists there.
2. After the deploy, share the batch and Site Emissions shared drive(s) with `mrv-qa-runner@charm-mrv.iam.gserviceaccount.com`: Viewer on the drives, Content manager on the publish folders.
3. Seed the state bucket once from the Mac workspace. The commands are printed at the end of `deploy.sh`.

The image contains `skills/qa/` (no other skills: nothing outside `skills/qa/` is used by a QA run, and some of it, like `orchestrator-mode`, can't run headless), `knowledge-base/`, `CLAUDE.md`, the README/index files and `.claude/hooks/`. It never contains `outputs/`, `archive/` or credentials. `settings.json` here replaces `.claude/settings.json` in the image. It keeps the portable project hooks and drops the Mac-only ones: auto-sync, the `~/.claude/hooks/*` guards and the browser cleanup.

## What keeps the cost down

Almost all of a run's cost is the model re-reading its context on every turn, so cost ≈ turns × context size. The container cuts the context, not the checks.

| Change | What it removes from context | Why the QA is unchanged |
|---|---|---|
| One session per gate | Everything earlier gates read, carried through every later turn | Every gate re-reads the rules and checks the previous gate's exit condition from the files on disk. The skills already require every value to live in the source-read log, and the adversarial review works only from that log. |
| Knowledge Base slice (`kb_slices.py`) | 20–29% of the Knowledge Base: biochar, KDHE permit, SLA, external-document standards, other oil types | Excluded sections are named with reasons, and new sections are kept by default. Sections that carry rules are guarded by a test. The full Knowledge Base is still in the image. |
| `drive_read.py rows` | Whole COBB / Ops Notes / emission-factor workbooks (Max's notes: a 320 KB COBB dump) | Returns every cell's value, formula, comment and link with its coordinate. Absence claims need a full-tab scan. The whole workbook stays on disk. PDFs and images are never narrowed. |
| `certify_read.py` summary | Full Certify dumps; ~30 turns of modal clicks and 400-line snapshots on the Mac | Lists every input value, SD and source with its JSON path into the full dump, which stays on disk. |
| Turn cap per gate (`QA_MAX_TURNS_PER_GATE`, default 200), 1 CPU / 2 GiB | Runaway sessions | Hitting the cap marks the gate failed. It never passes; the next run resumes at that gate. |

Unchanged: the model, the four gates, the adversarial reviewer, the independent ledger audit, `run_gates.py`, `audit_checklist.py` and the recompute scripts. The only Mac step dropped is `G4_render_in_excel`, which checks how the checklist looks in Excel. It's allowed `n/a` only when `QA_CONTAINER=1`. The code-enforced formatting checks still run.

## Proving it's as robust as the Mac runs

1. **Tests gate the image.** `tests/test_container.py` runs during the Docker build. It checks each change that could weaken QA:
   - slices drop only the named sections, and never a rule section
   - narrowed reads keep formulas, comments, links and full-tab absence scans
   - the Certify summary drops no datapoint
   - the delivery gate holds
   - the Excel `n/a` is allowed only in the container
   - Max's `test_findings_never_block.py` still passes

   I broke the slices, the summary, the ledger allow-list and the gate list on purpose to confirm the tests catch each break.
2. **Parity runs before relying on it.** Re-run 3 batches that were already QA'd on the Mac, picked to cover AECN rail, AECN truck, and Charm or Kerry, and preferably batches whose Certify data hasn't been corrected since. Then compare:
   ```bash
   python3 skills/qa/container/parity_check.py <mac checklist.xlsx> <container checklist.xlsx> --out parity.json
   ```
   - It fails if the container grades any item less severely than the Mac did (Fail→Flag/Pass, Flag→Pass), marks an applicable item N/A, or drops an item.
   - Items the container grades more strictly are listed for review.
   - Ship when all 3 pass. Any regression is a bug to fix before going live.
3. **Cost check.** Each run's `summary.json` reports turns and dollars per gate. Compare against Max's numbers in `batch-qa-aecn/COST_DOWN_BACKLOG.md`: $127–205 for a clean AECN batch.

## Using the tools on a workstation

The QA skills read Certify and Drive through `tools/certify_read.py` and `tools/drive_read.py` everywhere, not only in the container. QA no longer uses Playwright.

To run a skill locally:
- **Certify:** set `ISO_PROD_CLIENT_SECRET` and `ISO_PROD_JWT` in the environment.
- **Drive:** run `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform` once. `drive_read.py` then reads as you. Without that, the skills fall back to the Google Drive MCP connector.

## Known differences from the Mac runs

- **Per-component tCO2e** isn't in the Certify REST API. It's computed from each component's blueprint and inputs, and the total is checked against the removal's net.
- **Removal-level sources that aren't linked to a datapoint** can't be seen through the API. A document missing from both Drive and the API dump is still graded Fail, as before, with a note to confirm on the Sources tab. The API gap can cause a false Fail, never a missed one.
- **The `~/.claude/hooks` guards on Max's Mac** aren't in the repo, so the container doesn't have them: `qa_delivery_gate_guard`, `qa_chat_result_guard`, `no_deferral_guard`, `certify_readonly_guard` and `final_marker_receipt_guard`. Three things cover the most important ones:
  - Delivery gate: the receipt check in `drive_read.py put`.
  - Certify read-only: `certify_read.py` has no write path.
  - No Slack or Gmail tools exist in the container.
- **Max's Claude memory files** (e.g. `feedback_*.md`) that the skills mention aren't available.
