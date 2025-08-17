
from chatagent.services.persistence import (
    load_checkpoint,
    save_checkpoint,
    export_state,
    _resolve_path,
)


def test_checkpoint_round_trip():
    world = {"agents": ["alpha", "beta"]}
    scheduler = {"tasks": [1, 2, 3]}
    path = "checkpoints/../my:checkpoint.pkl"
    save_checkpoint(world, scheduler, path)
    w2, s2 = load_checkpoint(path)
    assert w2 == world
    assert s2 == scheduler


def test_export_state_has_content():
    world = {"logs": ["hello"]}
    scheduler = {"history": ["done"]}
    path = "logs/history?.json"
    export_state(world, scheduler, path)
    file_path = _resolve_path(path)
    assert file_path.exists()
    assert file_path.read_text().strip()
