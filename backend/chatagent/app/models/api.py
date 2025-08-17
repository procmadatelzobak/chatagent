from __future__ import annotations

from typing import Any, Dict, List, Literal
from pydantic import BaseModel, Field, conint


class ScenarioListResponse(BaseModel):
    """List of available scenarios."""

    scenarios: List[str]


class ScenarioLoadRequest(BaseModel):
    name: str = Field(..., description="Scenario identifier")


class ScenarioLoadResponse(BaseModel):
    name: str
    tick: int
    data: Dict[str, Any]


class ControlResponse(BaseModel):
    status: Literal["playing", "paused"]


class StepRequest(BaseModel):
    ticks: conint(gt=0) = Field(1, description="Number of ticks to advance")


class StateResponse(BaseModel):
    tick: int
    data: Dict[str, Any]


class CheckpointRequest(BaseModel):
    state: Dict[str, Any]


class CheckpointResponse(BaseModel):
    status: Literal["loaded"]
