"""Tests for gainz_tracker.consistency_score."""

import pytest
from datetime import date

from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.consistency_score import (
    compute_consistency,
    ConsistencyScore,
    _grade,
)


def make_entry(exercise: str, d: date, weight: float = 100.0, reps: int = 5) -> WorkoutEntry:
    return WorkoutEntry(date=d, exercise=exercise, weight=weight, reps=reps)


@pytest.fixture
def squat_entries():
    # 3 active days out of a 7-day window
    return [
        make_entry("Squat", date(2024, 1, 1)),
        make_entry("Squat", date(2024, 1, 4)),
        make_entry("Squat", date(2024, 1, 7)),
    ]


@pytest.fixture
def mixed_entries():
    return [
        make_entry("Squat", date(2024, 1, 1)),
        make_entry("Squat", date(2024, 1, 2)),
        make_entry("Bench", date(2024, 1, 1)),
        make_entry("Bench", date(2024, 1, 3)),
        make_entry("Squat", date(2024, 1, 5)),
    ]


def test_compute_consistency_empty():
    assert compute_consistency([]) == {}


def test_compute_consistency_returns_dict(squat_entries):
    result = compute_consistency(squat_entries)
    assert isinstance(result, dict)


def test_compute_consistency_keys_lowercase(squat_entries):
    result = compute_consistency(squat_entries)
    assert "squat" in result


def test_compute_consistency_score_is_float(squat_entries):
    result = compute_consistency(squat_entries)
    assert isinstance(result["squat"].score, float)


def test_compute_consistency_score_range(squat_entries):
    result = compute_consistency(squat_entries)
    score = result["squat"].score
    assert 0.0 <= score <= 1.0


def test_compute_consistency_squat_active_days(squat_entries):
    # 3 unique active days
    result = compute_consistency(squat_entries)
    assert result["squat"].active_days == 3


def test_compute_consistency_squat_total_days(squat_entries):
    # date range: Jan 1 to Jan 7 = 7 days
    result = compute_consistency(squat_entries)
    assert result["squat"].total_days == 7


def test_compute_consistency_squat_score_value(squat_entries):
    result = compute_consistency(squat_entries)
    # 3/7 ≈ 0.4286
    assert abs(result["squat"].score - round(3 / 7, 4)) < 1e-6


def test_compute_consistency_mixed_exercises(mixed_entries):
    result = compute_consistency(mixed_entries)
    assert "squat" in result
    assert "bench" in result


def test_compute_consistency_deduplicates_same_day():
    entries = [
        make_entry("Squat", date(2024, 1, 1)),
        make_entry("Squat", date(2024, 1, 1)),  # duplicate date
        make_entry("Squat", date(2024, 1, 2)),
    ]
    result = compute_consistency(entries)
    assert result["squat"].active_days == 2


def test_compute_consistency_single_entry():
    entries = [make_entry("Deadlift", date(2024, 3, 10))]
    result = compute_consistency(entries)
    assert result["deadlift"].score == 1.0
    assert result["deadlift"].total_days == 1


def test_grade_a():
    assert _grade(0.85) == "A"


def test_grade_b():
    assert _grade(0.65) == "B"


def test_grade_f():
    assert _grade(0.1) == "F"


def test_consistency_score_repr(squat_entries):
    result = compute_consistency(squat_entries)
    r = repr(result["squat"])
    assert "squat" in r
    assert "score" in r
