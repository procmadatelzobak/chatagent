#!/usr/bin/env bash
set -euo pipefail

trap 'echo "[ERROR] Update failed on line $LINENO" >&2' ERR

# Default installation directory
INSTALL_DIR="${1:-$HOME/chatagent}"

if [ ! -d "$INSTALL_DIR/.git" ]; then
  echo "[ERROR] ChatAgent is not installed in $INSTALL_DIR" >&2
  exit 1
fi

cd "$INSTALL_DIR" || { echo "[ERROR] cannot access $INSTALL_DIR" >&2; exit 1; }
GIT_TERMINAL_PROMPT=0 git pull || { echo "[ERROR] git pull failed" >&2; exit 1; }

if [ ! -d backend/.venv ]; then
  echo "[ERROR] virtual environment not found; run install_chatagent.sh first" >&2
  exit 1
fi

cd backend || { echo "[ERROR] backend directory missing" >&2; exit 1; }
source .venv/bin/activate || { echo "[ERROR] failed to activate virtual environment" >&2; exit 1; }
pip install -e . || { echo "[ERROR] pip install failed" >&2; exit 1; }

echo "ChatAgent updated in $INSTALL_DIR"
