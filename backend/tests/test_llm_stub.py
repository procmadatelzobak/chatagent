import asyncio
import pytest

from chatagent.agents import outer
from chatagent.services.llm import EchoLLMClient
from sqlmodel import delete

from chatagent.db.core import get_session, init_db
from chatagent.db.models import Message, Memory, Task
from chatagent.settings import settings


@pytest.mark.skip("requires writable database")
def test_llm_stub_echo():
    init_db()
    with get_session() as s:
        s.exec(delete(Message))
        s.exec(delete(Memory))
        s.exec(delete(Task))
        s.commit()
    llm = EchoLLMClient()
    reply = asyncio.run(outer.handle_user_input(1, "Test", llm))
    expected = (
        outer.SYSTEM_PROMPT
        + "\n"
        + "Paměť:\n\n\nPoslední zprávy:\nuser: Test"
    )
    assert reply == "(echo) " + expected
