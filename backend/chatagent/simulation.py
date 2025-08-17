from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Scenario:
    """Simple scenario with a counter that increments each tick."""

    name: str

    def initial_state(self) -> Dict[str, Any]:
        return {"counter": 0}

    def step(self, state: Dict[str, Any]) -> None:
        state["counter"] = state.get("counter", 0) + 1


SCENARIOS: Dict[str, Scenario] = {"demo": Scenario(name="demo")}


@dataclass
class Simulation:
    """In-memory simulation engine for demonstration and testing."""

    current: Optional[Scenario] = None
    state: Dict[str, Any] = field(default_factory=dict)
    tick: int = 0
    playing: bool = False

    def reset(self) -> None:
        self.current = None
        self.state.clear()
        self.tick = 0
        self.playing = False

    def list_scenarios(self) -> List[str]:
        return list(SCENARIOS.keys())

    def load(self, name: str) -> None:
        scenario = SCENARIOS.get(name)
        if not scenario:
            raise ValueError("Unknown scenario")
        self.current = scenario
        self.state = scenario.initial_state()
        self.tick = 0
        self.playing = False

    def play(self) -> None:
        if not self.current:
            raise RuntimeError("No scenario loaded")
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def step(self, ticks: int = 1) -> Dict[str, Any]:
        if not self.current:
            raise RuntimeError("No scenario loaded")
        for _ in range(ticks):
            self.current.step(self.state)
            self.tick += 1
        return self.export_state()

    def export_state(self) -> Dict[str, Any]:
        if not self.current:
            raise RuntimeError("No scenario loaded")
        return {"tick": self.tick, "data": dict(self.state)}

    def load_checkpoint(self, data: Dict[str, Any]) -> None:
        if not self.current:
            raise RuntimeError("No scenario loaded")
        self.state.update(data)
