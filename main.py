from pathlib import Path
from shutil import copy2

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen

from mobile.rules import evaluate_condition
from mobile.storage import LocalStore
from vision import assess_photo


KV = """
<LoginScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "24dp"
        spacing: "12dp"
        Label:
            text: "AiAnalisRambutan\\nMode Offline"
            font_size: "26sp"
            halign: "center"
        TextInput:
            id: username
            hint_text: "Nama pengguna"
            multiline: False
        TextInput:
            id: password
            hint_text: "Kata sandi"
            password: True
            multiline: False
        Button:
            text: "Masuk"
            on_release: root.login()
        Button:
            text: "Buat akun lokal"
            on_release: root.register()
        Label:
            text: root.message
            color: 1, .3, .3, 1

<TreesScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "8dp"
        Label:
            text: "Pilih pohon"
            font_size: "24sp"
            size_hint_y: None
            height: "42dp"
        ScrollView:
            GridLayout:
                id: tree_list
                cols: 1
                spacing: "8dp"
                size_hint_y: None
                height: self.minimum_height
        Button:
            text: "Keluar"
            size_hint_y: None
            height: "44dp"
            on_release: app.logout()

<InspectionScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "8dp"
        Label:
            text: "Inspeksi " + root.tree_code
            font_size: "22sp"
            size_hint_y: None
            height: "40dp"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            Label:
                text: "Permukaan tanah tampak gelap/lembap"
                halign: "left"
                text_size: self.size
            CheckBox:
                id: dark
                size_hint_x: None
                width: "48dp"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            Label:
                text: "Terlihat genangan"
                halign: "left"
                text_size: self.size
            CheckBox:
                id: water
                size_hint_x: None
                width: "48dp"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            Label:
                text: "Daun tampak layu"
                halign: "left"
                text_size: self.size
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
            hint_text: "Catatan"
            multiline: True
        Label:
            id: result
            text: root.result
            text_size: self.width, None
        Button:
            text: "Simpan inspeksi offline"
            size_hint_y: None
            height: "48dp"
            on_release: root.save()
        Button:
            text: "Ambil foto (opsional)"
            size_hint_y: None
            height: "44dp"
            on_release: root.capture_photo()
        Button:
            text: "Ekspor backup JSON"
            size_hint_y: None
            height: "44dp"
            on_release: app.export_backup()
        Button:
            text: "Kembali ke daftar"
            size_hint_y: None
            height: "44dp"
            on_release: app.show_trees()
"""


class LoginScreen(Screen):
    message = StringProperty("")

    def login(self):
        if self.manager.app.store.authenticate(
            self.ids.username.text.strip(), self.ids.password.text
        ):
            self.manager.app.show_trees()
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


class TreesScreen(Screen):
    def on_pre_enter(self):
        self.ids.tree_list.clear_widgets()
        from kivy.uix.button import Button

        for tree in self.manager.app.store.trees():
            button = Button(
                text=f"{tree['code']}  •  {tree['status']}",
                size_hint_y=None,
                height="52dp",
            )
            button.bind(
                on_release=lambda _, item=tree: self.manager.app.show_inspection(item)
            )
            self.ids.tree_list.add_widget(button)


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
        try:
            from plyer import camera
        except ImportError:
            self.result = "Kamera belum tersedia pada build ini; inspeksi manual tetap dapat disimpan."
            return
        target = Path(self.manager.app.user_data_dir) / "photos"
        target.mkdir(parents=True, exist_ok=True)
        output = target / f"inspection-{self.tree_id}.jpg"

        def done(path):
            if not path or not Path(path).exists():
                self.result = "Pengambilan foto dibatalkan."
                return
            copy2(path, output)
            quality = assess_photo(output)
            self.photo_path = str(output)
            self.result = f"Foto tersimpan. {quality['message']}"

        camera.take_picture(filename=str(output), on_complete=done)


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
        manager.add_widget(TreesScreen(name="trees"))
        manager.add_widget(InspectionScreen(name="inspection"))
        return manager

    def show_trees(self):
        self.root.current = "trees"

    def show_inspection(self, tree):
        screen = self.root.get_screen("inspection")
        screen.tree_id = tree["id"]
        screen.tree_code = tree["code"]
        screen.result = "Belum ada hasil."
        screen.photo_path = ""
        self.root.current = "inspection"

    def export_backup(self):
        destination = Path(self.user_data_dir) / "backup-rambutan.json"
        self.store.export_backup(destination)
        self.root.get_screen("trees").ids.tree_list.add_widget(
            __import__("kivy.uix.label", fromlist=["Label"]).Label(
                text=f"Backup tersimpan: {destination.name}", size_hint_y=None, height="32dp"
            )
        )

    def logout(self):
        self.root.current = "login"


if __name__ == "__main__":
    RambutanApp().run()
