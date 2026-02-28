"""Board model for Scrabble-like word placement.

Implements a simple grid that supports placing words horizontally or vertically
and scoring them using LETTER_SCORES (no multipliers).
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import BOARD_SIZE, LETTER_SCORES


Direction = str  # 'H' or 'V'


@dataclass
class _Step:
    dr: int
    dc: int


_STEPS: dict[Direction, _Step] = {
    "H": _Step(0, 1),
    "V": _Step(1, 0),
}


class Board:
    def __init__(self, size: int = BOARD_SIZE):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")
        self.size = size
        self._grid: list[list[str | None]] = [[None for _ in range(size)] for _ in range(size)]

    def get_cell(self, row: int, col: int) -> str | None:
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError("cell out of bounds")
        return self._grid[row][col]

    def _normalize_word(self, word: str) -> str:
        if not isinstance(word, str) or not word:
            raise ValueError("word must be a non-empty string")
        w = word.upper()
        for ch in w:
            if ch not in LETTER_SCORES:
                raise ValueError(f"invalid letter: {ch}")
        return w

    def _step_for(self, direction: Direction) -> _Step:
        if direction not in _STEPS:
            raise ValueError("direction must be 'H' or 'V'")
        return _STEPS[direction]

    def letters_needed(self, word: str, row: int, col: int, direction: Direction) -> list[str]:
        """Return letters that must be placed into empty cells.

        Raises ValueError if:
          - direction invalid
          - word contains invalid letters
          - placement goes out of bounds
          - any occupied cell mismatches the word letter
        """
        w = self._normalize_word(word)
        step = self._step_for(direction)

        end_row = row + step.dr * (len(w) - 1)
        end_col = col + step.dc * (len(w) - 1)
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError("start out of bounds")
        if not (0 <= end_row < self.size and 0 <= end_col < self.size):
            raise ValueError("word placement out of bounds")

        needed: list[str] = []
        r, c = row, col
        for ch in w:
            existing = self._grid[r][c]
            if existing is None:
                needed.append(ch)
            elif existing != ch:
                raise ValueError("letter mismatch with existing tile")
            r += step.dr
            c += step.dc
        return needed

    def can_place_word(self, word: str, row: int, col: int, direction: Direction) -> bool:
        try:
            self.letters_needed(word, row, col, direction)
            return True
        except ValueError:
            return False

    def place_word(self, word: str, row: int, col: int, direction: Direction) -> int:
        """Place a word on the board and return its total score.

        Score is the sum of LETTER_SCORES for all letters in the word.
        No multipliers or cross-word scoring is applied.
        """
        w = self._normalize_word(word)
        # Validate placement and mismatches first.
        self.letters_needed(w, row, col, direction)
        step = self._step_for(direction)

        r, c = row, col
        for ch in w:
            if self._grid[r][c] is None:
                self._grid[r][c] = ch
            r += step.dr
            c += step.dc

        return sum(LETTER_SCORES[ch] for ch in w)
