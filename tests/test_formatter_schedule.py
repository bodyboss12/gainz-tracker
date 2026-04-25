import pytest
from datetime import date
from gainz_tracker.scheduler import WorkoutSchedule
from gainz_tracker.formatter import format_schedule


@pytest.fixture
def sample_schedules():
    return [
        WorkoutSchedule(
            exercise="Bench Press",
            recommended_date=date(2024, 6, 11),
            days_since_last=3,
            overdue_by=0,
        ),
        WorkoutSchedule(
            exercise="Deadlift",
            recommended_date=date(2024, 6, 6),
            days_since_last=7,
            overdue_by=4,
        ),
        WorkoutSchedule(
            exercise="Squat",
            recommended_date=date(2024, 6, 10),
            days_since_last=3,
            overdue_by=0,
        ),
    ]


def test_format_schedule_contains_exercise(sample_schedules):
    output = format_schedule(sample_schedules)
    assert "Bench Press" in output
    assert "Deadlift" in output
    assert "Squat" in output


def test_format_schedule_header(sample_schedules):
    output = format_schedule(sample_schedules)
    assert "Exercise" in output
    assert "Next Session" in output
    assert "Overdue By" in output


def test_format_schedule_overdue_shown(sample_schedules):
    output = format_schedule(sample_schedules)
    assert "4d" in output


def test_format_schedule_not_overdue_dash(sample_schedules):
    output = format_schedule(sample_schedules)
    lines = output.split("\n")
    bench_line = next(l for l in lines if "Bench Press" in l)
    assert "-" in bench_line


def test_format_schedule_empty():
    output = format_schedule([])
    assert "No schedule" in output


def test_format_schedule_date_visible(sample_schedules):
    output = format_schedule(sample_schedules)
    assert "2024-06-11" in output
    assert "2024-06-06" in output
