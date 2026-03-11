import json
from pathlib import Path
from typing import Any

from lecture_tracker.models import LectureModel


class JsonStorage:
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file

    def load(self) -> dict[str, Any]:
        if not self.data_file.exists():
            return {"lectures": []}

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                raw = json.load(file)
        except (json.JSONDecodeError, OSError):
            return {"lectures": []}

        lectures = raw.get("lectures", []) if isinstance(raw, dict) else []
        if not isinstance(lectures, list):
            return {"lectures": []}

        normalized = [LectureModel.from_dict(item).to_dict() for item in lectures if isinstance(item, dict)]
        return {"lectures": normalized}

    def save(self, data: dict[str, Any]) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
