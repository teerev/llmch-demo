import argparse
import random
from typing import Callable, Iterable, Optional, Sequence

from . import game, words


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="hangman")
    parser.add_argument(
        "--word",
        default=None,
        help="Word to guess (default: None; choose from word list)",
    )
    parser.add_argument(
        "--max-attempts",
        dest="max_attempts",
        type=int,
        default=6,
        help="Maximum number of incorrect attempts (default: 6)",
    )
    return parser


def _normalize_guess(raw: str) -> Optional[str]:
    """Normalize user input to a single lowercase letter.

    Returns the normalized letter, or None if invalid.
    """
    if raw is None:
        return None

    s = raw.strip().lower()
    if len(s) != 1:
        return None
    if not s.isalpha():
        return None
    return s


def main(
    argv: Optional[Sequence[str]] = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[..., None] = print,
    word_list: Optional[Iterable[str]] = None,
) -> int:
    """CLI entrypoint.

    Runs an interactive hangman session.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.word is not None:
        chosen_word = args.word
    elif word_list is not None:
        chosen_word = random.choice(list(word_list))
    else:
        chosen_word = random.choice(words.DEFAULT_WORDS)

    state = game.new_game(chosen_word, max_attempts=args.max_attempts)

    output_fn("Welcome to Hangman!")
    output_fn(f"Word: {game.masked_word(state)}")

    while True:
        raw = input_fn("Guess a letter: ")
        letter = _normalize_guess(raw)

        if letter is None:
            output_fn("Please enter a letter.")
            continue

        if letter in state.guessed:
            output_fn("Already guessed.")
            continue

        state = game.apply_guess(state, letter)
        output_fn(f"Word: {game.masked_word(state)}")

        if game.is_won(state):
            output_fn("You won!")
            return 0

        if game.is_lost(state):
            output_fn(f"You lost! The word was: {state.word}")
            return 1
