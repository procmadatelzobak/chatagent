# Domain Model

This document outlines the core entities of the chat simulator and how they interact.

## Entities

### Conversation
- Orchestrates message exchange between Agents.
- Uses the active Scenario to seed initial context.
- Persists progress through Memory and exposes transcripts for evaluation.

### Agent
- An autonomous actor participating in a Conversation.
- Invokes Tools to perform actions.
- Maintains its own Memory of prior exchanges.

### Tool
- External capability that can be invoked by an Agent.
- Examples: shell commands, git operations, LLM calls.

### Scenario
- Describes initial world state and scheduled events.
- Provides the starting configuration for a Conversation.

### Memory
- Stores conversation state for each Agent.
- Supports retrieval of past exchanges during simulation.

### Evaluator
- Consumes Conversation outputs and Memories.
- Produces metrics or feedback about the simulation.

## Relationships and Boundaries

- A **Scenario** spawns a **Conversation** with participating **Agents**.
- **Agents** call **Tools** and update their **Memory** as the Conversation progresses.
- The **Evaluator** reads the Conversation transcript and Memory snapshots to score outcomes.
- Tools, storage, and user interfaces are treated as external adapters; the domain core remains framework‑agnostic.

## Target Modular Structure

| Module    | Responsibility                     | Existing code to migrate |
|-----------|------------------------------------|--------------------------|
| `core/`   | Entities and simulation logic      | `backend/app/models`, `backend/chatagent/agents`, `backend/chatagent/tools` (interfaces) |
| `adapters/` | Implementations of external services (LLMs, shell, git, etc.) | `backend/chatagent/providers`, `backend/chatagent/tools` (implementations) |
| `storage/` | Persistence and database access    | `backend/chatagent/db`, `backend/chatagent/services/persistence.py` |
| `cli/`    | Command‑line entry points          | `backend/chatagent/cli.py` |
| `web/`    | FastAPI app and static assets      | `backend/chatagent/app.py`, `backend/app/templates`, `backend/app/static`, `backend/chatagent/web` |

This layout separates the domain core from frameworks and I/O, enabling independent evolution of adapters and interfaces.
