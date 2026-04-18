# sgs_test_filer

Daily Cloud Function that files SGS Certificate of Analysis PDFs into the right Drive folders.

## Trigger

HTTP-triggered by Cloud Scheduler daily at 9:00 MST:
```
0 9 * * *   (America/Denver)
```

## Flow

1. Search Gmail for SGS emails in the last 2 days (queries in `shared/constants.py`)
2. Download PDF attachments
3. Parse each PDF via Claude API → one row per sample (Certificate #, CLIENT ID, Carbon %, etc.)
4. For each sample:
   - **CLIENT ID `BATCH X-XX`** (Flow A) → upload to that batch's `Testing/` folder in the current RP
   - **6-digit tote tag** (Flow B) → look up in BGN inventory, upload to `Miniforge Pyrolysis Output / YYYY / MonthName YY / Testing/`
5. Skip duplicates (by md5 match on filename)
6. Return JSON summary

## Dependencies

- Service account `mrv-automation@charm-mrv.iam.gserviceaccount.com` with:
  - Editor access to `Removals Reporting` root (`17aWrxiLuTWyqX3Aa4pkqQ2hFbx18qT0b`)
  - Editor access to `Invoices + Tracking Docs` root (`1k1Hk_7pQumdwZ7dnw-gSVdDlx-rmnzzi`)
  - Read access to BGN Production Inventory (`1cD9cd_y_SI8GA1Yv8TFtDPqevKKF1Jh42WFRWSSMJ6g`)
  - Domain-wide delegation enabled for `gmail.readonly` scope (to read Garrett's mailbox)
- Secrets in Secret Manager: `mrv-automation-key`, `anthropic-api-key`
- `sampling@charmindustrial.com` forwarding rules for SGS emails (current state)

## Local test

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/mrv-sa-key.json
export ANTHROPIC_API_KEY=sk-ant-...
cd functions/sgs_test_filer && python main.py
```

## Deploy

```bash
./scripts/deploy/deploy_function.sh sgs_test_filer
```
