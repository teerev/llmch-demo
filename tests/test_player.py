import random

import pytest

from scrabble import Player, TileBag


def test_draw_tiles_adds_to_rack_and_returns_drawn_tiles():
    rng = random.Random(0)
    bag = TileBag(rng=rng)
    p = Player("Alice")

    before = bag.remaining()
    drawn = p.draw_tiles(bag, 7)

    assert isinstance(drawn, list)
    assert len(drawn) == 7
    assert p.rack == drawn
    assert bag.remaining() == before - 7


def test_has_tiles_respects_multiplicity():
    p = Player("Bob")
    p.rack = list("AABC")

    assert p.has_tiles("A") is True
    assert p.has_tiles("AA") is True
    assert p.has_tiles("AAA") is False
    assert p.has_tiles("AB") is True
    assert p.has_tiles("AD") is False


def test_remove_tiles_removes_requested_letters():
    p = Player("Cara")
    p.rack = list("AABC")

    p.remove_tiles("AA")
    assert sorted(p.rack) == sorted(list("BC"))

    p.remove_tiles(["B"])
    assert p.rack == ["C"]


def test_remove_tiles_raises_value_error_if_unavailable_and_does_not_mutate():
    p = Player("Dan")
    p.rack = list("ABC")

    before = p.rack.copy()
    with pytest.raises(ValueError):
        p.remove_tiles("AA")
    assert p.rack == before
