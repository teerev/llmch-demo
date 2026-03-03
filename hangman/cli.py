from __future__ import annotations

import random
import sys
from typing import TextIO

from hangman.game import is_word_guessed, mask_word


DEFAULT_WORDS: list[str] = [
    "python",
    "hangman",
    "terminal",
]


def run_game(
    input_stream: TextIO,
    output_stream: TextIO,
    secret_word: str | None = None,
    max_attempts: int = 6,
) -> bool:
    if secret_word is None:
        secret_word = random.choice(DEFAULT_WORDS)

    secret_word = secret_word.lower()

    guessed_letters: set[str] = set()
    attempts_left = max_attempts

    while attempts_left > 0 and not is_word_guessed(secret_word, guessed_letters):
        output_stream.write(mask_word(secret_word, guessed_letters) + "\n")
        output_stream.write(f"Attempts left: {attempts_left}\n")
        output_stream.write("Guess a letter: ")
        output_stream.flush()

        line = input_stream.readline()
        if line == "":
            break

        guess = line.strip().lower()
        if guess == "":
            continue

        guess = guess[0]

        if guess not in guessed_letters:
            guessed_letters.add(guess)
            if guess not in secret_word:
                attempts_left -= 1

    if is_word_guessed(secret_word, guessed_letters):
        output_stream.write("You win!\n")
        return True

    output_stream.write(f"You lose! Word was: {secret_word}\n")
    return False


def main() -> None:
    run_game(sys.stdin, sys.stdout)
    return None
