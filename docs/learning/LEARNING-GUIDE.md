# Educational / Portfolio Track

## Learning objectives
1. Understand churn, class imbalance and the business cost of false negatives.
2. Inspect column types, missing values, label distribution and duplicate identifiers.
3. Split data *before* fitting imputers, encoders or scalers to prevent leakage.
4. Train the baseline pipeline and compare ROC-AUC, PR-AUC, F1 and calibration.
5. Run the FastAPI prediction endpoint with a trained artifact.
6. Explain coefficients, permutation importance and limits of observational inference.
7. Document model-card limitations and deployment risk.

## Practical labs
- **Lab 1:** Run `python scripts/generate_synthetic.py`, inspect its generated columns. Synthetic results are smoke-test only.
- **Lab 2:** `python scripts/train.py --data data/synthetic/churn.csv`; inspect `artifacts/evaluation.json`.
- **Lab 3:** `MODEL_PATH=artifacts/churn_pipeline.joblib uvicorn app.main:app`; POST a JSON feature record.
- **Lab 4:** Replace synthetic data with an appropriately licensed real Telco churn CSV; compare outcomes.
- **Lab 5:** Compare class-balanced logistic regression against a gradient boosting classifier under the same stratified splits.
- **Lab 6:** Tune decision threshold using a validation set and a documented false-negative/false-positive cost matrix; never optimize on test data.
- **Lab 7:** Produce a model card, confusion matrix, error analysis and reproducibility record.

## Exit criteria
Clean CI, dataset attribution, reproducible run, metrics, API demo, documented limitations and no committed raw customer data.
