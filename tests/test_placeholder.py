from ccsd_solver import solve_ccsd


def test_solve_ccsd_placeholder_is_deterministic():
    result = solve_ccsd(positions=[(0.0, 0.0, 0.0)], atomic_numbers=[1])

    assert set(result.keys()) == {"correlation_energy", "total_energy"}
    assert result["correlation_energy"] == 0.0
    assert result["total_energy"] == 0.0
