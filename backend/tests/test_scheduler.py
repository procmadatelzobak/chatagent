from app.services.scheduler import Scheduler
from app.services.world import World, Event


def test_stepping():
    world = World()
    sched = Scheduler(world, tick_size=1.0)
    sched.schedule(1.0, Event("inc", amount=1))
    events = sched.tick()
    assert len(events) == 1
    assert world.snapshot().counter == 1
    sched.schedule(1.0, Event("inc", amount=2))
    sched.tick()
    assert world.snapshot().counter == 3


def test_pause_play_step():
    world = World()
    sched = Scheduler(world, tick_size=1.0)
    sched.pause()
    sched.schedule(1.0, Event("inc", amount=1))
    sched.tick()
    assert world.snapshot().counter == 0
    sched.step()
    assert world.snapshot().counter == 1
    sched.tick()
    assert world.snapshot().counter == 1
    sched.play()
    sched.schedule(1.0, Event("inc", amount=1))
    sched.tick()
    assert world.snapshot().counter == 2


def test_deterministic_replay():
    world1 = World()
    sched1 = Scheduler(world1, deterministic=True, seed=123)
    sched1.schedule(1.0, Event("rand", max_value=10))
    sched1.tick()
    value1 = world1.snapshot().counter

    world2 = World()
    sched2 = Scheduler(world2, deterministic=True, seed=123)
    sched2.schedule(1.0, Event("rand", max_value=10))
    sched2.tick()
    value2 = world2.snapshot().counter

    assert value1 == value2

    world3 = World()
    sched3 = Scheduler(world3, deterministic=True, seed=321)
    sched3.schedule(1.0, Event("rand", max_value=10))
    sched3.tick()
    value3 = world3.snapshot().counter

    assert value1 != value3
