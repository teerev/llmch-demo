from __future__ import annotations

import argparse

from .core import compute_pi


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pi_calc", description="Compute pi to N significant digits")
    parser.add_argument("--digits", type=int, default=1000, help="Number of significant digits (default: 1000)")
    args = parser.parse_args(argv)

    print(compute_pi(args.digits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
