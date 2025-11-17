# Deploy PadAI to Google Cloud Run

This guide deploys the PadAI FastAPI server (with built frontend) to Cloud Run using the provided Dockerfile at repo root.

## Prerequisites
- A Google Cloud project with billing enabled
- gcloud CLI installed and authenticated

```bash
# Authenticate
gcloud auth login
# Set project
gcloud config set project YOUR_PROJECT_ID
# Set a default region (e.g., us-central1)
gcloud config set run/region us-central1
```

## Enable required APIs (handled by script)
```bash
gcloud services enable run.googleapis.com   artifactregistry.googleapis.com   cloudbuild.googleapis.com
```

## Artifact Registry (auto-created on first push)
```bash
REGION=us-central1
REPO=padai
PROJECT=$(gcloud config get-value project)

gcloud artifacts repositories create $REPO   --repository-format=docker   --location=$REGION   --description="PadAI containers"
```

If the repo already exists, this command will error; that’s fine—continue.

## Build and push the image (Cloud Build)
```bash
IMAGE=$REGION-docker.pkg.dev/$PROJECT/$REPO/padai:$(date +%Y%m%d-%H%M%S)

gcloud builds submit --tag $IMAGE .
```

This uses the Dockerfile to:
- Build the frontend (Vite)
- Install Python deps, copy server code
- Download bd CLI
- Copy your `.beads/` into `/workspace/.beads` inside the image

Note: Cloud Run instances are ephemeral. Any changes to the database at runtime will not persist across restarts. For durable state, back `/workspace/.beads` with GCS FUSE or move to a managed DB (future work).

## CI/CD path

This repo includes GitHub Actions workflows that build, push, and deploy on push. Current default auth is Service Account JSON. Required secrets and steps are documented in `docs/CI_CD.md` and the end‑to‑end replication steps in `docs/REPLICATION_CHECKLIST.md`.

## Deploy to Cloud Run (via gcloud)
```bash
SERVICE=padai

gcloud run deploy $SERVICE   --image $IMAGE   --allow-unauthenticated   --platform managed   --region $REGION   --set-env-vars WORKSPACE_PATH=/workspace,LOG_LEVEL=INFO
```

The server binds to `$PORT` automatically (Cloud Run default 8080). CORS is open by default.

Optional flags:
- `--min-instances=0 --max-instances=4` to cap autoscaling
- `--cpu=1 --memory=512Mi`

## Verify
```bash
URL=$(gcloud run services describe $SERVICE --region $REGION --format='value(status.url)')

curl -s $URL/ | jq
curl -s $URL/api/status | jq
curl -s $URL/api/tasks | jq '.tasks | length'
```

If you see `BEADS_JSONL=missing` in logs, ensure your repo’s `.beads/` exists and was copied into the image. The Dockerfile expects it at build time.

## Update / Rollback
```bash
# Build a new image
IMAGE=$REGION-docker.pkg.dev/$PROJECT/$REPO/padai:$(date +%Y%m%d-%H%M%S)
gcloud builds submit --tag $IMAGE .
# Deploy new image
gcloud run deploy $SERVICE --image $IMAGE --region $REGION --platform managed
# List revisions
gcloud run revisions list --service=$SERVICE --region=$REGION
# Rollback to a previous revision (example)
gcloud run services update-traffic $SERVICE --to-revisions=REVISION_NAME=100 --region=$REGION
```

## Custom Domain (optional)
Follow the Cloud Run guide: map a custom domain to `$SERVICE`, then update the dashboard `VITE_API_URL` to the new URL if serving frontend separately.

## Notes
- The Dockerfile exposes 8080 (Cloud Run default); the app uses `$PORT` internally.
- The frontend `dist/` is served statically by FastAPI under `/`.
- For persistent Beads data, consider mounting GCS via Cloud Run volumes (GCS FUSE) and pointing `WORKSPACE_PATH` there.

## Manual (no Terraform) — Quick Deploy with gcloud

If Terraform feels heavy for a personal project, use the provided script:

```bash
scripts/deploy_cloud_run.sh <PROJECT_ID> <REGION> <SERVICE>
# Example:
scripts/deploy_cloud_run.sh my-proj us-central1 padai
```

This will:
- Enable required APIs
- Build the container with Cloud Build
- Push to Artifact Registry (creates `padai` repo on first use)
- Deploy to Cloud Run service `<SERVICE>`

Env vars:
- Set via `ENV_VARS`, defaulting to `WORKSPACE_PATH=/workspace,LOG_LEVEL=INFO`.

```bash
ENV_VARS="WORKSPACE_PATH=/workspace,LOG_LEVEL=DEBUG" \
  scripts/deploy_cloud_run.sh my-proj us-central1 padai-preview
```

When Terraform is useful:
- Team environments (review apps, staging/prod)
- Repeatable infra across projects/regions
- Versioned infra, drift detection, and plan reviews
- Complex IAM and service bindings


## Future (Optional): Terraform
If you later want fully managed, reviewable infrastructure (triggers, registries, IAM), consider adding Terraform back. For now, this project deploys with `gcloud` via `scripts/deploy_cloud_run.sh` to keep things simple for a personal project.
