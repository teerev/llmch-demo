from __future__ import annotations

from pathlib import Path

from ascii_art.pgm import read_pgm


def test_read_pgm_sample_image() -> None:
    sample_path = Path(__file__).parent / "data" / "sample.pgm"
    w, h, pixels = read_pgm(str(sample_path))

    assert (w, h) == (3, 2)
    assert pixels == [0, 128, 255, 255, 128, 0]
