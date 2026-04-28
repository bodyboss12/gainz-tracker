"""Tests for gainz_tracker/body_weight.py"""

import pytest
from datetime import date
from gainz_tracker.body_weight import (
    BodyWeightEntry,
    log_weight,
    compute_trend,
    filter_by_date_range,
)


@pytest.fixture
def sample_entries():
    return [
        BodyWeightEntry(date=date(2024, 1, 1), weight_kg=80.0),
        BodyWeightEntry(date=date(2024, 1, 8), weight_kg=79.5),
        BodyWeightEntry(date=date(2024, 1, 15), weight_kg=79.0),
        BodyWeightEntry(date=date(2024, 1, 22), weight_kg=78.5),
    ]


def test_compute_trend_empty():
    assert compute_trend([]) is None


def test_compute_trend_single_entry():
    entries = [BodyWeightEntry(date=date(2024, 1, 1), weight_kg=80.0)]
    trend = compute_trend(entries)
    assert trend is not None
    assert trend.start_weight == 80.0
    assert trend.end_weight == 80.0
    assert trend.change_kg == 0.0
    assert trend.num_entries == 1


def test_compute_trend_change(sample_entries):
    trend = compute_trend(sample_entries)
    assert trend.change_kg == -1.5


def test_compute_trend_min_max(sample_entries):
    trend = compute_trend(sample_entries)
    assert trend.min_weight == 78.5
    assert trend.max_weight == 80.0


def test_compute_trend_avg(sample_entries):
    trend = compute_trend(sample_entries)
    assert trend.avg_weight == pytest.approx(79.25, abs=0.01)


def test_compute_trend_num_entries(sample_entries):
    trend = compute_trend(sample_entries)
    assert trend.num_entries == 4


def test_log_weight_adds_new_entry(sample_entries):
    updated = log_weight(sample_entries, date(2024, 1, 29), 78.0)
    assert len(updated) == 5
    assert updated[-1].weight_kg == 78.0


def test_log_weight_replaces_existing(sample_entries):
    updated = log_weight(sample_entries, date(2024, 1, 1), 82.0)
    assert len(updated) == 4
    assert updated[0].weight_kg == 82.0


def test_log_weight_sorted_by_date(sample_entries):
    updated = log_weight(sample_entries, date(2024, 1, 5), 79.8)
    dates = [e.date for e in updated]
    assert dates == sorted(dates)


def test_filter_by_date_range_start(sample_entries):
    result = filter_by_date_range(sample_entries, start=date(2024, 1, 8))
    assert all(e.date >= date(2024, 1, 8) for e in result)
    assert len(result) == 3


def test_filter_by_date_range_end(sample_entries):
    result = filter_by_date_range(sample_entries, end=date(2024, 1, 8))
    assert all(e.date <= date(2024, 1, 8) for e in result)
    assert len(result) == 2


def test_filter_by_date_range_both(sample_entries):
    result = filter_by_date_range(
        sample_entries, start=date(2024, 1, 8), end=date(2024, 1, 15)
    )
    assert len(result) == 2


def test_filter_by_date_range_none(sample_entries):
    result = filter_by_date_range(sample_entries)
    assert len(result) == len(sample_entries)
