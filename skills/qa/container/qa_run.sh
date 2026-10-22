#!/usr/bin/env bash
# Start a QA run in GCP from the command line, or check on one.
#
#   ./skills/qa/container/qa_run.sh <mode> [--batch ID] [--certify URL] [--drive URL]
#        [--rp "2026-09-01 to 2026-09-30"] [--site "Basco 6"] [--cobb-row N]
#        [--publish URL] [--notes "..."] [--start-gate N] [--model ID] [--wait]
#   ./skills/qa/container/qa_run.sh status <execution>
#   ./skills/qa/container/qa_run.sh post <execution>   (review, then post its messages to #team-mrv-alerts)
#
# Modes: batch-qa-aecn | batch-qa-charm | batch-qa-kerry | site-emissions-qa | re-review
#        smoke  (container check: qa_run.sh smoke --certify <removal URL> --wait)
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

if [[ "$mode" == "post" ]]; then
  # Operator-approved Slack delivery: show the run's delivery_messages.json, post on "y",
  # and record it so the same run can never post twice.
  ex="${1:?execution name required}"
  PYBIN="${QA_PYTHON:-python3}"
  HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if gcloud storage ls "gs://${BUCKET}/runs/${ex}/slack_posted.json" >/dev/null 2>&1; then
    echo "Already posted for ${ex}:"; gcloud storage cat "gs://${BUCKET}/runs/${ex}/slack_posted.json"; exit 1
  fi
  rel="$(gcloud storage cat "gs://${BUCKET}/runs/${ex}/summary.json" | "$PYBIN" -c \
    'import json,sys; s=json.load(sys.stdin); m=[p for p in s.get("state_files_pushed",[]) if p.endswith("delivery_messages.json")]; print(m[0] if len(m)==1 else "")')"
  [[ -n "$rel" ]] || { echo "Run ${ex} produced no single delivery_messages.json; nothing to post."; exit 1; }
  work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT
  dir="$(dirname "$rel")"
  mkdir -p "$work/$dir"
  gcloud storage cp -r "gs://${BUCKET}/state/${dir}/*" "$work/$dir/" >/dev/null   # messages + gate receipt + checklist
  "$PYBIN" "$HERE/tools/slack_post.py" "$work/$rel" --dry-run || exit 1
  read -r -p $'\nPost these to #team-mrv-alerts as MRV QA? [y/N] ' ok
  [[ "$ok" == "y" || "$ok" == "Y" ]] || { echo "Not posted."; exit 0; }
  out="$(SLACK_BOT_TOKEN="$(gcloud secrets versions access latest --secret=slack-bot-token --project="$PROJECT")" \
         "$PYBIN" "$HERE/tools/slack_post.py" "$work/$rel" | tail -1)"
  printf '{"execution": "%s", "posted_by": "%s", "result": %s}\n' "$ex" "$(gcloud config get-value account 2>/dev/null)" "$out" \
    | gcloud storage cp - "gs://${BUCKET}/runs/${ex}/slack_posted.json" >/dev/null
  echo "Posted. Record: gs://${BUCKET}/runs/${ex}/slack_posted.json"
  exit 0
fi

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
