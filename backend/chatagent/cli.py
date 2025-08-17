
"""Command line interface for ChatAgent."""

import typer
import uvicorn

from .settings import settings

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """ChatAgent command line utilities."""



@app.command()
def serve(host: str = settings.host, port: int = settings.port) -> None:
    """Run the ChatAgent API server."""
    uvicorn.run("chatagent.app:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    app()
