"""Track consecutive weeks/sessions where a personal record was broken."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Dict

from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class PRStreakResult:
    exercise: str
    current_streak: int  # consecutive weeks with a new PR
    best_streak: int
    last_pr_date: date | None
    last_pr_weight: float

    def __repr__(self) -> str:
        return (
            f"PRStreakResult(exercise={self.exercise!r}, "
            f"current_streak={self.current_streak}, "
            f"best_streak={self.best_streak}, "
            f"last_pr_weight={self.last_pr_weight})"
        )


def _weekly_maxes(entries: List[WorkoutEntry]) -> Dict[date, float]:
    """Return a dict of ISO week start (Monday) -> max weight for that week."""
    weekly: Dict[date, float] = {}
    for e in entries:
        week_start = e.date - timedelta(days=e.date.weekday())
        if week_start not in weekly or e.weight > weekly[week_start]:
            weekly[week_start] = e.weight
    return weekly


def compute_pr_streaks(
    entries: List[WorkoutEntry],
) -> Dict[str, PRStreakResult]:
    """Compute PR streaks per exercise across weekly buckets."""
    by_exercise: Dict[str, List[WorkoutEntry]] = {}
    for e in entries:
        by_exercise.setdefault(e.exercise.lower(), []).append(e)

    results: Dict[str, PRStreakResult] = {}

    for exercise, ex_entries in by_exercise.items():
        weekly = _weekly_maxes(ex_entries)
        sorted_weeks = sorted(weekly.keys())

        current_streak = 0
        best_streak = 0
        running_max = 0.0
        last_pr_date: date | None = None
        last_pr_weight = 0.0

        for week in sorted_weeks:
            weight = weekly[week]
            if weight > running_max:
                running_max = weight
                current_streak += 1
                last_pr_date = week
                last_pr_weight = weight
                if current_streak > best_streak:
                    best_streak = current_streak
            else:
                current_streak = 0

        results[exercise] = PRStreakResult(
            exercise=exercise,
            current_streak=current_streak,
            best_streak=best_streak,
            last_pr_date=last_pr_date,
            last_pr_weight=last_pr_weight,
        )

    return results
