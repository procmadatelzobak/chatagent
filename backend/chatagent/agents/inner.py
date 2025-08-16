
import asyncio, os
from ..settings import settings
from ..db.core import get_session
from ..db.models import Task, Project, Message
from ..tools import shell, git
from .shared import add_message, set_task_status

PROJECTS_DIR = settings.projects_root

async def worker_loop():
    """Poll tasks and execute simple actions (MVP)."""
    while True:
        await asyncio.sleep(0.5)
        with get_session() as s:
            task = s.exec(Task.select().where(Task.status=="queued")).first()
            if not task:
                continue
            set_task_status(s, task.id, "running")
            proj = s.get(Project, task.project_id)
            proj_dir = PROJECTS_DIR / proj.slug
            proj_dir.mkdir(parents=True, exist_ok=True)
        # Execute: init git, create README
        readme = proj_dir / "README.md"
        if not readme.exists():
            readme.write_text(f"# {proj.title}\n\nInicializováno ChatAgent MVP.\n")
        # git init & commit
        async for out in git.git_init(str(proj_dir)):
            add_message(get_session(), task.project_id, "inner", out)
        async for out in git.git_commit_all(str(proj_dir), "chore: initial commit with README"):
            add_message(get_session(), task.project_id, "inner", out)
        with get_session() as s:
            set_task_status(s, task.id, "done")
            add_message(s, task.project_id, "inner", "Úkol hotov: inicializace provedena.")
