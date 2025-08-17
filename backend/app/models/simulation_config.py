from typing import List

from pydantic import BaseModel

from .event import Event
from .world_state import WorldState


class SimulationConfig(BaseModel):
    """Full configuration for running a simulation."""

    world: WorldState
    events: List[Event]
