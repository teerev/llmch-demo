from countdown.core import solve_numbers


def test_solver_finds_solution_simple():
    sols = solve_numbers([1, 2, 3], 7, max_solutions=10)
    assert sols, "Expected at least one solution"
    assert any(eval(expr) == 7 for expr in sols)


def test_solver_no_solution_case():
    sols = solve_numbers([1, 1], 3, max_solutions=10)
    assert sols == []


def test_solver_respects_max_solutions():
    # There are multiple ways to make 2 from [1,1,1,1] (e.g., (1+1), (1+1) with different pairings)
    sols = solve_numbers([1, 1, 1, 1], 2, max_solutions=1)
    assert len(sols) == 1
    assert eval(sols[0]) == 2
