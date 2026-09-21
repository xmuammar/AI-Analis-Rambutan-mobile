from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen

from mobile.rules import evaluate_condition
from mobile.storage import LocalStore


KV = """
<Card@BoxLayout>:
    padding: "16dp"
    spacing: "8dp"
    canvas.before:
        Color:
            rgba: .97, 1, .97, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [14, 14, 14, 14]
        Color:
            rgba: .82, .9, .84, 1
        Line:
            rounded_rectangle: self.x, self.y, self.width, self.height, 14
<NavBar@BoxLayout>:
    size_hint_y: None
    height: "48dp"
    spacing: "6dp"
    padding: "8dp", "5dp"
    canvas.before:
        Color:
            rgba: .09, .19, .15, 1
        Rectangle:
            pos: self.pos
            size: self.size
<NavButton@Button>:
    background_normal: ""
    background_color: 0, 0, 0, 0
    color: .78, .9, .81, 1
    font_size: "12sp"
<PrimaryButton@Button>:
    background_normal: ""
    background_color: .14, .38, .23, 1
    color: 1, 1, 1, 1
    bold: True
    size_hint_y: None
    height: "48dp"
<SectionLabel@Label>:
    color: .14, .38, .23, 1
    bold: True
    font_size: "11sp"
    size_hint_y: None
    height: "24dp"
    text_size: self.size
    halign: "left"
    valign: "middle"
<LoginScreen>:
    ScrollView:
        do_scroll_x: False
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: "8dp", "18dp", "8dp", "62dp"
            spacing: "12dp"
            Widget:
                size_hint_y: None
                height: "12dp"
            Card:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                size_hint_x: 1
                padding: "18dp"
                spacing: "10dp"
                Label:
                    text: "WORKSTATION KEBUN"
                    color: .14, .38, .23, 1
                    bold: True
                    font_size: "11sp"
                    size_hint_y: None
                    height: "24dp"
                    text_size: self.width, None
                    halign: "left"
                Label:
                    text: "AI - Analis Rambutan"
                    color: .09, .19, .15, 1
                    font_size: "27sp"
                    bold: True
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8)
                    text_size: self.width, None
                    halign: "left"
                Label:
                    text: "Kelola pemeriksaan longitudinal untuk kebun rambutan Anda."
                    color: .39, .46, .42, 1
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8)
                    halign: "left"
                Label:
                    text: "Masuk untuk melanjutkan ke dashboard kebun."
                    color: .39, .46, .42, 1
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4)
                    halign: "left"
                TextInput:
                    id: username
                    hint_text: "Nama pengguna"
                    background_color: 1, 1, 1, 1
                    foreground_color: .09, .19, .15, 1
                    multiline: False
                    size_hint_y: None
                    height: "48dp"
                    padding: "12dp", "12dp"
                TextInput:
                    id: password
                    hint_text: "Kata sandi"
                    password: True
                    multiline: False
                    size_hint_y: None
                    height: "48dp"
                    padding: "12dp", "12dp"
                PrimaryButton:
                    text: "Masuk"
                    on_release: root.login()
                Button:
                    text: "Buat akun lokal"
                    color: .14, .38, .23, 1
                    background_normal: ""
                    background_color: 0, 0, 0, 0
                    size_hint_y: None
                    height: "42dp"
                    on_release: app.show_register()
                Label:
                    text: root.message
                    color: .65, .2, .2, 1
                    text_size: self.width, None
                    size_hint_y: None
                    height: max(dp(4), self.texture_size[1])
            Label:
                text: "© 2026 AI - Analis Rambutan · Data tersimpan lokal"
                color: .39, .46, .42, 1
                font_size: "12sp"
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1] + dp(8)
                halign: "center"
<RegisterScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "18dp"
        canvas.before:
            Color:
                rgba: .95, .98, .95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Widget:
            size_hint_y: .16
        Card:
            orientation: "vertical"
            size_hint_y: None
            height: "430dp"
            padding: "24dp"
            spacing: "12dp"
            Label:
                text: "AKUN LOKAL"
                color: .14, .38, .23, 1
                bold: True
                font_size: "11sp"
                size_hint_y: None
                height: "24dp"
            Label:
                text: "Buat akun"
                color: .09, .19, .15, 1
                font_size: "28sp"
                bold: True
                size_hint_y: None
                height: "55dp"
                text_size: self.size
                halign: "left"
            TextInput:
                id: username
                hint_text: "Nama pengguna"
                multiline: False
                size_hint_y: None
                height: "46dp"
            TextInput:
                id: password
                hint_text: "Kata sandi minimal 8 karakter"
                password: True
                multiline: False
                size_hint_y: None
                height: "46dp"
            TextInput:
                id: password_confirm
                hint_text: "Ulangi kata sandi"
                password: True
                multiline: False
                size_hint_y: None
                height: "46dp"
            PrimaryButton:
                text: "Buat akun"
                on_release: root.create_account()
            Label:
                text: root.message
                color: .65, .2, .2, 1
                text_size: self.width, None
            Button:
                text: "Kembali ke masuk"
                color: .14, .38, .23, 1
                background_normal: ""
                background_color: 0, 0, 0, 0
                size_hint_y: None
                height: "38dp"
                on_release: app.show_login()
        Widget:
            size_hint_y: .2

<DashboardScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: .95, .98, .95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        NavBar:
            Label:
                text: "AI - ANALIS RAMBUTAN"
                color: 1, 1, 1, 1
                bold: True
                font_size: "13sp"
            NavButton:
                text: "Beranda"
                on_release: app.show_dashboard()
            NavButton:
                text: "Pohon Saya"
                on_release: app.show_trees()
            NavButton:
                text: "Panduan"
                on_release: app.show_about()
            NavButton:
                text: "Keluar"
                on_release: app.logout()
        ScrollView:
            bar_width: "4dp"
            GridLayout:
                cols: 1
                padding: "14dp", "18dp", "14dp", "24dp"
                spacing: "14dp"
                size_hint_y: None
                height: self.minimum_height
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "18dp"
                    spacing: "7dp"
                    Label:
                        text: "BUKU KERJA PENGAMATAN KEBUN"
                        color: .14, .38, .23, 1
                        bold: True
                        font_size: "11sp"
                        size_hint_y: None
                        height: "22dp"
                        text_size: self.size
                        halign: "left"
                    Label:
                        text: "Ringkasan Kondisi Kebun"
                        color: .09, .19, .15, 1
                        font_size: "27sp"
                        bold: True
                        size_hint_y: None
                        height: "40dp"
                        text_size: self.width, None
                        halign: "left"
                    Label:
                        text: "Pusat keputusan lapangan untuk memantau kesehatan, pertumbuhan, perawatan, pembungaan, pembuahan, dan hasil pohon Rambutan Belereng."
                        color: .39, .46, .42, 1
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                    PrimaryButton:
                        text: "Mulai putaran pemeriksaan"
                        on_release: app.show_trees()
                GridLayout:
                    cols: 2
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height
                    Card:
                        orientation: "vertical"
                        size_hint_y: None
                        height: "126dp"
                        Label:
                            text: "KONDISI BAIK"
                            color: .39, .46, .42, 1
                            size_hint_y: None
                            height: "22dp"
                        Label:
                            text: root.healthy
                            color: .14, .38, .23, 1
                            font_size: "29sp"
                            bold: True
                            size_hint_y: None
                            height: "42dp"
                        Label:
                            text: "dari " + root.total + " pohon aktif"
                            color: .39, .46, .42, 1
                    Card:
                        orientation: "vertical"
                        size_hint_y: None
                        height: "126dp"
                        Label:
                            text: "PERLU DIAMATI"
                            color: .39, .46, .42, 1
                            size_hint_y: None
                            height: "22dp"
                        Label:
                            text: root.watch
                            color: .6, .39, .08, 1
                            font_size: "29sp"
                            bold: True
                            size_hint_y: None
                            height: "42dp"
                        Label:
                            text: "pantau perubahan berikutnya"
                            color: .39, .46, .42, 1
                GridLayout:
                    cols: 2
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height
                    Card:
                        orientation: "vertical"
                        size_hint_y: None
                        height: "126dp"
                        Label:
                            text: "PRIORITAS TINDAKAN"
                            color: .39, .46, .42, 1
                            size_hint_y: None
                            height: "22dp"
                        Label:
                            text: root.action
                            color: .63, .28, .28, 1
                            font_size: "29sp"
                            bold: True
                            size_hint_y: None
                            height: "42dp"
                        Label:
                            text: "prioritas hari ini"
                            color: .39, .46, .42, 1
                    Card:
                        orientation: "vertical"
                        size_hint_y: None
                        height: "126dp"
                        Label:
                            text: "KEYAKINAN PENILAIAN"
                            color: .39, .46, .42, 1
                            size_hint_y: None
                            height: "22dp"
                        Label:
                            text: root.confidence
                            color: .14, .38, .23, 1
                            font_size: "29sp"
                            bold: True
                            size_hint_y: None
                            height: "42dp"
                        Label:
                            text: root.priority_count + " pohon perlu perhatian"
                            color: .39, .46, .42, 1
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "16dp"
                    SectionLabel:
                        text: "KONTINUITAS PENGAMATAN"
                    Label:
                        text: "Putaran pemeriksaan 30 hari"
                        color: .09, .19, .15, 1
                        bold: True
                        font_size: "20sp"
                        size_hint_y: None
                        height: "32dp"
                    Label:
                        text: root.observation_summary
                        color: .39, .46, .42, 1
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "16dp"
                    SectionLabel:
                        text: "KOMPOSISI"
                    Label:
                        text: "Status kebun"
                        color: .09, .19, .15, 1
                        bold: True
                        font_size: "20sp"
                        size_hint_y: None
                        height: "32dp"
                    Label:
                        text: root.distribution
                        color: .09, .19, .15, 1
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "16dp"
                    SectionLabel:
                        text: "DECISION SUPPORT"
                    Label:
                        text: "Prioritas hari ini"
                        color: .09, .19, .15, 1
                        bold: True
                        font_size: "20sp"
                        size_hint_y: None
                        height: "32dp"
                    Label:
                        text: root.priority_text
                        color: .09, .19, .15, 1
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "16dp"
                    SectionLabel:
                        text: "AI ENGINE"
                    Label:
                        text: "●  Local-first aktif"
                        color: .14, .38, .23, 1
                        font_size: "20sp"
                        bold: True
                        size_hint_y: None
                        height: "32dp"
                    Label:
                        text: "Vision pipeline siap digunakan · READY"
                        color: .39, .46, .42, 1
                        size_hint_y: None
                        height: "28dp"
                    Label:
                        text: "Object detection       AVAILABLE\\nClassification           AVAILABLE\\nSegmentation            AVAILABLE\\nModel rambutan khusus  NEEDS_DATA"
                        color: .14, .38, .23, 1
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "16dp"
                    SectionLabel:
                        text: "LONGITUDINAL MONITORING"
                    Label:
                        text: "Status seluruh pohon"
                        color: .09, .19, .15, 1
                        bold: True
                        font_size: "20sp"
                        size_hint_y: None
                        height: "32dp"
                    Label:
                        text: root.tree_status
                        color: .09, .19, .15, 1
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                GridLayout:
                    cols: 2
                    spacing: "10dp"
                    size_hint_y: None
                    height: "112dp"
                    Card:
                        orientation: "vertical"
                        padding: "12dp"
                        Label:
                            text: "🌳  Pohon Saya"
                            color: .14, .38, .23, 1
                            bold: True
                            font_size: "17sp"
                        Label:
                            text: "Timeline dan pemeriksaan setiap pohon."
                            color: .39, .46, .42, 1
                            text_size: self.width, None
                            halign: "left"
                    Card:
                        orientation: "vertical"
                        padding: "12dp"
                        Label:
                            text: "🧠  Tentang Algoritma"
                            color: .14, .38, .23, 1
                            bold: True
                            font_size: "17sp"
                        Label:
                            text: "Algoritma, pipeline, dan batasan analisis AI."
                            color: .39, .46, .42, 1
                            text_size: self.width, None
                            halign: "left"
                Label:
                    text: "© 2026 AI - Analis Rambutan · Data tersimpan lokal"
                    color: .39, .46, .42, 1
                    size_hint_y: None
                    height: "36dp"
                    text_size: self.width, None
                    halign: "center"

<AboutScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: .95, .98, .95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        NavBar:
            Label:
                text: "AI - ANALIS RAMBUTAN"
                color: 1, 1, 1, 1
                bold: True
            NavButton:
                text: "Beranda"
                on_release: app.show_dashboard()
            NavButton:
                text: "Pohon Saya"
                on_release: app.show_trees()
        ScrollView:
            GridLayout:
                cols: 1
                padding: "14dp"
                spacing: "12dp"
                size_hint_y: None
                height: self.minimum_height
                Label:
                    text: "PANDUAN ANALISIS"
                    color: .14, .38, .23, 1
                    bold: True
                    font_size: "11sp"
                    size_hint_y: None
                    height: "24dp"
                Label:
                    text: "Tentang Algoritma"
                    color: .09, .19, .15, 1
                    font_size: "27sp"
                    bold: True
                    size_hint_y: None
                    height: "45dp"
                Label:
                    text: "Analisis lokal membantu menyusun bukti pemeriksaan, bukan menggantikan keputusan analis lapangan."
                    color: .39, .46, .42, 1
                    text_size: self.width, None
                    size_hint_y: None
                    height: "45dp"
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "118dp"
                    Label:
                        text: "01  Rule-Based Expert System"
                        color: .14, .38, .23, 1
                        bold: True
                        font_size: "18sp"
                    Label:
                        text: "Menggabungkan kelembapan, genangan, kondisi daun, dan catatan menjadi kondisi serta confidence yang mudah dijelaskan."
                        color: .39, .46, .42, 1
                        text_size: self.width, None
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "118dp"
                    Label:
                        text: "02  Local-first"
                        color: .14, .38, .23, 1
                        bold: True
                        font_size: "18sp"
                    Label:
                        text: "Data SQLite dan hasil inspeksi tersimpan di perangkat. Aplikasi dapat digunakan tanpa koneksi internet."
                        color: .39, .46, .42, 1
                        text_size: self.width, None
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "118dp"
                    Label:
                        text: "03  Kontinuitas pengamatan"
                        color: .14, .38, .23, 1
                        bold: True
                        font_size: "18sp"
                    Label:
                        text: "Gunakan pemeriksaan berkala untuk membangun baseline dan melihat perubahan kondisi setiap pohon."
                        color: .39, .46, .42, 1
                        text_size: self.width, None

<TreesScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: .95, .98, .95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        NavBar:
            Label:
                text: "AI - ANALIS RAMBUTAN"
                color: 1, 1, 1, 1
                bold: True
            NavButton:
                text: "Beranda"
                on_release: app.show_dashboard()
            NavButton:
                text: "Backup JSON"
                on_release: app.export_backup()
            NavButton:
                text: "Keluar"
                on_release: app.logout()
        ScrollView:
            GridLayout:
                cols: 1
                padding: "14dp"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height
                Label:
                    text: "REGISTER TANAMAN"
                    color: .14, .38, .23, 1
                    bold: True
                    font_size: "11sp"
                    size_hint_y: None
                    height: "24dp"
                    text_size: self.size
                    halign: "left"
                Label:
                    text: "Daftar Pohon dan Petak"
                    color: .09, .19, .15, 1
                    font_size: "27sp"
                    bold: True
                    size_hint_y: None
                    height: "45dp"
                    text_size: self.size
                    halign: "left"
                Label:
                    text: "Pilih pohon untuk membuka profil dan riwayat pengamatan."
                    color: .39, .46, .42, 1
                    size_hint_y: None
                    height: "35dp"
                    text_size: self.width, None
                Label:
                    id: tree_count
                    text: ""
                    color: .39, .46, .42, 1
                    size_hint_y: None
                    height: "25dp"
                GridLayout:
                    id: tree_list
                    cols: 1
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height

<TreeProfileScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: .95, .98, .95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        NavBar:
            Label:
                text: "AI - ANALIS RAMBUTAN"
                color: 1, 1, 1, 1
                bold: True
            NavButton:
                text: "Pohon Saya"
                on_release: app.show_trees()
            NavButton:
                text: "Beranda"
                on_release: app.show_dashboard()
        ScrollView:
            GridLayout:
                cols: 1
                padding: "14dp"
                spacing: "12dp"
                size_hint_y: None
                height: self.minimum_height
                Button:
                    text: "‹  Kembali ke register pohon"
                    color: .14, .38, .23, 1
                    background_normal: ""
                    background_color: 0, 0, 0, 0
                    size_hint_y: None
                    height: "35dp"
                    halign: "left"
                    on_release: app.show_trees()
                Label:
                    text: "PROFIL TANAMAN · " + root.variety.upper()
                    color: .14, .38, .23, 1
                    bold: True
                    font_size: "11sp"
                    size_hint_y: None
                    height: "24dp"
                    text_size: self.size
                    halign: "left"
                Label:
                    text: root.tree_code
                    color: .09, .19, .15, 1
                    font_size: "30sp"
                    bold: True
                    size_hint_y: None
                    height: "48dp"
                    text_size: self.size
                    halign: "left"
                Label:
                    text: "🌳  Rambutan · Catatan longitudinal"
                    color: .39, .46, .42, 1
                    size_hint_y: None
                    height: "32dp"
                    text_size: self.size
                    halign: "left"
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "205dp"
                    SectionLabel:
                        text: "IDENTITAS PETAK"
                    Label:
                        text: "Data dasar tanaman"
                        color: .09, .19, .15, 1
                        font_size: "19sp"
                        bold: True
                    Label:
                        text: "Varietas                         " + root.variety + "\\nStatus                            " + root.status + "\\nSesi pengamatan          " + root.observation_count
                        color: .39, .46, .42, 1
                        text_size: self.width, None
                        valign: "middle"
                    PrimaryButton:
                        text: "Buka lembar pemeriksaan"
                        on_release: app.show_inspection_from_profile()
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "180dp"
                    SectionLabel:
                        text: "TINJAUAN TERAKHIR"
                    Label:
                        text: root.summary
                        color: .09, .19, .15, 1
                        text_size: self.width, None
                    Label:
                        text: root.timeline
                        color: .39, .46, .42, 1
                        text_size: self.width, None
                        valign: "top"
                        halign: "left"

<InspectionScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: .95, .98, .95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        NavBar:
            Label:
                text: "AI - ANALIS RAMBUTAN"
                color: 1, 1, 1, 1
                bold: True
            NavButton:
                text: "Pohon Saya"
                on_release: app.show_trees()
            NavButton:
                text: "Beranda"
                on_release: app.show_dashboard()
        ScrollView:
            GridLayout:
                cols: 1
                padding: "14dp"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height
                Label:
                    text: "CATATAN INSPEKSI LAPANGAN"
                    color: .14, .38, .23, 1
                    bold: True
                    font_size: "11sp"
                    size_hint_y: None
                    height: "24dp"
                Label:
                    text: "Pemeriksaan " + root.tree_code
                    color: .09, .19, .15, 1
                    font_size: "27sp"
                    bold: True
                    size_hint_y: None
                    height: "45dp"
                Label:
                    text: "Lengkapi dokumentasi kondisi pohon hari ini. Hasil analisis menjadi bahan penilaian awal."
                    color: .39, .46, .42, 1
                    text_size: self.width, None
                    size_hint_y: None
                    height: "42dp"
                Card:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "245dp"
                    SectionLabel:
                        text: "01  PENILAIAN KONDISI"
                    Label:
                        text: "Observasi vegetatif"
                        color: .09, .19, .15, 1
                        font_size: "20sp"
                        bold: True
                    BoxLayout:
                        size_hint_y: None
                        height: "42dp"
                        Label:
                            text: "Permukaan tanah gelap / lembap"
                            color: .09, .19, .15, 1
                            text_size: self.size
                            halign: "left"
                        CheckBox:
                            id: dark
                            size_hint_x: None
                            width: "48dp"
                    BoxLayout:
                        size_hint_y: None
                        height: "42dp"
                        Label:
                            text: "Terlihat genangan"
                            color: .09, .19, .15, 1
                            text_size: self.size
                            halign: "left"
                        CheckBox:
                            id: water
                            size_hint_x: None
                            width: "48dp"
                    BoxLayout:
                        size_hint_y: None
                        height: "42dp"
                        Label:
                            text: "Daun tampak layu"
                            color: .09, .19, .15, 1
                            text_size: self.size
                            halign: "left"
                        CheckBox:
                            id: wilt
                            size_hint_x: None
                            width: "48dp"
        Spinner:
            id: moisture
            text: "Belum ditentukan"
            values: ["Belum ditentukan", "VERY_DRY", "DRY", "MOIST", "VERY_MOIST", "WATERLOGGED"]
            size_hint_y: None
            height: "44dp"
        TextInput:
            id: notes
            hint_text: "Catatan pemeriksa"
            multiline: True
            size_hint_y: None
            height: "110dp"
        Label:
            id: result
            text: root.result
            color: .14, .38, .23, 1
            text_size: self.width, None
            size_hint_y: None
            height: "60dp"
        PrimaryButton:
            text: "Simpan hasil pemeriksaan"
            on_release: root.save()
        Button:
            text: "Ambil foto (opsional)"
            color: .14, .38, .23, 1
            background_normal: ""
            background_color: 0, 0, 0, 0
            size_hint_y: None
            height: "42dp"
            on_release: root.capture_photo()
        Button:
            text: "Kembali ke daftar"
            color: .14, .38, .23, 1
            background_normal: ""
            background_color: 0, 0, 0, 0
            size_hint_y: None
            height: "42dp"
            on_release: app.show_trees()
"""


class LoginScreen(Screen):
    message = StringProperty("")

    def login(self):
        if self.manager.app.store.authenticate(
            self.ids.username.text.strip(), self.ids.password.text
        ):
            self.manager.app.show_dashboard()
        else:
            self.message = "Akun belum ada atau kata sandi salah."

    def register(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text
        if len(username) < 3 or len(password) < 8:
            self.message = "Nama pengguna minimal 3 dan kata sandi minimal 8 karakter."
            return
        try:
            self.manager.app.store.register(username, password)
        except Exception:
            self.message = "Nama pengguna sudah digunakan."
            return
        self.message = "Akun dibuat. Silakan masuk."


class RegisterScreen(Screen):
    message = StringProperty("")

    def create_account(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text
        confirmation = self.ids.password_confirm.text
        if len(username) < 3 or len(password) < 8:
            self.message = "Nama pengguna minimal 3 dan kata sandi minimal 8 karakter."
            return
        if password != confirmation:
            self.message = "Konfirmasi kata sandi tidak sama."
            return
        try:
            self.manager.app.store.register(username, password)
        except Exception:
            self.message = "Nama pengguna sudah digunakan."
            return
        self.manager.app.show_login("Akun dibuat. Silakan masuk.")


class TreesScreen(Screen):
    def on_pre_enter(self):
        self.ids.tree_list.clear_widgets()
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label

        trees = self.manager.app.store.trees()
        self.ids.tree_count.text = f"{len(trees)} pohon aktif"
        for tree in trees:
            card = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="86dp",
                padding=("12dp", "8dp"),
                spacing="10dp",
            )
            card.canvas.before.add(__import__("kivy.graphics", fromlist=["Color"]).Color(
                rgba=(0.97, 1, 0.97, 1)
            ))
            card.canvas.before.add(__import__("kivy.graphics", fromlist=["RoundedRectangle"]).RoundedRectangle(
                pos=card.pos, size=card.size, radius=[14, 14, 14, 14]
            ))
            card.bind(pos=lambda widget, _: setattr(
                widget.canvas.before.children[0], "pos", widget.pos
            ))
            card.bind(size=lambda widget, _: setattr(
                widget.canvas.before.children[0], "size", widget.size
            ))
            button = Button(
                text=f"🌳  {tree['code']}  •  {tree['status'].replace('_', ' ').title()}",
                color=(0.09, 0.19, 0.15, 1),
                background_normal="",
                background_color=(0, 0, 0, 0),
                halign="left",
                valign="middle",
                text_size=(None, None),
            )
            button.bind(
                on_release=lambda _, item=tree: self.manager.app.show_profile(item)
            )
            card.add_widget(button)
            card.add_widget(Label(
                text="›", color=(0.14, 0.38, 0.23, 1), font_size="28sp",
                size_hint_x=None, width="28dp",
            ))
            self.ids.tree_list.add_widget(card)


class TreeProfileScreen(Screen):
    tree_id = NumericProperty(0)
    tree_code = StringProperty("")
    variety = StringProperty("Belereng")
    status = StringProperty("SEHAT")
    observation_count = StringProperty("0")
    summary = StringProperty("Belum ada pengamatan.")
    timeline = StringProperty(
        "Mulai dengan satu putaran pemeriksaan agar profil tanaman memiliki baseline."
    )


class DashboardScreen(Screen):
    healthy = StringProperty("0")
    watch = StringProperty("0")
    action = StringProperty("0")
    total = StringProperty("0")
    confidence = StringProperty("0%")
    priority_count = StringProperty("0")
    observation_summary = StringProperty("Belum ada observasi pada 30 hari terakhir.")
    distribution = StringProperty("Belum dianalisis 0\nSehat 0 · Diamati 0 · Tindakan 0")
    tree_status = StringProperty("Belum ada data pohon.")
    priority_text = StringProperty("Belum ada prioritas tindakan. Data akan muncul setelah pemeriksaan.")

    def on_pre_enter(self):
        trees = self.manager.app.store.trees()
        rows = []
        for tree in trees:
            inspections = self.manager.app.store.inspections(tree["id"])
            latest = inspections[0] if inspections else None
            rows.append((tree, latest))

        self.total = str(len(rows))
        conditions = {
            "HEALTHY": "Sehat",
            "WATCH": "Diamati",
            "ACTION": "Tindakan",
        }
        counts = {key: 0 for key in conditions}
        for _, latest in rows:
            if latest and latest["condition"] in counts:
                counts[latest["condition"]] += 1
        self.healthy = str(counts["HEALTHY"])
        self.watch = str(counts["WATCH"])
        self.action = str(counts["ACTION"])
        self.priority_count = str(counts["WATCH"] + counts["ACTION"])
        assessed = [latest for _, latest in rows if latest]
        average = sum(item["confidence"] for item in assessed) / len(assessed) if assessed else 0
        self.confidence = f"{average:.0%}"
        self.distribution = (
            f"● Sehat                 {counts['HEALTHY']}\n"
            f"● Diamati              {counts['WATCH']}\n"
            f"● Tindakan             {counts['ACTION']}\n"
            f"● Belum dianalisis     {len(rows) - len(assessed)}"
        )
        self.tree_status = "\n".join(
            f"{tree['code']} · {tree['variety']}    "
            f"{conditions.get(latest['condition'], 'Belum dianalisis') if latest else 'Belum dianalisis'}    "
            f"{latest['confidence']:.0%}" if latest else
            f"{tree['code']} · {tree['variety']}    Belum dianalisis"
            for tree, latest in rows
        ) or "Belum ada data pohon."
        priorities = [
            (tree, latest)
            for tree, latest in rows
            if latest and latest["condition"] in {"WATCH", "ACTION"}
        ]
        priorities.sort(key=lambda item: (item[1]["condition"] != "ACTION", -item[1]["confidence"]))
        if priorities:
            self.priority_text = "\n".join(
                f"!  {tree['code']} · {tree['variety']} · "
                f"confidence {latest['confidence']:.0%} · "
                f"{conditions[latest['condition']]}"
                for tree, latest in priorities[:5]
            )
        else:
            self.priority_text = "Belum ada prioritas tindakan. Data akan muncul setelah pemeriksaan."
        if assessed:
            self.observation_summary = (
                f"{len(assessed)} pemeriksaan tercatat dari {len(rows)} pohon. "
                "Grafik 30 hari akan bertambah setiap kali observasi disimpan."
            )
        else:
            self.observation_summary = "Grafik kosong berarti belum ada observasi pada tanggal tersebut."


class AboutScreen(Screen):
    pass


class InspectionScreen(Screen):
    tree_id = NumericProperty(0)
    tree_code = StringProperty("")
    result = StringProperty("Belum ada hasil.")
    photo_path = StringProperty("")

    def save(self):
        moisture = self.ids.moisture.text
        moisture = "" if moisture == "Belum ditentukan" else moisture
        analysis = evaluate_condition(
            surface_dark=self.ids.dark.active,
            standing_water=self.ids.water.active,
            leaf_wilt=self.ids.wilt.active,
            moisture=moisture,
        )
        self.manager.app.store.save_inspection(
            self.tree_id,
            {
                **analysis,
                "surface_dark": self.ids.dark.active,
                "standing_water": self.ids.water.active,
                "leaf_wilt": self.ids.wilt.active,
                "moisture": moisture,
                "notes": self.ids.notes.text.strip(),
                "photo_path": self.photo_path,
            },
        )
        self.result = (
            f"Tersimpan: {analysis['condition']} "
            f"(confidence {analysis['confidence']:.2f})\n{analysis['evidence']}"
        )

    def capture_photo(self):
        self.result = (
            "Kamera belum tersedia pada build offline ini; "
            "inspeksi manual tetap dapat disimpan."
        )


class RambutanApp(App):
    def build(self):
        Builder.load_string(KV)
        data_dir = Path(self.user_data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        self.store = LocalStore(data_dir / "rambutan.sqlite3")
        from kivy.uix.screenmanager import ScreenManager

        manager = ScreenManager()
        manager.app = self
        manager.add_widget(LoginScreen(name="login"))
        manager.add_widget(RegisterScreen(name="register"))
        manager.add_widget(DashboardScreen(name="dashboard"))
        manager.add_widget(AboutScreen(name="about"))
        manager.add_widget(TreesScreen(name="trees"))
        manager.add_widget(TreeProfileScreen(name="profile"))
        manager.add_widget(InspectionScreen(name="inspection"))
        return manager

    def show_login(self, message=""):
        screen = self.root.get_screen("login")
        screen.message = message
        self.root.current = "login"

    def show_register(self):
        self.root.current = "register"

    def show_trees(self):
        self.root.current = "trees"

    def show_dashboard(self):
        self.root.current = "dashboard"

    def show_about(self):
        self.root.current = "about"

    def show_inspection(self, tree):
        screen = self.root.get_screen("inspection")
        screen.tree_id = tree["id"]
        screen.tree_code = tree["code"]
        screen.result = "Belum ada hasil."
        screen.photo_path = ""
        self.root.current = "inspection"

    def show_profile(self, tree):
        profile = self.root.get_screen("profile")
        inspections = self.store.inspections(tree["id"])
        profile.tree_id = tree["id"]
        profile.tree_code = tree["code"]
        profile.variety = tree["variety"]
        profile.status = tree["status"].replace("_", " ").title()
        profile.observation_count = str(len(inspections))
        if inspections:
            latest = inspections[0]
            profile.summary = (
                f"Kesimpulan terakhir: {latest['condition']}\n"
                f"Confidence: {latest['confidence']:.0%}"
            )
            profile.timeline = (
                f"{latest['captured_at'][:16].replace('T', ' · ')}\n"
                f"{latest['evidence']}"
            )
        else:
            profile.summary = "Belum ada pengamatan"
            profile.timeline = (
                "Mulai dengan satu putaran pemeriksaan agar profil tanaman "
                "memiliki baseline."
            )
        self.root.current = "profile"

    def show_inspection_from_profile(self):
        profile = self.root.get_screen("profile")
        tree = next(
            tree for tree in self.store.trees() if tree["id"] == profile.tree_id
        )
        self.show_inspection(tree)

    def export_backup(self):
        destination = Path(self.user_data_dir) / "backup-rambutan.json"
        self.store.export_backup(destination)
        self.root.get_screen("trees").ids.tree_list.add_widget(
            __import__("kivy.uix.label", fromlist=["Label"]).Label(
                text=f"Backup tersimpan: {destination.name}", size_hint_y=None, height="32dp"
            )
        )

    def logout(self):
        self.show_login()


if __name__ == "__main__":
    RambutanApp().run()
