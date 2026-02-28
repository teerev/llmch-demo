import pytest

from hangman.cli import play_game


def test_play_game_win() -> None:
    inputs = ["a"]
    outputs: list[str] = []

    def input_fn() -> str:
        return inputs.pop(0)

    def output_fn(s: str) -> None:
        outputs.append(s)

    result = play_game(input_fn, output_fn, secret_word="a", max_attempts=6)

    assert result == "won"
    assert outputs[-1] == "You won! The word was a."


def test_play_game_loss() -> None:
    inputs = ["b"]
    outputs: list[str] = []

    def input_fn() -> str:
        return inputs.pop(0)

    def output_fn(s: str) -> None:
        outputs.append(s)

    result = play_game(input_fn, output_fn, secret_word="a", max_attempts=1)

    assert result == "lost"
    assert outputs[-1] == "You lost! The word was a."
