"""Analyze rest days between workouts and flag overtraining or undertraining."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional

from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class RestAnalysis:
    exercise: str
    avg_rest_days: float
    min_rest_days: int
    max_rest_days: int
    overtraining_flags: int   # rest < min_threshold
    undertraining_flags: int  # rest > max_threshold

    def __repr__(self) -> str:
        return (
            f"RestAnalysis(exercise={self.exercise!r}, avg={self.avg_rest_days:.1f}d, "
            f"min={self.min_rest_days}d, max={self.max_rest_days}d, "
            f"over={self.overtraining_flags}, under={self.undertraining_flags})"
        )


def _unique_sorted_dates(entries: List[WorkoutEntry], exercise: str) -> List[date]:
    """Return sorted unique dates for a given exercise."""
    dates = {
        e.date for e in entries
        if e.exercise.lower() == exercise.lower()
    }
    return sorted(dates)


def analyze_rest(
    entries: List[WorkoutEntry],
    min_rest: int = 1,
    max_rest: int = 5,
) -> dict:
    """Compute rest day analysis per exercise.

    Args:
        entries: List of WorkoutEntry objects.
        min_rest: Days below this count as overtraining.
        max_rest: Days above this count as undertraining.

    Returns:
        Dict mapping exercise name to RestAnalysis.
    """
    exercises = {e.exercise.lower() for e in entries}
    result = {}

    for exercise in exercises:
        dates = _unique_sorted_dates(entries, exercise)
        if len(dates) < 2:
            continue

        gaps = [
            (dates[i] - dates[i - 1]).days
            for i in range(1, len(dates))
        ]

        avg = sum(gaps) / len(gaps)
        over = sum(1 for g in gaps if g < min_rest)
        under = sum(1 for g in gaps if g > max_rest)

        result[exercise] = RestAnalysis(
            exercise=exercise,
            avg_rest_days=round(avg, 2),
            min_rest_days=min(gaps),
            max_rest_days=max(gaps),
            overtraining_flags=over,
            undertraining_flags=under,
        )

    return result
