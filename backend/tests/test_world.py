from app.services.world import World, Event
import random

def test_apply_inc() -> None:
    world = World()
    world.apply(Event("inc", amount=5))
    assert world.snapshot().counter == 5


def test_apply_rand_deterministic() -> None:
    world = World()
    rng = random.Random(0)
    world.apply(Event("rand", max_value=5), rng=rng)
    assert world.snapshot().counter == 3
