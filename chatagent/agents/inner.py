import asyncio
import subprocess
import sys

from sqlmodel import select

from ..db.core import get_session
from ..db.models import Task
from ..settings import settings

WORKSPACE = settings.workspace


async def worker_loop() -> None:
    while True:
        await asyncio.sleep(1)
        with get_session() as s:
            task = s.exec(
                select(Task).where(Task.status == "queued").order_by(Task.created_at)
            ).first()
            if not task:
                continue
            task.status = "running"
            s.add(task)
            s.commit()
            task_id = task.id
            project_id = task.project_id
            task_input = task.input
        proj_dir = WORKSPACE / str(project_id)
        proj_dir.mkdir(parents=True, exist_ok=True)
        status = "done"
        result = ""
        try:
            if task_input.startswith("create_file "):
                _, path, content = task_input.split(" ", 2)
                file_path = proj_dir / path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content)
                result = "created"
            elif task_input.startswith("run_python "):
                _, path = task_input.split(" ", 1)
                file_path = proj_dir / path
                proc = subprocess.run(
                    [sys.executable, str(file_path)],
                    capture_output=True,
                    text=True,
                    cwd=proj_dir,
                )
                result = proc.stdout + proc.stderr
            else:
                status = "failed"
                result = "Unknown task input"
        except Exception as e:
            status = "failed"
            result = str(e)
        with get_session() as s:
            t = s.get(Task, task_id)
            t.status = status
            t.result = result
            s.add(t)
            s.commit()
