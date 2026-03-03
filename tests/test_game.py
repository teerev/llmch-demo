import pytest

from hangman.game import GameState, display_word, guess, is_lost, is_won, new_game


def test_new_game_initialization_defaults():
    state = new_game("apple")
    assert isinstance(state, GameState)
    assert state.secret_word == "apple"
    assert state.guessed_letters == frozenset()
    assert state.incorrect_guesses == 0
    assert state.max_incorrect == 6


def test_new_game_custom_max_incorrect():
    state = new_game("apple", max_incorrect=3)
    assert state.max_incorrect == 3


def test_correct_guess_adds_letter_and_does_not_increment_incorrect():
    state = new_game("apple")
    state2 = guess(state, "a")

    assert state2 is not state
    assert "a" in state2.guessed_letters
    assert state2.incorrect_guesses == 0


def test_incorrect_guess_increments_incorrect_and_adds_letter():
    state = new_game("apple")
    state2 = guess(state, "z")

    assert "z" in state2.guessed_letters
    assert state2.incorrect_guesses == 1


def test_repeat_guess_is_noop():
    state = new_game("apple")
    state2 = guess(state, "a")
    state3 = guess(state2, "a")

    assert state3 == state2


def test_display_word_shows_underscores_for_unguessed_letters():
    state = new_game("apple")
    assert display_word(state) == "_____"

    state = guess(state, "a")
    assert display_word(state) == "a____"

    state = guess(state, "p")
    assert display_word(state) == "app__"

    state = guess(state, "e")
    assert display_word(state) == "app_e"


def test_is_won_true_when_all_letters_guessed():
    state = new_game("ab")
    assert not is_won(state)

    state = guess(state, "a")
    assert not is_won(state)

    state = guess(state, "b")
    assert is_won(state)
    assert not is_lost(state)


def test_is_lost_true_when_incorrect_reaches_max():
    state = new_game("a", max_incorrect=2)
    assert not is_lost(state)

    state = guess(state, "x")
    assert state.incorrect_guesses == 1
    assert not is_lost(state)

    state = guess(state, "y")
    assert state.incorrect_guesses == 2
    assert is_lost(state)
    assert not is_won(state)


def test_guess_after_game_over_is_noop():
    state = new_game("a", max_incorrect=1)
    state = guess(state, "x")
    assert is_lost(state)

    state2 = guess(state, "a")
    assert state2 == state


def test_guess_validates_input():
    state = new_game("apple")

    with pytest.raises(ValueError):
        guess(state, "")
    with pytest.raises(ValueError):
        guess(state, "ab")
    with pytest.raises(ValueError):
        guess(state, "1")
    with pytest.raises(ValueError):
        guess(state, "-")
