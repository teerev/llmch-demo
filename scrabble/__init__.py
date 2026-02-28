"""Scrabble package.

Exposes core constants at the package root.
"""

from .constants import BOARD_SIZE, RACK_SIZE, LETTER_SCORES, STANDARD_DISTRIBUTION
from .board import Board
from .bag import TileBag

__all__ = [
    "BOARD_SIZE",
    "RACK_SIZE",
    "LETTER_SCORES",
    "STANDARD_DISTRIBUTION",
    "Board",
    "TileBag",
]
