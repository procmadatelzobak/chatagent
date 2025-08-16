CODEX_TASK.md — Runbook pro dokončení ChatAgent MVP

Kontext (co stavíme)
---------------------
ChatAgent je dvou-agentní nástroj pro vývoj software:

- Vnější pracovník (outer) – komunikuje s uživatelem, ukládá kontext, rozděluje práci na úkoly pro vnitřního.
- Vnitřní pracovník (inner) – autonomně vykonává přijaté úkoly, zapisuje stav a logy.

Backend: Python 3.12, FastAPI, Uvicorn, SQLite (SQLModel), jednoduché web UI (HTML/JS).
LLM provider (MVP): Google (Gemini) přes Chat Completions kompatibilní rozhraní.

Cíl MVP: Uživatel v UI napíše „hello world“ (nebo klikne na tlačítko); outer z toho vyrobí 2 úkoly („vytvoř hello.py“, „spusť hello.py“); inner je vykoná; v UI uvidíme výstup Hello, world!.

Akceptační kritéria MVP
-----------------------
- `GET /healthz` vrací 200 OK + `{ "status": "ok" }`.
- `GET /` a `GET /ui` vrací funkční web UI (černé pozadí, zelený text, pole pro prompt, výběr modelu, tlačítko „Send“, log panel).
- `POST /api/chat` s JSON `{project_id, text, model?}`:
  - uloží zprávu uživatele,
  - pokud text obsahuje „hello world“ (case-insensitive), outer enqueue:
    - `create_file: hello.py` s obsahem `print("Hello, world!")`
    - `run_python: hello.py`
  - jinak zavolá LLM a vrátí odpověď.
- Background worker (inner) polluje úkoly (`status="queued"`) a:
  - u `create_file` zapíše soubor do projektového workspace,
  - u `run_python` spustí proces, uloží stdout/stderr do DB a nastaví `status="done"`.
- UI po odeslání „hello world“ zobrazí:
  - zprávy v chatu (uživatel/outer),
  - stav úkolů a výstup `Hello, world!`.
- `systemd` služba `chatagent.service` na Ubuntu 24.04 běží (Restart=on-failure), logy jdou číst `journalctl -u chatagent`.

Důležité konvence
-----------------
- Nevkládat žádné API klíče do repa. Použít `.env`.
- Conventional Commits (`feat: …`, `fix: …`, `chore: …`, `docs: …`).
- Vše v branchi `feat/mvp-hello-flow`.

... (zkráceno pro přehlednost)
