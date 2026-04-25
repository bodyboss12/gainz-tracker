"""Tests for gainz_tracker.comparator module."""

from datetime import date

import pytest

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.comparator import compare_periods, ComparisonResult


@pytest.fixture
def sample_entries():
    return [
        WorkoutEntry(date=date(2024, 1, 5), exercise="Squat", sets=3, reps=5, weight=100.0),
        WorkoutEntry(date=date(2024, 1, 10), exercise="Squat", sets=3, reps=5, weight=105.0),
        WorkoutEntry(date=date(2024, 1, 10), exercise="Bench", sets=3, reps=8, weight=80.0),
        WorkoutEntry(date=date(2024, 2, 5), exercise="Squat", sets=3, reps=5, weight=110.0),
        WorkoutEntry(date=date(2024, 2, 10), exercise="Squat", sets=3, reps=5, weight=115.0),
        WorkoutEntry(date=date(2024, 2, 10), exercise="Bench", sets=3, reps=8, weight=85.0),
    ]


period_a = (date(2024, 1, 1), date(2024, 1, 31))
period_b = (date(2024, 2, 1), date(2024, 2, 28))


def test_compare_periods_returns_dict(sample_entries):
    result = compare_periods(sample_entries, period_a, period_b)
    assert isinstance(result, dict)


def test_compare_periods_keys(sample_entries):
    result = compare_periods(sample_entries, period_a, period_b)
    assert "Squat" in result
    assert "Bench" in result


def test_compare_periods_squat_max(sample_entries):
    result = compare_periods(sample_entries, period_a, period_b)
    squat = result["Squat"]
    assert squat.period_a_max == 105.0
    assert squat.period_b_max == 115.0
    assert squat.max_delta == pytest.approx(10.0)


def test_compare_periods_improved_flag(sample_entries):
    result = compare_periods(sample_entries, period_a, period_b)
    assert result["Squat"].improved is True
    assert result["Bench"].improved is True


def test_compare_periods_no_improvement():
    entries = [
        WorkoutEntry(date=date(2024, 1, 5), exercise="Squat", sets=3, reps=5, weight=120.0),
        WorkoutEntry(date=date(2024, 2, 5), exercise="Squat", sets=3, reps=5, weight=110.0),
    ]
    result = compare_periods(entries, period_a, period_b)
    assert result["Squat"].improved is False
    assert result["Squat"].max_delta == pytest.approx(-10.0)


def test_compare_periods_missing_in_period_a(sample_entries):
    """Exercise only in period B should have period_a_max of 0."""
    entries = sample_entries + [
        WorkoutEntry(date=date(2024, 2, 15), exercise="Deadlift", sets=1, reps=3, weight=150.0),
    ]
    result = compare_periods(entries, period_a, period_b)
    assert "Deadlift" in result
    assert result["Deadlift"].period_a_max == 0.0
    assert result["Deadlift"].period_b_max == 150.0
    assert result["Deadlift"].improved is True


def test_compare_periods_empty_entries():
    result = compare_periods([], period_a, period_b)
    assert result == {}


def test_comparison_result_repr(sample_entries):
    result = compare_periods(sample_entries, period_a, period_b)
    r = repr(result["Squat"])
    assert "Squat" in r
    assert "up" in r
