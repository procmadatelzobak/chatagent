from __future__ import annotations

import os

from .provider import LLMProvider


class OpenAILLM(LLMProvider):
    """Skeleton adapter for OpenAI's API."""

    def __init__(self, model: str = "gpt-4o") -> None:
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing OpenAI API key")

    async def predict(self, prompt: str) -> str:  # pragma: no cover - placeholder
        raise NotImplementedError("OpenAI adapter not implemented")
