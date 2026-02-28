import subprocess
import sys


def _run_cli(args):
    return subprocess.run(
        [sys.executable, "-m", "anagram_finder", *args],
        capture_output=True,
        text=True,
    )


def test_cli_prints_matching_anagrams():
    proc = _run_cli(["listen", "enlist", "google"])
    assert proc.returncode == 0
    assert proc.stdout.splitlines() == ["enlist"]


def test_cli_prints_nothing_when_no_matches():
    proc = _run_cli(["abc", "def"])
    assert proc.returncode == 0
    assert proc.stdout.splitlines() == []
