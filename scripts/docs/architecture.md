# MRV Automation — Architecture

## Overview

Four scheduled Cloud Functions running daily at 9am MST, each doing one narrow job. They read from Gmail + Google Sheets, write to Google Drive + Google Sheets, and use Claude API for the LLM-dependent parsing (messy scale ticket photos, SGS PDFs).

```
┌──────────────────────┐       ┌─────────────────────┐
│ Cloud Scheduler      │       │ GCP project: charm-mrv
│ (4 cron jobs, 9am)   │       └─────────────────────┘
└──────────┬───────────┘                 │
           │ HTTP POST (OIDC)            │
           ↓                             │
┌──────────────────────────────────┐     │
│ Cloud Functions (4)              │     │
│  - sgs_test_filer                │     │
│  - ops_notes_creator             │     │
│  - scale_ticket_sweep            │     │
│  - charm_contents_creator        │     │
└──────────┬───────────────────────┘     │
           │                             │
           │ service account creds       │
           │ (from Secret Manager)       │
           ↓                             │
┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────┐
│ Google Drive/Sheets  │  │ Gmail (delegated)   │  │ Anthropic API  │
│ (SA has Editor       │  │ (SA impersonates    │  │ (PDF / image   │
│  on target folders)  │  │  Garrett via DWD)   │  │  parsing)      │
└──────────────────────┘  └─────────────────────┘  └────────────────┘
```

## Auth model

- **Drive + Sheets:** direct service account. Each target folder is shared with `mrv-automation@charm-mrv.iam.gserviceaccount.com` as Editor (writes) or Viewer (read-only sources).
- **Gmail:** service account impersonates `garrett.lutz@charmindustrial.com` via domain-wide delegation. The SA's client ID is authorized in the Workspace admin console with `gmail.readonly` + `gmail.modify` scopes.
- **Anthropic API:** API key stored in Secret Manager (`anthropic-api-key`), mounted into Cloud Functions as env var at runtime.

## Deployment model

- **Repo:** `github.com/charmindustrial/mrv_land` (this repo), `scripts/` subtree
- **Deploy flow:** `./scripts/deploy/deploy_function.sh <fn>` stages the function dir + shared helpers, then `gcloud functions deploy` (Gen 2)
- **Scheduler:** `./scripts/deploy/create_scheduler_jobs.sh` creates 4 HTTP cron jobs pointing at each function's URL

## Why each function runs daily

| Function | Daily value | Cost if skipped |
|----------|-------------|-----------------|
| sgs_test_filer | SGS results land throughout the month — daily catches them within ~24h | CoAs pile up, harder to QA at RP close |
| ops_notes_creator | New batches appear in COBB most days — daily creates folder structure before ops team needs it | Folder creation becomes an end-of-period scramble |
| scale_ticket_sweep | Scale tickets get uploaded as batches happen — daily backfills loaded/unloaded lbs | Ops notes stay empty until someone manually fixes |
| charm_contents_creator | Charm batches form periodically — daily creates the contents sheet in time | Sheet creation blocks Mangrove entry |

## Idempotency

Every function is idempotent — running it twice back-to-back does nothing on the second run. Mechanisms:

- **sgs_test_filer:** check md5 of uploaded PDF before upload
- **ops_notes_creator:** check folder existence before creation
- **scale_ticket_sweep:** check cell already populated before writing
- **charm_contents_creator:** check sheet existence before creation

## Scope discipline: current period only

All four functions default to the **current RP** and **current PP month**. They don't touch historical periods unless explicitly invoked with a period override. This is codified in `shared/` and enforced by every function's entry point.

## Observability

- All output → Cloud Logging (retained 30 days by default)
- Each function returns a JSON summary with counts + flags
- Failures emit structured error logs (severity=ERROR) that can be alerted on

Future: add Slack notifications via the Slack MCP connector if more visibility is needed.

## Data sources reference

| Data | Source | How accessed |
|------|--------|-------------|
| Batch UIDs + completion dates | Bio-Oil Injection Tracker → `Basco Injection -- COBB` | Sheets API |
| Tote weights + production dates | BGN Production Bio-Oil Inventory → `Oil_inventory_data` | Sheets API |
| Railcar BOLs + total loaded mass | Bio-Oil Injection Tracker → `Loads` | Sheets API |
| SGS Certificate of Analysis PDFs | Gmail (from SGS + forwarded via sampling@) | Gmail API + Claude parser |
| Scale ticket photos | Drive: `{batch}/Scale Tickets/` | Drive API + Claude parser |

## Future: MFO → BigQuery

Once MFO database replicates to BigQuery, the COBB + inventory reads can bypass Sheets entirely and query BigQuery directly (faster, more reliable, no sheet quota issues). `shared/cobb.py` is the seam for that migration.
