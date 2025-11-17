# Postmortem: GitHub Actions Deploy Failures (Cloud Run)

Date: 2025-11-17
Owner: Tensegrity/PadAI

## Summary
Initial CI/CD runs to Google Cloud Run failed repeatedly due to a combination of IAM, configuration, and Dockerfile issues. We fixed auth, permissions, resource existence checks, and Dockerfile problems; added debug logging; enforced a single Dockerfile; and documented one-time project setup. CI is now stable.

## At‑a‑Glance Summary

| Issue | Symptom in CI/Logs | Root Cause | Fix/Change | Owner | Status |
|------|---------------------|------------|------------|-------|--------|
| OIDC unauthorized_client | google-github-actions/auth: unauthorized_client | WIF provider attribute condition didn’t match repo | Switched to Service Account JSON auth; added `scripts/setup_wif.sh` for future WIF | Infra | Mitigated (SA); WIF optional later |
| Cannot enable/list services | Permission denied to enable/list services | SA lacks Service Usage roles | Make API enablement best‑effort; document one‑time Owner enable | Project Owner | Documented; run once per project |
| AR repo missing | name unknown: Repository not found | Repo not created and SA lacked AR admin | Early repo existence check + instructions or grant AR admin | Project Owner | Fixed (docs + guard) |
| Dockerfile HEALTHCHECK parse error | “unknown instruction: import” | Python heredoc after HEALTHCHECK | Use curl one‑liner healthcheck | App | Fixed |
| CMD check mismatch | Pre‑push blocked exec‑form CMD | Hook only matched shell‑form | Hook accepts shell + exec; Dockerfile uses exec‑form | App | Fixed |
| Naming drift (padai vs tensegrity) | Mixed names in AR paths/services | Inconsistent renames | Renamed services/repo env to “tensegrity” | App | Fixed |
| Debug steps failing | services list 403 aborted job | SA lacked viewer | Guard debug steps; suggest roles/viewer | Infra | Mitigated |
| bd not usable / DB not found | 500 on /api/status, bd failed: no database | bd not initialized / DB env not set | Official installer; set `BEADS_DIR`; run `bd init` + import at build | App | Fixed |
| Drift across environments | Surprises between local/CI/prod | Multiple Dockerfiles and no smoke | Single root Dockerfile; pre‑push Docker build smoke test; `docker_smoke.sh` | App | Fixed |

## Impact
- PR and main branch deploys failed for multiple pushes.
- No production previews; manual debugging required.

## Timeline (UTC)
- T0: CI fails with OIDC unauthorized_client (WIF attribute condition not met).
- T0+1: Switched CI to Service Account JSON auth; pre-push hook updated to allow SA mode.
- T0+2: CI fails enabling services (Service Usage permissions missing).
- T0+3: CI fails creating Artifact Registry repo (AR admin missing) and later push fails with "Repository not found".
- T0+4: Docker build fails on HEALTHCHECK heredoc (parser sees `import` as instruction).
- T0+5: Pre-push hook blocks due to exec-form CMD; adjusted to accept shell/exec forms.
- T0+6: Renaming inconsistency (padai vs tensegrity) causes AR path/service name confusion.
- T0+7: Added gcloud debug output; guarded listing steps to not fail on insufficient permissions.
- T0+8: CI succeeds after manual project setup and AR repo creation.

## Root Causes
1) OIDC (WIF) attribute condition mismatch
- Provider condition didn’t match the repo (`attribute.repository=='bhi5hmaraj/tensegrity'`), causing unauthorized_client.

2) Insufficient SA permissions for project setup
- Deployer SA lacked Service Usage and Artifact Registry Admin; it could not enable APIs or create the AR repo.

3) Missing Artifact Registry repository
- The workflow attempted to create the repo, but without AR admin the step failed; image push then failed with "name unknown: Repository not found".

4) Dockerfile issues
- HEALTHCHECK heredoc used Python; Dockerfile parser treated "import" as an instruction → build error.
- Pre-push check initially only recognized shell-form CMD; using exec-form triggered a false negative.

5) CI steps failing on read-only operations
- `gcloud services list --enabled` failed under SA due to missing viewer/serviceusage.viewer; job aborted.

6) Naming drift
- Mixed "padai" and "tensegrity" names caused confusion in AR paths and service names.

## Contributing Factors
- No early repo existence check in CI before build/push.
- No single source Dockerfile guard; risk of drift.
- Lack of explicit project setup script for one-time API enable/repo create.
- Minimal debug output made diagnosis slow.

## What We Changed (Remediations)
- Auth: Switched CI to Service Account JSON (`GCP_SA_KEY`); pre-push detects SA/WIF modes.
- Permissions: Made API enablement best-effort; added explicit instructions for Owner to enable APIs and create the AR repo.
- AR Repo: CI now verifies repo existence and fails early with clear guidance.
- Dockerfile: Replaced HEALTHCHECK heredoc with curl; standardized to exec-form CMD; set `PORT=8080` and `BEADS_DIR=/workspace/.beads`.
- Naming: Renamed Cloud Run services and AR repo to "tensegrity" across workflows.
- Debugging: Enabled `CLOUDSDK_CORE_VERBOSITY=debug` and `CLOUDSDK_CORE_LOG_HTTP=true`; added context dumps and listings.
- Guardrails: Pre-push runs a Docker build smoke test; enforces a single root Dockerfile.
- Docs: Added replication checklist and updated CI/CD and Cloud Run docs.

## Verification
- Local: `scripts/docker_smoke.sh` builds image, runs container, and probes `/`, `/api/health`, `/api/status`, `/api/tasks` successfully.
- CI: After project Owner enabled APIs and created AR repo `tensegrity`, deploys succeed.

## Action Items
- Must (Project Owner, one-time)
  - Enable required APIs:
    - `gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com --project personal-457416`
  - Create Artifact Registry repo (or grant AR admin to CI SA):
    - `gcloud artifacts repositories create tensegrity --repository-format=docker --location=us-central1 --project personal-457416`

- Optional (Security/Convenience)
  - Switch back to keyless OIDC (WIF) once provider condition is set correctly.
    - Use `scripts/setup_wif.sh` to create/repair pool/provider and bindings.
  - Grant minimal viewer permissions to CI SA so debug listings don’t warn.
    - `roles/viewer` or narrower `roles/serviceusage.serviceUsageViewer`.

- CI Hardening
  - Add a container smoke test step (docker run -> curl /api/health & /api/status) before deploy.
  - Keep early-fail repo existence check.

- Process/Docs
  - Keep `docs/REPLICATION_CHECKLIST.md` up-to-date for new projects.
  - Maintain a single Dockerfile; pre-push ensures no drift.

## Lessons Learned
- WIF is great but brittle without correct attribute conditions; verify with a script and pre-push checks.
- CI SAs should not do project setup; have Owners enable APIs and create AR repos once, or give the SA scoped admin for that action.
- Fail early with precise guidance (repo existence, API enablement) to avoid wasting build minutes.
- Prefer exec-form CMD for signal handling; keep HEALTHCHECK simple (curl) to avoid Dockerfile parser pitfalls.
- A single Dockerfile across local/CI/prod prevents configuration drift.

## References
- CI Workflow: `.github/workflows/cloud-run.yml`
- Local Smoke: `scripts/docker_smoke.sh`
- Project Setup: `docs/REPLICATION_CHECKLIST.md`, `scripts/setup_wif.sh`
