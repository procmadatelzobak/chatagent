from typing import Dict, Any
from pydantic import BaseModel, Field

class Intent(BaseModel):
    """Desired action that an agent may perform."""

    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
