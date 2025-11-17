# Tensegrity / PadAI – Replication Checklist (GCP + CI/CD)

This checklist lets you stand up the project in a new Google Cloud project and wire up GitHub Actions deploys to Cloud Run. It captures the current setup (Service Account JSON auth in CI) and the repository checks we enforce.

## 0) Prerequisites
- Google Cloud project with billing enabled (note the `PROJECT_ID`).
- Local: `gcloud`, `docker`, `node` (for frontend), `python3.11` (for server).
- GitHub repo created with your code pushed (fork or new repo).

## 1) Service Account (CI deployer)
We use Service Account JSON auth for GitHub Actions (simpler than OIDC/WIF).

- Create CI deployer Service Account:
  - Name: `tensegrity-deployer`
  - Email: `tensegrity-deployer@<PROJECT_ID>.iam.gserviceaccount.com`
  - Roles on project:
    - `roles/run.admin`
    - `roles/artifactregistry.writer`
    - `roles/iam.serviceAccountUser`

- Create a JSON key and save to a temporary file:
  - `gcloud iam service-accounts keys create key.json \
     --iam-account tensegrity-deployer@<PROJECT_ID>.iam.gserviceaccount.com \
     --project <PROJECT_ID>`
  - Open `key.json`, copy entire contents.
  - Add GitHub repo secret `GCP_SA_KEY` with the copied JSON (Settings → Secrets and variables → Actions).
  - Delete the local `key.json` file after adding the secret.

Security note: SA keys are less secure than OIDC. Rotate the key periodically and restrict repo access. You can switch back to OIDC later (see Appendix A).

API enablement permission:
- Enabling services requires elevated permissions (Owner/Editor or `roles/serviceusage.serviceUsageAdmin`).
- Our CI tries to enable services as best‑effort but ignores permission errors. Make sure these APIs are enabled once by a project Owner:
  - `run.googleapis.com`
  - `artifactregistry.googleapis.com`
  - `cloudbuild.googleapis.com`

## 2) GitHub Actions Secrets
Add the following repository secrets (Actions):
- `GCP_PROJECT_ID` = `<PROJECT_ID>`
- `GCP_REGION` = `us-central1` (or your region)
- `GCP_SA_KEY` = JSON from step 1

## 3) CI Workflows
Already included in repo:
- `.github/workflows/cloud-run.yml` – builds and deploys on pushes to `main` and `preview`; PRs create preview services.
- `.github/workflows/cloud-run-pr-cleanup.yml` – cleans up preview service on PR close.

Defaults/behavior:
- Artifact Registry repo: `padai` (auto-created on first run).
- Service names:
  - `padai` on `main`
  - `padai-preview` on `preview`
  - `padai-pr-<PR>` on pull requests
- Env vars at deploy: `WORKSPACE_PATH=/workspace, LOG_LEVEL=INFO`

Optional rename: If you prefer `tensegrity` naming everywhere, update service names and `env.REPO` in the workflows accordingly.

## 4) Dockerfile constraints (what our checks enforce)
- Must start the server with:
  - `CMD python -m server.main`
- Must install dependencies from `server/requirements.txt`.
- Multi-stage build compiles `frontend/` and copies `frontend/dist` into the image.

## 5) Pre‑push checks (local safety net)
Install hooks once:
- `scripts/install_hooks.sh`

What the hook checks (`scripts/prepush_checks.sh`):
- Detects CI auth mode:
  - SA mode: allows `credentials_json` in workflows; validates that the deployer SA exists.
  - WIF mode (OIDC): requires `workload_identity_provider` in workflows; validates pool/provider condition and binding.
- Verifies Dockerfile contains `python -m server.main` and installs from `server/requirements.txt`.
- Uses defaults for project/SA; override via env when needed:
  - `GCP_PROJECT_ID`, `GCP_DEPLOY_SA_NAME`, `GITHUB_REPO_SLUG`, `GCP_WIF_POOL_ID`, `GCP_WIF_PROVIDER_ID`.

Bypass in emergencies only: `git push --no-verify`

## 6) First Deploy (CI path)
- Push to `main` → Actions “Deploy to Cloud Run” builds and deploys.
- Check the job logs for “Service URL: …”.

## 7) Manual Deploy (optional)
Use the helper script if you want to deploy from local once:
- `scripts/deploy_cloud_run.sh <PROJECT_ID> <REGION> <SERVICE_NAME>`
  - Builds the image, pushes to Artifact Registry, and deploys to Cloud Run.

## 8) Local run (dev)
- Backend: `scripts/run_server.sh` builds FE then starts FastAPI.
- Frontend dev: `npm run dev` in `frontend/` (uses Vite dev server).

## Troubleshooting
- CI “unauthorized_client / attribute condition” → you’re on OIDC without a proper provider condition. Either switch to SA (as above) or fix WIF (see Appendix A).
- Cloud Run permission errors → ensure the SA has the three roles listed.
- Artifact Registry errors → ensure AR API is enabled; region matches `GCP_REGION`; AR repo auto-creates on first run.
- Pre‑push hook fails Dockerfile check → ensure the literal `python -m server.main` appears (shell-form is accepted).

## Changes captured in this repo (what we modified)
- CI now uses Service Account JSON auth (`credentials_json`) instead of OIDC.
- Pre‑push hook updated to support both SA and WIF modes, with clear messages.
- Dockerfile entrypoint switched to shell‑form `CMD python -m server.main` for robust detection.
- Infra scripts consolidated under `scripts/` and `infra/` directories.
- Docs refreshed to reflect the above.

---
## Appendix A – Optional OIDC (Workload Identity Federation)
If you prefer keyless auth later, you can set up WIF and flip workflows back to OIDC.

Quick path:
- Run: `scripts/setup_wif.sh <PROJECT_ID> <GITHUB_OWNER/REPO> [POOL_ID] [PROVIDER_ID] [SA_NAME]`
  - Creates pool, provider (issuer: GitHub OIDC), SA, role bindings, and WIF binding.
  - Restricts trust to `attribute.repository=='<GITHUB_OWNER/REPO>'`.
- Update workflows to use OIDC:
  - `google-github-actions/auth@v2` with:
    - `workload_identity_provider: projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_ID/providers/$PROVIDER_ID`
    - `service_account: <SA_EMAIL>`
  - Remove `credentials_json` usage.
- Remove `GCP_SA_KEY` secret (no longer needed).

Hook behavior in OIDC mode:
- Ensures `workload_identity_provider` exists in workflows.
- Reads provider attribute condition and verifies it matches your repo.
- Verifies `roles/iam.workloadIdentityUser` binding for your repo on the SA.
