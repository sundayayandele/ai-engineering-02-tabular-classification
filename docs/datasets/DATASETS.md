# Dataset Provenance

Reference use case: IBM Telco Customer Churn (commonly published as WA_Fn-UseC_-Telco-Customer-Churn.csv). Verify the actual download host, license/terms and dataset version before using it. The repository intentionally does not redistribute the dataset.

Expected columns include `customerID`, `tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `Churn` and other telecom service fields.

Do not upload customer-identifiable records. `customerID` is dropped from training features. Consider protected attributes, fairness review and legal basis before production use.

The synthetic generator exists only for smoke testing and has no claim to match real telecom data.
