"""Format stats and records for CLI output."""

from typing import Dict

from gainz_tracker.stats import ExerciseStats
from gainz_tracker.csv_loader import WorkoutEntry


COL_WIDTH = 14
HEADER = (
    f"{'Exercise':<20} {'Sessions':>{COL_WIDTH}} {'Sets':>{COL_WIDTH}} "
    f"{'Total Reps':>{COL_WIDTH}} {'Max (kg)':>{COL_WIDTH}} {'Avg (kg)':>{COL_WIDTH}}"
)
SEPARATOR = "-" * len(HEADER)


def format_stats_table(stats: Dict[str, ExerciseStats]) -> str:
    """Render a plain-text table of exercise statistics."""
    if not stats:
        return "No data to display."

    lines = [HEADER, SEPARATOR]
    for exercise, s in sorted(stats.items()):
        lines.append(
            f"{exercise:<20} {s.sessions:>{COL_WIDTH}} {s.total_sets:>{COL_WIDTH}} "
            f"{s.total_reps:>{COL_WIDTH}} {s.max_weight:>{COL_WIDTH}.1f} "
            f"{s.avg_weight:>{COL_WIDTH}.1f}"
        )
    return "\n".join(lines)


def format_personal_records(prs: Dict[str, WorkoutEntry]) -> str:
    """Render a plain-text list of personal records."""
    if not prs:
        return "No personal records found."

    lines = ["Personal Records", SEPARATOR]
    for exercise, entry in sorted(prs.items()):
        lines.append(
            f"  {exercise:<20}  {entry.weight:>7.1f} kg  "
            f"({entry.reps} reps on {entry.date})"
        )
    return "\n".join(lines)


def format_single_exercise(
    exercise: str, stats: ExerciseStats, pr: WorkoutEntry
) -> str:
    """Render a brief summary for a single exercise."""
    return (
        f"Exercise : {exercise}\n"
        f"Sessions : {stats.sessions}\n"
        f"Total sets: {stats.total_sets}\n"
        f"Total reps: {stats.total_reps}\n"
        f"Max weight: {stats.max_weight:.1f} kg  (PR on {pr.date}, {pr.reps} reps)\n"
        f"Avg weight: {stats.avg_weight:.1f} kg\n"
        f"Min weight: {stats.min_weight:.1f} kg"
    )
