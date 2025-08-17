
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

## Web UI

A minimal control panel is served at `http://localhost:8080/`.
It allows selecting a scenario, playing or pausing the simulation,
stepping through 1/10/100 ticks, and viewing the current tick and
snapshot of the selected agent or world. The page uses vanilla
HTML/JS and is delivered directly by FastAPI.

## Notes

- This is a minimal skeleton: outer worker enqueues a dummy init task; inner worker initializes a git repo and README.
- Token/cost accounting, embeddings, retrieval, and richer UI are prepared to be added next.

See [docs/project-vision.md](docs/project-vision.md) for full project goals and conversation log.
