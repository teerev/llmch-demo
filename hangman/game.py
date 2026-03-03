from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    word: str
    guessed: frozenset[str]
    remaining_attempts: int
    max_attempts: int


def new_game(word: str, max_attempts: int) -> GameState:
    if not word:
        raise ValueError("word must be non-empty")
    if max_attempts <= 0:
        raise ValueError("max_attempts must be > 0")

    normalized_word = word.lower()
    return GameState(
        word=normalized_word,
        guessed=frozenset(),
        remaining_attempts=max_attempts,
        max_attempts=max_attempts,
    )


def apply_guess(state: GameState, letter: str) -> GameState:
    """Apply a single-letter guess to the game state.

    Rules:
    - Input is lowercased.
    - Must be a single alphabetic character, else ValueError.
    - Returns a NEW GameState (does not mutate).
    - If already guessed, returns the same state unchanged.
    - If not in word, remaining_attempts decreases by 1 but not below 0.
    """
    if not isinstance(letter, str):
        raise ValueError("letter must be a single alphabetic character")

    normalized = letter.lower()
    if len(normalized) != 1 or not normalized.isalpha():
        raise ValueError("letter must be a single alphabetic character")

    if normalized in state.guessed:
        return state

    new_guessed = frozenset(set(state.guessed) | {normalized})

    if normalized in state.word:
        return GameState(
            word=state.word,
            guessed=new_guessed,
            remaining_attempts=state.remaining_attempts,
            max_attempts=state.max_attempts,
        )

    new_remaining = max(0, state.remaining_attempts - 1)
    return GameState(
        word=state.word,
        guessed=new_guessed,
        remaining_attempts=new_remaining,
        max_attempts=state.max_attempts,
    )


def display_progress(state: GameState) -> str:
    """Return progress string like 'a _ a' for the current word/guesses."""
    chars = [(c if c in state.guessed else "_") for c in state.word]
    return " ".join(chars)


def is_won(state: GameState) -> bool:
    """True when all unique letters in the word have been guessed."""
    return set(state.word) <= set(state.guessed)


def is_lost(state: GameState) -> bool:
    """True when no attempts remain."""
    return state.remaining_attempts <= 0
