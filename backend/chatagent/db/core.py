from sqlmodel import Session, SQLModel, create_engine

from ..settings import settings

# Determine the correct database URL. When ``db_in_memory`` is enabled, an
# in-memory SQLite database is used. Otherwise a file-based database is
# created at the configured path.
if getattr(settings, "db_in_memory", False):
    db_url = "sqlite:///:memory:"
else:
    db_url = f"sqlite:///{settings.db}"
engine = create_engine(db_url, connect_args={"check_same_thread": False})


def init_db() -> None:
    if not getattr(settings, "db_in_memory", False):
        settings.db.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
