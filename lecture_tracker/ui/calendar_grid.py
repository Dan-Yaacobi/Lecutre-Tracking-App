from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from lecture_tracker.logic.time_calculator import calculate_time_summary, format_minutes_as_hours

DAYS = ["א", "ב", "ג", "ד", "ה"]
DAY_TO_INDEX = {day: idx for idx, day in enumerate(DAYS)}
HOUR_LABELS = [f"{hour:02d}:00" for hour in range(8, 21)]


class SlotCell(QFrame):
    clicked = Signal(int, int)

    def __init__(self, lecture_index: int, hour_offset: int, text: str, completed: bool) -> None:
        super().__init__()
        self.lecture_index = lecture_index
        self.hour_offset = hour_offset
        self.setObjectName("SlotCell")
        self.setProperty("completed", completed)

        title = QLabel(text)
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)

        status = QLabel("✔" if completed else "◻")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("slotStatus")

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(title)
        layout.addWidget(status)
        self.setLayout(layout)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.lecture_index, self.hour_offset)
        super().mousePressEvent(event)


class CalendarGrid(QWidget):
    add_requested = Signal()
    lecture_updated = Signal(int, dict)
    lecture_deleted = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.lectures: list[dict] = []

        self.stats_label = QLabel()
        self.stats_label.setWordWrap(True)

        self.grid = QGridLayout()
        self.grid.setSpacing(8)

        main_layout = QVBoxLayout()
        top = QHBoxLayout()
        top.addStretch(1)
        add_btn = QPushButton("+ הוספת הרצאה")
        add_btn.clicked.connect(self.add_requested.emit)
        top.addWidget(add_btn)

        main_layout.addLayout(top)
        main_layout.addLayout(self.grid)
        main_layout.addWidget(self.stats_label)
        self.setLayout(main_layout)

        self._build_headers()

    def _build_headers(self) -> None:
        self.grid.addWidget(self._header_label("שעה"), 0, 0)
        for col, day in enumerate(DAYS, start=1):
            self.grid.addWidget(self._header_label(day), 0, col)

        for row, time_label in enumerate(HOUR_LABELS, start=1):
            self.grid.addWidget(self._time_label(time_label), row, 0)
            for col in range(1, len(DAYS) + 1):
                placeholder = QFrame()
                placeholder.setObjectName("EmptyCell")
                self.grid.addWidget(placeholder, row, col)

    def _header_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("header")
        return label

    def _time_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("time")
        return label

    def set_lectures(self, lectures: list[dict]) -> None:
        self.lectures = lectures
        self._render()

    def _clear_dynamic_cells(self) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self._build_headers()

    def _render(self) -> None:
        self._clear_dynamic_cells()

        for lecture_index, lecture in enumerate(self.lectures):
            day_col = DAY_TO_INDEX.get(lecture["day"], 0) + 1
            for offset in range(lecture["duration_hours"]):
                row = lecture["start_hour"] + offset
                if row < 1 or row > len(HOUR_LABELS):
                    continue
                slot = lecture["hours"][offset] if offset < len(lecture["hours"]) else {"completed": False}
                text = lecture["course"] if not lecture.get("title") else f"{lecture['course']}\nנושא: {lecture['title']}"
                cell = SlotCell(lecture_index, offset, text, bool(slot.get("completed", False)))
                cell.clicked.connect(self._open_actions)
                self.grid.addWidget(cell, row, day_col)

        self._update_stats()

    def _open_actions(self, lecture_index: int, hour_offset: int) -> None:
        lecture = dict(self.lectures[lecture_index])

        actions_box = QMessageBox(self)
        actions_box.setWindowTitle("פעולות")
        actions_box.setText("בחר פעולה")

        toggle_slot = actions_box.addButton("החלף מצב שעה", QMessageBox.AcceptRole)
        toggle_all = actions_box.addButton("סמן כל ההרצאה", QMessageBox.ActionRole)
        focus_btn = actions_box.addButton("עדכון ריכוז", QMessageBox.ActionRole)
        delete_btn = actions_box.addButton("מחיקת הרצאה", QMessageBox.DestructiveRole)
        actions_box.addButton("סגירה", QMessageBox.RejectRole)

        focus_combo = QComboBox(actions_box)
        focus_combo.addItems(["-", "1", "2", "3"])
        if lecture.get("focus_rating"):
            focus_combo.setCurrentText(str(lecture["focus_rating"]))
        actions_box.layout().addWidget(QLabel("דירוג ריכוז:"), 1, 0)
        actions_box.layout().addWidget(focus_combo, 1, 1)

        actions_box.exec()
        clicked = actions_box.clickedButton()

        if clicked == toggle_slot:
            lecture["hours"][hour_offset]["completed"] = not bool(lecture["hours"][hour_offset].get("completed", False))
            self.lecture_updated.emit(lecture_index, lecture)
        elif clicked == toggle_all:
            all_completed = all(slot.get("completed", False) for slot in lecture["hours"])
            for slot in lecture["hours"]:
                slot["completed"] = not all_completed
            self.lecture_updated.emit(lecture_index, lecture)
        elif clicked == focus_btn:
            value = focus_combo.currentText()
            lecture["focus_rating"] = int(value) if value in {"1", "2", "3"} else None
            self.lecture_updated.emit(lecture_index, lecture)
        elif clicked == delete_btn:
            self.lecture_deleted.emit(lecture_index)

    def _update_stats(self) -> None:
        remaining_hours = sum(
            1
            for lecture in self.lectures
            for slot in lecture.get("hours", [])
            if not slot.get("completed", False)
        )
        summary = calculate_time_summary(remaining_hours)
        self.stats_label.setText(
            f"שעות אקדמיות להשלמה: {summary.remaining_academic_hours} | "
            f"1x: {format_minutes_as_hours(summary.minutes_1x)} | "
            f"1.5x: {format_minutes_as_hours(summary.minutes_1_5x)} | "
            f"2x: {format_minutes_as_hours(summary.minutes_2x)}"
        )
