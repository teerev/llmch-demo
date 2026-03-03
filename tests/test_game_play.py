import pytest

from hangman.game import (
    GameState,
    apply_guess,
    display_progress,
    is_lost,
    is_won,
    new_game,
)


def test_apply_guess_lowercases_and_adds_to_guessed() -> None:
    state = new_game("Apple", max_attempts=5)
    next_state = apply_guess(state, "A")

    assert next_state is not state
    assert next_state.word == "apple"
    assert "a" in next_state.guessed
    assert next_state.remaining_attempts == 5


@pytest.mark.parametrize("bad", ["", "ab", "1", "-", " ", "@"])
def test_apply_guess_validates_single_alpha_character(bad: str) -> None:
    state = new_game("test", max_attempts=3)
    with pytest.raises(ValueError):
        apply_guess(state, bad)


def test_apply_guess_already_guessed_returns_same_state_unchanged() -> None:
    state = new_game("banana", max_attempts=3)
    s1 = apply_guess(state, "b")
    s2 = apply_guess(s1, "B")

    assert s2 is s1
    assert s2.guessed == s1.guessed
    assert s2.remaining_attempts == s1.remaining_attempts


def test_apply_guess_wrong_letter_decrements_remaining_attempts_not_below_zero() -> None:
    state = new_game("hi", max_attempts=1)
    s1 = apply_guess(state, "z")
    assert s1.remaining_attempts == 0

    s2 = apply_guess(s1, "y")
    assert s2.remaining_attempts == 0


def test_display_progress_shows_guessed_letters_and_underscores_with_spaces() -> None:
    state = new_game("aba", max_attempts=5)
    assert display_progress(state) == "_ _ _"

    s1 = apply_guess(state, "a")
    assert display_progress(s1) == "a _ a"

    s2 = apply_guess(s1, "b")
    assert display_progress(s2) == "a b a"


def test_is_won_true_when_all_unique_letters_guessed() -> None:
    state = new_game("aba", max_attempts=5)
    assert is_won(state) is False

    s1 = apply_guess(state, "a")
    assert is_won(s1) is False

    s2 = apply_guess(s1, "b")
    assert is_won(s2) is True


def test_is_lost_true_when_remaining_attempts_zero_or_less() -> None:
    state = new_game("a", max_attempts=1)
    assert is_lost(state) is False

    s1 = apply_guess(state, "z")
    assert s1.remaining_attempts == 0
    assert is_lost(s1) is True


def test_apply_guess_does_not_mutate_original_state() -> None:
    state = new_game("abc", max_attempts=2)
    next_state = apply_guess(state, "a")

    assert isinstance(state, GameState)
    assert state.guessed == frozenset()
    assert state.remaining_attempts == 2

    assert next_state.guessed == frozenset({"a"})
    assert next_state.remaining_attempts == 2
