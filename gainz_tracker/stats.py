"""Compute summary statistics from workout entries."""

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional

from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class ExerciseStats:
    exercise: str
    total_sets: int
    total_reps: int
    max_weight: float
    min_weight: float
    avg_weight: float
    sessions: int

    def __repr__(self) -> str:
        return (
            f"ExerciseStats(exercise={self.exercise!r}, "
            f"max_weight={self.max_weight}, avg_weight={self.avg_weight:.2f}, "
            f"total_sets={self.total_sets})"
        )


def compute_stats(entries: List[WorkoutEntry]) -> Dict[str, ExerciseStats]:
    """Return per-exercise statistics from a list of WorkoutEntry objects."""
    grouped: Dict[str, List[WorkoutEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry.exercise].append(entry)

    stats: Dict[str, ExerciseStats] = {}
    for exercise, rows in grouped.items():
        weights = [r.weight for r in rows]
        dates = {r.date for r in rows}
        stats[exercise] = ExerciseStats(
            exercise=exercise,
            total_sets=len(rows),
            total_reps=sum(r.reps for r in rows),
            max_weight=max(weights),
            min_weight=min(weights),
            avg_weight=sum(weights) / len(weights),
            sessions=len(dates),
        )
    return stats


def personal_records(entries: List[WorkoutEntry]) -> Dict[str, WorkoutEntry]:
    """Return the entry with the highest weight for each exercise."""
    prs: Dict[str, WorkoutEntry] = {}
    for entry in entries:
        if entry.exercise not in prs or entry.weight > prs[entry.exercise].weight:
            prs[entry.exercise] = entry
    return prs


def filter_by_exercise(
    entries: List[WorkoutEntry], exercise: str
) -> List[WorkoutEntry]:
    """Return entries matching the given exercise name (case-insensitive)."""
    target = exercise.lower()
    return [e for e in entries if e.exercise.lower() == target]
