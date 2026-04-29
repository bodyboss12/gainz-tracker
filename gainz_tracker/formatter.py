"""Format stats, personal records, schedules, and rest analysis for CLI output."""

from typing import Dict, List

from gainz_tracker.stats import ExerciseStats
from gainz_tracker.scheduler import WorkoutSchedule
from gainz_tracker.rest_analyzer import RestAnalysis


def format_stats_table(stats: Dict[str, ExerciseStats]) -> str:
    if not stats:
        return "No stats available."
    header = f"{'Exercise':<20} {'Max Weight':>12} {'Total Reps':>12} {'Sessions':>10}"
    sep = "-" * len(header)
    rows = [header, sep]
    for name, s in sorted(stats.items()):
        rows.append(f"{name:<20} {s.max_weight:>12.1f} {s.total_reps:>12} {s.sessions:>10}")
    return "\n".join(rows)


def format_personal_records(prs: Dict[str, float]) -> str:
    if not prs:
        return "No personal records found."
    header = f"{'Exercise':<20} {'PR (kg)':>10}"
    sep = "-" * len(header)
    rows = [header, sep]
    for name, weight in sorted(prs.items()):
        rows.append(f"{name:<20} {weight:>10.1f}")
    return "\n".join(rows)


def format_single_exercise(name: str, stats: ExerciseStats) -> str:
    lines = [
        f"Exercise : {name}",
        f"Max Weight: {stats.max_weight:.1f} kg",
        f"Total Reps: {stats.total_reps}",
        f"Sessions  : {stats.sessions}",
    ]
    return "\n".join(lines)


def format_schedule(schedules: List[WorkoutSchedule]) -> str:
    if not schedules:
        return "No schedule data available."
    header = f"{'Exercise':<20} {'Next Session':>14} {'Overdue':>10}"
    sep = "-" * len(header)
    rows = [header, sep]
    for s in sorted(schedules, key=lambda x: x.exercise):
        overdue = "YES" if s.is_overdue else "-"
        rows.append(f"{s.exercise:<20} {str(s.next_session_date):>14} {overdue:>10}")
    return "\n".join(rows)


def format_rest_analysis(analysis: Dict[str, RestAnalysis]) -> str:
    """Format rest analysis results as a CLI table."""
    if not analysis:
        return "No rest analysis data available."
    header = (
        f"{'Exercise':<20} {'Avg Rest':>10} {'Min':>6} {'Max':>6} "
        f"{'Overtrain':>11} {'Undertrain':>12}"
    )
    sep = "-" * len(header)
    rows = [header, sep]
    for name, r in sorted(analysis.items()):
        rows.append(
            f"{name:<20} {r.avg_rest_days:>9.1f}d {r.min_rest_days:>5}d "
            f"{r.max_rest_days:>5}d {r.overtraining_flags:>11} {r.undertraining_flags:>12}"
        )
    return "\n".join(rows)
