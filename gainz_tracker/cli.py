"""Entry point for the gainz-tracker CLI."""

import argparse
import sys
from pathlib import Path

from gainz_tracker.csv_loader import load_csv
from gainz_tracker.stats import compute_stats, personal_records, filter_by_exercise
from gainz_tracker.formatter import (
    format_stats_table,
    format_personal_records,
    format_single_exercise,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gainz-tracker",
        description="Log and visualize workout progress from CSV exports.",
    )
    parser.add_argument("csv_file", type=Path, help="Path to the workout CSV file")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("summary", help="Show per-exercise statistics")
    sub.add_parser("prs", help="Show personal records")

    detail = sub.add_parser("detail", help="Show stats for a single exercise")
    detail.add_argument("exercise", type=str, help="Exercise name (case-insensitive)")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.csv_file.exists():
        print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
        return 1

    entries = load_csv(args.csv_file)
    if not entries:
        print("No valid entries found in CSV.", file=sys.stderr)
        return 1

    command = args.command or "summary"

    if command == "summary":
        stats = compute_stats(entries)
        print(format_stats_table(stats))

    elif command == "prs":
        prs = personal_records(entries)
        print(format_personal_records(prs))

    elif command == "detail":
        filtered = filter_by_exercise(entries, args.exercise)
        if not filtered:
            print(f"No entries found for exercise: {args.exercise!r}")
            return 1
        stats = compute_stats(filtered)
        prs = personal_records(filtered)
        ex_key = next(iter(stats))
        print(format_single_exercise(ex_key, stats[ex_key], prs[ex_key]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
