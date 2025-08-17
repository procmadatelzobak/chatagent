import subprocess
import sys
from pathlib import Path


def test_chatagent_help_shows_serve() -> None:
    cmd = [sys.executable, "-m", "chatagent.cli", "--help"]
    env = {"PYTHONPATH": str(Path(__file__).resolve().parents[1])}
    res = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
    assert "serve" in res.stdout
