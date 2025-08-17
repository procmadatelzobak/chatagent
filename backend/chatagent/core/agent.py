from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable


class Agent(ABC):
    """Interface for conversation agents."""

    @abstractmethod
    def decide(self, history: Iterable[str]) -> str:
        """Decide on the next message based on conversation history."""

    @abstractmethod
    def receive(self, message: str) -> None:
        """Receive a message from the environment."""

    @abstractmethod
    def state(self) -> dict[str, Any]:
        """Return internal state for debugging or inspection."""
