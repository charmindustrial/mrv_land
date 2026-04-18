#!/usr/bin/env bash
# Deploy a single Cloud Function.
# Usage: ./scripts/deploy/deploy_function.sh <function_name>
#   where <function_name> is one of: sgs_test_filer, ops_notes_creator,
#   scale_ticket_sweep, charm_contents_creator
set -euo pipefail

FN="${1:-}"
if [[ -z "$FN" ]]; then
  echo "Usage: $0 <function_name>"
  exit 1
fi

PROJECT="charm-mrv"
REGION="us-central1"
SA="mrv-automation@${PROJECT}.iam.gserviceaccount.com"
RUNTIME="python312"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FN_DIR="${REPO_ROOT}/scripts/functions/${FN}"
SHARED_DIR="${REPO_ROOT}/scripts/shared"

if [[ ! -d "$FN_DIR" ]]; then
  echo "Function directory not found: $FN_DIR"
  exit 1
fi

# Stage: copy shared/ into function directory before deploy so imports resolve
STAGE_DIR="$(mktemp -d)"
cp -r "${FN_DIR}/." "$STAGE_DIR/"
cp -r "$SHARED_DIR" "$STAGE_DIR/shared"
trap "rm -rf '$STAGE_DIR'" EXIT

echo "Deploying $FN from $STAGE_DIR ..."

gcloud functions deploy "$FN" \
  --project="$PROJECT" \
  --region="$REGION" \
  --runtime="$RUNTIME" \
  --source="$STAGE_DIR" \
  --entry-point="$FN" \
  --service-account="$SA" \
  --trigger-http \
  --no-allow-unauthenticated \
  --set-secrets="SA_KEY=mrv-automation-key:latest,ANTHROPIC_API_KEY=anthropic-api-key:latest" \
  --memory=512Mi \
  --timeout=540s \
  --gen2

echo ""
echo "Deployed. Get the URL with:"
echo "  gcloud functions describe $FN --region=$REGION --format='value(serviceConfig.uri)'"
