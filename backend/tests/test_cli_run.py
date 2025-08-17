import json
import subprocess
import sys
from pathlib import Path


def test_cli_run(tmp_path: Path) -> None:
    scenario = {
        "world": {
            "description": "demo",
            "agents": [{"id": "a1", "name": "A", "role": "user"}],
        },
        "events": [
            {
                "timestamp": 0,
                "agent_id": "a1",
                "intent": {"name": "inc", "parameters": {"amount": 2}},
            }
        ],
    }
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(json.dumps(scenario))

    cmd = [sys.executable, "-m", "chatagent.sim_cli", "run", "--scenario", str(scenario_path)]
    env = {"PYTHONPATH": str(Path(__file__).resolve().parents[1])}
    res = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
    lines = res.stdout.strip().splitlines()
    assert lines
    record = json.loads(lines[-1])
    assert record["world"]["counter"] == 2


def test_cli_report(tmp_path: Path) -> None:
    scenario = {
        "world": {
            "description": "demo",
            "agents": [{"id": "a1", "name": "A", "role": "user"}],
        },
        "events": [
            {
                "timestamp": 0,
                "agent_id": "a1",
                "intent": {"name": "inc", "parameters": {"amount": 1}},
            }
        ],
    }
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(json.dumps(scenario))
    cmd = [
        sys.executable,
        "-m",
        "chatagent.sim_cli",
        "run",
        "--scenario",
        str(scenario_path),
        "--report",
    ]
    env = {"PYTHONPATH": str(Path(__file__).resolve().parents[1])}
    subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=tmp_path, env=env)
    report_path = tmp_path / "reports" / "scenario.md"
    assert report_path.exists()
