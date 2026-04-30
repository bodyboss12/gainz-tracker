"""Track how personal bests evolved over time for each exercise."""

from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Optional

from gainz_tracker.csv_loader import WorkoutEntry


@dataclass
class PBTimelineEntry:
    exercise: str
    date: date
    weight: float
    previous_best: Optional[float]

    def __repr__(self) -> str:
        return (
            f"PBTimelineEntry(exercise={self.exercise!r}, date={self.date}, "
            f"weight={self.weight}, previous_best={self.previous_best})"
        )


def _sorted_entries(entries: List[WorkoutEntry], exercise: str) -> List[WorkoutEntry]:
    """Filter and sort entries for a given exercise by date."""
    filtered = [e for e in entries if e.exercise.lower() == exercise.lower()]
    return sorted(filtered, key=lambda e: e.date)


def build_pb_timeline(
    entries: List[WorkoutEntry],
) -> Dict[str, List[PBTimelineEntry]]:
    """Build a timeline of personal best progressions per exercise.

    Returns a dict mapping exercise name -> list of PBTimelineEntry,
    only including entries where a new personal best was set.
    """
    if not entries:
        return {}

    exercises = {e.exercise.lower() for e in entries}
    result: Dict[str, List[PBTimelineEntry]] = {}

    for exercise in exercises:
        sorted_ex = _sorted_entries(entries, exercise)
        timeline: List[PBTimelineEntry] = []
        current_best: Optional[float] = None

        for entry in sorted_ex:
            if current_best is None or entry.weight > current_best:
                timeline.append(
                    PBTimelineEntry(
                        exercise=entry.exercise,
                        date=entry.date,
                        weight=entry.weight,
                        previous_best=current_best,
                    )
                )
                current_best = entry.weight

        if timeline:
            result[exercise] = timeline

    return result


def days_between_pbs(timeline: List[PBTimelineEntry]) -> List[int]:
    """Return list of day gaps between consecutive personal bests."""
    if len(timeline) < 2:
        return []
    return [
        (timeline[i].date - timeline[i - 1].date).days
        for i in range(1, len(timeline))
    ]
