from __future__ import annotations

import argparse
import random
import sys
from typing import Iterable, Optional, TextIO

from hangman.cli import run_game

WORDS = ["python", "hangman", "terminal"]


def main(
    argv: Optional[Iterable[str]] = None,
    input_stream: Optional[TextIO] = None,
    output_stream: Optional[TextIO] = None,
) -> str:
    parser = argparse.ArgumentParser(prog="python -m hangman")
    parser.add_argument("--word", help="Secret word to use (optional)")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=6,
        help="Maximum number of incorrect attempts (default: 6)",
    )

    args = parser.parse_args(list(argv) if argv is not None else None)

    secret_word = args.word if args.word is not None else random.choice(WORDS)
    in_stream = input_stream if input_stream is not None else sys.stdin
    out_stream = output_stream if output_stream is not None else sys.stdout

    return run_game(in_stream, out_stream, secret_word=secret_word, max_attempts=args.max_attempts)


if __name__ == "__main__":
    raise SystemExit(0 if main() == "won" else 1)
