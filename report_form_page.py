from pathlib import Path
import os
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit,
    QPushButton, QLabel,
    QMessageBox, QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


def find_logo_path() -> Path | None:
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent.parent / "assets" / "logo.jpeg",
        here.parent.parent / "assets" / "logo.jpeg",
        Path.cwd() / "assets" / "logo.jpeg",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


class ReportFormPage(QWidget):
    def __init__(self, sb):
        super().__init__()
        self.sb = sb
        self.foto_path = None

        # ===== Layout utama =====
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # ===== Header (LOGO + TITLE TENGAH) =====
        header = QHBoxLayout()
        header.setSpacing(10)

        logo = QLabel()
        logo_path = find_logo_path()
        if logo_path:
            pix = QPixmap(str(logo_path))
            if not pix.isNull():
                logo.setPixmap(
                    pix.scaledToHeight(40, Qt.TransformationMode.SmoothTransformation)
                )

        title = QLabel("FORM PENGADUAN")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: white;")

        # Kunci biar center
        header.addStretch(1)
        header.addWidget(logo, 0, Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(title, 0, Qt.AlignmentFlag.AlignVCenter)
        header.addStretch(1)

        root.addLayout(header)

        # ===== Form (seperti awal) =====
        layout = QFormLayout()
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(10)
        root.addLayout(layout)

        self.nama = QLineEdit()
        self.jenis = QLineEdit()
        self.lokasi = QLineEdit()
        self.deskripsi = QTextEdit()
        self.deskripsi.setMinimumHeight(160)

        self.btn_foto = QPushButton("Pilih Foto")
        self.lbl_foto = QLabel("- belum pilih -")
        self.lbl_foto.setStyleSheet("color: #9ca3af;")

        self.btn_submit = QPushButton("Simpan Laporan")

        layout.addRow("Nama", self.nama)
        layout.addRow("Jenis Kerusakan", self.jenis)
        layout.addRow("Lokasi", self.lokasi)
        layout.addRow("Deskripsi", self.deskripsi)
        layout.addRow("Foto Bukti", self.btn_foto)
        layout.addRow("", self.lbl_foto)
        layout.addRow("", self.btn_submit)

        self.btn_foto.clicked.connect(self.pilih_foto)
        self.btn_submit.clicked.connect(self.save_data)

        # ===== STYLE: HITAM POLOS + PUTIH =====
        self.setStyleSheet("""
            QWidget {
                background: #000000;
                color: #ffffff;
                font-size: 14px;
            }

            QLabel {
                color: #ffffff;
            }

            QLineEdit, QTextEdit {
                background: #1f2933;
                border: 1px solid #374151;
                border-radius: 6px;
                padding: 6px;
                color: #ffffff;
            }

            QLineEdit::placeholder, QTextEdit::placeholder {
                color: #9ca3af;
            }

            QPushButton {
                background: #1f2933;
                border: 1px solid #374151;
                border-radius: 6px;
                padding: 6px 10px;
                color: #ffffff;
                font-weight: 600;
            }

            QPushButton:hover {
                background: #374151;
            }

            QPushButton:pressed {
                background: #111827;
            }
        """)

    def pilih_foto(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Pilih Foto", "", "Images (*.png *.jpg *.jpeg *.webp);;All Files (*)"
        )
        if file:
            self.foto_path = file
            self.lbl_foto.setText(os.path.basename(file))

    def save_data(self):
        if not self.nama.text().strip() or not self.jenis.text().strip() or not self.lokasi.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama, Jenis Kerusakan, dan Lokasi wajib diisi.")
            return

        foto_url = None
        try:
            if self.foto_path:
                try:
                    foto_url = self.sb.upload_foto(self.foto_path)
                except Exception as e:
                    QMessageBox.critical(self, "Upload Foto Gagal", f"Upload foto gagal:\n{e}")
                    return

            data = {
                "nama": self.nama.text().strip(),
                "jenis_kerusakan": self.jenis.text().strip(),
                "lokasi": self.lokasi.text().strip(),
                "deskripsi": self.deskripsi.toPlainText().strip(),
                "tanggal": date.today().isoformat(),
                "foto_url": foto_url
            }

            self.sb.insert_laporan(data)
            QMessageBox.information(self, "Sukses", "Laporan berhasil disimpan!")

            self.nama.clear()
            self.jenis.clear()
            self.lokasi.clear()
            self.deskripsi.clear()
            self.foto_path = None
            self.lbl_foto.setText("- belum pilih -")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal simpan laporan:\n{e}")
