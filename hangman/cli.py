"""Command-line interface for the hangman game.

This module provides a stable CLI surface and performs all I/O.
Core game logic lives in hangman.game.
"""

from __future__ import annotations

import argparse
import random
import sys
from typing import Sequence

from .game import guess, is_lost, is_won, new_game, progress_string


_DEFAULT_WORDS: list[str] = [
    "python",
    "hangman",
    "developer",
    "testing",
    "interface",
]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hangman")
    parser.add_argument(
        "--word",
        metavar="WORD",
        default=None,
        help="Target word to guess (if omitted, a random word is chosen).",
    )
    parser.add_argument(
        "--max-attempts",
        metavar="N",
        type=int,
        default=6,
        help="Maximum number of wrong guesses allowed (default: 6).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the hangman CLI.

    Args:
        argv: Optional argv sequence (excluding program name). If None, uses sys.argv[1:].

    Returns:
        Process exit code (0 for win, 1 for loss).
    """
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    word = args.word if args.word is not None else random.choice(_DEFAULT_WORDS)
    state = new_game(word=word, max_attempts=args.max_attempts)

    while not is_won(state) and not is_lost(state):
        remaining = state.max_attempts - state.wrong_guesses
        print(progress_string(state))
        print(f"Remaining attempts: {remaining}")

        line = sys.stdin.readline()
        if line == "":
            # EOF: stop the game loop and treat as a loss if not already won.
            break

        letter = line.strip()
        state = guess(state, letter)

    if is_won(state):
        print("You win!")
        return 0

    print(f"You lose! The word was: {state.word}")
    return 1
