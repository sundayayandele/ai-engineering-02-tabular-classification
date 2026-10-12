# Project 02 — Enterprise Tabular ML Classification

Production-oriented **customer churn prediction** with portfolio learning and enterprise reference tracks.

## Data
Reference dataset: IBM Telco Customer Churn. Obtain the CSV from its authorized source and place it at `data/raw/telco_churn.csv` (not committed). Verify source licensing and suitability before commercial use.

## Hands-on learner labs — Docker Desktop, Rancher Desktop, Podman Desktop, Postman and GitHub runners

**Two tracks remain:** Educational/Portfolio labs below; Enterprise/Production is the documented reference architecture and must be independently validated before deployment.

### Hardware and resource sizing

| Profile | CPU | RAM | Free disk |
|---|---|---|---|
| Single API container | 1 vCPU | 1 GiB | 5–10 GiB |
| Recommended desktop host | 2–4 logical CPUs | 8 GiB (16 GiB preferred) | 15–25 GiB |
| Desktop container engine VM (Windows/macOS) | 2–4 CPUs | 4 GiB minimum, 6–8 GiB comfortable | 15–25 GiB |
| Two-replica local simulation | 2 CPU total | 2 GiB total container limits, plus engine/host overhead | 15–25 GiB |

These are initial **learning estimates**, not measured production requirements. No GPU needed. For enterprise sizing and costs see [capacity planning](docs/infrastructure/CAPACITY-PLANNING.md) and [TCO](docs/COST-TCO.md).

### Step 1 — Fork, clone and prepare your model

Fork this repository, clone **your fork** and create a `learner/desktop-lab` branch. Install Git and Python 3.12:

```bash
git clone https://github.com/YOUR_USERNAME/ai-engineering-02-tabular-classification.git
cd ai-engineering-02-tabular-classification
git switch -c learner/desktop-lab
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/generate_synthetic.py
python scripts/train.py --data data/synthetic/churn.csv
pytest -q
```

Windows PowerShell: `py -3.12 -m venv .venv` then `.venv\\Scripts\\Activate.ps1`. Confirm `artifacts/churn_pipeline.joblib` exists. Project 02's model is mounted from the host, not baked into the container. On SELinux hosts, a :ro,Z mount may be necessary.

### Step 2A — Docker Desktop

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), start the Linux container engine and allocate at least **2 CPUs, 4 GiB RAM and 15 GiB disk** where supported (WSL2 limits may be configured separately). Verify `docker version` and `docker compose version`, then:

```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml ps
docker compose -f docker-compose.yml logs --tail=50
```

For a local-only lab, change the Compose port binding from `8000:8000` to `127.0.0.1:8000:8000` before starting, to avoid listening on all host interfaces.

### Step 2B — Rancher Desktop

Install [Rancher Desktop](https://rancherdesktop.io/), select **dockerd (moby)** engine, start the app, configure the VM resources (2+ CPUs, 4+ GiB RAM), and verify `docker version` and `docker compose version`. Use the **same Compose commands from Step 2A**. Optional Kubernetes is a learning cluster, not multi-node HA.

### Step 2C — Podman Desktop

Install [Podman Desktop](https://podman-desktop.io/), complete onboarding, and on Windows/macOS start a **Podman machine**. Confirm `podman version` and `podman info`. From the repository root:

```bash
podman build -t project02-churn:local .
podman run -d --name project02-api -p 127.0.0.1:8000:8000 --cpus 1 --memory 1g -e MODEL_PATH=/app/artifacts/churn_pipeline.joblib -v "$PWD/artifacts:/app/artifacts:ro" project02-churn:local
podman ps
podman logs project02-api
podman stats --no-stream project02-api
```

Podman machine host-volume sharing depends on OS and VM settings. See the detailed guide for troubleshooting, SELinux and Windows paths.

### Step 3 — Postman API test

1. Verify `GET http://127.0.0.1:8000/health/live` and `GET http://127.0.0.1:8000/health/ready` return HTTP 200.
2. Open `http://127.0.0.1:8000/docs` to inspect the API.
3. In **Postman**, create **POST** `http://127.0.0.1:8000/predict` → **Body → raw → JSON** and paste:

```json
{"features":{"tenure":12,"MonthlyCharges":75,"TotalCharges":900,"Contract":"Month-to-month"}}
```

4. Click **Send**; expect HTTP 200 with prediction fields. Capture logs and screenshots as portfolio evidence.
5. Cleanup: `docker compose -f docker-compose.yml down` (Docker/Rancher) or `podman rm -f project02-api` (Podman).

### Step 4 — GitHub-hosted runner lab (no desktop installation)

1. Fork the repository; create branch `learner/github-runner-lab` and enable **Actions** in your fork after reviewing the workflows.
2. Commit a small code change or open a pull request; inspect the **ci** run and record the SHA, logs and result.
3. Open **Actions → small-pilot-lab → Run workflow**, select your learner branch and run the two-container, resource-limited pilot simulation. Review resource measurements and API checks.
4. Check GitHub's current Actions free-runner eligibility, minutes and billing settings. A hosted runner is temporary, not persistent hosting or genuine HA.

**Detailed step-by-step guide:** [Desktop containers, Postman and GitHub runner lab](docs/learning/DESKTOP-CONTAINERS-AND-RUNNERS-LAB.md).

## Quick start
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python scripts/generate_synthetic.py
python scripts/train.py --data data/synthetic/churn.csv
uvicorn app.main:app --reload
pytest -q
```

Synthetic data is **for smoke tests only**, not evidence of real-world accuracy.

## API
- `GET /health/live`
- `GET /health/ready`
- `POST /predict` with `{"features":{"tenure":12,"MonthlyCharges":75,"Contract":"Month-to-month"}}`
- `GET /metrics`

## Model
Scikit-learn preprocessing (numeric imputation and scaling, categorical imputation and one-hot encoding) plus class-balanced logistic regression. The `customerID` and `Churn` columns are excluded from predictors. Use held-out evaluation, ROC-AUC, PR-AUC, F1, Brier score and cost-sensitive decision thresholds.

## Engineering standards
Python 3.12; FastAPI; pytest; Ruff; Prometheus; Docker; Kubernetes/OpenShift; cloud-neutral architecture with Terraform/OpenTofu examples. Model binaries, sensitive data, cloud secrets and generated artifacts must never be committed.

## Architectures and Infographics
![Architecture Diagrams](/diagrams/source/Customer%20Churn%20Architecture%20Blueprint.png)


![Architecture Diagrams](/diagrams/source/Machine%20Learning%20Pipeline%20Infographic.png)


![Architecture Diagrams](/diagrams/source/Kubernetes%20Churn%20Prediction%20Architecture.png)

## Learner guide — test your own branch with GitHub-hosted runners

You do **not** need a laptop, paid VPS, or cloud account for the basic educational labs. Learners can use a **personal fork** of this public repository and run tests on GitHub's standard hosted runners, subject to GitHub's current Actions eligibility and billing rules.

### 1. Fork the repository (Android or desktop)

1. Sign in to GitHub and open [this repository](https://github.com/sundayayandele/ai-engineering-02-tabular-classification).
2. Select **Fork → Create a new fork** under your own GitHub account.
3. Open **your fork**. Its default `main` branch is your own copy; you do not need write access to the original repository.
4. For isolated experiments, select the branch dropdown (usually **main**) → **View all branches → New branch**. Name it `learner/first-lab` and base it on `main`.
5. Edit files on **your branch**, using GitHub's web editor or the pencil icon. Commit changes to `learner/first-lab`, **not** the upstream repository.

On Android, if a GitHub control is hidden, open the page in Chrome and select **Desktop site**. The GitHub mobile app may expose fewer workflow controls than the browser.

### 2. Enable Actions in your fork

1. Open **your fork → Actions**.
2. If GitHub asks you to enable workflows for the fork, review the workflow files first, then choose **I understand my workflows, go ahead and enable them** (wording may vary).
3. Check **Settings → Actions → General** to ensure standard GitHub-hosted runners are allowed.
4. Check **Settings → Billing and plans → Actions** for your current plan, minutes, storage and spending limits. GitHub's standard runner usage for public repositories is generally free under its published policies; **fork visibility and billing conditions matter**, and larger runners or external infrastructure may cost money.

**Security:** Forked workflows can execute code. Do not add secrets, customer data, cloud credentials or untrusted third-party actions to your learning branch.

### 3. Run code quality and educational tests

- **Automatic branch test:** Commit a change to your `learner/first-lab` branch. The [CI workflow](.github/workflows/ci.yml) runs on pushes and pull requests; select **Actions → ci** in your fork to inspect the result.
- **Training smoke test:** The [education-smoke workflow](.github/workflows/education.yml) generates synthetic data, trains the classifier, performs a prediction and runs pytest. It runs on relevant source changes and pull requests.
- **View evidence:** Open a workflow run → job → step logs. Record the commit SHA, test results, training metrics and run URL in your portfolio.
- **Share improvements:** Optionally create a pull request **within your fork**, from `learner/first-lab` into your fork's `main`. Only submit a pull request to the original repository if you intend to propose a contribution.

**Important:** A manually triggered workflow normally runs against the selected branch **only if that workflow file is present on the fork's default branch**. For the small-pilot lab, select your `learner/first-lab` branch in the **Run workflow** dropdown after enabling the workflow in your fork.

### 4. Simulate the small pilot on a free-tier-eligible runner

Open **your fork → Actions → small-pilot-lab → Run workflow**, choose `learner/first-lab`, then select **Run workflow**.

The [small-pilot-lab workflow](.github/workflows/small-pilot-lab.yml) builds and tests the application, then starts two temporary Docker containers with CPU and memory limits:

| Target | Educational runner simulation | What it proves |
|---|---|---|
| 2 replicas | 2 containers on one hosted runner | Both API instances start and respond |
| 0.5–1 vCPU per replica | `--cpus=0.5` each | CPU throttling under a defined container limit |
| 1 GiB RAM per replica | `--memory=1g` each | Operation within the configured memory ceiling |
| 10–20 GiB storage | Inspect `df -h` on the ephemeral runner | Actual free disk; **10–20 GiB is not guaranteed** |
| Low-traffic HA pilot | 40 bounded prediction requests split across both containers | Functional/load smoke test; **not genuine high availability** |

These containers share a single temporary runner and stop when the job ends. For real high availability, use multiple worker nodes/failure domains in Kubernetes/OpenShift; GitHub Actions is a testing and deployment service, not a persistent application hosting platform.

### 5. Suggested learning exercises

1. Modify the model features and run CI on your branch.
2. Compare precision, recall, F1, ROC-AUC and PR-AUC on synthetic smoke-test data.
3. Change the decision threshold and discuss false-positive/false-negative costs.
4. Inspect the pilot workflow's `docker stats`, CPU/memory limits, request timings and available disk.
5. Document what the simulated pilot **cannot** prove: availability, realistic accuracy, fairness, security and production readiness.

Use a properly licensed real dataset only when authorized and keep it **outside Git**. Synthetic data is for reproducibility and smoke tests, not evidence of production model quality.

### Further reading

- [Detailed step-by-step GitHub-hosted runner lab](docs/learning/GITHUB-FREE-RUNNERS-SMALL-PILOT-LAB.md)
- [Educational learning guide](docs/learning/LEARNING-GUIDE.md)
- [Infrastructure capacity planning](docs/infrastructure/CAPACITY-PLANNING.md)
- [Infrastructure and TCO comparison](docs/COST-TCO.md)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [GitHub Actions billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

## Status
Initial source is being uploaded from the mobile-friendly connected GitHub workflow. The full prepared ZIP is available in the chat. Production readiness requires full CI, security and infrastructure validation.

## License
MIT for source code. Dataset and model licenses are separate.
