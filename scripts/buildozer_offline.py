import os
import subprocess
from pathlib import Path

from buildozer import Buildozer, BuildozerCommandException
from buildozer.targets.android import TargetAndroid


SDK = Path("/home/muammar/.buildozer/android/platform/android-sdk")
NDK = Path("/home/muammar/.android-ndk-arm64/r29")


def skip_sdk_manager_when_ready(self):
    required = (
        SDK / "platforms/android-36",
        SDK / "platform-tools",
        SDK / "build-tools/37.0.0",
        NDK,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError(
            "Offline Android toolchain is incomplete; missing: " + ", ".join(missing)
        )
    self.buildozer.info("Using installed amarPlayer-compatible Android toolchain")


TargetAndroid._install_android_packages = skip_sdk_manager_when_ready

compile_platform = TargetAndroid.compile_platform


def compile_without_java_home(self):
    java_home = os.environ.pop("JAVA_HOME", None)
    os.environ["JAVA_HOME"] = "/usr"
    self.buildozer.environ["JAVA_HOME"] = "/usr"
    try:
        return compile_platform(self)
    finally:
        if java_home is not None:
            os.environ["JAVA_HOME"] = java_home
        else:
            os.environ.pop("JAVA_HOME", None)
        self.buildozer.environ["JAVA_HOME"] = ""


TargetAndroid.compile_platform = compile_without_java_home

buildozer_cmd = Buildozer.cmd


def cmd_without_java_home(self, command, **kwargs):
    if any("pythonforandroid" in str(part) for part in command):
        environment = os.environ.copy()
        environment.update(self.environ)
        environment["JAVA_HOME"] = "/home/muammar/.jdk/jdk-21"
        kwargs["env"] = environment
    return buildozer_cmd(self, command, **kwargs)


Buildozer.cmd = cmd_without_java_home

buildozer = Buildozer("buildozer.spec")
try:
    buildozer.run_command(["android", "debug"])
except BuildozerCommandException:
    buildozer.info(
        "Buildozer berhenti pada tahap Gradle; melanjutkan assembleDebug melalui muvm"
    )

dist = Path(".buildozer/android/platform/build-arm64-v8a/dists/aianalisrambutan")
gradle_properties = dist / "gradle.properties"
aapt2 = SDK / "build-tools/37.0.0/aapt2"
if not dist.is_dir() or not gradle_properties.is_file():
    raise RuntimeError(f"Distribution Gradle tidak tersedia: {dist}")
if not aapt2.is_file():
    raise RuntimeError(f"AAPT2 tidak tersedia: {aapt2}")

properties = [
    line
    for line in gradle_properties.read_text().splitlines()
    if not line.startswith("android.aapt2FromMavenOverride=")
]
properties.append(f"android.aapt2FromMavenOverride={aapt2}")
gradle_properties.write_text("\n".join(properties) + "\n")

java_home = "/home/muammar/.jdk/jdk-21"
environment = {
    "JAVA_HOME": java_home,
    "PATH": f"{java_home}/bin:/home/muammar/.local/bin:/usr/local/bin:/usr/bin:/bin",
}
result = subprocess.run(
    [
        "/usr/bin/muvm",
        "--passt-args=--ipv4-only",
        "-e",
        f"JAVA_HOME={java_home}",
        "-e",
        f"PATH={environment['PATH']}",
        "/bin/bash",
        str(Path("scripts/gradle_muvm.sh").resolve()),
    ],
    check=False,
    env={**os.environ, **environment},
)
if result.returncode != 0:
    raise SystemExit(result.returncode)
