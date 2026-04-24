"""Tests for streak tracking module."""

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.streak import StreakResult, compute_streaks, _unique_workout_dates


def make_entry(d: date, exercise="Squat", weight=100.0, reps=5, sets=3) -> WorkoutEntry:
    return WorkoutEntry(date=d, exercise=exercise, weight_kg=weight, reps=reps, sets=sets)


TODAY = date(2024, 6, 15)


@pytest.fixture
def consecutive_entries():
    return [
        make_entry(TODAY - timedelta(days=2)),
        make_entry(TODAY - timedelta(days=1)),
        make_entry(TODAY),
    ]


@pytest.fixture
def broken_entries():
    return [
        make_entry(date(2024, 6, 1)),
        make_entry(date(2024, 6, 2)),
        make_entry(date(2024, 6, 5)),  # gap here
        make_entry(date(2024, 6, 6)),
        make_entry(date(2024, 6, 7)),
    ]


def test_compute_streaks_empty():
    result = compute_streaks([])
    assert result.current_streak == 0
    assert result.longest_streak == 0
    assert result.last_workout_date is None


def test_compute_streaks_single_entry():
    with patch("gainz_tracker.streak.date") as mock_date:
        mock_date.today.return_value = TODAY
        entries = [make_entry(TODAY)]
        result = compute_streaks(entries)
    assert result.longest_streak == 1
    assert result.last_workout_date == TODAY


def test_compute_streaks_longest(broken_entries):
    result = compute_streaks(broken_entries)
    assert result.longest_streak == 3


def test_compute_streaks_current_active(consecutive_entries):
    with patch("gainz_tracker.streak.date") as mock_date:
        mock_date.today.return_value = TODAY
        result = compute_streaks(consecutive_entries)
    assert result.current_streak == 3


def test_compute_streaks_current_expired(broken_entries):
    with patch("gainz_tracker.streak.date") as mock_date:
        mock_date.today.return_value = TODAY  # far from last entry (2024-06-07)
        result = compute_streaks(broken_entries)
    assert result.current_streak == 0


def test_unique_workout_dates_deduplicates():
    entries = [
        make_entry(date(2024, 6, 1), exercise="Squat"),
        make_entry(date(2024, 6, 1), exercise="Bench"),
        make_entry(date(2024, 6, 2)),
    ]
    dates = _unique_workout_dates(entries)
    assert len(dates) == 2
    assert dates == sorted(dates)


def test_streak_result_repr():
    r = StreakResult(current_streak=5, longest_streak=10, last_workout_date=TODAY)
    assert "current=5" in repr(r)
    assert "longest=10" in repr(r)
