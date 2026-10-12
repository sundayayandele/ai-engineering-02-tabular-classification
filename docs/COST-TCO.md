# Total Cost of Ownership — Scenario Comparison

These figures are **illustrative planning assumptions in EUR/month, not live vendor quotes**. Region, discounts, tax, egress, support, backups, retention, workload and existing infrastructure materially change actual costs. No billable resources are provisioned by this repository.

## Inputs
730 hours/month; CPU-only inference; 2–3 service replicas in pilot/production; small artifact (<100 MB); external managed or existing metrics infrastructure.

| Cost component (EUR/mo) | Local / private cloud | Self-hosted VPS | AWS managed | Azure managed | GCP managed |
|---|---:|---:|---:|---:|---:|
| Compute / node allocation | 25 | 45 | 75 | 80 | 75 |
| Cluster / control-plane allocation | 0 | 0 | 75 | 75 | 75 |
| Storage, registry, backups | 10 | 15 | 25 | 25 | 25 |
| Network / ingress / egress | 5 | 10 | 25 | 25 | 25 |
| Observability / operations tooling | 10 | 10 | 35 | 35 | 35 |
| **Illustrative infrastructure total** | **50** | **80** | **235** | **240** | **235** |

Cloud columns assume a paid managed-control-plane allowance and are **not official provider pricing**. On-prem excludes hardware depreciation beyond allocation; VPS excludes a managed HA control plane. Public cloud examples exclude premium support and enterprise security products.

## Labor-inclusive sensitivity
Assume 4 engineer-hours/month at €75/hour for local/VPS and 3 hours/month for managed cloud, purely as illustrative assumptions.

| Scenario | Infrastructure | Labor | Indicative TCO |
|---|---:|---:|---:|
| Local / private cloud | €50 | €300 | **€350/mo** |
| VPS | €80 | €300 | **€380/mo** |
| AWS | €235 | €225 | **€460/mo** |
| Azure | €240 | €225 | **€465/mo** |
| GCP | €235 | €225 | **€460/mo** |

## Recalculate
`monthly_cost = sum(hourly_resources * 730) + storage + network + telemetry + backups + support + labor`.

Use vendor calculators before a purchasing decision: AWS Pricing Calculator, Azure Pricing Calculator, Google Cloud Pricing Calculator. Run load tests and adjust instance size, zones, observability retention and RPS assumptions.

No claims are made that any one provider is cheapest for a specific region or workload.
