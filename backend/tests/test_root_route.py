from fastapi.testclient import TestClient

from chatagent.app import app


def test_root_route():
    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
