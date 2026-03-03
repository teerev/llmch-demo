from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ascii_art", *args],
        text=True,
        capture_output=True,
    )


def test_cli_writes_to_stdout() -> None:
    sample = Path(__file__).parent / "data" / "sample.pgm"
    proc = _run_cli("--input", str(sample), "--width", "3")
    assert proc.returncode == 0
    assert proc.stderr == ""
    # Expected mapping for sample.pgm at width=3:
    # Row1: 0->'@', 128->'+', 255->' '
    # Row2: 255->' ', 128->'+', 0->'@'
    assert proc.stdout == "@+ \n +@"


def test_cli_writes_to_output_file(tmp_path: Path) -> None:
    sample = Path(__file__).parent / "data" / "sample.pgm"
    out_path = tmp_path / "out.txt"

    proc = _run_cli(
        "--input",
        str(sample),
        "--width",
        "3",
        "--output",
        str(out_path),
    )
    assert proc.returncode == 0
    assert proc.stderr == ""
    # When --output is provided, stdout should be empty.
    assert proc.stdout == ""

    assert out_path.read_text(encoding="utf-8") == "@+ \n +@"
