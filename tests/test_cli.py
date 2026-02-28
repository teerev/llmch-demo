from __future__ import annotations

from typing import Callable, List, Tuple

from hangman import cli


def make_input_fn(inputs: List[str]) -> Callable[[str], str]:
    """Build an input function that returns successive values from `inputs`."""
    it = iter(inputs)

    def _input_fn(prompt: str = "") -> str:
        return next(it)

    return _input_fn


def make_output_capture() -> Tuple[Callable[..., None], List[str]]:
    """Build an output function that captures printed lines into a list."""
    out: List[str] = []

    def _output_fn(*args, **kwargs) -> None:
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        out.append(sep.join(str(a) for a in args) + end)

    return _output_fn, out


def test_cli_win() -> None:
    input_fn = make_input_fn(["c", "a", "t"])
    output_fn, out = make_output_capture()

    rc = cli.main(
        argv=["--word", "cat", "--max-attempts", "5"],
        input_fn=input_fn,
        output_fn=output_fn,
    )

    assert rc == 0
    combined = "".join(out)
    assert "You won!" in combined


def test_cli_loss() -> None:
    input_fn = make_input_fn(["x", "y"])
    output_fn, out = make_output_capture()

    rc = cli.main(
        argv=["--word", "hi", "--max-attempts", "2"],
        input_fn=input_fn,
        output_fn=output_fn,
    )

    assert rc == 1
    combined = "".join(out)
    assert "You lost!" in combined
    assert "hi" in combined
