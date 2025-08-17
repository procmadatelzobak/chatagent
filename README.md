# ChatAgent MVP

- Backend: FastAPI
- Storage: SQLite at `~/.chatagent/chatagent.sqlite3`
- Projects workspace: `/home/sandbox/chatagent/projects`
- Provider: Google Gemini (stubs) — set `CHATAGENT_GOOGLE_API_KEY` in `.env`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env  # add your Google API key
```

## Development

```bash
pre-commit install
pre-commit run --all-files  # lint + type check
```

## Running

```bash
chatagent serve
# open http://localhost:8080
```

## Tests

```bash
pytest
```

## Notes

- This is a minimal skeleton: outer worker enqueues a dummy init task; inner worker initializes a git repo and README.
- Token/cost accounting, embeddings, retrieval, and richer UI are prepared to be added next.

See [docs/project-vision.md](docs/project-vision.md) for full project goals and conversation log.
