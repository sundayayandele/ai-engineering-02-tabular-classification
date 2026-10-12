from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liveness():
    assert client.get('/health/live').json() == {'status': 'ok'}


def test_metrics():
    assert client.get('/metrics').status_code == 200


def test_request_validation():
    assert client.post('/predict', json={'features': {}}).status_code == 422
