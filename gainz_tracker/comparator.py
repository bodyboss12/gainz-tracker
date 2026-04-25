"""Compare workout stats across two date ranges."""

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.stats import ExerciseStats, compute_stats


@dataclass
class ComparisonResult:
    exercise: str
    period_a_max: float
    period_b_max: float
    period_a_volume: float
    period_b_volume: float
    max_delta: float
    volume_delta: float
    improved: bool

    def __repr__(self) -> str:
        direction = "up" if self.improved else "down"
        return (
            f"<ComparisonResult {self.exercise}: max {direction} "
            f"{self.max_delta:+.1f} kg, volume {self.volume_delta:+.1f} kg>"
        )


def _filter_by_date_range(
    entries: List[WorkoutEntry], start: date, end: date
) -> List[WorkoutEntry]:
    return [e for e in entries if start <= e.date <= end]


def compare_periods(
    entries: List[WorkoutEntry],
    period_a: tuple,
    period_b: tuple,
) -> Dict[str, ComparisonResult]:
    """Compare exercise stats between two date ranges.

    Args:
        entries: All workout entries.
        period_a: Tuple of (start_date, end_date) for the baseline period.
        period_b: Tuple of (start_date, end_date) for the comparison period.

    Returns:
        Dict mapping exercise name to ComparisonResult.
    """
    a_start, a_end = period_a
    b_start, b_end = period_b

    entries_a = _filter_by_date_range(entries, a_start, a_end)
    entries_b = _filter_by_date_range(entries, b_start, b_end)

    stats_a: Dict[str, ExerciseStats] = compute_stats(entries_a)
    stats_b: Dict[str, ExerciseStats] = compute_stats(entries_b)

    all_exercises = set(stats_a) | set(stats_b)
    results: Dict[str, ComparisonResult] = {}

    for exercise in all_exercises:
        a = stats_a.get(exercise)
        b = stats_b.get(exercise)

        a_max = a.max_weight if a else 0.0
        b_max = b.max_weight if b else 0.0
        a_vol = a.total_volume if a else 0.0
        b_vol = b.total_volume if b else 0.0

        max_delta = b_max - a_max
        vol_delta = b_vol - a_vol

        results[exercise] = ComparisonResult(
            exercise=exercise,
            period_a_max=a_max,
            period_b_max=b_max,
            period_a_volume=a_vol,
            period_b_volume=b_vol,
            max_delta=max_delta,
            volume_delta=vol_delta,
            improved=max_delta > 0,
        )

    return results
