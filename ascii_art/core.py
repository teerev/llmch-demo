"""Core functionality for the ascii_art package.

This module defines the stable, public interface for converting an image to
ASCII art. Behavior is intentionally not implemented yet.
"""

from __future__ import annotations


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
    This function's signature is considered part of the public API.
    The implementation will be added in a later change.
    """
    raise NotImplementedError("image_to_ascii() is not implemented yet")
