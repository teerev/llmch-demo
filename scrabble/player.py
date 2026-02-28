"""Player model.

Provides a Player class that manages a rack of tiles and score.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass
class Player:
    """A Scrabble player.

    Attributes
    ----------
    name:
        Player name.
    score:
        Player score.
    rack:
        List of single-character tile strings currently held by the player.
    """

    name: str
    score: int = 0
    rack: List[str] = field(default_factory=list)

    def draw_tiles(self, bag, n: int) -> list[str]:
        """Draw `n` tiles from `bag` and add them to the rack.

        Parameters
        ----------
        bag:
            An object providing a `draw(n: int) -> list[str]` method (e.g., TileBag).
        n:
            Number of tiles to draw.

        Returns
        -------
        list[str]
            The tiles drawn.
        """

        drawn = bag.draw(n)
        self.rack.extend(drawn)
        return drawn

    def has_tiles(self, letters: Iterable[str]) -> bool:
        """Return True if the rack contains all requested letters (with multiplicity)."""

        needed = Counter(letters)
        available = Counter(self.rack)
        for ch, count in needed.items():
            if available[ch] < count:
                return False
        return True

    def remove_tiles(self, letters: Iterable[str]) -> None:
        """Remove the given letters from the rack.

        Raises
        ------
        ValueError
            If the rack does not contain the requested letters.
        """

        if not self.has_tiles(letters):
            raise ValueError("Player does not have the required tiles")

        # Remove one-by-one to preserve rack as a list.
        for ch in letters:
            self.rack.remove(ch)
