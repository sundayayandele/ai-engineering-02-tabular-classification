# Security Baseline and Gaps

- Never commit raw customer records, credentials, model binaries or Terraform state.
- Joblib uses pickle serialization; load only verified artifacts from a trusted source.
- Gateway authentication, rate limits and TLS termination are required before exposing the API publicly; not implemented in FastAPI.
- Keep raw input out of logs, traces and metric labels.
- Enforce least privilege, workload identity, signed immutable images and vulnerability scanning.
- Review retention, lawful basis, PII minimization and GDPR obligations for real customer datasets.
- The current manifests are starter examples and do not establish a complete zero-trust deployment.
