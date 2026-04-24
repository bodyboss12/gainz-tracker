"""Tests for gainz_tracker.plotter."""

import datetime
import pytest

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.plotter import ascii_progress, _group_by_date


@pytest.fixture()
def squat_entries():
    return [
        WorkoutEntry(date=datetime.date(2024, 1, 1), exercise="Squat", sets=3, reps=5, weight_kg=100.0),
        WorkoutEntry(date=datetime.date(2024, 1, 8), exercise="Squat", sets=3, reps=5, weight_kg=105.0),
        WorkoutEntry(date=datetime.date(2024, 1, 8), exercise="Squat", sets=1, reps=1, weight_kg=110.0),
        WorkoutEntry(date=datetime.date(2024, 1, 15), exercise="Squat", sets=3, reps=5, weight_kg=107.5),
    ]


@pytest.fixture()
def mixed_entries(squat_entries):
    bench = WorkoutEntry(date=datetime.date(2024, 1, 1), exercise="Bench Press", sets=3, reps=8, weight_kg=80.0)
    return squat_entries + [bench]


def test_group_by_date_max_per_day(squat_entries):
    result = _group_by_date(squat_entries)
    assert result["2024-01-08"] == 110.0


def test_group_by_date_sorted(squat_entries):
    result = _group_by_date(squat_entries)
    keys = list(result.keys())
    assert keys == sorted(keys)


def test_group_by_date_unique_dates(squat_entries):
    result = _group_by_date(squat_entries)
    assert len(result) == 3


def test_ascii_progress_no_data(squat_entries):
    output = ascii_progress(squat_entries, "Deadlift")
    assert "No data" in output
    assert "Deadlift" in output


def test_ascii_progress_contains_exercise(squat_entries):
    output = ascii_progress(squat_entries, "Squat")
    assert "Squat" in output


def test_ascii_progress_shows_dates(squat_entries):
    output = ascii_progress(squat_entries, "Squat")
    assert "2024-01-01" in output
    assert "2024-01-15" in output


def test_ascii_progress_shows_max_weight(squat_entries):
    output = ascii_progress(squat_entries, "Squat")
    assert "110.0" in output


def test_ascii_progress_case_insensitive(squat_entries):
    lower = ascii_progress(squat_entries, "squat")
    upper = ascii_progress(squat_entries, "SQUAT")
    assert "No data" not in lower
    assert "No data" not in upper


def test_ascii_progress_filters_other_exercises(mixed_entries):
    output = ascii_progress(mixed_entries, "Squat")
    assert "Bench Press" not in output


def test_ascii_progress_single_entry():
    entries = [
        WorkoutEntry(date=datetime.date(2024, 3, 1), exercise="OHP", sets=3, reps=8, weight_kg=60.0)
    ]
    output = ascii_progress(entries, "OHP")
    assert "OHP" in output
    assert "60.0" in output
