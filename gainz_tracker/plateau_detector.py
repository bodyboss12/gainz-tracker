from dataclasses import dataclass
from typing import List, Dict
from datetime import date
from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class PlateauResult:
    exercise: str
    weeks_flat: int
    max_weight: float
    is_plateau: bool

    def __repr__(self) -> str:
        status = "PLATEAU" if self.is_plateau else "progressing"
        return (
            f"PlateauResult(exercise={self.exercise!r}, "
            f"weeks_flat={self.weeks_flat}, max_weight={self.max_weight}, "
            f"status={status})"
        )


def _week_key(d: date) -> str:
    """Return ISO year-week string for a date."""
    iso = d.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def _weekly_maxes(entries: List[WorkoutEntry]) -> Dict[str, float]:
    """Return mapping of week_key -> max weight for the given entries."""
    weeks: Dict[str, float] = {}
    for e in entries:
        key = _week_key(e.date)
        if key not in weeks or e.weight > weeks[key]:
            weeks[key] = e.weight
    return dict(sorted(weeks.items()))


def detect_plateaus(
    entries: List[WorkoutEntry],
    min_weeks: int = 3,
    tolerance: float = 0.0,
) -> Dict[str, PlateauResult]:
    """Detect exercises where max weight has not improved for min_weeks consecutive weeks.

    Args:
        entries: All workout entries.
        min_weeks: Number of consecutive flat weeks required to flag a plateau.
        tolerance: Allowable weight difference (kg/lb) still considered flat.

    Returns:
        Dict mapping exercise name to PlateauResult.
    """
    if not entries:
        return {}

    by_exercise: Dict[str, List[WorkoutEntry]] = {}
    for e in entries:
        by_exercise.setdefault(e.exercise, []).append(e)

    results: Dict[str, PlateauResult] = {}

    for exercise, ex_entries in by_exercise.items():
        weekly = _weekly_maxes(ex_entries)
        if len(weekly) < min_weeks:
            results[exercise] = PlateauResult(
                exercise=exercise,
                weeks_flat=0,
                max_weight=max(weekly.values()) if weekly else 0.0,
                is_plateau=False,
            )
            continue

        weights = list(weekly.values())
        max_flat = 1
        current_flat = 1
        for i in range(1, len(weights)):
            if abs(weights[i] - weights[i - 1]) <= tolerance:
                current_flat += 1
                max_flat = max(max_flat, current_flat)
            else:
                current_flat = 1

        is_plateau = max_flat >= min_weeks
        results[exercise] = PlateauResult(
            exercise=exercise,
            weeks_flat=max_flat,
            max_weight=max(weights),
            is_plateau=is_plateau,
        )

    return results
