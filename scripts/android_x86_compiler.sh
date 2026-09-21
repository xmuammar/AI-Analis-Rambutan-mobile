#!/usr/bin/env bash
set -euo pipefail

ndk_root="${ANDROID_NDK_HOME:-${ANDROID_NDK_ROOT:-/home/muammar/.buildozer/android/platform/android-ndk-r28c}}"
if [ -z "$ndk_root" ]; then
  echo "ANDROID_NDK_HOME or ANDROID_NDK_ROOT is required." >&2
  exit 1
fi

compiler="$ndk_root/toolchains/llvm/prebuilt/linux-x86_64/bin/clang"
if [ "${ANDROID_CXX:-0}" = "1" ]; then
  compiler="${compiler}++"
fi

exec /usr/bin/muvm \
  --emu=fex \
  --passt-args=--ipv4-only \
  -e "XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/1000}" \
  -e "HOME=${HOME}" \
  -e "ANDROID_NDK_HOME=${ndk_root}" \
  -e "ANDROID_NDK_ROOT=${ndk_root}" \
  "$compiler" "$@"
