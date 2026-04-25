from typing import List, Dict
from gainz_tracker.stats import ExerciseStats
from gainz_tracker.scheduler import WorkoutSchedule


def format_stats_table(stats: Dict[str, ExerciseStats]) -> str:
    """Render a summary table of all exercise stats."""
    if not stats:
        return "No stats available."

    header = f"{'Exercise':<20} {'Sessions':>8} {'Max Weight':>12} {'Avg Reps':>10}"
    sep = "-" * len(header)
    rows = [header, sep]

    for exercise, s in sorted(stats.items()):
        rows.append(
            f"{exercise:<20} {s.total_sessions:>8} {s.max_weight:>12.1f} {s.avg_reps:>10.1f}"
        )

    return "\n".join(rows)


def format_personal_records(prs: Dict[str, float]) -> str:
    """Render personal records as a formatted list."""
    if not prs:
        return "No personal records found."

    lines = ["Personal Records:", "-" * 30]
    for exercise, weight in sorted(prs.items()):
        lines.append(f"  {exercise:<20} {weight:.1f} kg")
    return "\n".join(lines)


def format_single_exercise(exercise: str, stats: ExerciseStats) -> str:
    """Render detailed stats for one exercise."""
    lines = [
        f"Exercise : {exercise}",
        f"Sessions : {stats.total_sessions}",
        f"Max Weight: {stats.max_weight:.1f} kg",
        f"Avg Reps : {stats.avg_reps:.1f}",
        f"Total Vol : {stats.total_volume:.1f} kg",
    ]
    return "\n".join(lines)


def format_schedule(schedules: List[WorkoutSchedule], as_of=None) -> str:
    """Render the recommended workout schedule as a table."""
    if not schedules:
        return "No schedule data available."

    header = f"{'Exercise':<20} {'Next Session':<14} {'Days Since':>10} {'Overdue By':>12}"
    sep = "-" * len(header)
    rows = [header, sep]

    for s in schedules:
        overdue_str = f"{s.overdue_by}d" if s.overdue_by > 0 else "-"
        rows.append(
            f"{s.exercise:<20} {str(s.recommended_date):<14} "
            f"{s.days_since_last:>10} {overdue_str:>12}"
        )

    return "\n".join(rows)
