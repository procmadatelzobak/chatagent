
from ..db.core import get_session
from ..db.models import Message, Task, Memory, Project
from datetime import datetime

def add_message(s, project_id: int, role: str, content: str, token_in: int=0, token_out: int=0, cost_usd: float=0.0):
    msg = Message(project_id=project_id, role=role, content=content, token_in=token_in, token_out=token_out, cost_usd=cost_usd)
    s.add(msg)
    s.commit()

def add_task(s, project_id: int, title: str, status: str, input: str):
    t = Task(project_id=project_id, title=title, status=status, input=input)
    s.add(t)

def set_task_status(s, task_id: int, status: str):
    t = s.get(Task, task_id)
    t.status = status
    s.add(t)
    s.commit()

def summarize_context(s, project_id: int) -> str:
    # MVP: take last memory docs and last 5 messages
    mems = s.exec(Memory.select().where(Memory.project_id==project_id)).all()
    memtxt = "\n".join(f"- [{m.kind}] {m.key}" for m in mems[-5:])
    msgs = s.exec(Message.select().where(Message.project_id==project_id)).all()
    hist = "\n".join(f"{m.role}: {m.content[:200]}" for m in msgs[-5:])
    return f"Paměť:\n{memtxt}\n\nPoslední zprávy:\n{hist}"
