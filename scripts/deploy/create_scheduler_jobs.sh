#!/usr/bin/env bash
# Create Cloud Scheduler jobs that hit each Cloud Function (4 daily at 9am MST,
# plus the weekly injectate_ph_feed). Run AFTER the functions are deployed.
set -euo pipefail

PROJECT="charm-mrv"
REGION="us-central1"
SA="mrv-automation@${PROJECT}.iam.gserviceaccount.com"
TZ="America/Denver"

create_job() {
  local name="$1"     # scheduler job name
  local fn="$2"       # Cloud Function name
  local schedule="$3" # cron expression in LOCAL time (America/Denver)
  local sa="${4:-$SA}" # OIDC identity; defaults to mrv-automation

  # Skip jobs that already exist, so new jobs can be added by re-running this script.
  if gcloud scheduler jobs describe "$name" --project="$PROJECT" --location="$REGION" >/dev/null 2>&1; then
    echo "exists: $name (skipped)"
    return
  fi

  # Skip functions not deployed yet, so one missing function doesn't stop the rest.
  local uri
  if ! uri=$(gcloud functions describe "$fn" \
      --project="$PROJECT" --region="$REGION" \
      --format='value(serviceConfig.uri)' 2>/dev/null) || [[ -z "$uri" ]]; then
    echo "not deployed: $fn (skipped $name)"
    return
  fi

  gcloud scheduler jobs create http "$name" \
    --project="$PROJECT" \
    --location="$REGION" \
    --schedule="$schedule" \
    --time-zone="$TZ" \
    --uri="$uri" \
    --http-method=POST \
    --oidc-service-account-email="$sa" \
    --oidc-token-audience="$uri"
}

# Jobs (staggered 5 min to avoid Drive API contention)
create_job sgs-test-filer-daily    sgs_test_filer     "10 9 * * *"
create_job ops-notes-creator-daily ops_notes_creator  "0 9 * * *"
create_job scale-ticket-sweep-daily scale_ticket_sweep "5 9 * * *"
create_job charm-contents-creator-daily charm_contents_creator "15 9 * * *"

# Weekly: Saturdays 01:00 Denver = 02:00 Central, two hours after the Sat->Sat
# injection week closes. No retries (Scheduler default): Mangrove processes the
# upload async, so a fast retry could double-post before the duplicate check sees it.
create_job injectate-ph-feed-weekly injectate_ph_feed "0 1 * * 6" "${PROJECT}@appspot.gserviceaccount.com"

echo "Done. List jobs with: gcloud scheduler jobs list --location=$REGION"
