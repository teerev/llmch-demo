import pytest

from hangman.game import guess_letter, is_lost, is_won, masked_word, new_game


def test_masked_word_reveals_only_guessed_letters():
    state = new_game("Apple")
    assert masked_word(state) == "_____"

    state = guess_letter(state, "a")
    assert masked_word(state) == "a____"

    state = guess_letter(state, "P")  # case-insensitive
    assert masked_word(state) == "app__"

    state = guess_letter(state, "e")
    assert masked_word(state) == "app_e"


def test_incorrect_guess_decrements_remaining_attempts():
    state = new_game("abc", max_attempts=2)
    state2 = guess_letter(state, "z")
    assert state2.remaining_attempts == 1

    state3 = guess_letter(state2, "y")
    assert state3.remaining_attempts == 0

    # cannot go below 0
    state4 = guess_letter(state3, "x")
    assert state4.remaining_attempts == 0


def test_repeated_guess_has_no_penalty_and_returns_same_state():
    state = new_game("abc", max_attempts=2)
    state2 = guess_letter(state, "z")
    assert state2.remaining_attempts == 1

    state3 = guess_letter(state2, "z")
    assert state3 is state2
    assert state3.remaining_attempts == 1


def test_win_detection_when_all_unique_letters_guessed():
    state = new_game("letter")
    for ch in "letr":
        state = guess_letter(state, ch)
    assert is_won(state) is True
    assert masked_word(state) == "letter"


def test_loss_detection_when_attempts_reach_zero():
    state = new_game("a", max_attempts=1)
    assert is_lost(state) is False

    state = guess_letter(state, "z")
    assert state.remaining_attempts == 0
    assert is_lost(state) is True
