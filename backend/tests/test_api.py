import pytest
from fastapi.testclient import TestClient

from chatagent.app import app, simulation


@pytest.fixture()
def client():
    simulation.reset()
    with TestClient(app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_and_load_scenario(client):
    r = client.get("/api/scenarios")
    assert r.status_code == 200
    assert "demo" in r.json()["scenarios"]

    r = client.post("/api/scenarios/load", json={"name": "demo"})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "demo"
    assert body["tick"] == 0


def test_play_step_state_pause(client):
    client.post("/api/scenarios/load", json={"name": "demo"})

    r = client.post("/api/play")
    assert r.status_code == 200
    assert r.json()["status"] == "playing"

    r = client.post("/api/step", json={"ticks": 2})
    assert r.status_code == 200
    assert r.json()["tick"] == 2
    assert r.json()["data"]["counter"] == 2

    r = client.get("/api/state")
    assert r.status_code == 200
    assert r.json()["tick"] == 2

    r = client.post("/api/pause")
    assert r.status_code == 200
    assert r.json()["status"] == "paused"


def test_export_and_checkpoint(client):
    client.post("/api/scenarios/load", json={"name": "demo"})
    client.post("/api/step", json={"ticks": 1})

    r = client.get("/api/state/export")
    assert r.status_code == 200
    assert r.json()["tick"] == 1

    r = client.post("/api/checkpoint", json={"state": {"counter": 5}})
    assert r.status_code == 200

    r = client.get("/api/state")
    assert r.json()["data"]["counter"] == 5


def test_errors(client):
    r = client.post("/api/step", json={"ticks": 1})
    assert r.status_code == 400

    r = client.post("/api/scenarios/load", json={"name": "unknown"})
    assert r.status_code == 404

    r = client.post("/api/step", json={"ticks": -1})
    assert r.status_code == 422
