#!/usr/bin/env bash
# Create Cloud Scheduler jobs that hit each Cloud Function daily at 9am MST.
# Run AFTER all four functions are deployed.
set -euo pipefail

PROJECT="charm-mrv"
REGION="us-central1"
SA="mrv-automation@${PROJECT}.iam.gserviceaccount.com"
TZ="America/Denver"

create_job() {
  local name="$1"     # scheduler job name
  local fn="$2"       # Cloud Function name
  local schedule="$3" # cron expression in LOCAL time (America/Denver)

  local uri
  uri=$(gcloud functions describe "$fn" \
    --project="$PROJECT" --region="$REGION" \
    --format='value(serviceConfig.uri)')

  gcloud scheduler jobs create http "$name" \
    --project="$PROJECT" \
    --location="$REGION" \
    --schedule="$schedule" \
    --time-zone="$TZ" \
    --uri="$uri" \
    --http-method=POST \
    --oidc-service-account-email="$SA" \
    --oidc-token-audience="$uri"
}

# Jobs (staggered 5 min to avoid Drive API contention)
create_job sgs-test-filer-daily    sgs_test_filer     "10 9 * * *"
create_job ops-notes-creator-daily ops_notes_creator  "0 9 * * *"
create_job scale-ticket-sweep-daily scale_ticket_sweep "5 9 * * *"
create_job charm-contents-creator-daily charm_contents_creator "15 9 * * *"

echo "Done. List jobs with: gcloud scheduler jobs list --location=$REGION"
