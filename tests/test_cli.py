from __future__ import annotations

import subprocess
import sys


def test_cli_outputs_expected_value() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pi_calc", "--digits", "5"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "3.1416"
