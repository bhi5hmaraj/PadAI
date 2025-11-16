terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "run" { project = var.project_id service = "run.googleapis.com" }
resource "google_project_service" "ar"  { project = var.project_id service = "artifactregistry.googleapis.com" }
resource "google_project_service" "cb"  { project = var.project_id service = "cloudbuild.googleapis.com" }

# Artifact Registry repository for images
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repo_name
  format        = "DOCKER"
  description   = "PadAI containers"
  depends_on    = [google_project_service.ar]
}

# Cloud Build service account permissions
data "google_project" "proj" {}

resource "google_project_iam_member" "cb_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project.proj.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cb_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${data.google_project.proj.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cb_ar_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${data.google_project.proj.number}@cloudbuild.gserviceaccount.com"
}

# Cloud Build GitHub triggers (requires GitHub App connection)
resource "google_cloudbuild_trigger" "main" {
  name        = "padai-main"
  description = "Build and deploy main to Cloud Run"

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^main$"
    }
  }

  filename   = "infra/cloudbuild/cloudbuild-main.yaml"
  substitutions = {
    _REGION  = var.region
    _REPO    = var.repo_name
    _SERVICE = var.service_main
  }

  depends_on = [google_project_service.cb]
}

resource "google_cloudbuild_trigger" "preview" {
  name        = "padai-preview"
  description = "Build and deploy preview branch to Cloud Run"

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^preview$"
    }
  }

  filename   = "infra/cloudbuild/cloudbuild-preview.yaml"
  substitutions = {
    _REGION  = var.region
    _REPO    = var.repo_name
    _SERVICE = var.service_preview
  }

  depends_on = [google_project_service.cb]
}

output "artifact_registry_repo" {
  value = google_artifact_registry_repository.repo.name
}

output "triggers" {
  value = {
    main    = google_cloudbuild_trigger.main.name
    preview = google_cloudbuild_trigger.preview.name
  }
}
