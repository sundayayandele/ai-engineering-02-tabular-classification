"""Generate synthetic churn-like rows for CI smoke tests, not real-world validation."""

from pathlib import Path

import numpy as np
import pandas as pd


def generate(rows: int = 400, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 73, size=rows)
    monthly = rng.uniform(20, 120, size=rows).round(2)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], size=rows)
    score = -0.025 * tenure + 0.012 * monthly + 0.8 * (contract == "Month-to-month")
    probability = 1 / (1 + np.exp(-score))
    churn = np.where(rng.random(rows) < probability, "Yes", "No")
    return pd.DataFrame({
        "customerID": [f"SYN-{i:05d}" for i in range(rows)],
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "TotalCharges": (tenure * monthly).round(2),
        "Contract": contract,
        "Churn": churn,
    })


if __name__ == "__main__":
    target = Path("data/synthetic/churn.csv")
    target.parent.mkdir(parents=True, exist_ok=True)
    generate().to_csv(target, index=False)
    print(f"Generated synthetic smoke-test data at {target}")
