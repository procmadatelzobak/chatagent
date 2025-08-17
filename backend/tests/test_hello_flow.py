from time import sleep

from fastapi.testclient import TestClient
from sqlmodel import select

from chatagent.app import app
from chatagent.db.core import get_session, init_db
from chatagent.db.models import Task
from chatagent.settings import settings


def test_hello_flow():
    if settings.db.exists():
        settings.db.unlink()
    init_db()
    with TestClient(app) as client:
        r = client.post("/api/chat", json={"project_id": 1, "text": "hello world"})
        assert r.status_code == 200
        with get_session() as s:
            tasks = s.exec(select(Task)).all()
            assert len(tasks) == 2
        sleep(4)
        with get_session() as s:
            run_task = s.exec(select(Task).where(Task.title == "Run hello.py")).first()
            assert run_task is not None
            assert "Hello, world!" in (run_task.result or "")
