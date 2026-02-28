import random

from hangman.words import WORDS, choose_word


def test_words_is_non_empty_list():
    assert isinstance(WORDS, list)
    assert len(WORDS) > 0
    assert all(isinstance(w, str) and w == w.lower() for w in WORDS)


def test_choose_word_returns_member_of_words():
    w = choose_word()
    assert w in WORDS


def test_choose_word_deterministic_with_seeded_rng():
    rng1 = random.Random(12345)
    rng2 = random.Random(12345)
    assert choose_word(rng1) == choose_word(rng2)
