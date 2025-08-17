
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

## Notes

- This is a minimal skeleton: outer worker enqueues a dummy init task; inner worker initializes a git repo and README.
- Token/cost accounting, embeddings, retrieval, and richer UI are prepared to be added next.

See [docs/project-vision.md](docs/project-vision.md) for full project goals and conversation log.
