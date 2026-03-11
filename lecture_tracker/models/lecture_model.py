from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class LectureModel:
    course: str
    title: str
    day: str
    start_hour: int
    duration_hours: int
    hours: list[dict[str, bool]]
    focus_rating: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LectureModel":
        duration = int(data.get("duration_hours", 1))
        hours = data.get("hours")
        if not isinstance(hours, list) or len(hours) != duration:
            completed = bool(data.get("completed", False))
            hours = [{"completed": completed} for _ in range(duration)]

        normalized_hours: list[dict[str, bool]] = []
        for slot in hours[:duration]:
            normalized_hours.append({"completed": bool(slot.get("completed", False))})

        return cls(
            course=str(data.get("course", "")).strip(),
            title=str(data.get("title", "")).strip(),
            day=str(data.get("day", "א")),
            start_hour=max(1, int(data.get("start_hour", 1))),
            duration_hours=max(1, duration),
            hours=normalized_hours,
            focus_rating=(int(data["focus_rating"]) if data.get("focus_rating") in {1, 2, 3} else None),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def incomplete_slots(self) -> int:
        return sum(1 for slot in self.hours if not slot.get("completed", False))
