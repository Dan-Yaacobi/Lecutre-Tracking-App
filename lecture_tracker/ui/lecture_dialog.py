from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
)

DAYS = ["א", "ב", "ג", "ד", "ה"]


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

        self.start_spin = QSpinBox()
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(max_hours)
        self.start_spin.setValue(1)
        self.start_spin.setFixedWidth(80)

        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(max_hours)
        self.duration_spin.setValue(1)
        self.duration_spin.setFixedWidth(80)

        form = QFormLayout()
        form.addRow("שם הקורס", self.course_input)
        form.addRow("כותרת ההרצאה (אופציונלי)", self.title_input)
        form.addRow("יום", self.day_combo)
        form.addRow("שעת התחלה", self.start_spin)
        form.addRow("משך (שעות אקדמיות)", self.duration_spin)

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

        start_hour = self.start_spin.value()
        duration = self.duration_spin.value()

        if not isinstance(duration, int) or duration <= 0:
            QMessageBox.warning(self, "שגיאה", "משך ההרצאה חייב להיות לפחות שעה אחת")
            return

        max_hours = self.start_spin.maximum()
        if start_hour + duration - 1 > max_hours:
            QMessageBox.warning(self, "שגיאה", "משך ההרצאה חורג מטווח השעות")
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
