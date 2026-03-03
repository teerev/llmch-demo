from hangman.game import (
    guess_letter,
    is_lost,
    is_won,
    masked_word,
    new_game,
)


def test_correct_guess_reveals_letter_and_does_not_increment_wrong_attempts():
    state = new_game("cat", max_attempts=3)

    returned = guess_letter(state, "c")

    assert returned is state
    assert state.wrong_attempts == 0
    assert state.guessed_letters == {"c"}
    assert masked_word(state) == "c__"


def test_wrong_guess_increments_wrong_attempts_and_does_not_reveal_letters():
    state = new_game("cat", max_attempts=3)

    returned = guess_letter(state, "x")

    assert returned is state
    assert state.wrong_attempts == 1
    assert state.guessed_letters == {"x"}
    assert masked_word(state) == "___"


def test_repeated_wrong_guess_does_not_increment_wrong_attempts():
    state = new_game("cat", max_attempts=3)

    guess_letter(state, "x")
    guess_letter(state, "x")

    assert state.wrong_attempts == 1
    assert state.guessed_letters == {"x"}


def test_is_won_when_all_letters_guessed():
    state = new_game("ab", max_attempts=5)

    assert not is_won(state)
    guess_letter(state, "a")
    assert not is_won(state)
    guess_letter(state, "b")

    assert is_won(state)
    assert masked_word(state) == "ab"


def test_is_lost_when_wrong_attempts_reaches_max_attempts():
    state = new_game("a", max_attempts=2)

    assert not is_lost(state)
    guess_letter(state, "x")
    assert not is_lost(state)
    guess_letter(state, "y")

    assert is_lost(state)
