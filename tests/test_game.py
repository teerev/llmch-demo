import pytest

from scrabble import Game
from scrabble.board import Board
from scrabble.player import Player


class EmptyBag:
    def remaining(self) -> int:
        return 0

    def draw(self, n: int):
        assert n == 0
        return []


def test_apply_move_scores_updates_rack_and_advances_turn():
    p1 = Player("A", rack=list("CAT"))
    p2 = Player("B", rack=list("DOG"))

    game = Game([p1, p2], bag=EmptyBag(), board=Board())

    assert game.current_player is p1

    score = game.apply_move("CAT", 7, 7, "H")

    # C(3)+A(1)+T(1)=5
    assert score == 5
    assert p1.score == 5
    assert p1.rack == []  # empty bag, no refill

    # Turn advanced
    assert game.current_player is p2


def test_apply_move_requires_letters_needed_only():
    board = Board()
    # Pre-place 'A' at (7,7)
    board.place_word("A", 7, 7, "H")

    p1 = Player("A", rack=["C", "T"])  # does not have 'A'
    p2 = Player("B", rack=[])
    game = Game([p1, p2], bag=EmptyBag(), board=board)

    # Placing "CAT" starting at the existing 'A' should only need C and T.
    score = game.apply_move("CAT", 7, 6, "H")
    assert score == 5
    assert p1.score == 5
    assert p1.rack == []
    assert game.current_player is p2


def test_apply_move_raises_if_player_lacks_required_tiles_and_does_not_advance():
    p1 = Player("A", rack=["C", "A"])  # missing T
    p2 = Player("B", rack=[])
    game = Game([p1, p2], bag=EmptyBag(), board=Board())

    with pytest.raises(ValueError):
        game.apply_move("CAT", 7, 7, "H")

    assert p1.score == 0
    assert p1.rack == ["C", "A"]
    assert game.current_player is p1
