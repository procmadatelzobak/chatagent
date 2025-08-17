#!/usr/bin/env bash
set -Eeuo pipefail

# === Nastavení ===
# Repo můžeš přepsat env proměnnou CHATAGENT_REPO (formát owner/repo nebo plná URL)
# Př.: CHATAGENT_REPO="procmadatelzobak/chatsimulator"
REPO_INPUT="${CHATAGENT_REPO:-procmadatelzobak/chatsimulator}"
BRANCH="${CHATAGENT_BRANCH:-main}"
TARGET_DIR="${CHATAGENT_DIR:-$HOME/chatagent}"

# === Normalizace URL na HTTPS bez přihlašování ===
if [[ "$REPO_INPUT" =~ ^https?:// ]]; then
  # plná URL -> očistit o trailing slash a doplnit .git, pokud chybí
  REPO_URL="${REPO_INPUT%/}"
  [[ "$REPO_URL" != *.git ]] && REPO_URL="${REPO_URL}.git"
else
  # owner/repo -> složit na https
  REPO_URL="https://github.com/${REPO_INPUT%/}"
  [[ "$REPO_URL" != *.git ]] && REPO_URL="${REPO_URL}.git"
fi

export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=/bin/true

echo "Repozitář: $REPO_URL"
echo "Větev:     $BRANCH"
echo "Cíl:       $TARGET_DIR"
echo

# === Závislosti ===
if ! command -v git >/dev/null 2>&1; then
  echo "Instaluji git…"
  sudo apt-get update -y
  sudo apt-get install -y git ca-certificates
fi

mkdir -p "$(dirname "$TARGET_DIR")"

# === Rychlá validace dostupnosti repozitáře (veřejnost / překlep) ===
echo "Kontroluji dostupnost repozitáře…"
TMP_ERR="$(mktemp)"
if ! git ls-remote --exit-code "$REPO_URL" >/dev/null 2>"$TMP_ERR"; then
  echo "❌ Nelze načíst repozitář: $REPO_URL"
  if grep -qi "Repository not found" "$TMP_ERR"; then
    echo "   → GitHub vrací 'Repository not found'. Obvykle jde o překlep v owner/repo nebo repo neexistuje."
  elif grep -qi "Authentication failed" "$TMP_ERR"; then
    echo "   → 'Authentication failed' u veřejného repa většinou také značí špatnou URL (překlep / jiné jméno)."
  else
    echo "   → Detail chyby:"
    sed 's/^/      /' "$TMP_ERR" || true
  fi
  rm -f "$TMP_ERR"
  exit 1
fi
rm -f "$TMP_ERR"

# === Klonování / aktualizace ===
if [ -d "$TARGET_DIR/.git" ]; then
  echo "Repo už existuje, aktualizuji…"
  git -C "$TARGET_DIR" remote set-url origin "$REPO_URL"
  git -C "$TARGET_DIR" fetch --depth=1 origin
  # Pokus o přepnutí na požadovanou větev, pokud existuje
  if git -C "$TARGET_DIR" rev-parse --verify --quiet "origin/$BRANCH"; then
    git -C "$TARGET_DIR" checkout -B "$BRANCH" "origin/$BRANCH"
  else
    echo "Pozn.: Větev '$BRANCH' na originu neexistuje, ponechávám výchozí."
  fi
else
  echo "Klonuji…"
  git clone --filter=blob:none --depth=1 "$REPO_URL" "$TARGET_DIR"
  # Po klonu přepnout na požadovanou větev, pokud existuje
  if git -C "$TARGET_DIR" rev-parse --verify --quiet "origin/$BRANCH"; then
    git -C "$TARGET_DIR" checkout -B "$BRANCH" "origin/$BRANCH"
  fi
fi

echo "✅ Hotovo."
