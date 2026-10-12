import pandas as pd

from churn_classifier.model import ChurnModel, build_pipeline, prepare_data


def test_model_pipeline(tmp_path):
    frame = pd.DataFrame({
        "customerID": [f"c{i}" for i in range(20)],
        "Churn": ["Yes", "No"] * 10,
        "tenure": list(range(20)),
        "MonthlyCharges": [60.0 + i for i in range(20)],
        "Contract": ["Month-to-month", "Two year"] * 10,
    })
    features, target = prepare_data(frame)
    assert "customerID" not in features.columns
    pipeline = build_pipeline(features)
    pipeline.fit(features, target)
    model = ChurnModel(pipeline, list(features.columns), ["tenure", "MonthlyCharges"])
    label, probability = model.predict({"tenure": 3, "MonthlyCharges": 72, "Contract": "Two year"})
    assert label in (0, 1)
    assert 0 <= probability <= 1
    path = tmp_path / "model.joblib"
    model.save(path)
    assert ChurnModel.load(path).version == "baseline-v1"
