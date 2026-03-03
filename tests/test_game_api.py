import pytest

from hangman.game import GameState, apply_guess, display_word, is_lost, is_won, new_game


def test_new_game_initializes_correctly_lowercases_and_sets_defaults():
    state = new_game("HeLLo", max_attempts=7)
    assert isinstance(state, GameState)
    assert state.secret_word == "hello"
    assert state.guessed == frozenset()
    assert state.remaining_attempts == 7


def test_new_game_handles_none_secret_word_as_empty_string():
    state = new_game(None, max_attempts=6)
    assert state.secret_word == ""
    assert state.guessed == frozenset()
    assert state.remaining_attempts == 6


def test_apply_guess_reveals_letters_and_normalizes_input():
    state = new_game("banana", max_attempts=6)

    # Guess with whitespace and uppercase; should normalize to 'a'
    state2 = apply_guess(state, "  A ")
    assert state2.guessed == frozenset({"a"})
    assert state2.remaining_attempts == 6

    # Display should reveal all occurrences of 'a'
    assert display_word(state2) == "_ a _ a _ a"


def test_apply_guess_does_not_penalize_repeat_guesses_and_state_unchanged():
    state = new_game("apple", max_attempts=6)
    state1 = apply_guess(state, "p")
    assert state1.remaining_attempts == 6
    assert "p" in state1.guessed

    # Repeat guess should not change guessed set or remaining attempts
    state2 = apply_guess(state1, "p")
    assert state2 is state1  # function returns same object when unchanged
    assert state2.remaining_attempts == 6
    assert state2.guessed == state1.guessed


def test_apply_guess_empty_input_does_not_change_state():
    state = new_game("test", max_attempts=6)
    state2 = apply_guess(state, "   ")
    assert state2 is state


def test_apply_guess_penalizes_incorrect_guesses_and_adds_to_guessed():
    state = new_game("apple", max_attempts=3)
    state2 = apply_guess(state, "z")

    assert state2.remaining_attempts == 2
    assert state2.guessed == frozenset({"z"})


def test_display_word_formats_with_single_spaces_and_underscores():
    state = new_game("abc", max_attempts=6)
    assert display_word(state) == "_ _ _"

    state = apply_guess(state, "a")
    assert display_word(state) == "a _ _"

    state = apply_guess(state, "c")
    assert display_word(state) == "a _ c"


def test_is_won_true_when_all_unique_letters_guessed_false_otherwise():
    state = new_game("banana", max_attempts=6)
    assert is_won(state) is False

    state = apply_guess(state, "b")
    assert is_won(state) is False

    state = apply_guess(state, "a")
    assert is_won(state) is False

    state = apply_guess(state, "n")
    assert is_won(state) is True


def test_is_lost_true_when_remaining_attempts_zero_or_below():
    state = new_game("a", max_attempts=1)
    assert is_lost(state) is False

    state = apply_guess(state, "z")
    assert state.remaining_attempts == 0
    assert is_lost(state) is True

    # Further incorrect guesses can take it below zero; still lost
    state2 = apply_guess(state, "y")
    assert state2.remaining_attempts == -1
    assert is_lost(state2) is True
