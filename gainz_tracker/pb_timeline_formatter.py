"""Format personal best timeline data for CLI display."""

from typing import Dict, List

from gainz_tracker.personal_best_timeline import PBTimelineEntry, days_between_pbs


def format_pb_timeline(
    timeline_data: Dict[str, List[PBTimelineEntry]],
) -> str:
    """Render a table of PB progressions per exercise."""
    if not timeline_data:
        return "No personal best data available."

    lines = []
    header = f"{'Exercise':<20} {'Date':<12} {'Weight':>8} {'Prev Best':>10} {'Gain':>8}"
    separator = "-" * len(header)

    lines.append("=== Personal Best Timeline ===")
    lines.append(separator)
    lines.append(header)
    lines.append(separator)

    for exercise, timeline in sorted(timeline_data.items()):
        for entry in timeline:
            gain_str = (
                f"+{entry.weight - entry.previous_best:.1f}"
                if entry.previous_best is not None
                else "first"
            )
            prev_str = (
                f"{entry.previous_best:.1f}" if entry.previous_best is not None else "-"
            )
            lines.append(
                f"{entry.exercise:<20} {str(entry.date):<12} "
                f"{entry.weight:>8.1f} {prev_str:>10} {gain_str:>8}"
            )
        lines.append("")

    return "\n".join(lines).rstrip()


def format_pb_gaps(timeline_data: Dict[str, List[PBTimelineEntry]]) -> str:
    """Show average days between personal bests per exercise."""
    if not timeline_data:
        return "No timeline data to summarize."

    lines = ["=== Avg Days Between PRs ==="]
    lines.append(f"{'Exercise':<20} {'Avg Days':>10} {'Total PRs':>10}")
    lines.append("-" * 42)

    for exercise, timeline in sorted(timeline_data.items()):
        gaps = days_between_pbs(timeline)
        avg = sum(gaps) / len(gaps) if gaps else 0.0
        lines.append(
            f"{exercise:<20} {avg:>10.1f} {len(timeline):>10}"
        )

    return "\n".join(lines)
