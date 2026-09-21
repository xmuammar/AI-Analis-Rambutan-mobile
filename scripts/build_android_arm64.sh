#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d "$ROOT_DIR/.venv_android" ]; then
  echo "Android venv belum dibuat. Jalankan scripts/setup_android_env.sh terlebih dahulu."
  exit 1
fi

JDK_DIR="$HOME/.jdk/jdk-21"
export JAVA_HOME="$JDK_DIR"
export PATH="$JDK_DIR/bin:$PATH"
export ANDROID_HOME="/home/muammar/.buildozer/android/platform/android-sdk"
export ANDROID_SDK_ROOT="/home/muammar/.buildozer/android/platform/android-sdk"
export ANDROID_NDK_HOME="/home/muammar/.android-ndk-arm64/r29"
export ANDROID_NDK_ROOT="/home/muammar/.android-ndk-arm64/r29"
export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
export LD_LIBRARY_PATH="$HOME/.android-ndk-arm64/compat${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PIP_NO_INDEX=1
export PIP_FIND_LINKS="$ROOT_DIR/.buildozer/offline-wheels"
export PIP_CONFIG_FILE="$ROOT_DIR/scripts/pip-offline.conf"
export PYTHONNOUSERSITE=1
export CC="$ROOT_DIR/scripts/android_x86_compiler.sh"
export CXX="$ROOT_DIR/scripts/android_x86_compiler.sh"

# shellcheck disable=SC1091
source "$ROOT_DIR/.venv_android/bin/activate"

python scripts/buildozer_offline.py
