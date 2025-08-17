from sqlmodel import select

from ..db.models import Memory, Message, Task


def add_message(session, project_id: int, role: str, content: str) -> None:
    msg = Message(project_id=project_id, role=role, content=content)
    session.add(msg)
    session.commit()

def add_task(
    session, project_id: int, title: str, input: str, status: str = "queued"
) -> None:
    task = Task(project_id=project_id, title=title, input=input, status=status)
    session.add(task)
    session.commit()


def summarize_context(session, project_id: int) -> str:
    mems = session.exec(
        select(Memory)
        .where(Memory.project_id == project_id)
        .order_by(Memory.created_at)
    ).all()
    memtxt = "\n".join(f"{m.key}: {m.value}" for m in mems[-5:])
    msgs = session.exec(
        select(Message)
        .where(Message.project_id == project_id)
        .order_by(Message.created_at)
    ).all()
    hist = "\n".join(f"{m.role}: {m.content[:200]}" for m in msgs[-5:])
    return f"Paměť:\n{memtxt}\n\nPoslední zprávy:\n{hist}"
