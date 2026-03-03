from __future__ import annotations

import argparse
from typing import Callable, Iterable, Optional

from .game import GameState, guess_letter, is_lost, is_won, new_game, render_progress


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hangman", description="Play hangman in your terminal")
    parser.add_argument("--word", default="python", help="Word to guess (default: python)")
    parser.add_argument(
        "--max-wrong",
        default=6,
        type=int,
        help="Maximum number of wrong guesses allowed (default: 6)",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def play_interactive(
    word: str,
    max_wrong: int,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> GameState:
    state = new_game(word=word, max_wrong=max_wrong)

    while not is_won(state) and not is_lost(state):
        output_fn(f"Word: {render_progress(state)}")
        remaining = state.max_wrong - state.wrong_guesses
        output_fn(f"Wrong guesses remaining: {remaining}")

        raw = input_fn("Guess a letter: ")
        guess = (raw or "").strip()

        if len(guess) != 1:
            output_fn("Please enter a single letter.")
            continue

        try:
            state = guess_letter(state, guess)
        except ValueError:
            output_fn("Please enter a single letter.")
            continue

    output_fn(f"Final: {render_progress(state)}")
    if is_won(state):
        output_fn("You won!")
    else:
        output_fn(f"You lost. The word was: {state.word}")

    return state


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    play_interactive(args.word, args.max_wrong)
    return 0
