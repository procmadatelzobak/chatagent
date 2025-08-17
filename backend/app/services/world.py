from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class WorldState:
    """Simple container for world state."""

    counter: int = 0


@dataclass
class Event:
    """Represents an action to be applied to the world."""

    name: str
    amount: Optional[int] = None
    max_value: Optional[int] = None


class World:
    """Holds mutable world state and applies events."""

    def __init__(self) -> None:
        self._state = WorldState()

    def apply(self, event: Event, rng: Optional[random.Random] = None) -> None:
        """Apply an event to the world state.

        Parameters
        ----------
        event: Event
            The event to apply.
        rng: Optional[random.Random]
            Source of randomness for stochastic events.
        """
        if event.name == "inc" and event.amount is not None:
            self._state.counter += event.amount
        elif event.name == "rand" and rng is not None and event.max_value is not None:
            self._state.counter += rng.randint(0, event.max_value)

    def snapshot(self) -> WorldState:
        """Return a read-only copy of the current world state."""
        return WorldState(self._state.counter)
