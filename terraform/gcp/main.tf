provider "google" {
  project = var.project_id
  region  = var.region
}
resource "google_artifact_registry_repository" "churn" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Project 02 customer churn prediction container images"
  format        = "DOCKER"
}
output "repository_id" {
  value = google_artifact_registry_repository.churn.id
}
