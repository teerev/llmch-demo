from __future__ import annotations

from collections import Counter
import random
import pytest

from scrabble import STANDARD_DISTRIBUTION, TileBag


def test_remaining_starts_at_standard_total() -> None:
    bag = TileBag(rng=random.Random(0))
    assert bag.remaining() == sum(STANDARD_DISTRIBUTION.values())


def test_draw_reduces_remaining_and_preserves_counts() -> None:
    rng = random.Random(12345)
    bag = TileBag(rng=rng)

    n = 10
    drawn = bag.draw(n)

    assert len(drawn) == n
    assert bag.remaining() == sum(STANDARD_DISTRIBUTION.values()) - n

    drawn_counts = Counter(drawn)
    for tile, count in drawn_counts.items():
        assert count <= STANDARD_DISTRIBUTION[tile]


def test_draw_all_tiles_matches_distribution_counts() -> None:
    rng = random.Random(999)
    bag = TileBag(rng=rng)

    total = sum(STANDARD_DISTRIBUTION.values())
    drawn = bag.draw(total)

    assert bag.remaining() == 0
    assert Counter(drawn) == Counter(STANDARD_DISTRIBUTION)


def test_draw_too_many_raises_value_error() -> None:
    bag = TileBag(rng=random.Random(0))
    with pytest.raises(ValueError):
        bag.draw(bag.remaining() + 1)


def test_draw_zero_returns_empty_list_and_does_not_change_remaining() -> None:
    bag = TileBag(rng=random.Random(0))
    before = bag.remaining()
    assert bag.draw(0) == []
    assert bag.remaining() == before
