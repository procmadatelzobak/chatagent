#!/usr/bin/env bash
set -euo pipefail

trap 'echo "[ERROR] Update failed on line $LINENO" >&2' ERR

# Default installation directory
INSTALL_DIR="${1:-$HOME/chatagent}"

# Optional repository URL to ensure correct remote
REPO_URL="${2:-https://github.com/procmadatelzobak/chatagent.git}"

if [[ -n "$REPO_URL" ]]; then
  if [[ ! "$REPO_URL" =~ ^https://github\.com/.+/.+\.git$ ]]; then
    echo "[ERROR] Invalid repository URL: $REPO_URL" >&2
    exit 1
  fi
fi

if [ ! -d "$INSTALL_DIR/.git" ]; then
  echo "[ERROR] ChatAgent is not installed in $INSTALL_DIR" >&2
  exit 1
fi

cd "$INSTALL_DIR" || { echo "[ERROR] cannot access $INSTALL_DIR" >&2; exit 1; }

if [[ -n "$REPO_URL" ]]; then
  git remote set-url origin "$REPO_URL" || { echo "[ERROR] failed to set remote URL" >&2; exit 1; }
fi

git pull || { echo "[ERROR] git pull failed" >&2; exit 1; }

if [ ! -d backend/.venv ]; then
  echo "[ERROR] virtual environment not found; run install_chatagent.sh first" >&2
  exit 1
fi

cd backend || { echo "[ERROR] backend directory missing" >&2; exit 1; }
source .venv/bin/activate || { echo "[ERROR] failed to activate virtual environment" >&2; exit 1; }
pip install -e . || { echo "[ERROR] pip install failed" >&2; exit 1; }

echo "ChatAgent updated in $INSTALL_DIR"
