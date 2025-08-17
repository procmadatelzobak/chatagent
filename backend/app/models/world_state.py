from typing import List
from pydantic import BaseModel

from .agent import Agent

class WorldState(BaseModel):
    """Initial state of the world for a simulation."""

    description: str
    agents: List[Agent]
