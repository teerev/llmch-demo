from __future__ import annotations

import argparse
import sys
from typing import List, Optional, Sequence

from .solver import solve


def _parse_numbers(value: str) -> List[int]:
    parts = [p.strip() for p in value.split(",")]
    if any(p == "" for p in parts):
        raise argparse.ArgumentTypeError(
            "--numbers must be a comma-separated list of integers (e.g. 1,2,3)"
        )
    try:
        return [int(p) for p in parts]
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            "--numbers must be a comma-separated list of integers (e.g. 1,2,3)"
        ) from e


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="countdown",
        description="Solve the Countdown numbers game.",
    )
    parser.add_argument(
        "--target",
        required=True,
        type=int,
        help="Target number to reach.",
    )
    parser.add_argument(
        "--numbers",
        required=True,
        type=_parse_numbers,
        help="Comma-separated list of available numbers (e.g. 25,50,3,6,7,8).",
    )

    args = parser.parse_args(list(argv) if argv is not None else None)

    solutions = solve(args.target, args.numbers)
    if solutions:
        print(solutions[0])
    else:
        print("NO SOLUTION")

    return 0


if __name__ == "__main__":
    sys.exit(main())
