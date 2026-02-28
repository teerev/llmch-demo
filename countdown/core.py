"""Core API contracts for the Countdown numbers game.

This module defines the core data model and function signatures.
Implementations are intentionally minimal per the work order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class GameState:
    numbers: List[int]
    target: int


def generate_game(seed: Optional[int] = None) -> GameState:
    """Generate a new game state.

    Args:
        seed: Optional seed for deterministic generation.

    Raises:
        NotImplementedError: Generation is not implemented yet.
    """
    raise NotImplementedError


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
