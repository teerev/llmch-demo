from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Optional, Tuple


@dataclass(frozen=True)
class _Term:
    value: int
    expr: str


def solve_numbers(numbers, target):
    """Solve a Countdown numbers round.

    Search for an expression using each input number at most once with
    operations +, -, *, and /. Only allow division when divisible (a % b == 0),
    and only keep positive intermediate results (> 0).

    Returns:
      - None if no solution
      - otherwise an expression string that evaluates to target
    """
    nums = tuple(int(n) for n in numbers)
    tgt = int(target)

    # Filter out non-positive inputs (they can't be used under the
    # "positive intermediate results" rule anyway).
    nums = tuple(n for n in nums if n > 0)
    if not nums:
        return None

    # Represent state as a sorted tuple of (value, expr) pairs.
    start_state: Tuple[_Term, ...] = tuple(sorted((_Term(n, str(n)) for n in nums), key=lambda t: t.value))

    @lru_cache(maxsize=None)
    def _search(state: Tuple[Tuple[int, str], ...]) -> Optional[str]:
        # state is a sorted tuple of (value, expr)
        if len(state) == 1:
            v, e = state[0]
            return e if v == tgt else None

        # Quick check: if any term already equals target, we can return it.
        for v, e in state:
            if v == tgt:
                return e

        n = len(state)
        # Choose unordered pairs i<j
        for i in range(n):
            a_val, a_expr = state[i]
            for j in range(i + 1, n):
                b_val, b_expr = state[j]

                rest = list(state[:i] + state[i + 1 : j] + state[j + 1 :])

                def try_add(val: int, expr: str) -> Optional[str]:
                    if val <= 0:
                        return None
                    new_state = rest + [(val, expr)]
                    new_state.sort(key=lambda t: t[0])
                    return _search(tuple(new_state))

                # Addition (commutative)
                res = try_add(a_val + b_val, f"({a_expr}+{b_expr})")
                if res is not None:
                    return res

                # Multiplication (commutative)
                res = try_add(a_val * b_val, f"({a_expr}*{b_expr})")
                if res is not None:
                    return res

                # Subtraction (non-commutative) - keep positive only
                if a_val > b_val:
                    res = try_add(a_val - b_val, f"({a_expr}-{b_expr})")
                    if res is not None:
                        return res
                if b_val > a_val:
                    res = try_add(b_val - a_val, f"({b_expr}-{a_expr})")
                    if res is not None:
                        return res

                # Division (non-commutative) - integer only, positive only
                if b_val != 0 and a_val % b_val == 0:
                    q = a_val // b_val
                    if q > 0:
                        res = try_add(q, f"({a_expr}/{b_expr})")
                        if res is not None:
                            return res
                if a_val != 0 and b_val % a_val == 0:
                    q = b_val // a_val
                    if q > 0:
                        res = try_add(q, f"({b_expr}/{a_expr})")
                        if res is not None:
                            return res

        return None

    # Convert to cacheable primitive state
    primitive_state = tuple((t.value, t.expr) for t in start_state)
    return _search(primitive_state)
