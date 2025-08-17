"""Parser utilities for scenario files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .models import Scenario


def load_scenario(path: Path) -> Scenario:
    """Load and validate a scenario from a JSON or YAML file."""

    raw = path.read_text()
    if path.suffix in {".yaml", ".yml"}:
        data: Any = yaml.safe_load(raw)
    else:
        data = json.loads(raw)
    return Scenario.model_validate(data)
