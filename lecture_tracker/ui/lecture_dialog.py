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
    def __init__(self, max_hours: int, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("הוספת הרצאה")
        self.setLayoutDirection(Qt.RightToLeft)
        self.result_data: dict | None = None

        self.course_input = QLineEdit()
        self.title_input = QLineEdit()

        self.day_combo = QComboBox()
        self.day_combo.addItems(DAYS)

        self.start_combo = QComboBox()
        self.start_combo.addItems(TIME_OPTIONS)
        self.start_combo.setFixedWidth(110)

        self.end_combo = QComboBox()
        self.end_combo.addItems(TIME_OPTIONS)
        self.end_combo.setCurrentIndex(1)
        self.end_combo.setFixedWidth(110)

        form = QFormLayout()
        form.addRow("שם הקורס", self.course_input)
        form.addRow("כותרת ההרצאה (אופציונלי)", self.title_input)
        form.addRow("יום", self.day_combo)
        form.addRow("שעת התחלה", self.start_combo)
        form.addRow("שעת סיום", self.end_combo)

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

        start_idx = self.start_combo.currentIndex()
        end_idx = self.end_combo.currentIndex()
        duration = end_idx - start_idx

        if duration <= 0:
            QMessageBox.warning(self, "שגיאה", "שעת הסיום חייבת להיות אחרי שעת ההתחלה")
            return

        start_hour = start_idx + 1
        if start_hour + duration - 1 > max_hours:
            QMessageBox.warning(self, "שגיאה", "שעת הסיום חייבת להיות אחרי שעת ההתחלה")
            return

        self.result_data = {
            "course": course,
            "title": title,
            "day": self.day_combo.currentText(),
            "start_hour": start_hour,
            "duration_hours": duration,
            "hours": [{"completed": False} for _ in range(duration)],
            "focus_rating": None,
        }
        self.accept()
