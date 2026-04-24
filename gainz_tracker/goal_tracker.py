"""Track user-defined goals against personal records and stats."""

from dataclasses import dataclass
from typing import Optional
from gainz_tracker.stats import ExerciseStats


@dataclass
class Goal:
    exercise: str
    target_weight: float
    target_reps: int = 1

    def __repr__(self) -> str:
        return (
            f"Goal(exercise={self.exercise!r}, "
            f"target_weight={self.target_weight}, "
            f"target_reps={self.target_reps})"
        )


@dataclass
class GoalResult:
    goal: Goal
    current_best: float
    achieved: bool
    gap: float  # how far off the target (0 if achieved)

    def __repr__(self) -> str:
        status = "ACHIEVED" if self.achieved else f"gap={self.gap:.1f}kg"
        return f"GoalResult({self.goal.exercise!r}, {status})"


def evaluate_goals(
    goals: list[Goal],
    stats: dict[str, ExerciseStats],
) -> list[GoalResult]:
    """Compare each goal against computed stats and return results."""
    results = []
    for goal in goals:
        exercise_key = goal.exercise.lower()
        matched = next(
            (v for k, v in stats.items() if k.lower() == exercise_key), None
        )
        if matched is None:
            current_best = 0.0
        else:
            current_best = matched.max_weight

        achieved = current_best >= goal.target_weight
        gap = max(0.0, goal.target_weight - current_best)
        results.append(
            GoalResult(
                goal=goal,
                current_best=current_best,
                achieved=achieved,
                gap=gap,
            )
        )
    return results


def format_goal_results(results: list[GoalResult]) -> str:
    """Return a human-readable summary of goal evaluation results."""
    if not results:
        return "No goals defined."

    lines = [f"{'Exercise':<20} {'Target':>8} {'Current':>8} {'Status':<12}"]
    lines.append("-" * 52)
    for r in results:
        status = "✓ Achieved" if r.achieved else f"↑ {r.gap:.1f}kg to go"
        lines.append(
            f"{r.goal.exercise:<20} {r.goal.target_weight:>8.1f} "
            f"{r.current_best:>8.1f} {status:<12}"
        )
    return "\n".join(lines)
