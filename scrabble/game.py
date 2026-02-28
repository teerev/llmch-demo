"""Game orchestration.

Provides a Game class that coordinates players, a board, and a tile bag.

Responsibilities:
- Track whose turn it is
- Validate and apply moves
- Update player score and rack
- Draw replacement tiles up to RACK_SIZE
- Advance turns

This module intentionally does not implement challenge rules, dictionary
validation, cross-word scoring, or premium squares.
"""

from __future__ import annotations

from typing import List, Optional

from .bag import TileBag
from .board import Board, Direction
from .constants import RACK_SIZE
from .player import Player


class Game:
    """A Scrabble-like game controller."""

    def __init__(
        self,
        players: List[Player],
        bag: Optional[TileBag] = None,
        board: Optional[Board] = None,
    ) -> None:
        if not isinstance(players, list) or len(players) == 0:
            raise ValueError("players must be a non-empty list")
        if any(not isinstance(p, Player) for p in players):
            raise TypeError("players must contain Player instances")

        self.players: List[Player] = players
        self.bag: TileBag = bag if bag is not None else TileBag()
        self.board: Board = board if board is not None else Board()
        self._turn_index: int = 0

    @property
    def current_player(self) -> Player:
        return self.players[self._turn_index]

    def next_player(self) -> Player:
        """Advance to the next player's turn and return them."""

        self._turn_index = (self._turn_index + 1) % len(self.players)
        return self.current_player

    def apply_move(self, word: str, row: int, col: int, direction: Direction) -> int:
        """Apply a move for the current player.

        Steps:
        - Determine which letters must be placed (Board.letters_needed)
        - Verify the current player has those tiles
        - Place the word on the board (Board.place_word) and get score
        - Remove used tiles from rack
        - Add score to player
        - Draw replacement tiles up to RACK_SIZE if available
        - Advance turn

        Returns
        -------
        int
            The score for the placed word.

        Raises
        ------
        ValueError
            If placement is invalid or player lacks required tiles.
        """

        player = self.current_player

        needed = self.board.letters_needed(word, row, col, direction)
        if not player.has_tiles(needed):
            raise ValueError("Player does not have the required tiles")

        score = self.board.place_word(word, row, col, direction)

        # Update rack and score.
        player.remove_tiles(needed)
        player.score += score

        # Refill rack.
        if self.bag is not None:
            to_draw = max(0, RACK_SIZE - len(player.rack))
            if to_draw:
                # TileBag.draw raises if n > remaining; clamp to remaining.
                remaining = self.bag.remaining() if hasattr(self.bag, "remaining") else None
                if remaining is None:
                    # Best-effort: attempt to draw requested amount.
                    draw_n = to_draw
                else:
                    draw_n = min(to_draw, remaining)
                if draw_n:
                    player.draw_tiles(self.bag, draw_n)

        # Advance turn.
        self.next_player()
        return score
