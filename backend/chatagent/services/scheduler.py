from __future__ import annotations

import heapq
import random
from dataclasses import dataclass, field
from typing import List, Optional

from .world import Event, World


@dataclass(order=True)
class ScheduledEvent:
    time: float
    event: Event = field(compare=False)


class Scheduler:
    """Tick-based scheduler with an event queue."""

    def __init__(
        self,
        world: World,
        tick_size: float = 1.0,
        *,
        deterministic: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        self.world = world
        self.tick_size = tick_size
        self.time = 0.0
        self.queue: List[ScheduledEvent] = []
        self.playing = True
        self._step = False
        self.deterministic = deterministic
        self.rng = random.Random(seed if deterministic else None)

    # control methods
    def play(self) -> None:
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def step(self) -> List[Event]:
        self._step = True
        return self.tick()

    def schedule(self, delay: float, event: Event) -> None:
        heapq.heappush(self.queue, ScheduledEvent(self.time + delay, event))

    def tick(self) -> List[Event]:
        if not self.playing and not self._step:
            return []
        self._step = False
        self.time += self.tick_size
        triggered: List[Event] = []
        while self.queue and self.queue[0].time <= self.time:
            scheduled = heapq.heappop(self.queue)
            self.world.apply(scheduled.event, self.rng)
            triggered.append(scheduled.event)
        return triggered
