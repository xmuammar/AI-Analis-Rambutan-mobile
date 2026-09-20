[app]
title = AiAnalisRambutan Offline
package.name = aianalisrambutan
package.domain = org.aianalisrambutan
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg
version = 0.1.0
requirements = python3,kivy,pillow,plyer
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.allow_backup = 1
