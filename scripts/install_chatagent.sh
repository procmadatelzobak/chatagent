#!/usr/bin/env bash
set -euo pipefail

trap 'echo "[ERROR] Installation failed on line $LINENO" >&2' ERR

# Default installation directory
INSTALL_DIR="${1:-$HOME/chatagent}"

# Determine whether sudo is needed
if command -v sudo >/dev/null 2>&1; then
  SUDO="sudo"
else
  SUDO=""
fi

required_packages=(git python3 python3-venv python3-pip build-essential)
missing_packages=()
for pkg in "${required_packages[@]}"; do
  dpkg -s "$pkg" >/dev/null 2>&1 || missing_packages+=("$pkg")
done

if [ ${#missing_packages[@]} -ne 0 ]; then
  echo "Installing missing packages: ${missing_packages[*]}"
  $SUDO apt-get update || { echo "[ERROR] apt-get update failed" >&2; exit 1; }
  $SUDO apt-get install -y "${missing_packages[@]}" || { echo "[ERROR] package installation failed" >&2; exit 1; }
else
  echo "All required packages already installed."
fi

# Clone repository if not already present
if [ ! -d "$INSTALL_DIR/.git" ]; then
  git clone https://github.com/OWNER/REPO.git "$INSTALL_DIR" || { echo "[ERROR] git clone failed" >&2; exit 1; }
else
  echo "Repository already present at $INSTALL_DIR, skipping clone."
fi

# Set up virtual environment and install package
cd "$INSTALL_DIR/backend" || { echo "[ERROR] backend directory missing" >&2; exit 1; }
if [ ! -d .venv ]; then
  python3 -m venv .venv || { echo "[ERROR] virtual environment creation failed" >&2; exit 1; }
fi
source .venv/bin/activate || { echo "[ERROR] failed to activate virtual environment" >&2; exit 1; }
pip install -e . || { echo "[ERROR] pip install failed" >&2; exit 1; }

echo "ChatAgent installed in $INSTALL_DIR"
