"""ASCII/matplotlib progress charts for workout entries."""

from __future__ import annotations

from collections import defaultdict
from typing import List

from gainz_tracker.csv_loader import WorkoutEntry

try:
    import matplotlib.pyplot as plt
    _MPL_AVAILABLE = True
except ImportError:  # pragma: no cover
    _MPL_AVAILABLE = False


def _group_by_date(entries: List[WorkoutEntry]) -> dict[str, float]:
    """Return max weight per date for a list of entries (single exercise)."""
    by_date: dict[str, float] = defaultdict(float)
    for e in entries:
        date_str = e.date.strftime("%Y-%m-%d")
        if e.weight_kg > by_date[date_str]:
            by_date[date_str] = e.weight_kg
    return dict(sorted(by_date.items()))


def ascii_progress(entries: List[WorkoutEntry], exercise: str) -> str:
    """Return a simple ASCII sparkline of max weight over time."""
    relevant = [e for e in entries if e.exercise.lower() == exercise.lower()]
    if not relevant:
        return f"No data found for '{exercise}'."

    by_date = _group_by_date(relevant)
    dates = list(by_date.keys())
    weights = list(by_date.values())

    max_w = max(weights)
    min_w = min(weights)
    height = 8
    width = len(weights)

    lines = []
    lines.append(f"Progress: {exercise}  ({dates[0]} → {dates[-1]})")
    lines.append(f"Max: {max_w:.1f} kg" + " " * 4 + f"Min: {min_w:.1f} kg")
    lines.append("")

    span = max_w - min_w or 1.0
    rows = []
    for row in range(height, 0, -1):
        threshold = min_w + span * (row - 1) / height
        label = f"{threshold:6.1f} |"
        bar = "".join("█" if w >= threshold else " " for w in weights)
        rows.append(label + bar)
    rows.append(" " * 8 + "-" * width)
    rows.append(" " * 8 + dates[0] + " " * (width - len(dates[0]) - len(dates[-1])) + dates[-1])
    lines.extend(rows)
    return "\n".join(lines)


def plot_progress(entries: List[WorkoutEntry], exercise: str, save_path: str | None = None) -> None:
    """Render a matplotlib line chart. Falls back to ascii_progress if unavailable."""
    if not _MPL_AVAILABLE:
        print(ascii_progress(entries, exercise))
        return

    relevant = [e for e in entries if e.exercise.lower() == exercise.lower()]
    if not relevant:
        print(f"No data found for '{exercise}'.")
        return

    by_date = _group_by_date(relevant)
    dates = list(by_date.keys())
    weights = list(by_date.values())

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dates, weights, marker="o", linewidth=2, color="steelblue")
    ax.set_title(f"{exercise} — weight over time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Max weight (kg)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path)
        print(f"Chart saved to {save_path}")
    else:
        plt.show()
