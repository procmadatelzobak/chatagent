import os
from pathlib import Path

os.environ.setdefault("CHATAGENT_DB", str(Path("test_db.sqlite3").absolute()))
