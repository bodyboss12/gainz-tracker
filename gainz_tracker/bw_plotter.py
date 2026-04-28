"""ASCII chart for body weight over time."""

from typing import List
from gainz_tracker.body_weight import BodyWeightEntry


def _normalize(value: float, min_val: float, max_val: float, height: int) -> int:
    """Map a value to a row index within chart height."""
    if max_val == min_val:
        return height // 2
    ratio = (value - min_val) / (max_val - min_val)
    return int(ratio * (height - 1))


def plot_weight_ascii(
    entries: List[BodyWeightEntry],
    width: int = 40,
    height: int = 10,
) -> str:
    """Render an ASCII line chart of body weight over time."""
    if not entries:
        return "No body weight data to display."

    sorted_entries = sorted(entries, key=lambda e: e.date)
    weights = [e.weight_kg for e in sorted_entries]
    min_w = min(weights)
    max_w = max(weights)

    # Sample down to fit width
    step = max(1, len(weights) // width)
    sampled = weights[::step][:width]

    grid = [[" " for _ in range(len(sampled))] for _ in range(height)]

    for col, w in enumerate(sampled):
        row = _normalize(w, min_w, max_w, height)
        grid[height - 1 - row][col] = "*"

    lines = []
    for i, row in enumerate(grid):
        label_val = max_w - (max_w - min_w) * i / (height - 1) if height > 1 else min_w
        label = f"{label_val:5.1f} |"
        lines.append(label + "".join(row))

    x_axis = "      " + "-" * len(sampled)
    date_labels = (
        f"      {sorted_entries[0].date}" + " " * (len(sampled) - 20) +
        f"{sorted_entries[-1].date}"
    )
    lines.append(x_axis)
    lines.append(date_labels)
    return "\n".join(lines)
