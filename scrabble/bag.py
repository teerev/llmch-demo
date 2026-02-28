"""Tile bag implementation.

Provides a TileBag class that can draw random tiles from a fixed distribution.
"""

from __future__ import annotations

from collections.abc import Mapping
import random
from typing import Optional

from .constants import STANDARD_DISTRIBUTION


class TileBag:
    """A bag of Scrabble tiles that can be drawn at random.

    Parameters
    ----------
    distribution:
        Mapping of tile -> count. If None, uses STANDARD_DISTRIBUTION.
    rng:
        Random number generator. If None, uses random.Random().
    """

    def __init__(
        self,
        distribution: Optional[Mapping[str, int]] = None,
        rng: Optional[random.Random] = None,
    ) -> None:
        dist = STANDARD_DISTRIBUTION if distribution is None else distribution

        tiles: list[str] = []
        for tile, count in dist.items():
            if not isinstance(tile, str) or len(tile) != 1:
                raise ValueError("Tile keys must be single-character strings")
            if not isinstance(count, int) or count < 0:
                raise ValueError("Tile counts must be non-negative integers")
            tiles.extend([tile] * count)

        self._tiles = tiles
        self._rng = rng if rng is not None else random.Random()

    def remaining(self) -> int:
        """Return the number of tiles remaining in the bag."""

        return len(self._tiles)

    def draw(self, n: int) -> list[str]:
        """Draw n tiles uniformly at random without replacement.

        Raises
        ------
        ValueError
            If n is negative or exceeds the number of remaining tiles.
        """

        if not isinstance(n, int):
            raise TypeError("n must be an int")
        if n < 0:
            raise ValueError("n must be non-negative")
        if n > len(self._tiles):
            raise ValueError("Cannot draw more tiles than remain in the bag")
        if n == 0:
            return []

        drawn: list[str] = []
        for _ in range(n):
            idx = self._rng.randrange(len(self._tiles))
            drawn.append(self._tiles.pop(idx))
        return drawn
