#!/usr/bin/env bash
set -euo pipefail

# Setup Workload Identity Federation (OIDC) for GitHub Actions → Google Cloud.
# Creates a pool + OIDC provider that trusts your GitHub repo, a deploy service
# account with required roles, and binds WorkloadIdentityUser so Actions can
# impersonate that service account without JSON keys.
#
# Usage (defaults hardcoded for convenience):
#   scripts/setup_wif.sh [PROJECT_ID] [GITHUB_OWNER/REPO] [POOL_ID=github-pool] [PROVIDER_ID=github] [SA_NAME=padai-deployer]
#
# Defaults (you can just run the script without args):
#   PROJECT_ID          = personal-457416
#   GITHUB_OWNER/REPO   = bhi5hmaraj/tensegrity
#   POOL_ID             = github-pool
#   PROVIDER_ID         = github
#   SA_NAME             = padai-deployer
#
# After running, add these to GitHub Actions secrets:
#   - GCP_PROJECT_ID            = <PROJECT_ID>
#   - GCP_PROJECT_NUMBER        = <returned>
#   - GCP_SERVICE_ACCOUNT_EMAIL = <returned>
#   - GCP_REGION                = us-central1 (or your region)
# And in your workflow use google-github-actions/auth@v2 with:
#   workload_identity_provider: projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_ID/providers/$PROVIDER_ID
#   service_account: $SA_EMAIL

# Accept args but fall back to hardcoded defaults so you don't have to pass anything.
PROJECT_ID="${1:-personal-457416}"
REPO="${2:-bhi5hmaraj/tensegrity}"    # e.g., owner/name
POOL_ID="${3:-github-pool}"
PROVIDER_ID="${4:-github}"
SA_NAME="${5:-padai-deployer}"

echo "→ Using configuration:"
echo "   PROJECT_ID            = $PROJECT_ID"
echo "   GITHUB_OWNER/REPO     = $REPO"
echo "   POOL_ID               = $POOL_ID"
echo "   PROVIDER_ID           = $PROVIDER_ID"
echo "   SA_NAME               = $SA_NAME"

PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
WIP_PATH="projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_ID"
PROVIDER_PATH="$WIP_PATH/providers/$PROVIDER_ID"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

# Create pool (idempotent)
if ! gcloud iam workload-identity-pools describe "$POOL_ID" --project "$PROJECT_ID" --location global >/dev/null 2>&1; then
  echo "→ Creating Workload Identity Pool: $POOL_ID"
  gcloud iam workload-identity-pools create "$POOL_ID"     --project "$PROJECT_ID"     --location global     --display-name "GitHub OIDC"
else
  echo "✓ Pool exists: $POOL_ID"
fi

# Create provider (idempotent); restrict to this repo via attribute.condition
if ! gcloud iam workload-identity-pools providers describe "$PROVIDER_ID"   --project "$PROJECT_ID" --location global --workload-identity-pool "$POOL_ID" >/dev/null 2>&1; then
  echo "→ Creating OIDC Provider: $PROVIDER_ID (repo=$REPO)"
  gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID"     --project "$PROJECT_ID"     --location global     --workload-identity-pool "$POOL_ID"     --display-name "GitHub"     --issuer-uri "https://token.actions.githubusercontent.com"     --attribute-mapping "google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref"     --attribute-condition "attribute.repository=='$REPO'"
else
  echo "✓ Provider exists: $PROVIDER_ID"
fi

# Service account (idempotent)
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project "$PROJECT_ID" >/dev/null 2>&1; then
  echo "→ Creating Service Account: $SA_EMAIL"
  gcloud iam service-accounts create "$SA_NAME" --project "$PROJECT_ID" --display-name "PadAI Deployer (GitHub OIDC)"
else
  echo "✓ Service Account exists: $SA_EMAIL"
fi

# Grant required roles
for ROLE in roles/run.admin roles/artifactregistry.writer roles/iam.serviceAccountUser; do
  echo "→ Ensuring $ROLE on project for $SA_EMAIL"
  gcloud projects add-iam-policy-binding "$PROJECT_ID"     --member "serviceAccount:$SA_EMAIL"     --role "$ROLE" >/dev/null
done

# Allow GitHub identities to impersonate the SA
echo "→ Binding WorkloadIdentityUser to $SA_EMAIL for $REPO"
MEMBER="principalSet://iam.googleapis.com/$WIP_PATH/attribute.repository/$REPO"
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL"   --project "$PROJECT_ID"   --role roles/iam.workloadIdentityUser   --member "$MEMBER" >/dev/null

echo ""
echo "✓ Workload Identity Federation setup complete."
echo ""
echo "Set these GitHub repo secrets:"
echo "  GCP_PROJECT_ID:        $PROJECT_ID"
echo "  GCP_PROJECT_NUMBER:    $PROJECT_NUMBER"
echo "  GCP_SERVICE_ACCOUNT_EMAIL: $SA_EMAIL"
echo "  GCP_REGION:            us-central1 (or your region)"
echo ""
echo "Use in workflow (google-github-actions/auth@v2):"
echo "  workload_identity_provider: $PROVIDER_PATH"
echo "  service_account:           $SA_EMAIL"
echo ""
echo "Example auth step:"
echo "  - uses: google-github-actions/auth@v2"
echo "    with:"
echo "      workload_identity_provider: $PROVIDER_PATH"
echo "      service_account: $SA_EMAIL"
echo "      token_format: access_token"
