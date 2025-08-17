from fastapi.testclient import TestClient

from chatagent.app import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        r = client.get("/healthz")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
