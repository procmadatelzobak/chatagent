from typing import List
from pydantic import BaseModel

from .world_state import WorldState
from .event import Event

class SimulationConfig(BaseModel):
    """Full configuration for running a simulation."""

    world: WorldState
    events: List[Event]
