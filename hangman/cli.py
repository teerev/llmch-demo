from __future__ import annotations

import argparse
import random
from typing import Callable, Iterable, Optional

from . import game


_WORDS = [
    "python",
    "hangman",
    "terminal",
    "testing",
    "argparse",
]


def _parse_args(argv: Optional[Iterable[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hangman", description="Play hangman in the terminal")
    parser.add_argument("--word", help="Secret word to use (for testing)")
    parser.add_argument(
        "--max-incorrect",
        type=int,
        default=6,
        help="Maximum number of incorrect guesses before losing (default: 6)",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(
    argv: Optional[Iterable[str]] = None,
    input_fn: Callable[[], str] = input,
    output_fn: Callable[..., None] = print,
) -> int:
    """Terminal CLI entry point.

    Returns:
        0 on win, 1 on loss.
    """
    args = _parse_args(argv)

    secret_word = args.word if args.word else random.choice(_WORDS)
    state = game.new_game(secret_word=secret_word, max_incorrect=args.max_incorrect)

    output_fn("Welcome to Hangman!")

    while not game.is_won(state) and not game.is_lost(state):
        output_fn(f"Word: {game.display_word(state)}")
        output_fn(f"Incorrect guesses: {state.incorrect_guesses}/{state.max_incorrect}")
        output_fn("Guess a letter: ")

        # Important: input_fn is injectable and may be a zero-arg callable.
        letter = input_fn()

        try:
            state = game.guess(state, letter)
        except ValueError as e:
            output_fn(str(e))

    if game.is_won(state):
        output_fn("You won!")
        return 0

    output_fn(f"You lost! The word was {state.secret_word}.")
    return 1
