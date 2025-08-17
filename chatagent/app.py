import asyncio
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .agents import outer
from .agents.inner import worker_loop
from .db.core import init_db
from .providers.google import GoogleProvider

app = FastAPI(title="ChatAgent MVP", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.on_event("startup")
async def startup() -> None:
    init_db()
    asyncio.create_task(worker_loop())


def load_index_html() -> str:
    p = Path(__file__).parent / "web" / "templates" / "index.html"
    return p.read_text(encoding="utf-8")


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return load_index_html()


@app.get("/ui", response_class=HTMLResponse)
async def ui() -> str:
    return load_index_html()


router = APIRouter()


@router.post("/chat")
async def chat(payload: dict) -> dict:
    project_id = int(payload.get("project_id", 0))
    text = payload.get("text", "")
    model = payload.get("model")
    provider = GoogleProvider(model=model)
    reply = await outer.handle_user_input(project_id, text, provider)
    return {"reply": reply}


app.include_router(router, prefix="/api")
