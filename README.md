# מעקב השלמת הרצאות

אפליקציית דסקטופ פשוטה (Tkinter + Python) לניהול השלמות הרצאות באופן מקומי וללא אינטרנט.

## יכולות מרכזיות
- לוח שבועי בעברית לפי ימים א-ה ושעות אקדמיות.
- כל תא מייצג שעה אקדמית אחת (45 דקות).
- הרצאות יכולות להימשך מספר שעות אקדמיות רצופות.
- סימון הרצאה כהושלמה/לא הושלמה.
- דירוג ריכוז לכל הרצאה (1-3).
- חישוב אוטומטי של זמן השלמה:
  - זמן צפייה רגיל (1x)
  - במהירות 1.5x
  - במהירות 2x
- שמירת נתונים אוטומטית לקובץ `lecture_tracker/data.json`.

## הרצה
```bash
python lecture_tracker/main.py
```

## מבנה הפרויקט
```text
lecture_tracker/
    main.py
    ui/
        calendar_view.py
        lecture_dialog.py
    logic/
        time_calculator.py
    storage/
        json_storage.py
    data.json
```
