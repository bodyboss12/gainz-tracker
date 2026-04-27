"""Workout frequency heatmap — shows activity intensity per day of week."""

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict
from gainz_tracker.csv_loader import WorkoutEntry

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SHADES = [" ", "░", "▒", "▓", "█"]


@dataclass
class HeatmapData:
    day_counts: Dict[str, int]
    max_count: int
    total_sessions: int

    def __repr__(self) -> str:
        return (
            f"HeatmapData(total_sessions={self.total_sessions}, "
            f"max_count={self.max_count})"
        )


def compute_heatmap(entries: List[WorkoutEntry]) -> HeatmapData:
    """Count unique workout sessions per day of week."""
    # group by (date, day_of_week) to avoid double-counting same day
    seen: Dict[str, str] = {}
    for entry in entries:
        date_str = entry.date.strftime("%Y-%m-%d")
        if date_str not in seen:
            seen[date_str] = DAYS[entry.date.weekday()]

    day_counts: Dict[str, int] = defaultdict(int)
    for day in DAYS:
        day_counts[day] = 0
    for day in seen.values():
        day_counts[day] += 1

    max_count = max(day_counts.values()) if day_counts else 0
    total_sessions = len(seen)
    return HeatmapData(
        day_counts=dict(day_counts),
        max_count=max_count,
        total_sessions=total_sessions,
    )


def render_heatmap(data: HeatmapData) -> str:
    """Render an ASCII heatmap bar chart for workout frequency by day."""
    if data.total_sessions == 0:
        return "No workout data to display."

    lines = ["Workout Frequency by Day of Week", "-" * 34]
    for day in DAYS:
        count = data.day_counts.get(day, 0)
        shade_idx = (
            int((count / data.max_count) * (len(SHADES) - 1))
            if data.max_count > 0
            else 0
        )
        bar = SHADES[shade_idx] * 10
        lines.append(f"{day}: {bar} {count:>3}")

    lines.append("-" * 34)
    lines.append(f"Total sessions: {data.total_sessions}")
    return "\n".join(lines)
