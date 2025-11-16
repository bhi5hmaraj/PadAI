variable "project_id" { type = string }
variable "region" { type = string  default = "us-central1" }
variable "repo_name" { type = string default = "padai" }
variable "service_main" { type = string default = "padai" }
variable "service_preview" { type = string default = "padai-preview" }
variable "github_owner" { type = string }
variable "github_repo" { type = string }
