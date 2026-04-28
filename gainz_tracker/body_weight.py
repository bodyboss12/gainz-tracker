"""Track body weight entries and compute trends over time."""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class BodyWeightEntry:
    date: date
    weight_kg: float

    def __repr__(self) -> str:
        return f"BodyWeightEntry(date={self.date}, weight_kg={self.weight_kg})"


@dataclass
class BodyWeightTrend:
    start_weight: float
    end_weight: float
    min_weight: float
    max_weight: float
    avg_weight: float
    change_kg: float
    num_entries: int

    def __repr__(self) -> str:
        return (
            f"BodyWeightTrend(start={self.start_weight}, end={self.end_weight}, "
            f"change={self.change_kg:+.2f}kg, entries={self.num_entries})"
        )


def log_weight(entries: List[BodyWeightEntry], new_date: date, weight_kg: float) -> List[BodyWeightEntry]:
    """Add or replace a body weight entry for the given date."""
    updated = [e for e in entries if e.date != new_date]
    updated.append(BodyWeightEntry(date=new_date, weight_kg=weight_kg))
    return sorted(updated, key=lambda e: e.date)


def compute_trend(entries: List[BodyWeightEntry]) -> Optional[BodyWeightTrend]:
    """Compute weight trend statistics from a list of entries."""
    if not entries:
        return None

    sorted_entries = sorted(entries, key=lambda e: e.date)
    weights = [e.weight_kg for e in sorted_entries]

    return BodyWeightTrend(
        start_weight=weights[0],
        end_weight=weights[-1],
        min_weight=min(weights),
        max_weight=max(weights),
        avg_weight=round(sum(weights) / len(weights), 2),
        change_kg=round(weights[-1] - weights[0], 2),
        num_entries=len(weights),
    )


def filter_by_date_range(
    entries: List[BodyWeightEntry],
    start: Optional[date] = None,
    end: Optional[date] = None,
) -> List[BodyWeightEntry]:
    """Return entries within an inclusive date range."""
    result = entries
    if start:
        result = [e for e in result if e.date >= start]
    if end:
        result = [e for e in result if e.date <= end]
    return result
