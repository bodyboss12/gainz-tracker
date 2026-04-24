"""Tests for gainz_tracker/exporter.py"""

import json
import csv
from io import StringIO

import pytest

from gainz_tracker.stats import ExerciseStats
from gainz_tracker.exporter import (
    export_stats_to_json,
    export_stats_to_csv,
    export_prs_to_json,
    export_prs_to_csv,
)


@pytest.fixture
def sample_stats():
    return {
        "Squat": ExerciseStats(
            exercise="Squat",
            total_sets=6,
            total_reps=30,
            max_weight=140.0,
            avg_weight=120.0,
            sessions=2,
        ),
        "Bench Press": ExerciseStats(
            exercise="Bench Press",
            total_sets=3,
            total_reps=15,
            max_weight=90.0,
            avg_weight=85.0,
            sessions=1,
        ),
    }


@pytest.fixture
def sample_prs():
    return {"Squat": 140.0, "Bench Press": 90.0}


def test_export_stats_to_json_valid_json(sample_stats):
    result = export_stats_to_json(sample_stats)
    parsed = json.loads(result)
    assert "Squat" in parsed
    assert "Bench Press" in parsed


def test_export_stats_to_json_fields(sample_stats):
    result = json.loads(export_stats_to_json(sample_stats))
    squat = result["Squat"]
    assert squat["total_sets"] == 6
    assert squat["total_reps"] == 30
    assert squat["max_weight"] == 140.0
    assert squat["avg_weight"] == 120.0
    assert squat["sessions"] == 2


def test_export_stats_to_json_empty():
    result = export_stats_to_json({})
    assert json.loads(result) == {}


def test_export_stats_to_csv_has_header(sample_stats):
    result = export_stats_to_csv(sample_stats)
    assert "exercise" in result
    assert "total_sets" in result
    assert "max_weight" in result


def test_export_stats_to_csv_row_count(sample_stats):
    result = export_stats_to_csv(sample_stats)
    reader = csv.DictReader(StringIO(result))
    rows = list(reader)
    assert len(rows) == 2


def test_export_stats_to_csv_values(sample_stats):
    result = export_stats_to_csv(sample_stats)
    reader = csv.DictReader(StringIO(result))
    rows = {r["exercise"]: r for r in reader}
    assert rows["Squat"]["max_weight"] == "140.0"
    assert rows["Bench Press"]["sessions"] == "1"


def test_export_prs_to_json(sample_prs):
    result = json.loads(export_prs_to_json(sample_prs))
    assert result["Squat"] == 140.0
    assert result["Bench Press"] == 90.0


def test_export_prs_to_csv(sample_prs):
    result = export_prs_to_csv(sample_prs)
    reader = csv.DictReader(StringIO(result))
    rows = {r["exercise"]: r for r in reader}
    assert rows["Squat"]["max_weight"] == "140.0"
    assert "Bench Press" in rows
