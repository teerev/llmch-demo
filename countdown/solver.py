"""Solver implementation for the Countdown numbers game.

The solver searches for arithmetic expressions that evaluate exactly to a target
using any subset of the provided numbers (each number at most once).

Expressions are formatted without spaces and with explicit parentheses for every
binary operation, e.g. '(A+B)'.

The search is deterministic and returns a sorted list of unique expressions.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Set, Tuple


@dataclass(frozen=True)
class _Term:
    value: Fraction
    expr: str


def _combine(a: _Term, b: _Term) -> List[_Term]:
    """Return all results of combining a and b with allowed operations."""
    out: List[_Term] = []

    # Addition
    out.append(_Term(a.value + b.value, f"({a.expr}+{b.expr})"))

    # Subtraction (both orders)
    out.append(_Term(a.value - b.value, f"({a.expr}-{b.expr})"))
    out.append(_Term(b.value - a.value, f"({b.expr}-{a.expr})"))

    # Multiplication
    out.append(_Term(a.value * b.value, f"({a.expr}*{b.expr})"))

    # Exact division only when divisible to an integer result.
    # Use Fraction to avoid precision issues.
    if b.value != 0:
        q = a.value / b.value
        if q.denominator == 1:
            out.append(_Term(q, f"({a.expr}/{b.expr})"))
    if a.value != 0:
        q = b.value / a.value
        if q.denominator == 1:
            out.append(_Term(q, f"({b.expr}/{a.expr})"))

    return out


def solve(target: int, numbers: Sequence[int]) -> List[str]:
    """Return sorted unique expression strings that evaluate to `target`.

    The solver may use any subset of `numbers`, each at most once.
    """

    target_f = Fraction(target)
    initial: Tuple[_Term, ...] = tuple(_Term(Fraction(n), str(n)) for n in numbers)

    solutions: Set[str] = set()
    seen: Set[Tuple[Fraction, ...]] = set()

    def state_key(terms: Tuple[_Term, ...]) -> Tuple[Fraction, ...]:
        # Canonicalize by multiset of values only; expressions don't matter for pruning.
        return tuple(sorted((t.value for t in terms)))

    def search(terms: Tuple[_Term, ...]) -> None:
        # Any subset allowed: check current terms as potential solutions.
        for t in terms:
            if t.value == target_f:
                solutions.add(t.expr)

        key = state_key(terms)
        if key in seen:
            return
        seen.add(key)

        n = len(terms)
        if n < 2:
            return

        # Combine any pair.
        for i in range(n):
            for j in range(i + 1, n):
                a, b = terms[i], terms[j]
                rest = [terms[k] for k in range(n) if k not in (i, j)]
                for c in _combine(a, b):
                    search(tuple(rest + [c]))

    search(initial)
    return sorted(solutions)
