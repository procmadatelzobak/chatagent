from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

# Ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from core.scenario import Scenario, load_scenario  # noqa: E402

EXAMPLES = ROOT / "examples" / "scenarios"


def test_load_valid_json() -> None:
    scenario = load_scenario(EXAMPLES / "valid.json")
    assert isinstance(scenario, Scenario)
    assert len(scenario.agents) == 2


def test_load_valid_yaml() -> None:
    scenario = load_scenario(EXAMPLES / "valid.yaml")
    assert scenario.roles[0].name == "user"


def test_load_invalid() -> None:
    with pytest.raises(ValidationError):
        load_scenario(EXAMPLES / "invalid.json")
