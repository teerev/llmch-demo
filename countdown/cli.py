from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from .core import generate_game, solve_numbers


def _parse_numbers_csv(value: str) -> List[int]:
    s = value.strip()
    if not s:
        raise argparse.ArgumentTypeError("--numbers must be a non-empty comma-separated list")
    parts = [p.strip() for p in s.split(",")]
    try:
        nums = [int(p) for p in parts if p != ""]
    except ValueError as e:
        raise argparse.ArgumentTypeError("--numbers must contain only integers") from e
    if not nums:
        raise argparse.ArgumentTypeError("--numbers must contain at least one integer")
    return nums


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="countdown", description="Countdown numbers game CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="Generate a new game")
    p_gen.add_argument("--seed", type=int, default=None, help="Optional RNG seed")

    p_solve = sub.add_parser("solve", help="Solve a numbers+target instance")
    p_solve.add_argument("--numbers", type=_parse_numbers_csv, required=True, help="Comma-separated numbers")
    p_solve.add_argument("--target", type=int, required=True, help="Target integer")
    p_solve.add_argument(
        "--max-solutions",
        type=int,
        default=1,
        help="Maximum number of solutions to return (default: 1)",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        state = generate_game(seed=args.seed)
        payload = {"numbers": list(state.numbers), "target": int(state.target)}
        json.dump(payload, sys.stdout)
        sys.stdout.write("\n")
        return 0

    if args.command == "solve":
        solutions = solve_numbers(args.numbers, args.target, max_solutions=args.max_solutions)
        payload = {
            "numbers": list(args.numbers),
            "target": int(args.target),
            "solutions": list(solutions),
        }
        json.dump(payload, sys.stdout)
        sys.stdout.write("\n")
        return 0

    parser.error("Unknown command")
    return 2
