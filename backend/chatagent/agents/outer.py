
from ..settings import settings
from ..db.core import get_session
from ..db.models import Project, Message, Task, Memory
from .shared import budget_ok, add_message, add_task, summarize_context

SYSTEM_PROMPT = """Jsi Vnější pracovník (facilitátor). Tvůj úkol:
- Vést stručný, efektivní rozhovor s uživatelem (česky).
- Udržovat úsporný kontext: používej stručné shrnutí projektu a vytažené body z paměti (retrieval).
- Rozdělit práci na malé úkoly (Tasks) pro Vnitřního pracovníka.
- Každý úkol má být: titul, cíl, definice hotovo, test/spouštěcí instrukce.
- Šetři tokeny: opakující se instrukce dej do paměťových dokumentů a pouze na ně odkazuj.
"""

async def handle_user_input(project_id: int, user_text: str, provider) -> str:
    # Very light stub that echoes a plan and enqueues a dummy task
    with get_session() as s:
        proj = s.get(Project, project_id)
        add_message(s, project_id, "user", user_text)
        # Summarize short context
        summary = summarize_context(s, project_id)
        system = SYSTEM_PROMPT + f"\n# Kontext:\n{summary}\n"
        # For MVP: static reply and create a task
        reply = "Rozumím. Vytvářím počáteční úkol: inicializace repozitáře a README."
        add_message(s, project_id, "outer", reply)
        add_task(s, project_id, "Inicializace projektu", "queued", input="init repo + README")
        s.commit()
    return reply
