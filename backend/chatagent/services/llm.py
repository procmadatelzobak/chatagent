from __future__ import annotations

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract interface for large language model providers."""

    @abstractmethod
    async def predict(self, prompt: str) -> str:
        """Return the model completion for the given prompt."""
        raise NotImplementedError


class EchoLLMClient(LLMClient):
    """Stub implementation that simply echoes the prompt back."""

    async def predict(self, prompt: str) -> str:
        return f"(echo) {prompt}"
