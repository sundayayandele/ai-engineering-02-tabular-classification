from __future__ import annotations

import os
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel, Field

from churn_classifier.model import ChurnModel

app = FastAPI(title="Enterprise Churn Prediction API", version="0.1.0")
app.mount("/metrics", make_asgi_app())
requests_total = Counter("churn_api_requests_total", "Requests", ["method", "path", "status"])
request_seconds = Histogram("churn_api_request_seconds", "Request duration", ["method", "path"])


@app.middleware("http")
async def metrics(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    path = request.scope.get("route")
    path = getattr(path, "path", request.url.path)
    requests_total.labels(request.method, path, str(response.status_code)).inc()
    request_seconds.labels(request.method, path).observe(time.perf_counter() - start)
    return response


class PredictionRequest(BaseModel):
    features: dict[str, Any] = Field(min_length=1)


class PredictionResponse(BaseModel):
    churn: bool
    churn_probability: float
    model_version: str


@lru_cache
def get_model() -> ChurnModel:
    path = Path(os.getenv("MODEL_PATH", "artifacts/churn_pipeline.joblib"))
    if not path.is_file():
        raise RuntimeError("Approved model artifact unavailable")
    return ChurnModel.load(path)


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    try:
        get_model()
    except (RuntimeError, OSError, ValueError, TypeError) as exc:
        raise HTTPException(status_code=503, detail="Model unavailable") from exc
    return {"status": "ready"}


@app.post("/predict", response_model=PredictionResponse)
def predict(body: PredictionRequest):
    try:
        threshold = float(os.getenv("DECISION_THRESHOLD", "0.5"))
        label, probability = get_model().predict(body.features, threshold)
    except (RuntimeError, ValueError, TypeError, OSError) as exc:
        raise HTTPException(status_code=503, detail="Prediction unavailable") from exc
    return PredictionResponse(churn=bool(label), churn_probability=probability,
                              model_version=get_model().version)
