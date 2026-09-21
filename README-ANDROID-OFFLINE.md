# Android Offline - AiAnalisRambutan

Project ini sudah memiliki versi Android offline berbasis Kivy. Fokus utamanya adalah menjalankan aplikasi tanpa koneksi internet dan menyimpan data di SQLite lokal perangkat.

## Struktur utama

- `main.py` — aplikasi Android PySide6/Qt utama
- `main_kivy.py` — aplikasi Kivy desktop/legacy
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

Dibutuhkan mesin Linux yang kompatibel dengan Android SDK dan NDK. Standar arm64 yang dipakai mengikuti pola yang sudah terbukti pada project `amarPlayer` di `/home/muammar/aplikasiMp3`.

## Setup Android (Python 3.11, arm64)

```bash
cd /home/muammar/AI-Analis-Rambutan-mobile
python3.11 -m venv .venv_android
source .venv_android/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r mobile/requirements.txt
pip install buildozer
```

## Java, SDK, dan NDK standar arm64

Pastikan Java 21 ARM64 terpasang seperti pada amarPlayer dan Android SDK + NDK tersedia
dengan path berikut:

```bash
export JAVA_HOME=/home/muammar/.jdk/jdk-21
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_SDK_ROOT=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_NDK_HOME=/home/muammar/.android-ndk-arm64/r29
export ANDROID_NDK_ROOT=/home/muammar/.android-ndk-arm64/r29
export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
```

## Build APK arm64

```bash
cd /home/muammar/AI-Analis-Rambutan-mobile
source .venv_android/bin/activate
export JAVA_HOME=/home/muammar/.jdk/jdk-21
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_SDK_ROOT=/home/muammar/.buildozer/android/platform/android-sdk
export ANDROID_NDK_HOME=/home/muammar/.android-ndk-arm64/r29
export ANDROID_NDK_ROOT=/home/muammar/.android-ndk-arm64/r29
export JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv6Addresses=false'
./scripts/build_android.sh
```

Atau langsung:

```bash
buildozer android debug
```

## Standar konfigurasi yang dipakai

Project ini mengikuti pola arm64 yang terbukti di `amarPlayer`:

- Python 3.11
- Java 21 ARM64
- Android API 36
- min API 24
- arsitektur `arm64-v8a`
- NDK `/home/muammar/.android-ndk-arm64/r29`
- SDK `/home/muammar/.buildozer/android/platform/android-sdk`

## Catatan penting

- Versi Android ini memang offline dan lokal.
- Model vision/ML berat tidak direpack ke APK. README utama project sudah menjelaskan bahwa model harus dikonversi ke TFLite atau ONNX mobile terlebih dahulu.
- Build APK bergantung pada toolchain Android yang berfungsi di mesin host.
- Pada host ARM64 dengan page size 16K, AAPT2 SDK x86_64 dijalankan melalui
  `muvm` dengan page size guest 4K, bukan langsung melalui FEX. Helper
  `scripts/buildozer_offline.py` menyiapkan override AAPT2 dan menjalankan Gradle
  melalui alur tersebut.
- Jika layanan `muvm`/`passt` tidak tersedia, build akan gagal sebelum APK dihasilkan.

## File helper yang tersedia

- `scripts/setup_android_env.sh`
- `scripts/build_android.sh`
- `scripts/build_android_arm64.sh`
- `scripts/buildozer_offline.py`
- `scripts/build_android_compat.sh`
- `scripts/fix_android_sdk_host.sh`

Semua file ini membantu menyiapkan build Android di mesin yang memiliki toolchain kompatibel.
