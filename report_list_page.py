from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox
)

STATUS_OPTIONS = ["Diajukan", "Ditinjau", "Diproses", "Selesai"]


class ReportListPage(QWidget):
    def __init__(self, sb, role="user", username=""):
        super().__init__()
        self.sb = sb
        self.role = role
        self.username = username
        self.selected_id = None

        # ================== STYLE (CLEAN, NO BLACK) ==================
        # Style ini hanya untuk halaman list (bukan global)
        self.setStyleSheet("""
        ReportListPage {
            background: #f5f7fa;
            color: #1f2937;
        }

        QLabel { color: #111827; }

        QPushButton {
            background: #2563eb;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 8px;
        }
        QPushButton:hover { background: #1d4ed8; }

        QComboBox {
            background: white;
            border: 1px solid #d1d5db;
            padding: 6px;
            border-radius: 6px;
        }

        QTableWidget {
            background: white;
            gridline-color: #e5e7eb;
            border: 1px solid #d1d5db;
            border-radius: 6px;
        }

        QHeaderView::section {
            background: #e5e7eb;
            color: #111827;
            padding: 6px;
            border: none;
        }

        QTableWidget::item:selected {
            background: #bfdbfe;
            color: #0b1220;
        }
        """)
        # ============================================================

        root = QVBoxLayout(self)
        root.setSpacing(12)

        # =========================
        # Header row: title + refresh
        # =========================
        header = QHBoxLayout()
        header.setSpacing(10)

        title_text = "Daftar Laporan (Admin)" if self.role == "admin" else f"Daftar Laporan Saya ({self.username})"
        self.title = QLabel(title_text)
        self.title.setStyleSheet("font-size: 16pt; font-weight: 700;")

        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setFixedHeight(38)

        header.addWidget(self.title, 1)
        header.addWidget(self.btn_refresh)
        root.addLayout(header)

        # =========================
        # Admin controls row (only admin)
        # =========================
        self.admin_row = QHBoxLayout()
        self.admin_row.setSpacing(10)

        self.lbl_status = QLabel("Ubah Status:")
        self.cmb_status = QComboBox()
        self.cmb_status.addItems(STATUS_OPTIONS)
        self.cmb_status.setFixedHeight(36)

        self.btn_update = QPushButton("✅ Update")
        self.btn_update.setFixedHeight(36)

        self.btn_delete = QPushButton("🗑️ Hapus")
        self.btn_delete.setFixedHeight(36)

        self.admin_row.addWidget(self.lbl_status)
        self.admin_row.addWidget(self.cmb_status)
        self.admin_row.addWidget(self.btn_update)
        self.admin_row.addWidget(self.btn_delete)
        self.admin_row.addStretch(1)

        if self.role == "admin":
            root.addLayout(self.admin_row)

        # =========================
        # Table
        # =========================
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nama", "Jenis Kerusakan", "Lokasi", "Status", "Foto"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setDefaultSectionSize(34)

        root.addWidget(self.table)

        # =========================
        # Events
        # =========================
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.table.itemSelectionChanged.connect(self.on_select_row)

        if self.role == "admin":
            self.btn_update.clicked.connect(self.update_selected_status)
            self.btn_delete.clicked.connect(self.delete_selected)

    def refresh_table(self):
        try:
            data = (self.sb.fetch_laporan().data) or []

            # User hanya melihat laporan miliknya
            if self.role == "user":
                key = self.username.strip().lower()
                data = [x for x in data if x.get("nama", "").strip().lower() == key]

            self.table.setRowCount(len(data))
            self.selected_id = None

            for row, item in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(str(item.get("id", ""))))
                self.table.setItem(row, 1, QTableWidgetItem(item.get("nama", "")))
                self.table.setItem(row, 2, QTableWidgetItem(item.get("jenis_kerusakan", "")))
                self.table.setItem(row, 3, QTableWidgetItem(item.get("lokasi", "")))
                self.table.setItem(row, 4, QTableWidgetItem(item.get("status", "")))
                self.table.setItem(row, 5, QTableWidgetItem("Ada" if item.get("foto_url") else "-"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal ambil data:\n{e}")

    def on_select_row(self):
        items = self.table.selectedItems()
        if not items:
            self.selected_id = None
            return

        row = items[0].row()
        id_item = self.table.item(row, 0)
        status_item = self.table.item(row, 4)

        try:
            self.selected_id = int(id_item.text()) if id_item else None
        except:
            self.selected_id = None

        if self.role == "admin" and status_item:
            current = status_item.text().strip()
            idx = self.cmb_status.findText(current)
            if idx >= 0:
                self.cmb_status.setCurrentIndex(idx)

    def update_selected_status(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Pilih Data", "Pilih 1 laporan di tabel dulu.")
            return

        new_status = self.cmb_status.currentText()

        try:
            self.sb.update_status(self.selected_id, new_status)
            QMessageBox.information(self, "Sukses", f"Status ID {self.selected_id} jadi: {new_status}")
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal update status:\n{e}")

    def delete_selected(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Pilih Data", "Pilih 1 laporan di tabel dulu.")
            return

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            f"Yakin hapus laporan ID {self.selected_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self.sb.delete_laporan(self.selected_id)
            QMessageBox.information(self, "Sukses", f"Laporan ID {self.selected_id} berhasil dihapus.")
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal hapus laporan:\n{e}")
