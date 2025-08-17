import asyncio
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from .db.core import init_db
from .agents.inner import worker_loop
from .agents import outer
from .providers.google import GoogleLLMClient
from .services.llm import EchoLLMClient, LLMClient
from .settings import settings

app = FastAPI(title="ChatAgent MVP", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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

def get_llm(model: str | None = None) -> LLMClient:
    if settings.llm_provider == "google":
        return GoogleLLMClient(model=model)
    return EchoLLMClient()


@router.post("/chat")
async def chat(payload: dict) -> dict:
    project_id = payload.get("project_id")
    text = payload.get("text", "")
    model = payload.get("model")
    llm = get_llm(model=model)
    reply = await outer.handle_user_input(project_id, text, llm)
    return {"reply": reply}

app.include_router(router, prefix="/api")
