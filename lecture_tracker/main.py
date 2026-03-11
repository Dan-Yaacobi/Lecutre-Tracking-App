from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox

if __package__ in (None, ""):
    # Allow running the file directly: `python lecture_tracker/main.py`
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lecture_tracker.storage.json_storage import JsonStorage
from lecture_tracker.ui.calendar_view import CalendarView, DAY_TO_INDEX
from lecture_tracker.ui.lecture_dialog import LectureDialog

TOTAL_ACADEMIC_HOURS = 10


class LectureTrackerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("מעקב השלמת הרצאות")
        self.root.geometry("1200x700")

        self.storage = JsonStorage(Path(__file__).resolve().parent / "data.json")
        self.data = self.storage.load()

        self.calendar = CalendarView(
            root,
            total_hours=TOTAL_ACADEMIC_HOURS,
            on_add=self.add_lecture,
            on_update=self.update_lecture,
            on_delete=self.delete_lecture,
        )
        self.calendar.pack(fill="both", expand=True)
        self.calendar.set_lectures(self.data["lectures"])

    def add_lecture(self) -> None:
        dialog = LectureDialog(self.root, max_hours=TOTAL_ACADEMIC_HOURS)
        self.root.wait_window(dialog)
        lecture = dialog.result
        if not lecture:
            return

        if self._has_overlap(lecture):
            messagebox.showerror("שגיאה", "יש חפיפה עם הרצאה קיימת באותו יום")
            return

        self.data["lectures"].append(lecture)
        self._save_and_refresh()

    def update_lecture(self, lecture_index: int, updated_lecture: dict) -> None:
        self.data["lectures"][lecture_index] = updated_lecture
        self._save_and_refresh()

    def delete_lecture(self, lecture_index: int) -> None:
        del self.data["lectures"][lecture_index]
        self._save_and_refresh()

    def _save_and_refresh(self) -> None:
        self.storage.save(self.data)
        self.calendar.set_lectures(self.data["lectures"])

    def _has_overlap(self, new_lecture: dict) -> bool:
        new_day = new_lecture["day"]
        new_slots = {
            new_lecture["start_hour"] + i for i in range(new_lecture["duration_hours"])
        }

        for lecture in self.data["lectures"]:
            if lecture["day"] != new_day:
                continue
            existing_slots = {
                lecture["start_hour"] + i for i in range(lecture["duration_hours"])
            }
            if new_slots & existing_slots:
                return True
        return False


def main() -> None:
    root = tk.Tk()
    app = LectureTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
