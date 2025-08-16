
import typer, uvicorn
from .settings import settings

app = typer.Typer()

@app.command()
def serve(host: str = settings.host, port: int = settings.port):
    uvicorn.run("chatagent.app:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    app()
