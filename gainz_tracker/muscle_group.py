from dataclasses import dataclass
from typing import Dict, List
from gainz_tracker.csv_loader import WorkoutEntry

EXERCISE_MUSCLE_MAP: Dict[str, str] = {
    "squat": "legs",
    "leg press": "legs",
    "lunge": "legs",
    "deadlift": "back",
    "bent over row": "back",
    "pull up": "back",
    "lat pulldown": "back",
    "bench press": "chest",
    "incline press": "chest",
    "chest fly": "chest",
    "overhead press": "shoulders",
    "lateral raise": "shoulders",
    "bicep curl": "arms",
    "tricep pushdown": "arms",
    "skull crusher": "arms",
    "plank": "core",
    "crunch": "core",
    "cable row": "back",
}


@dataclass
class MuscleGroupSummary:
    muscle_group: str
    total_volume: float
    exercise_count: int
    exercises: List[str]

    def __repr__(self) -> str:
        return (
            f"MuscleGroupSummary(group={self.muscle_group!r}, "
            f"volume={self.total_volume}, exercises={self.exercises})"
        )


def resolve_muscle_group(exercise_name: str) -> str:
    """Return the muscle group for an exercise, or 'other' if unknown."""
    normalized = exercise_name.strip().lower()
    return EXERCISE_MUSCLE_MAP.get(normalized, "other")


def group_by_muscle(entries: List[WorkoutEntry]) -> Dict[str, MuscleGroupSummary]:
    """Aggregate workout entries by muscle group."""
    groups: Dict[str, dict] = {}

    for entry in entries:
        group = resolve_muscle_group(entry.exercise)
        volume = entry.sets * entry.reps * entry.weight

        if group not in groups:
            groups[group] = {
                "total_volume": 0.0,
                "exercise_count": 0,
                "exercises": [],
        }

        groups[group]["total_volume"] += volume
        groups[group]["exercise_count"] += 1
        if entry.exercise not in groups[group]["exercises"]:
            groups[group]["exercises"].append(entry.exercise)

    return {
        group: MuscleGroupSummary(
            muscle_group=group,
            total_volume=round(data["total_volume"], 2),
            exercise_count=data["exercise_count"],
            exercises=data["exercises"],
        )
        for group, data in groups.items()
    }
