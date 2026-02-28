"""Core API contracts for the Countdown numbers game.

This module defines the core data model and function signatures.
Implementations are intentionally minimal per the work order.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Optional, Tuple


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

    Brute-force recursive search combining pairs of numbers using +, -, *, and /
    (division only when divisible). Only positive integer intermediate results
    are allowed.

    Expressions are returned as fully parenthesized strings like '(a+b)'.

    For + and * only one ordering is used; for - and / both orders are included.

    Args:
        numbers: Available numbers.
        target: Target value.
        max_solutions: Maximum number of solutions to return.

    Returns:
        A list of expression strings.
    """

    if max_solutions <= 0:
        return []

    # Work with (value, expr) pairs.
    items: List[Tuple[int, str]] = [(n, str(n)) for n in numbers]
    solutions: List[str] = []

    def search(current: List[Tuple[int, str]]) -> None:
        nonlocal solutions
        if len(solutions) >= max_solutions:
            return

        # If any current value matches target, record it.
        for v, e in current:
            if v == target:
                solutions.append(e)
                if len(solutions) >= max_solutions:
                    return

        if len(current) < 2:
            return

        n = len(current)
        for i in range(n):
            if len(solutions) >= max_solutions:
                return
            for j in range(i + 1, n):
                if len(solutions) >= max_solutions:
                    return

                a_val, a_expr = current[i]
                b_val, b_expr = current[j]

                rest = [current[k] for k in range(n) if k not in (i, j)]

                candidates: List[Tuple[int, str]] = []

                # + (one ordering)
                candidates.append((a_val + b_val, f"({a_expr}+{b_expr})"))

                # * (one ordering)
                candidates.append((a_val * b_val, f"({a_expr}*{b_expr})"))

                # - (both orders), only positive
                if a_val - b_val > 0:
                    candidates.append((a_val - b_val, f"({a_expr}-{b_expr})"))
                if b_val - a_val > 0:
                    candidates.append((b_val - a_val, f"({b_expr}-{a_expr})"))

                # / (both orders), only divisible and positive
                if b_val != 0 and a_val % b_val == 0:
                    q = a_val // b_val
                    if q > 0:
                        candidates.append((q, f"({a_expr}/{b_expr})"))
                if a_val != 0 and b_val % a_val == 0:
                    q = b_val // a_val
                    if q > 0:
                        candidates.append((q, f"({b_expr}/{a_expr})"))

                for new_val, new_expr in candidates:
                    if len(solutions) >= max_solutions:
                        return
                    if new_val <= 0:
                        continue
                    search(rest + [(new_val, new_expr)])

    search(items)
    return solutions


def solve_game(state: GameState, max_solutions: int = 1) -> List[object]:
    """Solve a game state by delegating to :func:`solve_numbers`."""
    return solve_numbers(state.numbers, state.target, max_solutions=max_solutions)
