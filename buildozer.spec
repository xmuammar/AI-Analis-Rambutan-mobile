[app]
title = AI Analisis Rambutan
package.name = aianalisisrambutan
package.domain = com.muammar
source.dir = .
source.include_exts = py,html,css,js,json,png,jpg,jpeg,webp,svg,ico
source.exclude_dirs = .git,.buildozer,bin,build,release,debian,packaging,installer,android-wheels,__pycache__,tests,download,deployment,.venv,.venv311,.venv_android,instance
source.exclude_patterns = *.pyc,*.pyo,*.so,*.pt,*.pth
version = 1.0.0
requirements = python3,flask,flask-login,flask-migrate,flask-sqlalchemy,flask-wtf,python-dotenv,email-validator,pillow
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 24
android.archs = arm64-v8a
android.permissions = android.permission.CAMERA
p4a.bootstrap = webview
p4a.port = 5000

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = bin
