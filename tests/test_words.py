from hangman.words import DEFAULT_WORDS, get_default_words


def test_default_words_non_empty_and_lowercase():
    assert DEFAULT_WORDS, "DEFAULT_WORDS must be non-empty"
    assert all(w == w.lower() for w in DEFAULT_WORDS), "All default words must be lowercase"


def test_get_default_words_returns_copy():
    words = get_default_words()
    assert words == DEFAULT_WORDS
    assert words is not DEFAULT_WORDS
