# Lab: Small-pilot simulation using GitHub-hosted runners (free-tier eligible)

**Project:** AI Engineering 02 — Customer Churn Classification  
**Track:** Educational / Portfolio  
**Goal:** Reproduce the small-pilot resource profile in CI, test the code and simulate two inference replicas without buying servers.

> **Important:** GitHub-hosted runners are temporary CI virtual machines, **not** two permanent high-availability servers. Two processes or containers on one runner do not provide real HA. The 10–20 GiB storage target is a **pilot capacity budget**, not a guarantee of free runner disk or persistent storage. The free quota, runner specifications and available disk vary by account, repository visibility, OS and GitHub policy; verify current details in GitHub Settings → Billing and plans → Actions, and in each job's setup logs. A public repository using standard GitHub-hosted runners is generally eligible for free standard-runner usage, subject to GitHub policies.

## Target and what the lab actually demonstrates

| Profile | Replicas | CPU / replica | Memory / replica | Storage | Workload |
|---|---:|---:|---:|---:|---|
| Desired small pilot | 2 | 0.5–1 vCPU | 1 GiB | 10–20 GiB | Low traffic, HA pilot |
| GitHub Actions simulation | 2 Docker containers | 0.5 CPU (Docker limit) | 1 GiB (Docker limit) | Ephemeral runner filesystem; **not** guaranteed 10–20 GiB free | Low-traffic functional and load smoke tests, **not HA** |

**Runner vs workload sizing:** A GitHub-hosted Ubuntu runner may have more CPU/RAM than the application containers. Container CPU and memory limits approximate the desired per-replica workload, but **do not reserve** dedicated CPU. The runner's available disk must be measured with `df -h` and may be below the target after checkout, tools and image layers. Do not assume a runner offers 20 GiB usable storage.

## Prerequisites

1. Open the public repository: https://github.com/sundayayandele/ai-engineering-02-tabular-classification
2. Open **Settings → Actions → General**. Confirm Actions is enabled and standard GitHub-hosted runners are permitted.
3. Open **Settings → Billing and plans → Actions** (wording may differ). Check free usage, storage and spending limits; avoid larger/GPU runners and self-hosted infrastructure for this lab.
4. Ensure `.github/workflows/ci.yml` and `.github/workflows/education.yml` exist.
5. Use only generated synthetic data. Do **not** commit real customer records, secrets, `.env`, trained `.joblib` artifacts or Terraform state.

## Lab A — Run the existing tests

1. Open the **Actions** tab.
2. Select the **ci** workflow. It runs on pushes to `main` and pull requests.
3. To trigger a fresh run without changing source, use a new pull request or add `workflow_dispatch:` to the workflow's `on:` section (the lab workflow below already supports manual runs).
4. Open the job logs. Confirm dependency installation, Ruff linting and pytest pass.
5. Select **education-smoke** and inspect its synthetic-data generation, training, prediction and test steps.
6. Capture the workflow URL, commit SHA, duration and results in your portfolio evidence.

## Lab B — Add a two-replica resource-constrained simulation

The companion workflow is `.github/workflows/small-pilot-lab.yml`. It:

- uses a standard `ubuntu-latest` GitHub-hosted runner;
- installs Python 3.12 and project dependencies;
- generates synthetic data and trains a smoke-test model;
- builds a Docker image;
- starts **two** containers, each with `--cpus=0.5 --memory=1g`, binding different localhost ports;
- mounts the trained model artifact read-only into each container;
- probes each container's liveness, readiness and prediction endpoint;
- runs a small, bounded concurrent request test;
- displays container resource usage and runner disk space;
- removes containers at the end.

**To execute on Android:** open **Actions → small-pilot-lab → Run workflow → main → Run workflow**. Refresh the run page, open the job, and review its logs. If the button is missing, check Actions permissions and that the workflow exists on the default branch.

## Lab C — Validate resources and behavior

Check the job output for:

- `docker inspect` memory limit approximately 1,073,741,824 bytes and CPU quota equivalent to 0.5 CPU per container;
- both endpoints returning HTTP 200 from `/health/live` and `/health/ready`;
- a JSON `POST /predict` response containing `churn_probability` and `model_version`;
- bounded load-test success count and latency distribution;
- `docker stats --no-stream` CPU and memory observations;
- `df -h` actual runner disk availability.

**Passing tests do not prove 24/7 uptime, high availability, failover, throughput SLOs, data security or production suitability.** Both containers share one runner and disappear when the job finishes.

## Lab D — Optional parallel jobs for fault isolation

Use a two-entry matrix (`replica: [1, 2]`) to run two **independent CI jobs**. Each job gets its own ephemeral runner, but they are not simultaneously reachable behind a shared load balancer and do not constitute a production HA pair. Matrix jobs can consume additional usage; confirm billing rules before enabling frequent runs.

## Lab E — Production-like HA, without pretending Actions is a hosting platform

For a genuine two-replica pilot, deploy to a Kubernetes/OpenShift cluster with **at least two distinct worker nodes/failure domains**, pod anti-affinity, readiness probes, a Service/Ingress, a trusted mounted model artifact, ingress authentication, network policies, metrics and rollback procedures. GitHub Actions can **test and deploy to** that cluster but should not be the cluster itself. A real HA cluster incurs separate infrastructure costs.

## Cost and quota safeguards

- Choose `runs-on: ubuntu-latest` (standard runner), not `ubuntu-latest-4-cores` or larger runners.
- Set `timeout-minutes: 20`, `permissions: contents: read` and `concurrency` to prevent runaway duplicate work.
- Do not run long-lived services after the job; no scheduled infinite loops.
- Keep synthetic data and model artifacts ephemeral; don't upload sensitive artifacts.
- Check GitHub's current pricing and your plan's usage; public-repository free eligibility does **not** make third-party cloud resources free.
- Stop/review the workflow if Docker images exhaust disk or training exceeds the timeout.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Run workflow button missing | Workflow not on default branch or Actions disabled |
| `/health/ready` returns 503 | Model file not mounted, incorrect `MODEL_PATH`, or untrusted/incompatible artifact |
| Docker exits with permission error | Check mount permissions and non-root container UID |
| `no space left on device` | Runner disk exhausted; inspect `df -h`, remove unused images, reduce artifacts |
| Containers OOM-killed | 1 GiB too small for observed workload; inspect `docker stats` and tune based on measurements |
| Slow response / failed load test | Shared CPU contention, cold start or too much concurrency; inspect logs |
| Unexpected billable usage | Review Actions billing, workflow frequency and repository visibility |

## Evidence checklist

- [ ] CI lint and unit tests pass
- [ ] Synthetic model trained and artifact loaded
- [ ] Two containers started with resource limits
- [ ] Both health/readiness/prediction checks pass
- [ ] Load smoke test recorded (request count, errors, latency)
- [ ] CPU, memory and disk observations recorded
- [ ] Limitations and no-real-HA distinction documented
- [ ] Workflow run URL and commit SHA linked in portfolio README

**Reference:** GitHub Docs — [GitHub-hosted runners](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners), [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [workflow_dispatch](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
