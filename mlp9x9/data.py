from __future__ import annotations

from typing import Iterable, List, Sequence, Union


Number = Union[int, float]


def flatten_image(image: Sequence[Sequence[Number]]) -> List[Number]:
    """Flatten a 9x9 nested sequence into a flat list of length 81 (row-major).

    Raises:
        ValueError: if the input is not exactly 9 rows of 9 elements each.
    """
    if image is None or not hasattr(image, "__len__"):
        raise ValueError("image must be a 9x9 nested sequence")

    if len(image) != 9:
        raise ValueError("image must have exactly 9 rows")

    flat: List[Number] = []
    for r, row in enumerate(image):
        if row is None or not hasattr(row, "__len__"):
            raise ValueError(f"row {r} must be a sequence of length 9")
        if len(row) != 9:
            raise ValueError("image must be 9x9")
        flat.extend(list(row))

    if len(flat) != 81:
        # Defensive: should not happen if checks above are correct.
        raise ValueError("flattened image must have length 81")

    return flat


def validate_flat_input(x: Iterable[Number]) -> List[float]:
    """Validate a flat input vector for a 9x9 image.

    Expects a flat sequence of length 81 with all values in [0, 1].

    Returns:
        A list of floats of length 81.

    Raises:
        ValueError: if length is not 81, values are not numeric, or any value is out of range.
    """
    if x is None:
        raise ValueError("x must be a flat sequence of length 81")

    try:
        values = list(x)
    except TypeError as e:
        raise ValueError("x must be an iterable") from e

    if len(values) != 81:
        raise ValueError("x must have length 81")

    out: List[float] = []
    for i, v in enumerate(values):
        try:
            fv = float(v)
        except (TypeError, ValueError) as e:
            raise ValueError(f"x[{i}] is not a number") from e
        if not (0.0 <= fv <= 1.0):
            raise ValueError(f"x[{i}] must be in [0, 1]")
        out.append(fv)

    return out
