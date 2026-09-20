#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3.11 >/dev/null 2>&1; then
  echo "Python 3.11 not found. Install it first."
  exit 1
fi

VENV_DIR="$ROOT_DIR/.venv_android"
if [ ! -d "$VENV_DIR" ]; then
  python3.11 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
pip install -r "$ROOT_DIR/mobile/requirements.txt"
pip install buildozer

JDK_DIR="$HOME/.local/jdk-17.0.15+6"
if [ ! -x "$JDK_DIR/bin/javac" ]; then
  mkdir -p "$HOME/.local"
  cd "$HOME/.local"
  curl -L -o jdk17.tar.gz "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.15%2B6/OpenJDK17U-jdk_x64_linux_hotspot_17.0.15_6.tar.gz"
  tar -xzf jdk17.tar.gz
  rm -f jdk17.tar.gz
fi

cat <<EOF
Android env is ready.

Use:
  export JAVA_HOME=$JDK_DIR
  export PATH=$JDK_DIR/bin:\$PATH
  source $VENV_DIR/bin/activate
  cd $ROOT_DIR
  buildozer android debug
EOF
