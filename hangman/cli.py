from __future__ import annotations

import argparse
import random
from typing import Sequence

from .game import apply_guess, display_progress, is_lost, is_won, new_game


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hangman", description="Play hangman in the terminal.")
    parser.add_argument("--word", help="Word to guess (defaults to a random internal word).")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=6,
        help="Maximum incorrect attempts allowed (default: 6).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    words = ["python", "hangman", "terminal", "guess"]
    word = args.word.lower() if args.word else random.choice(words)

    state = new_game(word=word, max_attempts=args.max_attempts)

    print("Welcome to Hangman!")

    while not is_won(state) and not is_lost(state):
        print()
        print(f"Word: {display_progress(state)}")
        print(f"Remaining attempts: {state.remaining_attempts}/{state.max_attempts}")

        guess = input("Guess a letter: ").strip()
        if not guess:
            print("Please enter a letter.")
            continue

        try:
            state = apply_guess(state, guess)
        except ValueError as e:
            print(str(e))
            continue

    print()
    print(f"Word: {display_progress(state)}")
    if is_won(state):
        print("You won!")
    else:
        print(f"You lost. The word was: {state.word}")

    return 0
