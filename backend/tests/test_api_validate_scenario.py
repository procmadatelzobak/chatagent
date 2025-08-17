from pathlib import Path
import json

from fastapi.testclient import TestClient

from chatagent.app import app

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text())


def test_validate_scenario_valid() -> None:
    payload = load_json("scenario_example.json")
    with TestClient(app) as client:
        response = client.post("/api/validate-scenario", json=payload)
    assert response.status_code == 200
    assert response.json() == {"ok": True, "errors": []}


def test_validate_scenario_invalid() -> None:
    payload = load_json("scenario_invalid.json")
    with TestClient(app) as client:
        response = client.post("/api/validate-scenario", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert any(err["path"] == "events.0.timestamp" for err in body["errors"])
