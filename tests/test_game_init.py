from hangman.game import HangmanGame


def test_game_initialization_and_mask():
    g = HangmanGame('Apple', max_misses=5)
    assert g.secret_word == 'apple'
    assert g.max_misses == 5
    assert g.correct_guesses == set()
    assert g.missed_guesses == set()
    assert g.masked_word() == '_____'
