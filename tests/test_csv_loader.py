"""Tests for the CSV loader module."""

import pytest
from pathlib import Path
from datetime import datetime

from gainz_tracker.csv_loader import load_csv, WorkoutEntry


SAMPLE_CSV = """date,exercise,sets,reps,weight_kg,notes
2024-01-15,Squat,3,5,100.0,felt strong
2024-01-15,Bench Press,3,8,80.0,
2024-01-17,Deadlift,1,5,140.0,PR!
"""

MISSING_COLS_CSV = """date,exercise,sets
2024-01-15,Squat,3
"""

BAD_ROW_CSV = """date,exercise,sets,reps,weight_kg
2024-01-15,Squat,three,5,100.0
"""


@pytest.fixture
def sample_csv_file(tmp_path: Path) -> Path:
    f = tmp_path / "workouts.csv"
    f.write_text(SAMPLE_CSV)
    return f


@pytest.fixture
def missing_cols_file(tmp_path: Path) -> Path:
    f = tmp_path / "bad.csv"
    f.write_text(MISSING_COLS_CSV)
    return f


@pytest.fixture
def bad_row_file(tmp_path: Path) -> Path:
    f = tmp_path / "bad_row.csv"
    f.write_text(BAD_ROW_CSV)
    return f


def test_load_csv_returns_entries(sample_csv_file):
    entries = load_csv(sample_csv_file)
    assert len(entries) == 3
    assert all(isinstance(e, WorkoutEntry) for e in entries)


def test_load_csv_parses_fields_correctly(sample_csv_file):
    entries = load_csv(sample_csv_file)
    first = entries[0]
    assert first.date == datetime(2024, 1, 15)
    assert first.exercise == "Squat"
    assert first.sets == 3
    assert first.reps == 5
    assert first.weight_kg == 100.0
    assert first.notes == "felt strong"


def test_load_csv_none_for_empty_notes(sample_csv_file):
    entries = load_csv(sample_csv_file)
    assert entries[1].notes is None


def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("/nonexistent/path/workouts.csv")


def test_load_csv_wrong_extension(tmp_path):
    f = tmp_path / "workouts.txt"
    f.write_text(SAMPLE_CSV)
    with pytest.raises(ValueError, match="Expected a .csv file"):
        load_csv(f)


def test_load_csv_missing_required_columns(missing_cols_file):
    with pytest.raises(ValueError, match="missing required columns"):
        load_csv(missing_cols_file)


def test_load_csv_bad_row_raises(bad_row_file):
    with pytest.raises(ValueError, match="Error parsing row"):
        load_csv(bad_row_file)
