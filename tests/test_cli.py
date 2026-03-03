import io

from hangman.cli import run_game


def test_run_game_win_case():
    input_stream = io.StringIO("a\nb\n")
    output_stream = io.StringIO()

    result = run_game(input_stream, output_stream, secret_word="ab", max_attempts=3)

    assert result == "won"
    out = output_stream.getvalue()
    assert "You win! The word was ab." in out


def test_run_game_lose_case():
    input_stream = io.StringIO("x\ny\n")
    output_stream = io.StringIO()

    result = run_game(input_stream, output_stream, secret_word="a", max_attempts=2)

    assert result == "lost"
    out = output_stream.getvalue()
    assert "You lose! The word was a." in out
