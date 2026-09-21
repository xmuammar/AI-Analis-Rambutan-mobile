# AiAnalisRambutan Mobile

Aplikasi analisis dan pencatatan kebun rambutan dengan **mode Android offline** dan
aplikasi web Flask. Repository ini berfokus pada data lapangan yang dapat dijelaskan:
akun lokal, inventaris pohon, inspeksi berkala, riwayat kondisi, backup, dan evaluasi
berbasis aturan. Sistem tidak mengarang diagnosis, confidence, atau pengukuran foto.

Repository: <https://github.com/xmuammar/AI-Analis-Rambutan-mobile>

## Fitur mobile offline

- Login dan pembuatan akun lokal.
- Seed 12 pohon awal untuk pengujian.
- Pencatatan inspeksi dan timeline tanaman.
- Evaluasi kondisi tanaman dengan rule engine explainable.
- Penyimpanan SQLite lokal dan backup JSON.
- Foto inspeksi opsional.
- Tidak membutuhkan jaringan setelah aplikasi terpasang.

`main.py` adalah entrypoint Android berbasis Kivy dan `main_kivy.py` berisi layar
offline Kivy. PySide6/Qt bukan runtime APK karena build Qt gagal tetap berjalan pada
perangkat uji. Model vision/ML berat dari aplikasi web
tidak dipaketkan ke APK; model harus dikonversi dan divalidasi ke TFLite atau ONNX
mobile sebelum digunakan di perangkat.

## Menjalankan mobile secara lokal

```bash
python3 -m venv .venv_mobile
source .venv_mobile/bin/activate
pip install -r mobile/requirements.txt
python main.py
```

Kode offline utama berada di `mobile/storage.py` dan `mobile/rules.py`.

## Build APK Android

Build arm64 Kivy mengikuti toolchain yang kompatibel dengan project amarPlayer:
Python 3.11, Java 21 ARM64, Android API 36, minimum API 24, dan arsitektur
`arm64-v8a`.

```bash
./scripts/setup_android_env.sh
./scripts/build_android_arm64.sh
```

Alternatif setup dan troubleshooting tersedia di
[`README-ANDROID-OFFLINE.md`](README-ANDROID-OFFLINE.md). Konfigurasi build utama ada
di [`buildozer.spec`](buildozer.spec), dan APK debug dihasilkan di `bin/` apabila
toolchain host berhasil menjalankan Gradle/AAPT2. Build dapat gagal pada host yang
menjalankan Android Build Tools x86_64 langsung melalui FEX. Pada host ARM64 dengan
page size 16K, AAPT2 harus dijalankan melalui `muvm` dengan page size guest 4K,
seperti alur yang berhasil dipakai amarPlayer.

## Struktur proyek

| Path | Kegunaan |
| --- | --- |
| `main.py` | Entry point Android Kivy |
| `main_kivy.py` | Layar dan alur aplikasi offline Kivy |
| `mobile/` | Storage SQLite dan rule engine offline |
| `buildozer.spec` | Konfigurasi packaging APK |
| `scripts/` | Setup environment dan helper build Android/web |
| `tests/test_mobile.py` | Tes storage dan rule engine mobile |
| `app/`, `templates/`, `static/` | Aplikasi web Flask |

## Menjalankan aplikasi web

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
flask --app run.py run --debug
```

Buka <http://127.0.0.1:5000>. SQLite adalah database development default; `DATABASE_URL`
dapat diarahkan ke PostgreSQL. Untuk migrasi:

```bash
flask --app run.py db upgrade
flask --app run.py seed-data
```

## Pengujian

```bash
pytest
```

Komponen vision/ML bersifat modular. Jika model belum tersedia, aplikasi melaporkan
`NOT_INSTALLED` atau `INSUFFICIENT_DATA`. Model umum seperti YOLO tidak boleh
dipresentasikan sebagai diagnosis hama, penyakit, atau ukuran agronomi rambutan tanpa
dataset dan evaluasi pertanian khusus.
