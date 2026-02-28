from __future__ import annotations

import argparse
import random
from typing import Sequence

from .game import guess_letter, is_lost, is_won, masked_word, new_game

DEFAULT_WORDS: list[str] = [
    "python",
    "hangman",
    "terminal",
    "testing",
    "argparse",
]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hangman", description="Play Hangman in the terminal.")
    parser.add_argument("--word", help="Word to guess (defaults to a random word).")
    parser.add_argument("--max-attempts", type=int, default=6, help="Maximum incorrect attempts (default: 6).")
    return parser


def main(args: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    ns = parser.parse_args(args=args)

    word = ns.word if ns.word is not None else random.choice(DEFAULT_WORDS)
    state = new_game(word=word, max_attempts=ns.max_attempts)

    print("Welcome to Hangman!")

    while not is_won(state) and not is_lost(state):
        print(f"Word: {masked_word(state)}")
        print(f"Remaining attempts: {state.remaining_attempts}")
        raw = input("Guess a letter: ")
        if raw:
            state = guess_letter(state, raw[:1].lower())

    if is_won(state):
        print(f"You won! The word was {state.word}.")
    else:
        print(f"You lost! The word was {state.word}.")

    return 0
