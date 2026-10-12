# TOGAF 10 Architecture Viewpoints — Project 02

This is a TOGAF 10-aligned *reference interpretation*, not a formal certification or complete ADM execution.

| ADM phase | Project artifact / decision |
|---|---|
| Preliminary | Architecture principles: privacy, portability, reproducibility, measurable business value |
| A — Vision | Reduce preventable customer churn through decision support, not automated adverse action |
| B — Business | Customer-success analyst reviews prioritized churn scores and chooses interventions |
| C — Information Systems | Governed tabular dataset, training pipeline, model artifact, prediction API |
| D — Technology | Python, Docker, Kubernetes/OpenShift, metrics and cloud-neutral registries |
| E/F — Opportunities and Migration | Educational baseline → secured enterprise pilot → production |
| G — Implementation Governance | CI checks, model approval, image digest, audit trail, change management |
| H — Change Management | Monitor drift, model quality, cost, privacy and retraining triggers |
| Requirements Management | Trace each control to model card, tests, ADR and operational evidence |

## Stakeholders
Customer success, ML engineer, platform engineer, security officer, privacy lead, finance owner.

## Quality attributes
Availability, explainability, integrity, data minimization, portability, repeatability and cost visibility.

## Governance gates
1. Dataset provenance and rights.
2. Reproducible held-out evaluation with business-specific acceptance criteria.
3. Security and privacy review.
4. Model artifact signing/approval and deployment rollback plan.
5. Monitored canary deployment with documented owner.

See `diagrams/source/enterprise-architecture.mmd`, `logical-architecture.mmd`, `technical-architecture.mmd` and C4 diagrams.
