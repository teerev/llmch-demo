import subprocess


def run_cmd(args, stdin=None):
    return subprocess.run(
        args,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def test_help_output_unchanged():
    res = run_cmd(["bash", "hangman.sh", "--help"])
    assert res.returncode == 0
    expected = (
        "Usage: bash hangman.sh [--demo]\n\n"
        "Options:\n"
        "  --help   Show this help message and exit.\n"
    )
    assert res.stdout == expected


def test_demo_mode_transcript():
    res = run_cmd(["bash", "hangman.sh", "--demo"])
    assert res.returncode == 0

    out = res.stdout
    lines = out.splitlines()

    assert lines[0] == "Demo mode"
    assert "State: b a s h" in lines
    assert lines[-1] == "Result: win"


def test_interactive_win():
    # Guess all letters correctly.
    res = run_cmd(["bash", "hangman.sh"], stdin="b\na\ns\nh\n")
    assert res.returncode == 0

    lines = res.stdout.splitlines()
    assert lines[0] == "Word: _ _ _ _"
    assert lines[-1] == "Result: win"
    assert "Guess: b" in lines
    assert "State: b _ _ _" in lines
    assert "State: b a s h" in lines


def test_interactive_lose():
    # 6 wrong guesses should lose.
    res = run_cmd(["bash", "hangman.sh"], stdin="x\ny\nz\nq\nw\ne\n")
    assert res.returncode == 0

    lines = res.stdout.splitlines()
    assert lines[0] == "Word: _ _ _ _"
    assert lines[-1] == "Result: lose"

    # Ensure we printed a guess and state for each input line.
    assert sum(1 for l in lines if l.startswith("Guess: ")) == 6
    assert sum(1 for l in lines if l.startswith("State: ")) == 6
