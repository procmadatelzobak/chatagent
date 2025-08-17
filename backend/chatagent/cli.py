
import typer, uvicorn
from .settings import settings

app = typer.Typer(invoke_without_command=False)

@app.command("serve")
def serve(host: str = settings.host, port: int = settings.port) -> None:
    """Run the ChatAgent FastAPI server."""
    uvicorn.run("chatagent.app:app", host=host, port=port, reload=True)


@app.command("version")
def version() -> None:
    """Display the ChatAgent version."""
    typer.echo("chatagent 0.1.0")

if __name__ == "__main__":
    app()
