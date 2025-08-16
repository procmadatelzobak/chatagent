from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    db: Path = Path("~/.chatagent/chatagent.sqlite3").expanduser()
    workspace: Path = Path("~/sandbox/chatagent/projects").expanduser()
    google_api_key: str | None = None
    model_default: str = "gemini-1.5-flash"
    host: str = "0.0.0.0"
    port: int = 8080

    model_config = SettingsConfigDict(
        env_prefix="CHATAGENT_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
settings.workspace.mkdir(parents=True, exist_ok=True)
settings.db.parent.mkdir(parents=True, exist_ok=True)
