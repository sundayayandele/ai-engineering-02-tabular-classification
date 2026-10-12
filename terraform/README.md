# Terraform / OpenTofu

Starter modules for container registries only: `aws` (ECR), `azure` (ACR), `gcp` (Artifact Registry). These modules do not provision Kubernetes clusters or deploy the API.

```bash
cd terraform/aws
terraform init -backend=false
terraform fmt -check
terraform validate
terraform plan
```

OpenTofu can be used with the same HCL subject to provider compatibility. `plan` may require authenticated cloud access; do not apply without approval and a budget. Never commit `*.tfstate`.
