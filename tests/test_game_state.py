from hangman.game import new_game


def test_new_game_initializes_state() -> None:
    state = new_game("AbC", 3)

    assert state.word == "abc"
    assert state.guessed == frozenset()
    assert state.remaining_attempts == 3
    assert state.max_attempts == 3
