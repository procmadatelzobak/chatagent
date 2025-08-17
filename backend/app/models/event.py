from pydantic import BaseModel

from .intent import Intent

class Event(BaseModel):
    """A point in time where an agent expresses an intent."""

    timestamp: float
    agent_id: str
    intent: Intent
