"""Command-line interface for the ascii_art package.

This module defines the stable CLI entrypoint interface.
"""

from __future__ import annotations

import argparse
import sys

from ascii_art.core import image_to_ascii


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ascii_art")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input image (P2 PGM)",
    )
    parser.add_argument(
        "--width",
        required=True,
        type=int,
        help="Target output width in characters",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write ASCII art output (no extra newline)",
    )
    return parser


def main(args=None) -> int:
    """Run the ascii_art command-line interface.

    Parameters
    ----------
    args:
        Optional sequence of CLI arguments (excluding the program name).
        If None, arguments will be taken from sys.argv.

    Returns
    -------
    int
        Process exit code (0 for success, nonzero for failure).
    """
    parser = _build_parser()

    try:
        ns = parser.parse_args(args=args)
        art = image_to_ascii(ns.input, ns.width)

        if ns.output:
            with open(ns.output, "w", encoding="utf-8") as f:
                f.write(art)
        else:
            sys.stdout.write(art)

        return 0
    except SystemExit as e:
        # argparse uses SystemExit for parse errors; propagate its code.
        code = e.code
        if code is None:
            return 1
        if isinstance(code, int):
            return code
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1
