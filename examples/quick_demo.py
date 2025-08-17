import asyncio

from adapters.llm import MockLLM
from chatagent.agents.outer import handle_user_input


async def main() -> None:
    """Run a minimal demo using the mock LLM."""
    llm = MockLLM(response="Hello from mock")
    reply = await handle_user_input(project_id=1, user_text="hi", llm=llm)
    print(f"Agent replied: {reply}")


if __name__ == "__main__":
    asyncio.run(main())
