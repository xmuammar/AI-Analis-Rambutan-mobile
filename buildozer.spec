[app]
title = AiAnalisRambutan Offline
package.name = aianalisrambutan
package.domain = org.aianalisrambutan
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv
source.exclude_dirs = .git,.buildozer,bin,build,release,debian,packaging,installer,android-wheels,__pycache__,tests,download,deployment,.venv,.venv311,.venv_android,instance,migrations,app
source.exclude_patterns = *.pyc,*.pyo,*.so
version = 0.1.0
requirements = python3==3.11.9,hostpython3==3.11.9,kivy
orientation = portrait
fullscreen = 0
android.api = 36
android.minapi = 24
android.archs = arm64-v8a
android.allow_backup = 1
android.sdk_path = /home/muammar/.buildozer/android/platform/android-sdk
android.ndk_path = /home/muammar/.android-ndk-arm64/r29
android.skip_update = 1
android.permissions = android.permission.CAMERA,android.permission.READ_EXTERNAL_STORAGE,android.permission.WRITE_EXTERNAL_STORAGE
p4a.bootstrap = sdl2
p4a.branch = master
p4a.extra_args = --skip-prebuilt

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = /home/muammar/AI-Analis-Rambutan-mobile
