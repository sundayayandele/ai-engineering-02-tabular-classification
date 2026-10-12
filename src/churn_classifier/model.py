from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

EXCLUDED = {"Churn", "customerID"}


def prepare_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    if "Churn" not in frame:
        raise ValueError("Expected a Churn target column")
    data = frame.copy()
    data["Churn"] = data["Churn"].astype(str).str.strip().str.lower().map(
        {"yes": 1, "no": 0, "1": 1, "0": 0, "true": 1, "false": 0}
    )
    if data["Churn"].isna().any():
        raise ValueError("Churn target contains missing or unexpected values")
    features = data.drop(columns=[c for c in EXCLUDED if c in data.columns])
    for column in ["TotalCharges", "tenure", "MonthlyCharges"]:
        if column in features:
            features[column] = pd.to_numeric(features[column], errors="coerce")
    return features, data["Churn"].astype(int)


def build_pipeline(features: pd.DataFrame) -> Pipeline:
    numeric = features.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in features.columns if c not in numeric]
    transforms = []
    if numeric:
        transforms.append(("numeric", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), numeric))
    if categorical:
        transforms.append(("categorical", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical))
    if not transforms:
        raise ValueError("At least one feature is required")
    return Pipeline([
        ("preprocess", ColumnTransformer(transforms)),
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ])


@dataclass
class ChurnModel:
    pipeline: Pipeline
    feature_columns: list[str]
    numeric_columns: list[str]
    version: str = "baseline-v1"

    def predict(self, record: dict, threshold: float = 0.5) -> tuple[int, float]:
        if not 0 < threshold < 1:
            raise ValueError("Threshold must be between zero and one")
        row = {name: record.get(name, np.nan) for name in self.feature_columns}
        for name in self.numeric_columns:
            row[name] = pd.to_numeric(row[name], errors="coerce")
        probability = float(self.pipeline.predict_proba(pd.DataFrame([row]))[0, 1])
        return int(probability >= threshold), probability

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, target)

    @classmethod
    def load(cls, path: str | Path) -> ChurnModel:
        # Only load artifacts produced by a trusted, approved training pipeline.
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError("Unexpected model artifact type")
        return model
