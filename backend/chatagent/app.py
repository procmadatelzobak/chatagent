import asyncio
from pathlib import Path
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .agents import outer
from .agents.inner import worker_loop
from .db.core import init_db
from .providers.google import GoogleProvider

app = FastAPI(title="ChatAgent MVP", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

base_dir = Path(__file__).resolve().parent.parent / "app"
templates = Jinja2Templates(directory=str(base_dir / "templates"))
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")


@app.on_event("startup")
async def startup() -> None:
    init_db()
    asyncio.create_task(worker_loop())


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui", response_class=HTMLResponse)
async def ui(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


router = APIRouter()


@router.post("/chat")
async def chat(payload: dict) -> dict:
    project_id = payload.get("project_id")
    text = payload.get("text", "")
    model = payload.get("model")
    provider = GoogleProvider(model=model)
    reply = await outer.handle_user_input(project_id, text, provider)
    return {"reply": reply}


app.include_router(router, prefix="/api")
