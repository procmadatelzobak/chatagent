import asyncio
import logging
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.validation import (
    ScenarioValidationError,
    validate_scenario,
    validate_scenario_file,
)

from .agents import outer
from .agents.inner import worker_loop
from .db.core import init_db
from .errors import ChatAgentError
from .providers.google import GoogleLLMClient
from .services.llm import EchoLLMClient, LLMClient
from .settings import settings

app = FastAPI(title="ChatAgent MVP", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

base_dir = Path(__file__).resolve().parent.parent / "app"
templates = Jinja2Templates(directory=str(base_dir / "templates"))
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup() -> None:
    init_db()
    scenario_path = (
        Path(__file__).resolve().parents[1] / "data" / "scenario_example.json"
    )
    try:
        validate_scenario_file(scenario_path)
    except ScenarioValidationError as exc:
        raise RuntimeError(f"Invalid scenario file: {exc}") from exc
    asyncio.create_task(worker_loop())


@app.exception_handler(ChatAgentError)
async def handle_chatagent_error(request: Request, exc: ChatAgentError) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(status_code=400, content={"error": str(exc)})


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


@router.get("/validate-scenario")
async def validate_sample_scenario() -> dict:
    scenario_path = (
        Path(__file__).resolve().parents[1] / "data" / "scenario_example.json"
    )
    try:
        validate_scenario_file(scenario_path)
    except ScenarioValidationError as exc:
        return {"valid": False, "error": str(exc)}
    return {"valid": True}


@router.post("/validate-scenario")
async def validate_scenario_payload(payload: dict) -> dict:
    errors = validate_scenario(payload)
    return {"ok": not errors, "errors": errors}


app.include_router(router, prefix="/api")
