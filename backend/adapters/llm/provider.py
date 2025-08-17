from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Interface for large language model providers."""

    @abstractmethod
    async def predict(self, prompt: str) -> str:
        """Return a completion for the given prompt."""
        raise NotImplementedError
