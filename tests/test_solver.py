from __future__ import annotations

import re
from collections import Counter

from countdown.solver import solve


def test_simple_solution() -> None:
    assert solve(3, [1, 2]) == ["(1+2)"]


def test_no_solution() -> None:
    assert solve(999, [1, 2]) == []


def test_solutions_valid() -> None:
    target = 6
    numbers = [1, 2, 3]
    sols = solve(target, numbers)

    # list is sorted
    assert sols == sorted(sols)

    # each expression evaluates to target and does not exceed input counts
    available = Counter(numbers)
    for expr in sols:
        # safe-ish eval: expressions contain only digits and operators/parentheses
        assert re.fullmatch(r"[0-9()+\-*/]+", expr)
        assert eval(expr) == target

        used_nums = [int(x) for x in re.findall(r"\d+", expr)]
        used = Counter(used_nums)
        for k, v in used.items():
            assert v <= available[k]
