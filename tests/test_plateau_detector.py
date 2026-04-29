import pytest
from datetime import date, timedelta
from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.plateau_detector import (
    detect_plateaus,
    _weekly_maxes,
    _week_key,
    PlateauResult,
)


def make_entry(exercise: str, d: date, weight: float) -> WorkoutEntry:
    return WorkoutEntry(date=d, exercise=exercise, sets=3, reps=5, weight=weight)


# Monday of a known week
WEEK1 = date(2024, 1, 1)   # 2024-W01
WEEK2 = date(2024, 1, 8)   # 2024-W02
WEEK3 = date(2024, 1, 15)  # 2024-W03
WEEK4 = date(2024, 1, 22)  # 2024-W04


@pytest.fixture
def flat_squat_entries():
    return [
        make_entry("Squat", WEEK1, 100.0),
        make_entry("Squat", WEEK2, 100.0),
        make_entry("Squat", WEEK3, 100.0),
        make_entry("Squat", WEEK4, 100.0),
    ]


@pytest.fixture
def improving_bench_entries():
    return [
        make_entry("Bench", WEEK1, 60.0),
        make_entry("Bench", WEEK2, 65.0),
        make_entry("Bench", WEEK3, 70.0),
        make_entry("Bench", WEEK4, 75.0),
    ]


def test_detect_plateaus_empty():
    assert detect_plateaus([]) == {}


def test_detect_plateaus_returns_dict(flat_squat_entries):
    result = detect_plateaus(flat_squat_entries)
    assert isinstance(result, dict)
    assert "Squat" in result


def test_detect_plateaus_flat_is_plateau(flat_squat_entries):
    result = detect_plateaus(flat_squat_entries, min_weeks=3)
    assert result["Squat"].is_plateau is True


def test_detect_plateaus_improving_not_plateau(improving_bench_entries):
    result = detect_plateaus(improving_bench_entries, min_weeks=3)
    assert result["Bench"].is_plateau is False


def test_detect_plateaus_weeks_flat_count(flat_squat_entries):
    result = detect_plateaus(flat_squat_entries, min_weeks=3)
    assert result["Squat"].weeks_flat == 4


def test_detect_plateaus_max_weight(flat_squat_entries):
    result = detect_plateaus(flat_squat_entries)
    assert result["Squat"].max_weight == 100.0


def test_detect_plateaus_insufficient_weeks():
    entries = [
        make_entry("Squat", WEEK1, 100.0),
        make_entry("Squat", WEEK2, 100.0),
    ]
    result = detect_plateaus(entries, min_weeks=3)
    assert result["Squat"].is_plateau is False
    assert result["Squat"].weeks_flat == 0


def test_detect_plateaus_tolerance(improving_bench_entries):
    # small increments within tolerance should be treated as flat
    entries = [
        make_entry("Bench", WEEK1, 100.0),
        make_entry("Bench", WEEK2, 100.5),
        make_entry("Bench", WEEK3, 100.2),
        make_entry("Bench", WEEK4, 100.8),
    ]
    result = detect_plateaus(entries, min_weeks=3, tolerance=1.0)
    assert result["Bench"].is_plateau is True


def test_weekly_maxes_picks_max():
    entries = [
        make_entry("Squat", WEEK1, 80.0),
        make_entry("Squat", WEEK1 + timedelta(days=2), 90.0),
    ]
    maxes = _weekly_maxes(entries)
    assert len(maxes) == 1
    assert list(maxes.values())[0] == 90.0


def test_weekly_maxes_sorted():
    entries = [
        make_entry("Squat", WEEK3, 90.0),
        make_entry("Squat", WEEK1, 80.0),
        make_entry("Squat", WEEK2, 85.0),
    ]
    maxes = _weekly_maxes(entries)
    keys = list(maxes.keys())
    assert keys == sorted(keys)


def test_week_key_format():
    d = date(2024, 1, 1)
    key = _week_key(d)
    assert key.startswith("2024-W")


def test_plateau_result_repr():
    pr = PlateauResult(exercise="Squat", weeks_flat=4, max_weight=100.0, is_plateau=True)
    assert "PLATEAU" in repr(pr)
    assert "Squat" in repr(pr)
