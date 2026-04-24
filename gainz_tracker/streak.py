"""Workout streak tracking — consecutive days with logged workouts."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List

from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class StreakResult:
    current_streak: int
    longest_streak: int
    last_workout_date: date | None

    def __repr__(self) -> str:
        return (
            f"StreakResult(current={self.current_streak}, "
            f"longest={self.longest_streak}, "
            f"last={self.last_workout_date})"
        )


def _unique_workout_dates(entries: List[WorkoutEntry]) -> List[date]:
    """Return sorted list of unique dates from workout entries."""
    return sorted({e.date for e in entries})


def compute_streaks(entries: List[WorkoutEntry]) -> StreakResult:
    """Compute current and longest workout streaks from entries."""
    if not entries:
        return StreakResult(current_streak=0, longest_streak=0, last_workout_date=None)

    workout_dates = _unique_workout_dates(entries)

    longest = 1
    current = 1

    for i in range(1, len(workout_dates)):
        if workout_dates[i] - workout_dates[i - 1] == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    # Check if current streak is still active (last workout was today or yesterday)
    today = date.today()
    last = workout_dates[-1]
    if (today - last).days > 1:
        current = 0

    return StreakResult(
        current_streak=current,
        longest_streak=longest,
        last_workout_date=last,
    )
