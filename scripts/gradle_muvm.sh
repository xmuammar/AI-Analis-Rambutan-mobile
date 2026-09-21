#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT_DIR/.buildozer/android/platform/build-arm64-v8a/dists/aianalisrambutan"

cd "$DIST"
exec ./gradlew --no-daemon --console=plain assembleDebug --stacktrace
