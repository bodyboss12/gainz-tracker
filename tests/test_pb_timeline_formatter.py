"""Tests for pb_timeline_formatter module."""

from datetime import date

import pytest

from gainz_tracker.personal_best_timeline import PBTimelineEntry
from gainz_tracker.pb_timeline_formatter import format_pb_timeline, format_pb_gaps


@pytest.fixture
def single_exercise_timeline():
    return {
        "squat": [
            PBTimelineEntry("Squat", date(2024, 1, 1), 100.0, None),
            PBTimelineEntry("Squat", date(2024, 1, 8), 105.0, 100.0),
            PBTimelineEntry("Squat", date(2024, 1, 15), 110.0, 105.0),
        ]
    }


@pytest.fixture
def multi_exercise_timeline(single_exercise_timeline):
    single_exercise_timeline["bench"] = [
        PBTimelineEntry("Bench", date(2024, 1, 2), 60.0, None),
        PBTimelineEntry("Bench", date(2024, 1, 9), 65.0, 60.0),
    ]
    return single_exercise_timeline


def test_format_pb_timeline_empty():
    result = format_pb_timeline({})
    assert "No personal best" in result


def test_format_pb_timeline_contains_header(single_exercise_timeline):
    result = format_pb_timeline(single_exercise_timeline)
    assert "Personal Best Timeline" in result


def test_format_pb_timeline_contains_exercise(single_exercise_timeline):
    result = format_pb_timeline(single_exercise_timeline)
    assert "Squat" in result


def test_format_pb_timeline_contains_weights(single_exercise_timeline):
    result = format_pb_timeline(single_exercise_timeline)
    assert "100.0" in result
    assert "105.0" in result
    assert "110.0" in result


def test_format_pb_timeline_first_entry_shows_first(single_exercise_timeline):
    result = format_pb_timeline(single_exercise_timeline)
    assert "first" in result


def test_format_pb_timeline_gain_shown(single_exercise_timeline):
    result = format_pb_timeline(single_exercise_timeline)
    assert "+5.0" in result


def test_format_pb_timeline_multiple_exercises(multi_exercise_timeline):
    result = format_pb_timeline(multi_exercise_timeline)
    assert "Squat" in result
    assert "Bench" in result


def test_format_pb_gaps_empty():
    result = format_pb_gaps({})
    assert "No timeline" in result


def test_format_pb_gaps_contains_exercise(single_exercise_timeline):
    result = format_pb_gaps(single_exercise_timeline)
    assert "squat" in result.lower()


def test_format_pb_gaps_shows_avg_days(single_exercise_timeline):
    result = format_pb_gaps(single_exercise_timeline)
    # 7 days between each PB, avg = 7.0
    assert "7.0" in result


def test_format_pb_gaps_shows_total_prs(single_exercise_timeline):
    result = format_pb_gaps(single_exercise_timeline)
    assert "3" in result
