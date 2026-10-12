# Model Card — Baseline v1

**Task:** Binary customer churn prediction; output probability and thresholded class.

**Intended use:** Decision support for authorized customer-success staff.

**Not intended:** Fully automated denial of service, eligibility, credit, employment or other consequential decisions.

**Architecture:** Scikit-learn preprocessing pipeline + class-balanced logistic regression.

**Training data:** User-supplied licensed CSV or synthetic smoke-test data; actual provenance must be recorded per run.

**Evaluation:** Stratified holdout with accuracy, precision, recall, F1, ROC-AUC, PR-AUC, Brier score and confusion matrix. Record split seed and data checksum for production experiments.

**Known limitations:** Label leakage risk, dataset shift, unmeasured fairness, calibration, class prevalence changes, missing values, stale features and potential privacy implications.

**Promotion:** Requires business-specific thresholds, privacy review, calibration check, representative real-world evaluation and monitored rollback.
