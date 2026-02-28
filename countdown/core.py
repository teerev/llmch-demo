"""Core API contracts for the Countdown numbers game.

This module defines the core data model and function signatures.
Implementations are intentionally minimal per the work order.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Optional


# Multiset: 1-10 twice each, plus 25, 50, 75, 100
NUMBER_POOL: List[int] = [
    1,
    1,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
    8,
    8,
    9,
    9,
    10,
    10,
    25,
    50,
    75,
    100,
]


@dataclass(frozen=True)
class GameState:
    numbers: List[int]
    target: int


def generate_game(seed: Optional[int] = None) -> GameState:
    """Generate a new game state.

    Args:
        seed: Optional seed for deterministic generation.

    Returns:
        A deterministically generated :class:`GameState` when seed is provided.
    """
    rng = random.Random(seed)
    numbers = rng.sample(NUMBER_POOL, 6)
    target = rng.randint(100, 999)
    return GameState(numbers, target)


def solve_numbers(numbers: List[int], target: int, max_solutions: int = 1) -> List[object]:
    """Solve a Countdown numbers instance.

    This is a placeholder contract; it currently returns no solutions.

    Args:
        numbers: Available numbers.
        target: Target value.
        max_solutions: Maximum number of solutions to return.

    Returns:
        A list of solutions (currently empty).
    """
    return []


def solve_game(state: GameState, max_solutions: int = 1) -> List[object]:
    """Solve a game state by delegating to :func:`solve_numbers`."""
    return solve_numbers(state.numbers, state.target, max_solutions=max_solutions)
