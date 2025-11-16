# Terraform — PadAI Cloud Run CI/CD

This module provisions:
- Artifact Registry (Docker)
- Cloud Build triggers for `main` and `preview` branches
- IAM for Cloud Build to deploy to Cloud Run

You still need to install the Cloud Build GitHub App and connect this repo.

## Usage

```bash
cd infra/terraform

# Set variables
export TF_VAR_project_id=YOUR_PROJECT
export TF_VAR_region=us-central1
export TF_VAR_github_owner=bhi5hmaraj
export TF_VAR_github_repo=PadAI

terraform init
terraform apply
```

## After apply
- Install/authorize the Cloud Build GitHub App for this repo if not already
- Push to `preview` → deploys `padai-preview`
- Push to `main` → deploys `padai`

The build files are at repo root:
- `cloudbuild-main.yaml`
- `cloudbuild-preview.yaml`

Substitutions default to:
- `_REGION`: `us-central1`
- `_REPO`: `padai` (Artifact Registry repo)
- `_SERVICE`: `padai` or `padai-preview`

## Notes
- Cloud Run services are created by `gcloud run deploy` in the build steps; Terraform manages triggers and registry.
- For persistent `.beads`, consider Cloud Run volumes (GCS FUSE) and point `WORKSPACE_PATH` to that mount. This Terraform does not provision GCS volumes by default.
