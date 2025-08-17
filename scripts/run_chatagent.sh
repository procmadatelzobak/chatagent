#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${1:-$HOME/chatagent}"

if [ ! -d "$INSTALL_DIR/backend" ]; then
  echo "[ERROR] ChatAgent is not installed in $INSTALL_DIR" >&2
  exit 1
fi

cd "$INSTALL_DIR/backend"

if [ ! -d .venv ]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -e .
else
  source .venv/bin/activate
fi

chatagent serve
