from typing import List, Dict
from gainz_tracker.stats import ExerciseStats
from gainz_tracker.scheduler import WorkoutSchedule
from gainz_tracker.rest_analyzer import RestAnalysis
from gainz_tracker.plateau_detector import PlateauResult


def format_stats_table(stats: Dict[str, ExerciseStats]) -> str:
    if not stats:
        return "No stats available."
    header = f"{'Exercise':<20} {'Sessions':>8} {'Max Weight':>12} {'Avg Reps':>9}"
    sep = "-" * len(header)
    rows = [header, sep]
    for name, s in sorted(stats.items()):
        rows.append(
            f"{name:<20} {s.sessions:>8} {s.max_weight:>12.1f} {s.avg_reps:>9.1f}"
        )
    return "\n".join(rows)


def format_personal_records(prs: Dict[str, float]) -> str:
    if not prs:
        return "No personal records found."
    header = f"{'Exercise':<20} {'PR Weight':>10}"
    sep = "-" * len(header)
    rows = [header, sep]
    for name, weight in sorted(prs.items()):
        rows.append(f"{name:<20} {weight:>10.1f}")
    return "\n".join(rows)


def format_single_exercise(name: str, stats: ExerciseStats) -> str:
    lines = [
        f"Exercise : {name}",
        f"Sessions : {stats.sessions}",
        f"Max Weight: {stats.max_weight:.1f}",
        f"Avg Reps : {stats.avg_reps:.1f}",
        f"Total Vol : {stats.total_volume:.1f}",
    ]
    return "\n".join(lines)


def format_schedule(schedules: List[WorkoutSchedule]) -> str:
    if not schedules:
        return "No schedule data available."
    header = f"{'Exercise':<20} {'Last Workout':<14} {'Next Due':<14} {'Overdue?':>8}"
    sep = "-" * len(header)
    rows = [header, sep]
    for s in sorted(schedules, key=lambda x: x.exercise):
        overdue = "YES" if s.is_overdue else "-"
        rows.append(
            f"{s.exercise:<20} {str(s.last_workout):<14} {str(s.next_due):<14} {overdue:>8}"
        )
    return "\n".join(rows)


def format_rest_analysis(analyses: Dict[str, RestAnalysis]) -> str:
    if not analyses:
        return "No rest data available."
    header = f"{'Exercise':<20} {'Avg Rest':>9} {'Min Rest':>9} {'Max Rest':>9} {'Overtrain?':>11}"
    sep = "-" * len(header)
    rows = [header, sep]
    for name, a in sorted(analyses.items()):
        flag = "YES" if a.overtraining_risk else "-"
        rows.append(
            f"{name:<20} {a.avg_rest_days:>9.1f} {a.min_rest_days:>9} "
            f"{a.max_rest_days:>9} {flag:>11}"
        )
    return "\n".join(rows)


def format_plateau_report(plateaus: Dict[str, PlateauResult]) -> str:
    """Format plateau detection results as a human-readable table."""
    if not plateaus:
        return "No plateau data available."
    header = (
        f"{'Exercise':<20} {'Weeks Flat':>11} {'Max Weight':>11} {'Status':>12}"
    )
    sep = "-" * len(header)
    rows = [header, sep]
    for name, p in sorted(plateaus.items()):
        status = "PLATEAU" if p.is_plateau else "Progressing"
        rows.append(
            f"{name:<20} {p.weeks_flat:>11} {p.max_weight:>11.1f} {status:>12}"
        )
    return "\n".join(rows)
