from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel

from lecture_tracker.storage.json_storage import JsonStorage
from lecture_tracker.ui.calendar_grid import CalendarGrid
from lecture_tracker.ui.lecture_dialog import LectureDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("מעקב השלמת הרצאות")
        self.resize(1220, 760)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setFont(QFont("Segoe UI", 10))

        self.storage = JsonStorage(Path(__file__).resolve().parent.parent / "data.json")
        self.data = self.storage.load()

        central = QWidget()
        layout = QVBoxLayout(central)

        title = QLabel("מעקב השלמת הרצאות")
        title.setObjectName("title")

        self.grid = CalendarGrid()
        self.grid.add_requested.connect(self._add_lecture)
        self.grid.lecture_updated.connect(self._update_lecture)
        self.grid.lecture_deleted.connect(self._delete_lecture)

        layout.addWidget(title)
        layout.addWidget(self.grid)
        self.setCentralWidget(central)

        self.grid.set_lectures(self.data["lectures"])

    def _add_lecture(self) -> None:
        dialog = LectureDialog(parent=self)
        if dialog.exec() != QDialog.DialogCode.Accepted or not dialog.result_data:
            return

        lecture = dialog.result_data
        if self._has_overlap(lecture):
            QMessageBox.critical(self, "שגיאה", "יש חפיפה עם הרצאה קיימת באותו יום")
            return

        self.data["lectures"].append(lecture)
        self._save_and_refresh()

    def _update_lecture(self, lecture_index: int, updated_lecture: dict) -> None:
        self.data["lectures"][lecture_index] = updated_lecture
        self._save_and_refresh()

    def _delete_lecture(self, lecture_index: int) -> None:
        answer = QMessageBox.question(self, "אישור", "למחוק את ההרצאה?")
        if answer != QMessageBox.Yes:
            return
        del self.data["lectures"][lecture_index]
        self._save_and_refresh()

    def _save_and_refresh(self) -> None:
        self.storage.save(self.data)
        self.grid.set_lectures(self.data["lectures"])

    def _has_overlap(self, new_lecture: dict) -> bool:
        new_day = new_lecture["day"]
        new_slots = {new_lecture["start_hour"] + i for i in range(new_lecture["duration_hours"])}
        for lecture in self.data["lectures"]:
            if lecture["day"] != new_day:
                continue
            existing_slots = {lecture["start_hour"] + i for i in range(lecture["duration_hours"])}
            if new_slots & existing_slots:
                return True
        return False
