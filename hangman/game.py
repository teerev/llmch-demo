from __future__ import annotations


def mask_word(secret_word: str, guessed_letters: set[str]) -> str:
    """Return a masked version of secret_word.

    Letters present in guessed_letters are revealed; all others are replaced
    with '_' (no spaces). Comparisons are done in lowercase.
    """
    secret_lower = secret_word.lower()
    guessed_lower = {ch.lower() for ch in guessed_letters}

    return "".join(ch if ch in guessed_lower else "_" for ch in secret_lower)


def is_word_guessed(secret_word: str, guessed_letters: set[str]) -> bool:
    """Return True only if every letter in secret_word is in guessed_letters.

    Comparisons are done in lowercase.
    """
    secret_lower = secret_word.lower()
    guessed_lower = {ch.lower() for ch in guessed_letters}

    return all(ch in guessed_lower for ch in secret_lower)


def apply_guess(
    secret_word: str, guessed_letters: set[str], guess: str
) -> tuple[set[str], bool]:
    """Apply a guess to the game state.

    Returns:
      (new_guessed_letters, is_correct)

    - Does not mutate the input guessed_letters set.
    - Uses lowercase comparisons (secret_word and guess are lowered internally).
    """
    secret_lower = secret_word.lower()
    guess_lower = guess.lower()

    new_guessed = set(guessed_letters)
    new_guessed.add(guess_lower)

    return new_guessed, (guess_lower in secret_lower)
