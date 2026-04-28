"""Tests for gainz_tracker.pr_streak module."""

import pytest
from datetime import date

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.pr_streak import (
    PRStreakResult,
    _weekly_maxes,
    compute_pr_streaks,
)


def make_entry(exercise: str, d: date, weight: float, reps: int = 5) -> WorkoutEntry:
    return WorkoutEntry(date=d, exercise=exercise, sets=3, reps=reps, weight=weight)


@pytest.fixture
def squat_entries():
    """Three consecutive weeks of improving squats."""
    return [
        make_entry("Squat", date(2024, 1, 1), 100.0),  # week 1
        make_entry("Squat", date(2024, 1, 8), 105.0),  # week 2
        make_entry("Squat", date(2024, 1, 15), 110.0), # week 3
    ]


@pytest.fixture
def broken_streak_entries():
    """Streak broken by a drop in weight."""
    return [
        make_entry("Bench", date(2024, 1, 1), 80.0),
        make_entry("Bench", date(2024, 1, 8), 85.0),
        make_entry("Bench", date(2024, 1, 15), 82.0),  # drop — streak resets
        make_entry("Bench", date(2024, 1, 22), 90.0),  # new PR, streak = 1
    ]


def test_weekly_maxes_single_entry():
    entries = [make_entry("Squat", date(2024, 1, 3), 100.0)]
    result = _weekly_maxes(entries)
    assert date(2024, 1, 1) in result
    assert result[date(2024, 1, 1)] == 100.0


def test_weekly_maxes_picks_max_within_week():
    entries = [
        make_entry("Squat", date(2024, 1, 1), 90.0),
        make_entry("Squat", date(2024, 1, 3), 100.0),
        make_entry("Squat", date(2024, 1, 5), 95.0),
    ]
    result = _weekly_maxes(entries)
    assert len(result) == 1
    assert result[date(2024, 1, 1)] == 100.0


def test_compute_pr_streaks_returns_dict(squat_entries):
    result = compute_pr_streaks(squat_entries)
    assert isinstance(result, dict)
    assert "squat" in result


def test_compute_pr_streaks_current_streak(squat_entries):
    result = compute_pr_streaks(squat_entries)
    assert result["squat"].current_streak == 3


def test_compute_pr_streaks_best_streak(squat_entries):
    result = compute_pr_streaks(squat_entries)
    assert result["squat"].best_streak == 3


def test_compute_pr_streaks_last_pr_weight(squat_entries):
    result = compute_pr_streaks(squat_entries)
    assert result["squat"].last_pr_weight == 110.0


def test_compute_pr_streaks_broken_streak(broken_streak_entries):
    result = compute_pr_streaks(broken_streak_entries)
    bench = result["bench"]
    assert bench.current_streak == 1
    assert bench.best_streak == 2


def test_compute_pr_streaks_empty():
    result = compute_pr_streaks([])
    assert result == {}


def test_compute_pr_streaks_case_insensitive():
    entries = [
        make_entry("SQUAT", date(2024, 1, 1), 100.0),
        make_entry("squat", date(2024, 1, 8), 110.0),
    ]
    result = compute_pr_streaks(entries)
    assert "squat" in result
    assert result["squat"].current_streak == 2


def test_pr_streak_result_repr():
    r = PRStreakResult(
        exercise="squat",
        current_streak=3,
        best_streak=3,
        last_pr_date=date(2024, 1, 15),
        last_pr_weight=110.0,
    )
    assert "squat" in repr(r)
    assert "110.0" in repr(r)
