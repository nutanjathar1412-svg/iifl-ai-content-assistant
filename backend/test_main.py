
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_rejects_short_text():
    response = client.post(
        "/entries",
        json={"text": "short"}
    )

    assert response.status_code == 422
