import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .logging import setup_logging


class Settings(BaseSettings):
    db: Path = Path("~/.chatagent/chatagent.sqlite3").expanduser()
    workspace: Path = Path("~/sandbox/chatagent/projects").expanduser()
    google_api_key: str | None = None
    model_default: str = "gemini-1.5-flash"
    llm_provider: str = "echo"
    # Polling interval for the background worker in seconds.  Shorter values
    # reduce the latency between a task being enqueued and it being executed.
    # Can be overridden using the environment variable CHATAGENT_WORKER_POLL_INTERVAL.
    worker_poll_interval: float = 1.0
    # Use an in-memory SQLite database when set to True.  This is useful for
    # running tests without requiring a writable filesystem.  When enabled,
    # the database URL will be ``sqlite:///:memory:``.  Can be toggled via
    # the environment variable CHATAGENT_DB_IN_MEMORY.
    db_in_memory: bool = False

    @field_validator("db", "workspace", mode="after")
    @classmethod
    def _expand_paths(cls, v: Path) -> Path:
        return v.expanduser()

    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    log_pii: bool = False

    model_config = SettingsConfigDict(
        env_prefix="CHATAGENT_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        config_path = Path(
            os.getenv(
                "CHATAGENT_CONFIG_FILE",
                Path(__file__).resolve().parent.parent / "config.toml",
            )
        )
        return (
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls, config_path),
            init_settings,
            file_secret_settings,
        )


settings = Settings()
settings.workspace.mkdir(parents=True, exist_ok=True)
settings.db.parent.mkdir(parents=True, exist_ok=True)
setup_logging(settings.log_level, settings.log_pii)
