from __future__ import annotations

from typing import Any, Iterable, List

from .agent import Agent


class RuleBasedAgent(Agent):
    """Deterministic agent using simple pattern matching."""

    def __init__(self) -> None:
        self._history: List[str] = []

    def decide(self, history: Iterable[str]) -> str:
        last = list(history)[-1].lower() if history else ""
        if "hello" in last:
            response = "Hi there!"
        elif "how are you" in last:
            response = "I'm just code, but I'm running."
        else:
            response = "I don't understand."
        self._history.append(response)
        return response

    def receive(self, message: str) -> None:
        self._history.append(message)

    def state(self) -> dict[str, Any]:
        return {"history": list(self._history)}
