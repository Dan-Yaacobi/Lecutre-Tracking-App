from dataclasses import dataclass


ACADEMIC_HOUR_MINUTES = 45


@dataclass
class TimeSummary:
    remaining_academic_hours: int
    minutes_1x: int
    minutes_1_5x: int
    minutes_2x: int


def calculate_time_summary(remaining_academic_hours: int) -> TimeSummary:
    minutes_1x = remaining_academic_hours * ACADEMIC_HOUR_MINUTES
    minutes_1_5x = round(minutes_1x / 1.5)
    minutes_2x = round(minutes_1x / 2)

    return TimeSummary(
        remaining_academic_hours=remaining_academic_hours,
        minutes_1x=minutes_1x,
        minutes_1_5x=minutes_1_5x,
        minutes_2x=minutes_2x,
    )


def format_minutes_as_hours(minutes: int) -> str:
    hours = minutes // 60
    remainder = minutes % 60
    if hours and remainder:
        return f"{hours} שעות ו-{remainder} דקות"
    if hours:
        return f"{hours} שעות"
    return f"{remainder} דקות"
