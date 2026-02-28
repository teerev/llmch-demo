import subprocess
import sys


def _run_cli(args, stdin_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "hangman", *args],
        input=stdin_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_win_message():
    # Word: "ab"; guesses: a then b => win
    proc = _run_cli(["--word", "ab", "--max-attempts", "6"], "a\nb\n")
    assert proc.returncode == 0
    assert "Welcome to Hangman!" in proc.stdout
    assert "You won! The word was ab." in proc.stdout


def test_cli_loss_message():
    # Word: "a"; max attempts 2; two wrong guesses => loss
    proc = _run_cli(["--word", "a", "--max-attempts", "2"], "b\nc\n")
    assert proc.returncode == 0
    assert "Welcome to Hangman!" in proc.stdout
    assert "You lost! The word was a." in proc.stdout
