"""Core functionality for the ascii_art package.

This module defines the stable, public interface for converting an image to
ASCII art.
"""

from __future__ import annotations

from ascii_art.pgm import read_pgm


_PALETTE = "@%#*+=-:. "  # dark to light


def _resize_nearest(
    src_w: int, src_h: int, src_pixels: list[int], dst_w: int
) -> tuple[int, int, list[int]]:
    """Resize to *dst_w* using nearest-neighbor scaling.

    Height is scaled to preserve aspect ratio.
    """
    if dst_w <= 0:
        raise ValueError("width must be a positive integer")

    if dst_w == src_w:
        return src_w, src_h, src_pixels

    # Preserve aspect ratio.
    dst_h = max(1, int(round(src_h * (dst_w / src_w))))

    dst_pixels: list[int] = [0] * (dst_w * dst_h)
    for y in range(dst_h):
        sy = min(src_h - 1, int(y * src_h / dst_h))
        for x in range(dst_w):
            sx = min(src_w - 1, int(x * src_w / dst_w))
            dst_pixels[y * dst_w + x] = src_pixels[sy * src_w + sx]

    return dst_w, dst_h, dst_pixels


def _pixel_to_char(v: int) -> str:
    # read_pgm does not rescale by maxval; sample uses 0..255.
    # Clamp to 0..255 and map to palette indices.
    v = 0 if v < 0 else 255 if v > 255 else v
    idx = int(v * (len(_PALETTE) - 1) / 255)
    return _PALETTE[idx]


def image_to_ascii(image_path: str, width: int) -> str:
    """Convert an image at *image_path* to an ASCII art string.

    Parameters
    ----------
    image_path:
        Path to the input image file.
    width:
        Target output width in characters.

    Returns
    -------
    str
        The rendered ASCII art.

    Notes
    -----
    - Reads P2 (ASCII) PGM via :func:`ascii_art.pgm.read_pgm`.
    - Optionally resizes to the requested width using nearest-neighbor scaling.
    - Maps pixels to characters using the fixed palette '@%#*+=-:. ' (dark to light).
    - Output is lines joined by '\n' with no trailing newline.
    """
    src_w, src_h, pixels = read_pgm(image_path)

    out_w, out_h, out_pixels = _resize_nearest(src_w, src_h, pixels, width)

    lines: list[str] = []
    for y in range(out_h):
        row = out_pixels[y * out_w : (y + 1) * out_w]
        lines.append("".join(_pixel_to_char(v) for v in row))

    return "\n".join(lines)
