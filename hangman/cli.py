from __future__ import annotations

import random
import sys
from typing import Sequence

from .game import display, guess, is_won, new_game


_USAGE = "Usage: python -m hangman"


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint.

    - No args: run an interactive hangman game.
    - -h/--help: print usage and exit 0.
    - Any other args: print usage and exit 2.
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 1 and argv[0] in {"-h", "--help"}:
        print(_USAGE)
        return 0

    if len(argv) != 0:
        print(_USAGE)
        return 2

    words = [
        "python",
        "terminal",
        "hangman",
        "developer",
        "function",
        "package",
        "testing",
        "dataclass",
    ]
    word = random.choice(words)
    state = new_game(word)

    while True:
        print(display(state))

        if is_won(state):
            print("You win!")
            return 0

        if state.remaining <= 0:
            print(f"You lose! The word was {state.word}.")
            return 1

        try:
            letter = input("Guess a letter: ")
        except EOFError:
            # Treat EOF as a loss/quit.
            print(f"You lose! The word was {state.word}.")
            return 1

        try:
            state = guess(state, letter)
        except ValueError:
            print("Invalid guess")
            continue
