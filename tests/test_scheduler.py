import pytest
from datetime import date, timedelta
from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.scheduler import (
    WorkoutSchedule,
    _last_workout_date,
    recommend_schedule,
)

REF_DATE = date(2024, 6, 10)


@pytest.fixture
def sample_entries():
    return [
        WorkoutEntry(date=date(2024, 6, 7), exercise="Squat", sets=3, reps=5, weight=100.0),
        WorkoutEntry(date=date(2024, 6, 5), exercise="Squat", sets=3, reps=5, weight=95.0),
        WorkoutEntry(date=date(2024, 6, 8), exercise="Bench Press", sets=4, reps=8, weight=80.0),
        WorkoutEntry(date=date(2024, 6, 3), exercise="Deadlift", sets=1, reps=5, weight=140.0),
    ]


def test_last_workout_date_returns_max(sample_entries):
    result = _last_workout_date(sample_entries, "Squat")
    assert result == date(2024, 6, 7)


def test_last_workout_date_case_insensitive(sample_entries):
    result = _last_workout_date(sample_entries, "squat")
    assert result == date(2024, 6, 7)


def test_last_workout_date_missing_exercise(sample_entries):
    result = _last_workout_date(sample_entries, "Pull Up")
    assert result is None


def test_recommend_schedule_returns_list(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    assert isinstance(result, list)
    assert all(isinstance(s, WorkoutSchedule) for s in result)


def test_recommend_schedule_exercise_count(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    exercises = {s.exercise for s in result}
    assert exercises == {"Squat", "Bench Press", "Deadlift"}


def test_recommend_schedule_sorted_by_date(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    dates = [s.recommended_date for s in result]
    assert dates == sorted(dates)


def test_recommend_schedule_correct_recommended_date(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    squat = next(s for s in result if s.exercise == "Squat")
    assert squat.recommended_date == date(2024, 6, 10)


def test_recommend_schedule_overdue(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    deadlift = next(s for s in result if s.exercise == "Deadlift")
    # last: June 3, recommended: June 6, as_of: June 10 => overdue by 4
    assert deadlift.overdue_by == 4


def test_recommend_schedule_not_overdue(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    bench = next(s for s in result if s.exercise == "Bench Press")
    # last: June 8, recommended: June 11, as_of: June 10 => not overdue
    assert bench.overdue_by == 0


def test_recommend_schedule_empty():
    result = recommend_schedule([], frequency_days=3, as_of=REF_DATE)
    assert result == []


def test_workout_schedule_repr(sample_entries):
    result = recommend_schedule(sample_entries, frequency_days=3, as_of=REF_DATE)
    squat = next(s for s in result if s.exercise == "Squat")
    r = repr(squat)
    assert "Squat" in r
    assert "overdue_by" in r
