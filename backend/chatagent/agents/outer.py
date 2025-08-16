from ..db.core import get_session
from ..db.models import Project
from .shared import add_message, add_task, summarize_context

SYSTEM_PROMPT = "Jsi vnější pracovník. Buď stručný, děl úkoly na malé dávky."

async def handle_user_input(project_id: int, user_text: str, provider) -> str:
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
    messages = [{"role": "user", "content": user_text}]
    data = await provider.chat(messages, system=SYSTEM_PROMPT + "\n" + summary)
    if "candidates" in data:
        reply = data["candidates"][0].get("content", "")
    else:
        reply = data["choices"][0]["message"]["content"]
    with get_session() as s:
        add_message(s, project_id, "outer", reply)
    return reply
