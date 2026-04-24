"""Tests for gainz_tracker.stats module."""

import pytest
from datetime import date

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.stats import (
    compute_stats,
    personal_records,
    filter_by_exercise,
)


@pytest.fixture
def sample_entries():
    return [
        WorkoutEntry(date=date(2024, 1, 1), exercise="Squat", sets=3, reps=5, weight=100.0),
        WorkoutEntry(date=date(2024, 1, 1), exercise="Squat", sets=3, reps=5, weight=100.0),
        WorkoutEntry(date=date(2024, 1, 8), exercise="Squat", sets=3, reps=3, weight=110.0),
        WorkoutEntry(date=date(2024, 1, 1), exercise="Bench Press", sets=4, reps=8, weight=80.0),
        WorkoutEntry(date=date(2024, 1, 8), exercise="Bench Press", sets=4, reps=8, weight=85.0),
    ]


def test_compute_stats_keys(sample_entries):
    stats = compute_stats(sample_entries)
    assert set(stats.keys()) == {"Squat", "Bench Press"}


def test_compute_stats_squat(sample_entries):
    stats = compute_stats(sample_entries)
    s = stats["Squat"]
    assert s.total_sets == 3
    assert s.total_reps == 5 + 5 + 3
    assert s.max_weight == 110.0
    assert s.min_weight == 100.0
    assert s.avg_weight == pytest.approx((100.0 + 100.0 + 110.0) / 3)
    assert s.sessions == 2


def test_compute_stats_bench(sample_entries):
    stats = compute_stats(sample_entries)
    b = stats["Bench Press"]
    assert b.total_sets == 2
    assert b.max_weight == 85.0
    assert b.sessions == 2


def test_compute_stats_empty():
    assert compute_stats([]) == {}


def test_personal_records(sample_entries):
    prs = personal_records(sample_entries)
    assert prs["Squat"].weight == 110.0
    assert prs["Bench Press"].weight == 85.0


def test_personal_records_empty():
    assert personal_records([]) == {}


def test_filter_by_exercise(sample_entries):
    result = filter_by_exercise(sample_entries, "squat")
    assert len(result) == 3
    assert all(e.exercise == "Squat" for e in result)


def test_filter_by_exercise_no_match(sample_entries):
    result = filter_by_exercise(sample_entries, "Deadlift")
    assert result == []


def test_exercise_stats_repr(sample_entries):
    stats = compute_stats(sample_entries)
    r = repr(stats["Squat"])
    assert "Squat" in r
    assert "max_weight" in r
