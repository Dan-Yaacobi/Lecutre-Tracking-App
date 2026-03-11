import tkinter as tk
from tkinter import ttk, messagebox


class LectureDialog(tk.Toplevel):
    def __init__(self, parent: tk.Widget, max_hours: int) -> None:
        super().__init__(parent)
        self.title("הוסף הרצאה")
        self.resizable(False, False)
        self.result = None
        self.max_hours = max_hours

        self.course_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.day_var = tk.StringVar(value="א")
        self.start_var = tk.StringVar(value="1")
        self.duration_var = tk.StringVar(value="1")

        self._build_ui()
        self.transient(parent)
        self.grab_set()
        self.focus()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="שם הקורס").grid(row=0, column=0, sticky="e", pady=4)
        ttk.Entry(frame, textvariable=self.course_var, width=30).grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="כותרת ההרצאה").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Entry(frame, textvariable=self.title_var, width=30).grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="יום בשבוע").grid(row=2, column=0, sticky="e", pady=4)
        ttk.Combobox(frame, textvariable=self.day_var, values=["א", "ב", "ג", "ד", "ה"], state="readonly", width=27).grid(row=2, column=1, pady=4)

        ttk.Label(frame, text="שעת התחלה").grid(row=3, column=0, sticky="e", pady=4)
        ttk.Spinbox(frame, from_=1, to=self.max_hours, textvariable=self.start_var, width=28).grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="משך ההרצאה (שעות אקדמיות)").grid(row=4, column=0, sticky="e", pady=4)
        ttk.Spinbox(frame, from_=1, to=self.max_hours, textvariable=self.duration_var, width=28).grid(row=4, column=1, pady=4)

        buttons = ttk.Frame(frame)
        buttons.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(buttons, text="ביטול", command=self.destroy).grid(row=0, column=0, padx=4)
        ttk.Button(buttons, text="שמור", command=self._save).grid(row=0, column=1, padx=4)

    def _save(self) -> None:
        course = self.course_var.get().strip()
        title = self.title_var.get().strip()

        if not course or not title:
            messagebox.showerror("שגיאה", "יש למלא שם קורס וכותרת הרצאה")
            return

        try:
            start_hour = int(self.start_var.get())
            duration_hours = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים מספריים תקינים")
            return

        if start_hour < 1 or duration_hours < 1 or start_hour + duration_hours - 1 > self.max_hours:
            messagebox.showerror("שגיאה", "משך ההרצאה חורג מגבולות המערכת")
            return

        self.result = {
            "course": course,
            "title": title,
            "day": self.day_var.get(),
            "start_hour": start_hour,
            "duration_hours": duration_hours,
            "completed": False,
            "focus_rating": None,
        }
        self.destroy()
