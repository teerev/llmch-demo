"""Core pi calculation utilities.

Implements compute_pi(digits) using the Chudnovsky series with decimal.Decimal.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, localcontext


def compute_pi(digits: int) -> str:
    """Return pi to the requested significant digits as a string.

    Args:
        digits: Number of significant digits to return.

    Returns:
        A string representation of pi rounded to the requested significant digits.
        For digits == 1: '3'
        For digits > 1: one digit before the decimal point and digits-1 after.

    Raises:
        ValueError: if digits < 1
    """

    if digits < 1:
        raise ValueError("digits must be >= 1")

    # Chudnovsky series adds ~14 digits of precision per term.
    n_terms = digits // 14 + 1

    with localcontext() as ctx:
        ctx.prec = digits + 10

        # Constants for Chudnovsky formula
        C = Decimal(426880) * Decimal(10005).sqrt()

        # Sum_{k=0..n_terms-1} ( (6k)! (13591409 + 545140134k) ) / ( (3k)! (k!)^3 (-640320)^(3k) )
        total = Decimal(0)
        for k in range(n_terms):
            k_dec = Decimal(k)

            # Use integer factorials for exactness, then convert to Decimal.
            six_k_fact = Decimal(_factorial(6 * k))
            three_k_fact = Decimal(_factorial(3 * k))
            k_fact = Decimal(_factorial(k))

            numerator = six_k_fact * (Decimal(13591409) + Decimal(545140134) * k_dec)
            denominator = three_k_fact * (k_fact ** 3) * (Decimal(-640320) ** (3 * k))
            total += numerator / denominator

        pi = C / total

        # Round to requested significant digits.
        if digits == 1:
            # Quantize to integer with HALF_UP.
            return str(pi.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

        quant = Decimal("1e-{}".format(digits - 1))
        rounded = pi.quantize(quant, rounding=ROUND_HALF_UP)

        # Ensure fixed-point formatting (no exponent) and correct number of decimals.
        return format(rounded, "f")


def _factorial(n: int) -> int:
    """Compute n! as an int."""
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
