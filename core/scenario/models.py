"""Pydantic models describing scenario configuration."""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class Role(BaseModel):
    """Reusable role definition."""

    name: str
    description: str | None = None


class Tool(BaseModel):
    """Tool available within the simulation."""

    name: str
    description: str | None = None


class Rule(BaseModel):
    """Simple rule described by trigger and resulting action."""

    trigger: str
    action: str


class Agent(BaseModel):
    """Agent participating in the scenario."""

    id: str
    name: str
    role: str
    goals: List[str] = Field(default_factory=list)


class Scenario(BaseModel):
    """Top level scenario configuration."""

    description: str
    roles: List[Role] = Field(default_factory=list)
    tools: List[Tool] = Field(default_factory=list)
    agents: List[Agent]
    rules: List[Rule] = Field(default_factory=list)
