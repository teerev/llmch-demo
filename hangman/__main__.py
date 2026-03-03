from __future__ import annotations

import argparse
import random
import sys

from .game import display_word, guess_letter, init_game, is_lost, is_won


_DEFAULT_WORDS = [
    "python",
    "hangman",
    "terminal",
    "argparse",
    "package",
    "testing",
]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hangman", description="Play Hangman in your terminal.")
    parser.add_argument(
        "--word",
        help="Explicit word to guess (optional). If omitted, a random word is chosen.",
        default=None,
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=6,
        help="Maximum number of incorrect attempts allowed (default: 6).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    word = args.word if args.word is not None else random.choice(_DEFAULT_WORDS)

    try:
        state = init_game(word=word, max_attempts=args.max_attempts)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if args.word is not None:
        print("Starting Hangman with the provided word.")
    else:
        print("Starting Hangman with a random word.")

    while not (is_won(state) or is_lost(state)):
        print(f"\nWord: {display_word(state)}")
        print(f"Remaining attempts: {state.remaining_attempts}")

        raw = input("Guess a letter: ").strip()
        if not raw:
            print("Please enter a single letter.")
            continue

        letter = raw[0]
        if len(raw) != 1:
            print("Please enter a single letter.")
            continue

        try:
            new_state = guess_letter(state, letter)
        except ValueError as e:
            print(f"Invalid guess: {e}")
            continue

        if new_state == state:
            print(f"You already guessed '{letter.lower()}'.")
        else:
            if letter.lower() in state.word:
                print("Correct!")
            else:
                print("Incorrect.")

        state = new_state

    print(f"\nFinal word: {state.word}")
    if is_won(state):
        print("You won!")
        return 0

    print("You lost!")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
