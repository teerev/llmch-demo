import subprocess
import sys


def test_cli_prints_expected_solution_simple_case() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "countdown",
            "--target",
            "3",
            "--numbers",
            "1,2",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == "(1+2)\n"
