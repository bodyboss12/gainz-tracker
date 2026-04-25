import pytest
from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.muscle_group import (
    resolve_muscle_group,
    group_by_muscle,
    MuscleGroupSummary,
)


def make_entry(exercise, sets=3, reps=10, weight=100.0, date="2024-01-01"):
    return WorkoutEntry(date=date, exercise=exercise, sets=sets, reps=reps, weight=weight)


@pytest.fixture
def mixed_entries():
    return [
        make_entry("Squat", sets=3, reps=5, weight=120.0),
        make_entry("Bench Press", sets=4, reps=8, weight=80.0),
        make_entry("Deadlift", sets=3, reps=5, weight=150.0),
        make_entry("Squat", sets=3, reps=5, weight=125.0),
        make_entry("Bicep Curl", sets=3, reps=12, weight=20.0),
    ]


def test_resolve_known_exercise():
    assert resolve_muscle_group("squat") == "legs"
    assert resolve_muscle_group("bench press") == "chest"
    assert resolve_muscle_group("deadlift") == "back"


def test_resolve_case_insensitive():
    assert resolve_muscle_group("Squat") == "legs"
    assert resolve_muscle_group("BENCH PRESS") == "chest"


def test_resolve_unknown_exercise():
    assert resolve_muscle_group("burpee") == "other"
    assert resolve_muscle_group("jumping jacks") == "other"


def test_group_by_muscle_returns_dict(mixed_entries):
    result = group_by_muscle(mixed_entries)
    assert isinstance(result, dict)


def test_group_by_muscle_keys(mixed_entries):
    result = group_by_muscle(mixed_entries)
    assert "legs" in result
    assert "chest" in result
    assert "back" in result
    assert "arms" in result


def test_group_by_muscle_volume(mixed_entries):
    result = group_by_muscle(mixed_entries)
    # legs: (3*5*120) + (3*5*125) = 1800 + 1875 = 3675
    assert result["legs"].total_volume == pytest.approx(3675.0)


def test_group_by_muscle_exercise_count(mixed_entries):
    result = group_by_muscle(mixed_entries)
    assert result["legs"].exercise_count == 2


def test_group_by_muscle_unique_exercises(mixed_entries):
    result = group_by_muscle(mixed_entries)
    # Squat appears twice but should only be listed once
    assert result["legs"].exercises == ["Squat"]


def test_group_by_muscle_empty():
    result = group_by_muscle([])
    assert result == {}


def test_muscle_group_summary_repr():
    summary = MuscleGroupSummary(
        muscle_group="legs",
        total_volume=3675.0,
        exercise_count=2,
        exercises=["Squat"],
    )
    assert "legs" in repr(summary)
    assert "3675" in repr(summary)
