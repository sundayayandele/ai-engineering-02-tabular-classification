# ADR-001 — CPU-first baseline

**Status:** Accepted for educational baseline.

Use leakage-safe scikit-learn preprocessing and class-balanced logistic regression for explainability, small artifact size, low cost and reproducible local training. Benchmark XGBoost/LightGBM as challengers only after real-data validation. Promotion requires a held-out improvement and measured latency/cost impact.
