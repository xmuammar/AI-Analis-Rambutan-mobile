# Android Offline - AiAnalisRambutan

Project ini sudah memiliki versi Android offline berbasis Kivy. Fokus utamanya adalah menjalankan aplikasi tanpa koneksi internet dan menyimpan data di SQLite lokal perangkat.

## Struktur utama

- `main.py` — aplikasi Android Kivy utama
- `mobile/` — kode offline: SQLite dan rule engine
- `mobile/storage.py` — database SQLite lokal
- `mobile/rules.py` — evaluasi kondisi tanaman secara lokal dan explainable
- `buildozer.spec` — konfigurasi build APK Android

## Tujuan

Aplikasi Android offline ini dapat:

- login lokal
- membuat akun lokal
- menampilkan pohon dan inspeksi
- menyimpan riwayat inspeksi ke SQLite
- mengambil foto opsional
- backup JSON lokal
- mengevaluasi kondisi tanaman tanpa akses internet

## Environment yang dibutuhkan untuk build APK

Dibutuhkan mesin Linux yang kompatibel dengan Android SDK dan NDK, misalnya Ubuntu 22.04/24.04 atau WSL2 dengan Android toolchain yang stabil.

## Setup Android (Python 3.11)

```bash
cd /home/muammar/AI-Analis-Rambutan-mobile
python3.11 -m venv .venv_android
source .venv_android/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r mobile/requirements.txt
pip install buildozer
```

## Java dan Android SDK

Pastikan Java 17 terpasang dan Android SDK + NDK tersedia.

```bash
export JAVA_HOME=/home/muammar/.local/jdk-17.0.15+6
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_SDK_ROOT=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_NDK_HOME=/home/muammar/.android-ndk-arm64/r29
export ANDROID_NDK_ROOT=/home/muammar/.android-ndk-arm64/r29
export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
```

## Build APK

```bash
cd /home/muammar/AI-Analis-Rambutan-mobile
source .venv_android/bin/activate
export JAVA_HOME=/home/muammar/.local/jdk-17.0.15+6
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_SDK_ROOT=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_NDK_HOME=/home/muammar/.android-ndk-arm64/r29
export ANDROID_NDK_ROOT=/home/muammar/.android-ndk-arm64/r29
export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
buildozer android debug
```

## Catatan penting

- Versi Android ini memang offline dan lokal.
- Model vision/ML berat tidak direpack ke APK. README utama project sudah menjelaskan bahwa model harus dikonversi ke TFLite atau ONNX mobile terlebih dahulu.
- Build APK bergantung pada toolchain Android yang berfungsi di mesin host.
- Jika host Linux intermiten atau punya masalah SDK manager / IPv6 / DNS, build akan gagal sebelum aplikasi benar-benar dikompilasi.

## File helper yang tersedia

- `scripts/setup_android_env.sh`
- `scripts/build_android.sh`
- `scripts/build_android_compat.sh`
- `scripts/fix_android_sdk_host.sh`

Semua file ini membantu menyiapkan build Android di mesin yang memiliki toolchain kompatibel.
