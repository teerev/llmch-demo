import pytest

from hangman.game import current_mask, guess, is_lost, is_won, new_game


def test_mask_updates_with_correct_guesses_and_preserves_state_immutability():
    state0 = new_game("apple", max_attempts=5)
    assert current_mask(state0) == "_____"

    state1 = guess(state0, "a")
    assert current_mask(state1) == "a____"
    # original state not mutated
    assert current_mask(state0) == "_____"

    state2 = guess(state1, "p")
    assert current_mask(state2) == "app__"


def test_win_detection_when_all_letters_guessed():
    state = new_game("aba", max_attempts=5)
    assert not is_won(state)

    state = guess(state, "a")
    assert not is_won(state)

    state = guess(state, "b")
    assert is_won(state)


def test_loss_detection_when_attempts_reach_zero_and_wrong_guess_decrements_once():
    state0 = new_game("hi", max_attempts=1)
    assert not is_lost(state0)

    state1 = guess(state0, "z")
    assert state1.remaining_attempts == 0
    assert is_lost(state1)

    # guessing the same wrong letter again should not decrement further
    state2 = guess(state1, "z")
    assert state2.remaining_attempts == 0
    assert is_lost(state2)
