# Security Baseline Report

## Dependabot
Configured weekly update checks for Python packages in `backend` and GitHub Actions.

## CodeQL
Added CodeQL analysis workflow for Python to run on pushes, pull requests, and weekly schedule.

## Policies
- Added `SECURITY.md` with reporting instructions.
- Expanded `.gitignore` and added `.gitattributes` for consistent line endings.

## Secret Scan
`gitleaks` found no secrets in the repository.
