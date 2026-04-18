# GCP Setup — One-time Infrastructure

Run these commands **once** to set up the `charm-mrv` GCP project for MRV automation. They are idempotent (safe to re-run).

## Prerequisites

- `gcloud` CLI installed (verify: `gcloud version`)
- Authenticated as an Owner of `charm-mrv` project
- A billing account must be linked to `charm-mrv` (this requires a Billing Admin at the org level — ask Shawn or IT if blocked)

## Step 1 — Enable APIs

```bash
gcloud config set project charm-mrv

gcloud services enable \
  cloudfunctions.googleapis.com \
  cloudscheduler.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com
```

Verify:
```bash
gcloud services list --enabled --filter="config.name:(cloudfunctions OR cloudscheduler OR secretmanager)"
```

## Step 2 — Create the service account

```bash
gcloud iam service-accounts create mrv-automation \
  --display-name="MRV Automation" \
  --description="Runs scheduled MRV jobs"
```

Grant it project-level roles it needs:
```bash
PROJECT=charm-mrv
SA=mrv-automation@${PROJECT}.iam.gserviceaccount.com

# Allow invoking Cloud Functions
gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:${SA}" \
  --role="roles/run.invoker"

# Allow reading Secret Manager secrets
gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:${SA}" \
  --role="roles/secretmanager.secretAccessor"

# Logging (for function output)
gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:${SA}" \
  --role="roles/logging.logWriter"
```

## Step 3 — Generate a service account key

```bash
gcloud iam service-accounts keys create /tmp/mrv-sa-key.json \
  --iam-account=mrv-automation@charm-mrv.iam.gserviceaccount.com
```

## Step 4 — Store the key in Secret Manager

```bash
gcloud secrets create mrv-automation-key --replication-policy="automatic"
gcloud secrets versions add mrv-automation-key --data-file=/tmp/mrv-sa-key.json

# IMPORTANT: delete the local copy immediately
rm /tmp/mrv-sa-key.json
```

## Step 5 — Store the Anthropic API key

First, generate a key at https://console.anthropic.com/settings/keys. Then:

```bash
read -s ANTHROPIC_KEY
gcloud secrets create anthropic-api-key --replication-policy="automatic"
printf "%s" "$ANTHROPIC_KEY" | gcloud secrets versions add anthropic-api-key --data-file=-
unset ANTHROPIC_KEY
```

## Step 6 — Share Drive folders with the service account

The service account's email is `mrv-automation@charm-mrv.iam.gserviceaccount.com`.

Share these folders with that email address (treat it like a user). **Editor** access on folders we write to, **Viewer** on read-only sources.

| Folder / Sheet | Drive ID | Permission |
|----------------|----------|-----------|
| Removals Reporting | `17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b` | Editor |
| Invoices + Tracking Docs | `1k1Hk_7pQumdwZ7dnw-gSVdDlx-rmnzzi` | Editor |
| Bio-Oil Injection Tracker | `116ZyeotERBTpPrHnWmxLfEjXpqPguTpHNAQKohy5j1Q` | Viewer |
| BGN Production Bio-Oil Inventory | `1cD9cd_y_SI8GA1Yv8TFtDPqevKKF1Jh42WFRWSSMJ6g` | Viewer |
| Standard Emission Factors | `1RPm-t6EyKIk_MQicbTitx1JLjj2rBkH7kz7Nx0N1ug4` | Viewer |

Can be done via the Drive web UI or via the Drive API. Easiest: open each folder, click Share, paste the SA email.

## Step 7 — Set up Gmail domain-wide delegation

Required so the service account can read Garrett's mailbox.

1. Get the service account's **client ID**:
   ```bash
   gcloud iam service-accounts describe mrv-automation@charm-mrv.iam.gserviceaccount.com --format='value(oauth2ClientId)'
   ```
2. Go to [Google Workspace Admin Console](https://admin.google.com) → Security → Access and data control → API controls → **Domain-wide Delegation**
3. Click "Add new" and paste:
   - **Client ID:** (from step 1)
   - **OAuth scopes:**
     ```
     https://www.googleapis.com/auth/gmail.readonly
     https://www.googleapis.com/auth/gmail.modify
     ```
4. Authorize. Changes propagate in ~5 minutes.

**Note:** This step requires Workspace Admin. Ask IT if you don't have access.

## Step 8 — Verify

```bash
gcloud beta billing projects describe charm-mrv         # billingEnabled: true
gcloud iam service-accounts list                         # shows mrv-automation
gcloud secrets list                                      # shows both secrets
```

## Step 9 — Deploy the first function

```bash
cd scripts
./deploy/deploy_function.sh sgs_test_filer
```

## Step 10 — Create the Scheduler jobs (after deploys)

```bash
./deploy/create_scheduler_jobs.sh
```

## Troubleshooting

- **"Billing not enabled"** — ask Shawn/IT to link a billing account to `charm-mrv`
- **"Permission denied" on Drive** — re-check folder sharing; the SA email must be in the folder's share list
- **"401 Unauthorized" on Gmail** — domain-wide delegation not set up or propagation still in progress (wait 5 min)
- **"Secret not found"** — secret name mismatch; check `gcloud secrets list`
