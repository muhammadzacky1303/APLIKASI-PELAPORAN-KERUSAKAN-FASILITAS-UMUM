import sys
from PyQt6.QtWidgets import QApplication

from supabase_client import SupabaseService
from login_window import LoginWindow
from main_window import MainWindow


APP_QSS = """
QMainWindow { background: #121212; }
QWidget { color: #eaeaea; font-size: 12pt; }

QLabel { color: #eaeaea; }

QLineEdit, QTextEdit {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px;
    color: #eaeaea;
}

QPushButton {
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 12px;
    padding: 10px 14px;
}
QPushButton:hover { background: #333333; }
QPushButton:pressed { background: #1f1f1f; }

QComboBox {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 8px;
    color: #eaeaea;
}
QComboBox QAbstractItemView {
    background: #1e1e1e;
    border: 1px solid #333;
    selection-background-color: #2f2f2f;
    color: #eaeaea;
}

QTableWidget {
    background: #1e1e1e;
    border: 1px solid #333;
    gridline-color: #2d2d2d;
}
QHeaderView::section {
    background: #262626;
    padding: 8px;
    border: 0px;
    color: #eaeaea;
}
"""


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_QSS)

    sb = SupabaseService()
    main_window = None

    def open_main(role: str, username: str):
        nonlocal main_window
        main_window = MainWindow(sb, role=role, username=username)
        main_window.show()
        login.close()

    login = LoginWindow(on_success=open_main)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
