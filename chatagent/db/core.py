from sqlmodel import Session, SQLModel, create_engine

from ..settings import settings

engine = create_engine(
    f"sqlite:///{settings.db}", connect_args={"check_same_thread": False}
)


def init_db() -> None:
    settings.db.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
