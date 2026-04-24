"""CSV loader module for parsing fitness app exports."""

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class WorkoutEntry:
    date: datetime
    exercise: str
    sets: int
    reps: int
    weight_kg: float
    notes: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"WorkoutEntry({self.date.date()} | {self.exercise} | "
            f"{self.sets}x{self.reps} @ {self.weight_kg}kg)"
        )


REQUIRED_COLUMNS = {"date", "exercise", "sets", "reps", "weight_kg"}


def load_csv(filepath: str | Path) -> List[WorkoutEntry]:
    """Load and parse a workout CSV file into a list of WorkoutEntry objects."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path.suffix}")

    entries: List[WorkoutEntry] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing headers.")

        columns = {col.strip().lower() for col in reader.fieldnames}
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"CSV is missing required columns: {missing}")

        for line_num, row in enumerate(reader, start=2):
            try:
                entry = WorkoutEntry(
                    date=datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                    exercise=row["exercise"].strip(),
                    sets=int(row["sets"]),
                    reps=int(row["reps"]),
                    weight_kg=float(row["weight_kg"]),
                    notes=row.get("notes", "").strip() or None,
                )
                entries.append(entry)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error parsing row {line_num}: {e}") from e

    return entries
