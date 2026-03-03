"""Command-line interface for the ascii_art package.

This module defines the stable CLI entrypoint interface. Argument parsing and
behavior are intentionally not implemented yet.
"""

from __future__ import annotations


def main(args=None) -> int:
    """Run the ascii_art command-line interface.

    Parameters
    ----------
    args:
        Optional sequence of CLI arguments (excluding the program name).
        If None, arguments will be taken from sys.argv by a future
        implementation.

    Returns
    -------
    int
        Process exit code (0 for success).

    Notes
    -----
    This function's signature is considered part of the public API.
    The implementation will be added in a later change.
    """
    raise NotImplementedError("CLI main() is not implemented yet")
