
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .db.core import init_db, get_session
from .db.models import Project, Message, Task
from .agents import inner, outer
from .providers.google import GoogleProvider
from sqlmodel import select

app = FastAPI(title="ChatAgent MVP", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"])
app.mount("/static", StaticFiles(directory=str(settings.data_root)), name="static")

init_db()

# Background worker
bg_started = False
inner_streams: dict[int, list[WebSocket]] = {}

@app.on_event("startup")
async def start_worker():
    global bg_started
    if not bg_started:
        asyncio.create_task(inner.worker_loop())
        bg_started = True

@app.get("/", response_class=HTMLResponse)
async def root():
    from .web.templates.index import html as tmpl
    return tmpl()

# Serve template without Jinja for MVP
from pathlib import Path
def load_index_html():
    p = Path(__file__).parent / "web" / "templates" / "index.html"
    return p.read_text(encoding="utf-8")
from fastapi import APIRouter
router = APIRouter()

@router.get("/projects")
def list_projects():
    with get_session() as s:
        res = s.exec(select(Project)).all()
        return res

@router.post("/projects")
def create_project(payload: dict):
    slug = payload.get("slug")
    title = payload.get("title") or slug
    with get_session() as s:
        p = Project(slug=slug, title=title)
        s.add(p); s.commit(); s.refresh(p)
        return p

@router.post("/projects/{pid}/subscribe")
def subscribe(pid: int):
    # noop; in future could bind streams per project
    return {"ok": True}

@router.post("/projects/{pid}/chat")
async def chat(pid: int, payload: dict):
    text = payload.get("text","")
    prov = GoogleProvider()
    reply = await outer.handle_user_input(pid, text, prov)
    return {"reply": reply}

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def ui():
    return load_index_html()

@app.websocket("/ws/inner/{pid}")
async def ws_inner(ws: WebSocket, pid: int):
    await ws.accept()
    if pid not in inner_streams:
        inner_streams[pid] = []
    inner_streams[pid].append(ws)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception:
        pass
    finally:
        inner_streams[pid].remove(ws)
