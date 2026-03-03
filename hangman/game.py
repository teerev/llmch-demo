"""Pure core hangman game logic.

This module defines an immutable game state and deterministic functions to
create a new game, apply guesses, and query/display state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import FrozenSet


@dataclass(frozen=True, slots=True)
class GameState:
    """Immutable hangman game state."""

    secret_word: str
    guessed: FrozenSet[str]
    remaining_attempts: int


def new_game(secret_word: str, max_attempts: int = 6) -> GameState:
    """Create a new game state.

    The secret word is lowercased. No guesses have been made.
    """

    return GameState(
        secret_word=(secret_word or "").lower(),
        guessed=frozenset(),
        remaining_attempts=int(max_attempts),
    )


def apply_guess(state: GameState, letter: str) -> GameState:
    """Apply a single-letter guess to the game state.

    Rules:
    - Input is stripped and lowercased.
    - If empty after stripping, state is unchanged.
    - If already guessed, state is unchanged (no penalty).
    - Otherwise, the letter is added to guessed.
      If the letter is not in the secret word, remaining_attempts is decremented.
    """

    normalized = (letter or "").strip().lower()
    if normalized == "":
        return state

    if normalized in state.guessed:
        return state

    new_guessed = frozenset(set(state.guessed) | {normalized})
    if normalized in state.secret_word:
        return replace(state, guessed=new_guessed)

    return replace(state, guessed=new_guessed, remaining_attempts=state.remaining_attempts - 1)


def display_word(state: GameState) -> str:
    """Return the display form of the secret word based on guesses.

    Each character is shown if guessed, otherwise '_', separated by single spaces.
    Example: 'a _ a'
    """

    return " ".join((ch if ch in state.guessed else "_") for ch in state.secret_word)


def is_won(state: GameState) -> bool:
    """Return True if all unique letters in the secret word have been guessed."""

    unique_letters = set(state.secret_word)
    return unique_letters.issubset(set(state.guessed))


def is_lost(state: GameState) -> bool:
    """Return True if no attempts remain."""

    return state.remaining_attempts <= 0
