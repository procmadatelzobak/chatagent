from __future__ import annotations

from typing import Iterable, List, Tuple

from ..agent import Agent


class ConversationEngine:
    """Simple tick-based conversation engine."""

    def __init__(self, agent: Agent, scenario: Iterable[str]):
        self.agent = agent
        self.scenario = list(scenario)
        self.tick = 0
        self.transcript: List[Tuple[str, str]] = []

    def step(self) -> bool:
        if self.tick >= len(self.scenario):
            return False
        message = self.scenario[self.tick]
        self.agent.receive(message)
        self.transcript.append(("env", message))
        response = self.agent.decide([m for _, m in self.transcript])
        self.transcript.append(("agent", response))
        self.tick += 1
        return True

    def run(self) -> List[Tuple[str, str]]:
        while self.step():
            pass
        return self.transcript
