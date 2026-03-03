import io

from hangman.cli import run_game


def test_cli_win() -> None:
    input_stream = io.StringIO("h\ni\n")
    output_stream = io.StringIO()

    result = run_game(input_stream, output_stream, secret_word="hi")

    assert result is True
    assert "You win!" in output_stream.getvalue()


def test_cli_lose() -> None:
    input_stream = io.StringIO("b\nc\nd\ne\nf\ng\n")
    output_stream = io.StringIO()

    result = run_game(input_stream, output_stream, secret_word="a")

    assert result is False
    assert "You lose! Word was: a" in output_stream.getvalue()
