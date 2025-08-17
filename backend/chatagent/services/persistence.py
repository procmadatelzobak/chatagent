from __future__ import annotations

import json
import pickle
import re
from pathlib import Path
from typing import Any, Tuple


# Base directory for persisted data (checkpoints, exports, etc.)
BASE_DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def _sanitize_filename(name: str) -> str:
    """Sanitize a single path component to avoid unsafe characters."""
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)


def _resolve_path(path: str | Path) -> Path:
    """Return a path under ``data/`` ensuring directories exist."""
    path_obj = Path(path)
    sanitized_parts = [_sanitize_filename(part) for part in path_obj.parts]
    full_path = BASE_DATA_DIR.joinpath(*sanitized_parts)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path


def save_checkpoint(world: Any, scheduler: Any, path: str | Path) -> Path:
    """Persist ``world`` and ``scheduler`` objects to ``path``.

    The objects are serialized with ``pickle`` so they can be reconstructed
    later via :func:`load_checkpoint`.
    """
    file_path = _resolve_path(path)
    with file_path.open("wb") as f:
        pickle.dump({"world": world, "scheduler": scheduler}, f)
    return file_path


def load_checkpoint(path: str | Path) -> Tuple[Any, Any]:
    """Load a previously saved checkpoint.

    Returns a tuple ``(world, scheduler)``.
    """
    file_path = _resolve_path(path)
    with file_path.open("rb") as f:
        data = pickle.load(f)
    return data["world"], data["scheduler"]


def export_state(world: Any, scheduler: Any, path: str | Path) -> Path:
    """Export ``world`` and ``scheduler`` to a JSON file for logs/history."""
    file_path = _resolve_path(path)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump({"world": world, "scheduler": scheduler}, f, ensure_ascii=False, indent=2)
    return file_path
