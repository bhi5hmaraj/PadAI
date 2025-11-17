# CI/CD with GitHub Actions + Cloud Run

This repo ships with GitHub Actions workflows that give a Vercel‑like DX on Google Cloud Run: every push to `main` deploys the production service, and every PR builds a preview service that’s auto‑cleaned up when the PR closes.

## What it does

- Build container from the repo’s Dockerfile (multi‑stage; builds the frontend and serves it via FastAPI).
- Push to Artifact Registry (auto‑creates repo `tensegrity` on first run).
- Deploy to Cloud Run with sensible defaults (env vars, unauthenticated on by default).
- Preview per PR: service name `tensegrity-pr-<PR_NUMBER>`.
- Cleanup job deletes the preview service on PR close.

## Files

- `.github/workflows/cloud-run.yml`
  - Push to `main` → deploy `tensegrity`
  - Pull request → deploy `tensegrity-pr-<PR_NUMBER>`
- `.github/workflows/cloud-run-pr-cleanup.yml`
  - Pull request `closed` → delete `tensegrity-pr-<PR_NUMBER>`

## Required GitHub Secrets

Add these repo secrets under: Settings → Secrets and variables → Actions

- `GCP_PROJECT_ID` (string)
- `GCP_REGION` (string, e.g., `us-central1`)
- `GCP_SA_KEY` (JSON service account key)

Service account (deployer) needs roles:
- `roles/run.admin`
- `roles/artifactregistry.writer`
- `roles/iam.serviceAccountUser`

Auth modes supported:
- Service Account JSON (default): workflows use `credentials_json: ${{ secrets.GCP_SA_KEY }}`.
- OIDC / Workload Identity Federation (optional): see `docs/REPLICATION_CHECKLIST.md` Appendix A to set up the provider and switch the workflows.

## How to use

- Push to `main`
- Deploys Cloud Run service `tensegrity`
- Push to `preview`
- Deploys Cloud Run service `tensegrity-preview`
- Open a PR
- Deploys preview service `tensegrity-pr-<PR_NUMBER>`
- Close the PR
- `cloud-run-pr-cleanup.yml` deletes `tensegrity-pr-<PR_NUMBER>`

## Environment Variables

The workflow sets (edit in workflow if needed):
- `WORKSPACE_PATH=/workspace`
- `LOG_LEVEL=INFO`

To change env vars in deploy step, update:
```
--set-env-vars WORKSPACE_PATH=/workspace,LOG_LEVEL=INFO
```

## Notes

- Artifact Registry repo `tensegrity` is created on first run if missing.
- Cloud Run defaults to port `$PORT` (8080). The server binds to `$PORT` automatically.
- For persistent Beads data, mount a GCS volume (Cloud Run volumes with GCS FUSE) and set `WORKSPACE_PATH` to that mount path. This workflow doesn’t provision volumes.
- If you want a PR comment with the service URL, add a step after deploy to call the GitHub API and post the URL.

API enablement:
- The workflow attempts to enable `run.googleapis.com`, `artifactregistry.googleapis.com`, and `cloudbuild.googleapis.com` as a best‑effort. If the deployer SA lacks permission to enable services, the step will continue with a warning. Ensure these APIs are enabled once by a project Owner.

Example (your project):
```
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com --project personal-457416
```

## Postmortem

See `docs/POSTMORTEM_GITHUB_ACTIONS.md` for a detailed write-up of the initial CI failures (auth, permissions, AR repo, Dockerfile) and how we fixed them, plus action items to avoid regressions.

## Local checks before pushing

Install hooks once with `scripts/install_hooks.sh`.

The pre‑push hook (`scripts/prepush_checks.sh`) verifies:
- Auth mode: SA or WIF, with appropriate validations.
- Dockerfile contains `python -m server.main` and installs from `server/requirements.txt`.
- Optional GCP specifics via `gcloud`.

Bypass with `git push --no-verify` only in emergencies.

## Troubleshooting

- `permission denied` on deploy: ensure the SA has the three roles above.
- `auth` failures: check that `GCP_SA_KEY` is a valid JSON key for the SA and that the project in `GCP_PROJECT_ID` matches the key’s project.
- `Artifact Registry` errors: ensure the region matches `GCP_REGION` and that AR API is enabled. The workflow enables APIs idempotently.
