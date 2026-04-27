"""Tests for gainz_tracker/notes.py"""

import pytest
from datetime import date
from gainz_tracker.notes import (
    WorkoutNote,
    attach_note,
    get_notes_for_exercise,
    get_notes_for_date,
    notes_summary,
    find_note,
)


@pytest.fixture
def sample_notes():
    return [
        WorkoutNote(date(2024, 1, 10), "Squat", "Felt strong today"),
        WorkoutNote(date(2024, 1, 12), "Bench Press", "Left shoulder tight"),
        WorkoutNote(date(2024, 1, 14), "Squat", "New PR attempt"),
        WorkoutNote(date(2024, 1, 14), "Deadlift", "Form breakdown at top"),
    ]


def test_attach_note_adds_new(sample_notes):
    updated = attach_note(sample_notes, date(2024, 1, 20), "OHP", "Strict form")
    assert any(n.exercise == "OHP" for n in updated)
    assert len(updated) == len(sample_notes) + 1


def test_attach_note_replaces_existing(sample_notes):
    updated = attach_note(sample_notes, date(2024, 1, 10), "Squat", "Updated note")
    squat_jan10 = [n for n in updated if n.workout_date == date(2024, 1, 10) and n.exercise == "Squat"]
    assert len(squat_jan10) == 1
    assert squat_jan10[0].note == "Updated note"


def test_attach_note_case_insensitive_replace(sample_notes):
    updated = attach_note(sample_notes, date(2024, 1, 10), "squat", "lowercase key")
    squat_jan10 = [n for n in updated if n.workout_date == date(2024, 1, 10)]
    assert len(squat_jan10) == 1


def test_get_notes_for_exercise_returns_sorted(sample_notes):
    result = get_notes_for_exercise(sample_notes, "Squat")
    assert len(result) == 2
    assert result[0].workout_date < result[1].workout_date


def test_get_notes_for_exercise_case_insensitive(sample_notes):
    result = get_notes_for_exercise(sample_notes, "bench press")
    assert len(result) == 1
    assert result[0].exercise == "Bench Press"


def test_get_notes_for_exercise_missing(sample_notes):
    result = get_notes_for_exercise(sample_notes, "Leg Press")
    assert result == []


def test_get_notes_for_date(sample_notes):
    result = get_notes_for_date(sample_notes, date(2024, 1, 14))
    assert len(result) == 2
    exercises = {n.exercise for n in result}
    assert "Squat" in exercises
    assert "Deadlift" in exercises


def test_get_notes_for_date_empty(sample_notes):
    result = get_notes_for_date(sample_notes, date(2024, 1, 1))
    assert result == []


def test_notes_summary(sample_notes):
    summary = notes_summary(sample_notes)
    assert summary["squat"] == 2
    assert summary["bench press"] == 1
    assert summary["deadlift"] == 1


def test_notes_summary_empty():
    assert notes_summary([]) == {}


def test_find_note_found(sample_notes):
    result = find_note(sample_notes, date(2024, 1, 12), "Bench Press")
    assert result is not None
    assert result.note == "Left shoulder tight"


def test_find_note_not_found(sample_notes):
    result = find_note(sample_notes, date(2024, 1, 12), "Squat")
    assert result is None


def test_workout_note_repr():
    n = WorkoutNote(date(2024, 1, 10), "Squat", "Good session")
    assert "Squat" in repr(n)
    assert "2024-01-10" in repr(n)
