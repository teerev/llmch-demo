import pytest

from scrabble.board import Board
from scrabble.constants import LETTER_SCORES


def test_place_word_horizontal_and_get_cell():
    b = Board(size=5)
    score = b.place_word("CAT", 0, 0, "H")
    assert score == LETTER_SCORES["C"] + LETTER_SCORES["A"] + LETTER_SCORES["T"]
    assert b.get_cell(0, 0) == "C"
    assert b.get_cell(0, 1) == "A"
    assert b.get_cell(0, 2) == "T"
    assert b.get_cell(0, 3) is None


def test_place_word_vertical():
    b = Board(size=5)
    b.place_word("DOG", 1, 2, "V")
    assert b.get_cell(1, 2) == "D"
    assert b.get_cell(2, 2) == "O"
    assert b.get_cell(3, 2) == "G"


def test_letters_needed_with_overlap_and_place():
    b = Board(size=7)
    b.place_word("HELLO", 0, 0, "H")

    # Place vertically through the existing 'L' at (0,2)
    needed = b.letters_needed("LID", 0, 2, "V")
    assert needed == ["I", "D"]

    score = b.place_word("LID", 0, 2, "V")
    assert score == LETTER_SCORES["L"] + LETTER_SCORES["I"] + LETTER_SCORES["D"]

    assert b.get_cell(0, 2) == "L"  # overlapped
    assert b.get_cell(1, 2) == "I"
    assert b.get_cell(2, 2) == "D"


def test_letters_needed_mismatch_raises_and_can_place_false():
    b = Board(size=5)
    b.place_word("CAT", 0, 0, "H")

    with pytest.raises(ValueError):
        b.letters_needed("CAR", 0, 0, "H")  # mismatch at last letter (T vs R)

    assert b.can_place_word("CAR", 0, 0, "H") is False


def test_out_of_bounds_raises_and_can_place_false():
    b = Board(size=5)
    with pytest.raises(ValueError):
        b.letters_needed("TOO", 0, 4, "H")
    assert b.can_place_word("TOO", 0, 4, "H") is False


def test_invalid_direction_raises():
    b = Board(size=5)
    with pytest.raises(ValueError):
        b.letters_needed("HI", 0, 0, "X")


def test_get_cell_out_of_bounds_raises():
    b = Board(size=5)
    with pytest.raises(ValueError):
        b.get_cell(-1, 0)
    with pytest.raises(ValueError):
        b.get_cell(0, 5)
