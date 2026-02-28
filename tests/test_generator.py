from __future__ import annotations

from collections import Counter

from countdown.core import GameState, NUMBER_POOL, generate_game


def test_generate_game_deterministic_same_seed():
    a = generate_game(seed=12345)
    b = generate_game(seed=12345)
    assert a == b


def test_generate_game_different_seeds_usually_different():
    a = generate_game(seed=1)
    b = generate_game(seed=2)
    # Not a strict guarantee in theory, but extremely unlikely to collide.
    assert a != b


def test_generate_game_returns_gamestate_and_shapes():
    state = generate_game(seed=0)
    assert isinstance(state, GameState)
    assert isinstance(state.numbers, list)
    assert len(state.numbers) == 6
    assert all(isinstance(n, int) for n in state.numbers)
    assert isinstance(state.target, int)


def test_generate_game_numbers_from_pool_multiset_respected():
    state = generate_game(seed=999)
    pool_counts = Counter(NUMBER_POOL)
    chosen_counts = Counter(state.numbers)
    for n, c in chosen_counts.items():
        assert c <= pool_counts[n]


def test_generate_game_target_range():
    state = generate_game(seed=42)
    assert 100 <= state.target <= 999
