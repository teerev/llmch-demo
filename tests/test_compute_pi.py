import pytest

from pi_calc import compute_pi


@pytest.mark.parametrize(
    "digits,expected",
    [
        (1, "3"),
        (2, "3.1"),
        (5, "3.1416"),
        (10, "3.141592654"),
        (20, "3.1415926535897932385"),
    ],
)
def test_compute_pi_exact_strings(digits, expected):
    assert compute_pi(digits) == expected
