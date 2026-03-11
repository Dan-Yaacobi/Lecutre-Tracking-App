import json
from pathlib import Path
from typing import Any


class JsonStorage:
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file

    def load(self) -> dict[str, Any]:
        if not self.data_file.exists():
            return {"lectures": []}

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if "lectures" not in data or not isinstance(data["lectures"], list):
                    return {"lectures": []}
                return data
        except (json.JSONDecodeError, OSError):
            return {"lectures": []}

    def save(self, data: dict[str, Any]) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
