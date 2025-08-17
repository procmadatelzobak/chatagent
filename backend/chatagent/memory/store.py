from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List


@dataclass
class MemoryItem:
    """Single conversation turn."""

    timestamp: datetime
    speaker: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemoryStore(ABC):
    """Interface for conversation memory stores."""

    @abstractmethod
    def add(self, speaker: str, content: str, metadata: Dict[str, Any] | None = None) -> None:
        """Persist a conversation turn."""

    @abstractmethod
    def items(self) -> Iterable[MemoryItem]:
        """Return all stored conversation turns in order."""


class InMemoryStore(MemoryStore):
    """Simple in-memory implementation of :class:`MemoryStore`."""

    def __init__(self) -> None:
        self._items: List[MemoryItem] = []

    def add(self, speaker: str, content: str, metadata: Dict[str, Any] | None = None) -> None:
        self._items.append(
            MemoryItem(
                timestamp=datetime.utcnow(),
                speaker=speaker,
                content=content,
                metadata=metadata or {},
            )
        )

    def items(self) -> Iterable[MemoryItem]:
        return list(self._items)
