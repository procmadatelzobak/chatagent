from __future__ import annotations

from .provider import LLMProvider


class MockLLM(LLMProvider):
    """Mock LLM provider used for tests."""

    def __init__(self, response: str = "(mock)") -> None:
        self.response = response

    async def predict(self, prompt: str) -> str:  # pragma: no cover - trivial
        return self.response
