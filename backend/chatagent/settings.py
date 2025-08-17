import os
from pathlib import Path

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
