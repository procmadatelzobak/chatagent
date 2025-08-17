import asyncio
from pathlib import Path
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from ..agents import outer
from ..agents.inner import worker_loop
from ..db.core import init_db
from ..providers.google import GoogleProvider
from ..simulation import Simulation
from .models.api import (
    CheckpointRequest,
    CheckpointResponse,
    ControlResponse,
    ScenarioListResponse,
    ScenarioLoadRequest,
    ScenarioLoadResponse,
    StateResponse,
    StepRequest,
)

app = FastAPI(title="ChatAgent MVP", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    init_db()
    asyncio.create_task(worker_loop())


def load_index_html() -> str:
    p = Path(__file__).parent.parent / "web" / "templates" / "index.html"
    return p.read_text(encoding="utf-8")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return load_index_html()


@app.get("/ui", response_class=HTMLResponse)
async def ui() -> str:
    return load_index_html()


# Router for existing chat endpoint and new simulation API
api_router = APIRouter()


@api_router.post("/chat")
async def chat(payload: dict) -> dict:
    project_id = payload.get("project_id")
    text = payload.get("text", "")
    model = payload.get("model")
    provider = GoogleProvider(model=model)
    reply = await outer.handle_user_input(project_id, text, provider)
    return {"reply": reply}


# Simulation instance
simulation = Simulation()


@api_router.get("/scenarios", response_model=ScenarioListResponse)
async def list_scenarios() -> ScenarioListResponse:
    return ScenarioListResponse(scenarios=simulation.list_scenarios())


@api_router.post(
    "/scenarios/load", response_model=ScenarioLoadResponse, status_code=200
)
async def load_scenario(req: ScenarioLoadRequest) -> ScenarioLoadResponse:
    try:
        simulation.load(req.name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Scenario not found")
    state = simulation.export_state()
    return ScenarioLoadResponse(name=req.name, **state)


@api_router.post("/play", response_model=ControlResponse)
async def play() -> ControlResponse:
    try:
        simulation.play()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ControlResponse(status="playing")


@api_router.post("/pause", response_model=ControlResponse)
async def pause() -> ControlResponse:
    simulation.pause()
    return ControlResponse(status="paused")


@api_router.post("/step", response_model=StateResponse)
async def step(req: StepRequest) -> StateResponse:
    try:
        state = simulation.step(req.ticks)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return StateResponse(**state)


@api_router.get("/state", response_model=StateResponse)
async def get_state() -> StateResponse:
    try:
        state = simulation.export_state()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return StateResponse(**state)


@api_router.get("/state/export", response_model=StateResponse)
async def export_state() -> StateResponse:
    try:
        state = simulation.export_state()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return StateResponse(**state)


@api_router.post("/checkpoint", response_model=CheckpointResponse)
async def load_checkpoint(req: CheckpointRequest) -> CheckpointResponse:
    try:
        simulation.load_checkpoint(req.state)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CheckpointResponse(status="loaded")


app.include_router(api_router, prefix="/api")
