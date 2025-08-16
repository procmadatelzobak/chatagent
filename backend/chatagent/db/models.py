
from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    provider: str = "google"
    max_usd: float = 2.0
    max_tokens_per_run: int = 16000
    notes: str = ""

class Memory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    kind: str  # 'summary','doc','task','log'
    key: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    role: str  # 'user','outer','inner','tool','system'
    content: str
    token_in: int = 0
    token_out: int = 0
    cost_usd: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    title: str
    status: str = "queued"  # 'queued','running','done','blocked','error'
    input: str = ""
    result: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Embedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    kind: str  # 'doc','msg','note'
    key: str
    vector: bytes  # store as raw floats (little-endian) or JSON; MVP: JSON
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
