from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional
from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class WorkoutSchedule:
    exercise: str
    recommended_date: date
    days_since_last: int
    overdue_by: int  # 0 if not overdue

    def __repr__(self):
        return (
            f"WorkoutSchedule(exercise={self.exercise!r}, "
            f"recommended={self.recommended_date}, "
            f"overdue_by={self.overdue_by})"
        )


def _last_workout_date(entries: List[WorkoutEntry], exercise: str) -> Optional[date]:
    """Return the most recent date an exercise was performed."""
    dates = [
        e.date for e in entries
        if e.exercise.lower() == exercise.lower()
    ]
    return max(dates) if dates else None


def recommend_schedule(
    entries: List[WorkoutEntry],
    frequency_days: int = 3,
    as_of: Optional[date] = None,
) -> List[WorkoutSchedule]:
    """
    For each unique exercise in entries, compute when it should next
    be performed based on a fixed rest frequency.

    Args:
        entries: list of WorkoutEntry objects
        frequency_days: how many days between sessions (default 3)
        as_of: reference date for overdue calculation (defaults to today)

    Returns:
        List of WorkoutSchedule sorted by recommended_date ascending.
    """
    if as_of is None:
        as_of = date.today()

    exercises = {e.exercise for e in entries}
    schedules = []

    for exercise in sorted(exercises):
        last = _last_workout_date(entries, exercise)
        if last is None:
            continue
        days_since = (as_of - last).days
        recommended = last + timedelta(days=frequency_days)
        overdue_by = max(0, (as_of - recommended).days)
        schedules.append(
            WorkoutSchedule(
                exercise=exercise,
                recommended_date=recommended,
                days_since_last=days_since,
                overdue_by=overdue_by,
            )
        )

    return sorted(schedules, key=lambda s: s.recommended_date)
