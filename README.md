
# ChatAgent MVP

- Backend: FastAPI
- Storage: SQLite at `~/.chatagent/chatagent.sqlite3`
- Projects workspace: `/home/sandbox/chatagent/projects`
- Provider: Google Gemini (stubs) — set `CHATAGENT_GOOGLE_API_KEY` in `.env`

## Quickstart

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
echo 'CHATAGENT_GOOGLE_API_KEY=YOUR_KEY' > .env
chatagent serve
# open http://localhost:8080
```

## Notes

- This is a minimal skeleton: outer worker enqueues a dummy init task; inner worker initializes a git repo and README.
- Token/cost accounting, embeddings, retrieval, and richer UI are prepared to be added next.

## Scenario format and validation

Simulation scenarios are described in JSON and validated on startup. The
core structures are:

- **WorldState** – initial description and participating agents.
- **Event** – timestamped intents executed by agents.
- **SimulationConfig** – top level object containing the world state and
  a list of events.

An example scenario is provided at `backend/data/scenario_example.json`.
The corresponding Pydantic models live under `app/models` and JSON Schema
definitions under `app/schemas`.

Use the `/api/validate-scenario` endpoint to manually trigger validation;
validation errors include the JSON path for quick debugging.

See [docs/project-vision.md](docs/project-vision.md) for full project goals and conversation log.
