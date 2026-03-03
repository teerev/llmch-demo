from __future__ import annotations

from typing import List, Tuple


def _tokenize_pgm_ascii(data: str) -> List[str]:
    """Tokenize PGM ASCII content, removing comments.

    PGM comments start with '#' and continue to end of line.
    """
    tokens: List[str] = []
    for line in data.splitlines():
        if "#" in line:
            line = line.split("#", 1)[0]
        line = line.strip()
        if not line:
            continue
        tokens.extend(line.split())
    return tokens


def read_pgm(path: str) -> Tuple[int, int, List[int]]:
    """Read a P2 (ASCII) PGM file.

    Returns:
        (width, height, pixels)

    Notes:
        - Supports only P2 (ASCII) PGM.
        - Pixels are returned as a flat list of ints in row-major order.
        - maxval is parsed but not used to rescale values.
    """
    with open(path, "r", encoding="ascii", errors="strict") as f:
        data = f.read()

    tokens = _tokenize_pgm_ascii(data)
    if not tokens:
        raise ValueError("Empty PGM file")

    magic = tokens[0]
    if magic != "P2":
        raise ValueError(f"Unsupported PGM format: {magic!r} (only 'P2' supported)")

    if len(tokens) < 4:
        raise ValueError("Invalid PGM header")

    try:
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])
    except ValueError as e:
        raise ValueError("Invalid PGM header values") from e

    if width <= 0 or height <= 0:
        raise ValueError("Invalid PGM dimensions")
    if maxval <= 0:
        raise ValueError("Invalid PGM maxval")

    expected = width * height
    pixel_tokens = tokens[4:]
    if len(pixel_tokens) < expected:
        raise ValueError(f"Not enough pixel data: expected {expected}, got {len(pixel_tokens)}")

    pixels: List[int] = []
    for i in range(expected):
        try:
            v = int(pixel_tokens[i])
        except ValueError as e:
            raise ValueError(f"Invalid pixel value at index {i}") from e
        if v < 0 or v > maxval:
            raise ValueError(f"Pixel value out of range at index {i}: {v} (maxval {maxval})")
        pixels.append(v)

    return width, height, pixels
