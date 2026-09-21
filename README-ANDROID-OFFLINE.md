# Build Android WebView Offline

Repository ini membungkus aplikasi Flask yang sudah ada ke APK Android melalui
python-for-android `webview` bootstrap. Template Jinja, CSS, JavaScript, route,
SQLite, upload foto, dan alur analisis tetap berasal dari aplikasi Flask.
Kivy bukan UI aplikasi ini.

## Arsitektur

```text
APK Android
  └── Flask lokal (127.0.0.1:5000)
        └── Android WebView
              └── app/templates + app/static + SQLite + uploads
```

`main.py` mematikan debug/reloader dan hanya mengikat loopback saat mendeteksi
runtime Android. `config.py` memindahkan SQLite dan foto ke direktori private
aplikasi yang writable; source APK tetap read-only.

## Build

```bash
python3 -m venv .venv-android
source .venv-android/bin/activate
pip install -r requirements-android.txt
pip install buildozer cython==0.29.37
buildozer -v android debug
```

Hasilnya berada di `bin/`. Build CI tersedia melalui
`.github/workflows/android-build.yml` dan artifact bernama
`AI-Analisis-Rambutan-Android`.

## Offline dan kamera

Audit template tidak menemukan CDN. Semua CSS dan JavaScript disajikan melalui
`url_for('static', ...)`. Form pemeriksaan menggunakan `accept="image/*"` dan
`capture="environment"`; WebView akan meneruskan pemilihan/kamera yang tersedia
di perangkat. Foto dikaitkan dengan sesi pengamatan dan pohon melalui route
Flask yang sudah ada.

Analisis ringan Pillow dapat berjalan lokal. Model besar yang tidak kompatibel
atau belum dikemas diberi status tidak tersedia; pengguna tetap dapat mengisi
dan menyimpan form secara manual.

## Debugging

Jalankan `python main.py` untuk uji browser desktop. Pada perangkat, gunakan
`adb logcat` untuk melihat log startup Flask/WebView. Uji login, pohon,
pemeriksaan, foto, reload, restart, dan mode pesawat sebelum distribusi.
