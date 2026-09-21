from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mobile.rules import evaluate_condition
from mobile.storage import LocalStore

STORE = None


def current_store() -> LocalStore:
    global STORE
    if STORE is None:
        data_dir = Path.home() / ".aianalisrambutan"
        data_dir.mkdir(parents=True, exist_ok=True)
        STORE = LocalStore(data_dir / "rambutan.sqlite3")
    return STORE


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AiAnalisRambutan Offline")
        self.resize(420, 220)

        layout = QVBoxLayout(self)
        title = QLabel("Login aplikasi offline")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Username", self.username)
        form.addRow("Password", self.password)
        layout.addLayout(form)

        actions = QHBoxLayout()
        btn_login = QPushButton("Masuk")
        btn_register = QPushButton("Buat akun")
        btn_login.clicked.connect(self.try_login)
        btn_register.clicked.connect(self.try_register)
        actions.addWidget(btn_login)
        actions.addWidget(btn_register)
        layout.addLayout(actions)

    def try_login(self):
        store = current_store()
        username = self.username.text().strip()
        password = self.password.text()
        if store.authenticate(username, password):
            self.accept()
            return
        QMessageBox.warning(self, "Login gagal", "Akun belum ada atau kata sandi salah.")

    def try_register(self):
        store = current_store()
        username = self.username.text().strip()
        password = self.password.text()
        if len(username) < 3 or len(password) < 8:
            QMessageBox.warning(self, "Validasi", "Nama pengguna minimal 3, password minimal 8 karakter.")
            return
        try:
            store.register(username, password)
            QMessageBox.information(self, "Berhasil", "Akun dibuat. Silakan masuk.")
        except Exception:
            QMessageBox.warning(self, "Gagal", "Username sudah digunakan.")


class InspectionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.tree_id = 0
        self.tree_code = ""

        self.title = QLabel("Inspeksi pohon")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.dark = QCheckBox("Permukaan tanah tampak gelap / lembap")
        self.water = QCheckBox("Ada genangan")
        self.wilt = QCheckBox("Daun tampak layu")

        self.moisture = QComboBox()
        self.moisture.addItems(["Belum ditentukan", "VERY_DRY", "DRY", "MOIST", "VERY_MOIST", "WATERLOGGED"])

        self.notes = QPlainTextEdit()
        self.notes.setPlaceholderText("Catatan inspeksi")

        self.result = QLabel("Belum ada hasil.")
        self.result.setWordWrap(True)

        btn_save = QPushButton("Simpan inspeksi")
        btn_save.clicked.connect(self.save_inspection)
        btn_photo = QPushButton("Ambil foto")
        btn_photo.clicked.connect(self.capture_photo)
        btn_backup = QPushButton("Backup JSON")
        btn_backup.clicked.connect(self.export_backup)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.dark)
        layout.addWidget(self.water)
        layout.addWidget(self.wilt)
        layout.addWidget(self.moisture)
        layout.addWidget(self.notes)
        layout.addWidget(self.result)
        layout.addWidget(btn_save)
        layout.addWidget(btn_photo)
        layout.addWidget(btn_backup)

    def set_tree(self, tree_id: int, tree_code: str):
        self.tree_id = tree_id
        self.tree_code = tree_code
        self.setWindowTitle(f"Inspeksi {tree_code}")
        self.result.setText("Belum ada hasil.")

    def save_inspection(self):
        moisture = self.moisture.currentText()
        if moisture == "Belum ditentukan":
            moisture = ""
        analysis = evaluate_condition(
            surface_dark=self.dark.isChecked(),
            standing_water=self.water.isChecked(),
            leaf_wilt=self.wilt.isChecked(),
            moisture=moisture,
        )
        current_store().save_inspection(
            self.tree_id,
            {
                **analysis,
                "surface_dark": self.dark.isChecked(),
                "standing_water": self.water.isChecked(),
                "leaf_wilt": self.wilt.isChecked(),
                "moisture": moisture,
                "notes": self.notes.toPlainText().strip(),
                "photo_path": "",
            },
        )
        self.result.setText(f"Tersimpan: {analysis['condition']} (confidence {analysis['confidence']:.2f})\n{analysis['evidence']}")

    def capture_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Pilih foto", str(Path.home()), "Images (*.png *.jpg *.jpeg)")
        if path:
            self.result.setText(f"Foto dipilih: {path}")

    def export_backup(self):
        destination = Path.home() / ".aianalisrambutan" / "backup-rambutan.json"
        current_store().export_backup(destination)
        self.result.setText(f"Backup tersimpan: {destination}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AiAnalisRambutan Offline")
        self.resize(480, 640)

        self.tree_list = QListWidget()
        self.tree_list.itemClicked.connect(self.open_tree)

        self.inspection = InspectionForm()
        self.inspection.hide()

        self.logout_btn = QPushButton("Keluar")
        self.logout_btn.clicked.connect(self.show_tree_list)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_list)
        layout.addWidget(self.logout_btn)
        layout.addWidget(self.inspection)

        self.load_trees()
        self.show_tree_list()

    def load_trees(self):
        self.tree_list.clear()
        for tree in current_store().trees():
            item = QListWidgetItem(f"{tree['code']}  •  {tree['status']}")
            item.setData(Qt.ItemDataRole.UserRole, tree)
            self.tree_list.addItem(item)

    def open_tree(self, item):
        tree = item.data(Qt.ItemDataRole.UserRole)
        self.inspection.set_tree(tree["id"], tree["code"])
        self.inspection.show()
        self.inspection.raise_()

    def show_tree_list(self):
        self.inspection.hide()
        self.tree_list.show()


def main():
    app = QApplication([])
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Accepted:
        window = MainWindow()
        window.show()
        app.exec()
    else:
        app.quit()


if __name__ == "__main__":
    main()
