## Summary

Introduced configuration options to improve testability and responsiveness:

- Added `worker_poll_interval` setting to control how frequently the background worker checks for tasks.
- Added `db_in_memory` setting to allow using an in-memory SQLite database, useful for tests and ephemeral environments.
- Updated database initialization to respect the new in-memory option.
- Enabled previously skipped tests that now run against the in-memory database.

## Fix repository URL in install scripts

- Added validation and configurable repository URL to `scripts/install_chatagent.sh` and `scripts/update_chatagent.sh` to prevent cloning the GitHub root when repository parameters are missing.

## Auto-run ChatAgent after installation

- Default repository URL in scripts now uses the full HTTPS link.
- Added `scripts/run_chatagent.sh` to set up a virtual environment and start the server.
- `scripts/install_chatagent.sh` now invokes the new run script after cloning to launch the application immediately.

