"""Tests for gainz_tracker/rest_analyzer.py"""

import pytest
from datetime import date

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.rest_analyzer import (
    RestAnalysis,
    _unique_sorted_dates,
    analyze_rest,
)


def make_entry(exercise: str, workout_date: date, weight: float = 100.0, reps: int = 5) -> WorkoutEntry:
    return WorkoutEntry(date=workout_date, exercise=exercise, weight=weight, reps=reps)


@pytest.fixture
def squat_entries():
    return [
        make_entry("squat", date(2024, 1, 1)),
        make_entry("squat", date(2024, 1, 3)),
        make_entry("squat", date(2024, 1, 5)),
        make_entry("squat", date(2024, 1, 12)),
    ]


@pytest.fixture
def mixed_entries(squat_entries):
    return squat_entries + [
        make_entry("bench", date(2024, 1, 1)),
        make_entry("bench", date(2024, 1, 2)),
    ]


def test_unique_sorted_dates_returns_sorted(squat_entries):
    dates = _unique_sorted_dates(squat_entries, "squat")
    assert dates == sorted(dates)


def test_unique_sorted_dates_deduplicates():
    entries = [
        make_entry("squat", date(2024, 1, 1)),
        make_entry("squat", date(2024, 1, 1)),
        make_entry("squat", date(2024, 1, 3)),
    ]
    dates = _unique_sorted_dates(entries, "squat")
    assert len(dates) == 2


def test_unique_sorted_dates_case_insensitive(squat_entries):
    dates_lower = _unique_sorted_dates(squat_entries, "squat")
    dates_upper = _unique_sorted_dates(squat_entries, "SQUAT")
    assert dates_lower == dates_upper


def test_analyze_rest_returns_dict(squat_entries):
    result = analyze_rest(squat_entries)
    assert isinstance(result, dict)


def test_analyze_rest_keys(mixed_entries):
    result = analyze_rest(mixed_entries)
    assert "squat" in result
    assert "bench" in result


def test_analyze_rest_avg_squat(squat_entries):
    result = analyze_rest(squat_entries)
    # gaps: 2, 2, 7 -> avg = 3.67
    assert abs(result["squat"].avg_rest_days - (2 + 2 + 7) / 3) < 0.01


def test_analyze_rest_min_max_squat(squat_entries):
    result = analyze_rest(squat_entries)
    assert result["squat"].min_rest_days == 2
    assert result["squat"].max_rest_days == 7


def test_analyze_rest_overtraining_flag():
    entries = [
        make_entry("deadlift", date(2024, 1, 1)),
        make_entry("deadlift", date(2024, 1, 2)),  # gap=1, threshold min=2
        make_entry("deadlift", date(2024, 1, 5)),
    ]
    result = analyze_rest(entries, min_rest=2, max_rest=6)
    assert result["deadlift"].overtraining_flags == 1


def test_analyze_rest_undertraining_flag(squat_entries):
    # gap of 7 days > max_rest=5
    result = analyze_rest(squat_entries, min_rest=1, max_rest=5)
    assert result["squat"].undertraining_flags == 1


def test_analyze_rest_single_entry_excluded():
    entries = [make_entry("curl", date(2024, 1, 1))]
    result = analyze_rest(entries)
    assert "curl" not in result


def test_analyze_rest_empty():
    result = analyze_rest([])
    assert result == {}


def test_rest_analysis_repr(squat_entries):
    result = analyze_rest(squat_entries)
    r = repr(result["squat"])
    assert "squat" in r
    assert "avg" in r
