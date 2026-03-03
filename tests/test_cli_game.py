import pytest

from hangman.cli import run_game


def test_run_game_can_be_driven_to_win_with_injected_io():
    # Arrange: secret word and a controlled sequence of guesses that will win.
    guesses = iter(["a", "b"])
    outputs: list[str] = []

    def input_fn(prompt: str) -> str:
        return next(guesses)

    def output_fn(message: str) -> None:
        outputs.append(message)

    # Act
    result = run_game("ab", input_fn=input_fn, output_fn=output_fn, max_attempts=6)

    # Assert
    assert result == "won"
    assert "You won!" in outputs
