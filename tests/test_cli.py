from __future__ import annotations

from hangman.cli import main


def test_cli_win_returns_0_and_prints_message() -> None:
    inputs = iter(["a", "b", "c"])
    out = []

    def input_fn() -> str:
        return next(inputs)

    def output_fn(*args, **kwargs) -> None:
        out.append(" ".join(str(a) for a in args))

    rc = main(["--word", "abc", "--max-incorrect", "6"], input_fn=input_fn, output_fn=output_fn)
    assert rc == 0
    assert any("You won!" in line for line in out)
