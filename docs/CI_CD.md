# CI/CD with GitHub Actions + Cloud Run

This repo ships with GitHub Actions workflows that give a Vercel‑like DX on Google Cloud Run: every push to `main` deploys the production service, and every PR builds a preview service that’s auto‑cleaned up when the PR closes.

## What it does

- Build container from the repo’s Dockerfile (multi‑stage; builds the frontend and serves it via FastAPI).
- Push to Artifact Registry (auto‑creates repo `padai` on first run).
- Deploy to Cloud Run with sensible defaults (env vars, unauthenticated on by default).
- Preview per PR: service name `padai-pr-<PR_NUMBER>`.
- Cleanup job deletes the preview service on PR close.

## Files

- `.github/workflows/cloud-run.yml`
  - Push to `main` → deploy `padai`
  - Pull request → deploy `padai-pr-<PR_NUMBER>`
- `.github/workflows/cloud-run-pr-cleanup.yml`
  - Pull request `closed` → delete `padai-pr-<PR_NUMBER>`

## Required GitHub Secrets

Add these repo secrets under: Settings → Secrets and variables → Actions

- `GCP_PROJECT_ID` (string)
- `GCP_REGION` (string, e.g., `us-central1`)
- `GCP_SA_KEY` (JSON service account key)

Service account needs roles:
- `roles/run.admin`
- `roles/artifactregistry.writer`
- `roles/iam.serviceAccountUser`

## How to use

- Push to `main`
  - Builds `:REGION-docker.pkg.dev/PROJECT/padai/padai:<ts>-<sha>`
  - Deploys Cloud Run service `padai`
- Open a PR
  - Builds `:REGION-docker.pkg.dev/PROJECT/padai/padai-pr-<PR>#:<ts>-<sha>`
  - Deploys service `padai-pr-<PR>#`
- Close the PR
  - `cloud-run-pr-cleanup.yml` deletes `padai-pr-<PR>#`

## Environment Variables

The workflow sets (edit in workflow if needed):
- `WORKSPACE_PATH=/workspace`
- `LOG_LEVEL=INFO`

To change env vars in deploy step, update:
```
--set-env-vars WORKSPACE_PATH=/workspace,LOG_LEVEL=INFO
```

## Notes

- Artifact Registry repo `padai` is created on first run if missing.
- Cloud Run defaults to port `$PORT` (8080). The server binds to `$PORT` automatically.
- For persistent Beads data, mount a GCS volume (Cloud Run volumes with GCS FUSE) and set `WORKSPACE_PATH` to that mount path. This workflow doesn’t provision volumes.
- If you want a PR comment with the service URL, add a step after deploy to call the GitHub API and post the URL.

## Troubleshooting

- `permission denied` on deploy: ensure the SA has the three roles above.
- `auth` failures: check that `GCP_SA_KEY` is a valid JSON key for the SA and that the project in `GCP_PROJECT_ID` matches the key’s project.
- `Artifact Registry` errors: ensure the region matches `GCP_REGION` and that AR API is enabled. The workflow enables APIs idempotently.
