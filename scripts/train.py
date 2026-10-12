from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from churn_classifier.evaluation import evaluate
from churn_classifier.model import ChurnModel, build_pipeline, prepare_data


def train(path: str, output: str = "artifacts/churn_pipeline.joblib") -> dict:
    features, target = prepare_data(pd.read_csv(path))
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42, stratify=target
    )
    pipeline = build_pipeline(x_train)
    pipeline.fit(x_train, y_train)
    probability = pipeline.predict_proba(x_test)[:, 1]
    report = evaluate(y_test.to_numpy(), probability)
    model = ChurnModel(
        pipeline=pipeline,
        feature_columns=x_train.columns.tolist(),
        numeric_columns=x_train.select_dtypes(include="number").columns.tolist(),
    )
    model.save(output)
    Path(output).with_name("evaluation.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="artifacts/churn_pipeline.joblib")
    args = parser.parse_args()
    print(json.dumps(train(args.data, args.output), indent=2))
