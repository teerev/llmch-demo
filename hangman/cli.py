import argparse
from typing import Callable, Iterable, Optional, Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="hangman")
    parser.add_argument(
        "--word",
        default=None,
        help="Word to guess (default: None; choose from word list)",
    )
    parser.add_argument(
        "--max-attempts",
        dest="max_attempts",
        type=int,
        default=6,
        help="Maximum number of incorrect attempts (default: 6)",
    )
    return parser


def main(
    argv: Optional[Sequence[str]] = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[..., None] = print,
    word_list: Optional[Iterable[str]] = None,
) -> int:
    """CLI entrypoint.

    Currently a skeleton: parses args, prints a short message, and exits 0.
    """
    _ = input_fn  # reserved for future interactive gameplay
    _ = word_list

    parser = build_parser()
    args = parser.parse_args(argv)

    output_fn(
        f"hangman CLI skeleton (word={args.word!r}, max_attempts={args.max_attempts})"
    )
    return 0
