# Infrastructure Sizing — Initial Planning Estimates

**Planning assumptions, not benchmarks:** scikit-learn logistic-regression pipeline, CPU-only inference, model artifact under 100 MB, 2 KB request payload, no GPU, no feature-store calls. Verify memory and latency under load before production.

| Environment | Replicas | vCPU / replica | RAM / replica | Disk | Intended load |
|---|---:|---:|---:|---:|---|
| Local lab | 1 | 1 | 1 GiB | 5 GiB | Development, manual testing |
| Small pilot | 2 | 0.5–1 | 1 GiB | 10–20 GiB | Low traffic, HA pilot |
| Production baseline | 3 | 1–2 | 2 GiB | 20–50 GiB | Moderate traffic, multi-zone target |
| Scale-out | 3–10 | 2 | 2–4 GiB | 50+ GiB | Load-test-driven autoscaling |

**Not a throughput guarantee.** Measure p50/p95/p99, CPU, RSS, serialization overhead and concurrent requests using the target hardware and realistic feature cardinality.

Capacity formula: `required_replicas = ceil((peak_rps * measured_cpu_seconds_per_request) / (vCPU_per_replica * target_utilization))`. Include 30% headroom, minimum two failure-domain replicas and separate model-training resource budgets.

Storage: small model + logs/metrics; avoid persistent raw customer records in serving pods. External Prometheus, registries, ingress, load balancers and backups are additional capacity/cost items.

OpenShift restricted SCC, arbitrary UID, read-only filesystem and mounted model artifacts must be tested on a real cluster.
