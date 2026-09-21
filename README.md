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

`main.py` adalah entrypoint Flask untuk desktop dan Android WebView. Pada APK,
Flask berjalan lokal di `127.0.0.1:5000` dan WebView membuka halaman HTML yang
sama; UI tidak diubah menjadi Kivy atau Qt. Model vision/ML berat tidak
dipaketkan ke APK dasar, sehingga fitur yang tidak memiliki model melaporkan
statusnya secara eksplisit dan pemeriksaan manual tetap dapat digunakan.

## Menjalankan aplikasi lokal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Build APK Android

APK memakai python-for-android WebView bootstrap dan target `arm64-v8a`.
Instruksi lengkap ada di [`ANDROID_BUILD.md`](ANDROID_BUILD.md).

## Struktur proyek

| Path | Kegunaan |
| --- | --- |
| `main.py` | Entry point Flask desktop dan WebView Android |
| `app/templates/` | UI HTML/Jinja yang dipakai browser dan APK |
| `app/static/` | CSS/JavaScript lokal, tanpa CDN |
| `config.py` | Konfigurasi database/upload writable Android |
| `buildozer.spec` | Konfigurasi python-for-android WebView |
| `.github/workflows/android-build.yml` | Build APK Ubuntu x86_64 |
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
