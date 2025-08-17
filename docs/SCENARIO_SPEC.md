# Scenario Specification

This document defines the JSON/YAML format for simulation scenarios. Each
scenario lists participating agents, their roles and goals, optional tools
available to the simulation, and high level interaction rules.

## Structure

```yaml
# High level description of the scenario
description: Demo scenario

# Optional reusable role definitions
roles:
  - name: user
    description: Human participant
  - name: assistant
    description: Helpful AI assistant

# Tools available to agents during the simulation
tools:
  - name: search
    description: Query external information

# Agents taking part in the scenario
agents:
  - id: a1
    name: Alice
    role: user
    goals:
      - greet everyone
  - id: a2
    name: Bot
    role: assistant

# Rules influencing the flow of the simulation
rules:
  - trigger: greet
    action: reply_greeting
```

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Scenario",
  "type": "object",
  "properties": {
    "description": {"type": "string"},
    "roles": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"}
        },
        "required": ["name"],
        "additionalProperties": false
      },
      "default": []
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"}
        },
        "required": ["name"],
        "additionalProperties": false
      },
      "default": []
    },
    "agents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "role": {"type": "string"},
          "goals": {
            "type": "array",
            "items": {"type": "string"},
            "default": []
          }
        },
        "required": ["id", "name", "role"],
        "additionalProperties": false
      }
    },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "trigger": {"type": "string"},
          "action": {"type": "string"}
        },
        "required": ["trigger", "action"],
        "additionalProperties": false
      },
      "default": []
    }
  },
  "required": ["description", "agents"],
  "additionalProperties": false
}
```

Example scenarios can be found under `examples/scenarios/`.
