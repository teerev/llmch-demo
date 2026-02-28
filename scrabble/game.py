from __future__ import annotations

from .models import Board, GameState, Tile


def new_game() -> GameState:
    """Create a deterministic new game state.

    Returns a GameState with an empty Board and a fixed rack of seven tiles:
    letters A through G, each worth 1 point.
    """

    board = Board()
    rack = [Tile(letter=chr(ord("A") + i), points=1) for i in range(7)]
    return GameState(board=board, rack=rack)
