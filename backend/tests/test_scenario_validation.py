from pathlib import Path

import pytest

from app.services.validation import validate_scenario_file, ScenarioValidationError


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_valid_scenario() -> None:
    path = DATA_DIR / "scenario_example.json"
    validate_scenario_file(path)


def test_invalid_scenario() -> None:
    path = DATA_DIR / "scenario_invalid.json"
    with pytest.raises(ScenarioValidationError):
        validate_scenario_file(path)
