from ..db.core import get_session
from ..db.models import Project
from ..services.llm import LLMClient
from .shared import add_message, add_task, summarize_context

SYSTEM_PROMPT = "Jsi vnější pracovník. Buď stručný, děl úkoly na malé dávky."


async def handle_user_input(project_id: int, user_text: str, llm: LLMClient) -> str:
    text_lower = user_text.lower()
    with get_session() as s:
        project = s.get(Project, project_id)
        if project is None:
            project = Project(id=project_id, name=f"Project {project_id}")
            s.add(project)
            s.commit()
        add_message(s, project_id, "user", user_text)
        if "hello world" in text_lower:
            add_message(s, project_id, "outer", "Vytvořím hello.py a spustím ho.")
            add_task(
                s,
                project_id,
                "Create hello.py",
                'create_file hello.py print("Hello, world!")',
            )
            add_task(
                s,
                project_id,
                "Run hello.py",
                "run_python hello.py",
            )
            return "Plán vytvořen. Spouštím vnitřního pracovníka."
    summary = summarize_context(s, project_id)
    prompt = SYSTEM_PROMPT + "\n" + summary
    reply = await llm.predict(prompt)
    with get_session() as s:
        add_message(s, project_id, "outer", reply)
    return reply
