import pytest


def test_placeholder_import_and_main_callable():
    import hangman.cli

    assert callable(hangman.cli.main)


def test_new_game_lowercases_and_initializes_state():
    from hangman.game import new_game

    state = new_game("Apple", max_attempts=6)
    assert state.word == "apple"
    assert state.guessed == frozenset()
    assert state.remaining == 6


@pytest.mark.parametrize(
    "word",
    [
        "",
        "   ",
        "hello!",
        "two words",
        "abc123",
        "-",
    ],
)
def test_new_game_rejects_non_alpha_or_empty_word(word):
    from hangman.game import new_game

    with pytest.raises(ValueError):
        new_game(word)


@pytest.mark.parametrize("attempts", [0, -1])
def test_new_game_rejects_non_positive_max_attempts(attempts):
    from hangman.game import new_game

    with pytest.raises(ValueError):
        new_game("abc", max_attempts=attempts)


def test_guess_validates_single_alpha_letter():
    from hangman.game import new_game, guess

    state = new_game("abc")
    for bad in ["", "ab", "1", "!", " "]:
        with pytest.raises(ValueError):
            guess(state, bad)


def test_guess_is_case_insensitive_and_does_not_decrement_on_correct_guess():
    from hangman.game import new_game, guess

    state = new_game("apple", max_attempts=6)
    state2 = guess(state, "A")
    assert state2.remaining == 6
    assert "a" in state2.guessed


def test_guess_decrements_remaining_only_on_incorrect_guess():
    from hangman.game import new_game, guess

    state = new_game("apple", max_attempts=2)
    state2 = guess(state, "z")
    assert state2.remaining == 1
    assert "z" in state2.guessed

    state3 = guess(state2, "p")
    assert state3.remaining == 1
    assert "p" in state3.guessed


def test_guess_repeated_letter_returns_state_unchanged():
    from hangman.game import new_game, guess

    state = new_game("apple", max_attempts=2)
    state2 = guess(state, "z")
    state3 = guess(state2, "Z")

    assert state3 is state2


def test_display_shows_underscores_and_revealed_letters_with_spaces():
    from hangman.game import new_game, guess, display

    state = new_game("aba")
    assert display(state) == "_ _ _"

    state2 = guess(state, "a")
    assert display(state2) == "a _ a"


def test_is_won_true_when_all_unique_letters_guessed():
    from hangman.game import new_game, guess, is_won

    state = new_game("aba")
    assert is_won(state) is False

    state = guess(state, "a")
    assert is_won(state) is False

    state = guess(state, "b")
    assert is_won(state) is True
