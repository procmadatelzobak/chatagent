#!/usr/bin/env bash
set -Eeuo pipefail

# --- Nastavení ---
REPO_URL="${CHATAGENT_REPO_URL:-https://github.com/procmadatelzobak/chatsimulator.git}"  # <- PLNÁ URL!
BRANCH="${CHATAGENT_BRANCH:-main}"
TARGET_DIR="${CHATAGENT_DIR:-$HOME/chatagent}"

# Neptej se na přihlašovací údaje (když je URL špatně, hned to spadne srozumitelně)
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=/bin/true

echo "Repozitář: $REPO_URL"
echo "Větev:     $BRANCH"
echo "Cíl:       $TARGET_DIR"
echo

# --- Závislosti (jen pokud potřebuješ) ---
if ! command -v git >/dev/null 2>&1; then
  echo "Instaluji git…"
  sudo apt-get update -y
  sudo apt-get install -y git
fi

mkdir -p "$(dirname "$TARGET_DIR")"

# --- Klonování / aktualizace ---
if [ -d "$TARGET_DIR/.git" ]; then
  echo "Repo už existuje, aktualizuji…"
  git -C "$TARGET_DIR" remote set-url origin "$REPO_URL"
  git -C "$TARGET_DIR" fetch --depth=1 origin "$BRANCH"
  git -C "$TARGET_DIR" checkout -B "$BRANCH" "origin/$BRANCH"
else
  echo "Klonuji…"
  git clone --depth=1 --branch "$BRANCH" "$REPO_URL" "$TARGET_DIR"
fi

echo "Hotovo."
