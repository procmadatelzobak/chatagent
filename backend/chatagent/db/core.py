from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from ..settings import settings

engine = None


def get_engine():
    """Return a cached SQLModel engine configured for current settings."""
    global engine
    if engine is None:
        if settings.db_in_memory:
            engine = create_engine(
                "sqlite:///:memory:",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            db_url = f"sqlite:///{settings.db}"
            engine = create_engine(db_url, connect_args={"check_same_thread": False})
    return engine


def init_db() -> None:
    if not settings.db_in_memory:
        settings.db.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(get_engine())


def get_session() -> Session:
    return Session(get_engine())
