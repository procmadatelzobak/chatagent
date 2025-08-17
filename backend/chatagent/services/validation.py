"""Utilities for validating scenario JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, RefResolver

DEFAULT_SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "simulation_config.schema.json"

class ScenarioValidationError(Exception):
    """Raised when a scenario file does not match the JSON schema."""


def load_schema(schema_path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    """Load a JSON schema from disk."""
    return json.loads(schema_path.read_text())


def validate_scenario_file(data_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> None:
    """Validate a scenario file against the simulation configuration schema.

    Args:
        data_path: Path to the scenario JSON file.
        schema_path: Path to the JSON schema for the scenario.

    Raises:
        ScenarioValidationError: If the data does not conform to the schema.
    """

    data = json.loads(data_path.read_text())
    schema = load_schema(schema_path)
    resolver = RefResolver(base_uri=schema_path.parent.as_uri() + "/", referrer=schema)
    validator = Draft7Validator(schema, resolver=resolver)

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        error = errors[0]
        path = ".".join(str(p) for p in error.path)
        raise ScenarioValidationError(f"{error.message} at path: {path}")
