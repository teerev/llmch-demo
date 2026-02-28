import pytest

from scrabble.game import new_game
from scrabble.models import Board
from scrabble.render import render_board


def test_new_game_returns_rack_a_through_g() -> None:
    state = new_game()
    letters = [tile.letter for tile in state.rack]
    assert letters == list("ABCDEFG")


def test_render_board_empty_board_is_15x15_cells() -> None:
    output = render_board(Board())
    lines = output.splitlines()

    assert len(lines) == 15

    for line in lines:
        cells = line.split(" ")
        assert len(cells) == 15
