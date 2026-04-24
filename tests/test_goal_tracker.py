"""Tests for gainz_tracker.goal_tracker module."""

import pytest
from gainz_tracker.goal_tracker import Goal, GoalResult, evaluate_goals, format_goal_results
from gainz_tracker.stats import ExerciseStats


@pytest.fixture
def sample_stats():
    return {
        "Squat": ExerciseStats(
            exercise="Squat",
            total_sessions=5,
            max_weight=120.0,
            avg_weight=100.0,
            max_reps=8,
        ),
        "Bench Press": ExerciseStats(
            exercise="Bench Press",
            total_sessions=3,
            max_weight=80.0,
            avg_weight=72.5,
            max_reps=5,
        ),
    }


@pytest.fixture
def sample_goals():
    return [
        Goal(exercise="Squat", target_weight=100.0),
        Goal(exercise="Bench Press", target_weight=90.0),
        Goal(exercise="Deadlift", target_weight=150.0),
    ]


def test_evaluate_goals_achieved(sample_stats, sample_goals):
    results = evaluate_goals(sample_goals, sample_stats)
    squat_result = next(r for r in results if r.goal.exercise == "Squat")
    assert squat_result.achieved is True
    assert squat_result.gap == 0.0


def test_evaluate_goals_not_achieved(sample_stats, sample_goals):
    results = evaluate_goals(sample_goals, sample_stats)
    bench_result = next(r for r in results if r.goal.exercise == "Bench Press")
    assert bench_result.achieved is False
    assert bench_result.gap == pytest.approx(10.0)


def test_evaluate_goals_missing_exercise(sample_stats, sample_goals):
    results = evaluate_goals(sample_goals, sample_stats)
    deadlift_result = next(r for r in results if r.goal.exercise == "Deadlift")
    assert deadlift_result.achieved is False
    assert deadlift_result.current_best == 0.0
    assert deadlift_result.gap == pytest.approx(150.0)


def test_evaluate_goals_empty_goals(sample_stats):
    results = evaluate_goals([], sample_stats)
    assert results == []


def test_evaluate_goals_empty_stats(sample_goals):
    results = evaluate_goals(sample_goals, {})
    for r in results:
        assert r.achieved is False
        assert r.current_best == 0.0


def test_evaluate_goals_case_insensitive(sample_stats):
    goals = [Goal(exercise="squat", target_weight=50.0)]
    results = evaluate_goals(goals, sample_stats)
    assert results[0].achieved is True


def test_format_goal_results_contains_exercise(sample_stats, sample_goals):
    results = evaluate_goals(sample_goals, sample_stats)
    output = format_goal_results(results)
    assert "Squat" in output
    assert "Bench Press" in output


def test_format_goal_results_achieved_marker(sample_stats):
    goals = [Goal(exercise="Squat", target_weight=100.0)]
    results = evaluate_goals(goals, sample_stats)
    output = format_goal_results(results)
    assert "Achieved" in output


def test_format_goal_results_empty():
    output = format_goal_results([])
    assert output == "No goals defined."


def test_goal_repr():
    g = Goal(exercise="Squat", target_weight=100.0, target_reps=3)
    assert "Squat" in repr(g)
    assert "100.0" in repr(g)


def test_goal_result_repr(sample_stats, sample_goals):
    results = evaluate_goals(sample_goals, sample_stats)
    for r in results:
        assert r.goal.exercise in repr(r)
