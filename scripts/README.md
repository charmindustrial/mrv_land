# MRV Automation — Cloud Functions

Python Cloud Functions that automate recurring MRV tasks. Runs on GCP project `charm-mrv`, triggered daily by Cloud Scheduler.

## What's in here

| Path | Purpose |
|------|---------|
| `functions/sgs_test_filer/` | **COMPLETE.** Daily SGS CoA PDF filing into batch Testing/ and PP output Testing/ folders |
| `functions/ops_notes_creator/` | **TODO.** Daily sweep for new batches in COBB, create folder + ops notes sheet |
| `functions/scale_ticket_sweep/` | **TODO.** Daily scale ticket PDF/image read + write loaded/unloaded lbs into ops notes |
| `functions/charm_contents_creator/` | **TODO.** Daily check for new 3-XX/5-XX batches, create Charm Contents sheet |
| `shared/` | Common helpers (auth, Drive/Sheets, Gmail, Claude API, COBB + inventory lookups, constants) |
| `deploy/deploy_function.sh` | Deploy a single function |
| `deploy/create_scheduler_jobs.sh` | Create the 4 daily scheduler jobs (after deploy) |
| `docs/gcp-setup.md` | One-time GCP setup commands |
| `docs/architecture.md` | Design overview |

## Current status (as of 2026-04-18)

- [x] Repo + code structure complete
- [x] `sgs_test_filer` fully implemented
- [x] Shared helpers fully implemented
- [ ] Billing account linked to `charm-mrv` — **BLOCKED** (need Shawn/IT to link)
- [ ] APIs enabled (Cloud Functions, Scheduler, Secret Manager, etc.)
- [ ] Service account created
- [ ] Drive folders shared with service account
- [ ] Gmail domain-wide delegation authorized by Workspace admin
- [ ] Anthropic API key generated + stored in Secret Manager
- [ ] Functions deployed
- [ ] Scheduler jobs created
- [ ] Remaining 3 functions ported from Claude Code agent specs

See [docs/gcp-setup.md](docs/gcp-setup.md) for the blocked setup steps.

## Quick local test of sgs_test_filer

Once you have a service account key + Anthropic key locally:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/mrv-sa-key.json
export ANTHROPIC_API_KEY=sk-ant-...

cd functions/sgs_test_filer
pip install -r requirements.txt
python main.py
```

The function will print a JSON summary with PDFs found, samples parsed, and files filed.

## Deploy (when GCP setup is done)

```bash
cd scripts
./deploy/deploy_function.sh sgs_test_filer
./deploy/create_scheduler_jobs.sh
```

## Reference

Source agent specs live at `~/.claude/agents/`:
- `sgs-test-filer.md` — maps to `functions/sgs_test_filer/`
- `ops-notes-creator.md` — port target for `ops_notes_creator`
- `charm-contents-creator.md` — port target for `charm_contents_creator`

The Claude Code agents use interactive Drive access via `drive.py` (Garrett's OAuth). These Cloud Functions re-implement the same logic using a service account for unattended execution.
