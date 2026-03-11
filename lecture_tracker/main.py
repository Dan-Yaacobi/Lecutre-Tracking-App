import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from lecture_tracker.ui.main_window import MainWindow


STYLE = """
QMainWindow, QWidget {
    background: #f4f7fb;
    color: #1f2937;
}
QLabel#title {
    font-size: 28px;
    font-weight: 700;
    padding: 8px 4px;
}
QLabel#header, QLabel#time {
    background: #e8eef8;
    border: 1px solid #d3deef;
    border-radius: 10px;
    padding: 10px;
    font-weight: 600;
}
QFrame#EmptyCell {
    background: #ffffff;
    border: 1px solid #e4eaf4;
    border-radius: 10px;
}
QFrame#SlotCell {
    background: #fff8e7;
    border: 1px solid #eeddb1;
    border-radius: 12px;
}
QFrame#SlotCell[completed="true"] {
    background: #daf5df;
    border: 1px solid #b6e4bf;
}
QLabel#slotStatus {
    color: #64748b;
    font-weight: 700;
}
QPushButton {
    background: #dbeafe;
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 8px 12px;
    font-weight: 600;
}
QPushButton:hover {
    background: #bfdbfe;
}
QLineEdit, QSpinBox, QComboBox {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 6px;
}
"""


def main() -> None:
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
