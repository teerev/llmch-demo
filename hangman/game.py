from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    word: str
    guessed_letters: frozenset[str]
    remaining_attempts: int


def new_game(word: str, max_attempts: int = 6) -> GameState:
    """Create a new game state.

    The word is normalized to lowercase and guessed_letters starts empty.
    """
    return GameState(word=str(word).lower(), guessed_letters=frozenset(), remaining_attempts=max_attempts)


def guess_letter(state: GameState, letter: str) -> GameState:
    """Apply a letter guess to the game state.

    Uses the first character of `letter` lowercased. If already guessed,
    returns the original state. Otherwise adds to guessed_letters and
    decrements remaining_attempts by 1 if the letter is not in the word
    (not below 0).
    """
    ch = (letter[:1].lower() if letter else "")
    if not ch:
        return state

    if ch in state.guessed_letters:
        return state

    new_guessed = frozenset(set(state.guessed_letters) | {ch})
    remaining = state.remaining_attempts
    if ch not in state.word:
        remaining = max(0, remaining - 1)

    return GameState(word=state.word, guessed_letters=new_guessed, remaining_attempts=remaining)


def masked_word(state: GameState) -> str:
    """Return the word with guessed letters revealed and '_' for others."""
    return "".join(c if c in state.guessed_letters else "_" for c in state.word)


def is_won(state: GameState) -> bool:
    """Return True if all unique letters in the word have been guessed."""
    return set(state.word) <= set(state.guessed_letters)


def is_lost(state: GameState) -> bool:
    """Return True if no attempts remain."""
    return state.remaining_attempts <= 0
