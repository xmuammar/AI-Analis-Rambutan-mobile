# Android WebView offline

APK ini mempertahankan aplikasi Flask, template Jinja, CSS, dan JavaScript yang
ada. Buildozer memakai `python-for-android` dengan bootstrap `webview`: Flask
berjalan pada `127.0.0.1:5000` di proses aplikasi, lalu WebView Android membuka
server lokal tersebut. Tidak ada server internet yang diperlukan.

## Data offline

Pada desktop, database berada di `instance/`. Pada Android, `ANDROID_PRIVATE`
atau `ANDROID_APP_PATH` dipakai sebagai direktori data aplikasi yang writable.
Database berada di `data/ai_analis_rambutan.sqlite3`, sedangkan foto berada di
`data/uploads/<kode-pohon>/`. Direktori ini tidak berada di source APK sehingga
data tetap ada setelah restart dan upgrade aplikasi.

Seluruh asset web saat ini lokal di `app/static`; audit template tidak menemukan
CDN atau font eksternal. Input foto pemeriksaan sudah memakai `accept="image/*"`
dan `capture="environment"` agar WebView dapat menawarkan kamera belakang.

## Build lokal

Prasyarat: Ubuntu x86_64, Java, Android SDK/NDK, dan Buildozer.

```bash
python3 -m venv .venv-android
source .venv-android/bin/activate
pip install -r requirements-android.txt
pip install buildozer cython==0.29.37
buildozer -v android debug
```

APK debug tersedia di `bin/`. Install dengan:

```

Pada Fedora Asahi ARM64, Build Tools/NDK x86_64 dapat membutuhkan FEX/muvm.
Workflow GitHub Actions adalah jalur build yang direkomendasikan karena berjalan
di Ubuntu x86_64. Helper `scripts/android_x86_compiler.sh` dan
`scripts/android_x86_cxx_compiler.sh` tersedia untuk host ARM64, tetapi beberapa
recipe native masih bergantung pada perilaku FEX host.bash
adb install -r bin/aianalisrambutan-1.0.0-arm64-v8a-debug.apk
```

## GitHub Actions

Workflow `.github/workflows/android-build.yml` membangun pada Ubuntu x86_64,
menggunakan cache Buildozer/Gradle, dan mengunggah artifact
`AI-Analisis-Rambutan-Android`. Jalankan melalui **Actions → Android APK →
Run workflow**.

## Pengujian dan debugging

Uji web dengan `python main.py`, lalu buka `http://127.0.0.1:5000`. Untuk APK,
uji login, pohon, pemeriksaan, kamera, preview/penyimpanan foto, reload,
restart, dan mode pesawat. Log Flask dapat dibaca dengan `adb logcat`.

Model PyTorch/Ultralytics yang besar sengaja tidak dipaketkan ke APK dasar.
Analisis foto tetap dapat menyimpan pemeriksaan dan menggunakan fitur visual
ringan Pillow; model yang tidak tersedia dilaporkan sebagai tidak tersedia,
bukan dianggap sebagai diagnosis.
