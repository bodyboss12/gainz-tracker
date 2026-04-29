"""Compute a consistency score for each exercise based on workout frequency."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Dict

from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class ConsistencyScore:
    exercise: str
    total_days: int
    active_days: int
    score: float  # 0.0 - 1.0
    grade: str

    def __repr__(self) -> str:
        return (
            f"ConsistencyScore(exercise={self.exercise!r}, "
            f"score={self.score:.2f}, grade={self.grade!r})"
        )


def _grade(score: float) -> str:
    if score >= 0.8:
        return "A"
    elif score >= 0.6:
        return "B"
    elif score >= 0.4:
        return "C"
    elif score >= 0.2:
        return "D"
    return "F"


def _unique_dates_for_exercise(entries: List[WorkoutEntry], exercise: str) -> List[date]:
    return sorted(
        set(
            e.date for e in entries
            if e.exercise.lower() == exercise.lower()
        )
    )


def compute_consistency(entries: List[WorkoutEntry]) -> Dict[str, ConsistencyScore]:
    """Compute a consistency score per exercise over the observed date range."""
    if not entries:
        return {}

    all_dates = [e.date for e in entries]
    start = min(all_dates)
    end = max(all_dates)
    total_days = (end - start).days + 1

    exercises = {e.exercise.lower() for e in entries}
    results: Dict[str, ConsistencyScore] = {}

    for exercise in exercises:
        active = _unique_dates_for_exercise(entries, exercise)
        active_days = len(active)
        score = round(active_days / total_days, 4) if total_days > 0 else 0.0
        # Cap at 1.0 in edge cases
        score = min(score, 1.0)
        results[exercise] = ConsistencyScore(
            exercise=exercise,
            total_days=total_days,
            active_days=active_days,
            score=score,
            grade=_grade(score),
        )

    return results
