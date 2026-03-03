import subprocess


def run_cmd(args):
    return subprocess.run(
        args,
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
