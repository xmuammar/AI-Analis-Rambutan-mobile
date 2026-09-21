import os
import subprocess
from pathlib import Path

from buildozer import Buildozer, BuildozerCommandException
from buildozer.targets.android import TargetAndroid


SDK = Path("/home/muammar/.buildozer/android/platform/android-sdk")
NDK = Path("/home/muammar/.android-ndk-arm64/r29")
PIP_WHEELS = Path.cwd() / ".buildozer/offline-wheels"
P4A_RECIPE = Path(".buildozer/android/platform/python-for-android/pythonforandroid/recipe.py")
KIVY_RECIPE = Path(
    ".buildozer/android/platform/python-for-android/pythonforandroid/recipes/kivy/__init__.py"
)
PYJNIUS_RECIPE = Path(
    ".buildozer/android/platform/python-for-android/pythonforandroid/recipes/pyjnius/__init__.py"
)


def configure_offline_pip():
    if not P4A_RECIPE.is_file():
        return
    source = P4A_RECIPE.read_text()
    marker = '            "install",\n'
    replacement = (
        '            "install",\n'
        f'            "--no-index", "--find-links", "{PIP_WHEELS}",\n'
    )
    if marker in source and replacement not in source:
        P4A_RECIPE.write_text(source.replace(marker, replacement, 1))
        source = P4A_RECIPE.read_text()
    env_marker = "        env['HOME'] = '/tmp'\n"
    env_replacement = (
        env_marker
        + f"        env['PIP_NO_INDEX'] = '1'\n"
        + f"        env['PIP_FIND_LINKS'] = '{PIP_WHEELS}'\n"
    )
    if env_marker in source and "env['PIP_NO_INDEX']" not in source:
        P4A_RECIPE.write_text(source.replace(env_marker, env_replacement, 1))
    source = P4A_RECIPE.read_text()
    wheel_marker = '            "--wheel",\n'
    wheel_replacement = wheel_marker + '            "--no-isolation",\n'
    if wheel_marker in source and wheel_replacement not in source:
        P4A_RECIPE.write_text(source.replace(wheel_marker, wheel_replacement, 1))
    if KIVY_RECIPE.is_file():
        kivy_source = KIVY_RECIPE.read_text()
        kivy_source = kivy_source.replace(
            'hostpython_prerequisites = ["cython>=0.29.1,<=3.0.12"]',
            'hostpython_prerequisites = ["Cython>=0.29.1,<=3.0.11", '
            '"setuptools==69.2.0", "wheel==0.44.0"]',
        )
        kivy_source = kivy_source.replace(
            "python_depends = ['certifi', 'chardet', 'idna', 'requests', "
            "'urllib3', 'filetype']",
            "python_depends = []",
        )
        kivy_source = kivy_source.replace(
            "python_depends = ['filetype']",
            "python_depends = []",
        )
        KIVY_RECIPE.write_text(kivy_source)
    if PYJNIUS_RECIPE.is_file():
        pyjnius_source = PYJNIUS_RECIPE.read_text()
        pyjnius_source = pyjnius_source.replace(
            "depends = [('genericndkbuild', 'sdl2', 'sdl3'), 'six']",
            "depends = [('genericndkbuild', 'sdl2', 'sdl3')]",
        )
        PYJNIUS_RECIPE.write_text(pyjnius_source)
    for setup_cfg in Path(".buildozer").glob(
        "android/platform/build-arm64-v8a/build/other_builds/**/kivy/setup.cfg"
    ):
        cfg = setup_cfg.read_text()
        cfg = cfg.replace("    requests\n", "").replace("    filetype\n", "")
        setup_cfg.write_text(cfg)
    source = P4A_RECIPE.read_text()
    source = source.replace(
        '"build[virtualenv]", "pip", "setuptools", "patchelf"',
        '"build[virtualenv]", "pip", "setuptools==69.2.0", "wheel==0.44.0", "patchelf"',
    )
    P4A_RECIPE.write_text(source)


configure_offline_pip()


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
    ["/bin/bash", str(Path("scripts/gradle_muvm.sh").resolve())],
    check=False,
    env={**os.environ, **environment},
)
if result.returncode != 0:
    raise SystemExit(result.returncode)

apk = dist / "build/outputs/apk/debug/aianalisrambutan-debug.apk"
if not apk.is_file():
    raise RuntimeError(f"APK tidak dihasilkan: {apk}")

output_dir = Path("bin")
output_dir.mkdir(exist_ok=True)
output_apk = output_dir / apk.name
output_apk.write_bytes(apk.read_bytes())
print(f"APK tersedia di {output_apk} ({output_apk.stat().st_size} bytes)")
