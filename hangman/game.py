from __future__ import annotations

from dataclasses import dataclass, replace

MAX_ATTEMPTS = 6


@dataclass(frozen=True)
class GameState:
    word: str
    guessed: set[str]
    remaining_attempts: int


def new_game(word: str, max_attempts: int = MAX_ATTEMPTS) -> GameState:
    """Create a new game state.

    The word is normalized to lowercase.
    """
    return GameState(word=word.lower(), guessed=set(), remaining_attempts=max_attempts)


def masked_word(state: GameState) -> str:
    """Return the masked word with spaces between characters.

    Example: word='cat', guessed={'c'} -> 'c _ _'
    """
    return " ".join((ch if ch in state.guessed else "_") for ch in state.word)


def apply_guess(state: GameState, letter: str) -> GameState:
    """Apply a single-letter guess and return a new state.

    - Guess is normalized to lowercase.
    - If already guessed, returns an unchanged copy.
    - Decrements remaining_attempts only when the guess is not in the word.
    """
    ltr = letter.lower()

    if ltr in state.guessed:
        return replace(state)

    new_guessed = set(state.guessed)
    new_guessed.add(ltr)

    remaining = state.remaining_attempts
    if ltr not in state.word:
        remaining -= 1

    return GameState(word=state.word, guessed=new_guessed, remaining_attempts=remaining)


def is_won(state: GameState) -> bool:
    """A game is won when all letters in the word have been guessed."""
    return all(ch in state.guessed for ch in state.word)


def is_lost(state: GameState) -> bool:
    """A game is lost when no attempts remain and it is not already won."""
    return state.remaining_attempts <= 0 and not is_won(state)
