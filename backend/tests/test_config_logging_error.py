import logging

from fastapi.testclient import TestClient

from chatagent.app import app
from chatagent.logging import setup_logging
from chatagent.settings import Settings, settings


def test_settings_from_file_and_env(monkeypatch, tmp_path):
    cfg = tmp_path / "config.toml"
    cfg.write_text("host = '1.2.3.4'\nport = 9000\n")
    monkeypatch.setenv("CHATAGENT_CONFIG_FILE", str(cfg))
    monkeypatch.setenv("CHATAGENT_PORT", "1234")
    s = Settings()
    assert s.host == "1.2.3.4"
    assert s.port == 1234


def test_logging_redacts_pii(capsys):
    setup_logging(level="INFO", show_pii=False)
    logger = logging.getLogger("chatagent.test")
    logger.info("secret", extra={"pii": True})
    captured = capsys.readouterr()
    assert "[REDACTED]" in captured.err


def test_error_handler(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "google")
    with TestClient(app) as client:
        r = client.post("/api/chat", json={"project_id": 1, "text": "hi"})
    assert r.status_code == 400
    assert "Google API key" in r.json()["error"]
