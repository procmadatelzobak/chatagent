import json
import logging
from typing import Any


class JsonFormatter(logging.Formatter):
    """Format log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        log_record: dict[str, Any] = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


class PiiFilter(logging.Filter):
    """Redact messages marked as PII when disabled."""

    def __init__(self, show_pii: bool) -> None:
        super().__init__()
        self.show_pii = show_pii

    def filter(self, record: logging.LogRecord) -> bool:  # type: ignore[override]
        if not self.show_pii and getattr(record, "pii", False):
            record.msg = "[REDACTED]"
        return True


def setup_logging(level: str = "INFO", show_pii: bool = False) -> None:
    """Configure root logger for structured JSON output."""

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(PiiFilter(show_pii))
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
