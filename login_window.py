from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QMessageBox
)


class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success  # callback(role, username)

        self.setWindowTitle("Pilih Akses")
        self.setMinimumWidth(320)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Masuk sebagai"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["User", "Admin"])
        layout.addWidget(self.role_combo)

        # Username/Nama (untuk User)
        self.user_label = QLabel("Nama Pelapor")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Contoh: Ara / Zacky / Dede")
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        # Password admin (untuk Admin)
        self.pw_label = QLabel("Password Admin")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pw_label)
        layout.addWidget(self.pw_input)

        self.btn = QPushButton("Lanjut")
        layout.addWidget(self.btn)

        self._apply_role_ui()

        self.role_combo.currentTextChanged.connect(self._apply_role_ui)
        self.btn.clicked.connect(self.handle_continue)

    def _apply_role_ui(self):
        is_admin = self.role_combo.currentText() == "Admin"

        # User fields
        self.user_label.setVisible(not is_admin)
        self.user_input.setVisible(not is_admin)
        if is_admin:
            self.user_input.clear()

        # Admin fields
        self.pw_label.setVisible(is_admin)
        self.pw_input.setVisible(is_admin)
        if not is_admin:
            self.pw_input.clear()

    def handle_continue(self):
        role = self.role_combo.currentText().lower()

        if role == "user":
            username = self.user_input.text().strip()
            if not username:
                QMessageBox.warning(self, "Validasi", "Nama pelapor wajib diisi.")
                return
            self.on_success("user", username)
            return

        # role == admin
        admin_pw = self.pw_input.text().strip()

        # Password admin (ubah jika mau)
        if admin_pw == "admin123":
            self.on_success("admin", "Admin")
        else:
            QMessageBox.critical(self, "Gagal", "Password admin salah.")
