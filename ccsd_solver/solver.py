def solve_ccsd(positions, atomic_numbers):
    """Deterministic placeholder for a future CCSD solver.

    This function defines the frozen public API for the package.
    It currently performs no computation and always returns zeros.

    Parameters
    ----------
    positions : sequence
        Atomic positions, e.g. [(x, y, z), ...].
    atomic_numbers : sequence
        Atomic numbers, e.g. [1, 8, ...].

    Returns
    -------
    dict
        Dictionary with exactly the keys 'correlation_energy' and
        'total_energy', both float values.
    """
    return {
        "correlation_energy": 0.0,
        "total_energy": 0.0,
    }
