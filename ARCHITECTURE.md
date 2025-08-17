# Architecture

## Scheduler

The scheduler is a simple tick-based loop that drives the simulated world. It
holds an event queue ordered by the time each event should fire. Calling
`tick()` advances the internal clock by a configurable `tick_size` and applies
all events whose scheduled time is now in the past. Events are delivered to the
`World` object which mutates its state accordingly.

The scheduler supports `play`, `pause` and `step` controls. When paused a call to
`tick()` has no effect; `step()` allows advancing exactly one tick while
remaining paused. The queue and the world state are unaffected until the event
is processed.

A deterministic mode seeds the scheduler's random number generator so that
stochastic events produce reproducible results. Tests can replay the same
sequence of events by constructing a scheduler with the same seed and feeding it
the same events.
