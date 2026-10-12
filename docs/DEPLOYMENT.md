# Deployment Paths

## Educational
Install `pip install -e '.[dev]'`; generate synthetic data, train and run Uvicorn. The generated joblib artifact is local-only.

## Docker
Train first, then run `docker compose up --build`. The Compose configuration mounts `./artifacts` read-only. The image itself does not contain a model artifact.

## Kubernetes / OpenShift
The manifests are **reference starters**. Production deployment is blocked until a trusted model artifact is mounted or packaged, immutable image digest is specified, ingress authentication is configured, resource sizing validated, and network/secret policy reviewed.

## Cloud
Terraform/OpenTofu modules under `terraform/` provision **container registries only**. They do not create EKS/AKS/GKE clusters, VPCs/VNets, identity, DNS, monitoring or a running application. Infrastructure creation incurs charges; use plan and explicit approval.
