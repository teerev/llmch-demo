from __future__ import annotations

from hangman.cli import parse_args, play_interactive
from hangman.game import is_won


def test_parse_args_defaults():
    args = parse_args([])
    assert args.word == "python"
    assert args.max_wrong == 6


def test_play_interactive_can_win_with_scripted_input():
    # Word has unique letters: p y t h o n
    inputs = iter(["p", "y", "t", "h", "o", "n"])

    def input_fn(prompt: str = "") -> str:
        return next(inputs)

    outputs: list[str] = []

    def output_fn(msg: str) -> None:
        outputs.append(msg)

    final_state = play_interactive("python", 6, input_fn=input_fn, output_fn=output_fn)
    assert is_won(final_state)
    assert final_state.wrong_guesses == 0
    assert any("You won" in line for line in outputs)
