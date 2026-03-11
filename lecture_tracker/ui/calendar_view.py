import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from lecture_tracker.logic.time_calculator import calculate_time_summary, format_minutes_as_hours


DAYS = ["א", "ב", "ג", "ד", "ה"]
DAY_TO_INDEX = {day: idx for idx, day in enumerate(DAYS)}


class CalendarView(ttk.Frame):
    def __init__(
        self,
        master: tk.Widget,
        total_hours: int,
        on_add: Callable[[], None],
        on_update: Callable[[int, dict], None],
        on_delete: Callable[[int], None],
    ) -> None:
        super().__init__(master, padding=12)
        self.total_hours = total_hours
        self.on_add = on_add
        self.on_update = on_update
        self.on_delete = on_delete
        self.lectures: list[dict] = []

        self.stats_var = tk.StringVar()
        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(header, text="מעקב השלמת הרצאות", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="הוסף הרצאה", command=self.on_add).grid(row=0, column=1, sticky="e", padx=(12, 0))
        header.columnconfigure(0, weight=1)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid(row=1, column=0, sticky="nsew")

        ttk.Label(self.grid_frame, text="שעה", borderwidth=1, relief="solid", anchor="center", width=8).grid(row=0, column=0, sticky="nsew")
        for col, day in enumerate(DAYS, start=1):
            ttk.Label(self.grid_frame, text=day, borderwidth=1, relief="solid", anchor="center", width=20).grid(row=0, column=col, sticky="nsew")

        self.cells: dict[tuple[int, int], tk.Label] = {}
        for hour in range(1, self.total_hours + 1):
            ttk.Label(self.grid_frame, text=str(hour), borderwidth=1, relief="solid", anchor="center").grid(row=hour, column=0, sticky="nsew")
            for col in range(1, len(DAYS) + 1):
                cell = tk.Label(self.grid_frame, text="", borderwidth=1, relief="solid", bg="#f7f7f7", width=20, height=3, justify="center")
                cell.grid(row=hour, column=col, sticky="nsew")
                self.cells[(hour, col)] = cell

        for col in range(0, len(DAYS) + 1):
            self.grid_frame.columnconfigure(col, weight=1)
        for row in range(0, self.total_hours + 1):
            self.grid_frame.rowconfigure(row, weight=1)

        stats = ttk.LabelFrame(self, text="סטטיסטיקה", padding=10)
        stats.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        ttk.Label(stats, textvariable=self.stats_var, justify="right").grid(row=0, column=0, sticky="w")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def set_lectures(self, lectures: list[dict]) -> None:
        self.lectures = lectures
        self._render()

    def _render(self) -> None:
        for cell in self.cells.values():
            cell.configure(text="", bg="#f7f7f7", cursor="")
            cell.unbind("<Button-1>")

        for lecture_index, lecture in enumerate(self.lectures):
            day_col = DAY_TO_INDEX.get(lecture["day"], 0) + 1
            for offset in range(lecture["duration_hours"]):
                row = lecture["start_hour"] + offset
                cell = self.cells.get((row, day_col))
                if not cell:
                    continue

                is_completed = lecture.get("completed", False)
                focus_value = lecture.get("focus_rating")
                status = "✔ הושלם" if is_completed else "⬜ לא הושלם"
                focus_text = f"ריכוז: {focus_value}" if focus_value else "ריכוז: -"
                text = f"{lecture['title']}\n{status}\n{focus_text}"
                color = "#b9f6ca" if is_completed else "#ffe0b2"

                cell.configure(text=text, bg=color, cursor="hand2")
                cell.bind("<Button-1>", lambda _event, idx=lecture_index: self._open_actions(idx))

        self._update_stats()

    def _open_actions(self, lecture_index: int) -> None:
        lecture = self.lectures[lecture_index]
        win = tk.Toplevel(self)
        win.title("פעולות הרצאה")
        win.resizable(False, False)
        win.transient(self.winfo_toplevel())
        win.grab_set()

        ttk.Label(win, text=f"{lecture['course']} - {lecture['title']}", padding=10).grid(row=0, column=0, columnspan=2)

        completed_text = "סמן כלא הושלם" if lecture.get("completed") else "סמן כהושלם"
        ttk.Button(win, text=completed_text, command=lambda: self._toggle_completed(lecture_index, win)).grid(row=1, column=0, columnspan=2, padx=10, pady=4, sticky="ew")

        ttk.Label(win, text="רמת ריכוז", padding=(10, 6, 10, 0)).grid(row=2, column=0, sticky="e")
        focus_var = tk.StringVar(value=str(lecture.get("focus_rating") or ""))
        focus_combo = ttk.Combobox(win, textvariable=focus_var, values=["", "1", "2", "3"], state="readonly", width=10)
        focus_combo.grid(row=2, column=1, padx=10, pady=(6, 0), sticky="w")

        ttk.Button(win, text="שמור ריכוז", command=lambda: self._set_focus(lecture_index, focus_var.get(), win)).grid(row=3, column=0, columnspan=2, padx=10, pady=4, sticky="ew")
        ttk.Button(win, text="מחק הרצאה", command=lambda: self._delete_lecture(lecture_index, win)).grid(row=4, column=0, columnspan=2, padx=10, pady=4, sticky="ew")
        ttk.Button(win, text="סגור", command=win.destroy).grid(row=5, column=0, columnspan=2, padx=10, pady=(4, 10), sticky="ew")

    def _toggle_completed(self, lecture_index: int, popup: tk.Toplevel) -> None:
        lecture = dict(self.lectures[lecture_index])
        lecture["completed"] = not lecture.get("completed", False)
        self.on_update(lecture_index, lecture)
        popup.destroy()

    def _set_focus(self, lecture_index: int, focus_value: str, popup: tk.Toplevel) -> None:
        lecture = dict(self.lectures[lecture_index])
        lecture["focus_rating"] = int(focus_value) if focus_value else None
        self.on_update(lecture_index, lecture)
        popup.destroy()

    def _delete_lecture(self, lecture_index: int, popup: tk.Toplevel) -> None:
        if messagebox.askyesno("אישור", "למחוק את ההרצאה?"):
            self.on_delete(lecture_index)
            popup.destroy()

    def _update_stats(self) -> None:
        remaining_hours = sum(lecture["duration_hours"] for lecture in self.lectures if not lecture.get("completed", False))
        summary = calculate_time_summary(remaining_hours)

        text = (
            f"שעות אקדמיות להשלמה: {summary.remaining_academic_hours}\n"
            f"זמן צפייה רגיל: {format_minutes_as_hours(summary.minutes_1x)}\n"
            f"במהירות 1.5x: {format_minutes_as_hours(summary.minutes_1_5x)}\n"
            f"במהירות 2x: {format_minutes_as_hours(summary.minutes_2x)}"
        )
        self.stats_var.set(text)
