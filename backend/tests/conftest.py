import os
from pathlib import Path

# Always point the application at an ephemeral database when running tests.
# Using ``:memory:`` avoids any filesystem permission issues in constrained
# environments and keeps tests hermetic.
os.environ["CHATAGENT_DB"] = str(Path("test_db.sqlite3").absolute())
os.environ["CHATAGENT_DB_IN_MEMORY"] = "1"
