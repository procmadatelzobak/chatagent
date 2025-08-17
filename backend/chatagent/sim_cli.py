import json
from pathlib import Path

import typer

from app.models import SimulationConfig
from app.services.scheduler import Scheduler
from app.services.validation import validate_scenario_file
from app.services.world import Event as WorldEvent, World

app = typer.Typer(help="Run chat simulations without the web UI")


@app.callback()
def main() -> None:
    """CLI entry point."""


@app.command()
def run(
    scenario: Path = typer.Option(..., exists=True, dir_okay=False, help="Path to scenario JSON"),
    report: bool = typer.Option(False, '--report', help="Write Markdown report to /reports"),
) -> None:
    """Run a simulation from SCENARIO and emit NDJSON logs."""
    try:
        validate_scenario_file(scenario)
    except Exception as exc:  # pragma: no cover - validation errors are simple to reproduce
        typer.echo(json.dumps({"error": str(exc)}))
        raise typer.Exit(1)

    config = SimulationConfig.model_validate_json(scenario.read_text())

    world = World()
    scheduler = Scheduler(world)

    for event in config.events:
        params = event.intent.parameters or {}
        world_event = WorldEvent(
            event.intent.name,
            amount=params.get("amount"),
            max_value=params.get("max_value"),
        )
        scheduler.schedule(event.timestamp, world_event)

    records = []
    while scheduler.queue:
        triggered = scheduler.tick()
        snapshot = world.snapshot()
        for triggered_event in triggered:
            record = {
                "time": scheduler.time,
                "event": triggered_event.__dict__,
                "world": snapshot.__dict__,
            }
            records.append(record)
            typer.echo(json.dumps(record))

    if report:
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"{scenario.stem}.md"
        report_path.write_text(
            "# Simulation Report\n\n" f"Scenario: {scenario.name}\n\n" f"Final counter: {world.snapshot().counter}\n"
        )


if __name__ == "__main__":
    app()
