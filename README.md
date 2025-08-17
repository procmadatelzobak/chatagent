
# ChatAgent MVP

- Backend: FastAPI
- Storage: SQLite at `~/.chatagent/chatagent.sqlite3`
- Projects workspace: `/home/sandbox/chatagent/projects`
- Provider: Google Gemini (stubs) — set `CHATAGENT_GOOGLE_API_KEY` in `.env`

## Project Status

Work is at an early stage; see [Roadmap v0.1](../../issues/1) for planned improvements and current progress.

## Quickstart

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
echo 'CHATAGENT_GOOGLE_API_KEY=YOUR_KEY' > .env
chatagent serve
# open http://localhost:8080
```




## Web UI

A minimal control panel is served at `http://localhost:8080/`.
It allows selecting a scenario, playing or pausing the simulation,
stepping through 1/10/100 ticks, and viewing the current tick and
snapshot of the selected agent or world. The page uses vanilla
HTML/JS and is delivered directly by FastAPI.


## Persistence

Checkpoint and log data are stored under the repository's `data/` directory.  Utility
functions are provided for saving and loading checkpoints as well as exporting state
for inspection:

```python
from chatagent.services.persistence import save_checkpoint, load_checkpoint, export_state

world = {"agents": ["alpha"]}
scheduler = {"tasks": []}

# store objects under data/checkpoints/run.pkl
save_checkpoint(world, scheduler, "checkpoints/run.pkl")

# later, reconstruct them
world2, scheduler2 = load_checkpoint("checkpoints/run.pkl")

# write human‑readable JSON logs
export_state(world2, scheduler2, "logs/state.json")
```

All paths are relative to `data/` and created on demand with filenames sanitized.


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

## LLM integration

The backend uses a pluggable `LLMClient` interface for all model calls. By
default an `EchoLLMClient` is used which simply returns the provided prompt, so
the project works without any API keys. To experiment with a real provider you
can implement another `LLMClient` (e.g. using OpenAI or Gemini) and set
`CHATAGENT_LLM_PROVIDER` in the environment to select it. The existing
`GoogleLLMClient` demonstrates this pattern.
