
from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path
from .models import *
from ..settings import settings

DB_PATH = settings.data_root / "chatagent.sqlite3"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
