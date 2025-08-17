# CI Setup Report

- Added GitHub Actions workflows for linting (`ci-lint.yml`), testing (`ci-test.yml`), and building (`ci-build.yml`).
- Workflows use Python versions 3.10 and 3.11 with pip caching.
- Lint step runs Ruff and Black; failures are tolerated until codebase is formatted.
- Test step runs pytest and attempts editable install; failures are tolerated pending dependencies.
- Build step uses `python -m build` and ignores packaging errors for now.
