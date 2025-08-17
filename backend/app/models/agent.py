from pydantic import BaseModel


class Agent(BaseModel):
    """Represents an actor participating in the simulation."""

    id: str
    name: str
    role: str
