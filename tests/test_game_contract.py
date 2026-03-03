import pytest

from hangman.game import (
    GameState,
    guess_letter,
    is_lost,
    is_won,
    new_game,
    render_progress,
)


def test_new_game_lowercases_word_and_initializes_state() -> None:
    s = new_game("PyThOn", max_wrong=7)
    assert isinstance(s, GameState)
    assert s.word == "python"
    assert s.guessed == frozenset()
    assert s.wrong_guesses == 0
    assert s.max_wrong == 7


def test_guess_letter_requires_length_1() -> None:
    s = new_game("abc")
    with pytest.raises(ValueError):
        guess_letter(s, "")
    with pytest.raises(ValueError):
        guess_letter(s, "ab")


def test_guess_letter_lowercases_and_adds_to_guessed_when_correct() -> None:
    s = new_game("apple")
    s2 = guess_letter(s, "A")
    assert s2.guessed == frozenset({"a"})
    assert s2.wrong_guesses == 0


def test_guess_letter_increments_wrong_guesses_when_incorrect() -> None:
    s = new_game("apple", max_wrong=6)
    s2 = guess_letter(s, "z")
    assert s2.guessed == frozenset({"z"})
    assert s2.wrong_guesses == 1


def test_guess_letter_is_idempotent_for_already_guessed_letter() -> None:
    s = new_game("apple")
    s2 = guess_letter(s, "a")
    s3 = guess_letter(s2, "A")
    assert s3 is s2


def test_is_won_all_unique_letters_in_word_guessed() -> None:
    s = new_game("letter")
    for ch in ["l", "e", "t", "r"]:
        s = guess_letter(s, ch)
    assert is_won(s) is True


def test_is_lost_when_wrong_guesses_reaches_max_wrong() -> None:
    s = new_game("a", max_wrong=2)
    s = guess_letter(s, "x")
    assert is_lost(s) is False
    s = guess_letter(s, "y")
    assert is_lost(s) is True


def test_render_progress_shows_underscores_and_letters_with_spaces() -> None:
    s = new_game("dog")
    assert render_progress(s) == "_ _ _"
    s = guess_letter(s, "d")
    assert render_progress(s) == "d _ _"
    s = guess_letter(s, "g")
    assert render_progress(s) == "d _ g"
