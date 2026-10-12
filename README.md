# Project 02 — Enterprise Tabular ML Classification

Production-oriented **customer churn prediction** with portfolio learning and enterprise reference tracks.

## Data
Reference dataset: IBM Telco Customer Churn. Obtain the CSV from its authorized source and place it at `data/raw/telco_churn.csv` (not committed). Verify source licensing and suitability before commercial use.

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
![Architecture Diagrams](/diagrams/source/Enterprise%20Churn%20Prediction%20Architecture%20Triptych.png)
![Architecture Diagrams](/diagrams/source/Kubernetes%20Churn%20Prediction%20Architecture.png)

## Status
Initial source is being uploaded from the mobile-friendly connected GitHub workflow. The full prepared ZIP is available in the chat. Production readiness requires full CI, security and infrastructure validation.

## License
MIT for source code. Dataset and model licenses are separate.
