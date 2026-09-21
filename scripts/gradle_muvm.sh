#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT_DIR/.buildozer/android/platform/build-arm64-v8a/dists/aianalisrambutan"

cd "$DIST"

# The generated gradlew delegates to muvm itself. On this host that nested
# invocation loses the project working directory, so invoke Gradle's wrapper
# main class directly inside the guest instead.
exec /usr/bin/muvm \
  --emu=fex \
  --passt-args=--ipv4-only \
  -e "JAVA_HOME=${JAVA_HOME:-/home/muammar/.jdk/jdk-21}" \
  -e "PATH=${JAVA_HOME:-/home/muammar/.jdk/jdk-21}/bin:/usr/bin:/bin" \
  /bin/bash -lc \
  "cd '$DIST' && exec '${JAVA_HOME:-/home/muammar/.jdk/jdk-21}/bin/java' \
  -classpath '$DIST/gradle/wrapper/gradle-wrapper.jar' \
  org.gradle.wrapper.GradleWrapperMain --no-daemon --console=plain \
  -p '$DIST' assembleDebug --stacktrace"
