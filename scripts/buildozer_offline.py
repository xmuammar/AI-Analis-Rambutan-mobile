import os
from pathlib import Path

from buildozer import Buildozer
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
buildozer.run_command(["android", "debug"])
wrapper = Path(".buildozer/aapt2_fex")
subprocess.run(
    ["cc", "scripts/aapt2_fex.c", "-o", str(wrapper)],
    check=True,
)
wrapper.chmod(0o755)
