"""Tests for gainz_tracker.formatter module."""

from datetime import date

import pytest

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.stats import ExerciseStats, compute_stats, personal_records
from gainz_tracker.formatter import (
    format_stats_table,
    format_personal_records,
    format_single_exercise,
)


@pytest.fixture
def squat_stats():
    return ExerciseStats(
        exercise="Squat",
        total_sets=6,
        total_reps=28,
        max_weight=120.0,
        min_weight=100.0,
        avg_weight=110.0,
        sessions=3,
    )


@pytest.fixture
def squat_pr():
    return WorkoutEntry(
        date=date(2024, 3, 1), exercise="Squat", sets=3, reps=3, weight=120.0
    )


def test_format_stats_table_contains_exercise(squat_stats):
    output = format_stats_table({"Squat": squat_stats})
    assert "Squat" in output
    assert "120.0" in output


def test_format_stats_table_empty():
    assert format_stats_table({}) == "No data to display."


def test_format_stats_table_header():
    stats = {"Squat": ExerciseStats("Squat", 1, 5, 100.0, 100.0, 100.0, 1)}
    output = format_stats_table(stats)
    assert "Exercise" in output
    assert "Sessions" in output
    assert "Max (kg)" in output


def test_format_personal_records(squat_pr):
    output = format_personal_records({"Squat": squat_pr})
    assert "Squat" in output
    assert "120.0" in output
    assert "2024-03-01" in output


def test_format_personal_records_empty():
    assert format_personal_records({}) == "No personal records found."


def test_format_single_exercise(squat_stats, squat_pr):
    output = format_single_exercise("Squat", squat_stats, squat_pr)
    assert "Squat" in output
    assert "120.0" in output
    assert "110.0" in output
    assert "PR on" in output
