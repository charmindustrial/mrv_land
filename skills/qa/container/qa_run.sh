#!/usr/bin/env bash
# Start a QA run in GCP from the command line, or check on one.
#
#   ./skills/qa/container/qa_run.sh <mode> [--batch ID] [--certify URL] [--drive URL]
#        [--rp "2026-09-01 to 2026-09-30"] [--site "Basco 6"] [--cobb-row N]
#        [--publish URL] [--notes "..."] [--start-gate N] [--model ID] [--wait]
#   ./skills/qa/container/qa_run.sh status <execution>
#
# Modes: batch-qa-aecn | batch-qa-charm | batch-qa-kerry | site-emissions-qa | re-review
#
# Examples:
#   qa_run.sh batch-qa-aecn --batch INJ-09-2026-W4-AECN --certify "https://registry.isometric.com/..." \
#     --drive "https://drive.google.com/drive/folders/..." --wait
#   qa_run.sh re-review --batch INJ-09-2026-W4-AECN
set -euo pipefail

PROJECT="charm-mrv"
REGION="us-central1"
JOB="qa-runner"
BUCKET="charm-mrv-qa-state"

mode="${1:?mode or 'status' required (see header)}"; shift

if [[ "$mode" == "status" ]]; then
  ex="${1:?execution name required}"
  gcloud run jobs executions describe "$ex" --project="$PROJECT" --region="$REGION" \
    --format='table(name,status.runningCount,status.succeededCount,status.failedCount,status.completionTime)'
  gcloud storage cat "gs://${BUCKET}/runs/${ex}/summary.json" 2>/dev/null \
    || echo "(no summary yet — the run is still going or failed before writing one)"
  exit 0
fi

declare -A env=([MODE]="$mode" [OPERATOR]="$(gcloud config get-value account 2>/dev/null)")
wait_flag=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --batch)    env[BATCH_ID]="$2"; shift 2 ;;
    --certify)  env[CERTIFY_URL]="$2"; shift 2 ;;
    --drive)    env[DRIVE_FOLDER]="$2"; shift 2 ;;
    --rp)       env[REPORTING_PERIOD]="$2"; shift 2 ;;
    --site)     env[SITE]="$2"; shift 2 ;;
    --cobb-row) env[COBB_ROW]="$2"; shift 2 ;;
    --publish)  env[PUBLISH_FOLDER]="$2"; shift 2 ;;
    --notes)    env[NOTES]="$2"; shift 2 ;;
    --start-gate) env[START_GATE]="$2"; shift 2 ;;
    --model)    env[MODEL]="$2"; shift 2 ;;
    --wait)     wait_flag=(--wait); shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# '^|^' switches gcloud's list delimiter to '|', so values may contain commas.
pairs=""
for k in "${!env[@]}"; do
  v="${env[$k]}"
  [[ "$v" == *"|"* ]] && { echo "Values may not contain '|': $k"; exit 1; }
  pairs+="${pairs:+|}QA_${k}=${v}"
done

# Validation (required fields per mode) happens in the job; an invalid run exits 2 at once.
gcloud run jobs execute "$JOB" --project="$PROJECT" --region="$REGION" \
  --update-env-vars="^|^${pairs}" "${wait_flag[@]}"

echo "Check on it with:  $0 status <execution name above>"
