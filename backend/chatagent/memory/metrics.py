from __future__ import annotations

from typing import Callable, Dict, Iterable

from .store import MemoryItem, MemoryStore

Evaluator = Callable[[Iterable[MemoryItem]], bool]


def compute_metrics(
    store: MemoryStore, evaluator: Evaluator
) -> Dict[str, float | bool]:
    """Calculate basic conversation metrics."""

    messages = list(store.items())
    turns = len(messages)
    avg_length = (
        sum(len(m.content) for m in messages) / turns if turns > 0 else 0.0
    )
    goal_reached = evaluator(messages)
    return {"turns": turns, "avg_length": avg_length, "goal_reached": goal_reached}
