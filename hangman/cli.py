"""Command-line interface for the hangman game.

This module provides a callable CLI game loop with injectable input/output
functions for testability, plus a simple main() entry point.
"""

from __future__ import annotations

from typing import Callable

from hangman.game import apply_guess, display_word, is_lost, is_won, new_game

# Deterministic word list (no randomness required by work order).
WORDS = [
    "python",
    "hangman",
    "testing",
]


def run_game(
    secret_word: str,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    max_attempts: int = 6,
) -> str:
    """Run a CLI hangman game loop.

    Args:
        secret_word: The word to guess.
        input_fn: Function used to read user input (injectable).
        output_fn: Function used to write output (injectable).
        max_attempts: Maximum incorrect attempts allowed.

    Returns:
        "won" if the player wins, otherwise "lost".
    """

    state = new_game(secret_word, max_attempts=max_attempts)

    while not is_won(state) and not is_lost(state):
        output_fn(f"Word: {display_word(state)}")
        output_fn(f"Guesses left: {state.remaining_attempts}")
        guess = input_fn("Guess a letter: ")
        state = apply_guess(state, guess)

    if is_won(state):
        output_fn("You won!")
        return "won"

    output_fn(f"You lost! Word was: {secret_word}")
    return "lost"


def main() -> None:
    """CLI entry point."""

    secret_word = WORDS[0]
    run_game(secret_word)
