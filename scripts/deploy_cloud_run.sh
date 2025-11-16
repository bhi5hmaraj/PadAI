#!/usr/bin/env bash
set -euo pipefail

# Deploy PadAI to Cloud Run using gcloud directly (no Terraform).
# - Builds the image via Cloud Build
# - Pushes to Artifact Registry (creates repo on first push)
# - Deploys to Cloud Run service
#
# Usage:
#   scripts/deploy_cloud_run.sh <project> <region> <service>
#
# Examples:
#   scripts/deploy_cloud_run.sh my-proj us-central1 padai
#   scripts/deploy_cloud_run.sh my-proj us-central1 padai-preview
#
# Optional env:
#   ENV_VARS   Comma-separated env vars for the service
#              (default: WORKSPACE_PATH=/workspace,LOG_LEVEL=INFO)

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <project> <region> <service>" >&2
  exit 2
fi

PROJECT="$1"
REGION="$2"
SERVICE="$3"

ENV_VARS="${ENV_VARS:-WORKSPACE_PATH=/workspace,LOG_LEVEL=INFO}"

echo "→ Project: $PROJECT  Region: $REGION  Service: $SERVICE"

echo "→ Enabling required APIs (idempotent)"
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  --project "$PROJECT" >/dev/null

REPO="padai"
IMAGE_PATH="$REGION-docker.pkg.dev/$PROJECT/$REPO/$SERVICE"
TAG=$(date +%Y%m%d-%H%M%S)
if git rev-parse --short HEAD >/dev/null 2>&1; then GIT_SHA=$(git rev-parse --short HEAD); TAG="$TAG-$GIT_SHA"; fi
IMAGE="$IMAGE_PATH:$TAG"

echo "→ Building image with Cloud Build: $IMAGE"
gcloud builds submit --project "$PROJECT" --tag "$IMAGE" .

echo "→ Deploying to Cloud Run: $SERVICE ($REGION)"
gcloud run deploy "$SERVICE" \
  --project "$PROJECT" \
  --image "$IMAGE" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "$ENV_VARS"

URL=$(gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" --format='value(status.url)')
echo "✓ Deployed: $URL"

