"""Tests for personal_best_timeline module."""

from datetime import date
from typing import List

import pytest

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.personal_best_timeline import (
    PBTimelineEntry,
    build_pb_timeline,
    days_between_pbs,
)


def make_entry(exercise: str, weight: float, day: int) -> WorkoutEntry:
    return WorkoutEntry(
        date=date(2024, 1, day),
        exercise=exercise,
        sets=3,
        reps=5,
        weight=weight,
    )


@pytest.fixture
def squat_entries() -> List[WorkoutEntry]:
    return [
        make_entry("Squat", 100.0, 1),
        make_entry("Squat", 95.0, 2),   # not a PB
        make_entry("Squat", 105.0, 3),  # new PB
        make_entry("Squat", 105.0, 4),  # tie, not a PB
        make_entry("Squat", 110.0, 5),  # new PB
    ]


@pytest.fixture
def mixed_entries(squat_entries) -> List[WorkoutEntry]:
    bench = [
        make_entry("Bench", 60.0, 1),
        make_entry("Bench", 65.0, 4),
    ]
    return squat_entries + bench


def test_build_pb_timeline_empty():
    result = build_pb_timeline([])
    assert result == {}


def test_build_pb_timeline_returns_dict(squat_entries):
    result = build_pb_timeline(squat_entries)
    assert isinstance(result, dict)
    assert "squat" in result


def test_build_pb_timeline_only_pbs(squat_entries):
    timeline = build_pb_timeline(squat_entries)["squat"]
    weights = [t.weight for t in timeline]
    assert weights == [100.0, 105.0, 110.0]


def test_build_pb_timeline_first_entry_has_no_previous(squat_entries):
    timeline = build_pb_timeline(squat_entries)["squat"]
    assert timeline[0].previous_best is None


def test_build_pb_timeline_previous_best_correct(squat_entries):
    timeline = build_pb_timeline(squat_entries)["squat"]
    assert timeline[1].previous_best == 100.0
    assert timeline[2].previous_best == 105.0


def test_build_pb_timeline_multiple_exercises(mixed_entries):
    result = build_pb_timeline(mixed_entries)
    assert "squat" in result
    assert "bench" in result


def test_build_pb_timeline_bench_pbs(mixed_entries):
    timeline = build_pb_timeline(mixed_entries)["bench"]
    assert [t.weight for t in timeline] == [60.0, 65.0]


def test_build_pb_timeline_case_insensitive():
    entries = [
        make_entry("SQUAT", 100.0, 1),
        make_entry("squat", 110.0, 2),
    ]
    result = build_pb_timeline(entries)
    assert "squat" in result
    assert len(result["squat"]) == 2


def test_days_between_pbs_empty():
    assert days_between_pbs([]) == []


def test_days_between_pbs_single():
    entry = PBTimelineEntry("Squat", date(2024, 1, 1), 100.0, None)
    assert days_between_pbs([entry]) == []


def test_days_between_pbs_correct(squat_entries):
    timeline = build_pb_timeline(squat_entries)["squat"]
    gaps = days_between_pbs(timeline)
    assert gaps == [2, 2]  # day1->day3, day3->day5
