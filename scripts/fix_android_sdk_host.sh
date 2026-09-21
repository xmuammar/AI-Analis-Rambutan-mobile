#!/usr/bin/env bash
set -euo pipefail

sudo true >/dev/null 2>&1 || {
  echo "This script needs sudo privileges to adjust systemd-resolved DNS."
  exit 1
}

# Fix systemd-resolved DNS to avoid the Android SDK issue on this host.
sudo mkdir -p /etc/systemd/resolved.conf.d
sudo tee /etc/systemd/resolved.conf.d/10-custom-dns.conf >/dev/null <<'EOF'
[Resolve]
DNS=192.168.100.1 8.8.8.8 1.1.1.1
FallbackDNS=8.8.8.8 1.1.1.1
EOF
sudo systemctl restart systemd-resolved || true

# Ensure Java 17 is installed locally.
JAVA_HOME="/home/muammar/.local/jdk-17.0.15+6"
if [ ! -x "$JAVA_HOME/bin/javac" ]; then
  echo "Downloading JDK 17 to $HOME/.local..."
  mkdir -p "$HOME/.local"
  cd "$HOME/.local"
  curl -L -o jdk17.tar.gz "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.15%2B6/OpenJDK17U-jdk_x64_linux_hotspot_17.0.15_6.tar.gz"
  tar -xzf jdk17.tar.gz
  rm -f jdk17.tar.gz
fi

# Ensure Android cmdline tools are present under the buildozer SDK root.
SDK_ROOT="/home/muammar/.buildozer/android/platform/android-sdk"
mkdir -p "$SDK_ROOT"
if [ ! -x "$SDK_ROOT/tools/bin/sdkmanager" ] && [ -x "$SDK_ROOT/cmdline-tools/cmdline-tools/bin/sdkmanager" ]; then
  ln -sfn "$SDK_ROOT/cmdline-tools/cmdline-tools" "$SDK_ROOT/tools"
fi

if [ ! -x "$SDK_ROOT/cmdline-tools/cmdline-tools/bin/sdkmanager" ]; then
  mkdir -p "$SDK_ROOT/cmdline-tools"
  cd "$SDK_ROOT/cmdline-tools"
  curl -L -o cmdline-tools.zip "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
  unzip -o -q cmdline-tools.zip
  rm -f cmdline-tools.zip
fi

# Install required Android packages.
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"
export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
"$SDK_ROOT/tools/bin/sdkmanager" --sdk_root="$SDK_ROOT" "platform-tools" "platforms;android-35" "build-tools;35.0.0"

printf "\nFix complete. You can now run:\n"
printf "  cd /home/muammar/AI-Analis-Rambutan-mobile\n"
printf "  source .venv_android/bin/activate\n"
printf "  export JAVA_HOME=%s\n" "$JAVA_HOME"
printf "  export PATH=\$JAVA_HOME/bin:\$PATH\n"
printf "  export ANDROID_HOME=%s\n" "$SDK_ROOT"
printf "  export ANDROID_SDK_ROOT=%s\n" "$SDK_ROOT"
printf "  export ANDROID_NDK_HOME=/home/muammar/.android-ndk-arm64/r29\n"
printf "  export ANDROID_NDK_ROOT=/home/muammar/.android-ndk-arm64/r29\n"
printf "  export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'\n"
printf "  buildozer android debug\n"
