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

JDK_DIR="$HOME/.jdk/jdk-21"
if [ ! -x "$JDK_DIR/bin/javac" ]; then
  echo "JDK 21 ARM64 tidak ditemukan di $JDK_DIR."
  echo "Pasang toolchain yang sama dengan amarPlayer terlebih dahulu."
  exit 1
fi

cat <<EOF
Android env is ready.

Use arm64 config standar seperti amarPlayer:
  export JAVA_HOME=$JDK_DIR
  export PATH=$JDK_DIR/bin:\$PATH
  export ANDROID_HOME=/home/muammar/.buildozer/android/platform/android-sdk
  export ANDROID_SDK_ROOT=/home/muammar/.buildozer/android/platform/android-sdk
  export ANDROID_NDK_HOME=/home/muammar/.android-ndk-arm64/r29
  export ANDROID_NDK_ROOT=/home/muammar/.android-ndk-arm64/r29
  export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
  source $VENV_DIR/bin/activate
  cd $ROOT_DIR
  buildozer android debug
EOF
