import pytest

from hangman.game import (
    MAX_ATTEMPTS,
    apply_guess,
    is_lost,
    is_won,
    masked_word,
    new_game,
)


def test_new_game_normalizes_word_and_initial_state():
    state = new_game("CaT")
    assert state.word == "cat"
    assert state.guessed == set()
    assert state.remaining_attempts == MAX_ATTEMPTS


def test_masked_word_spacing_and_reveal():
    state = new_game("cat")
    assert masked_word(state) == "_ _ _"

    state2 = apply_guess(state, "c")
    assert masked_word(state2) == "c _ _"


def test_apply_guess_correct_does_not_decrement_and_is_immutable():
    state = new_game("cat", max_attempts=3)
    state2 = apply_guess(state, "C")

    assert state.word == "cat"
    assert state.guessed == set()
    assert state.remaining_attempts == 3

    assert state2.guessed == {"c"}
    assert state2.remaining_attempts == 3


def test_apply_guess_incorrect_decrements():
    state = new_game("cat", max_attempts=3)
    state2 = apply_guess(state, "x")
    assert state2.guessed == {"x"}
    assert state2.remaining_attempts == 2


def test_apply_guess_repeated_guess_no_change():
    state = new_game("cat", max_attempts=3)
    state2 = apply_guess(state, "x")
    state3 = apply_guess(state2, "X")

    assert state3.guessed == {"x"}
    assert state3.remaining_attempts == 2


def test_win_detection():
    state = new_game("aba", max_attempts=6)
    state = apply_guess(state, "a")
    assert is_won(state) is False
    assert is_lost(state) is False

    state = apply_guess(state, "b")
    assert is_won(state) is True
    assert is_lost(state) is False


def test_loss_detection():
    state = new_game("a", max_attempts=2)
    state = apply_guess(state, "x")
    assert is_lost(state) is False

    state = apply_guess(state, "y")
    assert state.remaining_attempts == 0
    assert is_won(state) is False
    assert is_lost(state) is True


def test_not_lost_if_won_even_when_attempts_zero():
    # Ensure is_lost is not true for a won game even if attempts are 0.
    state = new_game("a", max_attempts=1)
    state = apply_guess(state, "a")
    assert is_won(state) is True
    assert is_lost(state) is False
