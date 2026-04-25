"""Track total training volume (sets * reps * weight) per exercise over time."""

from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict
from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class VolumeResult:
    exercise: str
    total_volume: float
    session_count: int
    avg_volume_per_session: float

    def __repr__(self) -> str:
        return (
            f"VolumeResult(exercise={self.exercise!r}, "
            f"total_volume={self.total_volume:.1f}, "
            f"sessions={self.session_count}, "
            f"avg_per_session={self.avg_volume_per_session:.1f})"
        )


def compute_volume(entries: List[WorkoutEntry]) -> Dict[str, VolumeResult]:
    """Compute total volume per exercise from a list of workout entries.

    Volume for a single entry = sets * reps * weight.
    """
    volume_totals: Dict[str, float] = defaultdict(float)
    session_counts: Dict[str, int] = defaultdict(int)

    for entry in entries:
        vol = entry.sets * entry.reps * entry.weight
        volume_totals[entry.exercise] += vol
        session_counts[entry.exercise] += 1

    results: Dict[str, VolumeResult] = {}
    for exercise, total in volume_totals.items():
        count = session_counts[exercise]
        results[exercise] = VolumeResult(
            exercise=exercise,
            total_volume=round(total, 2),
            session_count=count,
            avg_volume_per_session=round(total / count, 2) if count > 0 else 0.0,
        )

    return results


def volume_over_time(entries: List[WorkoutEntry], exercise: str) -> Dict[str, float]:
    """Return a date -> volume mapping for a specific exercise.

    Useful for plotting volume progression over time.
    """
    daily: Dict[str, float] = defaultdict(float)
    target = exercise.lower()

    for entry in entries:
        if entry.exercise.lower() == target:
            vol = entry.sets * entry.reps * entry.weight
            daily[entry.date] += vol

    return dict(sorted(daily.items()))
