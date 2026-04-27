"""Workout notes: attach and retrieve text notes for workout sessions."""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional
from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class WorkoutNote:
    workout_date: date
    exercise: str
    note: str

    def __repr__(self) -> str:
        return f"WorkoutNote({self.workout_date}, {self.exercise!r}, {self.note!r})"


def attach_note(notes: List[WorkoutNote], workout_date: date, exercise: str, note: str) -> List[WorkoutNote]:
    """Add a note for a specific date and exercise, replacing any existing one."""
    updated = [
        n for n in notes
        if not (n.workout_date == workout_date and n.exercise.lower() == exercise.lower())
    ]
    updated.append(WorkoutNote(workout_date=workout_date, exercise=exercise, note=note))
    return updated


def get_notes_for_exercise(notes: List[WorkoutNote], exercise: str) -> List[WorkoutNote]:
    """Return all notes for a given exercise, sorted by date."""
    matched = [n for n in notes if n.exercise.lower() == exercise.lower()]
    return sorted(matched, key=lambda n: n.workout_date)


def get_notes_for_date(notes: List[WorkoutNote], workout_date: date) -> List[WorkoutNote]:
    """Return all notes recorded on a specific date."""
    return [n for n in notes if n.workout_date == workout_date]


def notes_summary(notes: List[WorkoutNote]) -> Dict[str, int]:
    """Return a dict mapping each exercise to its note count."""
    summary: Dict[str, int] = {}
    for note in notes:
        key = note.exercise.lower()
        summary[key] = summary.get(key, 0) + 1
    return summary


def find_note(
    notes: List[WorkoutNote], workout_date: date, exercise: str
) -> Optional[WorkoutNote]:
    """Find a single note by date and exercise name."""
    for n in notes:
        if n.workout_date == workout_date and n.exercise.lower() == exercise.lower():
            return n
    return None
