"""Export workout stats and personal records to JSON or CSV formats."""

import csv
import json
from io import StringIO
from typing import Dict, List

from gainz_tracker.stats import ExerciseStats


def export_stats_to_json(stats: Dict[str, ExerciseStats], indent: int = 2) -> str:
    """Serialize exercise stats dict to a JSON string."""
    payload = {}
    for exercise, s in stats.items():
        payload[exercise] = {
            "exercise": s.exercise,
            "total_sets": s.total_sets,
            "total_reps": s.total_reps,
            "max_weight": s.max_weight,
            "avg_weight": round(s.avg_weight, 2),
            "sessions": s.sessions,
        }
    return json.dumps(payload, indent=indent)


def export_stats_to_csv(stats: Dict[str, ExerciseStats]) -> str:
    """Serialize exercise stats dict to a CSV string."""
    fieldnames = [
        "exercise",
        "total_sets",
        "total_reps",
        "max_weight",
        "avg_weight",
        "sessions",
    ]
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for exercise, s in stats.items():
        writer.writerow({
            "exercise": s.exercise,
            "total_sets": s.total_sets,
            "total_reps": s.total_reps,
            "max_weight": s.max_weight,
            "avg_weight": round(s.avg_weight, 2),
            "sessions": s.sessions,
        })
    return buf.getvalue()


def export_prs_to_json(prs: Dict[str, float], indent: int = 2) -> str:
    """Serialize personal records dict to a JSON string."""
    return json.dumps(prs, indent=indent)


def export_prs_to_csv(prs: Dict[str, float]) -> str:
    """Serialize personal records dict to a CSV string."""
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=["exercise", "max_weight"])
    writer.writeheader()
    for exercise, weight in prs.items():
        writer.writerow({"exercise": exercise, "max_weight": weight})
    return buf.getvalue()
