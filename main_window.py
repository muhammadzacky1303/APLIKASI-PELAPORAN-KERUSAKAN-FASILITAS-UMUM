from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)

from report_form_page import ReportFormPage
from report_list_page import ReportListPage


class MainWindow(QMainWindow):
    def __init__(self, supabase_service, role="user", username=""):
        super().__init__()
        self.sb = supabase_service
        self.role = role
        self.username = username

        self.setWindowTitle("Aplikasi Pelaporan Kerusakan Fasilitas Umum")
        self.resize(900, 600)

        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.layout = QVBoxLayout(self.container)

        # ✅ Welcome label
        role_text = "Admin" if self.role == "admin" else "User"
        self.lbl_welcome = QLabel(f"Selamat datang, {role_text}: {self.username}")
        self.layout.addWidget(self.lbl_welcome)

        # Navbar
        self.btn_form = QPushButton("➕ Buat Laporan")
        self.btn_list = QPushButton("📋 Daftar Laporan")

        nav = QHBoxLayout()
        nav.addWidget(self.btn_form)
        nav.addWidget(self.btn_list)
        self.layout.addLayout(nav)

        # Pages
        self.form_page = ReportFormPage(self.sb)
        self.list_page = ReportListPage(self.sb, role=self.role, username=self.username)

        self.layout.addWidget(self.form_page)
        self.layout.addWidget(self.list_page)

        self.btn_form.clicked.connect(self.show_form)
        self.btn_list.clicked.connect(self.show_list)

        # ✅ Start page by role
        if self.role == "admin":
            self.btn_form.hide()
            self.form_page.hide()
            self.show_list()
        else:
            self.list_page.hide()
            self.show_form()

    def show_form(self):
        self.list_page.hide()
        self.form_page.show()

    def show_list(self):
        self.form_page.hide()
        self.list_page.refresh_table()
        self.list_page.show()
