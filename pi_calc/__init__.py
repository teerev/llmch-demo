"""pi_calc package.

Public API:
- compute_pi(digits): return pi to the requested significant digits as a string.
"""

from .core import compute_pi

__all__ = ["compute_pi"]
