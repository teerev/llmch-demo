from __future__ import annotations

from collections.abc import Callable

from hangman.game import current_mask, guess, is_lost, is_won, new_game
from hangman.words import choose_word


def play_game(
    input_fn: Callable[[], str],
    output_fn: Callable[[str], None],
    secret_word: str,
    max_attempts: int = 6,
) -> str:
    output_fn("Welcome to Hangman!")

    state = new_game(secret_word, max_attempts)

    while not is_won(state) and not is_lost(state):
        output_fn(
            f"Word: {current_mask(state)} Attempts left: {state.remaining_attempts}"
        )

        raw = input_fn()
        letter = (raw or "").strip().lower()
        if not letter:
            continue

        letter = letter[0]
        state = guess(state, letter)

    if is_won(state):
        output_fn(f"You won! The word was {secret_word}.")
        return "won"

    output_fn(f"You lost! The word was {secret_word}.")
    return "lost"


def main() -> None:
    secret_word = choose_word()
    play_game(input, print, secret_word, max_attempts=6)
