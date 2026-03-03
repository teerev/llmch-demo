import pytest

from hangman.game import display_word, guess_letter, init_game, is_lost, is_won


def test_correct_guess_reveals_letters_without_decrementing_attempts():
    state = init_game("apple", max_attempts=5)

    next_state = guess_letter(state, "p")

    assert next_state.remaining_attempts == 5
    assert display_word(next_state) == "_pp__"
    assert "p" in next_state.guessed_letters


def test_incorrect_guess_decrements_remaining_attempts():
    state = init_game("apple", max_attempts=3)

    next_state = guess_letter(state, "z")

    assert next_state.remaining_attempts == 2
    assert display_word(next_state) == "_____"
    assert "z" in next_state.guessed_letters


def test_is_won_becomes_true_when_all_letters_guessed():
    state = init_game("aba", max_attempts=5)

    state = guess_letter(state, "a")
    assert is_won(state) is False

    state = guess_letter(state, "b")
    assert display_word(state) == "aba"
    assert is_won(state) is True
    assert is_lost(state) is False


def test_is_lost_becomes_true_when_remaining_attempts_reaches_zero():
    state = init_game("a", max_attempts=1)

    state = guess_letter(state, "z")

    assert state.remaining_attempts == 0
    assert is_won(state) is False
    assert is_lost(state) is True
