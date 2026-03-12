from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

DAYS = ["א", "ב", "ג", "ד", "ה"]
TIME_OPTIONS = [f"{hour:02d}:00" for hour in range(8, 21)]


class LectureDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("הוספת הרצאה")
        self.setLayoutDirection(Qt.RightToLeft)
        self.result_data: dict | None = None

        self.course_input = QLineEdit()
        self.title_input = QLineEdit()

        self.day_combo = QComboBox()
        self.day_combo.addItems(DAYS)

        self.start_time_combo = QComboBox()
        self.start_time_combo.addItems(TIME_OPTIONS)
        self.start_time_combo.setFixedWidth(110)

        self.end_time_combo = QComboBox()
        self.end_time_combo.addItems(TIME_OPTIONS)
        self.end_time_combo.setCurrentIndex(1)
        self.end_time_combo.setFixedWidth(110)

        form = QFormLayout()
        form.addRow("שם הקורס", self.course_input)
        form.addRow("כותרת ההרצאה (אופציונלי)", self.title_input)
        form.addRow("יום", self.day_combo)
        form.addRow("שעת התחלה", self.start_time_combo)
        form.addRow("שעת סיום", self.end_time_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _save(self) -> None:
        self.result_data = None
        course = self.course_input.text().strip()
        title = self.title_input.text().strip()

        if not course:
            QMessageBox.warning(self, "שגיאה", "יש למלא שם קורס")
            return

        start_index = self.start_time_combo.currentIndex()
        end_index = self.end_time_combo.currentIndex()

        if end_index <= start_index:
            QMessageBox.warning(self, "שגיאה", "שעת הסיום חייבת להיות אחרי שעת ההתחלה")
            return

        duration_hours = end_index - start_index

        self.result_data = {
            "course": course,
            "title": title,
            "day": self.day_combo.currentText(),
            "start_hour": start_index,
            "duration_hours": duration_hours,
            "hours": [{"completed": False} for _ in range(duration_hours)],
            "focus_rating": None,
        }
        self.accept()
