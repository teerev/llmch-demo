from hangman.game import HangmanGame
import pytest


def test_guessing_and_mask_updates():
    g = HangmanGame('aba', max_misses=2)
    assert g.guess('a') is True
    assert g.masked_word() == 'a_a'
    assert g.guess('z') is False
    assert g.missed_guesses == {'z'}


def test_win_and_loss_states():
    g = HangmanGame('ab', max_misses=1)
    assert g.guess('a') is True
    assert g.guess('b') is True
    assert g.is_won() is True
    g2 = HangmanGame('ab', max_misses=1)
    assert g2.guess('z') is False
    assert g2.is_lost() is True


def test_repeated_guess_and_invalid_guess():
    g = HangmanGame('ab')
    assert g.guess('a') is True
    assert g.guess('a') is False
    with pytest.raises(ValueError):
        g.guess('1')
