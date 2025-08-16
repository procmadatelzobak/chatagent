
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Paths
    home_dir: Path = Path.home()
    data_root: Path = Path.home() / "chatagent"
    projects_root: Path = Path.home() / "chatagent" / "projects"

    # Web
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = True

    # Providers
    provider: str = "google"
    google_api_key: str | None = None
    google_model_chat: str = "gemini-1.5-pro"
    google_model_mini: str = "gemini-1.5-flash"
    google_model_embed: str = "text-embedding-004"

    # Budgets
    max_usd_per_project: float = 2.00
    max_tokens_per_run: int = 16000

    # Security
    allow_root: bool = True

    model_config = SettingsConfigDict(env_prefix="CHATAGENT_", env_file=".env", env_file_encoding="utf-8")

settings = Settings()
settings.data_root.mkdir(parents=True, exist_ok=True)
settings.projects_root.mkdir(parents=True, exist_ok=True)
