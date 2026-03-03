from __future__ import annotations

from pathlib import Path

from ascii_art.core import image_to_ascii


def test_image_to_ascii_sample_width_3() -> None:
    sample = Path(__file__).parent / "data" / "sample.pgm"
    assert image_to_ascii(str(sample), width=3) == "@+ \n +@"
