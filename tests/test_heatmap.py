"""Tests for gainz_tracker/heatmap.py"""

import pytest
from datetime import date, datetime
from gainz_tracker.csv_loader import WorkoutEntry
from gainz_tracker.heatmap import compute_heatmap, render_heatmap, DAYS


def make_entry(d: date, exercise: str = "Squat") -> WorkoutEntry:
    return WorkoutEntry(
        date=datetime.combine(d, datetime.min.time()),
        exercise=exercise,
        sets=3,
        reps=5,
        weight_kg=100.0,
    )


@pytest.fixture
def monday_entries():
    # 2024-01-01 is a Monday
    return [
        make_entry(date(2024, 1, 1)),
        make_entry(date(2024, 1, 1), "Bench Press"),  # same day, should count once
        make_entry(date(2024, 1, 8)),  # next Monday
    ]


@pytest.fixture
def mixed_entries():
    return [
        make_entry(date(2024, 1, 1)),   # Mon
        make_entry(date(2024, 1, 2)),   # Tue
        make_entry(date(2024, 1, 3)),   # Wed
        make_entry(date(2024, 1, 6)),   # Sat
        make_entry(date(2024, 1, 6)),   # Sat again, same day
    ]


def test_compute_heatmap_empty():
    data = compute_heatmap([])
    assert data.total_sessions == 0
    assert data.max_count == 0
    assert all(data.day_counts[d] == 0 for d in DAYS)


def test_compute_heatmap_deduplicates_same_day(monday_entries):
    data = compute_heatmap(monday_entries)
    # Two entries on 2024-01-01 should count as one session
    assert data.day_counts["Mon"] == 2  # two Mondays
    assert data.total_sessions == 2


def test_compute_heatmap_all_days_present(mixed_entries):
    data = compute_heatmap(mixed_entries)
    assert set(data.day_counts.keys()) == set(DAYS)


def test_compute_heatmap_correct_counts(mixed_entries):
    data = compute_heatmap(mixed_entries)
    assert data.day_counts["Mon"] == 1
    assert data.day_counts["Tue"] == 1
    assert data.day_counts["Wed"] == 1
    assert data.day_counts["Sat"] == 1
    assert data.day_counts["Sun"] == 0


def test_compute_heatmap_total_sessions(mixed_entries):
    data = compute_heatmap(mixed_entries)
    assert data.total_sessions == 4  # 4 unique dates


def test_compute_heatmap_max_count(monday_entries):
    data = compute_heatmap(monday_entries)
    assert data.max_count == 2


def test_render_heatmap_empty():
    from gainz_tracker.heatmap import HeatmapData
    data = HeatmapData(day_counts={d: 0 for d in DAYS}, max_count=0, total_sessions=0)
    result = render_heatmap(data)
    assert "No workout data" in result


def test_render_heatmap_contains_all_days(mixed_entries):
    data = compute_heatmap(mixed_entries)
    result = render_heatmap(data)
    for day in DAYS:
        assert day in result


def test_render_heatmap_shows_total(mixed_entries):
    data = compute_heatmap(mixed_entries)
    result = render_heatmap(data)
    assert "Total sessions: 4" in result


def test_heatmap_repr(mixed_entries):
    data = compute_heatmap(mixed_entries)
    assert "HeatmapData" in repr(data)
    assert "total_sessions" in repr(data)
