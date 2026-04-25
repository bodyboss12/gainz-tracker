"""Tests for gainz_tracker.volume_tracker module."""

import pytest
from datetime import date
from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.volume_tracker import compute_volume, volume_over_time


@pytest.fixture
def sample_entries():
    return [
        WorkoutEntry(date="2024-01-01", exercise="Squat", sets=3, reps=5, weight=100.0),
        WorkoutEntry(date="2024-01-03", exercise="Squat", sets=4, reps=5, weight=110.0),
        WorkoutEntry(date="2024-01-02", exercise="Bench", sets=3, reps=8, weight=80.0),
        WorkoutEntry(date="2024-01-04", exercise="Bench", sets=3, reps=8, weight=85.0),
    ]


def test_compute_volume_returns_dict(sample_entries):
    result = compute_volume(sample_entries)
    assert isinstance(result, dict)


def test_compute_volume_keys(sample_entries):
    result = compute_volume(sample_entries)
    assert "Squat" in result
    assert "Bench" in result


def test_compute_volume_squat_total(sample_entries):
    result = compute_volume(sample_entries)
    # 3*5*100 + 4*5*110 = 1500 + 2200 = 3700
    assert result["Squat"].total_volume == pytest.approx(3700.0)


def test_compute_volume_bench_total(sample_entries):
    result = compute_volume(sample_entries)
    # 3*8*80 + 3*8*85 = 1920 + 2040 = 3960
    assert result["Bench"].total_volume == pytest.approx(3960.0)


def test_compute_volume_session_count(sample_entries):
    result = compute_volume(sample_entries)
    assert result["Squat"].session_count == 2
    assert result["Bench"].session_count == 2


def test_compute_volume_avg_per_session(sample_entries):
    result = compute_volume(sample_entries)
    assert result["Squat"].avg_volume_per_session == pytest.approx(3700.0 / 2)


def test_compute_volume_empty():
    result = compute_volume([])
    assert result == {}


def test_volume_over_time_returns_sorted(sample_entries):
    result = volume_over_time(sample_entries, "Squat")
    dates = list(result.keys())
    assert dates == sorted(dates)


def test_volume_over_time_correct_values(sample_entries):
    result = volume_over_time(sample_entries, "Squat")
    assert result["2024-01-01"] == pytest.approx(1500.0)
    assert result["2024-01-03"] == pytest.approx(2200.0)


def test_volume_over_time_case_insensitive(sample_entries):
    result_lower = volume_over_time(sample_entries, "squat")
    result_upper = volume_over_time(sample_entries, "SQUAT")
    assert result_lower == result_upper


def test_volume_over_time_missing_exercise(sample_entries):
    result = volume_over_time(sample_entries, "Deadlift")
    assert result == {}
