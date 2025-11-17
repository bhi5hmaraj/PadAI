#!/usr/bin/env bash
set -euo pipefail

echo "[prepush] Running PadAI/Tensegrity pre-push checks..."

ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# 1) Ensure workflows use OIDC (WIF), not JSON keys
if rg -n "credentials_json\s*:" .github/workflows 2>/dev/null | sed -n '1,3p'; then
  echo "[prepush][ERROR] Found credentials_json in workflows. Switch to OIDC (Workload Identity Federation)." >&2
  exit 1
else
  echo "[prepush] ✅ Workflows do not reference credentials_json"
fi

if ! rg -n "workload_identity_provider\s*:" .github/workflows >/dev/null 2>&1; then
  echo "[prepush][WARN] Workflows do not contain workload_identity_provider. Ensure OIDC auth is configured."
else
  echo "[prepush] ✅ Workflows contain workload_identity_provider"
fi

# 2) Optional GCP checks if gcloud is available
if command -v gcloud >/dev/null 2>&1; then
  PROJECT_ID=${GCP_PROJECT_ID:-personal-457416}
  POOL_ID=${GCP_WIF_POOL_ID:-github-pool}
  PROVIDER_ID=${GCP_WIF_PROVIDER_ID:-github}
  SA_NAME=${GCP_DEPLOY_SA_NAME:-tensegrity-deployer}
  REPO_SLUG=${GITHUB_REPO_SLUG:-bhi5hmaraj/tensegrity}

  echo "[prepush] gcloud present; validating WIF provider and SA in project '$PROJECT_ID'"

  set +e
  COND=$(gcloud iam workload-identity-pools providers describe "$PROVIDER_ID" \
    --project "$PROJECT_ID" --location global --workload-identity-pool "$POOL_ID" \
    --format='value(oidc.attributeCondition)' 2>/dev/null)
  RC=$?
  set -e

  if [[ $RC -ne 0 || -z "$COND" ]]; then
    echo "[prepush][WARN] Could not read provider condition for $POOL_ID/$PROVIDER_ID in $PROJECT_ID. Ensure WIF is set up."
  else
    echo "[prepush] Provider condition: $COND"
    if [[ "$COND" != *"attribute.repository=='$REPO_SLUG'"* ]]; then
      echo "[prepush][ERROR] Provider condition does not match repo '$REPO_SLUG'" >&2
      exit 1
    else
      echo "[prepush] ✅ Provider condition trusts $REPO_SLUG"
    fi
  fi

  SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
  if gcloud iam service-accounts describe "$SA_EMAIL" --project "$PROJECT_ID" >/dev/null 2>&1; then
    echo "[prepush] ✅ Service Account exists: $SA_EMAIL"
  else
    echo "[prepush][ERROR] Missing Service Account: $SA_EMAIL" >&2
    exit 1
  fi

  # Check WIF binding
  POLICY=$(gcloud iam service-accounts get-iam-policy "$SA_EMAIL" --project "$PROJECT_ID" --format=json)
  if echo "$POLICY" | rg -q "roles/iam.workloadIdentityUser" && echo "$POLICY" | rg -q "$REPO_SLUG"; then
    echo "[prepush] ✅ WorkloadIdentityUser binding present for $REPO_SLUG"
  else
    echo "[prepush][ERROR] WorkloadIdentityUser binding missing for $REPO_SLUG on $SA_EMAIL" >&2
    exit 1
  fi
else
  echo "[prepush] (gcloud not found) Skipping GCP validation."
fi

# 3) Sanity: ensure Dockerfile runs python -m server.main and uses server/requirements.txt
if ! rg -n "python -m server\.main" Dockerfile >/dev/null 2>&1; then
  echo "[prepush][ERROR] Dockerfile does not start server with 'python -m server.main'" >&2
  exit 1
else
  echo "[prepush] ✅ Dockerfile entrypoint references server.main"
fi

if ! rg -n "server/requirements\.txt" Dockerfile >/dev/null 2>&1; then
  echo "[prepush][ERROR] Dockerfile not installing from server/requirements.txt" >&2
  exit 1
else
  echo "[prepush] ✅ Dockerfile installs from server/requirements.txt"
fi

echo "[prepush] All checks passed."
