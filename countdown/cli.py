import argparse
import json
import random

from .generator import generate_numbers
from .solver import solve_numbers


def _parse_numbers_csv(value: str) -> list[int]:
    value = value.strip()
    if not value:
        return []
    parts = [p.strip() for p in value.split(",")]
    try:
        return [int(p) for p in parts if p != ""]
    except ValueError as e:
        raise argparse.ArgumentTypeError("--numbers must be a comma-separated list of ints") from e


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="countdown")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_gen = subparsers.add_parser("generate", help="Generate a numbers round")
    p_gen.add_argument("--count", type=int, default=6)
    p_gen.add_argument("--min", dest="min_value", type=int, default=1)
    p_gen.add_argument("--max", dest="max_value", type=int, default=10)
    p_gen.add_argument("--target-min", dest="target_min", type=int, default=100)
    p_gen.add_argument("--target-max", dest="target_max", type=int, default=999)
    p_gen.add_argument("--seed", type=int, default=None)

    p_solve = subparsers.add_parser("solve", help="Solve a numbers round")
    p_solve.add_argument("--numbers", required=True)
    p_solve.add_argument("--target", type=int, required=True)

    args = parser.parse_args(argv)

    if args.command == "generate":
        rng = random.Random(args.seed) if args.seed is not None else None
        result = generate_numbers(
            count=args.count,
            min_value=args.min_value,
            max_value=args.max_value,
            target_min=args.target_min,
            target_max=args.target_max,
            rng=rng,
        )
        print(json.dumps(result, sort_keys=True))
        return 0

    if args.command == "solve":
        numbers = _parse_numbers_csv(args.numbers)
        result = solve_numbers(numbers, args.target)
        if result is None:
            print("NO_SOLUTION")
        else:
            print(result)
        return 0

    # Should be unreachable due to required=True on subparsers.
    parser.error("No command provided")
    return 2
