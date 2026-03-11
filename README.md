# מעקב השלמת הרצאות (PySide6)

אפליקציית דסקטופ מודרנית למעקב השלמות הרצאות בעברית עם ממשק Qt נקי, RTL ושמירה מקומית ב-JSON.

## יכולות מרכזיות
- ממשק מודרני מבוסס **PySide6 (Qt for Python)**.
- לוח שבועי בעברית (א-ה) עם תצוגת שעות אמיתית: **08:00–20:00**.
- כל שורה מייצגת שעה אקדמית אחת (45 דקות).
- תמיכה בהרצאות רב-שעתיות עם **סימון השלמה לכל שעה בנפרד**.
- כותרת הרצאה היא **אופציונלית**.
- דירוג ריכוז (1–3) לכל הרצאה.
- חישובי זמן השלמה אוטומטיים:
  - רגיל (1x)
  - 1.5x
  - 2x
- שמירה אוטומטית בקובץ `lecture_tracker/data.json`.

## התקנה והרצה
```bash
pip install -r requirements.txt
python main.py
```

## מבנה הפרויקט
```text
lecture_tracker/
    main.py
    ui/
        main_window.py
        calendar_grid.py
        lecture_dialog.py
    logic/
        time_calculator.py
    storage/
        json_storage.py
    models/
        lecture_model.py
    data.json
main.py
requirements.txt
```
