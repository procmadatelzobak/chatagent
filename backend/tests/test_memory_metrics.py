from chatagent.memory import InMemoryStore, compute_metrics


def dummy_evaluator(messages):
    return any("goal" in m.content.lower() for m in messages)


def test_metrics_basic():
    store = InMemoryStore()
    store.add("user", "hello")
    store.add("assistant", "hi there")
    store.add("user", "goal accomplished")

    metrics = compute_metrics(store, dummy_evaluator)
    assert metrics["turns"] == 3
    assert metrics["avg_length"] > 0
    assert metrics["goal_reached"] is True
