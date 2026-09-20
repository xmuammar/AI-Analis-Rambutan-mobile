#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 not found. Install it first."
  exit 1
fi

VENV_DIR="$ROOT_DIR/.venv_web"
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
pip install -r "$ROOT_DIR/requirements.txt"

cat <<EOF
Web env is ready.

Use:
  source $VENV_DIR/bin/activate
  cd $ROOT_DIR
  cp .env.example .env
  flask --app run.py run --debug
EOF
