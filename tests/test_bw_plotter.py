"""Tests for gainz_tracker/bw_plotter.py"""

import pytest
from datetime import date
from gainz_tracker.body_weight import BodyWeightEntry
from gainz_tracker.bw_plotter import plot_weight_ascii


@pytest.fixture
def sample_entries():
    return [
        BodyWeightEntry(date=date(2024, 1, 1), weight_kg=80.0),
        BodyWeightEntry(date=date(2024, 1, 8), weight_kg=79.0),
        BodyWeightEntry(date=date(2024, 1, 15), weight_kg=78.5),
        BodyWeightEntry(date=date(2024, 1, 22), weight_kg=78.0),
    ]


def test_plot_empty_returns_message():
    result = plot_weight_ascii([])
    assert "No body weight data" in result


def test_plot_contains_asterisks(sample_entries):
    result = plot_weight_ascii(sample_entries)
    assert "*" in result


def test_plot_contains_date_labels(sample_entries):
    result = plot_weight_ascii(sample_entries)
    assert "2024-01-01" in result
    assert "2024-01-22" in result


def test_plot_has_correct_height(sample_entries):
    result = plot_weight_ascii(sample_entries, height=8)
    # height rows + x axis + date label = height + 2
    lines = result.split("\n")
    assert len(lines) == 8 + 2


def test_plot_single_entry():
    entries = [BodyWeightEntry(date=date(2024, 1, 1), weight_kg=75.0)]
    result = plot_weight_ascii(entries)
    assert "*" in result
    assert "75.0" in result


def test_plot_uniform_weights():
    entries = [
        BodyWeightEntry(date=date(2024, 1, d), weight_kg=80.0)
        for d in range(1, 6)
    ]
    result = plot_weight_ascii(entries)
    assert "*" in result
