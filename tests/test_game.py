from hangman.game import guess, is_lost, is_won, new_game, progress_string


def test_progress_string_and_guess_rules():
    state = new_game("Abba", max_attempts=5)
    assert progress_string(state) == "____"

    # invalid guesses are no-ops
    assert guess(state, "") == state
    assert guess(state, "ab") == state
    assert guess(state, "1") == state
    assert guess(state, "-") == state

    # case-insensitive guessing
    state = guess(state, "a")
    assert progress_string(state) == "A__a"

    state = guess(state, "B")
    assert progress_string(state) == "Abba"


def test_win_detection():
    state = new_game("cat", max_attempts=3)
    assert not is_won(state)

    state = guess(state, "c")
    state = guess(state, "a")
    assert not is_won(state)

    state = guess(state, "t")
    assert is_won(state)
    assert not is_lost(state)


def test_lose_detection_and_no_double_penalty_for_repeat_guess():
    state = new_game("hi", max_attempts=2)

    state = guess(state, "x")
    assert state.wrong_guesses == 1
    assert not is_lost(state)

    # repeating the same wrong guess should not increment
    state2 = guess(state, "x")
    assert state2.wrong_guesses == 1

    state = guess(state, "y")
    assert state.wrong_guesses == 2
    assert is_lost(state)
    assert not is_won(state)
