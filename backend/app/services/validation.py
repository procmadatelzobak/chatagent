"""Utilities for validating scenario JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, RefResolver

from chatagent.errors import ChatAgentError

DEFAULT_SCHEMA = (
    Path(__file__).resolve().parents[1] / "schemas" / "simulation_config.schema.json"
)


class ScenarioValidationError(ChatAgentError):
    """Raised when a scenario file does not match the JSON schema."""


def load_schema(schema_path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    """Load a JSON schema from disk."""
    return json.loads(schema_path.read_text())


def validate_scenario(
    data: dict[str, Any], schema_path: Path = DEFAULT_SCHEMA
) -> list[dict[str, str]]:
    """Validate in-memory scenario data against the simulation schema.

    Args:
        data: Scenario data loaded from JSON.
        schema_path: Path to the JSON schema for the scenario.

    Returns:
        A list of validation errors. Each error is a mapping with ``path`` and
        ``message`` keys describing the failing location and the reason. An empty
        list means the payload is valid.
    """

    schema = load_schema(schema_path)
    resolver = RefResolver(base_uri=schema_path.parent.as_uri() + "/", referrer=schema)
    validator = Draft7Validator(schema, resolver=resolver)

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    return [
        {"path": ".".join(str(p) for p in error.path), "message": error.message}
        for error in errors
    ]


def validate_scenario_file(data_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> None:
    """Validate a scenario file against the simulation configuration schema.

    Args:
        data_path: Path to the scenario JSON file.
        schema_path: Path to the JSON schema for the scenario.

    Raises:
        ScenarioValidationError: If the data does not conform to the schema.
    """

    data = json.loads(data_path.read_text())
    errors = validate_scenario(data, schema_path=schema_path)
    if errors:
        error = errors[0]
        raise ScenarioValidationError(f"{error['message']} at path: {error['path']}")
