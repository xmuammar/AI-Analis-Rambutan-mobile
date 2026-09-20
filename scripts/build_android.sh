#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VENV_DIR="$ROOT_DIR/.venv_android"
if [ ! -d "$VENV_DIR" ]; then
  echo "Android venv not found. Run scripts/setup_android_env.sh first."
  exit 1
fi

JDK_DIR="$HOME/.local/jdk-17.0.15+6"
export JAVA_HOME="$JDK_DIR"
export PATH="$JDK_DIR/bin:$PATH"

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

buildozer android debug
