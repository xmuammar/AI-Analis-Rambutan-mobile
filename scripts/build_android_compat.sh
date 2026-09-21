#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d "$ROOT_DIR/.venv_android" ]; then
  echo "Android venv not found. Run scripts/setup_android_env.sh first."
  exit 1
fi

export JAVA_HOME="/home/muammar/.local/jdk-17.0.15+6"
export PATH="$JAVA_HOME/bin:$PATH"
export ANDROID_HOME="/home/muammar/.buildozer/android/platform/android-sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export ANDROID_NDK_HOME="/home/muammar/.android-ndk-arm64/r29"
export ANDROID_NDK_ROOT="$ANDROID_NDK_HOME"

# Match the successful amarPlayer build pattern.
if [ -d "$ANDROID_HOME" ] && [ -d "$ANDROID_NDK_HOME" ]; then
  echo "Using SDK: $ANDROID_HOME"
  echo "Using NDK: $ANDROID_NDK_HOME"
else
  echo "Required Android SDK/NDK paths are missing."
  echo "SDK: $ANDROID_HOME"
  echo "NDK: $ANDROID_NDK_HOME"
  exit 1
fi

# Ensure the legacy sdkmanager path points to the current command-line tools.
SDK_TOOLS_DIR="$ANDROID_HOME/tools"
if [ ! -e "$SDK_TOOLS_DIR/bin/sdkmanager" ] || [ ! -x "$SDK_TOOLS_DIR/bin/sdkmanager" ]; then
  mkdir -p "$ANDROID_HOME/tools"
  ln -sfn "$ANDROID_HOME/cmdline-tools/cmdline-tools" "$SDK_TOOLS_DIR"
fi

# shellcheck disable=SC1091
source "$ROOT_DIR/.venv_android/bin/activate"

python - <<'PY'
import os
print('JAVA_HOME=', os.environ.get('JAVA_HOME'))
print('ANDROID_HOME=', os.environ.get('ANDROID_HOME'))
print('ANDROID_SDK_ROOT=', os.environ.get('ANDROID_SDK_ROOT'))
print('ANDROID_NDK_HOME=', os.environ.get('ANDROID_NDK_HOME'))
PY

if [ ! -d "$ANDROID_HOME/platform-tools" ]; then
  "$ANDROID_HOME/tools/bin/sdkmanager" --sdk_root="$ANDROID_HOME" 'platform-tools' >/dev/null
fi

if [ ! -d "$ANDROID_HOME/platforms/android-35" ]; then
  "$ANDROID_HOME/tools/bin/sdkmanager" --sdk_root="$ANDROID_HOME" 'platforms;android-35' 'build-tools;35.0.0' >/dev/null
fi

buildozer android debug
