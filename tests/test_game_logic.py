import pytest

from hangman.game import apply_guess, is_word_guessed, mask_word


def test_mask_word_reveals_guessed_letters_no_spaces() -> None:
    assert mask_word("apple", {"a", "e"}) == "a___e"


def test_mask_word_is_case_insensitive() -> None:
    # secret_word and guessed letters should be compared in lowercase
    assert mask_word("ApPlE", {"A", "p"}) == "app__"


def test_is_word_guessed_true_only_when_all_letters_guessed() -> None:
    assert is_word_guessed("apple", {"a", "p", "l", "e"}) is True
    assert is_word_guessed("apple", {"a", "p", "l"}) is False


def test_is_word_guessed_is_case_insensitive() -> None:
    assert is_word_guessed("ApPlE", {"A", "P", "L", "E"}) is True


def test_apply_guess_returns_new_set_and_correctness_true() -> None:
    original = {"a"}
    new_set, correct = apply_guess("apple", original, "p")

    assert correct is True
    assert new_set == {"a", "p"}
    # must not mutate input
    assert original == {"a"}
    assert new_set is not original


def test_apply_guess_incorrect_guess_and_lowercasing() -> None:
    original = {"a"}
    new_set, correct = apply_guess("Apple", original, "Z")

    assert correct is False
    assert new_set == {"a", "z"}
    assert original == {"a"}


def test_apply_guess_does_not_duplicate_existing_guess() -> None:
    original = {"a", "p"}
    new_set, correct = apply_guess("apple", original, "P")

    assert correct is True
    assert new_set == {"a", "p"}
    assert original == {"a", "p"}
    assert new_set is not original
