"""Tests for format_rest_analysis in gainz_tracker/formatter.py"""

import pytest

from gainz_tracker.rest_analyzer import RestAnalysis
from gainz_tracker.formatter import format_rest_analysis


@pytest.fixture
def sample_analysis():
    return {
        "squat": RestAnalysis(
            exercise="squat",
            avg_rest_days=3.0,
            min_rest_days=2,
            max_rest_days=7,
            overtraining_flags=0,
            undertraining_flags=1,
        ),
        "bench": RestAnalysis(
            exercise="bench",
            avg_rest_days=1.0,
            min_rest_days=1,
            max_rest_days=1,
            overtraining_flags=2,
            undertraining_flags=0,
        ),
    }


def test_format_rest_empty():
    result = format_rest_analysis({})
    assert "No rest analysis" in result


def test_format_rest_contains_exercise(sample_analysis):
    result = format_rest_analysis(sample_analysis)
    assert "squat" in result
    assert "bench" in result


def test_format_rest_header_present(sample_analysis):
    result = format_rest_analysis(sample_analysis)
    assert "Exercise" in result
    assert "Avg Rest" in result


def test_format_rest_shows_overtraining(sample_analysis):
    result = format_rest_analysis(sample_analysis)
    # bench has 2 overtraining flags
    lines = result.splitlines()
    bench_line = next(l for l in lines if "bench" in l)
    assert "2" in bench_line


def test_format_rest_shows_undertraining(sample_analysis):
    result = format_rest_analysis(sample_analysis)
    lines = result.splitlines()
    squat_line = next(l for l in lines if "squat" in l)
    assert "1" in squat_line


def test_format_rest_sorted_alphabetically(sample_analysis):
    result = format_rest_analysis(sample_analysis)
    lines = [l for l in result.splitlines() if l and not l.startswith("-") and "Exercise" not in l]
    names = [l.split()[0] for l in lines]
    assert names == sorted(names)
