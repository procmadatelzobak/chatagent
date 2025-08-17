## Summary

Introduced configuration options to improve testability and responsiveness:

- Added `worker_poll_interval` setting to control how frequently the background worker checks for tasks.
- Added `db_in_memory` setting to allow using an in-memory SQLite database, useful for tests and ephemeral environments.
- Updated database initialization to respect the new in-memory option.
- Enabled previously skipped tests that now run against the in-memory database.