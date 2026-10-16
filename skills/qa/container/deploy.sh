#!/usr/bin/env bash
# Build and deploy the QA container to GCP project charm-mrv.
# Safe to re-run: every create step checks first.
#
# Usage:
#   QA_OPERATORS="user:max@charmindustrial.com,user:someone@charmindustrial.com" \
#     ./skills/qa/container/deploy.sh
#
# Creates / updates:
#   - service accounts mrv-qa-runner (the job) and mrv-qa-trigger (the endpoint)
#   - GCS bucket gs://charm-mrv-qa-state (workspace state, run summaries)
#   - Artifact Registry repo mrv-qa
#   - Cloud Run job qa-runner and Cloud Run service qa-trigger
#   - IAM so QA_OPERATORS can start runs from the CLI or the endpoint
#
# Does NOT create secret values. These must already exist in Secret Manager:
#   anthropic-api-key, iso-prod-client-secret, iso-prod-jwt
set -euo pipefail

PROJECT="charm-mrv"
REGION="us-central1"
RUNNER_SA="mrv-qa-runner@${PROJECT}.iam.gserviceaccount.com"
TRIGGER_SA="mrv-qa-trigger@${PROJECT}.iam.gserviceaccount.com"
BUCKET="charm-mrv-qa-state"
REPO="mrv-qa"
JOB="qa-runner"
SERVICE="qa-trigger"
SECRETS=(anthropic-api-key iso-prod-client-secret iso-prod-jwt)
IMAGE_BASE="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}"
TAG="$(date -u +%Y%m%d-%H%M%S)"

: "${QA_OPERATORS:?Set QA_OPERATORS to a comma-separated list like user:name@charmindustrial.com}"

WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
C="${WS}/skills/qa/container"
g() { gcloud --project="$PROJECT" "$@"; }

echo "== APIs"
g services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com \
  secretmanager.googleapis.com storage.googleapis.com drive.googleapis.com

echo "== Secrets (must exist; values are never handled here)"
for s in "${SECRETS[@]}"; do
  if ! g secrets describe "$s" >/dev/null 2>&1; then
    echo "Missing secret '$s'. Create it first:  gcloud secrets create $s --project=$PROJECT --data-file=-"
    exit 1
  fi
done

echo "== Service accounts"
for sa in mrv-qa-runner mrv-qa-trigger; do
  g iam service-accounts describe "${sa}@${PROJECT}.iam.gserviceaccount.com" >/dev/null 2>&1 \
    || g iam service-accounts create "$sa" --display-name="MRV QA ${sa#mrv-qa-}"
done
for s in "${SECRETS[@]}"; do
  g secrets add-iam-policy-binding "$s" --member="serviceAccount:${RUNNER_SA}" \
    --role=roles/secretmanager.secretAccessor >/dev/null
done

echo "== State bucket"
gcloud storage buckets describe "gs://${BUCKET}" --project="$PROJECT" >/dev/null 2>&1 \
  || gcloud storage buckets create "gs://${BUCKET}" --project="$PROJECT" --location="$REGION" \
       --uniform-bucket-level-access
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${RUNNER_SA}" --role=roles/storage.objectAdmin >/dev/null
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${TRIGGER_SA}" --role=roles/storage.objectViewer >/dev/null

echo "== Artifact Registry"
g artifacts repositories describe "$REPO" --location="$REGION" >/dev/null 2>&1 \
  || g artifacts repositories create "$REPO" --location="$REGION" --repository-format=docker

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

echo "== Build runner image (staged: skills, knowledge-base, hooks; no outputs/, archive/ or secrets)"
mkdir -p "$STAGE/runner/.claude"
cp -r "$WS/skills" "$WS/knowledge-base" "$STAGE/runner/"
cp "$WS/CLAUDE.md" "$WS/README.txt" "$WS/FOLDER_INDEX.md" "$STAGE/runner/"
cp -r "$WS/.claude/hooks" "$STAGE/runner/.claude/"
cp "$C/Dockerfile" "$STAGE/runner/Dockerfile"
g builds submit "$STAGE/runner" --tag="${IMAGE_BASE}/${JOB}:${TAG}"

echo "== Deploy job ${JOB}"
g run jobs deploy "$JOB" --region="$REGION" --image="${IMAGE_BASE}/${JOB}:${TAG}" \
  --service-account="$RUNNER_SA" --tasks=1 --max-retries=0 --task-timeout=6h \
  --cpu=1 --memory=2Gi \
  --set-env-vars="QA_STATE_BUCKET=${BUCKET},ISOMETRIC_ENV=prod" \
  --set-secrets="ANTHROPIC_API_KEY=anthropic-api-key:latest,ISO_PROD_CLIENT_SECRET=iso-prod-client-secret:latest,ISO_PROD_JWT=iso-prod-jwt:latest"

echo "== Build + deploy trigger ${SERVICE}"
mkdir -p "$STAGE/trigger"
cp "$C/trigger/"* "$C/qa_inputs.py" "$STAGE/trigger/"
g builds submit "$STAGE/trigger" --tag="${IMAGE_BASE}/${SERVICE}:${TAG}"
g run deploy "$SERVICE" --region="$REGION" --image="${IMAGE_BASE}/${SERVICE}:${TAG}" \
  --service-account="$TRIGGER_SA" --no-allow-unauthenticated \
  --set-env-vars="QA_PROJECT=${PROJECT},QA_REGION=${REGION},QA_JOB=${JOB},QA_STATE_BUCKET=${BUCKET}"

echo "== IAM"
# The trigger starts executions with env overrides (run.jobs.runWithOverrides).
g run jobs add-iam-policy-binding "$JOB" --region="$REGION" \
  --member="serviceAccount:${TRIGGER_SA}" --role=roles/run.developer >/dev/null
g iam service-accounts add-iam-policy-binding "$RUNNER_SA" \
  --member="serviceAccount:${TRIGGER_SA}" --role=roles/iam.serviceAccountUser >/dev/null
IFS=',' read -ra OPS <<< "$QA_OPERATORS"
for m in "${OPS[@]}"; do
  g run services add-iam-policy-binding "$SERVICE" --region="$REGION" --member="$m" --role=roles/run.invoker >/dev/null
  g run jobs add-iam-policy-binding "$JOB" --region="$REGION" --member="$m" --role=roles/run.developer >/dev/null
  g iam service-accounts add-iam-policy-binding "$RUNNER_SA" --member="$m" --role=roles/iam.serviceAccountUser >/dev/null
  gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" --member="$m" --role=roles/storage.objectViewer >/dev/null
done

URL="$(g run services describe "$SERVICE" --region="$REGION" --format='value(status.url)')"
cat <<EOF

Deployed.
  Job:      ${JOB}  (image ${TAG})
  Endpoint: ${URL}
  State:    gs://${BUCKET}

One-time manual steps, if not done yet:
  1. Share the batch and Site Emissions shared drive(s) with ${RUNNER_SA} as Viewer,
     and each QA publish folder as Content manager.
  2. Seed state from the Mac workspace (registries + tracker) once:
       gcloud storage cp -r outputs/qa gs://${BUCKET}/state/outputs/
       for f in skills/qa/*/qa_active*.json; do gcloud storage cp "\$f" "gs://${BUCKET}/state/\$f"; done
EOF
